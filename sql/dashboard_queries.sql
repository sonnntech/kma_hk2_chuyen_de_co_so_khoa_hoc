-- Dashboard queries for the blockchain pipeline MVP.
-- Default schema comes from config/demo_config.py.
-- If you changed CATALOG_NAME or SCHEMA_NAME, update these two statements.

USE CATALOG `workspace`;
USE SCHEMA `blockchain_pipeline_demo`;

-- KPI 1: Total pipeline runs captured by the ledger.
SELECT
    COUNT(DISTINCT pipeline_run_id) AS total_pipeline_runs
FROM blockchain_ledger;

-- KPI 2: Total ledger blocks.
SELECT
    COUNT(*) AS total_blocks
FROM blockchain_ledger;

-- KPI 3: Latest verification status counts.
WITH latest_results AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id, block_index
            ORDER BY verified_at DESC
        ) AS result_rank
    FROM verification_results
)
SELECT
    verification_status,
    COUNT(*) AS block_count
FROM latest_results
WHERE result_rank = 1
GROUP BY verification_status
ORDER BY block_count DESC, verification_status;

-- KPI 4: Successful verification blocks.
WITH latest_results AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id, block_index
            ORDER BY verified_at DESC
        ) AS result_rank
    FROM verification_results
)
SELECT
    COUNT(*) AS successful_verification_blocks
FROM latest_results
WHERE result_rank = 1
  AND verification_status = 'VALID';

-- KPI 5: Tamper events detected by latest verification results.
WITH latest_results AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id, block_index
            ORDER BY verified_at DESC
        ) AS result_rank
    FROM verification_results
)
SELECT
    verification_status,
    COUNT(*) AS detected_event_count
FROM latest_results
WHERE result_rank = 1
  AND verification_status <> 'VALID'
GROUP BY verification_status
ORDER BY detected_event_count DESC, verification_status;

-- KPI 6: First broken block for each affected pipeline run.
WITH latest_results AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id, block_index
            ORDER BY verified_at DESC
        ) AS result_rank
    FROM verification_results
),
broken_blocks AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id
            ORDER BY block_index
        ) AS broken_rank
    FROM latest_results
    WHERE result_rank = 1
      AND verification_status <> 'VALID'
)
SELECT
    pipeline_run_id,
    block_index AS first_broken_block_index,
    pipeline_stage AS first_broken_stage,
    table_name,
    verification_status,
    failure_reason,
    verified_at
FROM broken_blocks
WHERE broken_rank = 1
ORDER BY verified_at DESC;

-- KPI 7: Verification latency by pipeline run.
WITH latest_run_verification AS (
    SELECT
        pipeline_run_id,
        MAX(verified_at) AS verified_at
    FROM verification_results
    GROUP BY pipeline_run_id
),
ledger_bounds AS (
    SELECT
        pipeline_run_id,
        MIN(created_at) AS first_block_created_at,
        MAX(created_at) AS last_block_created_at,
        COUNT(*) AS block_count
    FROM blockchain_ledger
    GROUP BY pipeline_run_id
)
SELECT
    l.pipeline_run_id,
    l.block_count,
    l.first_block_created_at,
    l.last_block_created_at,
    v.verified_at,
    CAST(
        (unix_timestamp(v.verified_at) - unix_timestamp(l.last_block_created_at))
        * 1000 AS BIGINT
    ) AS verification_latency_ms
FROM ledger_bounds l
JOIN latest_run_verification v
  ON l.pipeline_run_id = v.pipeline_run_id
ORDER BY v.verified_at DESC;

-- KPI 8: Processing overhead by record count.
SELECT
    record_count,
    COUNT(*) AS measured_runs,
    AVG(baseline_duration_ms) AS avg_baseline_duration_ms,
    AVG(secured_duration_ms) AS avg_secured_duration_ms,
    AVG(verification_duration_ms) AS avg_verification_duration_ms,
    AVG(overhead_percent) AS avg_overhead_percent,
    percentile_approx(overhead_percent, 0.5) AS median_overhead_percent,
    AVG(metadata_record_count) AS avg_metadata_record_count
FROM experiment_metrics
WHERE is_warmup = false
GROUP BY record_count
ORDER BY record_count;

-- KPI 9: Experiment run details.
SELECT
    experiment_id,
    record_count,
    run_number,
    is_warmup,
    baseline_duration_ms,
    secured_duration_ms,
    verification_duration_ms,
    overhead_percent,
    metadata_record_count,
    started_at,
    finished_at
FROM experiment_metrics
ORDER BY started_at DESC, record_count, run_number;

-- KPI 10: Lineage flow SOURCE -> BRONZE -> SILVER -> GOLD.
SELECT
    pipeline_run_id,
    source_stage,
    target_stage,
    source_table,
    target_table,
    transformation_name,
    input_record_count,
    output_record_count,
    status,
    started_at,
    finished_at,
    error_message
FROM lineage_events
ORDER BY started_at DESC;

-- KPI 11: Stage-level ledger overview.
SELECT
    pipeline_run_id,
    block_index,
    pipeline_stage,
    target_table,
    record_count,
    batch_hash,
    previous_hash,
    block_hash,
    created_at
FROM blockchain_ledger
ORDER BY created_at DESC, block_index;

-- KPI 12: Detection accuracy proxy from latest verification results.
-- A clean run is counted as clean when all latest block results are VALID.
-- A detected tamper run is counted when any latest block result is non-VALID.
WITH latest_results AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY pipeline_run_id, block_index
            ORDER BY verified_at DESC
        ) AS result_rank
    FROM verification_results
),
run_status AS (
    SELECT
        pipeline_run_id,
        MAX(CASE WHEN verification_status <> 'VALID' THEN 1 ELSE 0 END)
            AS has_detected_issue
    FROM latest_results
    WHERE result_rank = 1
    GROUP BY pipeline_run_id
)
SELECT
    COUNT(*) AS verified_runs,
    SUM(has_detected_issue) AS runs_with_detected_issue,
    COUNT(*) - SUM(has_detected_issue) AS runs_without_detected_issue,
    CASE
        WHEN COUNT(*) = 0 THEN NULL
        ELSE SUM(has_detected_issue) * 100.0 / COUNT(*)
    END AS detected_issue_run_percent
FROM run_status;
