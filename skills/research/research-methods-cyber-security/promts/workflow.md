```text
# AI Research Framework Workflow

You are operating inside an AI Research Framework.

The objective is NOT to write a thesis once.

The objective is to iteratively improve the thesis until it fully satisfies
Chapter 10 (Quasi-experimental Research)
from

Research Methods for Cyber Security.

========================================================

Repository Structure

skills/research/

    research-methods-cyber-security/

        chapters/
            ch10-quasi-experimental-research.md

        writers/
            ch10-writer.md

        reviewers/
            ch10-reviewer.md

        validators/
            ch10-validator.md

    vc_refactor.md

--------------------------------------------------------

Working Directory

working/

    thesis_working.md

    review_report.md

    validation_report.md

    change_log.md

--------------------------------------------------------

Final Directory

final/

    thesis_final.md

========================================================

Knowledge Source

Always use

skills/research/research-methods-cyber-security/chapters/ch10-quasi-experimental-research.md

as the ONLY methodology reference.

Never invent another research methodology.

========================================================

Input

Primary thesis

skills/research/vc_refactor.md

========================================================

Workflow

STEP 1

Load

Chapter 10 Knowledge

↓

Writer Skill

Rewrite

skills/research/vc_refactor.md

into

working/thesis_working.md

--------------------------------------------------------

STEP 2

Load

working/thesis_working.md

↓

Reviewer Skill

Generate

working/review_report.md

Do NOT modify the thesis.

Reviewer only evaluates.

--------------------------------------------------------

STEP 3

Load

working/thesis_working.md

↓

Validator Skill

Generate

working/validation_report.md

Do NOT modify the thesis.

Validator only validates.

--------------------------------------------------------

STEP 4

Decision

If

Reviewer

contains

Critical

or

Major

issues

OR

Validator

returns

FAIL

OR

Broken Evidence Chains

OR

Evidence Mismatch

OR

Unsupported Claims

Then

Return to Writer.

Writer must revise

working/thesis_working.md

using BOTH

review_report.md

and

validation_report.md.

Overwrite

working/thesis_working.md

Do not create a second draft.

--------------------------------------------------------

STEP 5

Repeat

Writer

↓

Reviewer

↓

Validator

until

ALL conditions below are satisfied.

========================================================

PASS Conditions

Reviewer

- No Critical issues
- No Major issues

Validator

- PASS
- No Broken Evidence Chains
- No Unsupported Claims
- No Evidence Mismatch

The document must fully comply with

Chapter 10

========================================================

Maximum Iterations

Maximum

5

iterations.

If

after iteration 5

the document still fails,

STOP.

Generate

working/final_report.md

containing

- Remaining Critical Issues
- Remaining Major Issues
- Remaining Evidence Gaps
- Manual Recommendations

========================================================

Writer Rules

Writer

IS ALLOWED TO

- rewrite
- reorganize
- improve
- refactor
- clarify

Writer

MUST NOT

invent

research methodology.

========================================================

Reviewer Rules

Reviewer

MUST ONLY

review

according to

Chapter 10.

Reviewer

MUST NOT

rewrite.

========================================================

Validator Rules

Validator

MUST ONLY

validate

Evidence

↓

Reasoning

↓

Conclusion

Validator

MUST NEVER

rewrite.

Validator

MUST NEVER

guess.

========================================================

Change Log

Every iteration

append

working/change_log.md

Iteration N

Writer

- modifications

Reviewer

- Critical
- Major
- Minor

Validator

- PASS / FAIL

Evidence Coverage

Summary

========================================================

Final Output

When

PASS

Copy

working/thesis_working.md

to

final/thesis_final.md

Also generate

final/final_review.md

containing

1.

Reviewer Summary

2.

Validator Summary

3.

Evidence Coverage

4.

Chapter 10 Compliance

5.

Overall Quality Assessment

========================================================

Golden Rules

Blockchain

is only the case study.

Research Methodology

is the primary artifact.

Never optimize for technical elegance.

Always optimize for

Quasi-experimental Research

compliance.

The process finishes only when

Reviewer

and

Validator

both approve the document.
```
