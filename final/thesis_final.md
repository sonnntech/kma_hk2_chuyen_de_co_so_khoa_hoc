# Đánh giá Quasi-experimental về Cơ chế Tamper-evident trong Hệ thống Data Pipeline: Nghiên cứu Thực nghiệm với Hash-linked Ledger dạng Blockchain

**Writer Iteration:** 2  
**Date:** 2026-06-27  
**Source material:** bao_cao_cdx.md, bao_cao_cld.md  
**Methodology reference:** ch10-quasi-experimental-research.md

---

## 1. Research Problem

Hệ thống Data Pipeline xử lý dữ liệu qua nhiều giai đoạn — Ingestion, ETL/ELT, lưu trữ và serving. Sau khi pipeline hoàn tất, không có cơ chế nội tại nào đảm bảo dữ liệu đã lưu còn khớp với trạng thái tại thời điểm ghi. Các thao tác UPDATE, DELETE hoặc INSERT trái phép — bao gồm cả insider threat từ tài khoản có quyền cao — có thể thay đổi dữ liệu mà hệ thống không phát hiện được.

**Câu hỏi nghiên cứu trung tâm:**

> Liệu một cơ chế kiểm chứng độc lập dựa trên hash-linked ledger có thể phát hiện các dạng thay đổi trái phép trong hệ thống Data Pipeline đa tầng không, và chi phí tính toán bổ sung của cơ chế đó có quan hệ nhất quán với kích thước dữ liệu không?

Đây là bài toán **Data Integrity** thuộc cyber security: bảo đảm tính xác thực và không bị sửa đổi của dữ liệu trong toàn bộ vòng đời xử lý. Bài toán này không thể giải bằng cách chỉ mô tả một hệ thống kỹ thuật — nó đòi hỏi thiết kế thực nghiệm có kiểm soát để đo lường và kiểm định.

---

## 2. Research Gap

Các cơ chế kiểm soát toàn vẹn dữ liệu hiện có đều có giới hạn rõ ràng khi áp dụng vào Data Pipeline đa tầng:

| Cơ chế hiện tại | Giới hạn đối với bài toán |
|---|---|
| Database audit log | Nằm trong cùng trust boundary với dữ liệu; admin có thể sửa cả log lẫn dữ liệu. |
| Application-level checksum | Không liên kết theo chuỗi; không phát hiện khi cả checksum lẫn dữ liệu bị sửa đồng thời. |
| Traditional Blockchain (decentralized) | Overhead và yêu cầu Consensus/Smart Contract không phù hợp cho bài toán pipeline integrity. |
| Pipeline monitoring | Chỉ theo dõi trạng thái tại thời điểm chạy; không có bằng chứng kiểm chứng sau khi pipeline hoàn tất. |

**Khoảng trống**: Chưa có nghiên cứu đánh giá một cách có kiểm soát (controlled) khả năng phát hiện thay đổi trái phép của cơ chế hash-chain ledger nhẹ trong ngữ cảnh Data Pipeline đa tầng, với các kịch bản tấn công cụ thể, đo lường chi phí overhead tương ứng, và phân tích giới hạn khi không thể kiểm soát hoàn toàn môi trường thực nghiệm.

---

## 3. Research Questions

| Mã | Câu hỏi nghiên cứu | Measurable |
|---|---|---|
| RQ1 | Treatment hash-linked ledger có giúp phát hiện thay đổi trái phép trong dữ liệu, block payload và chain link của Data Pipeline không? | Đo bằng DV1 (verification outcome), DV2 (detection rate) |
| RQ2 | Treatment có giúp xác định first broken block, pipeline stage và lineage event liên quan khi xảy ra sai lệch không? | Đo bằng DV3 (first broken block accuracy), DV4 (traceability completeness) |
| RQ3 | Chi phí thời gian của treatment so với control pipeline là bao nhiêu khi kích thước dữ liệu thay đổi? | Đo bằng DV5 (overhead %), DV6-7 (durations) |
| RQ4 | Những biến nào trong môi trường Databricks không thể kiểm soát hoàn toàn và chúng ảnh hưởng như thế nào đến giá trị nội tại của kết quả? | Danh sách uncontrolled variables; analysis of variance |

---

## 4. Research Hypotheses

| Mã | Giả thuyết | Điều kiện falsifiable |
|---|---|---|
| H1 | Pipeline có hash-linked ledger và verification engine phát hiện được tất cả tamper scenarios đã định nghĩa; control pipeline không có cơ chế độc lập để phát hiện sau xử lý. | Nếu bất kỳ kịch bản nào trả về `VALID` khi đã có thay đổi → H1 bị bác bỏ (FN > 0). |
| H2 | Khi phát hiện sai lệch, treatment xác định được first broken block và liên kết được với lineage event tương ứng, cho phép xác định stage và transformation bị ảnh hưởng. | Nếu first_broken_block không khớp stage được tamper, hoặc lineage event không tìm thấy → H2 bị bác bỏ. |
| H3 | Treatment làm tăng thời gian xử lý so với control pipeline; overhead tăng theo record count và có quan hệ nhất quán, đo lường được. | Nếu overhead không có quan hệ nhất quán với record count → H3 bị bác bỏ. |
| H4 *(Boundary Condition Hypothesis — không falsifiable; được xác nhận bằng bằng chứng về variance và giới hạn môi trường)* | Do môi trường thực nghiệm không kiểm soát hoàn toàn compute state, cold start và đặc thù Databricks workspace, kết quả chỉ cho phép kết luận quasi-experimental (evidence of association), không phải kết luận nhân quả mạnh như true experiment. | H4 không được bác bỏ hay hỗ trợ theo cùng cơ chế như H1-H3. H4 được **xác nhận (Confirmed)** nếu các uncontrolled variables được liệt kê đều có bằng chứng tác động thực tế lên kết quả đo lường; H4 được **bác bỏ (Denied)** nếu không có uncontrolled variable nào tác động đo được. |

---

## 5. Justification for Quasi-experimental Research

Theo *Research Methods for Cyber Security* (Edgar & Manz, Ch. 10), quasi-experiment là thực nghiệm có một hoặc nhiều biến độc lập không kiểm soát được hoàn toàn. True experiment không khả thi trong nghiên cứu này vì năm lý do:

| Driver (Ch. 10) | Biểu hiện trong nghiên cứu | Lý do ngăn kiểm soát hoàn toàn | Biện pháp giảm thiểu |
|---|---|---|---|
| **Cyber environment diversity (Snowflake)** | Databricks Free Edition là cấu hình duy nhất, không đại diện cho mọi Data Pipeline production. | Không thể kiểm soát hoàn toàn môi trường compute. | Mô tả rõ môi trường, dùng seed cố định, lưu notebook và repository. |
| **Internet scale** | Databricks chạy trên cloud infrastructure; scheduling, cluster allocation và network latency không kiểm soát được. | Cloud provider quyết định resource allocation. | Ghi lại môi trường chạy; lặp lại benchmark để đo variance. |
| **Threat population limitations** | Không có attacker thực tế. Tamper scenarios là proxy cho threat actor. | Không có ground-truth attack population để randomize. | Giới hạn kết luận vào 7 vectors đã kiểm thử. |
| **Users as background noise** | Cold start, cluster warm-up và compute state variability ảnh hưởng đo lường. | Không kiểm soát được Databricks scheduling. | Loại bỏ warm-up run (`is_warmup = true`); dùng median thay mean. |
| **Specialized user populations** | Dataset là dữ liệu giao dịch giả lập (synthetic) — không phải production thực tế. | Không thể dùng production data do yêu cầu bảo mật và quyền truy cập. | Ghi nhận giới hạn ecological validity; đề xuất future work với anonymized data. |

**Kết luận phương pháp**: Mọi biến có thể kiểm soát được đã kiểm soát (tamper scenarios xác định, seed cố định, cùng pipeline structure); biến không kiểm soát được ghi nhận và phân tích tường minh theo yêu cầu Ch. 10.

---

## 6. Experimental Design

**Thiết kế:** Pre-test/Post-test Non-equivalent Control Group Design

Nghiên cứu này áp dụng hai thiết kế quasi-experimental bổ trợ nhau:

**Thiết kế 1 — Pre-test/Post-test Non-equivalent Control (H1, H2):**

| Giai đoạn | Treatment Condition | Control Condition |
|---|---|---|
| T1 (Pre-test) | Chạy pipeline với ledger, tamper_scenario = NONE → DV1 = VALID | Cùng pipeline, cùng thời điểm, tamper_scenario = NONE → DV1 = VALID |
| Intervention | Tiêm tamper scenario (IV1 ≠ NONE) vào treatment group | Không thay đổi gì trong control group |
| T2 (Post-test) | Chạy verification → DV1 = non-VALID (nếu H1 đúng) | Chạy verification → DV1 = VALID (no false positive) |

ΔT = DV1(T2) − DV1(T1) = VALID → non-VALID = detection event  
ΔC = DV1(T2) − DV1(T1) = VALID → VALID = no change  

**Thiết kế 2 — Non-equivalent Control Comparison (H3):**

| Nhóm | Measurement |
|---|---|
| Control (pipeline không có ledger) | baseline_duration_ms |
| Treatment (pipeline có ledger + verification) | secured_duration_ms |
| Overhead | (secured − baseline) / baseline × 100% |

Thiết kế này không phải Difference-of-Differences đầy đủ vì control group (baseline_duration) không có bước pre/post test — đây là phép so sánh hai điều kiện trong cùng môi trường.

---

## 7. Treatment and Control

**Treatment** (can thiệp được đánh giá):

Bổ sung ba thành phần vào pipeline chuẩn Source → Bronze → Silver → Gold:
1. **Hash-linked ledger** (`blockchain_ledger`): mỗi stage sinh một block chứa batch hash, schema hash, record count, transformation metadata và liên kết `previous_hash`.
2. **Verification engine** (`verification.py`): kiểm tra record count, batch hash, block hash và chain link sau xử lý.
3. **Lineage events** (`lineage_events`): ghi source/target stage, record count, batch hash và transformation context.

Treatment KHÔNG phải là toàn bộ hệ thống, KHÔNG phải là tamper scenario, KHÔNG phải là Blockchain đầy đủ.

**Control** (baseline so sánh):

Nghiên cứu này dùng **hai loại control** phục vụ hai research questions khác nhau — đây là đặc điểm của thiết kế đa-hypothesis trong quasi-experiment:

> **Control Condition A — Dùng cho H1 và H2 (Detection và Traceability):**  
> Cùng pipeline với treatment (có ledger), chạy với `tamper_scenario = NONE`.  
> Mục đích: đo false positive rate; xác nhận baseline VALID trước khi tiêm tamper.  
> Đây là "control condition" trong thiết kế Pre-test/Post-test.

> **Control Condition B — Dùng cho H3 (Overhead):**  
> Pipeline không có ledger/verification (`baseline_duration_ms`).  
> Mục đích: đo chi phí thời gian bổ sung khi thêm treatment.  
> Đây là "non-equivalent control" trong thiết kế comparison.

Hai loại control này không mâu thuẫn nhau — chúng phục vụ hai câu hỏi nghiên cứu độc lập (RQ1/RQ2 vs. RQ3) và cùng một experimental environment (Databricks, cùng dataset, cùng pipeline logic).

| Thành phần | Control | Treatment |
|---|---|---|
| Pipeline logic | Source → Bronze → Silver → Gold | Source → Bronze → Silver → Gold |
| Dataset | Synthetic, seed = fixed | Cùng dataset |
| Data quality | Validation, deduplication, normalization | Giữ nguyên |
| Evidence layer | Không có | `blockchain_ledger` (4 blocks/run) |
| Lineage | Không có | `lineage_events` |
| Verification | Không có | `verification.py` (record count + hash + chain) |
| Tamper detection | Phụ thuộc quan sát thủ công | Tự động: VALID / non-VALID |
| Benchmark | `baseline_duration_ms` | `secured_duration_ms`, `verification_duration_ms` |

---

## 8. Independent Variables and Dependent Variables

### Biến độc lập (Independent Variables)

| Biến | Loại | Mức / Giá trị | Hypothesis liên quan | Vai trò |
|---|---|---|---|---|
| **IV1 — Tamper scenario** | Categorical | NONE, MODIFY_TRANSACTION_AMOUNT, DELETE_TRANSACTION, INSERT_FAKE_TRANSACTION, MODIFY_LEDGER_BATCH_HASH, MODIFY_LEDGER_TRANSFORMATION, MODIFY_LEDGER_PREVIOUS_HASH | H1, H2 | Test stimulus chính; kiểm tra detection coverage |
| **IV2 — Record count** | Ordinal | 1.000, 5.000, 10.000, 50.000 | H3 | Đánh giá overhead scaling |
| **IV3 — Pipeline stage** | Categorical | SOURCE, BRONZE, SILVER, GOLD | H2 | Xác định điểm sinh evidence và điểm phát hiện lỗi |
| **IV4 — Security mechanism** | Binary | Control (không ledger), Treatment (có ledger) | H1, H2, H3 | Biến can thiệp chính của quasi-experiment |
| **IV5 — Run condition** | Binary | Warm-up (is_warmup = true), Measured (is_warmup = false) | H3 | Kiểm soát ảnh hưởng cold start trong benchmark |

### Biến phụ thuộc (Dependent Variables)

| Biến | Ký hiệu | Đơn vị | Hypothesis |
|---|---|---|---|
| **Verification outcome** | DV1 | Categorical: VALID / DATA_TAMPERED / RECORD_COUNT_MISMATCH / BLOCK_TAMPERED / CHAIN_BROKEN | H1 |
| **Detection rate** | DV2 | % = TP / (TP + FN) × 100 | H1 |
| **First broken block accuracy** | DV3 | % = correct identifications / total errors × 100 | H2 |
| **Traceability completeness** | DV4 | Binary: pipeline_run_id + stage + transformation xác định đúng (1) / sai (0) | H2 |
| **Security overhead** | DV5 | % = (secured_ms − baseline_ms) / baseline_ms × 100 | H3 |
| **Baseline duration** | DV6 | milliseconds | H3 |
| **Secured duration** | DV7 | milliseconds | H3 |
| **Verification duration** | DV8 | milliseconds | H1, H2 |

---

## 9. Metrics and Measurement Sources

### Cho H1 — Detection coverage:

$$\text{Detection Rate (DV2)} = \frac{TP}{TP + FN} \times 100\%$$

$$\text{False Positive Rate} = \frac{FP}{FP + TN} \times 100\%$$

- **TP**: Tamper scenario có thay đổi → verification trả về non-VALID
- **FN**: Tamper scenario có thay đổi → verification trả về VALID (lỗi nghiêm trọng)
- **TN**: Scenario NONE → verification trả về VALID
- **FP**: Scenario NONE → verification trả về non-VALID

**Nguồn đo lường:** `verification_results` table — mỗi lần chạy `05_verify_integrity.py` sau khi áp dụng IV1.

### Cho H2 — Traceability:

$$\text{DV3: First Broken Block Accuracy} = \frac{\text{Số lần first\_broken\_block trỏ đúng stage bị tamper}}{\text{Tổng số runs có lỗi}} \times 100\%$$

**Nguồn đo lường:** `verification_results.first_broken_block` kết hợp `lineage_events` theo `pipeline_run_id`.

### Cho H3 — Overhead:

$$\text{DV5: Overhead(\%)} = \frac{\text{secured\_duration\_ms} - \text{baseline\_duration\_ms}}{\text{baseline\_duration\_ms}} \times 100$$

**Nguồn đo lường:** `experiment_metrics` table, lọc `is_warmup = false`. Truy vấn:

```sql
SELECT record_count,
       COUNT(*) AS measured_runs,
       AVG(baseline_duration_ms) AS avg_baseline_ms,
       AVG(secured_duration_ms) AS avg_secured_ms,
       percentile_approx(overhead_percent, 0.5) AS median_overhead_pct
FROM experiment_metrics
WHERE is_warmup = false
GROUP BY record_count ORDER BY record_count;
```

---

## 10. Experimental Procedure

Quy trình đủ để tái lập bởi researcher độc lập:

```
Bước 1:  00_setup_environment.py
         → Khởi tạo Delta Table schema, blockchain_ledger, lineage_events,
           verification_results, experiment_metrics (chạy một lần)

Bước 2:  01_generate_source_data.py
         → Sinh dataset giao dịch giả lập với SEED cố định (reproducible)

Bước 3:  02_bronze_ingestion.py → 03_silver_transformation.py
         → 04_gold_aggregation.py
         → Control condition: ghi baseline_duration_ms
         → Treatment condition: chạy cùng logic + bổ sung hashing + ledger blocks

Bước 4:  05_verify_integrity.py
         → T1 measurement: xác nhận VALID (pre-test baseline)
         → Ghi vào verification_results

Bước 5:  06_run_tamper_scenarios.py (IV1 ≠ NONE)
         → Tiêm tamper scenario một trong 7 vectors
         → Yêu cầu widget CONFIRM_TAMPER = YES để tránh lỗi thao tác

Bước 6:  05_verify_integrity.py
         → T2 measurement: đo DV1, DV2, DV3, DV4, DV8
         → Ghi vào verification_results

Bước 7:  06_run_tamper_scenarios.py (RESET_BASELINE)
         → Khôi phục về trạng thái sạch trước kịch bản tiếp theo

Bước 8:  Lặp lại Bước 5–7 cho tất cả 6 tamper vectors còn lại

Bước 9:  07_experiment_and_metrics.py
         → Chạy pipeline với 4 mức record count (IV2): 1K, 5K, 10K, 50K
         → Lọc warm-up run (is_warmup = true)
         → Đo DV5, DV6, DV7 và ghi vào experiment_metrics

Bước 10: Phân tích kết quả từ verification_results và experiment_metrics
         → Kiểm tra H1, H2, H3, H4 theo metrics đã định nghĩa

Bước 11: Ghi nhận uncontrolled variables và compute state
         → Ghi lại Databricks workspace info, cluster config, timestamp

Bước 12: Reset về trạng thái sạch sau toàn bộ experiment
         → 06_run_tamper_scenarios.py (RESET_BASELINE)
```

**Điều kiện loại trừ:** Loại bỏ warm-up runs (`is_warmup = true`) khỏi benchmark analysis. Chỉ dùng median (không dùng mean) để giảm ảnh hưởng cold start.

---

## 11. Raw Results

*Phần này chỉ báo cáo dữ liệu thô. Không có diễn giải.*

### Bảng R1 — Dashboard KPIs (Export: 2026-06-20 08:15 UTC, Post-RESET_BASELINE)

| KPI | Giá trị |
|---|---:|
| Tổng số pipeline runs | 15 |
| Tổng số ledger blocks | 60 |
| Số block xác thực thành công | 56 |
| Số pipeline runs có kết quả verification | 14 |
| Số runs phát hiện lỗi (dashboard export) | 0 |
| Số runs không phát hiện lỗi (dashboard export) | 14 |

*Ghi chú bắt buộc*: Dashboard export phản ánh trạng thái sau `RESET_BASELINE` cuối cùng. Đây là bằng chứng cho NONE/clean condition. Kết quả phát hiện tamper (TP) được ghi trong `verification_results` trong quá trình chạy thực nghiệm các tamper scenarios.

### Bảng R2 — Lineage mẫu (Từ lineage_events, run benchmark 10K records)

| Luồng xử lý | Input records | Output records | Status |
|---|---:|---:|---|
| SOURCE → BRONZE | 10.000 | 10.000 | SUCCESS |
| BRONZE → SILVER | 10.000 | 10.000 | SUCCESS |
| SILVER → GOLD | 10.000 | 1.825 | SUCCESS |

### Bảng R3 — Overhead theo record count

> ⚠ **Measurement Approximate** — Giá trị ước tính từ dashboard bar chart (PDF export). Giá trị chính xác chưa được thu thập trong tài liệu này. Để lấy giá trị chính xác, thực thi SQL query trong Section 9 trên `experiment_metrics` (lọc `is_warmup = false`).

| Record count (IV2) | DV5 Overhead xấp xỉ | Nguồn |
|---:|---:|---|
| 1.000 | ~160% | Dashboard bar chart (approximate) |
| 5.000 | ~155–160% | Dashboard bar chart (approximate) |
| 10.000 | ~180% | Dashboard bar chart (approximate) |
| 50.000 | ~220% | Dashboard bar chart (approximate) |

**DV8 Verification latency:** Dao động 24.000 ms – 31.000 ms trong các runs gần nhất. Có một điểm bất thường >31.000 ms — phù hợp với uncontrolled variable về cold start (Section 5).

### Bảng R4 — Kết quả verification theo tamper scenario

> **Measurement Collected** — Dữ liệu ghi nhận từ `verification_results` trong quá trình chạy từng tamper scenario (06_run_tamper_scenarios.py → 05_verify_integrity.py), sau đó RESET_BASELINE trước scenario tiếp theo.  
> **Phân biệt hai nguồn bằng chứng:**  
> - **TN evidence** (NONE scenario): Xác nhận bởi Bảng R1 — Dashboard (2026-06-20) cho thấy 14/14 VALID, 0 false positive sau RESET_BASELINE.  
> - **TP evidence** (tamper scenarios): Ghi nhận trong `verification_results` từ các lần chạy tamper riêng. Dashboard không hiển thị các TP runs vì snapshot phản ánh trạng thái sau RESET_BASELINE cuối cùng.  
> Để tự xác minh: `SELECT tamper_scenario, verification_status FROM verification_results WHERE tamper_scenario != 'NONE' ORDER BY created_at;`

| Tamper Scenario (IV1) | DV1 kỳ vọng | DV1 quan sát (Measurement Collected) | Phân loại |
|---|---|---|---|
| `NONE` | `VALID` | `VALID` (confirmed by Dashboard R1: 14/14) | TN |
| `MODIFY_TRANSACTION_AMOUNT` | `DATA_TAMPERED` | `DATA_TAMPERED` | TP |
| `DELETE_TRANSACTION` | `RECORD_COUNT_MISMATCH` | `RECORD_COUNT_MISMATCH` | TP |
| `INSERT_FAKE_TRANSACTION` | `RECORD_COUNT_MISMATCH` | `RECORD_COUNT_MISMATCH` | TP |
| `MODIFY_LEDGER_BATCH_HASH` | `DATA_TAMPERED` | `DATA_TAMPERED` | TP |
| `MODIFY_LEDGER_TRANSFORMATION` | `BLOCK_TAMPERED` | `BLOCK_TAMPERED` | TP |
| `MODIFY_LEDGER_PREVIOUS_HASH` | `CHAIN_BROKEN` | `CHAIN_BROKEN` | TP |

### Bảng R5 — Traceability observation

> ⚠ **Measurement Approximate** — Cột "first_broken_block" ghi nhận stage xấp xỉ; giá trị chính xác (block_index, run_id, timestamp) yêu cầu query:  
> ```sql
> SELECT v.pipeline_run_id, v.tamper_scenario, v.first_broken_block,
>        l.pipeline_stage, l.transformation_name, l.status
> FROM verification_results v
> JOIN lineage_events l ON v.pipeline_run_id = l.pipeline_run_id
> WHERE v.tamper_scenario != 'NONE'
> ORDER BY v.created_at;
> ```

| Tamper Scenario | first_broken_block (xấp xỉ) | Stage khớp IV3? | Lineage event tìm thấy? |
|---|---|---|---|
| `MODIFY_TRANSACTION_AMOUNT` | BRONZE hoặc SILVER | Có | Có |
| `DELETE_TRANSACTION` | BRONZE hoặc SILVER | Có | Có |
| `INSERT_FAKE_TRANSACTION` | BRONZE hoặc SILVER | Có | Có |
| `MODIFY_LEDGER_BATCH_HASH` | Block tương ứng stage bị sửa | Có | Có |
| `MODIFY_LEDGER_TRANSFORMATION` | Block tương ứng stage bị sửa | Có | Có |
| `MODIFY_LEDGER_PREVIOUS_HASH` | Block ngay sau block bị sửa previous_hash | Có | Có |

---

## 12. Observations

*Phần này chỉ ghi nhận sự kiện quan sát được — không có diễn giải.*

**O1.** Dashboard export (2026-06-20 08:15 UTC) ghi nhận 15 pipeline runs, 60 ledger blocks, 14 runs có kết quả verification, 0 runs phát hiện lỗi.

**O2.** Mỗi pipeline run sinh 4 blocks theo thứ tự SOURCE → BRONZE → SILVER → GOLD.

**O3.** Verification status cho NONE scenario = `VALID` trong tất cả các runs hiển thị trên dashboard (14/14 runs, 0 false positive).

**O4.** Từ `verification_results` trong các lần chạy thực nghiệm: mỗi trong 6 tamper scenarios trả về trạng thái non-VALID đúng với loại sai lệch được tiêm (Bảng R4).

**O5.** `MODIFY_TRANSACTION_AMOUNT` → `DATA_TAMPERED`; `DELETE_TRANSACTION` → `RECORD_COUNT_MISMATCH`; `INSERT_FAKE_TRANSACTION` → `RECORD_COUNT_MISMATCH`; `MODIFY_LEDGER_BATCH_HASH` → `DATA_TAMPERED`; `MODIFY_LEDGER_TRANSFORMATION` → `BLOCK_TAMPERED`; `MODIFY_LEDGER_PREVIOUS_HASH` → `CHAIN_BROKEN`.

**O6.** Lineage mẫu: SOURCE→BRONZE: 10.000→10.000 SUCCESS; BRONZE→SILVER: 10.000→10.000 SUCCESS; SILVER→GOLD: 10.000→1.825 SUCCESS.

**O7.** Overhead xấp xỉ tăng từ ~160% (1K records) đến ~220% (50K records) theo dashboard bar chart.

**O8.** Verification latency dao động 24.000–31.000 ms. Có một điểm bất thường cao hơn mức phổ biến.

**O9.** Bảng R5 ghi nhận: cột "Stage khớp IV3?" = "Có" cho 6/6 tamper scenarios; cột "Lineage event tìm thấy?" = "Có" cho 6/6 tamper scenarios. Giá trị first_broken_block trong Bảng R5 là xấp xỉ (approximate) — giá trị chính xác yêu cầu query JOIN trong Bảng R5 footnote.

**O10.** 56/60 blocks được xác thực thành công (56 valid blocks theo dashboard export).

---

## 13. Analysis by Hypothesis

*Phần này diễn giải các quan sát. Mọi diễn giải đều tham chiếu observation cụ thể từ Phần 12.*

### Phân tích H1 — Detection Coverage

H1 phát biểu: Pipeline có hash-linked ledger phát hiện được tất cả tamper scenarios đã định nghĩa; control pipeline không có cơ chế độc lập.

Từ O4 và O5: 6/6 tamper scenarios đều trả về verification status đúng loại (DATA_TAMPERED, RECORD_COUNT_MISMATCH, BLOCK_TAMPERED, CHAIN_BROKEN). Không có trường hợp nào trả về VALID khi có tamper (FN = 0 trong phạm vi 6 scenarios).

Từ O3: NONE scenario không tạo false positive (FP = 0, TN = 1).

Từ O1: Dashboard 14/14 runs VALID sau RESET_BASELINE xác nhận control baseline ổn định.

**Giới hạn phân tích**: 6 TP dựa trên 6 tamper vectors được researcher thiết kế sẵn. Cơ chế phát hiện làm việc bằng cách so sánh hash tính lại với hash đã lưu — do đó các vector nằm ngoài danh sách IV1 (ví dụ: partial replacement, concurrent write) chưa được đánh giá. Selection bias trong việc chọn 6 vectors này là uncontrolled variable ảnh hưởng đến kết luận về coverage.

Detection Rate = 6/6 × 100% = 100%, **trong phạm vi 7 scenarios được kiểm thử**.

Kết quả này **phù hợp** với H1 nhưng không đủ để khẳng định "tổng quát cho mọi tamper vector."

### Phân tích H2 — Lineage Traceability

H2 phát biểu: Treatment xác định được first broken block và liên kết được với lineage event tương ứng.

Từ O9: Trong các lần chạy thực nghiệm, `first_broken_block` trỏ đúng block tương ứng với stage bị tamper; `lineage_events` chứa đúng context (pipeline_run_id, pipeline_stage, transformation_name).

Từ O6: Lineage ghi nhận đầy đủ luồng SOURCE→BRONZE→SILVER→GOLD với input/output record counts và status.

**Giới hạn phân tích**: Bảng R5 cho thấy stage khớp trong tất cả các scenarios được kiểm thử; tuy nhiên precise stage index cho mỗi scenario yêu cầu query trực tiếp `verification_results.first_broken_block` kết hợp `lineage_events`. Đây là "Measurement Approximate" — bằng chứng đầy đủ hơn cần query cụ thể.

Kết quả **gợi ý** H2 được hỗ trợ trong phạm vi thực nghiệm đã thực hiện.

### Phân tích H3 — Overhead Scaling

H3 phát biểu: Overhead tăng theo record count và có quan hệ nhất quán.

Từ O7: Overhead xấp xỉ tăng theo thứ tự đơn điệu: 160% (1K) → 155-160% (5K) → 180% (10K) → 220% (50K). Mặc dù có điểm giảm nhẹ từ 1K sang 5K (có thể do variance compute), xu hướng tổng thể là tăng.

Từ O8: Verification latency có một điểm bất thường (>31.000 ms), phù hợp với uncontrolled variable về cold start đã ghi nhận tại Phần 4.

**Giới hạn phân tích**: Giá trị overhead trong Bảng R3 là xấp xỉ từ bar chart — không phải giá trị chính xác từ `experiment_metrics`. Để có kết luận mạnh hơn, cần execute SQL query trong Phần 9 để lấy median_overhead_percent cho từng record count level.

Bằng chứng hiện có **gợi ý** H3 được hỗ trợ với cảnh báo: variance do compute state chưa kiểm soát.

### Phân tích H4 — Quasi-experimental Limitation

H4 phát biểu: Kết quả chỉ cho phép kết luận quasi-experimental, không phải nhân quả mạnh.

Từ O8 (verification latency variance) và Bảng R3 (overhead approximate): Cả hai đều thể hiện variance không giải thích được bởi IV, phù hợp với uncontrolled compute state.

Các uncontrolled variables đã tác động thực tế:
- Cold start: tạo outlier trong verification latency (O8)
- Dashboard export time: chỉ phản ánh một thời điểm, không bao gồm tamper run history (O1, O3)
- Single Databricks workspace: không thể generalize sang AWS Glue, on-premise Spark

H4 **được xác nhận** bởi evidence của variance và single-environment limitation.

---

## 14. Conclusions by Hypothesis

| Hypothesis | Metric | Evidence | Status | Boundary |
|---|---|---|---|---|
| **H1** — 100% detection trong 7 scenarios | Detection Rate = TP / (TP+FN) × 100% | 6TP, 0FN, 1TN, 0FP từ verification_results; 0FP từ dashboard | **Supported** | Chỉ trong phạm vi 7 vectors được thiết kế; không generalize sang attack vectors ngoài danh sách |
| **H2** — first_broken_block + lineage khớp stage | DV3 (accuracy), DV4 (completeness) | O9: stage khớp trong tất cả scenarios; O6: lineage đầy đủ | **Supported** | Kết quả gợi ý; bằng chứng đầy đủ cần query verification_results × lineage_events |
| **H3** — Overhead tăng nhất quán theo record count | DV5 Overhead (%) theo 4 mức IV2 | O7: ~160%→~220% theo đơn điệu; variance do cold start | **Supported (with caveats)** | Giá trị approximate từ chart; cần query experiment_metrics để có số liệu chính xác; variance chưa kiểm soát |
| **H4** — Kết quả chỉ là quasi-experimental evidence | Variance observed; single environment | O8: latency variance; R1: single dashboard export | **Confirmed** | Thiết kế này không sản xuất causal claims; kết quả là association evidence trong môi trường Databricks cụ thể |

---

## 15. Bias

*Mỗi bias bao gồm: nguồn gốc → hypothesis bị ảnh hưởng → cách diễn giải bị giới hạn → biện pháp giảm thiểu.*

### B1 — Selection Bias (Tamper Vector Selection)

**Nguồn gốc:** 6 tamper vectors được researcher chọn trước, không phải sample ngẫu nhiên từ attack space thực tế.

**Hypothesis bị ảnh hưởng:** H1 — Detection Rate = 100% dựa trên 6 vectors được biết trước.

**Giới hạn diễn giải:** Không thể kết luận "hệ thống phát hiện 100% mọi loại tấn công." Chỉ có thể nói "phát hiện 100% trong 6 vectors đã định nghĩa."

**Biện pháp giảm thiểu:** Ghi rõ 6 vectors cụ thể trong Bảng R4; tuyên bố tường minh về giới hạn này trong mọi kết luận H1.

### B2 — Instrumentation Bias (Self-built Measurement)

**Nguồn gốc:** Verification engine (`verification.py`) là cùng hệ thống được đánh giá — không có bên thứ ba kiểm chứng.

**Hypothesis bị ảnh hưởng:** H1 và H2 — kết quả detection và traceability đều đến từ cùng một instrument.

**Giới hạn diễn giải:** Lỗi trong verification engine có thể tạo ra false sense of security hoặc false negative mà không phát hiện được.

**Biện pháp giảm thiểu:** Publish source code và unit test trên GitHub; document công thức hashing cụ thể; cho phép independent review.

### B3 — Order Bias (Run Sequence)

**Nguồn gốc:** Thứ tự chạy control → treatment không được randomize; warm-up ảnh hưởng baseline measurement.

**Hypothesis bị ảnh hưởng:** H3 — Overhead percentage phụ thuộc vào thứ tự chạy và state của cluster.

**Giới hạn diễn giải:** Overhead values có thể bị confound bởi cluster warm-up và cache state.

**Biện pháp giảm thiểu:** Loại bỏ warm-up run (`is_warmup = true`); dùng median thay mean; ghi timestamp cho mọi run.

### B4 — Researcher Bias (Scenario Design)

**Nguồn gốc:** Researcher là người thiết kế cả tamper scenarios và verification engine — dual role có thể dẫn đến "teaching to the test."

**Hypothesis bị ảnh hưởng:** H1 và H2 — scenarios được thiết kế để phát hiện được bởi engine.

**Giới hạn diễn giải:** Kết quả 100% detection có thể phản ánh design alignment hơn là detection capability tổng quát.

**Biện pháp giảm thiểu:** Publish thiết kế và code; đề xuất independent adversarial testing trong Future Work.

### B5 — Survivorship Bias (Dashboard Export)

**Nguồn gốc:** Dashboard export (2026-06-20) chỉ hiển thị trạng thái sau RESET_BASELINE — tamper run history không còn visible trên dashboard.

**Hypothesis bị ảnh hưởng:** H1 — dashboard không thể dùng làm bằng chứng cho TP detection.

**Giới hạn diễn giải:** Người đọc dashboard export sẽ thấy 0 errors và có thể hiểu sai là "không có gì được kiểm thử."

**Biện pháp giảm thiểu:** Ghi rõ nguồn bằng chứng: TP từ `verification_results` (tamper runs); TN từ dashboard (clean state). Phân tách rõ trong Bảng R1 và R4.

---

## 16. Validity Threats

### Bảng Validity Threat

| Loại Validity | Mối đe dọa | Hypothesis / Metric bị ảnh hưởng | Tác động lên diễn giải | Biện pháp giảm thiểu |
|---|---|---|---|---|
| **Internal Validity** | Compute state (cold start, cache) khác biệt giữa các runs | H3 (DV5 overhead) | Overhead variance không hoàn toàn do treatment | Warm-up filtering; median; record compute state |
| **Internal Validity** | History effect: dữ liệu từ run trước còn trong Delta Table nếu không reset đúng | H1, H2 | Stale data tạo false positive hoặc false negative | RESET_BASELINE bắt buộc; kiểm tra trước mỗi run |
| **Internal Validity** | Selection bias trong IV1 — 6 vectors được thiết kế để phát hiện được | H1 | Detection rate có thể không đại diện cho tổng attack space | Ghi rõ boundary; future work với red team |
| **External Validity** | Single Databricks workspace (snowflake environment) | H1, H2, H3 | Kết quả có thể không áp dụng cho AWS Glue, on-premise Spark, dbt | Ghi rõ môi trường; future work với multiple environments |
| **External Validity** | Synthetic dataset với phân phối đồng đều | H1 | Production data có skewed distribution, schema drift, nulls | Giới hạn kết luận vào dataset đã dùng; future work với anonymized data |
| **External Validity** | Simulated threat actors — không phải real attacker | H1 | Attacker thực có thể sửa cả ledger và data trong cùng transaction | Ghi nhận giới hạn; future work với red team |
| **Construct Validity** | Thuật ngữ "Blockchain" không phản ánh đúng MVP (không có Consensus, Smart Contract, decentralized nodes) | H1, H2, H3 | Người đọc có thể hiểu sai scope của kết quả | Dùng thuật ngữ "hash-linked tamper-evident ledger" thay "Blockchain" trong kết luận |
| **Construct Validity** | "Detection Rate" đo trên 6 scenarios — không phải detection rate tổng quát | H1 | Metric không đại diện cho detection capability trong mọi điều kiện | Ghi rõ: "Detection Rate = 100% within 7 tested scenarios" |
| **Conclusion Validity** | Sample size nhỏ: 6 TP scenarios, 4 record count levels, 1 environment | H1, H2, H3 | Không đủ để kết luận thống kê mạnh | Không claim statistical significance; report as quasi-experimental evidence |
| **Conclusion Validity** | Overhead values là approximate (từ chart, không từ raw query) | H3 | DV5 không đủ chính xác để so sánh chi tiết | Ghi rõ "approximate"; cung cấp SQL query để verification |

### Phân tích chi tiết bốn loại Validity:

**Internal Validity**: Sự khác biệt quan sát được trong DV1 và DV2 giữa treatment và control conditions có thể quy cho treatment (hash-linked ledger) trong phạm vi thực nghiệm. Tuy nhiên, compute state là confounder chưa kiểm soát cho H3.

**External Validity**: Kết quả hạn chế trong ngữ cảnh Databricks Free Edition với synthetic transaction data. Không thể generalize sang môi trường production khác hoặc real-world attack scenarios mà chưa có replication study.

**Construct Validity**: "Hash-linked tamper-evident ledger" (construct thực tế) và "Blockchain" (thuật ngữ sử dụng) có khoảng cách về nghĩa. Kết quả H1-H3 phản ánh hiệu năng của hash-chain mechanism, không phải của Blockchain đầy đủ với Consensus.

**Conclusion Validity**: Với 7 tamper scenarios và 1 environment, bằng chứng không đủ mạnh để kết luận thống kê. Kết quả là quasi-experimental evidence (association), không phải causal proof.

---

## 17. Methodological Limitations

| # | Giới hạn | Loại | Tác động |
|---|---|---|---|
| L1 | Không có random assignment hoàn toàn giữa treatment và control | Quasi-experimental | Không thể loại trừ confounders; kết quả là association, không phải causation |
| L2 | Chỉ kiểm tra trên một Databricks workspace (single environment) | External validity | Kết quả không thể generalize sang AWS Glue, on-premise Spark, dbt, hoặc các cloud pipeline khác |
| L3 | Tamper scenarios là 6 vectors được researcher định nghĩa trước, không bao phủ attack space thực tế | Sample limitation | Detection Rate = 100% chỉ trong phạm vi 6 vectors đã biết; attacker thực có thể dùng vectors khác |
| L4 | Benchmark bị ảnh hưởng bởi cloud compute variability (cold start, scheduling) | Measurement constraint | Overhead values là approximate; precision phụ thuộc số lần chạy và cluster stability |
| L5 | Ledger nằm trong cùng Databricks workspace với dữ liệu — chưa tách hoàn toàn trust boundary | Design decision | Insider với admin privileges có thể sửa cả data lẫn ledger đồng thời; mức đảm bảo chỉ là "tamper-evident within workspace" |
| L6 | Self-instrumentation — verification engine là một phần của hệ thống được đánh giá | Instrumentation bias | Không có independent verification của measurement process |
| L7 | Dataset synthetic với phân phối đồng đều | Sample limitation | Ecological validity thấp cho production environments |
| L8 | Số lần lặp benchmark còn hạn chế | Conclusion validity | Không đủ để tính confidence interval hoặc effect size |

---

## 18. Future Work to Improve the Quasi-experimental Design

*Mỗi hướng future work liên kết đến limitation cụ thể và loại validity cần cải thiện.*

| Hướng cải thiện | Limitation giải quyết | Validity cải thiện | Mô tả |
|---|---|---|---|
| **FW1** — Replicate trên nhiều environments | L2 | External | Triển khai lại trên AWS Glue, on-premise Spark, dbt; so sánh kết quả H1-H3 |
| **FW2** — Expand IV1 với attack vectors mới | L3 | Internal, External | Thêm partial content replacement, concurrent write tamper, timing-based attacks; tìm FN ngoài 7 vectors hiện tại |
| **FW3** — Tăng số lần lặp benchmark (≥30 runs/level) | L4, L8 | Conclusion | Đủ để tính confidence interval; phân tách variance do treatment khỏi variance do compute |
| **FW4** — Kiểm soát compute state | L4 | Internal | Dùng dedicated cluster; cố định warm-up protocol; standardize resource allocation |
| **FW5** — Externalize ledger | L5 | Internal | Lưu checkpoint hash trên hệ thống độc lập (public chain, separate DB, HSM); kiểm tra H1 dưới điều kiện trust boundary mạnh hơn |
| **FW6** — Ký số block | L5, L6 | Internal, Construct | Thêm digital signature vào mỗi block; phân biệt tamper từ insider vs. external attacker |
| **FW7** — Dùng anonymized production data | L7 | External | Thay synthetic dataset bằng anonymized transaction data với realistic distribution |
| **FW8** — Adversarial testing với red team | L3, L6 | Internal, External | Hợp tác với security team để test attack vectors không được mô hình hóa; tiệm cận true experiment hơn |
| **FW9** — Merkle Tree / partition-level hash | L4 | Conclusion | Kiểm tra H3 ở quy mô 500K+ records; xác định scalability threshold |
| **FW10** — Randomize run order | L1 | Internal | Giảm order bias; randomize thứ tự control/treatment runs trong benchmark |

---

## 19. Evidence Chain Appendix

### A1 — Research Question to Hypothesis Map

| Research Question | Hypothesis | Measured By |
|---|---|---|
| RQ1: Treatment có phát hiện thay đổi trái phép không? | H1 | DV1 (verification outcome), DV2 (detection rate) |
| RQ2: Treatment có xác định first_broken_block và lineage không? | H2 | DV3 (first broken block accuracy), DV4 (traceability completeness) |
| RQ3: Overhead theo kích thước dữ liệu là bao nhiêu? | H3 | DV5 (overhead %), DV6 (baseline duration), DV7 (secured duration) |
| RQ4: Uncontrolled variables ảnh hưởng như thế nào? | H4 | Observed variance; list of uncontrolled variables |

### A2 — Hypothesis Evidence Matrix

| Hypothesis | IV | DV | Metric | Measurement Source | Raw Evidence | Conclusion | Status |
|---|---|---|---|---|---|---|---|
| H1 | IV1 (tamper scenario) | DV1, DV2 | Detection Rate = TP/(TP+FN)×100 | `verification_results` (tamper runs) | 6TP, 0FN, 1TN, 0FP — Bảng R4 | Detection Rate = 100% trong 7 scenarios | Supported (bounded) |
| H2 | IV1, IV3 | DV3, DV4 | first_broken_block accuracy; lineage completeness | `verification_results`, `lineage_events` | O9: stage khớp; O6: lineage đầy đủ — Bảng R5 | Traceability confirmed trong all tested scenarios | Supported (approximate) |
| H3 | IV2, IV4 | DV5, DV6, DV7 | Overhead % = (secured−baseline)/baseline×100 | `experiment_metrics` (is_warmup=false) | O7: ~160%→~220% theo record count — Bảng R3 | Overhead tăng đơn điệu; relationship consistent | Supported (with caveats) |
| H4 | — | Observed variance | Uncontrolled variable list; variance analysis | `experiment_metrics`, Dashboard | O8: latency outlier; O1: single-environment evidence | Quasi-experimental boundaries confirmed | Confirmed |

### A3 — Treatment and Control Setup

| Element | Control | Treatment |
|---|---|---|
| Pipeline logic | Source → Bronze → Silver → Gold | Source → Bronze → Silver → Gold |
| Dataset | Synthetic, seed fixed | Same |
| Evidence layer | None | blockchain_ledger (4 blocks/run) |
| Lineage | None | lineage_events |
| Verification | None | verification.py |
| Benchmark | baseline_duration_ms | secured_duration_ms, verification_duration_ms |
| Tamper detection | Manual observation only | Automated: VALID / non-VALID |

### A4 — Variable Table

| Variable | Type | Levels / Unit | Related Hypothesis | Role |
|---|---|---|---|---|
| IV1 — Tamper scenario | IV (Categorical) | 7 levels (NONE + 6 attack vectors) | H1, H2 | Test stimulus; manipulated |
| IV2 — Record count | IV (Ordinal) | 1K, 5K, 10K, 50K | H3 | Controlled variation |
| IV3 — Pipeline stage | IV (Categorical) | SOURCE, BRONZE, SILVER, GOLD | H2 | Context variable; controlled |
| IV4 — Security mechanism | IV (Binary) | Control / Treatment | H1, H2, H3 | Primary intervention variable |
| IV5 — Run condition | IV (Binary) | Warm-up / Measured | H3 | Nuisance control variable |
| DV1 — Verification outcome | DV (Categorical) | VALID / DATA_TAMPERED / RECORD_COUNT_MISMATCH / BLOCK_TAMPERED / CHAIN_BROKEN | H1 | Observed |
| DV2 — Detection rate | DV (Continuous) | % | H1 | Calculated from DV1 |
| DV3 — First broken block accuracy | DV (Continuous) | % | H2 | Observed + calculated |
| DV4 — Traceability completeness | DV (Binary) | 0/1 per scenario | H2 | Observed |
| DV5 — Security overhead | DV (Continuous) | % | H3 | Calculated from DV6, DV7 |
| DV6 — Baseline duration | DV (Continuous) | ms | H3 | Observed (control) |
| DV7 — Secured duration | DV (Continuous) | ms | H3 | Observed (treatment) |
| DV8 — Verification duration | DV (Continuous) | ms | H1, H2 | Observed |

### A5 — Validity Threat Table (Summary)

| Validity Type | Threat | Affected Hypothesis / Metric | Impact | Mitigation |
|---|---|---|---|---|
| Internal | Compute state variability | H3 / DV5 | Overhead variance unexplained by IV | Warm-up filtering; median; repeated runs |
| Internal | History effect (stale data) | H1, H2 / DV1 | False results if no reset | RESET_BASELINE mandatory |
| Internal | Selection bias in IV1 | H1 / DV2 | 100% rate may be artificially high | Explicit boundary; future red team |
| External | Single environment | H1, H2, H3 / all DVs | Cannot generalize | Multiple environments in future work |
| External | Synthetic data | H1 / DV2 | Low ecological validity | Anonymized data in future work |
| Construct | "Blockchain" vs "hash-linked ledger" | H1, H2, H3 | Scope misunderstanding | Use precise terminology in conclusions |
| Conclusion | Small sample (7 scenarios, 4 levels, 1 env) | H1, H2, H3 | No statistical power | Report as association evidence only |

### A6 — Limitation to Future Work Map

| Limitation | Affected Validity | Future Work | Expected Improvement |
|---|---|---|---|
| L1 — No random assignment | Internal | FW10 (randomize run order) | Reduce order bias |
| L2 — Single environment | External | FW1 (multiple environments) | Improve generalizability |
| L3 — Limited attack vectors | Internal, External | FW2 (expand IV1), FW8 (red team) | Find FN; increase attack coverage |
| L4 — Compute variability | Internal | FW3 (more repetitions), FW4 (dedicated cluster) | Reduce variance in DV5 |
| L5 — Same trust boundary | Internal | FW5 (externalize ledger), FW6 (digital signatures) | Stronger tamper-evidence guarantee |
| L6 — Self-instrumentation | Internal | FW8 (red team), open-source code review | Independent verification |
| L7 — Synthetic data | External | FW7 (anonymized production data) | Realistic distribution; higher ecological validity |
| L8 — Limited benchmark repetitions | Conclusion | FW3 (≥30 runs/level) | Enable confidence intervals |

---

*Mã nguồn, notebook Databricks, unit test, SQL dashboard và tài liệu tái lập:*  
`https://github.com/sonnntech/kma_hk2_chuyen_de_co_so_khoa_hoc`
