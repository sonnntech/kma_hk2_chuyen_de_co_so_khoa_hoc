# Skill: Chapter 10 Evidence Validator
Version: 3.0

## Purpose
Validate whether a thesis satisfies two independent dimensions:

1. **Teacher Guidelines compliance**: course structure, required deliverables, reproducibility, ethics, visualization, scoping, and discussion.
2. **Chapter 10 methodology compliance**: Quasi-experimental Research design and traceable evidence.

The validator does not rewrite, improve, infer, or invent missing content. It only checks what is explicitly present.

---

## Repository Context

Teacher Guidelines:
`skills/research/research-methods-cyber-security/guidance/teacher-guidelines.md`

Chapter 10:
`skills/research/research-methods-cyber-security/chapters/ch10-quasi-experimental-research.md`

Primary target:
`working/thesis_working.md`

Fallback target:
`final/thesis_final.md`

Output:
`working/validation_report.md`

---

## Knowledge Model

Teacher Guidelines and Chapter 10 are complementary.

- Teacher Guidelines define what the course requires.
- Chapter 10 defines how the methodology must be demonstrated.

Both must pass independently.

---

## Validation Principle

Every major claim must follow this chain:

```text
Claim -> Evidence -> Reasoning -> Conclusion
```

If any link is missing, report the gap. Do not guess.

---

## Dimension A: Teacher Guidelines Validation

Check whether the thesis explicitly includes:

| Requirement | Evidence Location | Status | Notes |
|---|---|---|---|
| Research-first framing |  | PASS/PARTIAL/FAIL |  |
| Methodology mapping |  | PASS/PARTIAL/FAIL |  |
| Requirement analysis and scoping |  | PASS/PARTIAL/FAIL |  |
| Terminology precision |  | PASS/PARTIAL/FAIL |  |
| Threat or risk model |  | PASS/PARTIAL/FAIL |  |
| Ethics and dual-use |  | PASS/PARTIAL/FAIL |  |
| Visualization compliance |  | PASS/PARTIAL/FAIL |  |
| Reproducibility appendix |  | PASS/PARTIAL/FAIL |  |
| Scientific honesty |  | PASS/PARTIAL/FAIL |  |
| Discussion and limitations |  | PASS/PARTIAL/FAIL |  |

---

## Dimension B: Chapter 10 Evidence Validation

For every hypothesis, validate this chain:

```text
RQ -> Hypothesis -> IV -> DV -> Metric -> Measurement Source -> Raw Evidence -> Observation -> Analysis -> Conclusion -> Status
```

Use this matrix:

| RQ | H | IV | DV | Metric | Measurement Source | Raw Evidence | Observation | Analysis | Conclusion | Status |
|---|---|---|---|---|---|---|---|---|---|---|

---

## Validation Rules

1. Every RQ must map to at least one hypothesis.
2. Every hypothesis must have an observable metric.
3. Every metric must have a measurement source.
4. Every measurement must appear in the document.
5. Observations must contain facts only.
6. Analysis must reference observations or raw results.
7. Conclusions must reference hypotheses and evidence.
8. Treatment must be the intervention.
9. Control must be the baseline.
10. IVs must be manipulated or controlled.
11. DVs must be measured or observed.
12. Bias must affect interpretation.
13. Internal, external, construct, and conclusion validity must be explained.
14. Limitations must connect to design choices or constraints.
15. Future work must reduce stated limitations.

---

## Evidence Priority

Prefer evidence in this order:

1. Raw measurements
2. Experiment tables
3. SQL output
4. Logs
5. Figures
6. Dashboards
7. Observation section
8. Discussion
9. Conclusion

Never use a conclusion as its own evidence.

---

## PASS Criteria

Overall PASS only if:

- Teacher Guidelines have no Critical missing requirement.
- Chapter 10 has no broken major evidence chain.
- Treatment and control are correct.
- Metrics have measurement sources.
- Conclusions are supported by evidence.

Return PARTIAL when the document is mostly correct but has evidence gaps or missing course sections.

Return FAIL when core course requirements or methodology chains are missing.

---

## Required Output

1. Validation Summary: PASS / PARTIAL / FAIL
2. Teacher Guideline Validation Table
3. Chapter 10 Evidence Chain Matrix
4. Evidence Coverage Estimate
5. Broken Evidence Chains
6. Unsupported Claims
7. Consistency Report
8. Critical Findings
9. Required Fixes for Writer
10. Final Verdict

---

## Final Principle

Only validate what is explicitly present. If evidence cannot be located, report `Evidence Not Found`.
