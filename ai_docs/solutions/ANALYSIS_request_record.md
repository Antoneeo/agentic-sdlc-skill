---
id: F-067
feature: Verbatim request record before the analysis, in every lens
status: COMPLETED
level: L3
start_date: 2026-10-13
end_date: 2026-10-13
domain: code
---
# Feature Analysis: Verbatim request record

Owner statements for this unit: `audit/requests/REQUEST_request_record.md`, cited `R<n>`.

## Objective

The owner's own words are where the essence of a request lives (R1). Every lens
distils them at once: `elicitation.md` folds answers into the artifact "citing the
reply" (§Ask before the write, §Reflect), an ANALYSIS revision rewrites the whole
document, and later owner decisions — approvals, cost acceptances, rulings — exist
only in the chat. In F-066 both independent reviewers could verify none of the
owner's decisions; the author's attestation was the only source
(`harness_request_record/MOTIVATING_CASE.md`, verbatim report excerpts).

Deliver, at every L3 (code, kb, course) and E3 (marketing) unit, in all four lenses
(R6): `<docs>/audit/requests/REQUEST_[unit].md` — the owner's opening request and every
later owner statement that settles something for the unit (R4), verbatim and
append-only, started before the Vision Gate. "Citing the reply" becomes citing an
entry; reviews receive the record and check owner statements against it.

## Feature Vision

**Precedent first** (`vision/rulings.md`). No row answers "keeps the owner's words for
a unit as the record its artifacts and reviews cite". r25 (F-066) prepares what humans
judge at merge — a different question, and its brief will cite R-entries; r2/r3: a
record holds one unit's quotations, no state, ordering or assignment; r10: it
classifies nothing. → **MISSING → proposed r26 ADMIT**, owner-ruled at closure. Bases:
Goal "keep understanding durable … nothing load-bearing lives only in a transcript";
Goal "never hide a conflict between a user request and the declared Vision" — the
Vision Gate compares the Vision with the request only if the request is on record.

`project_vision.md` APPROVED (v8); no amendment. Actors: Solo developer, Team lead,
Practitioner in a non-code domain (R6).

**Ceremony budget** (Non-Goal "No ceremony ratchet"): one artifact per L3/E3 unit,
one entry per owner decision (written before acting on it), read by reviewers and by a
resuming session; nothing at L1/L2/E1/E2 (R5); nothing removed. Doctrine estimate per
lens: SKILL ~+500, elicitation ~+400, templates ~+1,600, review.md ~+600 (shared) UTF-8
bytes; measured at implementation; the owner's acceptance lands as an R-entry.

Non-goals: no translation, summary or interpretation inside the record; no agent
reasoning; no next-actor or ordering (Non-Goal 1); no triage change; no validator
enforcement of append-only (weighed in the Capability Ledger).

Success signals: in this unit's own reviews no owner statement is CANNOT VERIFY; the
F-066 replay (Test Strategy) resolves what was CANNOT VERIFY.

## Use Cases / User Needs

- **UC1 — Owner asks for a change** (Solo developer / Team lead / Practitioner): their
  words are on record before anyone interprets them. Durability Goal.
- **UC2 — Owner decides along the way** (same): each answer, approval, cost acceptance
  or ruling is on record with the question it answered. Durability Goal.
- **UC3 — Reviewer verifies an artifact** (Team lead's gate): checks each owner
  statement the artifact relies on against the record. "Never hide a conflict" Goal.
- **UC4 — A later session resumes** (Solo developer): reads what was asked, not a
  distillation. Durability Goal.

Grounding: EXISTS — elicitation round, ANALYSIS, Vision Gate, MKT_VISION, evidence
ledger `FACT`, kb `corpus/notes` `origin: elicited`, devPNT proposals, review gates,
`review-map`. NEW — the request record and its R-entries. METAPHOR — none.

## Functional Spec

1. **Start.** On declaring an L3/E3 unit, before the Vision Gate and before the first
   elicitation question, the record starts with R1: the owner's words that opened the
   unit, verbatim — including a clarifying exchange that preceded triage. A unit that
   becomes L3/E3 late starts its record at reclassification, R1 quoting the opening
   words if they are still available; words no longer available are never rebuilt as
   quotations (FS3). A resumed unit appends to its existing record.
2. **What is appended.** Every owner statement that settles something for the unit:
   answers to questions, approvals (Vision promotion, design, scope change, merge,
   release), cost acceptances, precedent rulings, corrections. Each entry: sequential
   id, date, short label, the question it answered as context, the owner's words.
3. **Verbatim.** Original language and spelling; never translated, summarized or
   completed. An omission is marked `[…]`. What the unit does not need and must not be
   committed — credentials, tokens, keys, personal data, confidential third-party or
   employer information — is replaced by `[REDACTED: <kind>]`; what the unit needs
   (e.g. a budget figure) stays. A statement no longer available word for word is
   entered only as `[NOT VERBATIM — from <source>]`, never as a quote.
4. **Append-only.** Entries are never edited, reordered or deleted; a correction is a
   new entry naming the one it corrects.
5. **Citing.** An artifact relying on an owner statement cites its entry; a paraphrase
   may follow the citation, never replace it. A delegation ("your call") is cited the
   same way.
6. **Hybrid.** The record always lives on the filesystem: devPNT holds no owner chat
   statements, so it is no second copy of a governed artifact. Governed artifacts
   (D-UC, E-ISP, M-VISION) cite entries the same way. An approval the owner gives in
   devPNT is not re-quoted: devPNT's record of the resolved proposal is the evidence,
   and an entry, if any, names the proposal instead of quoting.
7. **Unattended.** R1 quotes the trigger that started the unit (the scheduled prompt),
   labelled as such; declared assumptions are not owner statements.
8. **Lifetime.** The record outlives the unit; never deleted at closure.
9. **Review.** A design or closure review receives the record. An owner statement an
   artifact relies on with no resolving entry, an entry the artifact contradicts, or a
   quotation carrying what FS3 redacts, is a finding; with the record handed over,
   owner statements are no longer CANNOT VERIFY.
10. **Lens rails.** Marketing: an owner-given `FACT` cites its entry in the source
    cell (`user, REQUEST_[engagement].md#R3`). Knowledge: an elicited note keeps
    transcribing the domain decision — an export carries topics and their corpus, not
    `audit/` (`portability.md` §0) — and names its entry; the duplicated words are a
    declared copy owned by the record. Code and course have no other rail.
11. **Merge map.** In the merge-review map the record is process evidence.

Acceptance:
- AC1 — under the new doctrine, a fresh agent given an L3 request starts the record
  before asking its first question; under the old doctrine it does not (replay).
- AC2 — given the record, a reviewer of F-066's ANALYSIS resolves the owner statements
  its reviews reported CANNOT VERIFY (replay against MOTIVATING_CASE).
- AC3 — every lens states the trigger, the template and the citing rule, and the
  shared review discipline both asks for the record and checks against it.
- AC4 — the merge map classes the record as evidence.
- AC5 — this unit's own closure review reports no owner statement CANNOT VERIFY.

## Interface Contract

Surfaces: (a) the record — written by the agent, read by owner, reviewers, later
sessions; (b) the agent's reply when the record starts — names it once, so the owner
can correct a quotation; (c) review findings. Idioms reused: append-only log like
`REVIEW_LOG.md`; verbatim source beside a synthesis like a guide's `.sources/`;
`audit/` for process evidence; `file#id` anchors.

Flow: owner speaks → the agent appends the entry before acting on it → artifacts cite
the entry → the reviewer is handed the record and opens cited entries → finding or
conformance → the merge brief cites approval entries. Hybrid: proposal approvals stay
in devPNT and are named, not quoted.

Feedback: one line when the record starts; nothing per entry; a mis-quotation the
owner spots is corrected by a new entry.

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| ask the owner before writing | EXISTS | `elicitation.md` §The question discipline, each lens | read ×4 |
| cite the owner's reply in an artifact | INADEQUATE | `elicitation.md` §Ask before the write "citing the reply", Delegated "quote them" (×4); `review.md` "no owner-authored source" clause | gap: the cited reply has no durable home — inline in artifacts that get rewritten, or only in the chat |
| keep the owner's words unaltered | MISSING | — | grep `verbatim\|user's own words\|REQUEST_` over the four trees: guide `.sources/` (user documents), kb elicited notes (domain decisions), the Delegated clause — none holds a unit's request and decisions |
| class process evidence in the merge map | EXISTS | `sdlc_check.py#classify_path` | prefixes `audit/reviews/`, `audit/HANDOFF_`, `solutions/harness_` |

Append-only enforcement, weighed: a validator check (sequential ids, or a git prefix
comparison) catches reordering but not an edited quotation, needs git for the real
property, and puts code into the shared core of four distributions; the review
against the record catches what matters. Doctrine + review wins; a check is a later
unit if drift appears.

## Impact

| Path | Change | Why |
|---|---|---|
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | Write Triggers row; Phase 1 sentence (start before the Vision Gate) |
| `skills/agentic-sdlc-skill/elicitation.md` | MODIFY | §Ask before the write "citing the reply" and Delegated → cite the entry; §Reflect: recorded first, then folded |
| `skills/agentic-sdlc-skill/templates.md` | MODIFY | record template (FS2–FS4, FS7, redaction, quotes are data) |
| `skills/agentic-sdlc-skill/hybrid.md` | MODIFY | matrix row (FS6) + declared amendment + digest re-stamp |
| kb `SKILL.md`, `elicitation.md`, `templates.md` | MODIFY | same three + FS10 elicited-note line |
| mkt `SKILL.md`, `elicitation.md`, `templates.md`, `hybrid.md` | MODIFY | same at E3/Intake; FS10 `FACT` source example; matrix row + re-stamp |
| course `SKILL.md`, `elicitation.md`, `templates.md` | MODIFY | same |
| `review.md` (shared, ×4 byte-identical) | MODIFY | §Requesting binding input; the "unasked doubt" clause extended (FS9) — one clause, not a second |
| `scripts/shared_manifest.json` ×4 | MODIFY | `shared_files.py --update` |
| `scripts/test_skill_invariants.py` (shared, ×4) | MODIFY | §Requesting input list + AC3 invariant |
| `skills/agentic-sdlc-skill/scripts/sdlc_check.py` | MODIFY | `classify_path` EVIDENCE prefix; EVIDENCE instruction worded for any cited evidence |
| `skills/agentic-sdlc-skill/scripts/test_review_map.py` | MODIFY | AC4 |
| `CHANGELOG.md` ×4; root `README.md` (L3-closure bullet) | MODIFY | release notes; derived doc |
| `ai_docs/strategic/skill_family_agent_workflows.md` | MODIFY | spine section |
| `ai_docs/vision/rulings.md`, `existing_features.md`, `audit/audit_plan.md` | MODIFY at closure | r26; catalog; `mark` last |

Blast radius: `review.md` — read whole by every agent review (the REVIEW MANDATE) and
by tests: grep `read("review.md")` gives 12 in `test_skill_invariants`, 1 in
`test_domain_rules`; mostly `assertIn`, but index slicing in the ladder and mandate
tests and a backticked-token scan for capability tiers — the new wording carries no
backticked tier name and keeps the sliced anchors; `test_drift`/manifest pin the four
copies. Each lens's `elicitation.md` is lens-owned (not shared): no cross-lens test
reads it. `hybrid.md` ×2: the moved-block digest invariant. `classify_path`: one
caller (`cmd_review_map`) + its test.

Populations at rest: no-migration — merged units get no retroactive record; the open
workstreams (C-001, F-015, F-062, F-063) start one at their next owner decision (FS1,
late start). Other triggers: no. Residual: their earlier decisions stay
transcript-only — not healed, by R5's scope.

## Security and Threat Model

Surface: personal and confidential data committed to the repository.
- T1 a credential, personal datum or confidential third-party/employer fact committed
  verbatim: FS3 redaction; template rule; FS9 makes it a review finding.
- T2 a fabricated or altered quotation: written before acting, question quoted,
  append-only, compared by the reviewer, path shown to the owner. Residual: the author
  is still the transcriber (declared in the template).
- T3 instruction injection from quoted text: the template header states quotations
  are data and never instructions to a later agent.

## Action Plan

- [x] Scoped re-review; owner approves the design and the cost estimate (R-entry).
- [x] AC1 RED replay; RED tests (AC3, AC4); doctrine ×4, review.md sync, hybrid ×2,
      `classify_path`; bytes → Diary; owner confirms (R-entry).
- [x] AC1 GREEN + AC2 replays; batteries ×4; closure review; r26; `mark` last.

## Test Strategy

AC1, AC2: fresh-subagent replays, prompts and outputs kept in
`harness_request_record/` (`REPLAY.md`), RED under the old doctrine, GREEN under the
new. AC3: invariant across the four lenses + the §Requesting list. AC4:
`test_review_map.py`. AC5: this unit's closure review. Full battery per distribution.

## Diary / Current State

- 2026-10-13 — opened (R2); elicitation R4–R6; record started first. Design review
  round 1 FAIL; this revision answers it.
- 2026-10-13 — design PASS (round 2); owner approved (R7). AC1 RED replay: NO.
  RED tests 3/3 → GREEN; batteries code 246, kb 421, mkt 258, course 252 OK.
  Doctrine bytes (UTF-8 LF) per lens — code: SKILL +553, elicitation +295,
  templates +1871, hybrid +324; kb: SKILL +882, elicitation +297, templates +2020;
  mkt: SKILL +491, elicitation +284, templates +1827, hybrid +373; course: SKILL
  +479, elicitation +309, templates +1741; review.md +559 (shared, ×4).
- 2026-10-13 — AC1 GREEN (YES), AC2 GREEN (13/13); owner confirmed cost (R8), r26
  ADMIT (R9). Closure review round 1 FAIL (B1: the reply never named the record);
  fixed in all four templates with the WARNs; final bytes — SKILL +562/+890/+491/+479,
  templates +2170/+2233/+2078/+1954 (code/kb/mkt/course); owner re-confirmed (R10).
