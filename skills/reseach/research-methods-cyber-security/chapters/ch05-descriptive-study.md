# Chapter 5: Descriptive Study

## Core Idea
Descriptive study is the in-depth, individual-focused counterpart to exploratory study — it examines a specific case, actor, or system thoroughly rather than scanning across a population. It is the right method when you need deep qualitative understanding of a particular instance (e.g., a specific malware strain, threat actor, or policy implementation).

## Frameworks Introduced

- **Three Descriptive Study Methods**:
  1. **Case Study** — formal, structured in-depth study of a specific event or system (e.g., Stuxnet, APT1); NOT anecdotal; follows a collection-and-evaluation process; limited generalizability but contributes to systemic knowledge; appropriate for malware, threat actors, new policy implementations.
  2. **Elicitation Study** — gathers information from human subjects via surveys or interviews; used when models/theories don't yet exist to interpret results, or when expert judgment is required (e.g., risk scoring, scenario probability assessment).
  3. **Case Report** — least rigorous; describes a specific incident, detection method, or new countermeasure without associated performance experiment; appropriate for white papers and non-peer-reviewed publications; **not recommended for scientific publications** because scientific contribution is low.
  - When to use: Case study for deep investigation of a specific cyber event or system. Elicitation for capturing expert or user knowledge that cannot be directly measured. Case report for descriptive write-ups only — extend it with exploratory study or applied experiment before submitting to peer review.
  - How: Case study → define scope, collect all relevant data before treatment/remediation, conduct formal analysis. Elicitation → design survey/interview instrument, identify subject population, analyze qualitatively. Case report → describe the artifact, acknowledge lack of experimental validation explicitly.

- **Data Collection Timing Rule**: In first-hand descriptive data collection, collect ALL relevant data before any intervention (e.g., before wiping/rebuilding a compromised host). Post-intervention data is unavailable or contaminated.
  - When to use: During incident response, malware analysis, or any live system case study.
  - How: Create a data collection checklist before touching the system; include anticipated AND unanticipated data needs; take forensic images and memory dumps proactively.

## Key Concepts
- **Descriptive Study** — in-depth inductive study of a specific case; qualitative; generates insight rather than mathematically quantifiable results; more researcher control than exploratory studies
- **Exploratory vs. Descriptive** — exploratory = broad scope, population-level, retrospective data; descriptive = narrow scope, individual-level, first-hand data collected live or on specific targets
- **Case Study** — formal study of one event or system; contributes to systemic knowledge even if not generalizable; low on Hierarchy of Evidence (rank 7) but high in impact for foundational cases
- **Elicitation Study** — collecting human knowledge; used when direct measurement is impossible (risk, security value, scenario probabilities)
- **Case Report** — descriptive writeup of a new solution or detection method without experimental evaluation; common but scientifically weak
- **Qualitative Results** — informative, not mathematically quantifiable; appropriate for descriptive methods
- **Observer Bias** — distortion introduced by the researcher's presence or perspective during live data collection; must be controlled for
- **First-Hand Data** — data collected directly from the subject during the study; contrasts with secondary data (repurposed from another collection)

## Mental Models
- Think of exploratory vs. descriptive as a microscope dial: exploratory = low magnification, wide field; descriptive = high magnification, single subject.
- The Stuxnet case study is the model: deeply studied, limited in generalizability, but foundational for ICS security as a field. That's the value of a descriptive study.
- Treat "collect everything" as a heuristic, not a strategy — it can mask the failure to think critically about what matters. Know why you're collecting each data type.
- Case reports are appropriate in industry contexts; before submitting to peer review, add one of: exploratory study, applied experiment, or hypothetico-deductive validation.

## Anti-patterns
- **Treating a case study as anecdotal evidence**: A case study following formal collection-and-evaluation is structured research, not an anecdote — but it must be documented as such.
- **Submitting a case report to peer review without experimental validation**: Describing a new tool without testing it makes a weak scientific contribution; extend it with an applied experiment (Ch 11–12).
- **Collecting data after remediation**: Wiping or rebuilding a compromised system before collecting forensic evidence destroys the case study data permanently.
- **Blind "collect everything" without critical analysis**: Can miss that the most important data is in system memory (volatile), not on disk, or that key decision points require immediate attention.
- **Generalizing from a single case study**: One case establishes a pattern candidate, not a rule — requires corroboration from other studies or experimental validation.

## Reference Tables

| Method | Scope | Data Type | Peer Review Suitability | Cyber Security Example |
|---|---|---|---|---|
| Case Study | Single event/system | Qualitative, first-hand | Yes (with rigor) | APT1 group behavior analysis |
| Elicitation Study | Human subject group | Qualitative survey/interview | Yes | Expert risk scoring for SCADA vulnerabilities |
| Case Report | Single solution/detection | Descriptive | No (white paper only) | Write-up of a new firewall configuration approach |

## Worked Example
**Case Study of a Ransomware Incident:**
A researcher studies a single ransomware infection at a hospital (before remediation):
1. **Pre-intervention data collection**: Full disk image, RAM dump, network PCAP from the 72h before detection, AD logs, email gateway logs
2. **Timeline reconstruction**: Phishing email → credential harvesting → lateral movement → data exfiltration → encryption trigger
3. **Analysis**: Identified that encryption was triggered 6 days after initial compromise — extended dwell time that existing alerting missed
4. **Contribution**: Documented a new dwell-time pattern not previously observed in healthcare-specific ransomware → hypothesis candidate: "healthcare ransomware operators use longer dwell periods than financial sector targets" → ready for cross-sectional study (Ch 4) across 20+ cases for validation
5. **Limitation stated**: Single institution, specific ransomware family, results may not generalize

## Key Takeaways
1. Use case study when you need deep qualitative understanding of a specific event; use exploratory study when you need breadth across many instances.
2. Data collection must happen before any remediation or intervention — build a forensic collection checklist before touching a live system.
3. Case reports are appropriate for white papers and industry blogs; extend them with experimental or exploratory validation before peer review submission.
4. Elicitation studies (surveys, expert interviews) are the correct method when the question involves human judgment, expert knowledge, or variables that cannot be directly measured (risk, security value).
5. A rigorous case study (Stuxnet, APT1) can be foundational even if not generalizable — document the formal process to distinguish it from an anecdote.

## Connects To
- **Ch 4**: Exploratory Study — broader scope counterpart; same inductive approach at population level
- **Ch 9**: Hypothetico-deductive — case study findings often generate hypotheses for controlled experiments
- **Ch 11–12**: Applied Experimentation and Applied Observational Study — extend case reports to make them publishable
- **Ch 14**: Research with an Adversary — threat actor case studies are a primary method for adversarial research
- **Hierarchy of Evidence (Ch 1)**: Case studies rank 7 (lowest) but can be highly influential when foundational
