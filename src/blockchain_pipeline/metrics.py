"""Benchmark helpers for pipeline experiment metrics."""

from __future__ import annotations

import logging
import statistics
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import Any, Callable, Iterable, Sequence, TypeVar

LOGGER = logging.getLogger(__name__)
T = TypeVar("T")
DEFAULT_RECORD_COUNTS: tuple[int, ...] = (1_000, 5_000, 10_000, 50_000)
DEFAULT_RUNS_PER_SIZE = 3


@dataclass(frozen=True)
class ExperimentMetric:
    """One benchmark measurement row."""

    experiment_id: str
    record_count: int
    run_number: int
    is_warmup: bool
    baseline_duration_ms: int
    secured_duration_ms: int
    verification_duration_ms: int
    overhead_percent: float
    metadata_record_count: int
    started_at: datetime
    finished_at: datetime

    def as_record(self) -> dict[str, Any]:
        """Return a dictionary suitable for Spark DataFrame creation."""
        return asdict(self)


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def calculate_overhead_percent(
    baseline_duration_ms: int,
    secured_duration_ms: int,
) -> float:
    """Calculate processing overhead percentage."""
    if baseline_duration_ms <= 0:
        raise ValueError("baseline_duration_ms must be greater than zero")
    return (
        (secured_duration_ms - baseline_duration_ms)
        / baseline_duration_ms
        * 100.0
    )


def timed_call(function: Callable[[], T]) -> tuple[T, int]:
    """Run a function and return its result plus elapsed duration in ms."""
    start = time.perf_counter()
    result = function()
    elapsed_ms = int((time.perf_counter() - start) * 1000)
    return result, max(elapsed_ms, 1)


def create_metric(
    *,
    experiment_id: str,
    record_count: int,
    run_number: int,
    is_warmup: bool,
    baseline_duration_ms: int,
    secured_duration_ms: int,
    verification_duration_ms: int,
    metadata_record_count: int,
    started_at: datetime,
    finished_at: datetime,
) -> ExperimentMetric:
    """Create one metric row and calculate overhead."""
    return ExperimentMetric(
        experiment_id=experiment_id,
        record_count=record_count,
        run_number=run_number,
        is_warmup=is_warmup,
        baseline_duration_ms=baseline_duration_ms,
        secured_duration_ms=secured_duration_ms,
        verification_duration_ms=verification_duration_ms,
        overhead_percent=calculate_overhead_percent(
            baseline_duration_ms,
            secured_duration_ms,
        ),
        metadata_record_count=metadata_record_count,
        started_at=started_at,
        finished_at=finished_at,
    )


def summarize_metrics(metrics: Sequence[ExperimentMetric]) -> list[dict[str, Any]]:
    """Summarize non-warmup metrics by record_count."""
    grouped: dict[int, list[ExperimentMetric]] = {}
    for metric in metrics:
        if metric.is_warmup:
            continue
        grouped.setdefault(metric.record_count, []).append(metric)

    summaries: list[dict[str, Any]] = []
    for record_count, rows in sorted(grouped.items()):
        summaries.append(
            {
                "record_count": record_count,
                "run_count": len(rows),
                "avg_baseline_duration_ms": statistics.fmean(
                    row.baseline_duration_ms for row in rows
                ),
                "avg_secured_duration_ms": statistics.fmean(
                    row.secured_duration_ms for row in rows
                ),
                "avg_verification_duration_ms": statistics.fmean(
                    row.verification_duration_ms for row in rows
                ),
                "avg_overhead_percent": statistics.fmean(
                    row.overhead_percent for row in rows
                ),
                "median_overhead_percent": statistics.median(
                    row.overhead_percent for row in rows
                ),
            }
        )
    return summaries


def append_experiment_metrics(
    spark: Any,
    metrics_table: str,
    rows: Iterable[ExperimentMetric],
) -> None:
    """Append experiment metric rows to a managed Delta table."""
    records = [row.as_record() for row in rows]
    if not records:
        raise ValueError("rows must not be empty")
    LOGGER.info("Appending %s experiment metrics to %s", len(records), metrics_table)
    spark.createDataFrame(records, schema=_experiment_metric_schema()).write.format(
        "delta"
    ).mode("append").saveAsTable(metrics_table)


def _experiment_metric_schema() -> Any:
    """Return Spark schema for experiment metrics."""
    from pyspark.sql.types import (  # pylint: disable=import-outside-toplevel
        BooleanType,
        DoubleType,
        IntegerType,
        StringType,
        StructField,
        StructType,
        TimestampType,
    )

    return StructType(
        [
            StructField("experiment_id", StringType(), nullable=False),
            StructField("record_count", IntegerType(), nullable=False),
            StructField("run_number", IntegerType(), nullable=False),
            StructField("is_warmup", BooleanType(), nullable=False),
            StructField("baseline_duration_ms", IntegerType(), nullable=False),
            StructField("secured_duration_ms", IntegerType(), nullable=False),
            StructField("verification_duration_ms", IntegerType(), nullable=False),
            StructField("overhead_percent", DoubleType(), nullable=False),
            StructField("metadata_record_count", IntegerType(), nullable=False),
            StructField("started_at", TimestampType(), nullable=False),
            StructField("finished_at", TimestampType(), nullable=False),
        ]
    )
