# Chapter 9: Hypothetico-deductive Research

## Core Idea
Hypothetico-deductive research is the gold standard of experimental cyber security science — it converts inductive observations into deductive falsifiable hypotheses, designs controlled experiments to test them, and produces the strongest possible evidence for causal relationships. A poorly formed hypothesis makes the entire experiment worthless.

## Frameworks Introduced

- **4 Characteristics of a Good Hypothesis**:
  1. **Observable and Testable** — the behavior can be measured AND an experiment is practically feasible (ethically, legally, economically). If observable but not testable, use theoretical methods. If neither, reformulate.
  2. **Clearly Defined** — all terms, variables, and metrics are unambiguous; avoid "better/worse," "more/less" without specific thresholds; no domain jargon without explicit definition (e.g., define "APT" before using it)
  3. **Single Concept** — tests ONE causal relationship (if x, then y); multiple concepts in one hypothesis confound results; break into multiple atomic hypotheses
  4. **Predictive** — states specifically how the system will behave under defined conditions, not just that something will change
  - When to use: Before finalizing any experimental design — screen every hypothesis against all four characteristics.
  - How: Write the hypothesis. Then ask: Can I measure this? Can I control the conditions? Is every term defined? Is there exactly one independent variable? Is the prediction specific and directional?

- **Hypothetico-deductive vs. Applied Experimentation**:
  - **Basic (H-D)**: Understand how a system behaves; test causal relationships; study existing systems
  - **Applied**: Validate performance of a designed/built solution; quantify how well knowledge was applied
  - Rule of thumb: "Trying to understand how a system behaves" → H-D. "Testing a system you built for performance" → Applied (Ch 11).
  - When to use: Route at the start — confusing the two leads to experiments that answer the wrong question.

- **Falsifiability Principle** (Popper): We can never prove a theory true, but we CAN prove a hypothesis false. Science advances by eliminating false hypotheses and building confidence in those that survive. Every experiment is an attempt to falsify your hypothesis.
  - When to use: When evaluating whether a proposed experiment is scientifically meaningful.
  - How: Ask "what observation would make this hypothesis FALSE?" If no such observation is possible, the hypothesis is not scientific.

- **Experimental Design Components** (required documentation):
  - Independent variables (manipulated)
  - Dependent variables (measured)
  - Control variables (held constant)
  - Experimental setup and configuration
  - Equipment, personnel, and resources
  - Process and manipulation procedures
  - Data analysis methods
  - When to use: Before running any experiment; this documentation enables independent replication.

## Key Concepts
- **Hypothesis** — falsifiable, testable prediction of how a system will behave under clearly defined conditions; converts inductive observations into deductive testable statements
- **Independent Variable** — the variable you manipulate in the experiment (the cause)
- **Dependent Variable** — the variable you measure in the experiment (the effect)
- **Control Variable** — variables held constant to prevent confounding
- **Confounding Variable** — an uncontrolled variable that influences the dependent variable and distorts results
- **Falsifiability** — property of a hypothesis that it can be disproven by observation; the defining feature of scientific claims (Popper)
- **Quine-Duhem Thesis** — it is impossible to truly test a hypothesis in isolation; hypotheses are formulated within a web of background assumptions; state all assumptions explicitly
- **Replication** — independent reproduction of an experiment by a different researcher; essential for validating results and identifying errors
- **Basic Experimentation** — studies how a system behaves; generates evidence for causal relationships
- **Applied Experimentation** — validates performance of a designed solution (Ch 11)
- **Null Hypothesis** — the default assumption that there is no effect; the experiment attempts to reject it

## Mental Models
- The hypothesis is the keystone — build it wrong and the entire experiment is misaligned. A 30-minute hypothesis review prevents months of wasted experimentation.
- Think of each experiment as an attempt to DESTROY your hypothesis, not confirm it. Designing to confirm leads to confirmation bias; designing to falsify leads to valid science.
- Single-concept rule: "One cause, one effect." If you want to test IP hopping AND software diversity together, do three experiments: one for each separately, one for their interaction.
- Observable but untestable → theoretical research. Neither observable nor testable → reformulate the question. Both → proceed to experimental design.
- The Quine-Duhem thesis means: always state your assumptions, because a failed experiment could mean (a) the hypothesis is false, OR (b) one of your background assumptions is wrong.

## Anti-patterns
- **Multi-variable hypothesis**: Testing "IP hopping and software diversity increase attack time" → can't isolate which variable caused the effect; always split.
- **Undefined domain jargon**: "APT attackers have higher success rates than script kiddies" → APT and script kiddie are undefined; impossible to operationalize.
- **Relative measurements without thresholds**: "performance is better" → undefined; use "performance increases by at least 10% as measured by X metric."
- **Testing the untestable**: "The Internet will collapse if 60% of backbone is DDoS'd" → infeasible; redirect to theoretical research.
- **Designing to confirm**: Collecting only data that supports the hypothesis and stopping when confirmation appears; valid experiments try to reject the hypothesis.
- **Missing replication documentation**: Experiments that cannot be independently replicated are not scientifically verifiable — document all setup details.

## Reference Tables

| Hypothesis Quality Check | Good Example | Bad Example |
|---|---|---|
| Observable & Testable | "Public attack surface is linearly correlated with number of observed attacks" | "Attackers target AWS for monetary gain" (intent unobservable) |
| Clearly Defined | "NCCDC 2016 Red Team will have 20% higher success ratio vs. first-year teams" | "APTs outperform script kiddies" (APT undefined) |
| Single Concept | "Time to successful attack increases as IP hopping frequency increases" | "IP hopping and software diversity increase attack time" (two variables) |
| Predictive | "Detection rate decreases by ≥15% as packet encryption coverage increases from 0 to 100%" | "Detection rate will change with encryption" (non-directional) |

| Experiment Type | Goal | Suitable When |
|---|---|---|
| Basic (H-D) | Understand causal behavior of existing system | Variables controllable; studying causal relationships |
| Applied (Ch 11) | Validate performance of designed solution | Testing a system you built |
| Quasi-experimental (Ch 10) | Causal understanding when full control is infeasible | Some control possible; observational setting |

## Worked Example
**Password Complexity → Time-to-Crack Hypothesis:**

*Initial (bad) hypothesis*: "Complex passwords are harder to crack."
Problems: "complex" undefined, "harder" undefined, no specific prediction.

*Refined hypothesis*: "Increasing password entropy from 30 bits to 50 bits increases offline dictionary attack time from under 1 minute to over 24 hours on a single GPU (NVIDIA RTX 3080, hashcat default settings, bcrypt hash)."

Hypothesis check:
- Observable: Yes — crack time is measurable
- Testable: Yes — we can generate passwords at defined entropy levels and run hashcat
- Clearly defined: Yes — entropy, GPU, attack tool, hash function all specified
- Single concept: Yes — one independent variable (entropy), one dependent variable (crack time)
- Predictive: Yes — specific directional threshold (1 min → 24h)

Experimental design:
- **IV**: Password entropy (30, 35, 40, 45, 50 bits)
- **DV**: Time to crack (seconds)
- **Control**: Same GPU, same attack tool, same wordlist, same hash function
- **Confound controlled**: Multiple trials per entropy level; median reported
- **Replication**: Full setup documented; wordlist, hashcat config, and GPU specs published

## Key Takeaways
1. Screen every hypothesis against 4 criteria before designing the experiment: Observable, Testable, Clearly Defined, Single Concept.
2. Design experiments to FALSIFY the hypothesis, not confirm it — confirmation bias produces weak evidence.
3. State ALL background assumptions explicitly (Quine-Duhem): a failed experiment could mean either the hypothesis is wrong OR an assumption is wrong.
4. Document the full experimental design (IVs, DVs, controls, setup, analysis) to enable independent replication — unreplicable experiments are not scientifically valid.
5. Distinguish basic (H-D) from applied experimentation at the outset: H-D studies how systems behave; applied tests how well your solution performs.

## Connects To
- **Ch 3**: Routed here from decision tree when a falsifiable hypothesis exists and variables can be controlled
- **Ch 8**: Simulation output → hypotheses for H-D experiments
- **Ch 10**: Quasi-experimental — when full control is not achievable
- **Ch 11**: Applied Experimentation — when testing engineered solutions
- **Ch 1**: Hierarchy of Evidence — controlled experiments rank 2-3, highest attainable in most cyber security research
