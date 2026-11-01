# F-089 replay — old text (baseline), 2026-11-01

Reader: a cold general-purpose subagent of the authoring session, given only `replay.md`,
`cases.md` and the skill directory of worktree `claude/f089-coordination-gaps` at `c1ff546b`
(release 1.51.0: `SKILL.md`, `coordination.md`, `templates.md`, `dispatch.md`, `hybrid.md`).
The author's expected verdicts were not in its brief. Report condensed; line numbers refer to
that tree.

| case | verdict | route | file:line | what it misses |
|---|---|---|---|---|
| G1 | FLAGGED | forbids | coordination.md:72-73; SKILL.md:211 | no exception for a documents-only session; the two texts pull apart («writes no code there» vs unconditional «own git worktree») |
| G2 | FLAGGED | allows; routes to Shared | templates.md:808-809, 593-594 | covers merges between branches, not several sessions appending in one checkout; §1's heading «Every record has one writer» can be misread onto the review log |
| G3 | NOT FLAGGED | — | (resembles) coordination.md:134-137 | nothing places `.devpnt/*.db` in a commit map: Shared, Regenerated or Left out |
| G4 | NOT FLAGGED | — | (resembles) coordination.md:73-75 | «code» is undefined for the lease; whether a catalog fix by another session is forbidden depends on it |
| G5 | FLAGGED | forbids (by implication) | coordination.md:11-13, 15 | succession inside a chain is unsaid; «the session the owner named» only points against it |
| G6 | NOT FLAGGED | — | (resembles) dispatch.md:121-124 | the reread-after-compaction rule is for the dispatch ledger only; nothing sends the coordinator to `leases.md` over its summary |
| G7 | NOT FLAGGED | — | (resembles) coordination.md:59-60 | no succession: whether a new naming revokes the old, how the old learns of it, what happens to `leases.md`'s opening citation and to leases it granted |
| G8 | FLAGGED | allows (record before acting) | coordination.md:30-31, 34-35 | — (control) |

## G9, replayed on the old text with the new-text run (2026-11-01)

Same reader set-up, a separate cold subagent given the five files of `c1ff546b` and only G1 and G9.

| case | verdict | route | file:line | what it misses |
|---|---|---|---|---|
| G1 | FLAGGED | forbids | SKILL.md:211; coordination.md:71-72 | confirms the first run |
| G9 | FLAGGED, partly | forbids `index` only | SKILL.md:211 | names nobody to run `index` instead, while closure needs it twice (SKILL.md:232, :242); no rule for `review-map` or `mark` in a shared checkout; the closure message hands no steps over |
