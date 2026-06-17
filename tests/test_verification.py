"""Unit tests for integrity verification statuses."""

from dataclasses import replace
from datetime import datetime, timezone

from blockchain_pipeline.ledger import create_ledger_block, create_stage_block
from blockchain_pipeline.models import LedgerBlock
from blockchain_pipeline.verification import (
    BLOCK_TAMPERED,
    CHAIN_BROKEN,
    DATA_TAMPERED,
    RECORD_COUNT_MISMATCH,
    VALID,
    first_broken_block,
    verify_block,
)

CREATED_AT = datetime(2026, 6, 17, 1, 2, 3, tzinfo=timezone.utc)
VERIFIED_AT = datetime(2026, 6, 17, 1, 3, 0, tzinfo=timezone.utc)
BATCH_HASH = "a" * 64
SCHEMA_HASH = "b" * 64


def _block(
    stage: str = "SOURCE",
    previous_block: LedgerBlock | None = None,
) -> LedgerBlock:
    return create_stage_block(
        pipeline_run_id="run-001",
        pipeline_stage=stage,
        source_table=f"{stage.lower()}_source",
        target_table=f"{stage.lower()}_target",
        record_count=10,
        batch_hash=BATCH_HASH,
        transformation=f"{stage} transform",
        schema_hash=SCHEMA_HASH,
        created_at=CREATED_AT,
        previous_block=previous_block,
        block_id=f"block-{stage.lower()}",
    )


def test_valid_block_returns_valid_status() -> None:
    block = _block()

    result = verify_block(
        block=block,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=10,
        previous_block=None,
        verified_at=VERIFIED_AT,
    )

    assert result.verification_status == VALID
    assert result.failure_reason is None


def test_record_count_mismatch_status() -> None:
    block = _block()

    result = verify_block(
        block=block,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=9,
        previous_block=None,
        verified_at=VERIFIED_AT,
    )

    assert result.verification_status == RECORD_COUNT_MISMATCH
    assert result.expected_record_count == 10
    assert result.actual_record_count == 9


def test_data_tampered_status() -> None:
    block = _block()

    result = verify_block(
        block=block,
        actual_batch_hash="c" * 64,
        actual_record_count=10,
        previous_block=None,
        verified_at=VERIFIED_AT,
    )

    assert result.verification_status == DATA_TAMPERED


def test_block_tampered_status() -> None:
    block = replace(_block(), transformation="changed metadata")

    result = verify_block(
        block=block,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=10,
        previous_block=None,
        verified_at=VERIFIED_AT,
    )

    assert result.verification_status == BLOCK_TAMPERED


def test_chain_broken_status() -> None:
    source = _block()
    broken_bronze = create_ledger_block(
        block_index=1,
        pipeline_run_id="run-001",
        pipeline_stage="BRONZE",
        source_table="bronze_source",
        target_table="bronze_target",
        record_count=10,
        batch_hash=BATCH_HASH,
        previous_hash="f" * 64,
        transformation="BRONZE transform",
        schema_hash=SCHEMA_HASH,
        created_at=CREATED_AT,
        block_id="block-bronze",
    )

    result = verify_block(
        block=broken_bronze,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=10,
        previous_block=source,
        verified_at=VERIFIED_AT,
    )

    assert result.verification_status == CHAIN_BROKEN
    assert result.expected_hash == source.block_hash
    assert result.actual_hash == "f" * 64


def test_first_broken_block_returns_lowest_broken_index() -> None:
    source = _block()
    broken_bronze = create_ledger_block(
        block_index=1,
        pipeline_run_id="run-001",
        pipeline_stage="BRONZE",
        source_table="bronze_source",
        target_table="bronze_target",
        record_count=10,
        batch_hash=BATCH_HASH,
        previous_hash="f" * 64,
        transformation="BRONZE transform",
        schema_hash=SCHEMA_HASH,
        created_at=CREATED_AT,
        block_id="block-bronze",
    )
    valid = verify_block(
        block=source,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=10,
        previous_block=None,
        verified_at=VERIFIED_AT,
    )
    broken = verify_block(
        block=broken_bronze,
        actual_batch_hash=BATCH_HASH,
        actual_record_count=10,
        previous_block=source,
        verified_at=VERIFIED_AT,
    )

    assert first_broken_block([broken, valid]) == broken
