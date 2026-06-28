# Framework Audit

## Executive Summary

The Writer -> Reviewer -> Validator workflow improved the thesis substantially, but the framework's final **PASS** is only **partially trustworthy**.

The framework correctly identified and fixed many Chapter 10 structural issues:

- research-first framing
- treatment/control separation
- IV/DV mapping
- raw results vs observations vs analysis
- bias and validity sections
- limitations and future work mapping

However, the final PASS is too generous because the framework allowed several missing or approximate requirements to remain while still calling both Teacher Guidelines and Chapter 10 validation "PASS".

The strongest concern is that the Validator accepted evidence chains where the evidence is not fully visible inside the thesis:

- H1 tamper rows are claimed from `verification_results`, but exact row exports are not shown.
- H2 first_broken_block evidence is approximate and binary ("Co"), not actual block/run evidence.
- H3 overhead is approximate from a dashboard bar chart, not raw `experiment_metrics` output.
- Teacher Guidelines require IEEE-style output and detailed reproducibility metadata, but the thesis marks those as `Evidence Not Found` while still receiving PASS.

This is not a total framework failure. It is a **false-strong PASS** problem: the framework is useful for structure and methodology, but weak as an evidence auditor unless PASS criteria are stricter.

## False PASS Analysis

### FP-1: Teacher Guidelines PASS despite missing required deliverables

Teacher Guidelines require:

- IEEE-style conference paper format, 6-8 pages
- reproducibility appendix with environment details such as machine/CPU/RAM
- visualization beyond prose, using accepted data visualizations

The thesis explicitly says:

- IEEE PDF/LaTeX artifact: `Evidence Not Found`
- CPU/RAM and Databricks Runtime version: `Evidence Not Found`
- Box-plot/CDF/histogram: `Evidence Not Found`

The Reviewer and Validator treated disclosure as sufficient for PASS. That is too lenient if the framework goal is "satisfies Teacher Guidelines", not merely "honestly discloses gaps".

Audit result: **False PASS risk: High for Teacher Guidelines.**

### FP-2: H1 PASS despite invisible tamper-run evidence

The thesis reports:

```text
6TP, 0FN, 1TN, 0FP
```

But the actual `verification_results` rows are not shown. The thesis provides a SQL query, but not query output with:

- pipeline_run_id
- timestamp
- tamper_scenario
- verification_status
- first_broken_block

The Validator accepted the table as raw evidence because the thesis labels it "Measurement Collected". This weakens evidence-chain validation because the table is asserted by the thesis rather than independently visible.

Audit result: **False PASS risk: Medium-High for H1 evidence.**

### FP-3: H2 PASS despite approximate traceability evidence

H2 depends on first_broken_block and lineage matching. The raw result is:

```text
Stage khop IV3? Co
Lineage event tim thay? Co
```

This does not show exact first_broken_block values, stage IDs, lineage event IDs, or run IDs. The thesis explicitly marks this as approximate.

Validator still marks H2 PASS. A stricter evidence validator should mark this **PARTIAL**, because the metric is "first broken block accuracy" but the result does not expose the measured block IDs.

Audit result: **False PASS risk: High for H2 evidence precision.**

### FP-4: H3 PASS despite approximate overhead

H3 says overhead increases consistently with record count. The result table is approximate from a dashboard bar chart:

```text
1K: ~160%
5K: ~155-160%
10K: ~180%
50K: ~220%
```

This evidence is not raw measurement output. It also is not strictly monotonic from 1K to 5K. The thesis correctly adds caveats, but the conclusion still says H3 is "Supported (with caveats)".

A stricter framework should mark H3 **PARTIALLY SUPPORTED** until direct `experiment_metrics` output is included.

Audit result: **False PASS risk: Medium for H3.**

### FP-5: H4 treated as a hypothesis despite not being falsifiable

H4 is labeled a "Boundary Condition Hypothesis" and is explicitly not falsifiable like H1-H3. This is honest, but Chapter 10's hypothesis/evidence chain should not treat H4 as equivalent to a falsifiable hypothesis.

The framework allowed H4 into the same evidence matrix as H1-H3. That is acceptable as a boundary claim, but not as a hypothesis under the same rubric.

Audit result: **False PASS risk: Low-Medium.**

## False FAIL Analysis

No significant false FAIL was found.

The framework did not appear to unfairly reject valid content. In fact, the opposite happened: the framework leaned toward accepting disclosed missing evidence and approximate evidence as PASS.

Possible over-strict areas avoided:

- It did not fail the thesis merely because the work is not a true experiment.
- It did not fail the thesis for using a hash-linked ledger instead of a full blockchain.
- It did not fail the thesis for using synthetic data, because limitations were disclosed.

Audit result: **False FAIL risk: Low.**

## Reviewer Blind Spots

### RB-1: Disclosed missing deliverables were downgraded too far

The Reviewer listed missing IEEE artifact, CPU/RAM/runtime metadata, exact H2 export, exact H3 SQL output, and box-plot/CDF/histogram as Minor issues.

For a Teacher Guidelines audit, at least two should be Major:

- IEEE-style deliverable missing
- reproducibility metadata missing

The framework needs a stricter rule:

```text
If a Teacher Guideline says "bat buoc", disclosure alone does not make it PASS.
```

### RB-2: Reviewer did not enforce "raw measurements first" strongly enough

The Reviewer accepted H1/H2/H3 as PASS even though the actual measurement exports are not included.

The Reviewer should have required:

- exact tamper verification rows for H1
- exact first_broken_block/lineage rows for H2
- exact `experiment_metrics` summary output for H3

### RB-3: Reviewer did not challenge "Excellent"

The final recommendation is "Excellent", but the thesis still has:

- missing required deliverable format
- missing runtime metadata
- approximate core result values
- no exact query output for two major hypotheses

"Good / PASS with evidence gaps" would be more defensible than "Excellent".

## Validator Blind Spots

### VB-1: Validator accepted asserted tables as raw evidence

The Validator says H1 has raw evidence because Bảng R4 contains the result table. But Bảng R4 does not show exported rows from the measurement source; it is a summarized claim.

A stronger validator should distinguish:

- **raw evidence**: query output/log/table export with IDs/timestamps
- **summary evidence**: author-created table
- **claim table**: expected/observed statuses without row provenance

H1 currently has summary evidence, not raw evidence.

### VB-2: Validator allowed approximate evidence to pass major chains

H2 and H3 both rely on approximate evidence. The Validator notes this but still returns PASS.

A stricter policy should be:

```text
If a hypothesis conclusion is "Supported",
then its core metric must have non-approximate measurement evidence.
Approximate evidence may support only "Partially Supported".
```

### VB-3: Validator treated Teacher Guidelines as section-presence checks

Teacher Guidelines validation mostly checked whether a section exists. It did not strictly validate whether mandatory deliverables are complete.

Examples:

- Reproducibility appendix exists, but CPU/RAM/runtime are missing.
- Visualization section exists, but key visualization types are absent or deferred.
- IEEE artifact is missing but marked non-blocking.

### VB-4: Validator did not verify source files or executable evidence

The Validator did not run or inspect query outputs from:

- `verification_results`
- `lineage_events`
- `experiment_metrics`
- Databricks dashboard export

This may be acceptable for a text-only validator, but then it should not claim high evidence confidence.

## Writer Blind Spots

### WB-1: Writer converted missing requirements into disclosed gaps

The Writer handled missing Teacher Guideline requirements by adding `Evidence Not Found` and future work. That is scientifically honest, but it does not satisfy requirements that are mandatory.

This pattern can produce a polished document that appears compliant while still lacking required deliverables.

### WB-2: Writer retained "Supported" for approximate hypotheses

H2 and H3 should be safer as:

- H2: Partially Supported
- H3: Partially Supported

The current "Supported (with caveats)" is bounded, but stronger than the evidence warrants.

### WB-3: Writer did not fully normalize H4

H4 is not a falsifiable hypothesis. It should be separated as:

```text
Methodological boundary claim
```

not included as a hypothesis with equivalent status.

### WB-4: Writer did not add raw export appendices

The Writer added SQL queries but not outputs. For an evidence-centered framework, the document should include appendices such as:

- verification_results export
- lineage join export
- experiment_metrics export

## Teacher Guideline Gaps

### TG-1: IEEE-style paper artifact missing

The thesis says the IEEE two-column artifact is not present. Teacher Guidelines state the report should simulate a conference paper format. The framework marked PASS anyway.

Audit status: **Missing requirement; should be Major unless user explicitly accepts Markdown as the deliverable.**

### TG-2: Reproducibility metadata incomplete

The thesis lacks:

- CPU/RAM
- Databricks Runtime version
- exact cluster/serverless configuration

Teacher Guidelines require detailed environment configuration. The current appendix is useful but incomplete.

Audit status: **Partial, not full PASS.**

### TG-3: Visualization is not fully realized

The thesis uses Markdown tables and references a dashboard bar chart, but:

- exact chart image/export is not embedded
- box-plot/CDF/histogram are absent
- benchmark repetitions are insufficient for distribution plots

Audit status: **Partial.**

### TG-4: Validated framework requirement is only partly satisfied

The thesis says Databricks, PySpark, Delta Table, and Databricks SQL are used. That supports the Teacher Guideline not to hand-roll a complex system entirely.

However, the treatment and instrumentation are self-built. That is acceptable for the case study, but the framework should require a clearer boundary:

- what is provided by validated frameworks
- what is self-built instrumentation
- how self-built measurement was independently checked

Audit status: **Mostly satisfied, but instrumentation independence remains weak.**

## Chapter 10 Gaps

### C10-1: Core evidence chains are present but not all are strong

Chapter 10 structure is present. The issue is not missing sections; it is evidence strength.

| Hypothesis | Framework status | Audit status |
|---|---|---|
| H1 | PASS | Mostly PASS, but raw row evidence missing |
| H2 | PASS | PARTIAL due approximate first_broken_block evidence |
| H3 | PASS | PARTIAL due approximate overhead evidence |
| H4 | PASS | Should be boundary claim, not hypothesis |

### C10-2: Treatment/control mostly correct

Treatment is correctly defined as the hash-linked ledger + verification + lineage evidence.

Control is more complex:

- H1/H2 use clean `NONE` condition with ledger for false positive/baseline detection.
- H3 uses no-ledger pipeline for overhead.

The thesis explains this. The framework was right not to fail it, but future projects should require a design diagram or table that maps each control to a hypothesis and metric.

### C10-3: Difference-of-Differences correctly avoided

The thesis says the H3 comparison is not full Difference-of-Differences. This is a framework success.

### C10-4: Causal language is mostly bounded

The thesis generally uses bounded language:

- suggests
- supported within tested scenarios
- approximate
- association evidence

No major unsupported causal claim was found.

One phrase remains stronger than evidence:

```text
Traceability confirmed trong all tested scenarios
```

Because H2 evidence is approximate, "confirmed" should be considered too strong.

## Confidence Level

**Medium**

Reason:

The framework is strong at enforcing document structure and Chapter 10 vocabulary. It is weaker at evidence strictness and Teacher Guidelines deliverable enforcement.

Confidence is not High because:

- final PASS depends on approximate H2/H3 evidence
- final PASS accepts missing Teacher Guideline deliverables
- raw exports are not embedded
- environment reproducibility metadata is incomplete

Confidence is not Low because:

- missing/weak evidence is explicitly disclosed
- no obvious incorrect methodology conversion occurred
- treatment/control are mostly correct
- bias, validity, limitations, and future work are substantive

## Final Assessment

Can this framework be trusted for future research projects?

**PARTIALLY**

The framework can be trusted to improve a thesis toward Chapter 10 structure and to prevent common methodology errors such as:

- starting from a tool instead of RQs
- treating Blockchain as the research objective
- omitting treatment/control
- mixing raw results with analysis
- ignoring bias and validity
- making unbounded causal claims

But it should not yet be trusted as a strict final gate for research evidence or course compliance.

To make the framework trustworthy for future projects, update the PASS rules:

1. Mandatory Teacher Guideline deliverables cannot PASS when marked `Evidence Not Found`.
2. A hypothesis cannot be marked `Supported` if its core metric is approximate or lacks raw export evidence.
3. Validator must classify evidence as raw / summarized / approximate / missing.
4. Reviewer must not label missing IEEE artifact, missing runtime metadata, or missing raw result exports as merely Minor when the assignment requires them.
5. Final verdict should distinguish:
   - Methodology Structure PASS
   - Evidence Strength PARTIAL
   - Teacher Deliverables PARTIAL

Current framework verdict:

```text
Methodology structure: YES
Evidence validation: PARTIALLY
Teacher deliverable validation: PARTIALLY
Overall trust: PARTIALLY
```
