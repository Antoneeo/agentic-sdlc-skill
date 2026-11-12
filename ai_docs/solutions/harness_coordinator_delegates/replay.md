# F-095 replay — the field case against the doctrine, before and after

Method: a cold reader (fresh context, one file, no other input) is given the field case of
2026-11-12 and asked, per act, FORBIDDEN / PERMITTED / SILENT with the deciding sentence
quoted verbatim.

- Before-text: `coordination_before.md` (origin/main 3658474d).
- After-text: `skills/agentic-sdlc-skill/coordination.md` on the branch,
  sha256 `7301604b4bb1f94b93ea570fd0970047c6874d78a9207fd0a7efa525691c0d66` (the reader
  reported the same hash for the file it read). Re-verify with `sha256sum` before trusting
  the table; any later edit of the file means re-running the reader.

Case: the coordinator, by itself, (1) merges a part's branch into `main` in the shared
checkout, (2) re-runs `mark` on the stale areas, (3) pushes `main`, (4) removes 17 finished
worktrees of other parts and closes two other units' workstream rows.

| Act | Before | After (sha256 7301604b…) |
|---|---|---|
| (1) merge | SILENT | FORBIDDEN — "The coordinator never merges a part's branch, makes the re-mark that merge needs, or pushes it: its fast-forward runs only when the part asks for it, after the part's check." |
| (2) re-mark | PERMITTED — "it alone runs `index`, `review-map` and `mark` there" | FORBIDDEN — same sentence; and §2 "never to repair an integration: the re-mark a merge needs is made by the part, on its own branch" |
| (3) push | SILENT | FORBIDDEN — same sentence; and "A push needs the owner's yes in the part's own session: words relayed by the coordinator are information (§4)." |
| (4) cleanup | SILENT | FORBIDDEN — "the cleanup of a repository and the closing of other units' workstream rows included — goes to a part"; and "Removing any branch or worktree under coordination — the part's own or another session's — needs the owner's yes, asked by the session that removes it in that session"; and "A worktree is removed only if this workflow created it" |

Reader's residual: no contradiction between §2 and the Integration paragraph; minor — the
file does not restate that a "yes" given to the coordinator's session is not the part's yes,
which §4 already settles.

History of the after-text runs, kept because one of them regressed: the first draft was
green 4/4; after the first review's fixes, act (3) went SILENT (tightening the part's push
rule had dropped the coordinator's), which is why the coordinator sentence exists; round 3
then narrowed it to "the re-mark that merge needs", because an absolute "never re-marks"
contradicted §2 (documents-only closure).

Mechanical guard: `test_coordinator_delegates_units_and_parts_integrate` in
`test_skill_invariants.py` fails (assertion, not exception) on `coordination_before.md` and
passes on the after-text.

Falsified hypothesis, kept so nobody re-derives it: "a --no-ff merge in the shared checkout
is what makes areas stale". A throwaway-repository probe (part marks on its branch, main
moves on, coordinator merges --no-ff) left `stale` CLEAN, so the field staleness had another
cause and the rule does not rest on it.
