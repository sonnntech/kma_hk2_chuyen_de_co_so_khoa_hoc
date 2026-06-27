# Glossary — Research Methods for Cyber Security

**All-Hazards** — all possible sources of harm including deliberate threats, accidents, environmental events, and faults; used in risk-based security planning; broader than threat-only framing (Ch 14, Ch 15)

**Anomaly Detection** — ML problem type; learns a model of "normal" behavior; flags statistical deviations as potentially malicious (Ch 6)

**Applied Research** — quantifies how well scientific knowledge was applied to solve a real-world problem; validates that "the right system was built" (Ch 11, Ch 12)

**Authenticity** — security attribute ensuring parties in an exchange are who they claim; applies to actors, actions, and data (Ch 2)

**Availability** — security attribute ensuring resources/information are accessible in a timely, reliable manner; balances restriction against utility (Ch 2)

**Axiomatic Statement** — a concept taken as true; analogous to explicit assumptions in experimental and observational research (Ch 7)

**Bayesian Network (BN)** — probabilistic directed acyclic graph representing dependencies among random variables; enables inference of unobserved factors; updates dynamically as new data arrives (Ch 6)

**Benchmark** — a standard set of data, algorithm, or scenario used to generate comparable performance measurements; the "ruler" for solution comparison (Ch 11)

**Black Hat Cycle** — reactive pattern of vulnerability discovery → defense → next vulnerability, without grounding in underlying scientific understanding; breaks progress (Ch 11)

**Case-Control Study** — retrospective observational study dividing population into case (phenomenon present) and control (absent); examines what differs between groups (Ch 4)

**Case Report** — least rigorous descriptive method; describes a specific incident, solution, or detection method without experimental evaluation; suitable for white papers, not peer review (Ch 5)

**Case Study** — formal in-depth study of a specific event or system; follows structured collection-and-evaluation process; limited generalizability; contributes to systemic knowledge (Ch 5)

**CIA Triad** — foundational security attributes: Confidentiality (unauthorized access prevention), Integrity (unauthorized modification prevention), Availability (reliable access); extended with Authenticity and Nonrepudiation (Ch 2)

**Classification** — ML problem type; assigns new inputs to predefined learned categories (e.g., malware family identification) (Ch 6)

**Clustering** — ML problem type; groups similar inputs without predefined categories; discovers natural groupings in data (Ch 6)

**Cohort Study** — longitudinal study focused on a specific group sharing a common trait, tracked over time (Ch 4)

**Common Good Philosophy** — ethical framework where collective benefit can justify individual cost; NOT the current default in scientific research ethics (Ch 15)

**Confidentiality** — security attribute preventing unauthorized access to data (Ch 2)

**Confounding Variable** — uncontrolled variable that influences the dependent variable and distorts experimental results (Ch 9)

**Continuum of Discovery** — spectrum from simple/controlled experiments (high repeatability, low realism) to operational-scale observations (high realism, low control) (Ch 1)

**Coverage** — degree to which sensors capture all instances of a phenomenon across all relevant system locations (Ch 13)

**Cross-Sectional Study** — "census"; snapshot of a population at a specific point in time; describes prevalence; enables correlation-based inferences (Ch 4)

**Cross-Validation** — process to evaluate ML model generalizability; uses 60/20/20 data split for training/validation/test; never use test set for tuning (Ch 6)

**Cyber Security** — measures and actions to prevent unauthorized access to, manipulation of, or destruction of cyber resources; always conditional and bounded (Ch 2)

**Cyber Space** — the metaphysical construct created by the confluence of digital hardware, data, and the humans who interact with both (cybernetic perspective) (Ch 2)

**Data Fidelity** — accuracy and completeness of collected data; measured across time, sample rate, summarization, proxy, and scale axes (Ch 13)

**Dependent Variable (DV)** — the variable measured in an experiment; the effect (Ch 9)

**Descriptive Study** — in-depth inductive study of a specific case; qualitative; more researcher control than exploratory studies; narrower scope (Ch 5)

**Difference-of-Differences** — quasi-experimental design comparing the change in outcome for treatment vs. control groups before and after an intervention; controls for pre-existing group differences (Ch 10)

**Ecological Study** — observational study examining the entire population at geographic or temporal level; assesses risk factors at population scale; often uses secondary data (Ch 4)

**Elicitation Study** — gathers information from human subjects via surveys or interviews; used when direct measurement is impossible or expert judgment is required (Ch 5)

**Emulation** — simulation of inner workings of a system to produce realistic output; higher fidelity than plain simulation; more computationally expensive (Ch 8)

**Exploit** — a realized technique that takes advantage of a vulnerability to breach security (Ch 2)

**Exploratory Study** — inductive observational study; broad scope; collects and analyzes observations to discover patterns and generate theory; also called "correlative" (Ch 4)

**Falsifiability** — the property of a hypothesis that it CAN be disproven by observation; the defining feature of scientific claims (Popper) (Ch 9)

**Formal Theory** — mathematical representation of system behavior using formal proofs, theorems, and lemmas; basis of cryptography, access control models, formal methods (Ch 7)

**Full Disclosure** — immediate public release of vulnerability details without vendor notification; current practice considers this irresponsible (Ch 15)

**Full Packet Capture (PCAP)** — captures complete network packets including headers and payload; highest fidelity network data source; high storage cost (Ch 13)

**Full Virtualization** — complete hardware emulation enabling guest OS to run unmodified; highest fidelity virtualization (Ch 8)

**Hazard** — any source of potential harm, including non-deliberate sources (accidents, environmental events, faults); distinguished from threat (Ch 14)

**Hidden Markov Model (HMM)** — probabilistic sequence model for systems with hidden states; widely used for cyber behavior modeling and multi-stage attack pattern recognition (Ch 6)

**Hierarchy of Evidence** — ranked ordering of research method types by strength of evidence: 1) Systematic reviews of RCTs → 7) Case reports (Greenhalgh, adapted for cyber) (Ch 1)

**Hypothesis** — a falsifiable, testable prediction of how a system will behave under clearly defined conditions; must be observable, testable, clearly defined, single-concept, and predictive (Ch 9)

**Independent Variable (IV)** — the variable manipulated in an experiment; the cause (Ch 9)

**Individual Rights Philosophy** — ethical framework where individual interests override collective benefit; current default for scientific research ethics (Ch 15)

**Inductive Reasoning** — inferring general theory from specific observations; inherently uncertain; basis of observational research (Ch 4)

**Insider Threat** — a threat residing within the organization with legitimate (possibly privileged) access (Ch 14)

**Instrumentation** — the tools, sensors, and processes used to collect research data (Ch 13)

**Integrity** — security attribute ensuring data is only modified by authorized parties (Ch 2)

**Internal Validity** — degree to which observed effects are caused by the independent variable vs. uncontrolled confounders; primary risk in quasi-experiments (Ch 10)

**Law (Science)** — a theory with significant empirical support that is widely accepted as accurate; subject to revision with new evidence (Ch 7)

**Lemma** — an intermediate step or component in a larger theoretical proof (Ch 7)

**Literature Survey** — systematic review of existing published research; conducted before any research method is executed; sharpens questions and prevents duplication (Ch 3)

**Load Testing** — operational bounds test evaluating system behavior at maximum expected operational load (Ch 12)

**Longitudinal Study** — sequential observation of a system or behavior over extended time; captures full lifecycle and evolution (Ch 4)

**Machine Learning** — computational process to discover behavioral models from empirical data; falls within observational research category (Ch 6)

**Model Validation** — process of verifying that a simulation model's outputs match real-world observations within acceptable bounds (Ch 8)

**NetFlow / IPFIX** — flow-level network data summaries; captures communication metadata (IPs, ports, bytes, duration); loses payload content (Ch 13)

**Nonrepudiation** — security attribute enabling attribution of actions to actors via auditable logging; prevents denial of activity (Ch 2)

**Null Hypothesis** — the default assumption that there is no effect; the experiment attempts to reject it (Ch 9)

**Observational Research** — no independent variable controlled; researcher observes dependent variables in natural or operational settings; broader than experimental research (Ch 3, Ch 4)

**Operational Bounds Testing** — systematic exploration of system behavior limits via stress, load, and performance testing (Ch 12)

**Overfitting (Variance)** — ML model fits training data but fails to generalize to new data; fix by reducing features or regularization (Ch 6)

**Paravirtualization** — hardware virtualization via API; requires guest OS modification; intermediate fidelity (Ch 8)

**Performance Testing** — operational bounds test evaluating conformance to defined performance requirements under normal conditions (Ch 12)

**Principal Investigator (PI)** — lead researcher responsible for designing and conducting the study (Ch 3)

**Privacy** — still definition-contested in cyber context; research datasets must be assessed for re-identification risk beyond surface anonymization (Ch 15)

**Proxy Measurement** — indirect observation of an unmeasurable phenomenon; must capture the right abstraction level (Ch 13)

**Quasi-experiment** — experiment where one or more independent variables are not fully controlled; produces weaker evidence than true experiments; often the only viable option in cyber security research (Ch 10)

**Red Team** — professional penetration testers used as threat actor proxies in research; small population, high cost, limited generalizability (Ch 10, Ch 14)

**Regression** — ML problem type; predicts continuous output values (Ch 6)

**Replication** — independent reproduction of an experiment by a different researcher; essential for scientific validity (Ch 9)

**Responsible Disclosure** — vulnerability disclosure protocol: private vendor notification → 6 months → public disclosure if unpatched; current community standard (Ch 15)

**Sample Rate** — frequency of data collection; full capture vs. filtered, truncated, or downsampled (Ch 13)

**Secondary Data** — data collected for one purpose and repurposed for a research study; validate collection conditions before use (Ch 4)

**Semi-supervised Learning** — ML learning style using partially labeled data; hybrid of supervised and unsupervised (Ch 6)

**Simulation** — computer process imitating a cyber or physical process by generating similar responses; creates data mimicking real system behavior (Ch 8)

**Stress Testing** — operational bounds test pushing the system beyond expected extremes to find the breaking point (Ch 12)

**Supervised Learning** — ML learning style using labeled training data; requires ground truth; produces classifiers and regressors (Ch 6)

**Testbed** — controlled cyber environment replicating operational conditions at reduced scale; primary tool for experimental cyber security research (Ch 13)

**Theory** — interrelated concepts, definitions, and propositions explaining, predicting, and modeling relationships; NOT a guess; requires empirical support to be distinguished from a formal model (Ch 7)

**Theorem** — a statement proven true in mathematical/deductive contexts (Ch 7)

**Threat** — a person or group with both intent AND capability to cause deliberate harm; NOT accidents, faults, or environmental events (Ch 2, Ch 14)

**Threat Actor** — an individual, group, organization, or government with intent to cause harm in cyber space (Ch 2, Ch 14)

**Time Fidelity** — accuracy/precision of sensor timestamps; determines event ordering resolution; critical for causal analysis (Ch 13)

**TTP (Tactics, Techniques, and Procedures)** — how an adversary operates; their behavioral signature or modus operandi; can be faked; not sufficient alone for attribution (Ch 14)

**Underfitting (Bias)** — ML model has high training error; fix by adding features or polynomial terms (Ch 6)

**Unsupervised Learning** — ML learning style using unlabeled data; discovers structure without predefined categories (Ch 6)

**Validation Testing** — applied experimental method; evaluates a solution in controlled but realistically varied conditions; similar to H-D experiments but applied to existing systems (Ch 11)

**Virtualization** — emulation of the relevant subset of a computer enabling OS and application software to run; types: containerization, paravirtualization, full virtualization (Ch 8)

**Vulnerability** — a weakness in design, configuration, or process that makes a system susceptible to exploitation (Ch 2)
