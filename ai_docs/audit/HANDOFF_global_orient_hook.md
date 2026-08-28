---
workstream: F-042 Global orient hook at install time (UX fix of the F-041 note)
level: L3
branch: feat/global-orient-hook
status: DONE, AWAITING MERGE
since: 2026-08-28
next: the owner's merge call (closure PASS in 1 round, 0 BLOCK, 3 WARN folded; JS 50x3, python 184/316/202, gate CLEAN)
details: ANALYSIS_global_orient_hook.md; the owner's design ruling is below
updated: 2026-08-28
---

## The owner's ruling (this session, 2026-08-28)

The F-041 check note produced, in the field, an agent question a normal user
cannot evaluate ("manca l'hook di orientamento sessione (ENFORCEMENT §4) — lo
configuro?"). The owner rejected both consent-rephrasing and mid-session silent
repair, and ruled for the third way he proposed himself: **the install/update
script wires the hook** — at the USER level (`~/.claude/settings.json`), which
the installer knows exactly, covering every project on the machine. Consent is
the npm install itself; the incomprehensible question disappears.

## Design constraints agreed in-session

- `orient` is fail-open (no docs root → silent, exit 0, pinned by tests), so a
  global hook is safe by construction on non-managed projects.
- **Idempotent**: never add when ANY family orient hook already exists in the
  user settings (the F-041 detection predicate, JS side already has it).
- **Never re-add after deliberate removal**: wire only once per machine (a
  marker records "already wired once"); updates never re-add.
- **Multi-lens dedup**: one global hook per machine — first installed lens wins.
- **Claude Code only** for the auto-write; Codex/Antigravity keep the manual
  snippet (family rule: never write a hook schema no fixture pins).
- The check note stays as the residual net and still needs the user-language
  rewrite (part of this unit).
