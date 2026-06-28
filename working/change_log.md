# Change Log — AI Research Framework Workflow

## Iteration 2 → Iteration 3

**Date:** 2026-06-28  
**Trigger:** User requested full AI Research Framework workflow with Teacher Guidelines + Chapter 10 as independent PASS criteria.

### Changes made to working/thesis_working.md

| # | Section | Change | Reason |
|---|---|---|---|
| 1 | Header | Updated date and added Teacher Guidelines reference | Make governing requirements explicit. |
| 2 | Section 6 — Requirement Analysis and Scope | Added research requirements, functional requirements, four-week scope, terminology precision, visualization compliance, and validated framework use | Teacher Guidelines require RQ-first framing, requirements/scoping, terminology precision, visual reporting, and use of validated tools/frameworks. |
| 3 | Section 7 — Threat Model and Ethical Responsibilities | Added explicit threat model and dual-use/ethics table | Teacher Guidelines require threat modeling and ethical responsibility. |
| 4 | Section 13 — Raw Results | Updated stale Section 9 reference to Section 11 | Maintain internal consistency after inserted sections. |
| 5 | Section 15 — Analysis | Updated stale section references | Maintain consistency and avoid ambiguous evidence links. |
| 6 | Section 20 — Future Work | Added FW11 for benchmark distributions | Tie visualization gap to future experimental improvement. |
| 7 | Section 21 — Reproducibility Appendix | Added repository, environment config, clean run, tamper run, benchmark, dashboard SQL, and known reproducibility gaps | Teacher Guidelines require reproducibility appendix and transparency about environment/data/code. |

### Reviewer result

| Dimension | Result | Notes |
|---|---|---|
| Teacher Guidelines | PASS | No Critical or Major issues. Minor gaps: no IEEE artifact, missing CPU/RAM/runtime metadata. |
| Chapter 10 | PASS | No Critical or Major issues. Minor caveats: H2/H3 precise evidence exports remain future work. |

### Validator result

| Dimension | Result | Notes |
|---|---|---|
| Teacher Guidelines validation | PASS | All required course sections present; gaps explicitly marked. |
| Chapter 10 evidence validation | PASS | No broken major evidence chains. Evidence coverage estimate: 92%. |

### Remaining issues

| Severity | Issue |
|---|---|
| Minor | IEEE two-column PDF/LaTeX artifact not present. |
| Minor | CPU/RAM and Databricks Runtime version not captured. |
| Minor | Exact H2 first_broken_block export not included. |
| Minor | Exact H3 `experiment_metrics` SQL output not included. |
| Minor | Box-plot/CDF/histogram require more benchmark repetitions. |

## Iteration 1 → Iteration 2

**Date:** 2026-06-27  
**Trigger:** Reviewer MAJOR-1 + MAJOR-2; Validator PARTIAL (O9 inference, Bảng R5/R3 approximate unmarked, dual-control ambiguity)

### Changes made to working/thesis_working.md

| # | Section | Change | Reason |
|---|---|---|---|
| 1 | Section 4 — H4 | Added "Boundary Condition Hypothesis" label; clarified H4 is confirmed, not falsified | Reviewer MINOR-1 |
| 2 | Section 7 — Treatment and Control | Added explicit dual-control clarification paragraph separating "detection control" (NONE condition) from "overhead control" (baseline_duration) | Reviewer MAJOR-2; Validator dual-control ambiguity |
| 3 | Section 11 — Bảng R3 | Added "Measurement Approximate" footer with explicit marker | Reviewer MINOR-3; Validator Bảng R3 |
| 4 | Section 11 — Bảng R4 | Changed column header to "DV1 quan sát (Measurement Collected)"; expanded note to clarify dashboard vs. verification_results evidence sources | Reviewer MAJOR-1; Validator H1 chain |
| 5 | Section 11 — Bảng R5 | Added "Measurement Approximate" marker; added SQL query for precise first_broken_block data | Validator Bảng R5; Reviewer MINOR overall |
| 6 | Section 12 — O9 | Rewrote O9 to remove causal inference; replaced with pure observation from Bảng R5 | Validator Rule 5 (observations = facts only) |
