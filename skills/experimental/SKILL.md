---
name: blockchain-pipeline-mvp
description: Project skill for the Databricks blockchain pipeline MVP. Use when working in this repository on Source -> Bronze -> Silver -> Gold pipeline tasks, deterministic hashing, blockchain verification ledger, data lineage, integrity verification, tamper scenarios, benchmarks, dashboard queries, runbook, or debugging Databricks notebook execution for this project.
---

# Blockchain Pipeline MVP

Use this skill to work on the KMA Databricks MVP for tamper-evident data
pipelines. The project demonstrates Source -> Bronze -> Silver -> Gold
processing, deterministic SHA-256 hashes, a hash-linked verification ledger,
lineage, verification, tamper scenarios, benchmark metrics, and dashboard docs.

## Core Rules

1. Read `README.md` before changing project behavior.
2. Read the relevant reference file from `skills/reference/` for the active task.
3. Work on a task-specific branch; do not make feature work directly on `main`.
4. Keep each task scoped. Do not implement future tasks early.
5. Put reusable logic in `src/blockchain_pipeline/`.
6. Keep notebooks as Databricks source notebooks that orchestrate functions and
   display results.
7. Centralize catalog, schema, table names, seed, and record count in
   `config/demo_config.py`.
8. Do not use personal, secret, or sensitive data.
9. Prefer deterministic hashing and stable ordering; avoid relying on Spark
   partition order.
10. Make reruns safe: avoid uncontrolled appends and duplicate demo data.
11. Add or update focused tests for important pure-Python rules.
12. Do not change hashing, ledger, or verification semantics unless the active
    task or a verified bug requires it.

## Reference Map

Read only the files needed for the current request:

- `reference/00-working-rules.md`: branch names, per-task workflow, debug/review
  prompts, and full-project Definition of Done.
- `reference/01-foundation-and-pipeline.md`: Tasks 01-03, project scaffold,
  synthetic source data, and Medallion pipeline.
- `reference/02-integrity-ledger-lineage.md`: Tasks 04-07,
  canonicalization/hashing, ledger, lineage, and verification engine.
- `reference/03-demo-metrics-documentation.md`: Tasks 08-10, tamper scenarios,
  benchmark metrics, dashboard, runbook, and demo docs.

## Standard Workflow

1. Confirm the active task number and scope.
2. Inspect the current repo state with `git status --short --branch`.
3. Read `README.md` and the relevant reference file.
4. Identify files to create or edit.
5. Implement the smallest coherent change.
6. Run targeted tests or explain why they cannot run locally.
7. For notebook work, state the exact Databricks notebook order to verify.
8. Summarize changed files, verification, and remaining Databricks manual checks.

## Databricks Notes

- Python notebooks must run on Databricks notebook/serverless compute, not SQL
  Warehouse.
- SQL Warehouse is appropriate for `sql/dashboard_queries.sql`.
- If a notebook reports `Unsupported cell during execution. SQL warehouses only
  support executing SQL cells`, switch compute type.
- If Python code is parsed as SQL, remove `%sql` from the Python cell and run on
  Python compute.

## Expected Final Project Shape

```text
config/demo_config.py
notebooks/00_setup_environment.py
notebooks/01_generate_source_data.py
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
notebooks/05_verify_integrity.py
notebooks/06_run_tamper_scenarios.py
notebooks/07_experiment_and_metrics.py
src/blockchain_pipeline/
sql/dashboard_queries.sql
sql/tamper_scenarios.sql
RUNBOOK.md
DEMO_SCRIPT.md
tests/
```
