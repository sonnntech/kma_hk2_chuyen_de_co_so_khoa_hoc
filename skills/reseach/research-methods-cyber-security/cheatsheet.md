# Cheatsheet — Research Methods for Cyber Security
*Decision rules, routing logic, and judgment calls the authors apply*

---

## Method Routing: What Question Type → What Research Method

| Your Situation | Route To |
|---|---|
| No hypothesis yet; want to understand a system | Observational → Ch 4 (Exploratory) or Ch 5 (Descriptive) |
| No hypothesis; large dataset available | ML → Ch 6 |
| Cannot observe or experiment; too complex or rare | Theoretical → Ch 7 (Formal) or Ch 8 (Simulation) |
| Have a falsifiable hypothesis; can control variables | H-D Experiment → Ch 9 |
| Have a hypothesis; cannot fully control variables | Quasi-experiment → Ch 10 |
| Testing performance of an existing solution | Applied → Ch 11 (Experimentation) or Ch 12 (Observational) |
| Studying a specific known event or actor in depth | Descriptive → Ch 5 (Case Study) |
| Need to plan data collection infrastructure | Instrumentation → Ch 13 |
| Research involves attacker behavior | Adversarial model → Ch 14 first |
| Unsure if research action is ethically acceptable | Ethics review → Ch 15 |

---

## Hypothesis Quality Gate (OTCS)

| Check | Question | Fail → |
|---|---|---|
| **O**bservable | Can I measure the behavior? | Reformulate or use theoretical research |
| **T**estable | Can I create an ethical, feasible experiment? | Use theoretical or observational |
| **C**learly Defined | Are all terms, variables, thresholds unambiguous? | Add operational definitions |
| **S**ingle Concept | Exactly one IV → one DV? | Split into multiple atomic hypotheses |

*If all four pass: proceed to experimental design. If any fail: fix before continuing.*

---

## Evidence Strength Ranking (for the question: "how much should I trust this?")

```
Strongest: Systematic reviews/meta-analyses of controlled trials
           ↓ RCTs with definitive results
           ↓ RCTs with non-definitive results
           ↓ Cohort studies
           ↓ Case-control studies
           ↓ Cross-sectional surveys
Weakest:   Case reports
```

**Rule**: State your study type in every paper/presentation. Claiming causal conclusions from case-report evidence is the most common epistemic error in cyber security research.

---

## Observational Study Type Selection

| Time | Unit | → Method |
|---|---|---|
| Retrospective | Individual / group | Case-control |
| Point-in-time | Population | Cross-sectional (census) |
| Over time | Defined group | Cohort/Longitudinal |
| Any | Population-level patterns | Ecological |
| Deep single case | Single event/system | Case study (descriptive) |

---

## ML Algorithm Selection

**Step 1: Labels?**
- All labeled → Supervised
- None labeled → Unsupervised
- Some labeled → Semi-supervised

**Step 2: Answer shape?**
- Category → Classification (SVM, Random Forest, HMM, Neural Net)
- Groups → Clustering (K-means, DBSCAN, Hierarchical)
- Number → Regression (Linear, Logistic, MARS)
- Anomaly flag → Anomaly Detection (One-class SVM, FP-growth)

**Step 3: Validate**
- 60/20/20 split (train/val/test)
- Tune on val set ONLY
- Report test set results ONCE at end

**Overfit signal**: Low training error, high test error → reduce features or add regularization  
**Underfit signal**: High training error → add features or polynomial terms

---

## Simulation Use Case Decision

| Goal | Simulation Type | Produces |
|---|---|---|
| Explore theoretical model behavior | Theoretical Simulation | Understanding of model at extremes; NOT evidence for the theory |
| "What would happen if…?" planning | Decision Support | Scenario outcome predictions; bounded by model validity |
| Generate hypotheses to test experimentally | Empirical Simulation | Hypotheses; validated by matching real experiment data |

**Rule**: Simulation output ≠ experimental evidence. Always validate theory with a real experiment.

---

## Fidelity Selection by Data Source

| Need | Use |
|---|---|
| Payload analysis, DPI-based detection | Full PCAP (port span, network tap) |
| Behavioral patterns, lateral movement detection | NetFlow / IPFIX |
| Endpoint activity, privilege escalation, persistence | OS/host logs (syslog, Windows Event Log) |
| C2 detection, DGA | DNS query logs |
| Memory-resident malware, runtime state | Memory dump (volatile) |
| Causal ordering, millisecond-level timing | Synchronized clocks (NTP verified; GPS for ns-level) |

**Rule**: If you need payload → don't use NetFlow. If you need timing → verify clock sync before collection.

---

## Vulnerability Disclosure Decision Tree

```
Discover vulnerability?
├─ Is a patch available? → Yes → Publish with credit
└─ No patch available
    ├─ Notify vendor (Day 0)
    ├─ Vendor responds within 30 days? → No → Escalate; notify CERT
    └─ Vendor provides fix within 180 days? → No → Public disclosure
                                             → Yes → Coordinate joint publication
```

**Rule**: Default is responsible disclosure. Never immediate full disclosure for critical infrastructure vulnerabilities.

---

## Ethical Quick Test

Before any research action, ask:
1. **Authorization**: Do I have explicit written permission to access this system/data?
2. **Harm to subjects**: Would subjects be put at additional risk by this research?
3. **Individual rights default**: If a single subject would object to this, is the case for common good overwhelming?
4. **Disclosure requirements**: If I discover a vulnerability, am I prepared to follow responsible disclosure?

If any answer raises a concern → pause and get ethics review before proceeding.

---

## Adversary Tier vs. Research Implication

| DoD Tier | Capability | Research Implication |
|---|---|---|
| I–II | Off-the-shelf tools | Red team of junior pentesters is adequate proxy |
| III–IV | Discovers new vulns; more resources | Experienced red team; custom exploits in testbed |
| V–VI | Nation-state; supply chain; years of investment | Red team cannot replicate; use TTP-based simulation |

**Rule**: Always state your assumed adversary tier in any paper reporting adversarial experiment results. Results only generalize to the tier modeled.

---

## Applied Research Type Decision

| Question | Method |
|---|---|
| "How well does solution S perform against known test cases?" | Benchmarking (standardized comparison) |
| "How does solution S behave in realistic varied conditions?" | Validation Testing |
| "What are the operational limits of solution S?" | Operational Bounds Testing (stress/load/performance) |
| "How does solution S compare to solution T in a real environment?" | Comparison Study |

**Rule**: Benchmark scores ≠ operational performance. Run all three bounds tests (stress, load, performance) before any production deployment.

---

## Red Flags That Your Research Design Has a Problem

- Hypothesis contains "better/worse/improved" without numeric threshold → **undefined, fix it**
- Multiple IVs in one hypothesis → **split into separate hypotheses**
- Cannot state what observation would make the hypothesis FALSE → **not falsifiable, redesign**
- Using "APT" or "script kiddie" without defining them → **operationalize the term**
- Claim "anonymized data is safe to share" without re-identification analysis → **verify first**
- Applied experiment results claimed as causal findings → **basic ≠ applied; state the difference**
- Simulation results cited as evidence for the theory → **simulation ≠ experimental evidence**
