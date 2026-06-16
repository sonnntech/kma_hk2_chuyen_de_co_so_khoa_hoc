# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Gold aggregation
# MAGIC
# MAGIC Aggregates Silver transactions by transaction date and product.
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
    GOLD_TABLE,
    SILVER_TABLE,
    qualified_table_name,
)

ledger = importlib.reload(ledger)
pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

gold = pipeline.run_gold(
    spark=spark,
    silver_table=qualified_table_name(SILVER_TABLE),
    gold_table=qualified_table_name(GOLD_TABLE),
)
ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)
pipeline_run_id = (
    spark.table(qualified_table_name(SILVER_TABLE))
    .select("pipeline_run_id")
    .first()["pipeline_run_id"]
)
silver_block = ledger.read_stage_block(
    spark=spark,
    ledger_table=ledger_table,
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="SILVER",
)
gold_block = ledger.create_block_for_dataframe(
    dataframe=gold,
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="GOLD",
    source_table=qualified_table_name(SILVER_TABLE),
    target_table=qualified_table_name(GOLD_TABLE),
    transformation="Aggregate Silver transactions by date and product",
    created_at=datetime.now(timezone.utc),
    previous_block=silver_block,
    sort_columns=["transaction_date", "product"],
)
ledger.append_block_if_missing(spark, ledger_table, gold_block)

display(gold.selectExpr("count(*) AS gold_group_count"))
ledger_snapshot = spark.table(ledger_table)
display(ledger_snapshot.where(ledger_snapshot["pipeline_run_id"] == pipeline_run_id))
display(gold.orderBy("transaction_date", "product"))
