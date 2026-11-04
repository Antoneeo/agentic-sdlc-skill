---
feature: F-091
analysis: ANALYSIS_codex_hooks.md
---
# E2E test: Codex hook installation and upgrade

For the person testing the packaged change after merge. Run in disposable profiles;
never copy a trust store or credentials into the fixture. This script tests the main
software package. Sibling installers retain their previous hook scope.

## Environment and preconditions

Windows with Node/npm, Python 3 and a local Codex client supporting command hooks.
Inline TOML inspection needs Python 3.11+ (`tomllib`). Record the client version and
orchestration mode. POSIX and other client versions require their own run.

## New-behavior scenarios

### S1 — FS1/2/8: ordinary installation and update

Run `python -B ai_docs/solutions/harness_codex_hooks/test_install_upgrade.py --keep`
from the repository. It packs actual distributable files, installs baseline 1.52.0,
updates to the candidate tarball, repeats the update, and installs the candidate in
a second clean profile. It uses a temporary candidate version before the release bump, and the actual version once prepared; no release is published by the harness.

The baseline commit 74c1833f must be available in the clone; it is pinned so post-merge reruns still compare against the old behavior.

Expected: four Codex handlers; no duplicates; repeat definitions byte-identical;
Claude settings byte-identical across upgrade; a fresh Claude install still has its
four handlers. Installed commands produce orientation from root/nested cwd, reminder,
router deny/allow and bound constraint recall. Result: `harness_codex_hooks/consumer_results.json`.

### S2 — FS3: native loading and human trust

Run `python -B ai_docs/solutions/harness_codex_hooks/probe_native.py` after S1, using
the same machine's Codex binary. Inspect `native_results.json`: four enabled hooks,
user source, no errors/warnings, `untrusted` before any consent.

In a separate terminal set `CODEX_HOME` to the isolated path printed by S1, start
Codex in the printed project, open `/hooks` and inspect the four commands. Approve
their trust through the client only if you choose to. Never edit the trust store.
Restart the session if Codex asks. Confirm SessionStart orientation and prompt reminder.

Result: native loading verified on Windows Codex Desktop binary 0.166.0-alpha.6.
The later native_start_results.json records all four definitions trusted/enabled and completed SessionStart/UserPromptSubmit callbacks; orientation contains the fixture marker. The process uses an offline local endpoint, never an external model.

### S3 — FS4/5: native verdict and recall

After S2 trust, ask for an `apply_patch` edit of `src/a.py` before any router verdict:
expect a deny explaining the missing declaration. Declare
`Level: L3 · router: GUIDE_sample.md -> read`, read the guide and ANALYSIS with
literal `Get-Content -LiteralPath` (or `cat`), and retry. Expect the verdict to become
silent and the bound P1 context to appear. Observe that normal tool authorization
still applies. Repeat with a patch moving a file and a patch affecting several files.

Result: installed-command protocol cases pass. Live verdict deny/allowed retry was observed; native_recall_results.json records P1 context delivered before a disposable fixture patch. Reported live observations are distinguished from the automated app-server callbacks.

### S4 — FS2/6/7: opt-out and conservative configuration

Remove one generated handler and reinstall: it must stay absent. Disable an existing
handler: it must stay disabled. Add a foreign handler: it must survive reinstall and
explicit package `scripts/preuninstall.js`. A malformed JSON/TOML source or disabled
hooks policy must produce a diagnostic and remain unchanged. Existing inline TOML
orientation must avoid a new JSON duplicate. Run init twice in an isolated project:
one user-level orient definition, no new project Codex definition.

Run a second packaged pass without `--keep`:
`python -B ai_docs/solutions/harness_codex_hooks/test_install_upgrade.py --report consumer_cleanup_results.json`.
Expected: explicit preuninstall preserves the foreign handler; PASS is written only
after cleanup assertions finish. Result: `consumer_cleanup_results.json` (PASS).
The kept-profile S1 run intentionally skips cleanup to permit S2. For cleanup of its separate fresh-install fixture, run `python -B ai_docs/solutions/harness_codex_hooks/probe_cleanup.py`: latest-tarball result `final_cleanup_results.json` is PASS, with all owned Codex handlers removed and the foreign handler preserved.
Malformed/policy/TOML cases are covered by Node tests. Installed init runs twice,
then exercises both malformed Windows override spellings: diagnostics preserve
configuration and do not abort (`init_results.json`). Native policies still need
separate observation.

## Regression scenarios

- Run `node --test scripts/test_clients.js`: includes the existing Claude wiring,
  marker, opt-out and uninstall contracts beside Codex cases.
- Run `python -B -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"`:
  includes unchanged Claude transcript cases, schema checks and shared-copy guard.
- Test unknown transcript/patch carriers and shell writes: no claim of comprehensive
  enforcement; the documented written duties remain in force.
- On POSIX run S1–S4 and record results separately. This Windows run does not certify
  shell quoting, native dispatch or user consent on POSIX.

## Cleanup

Run the installed package's `scripts/preuninstall.js` with Node before removing its
isolated prefix. Verify the target is the S1 temporary root before deleting it.
`npm uninstall` alone may skip preuninstall on npm 11. Keep real profiles untouched.
