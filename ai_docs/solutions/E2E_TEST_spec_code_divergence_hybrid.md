---
feature: F-081
analysis: ANALYSIS_spec_code_divergence_hybrid.md
---
# E2E test: Spec/code divergence marker in Hybrid projects

## What changed, in user terms

In a project that uses devPNT, a knowledge-base claim can now say "the code does not
do this yet" by pointing at the devPNT design that put the fix off, through its shadow
file in `solutions/`. `check` reads the newest shadow of that design and refuses the
mark when no shadow exists or the newest one does not mention the claim. Standalone
projects are unchanged.

## Environment and preconditions

- The packages built from the merged commit (code and kb lenses installed side by
  side), Python 3 on the path.
- A scratch project with `ai_docs/`, one source in `corpus/given/` (any short text
  file), and a topic `topics/export.md` holding one claim from it. Use
  `sdlc_check.py anchor` and `claim-id --fill` to make the row valid, then confirm
  `sdlc_check.py check` is CLEAN before starting. Note the claim id.
- devPNT itself is not needed: shadows are plain files you create by hand here.

## New-behavior scenarios

### S1 — FS3: a Hybrid marker with no shadow is refused
Steps:
1. Set the claim's `about` cell to `not-yet-honored-by -> SHADOW_e_isp_export`.
2. Run `python <code skill>/scripts/sdlc_check.py check --root .`.

Expected: `check` fails with one line naming
`solutions/SHADOW_e_isp_export_v<X.Y>.md` and telling you to export the shadow from
the accepted devPNT version or remove the marker.

Result:

### S2 — FS3: a shadow without a version suffix is named, not read
Steps:
1. Create `ai_docs/solutions/SHADOW_e_isp_export.md` containing the claim id.
2. Run `check`.

Expected: the same error as S1, now also naming `SHADOW_e_isp_export.md` as not
named `_vX.Y`.

Result:

### S3 — FS1/FS4: the newest shadow cites the claim, clean
Steps:
1. Delete the file from S2. Create `ai_docs/solutions/SHADOW_e_isp_export_v1.0.md`
   whose first line is `<!-- SHADOW generated from devPNT (e_isp_export v1.0) - do not
   edit by hand -->` and whose body contains the claim id.
2. Run `check`, then `check --hybrid`.

Expected: both CLEAN.

Result:

### S4 — FS2/FS4: a newer version without the id is refused
Steps:
1. Add `SHADOW_e_isp_export_v1.10.md` without the claim id (keep v1.0).
2. Run `check`.

Expected: one error naming the claim id and `solutions/SHADOW_e_isp_export_v1.10.md`
(v1.10 is newer than v1.0). Add the id to v1.10: CLEAN again.

Result:

### S5 — FS6: export drops a Hybrid marker
Steps:
1. With S4 clean, set `about` to `depends-on -> export; not-yet-honored-by ->
   SHADOW_e_isp_export` and run `sdlc_check.py export --root . --out ../bundle`.
2. Open `../bundle/topics/export.md`.

Expected: the report has one line saying not-yet-honored markers were dropped, with no
number; the bundle's claim keeps `depends-on -> export` and has no
`not-yet-honored-by`; every other line equals the original.

Result:

### S6 — FS7: recall names the target
Steps:
1. In an agent session with the kb lens, ask "does the export run nightly?".

Expected: the answer says the specification requires it and the code does not yet do
it, naming `SHADOW_e_isp_export` (or the design it shadows), citing the claim id —
never as current behavior.

Result:

## Regression scenarios

### R1 — Standalone markers still behave as in F-080
Steps:
1. Replace the marker with `not-yet-honored-by -> ANALYSIS_export_schedule` and create
   `ai_docs/solutions/ANALYSIS_export_schedule.md` (valid frontmatter) citing the id.
2. Run `check`; then remove the id from the analysis and run `check` again.

Expected: CLEAN, then one error naming the claim id and the analysis.

Result:

### R2 — Ordinary relations and a malformed target
Steps:
1. Set `about` to `depends-on -> SHADOW_e_isp_export`, then to
   `not-yet-honored-by -> SHADOW_e_isp_export_v1.2`.

Expected: each is refused as a malformed `about` part.

Result:

### R3 — A project with no marked claim
Steps:
1. Remove every marker and run `check` and `check --hybrid` on a project that has
   unrelated shadows in `solutions/`.

Expected: the same result as with the previous release (no new finding).

Result:
