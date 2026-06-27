# Chapter 14: Addressing the Adversary

## Core Idea
Cyber security is fundamentally adversarial — unlike any other field of science, your subject of study actively hides, adapts, and may counterstrike. Research that ignores the adversary produces defenses that work in labs but fail against real threats. This chapter provides a framework for modeling, studying, and incorporating adversaries into research designs.

## Frameworks Introduced

- **DoD Adversary Tier Model** (Defense Science Board, 6 tiers):
  - **Tier I–II**: Script kiddies; use off-the-shelf vulnerabilities and tools
  - **Tier III–IV**: More capable; discover new vulnerabilities; greater resources
  - **Tier V–VI**: Nation-state level; billions of dollars; years to develop; supply chain access, hardware tampering, on-premise attacks
  - When to use: When designing threat models for research — match the adversary tier to the threat model to avoid under- or over-specifying attacker capability.
  - Caution: Tool sharing means lower-tier adversaries increasingly wield higher-tier tools (commoditized exploits); capability tiers are no longer as clean as they appear.

- **Threat Modeling for Research**: A formal representation of a specific adversary for experimental design. Three modeling dimensions:
  1. **Capability** — resources, money, time, training, tools; cyber space is a "great equalizer" because exploits developed by Tier V can be purchased and used by Tier II
  2. **Intent** — motivation and objectives: criminal, hacktivist, insider, nation-state, etc. More useful than capability tiers now that tools are commoditized
  3. **TTP (Tactics, Techniques, and Procedures)** — how the adversary operates; their modus operandi; tradecraft term from military; note: TTP can be faked and should not be used as sole identity attribution
  - When to use: Before designing any experiment involving adversarial behavior; explicitly state your threat model so readers can calibrate the scope of your findings.

- **Threat Equation**: Threat = Intent × Capability. Simple model for abstract threat assessment. Useful at conceptual level; over-simplifies complex adversarial dynamics at detailed level.

- **All-Hazards vs. Threat Focus**: 
  - **All-Hazards**: All sources of harm (deliberate threats + accidents + environmental + faults); used in risk management and emergency planning
  - **Threat**: Only deliberate, malicious adversaries with intent and capability
  - When to use: Use All-Hazards for organizational risk planning; use Threat-only framing for adversarial research. Mixing the two dilutes defensive focus.

## Key Concepts
- **Adversary** — a collection or group of threats; the entity against which security is designed (e.g., hacker collective, nation state)
- **Threat / Threat Actor** — a specific source of deliberate harm; person with capability AND intent; NOT accidents, environmental events, or faults
- **Intent** — motivation and objectives of the adversary; degrees (purposely, knowingly, recklessly, negligently) from Model Penal Code
- **Capability** — resources, means, training, tools available to the threat
- **TTP (Tactics, Techniques, and Procedures)** — how an adversary operates; their behavioral signature; can be faked
- **Insider Threat** — threat residing within the organization with legitimate (possibly privileged) access
- **All-Hazards** — all possible sources of harm including threats, accidents, environmental events; used in risk-based security planning
- **Red Team** — professional pen-testers used as threat proxies in research; legitimate participant in controlled experiments
- **Threat Model** — formal representation of a specific adversary for research or operational use; includes capability, intent, and TTP dimensions
- **Attribution** — identifying the specific threat actor responsible for an attack; inherently difficult in cyber space; TTP alone is insufficient

## Mental Models
- Think of adversaries as a variable in your experiment, not just context — if your research involves "attacker behavior," you need a formal threat model the same way you need a formal specification of every other variable.
- Capability tiers are not stable — a Tier V adversary's exploits can become Tier II tools in 12 months through dark web markets. Model intent, not just capability.
- Red teams are NOT equivalent to real adversaries — they have time constraints, legal constraints, and professional motivation mismatches. Explicitly state when you're using a red team proxy and what aspects of real adversarial behavior they may not capture.
- "Threat = Intent × Capability" is useful as a REMINDER that both must be present; it is NOT a formula for scoring threat level.
- Attribution is a conclusion, not a data point — TTP-based attribution is probabilistic and can be spoofed; always qualify attribution claims.

## Anti-patterns
- **Designing defenses against vulnerabilities without threat models**: Building a stronger lock without knowing whether the adversary picks locks or breaks windows — wastes resources on the wrong control.
- **Conflating threat with hazard**: Treating server room flooding as a "threat" muddies threat-focused defensive design; separate the two conceptually.
- **Assuming capability tiers map cleanly to tool sophistication**: A "script kiddie" deploying a nation-state-developed exploit kit is a Tier I intent actor with Tier V tools — capability-tier models underestimate this.
- **Using TTP as sole attribution evidence**: TTP can be deliberately faked (false flag operations); it is a probabilistic indicator, not proof.
- **Running red team experiments as if they're equivalent to real attacker data**: Red teams work to a schedule, avoid permanent damage, and operate within legal constraints; real adversaries do none of these.
- **Studying cyber threats without adversarial perspective**: Security research that doesn't model attacker decision-making produces defenses that work against the attacker you imagined, not the one you'll face.

## Reference Tables

| Adversary Taxonomy Dimension | Categories | Research Use |
|---|---|---|
| Intent | Criminal, Hacktivist, Insider, Nation-state, Opportunistic | Scope threat model; guide data collection on motivation |
| Capability | Tier I–VI (DoD); script-kiddie → nation-state | Set experimental attacker capability parameters |
| TTP | Tactics, Techniques, Procedures | Model attacker behavior in experiments; compare to kill chain |

| Term | Definition | NOT |
|---|---|---|
| Threat | Person with intent + capability to cause deliberate harm | Accidents, faults, environmental events |
| Adversary | Group or collection of threats | Individual specific actor |
| Hazard | Any source of harm (including non-deliberate) | Purely deliberate threats |
| Vulnerability | Weakness exploitable by threat | The exploit itself |
| Exploit | Realized technique to leverage a vulnerability | A vulnerability without a technique |

## Worked Example
**Threat Model for a Ransomware Experiment:**

A researcher wants to test whether a behavioral anomaly detection system (BADS) can detect ransomware encryption activity before 10% of files are encrypted.

**Threat model specification**:
- **Tier**: III–IV (uses known ransomware families; has capability to modify obfuscation to evade signature detection; not nation-state)
- **Intent**: Criminal — financial extortion; will avoid noisy behavior that triggers alerts; will prioritize high-value files
- **TTP**: 
  - Tactics: Establish foothold → elevate privilege → disable backups → encrypt files → drop ransom note
  - Techniques: WMI execution, VSS deletion (vssadmin), SMB lateral movement, AES file encryption
  - Procedures: Encrypt user documents before system files; target file extensions (.docx, .xlsx, .pdf first)
- **Red team proxy**: Use a researcher-controlled ransomware simulator that implements the above TTPs without network propagation
- **Limitations stated**: Red team operates without time pressure; real ransomware actors may encrypt faster under detection risk; results may underestimate attacker speed

## Key Takeaways
1. Always specify a formal threat model (capability + intent + TTP) before designing any adversarial experiment — it scopes your conclusions.
2. Use intent to categorize adversaries, not just capability — tools are commoditized; intent is more stable and useful for defensive design.
3. Red teams are necessary proxies but introduce biases (time constraints, legal constraints, professional motivation) — state these limitations explicitly.
4. Attribution from TTP alone is probabilistic and can be faked — qualify attribution claims accordingly.
5. Security research that doesn't model attacker decision-making will generate defenses that only work against the attacker you imagined.

## Connects To
- **Ch 2**: CIA triad and threat fundamentals — this chapter deepens the adversary/threat taxonomy introduced there
- **Ch 9**: Hypothetico-deductive — red teams provide the adversarial IV in controlled experiments
- **Ch 10**: Quasi-experimental — threat population limitations (small, adversarial to research) drive quasi-experimental designs
- **Ch 5**: Descriptive Study (case study) — APT group analysis is a primary application of threat actor case studies
