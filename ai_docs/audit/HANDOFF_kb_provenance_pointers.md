---
workstream: F-035 Provenance Chains and Pointer Integrity
level: L3
branch: feat/kb-field-report-2
status: DONE, AWAITING MERGE + RELEASE
since: 2026-08-25
next: release as kb 1.4.8 per `reference/GUIDE_release.md` (bump 4 points, git_push_tag.bat, merge, publish_all.bat)
details: ANALYSIS_kb_provenance_pointers.md
updated: 2026-08-25
---

## Resume state

Branch `feat/kb-field-report-2`, cut from `main`@61f1425 (v1.26.1). Second field
report from the F-029 practitioner. Code, tests and doctrine complete on the branch;
kb battery 258 green.

Four fixes, all in the kb overlay `sdlc_check.py` (the spine is untouched, drift guard
identical):

- **A** `_note_frontmatter` reads the artifact's `.meta.md` sidecar when one exists,
  so DERIVED / RULING / IMPORTED become reachable for a claim citing `corpus/given/`;
  it returns the file it read so the finding names it.
- **A'** a `GIVEN` row whose artifact's sidecar declares a weaker `provenance:` warns.
- **B** `original_path:` is checked for resolution — a **warning**, never an error.
- **C** the duplicate-id error branches on claim text: same text is a copied row,
  different text is a `kb_claim_id` collision, and each says so.

## Watch out

- **The reporter filed this against the wrong tree.** `D:\SoftwareDev\skill_sdlc\
  kb-agentic-skill` is a stale v1.0.0 lineage with no corpus machinery and seven
  unpushed commits; it is a plausible place to "fix" a bug that would then never ship.
  The live source is `distributions/kb-agentic-skill/`.
- **Ceremony cost ACCEPTED** by the owner on 2026-08-25; recorded in the ANALYSIS
  Feature Vision section with its basis. No decision outstanding on the unit itself.
- **Release is the remaining work**, and it is kb-only: all four kb bump points agree
  at 1.4.7, so the target is **1.4.8**. `GUIDE_release.md` owns the sequence; note its
  step 3 — `git_push_tag.bat` runs `git add .`, so the tree must hold ONLY the release
  edits when it runs.
- **Deferred, named so it is not lost**: `--errors-only` on `corpus`/`graph` (the
  reporter's item D, ranked last by them). And `ELICITED` is accepted with no required
  field at all — a pre-existing gap found while fixing A, not repaired here because it
  is a new gate rather than a repair.
- **Review history.** The DESIGN review ran at rung 3 (declared self-pass, 5 findings):
  subagents were off by session policy, `gemini` fails with `IneligibleTierError` (and
  exits 0 while doing so), `codex` fails to load `~/.codex/config.toml`
  (`service_tier = "default"` is not a valid variant — it wants `fast` or `flex`).
  Fixing that config restores rung 2 for future sessions.
  The CLOSURE review then ran at **rung 1**, on the owner's explicit authorization: two
  independent subagents in parallel, different lenses (conformance / adversarial). They
  returned 3 BLOCK + 20 WARN, converging independently on four findings. All three
  blockers were reproduced by hand before being acted on, and the worst of them —
  `Path.is_absolute()` being False for the `/vault/...` form the project's own templates
  print — was invisible to the self-pass and to the whole first battery.
- **Lesson worth keeping:** the self-pass found real defects but missed every
  platform-semantics bug. Rung 3 is not a substitute for rung 1; it is what you do when
  rung 1 is unavailable, and the log row has to say which one ran.
