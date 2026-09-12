---
workstream: F-054 kb recall multi-slug verdict (the false-negative claim was refuted; the verdict form was the real gap)
level: L2
branch: main
status: DONE, UNRELEASED
since: 2026-09-12
next: owner's integration call; kb-only delta, so a single-package release when they call it
details: SPIKE_kb_recall_second_instrument.md (the negative spike this unit came out of); harness_kb_recall_probe/{probe.py,replay_2026-09-12.md}
updated: 2026-09-12
---

## Resume logistics

Implemented, uncommitted on `main`, kb lens only — the recall verdicts live in
`distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` and in no other
lens, so code and mkt are untouched and this is a single-package release.

Four files:

- `SKILL.md` §Topic Recall — both node-naming verdicts now read
  `kb: <slug>[, <slug> …] → …`, with the reason on the record. **Four legal values,
  unchanged**: the repair is the form, never a fifth value.
- `scripts/test_kb_recall.py` — two anchors added to the existing recall-clause list
  plus `test_the_verdict_form_admits_every_branch_the_descent_opened`, which also pins
  the vocabulary size against creep.
- `evals/scenarios/recall_verdict_names_every_branch.md` — the behavioural scenario;
  its fixture IS the spike's run-2 KB, so the scenario replays the case that motivated
  the change rather than a restatement of it.
- `evals/run_behavioral.py` — the L1 fixed in passing (below).

Evidence: kb static battery **383 tests, OK (14 skipped)**. The new invariant proven
**red against `HEAD`** before the edit and green in the working tree, with the
"Four legal values" count identical on both sides. Both recall scenarios exit 0 under
the driver.

## The unit is what survived a refutation

This started as a severity-high claim of mine: the recall's four verdicts sit
downstream of one instrument, so a wrong-branch descent yields a false
`kb: no coverage`. Two agent-level replays refuted it — including one fixture built
to be hostile, eight topics with a more plausible decoy branch. The descent judges
semantic coverage of concepts (not term presence), it is multi-branch by mandate, and
run 2 ran a `grep` cross-check **unprompted**. The mandated probe and the claims
inventory were abandoned with the claim, after the owner had already accepted a cost
priced on my framing — the correction was surfaced before anything was written.

What the replays DID reproduce is this unit: run 2 had to invent
`kb: gdpr_compliance, observability → 2 claims cited` and said so, because the
doctrine mandates descending every candidate branch and gave no legal form to declare
more than one. Full record in `SPIKE_kb_recall_second_instrument.md`.

## The L1 fixed in passing, and why it was not optional

`run_behavioral.py` read scenarios as UTF-8 and printed them to a cp1252 console,
raising `UnicodeEncodeError` on `→`. The shipped scenario
`recall_descends_before_answering.md` already contains that character, so on a default
Windows console that eval had been **un-runnable since kb 1.7.0** and the driver died
before printing its own pass criteria. `sys.stdout.reconfigure(encoding="utf-8",
errors="replace")`, guarded for exotic streams. It was a prerequisite: this unit's own
scenario could not be verified without it.

## Not done here, deliberately

No CHANGELOG entry and no version bump — the release is the owner's act per
`GUIDE_release.md`, as with every other UNRELEASED row. No ADR: the multi-slug form
took no architectural decision, it repaired a form the doctrine already required
producing (no decision, no ADR).
