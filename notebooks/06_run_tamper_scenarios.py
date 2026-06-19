# Databricks notebook source
# MAGIC %md
# MAGIC # Task 08 - Tamper scenarios and reset
# MAGIC
# MAGIC Select one scenario, confirm intentional tampering, show affected rows
# MAGIC before and after, then run integrity verification.
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

from blockchain_pipeline import tamper, verification  # noqa: E402
from config.demo_config import (  # noqa: E402
    BLOCKCHAIN_LEDGER_TABLE,
    BRONZE_TABLE,
    GOLD_TABLE,
    RANDOM_SEED,
    RECORD_COUNT,
    SILVER_TABLE,
    SOURCE_SYSTEM,
    SOURCE_TABLE,
    VERIFICATION_RESULTS_TABLE,
    qualified_table_name,
)

tamper = importlib.reload(tamper)
verification = importlib.reload(verification)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

dbutils.widgets.dropdown("SCENARIO", tamper.SCENARIO_NONE, list(tamper.SCENARIOS))
dbutils.widgets.text("PIPELINE_RUN_ID", "")
dbutils.widgets.text("CONFIRM_TAMPER", "NO")

scenario = dbutils.widgets.get("SCENARIO").strip()
pipeline_run_id = dbutils.widgets.get("PIPELINE_RUN_ID").strip() or None
confirm_tamper = dbutils.widgets.get("CONFIRM_TAMPER").strip()

tables = tamper.DemoTables(
    source=qualified_table_name(SOURCE_TABLE),
    bronze=qualified_table_name(BRONZE_TABLE),
    silver=qualified_table_name(SILVER_TABLE),
    gold=qualified_table_name(GOLD_TABLE),
    ledger=qualified_table_name(BLOCKCHAIN_LEDGER_TABLE),
    verification_results=qualified_table_name(VERIFICATION_RESULTS_TABLE),
)

tamper.require_confirmation(scenario, confirm_tamper)
plan = tamper.build_scenario_plan(
    spark=spark,
    scenario=scenario,
    tables=tables,
    pipeline_run_id=pipeline_run_id,
)

print(f"Scenario: {plan.scenario}")
print(f"Description: {plan.description}")
print(f"Pipeline run: {plan.pipeline_run_id}")
print(f"Expected verification status: {plan.expected_status}")

display(tamper.preview_plan(spark, plan))

execution = tamper.run_scenario(
    spark=spark,
    plan=plan,
    tables=tables,
    record_count=RECORD_COUNT,
    random_seed=RANDOM_SEED,
    source_system=SOURCE_SYSTEM,
)
active_run_id = execution.new_pipeline_run_id or plan.pipeline_run_id

display(
    tamper.preview_plan(
        spark,
        tamper.build_scenario_plan(
            spark=spark,
            scenario=tamper.SCENARIO_NONE
            if scenario == tamper.SCENARIO_RESET_BASELINE
            else scenario,
            tables=tables,
            pipeline_run_id=active_run_id,
        ),
    )
)

results = verification.verify_pipeline_run(
    spark=spark,
    ledger_table=tables.ledger,
    pipeline_run_id=active_run_id,
)
verification.append_verification_results(
    spark=spark,
    results_table=tables.verification_results,
    results=results,
)

verified_at = results[0].verified_at
verification_snapshot = spark.table(tables.verification_results)
display(
    verification_snapshot.where(
        (verification_snapshot["pipeline_run_id"] == active_run_id)
        & (verification_snapshot["verified_at"] == verified_at)
    ).orderBy("block_index")
)

first_broken = verification.first_broken_block(results)
if first_broken is None:
    print(f"Verification result for {active_run_id}: VALID")
else:
    print(
        "First broken block: "
        f"index={first_broken.block_index}, "
        f"stage={first_broken.pipeline_stage}, "
        f"status={first_broken.verification_status}, "
        f"reason={first_broken.failure_reason}"
    )
