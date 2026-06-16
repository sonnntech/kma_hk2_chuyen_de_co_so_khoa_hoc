"""Unit tests for blockchain ledger block creation."""

from dataclasses import replace
from datetime import datetime, timezone

import pytest

from blockchain_pipeline.ledger import (
    block_payload_is_unchanged,
    canonicalize_block_payload,
    create_stage_block,
    recalculate_block_hash,
)
from blockchain_pipeline.models import (
    GENESIS_PREVIOUS_HASH,
    PIPELINE_STAGES,
    LedgerBlock,
)

FIXED_CREATED_AT = datetime(2026, 6, 16, 1, 2, 3, tzinfo=timezone.utc)
FIXED_BATCH_HASH = "a" * 64
FIXED_SCHEMA_HASH = "b" * 64


def _create_block(
    stage: str,
    previous_block: LedgerBlock | None = None,
) -> LedgerBlock:
    return create_stage_block(
        pipeline_run_id="run-001",
        pipeline_stage=stage,
        source_table=f"{stage.lower()}_source",
        target_table=f"{stage.lower()}_target",
        record_count=10,
        batch_hash=FIXED_BATCH_HASH,
        transformation=f"{stage} transform",
        schema_hash=FIXED_SCHEMA_HASH,
        created_at=FIXED_CREATED_AT,
        previous_block=previous_block,
        block_id=f"block-{stage.lower()}",
    )


def test_source_block_uses_genesis_previous_hash() -> None:
    source = _create_block("SOURCE")

    assert source.block_index == 0
    assert source.previous_hash == GENESIS_PREVIOUS_HASH
    assert block_payload_is_unchanged(source)


def test_stage_blocks_link_in_expected_order() -> None:
    blocks: list[LedgerBlock] = []
    previous: LedgerBlock | None = None

    for stage in PIPELINE_STAGES:
        current = _create_block(stage, previous)
        blocks.append(current)
        previous = current

    assert [block.pipeline_stage for block in blocks] == list(PIPELINE_STAGES)
    assert [block.block_index for block in blocks] == [0, 1, 2, 3]
    assert blocks[1].previous_hash == blocks[0].block_hash
    assert blocks[2].previous_hash == blocks[1].block_hash
    assert blocks[3].previous_hash == blocks[2].block_hash


def test_block_hash_is_deterministic_from_canonical_payload() -> None:
    first = _create_block("SOURCE")
    second = _create_block("SOURCE")

    assert canonicalize_block_payload(first.payload()) == (
        canonicalize_block_payload(second.payload())
    )
    assert first.block_hash == second.block_hash


def test_changed_payload_invalidates_existing_block_hash() -> None:
    block = _create_block("SOURCE")
    tampered = replace(block, record_count=11)

    assert recalculate_block_hash(tampered) != block.block_hash
    assert not block_payload_is_unchanged(tampered)


def test_non_source_requires_previous_block() -> None:
    with pytest.raises(ValueError, match="Only SOURCE"):
        _create_block("BRONZE")


def test_rejects_out_of_order_stage() -> None:
    source = _create_block("SOURCE")

    with pytest.raises(ValueError, match="Expected next stage BRONZE"):
        _create_block("SILVER", source)
