# Databricks notebook source
# MAGIC %md
# MAGIC # Task 03 - Gold aggregation
# MAGIC
# MAGIC Aggregates Silver transactions by transaction date and product.

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
    GOLD_TABLE,
    SILVER_TABLE,
    qualified_table_name,
)

pipeline = importlib.reload(pipeline)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

gold = pipeline.run_gold(
    spark=spark,
    silver_table=qualified_table_name(SILVER_TABLE),
    gold_table=qualified_table_name(GOLD_TABLE),
)

display(gold.selectExpr("count(*) AS gold_group_count"))
display(gold.orderBy("transaction_date", "product"))
