"""Unit tests for lineage event creation."""

from datetime import datetime, timezone

import pytest

from blockchain_pipeline.lineage import (
    FAILED,
    SUCCESS,
    create_failed_event,
    create_lineage_event,
    create_success_event,
)

STARTED_AT = datetime(2026, 6, 17, 1, 0, 0, tzinfo=timezone.utc)
FINISHED_AT = datetime(2026, 6, 17, 1, 0, 5, tzinfo=timezone.utc)


def test_create_success_event_records_counts_hashes_and_status() -> None:
    event = create_success_event(
        pipeline_run_id="run-001",
        source_stage="BRONZE",
        target_stage="SILVER",
        source_table="bronze_transactions",
        target_table="silver_transactions",
        transformation_name="silver_transformation",
        transformation_description="Validate and deduplicate transactions",
        input_record_count=10,
        output_record_count=9,
        input_batch_hash="a" * 64,
        output_batch_hash="b" * 64,
        started_at=STARTED_AT,
        finished_at=FINISHED_AT,
    )

    assert event.status == SUCCESS
    assert event.error_message is None
    assert event.input_record_count == 10
    assert event.output_record_count == 9
    assert event.input_batch_hash == "a" * 64
    assert event.output_batch_hash == "b" * 64
    assert event.as_record()["target_stage"] == "SILVER"


def test_create_failed_event_records_error_message() -> None:
    event = create_failed_event(
        pipeline_run_id="run-001",
        source_stage="SILVER",
        target_stage="GOLD",
        source_table="silver_transactions",
        target_table="gold_daily_summary",
        transformation_name="gold_aggregation",
        transformation_description="Aggregate daily product totals",
        started_at=STARTED_AT,
        finished_at=FINISHED_AT,
        error_message="source table missing",
    )

    assert event.status == FAILED
    assert event.error_message == "source table missing"
    assert event.input_record_count == 0
    assert event.output_record_count == 0


def test_success_event_rejects_error_message() -> None:
    with pytest.raises(ValueError, match="SUCCESS"):
        create_lineage_event(
            pipeline_run_id="run-001",
            source_stage="SOURCE",
            target_stage="BRONZE",
            source_table="source_transactions",
            target_table="bronze_transactions",
            transformation_name="bronze_ingestion",
            transformation_description="Add metadata",
            input_record_count=1,
            output_record_count=1,
            input_batch_hash="a" * 64,
            output_batch_hash="b" * 64,
            started_at=STARTED_AT,
            finished_at=FINISHED_AT,
            status=SUCCESS,
            error_message="should not be set",
        )


def test_failed_event_requires_error_message() -> None:
    with pytest.raises(ValueError, match="FAILED"):
        create_lineage_event(
            pipeline_run_id="run-001",
            source_stage="SOURCE",
            target_stage="BRONZE",
            source_table="source_transactions",
            target_table="bronze_transactions",
            transformation_name="bronze_ingestion",
            transformation_description="Add metadata",
            input_record_count=1,
            output_record_count=0,
            input_batch_hash=None,
            output_batch_hash=None,
            started_at=STARTED_AT,
            finished_at=FINISHED_AT,
            status=FAILED,
        )
