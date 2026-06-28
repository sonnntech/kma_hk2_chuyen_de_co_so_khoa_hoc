# Review Report — Iteration 2

**Reviewer Role:** Research Methodology and Course Compliance Reviewer  
**Target:** `working/thesis_working.md`  
**Date:** 2026-06-28  
**Review Dimensions:** Teacher Guidelines + Chapter 10 Quasi-experimental Research  

---

## 1. Executive Summary

The thesis now satisfies both independent requirements at review level:

1. **Teacher Guidelines Compliance:** PASS with minor residual formatting/reproducibility risks.
2. **Chapter 10 Methodology Compliance:** PASS with minor evidence precision caveats.

The document now starts from research questions, maps the methodology explicitly, includes requirement analysis and scoping, defines terminology, provides a threat model, discusses ethics and dual-use risk, separates raw results from observations and analysis, documents bias/validity/limitations, and includes a reproducibility appendix.

No Critical or Major issues remain.

---

## 2. Teacher Guidelines Review

| Requirement | Status | Evidence / Location | Issue |
|---|---|---|---|
| Research-first framing | PASS | Sections 1, 3, 4 | RQs precede technical design. |
| Methodology mapping | PASS | Sections 5, 8, 18, 22 | Chapter 10 is explicitly mapped to design, variables, evidence, and validity. |
| Requirement analysis and scoping | PASS | Section 6 | Requirements and four-week scope are explicit. |
| Terminology precision | PASS | Section 6.4 | Architecture, pipeline, workflow, procedure, cyber/security/safety terms are distinguished. |
| Risk / threat model | PASS | Section 7.1 | Threat actor assumptions, goals, resources, trust boundary, and IV1 mapping are explicit. |
| Ethics and dual-use | PASS | Section 7.2 | Synthetic data, tamper confirmation, bounded claims, and misuse risk are addressed. |
| Visualization requirements | PASS | Section 6.5, Section 13, SQL dashboard references | No pie chart. Uses Markdown tables and dashboard bar chart. Box-plot/CDF/histogram marked as not yet supported due insufficient repetitions. |
| Reproducibility appendix | PASS | Section 21 | Notebook order, widgets, config, benchmark and SQL evidence steps are present. |
| Scientific honesty | PASS | Sections 13, 15, 18, 21.7 | Approximate and missing evidence are marked explicitly. |
| Discussion of limitations | PASS | Sections 15, 17, 18, 19, 20 | Discussion ties weak results and limitations to interpretation and future work. |

**Teacher Guidelines Score:** 94/100

Minor residual risks:
- IEEE two-column PDF/LaTeX artifact is not present; thesis marks this as `Evidence Not Found`.
- CPU/RAM and Databricks Runtime version are not present; thesis marks these as reproducibility gaps.

These are not Major because the thesis is a Markdown research artifact and does not hide the gaps.

---

## 3. Chapter 10 Methodology Review

| Requirement | Status | Evidence / Location | Issue |
|---|---|---|---|
| Research problem | PASS | Section 1 | Clear cyber security research problem. |
| Research gap | PASS | Section 2 | Existing controls and gaps are stated. |
| Research questions | PASS | Section 3 | Four measurable RQs. |
| Hypotheses | PASS | Section 4 | H1-H3 falsifiable; H4 correctly labeled boundary condition. |
| Why quasi-experimental | PASS | Section 5 | True experiment infeasibility explained with Chapter 10 drivers. |
| Experimental design | PASS | Section 8 | Pre-test/post-test non-equivalent control and overhead comparison are clearly bounded. |
| Treatment | PASS | Section 9 | Treatment is the intervention, not the whole system or attack scenario. |
| Control | PASS | Section 9 | Two control conditions are explicitly separated by hypothesis purpose. |
| Independent variables | PASS | Section 10 | IV1-IV5 defined. |
| Dependent variables | PASS | Section 10 | DV1-DV8 defined. |
| Metrics and measurements | PASS | Section 11 | Metrics, formulas, and sources are explicit. |
| Experimental procedure | PASS | Section 12 | Reproducible notebook sequence and reset protocol. |
| Raw results | PASS | Section 13 | Raw results precede interpretation. |
| Observations | PASS | Section 14 | Observations are factual. |
| Analysis | PASS | Section 15 | Analysis references observations. |
| Bias | PASS | Section 17 | Bias affects interpretation and names affected hypotheses. |
| Validity | PASS | Section 18 | Internal, external, construct, and conclusion validity are explained. |
| Limitations | PASS | Section 19 | Methodological limitations are explicit. |
| Future work | PASS | Section 20 | Future work maps to limitations/validity. |

**Chapter 10 Score:** 96/100

Minor residual risks:
- H2 first_broken_block evidence is approximate and requires query export for exact block IDs.
- H3 overhead values are approximate from dashboard chart, not raw exported `experiment_metrics`.

These are explicitly marked and bounded, so they do not block acceptance.

---

## 4. Scores

| Dimension | Score | Result |
|---|---:|---|
| Teacher Guidelines | 94/100 | PASS |
| Chapter 10 Methodology | 96/100 | PASS |
| Overall Review | 95/100 | PASS |

---

## 5. Critical Issues

None.

---

## 6. Major Issues

None.

---

## 7. Minor Issues

1. IEEE two-column formatted artifact is not included in the repository.
2. CPU/RAM and Databricks Runtime version are not captured.
3. H2 exact first_broken_block rows should be exported in a future evidence table.
4. H3 overhead should be replaced with direct SQL output from `experiment_metrics`.
5. Box-plot/CDF/histogram require more repetitions before they become meaningful.

---

## 8. Strengths

- Research methodology is now the main artifact; Blockchain is kept as case study/treatment mechanism.
- Treatment and control are correct and explicitly separated.
- Raw results, observations, analysis, and conclusions are separated.
- Bias and validity sections affect interpretation rather than serving as cosmetic lists.
- Teacher Guidelines additions are integrated without replacing Chapter 10 requirements.
- Missing or weak evidence is disclosed instead of hidden.

---

## 9. Priority Fix Plan for Writer

No required fixes before finalization.

Optional future improvements:

1. Export exact `verification_results` rows for all tamper scenarios.
2. Export exact `experiment_metrics` rows and replace approximate overhead values.
3. Record CPU/RAM/runtime metadata from Databricks.
4. Produce IEEE two-column PDF/LaTeX.
5. Run ≥30 benchmark repetitions per record count and add box-plot/CDF.

---

## 10. Final Recommendation

**Excellent**

The thesis is ready to finalize under the AI Research Framework workflow.
