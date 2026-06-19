# DEMO SCRIPT

Kịch bản trình bày 10-15 phút cho MVP blockchain verification trong data
pipeline.

## 0. Chuẩn bị trước buổi demo

- Mở sẵn Databricks repo.
- Chọn Python notebook compute.
- Đảm bảo đã chạy một lần sạch từ notebook 00 đến 05.
- Có sẵn ít nhất một kết quả benchmark trong `experiment_metrics`.
- Mở sẵn `sql/dashboard_queries.sql` trong Databricks SQL.

## 1. Giới thiệu bài toán (1 phút)

Câu nói:

```text
Demo này kiểm tra tính toàn vẹn dữ liệu trong pipeline Source, Bronze, Silver,
Gold bằng SHA-256, hash chain và metadata lineage.
```

Expected result:

```text
Người nghe hiểu đây là mô hình tamper-evident, không phải blockchain phi tập
trung hoàn chỉnh.
```

## 2. Trình bày kiến trúc (2 phút)

Mở README phần kiến trúc.

Câu nói:

```text
Mỗi stage tạo batch hash. Ledger lưu record count, batch hash, schema hash,
previous hash và block hash. Nếu dữ liệu hoặc metadata bị sửa, verification sẽ
phát hiện sai lệch.
```

Expected result:

```text
Luồng Source -> Bronze -> Silver -> Gold -> Ledger -> Verification rõ ràng.
```

## 3. Chạy pipeline sạch (2-3 phút)

Chạy hoặc mở kết quả các notebook:

```text
00_setup_environment.py
01_generate_source_data.py
02_bronze_ingestion.py
03_silver_transformation.py
04_gold_aggregation.py
05_verify_integrity.py
```

Câu nói:

```text
Run sạch tạo bốn block tương ứng SOURCE, BRONZE, SILVER và GOLD. Verification
đối chiếu dữ liệu hiện tại với ledger.
```

Expected result:

```text
SOURCE  VALID
BRONZE  VALID
SILVER  VALID
GOLD    VALID
```

## 4. Demo tamper dữ liệu (3 phút)

Mở `06_run_tamper_scenarios.py`.

Widget:

```text
SCENARIO = MODIFY_TRANSACTION_AMOUNT
CONFIRM_TAMPER = YES
PIPELINE_RUN_ID = để trống
```

Câu nói:

```text
Bây giờ tôi sửa amount của một giao dịch trong Silver. Ledger không đổi, nên
batch hash hiện tại sẽ khác batch hash đã lưu.
```

Expected result:

```text
Notebook hiển thị dữ liệu trước/sau và verification trả về DATA_TAMPERED ở
stage SILVER hoặc stage bị ảnh hưởng đầu tiên.
```

## 5. Demo tamper ledger hoặc chain (2 phút)

Chạy lại `06_run_tamper_scenarios.py` sau reset baseline.

Widget:

```text
SCENARIO = MODIFY_LEDGER_TRANSFORMATION
CONFIRM_TAMPER = YES
```

Câu nói:

```text
Lần này dữ liệu không đổi, nhưng metadata của block bị sửa. Vì block_hash được
tính từ payload canonicalized, verification phát hiện BLOCK_TAMPERED.
```

Expected result:

```text
First broken block hiển thị stage SILVER với status BLOCK_TAMPERED.
```

## 6. Lineage và dashboard (2 phút)

Mở dashboard SQL hoặc chạy các query chính trong `sql/dashboard_queries.sql`.

Câu nói:

```text
Lineage cho biết stage nguồn, stage đích, số bản ghi vào/ra, batch hash và
trạng thái xử lý. Dashboard tổng hợp số run, số block, trạng thái verification,
block lỗi đầu tiên và overhead thực nghiệm.
```

Expected result:

```text
KPI hiển thị total_pipeline_runs, total_blocks, verification status counts,
first broken block, lineage flow và overhead theo record_count.
```

## 7. Benchmark và overhead (1-2 phút)

Mở kết quả `07_experiment_and_metrics.py` hoặc query overhead.

Câu nói:

```text
Benchmark chạy baseline và secured pipeline trên các mức 1k, 5k, 10k, 50k. Công
thức overhead là secured duration trừ baseline duration, chia baseline duration.
```

Expected result:

```text
experiment_metrics có ít nhất ba run chính cho mỗi record_count và warm-up được
tách bằng is_warmup.
```

## 8. Kết luận (1 phút)

Câu nói:

```text
MVP chứng minh cơ chế phát hiện thay đổi và truy vết trong data pipeline. Giới
hạn hiện tại là ledger vẫn nằm trong cùng workspace; hướng phát triển là ký số
hoặc đưa checkpoint hash ra hệ thống độc lập hay blockchain thật.
```

Expected result:

```text
Người nghe nắm được giá trị, giới hạn và hướng mở rộng của mô hình.
```

## Phương án dự phòng khi Databricks hết quota

- Không chạy lại benchmark đầy đủ; dùng kết quả đã ghi trong `experiment_metrics`.
- Không chạy lại toàn bộ pipeline; mở output đã chạy trước đó.
- Nếu cần demo tamper nhanh, dùng scenario `MODIFY_LEDGER_TRANSFORMATION` vì chỉ
  sửa metadata ledger và verification phát hiện nhanh.
- Nếu compute không khởi động được, trình bày qua README, dashboard query và ảnh
  chụp/kết quả đã lưu từ các bảng Delta.
