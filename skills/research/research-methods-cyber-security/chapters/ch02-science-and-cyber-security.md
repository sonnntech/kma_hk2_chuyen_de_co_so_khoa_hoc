# Chapter 2: Science and Cyber Security

## Core Idea
Cyber security is a young, rapidly evolving field that lacks a unifying scientific foundation. This chapter defines what cyber space and cyber security actually are, establishes core security attributes, and introduces the research sub-fields — giving researchers a precise vocabulary before diving into methods.

## Frameworks Introduced

- **Cybernetic Perspective of Cyber Space**: Cyber space = data + technology + humans. The human is as much a driver of cyber system dynamics as the hardware. Security models that ignore the human factor are incomplete.
  - When to use: Scoping a research problem — always check if the human-behavioral dimension needs to be included.
  - How: Ask "does this threat or vulnerability exist without a human acting on or in the system?" If no, include the human layer in your model.

- **CIA Triad + Extensions**: The foundational attributes of a secure system. Original: Confidentiality, Integrity, Availability. Extended with: Authenticity, Nonrepudiation.
  - When to use: Defining security requirements or classifying the security impact of a vulnerability.
  - How: Map each requirement to one or more attributes; identify which attribute a given attack targets. Note: these attributes are *desirable* properties, not measurable quantities — the field still lacks quantitative measures.

- **Analogy as a Dangerous Tool**: Analogies to physical security or other fields are useful for explaining concepts but fail at the detailed level. Research programs built on analogies without empirical validation waste effort.
  - When to use: When borrowing a framework from another field.
  - How: Use analogies only for high-level conceptual orientation. Before treating the analogy as a research basis, verify it holds empirically at the level of detail needed.

## Key Concepts
- **Cyber Space** — the metaphysical construct created by the confluence of digital hardware, data, and humans who interact with both (cybernetic perspective)
- **Cyber Security** — measures and actions to prevent unauthorized access to, manipulation of, or destruction of cyber resources and data; always conditional and limited, never absolute
- **Confidentiality** — prevents unauthorized access to data (access control, encryption)
- **Integrity** — ensures data is only modified by authorized parties; critical when data passes through shared channels
- **Availability** — resources/information accessible in a timely, reliable manner; balances restriction against utility
- **Authenticity** — assurance that parties in an exchange are who they claim to be; applies to actors, actions, and data
- **Nonrepudiation** — attributability of actions to actors via auditable logging; prevents refutation of performed activities
- **Vulnerability** — weakness in design, configuration, or process that opens a system to exploitation
- **Exploit** — realized technique that takes advantage of a vulnerability to breach security
- **Threat** — deliberate source of potential damage; requires both intent and capability
- **Threat Actor** — individual, group, organization, or government with intent to cause harm
- **Information Assurance (IA)** — broader than cyber security: protects information in transit, at rest, and in non-digital forms; adds business continuity emphasis

## Mental Models
- Think of security as a triple-AND gate: Confidentiality AND Integrity AND Availability must all hold — defeating any one breaks the system's security posture.
- Use the cybernetic model to frame research: "data problem, technology problem, or human problem?" — most hard cyber security problems are all three simultaneously.
- Treat claims of "secure" or "protected" as red flags: security is always bounded by scope (secure from what, for whom, under what conditions).
- Analogies to physical security work at the concept level; verify at the mechanism level before using them to design experiments.

## Anti-patterns
- **Treating "secure" as an absolute property**: security is always conditional; undefined scope makes security claims unfalsifiable.
- **Building research programs on untested analogies**: analogies break down at the detail level; empirically validate before extending the analogy to research.
- **Ignoring nonrepudiation / logging in system design**: security attributes can only be demonstrated if there is auditable evidence — missing logs undermine all other attributes.
- **Conflating computer security / network security / IA**: each has distinct scope; using terms interchangeably obscures what is actually being secured.
- **Fixating only on software/hardware vulnerabilities**: users, policies, and data artifacts also introduce vulnerabilities.

## Reference Tables

| Attribute | What it Protects | Broken When... |
|---|---|---|
| Confidentiality | Data privacy | Unauthorized party can read data |
| Integrity | Data accuracy | Unauthorized party can modify data |
| Availability | System usability | Legitimate users cannot access resources |
| Authenticity | Identity assurance | Impersonation succeeds |
| Nonrepudiation | Accountability | Actor can deny their actions; no audit trail |

| Cyber Space Perspective | What it Includes | Field of Origin |
|---|---|---|
| Data | Information encoding and transmission | Information Theory / IA |
| Technology | Hardware, software, networks | 1990s Internet era |
| Cybernetic (preferred) | Data + Technology + Humans | Modern security science |

## Worked Example
**Scoping a Security Research Question Using CIA + Human Layer:**
A researcher wants to study phishing attacks. Using only the technology perspective, the problem is "email filtering." Using the cybernetic perspective, the system is "email filtering + user cognition + organizational policy." The research question becomes: "Under what conditions does user training reduce click-through rates more effectively than filtering?" This is now testable, measurable, and scoped to a bounded set of attributes (Confidentiality broken by social engineering; Authenticity assumption exploited). The cybernetic framing reveals two study arms that the technology-only framing missed entirely.

## Key Takeaways
1. Cyber security is never absolute — always define "secure from what, for whom, under what conditions" before designing a study.
2. The cybernetic view of cyber space (data + technology + humans) is the most complete; ignore the human layer and your model will miss the most common attack vectors.
3. The CIA triad plus Authenticity and Nonrepudiation are the definitional attributes of security — use them to classify both requirements and attack impacts.
4. The field lacks quantitative measures of security attributes; this is a core research gap and opportunity.
5. Use analogies to other fields for orientation, never as research foundations — verify empirically before extending.

## Connects To
- **Ch 1**: Applies the "observational science" framing to the specific domain of cyber security
- **Ch 3**: CIA triad attributes become criteria for selecting appropriate research methods
- **Ch 14**: Deep dive on threat actors and adversarial research
- **CIA Triad**: Standard from NIST SP 800-33 and ISO 27001; extended attributes align with NIST SP 800-53
