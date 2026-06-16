# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Bronze ingestion
# MAGIC
# MAGIC Reads Source, adds run metadata, and safely replaces the Bronze table.
# MAGIC
# MAGIC **Compute requirement:** run this as a Python notebook on Databricks
# MAGIC notebook/serverless compute. SQL Warehouses only execute SQL cells and
# MAGIC cannot run this notebook.

# COMMAND ----------

import importlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path


def _add_project_paths() -> None:
    """Add repository modules to the Python import path."""
    for candidate in (Path.cwd(), Path.cwd().parent):
        if (candidate / "config").is_dir() and (candidate / "src").is_dir():
            for path in (candidate, candidate / "src"):
                if str(path) not in sys.path:
                    sys.path.insert(0, str(path))
            return
    raise RuntimeError("Unable to locate the repository root")


_add_project_paths()

from blockchain_pipeline import ledger, pipeline  # noqa: E402
from config.demo_config import (  # noqa: E402
    BLOCKCHAIN_LEDGER_TABLE,
    BRONZE_TABLE,
    SOURCE_TABLE,
    qualified_table_name,
)

ledger = importlib.reload(ledger)
pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

bronze = pipeline.run_bronze(
    spark=spark,
    source_table=qualified_table_name(SOURCE_TABLE),
    bronze_table=qualified_table_name(BRONZE_TABLE),
)
pipeline_run_id = bronze.select("pipeline_run_id").first()["pipeline_run_id"]
created_at = datetime.now(timezone.utc)
source_table = qualified_table_name(SOURCE_TABLE)
bronze_table = qualified_table_name(BRONZE_TABLE)
ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)

source_block = ledger.create_block_for_dataframe(
    dataframe=spark.table(source_table),
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="SOURCE",
    source_table=source_table,
    target_table=source_table,
    transformation="Source transaction data snapshot",
    created_at=created_at,
    sort_columns=["transaction_id"],
)
ledger.append_block_if_missing(spark, ledger_table, source_block)

bronze_block = ledger.create_block_for_dataframe(
    dataframe=bronze,
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="BRONZE",
    source_table=source_table,
    target_table=bronze_table,
    transformation="Add pipeline_run_id, ingestion_time and source_table",
    created_at=created_at,
    previous_block=source_block,
    sort_columns=["transaction_id"],
)
ledger.append_block_if_missing(spark, ledger_table, bronze_block)

display(bronze.groupBy("pipeline_run_id", "source_table").count())
ledger_snapshot = spark.table(ledger_table)
display(ledger_snapshot.where(ledger_snapshot["pipeline_run_id"] == pipeline_run_id))
display(bronze.orderBy("transaction_id").limit(10))
