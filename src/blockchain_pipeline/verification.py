"""Integrity verification engine for data, blocks, and hash-chain links."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Iterable, Sequence

from blockchain_pipeline.ledger import (
    compute_dataframe_batch_hash,
    recalculate_block_hash,
)
from blockchain_pipeline.models import GENESIS_PREVIOUS_HASH, LedgerBlock

LOGGER = logging.getLogger(__name__)

VALID = "VALID"
DATA_TAMPERED = "DATA_TAMPERED"
RECORD_COUNT_MISMATCH = "RECORD_COUNT_MISMATCH"
BLOCK_TAMPERED = "BLOCK_TAMPERED"
CHAIN_BROKEN = "CHAIN_BROKEN"
SOURCE_STAGE = "SOURCE"


@dataclass(frozen=True)
class VerificationResult:
    """Result of verifying one ledger block against current state."""

    pipeline_run_id: str
    block_index: int
    pipeline_stage: str
    table_name: str
    expected_hash: str
    actual_hash: str
    expected_record_count: int
    actual_record_count: int
    verification_status: str
    failure_reason: str | None
    verified_at: datetime

    def as_record(self) -> dict[str, Any]:
        """Return a dictionary suitable for Spark DataFrame creation."""
        return asdict(self)


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def verify_block(
    *,
    block: LedgerBlock,
    actual_batch_hash: str,
    actual_record_count: int,
    previous_block: LedgerBlock | None,
    verified_at: datetime | None = None,
) -> VerificationResult:
    """Verify one block's data hash, record count, block hash, and chain link."""
    if actual_record_count != block.record_count:
        return _result(
            block=block,
            actual_hash=actual_batch_hash,
            actual_record_count=actual_record_count,
            status=RECORD_COUNT_MISMATCH,
            reason=(
                "Expected record_count "
                f"{block.record_count}, got {actual_record_count}"
            ),
            verified_at=verified_at,
        )

    if actual_batch_hash != block.batch_hash:
        return _result(
            block=block,
            actual_hash=actual_batch_hash,
            actual_record_count=actual_record_count,
            status=DATA_TAMPERED,
            reason="Current batch hash does not match stored batch hash",
            verified_at=verified_at,
        )

    recalculated_block_hash = recalculate_block_hash(block)
    if recalculated_block_hash != block.block_hash:
        return _result(
            block=block,
            actual_hash=recalculated_block_hash,
            actual_record_count=actual_record_count,
            status=BLOCK_TAMPERED,
            reason="Recalculated block hash does not match stored block hash",
            verified_at=verified_at,
        )

    chain_reason = _chain_failure_reason(block, previous_block)
    if chain_reason is not None:
        expected_previous_hash = (
            GENESIS_PREVIOUS_HASH
            if previous_block is None
            else previous_block.block_hash
        )
        return _result(
            block=block,
            actual_hash=block.previous_hash,
            expected_hash=expected_previous_hash,
            actual_record_count=actual_record_count,
            status=CHAIN_BROKEN,
            reason=chain_reason,
            verified_at=verified_at,
        )

    return _result(
        block=block,
        actual_hash=actual_batch_hash,
        actual_record_count=actual_record_count,
        status=VALID,
        reason=None,
        verified_at=verified_at,
    )


def first_broken_block(
    results: Sequence[VerificationResult],
) -> VerificationResult | None:
    """Return the first non-VALID verification result by block index."""
    broken_results = [
        result for result in results if result.verification_status != VALID
    ]
    if not broken_results:
        return None
    return min(broken_results, key=lambda result: result.block_index)


def verify_chain_results(
    blocks: Sequence[LedgerBlock],
    current_hashes: dict[str, str],
    current_counts: dict[str, int],
    verified_at: datetime | None = None,
) -> list[VerificationResult]:
    """Verify a sequence of blocks with supplied current table state."""
    ordered_blocks = sorted(blocks, key=lambda block: block.block_index)
    results: list[VerificationResult] = []
    previous_block: LedgerBlock | None = None

    for block in ordered_blocks:
        table_name = block.target_table
        results.append(
            verify_block(
                block=block,
                actual_batch_hash=current_hashes[table_name],
                actual_record_count=current_counts[table_name],
                previous_block=previous_block,
                verified_at=verified_at,
            )
        )
        previous_block = block
    return results


def read_blocks_for_run(
    spark: Any,
    ledger_table: str,
    pipeline_run_id: str,
) -> list[LedgerBlock]:
    """Read all ledger blocks for a pipeline run ordered by block_index."""
    ledger_df = spark.table(ledger_table)
    rows = (
        ledger_df.where(ledger_df["pipeline_run_id"] == pipeline_run_id)
        .orderBy("block_index")
        .collect()
    )
    return [LedgerBlock(**row.asDict()) for row in rows]


def verify_pipeline_run(
    *,
    spark: Any,
    ledger_table: str,
    pipeline_run_id: str,
) -> list[VerificationResult]:
    """Verify all blocks for a pipeline run against current Delta tables."""
    blocks = read_blocks_for_run(
        spark=spark,
        ledger_table=ledger_table,
        pipeline_run_id=pipeline_run_id,
    )
    if not blocks:
        raise ValueError(f"No ledger blocks found for run {pipeline_run_id}")

    results: list[VerificationResult] = []
    previous_block: LedgerBlock | None = None
    verified_at = utc_now()

    for block in blocks:
        current_df = spark.table(block.target_table)
        actual_count = current_df.count()
        actual_hash = compute_dataframe_batch_hash(
            current_df,
            sort_columns=_default_sort_columns(block.pipeline_stage),
        )
        results.append(
            verify_block(
                block=block,
                actual_batch_hash=actual_hash,
                actual_record_count=actual_count,
                previous_block=previous_block,
                verified_at=verified_at,
            )
        )
        previous_block = block
    return results


def append_verification_results(
    spark: Any,
    results_table: str,
    results: Iterable[VerificationResult],
) -> None:
    """Append verification results to a managed Delta table."""
    from pyspark.sql.types import (  # pylint: disable=import-outside-toplevel
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    records = [result.as_record() for result in results]
    if not records:
        raise ValueError("results must not be empty")
    schema = StructType(
        [
            StructField("pipeline_run_id", StringType(), nullable=False),
            StructField("block_index", IntegerType(), nullable=False),
            StructField("pipeline_stage", StringType(), nullable=False),
            StructField("table_name", StringType(), nullable=False),
            StructField("expected_hash", StringType(), nullable=False),
            StructField("actual_hash", StringType(), nullable=False),
            StructField("expected_record_count", IntegerType(), nullable=False),
            StructField("actual_record_count", IntegerType(), nullable=False),
            StructField("verification_status", StringType(), nullable=False),
            StructField("failure_reason", StringType(), nullable=True),
            StructField("verified_at", TimestampType(), nullable=False),
        ]
    )
    LOGGER.info("Appending %s verification results to %s", len(records), results_table)
    spark.createDataFrame(records, schema=schema).write.format("delta").mode(
        "append"
    ).saveAsTable(results_table)


def _result(
    *,
    block: LedgerBlock,
    actual_hash: str,
    actual_record_count: int,
    status: str,
    reason: str | None,
    verified_at: datetime | None,
    expected_hash: str | None = None,
) -> VerificationResult:
    return VerificationResult(
        pipeline_run_id=block.pipeline_run_id,
        block_index=block.block_index,
        pipeline_stage=block.pipeline_stage,
        table_name=block.target_table,
        expected_hash=expected_hash
        or (block.block_hash if status == BLOCK_TAMPERED else block.batch_hash),
        actual_hash=actual_hash,
        expected_record_count=block.record_count,
        actual_record_count=actual_record_count,
        verification_status=status,
        failure_reason=reason,
        verified_at=verified_at or utc_now(),
    )


def _chain_failure_reason(
    block: LedgerBlock,
    previous_block: LedgerBlock | None,
) -> str | None:
    if previous_block is None:
        if block.block_index != 0:
            return "First block must have block_index 0"
        if block.pipeline_stage != SOURCE_STAGE:
            return "First block must be SOURCE"
        if block.previous_hash != GENESIS_PREVIOUS_HASH:
            return "Genesis block previous_hash is not 64 zero characters"
        return None

    if block.block_index != previous_block.block_index + 1:
        return "Block index does not follow previous block"
    if block.previous_hash != previous_block.block_hash:
        return "previous_hash does not match previous block_hash"
    return None


def _default_sort_columns(pipeline_stage: str) -> list[str] | None:
    if pipeline_stage in {"SOURCE", "BRONZE", "SILVER"}:
        return ["transaction_id"]
    if pipeline_stage == "GOLD":
        return ["transaction_date", "product"]
    return None
