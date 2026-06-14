Bạn đang làm việc trong repository:

`sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc`

Hãy đọc đầy đủ hai file sau trước khi thay đổi code:

1. `README.md`
2. `docs/CODEX_IMPLEMENTATION_PLAN.md`

Chỉ thực hiện **Task 01 – Scaffold project và dữ liệu nguồn**.

Không triển khai trước các nội dung thuộc Task 02 trở đi, bao gồm:

* Canonicalization.
* SHA-256 hashing.
* Blockchain ledger.
* Data lineage.
* Integrity verification.
* Tamper scenarios.
* Experiment metrics.
* Dashboard.

## Mục tiêu Task 01

1. Tạo cấu trúc project Python phù hợp với Databricks.
2. Tạo file cấu hình dùng chung.
3. Định nghĩa schema dữ liệu giao dịch bằng PySpark.
4. Tạo notebook chuẩn bị môi trường.
5. Tạo notebook sinh dữ liệu giao dịch giả lập.
6. Lưu dữ liệu vào Delta Table `source_transactions`.

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

## Cấu hình mặc định

```text
CATALOG_NAME = workspace
SCHEMA_NAME = blockchain_pipeline_demo
SOURCE_TABLE = source_transactions
RECORD_COUNT = 10000
RANDOM_SEED = 42
SOURCE_SYSTEM = SCHOOL_DEMO
```

Catalog phải có khả năng thay đổi từ file cấu hình, không hard-code ở nhiều notebook.

## Schema giao dịch

```text
transaction_id: string
customer_id: string
transaction_time: timestamp
product: string
quantity: integer
unit_price: decimal(18,2)
amount: decimal(18,2)
source_system: string
```

## Yêu cầu notebook 00_setup_environment.py

* Dùng định dạng Databricks notebook source.
* Tạo schema nếu chưa tồn tại.
* Thiết kế để chạy lại nhiều lần không lỗi.
* Kiểm tra và hiển thị catalog, schema đang sử dụng.
* Không xóa dữ liệu hiện có khi chưa được yêu cầu.
* Chuẩn bị các cấu trúc cần thiết cho Task 01.

Phần đầu notebook:

```python
# Databricks notebook source
```

## Yêu cầu notebook 01_generate_source_data.py

* Sinh đúng 10.000 giao dịch.
* Dùng random seed `42`.
* Không sử dụng dữ liệu cá nhân thật.
* `transaction_id` phải duy nhất.
* `quantity` phải lớn hơn 0.
* `unit_price` phải lớn hơn 0.
* `amount = quantity × unit_price`.
* Dữ liệu phải có thể tái lập khi dùng cùng seed.
* Lưu vào Delta Table `source_transactions`.
* Hiển thị record count và một số bản ghi mẫu sau khi ghi.
* Có kiểm tra dữ liệu cơ bản trước khi hoàn thành.

## Yêu cầu chất lượng code

* Python có type hints.
* Hàm public có docstring.
* Không hard-code catalog và schema trong nhiều file.
* Không ghi secret, token hoặc mật khẩu vào repository.
* Logic dùng chung phải đặt trong `src/`.
* Notebook chỉ điều phối các bước chính.
* Có logging rõ ràng.
* Có xử lý lỗi hợp lý.
* Code phù hợp để chạy trên Databricks Free Edition.

## Tiêu chí nghiệm thu

Task chỉ hoàn thành khi:

* `00_setup_environment.py` chạy thành công.
* Notebook có thể chạy lại mà không lỗi.
* `01_generate_source_data.py` tạo đúng 10.000 dòng.
* `transaction_id` không trùng.
* Không có `quantity <= 0`.
* Không có `unit_price <= 0`.
* Không có bản ghi sai công thức `amount`.
* Bảng `source_transactions` đọc lại được.
* Codex không triển khai nội dung của các task tiếp theo.

## Cách làm việc

Trước khi sửa code, hãy trả về:

1. Tóm tắt cách bạn hiểu Task 01.
2. Danh sách file sẽ tạo hoặc sửa.
3. Các giả định về Databricks Free Edition.
4. Kế hoạch triển khai ngắn.

Sau khi được xác nhận, hãy thực hiện code.

Khi hoàn thành, báo cáo:

1. Danh sách file đã tạo hoặc sửa.
2. Mô tả ngắn chức năng từng file.
3. Các lệnh hoặc notebook cần chạy.
4. Kết quả kiểm tra.
5. Các giả định và giới hạn.
6. Những nội dung cố ý chưa triển khai.
