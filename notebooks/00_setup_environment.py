# Databricks notebook source
# MAGIC %md
# MAGIC # Task 01 - Setup environment
# MAGIC
# MAGIC **Input:** Shared values from `config/demo_config.py`.
# MAGIC
# MAGIC **Output:** The configured schema exists and is selected.
# MAGIC
# MAGIC **Expected result:** This notebook can be run repeatedly without deleting data.

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

from config.demo_config import (  # noqa: E402
    CATALOG_NAME,
    SCHEMA_NAME,
    qualified_schema_name,
)

# COMMAND ----------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger("setup_environment")

try:
    logger.info("Creating schema if needed: %s", qualified_schema_name())
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {qualified_schema_name()}")
    spark.sql(f"USE CATALOG `{CATALOG_NAME}`")
    spark.sql(f"USE SCHEMA `{SCHEMA_NAME}`")

    active_context = spark.sql(
        "SELECT current_catalog() AS catalog, current_schema() AS schema"
    )
    display(active_context)
    logger.info("Environment setup completed successfully")
except Exception:
    logger.exception("Environment setup failed")
    raise
