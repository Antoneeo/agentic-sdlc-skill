# F-098 inventory: where the four lenses assume a team shape or a role

Taken on 2026-11-15 by a read-only subagent over the doctrine files of the four lenses
(`skills/agentic-sdlc-skill/`, `distributions/kb-agentic-skill/skills/kb-agentic-skill/`,
`distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/`,
`distributions/course-creator/skills/course-creator/`), commit 2f007f36. Condensed here to
the facts the design uses; every one is re-derivable with the grep or the file named.

## Files, by how the lenses carry them (`scripts/shared_files.py`, `SHARED_FILES`)

- Byte-identical in the four lenses: `review.md`, `routing.md`, `vision.md`, `guides.md`,
  `dispatch.md`, `memory.md`; `scripts/sdlc_core.py`, `scripts/shared_files.py`,
  `scripts/test_session_start.py`, `scripts/test_skill_invariants.py`,
  `scripts/test_drift.py`.
- Different in each lens, on purpose: `SKILL.md`, `templates.md`, `ENFORCEMENT.md`,
  `elicitation.md`.
- Code lens only: `coordination.md`, `architect.md`, `tdd.md`, `debugging.md`.
  `hybrid.md`: code and marketing.
- No sibling lens mentions "coordination" or "leases". Their REQUEST templates keep the
  delegated and received entries and drop the pointer to `coordination.md`.

## The decider's name, by lens

Code: "owner" or "user". Knowledge: "practitioner". Marketing: "client" or "user".
Course: "person" or "owner". The shared files say "owner" or "user" in every lens.

## Where a role or a shape is assumed (file — section — what it assumes)

Who decides, what stays with the owner:
- `elicitation.md` — §The legality test: "what the user uniquely owns" (benefit,
  priorities, non-goals, acceptance, the reserved approvals); the knowledge and course
  lenses do not list the approvals, they say "the approvals doctrine reserves to them".
  §Ask before the write: the Delegated case ("the user's own words handed you this
  choice"). §When a doubt emerges: "Design is yours until it trades off something the
  user owns".
- `review.md` — "The owner approves the design before the work starts"; "a PASS is not an
  approval to merge — the human owns that"; the gated rung is the user's call.
- `SKILL.md`, every lens — Vision promotion only on the user's confirmation; the design
  approval; integration and deletion are the owner's (code: Phase 5 destructive guards;
  knowledge: "the integration choice is the practitioner's"; course: "the project owner's
  integration choice"; marketing: nodes DONE "only after the user accepts").
- `vision.md` — the owner interview and its two gates.

Members and how work passes:
- `coordination.md` (code) — coordinator and parts, leases, the closure message, relayed
  words as information, the shared checkout.
- `dispatch.md` — orchestrator and subagents; "An open point whose answer changes the
  work is not yours to decide: return it"; §What may be delegated at all.
- `SKILL.md` Phase 4, every lens — own git worktree when another session may use the
  checkout; subagent execution opt-in.
- `simulation.md` (course) — principal author/coordinator, independent readers,
  independent didactic reviewer: the roles of one procedure.
- `templates.md` — REQUEST labelled entries (`decided under delegation`, `received for`);
  code only: `leases.md`, commit map, E2E tester, merge-review integrator; marketing:
  `Owner` columns and "who writes, who runs ads" (the client's own people, content of the
  plan); course: SIMULATION_REPORT roles.

What does not travel:
- `coordination.md` §4 (code only): an authorization for a gated act is valid only in the
  session the owner gave it to.
- `review.md` — the gated rung keeps no grant memory.
- `SKILL.md` §1, every lens — a brief from another session is a summary (F-096).
- knowledge lens — `portability.md`, `reconciliation.md`: another project's owner ruling
  does not bind here.

Nothing in any lens asks the owner how the team is made.

## Tests that pin these texts (`skills/agentic-sdlc-skill/scripts/`)

- `test_skill_invariants.py`: `test_support_files_wired`,
  `test_every_support_file_on_disk_is_declared`,
  `test_every_support_file_is_in_the_package`, `test_question_discipline_wired` (twenty
  anchors), `test_capability_floor_and_delegation_boundary`,
  `WorkingModelDoctrine.test_coordinator_delegates_units_and_parts_integrate` (code lens),
  `F096_HonestSignals.test_resume_from_a_summary_re_reads_the_unit`,
  `test_request_record_is_stated_in_every_lens`, `test_human_approval_rule_in_every_lens`.
- `test_design_approval.py`: the design-approval paragraph of `review.md` and each lens's
  pointer to it.
- `test_drift.py`: the hash of every `SHARED_FILES` entry, in the four trees.
- `test_session_start.py`: the orientation's order (triage, resume line, lens line, guide
  router, workstream registry, README, read on demand) and its bounds
  (`ORIENT_MAX_TOTAL_CHARS` 9500, `ORIENT_APPEND_RESERVE` 2000).

## The orientation (`sdlc_core.py::cmd_orient`)

Fixed head: banner, blank line, triage line, resume line, and the sibling-lens line when
siblings are installed. Body: guide router (cap 3000), workstream registry (cap 2600),
README (the remaining room). Tail: read-on-demand pointers, wiring notes, the Hybrid line.
The body budget is the spine's share minus head and tail, so a line added to the head
comes out of the body's room. The knowledge layer appends its own lines after it, within
the reserve.
