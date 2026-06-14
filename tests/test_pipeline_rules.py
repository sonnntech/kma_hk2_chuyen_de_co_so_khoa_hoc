"""Tests for Silver validation and Gold aggregation rules."""

from datetime import datetime
from decimal import Decimal

import pytest

pyspark = pytest.importorskip("pyspark")

from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from blockchain_pipeline.pipeline import build_gold, build_silver


@pytest.fixture(scope="session")
def spark() -> SparkSession:
    """Create a local Spark session for transformation tests."""
    session = (
        SparkSession.builder.master("local[1]")
        .appName("pipeline-rules-test")
        .getOrCreate()
    )
    yield session
    session.stop()


def test_silver_normalizes_validates_deduplicates_and_recalculates_amount(
    spark: SparkSession,
) -> None:
    """Silver keeps the newest valid transaction and recalculates amount."""
    rows = [
        (
            " TX0001 ",
            " CUS001 ",
            "2026-01-02 08:00:00",
            " Laptop ",
            "2",
            "10.50",
            "999.99",
            " SCHOOL_DEMO ",
            "run-old",
            datetime(2026, 1, 2, 8, 1),
            "source_transactions",
        ),
        (
            "TX0001",
            "CUS001",
            "2026-01-02 08:00:00",
            "Laptop",
            "3",
            "10.50",
            "0.00",
            "SCHOOL_DEMO",
            "run-new",
            datetime(2026, 1, 2, 8, 2),
            "source_transactions",
        ),
        (
            "TX0002",
            "CUS002",
            "2026-01-02 09:00:00",
            "Mouse",
            "0",
            "5.00",
            "0.00",
            "SCHOOL_DEMO",
            "run-new",
            datetime(2026, 1, 2, 9, 1),
            "source_transactions",
        ),
    ]
    bronze = spark.createDataFrame(
        rows,
        [
            "transaction_id",
            "customer_id",
            "transaction_time",
            "product",
            "quantity",
            "unit_price",
            "amount",
            "source_system",
            "pipeline_run_id",
            "ingestion_time",
            "source_table",
        ],
    )

    result = build_silver(bronze).collect()

    assert len(result) == 1
    assert result[0]["transaction_id"] == "TX0001"
    assert result[0]["pipeline_run_id"] == "run-new"
    assert result[0]["quantity"] == 3
    assert result[0]["unit_price"] == Decimal("10.50")
    assert result[0]["amount"] == Decimal("31.50")


def test_gold_aggregates_by_date_and_product(spark: SparkSession) -> None:
    """Gold calculates quantity, revenue, and count for each date/product."""
    rows = [
        ("2026-01-02 08:00:00", "Laptop", 2, Decimal("21.00")),
        ("2026-01-02 09:00:00", "Laptop", 3, Decimal("31.50")),
        ("2026-01-02 10:00:00", "Mouse", 1, Decimal("5.00")),
    ]
    base = spark.createDataFrame(
        rows, ["transaction_time", "product", "quantity", "amount"]
    )
    silver = (
        base.withColumn(
            "transaction_time", base["transaction_time"].cast("timestamp")
        )
        .withColumn("amount", base["amount"].cast("decimal(18,2)"))
        .select(
            "transaction_time",
            "product",
            "quantity",
            "amount",
            *[
                F.lit("test").alias(column_name)
                for column_name in (
                    "transaction_id",
                    "customer_id",
                    "unit_price",
                    "source_system",
                )
            ],
        )
    )

    result = {
        row["product"]: row.asDict()
        for row in build_gold(silver).collect()
    }

    assert result["Laptop"]["total_quantity"] == 5
    assert result["Laptop"]["total_revenue"] == Decimal("52.50")
    assert result["Laptop"]["transaction_count"] == 2
    assert result["Mouse"]["total_quantity"] == 1
    assert result["Mouse"]["total_revenue"] == Decimal("5.00")
    assert result["Mouse"]["transaction_count"] == 1
