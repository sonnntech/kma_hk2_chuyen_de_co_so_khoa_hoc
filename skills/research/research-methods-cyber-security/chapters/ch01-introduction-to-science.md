# Chapter 1: Introduction to Science

## Core Idea
Science is a philosophy, body of knowledge, AND a rigorous process — and cyber security needs all three to evolve from a reactive craft into a predictive discipline. This chapter establishes the vocabulary and hierarchy of evidence that frames every method in the book.

## Frameworks Introduced

- **Three Faces of Science**: Science = (1) philosophy (what it means to observe from within the universe), (2) body of knowledge (accumulated understanding), (3) method (rigorous process to generate evidence). Cyber security research must engage all three, not just #2.
  - When to use: When scoping a research proposal — ask which face(s) your work targets.
  - How: Check whether your work challenges an assumption (philosophy), adds to known facts (body), or produces replicable evidence (method). Most cyber work stays in #2; promote it to #3.

- **Continuum of Discovery (Simple ↔ Operationally Relevant)**: A spectrum from fully controlled lab experiments (high repeatability, low realism) to field observations (high realism, low control). Progress requires moving along this continuum, not jumping straight to operational scale.
  - When to use: Deciding where to start a research program.
  - How: Start simple — isolate variables in a testbed — then iteratively increase realism. Skipping the simple end leads to firmly held false beliefs.

- **Hierarchy of Evidence** (Greenhalgh's ranking, adapted for cyber):
  1. Systematic reviews / meta-analyses of RCTs
  2. Randomized Controlled Trials (definitive results)
  3. RCTs (nondefinitive, but CI suggests effect)
  4. Cohort studies
  5. Case-control studies
  6. Cross-sectional surveys
  7. Case reports
  - When to use: Evaluating how strongly a study's conclusion can be trusted; deciding whether to replicate.
  - How: Locate your study type on this list. Observational studies are valid, especially when controlled experiments are infeasible — but communicate the rank honestly so readers calibrate accordingly.

## Key Concepts
- **Science** — philosophy + body of knowledge + rigorous method to generate evidence (not synonymous with "engineering")
- **Engineering vs. Science** — engineering applies scientific knowledge; science generates it. Both require rigor, but the goals differ.
- **Observational Research** — phenomenon embedded in a dynamic system; investigator cannot fully control variables; uses testbeds/microcosms as simplifications
- **Experimental Research** — investigator controls all variables; all influences known; results are highly repeatable but may lack operational realism
- **Mathematical Research** — based on logic and formal proofs; enables data analysis; precursor to empirical advances
- **Applied Research** — leverages all other forms to assess ability to solve a societal problem; core to cyber security
- **Hierarchy of Evidence** — ranked ordering of research method types by strength of evidence produced
- **Testbed / Microcosm** — a controlled simplification of a real environment used to study basic relationships without full-scale complexity
- **Operational Relevance** — the degree to which experimental results reflect real-world conditions

## Mental Models
- Think of science as a *discipline*, not a *body of facts* — any claim without a rigorous method behind it is engineering opinion at best.
- Use the Simple ↔ Operational Relevance spectrum as a map: when stuck, ask "am I too far left (too artificial) or too far right (too uncontrolled)?"
- Use the Hierarchy of Evidence when reading a security paper: "What study type is this?" before trusting the conclusion.
- Think of cyber security as an *observational science* (like atmospheric science), not a physical science — full control of variables at operational scale is rarely achievable.

## Anti-patterns
- **Jumping to operational scale without simple experiments first**: leads to biases and distractions; results are not reproducible.
- **Treating engineering solutions as scientific findings**: applying a tool is not the same as generating evidence about why it works.
- **Ignoring study type when citing evidence**: a case report and an RCT do not carry equal weight; conflating them weakens the field.
- **Treating lack of repeatability as unique to cyber**: observational sciences (ecology, atmospheric science, economics) face the same constraints and have developed rigorous methods around them.

## Reference Tables

| Branch of Science | Driving Approach | Example Fields |
|---|---|---|
| Physical Sciences | Controlled experiment validation of theories | Physics, Chemistry |
| Life Sciences | Observational + experimental | Biology, Ecology |
| Social Sciences | Qualitative/descriptive, best-fit models | Psychology, Sociology, Criminology |
| Mathematical Sciences | Logic, formal proofs | Mathematics, Data Science |
| Computational | Algorithm-generated models from empirical data | ML, AI |

## Worked Example
**The Heliocentric Model as a Pattern for Cyber Science:**
Astronomy progressed from geocentric (Earth-center) to heliocentric not through a single experiment but through iterative observations, model revisions, and perspective shifts. The key insight: the *same data* yielded different conclusions when analyzed from a new vantage point (Copernicus re-analyzing existing observations). Applied to cyber security: the same network traffic data can look benign or malicious depending on the analytical frame. The lesson — invest in building better models and changing perspective, not just collecting more data.

## Key Takeaways
1. Cyber security research is fundamentally an observational science; controlled experiments at operational scale are rarely achievable — design accordingly.
2. Use the Hierarchy of Evidence to calibrate how strongly any study result should be trusted; always disclose your study type.
3. Start every research program at the simple/controlled end of the continuum and iterate toward operational realism — skipping this step produces unreproducible results.
4. Science ≠ engineering: producing a tool is not the same as generating scientific knowledge about cyber security.
5. Reproducibility is the field's core deficit; every study design should ask "can someone replicate this?"

## Connects To
- **Ch 2**: Applies these science foundations specifically to the cyber security domain
- **Ch 3**: Uses the research type taxonomy (observational/experimental/mathematical/applied) to guide method selection
- **Ch 9**: Hypothetico-deductive research is the highest-rigor method in the Hierarchy of Evidence for cyber
- **Greenhalgh Hierarchy**: Standard evidence ranking framework from evidence-based medicine, adapted here for cyber
