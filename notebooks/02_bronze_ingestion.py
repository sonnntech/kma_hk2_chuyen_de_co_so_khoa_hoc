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

from blockchain_pipeline import ledger, lineage, pipeline  # noqa: E402
from config.demo_config import (  # noqa: E402
    BLOCKCHAIN_LEDGER_TABLE,
    BRONZE_TABLE,
    LINEAGE_EVENTS_TABLE,
    SOURCE_TABLE,
    qualified_table_name,
)

ledger = importlib.reload(ledger)
lineage = importlib.reload(lineage)
pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

source_table = qualified_table_name(SOURCE_TABLE)
bronze_table = qualified_table_name(BRONZE_TABLE)
ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)
lineage_table = qualified_table_name(LINEAGE_EVENTS_TABLE)
started_at = lineage.utc_now()
pipeline_run_id = "UNKNOWN"
transformation_name = "bronze_ingestion"
transformation_description = (
    "Read Source transactions and add pipeline_run_id, ingestion_time and source_table"
)

try:
    source = spark.table(source_table)
    source_block = None
    bronze = pipeline.run_bronze(
        spark=spark,
        source_table=source_table,
        bronze_table=bronze_table,
    )
    pipeline_run_id = bronze.select("pipeline_run_id").first()["pipeline_run_id"]
    created_at = datetime.now(timezone.utc)

    source_block = ledger.create_block_for_dataframe(
        dataframe=source,
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
    lineage.append_lineage_event(
        spark=spark,
        lineage_table=lineage_table,
        event=lineage.create_success_event(
            pipeline_run_id=pipeline_run_id,
            source_stage="SOURCE",
            target_stage="BRONZE",
            source_table=source_table,
            target_table=bronze_table,
            transformation_name=transformation_name,
            transformation_description=transformation_description,
            input_record_count=source_block.record_count,
            output_record_count=bronze_block.record_count,
            input_batch_hash=source_block.batch_hash,
            output_batch_hash=bronze_block.batch_hash,
            started_at=started_at,
            finished_at=lineage.utc_now(),
        ),
    )
except Exception as error:
    lineage.safe_append_lineage_event(
        spark=spark,
        lineage_table=lineage_table,
        event=lineage.create_failed_event(
            pipeline_run_id=pipeline_run_id,
            source_stage="SOURCE",
            target_stage="BRONZE",
            source_table=source_table,
            target_table=bronze_table,
            transformation_name=transformation_name,
            transformation_description=transformation_description,
            started_at=started_at,
            error_message=str(error),
        ),
    )
    raise

display(bronze.groupBy("pipeline_run_id", "source_table").count())
ledger_snapshot = spark.table(ledger_table)
display(ledger_snapshot.where(ledger_snapshot["pipeline_run_id"] == pipeline_run_id))
lineage_snapshot = spark.table(lineage_table)
display(lineage_snapshot.where(lineage_snapshot["pipeline_run_id"] == pipeline_run_id))
display(bronze.orderBy("transaction_id").limit(10))
