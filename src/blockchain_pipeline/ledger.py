"""Blockchain-style verification ledger helpers."""

from __future__ import annotations

import hashlib
import json
import logging
from datetime import date, datetime, timezone
from decimal import Decimal
from typing import Any, Mapping, Sequence
from uuid import uuid4

from blockchain_pipeline.models import (
    BLOCK_PAYLOAD_COLUMNS,
    GENESIS_PREVIOUS_HASH,
    PIPELINE_STAGES,
    LedgerBlock,
)

LOGGER = logging.getLogger(__name__)
NULL_TOKEN = "<NULL>"
FIELD_DELIMITER = "|"
ESCAPE_CHARACTER = "\\"


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _escape_string(value: str) -> str:
    escaped = (
        value.replace(ESCAPE_CHARACTER, ESCAPE_CHARACTER * 2)
        .replace(FIELD_DELIMITER, ESCAPE_CHARACTER + FIELD_DELIMITER)
        .replace("\r", r"\r")
        .replace("\n", r"\n")
    )
    return ESCAPE_CHARACTER + escaped if value == NULL_TOKEN else escaped


def canonicalize_ledger_value(value: Any) -> str:
    """Return a deterministic string representation for ledger payload values."""
    if value is None:
        return NULL_TOKEN
    if isinstance(value, datetime):
        timestamp = value
        if timestamp.tzinfo is None:
            timestamp = timestamp.replace(tzinfo=timezone.utc)
        else:
            timestamp = timestamp.astimezone(timezone.utc)
        return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return format(value, "f")
    if isinstance(value, bool):
        return "true" if value else "false"
    return _escape_string(str(value))


def canonicalize_block_payload(payload: Mapping[str, Any]) -> str:
    """Canonicalize the ordered block payload used for block_hash."""
    missing_columns = [
        column for column in BLOCK_PAYLOAD_COLUMNS if column not in payload
    ]
    if missing_columns:
        raise ValueError(f"Missing payload columns: {', '.join(missing_columns)}")
    return FIELD_DELIMITER.join(
        canonicalize_ledger_value(payload[column])
        for column in BLOCK_PAYLOAD_COLUMNS
    )


def compute_block_hash(payload: Mapping[str, Any]) -> str:
    """Compute a SHA-256 block hash from a canonicalized payload."""
    return _sha256(canonicalize_block_payload(payload))


def compute_schema_hash(schema: Any) -> str:
    """Compute a deterministic SHA-256 hash for a Spark or JSON-like schema."""
    schema_value = schema.jsonValue() if hasattr(schema, "jsonValue") else schema
    canonical_schema = json.dumps(
        schema_value,
        ensure_ascii=True,
        separators=(",", ":"),
        sort_keys=True,
    )
    return _sha256(canonical_schema)


def _canonicalize_row_value(value: Any) -> str:
    return canonicalize_ledger_value(value)


def compute_dataframe_batch_hash(
    dataframe: Any,
    ordered_columns: Sequence[str] | None = None,
    sort_columns: Sequence[str] | None = None,
) -> str:
    """Compute a deterministic table hash without collecting all rows at once.

    This MVP implementation globally sorts the selected rows and streams them
    through ``toLocalIterator``. It avoids ``collect()``, but the global sort and
    single digest stream are still intended for demo-scale data.
    """
    columns = list(ordered_columns or dataframe.columns)
    if not columns:
        raise ValueError("ordered_columns must not be empty")

    dataframe_columns = set(dataframe.columns)
    missing_columns = sorted(set(columns) - dataframe_columns)
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    requested_sort_columns = list(sort_columns or columns)
    missing_sort_columns = sorted(set(requested_sort_columns) - dataframe_columns)
    if missing_sort_columns:
        raise ValueError(
            f"Missing sort columns: {', '.join(missing_sort_columns)}"
        )

    selected = dataframe.select(*columns)
    ordered = selected.orderBy(
        *list(dict.fromkeys([*requested_sort_columns, *columns]))
    )

    digest = hashlib.sha256()
    for row in ordered.toLocalIterator():
        canonical_row = FIELD_DELIMITER.join(
            _canonicalize_row_value(row[column]) for column in columns
        )
        digest.update(_sha256(canonical_row).encode("ascii"))
    return digest.hexdigest()


def create_ledger_block(
    *,
    block_index: int,
    pipeline_run_id: str,
    pipeline_stage: str,
    source_table: str,
    target_table: str,
    record_count: int,
    batch_hash: str,
    previous_hash: str,
    transformation: str,
    schema_hash: str,
    created_at: datetime,
    block_id: str | None = None,
) -> LedgerBlock:
    """Create a ledger block and calculate block_hash from its payload."""
    if pipeline_stage not in PIPELINE_STAGES:
        raise ValueError(f"Unsupported pipeline_stage: {pipeline_stage}")
    if block_index < 0:
        raise ValueError("block_index must be non-negative")
    if record_count < 0:
        raise ValueError("record_count must be non-negative")
    if not previous_hash or len(previous_hash) != 64:
        raise ValueError("previous_hash must be a 64-character hash")

    payload = {
        "block_index": block_index,
        "block_id": block_id or str(uuid4()),
        "pipeline_run_id": pipeline_run_id,
        "pipeline_stage": pipeline_stage,
        "source_table": source_table,
        "target_table": target_table,
        "record_count": record_count,
        "batch_hash": batch_hash,
        "previous_hash": previous_hash,
        "transformation": transformation,
        "schema_hash": schema_hash,
        "created_at": created_at,
    }
    return LedgerBlock(
        **payload,
        block_hash=compute_block_hash(payload),
    )


def create_stage_block(
    *,
    pipeline_run_id: str,
    pipeline_stage: str,
    source_table: str,
    target_table: str,
    record_count: int,
    batch_hash: str,
    transformation: str,
    schema_hash: str,
    created_at: datetime,
    previous_block: LedgerBlock | None = None,
    block_id: str | None = None,
) -> LedgerBlock:
    """Create the next stage block, using genesis previous_hash for SOURCE."""
    if previous_block is None:
        if pipeline_stage != "SOURCE":
            raise ValueError("Only SOURCE can be created without a previous block")
        block_index = 0
        previous_hash = GENESIS_PREVIOUS_HASH
    else:
        expected_stage = PIPELINE_STAGES[previous_block.block_index + 1]
        if pipeline_stage != expected_stage:
            raise ValueError(
                f"Expected next stage {expected_stage}, got {pipeline_stage}"
            )
        block_index = previous_block.block_index + 1
        previous_hash = previous_block.block_hash

    return create_ledger_block(
        block_index=block_index,
        pipeline_run_id=pipeline_run_id,
        pipeline_stage=pipeline_stage,
        source_table=source_table,
        target_table=target_table,
        record_count=record_count,
        batch_hash=batch_hash,
        previous_hash=previous_hash,
        transformation=transformation,
        schema_hash=schema_hash,
        created_at=created_at,
        block_id=block_id,
    )


def recalculate_block_hash(block: LedgerBlock) -> str:
    """Recalculate block_hash from the current block payload."""
    return compute_block_hash(block.payload())


def block_payload_is_unchanged(block: LedgerBlock) -> bool:
    """Return whether block_hash still matches the block payload."""
    return recalculate_block_hash(block) == block.block_hash


def create_block_for_dataframe(
    *,
    dataframe: Any,
    pipeline_run_id: str,
    pipeline_stage: str,
    source_table: str,
    target_table: str,
    transformation: str,
    created_at: datetime,
    previous_block: LedgerBlock | None = None,
    sort_columns: Sequence[str] | None = None,
) -> LedgerBlock:
    """Create a stage ledger block from a Spark DataFrame snapshot."""
    return create_stage_block(
        pipeline_run_id=pipeline_run_id,
        pipeline_stage=pipeline_stage,
        source_table=source_table,
        target_table=target_table,
        record_count=dataframe.count(),
        batch_hash=compute_dataframe_batch_hash(
            dataframe=dataframe,
            sort_columns=sort_columns,
        ),
        transformation=transformation,
        schema_hash=compute_schema_hash(dataframe.schema),
        created_at=created_at,
        previous_block=previous_block,
    )


def append_block(spark: Any, ledger_table: str, block: LedgerBlock) -> None:
    """Append one block to the managed Delta ledger table."""
    if not ledger_table.strip():
        raise ValueError("ledger_table must not be empty")
    LOGGER.info(
        "Appending ledger block stage=%s index=%s table=%s",
        block.pipeline_stage,
        block.block_index,
        ledger_table,
    )
    spark.createDataFrame([block.as_record()]).write.format("delta").mode(
        "append"
    ).saveAsTable(ledger_table)


def block_exists(spark: Any, ledger_table: str, block: LedgerBlock) -> bool:
    """Return whether a block for the run and stage is already present."""
    try:
        ledger = spark.table(ledger_table)
        existing_count = (
            ledger
            .where(
                (ledger["pipeline_run_id"] == block.pipeline_run_id)
                & (ledger["pipeline_stage"] == block.pipeline_stage)
            )
            .count()
        )
    except Exception:
        return False
    return existing_count > 0


def append_block_if_missing(
    spark: Any,
    ledger_table: str,
    block: LedgerBlock,
) -> None:
    """Append a block unless the same run/stage already exists."""
    if block_exists(spark, ledger_table, block):
        LOGGER.info(
            "Ledger block already exists for run=%s stage=%s; skipping append",
            block.pipeline_run_id,
            block.pipeline_stage,
        )
        return
    append_block(spark, ledger_table, block)


def read_latest_block(
    spark: Any,
    ledger_table: str,
    pipeline_run_id: str,
) -> LedgerBlock:
    """Read the latest block for a pipeline run from the ledger table."""
    ledger = spark.table(ledger_table)
    rows = ledger.where(
        ledger["pipeline_run_id"] == pipeline_run_id
    ).orderBy("block_index").collect()
    if not rows:
        raise ValueError(f"No ledger blocks found for run {pipeline_run_id}")
    return LedgerBlock(**rows[-1].asDict())


def read_stage_block(
    spark: Any,
    ledger_table: str,
    pipeline_run_id: str,
    pipeline_stage: str,
) -> LedgerBlock:
    """Read one stage block for a pipeline run from the ledger table."""
    ledger = spark.table(ledger_table)
    rows = ledger.where(
        (ledger["pipeline_run_id"] == pipeline_run_id)
        & (ledger["pipeline_stage"] == pipeline_stage)
    ).collect()
    if not rows:
        raise ValueError(
            f"No {pipeline_stage} block found for run {pipeline_run_id}"
        )
    return LedgerBlock(**rows[0].asDict())
