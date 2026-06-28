# Validation Report — Iteration 1
**Validator Role:** Independent Methodology Auditor  
**Target:** working/thesis_working.md  
**Date:** 2026-06-27  
**Absolute Rule:** Claim → Evidence → Reasoning → Conclusion. Every chain must be complete. If any link is missing → FAIL.

---

## 1. Validation Summary

**Overall Result: PARTIAL**

| Hypothesis | Evidence Chain Status | Detail |
|---|---|---|
| H1 | PARTIAL PASS | Chain complete; TP evidence in Bảng R4 (verification_results named); TN confirmed by Dashboard R1. Actual query output/timestamps not shown — evidence present but not independently verifiable from thesis text alone. |
| H2 | PARTIAL | Chain present; Bảng R5 shows binary Có/Không without actual first_broken_block values or stage IDs. O9 mixes observation with inference. |
| H3 | PARTIAL PASS | Chain complete; Bảng R3 values are approximate (~160%–~220%) from dashboard bar chart. SQL query provided but not executed. |
| H4 | PASS | Chain complete; confirmed by observed variance (O8) and single-environment evidence (O1). |

---

## 2. Evidence Coverage

| Category | Count | Supported |
|---|---|---|
| Research Questions with Hypothesis mapping | 4/4 | ✓ 100% |
| Hypotheses with Observable Metrics | 4/4 | ✓ 100% |
| Metrics with Measurement Sources | 8/8 | ✓ 100% |
| Measurements appearing in Results section | 8/8 | ✓ 100% (approximate for DV3–DV5) |
| Observations containing facts only | 10/10 | O9 partial fail — see below |
| Analyses referencing actual observations | 4/4 | ✓ |
| Conclusions referencing hypotheses | 4/4 | ✓ |
| Causal language bounded | All claims | ✓ "gợi ý", "phù hợp với", "trong phạm vi" |
| Bias influencing interpretation | 5/5 | ✓ each bias names affected hypothesis |
| Future work reducing limitations | 10/10 | ✓ all linked |

**Evidence Coverage Score: 88%**  
(H2 partial: -8%; O9 inference: -4%)

---

## 3. Evidence Chain Matrix

### H1

| Link | Content | Status |
|---|---|---|
| RQ | RQ1: Treatment có phát hiện thay đổi trái phép không? | ✓ Present |
| Hypothesis | H1: Pipeline có ledger phát hiện được tất cả tamper scenarios; control không có cơ chế độc lập | ✓ Present, falsifiable |
| IV | IV1 (tamper scenario), IV4 (security mechanism) | ✓ Defined |
| DV | DV1 (verification outcome), DV2 (detection rate) | ✓ Defined |
| Metric | Detection Rate = TP/(TP+FN)×100%; FPR = FP/(FP+TN)×100% | ✓ Formula explicit |
| Measurement Source | verification_results table (tamper runs); Dashboard (NONE/TN) | ✓ Named |
| Raw Evidence | Bảng R4: 6TP, 0FN, 1TN, 0FP. Source: verification_results. Bảng R1: 14/14 VALID (TN). | ✓ In Results section |
| Observation | O3 (TN: 0 FP on dashboard), O4, O5 (TP: non-VALID per scenario) | ✓ Present |
| Analysis | Analysis H1: references O4, O5, O3, O1. Bounds scope to 6 vectors. | ✓ Appropriate |
| Conclusion | Supported within 7 scenarios; not generalizable beyond IV1 list | ✓ Bounded |
| Status | Supported | ✓ |

**Chain Assessment:** PARTIAL PASS — Chain is logically complete. One concern: Bảng R4 "DV1 quan sát" column represents observed outcomes from `verification_results` during tamper runs, but actual row data (run_id, timestamp) not shown. Thesis correctly distinguishes TN evidence (dashboard) from TP evidence (verification_results). No Evidence Mismatch detected — thesis does NOT claim dashboard supports TP. Risk: if examiner queries "prove Bảng R4 was actually observed," precise query output would be needed.

---

### H2

| Link | Content | Status |
|---|---|---|
| RQ | RQ2: Treatment có xác định first_broken_block và lineage không? | ✓ Present |
| Hypothesis | H2: Treatment xác định first_broken_block và liên kết lineage event | ✓ Present, falsifiable |
| IV | IV1, IV3 | ✓ Defined |
| DV | DV3 (first_broken_block accuracy), DV4 (traceability completeness) | ✓ Defined |
| Metric | DV3 = correct IDs / total errors × 100%; DV4 = binary completeness | ✓ Formula explicit |
| Measurement Source | verification_results × lineage_events | ✓ Named |
| Raw Evidence | Bảng R5: "Có" for all 6 scenarios (binary). No actual block IDs, stage names, or run_ids shown. | ⚠ PARTIAL |
| Observation | O9: contains inference ("Khi tamper xảy ra tại một stage...trỏ đến block tương ứng") | ⚠ Rule 5 violation |
| Analysis | References O9 and Bảng R5; appropriately cautious "gợi ý" | ✓ |
| Conclusion | Supported (approximate) — pending precise query | ✓ Appropriately bounded |
| Status | Supported approximate | ✓ |

**Chain Assessment:** PARTIAL — Evidence present but not fully detailed. Bảng R5 shows binary outcomes without actual first_broken_block values. O9 mixes observation with causal inference. These are weaknesses but NOT broken chains — the evidence link exists, it is just imprecise.

---

### H3

| Link | Content | Status |
|---|---|---|
| RQ | RQ3: Chi phí overhead theo kích thước dữ liệu? | ✓ Present |
| Hypothesis | H3: Overhead tăng theo record count, quan hệ nhất quán | ✓ Present, falsifiable |
| IV | IV2 (record count), IV4 (security mechanism) | ✓ Defined |
| DV | DV5 (overhead %), DV6, DV7 (durations) | ✓ Defined |
| Metric | Overhead = (secured−baseline)/baseline×100 | ✓ Formula explicit |
| Measurement Source | experiment_metrics (is_warmup=false); SQL query provided | ✓ Named |
| Raw Evidence | Bảng R3: ~160%, ~155-160%, ~180%, ~220% (approximate from bar chart) | ⚠ APPROXIMATE |
| Observation | O7: References Bảng R3 directly. O8: latency variance noted. | ✓ Factual |
| Analysis | References O7; appropriately notes compute state variance; "gợi ý" caution | ✓ |
| Conclusion | Supported (with caveats); approximate pending SQL execution | ✓ Bounded |
| Status | Supported (with caveats) | ✓ |

**Chain Assessment:** PARTIAL PASS — Chain logically complete. Bảng R3 is approximate but honest about it. Thesis explicitly states "approximate từ dashboard bar chart; chính xác cần query experiment_metrics" — this is correct self-disclosure per Ch.10 norms. No unsupported claims.

---

### H4

| Link | Content | Status |
|---|---|---|
| RQ | RQ4: Uncontrolled variables ảnh hưởng như thế nào? | ✓ Present |
| Hypothesis | H4: Kết quả chỉ là quasi-experimental evidence, không phải causal proof | ✓ Present (boundary condition) |
| Metric | Observed variance; uncontrolled variable list; single-environment evidence | ✓ Defined |
| Measurement Source | experiment_metrics, Dashboard, observation log | ✓ Named |
| Raw Evidence | O8 (latency outlier); O1 (single dashboard snapshot); Bảng R3 (overhead variance) | ✓ Present |
| Observation | Variance and single-environment observations factual | ✓ |
| Analysis | References O8, O1; confirms quasi-experimental boundary | ✓ |
| Conclusion | Confirmed — no causal claims made in thesis | ✓ |
| Status | Confirmed | ✓ |

**Chain Assessment:** PASS

---

## 4. Broken Evidence Chains

**None detected.**

All four hypothesis chains have all required links present. Chains for H2 and H3 are approximate/indirect but not broken.

---

## 5. Unsupported Claims

**None detected.**

All major claims are bounded with:
- "trong phạm vi 7 scenarios được kiểm thử" (H1)
- "gợi ý; bằng chứng đầy đủ cần query" (H2)
- "cần query experiment_metrics để có số liệu chính xác" (H3)

No claim asserts causality, universality, or generalization beyond tested conditions.

---

## 6. Evidence Mismatch

**One near-miss detected, correctly handled:**

| Claim | Referenced Evidence | Actual Evidence | Assessment |
|---|---|---|---|
| H1: 6 TP detected (Bảng R4) | verification_results (tamper runs) | Dashboard (Bảng R1) shows 0 detections | ✓ NOT a mismatch — thesis explicitly separates these: "Dashboard phản ánh trạng thái sau RESET_BASELINE; TP evidence từ verification_results." The thesis does not claim dashboard confirms TP. |

**Assessment:** No Evidence Mismatch. The thesis correctly distinguishes two evidence sources for two different claims (TN from dashboard; TP from verification_results). This is textbook evidence handling.

---

## 7. Consistency Report

| Check | Result |
|---|---|
| RQ → H mapping consistent | ✓ A1 table matches body text |
| IV definitions consistent | ✓ Section 8 ↔ Appendix A4 consistent |
| DV definitions consistent | ✓ Section 8 ↔ Appendix A4 consistent |
| Metric formulas consistent | ✓ Section 9 ↔ Analysis ↔ Appendix A2 consistent |
| Conclusion status consistent | ✓ Body conclusions match A2 matrix |
| Bias → affected hypothesis consistent | ✓ B1-B5 match Analysis sections |
| Limitation → future work consistent | ✓ A6 table matches body |
| O9 consistent with Bảng R5 | ⚠ O9 says "trỏ đúng block" (interpretive); Bảng R5 says "Có" (binary). Not inconsistent but O9 makes a claim beyond what Bảng R5 explicitly shows. |

---

## 8. Methodology Compliance (Chapter 10)

| Ch.10 Requirement | Status |
|---|---|
| Quasi-experimental design named and justified | ✓ Pre-test/Post-test Non-equivalent Control |
| True experiment infeasibility explained with 5 drivers | ✓ |
| Treatment = intervention (not tamper, not whole system) | ✓ |
| Control = feasible baseline | ✓ (two controls, needs clarification) |
| IVs manipulated or controlled | ✓ |
| DVs measured and observed | ✓ |
| Uncontrolled variables listed | ✓ (in Sections 5 and 17) |
| Bias with effect on interpretation | ✓ |
| All 4 validity types | ✓ |
| Causal language bounded | ✓ |
| Limitations methodological | ✓ |
| Future work reduces limitations | ✓ |
| Raw Results before interpretation | ✓ (Sections 11, 12, 13 separated) |
| Evidence Not Found / Measurement Approximate used | ⚠ Partially — H3 approximate noted in text but not with standard marker. H2 approximate not marked. |

---

## 9. Critical Findings

**No Critical findings.**

The thesis does not contain:
- Circular reasoning
- Unsupported causal claims
- Incorrect treatment/control labeling
- Evidence mismatch (the dashboard/verification_results distinction is correctly handled)
- Fabricated evidence

**Issues requiring attention before PASS:**

| Issue | Severity | Location | Action needed |
|---|---|---|---|
| O9 contains inference ("trỏ đến block tương ứng với stage bị tấn công") | Minor | Section 12, O9 | Rewrite as pure observation: "Cột 'Stage khớp IV3?' trong Bảng R5 ghi nhận 'Có' cho 6/6 scenarios" |
| Bảng R5 shows binary "Có/Không" without actual first_broken_block values | Moderate | Section 11, Bảng R5 | Add clarification: "Measurement Approximate — precise block IDs require query: SELECT first_broken_block FROM verification_results WHERE tamper_scenario != 'NONE'" |
| Bảng R3 overhead values approximate — not marked with standard notation | Minor | Section 11, Bảng R3 | Add "Measurement Approximate" footer to Bảng R3 |
| Two control conditions (NONE condition vs. baseline_duration) not explicitly labeled as distinct | Moderate | Sections 6, 7 | Add clarifying paragraph separating "detection control" from "overhead control" |

---

## 10. Validator Recommendation

**PARTIAL → requires targeted revision before PASS.**

The thesis is structurally sound and methodologically compliant. No broken chains. No unsupported claims. No evidence mismatch.

To achieve PASS, the Writer must address:
1. O9 rewrite (remove inference from observation section)
2. Bảng R5 — add "Measurement Approximate" + SQL query for precise data
3. Bảng R3 — add explicit "Measurement Approximate" marker
4. Section 7/8 — clarify dual-control definition

After these targeted revisions, the evidence chains will be PASS-eligible.

**Evidence Coverage after revision (projected): 95%**
