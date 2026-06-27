# Chapter 3: Starting Your Research

## Core Idea
Research doesn't start with a method — it starts with a question. This chapter gives a decision framework for mapping your cyber security research question to the right category of research method, then directing you to the appropriate chapter. Think of it as a "Choose Your Own Adventure" for research design.

## Frameworks Introduced

- **Four Categories of Cyber Security Research**: The book's organizing taxonomy:
  1. **Observational Research** — understand real cyber systems; best for open-ended questions and when controlled experiments are infeasible (sub-methods: Exploratory, Descriptive, Machine Learning)
  2. **Theoretical Research** — logical exploration of system models; best for proving bounds, edge cases, emergent behavior (sub-methods: Formal Theory, Simulation)
  3. **Experimental Research** — controlled testing of hypotheses; best for generating strong causal evidence
  4. **Applied Research** — leverages all the above to assess solutions to real-world problems
  - When to use: As the first decision gate after formulating a research question.
  - How: Answer the branching questions below; the answers route you to one of these four categories.

- **Research Method Decision Tree** (simplified from the book's branching guide):
  - Is your question open-ended or exploratory? → Observational
  - Is your question about how a system *should* work, or can you only study it theoretically? → Theoretical
  - Do you have a specific testable hypothesis and can control variables? → Experimental
  - Are you assessing the effectiveness of an applied solution in a real environment? → Applied
  - When to use: At the start of every research project.
  - How: Write down your research question, then walk the tree. If the answer is ambiguous, break the question into smaller atomic sub-questions first.

- **Hypothesis Definition**: A hypothesis is a *predictive statement* about how a system would behave under certain conditions — it must be answerable (falsifiable with evidence). Distinguish from a research question: a question asks "why"; a hypothesis states "if X then Y."
  - When to use: Before moving into Experimental or Hypothetico-deductive research.
  - How: Restate your research question as a falsifiable prediction. If you can't state it as true/false, it's not yet a hypothesis.

- **Literature Survey as Research Foundation**: Before executing any method, conduct a literature survey to understand what is already known, avoid duplication, and identify gaps.
  - When to use: Immediately after formulating the initial research question.
  - How: Search primary sources (journals, conference proceedings), trace citations, and synthesize what is agreed upon vs. contested. Use the survey to sharpen your research question into an atomic, answerable form.

## Key Concepts
- **Research Question** — the core driver of all scientific process; should be as specific and atomic as possible; can be refined as research proceeds
- **Hypothesis** — predictive, falsifiable statement; requires evidence to confirm or deny; distinguishable from a research question
- **Observational Research** — sensing real-world environments, data mining; best when controlled experiments are infeasible
- **Exploratory Study** — inductive; collects and analyzes observations across a broad system to discover patterns and generate theory
- **Descriptive Study** — focuses in depth on a specific case of a system; narrower scope than exploratory
- **Machine Learning (as research method)** — automates phases of the research cycle; useful when large datasets are available; detects correlations or generates models
- **Theoretical Research** — logical/mathematical exploration; postulates rules and conditions; tests bounds, edge cases, emergent behavior
- **Formal Theory** — mathematical proofs and formal models; basis of cryptography, access control models, formal methods
- **Simulation** — automated sampling of large variable spaces to test theoretical models; used when physical experiments are infeasible or too costly
- **Experimental Research** — controlled testing; all variables known; generates strong causal evidence
- **Applied Research** — assesses effectiveness of solutions in real-world operational environments
- **Literature Survey** — systematic review of existing published research; foundational step before executing any method
- **Principal Investigator (PI)** — lead researcher responsible for designing the study and, often, also leading related engineering work

## Mental Models
- Think of research types as tools in a progression: Observation → Theory → Experiment → Application. Each phase informs the next; skipping phases (especially building applications without theoretical foundations) leads to indeterminate results.
- "If you don't know which method to use, break your question down into smaller atomic pieces first." Smaller questions route more clearly.
- A bad research path with clear documentation is not a failure — it is still science. A bad research path without documentation is a dead end.
- Engineer after you have theoretical or empirical foundations, not before — "engineer first, figure out the theory later" is a common anti-pattern in cyber security.

## Anti-patterns
- **Engineering before theorizing**: Building an intrusion detection system based on assumptions about how cyber space works, then trying to test it, without prior observational or theoretical grounding — produces indeterminate success at best.
- **Overly broad research questions**: "Why is cyber security failing?" is harder to answer than "Does poor user motivation lead to weaker passwords?" Always atomize.
- **Skipping the literature survey**: Reinvents knowledge that already exists; misses adjacent insights that could sharpen the question.
- **Treating the idealized research cycle as reality**: In practice, researchers can start at any phase and loop back unpredictably — design your research plan to accommodate course corrections.
- **Confusing research category superiority**: No category is "better" than another; they are complementary and each is essential at different phases of a research program.

## Worked Example
**Password Strength Research — Decision Tree in Action:**
Initial question: "Why are passwords so weak?"
1. Too broad → atomize → "What impact does poor motivation have on password strength?"
2. Walk the decision tree: question is about human behavior in real systems → no controlled experiment yet → **Observational** category
3. Specific case of a user group → **Descriptive Study** (university students)
4. After the descriptive study, results may generate a hypothesis → hand off to **Experimental** (hypothetico-deductive) for validation
5. If validated, apply findings to a password policy design → **Applied Research**

This progression shows that a single research program may touch all four categories sequentially.

## Key Takeaways
1. Always start with a written research question; refine it into the smallest atomic unit before selecting a method.
2. Use the four-category taxonomy (Observational, Theoretical, Experimental, Applied) as the first routing decision in method selection.
3. A hypothesis must be falsifiable — if you can't state it as true/false with evidence, refine it further.
4. Conduct a literature survey before executing any method; it sharpens the question and prevents duplication.
5. Build engineering on theoretical or observational foundations first; never engineer first and ask why it works later.
6. Real research is non-linear; document every decision and assumption so the path remains reproducible even if unexpected.

## Connects To
- **Ch 1**: The four research categories map to the types of science introduced (observational, mathematical, experimental, applied)
- **Ch 4**: Exploratory Study — first observational sub-method
- **Ch 5**: Descriptive Study — second observational sub-method
- **Ch 6**: Machine Learning — third observational sub-method
- **Ch 7**: Theoretical Research (Formal Theory)
- **Ch 8**: Simulation
- **Ch 9**: Hypothetico-deductive (Experimental)
- **Ch 10–11**: Quasi-experimental and Applied Experimentation
- **Ch 12**: Applied Observational Study
