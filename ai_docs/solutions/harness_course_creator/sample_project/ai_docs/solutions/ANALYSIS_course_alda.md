---
id: C-900
feature: Alda receipt lesson
status: IN_PROGRESS
domain: course
level: L3
start_date: 2026-09-27
end_date:
---
# Course Analysis: Alda receipts
## Objective
Explain a fictional receipt check to a reader starting from zero.
## Feature Vision
`vision/features/VISION_course_alda.md`; the expected benefit is an explainable receipt verdict.
## Use Cases / User Needs
### UC1
The novice reads the course and checks a new receipt to decide if it is valid.
## Functional Spec
Teach values, rotation and addition before a validity verdict. The fiction's own source is authoritative for its invented rules.
## Interface Contract
### IC1
The reader opens text modules in order; feedback is not available in this exercise. An unclear rule is reported to the author separately.
## Capability Ledger
| Capability | Existing or missing | Evidence and consequence |
|---|---|---|
| Source | Existing | The invented protocol is fully defined in sources.md. |
## Impact
| Path | ADD/MODIFY/DELETE | Responsibility and why |
|---|---|---|
| ai_docs/solutions/courses/alda/ | ADD | Learner material. |
## Learning and Content Risks
### C-1
Omitting rotation would make the check impossible; teach it before the total.
## Action Plan
Write three modules, inspect the graph and references, then compare fresh learners with and without the course.
## Test Strategy
A novel receipt tests transfer. A correct control makes the comparison inconclusive. No simulator result proves human efficacy.
## Diary / Current State
2026-09-27: Example course authored for the course_creator fixture.
