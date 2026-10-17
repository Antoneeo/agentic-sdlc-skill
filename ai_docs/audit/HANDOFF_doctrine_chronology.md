---
workstream: F-073 readable chronology and parallel workstreams (doctrine)
level: L3
branch: doctrine-chronology
status: PLANNED
since: 2026-10-17
next: measure the parallel-workstream issues (a)-(c), then write ANALYSIS_doctrine_chronology.md through the design review
details: REQUEST_doctrine_chronology.md · harness_doctrine_chronology/misura_cronologia_2026-10-17.md
updated: 2026-10-17
---

## Resume logistics

Nothing is implemented. This branch carries the request record, the measurement and
this brief, so the work can start on the owner's other machine (R5): `git fetch`, then
work on branch `doctrine-chronology` (it was cut from `main` at c2e9d33).

**The task.** L3 doctrine change across the family (shared spine files change in all
four distributions via `shared_files.py`; `reference/GUIDE_release.md` governs
packaging; design review before code). Read `README.md`, `audit/handoff.md`,
`reference/INDEX.md`, `vision/project_vision.md` and `vision/rulings.md` first. The
Vision v9 amendment (read-only state view) is applied on branch `feat/kb-site-spec`; if
it is not on `main` yet, note it and do not depend on it.

**Measured** (`solutions/harness_doctrine_chronology/misura_cronologia_2026-10-17.md`):
"what did we do this week, and when" cannot be read reliably from documents. Diary
entries come in 15 forms; `next:` has become a state summary in a field project (median
500 characters, maximum 7,540) that paraphrases what the Diary dates; work without its
own ANALYSIS (release, fix, spike) leaves no dated entry in this repository (6 of 12
unit-days covered).

**Observed, to measure before designing** (R3):
- (a) feature ids are chosen from the local checkout and collide across branches —
  F-069 was taken on `main` while `feat/kb-site-spec` used it, and was renumbered F-072;
- (b) hand-written append-only shared files (`audit/reviews/REVIEW_LOG.md`,
  `audit/project_notes.md`, `vision/rulings.md`, shared KB topic nodes) conflict at
  merge across branches;
- (c) two sessions on the same checkout: the doctrine says nothing.
Measure on this repository's history (branches, merge conflicts, id reuse) and on the
field project, read-only, then propose the smallest mechanism for each (for example an
id-uniqueness check against `origin`, a merge strategy for append-only logs) or record
why none is needed.

**Starting proposal from the measurement** (verify, weigh and refine — not to copy):
`validate` checks that every Diary entry starts with one date format; `next:` holds only
the next step, with a length warning, and state goes to the Diary; work without an
ANALYSIS leaves a dated line in `project_notes` (no new mandatory document).

**Constraints.** The ceremony budget (Non-Goal "No ceremony ratchet"): any new check at
L2/L3 states its cost or removes a comparable one; nothing at L1. F-072's chronology
depends on this unit's rules. Commit on this branch with the owner's approval; ask
before pushing or merging.

**Done for the first session** = measurements of (a)–(c) and an ANALYSIS with the
proposed rules and their checks, through the design review; then report to the owner.
