"""Deterministic SHA-256 helpers for records, schemas, and Spark batches."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping, Sequence

from blockchain_pipeline.canonicalization import canonicalize_record


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def compute_row_hash(
    record: Mapping[str, Any],
    ordered_columns: Sequence[str],
    data_types: Mapping[str, Any] | None = None,
) -> str:
    """Return the SHA-256 hash of a canonicalized record."""
    canonical_record = canonicalize_record(
        record=record,
        ordered_columns=ordered_columns,
        data_types=data_types,
    )
    return _sha256(canonical_record)


def compute_schema_hash(schema: Any) -> str:
    """Return a deterministic SHA-256 hash for a Spark or JSON-like schema."""
    schema_value = schema.jsonValue() if hasattr(schema, "jsonValue") else schema
    try:
        canonical_schema = json.dumps(
            schema_value,
            ensure_ascii=True,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as exc:
        raise TypeError("schema must be JSON serializable") from exc
    return _sha256(canonical_schema)


def compute_batch_hash(
    dataframe: Any,
    ordered_columns: Sequence[str],
    sort_columns: Sequence[str] | None = None,
) -> str:
    """Return a partition-independent SHA-256 hash for a Spark DataFrame.

    The implementation performs a deterministic global sort and streams rows
    through ``toLocalIterator``. It avoids ``collect`` and does not hold the
    complete batch in driver memory, but the global sort and sequential digest
    remain an MVP limitation for very large datasets.
    """
    if not ordered_columns:
        raise ValueError("ordered_columns must not be empty")

    dataframe_columns = set(dataframe.columns)
    missing_columns = sorted(set(ordered_columns) - dataframe_columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    requested_sort_columns = list(sort_columns or ())
    invalid_sort_columns = sorted(
        set(requested_sort_columns) - set(ordered_columns)
    )
    if invalid_sort_columns:
        raise ValueError(
            "sort_columns must be included in ordered_columns: "
            + ", ".join(invalid_sort_columns)
        )

    total_order = list(
        dict.fromkeys([*requested_sort_columns, *ordered_columns])
    )
    selected = dataframe.select(*ordered_columns).orderBy(*total_order)
    data_types = {
        field.name: field.dataType
        for field in selected.schema.fields
        if field.name in ordered_columns
    }

    digest = hashlib.sha256()
    for row in selected.toLocalIterator():
        row_hash = compute_row_hash(
            record=row.asDict(recursive=True),
            ordered_columns=ordered_columns,
            data_types=data_types,
        )
        digest.update(row_hash.encode("ascii"))
    return digest.hexdigest()
