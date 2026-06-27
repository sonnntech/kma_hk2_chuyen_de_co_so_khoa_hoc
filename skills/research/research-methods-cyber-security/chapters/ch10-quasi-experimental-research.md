# Chapter 10: Quasi-experimental Research

## Core Idea
Quasi-experiments are the pragmatic alternative when full variable control is infeasible — a common situation in cyber security due to Internet-scale complexity, small threat populations, and diverse environments. They produce weaker evidence than true experiments but are often the only option; the goal is to control as many variables as possible and document the rest.

## Frameworks Introduced

- **Quasi-experiment Definition (Expanded for Cyber)**: Any experiment where a small number of independent variables are NOT completely controlled. Standard social science definition is "insufficiently randomized population"; the book expands this to include "any experiment that intersects with a natural or operational environment."
  - When to use: When a hypothesis is formed and testable in principle, but one or more independent variables cannot be fully controlled due to scale, ethics, cost, or population size.
  - How: Attempt to control as many variables as possible first; treat only genuinely uncontrollable variables as quasi-experimental; document all uncontrolled variables explicitly.

- **5 Cyber Drivers for Quasi-experimental Design**:
  1. **Internet scale** — impossible to replicate or fully simulate Internet complexity; studies involving real Internet must be quasi-experimental
  2. **Users as background noise** — human behavior needed for realism but cannot be fully controlled; provides fidelity at the cost of control
  3. **Population limitations (Threats)** — threat actor populations are small and adversarial to research; red teams substitute but create sample size challenges
  4. **Cyber environment diversity** — every cyber environment is unique ("snowflake"); testing across all configurations is infeasible; limited test environments = quasi-experimental scope
  5. **Specialized user populations** — access to users tied to specific use cases is restricted; population size limits randomization
  - When to use: As a checklist when deciding if a true experiment is achievable or if quasi-experimental design is necessary.

- **Difference-of-Differences Design**: A common quasi-experimental method.
  - Compares the change in outcome for a treatment group versus the change for a control group, before and after the treatment is applied.
  - Used extensively with red teams: compare pre/post metrics for the treated system vs. the untreated control system.
  - Controls for pre-existing differences between groups by focusing on the delta-of-deltas.
  - When to use: When random assignment is not possible and you have baseline measurements for both groups before treatment.

## Key Concepts
- **True Experiment** — all independent variables controlled; maximum evidence strength; typically infeasible at operational cyber scale
- **Quasi-experiment** — one or more independent variables not fully controlled; weaker evidence; often the only viable option in cyber research
- **Internal Validity** — degree to which observed effects are caused by the independent variable vs. uncontrolled confounders; the primary risk in quasi-experiments
- **Randomization** — assigning subjects to treatment/control groups randomly; the gold standard control for individual differences; often infeasible with small or adversarial populations
- **Red Team** — professional penetration testers used as threat actor proxies in research; small population, high cost, difficult to randomize
- **Difference-of-Differences** — quasi-experimental design measuring delta between pre/post outcomes in treatment vs. control groups; controls for baseline differences without randomization
- **Background Noise (Users)** — human behavior introduced to increase experimental realism; inherently uncontrollable; a source of both validity (ecological) and confounding (experimental)
- **Operational Environment** — real-world cyber environment, not a controlled testbed; high realism, low controllability
- **Internet Scale** — scale of the global Internet; creates uncontrollable variables in any experiment touching real Internet infrastructure
- **Snowflake Environment** — any cyber environment with unique configuration; means no two test environments are equivalent; limits generalizability

## Mental Models
- Think of quasi-experiments as "true experiments with documented compromises" — not inferior by nature, but requiring explicit acknowledgment of what you couldn't control.
- "Always strive toward the true experiment" — if a variable CAN be controlled, control it; quasi-experimental status applies only to genuinely uncontrollable variables.
- Red teams are to cyber security research as clinical trial participants are to medicine: necessary proxies for the real population, but with significant selection and size limitations.
- Internet-involving research is almost always quasi-experimental — design for it explicitly rather than treating it as a failure mode.
- Document uncontrolled variables the same way you document controlled ones — this enables future researchers to add controls you couldn't.

## Anti-patterns
- **Using quasi-experimental as a shortcut**: Choosing quasi-experimental design because controlling variables is hard, not because it's genuinely infeasible — produces weak evidence when strong evidence was achievable.
- **Failing to maximize control of remaining variables**: Treating "quasi" as "uncontrolled" — even in quasi-experiments, control everything you can and document what you can't.
- **Not documenting uncontrolled variables**: Quasi-experiments with undocumented confounders cannot be interpreted, replicated, or built upon.
- **Claiming causal conclusions from quasi-experiments**: Quasi-experiments produce evidence of association and may suggest causality, but the uncontrolled variables prevent strong causal claims without further experimental validation.
- **Equating red team results with real attacker results**: Red teams have different incentives, constraints, and knowledge than real attackers; always bound the generalizability of red team-based findings.

## Reference Tables

| Situation | Recommends | Reason |
|---|---|---|
| All variables controllable, randomizable | True experiment (Ch 9) | Maximum evidence strength |
| One or a few variables uncontrollable, hypothesis testable | Quasi-experiment (Ch 10) | Only viable experimental option |
| Variables uncontrollable, no feasible experiment | Observational study (Ch 4–5) | No experimental control possible |
| System untestable, observational data unavailable | Theoretical research (Ch 7) | Formal model is the only path |

| Quasi-experimental Driver | Example in Cyber Security | Mitigation |
|---|---|---|
| Internet scale | Studying real BGP hijacking behavior | Use Internet-connected testbed; document Internet-sourced confounders |
| Threat population size | Red team study with 5 teams | Report power analysis; bound conclusions to studied population |
| Snowflake environments | Testing across 3 org network configs | Characterize each config; test for interaction effects |
| Specialized users | Testing a SCADA operator population | Partner with an org; document selection bias |

## Worked Example
**Difference-of-Differences: Testing a New Firewall Rule Against Red Team Attacks**

The researcher wants to know if a new egress filtering rule reduces data exfiltration during red team exercises. Full randomization is not feasible (only 6 red teams available).

**Design**:
- **Treatment group**: 3 networks with new egress filtering applied mid-exercise
- **Control group**: 3 networks with no change
- **Measurement**: Volume of data exfiltrated (MB) at two points: T1 (before) and T2 (after) the firewall change

**Difference-of-differences calculation**:
- Treatment: T1_treat = 450 MB, T2_treat = 120 MB → ΔT = −330 MB
- Control: T1_ctrl = 430 MB, T2_ctrl = 410 MB → ΔC = −20 MB
- DiD = ΔT − ΔC = −330 − (−20) = −310 MB → egress filtering reduced exfiltration by ~310 MB beyond the trend

**Limitations stated**: Small sample (n=6 teams); red teams, not real attackers; networks are not identical configurations; Internet connection present in 2 of 6 networks (documented as confounder)

## Key Takeaways
1. Choose quasi-experimental design when a variable is genuinely uncontrollable — not as a shortcut; document the justification.
2. Maximize control of everything you can; quasi-experimental applies only to the specific uncontrollable variables.
3. The 5 cyber-specific drivers (Internet, users, threat population, environment diversity, specialized users) are the checklist for whether quasi-experimental is justified.
4. Difference-of-differences is the go-to design when randomization is infeasible but baseline measurements for both groups are available.
5. Always explicitly state what uncontrolled variables remain and how they might affect internal validity — this is non-negotiable for peer review.

## Connects To
- **Ch 9**: Hypothetico-deductive — quasi-experiment is the fallback when true experimental control is infeasible
- **Ch 4**: Exploratory Study — if even quasi-experimental is infeasible, move to observational
- **Ch 13**: Instrumentation — testbed selection is the primary mitigation for cyber environment quasi-experimental limitations
- **Ch 14**: Adversarial Research — red teams and threat populations are the primary quasi-experimental population in adversarial studies
