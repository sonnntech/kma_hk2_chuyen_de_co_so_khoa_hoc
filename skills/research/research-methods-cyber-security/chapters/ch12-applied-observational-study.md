# Chapter 12: Applied Observational Study

## Core Idea
Applied observational study is the most common research type in cyber security — it evaluates how a solution or change performs under real or near-real conditions without the strict controls of a true experiment. The distinction from foundational observational study is that the researcher introduces a specific system/change and has a performance expectation to evaluate.

## Frameworks Introduced

- **Applied vs. Foundational Observational Study Distinction**:
  - **Foundational**: Observes the entire system without presumption; no change introduced by researcher; goal = understand natural behavior
  - **Applied**: Introduces a specific change or subject; researcher has a performance expectation; goal = understand how well a solution performs
  - When to use: If you are studying how a real system behaves → foundational (Ch 4–5). If you are studying how a change to a system performs → applied (Ch 12).

- **Two Applied Study Subtypes**:
  1. **Applied Exploratory Study** — explores the consequences and extent of a solution's behavior; includes operational bounds testing (stress, performance, load); determines capability envelope
  2. **Applied Descriptive Study** — describes implementation and effect of a specific solution in a real context; the "here's how we applied the science" paper
  - When to use: Exploratory when you want to find the limits. Descriptive when you want to document an implementation.

- **Operational Bounds Testing** (3 variants):
  1. **Stress Testing** — push the system beyond expected extremes; find the breaking point
  2. **Performance Testing** — evaluate how well system behavior conforms to stated expectations under normal conditions
  3. **Load Testing** — evaluate the system at maximum expected operational load; confirm it holds up in production-representative conditions
  - When to use: Any new security tool deployment requires all three before operational deployment. Use stress when safety/reliability matters; use load when capacity planning is needed; use performance to confirm spec compliance.
  - How: Increment one variable at a time until failure or physical limit; document the failure mode and threshold.

## Key Concepts
- **Applied Observational Study** — observes a specific subject (solution, policy, tool) for performance, function, or security; includes an expectation of behavior; most common research type in cyber security
- **Applied Exploratory Study** — determines the envelope of solution behavior; sensitivity analysis, stress/load/performance testing
- **Applied Descriptive Study** — documents the implementation and observed effects of applying scientific knowledge; qualitative; "case report with a scientific basis"
- **Operational Bounds Testing** — systematic exploration of system behavior at extremes (stress), at max load (load), and against performance expectations (performance)
- **Stress Testing** — evaluates system at and beyond operational extremes; finds breaking point
- **Load Testing** — evaluates system at maximum expected operational load; confirms production viability
- **Performance Testing** — evaluates conformance to defined performance requirements under normal conditions
- **Sensitivity Analysis** — explores how sensitive system behavior is to changes in input parameters
- **Foundational vs. Applied** — foundational seeks causal understanding; applied seeks performance characterization of an existing solution

## Mental Models
- Think of applied observational study as "taking the solution on a shakedown cruise" — you're not proving causal science, you're characterizing real behavior in realistic conditions.
- Operational bounds testing is the scientific form of "how much can this thing take?" — increment methodically, document failure modes, don't just run it once and call it "stress tested."
- Applied and foundational research form a loop, not a pipeline — applied results that reveal unexpected behavior should route back to foundational research to explain the underlying phenomenon.
- The "my solution is 12% faster" paper is an applied descriptive study with an implied hypothesis and no experimental control — it's valid as a descriptive contribution, not as causal science.

## Anti-patterns
- **"My security widget is 12% faster" as a scientific claim**: This is an applied descriptive study at best; without controlled comparison and standardized metrics, the 12% figure is meaningless across contexts.
- **Confusing applied observational with foundational observational**: Introducing a specific change makes it applied; studying the system as-is makes it foundational. Mixing these produces uninterpretable results.
- **Stress testing without incrementing**: Running a single maximum-load test without incrementally increasing load misses the failure threshold and provides no curve characterization.
- **Applied study without a stated performance expectation**: Applied study requires an expectation or prediction — without it, you're just observing (foundational), not evaluating performance against a standard.
- **Skipping applied study before deployment**: Deploying a security tool without operational bounds testing means discovering its limits in production under real attacks.

## Reference Tables

| Applied Study Type | What it Evaluates | Example |
|---|---|---|
| Applied Exploratory (Stress) | Maximum capability; breaking point | How many concurrent connections can the IDS process before dropping packets? |
| Applied Exploratory (Load) | Behavior at maximum expected load | Does the IDS maintain <1ms latency at 10 Gbps link speed? |
| Applied Exploratory (Performance) | Conformance to specs under normal conditions | Does the IDS detection rate exceed 95% at standard enterprise traffic volume? |
| Applied Descriptive | Implementation and observed behavior of a solution | Documenting deployment of zero-trust architecture at a hospital and observing lateral movement reduction |

| Study Type | Introduces Change? | Has Performance Expectation? | Research Goal |
|---|---|---|---|
| Foundational Exploratory (Ch 4) | No | No | Understand natural system behavior |
| Foundational Descriptive (Ch 5) | No | No | Understand specific case's behavior |
| Applied Exploratory (Ch 12) | Yes | Yes | Find capability envelope |
| Applied Descriptive (Ch 12) | Yes | Yes | Document performance in context |
| Applied Experimental (Ch 11) | Yes | Yes | Controlled performance comparison |

## Worked Example
**Operational Bounds Testing of a New Anomaly-Based IDS:**

A team deploys a new IDS and wants to characterize its operational limits before production.

**Stress testing** (find breaking point):
- Generate synthetic TCP connections between two network probes
- Increment by 1,000 connections per step
- Monitor: packet processing rate, detection latency, dropped packets
- Result: IDS maintains real-time processing up to 85,000 simultaneous connections; above that, detection latency exceeds 500ms and false negatives spike → this is the stress limit

**Load testing** (maximum expected operational load):
- Production network has ~40,000 peak concurrent connections
- Run the IDS at 40,000 connections for 72 hours
- Monitor: sustained detection rate, memory utilization, CPU usage
- Result: 99.1% detection rate sustained; CPU at 73% sustained → acceptable for deployment

**Performance testing** (spec conformance):
- Spec: detection rate ≥ 95% against known attack signature set
- Run full benchmark attack set
- Result: 96.4% detection rate → meets spec

**Applied descriptive contribution**: Document the full operational bounds; publish with the limits clearly stated so operators know not to deploy this IDS on links exceeding 85,000 concurrent connections.

## Key Takeaways
1. Applied observational study is the most common cyber security research type — recognize it and design it rigorously rather than treating it as a "lesser" research form.
2. The key distinction from foundational study is the researcher introducing a specific change and having a performance expectation to evaluate.
3. Always run all three bounds tests before deployment: stress (find limits), load (confirm production viability), performance (verify spec compliance).
4. Applied results that reveal unexpected behavior should route back to basic science — the loop is iterative, not linear.
5. "12% faster" claims require a stated baseline, a defined metric, and controlled conditions to be scientifically meaningful.

## Connects To
- **Ch 4–5**: Foundational Exploratory and Descriptive studies — this chapter adapts those methods for applied contexts
- **Ch 11**: Applied Experimentation — the more controlled complement with stricter experimental design
- **Ch 9**: Hypothetico-deductive — applied study results may generate hypotheses for basic experiments
- **Ch 13**: Instrumentation — testbeds and monitoring infrastructure enable operational bounds testing
