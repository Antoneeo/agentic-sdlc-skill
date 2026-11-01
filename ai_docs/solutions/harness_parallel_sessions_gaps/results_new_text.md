# F-089 replay — new text, 2026-11-01

Reader: a cold general-purpose subagent of the authoring session, given only `replay.md`,
`cases.md` and the skill directory of worktree `claude/f089-coordination-gaps` with the
F-089 doctrine written, uncommitted on `c1ff546b` (`SKILL.md`, `coordination.md`,
`templates.md`, `dispatch.md`, `hybrid.md`). The author's expected verdicts were not in its
brief. Report condensed; line numbers refer to that tree before the G9 edit below.

| case | verdict | route | file:line | old text (`results_old_text.md`) |
|---|---|---|---|---|
| G1 | FLAGGED | allows (bounded) | coordination.md:106-107, 116-118; SKILL.md:211 | forbids |
| G2 | FLAGGED | allows (own rows, reread, no rewrite) | coordination.md:67-69 | merges only |
| G3 | FLAGGED | routes to Shared, never Regenerated | coordination.md:75-77; templates.md:595 | NOT FLAGGED |
| G4 | FLAGGED | forbids + routes to the holder | coordination.md:72-74, 111-113 | NOT FLAGGED |
| G5 | FLAGGED | forbids | coordination.md:25-27, 49-50, 93 | by implication |
| G6 | FLAGGED | routes (reread before acting) | coordination.md:23-24 | NOT FLAGGED |
| G7 | FLAGGED | routes to the owner | coordination.md:34-35 | NOT FLAGGED |
| G8 | FLAGGED | allows (control) | coordination.md:47-48, 51-52 | FLAGGED |
| G9 | FLAGGED | routes to the coordinator | coordination.md:124-127, 117-118, 166-167 | partly (forbids `index`, no route) |

Every case moved as targeted; the control is unchanged.

Ambiguities the reader named, and what was done:
- **G9** — who writes the merge brief, and the commit map may not exist yet at the part's
  closure. Fixed: when a documents-only part closes, the coordinator writes that unit's
  section of the commit map, and the part's brief takes its table from it.
- **G7** — the status of A's `release` while the owner decides. Left: the owner decides
  (ANALYSIS T6 residual); «leases in force stay» already reads against it.
- **G6** — a session may not tell compaction in place from a new conversation seeded with
  a summary. Left: the client shows it; the reread protects either way.
- **G5** — what the chained session becomes. Left: a part only if the owner gives it a unit;
  the rules on parts then apply.
- **G3** — which units a binary store holds. Left: the coordinator names them from the
  sessions' work; Shared takes free text.
- **G1, G4** — who designates a documents-only part; which record UUS#R170's words go to.
  Left: the part is defined by what it writes; record placement is §1, unchanged.

Bytes (LF), against `c1ff546b`: `coordination.md` +3,961 before the G9 edit (6,941 →
10,902), `SKILL.md` +103, `templates.md` +92.
