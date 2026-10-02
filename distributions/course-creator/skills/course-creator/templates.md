# Course Creator templates

These are starting shapes, not substitute explanations. Keep one authority for each fact and ID. The project root is `ai_docs/`; its curated `README.md` lists `vision/project_vision.md`, `INDEX.md`, and `reference/INDEX.md` as must-reads. Run `sdlc_check.py index` for generated indexes.

## Course Vision — `vision/features/VISION_course_<slug>.md`

Read `vision.md` and use its blind check before APPROVED. The person approves benefit and scope, not the agent.

```markdown
---
description: What this course enables for its named learners.
status: DRAFT
domain: course
---
# Course Vision: <title>
Status: DRAFT

## Expected Benefit
<Why the learner needs the knowledge and what becomes possible.>
## Learners and Starting Point
<Who, context of use, what is known with evidence, what remains uncertain.>
## Promised Understanding and Ability
<Knowledge and usable capability, not a list of slides.>
## Success Signals
<Observable understanding or use; distinguish simulated diagnosis from real evidence.>
## Scope and Non-Goals
<Boundaries, delivery constraints and facts outside this course.>
```

Approval changes both `status:` and `Status:` to `APPROVED`.

## Canonical analysis — `solutions/ANALYSIS_course_<slug>.md`

The core uses this file for workstream state and course risk. It is the only authority for UC, IC flow and risk IDs. The details below cite these IDs. The Interface Contract is due when an actor acts on or perceives a surface: for a course, the learner necessarily does. Design and code review use `review.md`; log them in `audit/reviews/REVIEW_LOG.md`. If reviewer access is permission-gated, record `gated, declined`, `gated, unattended` or `gated, pre-empted` truthfully and use the next available rung rather than claiming independence.

```markdown
---
id: C-<number>
feature: <course title>
domain: course
level: L3
status: PLANNED
start_date: YYYY-MM-DD
end_date:
---
# Course Analysis: <title>
## Objective
<Value delivered to this learner.>
## Feature Vision
`vision/features/VISION_course_<slug>.md`; benefit and success signal served.
## Use Cases / User Needs
### UC1 — <actor, need, expected use and benefit>
## Functional Spec
<Course behavior visible to learner and author.>
## Interface Contract
### IC1 — <surface, flow, feedback and failure response>
## Capability Ledger
| Capability | Existing or missing | Evidence and consequence |
|---|---|---|
## Impact
| Path | ADD/MODIFY/DELETE | Responsibility and why |
|---|---|---|
## Learning and Content Risks
### C-1 — <failure, mitigation, residual and evidence>
## Action Plan
<Execution and review sequence.>
## Test Strategy
<Structural, source, explanation and simulated checks; human evidence limits.>
## Diary / Current State
<Dated state and decisions.>
```

For parallel work, `audit/HANDOFF_[course].md` carries resume logistics, not a duplicate Diary. Its frontmatter includes `workstream: <slug>`. `audit/handoff.md` is the GENERATED workstream registry: convert existing handoffs all at once, then run `index`; do not edit the generated file by hand.

## Course detail files — `solutions/courses/<slug>/`

Use these names and headers because `course_check.py` checks the link structure. IDs in the first three tables must be defined in the ANALYSIS. Every reference to a local explanation, check or source uses a project-relative path plus `#heading-locator`; an audio/video locator uses a timecode such as `#00:01:00`. A URL source is allowed when reopenable; its truth and availability require human/source review.

### `D-UC.md`

Use one row per (UC ID, Profile). The same use case may serve several profiles;
repeat its ID for each profile, but never duplicate a pair. Profile names here
are the authority for graph and module references; use the same exact name in
each table. Empty names and `-` are not profiles.

```markdown
| UC ID | Profile | Starting knowledge | Evidence | Need |
|---|---|---|---|---|
| UC1 | <specific learner> | <known/uncertain concepts> | <observation, task or interview> | <why they learn and where they use it> |

## evidence-1
<Precise evidence for a concept marked PROVATO, linked to a profile.>
```

### `D-IC.md`

This is the single authority for the chosen feedback channel. Use `not available` if none exists; never invent a service. The channel must carry course/version/module, and the material points at this flow ID.

```markdown
| Flow ID | Surface | Conditions | Feedback channel |
|---|---|---|---|
| IC1 | <format, device, access> | <when and where used> | <actual channel or not available> |
```

### `P-TM.md`

```markdown
| Risk ID | Vector | Mitigation | Residual |
|---|---|---|---|
| C-1 | <content, learning, safety or privacy failure> | <action> | <remaining limit> |
```

### `CONCEPT_GRAPH.md`

The IDs identify instructional concepts, not KB topics. Use one row per
(Concept ID, Profile), with the profile defined in `D-UC.md`. The same concept
can be `PROVATO` for one profile and `DA_INSEGNARE` for another; each pair has
its own state, evidence and objectives. Repeated concept IDs must declare the
same prerequisite IDs, since they describe the same concept. Every prerequisite
also needs a row for that profile; knowledge or teaching for a different profile
does not satisfy it. `PROVATO` needs precise learner evidence in this course's
`D-UC.md#locator`. An uncertain prerequisite is taught before use or declared as
an unresolved limit. `Source` is a reopenable reference, not the model's memory.

```markdown
| Concept ID | Prerequisites | Profile | Initial state | Evidence | Source | Objectives |
|---|---|---|---|---|---|---|
| CO1 | - | <profile> | DA_INSEGNARE | - | ai_docs/.../sources.md#claim-1 | O1 |
| CO2 | CO1 | <profile> | INCERTO | - | https://example.org/reference | O2 |
```

For example, add a second `CO1` row for `expert` with `PROVATO` and an evidence
locator while the `novice` row stays `DA_INSEGNARE`. Both names must already be
defined in `D-UC.md`. Keep a single row if the course has only one profile.

### `COURSE_PLAN.md`

`Feedback flow` cites `D-IC.md`; it does not redefine the channel. New and substantially revised courses use the complete primary text contract in `slide_content.md`; renderings are optional. Explanation and Check locate the canonical units. Each module has a named learner, objective and check. Sequence modules by prerequisite order. Keep the efficacy label visible; a simulator PASS cannot change it.

Each module names one profile from `D-UC.md` and uses that profile's concept
rows. Module IDs remain unique across the course; `Next` follows the one declared
sequence. A shared explanation may be referenced by separate module rows for
different profiles without copying its material. Prerequisite teaching is
checked within each profile, including concept order inside a module.

```markdown
Course version: 1.0
Content contract: slide-content-v1
Efficacy: efficacy not verified
Feedback flow: IC1

| Module ID | Profile | Objective ID | Concepts | Explanation | Sources | Check | Next |
|---|---|---|---|---|---|---|---|
| M1 | <profile> | O1 | CO1 | ai_docs/.../SLIDE_CONTENT.md#s01 | ai_docs/.../sources.md#claim-1 | ai_docs/.../SLIDE_CONTENT.md#s03 | M2 |
```

Before drafting units, use `learning_design.md` to define evidence for the promised result. Add this compact alignment under the module sequence. Descriptions suffice in design; retain them and add exact locators to the authored explanation, example, check and correction before delivery. A row can cover several objectives if the relationship is explicit; the table is reviewed semantically, not certified by the structural validator.

```markdown
## Teaching alignment
| Objectives and use context | Evidence and success criterion | Explanatory bridge | Example or contrast | Support and correction |
|---|---|---|---|---|
| O1: <observable comprehension/decision and conditions; for a course on a tool or agent, the learner's act and, where one exists, the tool output it acts on or the request it formulates (learning_design.md §1)> | <task + what distinguishes an adequate answer> | <passage explaining the connection, not its topic name> | <case/changed condition and locator> | <appropriate guidance, rationale, likely error and recovery locator> |
```

The module material itself names course/version/module, explains the concept for that profile, gives a useful example and transition, and points to IC1 or says feedback is unavailable.

## Review log and project architecture

Use the shared `review.md` schema at `audit/reviews/REVIEW_LOG.md`:

| date | doc_key | tier | model | reviewer | findings_raised | findings_real | verdict | revise_rounds |
|---|---|---|---|---|---|---|---|---|

The `model` cell identifies the available capability: `deep`, `light`, `economy`, `single (client exposes no choice)` or `below floor: <reason>`. A declared self-pass is labeled as such. This log records evidence and limits; it does not grant approval.

The shared `strategic/architecture.md` still records components actually discovered. A fresh project has an empty map; never invent one from the course template.

## Component Map

Coverage follows `audit/audit_plan.md` areas marked ANALYZED. Outside them the map is unread, not empty. Add a row only after a real component is inspected.

| Component | Capability it owns | Contract | Where |
|---|---|---|---|

## Architectural Patterns

<Patterns verified from the project, if any.>

### `SIMULATION_REPORT.md`

```markdown
Status: not run | diagnostic pass | diagnostic fail | inconclusive
Course version/hash: <exact material>
Author/coordinator: <session responsible for canonical artifacts>
Didactic reviewer: <independent session and review verdict/locator; or declared fallback>
Profile and objective: <fixed before tests>
Permitted tools and materials: <same except course packet>
Course session ID and verbatim prompt: <fresh agent; no answers>
Control session ID and verbatim prompt: <fresh agent; no course>
Responses and cited material: <verbatim or artifact paths>
Criteria, blocks and corrections: <including control already succeeding>
Conclusion: diagnostic only; no claim of human efficacy
```

Follow the role handoffs in `simulation.md`. Repeat profile-specific attempts for each tested profile; keep each reveal/response in order and identify the fresh reader and new material version after a correction. Distinguish untested profiles or units from passed ones. The didactic reviewer uses these records for the existing REVIEW_LOG verdict.

If sessions are unavailable, write `Status: not run` and the reason. A control already successful makes a course-assisted success inconclusive.

### `FEEDBACK_REPORT.md` — only after real feedback

```markdown
| Date | Source/channel | Course version | Module ID | Context | Feedback | Correction |
|---|---|---|---|---|---|---|
| YYYY-MM-DD | <identified origin> | 1.0 | M1 | <minimal context> | <observation> | <proposed change> |

## Effectiveness assessment, if claimed
<Comparable learner profile, explicit criterion, observed comprehension/use,
contrary results and limits. One isolated comment is not proof.>
```

Keep only the minimal necessary learner data; do not build a continuing personal register.
