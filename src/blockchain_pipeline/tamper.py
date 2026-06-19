"""Tamper scenarios and reset helpers for the Databricks demo."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from blockchain_pipeline import ledger
from blockchain_pipeline.verification import (
    BLOCK_TAMPERED,
    CHAIN_BROKEN,
    DATA_TAMPERED,
    RECORD_COUNT_MISMATCH,
    VALID,
)

SCENARIO_NONE = "NONE"
SCENARIO_MODIFY_TRANSACTION_AMOUNT = "MODIFY_TRANSACTION_AMOUNT"
SCENARIO_DELETE_TRANSACTION = "DELETE_TRANSACTION"
SCENARIO_INSERT_FAKE_TRANSACTION = "INSERT_FAKE_TRANSACTION"
SCENARIO_MODIFY_LEDGER_BATCH_HASH = "MODIFY_LEDGER_BATCH_HASH"
SCENARIO_MODIFY_LEDGER_TRANSFORMATION = "MODIFY_LEDGER_TRANSFORMATION"
SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH = "MODIFY_LEDGER_PREVIOUS_HASH"
SCENARIO_RESET_BASELINE = "RESET_BASELINE"
CONFIRM_VALUE = "YES"
FAKE_TRANSACTION_ID = "TX_FAKE_TAMPER_0001"

SCENARIOS: tuple[str, ...] = (
    SCENARIO_NONE,
    SCENARIO_MODIFY_TRANSACTION_AMOUNT,
    SCENARIO_DELETE_TRANSACTION,
    SCENARIO_INSERT_FAKE_TRANSACTION,
    SCENARIO_MODIFY_LEDGER_BATCH_HASH,
    SCENARIO_MODIFY_LEDGER_TRANSFORMATION,
    SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH,
    SCENARIO_RESET_BASELINE,
)


@dataclass(frozen=True)
class DemoTables:
    """Fully qualified table names used by tamper scenarios."""

    source: str
    bronze: str
    silver: str
    gold: str
    ledger: str
    verification_results: str


@dataclass(frozen=True)
class ScenarioPlan:
    """Resolved scenario target and expected verification behavior."""

    scenario: str
    pipeline_run_id: str
    target_table: str
    preview_predicate: str | None
    expected_status: str
    description: str


@dataclass(frozen=True)
class ScenarioExecution:
    """Result metadata after running a scenario."""

    plan: ScenarioPlan
    new_pipeline_run_id: str | None = None


def require_confirmation(scenario: str, confirm_tamper: str) -> None:
    """Require explicit confirmation before any mutating scenario runs."""
    if scenario == SCENARIO_NONE:
        return
    if confirm_tamper.strip().upper() != CONFIRM_VALUE:
        raise ValueError(
            f"Set CONFIRM_TAMPER to {CONFIRM_VALUE!r} before running {scenario}"
        )


def latest_pipeline_run_id(spark: Any, ledger_table: str) -> str:
    """Return the most recent pipeline_run_id from the ledger table."""
    row = (
        spark.table(ledger_table)
        .orderBy("created_at", ascending=False)
        .select("pipeline_run_id")
        .first()
    )
    if row is None:
        raise ValueError("No pipeline run found in blockchain ledger")
    return str(row["pipeline_run_id"])


def build_scenario_plan(
    spark: Any,
    scenario: str,
    tables: DemoTables,
    pipeline_run_id: str | None = None,
) -> ScenarioPlan:
    """Build a concrete plan for the selected scenario."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Unsupported scenario: {scenario}")

    run_id = pipeline_run_id or latest_pipeline_run_id(spark, tables.ledger)
    if scenario == SCENARIO_NONE:
        return ScenarioPlan(
            scenario=scenario,
            pipeline_run_id=run_id,
            target_table=tables.ledger,
            preview_predicate=f"pipeline_run_id = '{run_id}'",
            expected_status=VALID,
            description="No data is modified; verification should remain VALID.",
        )
    if scenario == SCENARIO_MODIFY_TRANSACTION_AMOUNT:
        transaction_id = _first_transaction_id(spark, tables.silver)
        return ScenarioPlan(
            scenario=scenario,
            pipeline_run_id=run_id,
            target_table=tables.silver,
            preview_predicate=f"transaction_id = '{transaction_id}'",
            expected_status=DATA_TAMPERED,
            description="Increase amount for one Silver transaction.",
        )
    if scenario == SCENARIO_DELETE_TRANSACTION:
        transaction_id = _first_transaction_id(spark, tables.silver)
        return ScenarioPlan(
            scenario=scenario,
            pipeline_run_id=run_id,
            target_table=tables.silver,
            preview_predicate=f"transaction_id = '{transaction_id}'",
            expected_status=RECORD_COUNT_MISMATCH,
            description="Delete one Silver transaction.",
        )
    if scenario == SCENARIO_INSERT_FAKE_TRANSACTION:
        return ScenarioPlan(
            scenario=scenario,
            pipeline_run_id=run_id,
            target_table=tables.silver,
            preview_predicate=f"transaction_id = '{FAKE_TRANSACTION_ID}'",
            expected_status=RECORD_COUNT_MISMATCH,
            description="Insert one synthetic fake Silver transaction.",
        )
    if scenario == SCENARIO_MODIFY_LEDGER_BATCH_HASH:
        return _ledger_plan(
            scenario=scenario,
            run_id=run_id,
            tables=tables,
            expected_status=DATA_TAMPERED,
            description="Change the stored Silver batch_hash in the ledger.",
        )
    if scenario == SCENARIO_MODIFY_LEDGER_TRANSFORMATION:
        return _ledger_plan(
            scenario=scenario,
            run_id=run_id,
            tables=tables,
            expected_status=BLOCK_TAMPERED,
            description="Change the Silver block transformation metadata.",
        )
    if scenario == SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH:
        return _ledger_plan(
            scenario=scenario,
            run_id=run_id,
            tables=tables,
            expected_status=CHAIN_BROKEN,
            description="Change Silver previous_hash and recompute block_hash.",
        )

    return ScenarioPlan(
        scenario=scenario,
        pipeline_run_id=run_id,
        target_table=tables.ledger,
        preview_predicate=f"pipeline_run_id = '{run_id}'",
        expected_status=VALID,
        description="Reset demo data by creating a new clean pipeline run.",
    )


def preview_plan(spark: Any, plan: ScenarioPlan) -> Any:
    """Return rows that will be affected by a scenario plan."""
    dataframe = spark.table(plan.target_table)
    if plan.preview_predicate:
        return dataframe.where(plan.preview_predicate)
    return dataframe


def run_scenario(
    spark: Any,
    plan: ScenarioPlan,
    tables: DemoTables,
    *,
    record_count: int,
    random_seed: int,
    source_system: str,
) -> ScenarioExecution:
    """Run one selected scenario."""
    if plan.scenario == SCENARIO_NONE:
        return ScenarioExecution(plan=plan)
    if plan.scenario == SCENARIO_MODIFY_TRANSACTION_AMOUNT:
        modify_transaction_amount(spark, plan)
    elif plan.scenario == SCENARIO_DELETE_TRANSACTION:
        delete_transaction(spark, plan)
    elif plan.scenario == SCENARIO_INSERT_FAKE_TRANSACTION:
        insert_fake_transaction(spark, plan)
    elif plan.scenario == SCENARIO_MODIFY_LEDGER_BATCH_HASH:
        modify_ledger_batch_hash(spark, plan, tables.ledger)
    elif plan.scenario == SCENARIO_MODIFY_LEDGER_TRANSFORMATION:
        modify_ledger_transformation(spark, plan, tables.ledger)
    elif plan.scenario == SCENARIO_MODIFY_LEDGER_PREVIOUS_HASH:
        modify_ledger_previous_hash(spark, plan, tables.ledger)
    elif plan.scenario == SCENARIO_RESET_BASELINE:
        new_run_id = reset_clean_baseline(
            spark=spark,
            tables=tables,
            record_count=record_count,
            random_seed=random_seed,
            source_system=source_system,
        )
        return ScenarioExecution(plan=plan, new_pipeline_run_id=new_run_id)
    else:
        raise ValueError(f"Unsupported scenario: {plan.scenario}")
    return ScenarioExecution(plan=plan)


def modify_transaction_amount(spark: Any, plan: ScenarioPlan) -> None:
    """Modify amount for one Silver transaction."""
    spark.sql(
        f"""
        UPDATE {plan.target_table}
        SET amount = CAST(amount + 1.00 AS DECIMAL(18, 2))
        WHERE {plan.preview_predicate}
        """
    )


def delete_transaction(spark: Any, plan: ScenarioPlan) -> None:
    """Delete one Silver transaction."""
    spark.sql(f"DELETE FROM {plan.target_table} WHERE {plan.preview_predicate}")


def insert_fake_transaction(spark: Any, plan: ScenarioPlan) -> None:
    """Insert one fake Silver transaction."""
    spark.sql(
        f"""
        INSERT INTO {plan.target_table}
        SELECT
            '{FAKE_TRANSACTION_ID}' AS transaction_id,
            'CUS_FAKE' AS customer_id,
            current_timestamp() AS transaction_time,
            'Tamper Product' AS product,
            CAST(1 AS INT) AS quantity,
            CAST(99.99 AS DECIMAL(18, 2)) AS unit_price,
            CAST(99.99 AS DECIMAL(18, 2)) AS amount,
            'TAMPER_DEMO' AS source_system,
            '{plan.pipeline_run_id}' AS pipeline_run_id,
            current_timestamp() AS ingestion_time,
            'tamper_scenario' AS source_table
        """
    )


def modify_ledger_batch_hash(spark: Any, plan: ScenarioPlan, ledger_table: str) -> None:
    """Change batch_hash for the Silver block and keep block_hash self-consistent."""
    block = ledger.read_stage_block(
        spark=spark,
        ledger_table=ledger_table,
        pipeline_run_id=plan.pipeline_run_id,
        pipeline_stage="SILVER",
    )
    replacement = ledger.create_ledger_block(
        block_index=block.block_index,
        block_id=block.block_id,
        pipeline_run_id=block.pipeline_run_id,
        pipeline_stage=block.pipeline_stage,
        source_table=block.source_table,
        target_table=block.target_table,
        record_count=block.record_count,
        batch_hash="f" * 64,
        previous_hash=block.previous_hash,
        transformation=block.transformation,
        schema_hash=block.schema_hash,
        created_at=block.created_at,
    )
    _update_ledger_block(spark, ledger_table, replacement)


def modify_ledger_transformation(
    spark: Any,
    plan: ScenarioPlan,
    ledger_table: str,
) -> None:
    """Change transformation metadata without updating block_hash."""
    spark.sql(
        f"""
        UPDATE {ledger_table}
        SET transformation = 'tampered transformation metadata'
        WHERE pipeline_run_id = '{plan.pipeline_run_id}'
          AND pipeline_stage = 'SILVER'
        """
    )


def modify_ledger_previous_hash(
    spark: Any,
    plan: ScenarioPlan,
    ledger_table: str,
) -> None:
    """Change previous_hash and recompute block_hash to demonstrate chain break."""
    block = ledger.read_stage_block(
        spark=spark,
        ledger_table=ledger_table,
        pipeline_run_id=plan.pipeline_run_id,
        pipeline_stage="SILVER",
    )
    replacement = ledger.create_ledger_block(
        block_index=block.block_index,
        block_id=block.block_id,
        pipeline_run_id=block.pipeline_run_id,
        pipeline_stage=block.pipeline_stage,
        source_table=block.source_table,
        target_table=block.target_table,
        record_count=block.record_count,
        batch_hash=block.batch_hash,
        previous_hash="f" * 64,
        transformation=block.transformation,
        schema_hash=block.schema_hash,
        created_at=block.created_at,
    )
    _update_ledger_block(spark, ledger_table, replacement)


def reset_clean_baseline(
    *,
    spark: Any,
    tables: DemoTables,
    record_count: int,
    random_seed: int,
    source_system: str,
) -> str:
    """Rebuild clean data tables and append a new valid SOURCE->GOLD chain."""
    from blockchain_pipeline import pipeline, source_data

    pipeline_run_id = str(uuid4())
    created_at = datetime.now(timezone.utc)

    source = source_data.build_source_transactions(
        spark=spark,
        record_count=record_count,
        random_seed=random_seed,
        source_system=source_system,
    )
    pipeline.overwrite_delta_table(source, tables.source)
    source = spark.table(tables.source)

    bronze = pipeline.run_bronze(
        spark=spark,
        source_table=tables.source,
        bronze_table=tables.bronze,
        pipeline_run_id=pipeline_run_id,
    )
    silver = pipeline.run_silver(
        spark=spark,
        bronze_table=tables.bronze,
        silver_table=tables.silver,
    )
    gold = pipeline.run_gold(
        spark=spark,
        silver_table=tables.silver,
        gold_table=tables.gold,
    )

    source_block = ledger.create_block_for_dataframe(
        dataframe=source,
        pipeline_run_id=pipeline_run_id,
        pipeline_stage="SOURCE",
        source_table=tables.source,
        target_table=tables.source,
        transformation="Reset baseline source snapshot",
        created_at=created_at,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, tables.ledger, source_block)
    bronze_block = ledger.create_block_for_dataframe(
        dataframe=bronze,
        pipeline_run_id=pipeline_run_id,
        pipeline_stage="BRONZE",
        source_table=tables.source,
        target_table=tables.bronze,
        transformation="Reset baseline Bronze ingestion",
        created_at=created_at,
        previous_block=source_block,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, tables.ledger, bronze_block)
    silver_block = ledger.create_block_for_dataframe(
        dataframe=silver,
        pipeline_run_id=pipeline_run_id,
        pipeline_stage="SILVER",
        source_table=tables.bronze,
        target_table=tables.silver,
        transformation="Reset baseline Silver transformation",
        created_at=created_at,
        previous_block=bronze_block,
        sort_columns=["transaction_id"],
    )
    ledger.append_block_if_missing(spark, tables.ledger, silver_block)
    gold_block = ledger.create_block_for_dataframe(
        dataframe=gold,
        pipeline_run_id=pipeline_run_id,
        pipeline_stage="GOLD",
        source_table=tables.silver,
        target_table=tables.gold,
        transformation="Reset baseline Gold aggregation",
        created_at=created_at,
        previous_block=silver_block,
        sort_columns=["transaction_date", "product"],
    )
    ledger.append_block_if_missing(spark, tables.ledger, gold_block)
    return pipeline_run_id


def _first_transaction_id(spark: Any, table_name: str) -> str:
    row = spark.table(table_name).orderBy("transaction_id").select(
        "transaction_id"
    ).first()
    if row is None:
        raise ValueError(f"No transactions found in {table_name}")
    return str(row["transaction_id"])


def _ledger_plan(
    *,
    scenario: str,
    run_id: str,
    tables: DemoTables,
    expected_status: str,
    description: str,
) -> ScenarioPlan:
    return ScenarioPlan(
        scenario=scenario,
        pipeline_run_id=run_id,
        target_table=tables.ledger,
        preview_predicate=(
            f"pipeline_run_id = '{run_id}' AND pipeline_stage = 'SILVER'"
        ),
        expected_status=expected_status,
        description=description,
    )


def _update_ledger_block(spark: Any, ledger_table: str, block: Any) -> None:
    spark.sql(
        f"""
        UPDATE {ledger_table}
        SET
            batch_hash = '{block.batch_hash}',
            previous_hash = '{block.previous_hash}',
            block_hash = '{block.block_hash}',
            transformation = '{block.transformation}'
        WHERE pipeline_run_id = '{block.pipeline_run_id}'
          AND pipeline_stage = '{block.pipeline_stage}'
        """
    )
