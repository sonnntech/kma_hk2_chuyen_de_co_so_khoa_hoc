"""Unit tests for deterministic canonicalization."""

from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest

from blockchain_pipeline.canonicalization import (
    NULL_TOKEN,
    canonicalize_record,
    canonicalize_value,
)


def test_canonicalize_null_uses_fixed_token() -> None:
    assert canonicalize_value(None) == NULL_TOKEN
    assert canonicalize_value(NULL_TOKEN) == "\\" + NULL_TOKEN


def test_canonicalize_decimal_uses_fixed_scale() -> None:
    assert canonicalize_value(Decimal("12.5"), "decimal(18,2)") == "12.50"
    assert canonicalize_value(Decimal("12.555"), "decimal(18,2)") == "12.56"


def test_canonicalize_timestamp_converts_to_utc_iso_8601() -> None:
    value = datetime(
        2026,
        6,
        15,
        14,
        30,
        45,
        123456,
        tzinfo=timezone(timedelta(hours=7)),
    )
    assert canonicalize_value(value, "timestamp") == (
        "2026-06-15T07:30:45.123456Z"
    )


def test_canonicalize_record_uses_explicit_order_and_escapes_delimiter() -> None:
    first = {"product": r"A|B\C", "quantity": 2}
    second = {"quantity": 2, "product": r"A|B\C"}

    expected = r"A\|B\\C|2"
    assert canonicalize_record(first, ["product", "quantity"]) == expected
    assert canonicalize_record(second, ["product", "quantity"]) == expected


def test_canonicalize_record_rejects_missing_columns() -> None:
    with pytest.raises(ValueError, match="Missing columns: amount"):
        canonicalize_record({"quantity": 2}, ["quantity", "amount"])
