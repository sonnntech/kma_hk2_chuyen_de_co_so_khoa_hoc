# Chapter 15: Scientific Ethics

## Core Idea
All research has a cost — financial, time, or human harm — and cyber security research is ethically distinct because the subject of study (cyber space) is where users live their digital lives. Research ethics define which costs are justifiable; cyber security adds unique grey areas that other fields have not had to resolve.

## Frameworks Introduced

- **Two Competing Ethical Philosophies**:
  1. **Common Good (Utilitarian)**: Collective benefit outweighs individual cost; some individuals can be harmed if total benefit is greater. Current scientific ethics lean AGAINST this for human subjects research.
  2. **Individual Rights**: No research subject may be harmed even if the collective benefit would be significant. **Current scientific research ethics strongly favor this framework.**
  - When to use: When evaluating whether a research design is ethically justifiable; default to individual rights unless a compelling case for common good can be made AND proper authorization obtained.

- **Responsible Disclosure Protocol**: The community-accepted standard for vulnerability disclosure:
  1. Privately disclose the vulnerability to the vendor
  2. Allow 6 months for the vendor to produce a fix with adequate evidence of progress
  3. If no fix after 6 months → publish the vulnerability publicly (full disclosure)
  - When to use: Any time a research activity discovers a vulnerability in a product or system. Do NOT immediately publish; do NOT indefinitely withhold.
  - Rationale: Pure non-disclosure protects vendors who don't fix vulnerabilities; pure full-disclosure exposes users before patches exist; responsible disclosure balances both.

- **Ethical Grey Areas in Cyber Security Research** (community decisions and ongoing debates):
  1. **Antiworm / Automated Patching**: Deploying patches like malware to fix vulnerable systems → **Not ethical** (community consensus); organizations must control their own patch processes
  2. **Attack-back / Botnet Sinkholing**: Taking over C2 infrastructure to neutralize botnets involving victim machines → **Grey area; requires legal authorization**
  3. **Unauthorized system access**: Accessing systems without authorization even for research → **Not ethical** (and illegal in most jurisdictions)
  4. **Ill-gotten datasets**: Using illegally obtained data (e.g., released breach datasets) → **Debated; currently acceptable if common good benefit case is made for already-released data**
  5. **Privacy/Anonymization**: Releasing research datasets that are "sufficiently anonymized" → **Ongoing debate**; re-identification attacks show anonymization is harder than assumed
  6. **EULA/TOS violations**: Breaking terms of service for reverse engineering or web scraping in research → **Grey area; fair use applies in some cases**
  7. **Vulnerability disclosure**: Covered in Responsible Disclosure Protocol above

## Key Concepts
- **Scientific Ethics** — accepted guidelines on justifiable research actions and intolerable behaviors; specific to each research community; enforced via publication standards
- **Morality** — individual-level principles of right and wrong; basis for ethics
- **Ethics** — study and application of morality at group/societal scale; defines community-acceptable behavior
- **Common Good Philosophy** — collective benefit justifies individual cost; utilitarian framework
- **Individual Rights Philosophy** — individual interests override collective benefit; current default for human subjects research
- **Responsible Disclosure** — structured vulnerability notification process: private → 6 months → public
- **Full Disclosure** — immediate public release of vulnerability details
- **Unauthorized Access** — accessing systems without permission; unethical AND illegal under computer fraud laws in most jurisdictions
- **Ill-gotten Goods / Datasets** — data obtained through illegal means; use in research is debated; current guidance is "only if already released and common good benefit is clear"
- **Privacy** — still definition-contested in cyber context; research datasets must be assessed for re-identification risk, not just surface anonymization
- **Antiworm** — automated patch deployment using malware-like distribution; considered unethical; organizations own their patch decisions
- **All-Hazards** — all sources of harm; used in risk-based security planning (distinct from threat-focused research ethics)

## Mental Models
- Ethics is the "cost-benefit analysis of harm vs. knowledge" — before any research design is finalized, ask: "Who bears the cost of this research?" and "Is the knowledge gain proportionate to that cost?"
- Default to individual rights — if you're unsure whether a research action is ethical, ask: "Would this be acceptable if the subject knew exactly what I was doing?" If no → don't proceed without ethics review.
- Responsible disclosure is NOT optional — it is the community's agreed standard; departing from it in either direction (no disclosure OR immediate full disclosure) damages the research community's relationship with vendors and users.
- "Grey area" ≠ "no answer" — for most of the contested issues, the community has a leaning position; know the leaning before you act and document your reasoning.
- Re-identification attacks on "anonymized" data have happened repeatedly — treat privacy/anonymization claims as hypotheses requiring verification, not facts.

## Anti-patterns
- **Publishing vulnerabilities immediately without vendor notification**: Exposes users before patches are available; violates responsible disclosure; burns bridges with vendors.
- **Assuming "anonymized" data is safe to release**: Multiple major research datasets believed to be anonymized have been re-identified; validate anonymization rigorously, especially for cyber/network data.
- **Using unauthorized access for "benign" research purposes**: Unauthorized access is both unethical and criminal regardless of intent.
- **Treating EULA violations as ethically neutral**: Terms of service restrict specific research activities; document and justify any necessary TOS violations before conducting the research.
- **Applying "common good" to justify harming research subjects**: Current scientific ethics in cyber security strongly favor individual rights; the common good argument is not a free pass.
- **Deploying antiworms or automated patches without authorization**: Even if the intent is protective, the community has decided this violates organizations' right to control their own systems.

## Reference Tables

| Ethical Issue | Current Community Position | Open/Decided |
|---|---|---|
| Antiworm deployment | Not ethical | Decided |
| Attack-back / sinkholing | Grey; requires legal authorization | Mostly decided |
| Unauthorized system access | Not ethical; also illegal | Decided |
| Ill-gotten datasets (already released) | Acceptable if common good benefit clear | Debated |
| Privacy / anonymization | Case-by-case; re-ID risk must be evaluated | Ongoing |
| EULA/TOS violations for research | Grey; fair use applies in some cases | Debated |
| Vulnerability disclosure | Responsible disclosure (private → 6 months → public) | Mostly decided |

| Disclosure Approach | Timing | Risk |
|---|---|---|
| No disclosure / Coordinated only | Indefinite delay | Vendors who don't fix leave users exposed indefinitely |
| Responsible disclosure | Private → 6 months → public | Balanced; current best practice |
| Full disclosure (immediate public) | Immediate | Exposes users before patches exist; may assist attackers |

## Worked Example
**Responsible Disclosure of a Critical ICS Vulnerability:**

A researcher discovers a buffer overflow in a widely deployed SCADA historian (used in power plants) that allows unauthenticated remote code execution.

**Ethical decision process**:
1. Individual rights vs. common good: Direct public disclosure puts critical infrastructure users at risk immediately (common good argument fails here — victims bear the cost); choose responsible disclosure.
2. **Day 0**: Contact vendor CERT; provide technical details, proof-of-concept code, affected versions. Request NDA to allow coordinated patching.
3. **Day 30**: Vendor acknowledges receipt; confirms vulnerability; commits to patch timeline of 90 days.
4. **Day 90**: Vendor releases patch. Researcher confirms patch validity.
5. **Day 95**: Joint publication: researcher publishes technical details; vendor publishes patch and advisory simultaneously. ICS-CERT notified before joint publication.

**What would have been unethical**:
- Immediate full disclosure on Day 0 → power plants would be exposed for 90+ days with no defense
- No disclosure → researcher at a different org independently finds it 6 months later; vendor has no incentive to prioritize the fix

## Key Takeaways
1. Default to individual rights as the ethical baseline for cyber security research — the common good argument rarely justifies harming research subjects or users.
2. Responsible disclosure is the community standard: private disclosure → 6 months → public; departing from it in either direction is harmful.
3. "Anonymized" data is not safe until verified against re-identification attacks; treat anonymization as a hypothesis requiring testing.
4. Unauthorized access to systems is both unethical and illegal regardless of research intent — always obtain explicit written authorization before accessing systems you don't own.
5. Grey areas (ill-gotten data, EULA violations, attack-back) require documented reasoning and often legal advice before proceeding.

## Connects To
- **Ch 2**: CIA triad — availability and privacy are ethical considerations as much as security properties
- **Ch 9**: Hypothetico-deductive — experiment design must include ethics review, especially for human subjects (IRB in US context)
- **Ch 10**: Quasi-experimental — threat research populations (studying real attackers) raise immediate ethical issues around authorization
- **Ch 14**: Adversarial Research — attack-back and botnet sinkholing are both in Ch 14's scope and Ch 15's ethical grey area simultaneously
