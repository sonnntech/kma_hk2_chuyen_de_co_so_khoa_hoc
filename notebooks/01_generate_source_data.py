# Databricks notebook source
# MAGIC %md
# MAGIC # Task 01 - Generate source transactions
# MAGIC
# MAGIC **Input:** Record count, seed, source system, and table configuration.
# MAGIC
# MAGIC **Output:** Managed Delta table `source_transactions`.
# MAGIC
# MAGIC **Expected result:** Exactly 10,000 valid, reproducible synthetic rows.

# COMMAND ----------

import logging
import sys
from pathlib import Path


def _add_project_paths() -> None:
    """Add repository modules to the Python import path."""
    candidates = (Path.cwd(), Path.cwd().parent)
    for candidate in candidates:
        if (candidate / "config").is_dir() and (candidate / "src").is_dir():
            for path in (candidate, candidate / "src"):
                if str(path) not in sys.path:
                    sys.path.insert(0, str(path))
            return
    raise RuntimeError("Unable to locate the repository root")


_add_project_paths()

from blockchain_pipeline.source_data import (  # noqa: E402
    build_source_transactions,
    validate_source_transactions,
)
from config.demo_config import (  # noqa: E402
    CATALOG_NAME,
    RANDOM_SEED,
    RECORD_COUNT,
    SCHEMA_NAME,
    SOURCE_SYSTEM,
    SOURCE_TABLE,
    qualified_schema_name,
    qualified_table_name,
)

# COMMAND ----------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("generate_source_data")

try:
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qualified_schema_name()}")
    spark.sql(f"USE CATALOG `{CATALOG_NAME}`")
    spark.sql(f"USE SCHEMA `{SCHEMA_NAME}`")

    source_transactions = build_source_transactions(
        spark=spark,
        record_count=RECORD_COUNT,
        random_seed=RANDOM_SEED,
        source_system=SOURCE_SYSTEM,
    )
    validation = validate_source_transactions(source_transactions)

    expected_validation = {
        "record_count": RECORD_COUNT,
        "duplicate_transaction_ids": 0,
        "invalid_quantities": 0,
        "invalid_unit_prices": 0,
        "invalid_amounts": 0,
        "null_required_values": 0,
    }
    if validation != expected_validation:
        raise ValueError(f"Source data validation failed: {validation}")

    table_name = qualified_table_name(SOURCE_TABLE)
    logger.info("Writing %s records to %s", RECORD_COUNT, table_name)
    (
        source_transactions.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    persisted_transactions = spark.table(table_name)
    persisted_validation = validate_source_transactions(persisted_transactions)
    if persisted_validation != expected_validation:
        raise ValueError(
            f"Persisted source data validation failed: {persisted_validation}"
        )

    display(
        spark.createDataFrame(
            [(key, value) for key, value in persisted_validation.items()],
            ["validation_check", "value"],
        )
    )
    display(persisted_transactions.orderBy("transaction_id").limit(10))
    logger.info("Source transaction generation completed successfully")
except Exception:
    logger.exception("Source transaction generation failed")
    raise
