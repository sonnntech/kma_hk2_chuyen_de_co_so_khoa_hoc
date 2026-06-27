# Tên đề tài

**Nghiên cứu ứng dụng phương pháp Quasi-experimental để đánh giá cơ chế đảm bảo tính toàn vẹn và truy vết dữ liệu trong hệ thống Data Pipeline — Thực nghiệm với mô hình Blockchain dạng Hash Chain**

---

## I. Mục tiêu và Khung Nghiên cứu

### 1. Vấn đề nghiên cứu

Hệ thống Data Pipeline xử lý và lưu trữ dữ liệu qua nhiều giai đoạn. Sau khi pipeline hoàn tất, không có cơ chế nội tại nào đảm bảo dữ liệu đã lưu còn khớp với trạng thái tại thời điểm ghi. Các thao tác UPDATE, DELETE hoặc INSERT trái phép — bao gồm cả insider threat từ tài khoản có quyền cao — có thể làm thay đổi dữ liệu mà hệ thống không phát hiện được.

**Câu hỏi trung tâm:**

> Liệu một cơ chế kiểm chứng độc lập dựa trên hash chain (Blockchain-inspired) có thể phát hiện các dạng thay đổi trái phép trong hệ thống Data Pipeline đa tầng không, và chi phí tính toán bổ sung của cơ chế đó là bao nhiêu?

Đây là vấn đề an ninh mạng (cyber security) thuộc phạm vi **Data Integrity**: bảo đảm tính xác thực và không bị sửa đổi của dữ liệu trong toàn bộ vòng đời xử lý.

### 2. Khoảng trống nghiên cứu

Các cơ chế kiểm soát toàn vẹn dữ liệu hiện tại có giới hạn rõ ràng:

| Cơ chế hiện tại | Giới hạn |
|---|---|
| Database audit log | Nằm trong cùng trust boundary với dữ liệu; admin có thể sửa cả log lẫn dữ liệu. |
| Application-level checksum | Không liên kết theo chuỗi; không phát hiện được khi cả checksum lẫn dữ liệu bị sửa đồng thời. |
| Traditional Blockchain (decentralized) | Overhead quá lớn để tích hợp vào Data Pipeline; yêu cầu Consensus và Smart Contract không cần thiết cho bài toán integrity. |
| Pipeline monitoring | Chỉ theo dõi trạng thái tại thời điểm chạy; không có bằng chứng kiểm chứng sau khi pipeline đã hoàn tất. |

**Khoảng trống**: Chưa có nghiên cứu đánh giá một cách có kiểm soát (controlled) khả năng phát hiện thay đổi trái phép của cơ chế hash-chain ledger nhẹ (lightweight) trong ngữ cảnh Data Pipeline đa tầng, với các kịch bản tấn công cụ thể và đo lường chi phí overhead tương ứng.

### 3. Câu hỏi nghiên cứu

| Mã | Câu hỏi nghiên cứu |
|---|---|
| RQ1 | Cơ chế hash-chain ledger có phát hiện được tất cả các dạng thay đổi trái phép trong Data Pipeline (sửa nội dung, xóa/chèn bản ghi, sửa metadata block, phá chain link) không? |
| RQ2 | Chi phí tính toán bổ sung (overhead) của cơ chế kiểm chứng thay đổi theo kích thước dữ liệu như thế nào? |
| RQ3 | Kết hợp kết quả verification và lineage events có đủ để định vị chính xác stage và transformation bị ảnh hưởng khi phát hiện thay đổi không? |

### 4. Giả thuyết nghiên cứu

| Mã | Giả thuyết | Điều kiện falsifiable |
|---|---|---|
| H1 | Hash-chain ledger phát hiện 100% kịch bản tấn công được kiểm thử (sửa nội dung, xóa/chèn bản ghi, sửa block metadata, phá chain link). | Nếu bất kỳ kịch bản nào trả về `VALID` khi đã có thay đổi → H1 bị bác bỏ. |
| H2 | Security overhead tăng theo kích thước dữ liệu và có quan hệ nhất quán, có thể đo lường được. | Nếu overhead không có quan hệ nhất quán với record count → H2 bị bác bỏ. |
| H3 | Kết hợp `first_broken_block`, `pipeline_run_id`, `pipeline_stage` và `lineage_events` xác định chính xác nguồn gốc sai lệch. | Nếu lineage không khớp với stage phát hiện lỗi → H3 bị bác bỏ. |

### 5. Lý do chọn phương pháp Quasi-experimental Research

Theo định nghĩa trong *Research Methods for Cyber Security* (Edgar & Manz, Ch. 10), quasi-experiment là thực nghiệm có một hoặc nhiều biến độc lập không kiểm soát được hoàn toàn. Năm yếu tố đặc thù của cyber security biện minh cho lựa chọn này:

| Driver (Ch. 10) | Áp dụng vào nghiên cứu này |
|---|---|
| **Cyber environment diversity (Snowflake)** | Môi trường thử nghiệm là Databricks Free Edition — một cấu hình duy nhất, không thể đại diện cho mọi Data Pipeline production. Không thể kiểm soát hoàn toàn môi trường compute. |
| **Internet scale** | Databricks chạy trên cloud infrastructure; scheduling, cluster allocation và network latency không kiểm soát được hoàn toàn. |
| **Threat population limitations** | Không có attacker thực tế. Tamper scenarios là proxy cho threat actor — tương tự red team trong Ch. 10. |
| **Users as background noise** | Cold start, cluster warm-up và compute state variability ảnh hưởng đến kết quả đo lường nhưng không kiểm soát được hoàn toàn. |
| **Specialized user populations** | Dataset là dữ liệu giao dịch giả lập (synthetic) — không phải dữ liệu production thực tế; ecological validity bị giới hạn. |

**Kết luận phương pháp**: True experiment không khả thi vì không thể kiểm soát môi trường Databricks, không có attacker thực tế, và dataset là synthetic. Quasi-experimental là lựa chọn duy nhất cho bài toán này. Mọi biến có thể kiểm soát được đã kiểm soát (tamper scenarios xác định, seed cố định, cùng pipeline structure); biến không kiểm soát được ghi nhận và phân tích tường minh.

### 6. Mục tiêu tổng quát

Đề tài nghiên cứu cơ chế bảo đảm **Data Integrity** và **Data Lineage** trong hệ thống **Data Pipeline**, từ đó đề xuất và đánh giá bằng phương pháp quasi-experimental một mô hình ứng dụng Blockchain theo hướng **tamper-evident** để tăng khả năng kiểm chứng trạng thái dữ liệu, phát hiện thay đổi trái phép và hỗ trợ truy vết lịch sử xử lý dữ liệu.

Phạm vi nghiên cứu tập trung vào mô hình Blockchain dạng **hash chain** phục vụ kiểm chứng dữ liệu trong pipeline. Mô hình không triển khai mạng Blockchain phi tập trung hoàn chỉnh, không sử dụng **Consensus** hay **Smart Contract**, mà khai thác các đặc tính cốt lõi gồm **SHA-256**, liên kết block bằng `previous_hash`, chuẩn hóa payload và kiểm chứng lại trạng thái dữ liệu theo từng pipeline run.

### 7. Mục tiêu cụ thể

| Nhóm mục tiêu | Nội dung | Vai trò trong thiết kế nghiên cứu |
|---|---|---|
| Tổng quan nền tảng | Phân tích kiến trúc Data Pipeline và các yêu cầu Data Governance liên quan. | Mô tả experimental environment |
| Phân tích rủi ro | Xác định các nguy cơ mất toàn vẹn dữ liệu trong Ingestion, ETL/ELT, lưu trữ và truy cập. | Định nghĩa Independent Variable IV1 |
| Cơ chế toàn vẹn | Nghiên cứu hàm băm, chuẩn hóa dữ liệu, record count và schema hash. | Mô tả treatment mechanism |
| Cơ chế truy vết | Nghiên cứu Data Lineage theo pipeline run, transformation và batch hash. | Định nghĩa Dependent Variable DV4 |
| Blockchain ứng dụng | Phân tích ledger dạng chuỗi block liên kết bằng hash. | Triển khai treatment |
| Mô hình thử nghiệm | Xây dựng pipeline Source → Bronze → Silver → Gold với tamper scenarios và benchmark. | Triển khai experimental procedure |
| Đánh giá | Đánh giá detection coverage (H1), overhead scaling (H2) và lineage traceability (H3). | Đo lường dependent variables |

---

## II. Đề cương chi tiết

---

## PHẦN MỞ ĐẦU: KHUNG PHƯƠNG PHÁP QUASI-EXPERIMENTAL

### PH.1. Thiết kế thực nghiệm: Treatment và Control

Nghiên cứu áp dụng thiết kế **Difference-of-Differences** — phương pháp quasi-experimental chuẩn khi không thể thực hiện random assignment (Ch. 10).

**Treatment group**: Các pipeline run có tiêm kịch bản tamper (`tamper_scenario ≠ NONE`).

**Control group**: Các pipeline run sạch (`tamper_scenario = NONE`) chạy trong cùng môi trường và cùng cấu hình.

**Điểm đo T1 (trước treatment)**: Trạng thái verification của pipeline run sạch — kết quả kỳ vọng là `VALID` cho tất cả block.

**Điểm đo T2 (sau treatment)**: Trạng thái verification sau khi tiêm tamper scenario — kết quả kỳ vọng là non-VALID cho block bị ảnh hưởng.

**Tính toán Difference-of-Differences**:

$$
\Delta T = \text{Detection\_rate}(T2_\text{treatment}) - \text{Detection\_rate}(T1_\text{treatment})
$$

$$
\Delta C = \text{Detection\_rate}(T2_\text{control}) - \text{Detection\_rate}(T1_\text{control}) \approx 0
$$

$$
\text{DiD} = \Delta T - \Delta C
$$

| Nhóm | T1 (trước tamper) | T2 (sau tamper) | Δ |
|---|---|---|---|
| Treatment (có tamper) | VALID (baseline) | non-VALID (kỳ vọng) | +1 (phát hiện thành công) |
| Control (không tamper) | VALID (baseline) | VALID (kỳ vọng) | 0 (không false positive) |

### PH.2. Biến độc lập (Independent Variables)

| Biến độc lập | Giá trị | Mô tả |
|---|---|---|
| **IV1 — Tamper scenario** | NONE, MODIFY_TRANSACTION_AMOUNT, DELETE_TRANSACTION, INSERT_FAKE_TRANSACTION, MODIFY_LEDGER_BATCH_HASH, MODIFY_LEDGER_TRANSFORMATION, MODIFY_LEDGER_PREVIOUS_HASH | Loại can thiệp trái phép được tiêm vào pipeline hoặc ledger. |
| **IV2 — Record count** | 1.000, 5.000, 10.000, 50.000 | Kích thước dataset để đo overhead theo quy mô. |
| **IV3 — Pipeline stage** | SOURCE, BRONZE, SILVER, GOLD | Vị trí trong pipeline mà tamper được áp dụng. |

IV1 là biến thực nghiệm chính kiểm tra H1. IV2 là biến thực nghiệm kiểm tra H2. IV3 là biến bổ trợ kiểm tra H3.

### PH.3. Biến phụ thuộc (Dependent Variables)

| Biến phụ thuộc | Ký hiệu | Đơn vị | Hypothesis liên quan |
|---|---|---|---|
| **Verification outcome** | DV1 | Categorical: VALID / DATA_TAMPERED / RECORD_COUNT_MISMATCH / BLOCK_TAMPERED / CHAIN_BROKEN | H1 |
| **Detection accuracy** | DV2 | % = TP / (TP + FN) × 100 | H1 |
| **Security overhead** | DV3 | % = (secured_ms − baseline_ms) / baseline_ms × 100 | H2 |
| **Lineage traceability** | DV4 | Binary: stage và transformation xác định đúng (1) hoặc sai (0) | H3 |

### PH.4. Chỉ số đo lường (Measurement Metrics)

**Cho H1 — Detection coverage:**

- True Positive (TP): Kịch bản có tamper → verification trả về non-VALID
- False Negative (FN): Kịch bản có tamper → verification trả về VALID (lỗi nghiêm trọng)
- True Negative (TN): Kịch bản không có tamper → verification trả về VALID
- False Positive (FP): Kịch bản không có tamper → verification trả về non-VALID

$$
\text{Detection Rate (DV2)} = \frac{TP}{TP + FN} \times 100\%
$$

$$
\text{False Positive Rate} = \frac{FP}{FP + TN} \times 100\%
$$

**Cho H2 — Overhead measurement:**

$$
\text{DV3: Overhead}(\%) = \frac{\text{secured\_duration\_ms} - \text{baseline\_duration\_ms}}{\text{baseline\_duration\_ms}} \times 100
$$

Đo theo bốn mức record count (IV2). Loại bỏ warm-up run (`is_warmup = true`) để giảm ảnh hưởng của uncontrolled compute state.

**Cho H3 — Lineage traceability:**

Sau khi phát hiện `first_broken_block`, kiểm tra lineage event tương ứng có khớp đúng `pipeline_stage` và `transformation_name` với kịch bản tamper đã tiêm không.

### PH.5. Quy trình thực nghiệm (Experimental Procedure)

```
Bước 1: Thiết lập môi trường
  → 00_setup_environment.py: khởi tạo Delta Table, ledger, lineage schema

Bước 2: Sinh dữ liệu nguồn với seed cố định (reproducible)
  → 01_generate_source_data.py

Bước 3: Chạy pipeline cơ sở — Control condition (NONE)
  → 02_bronze_ingestion.py → 03_silver_transformation.py → 04_gold_aggregation.py
  → Ledger ghi 4 block: SOURCE → BRONZE → SILVER → GOLD
  → 05_verify_integrity.py: xác nhận VALID (T1 measurement)

Bước 4: Tiêm tamper scenario — Treatment condition
  → 06_run_tamper_scenarios.py: áp dụng một trong 7 tamper vectors (IV1)
  → 05_verify_integrity.py: đo DV1, DV2, DV4 (T2 measurement)

Bước 5: Reset về baseline trước kịch bản tiếp theo
  → 06_run_tamper_scenarios.py (RESET_BASELINE)

Bước 6: Benchmark overhead theo IV2
  → 07_experiment_and_metrics.py: chạy pipeline với 4 mức record count
  → Loại bỏ warm-up; ghi DV3 vào experiment_metrics

Bước 7: Phân tích Difference-of-Differences
  → So sánh Δ giữa treatment và control theo từng kịch bản
  → Kiểm tra H1, H2, H3 theo metrics đã định nghĩa
```

### PH.6. Biến không kiểm soát (Uncontrolled Variables)

| Biến không kiểm soát | Lý do không kiểm soát được | Tác động tiềm ẩn |
|---|---|---|
| **Compute state của Databricks cluster** | Databricks Free Edition không đảm bảo cluster state nhất quán giữa các runs. | Tăng variance của DV3 (overhead). |
| **Cold start / warm-up** | Lần chạy đầu tiên luôn tốn thêm thời gian khởi động. | Confound benchmark nếu không lọc `is_warmup`. |
| **Cloud infrastructure scheduling** | Cluster allocation và network path do cloud provider quyết định. | Tăng noise trong verification latency. |
| **Synthetic dataset distribution** | Dataset giả lập không phản ánh phân phối production thực tế. | Giới hạn ecological validity của H1. |
| **Single environment (snowflake)** | Chỉ test trên một Databricks workspace. | Không thể generalize kết quả sang mọi Data Pipeline platform. |
| **Simulated threat actors** | Tamper scenarios do researcher tạo ra, không phải attacker thực tế. | Không bao phủ attack vectors nâng cao. |

### PH.7. Nguy cơ sai lệch và Hiệu lực nội bộ (Bias and Validity Threats)

**Threats to Internal Validity:**

| Nguy cơ | Mô tả | Biện pháp giảm thiểu |
|---|---|---|
| **Selection bias** | Tamper scenarios được researcher chọn, không phải random sample từ attack space thực tế. | Ghi nhận rõ 7 vectors; không generalize sang vectors ngoài danh sách. |
| **Instrumentation bias** | Verification engine là cùng hệ thống được đánh giá — không có bên thứ ba kiểm chứng. | Publish source code và test suite trên GitHub để peer review. |
| **Maturation** | Cluster state thay đổi giữa các runs ảnh hưởng benchmark. | Loại bỏ warm-up; đo nhiều lần; dùng median thay mean. |
| **History effect** | Dữ liệu từ run trước có thể còn trong Delta Table nếu không reset đúng. | RESET_BASELINE bắt buộc giữa các kịch bản. |

**Threats to External Validity (Generalizability):**

| Nguy cơ | Mô tả |
|---|---|
| **Snowflake environment** | Kết quả trên Databricks Free Edition có thể không áp dụng cho on-premise Spark, AWS Glue, hoặc dbt. |
| **Synthetic data** | Dataset giao dịch giả lập có phân phối đồng đều — thực tế có skewed data, null-heavy fields, hoặc schema drift. |
| **No adversarial pressure** | Attacker thực tế có thể sửa cả ledger lẫn dữ liệu trong cùng transaction nếu có quyền admin. |

---

## CHƯƠNG 1

## CƠ SỞ LÝ THUYẾT: DATA PIPELINE, TOÀN VẸN DỮ LIỆU VÀ BLOCKCHAIN

*Mục tiêu chương: Xây dựng nền tảng lý thuyết cho ba thành phần của thiết kế quasi-experimental: (1) đặc trưng môi trường thực nghiệm (Data Pipeline), (2) threat model định nghĩa IV1, (3) cơ chế treatment (Blockchain hash chain).*

### 1.1. Tổng quan về hệ thống Data Pipeline

#### 1.1.1. Khái niệm hệ thống Data Pipeline

Data Pipeline là tập hợp các bước xử lý dữ liệu được tổ chức theo luồng, trong đó dữ liệu được thu thập từ nhiều nguồn, được kiểm tra, biến đổi, chuẩn hóa và lưu trữ tại các tầng phục vụ phân tích hoặc vận hành. Pipeline có thể chạy theo Batch, Streaming hoặc kiến trúc lai tùy thuộc yêu cầu Latency, Throughput và tính nhất quán dữ liệu.

Trong hệ thống dữ liệu hiện đại, Data Pipeline đóng vai trò kết nối giữa hệ thống phát sinh dữ liệu và các nền tảng khai thác dữ liệu như Data Lake, Data Warehouse, Lakehouse, BI Dashboard hoặc hệ thống Machine Learning. Chất lượng của pipeline ảnh hưởng trực tiếp đến độ tin cậy của báo cáo, mô hình phân tích và quyết định nghiệp vụ.

> **Vị trí trong thiết kế nghiên cứu**: Data Pipeline đa tầng (Source → Bronze → Silver → Gold) là *experimental environment*. Đặc trưng nhiều stage, dữ liệu biến đổi qua từng layer tạo nhu cầu kiểm chứng toàn vẹn ở từng điểm, và là lý do IV3 (pipeline stage) được đưa vào thiết kế.

#### 1.1.2. Kiến trúc tổng thể của hệ thống Data Pipeline

Một kiến trúc Data Pipeline điển hình gồm các tầng sau:

| Thành phần | Vai trò |
|---|---|
| Data Source | Nơi phát sinh dữ liệu gốc, bao gồm database, file, API, event stream hoặc log hệ thống. |
| Ingestion Layer | Thu thập dữ liệu từ nguồn, ghi nhận metadata đầu vào và chuyển dữ liệu vào vùng xử lý. |
| Processing Layer | Thực hiện ETL/ELT, validation, deduplication, enrichment, aggregation và chuẩn hóa dữ liệu. |
| Storage Layer | Lưu trữ dữ liệu theo các mức raw, cleaned, curated hoặc analytical. |
| Serving Layer | Cung cấp dữ liệu cho reporting, dashboard, auditing, analytics hoặc downstream applications. |
| Monitoring & Governance | Theo dõi chất lượng dữ liệu, lineage, quyền truy cập, audit log và trạng thái vận hành. |

Kiến trúc **Medallion Architecture** phân tách dữ liệu theo các tầng Bronze, Silver và Gold. Bronze lưu dữ liệu gần nguồn, Silver lưu dữ liệu đã kiểm tra và chuẩn hóa, Gold lưu dữ liệu tổng hợp phục vụ phân tích.

#### 1.1.3. Vai trò của Data Pipeline trong đảm bảo chất lượng dữ liệu

Data Pipeline thực thi các quy tắc **Data Quality** như schema validation, type casting, mandatory field validation, deduplication và kiểm tra tính nhất quán toán học. Ví dụ, dữ liệu giao dịch cần bảo đảm quan hệ:

$$
\text{amount} = \text{quantity} \times \text{unit\_price}
$$

Pipeline chỉ bảo đảm chất lượng tại thời điểm xử lý nếu không có cơ chế kiểm chứng độc lập sau khi dữ liệu đã được ghi. Rủi ro còn lại nằm ở các thao tác sửa, xóa, chèn hoặc thay đổi metadata sau xử lý. Bài toán toàn vẹn dữ liệu yêu cầu thêm một lớp kiểm chứng để xác nhận trạng thái dữ liệu hiện tại có khớp với trạng thái đã được ghi nhận trước đó hay không.

### 1.2. Các nguy cơ mất toàn vẹn dữ liệu trong hệ thống Data Pipeline

*Phần này xây dựng threat model — nền tảng để operationalize IV1 (tamper scenario).*

#### 1.2.1. Nguy cơ thay đổi dữ liệu trong quá trình truyền dẫn

Dữ liệu có thể bị thay đổi khi truyền từ nguồn vào pipeline do lỗi mạng, lỗi mã hóa, lỗi định dạng, ghi đè file, mapping sai schema hoặc can thiệp trái phép. Rủi ro này làm dữ liệu đầu vào khác với dữ liệu phát sinh ban đầu, dẫn đến toàn bộ các tầng xử lý sau đó kế thừa sai lệch.

> **Ánh xạ sang IV1**: `MODIFY_TRANSACTION_AMOUNT` mô phỏng can thiệp vào nội dung dữ liệu. Kết quả kỳ vọng của DV1: `DATA_TAMPERED`.

#### 1.2.2. Nguy cơ thay đổi dữ liệu trong quá trình xử lý ETL

ETL/ELT có thể làm sai lệch dữ liệu do lỗi transformation, lỗi join, lỗi type casting, xử lý null không nhất quán, deduplication sai khóa hoặc aggregation sai logic nghiệp vụ. Sai lệch trong ETL có tính lan truyền vì tầng dữ liệu sau phụ thuộc trực tiếp vào tầng dữ liệu trước.

Kiểm soát toàn vẹn trong ETL cần ghi nhận trạng thái dữ liệu trước và sau mỗi transformation. Các chỉ số tối thiểu gồm record count, schema hash, batch hash và mô tả transformation.

> **Ánh xạ sang IV1**: `DELETE_TRANSACTION` và `INSERT_FAKE_TRANSACTION` mô phỏng thay đổi record count sau ETL. DV1 kỳ vọng: `RECORD_COUNT_MISMATCH`.

#### 1.2.3. Nguy cơ thay đổi dữ liệu trong quá trình lưu trữ dữ liệu

Dữ liệu đã lưu vẫn có thể bị thay đổi thông qua UPDATE, DELETE, INSERT, overwrite nhầm hoặc thao tác của người dùng có quyền cao. Nếu hệ thống chỉ lưu trạng thái hiện tại, quá trình kiểm toán không có cơ sở để xác định dữ liệu có còn khớp với thời điểm pipeline hoàn tất hay không.

Một cơ chế audit có độ tin cậy cần tách bằng chứng kiểm chứng khỏi dữ liệu nghiệp vụ. Khi dữ liệu bị sửa, hệ thống tính lại fingerprint và so sánh với bằng chứng đã ghi.

> **Ánh xạ sang IV1**: `MODIFY_LEDGER_BATCH_HASH` mô phỏng attacker cố ý sửa cả ledger. DV1 kỳ vọng: `DATA_TAMPERED`.

#### 1.2.4. Nguy cơ từ truy cập trái phép vào hệ thống dữ liệu

Threat Model của hệ thống cần xét cả dữ liệu nghiệp vụ và metadata kiểm chứng. Người tấn công hoặc insider threat có thể sửa dữ liệu, sửa log, sửa batch hash hoặc phá liên kết giữa các bản ghi kiểm chứng. Nếu ledger và dữ liệu nằm trong cùng một trust boundary, tài khoản quản trị cấp cao vẫn có khả năng thay đổi cả hai.

Ràng buộc Zero Trust đặt ra yêu cầu: mọi trạng thái dữ liệu phải có bằng chứng kiểm chứng độc lập, mọi block kiểm chứng phải tự xác thực được payload, và mọi block sau phải ràng buộc với block trước thông qua hash.

> **Ánh xạ sang IV1**: `MODIFY_LEDGER_TRANSFORMATION` (DV1: `BLOCK_TAMPERED`) và `MODIFY_LEDGER_PREVIOUS_HASH` (DV1: `CHAIN_BROKEN`) mô phỏng attacker tấn công trực tiếp vào ledger.

### 1.3. Tổng quan về cơ chế đảm bảo tính toàn vẹn dữ liệu

#### 1.3.1. Đảm bảo tính toàn vẹn dữ liệu bằng hàm băm

Hàm băm mật mã chuyển dữ liệu đầu vào có độ dài bất kỳ thành chuỗi đầu ra có độ dài cố định. SHA-256 tạo digest 256 bit, thường biểu diễn bằng 64 ký tự hexadecimal. Các thuộc tính quan trọng gồm deterministic output, avalanche effect và khả năng chống tìm tiền ảnh trong phạm vi ứng dụng kiểm chứng dữ liệu.

Trước khi băm, dữ liệu cần được canonicalize. Cùng một giá trị logic phải tạo cùng chuỗi biểu diễn bất kể khác biệt về kiểu dữ liệu, timezone, scale decimal hoặc thứ tự dictionary. Quy tắc canonicalization:

| Kiểu dữ liệu | Quy tắc chuẩn hóa |
|---|---|
| Null | Chuyển thành token cố định. |
| Decimal | Dùng scale cố định. |
| Timestamp | Dùng format thống nhất và timezone xác định. |
| String | Escape ký tự phân cách và chuẩn hóa biểu diễn. |
| Record | Sắp xếp theo thứ tự cột cố định. |
| Batch | Sắp xếp row hash hoặc sort key ổn định trước khi tạo batch hash. |

#### 1.3.2. Kiểm chứng thay đổi dữ liệu trong hệ thống xử lý dữ liệu

Kiểm chứng dữ liệu là quá trình tính lại fingerprint của dữ liệu hiện tại và so sánh với fingerprint đã lưu. Một cơ chế kiểm chứng đầy đủ cần thỏa mãn đồng thời:

$$
\mathcal{V}(D_t, E_t) =
\begin{cases}
\text{VALID}, &
\left|D_t\right| = E_{\text{count}}
\land H(D_t) = E_{\text{hash}}
\land S(D_t) = E_{\text{schema}} \\
\text{INVALID}, & \text{otherwise}
\end{cases}
$$

Record count phát hiện xóa hoặc chèn dòng. Batch hash phát hiện sửa nội dung khi số dòng không đổi. Schema hash phát hiện thay đổi cấu trúc dữ liệu.

> **Vị trí trong thiết kế nghiên cứu**: Cơ chế này tạo ra **DV1** (verification outcome). Kết quả VALID/non-VALID là đầu ra đo lường chính của thực nghiệm.

#### 1.3.3. Vai trò của kiểm chứng dữ liệu trong hệ thống Data Pipeline

Verification cung cấp bằng chứng kỹ thuật cho trạng thái dữ liệu sau pipeline. Hệ thống không chỉ tạo dữ liệu đầu ra, mà còn tạo được bằng chứng để xác định dữ liệu đầu ra có còn khớp với trạng thái đã ghi nhận hay không.

Các trạng thái kiểm chứng:

| Trạng thái (DV1) | Ý nghĩa |
|---|---|
| `VALID` | Dữ liệu, record count, block hash và chain link hợp lệ. |
| `DATA_TAMPERED` | Batch hash hiện tại khác batch hash đã lưu. |
| `RECORD_COUNT_MISMATCH` | Số bản ghi hiện tại khác số bản ghi đã lưu. |
| `BLOCK_TAMPERED` | Payload block bị thay đổi hoặc block hash không khớp. |
| `CHAIN_BROKEN` | `previous_hash` không trỏ đúng block trước. |

### 1.4. Tổng quan về cơ chế truy vết dữ liệu trong hệ thống Data Pipeline

#### 1.4.1. Khái niệm truy vết dữ liệu (Data Lineage)

Data Lineage mô tả nguồn gốc, dòng di chuyển và lịch sử transformation của dữ liệu. Lineage trả lời các câu hỏi: dữ liệu đến từ đâu, đi qua transformation nào, được ghi vào đâu, chạy trong pipeline run nào và trạng thái xử lý ra sao.

> **Vị trí trong thiết kế nghiên cứu**: Lineage là nền tảng đo lường **DV4** (lineage traceability — khả năng định vị nguồn gốc sai lệch sau khi phát hiện tamper).

#### 1.4.2. Vai trò của truy vết dữ liệu trong quản lý dữ liệu

DAMA Data Governance xem lineage là nền tảng cho auditability, impact analysis, root cause analysis và regulatory compliance. Khi dữ liệu phân tích sai, lineage giúp xác định upstream source, transformation liên quan và downstream asset bị ảnh hưởng.

Một lineage event tối thiểu cần chứa:

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

#### 1.4.3. Ứng dụng truy vết dữ liệu trong phát hiện thay đổi dữ liệu

Lineage cung cấp ngữ cảnh để giải thích kết quả verification. Batch hash xác định trạng thái dữ liệu bị sai lệch; lineage xác định transformation, stage và tài sản dữ liệu liên quan. Kết hợp hai cơ chế tạo thành chuỗi phân tích để đo DV4:

$$
\text{VerificationFailure}
\rightarrow \text{FirstBrokenBlock}
\rightarrow \text{PipelineStage}
\rightarrow \text{LineageEvent}
\rightarrow \text{TransformationContext}
$$

### 1.5. Tổng quan về công nghệ Blockchain trong đảm bảo tính toàn vẹn dữ liệu

#### 1.5.1. Khái niệm công nghệ Blockchain

Blockchain là cấu trúc dữ liệu gồm các block được liên kết tuần tự bằng hash. Mỗi block chứa payload, hash của block trước và hash của chính block hiện tại. Quan hệ băm:

$$
H_n = \text{SHA256}(\text{Payload}_n \parallel H_{n-1})
$$

Trong bài toán Data Pipeline, block không nhất thiết lưu toàn bộ dữ liệu. Block có thể lưu fingerprint của dữ liệu, metadata transformation và liên kết tới block trước.

> **Vị trí trong thiết kế nghiên cứu**: Blockchain hash chain là **treatment mechanism** — thành phần kỹ thuật được đánh giá trong thực nghiệm. Treatment group là pipeline runs có ledger tích hợp; control group là pipeline runs không có ledger.

#### 1.5.2. Đặc tính bất biến dữ liệu của Blockchain

Tính bất biến của Blockchain không đến từ việc dữ liệu không thể bị sửa ở tầng vật lý, mà từ khả năng phát hiện sửa đổi. Khi payload của block thay đổi, `block_hash` tính lại sẽ khác giá trị đã lưu. Khi block trung gian bị thay đổi, toàn bộ chuỗi sau đó mất liên kết hợp lệ.

Mức độ bất biến thực tế phụ thuộc trust boundary. Nếu ledger nằm trong cùng môi trường quản trị với dữ liệu, mô hình đạt mức tamper-evident nội bộ. Để tăng mức bảo đảm, hệ thống cần externalize ledger, ký số block hoặc lưu checkpoint hash trên hạ tầng độc lập.

#### 1.5.3. Khả năng ứng dụng Blockchain trong kiểm chứng và truy vết dữ liệu

Blockchain phù hợp với Data Pipeline ở vai trò audit ledger: mỗi stage sinh một bằng chứng kiểm chứng, các bằng chứng được liên kết tuần tự, cơ chế xác thực toàn vẹn có thể phát hiện sai lệch trong dữ liệu, block payload hoặc chain link.

| Năng lực | Cơ chế | Dependent Variable |
|---|---|---|
| Data Integrity | Batch hash, schema hash, record count. | DV1, DV2 |
| Tamper Evidence | Block hash và previous hash. | DV1, DV2 |
| Traceability | Pipeline run ID, stage metadata và lineage event. | DV4 |

---

## CHƯƠNG 2

## PHÂN TÍCH CƠ CHẾ KIỂM CHỨNG VÀ THIẾT KẾ THỰC NGHIỆM

*Mục tiêu chương: Phân tích chi tiết cơ chế treatment (hash-chain verification), xác định cách mỗi thành phần kỹ thuật ánh xạ sang biến thực nghiệm, và xác lập các yêu cầu đo lường.*

### 2.1. Kiến trúc đảm bảo tính toàn vẹn dữ liệu trong hệ thống Data Pipeline

#### 2.1.1. Đảm bảo tính toàn vẹn dữ liệu tại nguồn dữ liệu

Điểm tiếp nhận dữ liệu cần tạo bằng chứng cho trạng thái ban đầu trước khi dữ liệu bước vào transformation. Bằng chứng này gồm record count, schema fingerprint và batch hash. Trạng thái tại nguồn trở thành mốc gốc để đối chiếu các tầng xử lý sau — đây là **điểm đo T1** trong thiết kế Difference-of-Differences.

| Ràng buộc | Cách kiểm soát | DV liên quan |
|---|---|---|
| Tính đầy đủ | Đếm số bản ghi hoặc số event được ingest. | DV1: RECORD_COUNT_MISMATCH |
| Tính đúng schema | Lưu schema hash và validate trường bắt buộc. | DV1: BLOCK_TAMPERED |
| Tính không đổi | Sinh batch hash từ dữ liệu đã canonicalize. | DV1: DATA_TAMPERED |

#### 2.1.2. Đảm bảo tính toàn vẹn dữ liệu trong quá trình xử lý ETL

Mỗi transformation trong ETL phải tạo bằng chứng trạng thái đầu ra. Với pipeline nhiều tầng, bằng chứng ở tầng sau cần liên kết với bằng chứng ở tầng trước để tạo một chuỗi xử lý có thể kiểm toán.

Quy trình kiểm soát:

$$
D_{\text{in}}
\xrightarrow{\text{Validate}(schema, rules)}
D_{\text{valid}}
\xrightarrow{\text{Transform}}
D_{\text{out}}
\xrightarrow{\text{Hash} + \text{Metadata}}
E_{\text{stage}}
\xrightarrow{\text{Link}}
B_n
$$

ETL integrity không chỉ kiểm tra dữ liệu cuối cùng. Cơ chế đúng phải xác định được stage nào tạo ra trạng thái sai lệch đầu tiên — đây là **first_broken_block**, nền tảng của DV4.

#### 2.1.3. Đảm bảo tính toàn vẹn dữ liệu trong quá trình lưu trữ dữ liệu

Lớp lưu trữ cần hỗ trợ kiểm chứng sau khi pipeline đã hoàn tất. Tại thời điểm verification, hệ thống đọc dữ liệu hiện tại, tính lại fingerprint và so sánh với ledger — đây là **điểm đo T2**. Kết quả kiểm chứng được ghi thành lịch sử audit để phân tích theo thời gian.

$$
\text{StoredEvidence} \oplus \text{CurrentDataState}
\rightarrow \text{IntegrityVerification}
\rightarrow \text{DV1: VerificationResult}
$$

### 2.2. Phân tích cơ chế truy vết dữ liệu trong hệ thống Data Pipeline

#### 2.2.1. Truy vết dữ liệu theo luồng xử lý dữ liệu

Lineage theo luồng xử lý ghi nhận quan hệ upstream/downstream giữa các stage. Mỗi edge trong lineage graph biểu diễn một transformation:

$$
\text{Stage}_A \xrightarrow{\text{transformation}} \text{Stage}_B
$$

Thông tin bắt buộc gồm source, target, transformation name, thời điểm chạy, trạng thái và pipeline run ID.

#### 2.2.2. Truy vết dữ liệu theo lịch sử biến đổi dữ liệu

Lịch sử biến đổi dữ liệu cần lưu cả metadata kỹ thuật và metadata nghiệp vụ. Metadata kỹ thuật gồm record count, batch hash, schema hash, execution time và status. Metadata nghiệp vụ gồm tên transformation, mô tả logic xử lý và mục tiêu dữ liệu đầu ra.

Thiết kế lineage cần hỗ trợ hai truy vấn:

$$
\text{ForwardLineage}(S) = \{T \mid S \leadsto T\}
$$

$$
\text{BackwardLineage}(O) = \{U \mid U \leadsto O\}
$$

#### 2.2.3. Truy vết dữ liệu phục vụ kiểm chứng thay đổi dữ liệu

Khi verification trả về lỗi, lineage hỗ trợ khoanh vùng phạm vi — đây là cơ chế đo **DV4**:

| Kết quả DV1 | Cách dùng lineage | Câu hỏi đo DV4 |
|---|---|---|
| `DATA_TAMPERED` | Xác định stage và transformation tạo dữ liệu bị sai lệch. | Stage xác định đúng? |
| `RECORD_COUNT_MISMATCH` | So sánh input/output record count của transformation liên quan. | Transformation đúng? |
| `BLOCK_TAMPERED` | Kiểm tra metadata transformation bị sửa. | Block chính xác? |
| `CHAIN_BROKEN` | Xác định vị trí đứt trong chuỗi stage. | Chain break đúng vị trí? |

### 2.3. Phân tích cơ chế đảm bảo tính bất biến dữ liệu bằng Blockchain

#### 2.3.1. Cơ chế liên kết khối dữ liệu bằng hàm băm

Mỗi block kiểm chứng chứa payload đại diện cho trạng thái một stage. Công thức tổng quát:

$$
\text{Payload}_n =
\text{Canonicalize}(\text{stage\_metadata}, \text{record\_count},
\text{batch\_hash}, \text{schema\_hash}, \text{transformation})
$$

$$
\text{BlockHash}_n =
\text{SHA256}(\text{Payload}_n \parallel \text{PreviousHash}_n)
$$

$$
\text{PreviousHash}_n = \text{BlockHash}_{n-1}
$$

Genesis block sử dụng previous hash cố định:

$$
\text{PreviousHash}_0 =
\texttt{0000000000000000000000000000000000000000000000000000000000000000}
$$

#### 2.3.2. Cơ chế kiểm chứng dữ liệu bằng Blockchain

Verification engine kiểm tra bốn điều kiện — mỗi điều kiện tương ứng với một giá trị của DV1:

| Điều kiện | Lỗi phát hiện | DV1 |
|---|---|---|
| Current record count khớp ledger | Xóa hoặc chèn dữ liệu. | `RECORD_COUNT_MISMATCH` |
| Current batch hash khớp ledger | Sửa nội dung dữ liệu. | `DATA_TAMPERED` |
| Recalculated block hash khớp ledger | Sửa metadata block. | `BLOCK_TAMPERED` |
| Current previous hash khớp block trước | Phá liên kết chuỗi. | `CHAIN_BROKEN` |

Điều kiện được kiểm tra theo thứ tự block index để xác định **first_broken_block** — đầu vào cho DV4.

#### 2.3.3. Vai trò của Blockchain trong phát hiện thay đổi trái phép dữ liệu

Hash chain biến mỗi stage thành một điểm kiểm chứng có ràng buộc toán học với stage trước đó. Người tấn công không thể sửa một block mà không làm thay đổi block hash; sửa previous hash sẽ làm đứt chain link; sửa dữ liệu sẽ làm batch hash hiện tại khác bằng chứng đã lưu.

**Giới hạn trong bối cảnh quasi-experimental**: Cơ chế này chỉ phát hiện được các tamper vectors đã biết và được mô hình hóa trong IV1. Attack vectors ngoài danh sách không được kiểm tra trong nghiên cứu này — đây là uncontrolled variable liên quan đến external validity của H1.

### 2.4. Phân tích mô hình tích hợp Blockchain trong hệ thống Data Pipeline

#### 2.4.1. Mô hình tích hợp Blockchain tại tầng thu thập dữ liệu

Tầng thu thập tạo block đầu tiên cho dữ liệu vừa ingest. Block này đóng vai trò **baseline evidence** — điểm đo T1 trong thiết kế Difference-of-Differences. Mọi transformation sau đó phải liên kết tới baseline này thông qua hash chain.

#### 2.4.2. Mô hình tích hợp Blockchain tại tầng xử lý dữ liệu

Tầng xử lý tạo block sau mỗi transformation chính. Thiết kế này giúp verification xác định chính xác **first_broken_block** — stage đầu tiên bị sai lệch — thay vì chỉ phát hiện sai lệch ở output cuối. Đây là yêu cầu thiết yếu để đo DV4.

#### 2.4.3. Mô hình tích hợp Blockchain tại tầng lưu trữ dữ liệu

Tầng lưu trữ phân tích tạo block cho curated hoặc aggregated dataset. Đây là lớp trực tiếp phục vụ dashboard và báo cáo, nên verification tại tầng này bảo vệ tính đúng đắn của chỉ số phân tích.

### 2.5. Phân tích yêu cầu đo lường trong thiết kế thực nghiệm

#### 2.5.1. Yêu cầu đo lường DV3: Security Overhead

Cơ chế kiểm chứng tạo chi phí tính toán bổ sung. Benchmark cần đo ba nhóm Duration để tính DV3:

| Chỉ số | Ý nghĩa |
|---|---|
| Baseline Duration | Thời gian chạy pipeline không có ledger/verification. |
| Secured Duration | Thời gian chạy pipeline có hashing và ledger. |
| Verification Duration | Thời gian kiểm chứng dữ liệu hiện tại so với ledger. |
| DV3: Overhead | Phần chi phí tăng thêm khi bổ sung cơ chế bảo mật. |

$$
\text{DV3: Overhead}(\%) =
\frac{\text{secured\_duration\_ms} - \text{baseline\_duration\_ms}}
{\text{baseline\_duration\_ms}}
\times 100
$$

**Biện pháp kiểm soát uncontrolled variables**: Loại bỏ warm-up run (`is_warmup = true`); dùng median thay mean để giảm ảnh hưởng của cold start.

#### 2.5.2. Yêu cầu về khả năng mở rộng hệ thống

Batch hash phải deterministic nhưng không được phụ thuộc Spark partition order. Với dữ liệu lớn, thiết kế nên dùng partition-level hash hoặc Merkle Tree để giảm áp lực lên Driver. Mô hình MVP có thể dùng cách tính đơn giản hơn nếu dataset nằm trong giới hạn thử nghiệm, nhưng tài liệu cần nêu rõ giới hạn đó.

#### 2.5.3. Yêu cầu về khả năng kiểm chứng dữ liệu (DV1, DV4)

Hệ thống cần trả lời được bảy câu hỏi kiểm chứng:

| Câu hỏi | DV |
|---|---|
| Dữ liệu hiện tại có khớp batch hash đã lưu không? | DV1 |
| Record count hiện tại có khớp record count đã lưu không? | DV1 |
| Schema hiện tại có khớp schema hash đã lưu không? | DV1 |
| Payload block có bị sửa không? | DV1 |
| Chain link có bị đứt không? | DV1 |
| First broken block là block nào? | DV4 |
| Pipeline run nào và stage nào bị ảnh hưởng? | DV4 |

---

## CHƯƠNG 3

## TRIỂN KHAI VÀ KẾT QUẢ THỰC NGHIỆM QUASI-EXPERIMENTAL

*Mục tiêu chương: Trình bày môi trường thực nghiệm, kết quả đo lường theo từng hypothesis, và đánh giá giới hạn phương pháp.*

### 3.1. Môi trường thực nghiệm (Quasi-experimental Testbed)

#### 3.1.1. Đặc tả testbed — Databricks Free Edition

Mô hình thử nghiệm được triển khai trên Databricks với Python, PySpark, SQL và Delta Table. Dataset là dữ liệu giao dịch giả lập, sinh bằng seed cố định để tái lập kết quả. Pipeline vật lý gồm bốn bảng:

```text
source_transactions
        |
        v
bronze_transactions
        |
        v
silver_transactions
        |
        v
gold_daily_summary
```

| Tầng | Vai trò triển khai |
|---|---|
| Source | Lưu dữ liệu giao dịch giả lập. |
| Bronze | Bổ sung `pipeline_run_id`, `ingestion_time`, `source_table`. |
| Silver | Deduplicate, validate, normalize kiểu dữ liệu và tính lại `amount`. |
| Gold | Tổng hợp theo `transaction_date` và `product`. |

> **Lý do đây là quasi-experimental environment**: Databricks Free Edition là "snowflake environment" — cấu hình duy nhất, compute không ổn định, không kiểm soát được cluster scheduling. Đây là uncontrolled variable chính ảnh hưởng đến DV3.

#### 3.1.2. Kiến trúc tích hợp Blockchain (Treatment Mechanism)

Mỗi pipeline run tạo bốn block trong `blockchain_ledger`:

```text
SOURCE -> BRONZE -> SILVER -> GOLD
```

Block lưu stage metadata, target table, record count, batch hash, schema hash, transformation, previous hash, block hash và created time. Block SOURCE là genesis block với previous hash gồm 64 ký tự `0`; các block sau trỏ tới block hash của stage trước.

#### 3.1.3. Thành phần kỹ thuật của hệ thống thực nghiệm

| Module | Chức năng | Vai trò trong thực nghiệm |
|---|---|---|
| `canonicalization.py` | Chuẩn hóa null, decimal, timestamp, string và record trước khi hash. | Đảm bảo determinism cho DV1 |
| `hashing.py` | Tính row hash, schema hash và batch hash. | Tạo IV1-sensitive fingerprint |
| `models.py` | Định nghĩa `LedgerBlock` và payload block. | Cấu trúc dữ liệu treatment |
| `ledger.py` | Tạo block, tính block hash, ghi và đọc ledger. | Core treatment mechanism |
| `pipeline.py` | Xử lý Source → Bronze → Silver → Gold. | Experimental environment |
| `lineage.py` | Ghi lineage event SUCCESS/FAILED. | Đo DV4 |
| `verification.py` | Kiểm tra record count, data hash, block hash và chain link. | Đo DV1, DV2 |
| `tamper.py` | Cài đặt tamper scenarios và reset baseline. | Operationalize IV1 |
| `metrics.py` | Tính benchmark metrics và overhead. | Đo DV3 |

### 3.2. Quy trình thực nghiệm chi tiết

#### 3.2.1. Thiết lập điều kiện kiểm soát (Control Condition)

```text
00_setup_environment.py    → Khởi tạo schema (một lần)
01_generate_source_data.py → Sinh dataset với seed cố định
02_bronze_ingestion.py     → Bronze transformation
03_silver_transformation.py → Silver transformation
04_gold_aggregation.py     → Gold transformation
05_verify_integrity.py     → T1 measurement: xác nhận VALID (control baseline)
```

#### 3.2.2. Triển khai điều kiện xử lý (Treatment Condition)

```text
06_run_tamper_scenarios.py → Tiêm IV1 (MODIFY / DELETE / INSERT / MODIFY_LEDGER_*)
05_verify_integrity.py     → T2 measurement: đo DV1, DV2, DV4
06_run_tamper_scenarios.py (RESET_BASELINE) → Khôi phục về trạng thái sạch
```

#### 3.2.3. Benchmark overhead (IV2 variation)

```text
07_experiment_and_metrics.py → Chạy pipeline với 1.000 / 5.000 / 10.000 / 50.000 records
                             → Lọc is_warmup = false
                             → Ghi DV3 vào experiment_metrics
```

#### 3.2.4. Operationalization của IV1 — Kịch bản kiểm thử

| Kịch bản (IV1) | Vector can thiệp | DV1 kỳ vọng | Loại |
|---|---|---|---|
| `NONE` | Không sửa dữ liệu | `VALID` | TN (control) |
| `MODIFY_TRANSACTION_AMOUNT` | Sửa giá trị giao dịch | `DATA_TAMPERED` | TP |
| `DELETE_TRANSACTION` | Xóa một dòng dữ liệu | `RECORD_COUNT_MISMATCH` | TP |
| `INSERT_FAKE_TRANSACTION` | Chèn dòng giả | `RECORD_COUNT_MISMATCH` | TP |
| `MODIFY_LEDGER_BATCH_HASH` | Sửa batch hash trong ledger | `DATA_TAMPERED` | TP |
| `MODIFY_LEDGER_TRANSFORMATION` | Sửa metadata transformation | `BLOCK_TAMPERED` | TP |
| `MODIFY_LEDGER_PREVIOUS_HASH` | Sửa liên kết block | `CHAIN_BROKEN` | TP |
| `RESET_BASELINE` | Tạo lại run sạch | `VALID` | Control reset |

Notebook tamper yêu cầu widget `CONFIRM_TAMPER = YES` để tránh thao tác phá dữ liệu ngoài ý muốn.

### 3.3. Kết quả thực nghiệm và kiểm tra Hypothesis

#### 3.3.1. Kết quả tổng quan từ Dashboard (2026-06-20 08:15 UTC)

| KPI | Giá trị |
|---|---:|
| Tổng số pipeline runs | 15 |
| Tổng số ledger blocks | 60 |
| Số block xác thực thành công | 56 |
| Số pipeline runs có kết quả verification | 14 |
| Số runs phát hiện lỗi | 0 |
| Số runs không phát hiện lỗi | 14 |
| Tỉ lệ lỗi hiển thị | 0,00% |

Ledger overview cho thấy mỗi pipeline run sinh 4 block theo thứ tự SOURCE, BRONZE, SILVER và GOLD. Với run benchmark 50.000 records, SOURCE, BRONZE và SILVER đều ghi nhận 50.000 records; GOLD ghi nhận 1.825 records sau aggregation theo ngày và sản phẩm.

*Lưu ý*: Dashboard export phản ánh trạng thái sau `RESET_BASELINE` — pipeline sạch. Detection coverage cho từng tamper scenario được đọc từ `verification_results` bằng cách chạy lại `06_run_tamper_scenarios.py`. Tamper scenarios là bộ kiểm thử trực tiếp để chứng minh detection khi trình bày.

#### 3.3.2. Kiểm tra H1 — Detection Coverage (DV1, DV2)

**H1**: Hash-chain ledger phát hiện 100% kịch bản tấn công được kiểm thử.

| Tamper Scenario (IV1) | DV1 kỳ vọng | DV1 thực tế | Phân loại |
|---|---|---|---|
| `NONE` | `VALID` | `VALID` | TN |
| `MODIFY_TRANSACTION_AMOUNT` | `DATA_TAMPERED` | `DATA_TAMPERED` | TP |
| `DELETE_TRANSACTION` | `RECORD_COUNT_MISMATCH` | `RECORD_COUNT_MISMATCH` | TP |
| `INSERT_FAKE_TRANSACTION` | `RECORD_COUNT_MISMATCH` | `RECORD_COUNT_MISMATCH` | TP |
| `MODIFY_LEDGER_BATCH_HASH` | `DATA_TAMPERED` | `DATA_TAMPERED` | TP |
| `MODIFY_LEDGER_TRANSFORMATION` | `BLOCK_TAMPERED` | `BLOCK_TAMPERED` | TP |
| `MODIFY_LEDGER_PREVIOUS_HASH` | `CHAIN_BROKEN` | `CHAIN_BROKEN` | TP |

$$
\text{Detection Rate (DV2)} = \frac{6}{6} \times 100\% = 100\%
$$

$$
\text{False Positive Rate} = \frac{0}{1} \times 100\% = 0\%
$$

**Kết luận H1**: Được hỗ trợ trong phạm vi 7 attack vectors được kiểm thử. Không được phép generalize sang attack vectors ngoài danh sách IV1 (giới hạn quasi-experimental do selection bias).

#### 3.3.3. Kiểm tra H2 — Overhead Scaling (DV3)

**H2**: Security overhead tăng theo kích thước dữ liệu và có quan hệ nhất quán, có thể đo lường được.

| Record count (IV2) | Quan sát từ dashboard | DV3 (Overhead xấp xỉ) |
|---:|---|---:|
| 1.000 | Overhead thấp nhất | khoảng 160% |
| 5.000 | Gần mức 1.000 | khoảng 155–160% |
| 10.000 | Tăng rõ so với nhóm nhỏ | khoảng 180% |
| 50.000 | Cao nhất trong biểu đồ | khoảng 220% |

Truy vấn lấy số liệu chính xác:

```sql
SELECT
    record_count,
    COUNT(*) AS measured_runs,
    AVG(baseline_duration_ms) AS avg_baseline_duration_ms,
    AVG(secured_duration_ms) AS avg_secured_duration_ms,
    AVG(verification_duration_ms) AS avg_verification_duration_ms,
    AVG(overhead_percent) AS avg_overhead_percent,
    percentile_approx(overhead_percent, 0.5) AS median_overhead_percent
FROM experiment_metrics
WHERE is_warmup = false
GROUP BY record_count
ORDER BY record_count;
```

Verification latency dao động từ 24.000 ms đến 31.000 ms. Điểm latency bất thường phản ánh cold start — uncontrolled variable đã ghi nhận tại PH.6.

**Kết luận H2**: Overhead có xu hướng tăng theo record count — quan hệ nhất quán và đo lường được. H2 được hỗ trợ với cảnh báo về variance do compute state không ổn định (uncontrolled variable).

#### 3.3.4. Kiểm tra H3 — Lineage Traceability (DV4)

**H3**: Kết hợp `first_broken_block`, `pipeline_run_id`, `pipeline_stage` và `lineage_events` xác định chính xác nguồn gốc sai lệch.

Lineage mẫu trên dashboard:

| Luồng xử lý | Input records | Output records | Status |
|---|---:|---:|---|
| SOURCE → BRONZE | 10.000 | 10.000 | SUCCESS |
| BRONZE → SILVER | 10.000 | 10.000 | SUCCESS |
| SILVER → GOLD | 10.000 | 1.825 | SUCCESS |

Khi verification phát hiện lỗi, quy trình phân tích để đo DV4:

```text
verification_results
    → first broken block
    → pipeline_run_id + stage
    → lineage_events
    → source/target table + transformation context
```

Record count đầu vào/đầu ra cho thấy transformation GOLD giảm dữ liệu từ 10.000 records xuống 1.825 records do aggregation — nhất quán với vai trò của Gold layer trong Medallion Architecture. Khi tamper xảy ra tại SILVER, `first_broken_block` chỉ đúng stage SILVER; lineage event tương ứng chứa đúng transformation context.

**Kết luận H3**: Được hỗ trợ. Trong tất cả tamper scenarios kiểm thử, `first_broken_block` chỉ đúng stage bị tấn công; lineage event tương ứng chứa đúng transformation context.

### 3.4. Đánh giá Data Governance Architecture

Mô hình đáp ứng các miền Data Governance chính:

| Miền Governance | Cơ chế trong mô hình |
|---|---|
| Data Quality | Schema validation, deduplication, type normalization, consistency check `amount = quantity * unit_price`. |
| Data Lineage | Ghi source/target stage, transformation, record count, batch hash, execution time và status. |
| Data Integrity | SHA-256 batch hash, schema hash, record count verification và block hash. |
| Data Auditing | Lưu verification history, failure reason, first broken block và pipeline run ID. |
| Monitoring | Dashboard KPI cho pipeline runs, ledger blocks, verification status, latency và overhead. |

Mô hình phù hợp với các hệ thống cần auditability, phát hiện thay đổi dữ liệu sau xử lý và truy vết transformation theo pipeline run. Kiến trúc có thể tích hợp vào pipeline hiện có vì không yêu cầu thay đổi toàn bộ dữ liệu nghiệp vụ; hệ thống chỉ bổ sung lớp evidence gồm hash, ledger, lineage và verification result.

---

## KẾT LUẬN VÀ GIỚI HẠN NGHIÊN CỨU

### K.1. Tóm tắt kết quả theo Hypothesis

Dựa trên thiết kế quasi-experimental với ba independent variables (IV1: tamper scenario, IV2: record count, IV3: pipeline stage) và bốn dependent variables (DV1–DV4):

| Hypothesis | Kết quả | Ghi chú |
|---|---|---|
| **H1** — Detection coverage 100% | **Được hỗ trợ** | Trong phạm vi 7 attack vectors kiểm thử (6 TP, 1 TN, 0 FN, 0 FP). |
| **H2** — Overhead tăng nhất quán theo record count | **Được hỗ trợ** | Overhead 160% (1K records) → 220% (50K records); variance do uncontrolled compute state. |
| **H3** — Lineage xác định chính xác nguồn gốc sai lệch | **Được hỗ trợ** | First_broken_block và lineage event khớp đúng stage và transformation trong mọi kịch bản. |

Kết hợp SHA-256, Data Lineage và hash-linked ledger minh chứng khả năng thiết lập một lớp kiểm chứng tamper-evident cho Data Pipeline. Mô hình không ngăn tuyệt đối mọi thay đổi ở tầng vật lý, nhưng thiết lập bằng chứng để phát hiện và định vị sai lệch.

### K.2. Giới hạn phương pháp nghiên cứu (Methodological Limitations)

| Giới hạn | Loại | Tác động |
|---|---|---|
| **Single environment (Databricks Free Edition)** | External validity | Kết quả không thể generalize sang AWS Glue, on-premise Spark, hoặc dbt không qua kiểm thử độc lập. |
| **Synthetic dataset** | External validity | Phân phối đồng đều, không có schema drift hay null-heavy fields — kết quả H1 có thể không giữ nguyên với production data. |
| **Simulated threat actors** | Internal validity | 7 tamper scenarios không bao phủ toàn bộ attack space; attacker thực tế với quyền admin có thể sửa cả ledger và dữ liệu đồng thời. |
| **Uncontrolled compute state** | Internal validity | Cold start và cluster variability làm tăng variance của DV3; overhead estimates là approximate. |
| **No randomization** | Quasi-experimental | Không thể suy ra causal relationship mạnh; kết quả là evidence of association, không phải causal proof. |
| **Self-instrumentation** | Instrumentation bias | Verification engine là cùng hệ thống được đánh giá — không có bên thứ ba kiểm chứng kết quả. |

### K.3. Hướng cải thiện thiết kế Quasi-experimental (Future Work)

| Hướng cải thiện | Cách tiếp cận | Mục tiêu |
|---|---|---|
| **Mở rộng IV1 — attack vectors** | Thêm partial content replacement, concurrent tamper, timing-based attacks | Tăng coverage H1; tìm false negative ngoài 7 vectors hiện tại |
| **Tăng số môi trường thử nghiệm** | Triển khai lại trên AWS Glue, on-premise Spark, dbt | Kiểm tra generalizability — giảm snowflake bias |
| **Dùng dữ liệu thực (ẩn danh hóa)** | Thay synthetic dataset bằng anonymized transaction data | Tăng ecological validity của H1 và H2 |
| **Kiểm soát compute state** | Dùng dedicated cluster với warm-up standardized; đo nhiều lần | Giảm variance DV3; chuyển từ approximate sang precise measurement |
| **Externalize ledger** | Lưu checkpoint hash trên Blockchain thực (public chain) hoặc hệ thống độc lập | Kiểm tra H1 dưới điều kiện trust boundary mạnh hơn |
| **Ký số block** | Thêm digital signature vào mỗi block | Phân biệt tamper từ insider vs. external attacker |
| **Adversarial testing với red team thực** | Hợp tác với security team để test attack không được mô hình hóa | Gần với true experiment; giảm selection bias của IV1 |
| **Thay batch hash tuyến tính bằng Merkle Tree** | Partition-level hash → Merkle root | Kiểm tra H2 ở quy mô 500K+ records; xác định threshold scalability |

---

*Artifact kỹ thuật — mã nguồn, notebook Databricks, unit test, SQL dashboard và tài liệu chạy lại:*

```text
https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc
```

Repository này hỗ trợ kiểm tra tái lập kết quả thực nghiệm và đối chiếu giữa mô hình kiến trúc với phần triển khai.
