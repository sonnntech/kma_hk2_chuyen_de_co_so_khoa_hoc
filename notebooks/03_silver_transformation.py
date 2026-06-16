# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Silver transformation
# MAGIC
# MAGIC Normalizes, validates, recalculates amount, and deduplicates Bronze data.

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
    SILVER_TABLE,
    qualified_table_name,
)

ledger = importlib.reload(ledger)
pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

silver = pipeline.run_silver(
    spark=spark,
    bronze_table=qualified_table_name(BRONZE_TABLE),
    silver_table=qualified_table_name(SILVER_TABLE),
)
pipeline_run_id = silver.select("pipeline_run_id").first()["pipeline_run_id"]
ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)
bronze_block = ledger.read_stage_block(
    spark=spark,
    ledger_table=ledger_table,
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="BRONZE",
)
silver_block = ledger.create_block_for_dataframe(
    dataframe=silver,
    pipeline_run_id=pipeline_run_id,
    pipeline_stage="SILVER",
    source_table=qualified_table_name(BRONZE_TABLE),
    target_table=qualified_table_name(SILVER_TABLE),
    transformation="Validate, normalize, deduplicate and recalculate amount",
    created_at=datetime.now(timezone.utc),
    previous_block=bronze_block,
    sort_columns=["transaction_id"],
)
ledger.append_block_if_missing(spark, ledger_table, silver_block)

display(silver.selectExpr("count(*) AS silver_record_count"))
ledger_snapshot = spark.table(ledger_table)
display(ledger_snapshot.where(ledger_snapshot["pipeline_run_id"] == pipeline_run_id))
display(silver.orderBy("transaction_id").limit(10))
