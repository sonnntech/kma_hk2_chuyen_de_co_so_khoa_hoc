# Review Report — Iteration 1
**Reviewer Role:** Chapter 10 Lecturer (Quasi-experimental Research)  
**Target:** working/thesis_working.md  
**Date:** 2026-06-27  
**Primary Question:** "Would this receive full marks for demonstrating Quasi-experimental Research?"

---

## 1. Executive Summary

Bản thảo này là cải tiến đáng kể so với cả bao_cao_cdx.md và bao_cao_cld.md. Tất cả 20 section theo Writer template đều có mặt. Sáu bảng mapping bắt buộc đã được thêm vào. Causal language được kiểm soát tốt. Treatment được định nghĩa đúng (không phải tamper scenario). Thiết kế Pre-test/Post-test Non-equivalent Control là chính xác hơn DiD claim của bao_cao_cld.md.

Tuy nhiên, còn **2 Major issues** cần giải quyết trước khi có thể đạt điểm cao nhất.

---

## 2. Scoring

| Mục | Điểm tối đa | Điểm nhận được | Ghi chú |
|---|---|---|---|
| Research Problem | 10 | 9 | Tốt. Cyber security framing rõ. Câu hỏi trung tâm chính xác. |
| Research Gap | 10 | 8 | Bảng limitation tốt; gap statement hơi chung chung ở cuối. |
| Research Questions | 10 | 9 | 4 RQs measurable. RQ4 về uncontrolled variables là điểm cộng Ch.10. |
| Hypotheses | 10 | 8 | H1-H3 falsifiable tốt. H4 không falsifiable — cần clarify là boundary condition. |
| Why Quasi | 15 | 13 | 5 drivers đầy đủ. Thiếu explicit statement: "Các biến có thể kiểm soát được đã kiểm soát." |
| Experimental Design | 15 | 11 | Correct design type; nhưng hai "control" khác nhau (NONE và baseline_duration) cần giải thích rõ hơn. |
| Variables | 10 | 9 | 5 IVs + 8 DVs + Variable Table đầy đủ. Nhỏ: IV3 role ít được dùng trong analysis. |
| Measurements | 10 | 7 | **Major**: H1 TP evidence không có timestamps/query output; H3 là approximate từ chart. |
| Bias & Validity | 15 | 12 | 5 biases với affected hypothesis: tốt. All 4 validity types: tốt. Nhỏ: B4 mitigation quá generic. |
| Limitations | 10 | 9 | 8 limitations methodological. Tốt. Nhỏ: L8 (limited benchmark repetitions) cần con số cụ thể. |
| Future Work | 5 | 4 | 10 items, tất cả linked to limitations. Tốt. Nhỏ: FW3 thiếu rõ "số lần lặp tối thiểu cần thiết." |
| **TOTAL** | **100** | **99** | |

---

## 3. Critical Issues

*(Không có)*

---

## 4. Major Issues

### MAJOR-1: Evidence cho H1 (Bảng R4) — Measurement visibility

**Vấn đề:** Bảng R4 báo cáo "DV1 quan sát = DATA_TAMPERED" cho MODIFY_TRANSACTION_AMOUNT v.v., và nói rõ nguồn là `verification_results` "trong quá trình chạy thực nghiệm." Tuy nhiên, không có row data nào từ bảng này xuất hiện trong thesis — không có timestamps, không có run IDs, không có query output.

Đồng thời, Dashboard export (Bảng R1) cho thấy 14 runs VALID và 0 detection errors. Người đọc không thể tự xác minh Bảng R4 từ dashboard.

**Hệ quả:** Theo Ch.10 Writer rules: *"Every Measurement must appear inside the Results section. Reject invisible evidence."* Bảng R4 là boundary case — nguồn được nêu, nhưng actual data không visible.

**Yêu cầu sửa:** Thêm một trong hai:
- (Option A) Actual query output từ `verification_results` cho từng tamper scenario: run_id, timestamp, scenario, result, status
- (Option B) Đổi từ "DV1 quan sát" thành "DV1 thiết kế/kỳ vọng" và thêm note "Measurement Collected — verification_results table; query yêu cầu chạy lại tamper scenarios để export. Bằng chứng TN có thể xác nhận từ Dashboard R1 (14/14 VALID sau RESET_BASELINE)."

Option B là honest approach phù hợp với giới hạn thực tế.

**Severity: MAJOR** — Nếu không sửa, Validator có thể đánh Evidence Mismatch giữa Bảng R4 và Dashboard R1.

---

### MAJOR-2: Experimental Design — Hai "control" khác nhau chưa được giải thích rõ

**Vấn đề:** Thesis dùng:
- "Control" = NONE scenario (trong cùng treatment pipeline) cho H1, H2
- "Control" = pipeline không có ledger (`baseline_duration_ms`) cho H3

Đây là hai "control" khác nhau hoàn toàn. Phần 6 (Experimental Design) mô tả điều này nhưng không label rõ ràng để reader phân biệt ngay.

**Hệ quả:** Validator có thể hỏi: "Control được định nghĩa là pipeline không có ledger (Section 7) — nhưng sao control cho H1 là NONE condition trong treatment pipeline?"

**Yêu cầu sửa:** Thêm một bảng nhỏ hoặc clarification paragraph trong Section 7 hoặc Section 8:

```
Lưu ý về hai loại control trong thiết kế:
- Control Condition for H1/H2 (Detection/Traceability):
  Cùng pipeline với ledger, tamper_scenario = NONE.
  Mục đích: đo false positive rate; xác nhận baseline VALID.
- Control Condition for H3 (Overhead):
  Pipeline không có ledger (baseline_duration_ms).
  Mục đích: đo chi phí bổ sung của treatment.
Hai control này phục vụ hai research questions khác nhau và không mâu thuẫn.
```

**Severity: MAJOR** — Nếu không sửa, thiết kế quasi-experimental sẽ gây confusing cho người đọc và Validator.

---

## 5. Minor Issues

### MINOR-1: H4 là boundary condition hypothesis, không phải falsifiable hypothesis

**Vấn đề:** H4 nói "không thể falsify" trong cùng section với H1-H3 được nêu là "điều kiện falsifiable." Điều này có thể gây hiểu nhầm.

**Gợi ý sửa:** Thêm label rõ ràng: "H4 là Methodological Boundary Hypothesis — không falsifiable theo cùng cơ chế như H1-H3, nhưng được xác nhận (confirmed/denied) bằng cách kiểm tra xem uncontrolled variables có thực sự tác động đến kết quả không."

### MINOR-2: O9 trong Observations mang tính diễn giải

**Vấn đề:** "Khi tamper xảy ra tại một stage, first_broken_block...trỏ đến block tương ứng" — "Khi tamper xảy ra" đã là diễn giải nhân quả, không phải observation thuần túy.

**Gợi ý sửa:** "Trong Bảng R5, cột 'Stage khớp IV3?' ghi nhận 'Có' cho tất cả 6 tamper scenarios. Cột 'Lineage event tìm thấy?' ghi nhận 'Có' cho tất cả 6 scenarios."

### MINOR-3: Bảng R3 — Overhead approximate thiếu "Measurement Not Yet Collected" marker

**Vấn đề:** Thesis honest về việc đây là approximate values, nhưng không dùng explicit marker theo Writer skill requirements.

**Gợi ý sửa:** Thêm vào cuối Bảng R3: "*Measurement Approximate — Giá trị chính xác: chưa thu thập trong tài liệu này. SQL query trong Section 9 trả về median_overhead_percent từ experiment_metrics.*"

---

## 6. Side-by-Side Comparison: CDX vs CLD vs Working Draft

| Tiêu chí Ch.10 | bao_cao_cdx.md | bao_cao_cld.md | thesis_working.md | Winner |
|---|---|---|---|---|
| Research Problem framing | Tốt | Tốt | Tốt, explicit | Working |
| Research Gap | Có | Có | Có + table | Working |
| RQ measurability | 4 RQs, clear | 3 RQs, clear | 4 RQs + measurable column | Working |
| Hypotheses falsifiability | 4H, tốt | 3H, tốt | 4H + explicit falsification | Working |
| Why Quasi — 5 drivers | Có | Có | Có + mitigation column | Working |
| Treatment definition | Correct | Correct | Correct | Tie |
| Experimental Design type | Pre-test/Post-test | DiD (incorrect) | Pre-test/Post-test (corrected) | Working |
| Two "control" clarity | Không rõ | Không rõ | Không rõ (MAJOR-2) | None pass |
| IVs | 5 | 3 | 5 + Variable Table | Working |
| DVs | 8 | 4 | 8 + full table | Working |
| Raw Results (separate) | Không | Không | Có (Sections 11) | Working |
| Observations (separate) | Không | Không | Có (Section 12) | Working |
| Analysis (separate) | Có (partial) | Có (partial) | Có (Section 13) | Working |
| Conclusions — Supported/Rejected | Implicit | Implicit | Explicit | Working |
| Bias with affected H | Không | Có (partial) | Có (explicit) | Working |
| All 4 validity types | Có | Có (partial) | Có + Validity Threat Table | Working |
| Methodological limitations | Có | Có | Có (8 items) | Working |
| Future Work → limitations | Có | Có | Có (10 items, all linked) | Working |
| 6 required mapping tables | Không | Không | Có (Appendix) | Working |
| H1 evidence visible | Không | Không | Partial (MAJOR-1) | None pass |
| H3 overhead precise | Approximate | Approximate | Approximate (MINOR-3) | None pass |

---

## 7. Missing Chapter 10 Concepts

Không còn missing Ch.10 concepts. Tất cả 20 sections từ Writer template đều có mặt. Sáu bảng mapping đều có.

---

## 8. Priority Improvements

Theo thứ tự ưu tiên:

1. **[MAJOR-1]** Clarify H1 evidence status: đổi "DV1 quan sát" → "DV1 thiết kế + Measurement Collected" với explicit note về dashboard vs. verification_results distinction.

2. **[MAJOR-2]** Add clarifying paragraph trong Section 7 hoặc 8 về hai loại control được dùng cho hai research questions khác nhau.

3. **[MINOR-3]** Thêm "Measurement Approximate" marker rõ ràng cho Bảng R3.

4. **[MINOR-2]** Sửa O9 để chỉ là observation thuần túy (không có "Khi tamper xảy ra").

5. **[MINOR-1]** Clarify H4 là Boundary Condition Hypothesis, không phải falsifiable hypothesis.

---

## 9. Final Verdict

**Good** — Thesis này thể hiện tốt Quasi-experimental Research. Tất cả cấu trúc Ch.10 đều có mặt. Tuy nhiên, hai Major issues về evidence visibility (H1) và dual-control clarity cần được giải quyết trước khi có thể nâng lên **Excellent**.

Sau khi sửa MAJOR-1 và MAJOR-2, thesis này có khả năng đạt PASS từ Validator.

---

**Reviewer Recommendation:** → ITERATE (Writer revises MAJOR-1, MAJOR-2, và 3 Minor issues)
