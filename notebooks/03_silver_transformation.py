# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Silver transformation
# MAGIC
# MAGIC Normalizes, validates, recalculates amount, and deduplicates Bronze data.

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
    SILVER_TABLE,
    qualified_table_name,
)

pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

silver = pipeline.run_silver(
    spark=spark,
    bronze_table=qualified_table_name(BRONZE_TABLE),
    silver_table=qualified_table_name(SILVER_TABLE),
)

display(silver.selectExpr("count(*) AS silver_record_count"))
display(silver.orderBy("transaction_id").limit(10))
