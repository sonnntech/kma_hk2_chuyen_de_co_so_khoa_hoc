"""Data lineage event helpers for pipeline stage execution."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

LOGGER = logging.getLogger(__name__)
SUCCESS = "SUCCESS"
FAILED = "FAILED"
VALID_STATUSES = {SUCCESS, FAILED}


@dataclass(frozen=True)
class LineageEvent:
    """A lineage event describing one pipeline stage transition."""

    event_id: str
    pipeline_run_id: str
    source_stage: str
    target_stage: str
    source_table: str
    target_table: str
    transformation_name: str
    transformation_description: str
    input_record_count: int
    output_record_count: int
    input_batch_hash: str | None
    output_batch_hash: str | None
    started_at: datetime
    finished_at: datetime
    status: str
    error_message: str | None

    def as_record(self) -> dict[str, Any]:
        """Return a dictionary suitable for Spark DataFrame creation."""
        return asdict(self)


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def create_lineage_event(
    *,
    pipeline_run_id: str,
    source_stage: str,
    target_stage: str,
    source_table: str,
    target_table: str,
    transformation_name: str,
    transformation_description: str,
    input_record_count: int,
    output_record_count: int,
    input_batch_hash: str | None,
    output_batch_hash: str | None,
    started_at: datetime,
    finished_at: datetime,
    status: str,
    error_message: str | None = None,
    event_id: str | None = None,
) -> LineageEvent:
    """Create a validated lineage event."""
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported lineage status: {status}")
    if input_record_count < 0 or output_record_count < 0:
        raise ValueError("record counts must be non-negative")
    if status == SUCCESS and error_message:
        raise ValueError("SUCCESS lineage events must not have error_message")
    if status == FAILED and not error_message:
        raise ValueError("FAILED lineage events require error_message")

    return LineageEvent(
        event_id=event_id or str(uuid4()),
        pipeline_run_id=pipeline_run_id,
        source_stage=source_stage,
        target_stage=target_stage,
        source_table=source_table,
        target_table=target_table,
        transformation_name=transformation_name,
        transformation_description=transformation_description,
        input_record_count=input_record_count,
        output_record_count=output_record_count,
        input_batch_hash=input_batch_hash,
        output_batch_hash=output_batch_hash,
        started_at=started_at,
        finished_at=finished_at,
        status=status,
        error_message=error_message,
    )


def create_success_event(
    *,
    pipeline_run_id: str,
    source_stage: str,
    target_stage: str,
    source_table: str,
    target_table: str,
    transformation_name: str,
    transformation_description: str,
    input_record_count: int,
    output_record_count: int,
    input_batch_hash: str,
    output_batch_hash: str,
    started_at: datetime,
    finished_at: datetime,
) -> LineageEvent:
    """Create a successful lineage event."""
    return create_lineage_event(
        pipeline_run_id=pipeline_run_id,
        source_stage=source_stage,
        target_stage=target_stage,
        source_table=source_table,
        target_table=target_table,
        transformation_name=transformation_name,
        transformation_description=transformation_description,
        input_record_count=input_record_count,
        output_record_count=output_record_count,
        input_batch_hash=input_batch_hash,
        output_batch_hash=output_batch_hash,
        started_at=started_at,
        finished_at=finished_at,
        status=SUCCESS,
    )


def create_failed_event(
    *,
    pipeline_run_id: str,
    source_stage: str,
    target_stage: str,
    source_table: str,
    target_table: str,
    transformation_name: str,
    transformation_description: str,
    started_at: datetime,
    error_message: str,
    input_record_count: int = 0,
    output_record_count: int = 0,
    input_batch_hash: str | None = None,
    output_batch_hash: str | None = None,
    finished_at: datetime | None = None,
) -> LineageEvent:
    """Create a failed lineage event with an error message."""
    return create_lineage_event(
        pipeline_run_id=pipeline_run_id,
        source_stage=source_stage,
        target_stage=target_stage,
        source_table=source_table,
        target_table=target_table,
        transformation_name=transformation_name,
        transformation_description=transformation_description,
        input_record_count=input_record_count,
        output_record_count=output_record_count,
        input_batch_hash=input_batch_hash,
        output_batch_hash=output_batch_hash,
        started_at=started_at,
        finished_at=finished_at or utc_now(),
        status=FAILED,
        error_message=error_message,
    )


def append_lineage_event(
    spark: Any,
    lineage_table: str,
    event: LineageEvent,
) -> None:
    """Append one lineage event to the managed Delta lineage table."""
    from pyspark.sql.types import (  # pylint: disable=import-outside-toplevel
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    if not lineage_table.strip():
        raise ValueError("lineage_table must not be empty")
    LOGGER.info(
        "Appending lineage event run=%s %s->%s status=%s",
        event.pipeline_run_id,
        event.source_stage,
        event.target_stage,
        event.status,
    )
    schema = StructType(
        [
            StructField("event_id", StringType(), nullable=False),
            StructField("pipeline_run_id", StringType(), nullable=False),
            StructField("source_stage", StringType(), nullable=False),
            StructField("target_stage", StringType(), nullable=False),
            StructField("source_table", StringType(), nullable=False),
            StructField("target_table", StringType(), nullable=False),
            StructField("transformation_name", StringType(), nullable=False),
            StructField(
                "transformation_description", StringType(), nullable=False
            ),
            StructField("input_record_count", IntegerType(), nullable=False),
            StructField("output_record_count", IntegerType(), nullable=False),
            StructField("input_batch_hash", StringType(), nullable=True),
            StructField("output_batch_hash", StringType(), nullable=True),
            StructField("started_at", TimestampType(), nullable=False),
            StructField("finished_at", TimestampType(), nullable=False),
            StructField("status", StringType(), nullable=False),
            StructField("error_message", StringType(), nullable=True),
        ]
    )
    spark.createDataFrame([event.as_record()], schema=schema).write.format(
        "delta"
    ).mode("append").saveAsTable(lineage_table)


def safe_append_lineage_event(
    spark: Any,
    lineage_table: str,
    event: LineageEvent,
) -> None:
    """Append lineage and log failures without hiding the original pipeline error."""
    try:
        append_lineage_event(spark=spark, lineage_table=lineage_table, event=event)
    except Exception:
        LOGGER.exception("Unable to append lineage event")
