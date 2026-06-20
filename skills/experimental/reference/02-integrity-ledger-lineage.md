# Tasks 04-07: Hashing, Ledger, Lineage, and Verification

Use this reference for deterministic hashing, blockchain-style ledger blocks,
data lineage, and integrity verification.

## Task 04 - Canonicalization and Hashing

### Goal

Ensure the same logical data always creates the same SHA-256 value.

### Branch

```text
feature/task-04-canonical-hashing
```

### Files

```text
src/blockchain_pipeline/canonicalization.py
src/blockchain_pipeline/hashing.py
tests/test_canonicalization.py
tests/test_hashing.py
```

### Requirements

- Normalize null, decimal, timestamp, and string values.
- Use fixed column order.
- Escape separator characters.
- Create row hash, schema hash, and batch hash.
- Batch hash must not depend on Spark partition order.
- Document limitations if the MVP must collect records to the driver.

### Acceptance

- Same data creates same hash.
- Changing one value changes hash.
- Dictionary key order does not change hash when ordered columns are supplied.
- Row order does not change batch hash after stable sorting.
- Null, decimal, and timestamp canonicalization are stable.

### Prompt

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

## Task 05 - Blockchain Verification Ledger

### Goal

Create a hash-linked block chain for every pipeline stage.

### Branch

```text
feature/task-05-blockchain-ledger
```

### Files

```text
src/blockchain_pipeline/ledger.py
src/blockchain_pipeline/models.py
tests/test_ledger.py
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
```

### Requirements

- Define a clear block model.
- Create genesis block behavior.
- Read previous block.
- Set `previous_hash`.
- Calculate `block_hash`.
- Append one block after each stage.
- Keep block ordering clear within a `pipeline_run_id`.

### Acceptance

- First block uses 64 zero characters as previous hash.
- Each following block points to previous block hash.
- Payload changes make block hash invalid.
- One pipeline run creates SOURCE -> BRONZE -> SILVER -> GOLD.

### Prompt

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

## Task 06 - Data Lineage

### Goal

Record data transformations between stages.

### Branch

```text
feature/task-06-data-lineage
```

### Files

```text
src/blockchain_pipeline/lineage.py
tests/test_lineage.py
notebooks/02_bronze_ingestion.py
notebooks/03_silver_transformation.py
notebooks/04_gold_aggregation.py
```

### Requirements

- Record source stage and target stage.
- Record source table and target table.
- Record input and output record counts.
- Record input and output batch hashes.
- Record transformation name and description.
- Record start time, finish time, and status.
- Record errors when a stage fails.

### Acceptance

- Full lineage exists for SOURCE -> BRONZE -> SILVER -> GOLD.
- A `pipeline_run_id` can be traced.
- Failed event includes `error_message`.
- Record counts and batch hashes match the run.

### Prompt

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

## Task 07 - Integrity Verification Engine

### Goal

Verify current data, block payloads, and full chain links.

### Branch

```text
feature/task-07-integrity-verification
```

### Files

```text
src/blockchain_pipeline/verification.py
notebooks/05_verify_integrity.py
tests/test_verification.py
```

### Requirements

- Recalculate current table batch hash.
- Compare record count.
- Recalculate block hash.
- Check previous hash.
- Identify first broken block.
- Write results to `verification_results`.
- Do not automatically repair data.

### Status Values

```text
VALID
DATA_TAMPERED
RECORD_COUNT_MISMATCH
BLOCK_TAMPERED
CHAIN_BROKEN
```

### Acceptance

- Clean pipeline returns VALID.
- Data modification returns DATA_TAMPERED.
- Deleted/inserted rows return RECORD_COUNT_MISMATCH.
- Block payload modification returns BLOCK_TAMPERED.
- Previous hash modification returns CHAIN_BROKEN.

### Prompt

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
