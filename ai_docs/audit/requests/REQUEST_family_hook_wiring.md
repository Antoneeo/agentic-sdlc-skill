---
description: Request record for F-093 - sibling lenses' machine-wide hooks on a multi-lens install.
status: CURRENT
analysis: ANALYSIS_family_hook_wiring.md
---
# Request record: family hook wiring (F-093)

### R1 — 2026-11-08 — opening request (relayed by the coordinating session)

The owner's words were not relayed verbatim; the coordinating session (D:\kb) wrote the
brief after the owner said a session that never used kb-agentic was useless and doubted the
skill setup for every installer. Quoted from that brief:

> Verify, and if confirmed fix, a suspected installer defect: when several skills of the
> family are installed (agentic-sdlc, kb-agentic, mkt-agentic-sdlc, course-creator), only the
> first one's machine-wide hook of each kind gets wired, and the others are silently skipped
> as if the user had opted out.

> Also decide whether the family wants one remind per lens or one lens-aware remind [...];
> if the design intends one shared remind, the defect is that the shared line is
> agentic-sdlc's code-specific one — say which and why from the repo's own rulings/docs.

> Do not touch `~/.claude/settings.json` or `~/.agentic-sdlc/` on this PC, do not publish to
> npm, do not push or merge. Report in Italian to Antonio.

Scope: diagnosis, reproducing test, fix on the branch if confirmed. No release.

### R2 — 2026-11-08 — design approved (option A); costs of B asked

> A ora. Per B vorrei sapere quali sarebbero i costi, è un grosso problema leggere ad ogni turno la cartella delle skill?

Reply to the three options in ANALYSIS_family_hook_wiring.md. Approves option A (kb and
marketing installers wire the per-turn reminder, family dedup kept). Option B is not
approved: the owner asks for its costs, in particular of reading the skills directory every
turn.
