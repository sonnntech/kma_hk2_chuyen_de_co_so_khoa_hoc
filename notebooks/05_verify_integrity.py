# Databricks notebook source
# MAGIC %md
# MAGIC # Task 07 - Verify integrity
# MAGIC
# MAGIC Verifies current data hash, record count, block hash and chain links for
# MAGIC one `pipeline_run_id`. This notebook only reports and records results; it
# MAGIC does not repair or mutate pipeline data.
# MAGIC
# MAGIC **Compute requirement:** run this as a Python notebook on Databricks
# MAGIC notebook/serverless compute. SQL Warehouses only execute SQL cells and
# MAGIC cannot run this notebook.

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

from blockchain_pipeline import verification  # noqa: E402
from config.demo_config import (  # noqa: E402
    BLOCKCHAIN_LEDGER_TABLE,
    VERIFICATION_RESULTS_TABLE,
    qualified_table_name,
)

verification = importlib.reload(verification)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

dbutils.widgets.text("pipeline_run_id", "")
selected_pipeline_run_id = dbutils.widgets.get("pipeline_run_id").strip()

ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)
results_table = qualified_table_name(VERIFICATION_RESULTS_TABLE)

if not selected_pipeline_run_id:
    latest_run = (
        spark.table(ledger_table)
        .orderBy("created_at", ascending=False)
        .select("pipeline_run_id")
        .first()
    )
    if latest_run is None:
        raise ValueError("No ledger blocks found. Run notebooks 02, 03 and 04 first.")
    selected_pipeline_run_id = latest_run["pipeline_run_id"]

results = verification.verify_pipeline_run(
    spark=spark,
    ledger_table=ledger_table,
    pipeline_run_id=selected_pipeline_run_id,
)
verification.append_verification_results(
    spark=spark,
    results_table=results_table,
    results=results,
)

current_verified_at = results[0].verified_at
results_df = spark.table(results_table)
display(
    results_df.where(
        (results_df["pipeline_run_id"] == selected_pipeline_run_id)
        & (results_df["verified_at"] == current_verified_at)
    ).orderBy("block_index")
)

first_broken = verification.first_broken_block(results)
if first_broken is None:
    print(f"Pipeline run {selected_pipeline_run_id} verification status: VALID")
else:
    print(
        "First broken block: "
        f"index={first_broken.block_index}, "
        f"stage={first_broken.pipeline_stage}, "
        f"status={first_broken.verification_status}, "
        f"reason={first_broken.failure_reason}"
    )
