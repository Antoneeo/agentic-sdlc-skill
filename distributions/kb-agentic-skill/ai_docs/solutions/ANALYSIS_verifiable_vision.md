---
id: F-018
feature: Verifiable Vision (the drafting discipline)
status: COMPLETED
level: L3
start_date: 2026-07-27
end_date: 2026-07-27
---
# Feature Analysis: Verifiable Vision

## Objective

Make a Vision verifiable **on the first draft**, not after six rounds of adversarial
patching.

Owner's framing, at the point it became clear (2026-07-27): *"dobbiamo arrivare
all'anima del concetto di vision in modo che sia davvero verificabile dai reviewer,
non in 5 step di approssimazione."*

F-017 fixed one project's Vision by iteration: six blind rounds, each closing the
previous round's findings and opening narrower ones. It worked, and it cost far too
much. The waste was not the reviewing — it was rediscovering the same *classes* of
defect in new disguises, because nothing anywhere said what makes a Vision rule hold.

That knowledge existed by round 6 as evidence and nowhere as doctrine. This feature
extracts it.

## Feature Vision

Serves the project Vision's cold-start operability goal at its root: the Vision is the
entry point of the whole Documentation-First chain, and every downstream gate that
claims to check alignment is checking against it. A Vision no cold reader can apply
makes every one of those gates report PASS by construction.

Non-Goals for this feature: not a new phase, not a new artifact, not a validator check.
The discipline is a support file consulted when writing a Vision, plus one procedure at
one existing gate (promotion to APPROVED). Nothing fires on DRAFT edits.

Success signal: a Vision drafted against `vision.md` §1–§4 survives its first blind
round with judgement findings only — no structural class defects (promise-predicates,
undefined subjects, mechanism definitions, unscoped prohibitions, exemptions without
defaults, positive criteria with no headroom).

## Use Cases / User Needs

- **Solo developer using an AI agent** — needs the Vision they write once to still rule
  correctly a year later, without having run six adversarial rounds on it.
- **Team lead needing governance** — needs a rule that a motivated colleague cannot
  reword around; the review evidence shows the difference between such a rule and a
  leaky one is structural and teachable, not a matter of care.
- **Any later reviewer, human or agent** — needs to know *how* to check a Vision, not
  only that they should: the blind-check procedure, with a battery, and the demand for
  the mechanism behind each ruling rather than a verdict.

## Impact

| Path | Change | What |
|---|---|---|
| `skills/agentic-sdlc-skill/vision.md` | ADD | The discipline: nine properties of a rule that holds, five structural clauses around them, the reject/admit asymmetry, minimum operable sections, the five failure classes needing mechanisms, the blind-check procedure |
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Support-file list; Vision Gate routes drafting and promotion through `vision.md` (Standalone and Hybrid/M-VISION); Write-Triggers Vision row names the blind check |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | Vision template restructured to the minimum operable sections, each marked `[gate]` or orientation, with the drafting rule inline |
| `skills/agentic-sdlc-skill/scripts/test_skill_invariants.py` | MODIFY | `test_vision_discipline_wired` — the anchors exist and are reachable from SKILL.md and the template |
| `package.json`, `README.md` | MODIFY | `vision.md` added to the `files` allowlist (a support file not in it never reaches an installed skill), support-file bullet and runtime-shape tree |
| `ai_docs/vision/project_vision.md` | MODIFY | v6 — the five repairs round 6 named, applied to this project's own Vision |
| `ai_docs/audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` | MODIFY | Round 6 evidence + the standing battery |

**Blast radius.** `vision.md` is a new support file: the anti-orphan invariant requires
it to be referenced in `SKILL.md` (done), and the packaging allowlist requires it to be
listed or it silently never installs (done — verified every allowlist entry exists).
`test_support_files_wired` covers both directions. No existing asserted substring was
changed. `sdlc_check.py` untouched.

## Security and Threat Model

Surface: **governance integrity** only — doctrine prose plus one test. No code path, no
input parsing, no network, no credentials.

| Threat | Mitigation |
|---|---|
| T1 — the checklist becomes ceremony: every Vision edit pays a nine-point audit | Scoped to *writing or amending* a Vision, and the blind check only to promotion and to amending an approved one. DRAFT edits pay nothing. The project Vision's own ceremony Non-Goal applies to the skill's own process. |
| T2 — false confidence: a Vision passing the checklist is assumed correct | `vision.md` §5 and §7 state the opposite in the text: the checklist removes structural classes, not judgement errors; expect one round to find real things. Structural compliance without truth is named as a failure no wording fixes. |
| T3 — the battery decays into theater (fixtures kept, never re-run) | The fixtures live in the evidence file next to the findings that produced them, and §5 states the ratchet is the *re-run*, not the list. Not mechanically enforced — declared, not claimed. |
| T4 — the discipline is applied to devPNT M-VISIONs disproportionately | SKILL.md Phase 2 names the gate lens alone as the proportional subset for a milestone-scope document. |

## Action Plan

- [x] Six blind rounds; round 6 asked for the anatomy, not only the findings.
- [x] `vision.md` written from that evidence.
- [x] Wired: SKILL.md (support list, Vision Gate, Write Triggers), templates.md.
- [x] Packaging: allowlist + README bullet + runtime tree.
- [x] Invariant `test_vision_discipline_wired`; battery 57/57.
- [x] Dogfood: this project's Vision to v6 against the same findings.
- [x] Standing battery recorded in the evidence file.

## Test Strategy

- Static battery 57/57 (new invariant added; no existing assertion weakened).
- `sdlc_check.py check` CLEAN, `validate` 0 errors / 4 baseline warnings.
- Packaging verified: every `package.json` `files` entry exists on disk.
- The real test is F-018's success signal and it is **not yet run**: the next Vision
  drafted against `vision.md` should survive its first blind round with judgement
  findings only. Until a Vision is written from scratch under the discipline, the claim
  that it prevents the six-round treadmill is reasoned from evidence, not demonstrated.

## Diary / Current State

**2026-07-27 — complete.** Standalone (devPNT off). Level declared: **L3 · router: no
match**.

The honest shape of what was learned: rules do not hold because they are carefully
written, they hold because of specific mechanisms — a decision question with both
branches answered, counterfactual phrasing, layer-blindness, near-miss verbs enumerated,
forms rather than instances, anticipated re-descriptions named inside the sentence, an
IN/OUT pair, a supremacy clause, exceptions attached affirmatively. Rules fall from a
small, recurring set of defects, the sharpest being **a predicate that is a promise**:
a rule forbidding "committing to track someone's format" is satisfied by saying "we
commit to nothing", while one forbidding "code here that parses a format we do not
define" is not.

The second lesson is asymmetry: **only prohibitions reject, only positives admit**. A
Goal cannot stop anything, so a Vision whose counterweight to scope creep lives in the
Goals has no counterweight. And a positive criterion phrased as an already-true state
cannot be advanced, which makes every proposal citing it undecidable — the reason
ordinary maintenance kept failing the admission test across rounds 3–5.

Limits, stated: the discipline is derived from six rounds against **one** Vision, in one
product domain, with commercial and architectural invariants. It should generalize —
the defects are structural, not domain-specific — but that is an expectation, not
evidence. `vision.md` §7 states the expected cost honestly (one round finds real things,
a second confirms) rather than promising a clean first pass.

**2026-07-27, later — the owner's definition anchors the file.** After reviewing the
work, the owner supplied the definition the six rounds had been circling without
stating: *a Vision is what is to be obtained — the benefit — leaving the most degrees
of freedom possible; it binds nothing that does not obstruct it.* Folded into
`vision.md` as the new opening section (`## What a Vision IS`), with four operational
consequences: benefit-not-mechanism (the test a North Star must pass — from
"best-in-class" no constraint is derivable, which re-explains the round-1 BLOCKER from
the generative side); the **deletion test** as the rule that decides *which* constraints
exist (remove the rule — benefit still reachable? then delete it), also giving the
discipline its stop rule; constraints **accumulate** as work reveals obstacles, which
dissolves the "written first, yet made of decisions" paradox — an almost-empty first
draft is correct, DRAFT informs, APPROVED binds; and a constraint **never obstructs the
Vision** — a conflict is an amendment, owner-owned. Division of labor now explicit: the
deletion test decides WHICH rules exist, the nine properties decide HOW to write one
that holds. `templates.md` (North Star = benefit; Non-Goals derived by deletion test)
and `elicitation.md` (a mechanism is not an acceptable answer to the benefit question)
aligned; invariant extended. Verified against the live Vision: the metering Non-Goal
survives deletion-test scrutiny (remove it → the guarantee's benefit is unreachable),
and the one rule that failed it — the prose rule that could never fire — had already
been moved out in v4 by the adversarial route. The two methods agree, from opposite
directions.
