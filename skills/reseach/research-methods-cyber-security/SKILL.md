---
name: research-methods-cyber-security
description: "Knowledge base from \"Research Methods for Cyber Security\" by Thomas W. Edgar & David O. Manz. Use when applying scientific research methods to cyber security questions, selecting a research method (observational, theoretical, experimental, applied), designing experiments, formulating hypotheses, planning data collection/instrumentation, or addressing ethical issues in cyber security research."
---

<!-- argument-hint: [research method, chapter number, topic like hypothesis/instrumentation/adversary/ethics] -->

# Research Methods for Cyber Security
**Author**: Thomas W. Edgar & David O. Manz (Pacific Northwest National Laboratory) | **Pages**: ~402 | **Chapters**: 15 | **Generated**: 2026-06-21

## How to Use This Skill

- **Without arguments** — load core frameworks for method selection and research design
- **With a topic** — ask about `hypothesis`, `instrumentation`, `adversary`, `ML`, or another topic; I find and read the relevant chapter
- **With chapter** — ask for `ch09`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" to see the full index

When you ask about a topic not covered in Core Frameworks below, I will read the relevant chapter file before answering.

---

## Core Frameworks & Mental Models

### The Central Routing Decision: Which Research Method?

The entire book is a routing system. Use this gate first:

| Your Situation | Method Category | Chapter |
|---|---|---|
| No hypothesis; want to understand real system | Observational | Ch 4–6 |
| System too complex to observe/experiment; data unavailable | Theoretical | Ch 7–8 |
| Falsifiable hypothesis; can control variables | Experimental (H-D) | Ch 9 |
| Hypothesis but cannot fully control variables | Quasi-experimental | Ch 10 |
| Testing performance of an existing solution | Applied | Ch 11–12 |

**Rule 0**: Always start with the smallest possible atomic research question. "Why is cyber security failing?" is unanswerable; "Does password entropy above 50 bits prevent offline dictionary attacks under 24h on GPU?" is testable.

---

### Framework 1: Hierarchy of Evidence

Every study type produces evidence of a different strength. Know where you stand:

```
Strongest → Systematic reviews / meta-analyses of RCTs
            RCTs with definitive results
            RCTs with non-definitive results  
            Cohort studies
            Case-control studies
            Cross-sectional surveys
Weakest  → Case reports
```

**Cyber security is mostly observational** — the field cannot run RCTs at operational scale. Explicitly state your study type so readers calibrate accordingly. The single most common epistemic failure in cyber security research is claiming causal conclusions from case-report or correlation evidence.

---

### Framework 2: The Good Hypothesis (OTCS)

Before designing any experiment, screen the hypothesis against 4 criteria:

1. **Observable** — can you measure it? ("Intent of AWS attackers" is not observable; "number of observed attacks correlated with public attack surface" is)
2. **Testable** — can you create an ethical, feasible experiment? ("DDoS the Internet backbone" is not testable)
3. **Clearly Defined** — all terms, variables, and metrics are unambiguous with numeric thresholds. Replace "better performance" with "≥10% reduction in mean detection latency"
4. **Single Concept** — exactly one independent variable → one dependent variable. Two IVs in one hypothesis → confounded results → split into separate hypotheses

**Popper's corollary**: Design experiments to FALSIFY the hypothesis, not confirm it. Ask: "What observation would make this false?" If none exists, it is not scientific.

---

### Framework 3: The Continuum of Discovery

Simple/controlled experiments ↔ Operational/realistic observations

```
More control  ←────────────────────────────→  More realism
Lab testbed      Quasi-experiment      Real network
(repeatable)       (mixed)           (operationally relevant)
```

**Rules**:
- Start at the simple/controlled end; iterate toward operational realism
- Jumping straight to operational scale produces unreproducible results and firmly-held false beliefs
- Cyber security is fundamentally an **observational science** (like atmospheric science) — full control at operational scale is rarely achievable

---

### Framework 4: Theory Lifecycle

Cognitive model → Formal model (mathematical) → Theory (empirically supported) → Law (widely accepted)

**Good theory must be**: Coherent (self-consistent), Parsimonious (simplest fit), Systematic (covers the range), **Predictive** (generates testable hypotheses), **Falsifiable** (can be disproven).

Choose theoretical research ONLY when: (1) data is unavailable, (2) experiments are infeasible/unethical, or (3) the system requires formalization before empirical work can begin.

---

### Framework 5: Data Fidelity (5 Axes)

Before selecting any sensor, check all five:

| Axis | What to Ask | Common Failure |
|---|---|---|
| Time | Is timestamp precision adequate for event ordering? | NTP insufficient for ns-level causal analysis |
| Sample Rate | Does downsampling miss rare events? | 1-in-1000 NetFlow misses short attack bursts |
| Summarization | Does aggregation remove needed information? | NetFlow loses payload; inadequate for DPI detection |
| Proxy | Does the indirect measure capture the right level? | Log-level data misses in-memory behavior |
| Scale | Are sensors at ALL locations the phenomenon appears? | Worm study without DNS sensor misses C2 traffic |

**Key rule**: Operational sensors were built for operations, not science. Validate before reusing them for research.

---

### Framework 6: The Adversarial Model

Cyber security is unique: your subject of study actively hides and adapts. Every experiment involving attacker behavior needs an explicit threat model with 3 dimensions:

1. **Capability** — DoD Tier (I–VI); resources, tools, time. Warning: tool commoditization means Tier I actors can wield Tier V tools.
2. **Intent** — criminal, hacktivist, insider, nation-state, opportunistic. More stable than capability for modeling purposes.
3. **TTP** — Tactics (resource application), Techniques (specific methods), Procedures (exact steps). Can be faked; insufficient alone for attribution.

**Red team rule**: Red teams are proxies with time constraints, legal limits, and professional motivation mismatches. Always state what aspects of real adversarial behavior they do NOT capture.

---

### Framework 7: Scientific Ethics Defaults

- **Default to individual rights**: A single subject's objection can override a common-good argument unless the case is overwhelming.
- **Responsible disclosure protocol**: Private vendor notification → 6 months → public if unpatched.
- **Unauthorized access is a hard line**: Unethical AND illegal regardless of research intent.
- **Anonymized ≠ safe**: Re-identification attacks have defeated multiple research datasets believed to be safely anonymized.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-introduction-to-science.md) | Introduction to Science | Hierarchy of Evidence, Continuum of Discovery, Three Faces of Science |
| [ch02](chapters/ch02-science-and-cyber-security.md) | Science and Cyber Security | CIA Triad, Cybernetic Perspective, Analogy Danger |
| [ch03](chapters/ch03-starting-your-research.md) | Starting Your Research | Research Method Decision Tree, Hypothesis Definition, Literature Survey |
| [ch04](chapters/ch04-exploratory-study.md) | Exploratory Study | Case-Control, Ecological, Cross-Sectional, Longitudinal/Cohort, Inductive Reasoning Defense |
| [ch05](chapters/ch05-descriptive-study.md) | Descriptive Study | Case Study, Elicitation Study, Case Report, Data Collection Timing Rule |
| [ch06](chapters/ch06-machine-learning.md) | Machine Learning | ML Learning Style Selection, ML Problem Type Selection, Cross-Validation Protocol, Bayesian Networks, HMMs |
| [ch07](chapters/ch07-theoretical-research.md) | Theoretical Research | Theory Development Process (7-step), Theory Lifecycle, 5 Characteristics of Good Theory |
| [ch08](chapters/ch08-simulation.md) | Using Simulation for Research | Simulation Fidelity Hierarchy, 3 Use Cases (Theoretical/Decision Support/Empirical), Model Validation |
| [ch09](chapters/ch09-hypothetico-deductive-research.md) | Hypothetico-deductive Research | 4-Criterion Hypothesis Screen (OTCS), Falsifiability, Experimental Design Components, Basic vs. Applied |
| [ch10](chapters/ch10-quasi-experimental-research.md) | Quasi-experimental Research | 5 Cyber Drivers for Quasi-experimental, Difference-of-Differences, Internal Validity |
| [ch11](chapters/ch11-applied-experimentation.md) | Applied Experimentation | Benchmarking, Validation Testing, Basic→Applied Feedback Loop, Black Hat Cycle |
| [ch12](chapters/ch12-applied-observational-study.md) | Applied Observational Study | Applied Exploratory/Descriptive, Operational Bounds Testing (Stress/Load/Performance) |
| [ch13](chapters/ch13-instrumentation.md) | Instrumentation | 5-Axis Data Fidelity, Scientific vs. Operational Sensors, Testbed Design |
| [ch14](chapters/ch14-addressing-the-adversary.md) | Addressing the Adversary | DoD Adversary Tier Model, Threat Modeling (Capability/Intent/TTP), Threat vs. Hazard |
| [ch15](chapters/ch15-scientific-ethics.md) | Scientific Ethics | Responsible Disclosure Protocol, Ethical Grey Areas, Individual Rights vs. Common Good |

## Topic Index

- **Adversary / Threat Actor** → ch02, ch14
- **All-Hazards** → ch14, ch15
- **Anomaly Detection** → ch06, ch12
- **Applied Research** → ch11, ch12
- **Attribution** → ch14
- **Bayesian Networks** → ch06
- **Benchmarking** → ch11
- **Black Hat Cycle** → ch11
- **Case-Control Study** → ch04
- **Case Report** → ch05
- **Case Study** → ch05, ch14
- **CIA Triad** → ch02
- **Classification (ML)** → ch06
- **Cohort Study** → ch04
- **Continuum of Discovery** → ch01
- **Cross-Sectional Study** → ch04
- **Cross-Validation** → ch06
- **Cyber Space (definition)** → ch02
- **Data Fidelity** → ch13
- **Decision Tree (method selection)** → ch03
- **Descriptive Study** → ch05
- **Difference-of-Differences** → ch10
- **Elicitation Study** → ch05
- **Emulation** → ch08
- **Experimental Design** → ch09
- **Exploratory Study** → ch04
- **Falsifiability** → ch09
- **Formal Theory** → ch07
- **Hidden Markov Model** → ch06
- **Hierarchy of Evidence** → ch01, ch04, ch05
- **Hypothesis** → ch03, ch09
- **Inductive Reasoning** → ch04, ch07
- **Insider Threat** → ch14
- **Instrumentation** → ch13
- **Literature Survey** → ch03
- **Load Testing** → ch12
- **Longitudinal Study** → ch04
- **Machine Learning** → ch06
- **Model Validation** → ch08
- **NetFlow / IPFIX** → ch13
- **Nonrepudiation** → ch02
- **Observational Research** → ch04, ch05
- **Operational Bounds Testing** → ch12
- **Overfitting / Underfitting** → ch06
- **Performance Testing** → ch12
- **Privacy** → ch15
- **Proxy Measurement** → ch13
- **Quasi-experimental** → ch10
- **Red Team** → ch10, ch14
- **Regression (ML)** → ch06
- **Replication** → ch09
- **Responsible Disclosure** → ch15
- **Scientific Ethics** → ch15
- **Simulation** → ch08
- **Stress Testing** → ch12
- **Testbed** → ch13
- **Theory Development** → ch07
- **Threat Model** → ch14
- **TTP** → ch14
- **Validation Testing** → ch11
- **Virtualization** → ch08
- **Vulnerability** → ch02
- **Vulnerability Disclosure** → ch15

## Supporting Files

- [glossary.md](glossary.md) — all key terms with definitions
- [patterns.md](patterns.md) — all techniques, patterns, and research methods
- [cheatsheet.md](cheatsheet.md) — decision rules, routing tables, and quick-reference judgment calls

---

## Scope & Limits

This skill covers the book content only. For hands-on implementation in your codebase, combine with project-specific tools. The book was published in 2017 — ML techniques, tool names, and some ethical norms (especially around AI) have evolved since then. For topics beyond this book (e.g., AI-specific research ethics, LLM security), check related skills or ask the agent directly.
