---
workstream: F-049 the floor reaches the author (authoring is a deep-floor role; disclosure, not routing)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-10
next: owner's integration call; six commits now sit unpushed
details: ANALYSIS_authoring_floor.md; harness_authoring_floor/probe.py; ADR_2026-09-11_authoring_floor.md
updated: 2026-09-11
---

## Resume logistics

Implemented, uncommitted on `main`: the authoring row in `review.md`'s floor table,
the session rule, the discouraged-combination clause with its arbitration
exception, the fail-open clause; a pointer at the head of Standalone L3 in
`SKILL.md`; the user-facing "Which model to run it on" section in all three
READMEs; four battery pins. Spine ported x3, manifests regenerated. Owner accepted
the ceremony cost 2026-09-11 (ledger r23).

## What the two reviews changed, and it was three of my own claims

- **The rule was unreachable at the moment it binds.** Its only home was
  `review.md`, which `SKILL.md` loads at the design-review gate -- i.e. AFTER the
  artifact is authored. A compliant agent would have met the authoring floor one
  phase too late. Now `SKILL.md` carries the pointer at the head of Phase 3.
- **"Checkable in the log" was false.** The `model` cell records the REVIEW's
  tier; no column holds the authoring session's, and nothing told the writer to
  record it. So the forbidden pair could never both be visible. The disclosure now
  lands in the existing `reviewer` cell (Hybrid: `notes`) -- no new column, which
  is what the accepted ceremony bought -- and the claim is restated as what it is:
  readable by a human, not parseable by a script.
- **The forbidden combination contradicted F-048's arbitration.** Both reviewers
  found it independently, in a configuration that arbitration itself names: a
  subagent facility pinned to a cheap model plus an under-tiered session. My rule
  forbade the state; "independence wins" mandates it and calls the alternative
  worse. Now the exception is explicit and the combination is the worst admissible
  state, not a violation.

## The honest limit, now written into the doctrine

A session knows its model NAME; tiers are deliberately client-relative and the
skill maps no name to a tier. So the agent-facing half fires only where a session
can recognize its own tier -- which is also the session least likely to run the
check. **The reliably working half is the README telling the USER**, and the
doctrine now says so instead of implying more coverage than it has.
