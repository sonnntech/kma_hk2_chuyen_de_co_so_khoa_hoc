# KMA HK2 – Chuyên đề cơ sở khoa học

## Nghiên cứu xây dựng mô hình ứng dụng Blockchain nhằm đảm bảo tính toàn vẹn và truy vết dữ liệu trong hệ thống Data Pipeline

Repository này dùng để xây dựng mô hình thử nghiệm phục vụ chuyên đề tại trường.

Mục tiêu của demo:

- Xây dựng Data Pipeline trên Databricks theo luồng Source → Bronze → Silver → Gold.
- Tạo giá trị kiểm chứng SHA-256 tại từng giai đoạn.
- Ghi nhận lịch sử xử lý và data lineage.
- Liên kết các bản ghi kiểm chứng bằng `previous_hash` và `block_hash`.
- Phát hiện dữ liệu bị sửa, xóa, chèn thêm hoặc lịch sử kiểm chứng bị thay đổi.
- Đo thời gian xử lý và chi phí phát sinh khi bổ sung cơ chế kiểm chứng.

> MVP là mô hình `tamper-evident`: giúp phát hiện thay đổi. Đây chưa phải blockchain phi tập trung hoàn chỉnh như Ethereum.

---

## 1. Kiến trúc đề xuất

```text
Source CSV / Generated Data
            │
            ▼
┌─────────────────────┐
│ Bronze Delta Table  │
│ Raw data + metadata │
└──────────┬──────────┘
           │ SHA-256
           ▼
┌─────────────────────┐
│ Silver Delta Table  │
│ Cleaned data        │
└──────────┬──────────┘
           │ SHA-256
           ▼
┌─────────────────────┐
│ Gold Delta Table    │
│ Aggregated data     │
└──────────┬──────────┘
           ▼
┌──────────────────────────────────┐
│ Blockchain Verification Ledger   │
│ batch_hash                       │
│ previous_hash                    │
│ block_hash                       │
│ pipeline_run_id                  │
│ source_table / target_table      │
│ transformation / record_count    │
└──────────┬───────────────────────┘
           ▼
┌──────────────────────────────────┐
│ Integrity Verification          │
│ VALID / TAMPERED / CHAIN_BROKEN │
└──────────────────────────────────┘
```

---

## 2. Công nghệ

| Thành phần | Công nghệ |
|---|---|
| Nền tảng | Databricks Free Edition |
| Ngôn ngữ | Python, PySpark, SQL |
| Lưu trữ | Delta Table |
| Hàm băm | SHA-256 |
| Blockchain MVP | Hash chain bằng Python |
| Data lineage | Metadata tables tự xây dựng |
| Dashboard | Databricks SQL |
| Source control | GitHub |

Không sử dụng dữ liệu thật hoặc dữ liệu nhạy cảm trong môi trường demo.

---

## 3. Cấu trúc repository dự kiến

```text
.
├── README.md
├── requirements.txt
├── .gitignore
├── config/
│   └── demo_config.py
├── notebooks/
│   ├── 00_setup_environment.py
│   ├── 01_generate_source_data.py
│   ├── 02_bronze_ingestion.py
│   ├── 03_silver_transformation.py
│   ├── 04_gold_aggregation.py
│   ├── 05_verify_integrity.py
│   ├── 06_run_tamper_scenarios.py
│   └── 07_experiment_and_metrics.py
├── src/
│   └── blockchain_pipeline/
│       ├── __init__.py
│       ├── canonicalization.py
│       ├── hashing.py
│       ├── ledger.py
│       ├── lineage.py
│       ├── verification.py
│       ├── metrics.py
│       └── schemas.py
├── sql/
│   ├── dashboard_queries.sql
│   └── tamper_scenarios.sql
└── tests/
    ├── test_canonicalization.py
    ├── test_hashing.py
    ├── test_ledger.py
    └── test_verification.py
```

Notebook `.py` phải dùng định dạng Databricks notebook source:

```python
# Databricks notebook source
```

---

## 4. Dataset thử nghiệm

Tạo dữ liệu giao dịch giả lập với các cột:

| Cột | Kiểu dữ liệu | Ý nghĩa |
|---|---|---|
| `transaction_id` | string | Mã giao dịch duy nhất |
| `customer_id` | string | Mã khách hàng giả lập |
| `transaction_time` | timestamp | Thời gian giao dịch |
| `product` | string | Sản phẩm |
| `quantity` | integer | Số lượng |
| `unit_price` | decimal | Đơn giá |
| `amount` | decimal | Thành tiền |
| `source_system` | string | Hệ thống nguồn |

Cấu hình mặc định:

```text
Số bản ghi: 10.000
Random seed: 42
Source system: SCHOOL_DEMO
```

---

## 5. Các bảng cần tạo

Schema mặc định:

```text
blockchain_pipeline_demo
```

Các bảng:

```text
source_transactions
bronze_transactions
silver_transactions
gold_daily_summary
blockchain_ledger
lineage_events
verification_results
experiment_metrics
```

Tên catalog và schema phải đặt trong `config/demo_config.py`, không hard-code ở nhiều nơi.

---

## 6. Xử lý từng tầng

### Source

Sinh dữ liệu giao dịch giả lập có thể tái lập bằng random seed cố định.

### Bronze

Lưu dữ liệu gần với nguồn và bổ sung:

```text
pipeline_run_id
source_file
source_system
ingestion_time
row_hash
```

### Silver

Thực hiện:

- Loại bỏ trùng theo `transaction_id`.
- Kiểm tra trường bắt buộc.
- Chuẩn hóa timestamp và decimal.
- Tính lại `amount = quantity × unit_price`.
- Tạo `row_hash` mới sau biến đổi.

### Gold

Tổng hợp theo ngày và sản phẩm:

```text
transaction_date
product
total_quantity
total_revenue
transaction_count
```

---

## 7. Canonicalization và SHA-256

Cùng một dữ liệu phải luôn tạo ra cùng một chuỗi trước khi hash.

Quy tắc:

1. Dùng thứ tự cột cố định.
2. Chuyển `null` thành chuỗi `<NULL>`.
3. Timestamp dùng định dạng ISO-8601 thống nhất.
4. Decimal dùng scale cố định.
5. Dùng ký tự phân tách cố định.
6. Sắp xếp bản ghi theo khóa ổn định.
7. Không phụ thuộc thứ tự partition của Spark.

Ví dụ canonical record:

```text
TX000001|CUS0005|2026-06-14T08:30:00Z|Laptop|2|1500.00|3000.00|SCHOOL_DEMO
```

Công thức:

```text
row_hash = SHA256(canonical_record)
```

Batch hash:

```text
Chuẩn hóa từng bản ghi
    ↓
Tính row_hash
    ↓
Sắp xếp row_hash
    ↓
Ghép theo thứ tự xác định
    ↓
SHA-256
    ↓
batch_hash
```

Hàm cần xây dựng:

```python
def canonicalize_value(value, data_type=None) -> str:
    ...


def canonicalize_record(record: dict, ordered_columns: list[str]) -> str:
    ...


def compute_row_hash(...):
    ...


def compute_batch_hash(df, ordered_columns, sort_columns):
    ...
```

Với dữ liệu lớn, không nên đưa toàn bộ dữ liệu về driver. Hướng mở rộng là hash theo partition hoặc sử dụng Merkle Tree.

---

## 8. Blockchain ledger

Bảng `blockchain_ledger` gồm:

| Cột | Ý nghĩa |
|---|---|
| `block_index` | Số thứ tự block |
| `block_id` | UUID của block |
| `pipeline_run_id` | Mã lần chạy pipeline |
| `pipeline_stage` | SOURCE, BRONZE, SILVER hoặc GOLD |
| `source_table` | Bảng nguồn |
| `target_table` | Bảng đích |
| `record_count` | Số bản ghi |
| `batch_hash` | Hash đại diện cho dữ liệu |
| `previous_hash` | Hash của block trước |
| `block_hash` | Hash của block hiện tại |
| `transformation` | Mô tả phép biến đổi |
| `schema_hash` | Hash của schema |
| `created_at` | Thời gian tạo |

Genesis block dùng `previous_hash` gồm 64 ký tự `0`.

```text
block_hash = SHA256(
    block_index
    + block_id
    + pipeline_run_id
    + pipeline_stage
    + source_table
    + target_table
    + record_count
    + batch_hash
    + previous_hash
    + transformation
    + schema_hash
    + created_at
)
```

Tất cả trường phải được canonicalize trước khi tạo `block_hash`.

---

## 9. Data lineage

Bảng `lineage_events` ghi nhận:

```text
event_id
pipeline_run_id
source_stage
target_stage
source_table
target_table
transformation_name
transformation_description
input_record_count
output_record_count
input_batch_hash
output_batch_hash
started_at
finished_at
status
error_message
```

Luồng lineage mong đợi:

```text
SOURCE → BRONZE → SILVER → GOLD
```

---

## 10. Integrity verification

Notebook `05_verify_integrity.py` thực hiện:

### Kiểm tra dữ liệu

```text
current_batch_hash == stored_batch_hash
```

### Kiểm tra nội dung block

```text
recalculated_block_hash == stored_block_hash
```

### Kiểm tra liên kết chuỗi

```text
current.previous_hash == previous.block_hash
```

Trạng thái kết quả:

```text
VALID
DATA_TAMPERED
RECORD_COUNT_MISMATCH
BLOCK_TAMPERED
CHAIN_BROKEN
```

Kết quả được lưu vào `verification_results` cùng:

```text
pipeline_run_id
block_index
pipeline_stage
table_name
expected_hash
actual_hash
expected_record_count
actual_record_count
verification_status
failure_reason
verified_at
```

---

## 11. Kịch bản demo

Notebook `06_run_tamper_scenarios.py` cần hỗ trợ:

1. Pipeline hợp lệ: tất cả stage trả về `VALID`.
2. Sửa giá trị một giao dịch: trả về `DATA_TAMPERED`.
3. Xóa một giao dịch: trả về `RECORD_COUNT_MISMATCH` và `DATA_TAMPERED`.
4. Chèn thêm giao dịch giả: trả về `RECORD_COUNT_MISMATCH` và `DATA_TAMPERED`.
5. Thay đổi metadata của block: trả về `BLOCK_TAMPERED`.
6. Thay đổi liên kết block: trả về `CHAIN_BROKEN` và vị trí block lỗi đầu tiên.

Mỗi kịch bản phải có khả năng reset dữ liệu để chạy lại demo.

---

## 12. Thực nghiệm

Thử với các kích thước:

```text
1.000
5.000
10.000
50.000 bản ghi
```

Mỗi cấu hình chạy tối thiểu ba lần.

Đo:

```text
baseline_pipeline_duration_ms
secured_pipeline_duration_ms
verification_duration_ms
overhead_percent
```

Công thức overhead:

```text
Overhead (%) =
(secured duration - baseline duration)
/ baseline duration
× 100
```

Detection accuracy:

```text
Số kịch bản phát hiện đúng / Tổng số kịch bản thử nghiệm
```

Kết quả lưu vào `experiment_metrics`.

---

## 13. Dashboard

Các KPI và biểu đồ cần có:

- Tổng số pipeline run.
- Tổng số block.
- Số lần kiểm chứng thành công.
- Số lần phát hiện thay đổi.
- Tỷ lệ phát hiện đúng.
- Verification latency theo số bản ghi.
- Processing overhead theo số bản ghi.
- Luồng SOURCE → BRONZE → SILVER → GOLD.
- Block đầu tiên bị phá vỡ.
- Lịch sử verification theo thời gian.

SQL đặt tại `sql/dashboard_queries.sql`.

---

## 14. Trình tự chạy demo

```text
1. 00_setup_environment
2. 01_generate_source_data
3. 02_bronze_ingestion
4. 03_silver_transformation
5. 04_gold_aggregation
6. 05_verify_integrity
7. Xác nhận tất cả trạng thái VALID
8. Chạy một tamper scenario
9. Chạy lại 05_verify_integrity
10. Hiển thị stage và block bị lỗi
11. Trình bày dashboard và kết quả thực nghiệm
```

---

## 15. Yêu cầu chất lượng code

- Python có type hints và docstring.
- Không hard-code catalog, schema và table name trong logic.
- Hàm nhỏ, rõ trách nhiệm.
- Có logging và xử lý lỗi.
- Logic Python thuần nằm trong `src/`; notebook chủ yếu điều phối.
- Hash phải deterministic.
- Unit test không phụ thuộc Databricks khi không cần thiết.
- Mỗi notebook mô tả rõ input, output và expected result.

Unit test cần kiểm tra:

- Canonicalization của null, decimal và timestamp.
- Cùng dữ liệu tạo cùng hash.
- Thay đổi dữ liệu làm hash thay đổi.
- Thứ tự dòng không làm batch hash thay đổi sau khi chuẩn hóa.
- Genesis block và liên kết block.
- Phát hiện block bị sửa và chain bị đứt.

---

## 16. Tiêu chí nghiệm thu MVP

- [ ] Sinh được dữ liệu giả lập có thể tái lập.
- [ ] Chạy được Source → Bronze → Silver → Gold.
- [ ] Sinh được `row_hash` và `batch_hash`.
- [ ] Ghi được block theo từng stage.
- [ ] Liên kết block bằng `previous_hash`.
- [ ] Ghi được data lineage.
- [ ] Kiểm chứng được dữ liệu từng stage.
- [ ] Phát hiện được sửa, xóa và chèn dữ liệu.
- [ ] Phát hiện được block bị sửa và chain bị đứt.
- [ ] Có bảng số liệu thực nghiệm.
- [ ] Có dashboard queries.
- [ ] Có unit test cho logic chính.

---

## 17. Giới hạn nghiên cứu

Mô hình MVP có các giới hạn:

- Ledger và dữ liệu có thể nằm trong cùng một workspace.
- Người có toàn quyền quản trị có thể sửa cả dữ liệu và ledger.
- SHA-256 giúp phát hiện thay đổi nhưng không tự ngăn chặn thay đổi.
- Chưa có consensus giữa nhiều node.
- Chưa sử dụng smart contract thật.
- Lineage chủ yếu ở mức pipeline và table.

Cách kết luận phù hợp:

> Mô hình cung cấp khả năng phát hiện thay đổi và hỗ trợ truy vết dữ liệu; không khẳng định dữ liệu tuyệt đối không thể bị sửa.

Hướng phát triển:

- Lưu checkpoint hash lên Ethereum testnet.
- Dùng smart contract để lưu hash.
- Dùng Merkle Tree.
- Tách ledger sang hệ thống độc lập.
- Ký số block.
- Tích hợp Airflow, DataHub hoặc OpenLineage.

---

## 18. Kế hoạch bốn tuần

### Tuần 1

- Tạo môi trường Databricks.
- Sinh dữ liệu.
- Xây dựng Source, Bronze, Silver, Gold.

### Tuần 2

- Xây dựng canonicalization.
- Tạo row hash và batch hash.
- Xây dựng blockchain ledger.

### Tuần 3

- Xây dựng verification và lineage.
- Chạy các kịch bản thay đổi dữ liệu.

### Tuần 4

- Đo hiệu năng và overhead.
- Tạo dashboard.
- Hoàn thiện báo cáo và kịch bản trình bày.

---

## 19. Trình tự giao việc cho Codex

Không tạo toàn bộ project trong một lần. Thực hiện theo từng task nhỏ:

1. Scaffold project và tạo dữ liệu nguồn.
2. Canonicalization và hashing.
3. Bronze, Silver và Gold notebooks.
4. Blockchain ledger.
5. Data lineage và verification.
6. Tamper scenarios.
7. Experiment metrics và dashboard.

### Prompt Codex cho Task 1

```text
Bạn đang làm việc trong repository:
sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc

Hãy đọc toàn bộ README.md trước khi thay đổi code.

Chỉ thực hiện Task 1 – Scaffold project, không triển khai trước các task khác.

Mục tiêu:
1. Tạo cấu trúc project Python cho demo Databricks.
2. Tạo config/demo_config.py chứa catalog, schema, random seed và số bản ghi.
3. Tạo schemas.py định nghĩa schema giao dịch bằng PySpark StructType.
4. Tạo Databricks notebook 00_setup_environment.py để tạo schema và các bảng cần thiết nếu chưa tồn tại.
5. Tạo Databricks notebook 01_generate_source_data.py để sinh 10.000 giao dịch giả lập với random seed 42 và lưu vào source_transactions.
6. Tạo requirements.txt và .gitignore phù hợp.

Ràng buộc:
- Notebook phải dùng định dạng Databricks notebook source.
- Không hard-code catalog và schema ở nhiều file.
- Không dùng dữ liệu cá nhân thật.
- Python có type hints và docstring.
- Chưa triển khai hash, blockchain ledger hoặc verification.
- Cuối cùng liệt kê file đã tạo, cách chạy và các giả định.
```

---

## 20. Kết quả kỳ vọng

Demo cuối cùng cần trả lời được:

1. Dữ liệu có bị thay đổi sau khi đi qua pipeline hay không?
2. Thay đổi xảy ra ở stage nào?
3. Pipeline run nào liên quan?
4. Bảng nào bị ảnh hưởng?
5. Block nào không hợp lệ đầu tiên?
6. Lịch sử biến đổi dữ liệu là gì?
7. Chi phí hiệu năng của cơ chế kiểm chứng là bao nhiêu?

Kết luận kỹ thuật mong đợi:

> Việc kết hợp SHA-256, metadata lineage và chuỗi block liên kết bằng hash có thể tạo ra cơ chế kiểm chứng giúp phát hiện thay đổi và hỗ trợ truy vết dữ liệu trong Data Pipeline. Mô hình thử nghiệm cho phép đánh giá khả năng phát hiện sai lệch và chi phí hiệu năng trước khi mở rộng sang blockchain hoặc smart contract thực tế.
