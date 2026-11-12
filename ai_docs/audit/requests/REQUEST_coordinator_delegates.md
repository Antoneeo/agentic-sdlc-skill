---
description: Request record for F-095 - under coordination the coordinator does not do a part's work, and a part integrates its own branch.
status: CURRENT
analysis: ANALYSIS_coordinator_delegates.md
---
# Request record: the coordinator does not do a part's work (F-095)

### R1 — 2026-11-12 — opening request

Field case first. On 2026-11-12 the named coordinator (the D:\kb session) cleaned this
repository itself (closed two workstream rows, removed 17 worktrees, deleted 22 branches),
then merged the F-094 part's branch into `main`, re-marked the areas the merge made stale,
amended a commit against the validator's warning, and pushed. It declared no level and no
router verdict for any of it. Asked whether it had followed the guide, it answered no; the
owner then said:

> qui secondo me il problema è che tu hai fatto qualcosa che avresti dovuto delegare, non credi?

and, after the coordinator agreed:

> si ma la skill spiega come si delega.. ma forse non spiega questo

### R2 — 2026-11-12 — do it in the coordinator session

The coordinator proposed a separate session for the unit. The owner:

> Esegui questa attività qui: “Il coordinatore non fa il lavoro delle parti”

Scope: doctrine in `coordination.md` (the only lens that carries coordination), a probe, an
eval scenario, tests, commit on the branch. No release; merge and push wait for the owner.

### R3 — 2026-11-12 — integrate and push

After the summary (review FAIL, FAIL, PASS; three WARN fixed after the cap), the owner:

> Sì, integra e push
