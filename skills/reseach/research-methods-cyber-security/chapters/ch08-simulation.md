# Chapter 8: Using Simulation for Research

## Core Idea
Simulation is a bridge between theory and experiment — it lets you explore theoretical models computationally, generate hypotheses for real experiments, and study systems that are too complex, expensive, or dangerous to experiment on directly. Its value is proportional to the fidelity and validity of the underlying model.

## Frameworks Introduced

- **Simulation Fidelity Hierarchy**: From lowest to highest fidelity:
  1. **Simulation** — black box; produces realistic-looking output without modeling internals
  2. **Emulation** — models inner workings to produce realistic output; higher fidelity, more computational cost
  3. **Virtualization** — emulation of a computer subset; types in increasing fidelity: Containerization → Paravirtualization → Full Virtualization
  - When to use: Match fidelity to research question. Full virtualization when you need guest OS behavior. Containers when you need application isolation with lower overhead. Plain simulation when output realism matters more than internal accuracy.

- **Three Use Cases for Simulation**:
  1. **Theoretical Simulation** — explore boundary conditions of a theory; understand behavior at extremes before committing to real experiments; does NOT prove/disprove the theory, just instantiates it
  2. **Decision Support Simulation** — "what-if" scenarios for systems that cannot be experimentally controlled (e.g., power grid attacks, pandemic-level malware propagation)
  3. **Empirical Simulation** — use simulation output as hypotheses for real experiments; if the controlled experiment matches simulation output, it is evidence for the theoretical model's accuracy
  - When to use: Select use case first. If you're exploring a new theory → Theoretical. If you need operational "what-if" answers → Decision Support. If you want to validate a theory via controlled experiment → Empirical.

- **Model Validation Requirement**: A simulation is only as good as the model it instantiates. Model validation must precede using simulation results for research conclusions.
  - When to use: Before using any simulation for decision support or empirical hypothesis generation.
  - How: Compare simulation output to known real-world data; measure divergence; calibrate model parameters; document the bounds within which the model is valid.

## Key Concepts
- **Simulation** — computer process imitating a cyber or physical process by generating similar responses; creates data mimicking real system behavior
- **Emulation** — simulation of inner workings for higher output fidelity; more expensive to build and compute
- **Virtualization** — emulation of the relevant subset of a computer for OS/application-level software to run
- **Containerization** — lightweight virtualization; multiple containers within a single OS namespace
- **Paravirtualization** — hardware virtualization via API; requires guest OS modification
- **Full Virtualization** — full hardware emulation; guest OS runs unmodified; highest fidelity
- **Model Fidelity** — degree to which a simulation model accurately represents the real system
- **Model Validation** — process of verifying that a model's outputs match real-world observations within acceptable bounds
- **Theoretical Simulation** — explores theoretical model behavior; output is not evidence for/against the theory itself
- **Empirical Simulation** — simulation output treated as hypothesis; validated by matching against real experiment data
- **Decision Support** — using simulation to evaluate "what-if" scenarios for operationally uncontrollable systems

## Mental Models
- Think of simulation as a "theory telescope" — you can observe a theory's implications without being able to directly see or control the real system.
- Simulation output ≠ experimental evidence. A simulation that "proves" your theory only shows that your model is internally consistent with your assumptions — you still need a real experiment.
- Mismatch between simulation and experiment can mean: (a) the theory is wrong, OR (b) the simulation implementation introduced errors. Investigate both before discarding the theory.
- Fidelity is a cost-benefit trade-off: higher fidelity requires more complex models and more compute; only pay the cost if your research question requires it.
- Simulation is to experimentation what a map is to territory — useful for navigation, but the map is not the territory.

## Anti-patterns
- **Treating simulation output as experimental evidence**: Simulation explores theoretical models; validating the theory requires a controlled experiment comparing simulation output to real system behavior.
- **Using simulation as the final validation step**: Simulation validates the model, not the theory. The theory is only validated when real-world experimental data matches simulation predictions.
- **Building high-fidelity simulations without model validation**: An accurate simulation of a wrong model produces wrong answers with high confidence.
- **Conflating virtualization fidelity levels**: Running an experiment in containers when the research question requires full OS-level hardware behavior will produce incorrect results.
- **Using simulation for decision support without stating model bounds**: Simulation results are only valid within the parameter ranges the model was validated against; extrapolating beyond those ranges is dangerous.

## Reference Tables

| Simulation Type | Fidelity | Use Case | Compute Cost |
|---|---|---|---|
| Simulation | Low (output only) | Theoretical exploration, decision support | Low |
| Emulation | Medium (internal behavior) | Higher-fidelity behavior modeling | Medium |
| Containerization | Medium | Application isolation, testbed setup | Low-Medium |
| Paravirtualization | High | OS-level behavior requiring hardware abstraction | Medium-High |
| Full Virtualization | Highest | Guest OS unmodified; maximum realism | High |

| Use Case | What it Produces | What it Does NOT Produce |
|---|---|---|
| Theoretical Simulation | Understanding of model behavior at extremes | Evidence for/against the theory |
| Decision Support | Scenario outcome predictions | Proof of real-world behavior |
| Empirical Simulation | Hypotheses for controlled experiments | Experimental evidence |

## Worked Example
**Malware Propagation as Disease: Simulation Before Experiment**

Theory: "Malware spreads through enterprise social networks following the same dynamics as communicable disease (SIR model)."

1. **Theoretical simulation**: Model a 10,000-node enterprise network; assign communication probabilities between nodes; model malware transmission as infection events; simulate with R₀ = 2.5 (reproduction number from flu analogy)
2. **Boundary exploration**: Simulate at 10%, 30%, 50% patch penetration — discover the model predicts that 40% patching achieves "herd immunity" and propagation collapses
3. **Hypothesis generated**: "In a real enterprise network with 40%+ patched hosts, a new worm will self-limit without reaching >10% of unpatched hosts" (empirical simulation use case)
4. **Validation experiment**: Deploy a non-destructive worm marker in a controlled testbed; vary patching rate; compare infection curves to simulation output
5. **Result**: If real experiment matches simulation within ±15%, this is evidence the SIR model is a valid approximation for malware propagation in enterprise environments

## Key Takeaways
1. Simulation is a bridge between theory and experiment — use it to explore theoretical models before committing to expensive real-world experiments.
2. Match fidelity to your research question: containerization for application behavior, full virtualization for OS-level experiments, plain simulation for population dynamics.
3. Always validate the simulation model against known real-world data before using it for decision support or hypothesis generation.
4. Simulation output is a hypothesis, not experimental evidence — validate by running the corresponding real experiment.
5. When simulation and experiment diverge, investigate both the theory AND the simulation implementation before drawing conclusions.

## Connects To
- **Ch 7**: Theoretical Research — simulation is the computational partner to formal theory
- **Ch 9**: Hypothetico-deductive — empirical simulation outputs become experimental hypotheses
- **Ch 6**: Machine Learning — empirical models (from ML) can replace theoretical models in simulation, producing data-driven simulations
- **Ch 13**: Instrumentation — the testbed and data collection infrastructure that makes simulation-to-experiment validation possible
