"""Deterministic value and record canonicalization."""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal, InvalidOperation, ROUND_HALF_EVEN
from typing import Any, Mapping, Sequence

NULL_TOKEN = "<NULL>"
FIELD_DELIMITER = "|"
ESCAPE_CHARACTER = "\\"
DEFAULT_DECIMAL_SCALE = 2


def _data_type_name(data_type: Any) -> str:
    if data_type is None:
        return ""
    if isinstance(data_type, str):
        return data_type.lower()
    if hasattr(data_type, "typeName"):
        return str(data_type.typeName()).lower()
    return type(data_type).__name__.lower()


def _decimal_scale(data_type: Any) -> int:
    scale = getattr(data_type, "scale", None)
    if scale is not None:
        return int(scale)

    type_name = _data_type_name(data_type)
    if type_name.startswith("decimal(") and type_name.endswith(")"):
        return int(type_name[:-1].split(",")[1].strip())
    return DEFAULT_DECIMAL_SCALE


def _canonicalize_decimal(value: Any, scale: int) -> str:
    try:
        decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
        quantum = Decimal(1).scaleb(-scale)
        return format(
            decimal_value.quantize(quantum, rounding=ROUND_HALF_EVEN),
            f".{scale}f",
        )
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"Unable to canonicalize decimal value: {value!r}") from exc


def _canonicalize_timestamp(value: Any) -> str:
    if not isinstance(value, datetime):
        raise TypeError("Timestamp values must be datetime instances")

    timestamp = value
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    else:
        timestamp = timestamp.astimezone(timezone.utc)
    return timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _escape_string(value: str) -> str:
    escaped = (
        value.replace(ESCAPE_CHARACTER, ESCAPE_CHARACTER * 2)
        .replace(FIELD_DELIMITER, ESCAPE_CHARACTER + FIELD_DELIMITER)
        .replace("\r", r"\r")
        .replace("\n", r"\n")
    )
    return ESCAPE_CHARACTER + escaped if value == NULL_TOKEN else escaped


def canonicalize_value(value: Any, data_type: Any = None) -> str:
    """Convert a supported value to its deterministic string representation."""
    if value is None:
        return NULL_TOKEN

    type_name = _data_type_name(data_type)
    if isinstance(value, datetime) or "timestamp" in type_name:
        return _canonicalize_timestamp(value)
    if isinstance(value, date) or type_name in {"date", "datetype"}:
        if not isinstance(value, date):
            raise TypeError("Date values must be date instances")
        return value.isoformat()
    if isinstance(value, Decimal) or type_name.startswith("decimal"):
        return _canonicalize_decimal(value, _decimal_scale(data_type))
    if isinstance(value, bool) or type_name in {"boolean", "booleantype"}:
        return "true" if bool(value) else "false"
    if isinstance(value, float):
        return format(Decimal(str(value)).normalize(), "f")

    return _escape_string(str(value))


def canonicalize_record(
    record: Mapping[str, Any],
    ordered_columns: Sequence[str],
    data_types: Mapping[str, Any] | None = None,
) -> str:
    """Canonicalize a record using an explicit and stable column order."""
    if not ordered_columns:
        raise ValueError("ordered_columns must not be empty")

    missing_columns = [column for column in ordered_columns if column not in record]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    types = data_types or {}
    return FIELD_DELIMITER.join(
        canonicalize_value(record[column], types.get(column))
        for column in ordered_columns
    )
