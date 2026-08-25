---
workstream: F-036 Init Wires the Orientation Hook
level: L3
branch: feat/init-wires-orient-hook
status: DONE, AWAITING MERGE
since: 2026-08-25
next: the owner's merge call (closure review PASSED after one rework round)
details: ANALYSIS_init_wires_orient_hook.md
updated: 2026-08-25
---

## Resume state

Branch `feat/init-wires-orient-hook`, cut from `main`@5f14f24. Code, tests and doctrine
complete in all three distributions.

`wireOrientHook()` / `orientHookCommand()` live in `lib.js` (byte-identical in the three
copies, verified by hash); `init.js` calls them for Claude Code only. Seven result codes:
`wired | already | broken | malformed | no-validator | no-python | unquotable` — data,
never printed text, so the battery asserts on the code and `init.js` owns the wording.

Verified: Python batteries 3/3 OK, `node test_clients.js` 20 pass in each of the three,
end-to-end init in a scratch project wired the hook AND the wired command was executed
and produced real orientation (exit 0).

## Watch out

- **The three `init.js` / `lib.js` / `test_clients.js` copies are NOT in the drift
  guard** and have already diverged (245/237/235 lines). `test_skill_invariants.py` IS
  shared, so editing it required `shared_files.py --update` plus copying the regenerated
  manifest into the other two. Folding the installers into the drift guard is worth its
  own unit and is not done here.
- **mkt ships `mkt_check.py`, not `sdlc_check.py`.** The first draft hard-coded the
  latter, so the mkt copy would have reported `no-validator` forever. The entry point is
  now derived — `test_clients.js` already had that convention (`ENTRY_POINT_FILE`) and
  following it is what caught the bug.
- **The docs-root label differs too** (`mkt_docs`), so the hook's `statusMessage` is a
  caller-supplied option rather than a constant.
- Only Claude Code is wired. Codex/Gemini deliberately left to the manual snippet: no
  fixture in this repo pins their hook schema.

## Owed

- Closure review DONE at rung 1 (two parallel subagents, FAIL then reworked); see
  `reviews/REVIEW_LOG.md`. Rung 2 remains unavailable on this machine.
- Not in this unit, named so they are not lost: **the broken hook in
  `D:\SoftwareDev\skill_sdlc\kb-agentic-skill/.claude/settings.json`** (points at
  `skills/agentic-sdlc-skill/...`, a path that tree does not have — this is the probable
  cause of the field incident and needs a one-line correction in that repo); and
  **mkt's ENFORCEMENT 4 example names `.claude/skills/agentic-sdlc/scripts/mkt_check.py`**,
  the wrong skill directory for that lens.
