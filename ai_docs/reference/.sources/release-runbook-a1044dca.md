# Release Runbook — @antoneeo/agentic-sdlc-skill

Approved by Antonio Pinto, 2026-07-02. Distilled from the v1.8.0 release session
(first documented release run); amended same day by Antonio's indication to use
`git_push_tag.bat` for the commit+tag+push step. This is the verbatim source
("book") for `GUIDE_release.md`; detail lives here, the guide is the synthesis.

## Preconditions

- The unit/feature being shipped is DONE: independent code review PASS, scenario
  battery green, ADR (if any) accepted.
- `CHANGELOG.md` has an `## [Unreleased - X.Y.Z] (...)` section describing the release.
- `python skills/agentic-sdlc-skill/scripts/sdlc_check.py check --hybrid --root <repo>`
  is CLEAN (known DRAFT warnings on vision docs are acceptable).
- The target version does not already exist on npm:
  `npm view @antoneeo/agentic-sdlc-skill version`.

## Version bump points

All three, in the same commit:

1. `package.json` → `"version"`.
2. `gemini-extension.json` → `"version"`.
3. `CHANGELOG.md` → heading `## [Unreleased - X.Y.Z] (...)` becomes
   `## [X.Y.Z] - YYYY-MM-DD (...)` (date the entry, keep the parenthetical title).

## Packaging completeness

- `package.json` `files` is an explicit allowlist. Every NEW runtime/support file
  (anything under `skills/agentic-sdlc-skill/` that the skill needs at runtime)
  MUST be added there, or it ships neither in the npm tarball nor to installed
  skill folders — `postinstall.js` copies the *installed package's* skill folder
  recursively, so it can only copy what the tarball contains.
- Field precedent: in v1.8.0, `skills/agentic-sdlc-skill/guides.md` (added by
  Feature B unit 1) was missing from `files` and would not have shipped; caught
  only at release time.
- Verify with `npm pack --dry-run --json`: every expected file listed;
  `__pycache__` and `.sources/` snapshots NOT listed.

## README alignment

- The "Installed support files" bullet in `README.md` lists the support files —
  add any new one.
- The "Runtime Shape" tree in `README.md` lists the skill folder contents — add
  any new file there too.

## Verification battery

Run before any commit/tag/publish:

1. `npm pack --dry-run --json` — see Packaging completeness above.
2. init.js smoke on a scratch project: run `node <repo>/scripts/init.js` in an
   empty directory → all templates extracted, no errors; then
   `sdlc_check.py check --root <scratch>` → CLEAN (3 DRAFT warnings on the
   boilerplate vision docs are expected).
3. Closure gate on the repo itself:
   `sdlc_check.py check --hybrid --root <repo>` → CLEAN.

After publish: `npm view @antoneeo/agentic-sdlc-skill version` must return the
new version.

## Git sequence

Commit + tag + push are done with the repo-root script `git_push_tag.bat`
(per Antonio's indication, 2026-07-02).

1. Ensure the working tree contains ONLY the release edits — the script runs
   `git add .`, so every pending change (including devPNT db churn, which is
   tracked in this repo) is swept into the release commit. If unrelated changes
   are pending, commit or isolate them first.
2. From the feature branch run:
   `git_push_tag.bat "Release vX.Y.Z: <short title>" vX.Y.Z`
   The script stages everything, commits with the given message, tags, and
   pushes both the current branch and the tag. The release commit carries the
   version bumps, CHANGELOG, README and handoff update together.
3. VERIFY the tag landed on the release commit:
   `git rev-parse vX.Y.Z` must equal `git rev-parse HEAD`. The script tags HEAD
   unconditionally — if its commit step failed (hook, empty stage), the tag
   lands on the PREVIOUS commit; this is the same wrong-tag failure hit
   manually in the v1.8.0 run. If the tag is wrong: `git tag -d vX.Y.Z`, fix,
   re-run (if the tag was already pushed, delete the remote tag too:
   `git push origin :refs/tags/vX.Y.Z`).
4. Merge to main. Constraints on this machine (as of 2026-07): the `gh` CLI is
   NOT installed — create the PR via the GitHub web UI
   (`https://github.com/Antoneeo/agentic-sdlc-skill/pull/new/<branch>`); a
   direct push to main requires the user's explicit authorization in-session.
   Historical pattern: one tag per release, name `vX.Y.Z`.

## Known traps

Verified in the field, 2026-07-02:

- **devPNT db locks**: while the devPNT MCP server runs,
  `.devpnt/agent/agent_knowledge.db` and `.devpnt/plans/plans.db` are held open
  and continuously rewritten. Any git operation that must replace them in the
  primary working tree (checkout, merge, stash) fails with
  `error: unable to unlink old '...': Invalid argument` — and
  "commit then switch" fails too, because the dbs re-drift immediately after
  each commit. Committing on the CURRENT branch (what `git_push_tag.bat` does)
  is fine; do branch-crossing work in a separate `git worktree add` checkout,
  or defer it to a session where the devPNT server is stopped.
- **`git_push_tag.bat` failure mode**: the script does not stop on a failed
  commit — the tag then lands on the previous HEAD. Always run the step-3
  verification from the Git sequence above.
- **npm 2FA**: `npm publish` stops with `EOTP` (one-time password via browser).
  The agent cannot complete it — the USER runs the final `npm publish`.
- **PowerShell 5.1**: no `&&` chaining; `npm pack --dry-run` prints its file
  listing to stderr — use `--json` and parse instead.

## Publish

1. Publish from a clean checkout of the release content. If the primary
   worktree is stuck on another branch (see devPNT db locks),
   `git worktree add <tmp> <release-branch>` provides one.
2. `npm publish` — run by the USER (2FA OTP). npm prints the full tarball
   listing before the OTP prompt: check it one last time.
3. Confirm with `npm view @antoneeo/agentic-sdlc-skill version`.

## Post-release

- `ai_docs/audit/handoff.md`: record the release (version, date) and the next
  step; include it in the release commit when possible.
- devPNT: update milestone / Action Plan state if the release closes a unit or
  a milestone.
- If new canonical docs were added, run `sdlc_check.py index` and commit the
  regenerated indexes.
