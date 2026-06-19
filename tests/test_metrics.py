"""Unit tests for experiment metric calculations."""

from datetime import datetime, timezone

import pytest

from blockchain_pipeline.metrics import (
    calculate_overhead_percent,
    create_metric,
    summarize_metrics,
)

STARTED_AT = datetime(2026, 6, 19, 1, 0, 0, tzinfo=timezone.utc)
FINISHED_AT = datetime(2026, 6, 19, 1, 0, 5, tzinfo=timezone.utc)


def test_calculate_overhead_percent() -> None:
    assert calculate_overhead_percent(100, 125) == 25.0
    assert calculate_overhead_percent(200, 150) == -25.0


def test_calculate_overhead_rejects_zero_baseline() -> None:
    with pytest.raises(ValueError, match="greater than zero"):
        calculate_overhead_percent(0, 100)


def test_create_metric_calculates_overhead() -> None:
    metric = create_metric(
        experiment_id="exp-1",
        record_count=1000,
        run_number=1,
        is_warmup=False,
        baseline_duration_ms=100,
        secured_duration_ms=130,
        verification_duration_ms=20,
        metadata_record_count=8,
        started_at=STARTED_AT,
        finished_at=FINISHED_AT,
    )

    assert metric.overhead_percent == 30.0
    assert metric.as_record()["metadata_record_count"] == 8


def test_summarize_metrics_ignores_warmup() -> None:
    warmup = create_metric(
        experiment_id="exp-1",
        record_count=1000,
        run_number=0,
        is_warmup=True,
        baseline_duration_ms=100,
        secured_duration_ms=500,
        verification_duration_ms=50,
        metadata_record_count=8,
        started_at=STARTED_AT,
        finished_at=FINISHED_AT,
    )
    measured = create_metric(
        experiment_id="exp-1",
        record_count=1000,
        run_number=1,
        is_warmup=False,
        baseline_duration_ms=100,
        secured_duration_ms=125,
        verification_duration_ms=20,
        metadata_record_count=8,
        started_at=STARTED_AT,
        finished_at=FINISHED_AT,
    )

    summary = summarize_metrics([warmup, measured])

    assert summary == [
        {
            "record_count": 1000,
            "run_count": 1,
            "avg_baseline_duration_ms": 100.0,
            "avg_secured_duration_ms": 125.0,
            "avg_verification_duration_ms": 20.0,
            "avg_overhead_percent": 25.0,
            "median_overhead_percent": 25.0,
        }
    ]
