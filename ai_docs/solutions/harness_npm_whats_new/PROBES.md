---
description: F-070 probes — publish_all.bat run against an npm stub (skip path, refusal path) and npm's rendering of README HTML comments.
status: CURRENT
---
# F-070 probes

`npm_stub.js` (called by `npm.cmd`) stands in for `npm`; `run_publish_probe.cmd
all|none <repo> <log>` puts this folder first on PATH and answers publish_all.bat's
prompt. `publish` is only logged: nothing reaches a registry.

## P1 — the registry skip comes first (2026-10-27, `publish_all.bat` at 20a92ef8)

`run_publish_probe.cmd all …` → `p1.out`, `p1.log`: four `[ok] … already on the
registry - skipped`, verify `[ok]` ×4, exit 0, **0 publish calls**. To re-run after
the FS4 change: same command, same expected result.

## FS4 — refusal before publish (RED baseline, 2026-10-27, 20a92ef8)

`run_publish_probe.cmd none …` → `red.out`, `red.log`: the current script publishes
all four packages at versions with no `### What's new` (**4 publish calls**; the
verify then fails only because the stub's registry stays empty). GREEN after the change: on a tree whose
versions carry no notes, `[FAIL]` names the code package and **0 publish calls**.

## GREEN after the change (2026-10-28, working tree on 20a92ef8)

Logs went to the session scratchpad (absolute paths); the outputs are kept here.

- **P1** — `run_publish_probe.cmd all <repo> <abs log>` → `green_p1.out`: four skips,
  verify `[ok]` ×4, exit 0, **0 publish calls**; the new check is never reached.
- **FS4 refusal** — `run_publish_probe.cmd none <repo> <abs log>` → `green_refusal.out`:
  `[FAIL] @antoneeo/agentic-sdlc-skill 1.49.0: no "What's new" for 1.49.0 …`, then the
  publish run's own `[FAIL] … not published`, exit 1, **0 publish calls**.
- **Positive path and per-package stop** — `make_notes_tree.py <empty scratch dir>`
  copies the publish inputs and gives only the code package's 1.49.0 a `### What's new`;
  `run_publish_probe.cmd none <that dir> <abs log>` → `green_notes.out`: code passes the
  check and reaches the stub's `publish --tag latest` (**1 publish call**), kb is refused
  next. This is ANALYSIS T3's residual, shown: an earlier package is already out when a
  later one is refused, which the pre-tag check exists to prevent.
- **A10 / P3** — `probe_readmes.py` (from the repository root): each moved F-057 block is
  identical to its text at `HEAD`, and undoing the change in memory gives `HEAD`'s README
  exactly, for all four READMEs.

## FS1/FS2 — npm hides HTML comments (2026-10-27)

`npm view all-contributors-cli readme` opens with three top-level `<!-- … -->` lines
outside any code fence. Its page `https://www.npmjs.com/package/all-contributors-cli`,
read in a browser: the `#readme` element's text and HTML contain neither `<!--` nor
the comment text ("START doctoc"). npm drops the comments when rendering, so empty
markers and the generated comment show nothing on the page.
