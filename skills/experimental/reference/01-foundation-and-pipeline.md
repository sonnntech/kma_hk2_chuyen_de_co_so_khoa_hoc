# Tasks 01-03: Foundation, Source Data, and Pipeline

Use this reference for scaffold, generated source data, and Medallion pipeline
work.

## Task 01 - Project Scaffold

### Goal

Create a Python/Databricks project structure that can be imported locally and
run from Databricks notebooks.

### Branch

```text
feature/task-01-project-scaffold
```

### Files

```text
requirements.txt
.gitignore
config/demo_config.py
src/blockchain_pipeline/__init__.py
src/blockchain_pipeline/schemas.py
notebooks/00_setup_environment.py
tests/__init__.py
```

### Requirements

- Central config for catalog, schema, random seed, and record count.
- PySpark `StructType` for transaction data.
- Notebook creates schema and empty Delta tables.
- Notebook must start with `# Databricks notebook source`.
- Do not implement hashing or blockchain yet.

### Acceptance

- `blockchain_pipeline` imports successfully.
- `00_setup_environment.py` runs on Databricks.
- Schema `blockchain_pipeline_demo` is created.
- Catalog/schema are not hard-coded across many files.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 01 – Khởi tạo cấu trúc project.
Không triển khai hashing, ledger, lineage hoặc verification.

Yêu cầu:
- Tạo đúng các file được liệt kê trong Task 01.
- Notebook phải có dòng đầu: # Databricks notebook source
- Cấu hình catalog, schema, seed và record count đặt trong config/demo_config.py.
- schemas.py định nghĩa StructType cho dữ liệu giao dịch.
- 00_setup_environment.py tạo schema và các Delta Table rỗng nếu chưa tồn tại.
- Python có type hints, docstring và logging cơ bản.
- Cuối cùng liệt kê file đã tạo, cách chạy và các giả định.
```

## Task 02 - Synthetic Source Data

### Goal

Create reproducible fake transaction data for the whole demo.

### Branch

```text
feature/task-02-source-data
```

### Files

```text
notebooks/01_generate_source_data.py
src/blockchain_pipeline/data_generator.py
tests/test_data_generator.py
```

The implemented project may name the reusable source module
`source_data.py`; follow existing repo names when continuing work.

### Requirements

- Generate 10,000 transactions by default.
- Use random seed `42`.
- Include transaction, customer, product, quantity, price, amount, and source
  system.
- Do not use real data.
- Support record count through widget or config.
- Write to `source_transactions`.

### Acceptance

- Same seed creates the same logical dataset.
- `transaction_id` is unique.
- `amount = quantity * unit_price`.
- `source_transactions` has the configured row count.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 02 – Sinh dữ liệu nguồn giả lập.

Yêu cầu:
- Tạo data_generator.py chứa logic Python/PySpark có thể tái sử dụng.
- Tạo notebook 01_generate_source_data.py để sinh dữ liệu và ghi vào source_transactions.
- Mặc định 10.000 dòng, random seed 42.
- Không dùng dữ liệu cá nhân thật.
- transaction_id phải duy nhất.
- amount phải bằng quantity nhân unit_price.
- Có unit test cho tính deterministic và tính hợp lệ cơ bản.
- Không triển khai hashing hoặc blockchain.
```

## Task 03 - Source -> Bronze -> Silver -> Gold

### Goal

Build the Medallion pipeline before adding blockchain features.

### Branch

```text
feature/task-03-medallion-pipeline
```

### Files

```text
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
src/blockchain_pipeline/pipeline.py
tests/test_pipeline_rules.py
```

### Bronze Requirements

- Read `source_transactions`.
- Add `pipeline_run_id`, `ingestion_time`, and `source_table`.
- Write `bronze_transactions`.

### Silver Requirements

- Deduplicate by `transaction_id`.
- Validate required fields.
- Normalize timestamp and decimal types.
- Recalculate `amount`.
- Write `silver_transactions`.

### Gold Requirements

- Aggregate by `transaction_date` and `product`.
- Calculate total quantity, total revenue, and transaction count.
- Write `gold_daily_summary`.

### Acceptance

- Three notebooks run in sequence.
- Bronze has required metadata.
- Silver has no duplicate transactions.
- Gold aggregates correctly.
- Reruns do not create uncontrolled duplicate appends.

### Prompt

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 03 – Xây dựng Source → Bronze → Silver → Gold.

Yêu cầu:
- Logic xử lý đặt trong src/blockchain_pipeline/pipeline.py.
- Notebook chỉ gọi hàm và hiển thị kết quả.
- Bronze thêm pipeline_run_id, ingestion_time và source_table.
- Silver deduplicate, validate, chuẩn hóa kiểu dữ liệu và tính lại amount.
- Gold tổng hợp theo ngày và sản phẩm.
- Thiết kế chạy lại an toàn, tránh append trùng không kiểm soát.
- Có test cho quy tắc Silver và Gold.
- Chưa triển khai hash, ledger hoặc verification.
```
