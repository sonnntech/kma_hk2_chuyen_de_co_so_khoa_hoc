# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Bronze ingestion
# MAGIC
# MAGIC Reads Source, adds run metadata, and safely replaces the Bronze table.

# COMMAND ----------

import importlib
import logging
import sys
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

from blockchain_pipeline import pipeline  # noqa: E402
from config.demo_config import (  # noqa: E402
    BRONZE_TABLE,
    SOURCE_TABLE,
    qualified_table_name,
)

pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

bronze = pipeline.run_bronze(
    spark=spark,
    source_table=qualified_table_name(SOURCE_TABLE),
    bronze_table=qualified_table_name(BRONZE_TABLE),
)

display(bronze.groupBy("pipeline_run_id", "source_table").count())
display(bronze.orderBy("transaction_id").limit(10))
