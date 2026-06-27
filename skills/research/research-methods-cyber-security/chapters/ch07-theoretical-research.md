# Chapter 7: Theoretical Research

## Core Idea
Theoretical research formalizes cognitive models of how cyber systems behave — when observational or experimental methods cannot be applied. Good theory is testable, falsifiable, and feeds the empirical research cycle rather than replacing it.

## Frameworks Introduced

- **Theory Development Process** (7-step optional guide):
  1. Identify insight (from observation, prior experiments, or inspiration)
  2. Determine relevant factors (key inputs, assumptions, variables)
  3. Formally define theory (pseudocode, mathematics, model, or laws)
  4. Test for internal consistency (does the theory contradict itself?)
  5. Test for external consistency (does it align with known observations?)
  6. Refute (conduct experiments or observational studies to validate or challenge)
  7. Seek refinements (iterate based on outcomes)
  - When to use: When empirical data is unavailable, experiments are infeasible, or you need to formalize a cognitive model to generate testable hypotheses.
  - How: Don't wait for "eureka" — start with an observation or a frustrating experiment result and reason abductively to the best-fit explanation.

- **Theory → Law Lifecycle**: Observation → cognitive model → formal model (mathematical) → theory (with empirical support) → law (widely accepted). Understand which stage your work is at before claiming it.
  - When to use: When positioning a theoretical contribution relative to existing work.
  - How: Be explicit about the stage of your model — a formal model without empirical validation is not yet a theory; a widely validated theory with strong consensus is approaching law status.

- **Characteristics of Good Theory** (5-property checklist):
  1. **Coherent** — internally consistent, no contradictions
  2. **Parsimonious** — simplest explanation that covers the phenomena
  3. **Systematic** — covers the full range of relevant phenomena
  4. **Predictive** — generates testable hypotheses about future behavior
  5. **Falsifiable** — can be disproven through observations, experiments, or logical reasoning
  - When to use: To evaluate whether a proposed theoretical model is scientifically sound before publishing or using it to design experiments.

## Key Concepts
- **Theory** — interrelated concepts, definitions, and propositions explaining, predicting, and modeling relationships; NOT a guess; generalized and broadly applicable
- **Theorem** — statement proven true in deductive/mathematical contexts
- **Axiom** — statement taken as true; analogous to explicit assumptions in empirical research
- **Lemma** — intermediate step/component in a larger theoretical proof
- **Law** — theory with significant empirical support; widely accepted as accurate
- **Formal Model** — mathematical representation of system behavior; the target output of theoretical research
- **Cognitive Model** — pre-formal mental representation; starting point before mathematical formalization
- **Internal Consistency** — the theory does not contradict itself
- **External Consistency** — the theory aligns with known empirical observations
- **Abductive Reasoning** — "best fit" explanation from available knowledge; the driving logic of theory formation
- **Parsimony** — preference for the simplest explanation that accounts for the phenomena (Occam's Razor)

## Mental Models
- Theory is NOT separate from empirical research — it feeds and is refined by it. The cycle: observation → theory → hypothesis → experiment → refined theory is infinite.
- Choose theoretical research when: (1) data is unavailable, (2) experiments are infeasible or unethical, OR (3) the system is so complex that formalization must precede empirical work.
- Ask "can I test this?" before committing to theoretical research — if yes, run the experiment instead. Theoretical research is for when you genuinely cannot.
- Cryptography is the gold standard of theoretical cyber security research: mathematical foundations that have been proven, tested, and refined over decades.
- "Ivory tower" is a failure mode, not an inherent property — theory becomes ivory tower when it stops being testable or when theorists stop engaging with empirical results.

## Anti-patterns
- **Treating "theory" as synonymous with "guess"**: In science, a theory is a formally supported model — calling an untested idea a theory overstates its epistemic status.
- **Skipping internal consistency checks**: A theory that contradicts itself cannot generate valid hypotheses — check before publishing.
- **Developing theory in isolation from empirical research**: Theory that cannot be tested or that ignores existing observational data will be dismissed or ignored.
- **Over-relying on mathematical formalism without cyber-specific validation**: Information theory and cryptography benefit from pure mathematical derivation; most other cyber security topics do not reduce cleanly to existing mathematical spaces.
- **Building a non-falsifiable theory**: If there is no possible observation or experiment that could disprove it, it is not science — it is philosophy.

## Reference Tables

| Theoretical Work Stage | What it Is | What it Is NOT |
|---|---|---|
| Cognitive model | Mental/linguistic description of system behavior | Formal theory |
| Formal model | Mathematical representation | Empirically validated theory |
| Theory | Formal model with empirical support | Law |
| Law | Widely accepted, strongly validated theory | Absolute truth (still subject to revision) |

| Characteristic | Good Theory | Bad Theory |
|---|---|---|
| Coherent | Self-consistent | Contains contradictions |
| Parsimonious | Simplest fit | Unnecessarily complex |
| Predictive | Generates testable hypotheses | Explains only past observations |
| Falsifiable | Can be disproven | Cannot be tested |
| Systematic | Covers all relevant phenomena | Explains only narrow cases |

## Worked Example
**Formal Theory of Attacker Dwell Time:**
A researcher observes (from case studies) that sophisticated attackers remain undetected for 200+ days. She wants to build a formal model of this.

1. **Insight**: Dwell time correlates with attacker sophistication and defender alert fatigue (observed)
2. **Relevant factors**: Attacker evasion capability (A), defender alert volume (V), detection threshold (T), network size (N)
3. **Formal definition**: Model dwell time D as: D ∝ A × V / (T × N⁻¹) — higher attacker capability and alert volume increase dwell; lower threshold and larger network decrease it
4. **Internal consistency**: Does the model produce contradictions? (e.g., does D increase as defenders improve? Check — no, T increases as defenders improve → D decreases ✓)
5. **External consistency**: Does this align with observed dwell times in APT case studies? (roughly, yes)
6. **Refutation path**: Conduct a quasi-experiment (Ch 10) on a test network, vary alert threshold T, measure detected dwell time
7. **Refinement**: If experiment shows N has no effect, remove it from the model

## Key Takeaways
1. Choose theoretical research when data is unavailable, experiments are infeasible, or you need to formalize a cognitive model before empirical work can begin.
2. Good theory must be coherent, parsimonious, systematic, predictive, and falsifiable — check all five before publishing.
3. Theory feeds the empirical cycle: it generates hypotheses for experiments, and experimental results refine or refute the theory.
4. Cryptography and formal methods (access control models, MLS) are the strongest examples of theoretical cyber security research — they are mathematical proofs, not guesses.
5. Always be explicit about the stage of your model: cognitive, formal, or theory — don't claim theory status before empirical validation.

## Connects To
- **Ch 3**: Decision tree routes here when the system cannot be observed or experimented on directly
- **Ch 8**: Simulation — the computational partner to formal theory; tests theory over a large variable space
- **Ch 9**: Hypothetico-deductive — theories generate hypotheses that become experimental hypotheses
- **Ch 1**: Hierarchy of Evidence — theoretical work is a precursor to empirical evidence but is not itself ranked in the observational hierarchy
