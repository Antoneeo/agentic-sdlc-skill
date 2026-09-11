---
workstream: F-052 the read diet applied per lens (mkt extracted; kb measured and deliberately NOT extracted)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-11
next: owner's integration call; four commits now sit unpushed
details: ANALYSIS_mkt_read_diet.md; harness_mkt_read_diet/probe.py
updated: 2026-09-11
---

## Resume logistics

Implemented, uncommitted on `main`: mkt's Hybrid seam moved verbatim to
`distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/hybrid.md`, pointer with
trigger and consequence in its place, declared in the lens profile, the package
allowlist and the README's `## Modes` section; the dangling
`ENFORCEMENT.md` citation repointed; the shared conservation check generalized.

mkt mandatory read: **23,120 → 21,215 bytes (−8.2%)** Standalone; Hybrid rises to
24,653 (+6.6%). Run the probe rather than trusting these lines — the first draft of
this file carried a figure taken before the last pointer edit, which the closure
review caught.

## The gravest finding of the unit, and it was mine

F-051 shipped a **mojibake-corrupted `hybrid.md`** in the code lens: six sequences
where UTF-8 had been decoded through the Windows console codepage and re-encoded.
I introduced it in the step that "rebuilt the file verbatim" using `git show`
without an explicit encoding — and then, in F-052, recorded THAT file's digest as
the certified reference, which would have frozen the corruption permanently. The
design review caught both. The file is rebuilt from the pre-move source and the
digest now comes from the source, never from the artifact it is meant to check.

## kb: measured, decided, NOT done

kb's entire Hybrid material is **299 bytes** — a mode subsection, no Coexistence
section at all. The pointer F-051 shipped costs **1,282 bytes** (979 pointer +
303 support-list line). Extracting kb would therefore **grow** its `SKILL.md` by
983 bytes (+3.4%) and add a twelfth support file plus an allowlist entry to
maintain. That is the diet's own rule refusing the diet, and probe P6 asserts kb
still carries its block inline so nobody later "finishes the job" without
redoing the measurement.

## What this unit found in its own instruments

Three defects, all in the harnesses rather than the product — the fourth, fifth
and sixth of this session:

1. **A shared check carrying one lens's assumptions.** F-051's conservation test
   hardcoded the code lens's headings (`### Shadow discipline (Hybrid)` and
   friends), which mkt's seam does not contain. It now DERIVES its anchors from
   whatever that lens actually moved, and additionally asserts that moved table
   ROWS left the contract — a heading can survive while its substance does not.
2. **`subprocess` without an explicit encoding.** Both probes shelled out to
   `git show` with `text=True` and no `encoding=`, so on Windows git's UTF-8 was
   decoded through the console codepage and em-dashes became replacement
   characters. It produced a false FAIL here; it could as easily have produced a
   false PASS.
3. **A conservation proof anchored to a moving reference.** P3c compared against
   `git show HEAD:` — which stops proving anything the moment the unit is
   committed, because HEAD then IS the post-move state. Both probes now anchor on
   a recorded sha256 of the moved block, which is environment-free and does not
   move.

## Inbound citations, swept BEFORE the move this time

F-051's blocking finding was that its weighing never asked who cites the moved
sections. Run first here, the sweep found mkt's `ENFORCEMENT.md` citing "the
SKILL.md shadow discipline" — a section that has **never existed in mkt**, a
pre-existing defect that shipped. Repointed.
