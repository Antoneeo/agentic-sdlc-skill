---
id: F-099
feature: Vision anchored - a restriction answers to the source it serves
description: F-099 - a requirement drifted stricter than the Vision clause it served and four review rounds never measured it against that clause's test; the design makes every restriction in a significant design name its source and stay within that source's test, makes the design review check it in that direction too, and makes a second design-review FAIL of the same class re-read the source before adding mechanism.
status: COMPLETED
level: L3
start_date: 2026-11-15
end_date: 2026-11-15
domain: code
---
# Feature Analysis: Vision anchored (F-099)

## Objective

A field case from another project (held outside the repository, R8;
`REQUEST_vision_anchored.md#R1`): a milestone vision asked that whoever runs a protected
workflow does not obtain «the full definition». The interface contract, the threat model
and the plan node narrowed it to «no key in any error». Four review rounds failed for want
of a mechanism able to meet the narrowed requirement. After round 2 the requirement was
narrowed for cost by its owner, but nobody measured it against the
vision's test until the owner asked, after round 4, whether the node had a clear vision. At
round five the requirement was brought back to that test and the review passed.

The owner's diagnosis (R1): «si è perso di vista la VISION che è fondamentale per evitare
la miopia che è il motivo per cui esistono le skills».

The mechanism, named with the owner (R2): the Vision is read once, at the gate. Each later
artifact derives from the previous one. The review checks the artifact against the
constraints upstream of it, never those constraints against the Vision. And the Vision
check that does run looks one way only: it catches scope added, not a constraint made
stricter. A stricter constraint is not "extra safety": it can take away what the Vision
promises elsewhere, and it spends review rounds on mechanism the Vision never asked for.

The unit makes every restriction in a significant design name the source it serves and
stay within that source's test; makes the design review check that direction; and makes a
second design-review FAIL of the same class re-read the source before another round adds
mechanism. Scope and cost: R2 (framing), R4 (restrictions only), R5 (measured cost, three
sources).

## Feature Vision

No feature Vision: the unit serves the project Vision (`vision/project_vision.md`, v9,
APPROVED) and stays inside one milestone.

- Core Problem: «Myopia: an agent acts from partial understanding … Every element of this
  methodology … exists to make understanding durable and to make drift visible before it
  lands.» The case is drift that stayed invisible for four rounds.
- Goal: «Make divergence from the declared intent visible *before* implementation, and
  again before merge. Never hide a conflict between a user request and the declared
  Vision: surface it and let the user choose.» A restriction stricter than its clause is a
  divergence that today is not surfaced.
- `vision.md` §What a Vision IS (the skill's own reading of any Vision): «It binds nothing
  that does not obstruct that benefit.» The unit carries that sentence downstream: what an
  artifact derived from the Vision binds, it binds because a source asks it.
- Non-Goal 3 (no ceremony ratchet): the unit adds a mandatory duty at L3; its cost is stated
  in §Ceremony cost and accepted by the owner (R4, R5). Nothing at L1 or L2.
- Non-Goal 1 (not a work-management system): untouched — no count, cap, order or
  assignment.

## Use Cases / User Needs

- **UC1 (owner)** — a requirement written in their name is never stricter than what they
  asked, unless they chose it. *Benefit: divergence surfaced before implementation.*
- **UC2 (author agent)** — writing a protection, a prohibition or a closed list, knows
  against what to measure it and when it has gone too far. *Benefit: same.*
- **UC3 (reviewer)** — has a check that can fail a requirement, not only an artifact that
  does not meet it. *Benefit: same, before merge.*
- **UC4 (author agent after repeated FAILs)** — stops adding mechanism to a requirement
  nobody re-examined. *Benefit: ceremony proportional to risk; review rounds spent on what
  the Vision asks.*

## Functional Spec

- **FS1 — a restriction names its source.** In an L3 design (an ANALYSIS; in Hybrid the
  governed D-IC, P-TM, E-ISP and E-TDD; the lens's top level elsewhere), every requirement
  that restricts — a protection, a prohibition, a closed list, a "never" or "only", a
  mitigation — names its source: a Vision clause quoted, the owner's words with their
  request-record entry, or a threat of the design's own threat model. One quotation may
  serve several restrictions.
- **FS2 — within the source's test.** A Vision clause's test is its own question; the
  owner's words, what they asked; a mitigation's, what stopping its threat requires. A
  restriction asks no more: it forbids nothing the test allows, and its wording is no
  stricter. A stricter one is a divergence: tighten it back to the test, or bring the
  stricter reading to the owner as a choice about the Vision.
- **FS3 — a restriction that takes away a Vision promise.** One that takes away what the
  Vision promises elsewhere (an obligation, a Success Signal, an actor's good experience)
  is out as written, whatever its source, a threat included: it enters the design only if
  the owner chooses it, and the owner is told in the same message either way.
- **FS4 — never below the source.** Tightening back stops at the source's test. A
  restriction is never removed because no Vision clause names it: one with no source that
  takes nothing the Vision promises is a doubt asked of the owner or a threat written down,
  never a deletion.
- **FS5 — the design review checks the reverse direction.** The conformance statement
  carries one row per restriction: its source and whether it stays within the source's
  test. No source, beyond the test, or taking a Vision promise is a finding; the fix for a
  missing source is a source asked or a threat written, never a deletion.
- **FS6 — re-anchor at the second design-review FAIL of the same class.** When a design
  review (L3, or the lens's top level) FAILs a second time on findings of one class (the
  same requirement, surface or property, even with different instances), the author
  re-reads that requirement's source and checks FS2 before revising. Beyond the test: the
  next step is the question to whoever owns the requirement, not another round of
  mechanism. The answer is written in the REVIEW_LOG row's notes, either way. The round cap
  is unchanged.
- **FS7 — where it applies.** The four lenses, Standalone and Hybrid; each lens points at
  the shared rule in its own words. Nothing at L1 or L2, and nothing in a review that is not
  a design review.

## Interface Contract

The surfaces are the doctrine the agent loads and three outputs a person reads. Each
reuses an existing idiom; no new file, section or field.

- UC1: the owner reads, in the message that carries a design, the restrictions a source
  could not justify or that take a Vision promise (FS2, FS3), and answers there.
- UC2: the author writes the source beside each restriction, in the section that holds it
  (Interface Contract, Security and Threat Model; the governed artifact in Hybrid), as a
  quotation with its provenance (`vision.md` §The owner interview, question 6).
- UC3: the reviewer adds the restriction rows to the conformance statement it already
  writes (`review.md`).
- UC4: after the second design-review FAIL of one class, the author's next message is the
  re-anchor's answer, and the REVIEW_LOG row's notes column holds it.

## Capability Ledger

| Capability | Verdict | Where / gap |
|---|---|---|
| state where a restriction comes from | INADEQUATE | `vision.md` question 6 asks provenance for constraints *in a Vision*; nothing asks it downstream |
| compare a requirement with the Vision | INADEQUATE | `review.md` conformance statement maps each constraint to where the artifact satisfies it: one direction only |
| notice a review loop on one requirement | INADEQUATE | `review.md` caps rounds at 3; nothing reads what the failed rounds have in common |

Each becomes doctrine in the files that already own the duty (Impact), no new component.

## Guide check

No CURRENT guide covers the review or Vision doctrine (`reference/INDEX.md`: hooks,
release, shared project memory, skill-family changes). `GUIDE_skill_family_changes.md`
governs the triage of a change copied into the distributions: read whole; it counts the
copies as one change per shared file. No guide is owed: the unit forced no model of a
complex component.

## Impact

Shared core (authored once in the code lens, copied verbatim into three trees by
`shared_files.py --update`):

- `skills/agentic-sdlc-skill/vision.md` — MODIFY: a header clause and new §8 "Downstream: a
  restriction answers to its source" (FS1–FS4, FS7).
- `skills/agentic-sdlc-skill/review.md` — MODIFY: the conformance statement gains the
  restriction row and its fix (FS5); after "Rounds are capped at 3", the re-anchor
  paragraph (FS6).
- `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` — MODIFY: class
  `F099_VisionAnchored`, in every tree.
- The three copies of each, and `shared_manifest.json` in the four trees — regenerated.

Per lens, own words:

- `skills/agentic-sdlc-skill/SKILL.md` — one sentence after "Protect the Vision"; the
  support-file line for `vision.md` names §8.
- `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` — the same two places.
- `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` — after "Protect the
  Marketing Vision" (E3 plan).
- `distributions/course-creator/skills/course-creator/SKILL.md` — §3 Course Design.

Evidence and records:

- `skills/agentic-sdlc-skill/evals/scenarios/restriction_exceeds_its_source.md` — ADD. One
  scenario, in the code lens: the rule is shared text, identical in four trees, and each
  lens's own sentence is held by the invariants.
- `ai_docs/vision/rulings.md` — rows r51, r52.
- `ai_docs/solutions/harness_vision_anchored/` — the proposal, two replays (replay 1:
  criteria and results only; replay 2 whole). The case itself is held outside (R8).
- `ai_docs/strategic/process_agentic_sdlc_devpnt.md` — the conformance-statement line names
  the reverse direction.
- `ai_docs/README.md` — the `## Team` section (R3, F-098's rule, asked by this unit).

Read and left unchanged, because they are not wrong: `README.md` and the three
distribution READMEs (they do not describe the conformance statement or the round cap),
`ai_docs/strategic/skill_family_agent_workflows.md`, `ai_docs/strategic/architecture.md`.
No CHANGELOG entry: F-096 to F-099 are unreleased, and publication is the owner's.

**Out of scope, declared:** the proposal's devPNT half (items 1a and 2a, devPNT doctrine
§4.2 and §4.5). That doctrine is generated from devPNT's own source, not this repository;
its change is the owner's to make there. In Hybrid the skill's rule already reaches the
governed artifacts by name (§8, FS1).

No validator code changes: the duty is a judgement, not a form a parser can read. No
golden transcript changes.

### Preservation constraints

| Symbol / text | What must stay true |
|---|---|
| `review.md` conformance statement | its existing rows and "PASS not valid on found nothing" unchanged |
| `review.md` round cap | 3 rounds, then the user: FS6 adds a question inside the cap, never a fourth round |
| `vision.md` §1–§7 | unchanged: §8 is about reading a Vision, not writing one |
| `SHARED_FILES` | no file added or removed |

## Security and Threat Model

No code, input or data surface. Two threats, on the rule itself:

- **T1 — the rule used to strip a protection.** An agent reads FS2 as "remove whatever no
  Vision clause asks". Mitigation by construction: a threat is a valid source (FS1) with its
  own test (FS2); FS4 forbids going below the source and turns a missing source into a
  question, never a deletion; FS5 tells the reviewer the same. Tested: `replay2/` (an old-text
  reader dropped the threat-sourced protection; no new-text reader did). **Residual,
  declared:** a threat-sourced protection may be narrowed to the threat's own wording (three
  of four new-text readers narrowed "every export" to "bulk export", one without asking). That
  is FS2 applied, but a threat worded too narrowly carries the narrowing with it; the design
  review's restriction row (FS5) is its only check.
- **T2 — a mitigation that removes a Vision promise passes because it cites a threat.**
  FS3 keeps it out until the owner chooses it.

## Ceremony cost

Accepted by the owner: the shape (R4, restrictions only) and the measured figures and three
sources (R5).

| Level | Added | Cost |
|---|---|---|
| L1, L2 | nothing | 0 |
| L3 design | one source per restriction, quoted or referenced (`R<n>`, `T<n>`) | a line per restriction; one quotation may serve several |
| L3 design review | one conformance row per restriction | inside the statement already owed |
| a second design-review FAIL of one class | one re-read and one note | 0 unless a review fails twice |
| every session that loads a lens | `SKILL.md` | +282 code, +283 knowledge, +236 marketing, +241 course (UTF-8 bytes, LF) |

Read on their own triggers: `vision.md` +2,470 bytes, `review.md` +1,063, both shared.

## Action Plan

- [x] Case artifacts received and redaction-read.
- [x] RED: invariants in `test_skill_invariants.py` (4 failing before the doctrine).
- [x] `vision.md` §8, `review.md`; copies and manifests.
- [x] One sentence per lens `SKILL.md`.
- [x] Eval scenario; replay 1 on the recorded case, old against new.
- [x] Rulings rows r51, r52.
- [x] Review round 1 (FAIL); fixes; replay 2 (drafting time, T1); measured cost to the owner (R5).
- [x] Review rounds 2 (PASS, 9 WARN taken) and 3 (PASS); design approved by the agent under R3 (R6); local commit.
- [x] Merge into local `main` on the owner's word (R7).
- [x] Case material moved outside the repository; unpushed history rewritten (R8).
- [ ] The owner: the devPNT half in devPNT's source, if wanted.

## Test Strategy

- **Replay 1, the recorded case** (`harness_vision_anchored/replay/`: criteria and results; the case, prompts and raw answers held outside the repository, R8): a cold reader in the
  author's place after round 2, old doctrine against new; criteria written first. Result:
  old 0/2, new 2/2.
- **Replay 2, drafting time and T1** (`replay2/`): a neutral fixture with four draft
  restrictions — one Vision-sourced, one sourceless and stricter, one threat-sourced with no
  Vision clause, one taking a Vision promise. Result: old 0/2 (one dropped the threat-sourced
  protection); new v1 0/2 on one criterion, traced to a contradiction in §8 and fixed; new v2
  2/2.
- **Invariants**: `F099_VisionAnchored` in every tree — §8's anchors, the review row and its
  fix, the re-anchor inside the unchanged cap, the lens sentence at the top level.
- **Suite**: `unittest discover` in each lens's `scripts/`; `test_drift`.
- **Eval scenario** `restriction_exceeds_its_source`: kept for the battery; not executed in
  this unit (replays 1 and 2 cover its behaviour).

## Diary / Current State

**2026-11-15 — opened; team section written; cost accepted.** Request record R1–R4. The
team questions answered in R3 and written as the reading guide's `## Team`. Ceremony shape
chosen by the owner (R4). Case artifacts requested from the session that wrote the
proposal.

**2026-11-15 — implemented; replay old 0/2, new 2/2.** Doctrine in `vision.md` §8 and
`review.md` (shared, four trees), one sentence per lens, eval scenario, rulings r51–r52.
Replay on the recorded case after round 2 (`replay/RESULTS.md`, criteria written first).
A first draft of §8 used the case's own words as its example; replaced by a neutral one.
**Deviation from the workflow:** the doctrine was written before the replay and before an
independent design review, while the case artifacts were on their way. The replay ran the
old text from the base commit against the new, so the comparison holds; the design and
closure reviews run as one review of this ANALYSIS and the diff, and say so in the log.

**2026-11-15 — review round 1: FAIL, 4 BLOCK, 10 WARN, 6 CANNOT VERIFY; all taken.**
B1 the other project's name in the request record (redacted before the first commit). B2 the
re-anchor and the lens sentences reached L1/L2 and every review type (now L3 design reviews
and an L3 design, in all four lenses). B3 the T1 counter-case was promised and absent (replay
2). B4 the always-loaded bytes were labelled accepted without a record (put to the owner with
the measured figures: R5). W1 a threat had no "test" (defined: what stopping it requires); W2
the review clause did not say a missing source is never fixed by deletion (added); W3 r52 and
the description overstated the case (reworded: the requirement was narrowed for cost after
round 2, first measured against the vision's test after round 4); W4 raw answers kept; W5
byte figures re-measured; W6 four code identifiers left in the case files (replaced); W7 the
devPNT half declared out of scope; W8 derived documents (the `vision.md` support-file line,
the process document; the `## Team` section listed); W9 three sources put to the owner (R5);
W10 the design approval is recorded after round 2 under R3, the Interface Contract now has a
flow per use case, and the eval stays in the code lens (declared above). CANNOT VERIFY 1 (the
criteria's order) stands: the files are untracked; the transcript of this session wrote
`CRITERIA.md` before the runs, which no file can show. Replay 2 v1 found a contradiction in
§8 (a restriction taking a Vision promise "goes to the owner" against "never a deletion");
the rule now says it is out as written and the owner is told.

The case's session added one more instance of the defect: decision M of its interface
contract was left unchanged in version 1.7 and still contradicts the new S2.6 sentence on
error messages — a downstream artifact not realigned with the one it serves.

**2026-11-15 — review rounds 2 and 3: PASS.** Round 2 (deep, scoped): all fourteen round-1
findings addressed; nine new WARNs, taken (rulings aligned with §8 and the L3 design-review
scope, FS numbers in the invariants, T1 residual declared, `## Team` cut to R3's words); W5
left (antecedent of "the same message", anchored by the invariant and both v2 readers).
Round 3 (light, last, on the corrections only): PASS, two wording WARNs on `## Team` taken
after it. Design approved by the agent under R3 (R6). Suites: code 691, knowledge 1004,
marketing 707, course 697, all OK. Committed locally on `feat/f099-vision-anchored`; not
merged, not pushed. 

**2026-11-15 — closed: merged into local `main` by fast-forward on the owner's word (R7).**
Workstream file deleted, ANALYSIS COMPLETED, areas marked by commit hash. Not pushed and not
released. Before any push: the owner reads the redacted case files. Open elsewhere: the devPNT
doctrine half of the proposal (devPNT's source); the eval scenario not yet executed.

**2026-11-15 — case material out of the repository (R8).** The redacted case described open
defects of another project, recognisable from labels and from that project's name in other
public files here. The case files and replay 1's prompts and raw answers moved outside the
repository; the three local F-099 commits were rebuilt without them before any push. Replay 1
keeps its criteria and results; replay 2, on a neutral fixture, is whole.
