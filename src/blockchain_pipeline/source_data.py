"""Deterministic source transaction generation and validation."""

from typing import TypedDict

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql import functions as F

from blockchain_pipeline.schemas import TRANSACTION_SCHEMA


class ValidationResult(TypedDict):
    """Summary of source transaction validation checks."""

    record_count: int
    duplicate_transaction_ids: int
    invalid_quantities: int
    invalid_unit_prices: int
    invalid_amounts: int
    null_required_values: int


def build_source_transactions(
    spark: SparkSession,
    record_count: int,
    random_seed: int,
    source_system: str,
) -> DataFrame:
    """Build reproducible synthetic transactions without personal data."""
    if record_count <= 0:
        raise ValueError("record_count must be greater than zero")
    if not source_system.strip():
        raise ValueError("source_system must not be empty")

    row_number = F.col("id") + F.lit(1)
    mixed_value = F.pmod(
        row_number * F.lit(1_103_515_245) + F.lit(random_seed * 12_345),
        F.lit(2_147_483_647),
    )
    products = F.array(
        F.lit("Laptop"),
        F.lit("Monitor"),
        F.lit("Keyboard"),
        F.lit("Mouse"),
        F.lit("Headset"),
    )
    product_index = (
        F.pmod(mixed_value, F.lit(5)) + F.lit(1)
    ).cast("integer")

    generated = (
        spark.range(record_count)
        .select(
            F.format_string("TX%08d", row_number).alias("transaction_id"),
            F.format_string(
                "CUS%05d", F.pmod(mixed_value, F.lit(2_000)) + F.lit(1)
            ).alias("customer_id"),
            F.timestamp_seconds(
                F.lit(1_735_689_600)
                + F.pmod(mixed_value, F.lit(365 * 24 * 60 * 60))
            ).alias("transaction_time"),
            F.element_at(products, product_index).alias("product"),
            (F.pmod(mixed_value, F.lit(5)) + F.lit(1))
            .cast("integer")
            .alias("quantity"),
            (
                (F.pmod(mixed_value, F.lit(199_901)) + F.lit(100))
                / F.lit(100)
            )
            .cast("decimal(18,2)")
            .alias("unit_price"),
            F.lit(source_system).alias("source_system"),
        )
        .withColumn(
            "amount",
            (F.col("quantity") * F.col("unit_price")).cast("decimal(18,2)"),
        )
        .select(*TRANSACTION_SCHEMA.fieldNames())
    )

    return generated.select(
        *[
            F.col(field.name).cast(field.dataType).alias(field.name)
            for field in TRANSACTION_SCHEMA.fields
        ]
    )


def validate_source_transactions(dataframe: DataFrame) -> ValidationResult:
    """Validate row count, uniqueness, required values, and arithmetic."""
    required_columns = TRANSACTION_SCHEMA.fieldNames()
    missing_columns = sorted(set(required_columns) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    metrics = dataframe.agg(
        F.count(F.lit(1)).alias("record_count"),
        (
            F.count(F.lit(1)) - F.countDistinct("transaction_id")
        ).alias("duplicate_transaction_ids"),
        F.sum(F.when(F.col("quantity") <= 0, 1).otherwise(0)).alias(
            "invalid_quantities"
        ),
        F.sum(F.when(F.col("unit_price") <= 0, 1).otherwise(0)).alias(
            "invalid_unit_prices"
        ),
        F.sum(
            F.when(
                F.col("amount")
                != (F.col("quantity") * F.col("unit_price")).cast(
                    "decimal(18,2)"
                ),
                1,
            ).otherwise(0)
        ).alias("invalid_amounts"),
        F.sum(
            F.when(
                F.greatest(
                    *[
                        F.col(column_name).isNull().cast("integer")
                        for column_name in required_columns
                    ]
                )
                > 0,
                1,
            ).otherwise(0)
        ).alias("null_required_values"),
    ).first()

    if metrics is None:
        raise RuntimeError("Unable to calculate validation metrics")

    return ValidationResult(
        record_count=int(metrics["record_count"]),
        duplicate_transaction_ids=int(metrics["duplicate_transaction_ids"]),
        invalid_quantities=int(metrics["invalid_quantities"]),
        invalid_unit_prices=int(metrics["invalid_unit_prices"]),
        invalid_amounts=int(metrics["invalid_amounts"]),
        null_required_values=int(metrics["null_required_values"]),
    )
