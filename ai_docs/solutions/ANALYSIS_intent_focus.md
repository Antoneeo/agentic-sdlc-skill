---
id: F-071
feature: Intent focus — the anti-myopia promise at the level of intent
description: Why every gate stayed green while F-063/F-064 lost the owner's core promise and spent its effort elsewhere; the doctrine that would have stopped it, replayed against that incident.
status: PLANNED
level: L3
domain: code
topics: [anti-myopia, vision-gate, review, proportionality]
start_date: 2026-10-04
branch: main
---
# Intent focus — the anti-myopia promise at the level of intent

For the owner and the next implementer: decide which doctrine change closes the
failure class shown by F-063/F-064, then design it. Elicitation is open (§Open
questions); nothing below is a design yet.

## Objective

Today the skill's anti-myopia defenses are **local**: they protect code (DRY,
consumer enumeration, blast radius) and the completeness of documents. No gate
protects **priority**: whether each step still serves the promise the owner cares
about most, and whether effort is proportional to it. F-063/F-064 passed every
gate while losing that promise. The objective is a mechanism, not more prose, that
makes this drift visible before code lands, at a cost proportional to risk.

## Feature Vision

`vision/project_vision.md` is APPROVED. Its Core Problem is myopia, and every
element exists "to make drift visible before it lands". This unit serves:

- **Solo developer** — "without losing the thread"; ceremony proportional to risk.
- **Team lead** — "divergence from the declared intent surfaced before the change
  is merged".

Constraint carried from the Vision: L1 gains no step; L2 gains none unless a
rule demonstrably needs it. No new artifact type unless the replay proves the
existing ones cannot carry the rule.

## Reference incident — F-063/F-064 (2026-10-04)

Evidence is snapshotted with hashes in `harness_intent_focus/incident/`
(`sources.json`): the work lives uncommitted on `codex/software-knowledge`, so the
snapshot is what keeps the replay possible whatever happens to that branch.
Author: a ChatGPT/Codex session (per the owner; the reviewers were gpt-6-astra).
Owner's intent, stated to Claude on 2026-10-04:
apply ingestion and knowledge management to source code and to how the software
works, so the agent understands more easily and better **how it works and why**.

Measured facts:

1. **The "why" never entered the chain.** Matches for why/perché/rationale/
   motivazione: Vision 0, ANALYSIS_kb_evidence 0, shipped `memory.md` 0, frozen
   rubric 0; ANALYSIS_software_knowledge 2, both incidental. None of UC1–UC5 names
   it. Elicitation was skipped: "non ripetuta: sono espliciti nella Vision".
2. **Effort went to the secondary risk.** New engine code in `knowledge.py`,
   lines per function (AST, current tree): confinement, integrity and publication
   ~190; evidence/drift ~220; capture ~75; claim kinds ~20; rationale 0. Design
   documents ~1,200 lines. A post-hoc review found a BLOCK caused by the
   over-hardening itself (links above the root refused, legacy corpora broken).
3. **The promise was measured after the code, with a test that could not show it.**
   Benefit was compared only after implementation. Fixture: 92 input lines, which
   the candidate turned into 45 knowledge files and 95 claims. No rubric question
   asks why. Result: candidate correct but 1081.7 s against 461.1 s for the
   baseline; FS7 failed and was honestly recorded.
4. **Every gate stayed green.** Vision blind check PASS, design review R2 PASS,
   code review R2 PASS, `check` CLEAN.

## Mechanism hypotheses (to be confirmed by the replay)

| ID | Where the skill let it through | Current text that allowed it |
|---|---|---|
| M1 | The core promise is never stated in the owner's words, so it can be dropped in translation | `elicitation.md` skip path accepts an approved Vision as a complete spec; the use-case grounding trace is existence-only (each UC traces to *a* benefit), never coverage of the essential one |
| M2 | Nothing measures where effort goes against the promise | Gates reward completeness: an agent that completes everything with equal care drowns the centre in detail |
| M3 | The promise is tested last, by a test that cannot discriminate | Execute-Before-Specify covers claims about *existing* code, not the claim that the feature will deliver its benefit |
| M4 | Reviews check conformance to the design, not the design's fidelity to the intent | `review.md` conformance statement maps each input constraint; a dropped essence is not an input row |

## Candidate remedies (direction only — designed after elicitation)

- **R1 Core promise:** at the Vision gate, 1–3 essential outcomes in the owner's
  words; every artifact and review shows where each is served, by weight.
- **R2 Promise probe before code:** the case that would demonstrate the promise,
  able to succeed and to fail, run red on the baseline before implementation.
- **R3 Proportion question at review:** which part of the diff serves the core
  promise; if the bulk is elsewhere, why.
- **R4 Thin slice first:** implement the minimum that exercises the promise,
  measure, then harden.

## Security and Threat Model

Doctrine-only change; no input parsing, filesystem or network surface is planned.
Risks to the process itself, kept open while the design is drafted:

| ID | Risk | Requirement |
|---|---|---|
| T1 | The new gate becomes ceremony: restating the promise in every document | Proven by the replay to fire where drift entered; L1/L2 untouched |
| T2 | The promise is gamed: copied verbatim into artifacts that do not serve it | Check by weight (where the effort goes), not by mention |
| T3 | A PASS on the new gate is read as proof of benefit | The promise probe reports benefit separately from conformance |

## Replay plan

Execute-Before-Specify applied to doctrine: each new rule is replayed against the
incident snapshot. **Red under the current text** — show the gate the incident
passed; **green under the new text** — show the rule firing at the exact artifact
where the drift entered (UC table, effort split, test design, review verdict).
A rule that would not have fired on this incident is not admitted.

## Open questions

1. *Answered 2026-10-05.* The Vision was drafted by ChatGPT from the owner's
   request and approved by the owner, who may have missed details; its provenance
   note ("Testo fornito da Antonio Pinto") overstates authorship. The owner's model:
   **why** = the milestone Vision's sought benefit; **what** = UC and IC, with the
   TM's risks; **how** = ISP and TDD. Their request meant the knowledge layer should
   let an agent climb from code to the what and the why. The drafted Vision links
   "general functioning" *down* to code and test evidence only; no element links
   code *up* to the benefit and use cases it serves. M1 is confirmed and located:
   the loss happened when the agent wrote the Vision, and the owner's approval was
   given against the agent's text, not against the owner's own words. The
   elicitation skip then treated that same-session, agent-drafted Vision as an
   explicit owner spec.

Consequence for M1's remedy (direction): an agent-drafted Vision is approved
against a coverage map of the owner's original request (each element of the
request → where the Vision carries it, or "dropped"), and it never qualifies for
the elicitation skip path in the same flow.

Consequence for a future redo of F-063 (not this unit): the knowledge layer should
mirror the skill's own chain — Vision (why) → UC/IC/TM (what) → ISP/TDD (how) →
code and test evidence — so navigation works in both directions.

## Status of the incident work

F-063/F-064 is parked, not reverted: uncommitted on `codex/software-knowledge`.
The owner decides whether to commit it as a parked branch; it is not merged.

## Diary

- 2026-10-04: opened from the post-implementation review of F-063/F-064 by Claude
  (claude-opus-5-5). Worktree `claude/intent-focus` from `main` (2d5a5c6); incident
  snapshot taken; facts above measured, not inferred. Elicitation open.
- 2026-10-05: owner answered question 1 — Vision drafted by ChatGPT, approved by the
  owner; why/what/how = Vision / UC-IC-TM / ISP-TDD. M1 located at Vision drafting.
- 2026-10-17: records moved to `main` (no local branches, owner ruling) and the unit
  renumbered F-065 -> F-071: F-065 was already taken on `main` by
  `ANALYSIS_review_mandate_contract.md`. The archive tag `archive/software-knowledge`
  and its commit message still call this unit F-065.

## Diary

- 2026-10-18 — M1 is closed for Vision authoring by F-074 (`ANALYSIS_vision_interview.md`):
  every Vision is written only after an owner interview and an owner-approved north
  star, and elicitation's skip path no longer reaches a Vision. R1's coverage of the
  core promise in downstream artifacts, and M2–M4, remain here.
