"""Medallion pipeline transformations and Delta table orchestration."""

from __future__ import annotations

import logging
from uuid import uuid4

from pyspark.sql import Column, DataFrame, SparkSession, Window
from pyspark.sql import functions as F

LOGGER = logging.getLogger(__name__)

TRANSACTION_COLUMNS: tuple[str, ...] = (
    "transaction_id",
    "customer_id",
    "transaction_time",
    "product",
    "quantity",
    "unit_price",
    "amount",
    "source_system",
)
BRONZE_METADATA_COLUMNS: tuple[str, ...] = (
    "pipeline_run_id",
    "ingestion_time",
    "source_table",
)


def _require_columns(dataframe: DataFrame, columns: tuple[str, ...]) -> None:
    missing_columns = sorted(set(columns) - set(dataframe.columns))
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")


def _non_empty(column_name: str) -> Column:
    return F.col(column_name).isNotNull() & (
        F.length(F.trim(F.col(column_name))) > 0
    )


def build_bronze(
    source: DataFrame,
    pipeline_run_id: str,
    source_table: str,
) -> DataFrame:
    """Add ingestion metadata to source transactions."""
    _require_columns(source, TRANSACTION_COLUMNS)
    if not pipeline_run_id.strip():
        raise ValueError("pipeline_run_id must not be empty")
    if not source_table.strip():
        raise ValueError("source_table must not be empty")

    return source.select(*TRANSACTION_COLUMNS).select(
        "*",
        F.lit(pipeline_run_id).alias("pipeline_run_id"),
        F.current_timestamp().alias("ingestion_time"),
        F.lit(source_table).alias("source_table"),
    )


def build_silver(bronze: DataFrame) -> DataFrame:
    """Normalize, validate, and deduplicate Bronze transactions."""
    _require_columns(bronze, TRANSACTION_COLUMNS + BRONZE_METADATA_COLUMNS)

    normalized = bronze.select(
        F.trim(F.col("transaction_id")).cast("string").alias("transaction_id"),
        F.trim(F.col("customer_id")).cast("string").alias("customer_id"),
        F.col("transaction_time").cast("timestamp").alias("transaction_time"),
        F.trim(F.col("product")).cast("string").alias("product"),
        F.col("quantity").cast("integer").alias("quantity"),
        F.col("unit_price").cast("decimal(18,2)").alias("unit_price"),
        F.trim(F.col("source_system")).cast("string").alias("source_system"),
        F.col("pipeline_run_id").cast("string").alias("pipeline_run_id"),
        F.col("ingestion_time").cast("timestamp").alias("ingestion_time"),
        F.col("source_table").cast("string").alias("source_table"),
    )

    valid_rows = normalized.filter(
        _non_empty("transaction_id")
        & _non_empty("customer_id")
        & F.col("transaction_time").isNotNull()
        & _non_empty("product")
        & F.col("quantity").isNotNull()
        & (F.col("quantity") > 0)
        & F.col("unit_price").isNotNull()
        & (F.col("unit_price") > 0)
        & _non_empty("source_system")
        & _non_empty("pipeline_run_id")
        & F.col("ingestion_time").isNotNull()
        & _non_empty("source_table")
    )

    deduplication_order = Window.partitionBy("transaction_id").orderBy(
        F.col("ingestion_time").desc(),
        F.col("pipeline_run_id").desc(),
        F.col("customer_id").asc(),
        F.col("product").asc(),
    )
    deduplicated = (
        valid_rows.withColumn(
            "_deduplication_rank", F.row_number().over(deduplication_order)
        )
        .filter(F.col("_deduplication_rank") == 1)
        .drop("_deduplication_rank")
    )

    return deduplicated.withColumn(
        "amount",
        (F.col("quantity") * F.col("unit_price")).cast("decimal(18,2)"),
    ).select(
        *TRANSACTION_COLUMNS,
        *BRONZE_METADATA_COLUMNS,
    )


def build_gold(silver: DataFrame) -> DataFrame:
    """Aggregate valid Silver transactions by date and product."""
    _require_columns(silver, TRANSACTION_COLUMNS)

    return (
        silver.groupBy(
            F.to_date("transaction_time").alias("transaction_date"),
            F.col("product"),
        )
        .agg(
            F.sum("quantity").alias("total_quantity"),
            F.sum("amount").cast("decimal(38,2)").alias("total_revenue"),
            F.count(F.lit(1)).alias("transaction_count"),
        )
        .select(
            "transaction_date",
            "product",
            "total_quantity",
            "total_revenue",
            "transaction_count",
        )
    )


def overwrite_delta_table(dataframe: DataFrame, table_name: str) -> None:
    """Replace a managed Delta table to make stage reruns idempotent."""
    if not table_name.strip():
        raise ValueError("table_name must not be empty")
    LOGGER.info("Overwriting Delta table %s", table_name)
    (
        dataframe.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def run_bronze(
    spark: SparkSession,
    source_table: str,
    bronze_table: str,
    pipeline_run_id: str | None = None,
) -> DataFrame:
    """Read Source, build Bronze, overwrite its table, and return persisted data."""
    current_run_id = pipeline_run_id or str(uuid4())
    bronze = build_bronze(
        source=spark.table(source_table),
        pipeline_run_id=current_run_id,
        source_table=source_table,
    )
    overwrite_delta_table(bronze, bronze_table)
    return spark.table(bronze_table)


def run_silver(
    spark: SparkSession,
    bronze_table: str,
    silver_table: str,
) -> DataFrame:
    """Read Bronze, build Silver, overwrite its table, and return persisted data."""
    silver = build_silver(spark.table(bronze_table))
    overwrite_delta_table(silver, silver_table)
    return spark.table(silver_table)


def run_gold(
    spark: SparkSession,
    silver_table: str,
    gold_table: str,
) -> DataFrame:
    """Read Silver, build Gold, overwrite its table, and return persisted data."""
    gold = build_gold(spark.table(silver_table))
    overwrite_delta_table(gold, gold_table)
    return spark.table(gold_table)
