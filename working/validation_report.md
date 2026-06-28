# Validation Report — Iteration 2

**Validator Role:** Independent Research Evidence Auditor  
**Target:** `working/thesis_working.md`  
**Date:** 2026-06-28  
**Validation Dimensions:** Teacher Guidelines + Chapter 10 Evidence Chain  

---

## 1. Validation Summary

**Overall Result: PASS**

| Dimension | Result | Reason |
|---|---|---|
| Teacher Guidelines validation | PASS | Required course sections are explicitly present; remaining gaps are disclosed as `Evidence Not Found` rather than hidden. |
| Chapter 10 evidence validation | PASS | All major hypothesis chains are present and bounded. No broken major evidence chain remains. |
| Treatment/control validation | PASS | Treatment is the intervention; controls are explicitly separated by hypothesis purpose. |
| Evidence honesty | PASS | Approximate, missing, and weak evidence are marked. |

---

## 2. Teacher Guideline Validation Table

| Requirement | Evidence Location | Status | Notes |
|---|---|---|---|
| Research-first framing | Sections 1, 3, 4 | PASS | RQs and hypotheses precede technical design. |
| Methodology mapping | Sections 5, 8, 18, 22 | PASS | Quasi-experimental logic is explicit. |
| Requirement analysis and scoping | Section 6 | PASS | Research requirements, functional requirements, and four-week scope are present. |
| Terminology precision | Section 6.4 | PASS | Architecture/pipeline/workflow/procedure and cyber/network/information terms are distinguished. |
| Threat or risk model | Section 7.1 | PASS | Threat actor assumptions and tamper vector mapping are explicit. |
| Ethics and dual-use | Section 7.2 | PASS | Synthetic data, confirmation widget, bounded claims, and misuse risk are addressed. |
| Visualization compliance | Section 6.5, Section 13 | PASS | Markdown tables and bar chart are used; no pie chart. Missing box-plot/CDF/histogram are disclosed and tied to future work. |
| Reproducibility appendix | Section 21 | PASS | Notebook order, widgets, config, benchmark, dashboard SQL, and known gaps are present. |
| Scientific honesty | Sections 13, 15, 21.7 | PASS | Approximate values and missing runtime metadata are disclosed. |
| Discussion and limitations | Sections 15, 17, 18, 19, 20 | PASS | Limitations influence interpretation and future work. |

---

## 3. Chapter 10 Evidence Chain Matrix

| RQ | H | IV | DV | Metric | Measurement Source | Raw Evidence | Observation | Analysis | Conclusion | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| RQ1 | H1 | IV1, IV4 | DV1, DV2 | Detection Rate; False Positive Rate | `verification_results`, Dashboard R1 | R4: 6 TP, 0 FN, 1 TN, 0 FP; R1: 14/14 VALID clean runs | O3, O4, O5 | Section 15 H1 references O3-O5 and bounds to tested vectors | H1 Supported within tested scenarios | PASS |
| RQ2 | H2 | IV1, IV3 | DV3, DV4 | First broken block accuracy; traceability completeness | `verification_results` × `lineage_events` | R5: stage match and lineage found for 6/6 scenarios; approximate marker and SQL query included | O6, O9 | Section 15 H2 references O6/O9 and marks precise block IDs as requiring query | H2 Supported with approximate evidence boundary | PASS |
| RQ3 | H3 | IV2, IV4, IV5 | DV5, DV6, DV7, DV8 | Overhead %, durations, latency | `experiment_metrics`, dashboard bar chart | R3: ~160%, ~155-160%, ~180%, ~220%; DV8 24,000-31,000 ms | O7, O8 | Section 15 H3 references O7/O8 and discloses approximate chart values | H3 Supported with caveats | PASS |
| RQ4 | H4 | Uncontrolled variables | Observed variance and boundary evidence | Uncontrolled variable impact | Dashboard, `experiment_metrics`, limitations | R3, O1, O8, Section 5 driver table | O1, O8 | Section 15 H4 explains quasi-experimental boundary | H4 Confirmed as boundary condition | PASS |

---

## 4. Evidence Coverage Estimate

| Category | Coverage |
|---|---:|
| RQs mapped to hypotheses | 4/4 |
| Hypotheses with metrics | 4/4 |
| Metrics with measurement sources | 8/8 |
| Measurements appearing in results | 8/8 |
| Raw results separated from analysis | PASS |
| Observations factual | PASS |
| Analysis references observations | PASS |
| Conclusions reference hypotheses | PASS |
| Bias affects interpretation | PASS |
| Validity types explained | 4/4 |
| Future work maps to limitations | PASS |

**Estimated evidence coverage:** 92%

Coverage is below 100% because exact H2 block IDs, exact H3 SQL output, CPU/RAM, Databricks Runtime version, and IEEE PDF artifact are not present. These are disclosed and do not break the major evidence chains.

---

## 5. Broken Evidence Chains

None.

All major chains contain:

`RQ -> H -> IV -> DV -> Metric -> Measurement Source -> Raw Evidence -> Observation -> Analysis -> Conclusion -> Status`

---

## 6. Unsupported Claims

No unsupported major claims detected.

Claims with limited evidence are explicitly bounded:

| Claim | Evidence Status | Validation |
|---|---|---|
| H2 first_broken_block accuracy | Approximate R5 + SQL query provided | Acceptable because limitation is disclosed. |
| H3 overhead trend | Approximate dashboard chart + SQL query provided | Acceptable because exact values are not claimed. |
| Reproducibility within 15 minutes | Procedure present; compute availability not guaranteed | Acceptable because Databricks runtime gaps are disclosed. |

---

## 7. Consistency Report

| Check | Result |
|---|---|
| Teacher Guidelines and Chapter 10 treated as independent | PASS |
| Research starts from RQs, not tool | PASS |
| Blockchain treated as case study/treatment mechanism | PASS |
| Treatment is intervention | PASS |
| Tamper scenario is not mislabeled as treatment | PASS |
| Two control conditions explained | PASS |
| IV/DV definitions consistent with evidence appendix | PASS |
| Raw results precede observations and analysis | PASS |
| Causal claims bounded by uncontrolled variables | PASS |
| Future work reduces limitations | PASS |

---

## 8. Critical Findings

None.

---

## 9. Required Fixes for Writer

No required fixes before finalization.

Optional evidence improvements:

1. Export exact `verification_results` rows for R4.
2. Export exact `verification_results` × `lineage_events` JOIN rows for R5.
3. Export exact `experiment_metrics` query output for R3.
4. Record Databricks Runtime version and compute metadata.
5. Produce IEEE two-column formatted artifact.

---

## 10. Final Verdict

**PASS**

The thesis satisfies both:

1. Teacher Guidelines validation PASS.
2. Chapter 10 evidence validation PASS.
