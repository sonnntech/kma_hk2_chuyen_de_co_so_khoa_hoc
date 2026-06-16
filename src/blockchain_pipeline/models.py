"""Data models for the blockchain verification ledger."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any

GENESIS_PREVIOUS_HASH = "0" * 64
PIPELINE_STAGES: tuple[str, ...] = ("SOURCE", "BRONZE", "SILVER", "GOLD")
BLOCK_PAYLOAD_COLUMNS: tuple[str, ...] = (
    "block_index",
    "block_id",
    "pipeline_run_id",
    "pipeline_stage",
    "source_table",
    "target_table",
    "record_count",
    "batch_hash",
    "previous_hash",
    "transformation",
    "schema_hash",
    "created_at",
)


@dataclass(frozen=True)
class LedgerBlock:
    """A single block in the pipeline verification ledger."""

    block_index: int
    block_id: str
    pipeline_run_id: str
    pipeline_stage: str
    source_table: str
    target_table: str
    record_count: int
    batch_hash: str
    previous_hash: str
    block_hash: str
    transformation: str
    schema_hash: str
    created_at: datetime

    def payload(self) -> dict[str, Any]:
        """Return the hash payload, excluding block_hash itself."""
        return {
            column: getattr(self, column)
            for column in BLOCK_PAYLOAD_COLUMNS
        }

    def as_record(self) -> dict[str, Any]:
        """Return a dictionary suitable for writing to Spark."""
        return asdict(self)
