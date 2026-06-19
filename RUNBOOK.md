# RUNBOOK

Hướng dẫn này chạy MVP từ đầu trên Databricks. Các notebook Python phải chạy trên
Databricks notebook compute hoặc serverless compute; SQL Warehouse chỉ dùng cho
dashboard SQL.

## 1. Clone repo vào Databricks

1. Mở Databricks workspace.
2. Vào **Workspace** hoặc **Repos**.
3. Chọn **Add Repo**.
4. Dán URL GitHub của repository.
5. Chọn branch cần chạy, ví dụ `main` hoặc branch task hiện tại.

## 2. Cấu hình catalog và schema

Mặc định trong `config/demo_config.py`:

```text
CATALOG_NAME = workspace
SCHEMA_NAME = blockchain_pipeline_demo
```

Nếu đổi catalog hoặc schema, sửa trong `config/demo_config.py` trước khi chạy.
Không sửa trực tiếp tên bảng trong notebook.

## 3. Thứ tự chạy notebook sạch

Chạy lần lượt bằng Python compute:

```text
notebooks/00_setup_environment.py
notebooks/01_generate_source_data.py
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
notebooks/05_verify_integrity.py
```

Kết quả kỳ vọng sau `05_verify_integrity.py`:

```text
SOURCE  VALID
BRONZE  VALID
SILVER  VALID
GOLD    VALID
```

Nếu widget `pipeline_run_id` để trống, notebook 05 tự chọn run mới nhất trong
`blockchain_ledger`.

## 4. Chạy kịch bản tamper

Chạy `notebooks/06_run_tamper_scenarios.py` bằng Python compute.

Widget cần đặt:

```text
SCENARIO = MODIFY_TRANSACTION_AMOUNT
CONFIRM_TAMPER = YES
PIPELINE_RUN_ID = để trống hoặc nhập run id cụ thể
```

Các scenario đang hỗ trợ:

```text
NONE
MODIFY_TRANSACTION_AMOUNT
DELETE_TRANSACTION
INSERT_FAKE_TRANSACTION
MODIFY_LEDGER_BATCH_HASH
MODIFY_LEDGER_TRANSFORMATION
MODIFY_LEDGER_PREVIOUS_HASH
RESET_BASELINE
```

Notebook sẽ hiển thị dữ liệu trước và sau khi sửa, chạy verification, rồi hiển
thị block lỗi đầu tiên.

## 5. Reset demo

Chạy lại `notebooks/06_run_tamper_scenarios.py` với:

```text
SCENARIO = RESET_BASELINE
CONFIRM_TAMPER = YES
```

Reset tạo một pipeline run sạch mới. Sau đó kết quả verification kỳ vọng là
`VALID` cho toàn bộ stage.

## 6. Chạy benchmark

Chạy `notebooks/07_experiment_and_metrics.py` bằng Python compute.

Widget mặc định:

```text
RECORD_COUNTS = 1000,5000,10000,50000
RUNS_PER_SIZE = 3
INCLUDE_WARMUP = YES
```

Notebook ghi kết quả thật vào `experiment_metrics`. Lần warm-up được đánh dấu
`is_warmup = true` và không dùng trong truy vấn summary chính.

## 7. Tạo dashboard

1. Mở Databricks SQL.
2. Tạo query mới.
3. Copy từng block truy vấn trong `sql/dashboard_queries.sql`.
4. Nếu đã đổi catalog/schema, sửa hai dòng:

```sql
USE CATALOG `workspace`;
USE SCHEMA `blockchain_pipeline_demo`;
```

5. Tạo visualization cho các KPI:

```text
total_pipeline_runs
total_blocks
successful_verification_blocks
detected_event_count
verification_latency_ms
avg_overhead_percent
lineage flow
first_broken_block
```

## 8. Lỗi thường gặp

`Unsupported cell during execution. SQL warehouses only support executing SQL cells.`

Nguyên nhân: đang chạy notebook Python bằng SQL Warehouse. Chuyển sang Python
notebook compute hoặc serverless compute.

`PARSE_SYNTAX_ERROR` tại dòng `import ...`

Nguyên nhân: cell Python bị chạy như SQL cell, thường do thêm `%sql` trước code
Python hoặc dùng SQL Warehouse. Bỏ `%sql` và chạy bằng Python compute.

`No ledger blocks found`

Nguyên nhân: chưa chạy đủ `02_bronze_ingestion.py`, `03_silver_transformation.py`
và `04_gold_aggregation.py`. Chạy lại pipeline theo đúng thứ tự.

`CANNOT_DETERMINE_TYPE`

Nguyên nhân thường gặp là Spark infer schema từ dữ liệu có nhiều giá trị null.
Code hiện dùng explicit schema cho verification và metrics; hãy pull code mới
nhất rồi chạy lại notebook.

Benchmark chạy lâu hoặc hết quota

Giữ kết quả từ các lần đã ghi vào `experiment_metrics`. Khi cần demo nhanh, dùng
dashboard trên kết quả đã có thay vì chạy lại benchmark đầy đủ.

## 9. Checklist chạy lại

- [ ] Đang dùng Python compute cho notebook 00-07.
- [ ] `config/demo_config.py` có catalog/schema đúng.
- [ ] Notebook 00 tạo schema thành công.
- [ ] Notebook 01 tạo `source_transactions`.
- [ ] Notebook 02-04 tạo đủ ledger blocks SOURCE, BRONZE, SILVER, GOLD.
- [ ] Notebook 05 trả về `VALID` cho run sạch.
- [ ] Notebook 06 phát hiện ít nhất một tamper scenario.
- [ ] Notebook 07 ghi số liệu thật vào `experiment_metrics`.
- [ ] Dashboard SQL đọc đúng schema và hiển thị KPI.
