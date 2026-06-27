# Patterns & Techniques — Research Methods for Cyber Security

## Pattern: Hierarchy of Evidence (Greenhalgh, adapted for cyber)
**When to use**: Evaluating how much weight to give a study's conclusion; deciding whether to replicate.
**How**: Locate your study type on the ranked list:
1. Systematic reviews / meta-analyses of RCTs
2. RCTs with definitive results
3. RCTs with non-definitive results
4. Cohort studies
5. Case-control studies
6. Cross-sectional surveys
7. Case reports
**Trade-offs**: Lower-ranked methods are valid when higher-ranked methods are infeasible (ethical, cost, scale). Never skip stating where your study falls.

---

## Pattern: Research Method Decision Tree
**When to use**: At the start of every research project, after formulating the research question.
**How**:
1. Write your research question
2. Atomize it into the smallest meaningful sub-questions
3. Route each sub-question:
   - Open-ended / no hypothesis / uncontrollable system → **Observational** (Ch 4–6)
   - System too complex / data unavailable / experiments infeasible → **Theoretical** (Ch 7–8)
   - Specific falsifiable hypothesis / variables controllable → **Experimental** (Ch 9–10)
   - Testing performance of an existing solution → **Applied** (Ch 11–12)
**Trade-offs**: Misrouting wastes months — spend 30 min checking all four branches before committing.

---

## Pattern: 4-Criterion Hypothesis Screen
**When to use**: Before designing any experiment (Ch 9).
**How**: Check ALL four criteria:
1. **Observable**: Can you measure the hypothesized behavior?
2. **Testable**: Can you create an experiment to test it (ethical, legal, economical)?
3. **Clearly Defined**: Are all terms, variables, and metrics unambiguous with numeric thresholds?
4. **Single Concept**: Does it test exactly ONE causal relationship?
If any criterion fails → reformulate before proceeding.
**Trade-offs**: Multi-variable hypotheses produce confounded results; unclear metrics make the experiment irreproducible.

---

## Pattern: Theory Development Process (7-step)
**When to use**: When developing a formal theoretical model (Ch 7).
**How**:
1. Identify insight (from observation, prior experiment, or inspiration)
2. Determine relevant factors (key inputs, assumptions, variables)
3. Formally define the theory (pseudocode, mathematics, laws, or model)
4. Test for internal consistency (no contradictions)
5. Test for external consistency (aligns with known observations)
6. Refute (conduct experiments or observational studies to validate/challenge)
7. Seek refinements (iterate based on results)
**Trade-offs**: Steps 4 and 5 are often skipped; a theory that contradicts itself cannot generate valid hypotheses.

---

## Pattern: Machine Learning Method Selection
**When to use**: When selecting an ML algorithm for cyber security research (Ch 6).
**How**:
1. Choose learning style by label availability:
   - Labels available → Supervised
   - No labels → Unsupervised
   - Partial labels → Semi-supervised
2. Choose algorithm by problem type:
   - "What category is this?" → Classification (SVM, Random Forest, HMM)
   - "What groups exist?" → Clustering (K-means, DBSCAN)
   - "What value will this be?" → Regression
   - "Is this unusual?" → Anomaly Detection (One-class SVM)
3. Validate with 60/20/20 cross-validation split
**Trade-offs**: Skipping step 3 produces models that appear accurate but fail to generalize.

---

## Pattern: Cross-Validation Protocol
**When to use**: Any time a ML model is developed for research (Ch 6).
**How**:
1. Split dataset: 60% training / 20% cross-validation / 20% test
2. Train on training set
3. Tune hyperparameters using cross-validation set
4. Measure final generalizability on test set ONLY (never touched during tuning)
**Trade-offs**: Using the test set for tuning invalidates the generalizability estimate; the test set is blind until final evaluation.

---

## Pattern: Responsible Disclosure Protocol
**When to use**: Any time research discovers a vulnerability in a product or system (Ch 15).
**How**:
1. Day 0: Privately notify vendor CERT with technical details, PoC, affected versions
2. Days 0–180: Allow vendor up to 6 months to produce an adequate fix
3. Day 180+: If no fix with adequate progress evidence → public disclosure
4. On patch release: Coordinate joint publication with vendor + notify ICS-CERT/relevant CERT if critical infrastructure
**Trade-offs**: Immediate full disclosure exposes users before patches exist; indefinite non-disclosure enables unpatched exploitation. 6 months balances both.

---

## Pattern: 5-Axis Instrumentation Planning
**When to use**: When designing data collection for any research study (Ch 13).
**How**: For each data source, evaluate:
1. **Time fidelity**: Is precision adequate for event ordering? (NTP ≈ ms; GPS ≈ ns)
2. **Sample rate**: Is collection frequency sufficient to capture rare events?
3. **Summarization**: Does aggregation (e.g., NetFlow) remove information needed to answer the question?
4. **Proxy**: Does the indirect measure capture the right abstraction level?
5. **Scale**: Are sensors placed at all locations where the phenomenon manifests?
**Trade-offs**: Missing even one axis can make data insufficient to answer the research question after collection — no recovery possible.

---

## Pattern: Operational Bounds Testing (3-variant)
**When to use**: Before deploying any new security solution (Ch 12).
**How**:
1. **Stress test**: Increment the load parameter (connections, requests, data volume) until system fails or hits physical limits; document the breaking point
2. **Load test**: Run the system at maximum expected operational load for a sustained period; monitor resource utilization, detection rates, error rates
3. **Performance test**: Run system against defined performance requirements under normal conditions; confirm spec compliance
**Trade-offs**: Skipping stress testing discovers limits in production under real attacks; skipping load testing risks production failures at peak load.

---

## Pattern: Threat Model Specification (3-dimension)
**When to use**: Before designing any experiment or study involving adversarial behavior (Ch 14).
**How**: Specify all three dimensions:
1. **Capability** — tier (I–VI DoD model), resources, time available, tool sophistication
2. **Intent** — category (criminal, hacktivist, insider, nation-state, opportunistic) and specific objectives
3. **TTP** — Tactics (how resources are applied), Techniques (specific methods), Procedures (exact steps in the attack)
**Trade-offs**: Under-specifying capability creates unrealistic threat model; using TTP alone for attribution is insufficient (can be faked).

---

## Pattern: Quasi-experimental Design Checklist
**When to use**: When deciding whether a quasi-experiment is justified and how to design it (Ch 10).
**How**:
1. Identify which specific variables cannot be controlled and WHY (scale, ethics, cost, population size)
2. For each uncontrollable variable, document it explicitly
3. Control everything else as rigorously as a true experiment
4. Consider Difference-of-Differences if pre/post measurements are available for both groups
5. Report all uncontrolled variables and their likely impact on internal validity in the Methods section
**Trade-offs**: Quasi-experimental is not an "easy out" — it requires MORE documentation than a true experiment, not less.

---

## Pattern: Applied Research Feedback Loop
**When to use**: When interpreting failed or suboptimal applied research results (Ch 11).
**How**:
1. When applied experiment/study result is suboptimal, ask: "Which variable drove the failure?"
2. If the failure is unexpected → route back to **basic science** to explain the underlying phenomenon
3. If the failure is expected given theory → use it to refine the applied solution design
4. Document the feedback loop explicitly so readers can see the research progression
**Trade-offs**: Ignoring failed applied results and moving on prevents the field from building causal knowledge that would improve future solutions.

---

## Pattern: Case Study Evidence Ladder
**When to use**: When deciding how to present or use descriptive research findings (Ch 5).
**How**: Recognize your position on the evidence ladder and communicate it explicitly:
- **Case report** → descriptive only; no experimental validation; use for white papers
- **Case study** → formal structured process; qualitative; contributes to systemic knowledge; low on Hierarchy of Evidence but foundational when well-documented
- **Exploratory study (cross-sectional/ecological)** → broader evidence across multiple cases; still observational
- **Experimental validation** → the target for moving from case study to scientific finding
**Trade-offs**: Presenting a case study as experimental evidence overstates its epistemic status; presenting an experimental result without prior case study misses the motivating context.
