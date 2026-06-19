# Databricks notebook source
# MAGIC %md
# MAGIC # Task 09 - Experiment metrics
# MAGIC
# MAGIC Benchmarks baseline pipeline and secured pipeline using real Databricks
# MAGIC execution. The first run is a warm-up and is marked with `is_warmup=true`;
# MAGIC non-warmup runs use record sizes 1k, 5k, 10k and 50k, three runs each.
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
from uuid import uuid4


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

from blockchain_pipeline import (  # noqa: E402
    ledger,
    metrics,
    pipeline,
    source_data,
    verification,
)
from config.demo_config import (  # noqa: E402
    BLOCKCHAIN_LEDGER_TABLE,
    BRONZE_TABLE,
    EXPERIMENT_METRICS_TABLE,
    GOLD_TABLE,
    RANDOM_SEED,
    SILVER_TABLE,
    SOURCE_SYSTEM,
    SOURCE_TABLE,
    VERIFICATION_RESULTS_TABLE,
    qualified_table_name,
)

ledger = importlib.reload(ledger)
metrics = importlib.reload(metrics)
pipeline = importlib.reload(pipeline)
source_data = importlib.reload(source_data)
verification = importlib.reload(verification)
logging.basicConfig(level=logging.INFO)

# COMMAND ----------

dbutils.widgets.text("RECORD_COUNTS", "1000,5000,10000,50000")
dbutils.widgets.text("RUNS_PER_SIZE", "3")
dbutils.widgets.text("INCLUDE_WARMUP", "YES")

record_counts = [
    int(value.strip())
    for value in dbutils.widgets.get("RECORD_COUNTS").split(",")
    if value.strip()
]
runs_per_size = int(dbutils.widgets.get("RUNS_PER_SIZE").strip())
include_warmup = dbutils.widgets.get("INCLUDE_WARMUP").strip().upper() == "YES"

if runs_per_size < 3:
    raise ValueError("RUNS_PER_SIZE must be at least 3")
if not record_counts:
    raise ValueError("RECORD_COUNTS must contain at least one positive integer")
if any(record_count <= 0 for record_count in record_counts):
    raise ValueError("All RECORD_COUNTS values must be positive")

source_table = qualified_table_name(SOURCE_TABLE)
bronze_table = qualified_table_name(BRONZE_TABLE)
silver_table = qualified_table_name(SILVER_TABLE)
gold_table = qualified_table_name(GOLD_TABLE)
ledger_table = qualified_table_name(BLOCKCHAIN_LEDGER_TABLE)
verification_results_table = qualified_table_name(VERIFICATION_RESULTS_TABLE)
experiment_metrics_table = qualified_table_name(EXPERIMENT_METRICS_TABLE)

experiment_id = str(uuid4())
all_metrics = []


def _write_source(record_count: int) -> None:
    source = source_data.build_source_transactions(
        spark=spark,
        record_count=record_count,
        random_seed=RANDOM_SEED,
        source_system=SOURCE_SYSTEM,
    )
    pipeline.overwrite_delta_table(source, source_table)


def _run_baseline(record_count: int) -> None:
    baseline_run_id = f"baseline-{experiment_id}-{record_count}-{uuid4()}"
    _write_source(record_count)
    pipeline.run_bronze(
        spark=spark,
        source_table=source_table,
        bronze_table=bronze_table,
        pipeline_run_id=baseline_run_id,
    )
    pipeline.run_silver(
        spark=spark,
        bronze_table=bronze_table,
        silver_table=silver_table,
    )
    pipeline.run_gold(
        spark=spark,
        silver_table=silver_table,
        gold_table=gold_table,
    )


def _run_secured(record_count: int) -> str:
    secured_run_id = f"secured-{experiment_id}-{record_count}-{uuid4()}"
    created_at = datetime.now(timezone.utc)
    _write_source(record_count)
    source = spark.table(source_table)
    bronze = pipeline.run_bronze(
        spark=spark,
        source_table=source_table,
        bronze_table=bronze_table,
        pipeline_run_id=secured_run_id,
    )
    silver = pipeline.run_silver(
        spark=spark,
        bronze_table=bronze_table,
        silver_table=silver_table,
    )
    gold = pipeline.run_gold(
        spark=spark,
        silver_table=silver_table,
        gold_table=gold_table,
    )

    source_block = ledger.create_block_for_dataframe(
        dataframe=source,
        pipeline_run_id=secured_run_id,
        pipeline_stage="SOURCE",
        source_table=source_table,
        target_table=source_table,
        transformation="Benchmark source snapshot",
        created_at=created_at,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, ledger_table, source_block)
    bronze_block = ledger.create_block_for_dataframe(
        dataframe=bronze,
        pipeline_run_id=secured_run_id,
        pipeline_stage="BRONZE",
        source_table=source_table,
        target_table=bronze_table,
        transformation="Benchmark Bronze ingestion",
        created_at=created_at,
        previous_block=source_block,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, ledger_table, bronze_block)
    silver_block = ledger.create_block_for_dataframe(
        dataframe=silver,
        pipeline_run_id=secured_run_id,
        pipeline_stage="SILVER",
        source_table=bronze_table,
        target_table=silver_table,
        transformation="Benchmark Silver transformation",
        created_at=created_at,
        previous_block=bronze_block,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, ledger_table, silver_block)
    gold_block = ledger.create_block_for_dataframe(
        dataframe=gold,
        pipeline_run_id=secured_run_id,
        pipeline_stage="GOLD",
        source_table=silver_table,
        target_table=gold_table,
        transformation="Benchmark Gold aggregation",
        created_at=created_at,
        previous_block=silver_block,
        sort_columns=["transaction_date", "product"],
    )
    ledger.append_block_if_missing(spark, ledger_table, gold_block)
    return secured_run_id


def _verify_run(pipeline_run_id: str):
    results = verification.verify_pipeline_run(
        spark=spark,
        ledger_table=ledger_table,
        pipeline_run_id=pipeline_run_id,
    )
    verification.append_verification_results(
        spark=spark,
        results_table=verification_results_table,
        results=results,
    )
    return results


def _metadata_record_count(pipeline_run_id: str) -> int:
    ledger_df = spark.table(ledger_table)
    verification_df = spark.table(verification_results_table)
    ledger_count = (
        ledger_df
        .where(ledger_df["pipeline_run_id"] == pipeline_run_id)
        .count()
    )
    verification_count = (
        verification_df
        .where(verification_df["pipeline_run_id"] == pipeline_run_id)
        .count()
    )
    return int(ledger_count + verification_count)


benchmark_plan = []
if include_warmup:
    benchmark_plan.append((min(record_counts), 0, True))
for record_count in record_counts:
    for run_number in range(1, runs_per_size + 1):
        benchmark_plan.append((record_count, run_number, False))

for record_count, run_number, is_warmup in benchmark_plan:
    started_at = metrics.utc_now()
    _, baseline_duration_ms = metrics.timed_call(
        lambda rc=record_count: _run_baseline(rc)
    )
    secured_run_id, secured_duration_ms = metrics.timed_call(
        lambda rc=record_count: _run_secured(rc)
    )
    _, verification_duration_ms = metrics.timed_call(
        lambda run_id=secured_run_id: _verify_run(run_id)
    )
    finished_at = metrics.utc_now()
    metric = metrics.create_metric(
        experiment_id=experiment_id,
        record_count=record_count,
        run_number=run_number,
        is_warmup=is_warmup,
        baseline_duration_ms=baseline_duration_ms,
        secured_duration_ms=secured_duration_ms,
        verification_duration_ms=verification_duration_ms,
        metadata_record_count=_metadata_record_count(secured_run_id),
        started_at=started_at,
        finished_at=finished_at,
    )
    all_metrics.append(metric)
    metrics.append_experiment_metrics(
        spark=spark,
        metrics_table=experiment_metrics_table,
        rows=[metric],
    )

experiment_metrics_df = spark.table(experiment_metrics_table)
metrics_df = experiment_metrics_df.where(
    experiment_metrics_df["experiment_id"] == experiment_id
)
display(metrics_df.orderBy("is_warmup", "record_count", "run_number"))
display(spark.createDataFrame(metrics.summarize_metrics(all_metrics)))
print(f"Experiment ID: {experiment_id}")
