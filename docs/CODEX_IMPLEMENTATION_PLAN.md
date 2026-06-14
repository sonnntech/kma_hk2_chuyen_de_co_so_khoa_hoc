# Codex Implementation Plan

## Mục tiêu

Tài liệu này chia dự án thành các task nhỏ để Codex triển khai tuần tự, dễ kiểm tra trên GitHub và Databricks.

Nguyên tắc chính:

- Mỗi task chỉ giải quyết một nhóm chức năng.
- Mỗi task dùng một branch riêng.
- Codex phải đọc `README.md` và tài liệu này trước khi sửa code.
- Không làm trước nội dung của task sau.
- Mỗi task phải có kiểm thử và tiêu chí nghiệm thu rõ ràng.
- Chỉ merge khi notebook chạy được trên Databricks và code review đạt yêu cầu.

---

## 1. Quy trình làm việc chuẩn

```text
GitHub main
   ↓
Tạo branch task riêng
   ↓
Giao prompt cho Codex
   ↓
Codex phân tích và lập kế hoạch ngắn
   ↓
Codex sửa code
   ↓
Chạy unit test cục bộ
   ↓
Push branch và tạo Pull Request
   ↓
Review file thay đổi
   ↓
Pull branch vào Databricks Git Folder
   ↓
Chạy notebook kiểm thử
   ↓
Ghi kết quả test vào Pull Request
   ↓
Merge vào main
```

Quy ước branch:

```text
feature/task-01-scaffold
feature/task-02-canonicalization-hashing
feature/task-03-medallion-pipeline
feature/task-04-blockchain-ledger
feature/task-05-lineage-verification
feature/task-06-tamper-scenarios
feature/task-07-experiment-dashboard
```

Quy ước commit:

```text
feat: ...
fix: ...
test: ...
docs: ...
refactor: ...
```

---

## 2. Definition of Done chung

Một task chỉ được xem là hoàn thành khi:

- Code đúng phạm vi task.
- Không hard-code catalog và schema ở nhiều nơi.
- Có type hints và docstring cho hàm public.
- Có logging và xử lý lỗi phù hợp.
- Unit test liên quan chạy thành công.
- Notebook có mô tả input, output và expected result.
- Không chứa token, mật khẩu hoặc dữ liệu nhạy cảm.
- Codex liệt kê file đã tạo hoặc sửa.
- Codex giải thích cách chạy.
- Codex nêu rõ giả định và giới hạn.
- Đã chạy thử trên Databricks trước khi merge.

---

# Task 01 – Scaffold project và dữ liệu nguồn

## Mục tiêu

Tạo bộ khung dự án, cấu hình dùng chung và notebook sinh dữ liệu giao dịch giả lập.

## Branch

```text
feature/task-01-scaffold
```

## File cần tạo

```text
requirements.txt
.gitignore
config/__init__.py
config/demo_config.py
src/blockchain_pipeline/__init__.py
src/blockchain_pipeline/schemas.py
notebooks/00_setup_environment.py
notebooks/01_generate_source_data.py
tests/__init__.py
```

## Yêu cầu chức năng

- Cấu hình catalog, schema, random seed và số bản ghi tại một nơi.
- Tạo schema `blockchain_pipeline_demo` nếu chưa tồn tại.
- Tạo 10.000 giao dịch giả lập với seed `42`.
- Lưu dữ liệu vào bảng `source_transactions`.
- Dữ liệu không chứa thông tin cá nhân thật.
- Notebook phải có định dạng Databricks source.

## Tiêu chí nghiệm thu

- `00_setup_environment.py` chạy không lỗi nhiều lần.
- `01_generate_source_data.py` sinh đúng 10.000 bản ghi.
- Hai lần chạy cùng seed tạo cùng dữ liệu logic.
- `transaction_id` là duy nhất.
- `amount = quantity × unit_price`.

## Prompt cho Codex

```text
Bạn đang làm việc trong repository sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc.

Hãy đọc toàn bộ README.md và docs/CODEX_IMPLEMENTATION_PLAN.md.
Chỉ thực hiện Task 01 – Scaffold project và dữ liệu nguồn.
Không triển khai hashing, blockchain ledger, lineage hoặc verification.

Trước khi sửa code:
1. Tóm tắt cách hiểu của bạn về Task 01.
2. Liệt kê file sẽ tạo hoặc sửa.
3. Nêu các giả định về Databricks Free Edition.

Sau đó triển khai đúng phạm vi, chạy kiểm tra phù hợp và cuối cùng báo cáo:
- File đã tạo hoặc sửa.
- Cách chạy trong Databricks.
- Kết quả kiểm tra.
- Hạn chế còn lại.
```

---

# Task 02 – Canonicalization và hashing

## Mục tiêu

Tạo cơ chế chuẩn hóa dữ liệu và sinh hash có tính xác định.

## Branch

```text
feature/task-02-canonicalization-hashing
```

## File cần tạo

```text
src/blockchain_pipeline/canonicalization.py
src/blockchain_pipeline/hashing.py
tests/test_canonicalization.py
tests/test_hashing.py
```

## Yêu cầu chức năng

- Chuẩn hóa `null`, string, integer, decimal và timestamp.
- Dùng thứ tự cột cố định.
- Escape ký tự phân cách.
- Tạo `row_hash` bằng SHA-256.
- Tạo `batch_hash` không phụ thuộc thứ tự partition Spark.
- Không thu toàn bộ dataset lớn về driver.
- Với MVP có thể dùng giải pháp đơn giản cho dataset nhỏ nhưng phải ghi rõ giới hạn.

## Hàm kỳ vọng

```python
def canonicalize_value(value, data_type=None) -> str:
    ...


def canonicalize_record(record: dict, ordered_columns: list[str]) -> str:
    ...


def compute_sha256(value: str) -> str:
    ...


def add_row_hash(df, ordered_columns):
    ...


def compute_batch_hash(df, hash_column="row_hash") -> str:
    ...
```

## Tiêu chí nghiệm thu

- Cùng input luôn tạo cùng canonical string.
- Thứ tự key trong dictionary không làm thay đổi hash.
- Thay đổi một giá trị làm hash thay đổi.
- Thứ tự row đầu vào không làm batch hash thay đổi.
- Unit test chạy thành công.

## Prompt cho Codex

```text
Đọc README.md và docs/CODEX_IMPLEMENTATION_PLAN.md.
Chỉ thực hiện Task 02 – Canonicalization và hashing.

Không sửa notebook pipeline ngoài phần import thật sự cần thiết.
Không triển khai blockchain ledger.

Hãy ưu tiên logic Python thuần có thể unit test ngoài Databricks.
Mọi phép hash phải deterministic.
Giải thích rõ cách xử lý null, decimal, timestamp, delimiter và row ordering.

Cuối task, chạy test và báo cáo các giới hạn của cách tính batch hash hiện tại.
```

---

# Task 03 – Medallion Data Pipeline

## Mục tiêu

Xây dựng pipeline Source → Bronze → Silver → Gold và tích hợp row hash, batch hash.

## Branch

```text
feature/task-03-medallion-pipeline
```

## File cần tạo

```text
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
src/blockchain_pipeline/pipeline_utils.py
```

## Yêu cầu chức năng

### Bronze

- Đọc từ `source_transactions`.
- Thêm `pipeline_run_id`, `ingestion_time`, `source_table`.
- Tạo `row_hash`.
- Lưu `bronze_transactions`.

### Silver

- Loại duplicate theo `transaction_id`.
- Kiểm tra trường bắt buộc.
- Chuẩn hóa timestamp và decimal.
- Tính lại `amount`.
- Tạo row hash mới.
- Lưu `silver_transactions`.

### Gold

- Tổng hợp theo `transaction_date`, `product`.
- Tạo `total_quantity`, `total_revenue`, `transaction_count`.
- Lưu `gold_daily_summary`.

## Tiêu chí nghiệm thu

- Pipeline chạy lại không tạo dữ liệu sai hoặc duplicate ngoài dự kiến.
- Số dòng Source, Bronze và Silver được giải thích rõ.
- Tổng doanh thu Gold khớp Silver.
- Mỗi stage có thể tính được batch hash.
- Notebook chạy đúng thứ tự.

## Prompt cho Codex

```text
Chỉ thực hiện Task 03 – Medallion Data Pipeline.
Đọc README.md và CODEX_IMPLEMENTATION_PLAN.md trước khi sửa code.

Tái sử dụng canonicalization và hashing từ Task 02.
Không triển khai blockchain ledger hoặc verification.
Notebook chỉ điều phối; logic tái sử dụng phải nằm trong src/.

Cuối task, cung cấp bảng đối chiếu record count và tổng amount giữa các stage.
```

---

# Task 04 – Blockchain verification ledger

## Mục tiêu

Tạo chuỗi block lưu hash kiểm chứng của từng pipeline stage.

## Branch

```text
feature/task-04-blockchain-ledger
```

## File cần tạo

```text
src/blockchain_pipeline/ledger.py
tests/test_ledger.py
notebooks/04a_build_ledger.py
```

## Yêu cầu chức năng

- Tạo bảng `blockchain_ledger`.
- Tạo genesis block với `previous_hash` là 64 ký tự `0`.
- Mỗi stage tạo một block.
- `block_hash` phải bao gồm metadata quan trọng.
- Chống tạo duplicate block cho cùng `pipeline_run_id` và `pipeline_stage`.
- Append block theo thứ tự SOURCE → BRONZE → SILVER → GOLD.

## Schema tối thiểu

```text
block_index
block_id
pipeline_run_id
pipeline_stage
source_table
target_table
record_count
batch_hash
previous_hash
block_hash
transformation
schema_hash
created_at
```

## Tiêu chí nghiệm thu

- Genesis block hợp lệ.
- Mỗi block trỏ đúng block trước.
- Tính lại block hash cho kết quả giống stored hash.
- Sửa payload làm block hash không còn hợp lệ.
- Unit test chạy thành công.

## Prompt cho Codex

```text
Chỉ thực hiện Task 04 – Blockchain verification ledger.
Không triển khai tamper scenarios hoặc dashboard.

Hãy thiết kế payload block deterministic và ghi rõ thứ tự field dùng để hash.
Bảo đảm append block có kiểm tra duplicate và thứ tự stage.
Thêm unit test cho genesis block, linkage và tamper detection ở cấp block.
```

---

# Task 05 – Data lineage và integrity verification

## Mục tiêu

Ghi lịch sử biến đổi dữ liệu và xây engine kiểm chứng dữ liệu, block và chain.

## Branch

```text
feature/task-05-lineage-verification
```

## File cần tạo

```text
src/blockchain_pipeline/lineage.py
src/blockchain_pipeline/verification.py
notebooks/05_verify_integrity.py
tests/test_verification.py
```

## Yêu cầu chức năng

### Lineage

Ghi:

```text
pipeline_run_id
source_stage
target_stage
source_table
target_table
transformation_name
input_record_count
output_record_count
input_batch_hash
output_batch_hash
started_at
finished_at
status
error_message
```

### Verification

Kiểm tra:

1. Current batch hash so với stored batch hash.
2. Recalculated block hash so với stored block hash.
3. `previous_hash` so với block trước.
4. Current record count so với stored record count.

Trạng thái:

```text
VALID
DATA_TAMPERED
RECORD_COUNT_MISMATCH
BLOCK_TAMPERED
CHAIN_BROKEN
```

## Tiêu chí nghiệm thu

- Pipeline sạch trả về VALID.
- Sửa dữ liệu trả về DATA_TAMPERED.
- Sửa block trả về BLOCK_TAMPERED.
- Sửa previous hash trả về CHAIN_BROKEN.
- Kết quả được lưu vào `verification_results`.

## Prompt cho Codex

```text
Chỉ thực hiện Task 05 – Data lineage và integrity verification.

Không tạo dữ liệu tấn công tự động; phần đó thuộc Task 06.
Verification phải phân biệt rõ lỗi dữ liệu, record count, block và chain.
Kết quả phải chỉ ra pipeline_run_id, stage, table và block_index bị ảnh hưởng.

Thêm unit test cho từng trạng thái lỗi.
```

---

# Task 06 – Tamper scenarios và reset demo

## Mục tiêu

Tạo các kịch bản thay đổi dữ liệu để trình diễn và cơ chế reset an toàn.

## Branch

```text
feature/task-06-tamper-scenarios
```

## File cần tạo

```text
notebooks/06_run_tamper_scenarios.py
sql/tamper_scenarios.sql
src/blockchain_pipeline/demo_scenarios.py
```

## Kịch bản bắt buộc

1. Không thay đổi dữ liệu.
2. Sửa `amount` của một transaction.
3. Xóa một transaction.
4. Chèn một transaction giả.
5. Sửa metadata trong block.
6. Sửa `previous_hash`.

## Yêu cầu an toàn

- Chỉ chạy trên schema demo.
- Có tham số xác nhận trước khi sửa dữ liệu.
- Log rõ scenario đã chạy.
- Có hàm reset về baseline.
- Không được chạy tự động tất cả scenario khi mở notebook.

## Tiêu chí nghiệm thu

- Mỗi scenario tạo đúng trạng thái lỗi mong đợi.
- Reset trả hệ thống về VALID.
- Có bảng tổng hợp expected status và actual status.

## Prompt cho Codex

```text
Chỉ thực hiện Task 06 – Tamper scenarios và reset demo.

Mọi lệnh UPDATE, DELETE, INSERT phải giới hạn trong schema demo.
Không chạy destructive action nếu người dùng chưa chọn scenario và xác nhận.
Mỗi scenario phải có expected result, actual result và cách reset.
```

---

# Task 07 – Thực nghiệm, metrics và dashboard

## Mục tiêu

Đo hiệu năng, tính overhead và tạo SQL cho dashboard trình bày.

## Branch

```text
feature/task-07-experiment-dashboard
```

## File cần tạo

```text
notebooks/07_experiment_and_metrics.py
src/blockchain_pipeline/metrics.py
sql/dashboard_queries.sql
```

## Thực nghiệm

Kích thước dữ liệu:

```text
1.000
5.000
10.000
50.000
```

Mỗi kích thước chạy ít nhất 3 lần.

Đo:

```text
baseline_duration_ms
secured_duration_ms
verification_duration_ms
overhead_percent
```

Công thức:

```text
overhead_percent =
(secured_duration_ms - baseline_duration_ms)
/ baseline_duration_ms
× 100
```

## Dashboard cần có

- Tổng pipeline run.
- Tổng block.
- Số verification hợp lệ.
- Số lần phát hiện tamper.
- Detection accuracy.
- Verification latency theo record count.
- Processing overhead theo record count.
- Lịch sử verification.
- Block lỗi đầu tiên.

## Tiêu chí nghiệm thu

- Kết quả lưu vào `experiment_metrics`.
- Có thể chạy lại thực nghiệm mà không nhầm lẫn run cũ.
- SQL dashboard chạy được trên Databricks SQL.
- Có bảng kết quả đủ dùng cho báo cáo Chương 3.

## Prompt cho Codex

```text
Chỉ thực hiện Task 07 – Experiment metrics và dashboard.

Không thay đổi logic hashing hoặc ledger trừ khi có lỗi được chứng minh bằng test.
Mỗi benchmark phải ghi record_count, run_number và timestamp.
Tạo SQL rõ ràng để dùng trực tiếp trong Databricks Dashboard.
Cuối task, xuất bảng kết quả và giải thích cách đưa số liệu vào báo cáo.
```

---

# Task 08 – Hardening, documentation và rehearsal

## Mục tiêu

Rà soát toàn bộ project trước khi trình bày.

## Branch

```text
chore/task-08-hardening-docs
```

## Nội dung

- Chạy toàn bộ unit test.
- Kiểm tra notebook theo thứ tự từ đầu.
- Xóa code thừa và debug output.
- Chuẩn hóa logging.
- Hoàn thiện README hướng dẫn chạy.
- Tạo troubleshooting guide.
- Ghi giới hạn mô hình.
- Chuẩn bị script demo 10–15 phút.

## Tiêu chí nghiệm thu

- Clone repository mới và chạy được theo README.
- Tất cả test thành công.
- Pipeline baseline trả về VALID.
- Ít nhất ba tamper scenario được demo thành công.
- Có số liệu overhead và verification latency.
- Không có secret trong Git history hiện tại.

---

## 3. Checklist review Pull Request

Mỗi PR cần được kiểm tra theo checklist:

```text
[ ] Đúng phạm vi task
[ ] Không làm trước task sau
[ ] Không chứa secret
[ ] Không hard-code catalog/schema tràn lan
[ ] Có test mới cho logic mới
[ ] Test chạy thành công
[ ] Notebook chạy trên Databricks
[ ] Có hướng dẫn chạy
[ ] Có expected result
[ ] Không thay đổi dữ liệu ngoài schema demo
[ ] README hoặc docs được cập nhật khi cần
```

---

## 4. Prompt review code dùng chung

Sau khi Codex tạo PR, dùng prompt sau:

```text
Hãy review Pull Request hiện tại theo chế độ zero-trust.

Kiểm tra:
1. Code có đúng phạm vi task không.
2. Có hard-code, secret hoặc destructive operation nguy hiểm không.
3. Hash có deterministic không.
4. Spark logic có phụ thuộc row order hoặc partition order không.
5. Notebook có chạy lại an toàn không.
6. Unit test đã phủ các case quan trọng chưa.
7. Có lỗi làm sai kết quả nghiên cứu hoặc số liệu thực nghiệm không.

Hãy trả về:
- Blocking issues.
- Non-blocking issues.
- File và dòng liên quan.
- Đề xuất sửa tối thiểu.
- Verdict: APPROVE hoặc REQUEST CHANGES.
```

---

## 5. Thứ tự triển khai khuyến nghị

```text
Task 01
  ↓
Task 02
  ↓
Task 03
  ↓
Task 04
  ↓
Task 05
  ↓
Task 06
  ↓
Task 07
  ↓
Task 08
```

Không nên giao Codex làm toàn bộ trong một prompt. Mỗi task nên là một PR riêng để dễ tìm lỗi, rollback và kiểm chứng trên Databricks.
