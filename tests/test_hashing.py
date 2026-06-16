"""Unit tests for deterministic SHA-256 helpers."""

from datetime import datetime
from decimal import Decimal
from typing import Any

import pytest

from blockchain_pipeline.hashing import (
    compute_batch_hash,
    compute_row_hash,
    compute_schema_hash,
)


def test_same_record_with_different_mapping_order_has_same_hash() -> None:
    columns = ["transaction_id", "amount"]
    first = {"transaction_id": "TX1", "amount": Decimal("10.00")}
    second = {"amount": Decimal("10.00"), "transaction_id": "TX1"}

    assert compute_row_hash(first, columns) == compute_row_hash(second, columns)


def test_changed_value_changes_row_hash() -> None:
    columns = ["transaction_id", "amount"]
    first = {"transaction_id": "TX1", "amount": Decimal("10.00")}
    changed = {"transaction_id": "TX1", "amount": Decimal("10.01")}

    assert compute_row_hash(first, columns) != compute_row_hash(changed, columns)


def test_schema_hash_is_independent_of_mapping_key_order() -> None:
    first = {"type": "struct", "nullable": False}
    second = {"nullable": False, "type": "struct"}

    assert compute_schema_hash(first) == compute_schema_hash(second)
    assert compute_schema_hash(first) != compute_schema_hash(
        {"type": "struct", "nullable": True}
    )


try:
    from pyspark.sql import SparkSession
    from pyspark.sql.types import (
        DecimalType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )
except ImportError:
    SparkSession = None


@pytest.fixture(scope="module")
def spark() -> Any:
    """Create a local Spark session for batch hashing tests."""
    if SparkSession is None:
        pytest.skip("PySpark is not installed")
    session = (
        SparkSession.builder.master("local[2]")
        .appName("hashing-test")
        .getOrCreate()
    )
    yield session
    session.stop()


def _transaction_schema() -> Any:
    if SparkSession is None:
        pytest.skip("PySpark is not installed")
    return StructType(
        [
            StructField("transaction_id", StringType(), nullable=False),
            StructField("transaction_time", TimestampType(), nullable=False),
            StructField("amount", DecimalType(18, 2), nullable=False),
        ]
    )


def test_batch_hash_ignores_input_row_and_partition_order(
    spark: Any,
) -> None:
    rows = [
        ("TX2", datetime(2026, 1, 2, 9), Decimal("20.00")),
        ("TX1", datetime(2026, 1, 2, 8), Decimal("10.00")),
        ("TX3", datetime(2026, 1, 2, 10), Decimal("30.00")),
    ]
    columns = ["transaction_id", "transaction_time", "amount"]
    first = spark.createDataFrame(rows, _transaction_schema()).repartition(3)
    second = spark.createDataFrame(
        list(reversed(rows)), _transaction_schema()
    ).repartition(1)

    assert compute_batch_hash(first, columns, ["transaction_id"]) == (
        compute_batch_hash(second, columns, ["transaction_id"])
    )


def test_changed_row_changes_batch_hash(spark: Any) -> None:
    columns = ["transaction_id", "transaction_time", "amount"]
    original = spark.createDataFrame(
        [("TX1", datetime(2026, 1, 2, 8), Decimal("10.00"))],
        _transaction_schema(),
    )
    changed = spark.createDataFrame(
        [("TX1", datetime(2026, 1, 2, 8), Decimal("10.01"))],
        _transaction_schema(),
    )

    assert compute_batch_hash(original, columns) != compute_batch_hash(
        changed, columns
    )


def test_spark_schema_change_changes_schema_hash(spark: Any) -> None:
    first = _transaction_schema()
    second = StructType(
        [
            StructField("transaction_id", StringType(), nullable=False),
            StructField("transaction_time", TimestampType(), nullable=False),
            StructField("amount", DecimalType(20, 2), nullable=False),
        ]
    )

    assert compute_schema_hash(first) != compute_schema_hash(second)
