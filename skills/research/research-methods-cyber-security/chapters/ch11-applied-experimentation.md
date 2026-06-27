# Chapter 11: Applied Experimentation

## Core Idea
Applied experimentation quantifies how well an engineered solution actually solves a cyber security problem — it is the "did we build the right system?" question, distinct from the "how does the system behave?" question of basic research. Two primary methods: benchmarking (atomic test cases, good for comparison) and validation testing (realistic conditions, good for operational understanding).

## Frameworks Introduced

- **Benchmarking**: A standard set of data, algorithm, or process used to generate comparable performance measurements across solutions.
  - When to use: When you need cross-solution comparison with a fixed "ruler"; when the problem has discrete, atomic test cases (e.g., malware detection, packet processing speed).
  - How: Define the benchmark (dataset, algorithm, or scenario set); choose one or more standardized metrics; run each solution against the same benchmark; report metrics with enough detail for replication.
  - Limitation: Does not replicate operational conditions; results may not reflect real-world performance.

- **Validation Testing**: Evaluates solutions in controlled environments under varied but realistic conditions.
  - When to use: When you want to understand how a solution behaves operationally, not just on curated test cases; when operational realism matters more than cross-solution comparability.
  - How: Define realistic scenarios from operational data; vary conditions systematically; measure performance against defined requirements.
  - Limitation: Harder to replicate realistically modeled environments; less directly comparable across implementations.

- **Basic Science → Applied Research Feedback Loop**:
  - Basic science generates causal knowledge → informs solution design
  - Applied experimentation validates whether the solution works
  - Applied results that fail feed BACK to basic science → identify missing causal knowledge
  - When to use: As a mental framework to avoid the "black hat cycle" (patching last year's vulnerabilities without understanding the underlying phenomena).
  - How: Before building a solution, check: "What basic science finding motivates this design?" If none, the applied result will be difficult to interpret when it fails.

## Key Concepts
- **Applied Research** — quantifies the effectiveness of applying scientific knowledge to a real-world problem; "validation testing"
- **Applied Experimentation** — controlled tests to evaluate engineered system performance; dependent variables are always performance/effectiveness metrics
- **Benchmarking** — standard test set applied consistently across solutions to produce comparable performance metrics
- **Benchmark** — the standard data, algorithm, or scenario; the "ruler"
- **Metric** — derived quantity that standardizes measurement; may combine multiple measures (e.g., F1 score, detection rate, GFLOPS)
- **Validation Testing** — evaluates solution in controlled but realistically varied conditions; similar to H-D experiments but applied to an existing system
- **Black Hat Cycle** — the reactive cycle of vulnerability discovery → defense → next vulnerability, without underlying scientific progress; breaks when basic science informs defense design
- **Applied vs. Basic Experimentation** — basic: "how does the system behave?"; applied: "how well does our solution perform?"; differ in hypothesis type, dependent variable focus, and research objective
- **Comparison Study** — applied experimental design that evaluates two or more solutions against the same benchmark or test conditions to identify the best option for a given use case

## Mental Models
- Think of benchmarking as using a ruler: the ruler stays fixed, you measure each solution against it. You can compare "Ruler says 7" and "Ruler says 9" — but the ruler's scale must be agreed upon in advance.
- Think of validation testing as "adversarial rehearsal" — vary the conditions the way an adversary would vary their attacks, and measure how well the solution holds up.
- The basic → applied → basic feedback cycle is how cyber security science should work: observe, theorize, experiment, build, test, refine. The "black hat cycle" skips the first three steps.
- A failed applied experiment is not a wasted applied experiment — it identifies where basic science is incomplete and redirects basic research.

## Anti-patterns
- **Building solutions without basic science foundations**: Developing defenses without knowing which variables drive the attack; produces solutions that work against last year's attacks, not the underlying phenomenon.
- **Using benchmarks as operational validation**: Benchmark results reflect curated test conditions; claiming operational effectiveness from benchmark scores alone is overstatement.
- **Non-standardized metrics**: Reporting different performance metrics for the same type of solution makes cross-study comparison impossible; agree on and use standard metrics.
- **Implied hypothesis without specification**: Applied experiments have an implied hypothesis ("the solution will solve the problem"), but that hypothesis still needs to be explicitly stated and the performance threshold defined.
- **Ignoring packer variance in malware detection benchmarks**: Malware benchmarks that don't vary packers underestimate real-world detection difficulty; benchmark must reflect real threat distribution.

## Reference Tables

| Method | Purpose | Conditions | Best For | Limitation |
|---|---|---|---|---|
| Benchmarking | Cross-solution comparison | Controlled, curated test set | Comparing AV tools, IDS signatures, firewall rules | May not reflect operational reality |
| Validation Testing | Operational effectiveness | Controlled, realistic variation | Understanding behavior under varied real-world conditions | Harder to compare across studies |

| Research Type | Hypothesis Form | DV Focus | Objective |
|---|---|---|---|
| Basic (H-D, Ch 9) | "If X then Y" (falsifiable causal prediction) | System behavior | Understand causal relationships |
| Applied (Ch 11) | "Solution S solves problem P" (implied) | Performance/effectiveness metrics | Quantify solution performance |
| Applied Observational (Ch 12) | "Solution S in operational setting Z shows behavior B" | Operational behavior, less controlled | Understand bounds of performance in realistic settings |

## Worked Example
**Benchmarking Mobile Antivirus Against Malware Packers:**

Problem: Mobile AV detection rates vary widely with malware packing techniques. A benchmark is needed to enable comparison.

1. **Benchmark design**:
   - Dataset: 500 malware samples from 5 families, each packed with 4 common packers (UPX, MPRESS, Themida, custom) = 2,000 sample variants
   - Control: Each AV product receives identical sample set; scanning performed with default settings
   - Metric: Detection Rate (DR) = detected samples / total samples × 100%; False Positive Rate (FPR) against 200 benign packed executables

2. **Execution**:
   - 3 mobile AV products tested
   - Results: Product A: DR=62%, FPR=4%; Product B: DR=81%, FPR=11%; Product C: DR=79%, FPR=2%

3. **Interpretation**: No single product dominates across both metrics — Product B maximizes detection; Product C balances detection with low false positives

4. **Applied feedback to basic science**: Products systematically fail on Themida-packed samples (DR < 30% across all three) → suggests Themida's obfuscation method is not captured in current signature approaches → basic research question: "What behavioral features distinguish Themida-packed malware from benign packed executables?"

## Key Takeaways
1. Use benchmarking when you need cross-solution comparison; use validation testing when you need operational realism — they answer different questions.
2. Define your metric before running the test — post-hoc metric selection leads to reporting bias.
3. Applied experimentation validates whether basic science produced a correct solution; failed applied experiments should route back to basic science to identify what was missing.
4. The "black hat cycle" (patch-last-year's-vulnerability) is broken only by grounding defenses in basic scientific understanding of the underlying phenomenon.
5. Always report both detection rate AND false positive rate for detection tools — optimizing only one is misleading.

## Connects To
- **Ch 9**: Hypothetico-deductive — applied experimentation is structurally similar but with performance DV and implied hypothesis
- **Ch 12**: Applied Observational Study — the less-controlled complement to applied experimentation
- **Ch 13**: Instrumentation — testbed and data collection setup enables applied experimentation in controlled environments
- **Ch 3**: Starting Research — decision tree routes to this chapter when testing performance of an existing solution
