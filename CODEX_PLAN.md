# Kế hoạch làm việc với Codex

Tài liệu này chia toàn bộ đề tài thành các task nhỏ để Codex thực hiện tuần tự, dễ kiểm tra, dễ chạy thử trên Databricks và hạn chế việc sinh code quá nhiều trong một lần.

## 1. Nguyên tắc làm việc

1. Codex phải đọc `README.md` và `CODEX_PLAN.md` trước khi sửa code.
2. Không làm trực tiếp trên branch `main`.
3. Mỗi task sử dụng một branch riêng.
4. Mỗi task chỉ giải quyết một nhóm chức năng.
5. Không triển khai trước các task chưa đến lượt.
6. Mỗi task phải có kiểm thử hoặc hướng dẫn kiểm tra thủ công.
7. Notebook chỉ điều phối; logic chính đặt trong `src/`.
8. Không sử dụng dữ liệu cá nhân thật.
9. Catalog, schema và table name phải cấu hình tập trung.
10. Sau mỗi task phải chạy trên Databricks trước khi merge.

Quy ước branch:

```text
feature/task-01-project-scaffold
feature/task-02-source-data
feature/task-03-medallion-pipeline
feature/task-04-canonical-hashing
feature/task-05-blockchain-ledger
feature/task-06-data-lineage
feature/task-07-integrity-verification
feature/task-08-tamper-scenarios
feature/task-09-experiment-metrics
feature/task-10-dashboard-documentation
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

# Giai đoạn 1 — Chuẩn bị nền tảng

## Task 01 — Khởi tạo cấu trúc project

### Mục tiêu

Tạo bộ khung source code có thể sử dụng cho Databricks và Python unit test.

### Branch

```text
feature/task-01-project-scaffold
```

### File cần tạo

```text
requirements.txt
.gitignore
config/demo_config.py
src/blockchain_pipeline/__init__.py
src/blockchain_pipeline/schemas.py
notebooks/00_setup_environment.py
tests/__init__.py
```

### Nội dung cần thực hiện

- Tạo cấu hình tập trung cho catalog, schema, random seed và số lượng bản ghi.
- Tạo schema PySpark cho dữ liệu giao dịch.
- Tạo notebook khởi tạo schema và các Delta Table rỗng.
- Notebook phải dùng định dạng Databricks source file.
- Không xây dựng hashing hoặc blockchain trong task này.

### Tiêu chí nghiệm thu

- Import được module `blockchain_pipeline`.
- Chạy được `00_setup_environment.py` trên Databricks.
- Schema `blockchain_pipeline_demo` được tạo thành công.
- Không có tên catalog/schema bị hard-code rải rác.

### Prompt cho Codex

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

---

## Task 02 — Sinh dữ liệu nguồn giả lập

### Mục tiêu

Tạo dataset giao dịch giả lập có thể tái lập để dùng xuyên suốt toàn bộ demo.

### Branch

```text
feature/task-02-source-data
```

### File cần tạo hoặc sửa

```text
notebooks/01_generate_source_data.py
src/blockchain_pipeline/data_generator.py
tests/test_data_generator.py
```

### Nội dung cần thực hiện

- Sinh mặc định 10.000 giao dịch.
- Dùng random seed `42`.
- Dữ liệu gồm transaction, customer, product, quantity, price, amount và source system.
- Không sử dụng dữ liệu thật.
- Hỗ trợ truyền record count bằng widget hoặc config.
- Ghi vào bảng `source_transactions`.

### Tiêu chí nghiệm thu

- Hai lần chạy cùng seed tạo cùng tập dữ liệu logic.
- `transaction_id` không trùng.
- `amount = quantity × unit_price`.
- Bảng `source_transactions` có đủ số dòng cấu hình.

### Prompt cho Codex

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

---

# Giai đoạn 2 — Xây dựng Data Pipeline

## Task 03 — Pipeline Source, Bronze, Silver, Gold

### Mục tiêu

Xây dựng pipeline Medallion chạy hoàn chỉnh trước khi thêm blockchain.

### Branch

```text
feature/task-03-medallion-pipeline
```

### File cần tạo

```text
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
src/blockchain_pipeline/pipeline.py
tests/test_pipeline_rules.py
```

### Nội dung cần thực hiện

#### Bronze

- Đọc `source_transactions`.
- Bổ sung `pipeline_run_id`, `ingestion_time`, `source_table`.
- Ghi `bronze_transactions`.

#### Silver

- Loại bỏ trùng theo `transaction_id`.
- Kiểm tra trường bắt buộc.
- Chuẩn hóa timestamp và decimal.
- Tính lại amount.
- Ghi `silver_transactions`.

#### Gold

- Tổng hợp theo `transaction_date` và `product`.
- Tính total quantity, total revenue và transaction count.
- Ghi `gold_daily_summary`.

### Tiêu chí nghiệm thu

- Chạy tuần tự được ba notebook.
- Bronze có đủ metadata.
- Silver không có transaction trùng.
- Gold có tổng hợp đúng.
- Chạy lại pipeline không sinh dữ liệu trùng ngoài ý muốn.

### Prompt cho Codex

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

---

# Giai đoạn 3 — Cơ chế đảm bảo tính toàn vẹn

## Task 04 — Canonicalization và hashing

### Mục tiêu

Đảm bảo cùng một dữ liệu luôn tạo ra cùng một giá trị SHA-256.

### Branch

```text
feature/task-04-canonical-hashing
```

### File cần tạo

```text
src/blockchain_pipeline/canonicalization.py
src/blockchain_pipeline/hashing.py
tests/test_canonicalization.py
tests/test_hashing.py
```

### Nội dung cần thực hiện

- Chuẩn hóa null, decimal, timestamp và string.
- Dùng thứ tự cột cố định.
- Escape ký tự phân cách.
- Tạo `row_hash`.
- Tạo `schema_hash`.
- Tạo `batch_hash` không phụ thuộc thứ tự partition.
- Ghi chú giới hạn khi dùng collect với dữ liệu lớn.

### Tiêu chí nghiệm thu

- Cùng dữ liệu tạo cùng hash.
- Thay đổi một giá trị làm hash thay đổi.
- Thay đổi thứ tự dictionary không làm hash thay đổi.
- Thay đổi thứ tự dòng không làm batch hash thay đổi sau khi sort.
- Null, decimal và timestamp được chuẩn hóa ổn định.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 04 – Canonicalization và hashing.

Yêu cầu:
- Tạo canonicalize_value và canonicalize_record.
- Null dùng token cố định.
- Decimal dùng scale cố định.
- Timestamp dùng format thống nhất.
- Tạo compute_row_hash, compute_schema_hash và compute_batch_hash.
- Batch hash phải deterministic và không phụ thuộc thứ tự partition.
- Không collect toàn bộ dữ liệu nếu không cần; nếu MVP buộc phải dùng thì ghi chú giới hạn rõ ràng.
- Viết unit test đầy đủ cho các trường hợp thay đổi dữ liệu và thay đổi thứ tự.
```

---

## Task 05 — Blockchain verification ledger

### Mục tiêu

Tạo chuỗi block liên kết theo từng stage của pipeline.

### Branch

```text
feature/task-05-blockchain-ledger
```

### File cần tạo hoặc sửa

```text
src/blockchain_pipeline/ledger.py
src/blockchain_pipeline/models.py
tests/test_ledger.py
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
```

### Nội dung cần thực hiện

- Định nghĩa cấu trúc block.
- Tạo genesis block.
- Lấy block trước đó.
- Tạo `previous_hash`.
- Tính `block_hash`.
- Append block sau mỗi stage.
- Đảm bảo thứ tự block rõ ràng theo một pipeline run.

### Tiêu chí nghiệm thu

- Block đầu tiên có previous hash bằng 64 ký tự `0`.
- Block sau trỏ đúng hash block trước.
- Thay đổi payload làm block hash không hợp lệ.
- Một pipeline run tạo được chuỗi SOURCE → BRONZE → SILVER → GOLD.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 05 – Blockchain verification ledger.

Yêu cầu:
- Tạo model block rõ ràng.
- Genesis block dùng previous_hash gồm 64 ký tự 0.
- block_hash phải được tính từ payload đã canonicalize.
- Mỗi stage SOURCE, BRONZE, SILVER, GOLD tạo một block.
- Không dùng timestamp ngẫu nhiên trong unit test.
- Có test xác nhận liên kết block và phát hiện payload bị sửa.
- Không triển khai verification engine hoàn chỉnh trong task này.
```

---

# Giai đoạn 4 — Truy vết và kiểm chứng

## Task 06 — Data lineage

### Mục tiêu

Ghi lại lịch sử biến đổi dữ liệu giữa các stage.

### Branch

```text
feature/task-06-data-lineage
```

### File cần tạo

```text
src/blockchain_pipeline/lineage.py
tests/test_lineage.py
```

### File cần cập nhật

```text
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
```

### Nội dung cần thực hiện

- Ghi source stage, target stage.
- Ghi source table, target table.
- Ghi input/output record count.
- Ghi input/output batch hash.
- Ghi transformation name và description.
- Ghi start time, finish time và status.
- Ghi lỗi khi stage thất bại.

### Tiêu chí nghiệm thu

- Có đủ lineage SOURCE → BRONZE → SILVER → GOLD.
- Có thể truy ngược một pipeline run.
- Failure event được ghi rõ error message.
- Record count và batch hash khớp với pipeline run.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 06 – Data lineage.

Yêu cầu:
- Tạo lineage.py với hàm ghi lineage event.
- Tích hợp vào ba notebook pipeline.
- Ghi source, target, transformation, record count, batch hash, thời gian và status.
- Khi có lỗi phải ghi FAILED và error_message trước khi raise lại exception.
- Có unit test cho event SUCCESS và FAILED.
- Không xây dashboard trong task này.
```

---

## Task 07 — Integrity verification engine

### Mục tiêu

Kiểm tra dữ liệu hiện tại, block và toàn bộ liên kết chuỗi.

### Branch

```text
feature/task-07-integrity-verification
```

### File cần tạo

```text
src/blockchain_pipeline/verification.py
notebooks/05_verify_integrity.py
tests/test_verification.py
```

### Nội dung cần thực hiện

- Tính lại batch hash của bảng.
- So sánh record count.
- Tính lại block hash.
- Kiểm tra previous hash.
- Xác định block lỗi đầu tiên.
- Ghi kết quả vào `verification_results`.

### Trạng thái

```text
VALID
DATA_TAMPERED
RECORD_COUNT_MISMATCH
BLOCK_TAMPERED
CHAIN_BROKEN
```

### Tiêu chí nghiệm thu

- Pipeline bình thường trả về VALID.
- Sửa dữ liệu trả về DATA_TAMPERED.
- Xóa/chèn dòng trả về RECORD_COUNT_MISMATCH.
- Sửa payload block trả về BLOCK_TAMPERED.
- Sửa previous hash trả về CHAIN_BROKEN.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 07 – Integrity verification engine.

Yêu cầu:
- Kiểm tra data hash, record count, block hash và chain link.
- Trả về các trạng thái đã định nghĩa trong kế hoạch.
- Xác định first broken block.
- Ghi kết quả vào verification_results.
- Notebook 05_verify_integrity.py phải hỗ trợ chọn pipeline_run_id.
- Có unit test cho toàn bộ trạng thái lỗi.
- Không tự động sửa dữ liệu khi phát hiện lỗi.
```

---

# Giai đoạn 5 — Demo tấn công và thực nghiệm

## Task 08 — Tamper scenarios và reset

### Mục tiêu

Tạo các kịch bản chỉnh sửa dữ liệu để trình diễn trực tiếp.

### Branch

```text
feature/task-08-tamper-scenarios
```

### File cần tạo

```text
notebooks/06_run_tamper_scenarios.py
sql/tamper_scenarios.sql
src/blockchain_pipeline/tamper.py
```

### Kịch bản

1. Sửa một transaction.
2. Xóa một transaction.
3. Chèn một transaction giả.
4. Sửa batch hash trong ledger.
5. Sửa transformation trong ledger.
6. Sửa previous hash.
7. Reset về trạng thái sạch.

### Tiêu chí nghiệm thu

- Mỗi scenario chạy độc lập.
- Có log dữ liệu trước và sau thay đổi.
- Verification phát hiện đúng loại lỗi.
- Có chức năng reset để demo lại.
- Không chạy scenario phá dữ liệu nếu chưa có xác nhận qua widget.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 08 – Tamper scenarios và reset.

Yêu cầu:
- Mỗi scenario là một hàm riêng.
- Notebook dùng widget để chọn scenario.
- Có tham số CONFIRM_TAMPER để tránh chạy nhầm.
- Hiển thị dữ liệu trước và sau khi sửa.
- Sau khi chạy, gọi verification và hiển thị kết quả.
- Có reset scenario để khôi phục dữ liệu demo.
- Không sửa cấu trúc cốt lõi của hashing và ledger nếu không cần.
```

---

## Task 09 — Benchmark và experimental metrics

### Mục tiêu

Tạo số liệu thực nghiệm cho phần đánh giá của đề tài.

### Branch

```text
feature/task-09-experiment-metrics
```

### File cần tạo

```text
src/blockchain_pipeline/metrics.py
notebooks/07_experiment_and_metrics.py
tests/test_metrics.py
```

### Thực nghiệm

```text
1.000 dòng
5.000 dòng
10.000 dòng
50.000 dòng
```

Mỗi kích thước chạy ít nhất ba lần.

### Chỉ số

- Baseline pipeline duration.
- Secured pipeline duration.
- Verification duration.
- Processing overhead phần trăm.
- Detection accuracy.
- Số lượng metadata records.

### Tiêu chí nghiệm thu

- Kết quả ghi vào `experiment_metrics`.
- Không dùng một lần chạy duy nhất để kết luận.
- Có warm-up hoặc ghi chú ảnh hưởng cold start.
- Có median hoặc average rõ ràng.
- Xử lý trường hợp baseline bằng 0.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 09 – Benchmark và experimental metrics.

Yêu cầu:
- Benchmark baseline pipeline và secured pipeline.
- Chạy các mức 1k, 5k, 10k, 50k; mỗi mức tối thiểu ba lần.
- Đo pipeline duration, verification duration và overhead.
- Ghi kết quả vào experiment_metrics.
- Tách warm-up khỏi lần đo chính hoặc ghi chú rõ.
- Không giả lập số liệu; tất cả số liệu phải sinh từ lần chạy thật.
- Có kiểm tra công thức overhead.
```

---

# Giai đoạn 6 — Dashboard và hoàn thiện

## Task 10 — Dashboard, tài liệu chạy và chuẩn bị demo

### Mục tiêu

Hoàn thiện các truy vấn, tài liệu và kịch bản trình bày.

### Branch

```text
feature/task-10-dashboard-documentation
```

### File cần tạo hoặc cập nhật

```text
sql/dashboard_queries.sql
RUNBOOK.md
DEMO_SCRIPT.md
README.md
```

### Dashboard cần có

- Tổng số pipeline run.
- Tổng số block.
- Số verification thành công.
- Số tamper event phát hiện được.
- Verification latency.
- Processing overhead.
- Lineage SOURCE → BRONZE → SILVER → GOLD.
- Block lỗi đầu tiên.

### RUNBOOK cần có

- Cách clone GitHub vào Databricks.
- Cách thiết lập catalog/schema.
- Thứ tự chạy notebook.
- Cách reset demo.
- Cách xử lý lỗi thường gặp.

### DEMO_SCRIPT cần có

- Kịch bản trình bày 10–15 phút.
- Câu nói ngắn cho từng bước.
- Expected result tại từng màn hình.
- Phương án dự phòng nếu Databricks hết quota.

### Tiêu chí nghiệm thu

- Người khác có thể chạy lại demo chỉ bằng tài liệu.
- SQL dashboard chạy được trên schema cấu hình.
- Có kịch bản demo sạch và kịch bản tamper.
- README phản ánh đúng cấu trúc code cuối cùng.

### Prompt cho Codex

```text
Hãy đọc README.md và CODEX_PLAN.md.

Chỉ thực hiện Task 10 – Dashboard và tài liệu hoàn thiện.

Yêu cầu:
- Tạo dashboard_queries.sql với các KPI đã mô tả.
- Tạo RUNBOOK.md hướng dẫn chạy từ đầu trên Databricks.
- Tạo DEMO_SCRIPT.md cho phần trình bày 10–15 phút.
- Cập nhật README theo cấu trúc project thực tế.
- Không thay đổi logic hashing, ledger hoặc verification nếu không có lỗi rõ ràng.
- Cuối cùng lập checklist nghiệm thu toàn bộ MVP.
```

---

# 2. Quy trình cho mỗi task

Mỗi task thực hiện theo chu trình:

```text
1. Tạo branch từ main mới nhất
2. Gửi prompt task cho Codex
3. Codex phân tích và liệt kê file sẽ thay đổi
4. Codex thực hiện code
5. Chạy unit test
6. Push branch lên GitHub
7. Pull branch vào Databricks
8. Chạy notebook thủ công
9. Ghi lại lỗi và kết quả
10. Sửa lỗi nếu có
11. Tạo Pull Request
12. Review diff
13. Merge vào main
14. Chuyển sang task tiếp theo
```

Không bắt đầu task tiếp theo khi task hiện tại chưa chạy thành công trên Databricks.

---

# 3. Mẫu yêu cầu Codex review trước khi code

Dùng đoạn sau trước mỗi task:

```text
Trước khi sửa code, hãy:

1. Đọc README.md và CODEX_PLAN.md.
2. Kiểm tra cấu trúc repository hiện tại.
3. Xác nhận task đang thực hiện và các task không được thực hiện trước.
4. Liệt kê file dự kiến tạo hoặc sửa.
5. Nêu các giả định kỹ thuật.
6. Nêu rủi ro có thể ảnh hưởng Databricks Free Edition.
7. Chờ tôi xác nhận kế hoạch trước khi bắt đầu thay đổi lớn.
```

---

# 4. Mẫu yêu cầu Codex debug

```text
Hãy debug lỗi này theo phạm vi tối thiểu.

Yêu cầu:
1. Đọc log đầy đủ và xác định root cause.
2. Không viết lại toàn bộ project.
3. Nêu file, hàm và dòng logic có vấn đề.
4. Đề xuất bản sửa nhỏ nhất.
5. Bổ sung test tái hiện lỗi trước khi sửa nếu có thể.
6. Sau khi sửa, chạy lại test liên quan.
7. Tóm tắt root cause, thay đổi và cách xác minh trên Databricks.

Log lỗi:
<dán log vào đây>
```

---

# 5. Mẫu yêu cầu Codex review Pull Request

```text
Hãy review thay đổi hiện tại như một Senior Data Engineer.

Kiểm tra:
- Có vượt phạm vi task không.
- Có hard-code catalog/schema/table name không.
- Hash có deterministic không.
- Có phụ thuộc thứ tự partition của Spark không.
- Notebook có chứa quá nhiều business logic không.
- Có rủi ro collect dữ liệu lớn về driver không.
- Có xử lý rerun/idempotency không.
- Có unit test cho logic quan trọng không.
- Có làm sai ý nghĩa blockchain hoặc data lineage không.
- Có đưa dữ liệu nhạy cảm vào repository không.

Hãy trả về:
1. Blocking issues.
2. Non-blocking improvements.
3. Test còn thiếu.
4. Verdict: APPROVE hoặc REQUEST CHANGES.
```

---

# 6. Definition of Done toàn dự án

Dự án hoàn thành khi:

- [ ] Source → Bronze → Silver → Gold chạy thành công.
- [ ] Dữ liệu mẫu có thể tái lập.
- [ ] Row hash, batch hash và schema hash ổn định.
- [ ] Mỗi stage tạo một block kiểm chứng.
- [ ] Chuỗi block liên kết đúng.
- [ ] Data lineage được ghi đầy đủ.
- [ ] Verification phát hiện được thay đổi dữ liệu.
- [ ] Verification phát hiện được ledger bị sửa.
- [ ] Có reset để chạy lại demo.
- [ ] Có benchmark nhiều kích thước dữ liệu.
- [ ] Có số liệu overhead thực tế.
- [ ] Có dashboard queries.
- [ ] Có RUNBOOK và DEMO_SCRIPT.
- [ ] Unit test chính chạy thành công.
- [ ] README phản ánh đúng cách chạy thực tế.
- [ ] Không lưu secret hoặc dữ liệu nhạy cảm trong GitHub.
