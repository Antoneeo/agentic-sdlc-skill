---
description: F-071 behavioural replay — six cases a cold agent rules from review.md and SKILL.md alone; expected rulings per text.
status: CURRENT
---
# F-071 behavioural replay cases

The prompt given to each cold agent is §Prompt, with DIR set to the doctrine under test
(current: `skills/agentic-sdlc-skill/`; proposed: a copy with `proposed.patch` applied).
§Expected is never shown to the agent.

## Prompt

You are an agent following the agentic-sdlc skill. Read DIR/review.md and DIR/SKILL.md
in full; use nothing else (no other file, no memory of other versions). For each case,
answer the question, quote the sentence(s) of those two files that rule it, and say
"the text does not rule this" when no sentence does. Do not infer a rule the text does
not state.

- **C1 (design review).** You review the design of an L3 unit in the code lens. The
  owner's opening request in the request record: "the agent should understand more easily
  and better how the software works and why". The design has five use cases (ingesting
  code knowledge, evidence, drift, capture, claim kinds); none mentions why or rationale.
  Planned code: ~190 lines confinement/integrity/publication, ~220 evidence/drift, ~75
  capture, 0 for rationale. Every use case traces to a Vision benefit; the Functional Spec
  is present. The benefit is to be measured after implementation, with a rubric that asks
  no "why" question. Question: does the mandate REQUIRE you to raise a finding (a) on how
  the design covers the owner's outcome, (b) on when and how the benefit is measured?
- **C2.** After the closure review of an L3 unit returned PASS, the author makes a delta:
  version bumps in four package.json files, regenerated INDEX.md, and a CHANGELOG entry
  restating the reviewed change's summary. Question: is a closure review due on this
  delta? What, if anything, must be logged?
- **C3.** Same as C2, plus one README line claiming a capability that the reviewed
  artifacts do not describe. Question: is a review due, and on what?
- **C4.** A closure review returned PASS with two WARNs; the author fixes one WARN by
  editing a CHANGELOG line. Question: is a review of that edit due?
- **C5.** An L2 change (clear root cause, one doctrine line plus one test, no
  security-sensitive area), test shown red then green, batteries green. Question: is an
  independent closure review due, optional, or not due?
- **C6.** An L3 unit in the code lens; the owner's request: "make the agent find the
  right guide faster". The author frames it as a new capability, "a guide search
  command", with Functional Spec acceptance criteria. Question: before code is written,
  what must exist concerning the benefit the owner named?

Return one block per case: ANSWER, QUOTE, and RULED-BY-TEXT yes/no.

## Expected

| Case | Current text (red) | Proposed text (green) |
|---|---|---|
| C1 | (a) no rule requires it; (b) no rule requires it | (a) finding required (outcome row, minor share); (b) finding required (probe red on baseline missing) |
| C2 | not ruled as not due (moment 2 applies to any diff) | not due; NOT DUE row |
| C3 | not ruled as not due | due, scoped to the README line |
| C4 | due (scoped re-review) | due (scoped re-review) — never NOT DUE |
| C5 | optional, no criterion | not due |
| C6 | nothing specific (Execute-Before-Specify covers existing code) | probe built, red on baseline, before code; framing does not exempt |

C3 and C4 are controls: the proposed text must rule both due. A proposed text that rules
either not due fails the replay.

## Results — 2026-10-18

Two fresh general-purpose subagents (light tier, one per text, neutral directory
names), prompt as above; full answers in the F-071 session transcript, summarized here.

| Case | Current text | Proposed text | Verdict |
|---|---|---|---|
| C1 | (a) no, (b) no — "the text does not rule this"; quotes the request-record clause as covering only statements the artifact relies on | (a) yes, outcome row with minor share; (b) yes, comparative wording, probe red on baseline missing | red → green |
| C2 | not ruled ("nothing says a post-PASS mechanical delta triggers a review"), no row | not due; NOT DUE row with the stated cells | red → green |
| C3 | not ruled | due, scoped to the README line | control holds |
| C4 | due, scoped re-review | due, scoped re-review ("never in it") | control holds |
| C5 | optional | not due | red → green |
| C6 | not ruled (generic L3 gates only) | probe before code, red on baseline; framing does not exempt | red → green |

Gaps the proposed-text agent named: whether a skipped L2 review logs a row (closed by
adding "and logs no row" to the L2 trigger) and what check proves a version bump (left
to the delta's own tooling, named in the row).

Re-run on the applied text (Action Plan step 4): not run. The applied `review.md`
differs from the replayed one by one clause, "and logs no row", added to close the gap
above; `SKILL.md` is identical (compared LF-normalized, 2026-10-18). No case ruling can
change, so a second ~140k-token cold run would lower no risk.
