---
feature: F-091
analysis: ANALYSIS_codex_hooks.md
status: CURRENT
---
# Integration brief: Codex hook parity

For the integrator reviewing `codex/f091-codex-hooks`. This branch is pushed for
review; the code unit is reviewed and complete. Integration/publication authorization is REQUEST R9.

## Scope

The main package supplies four user-level Codex hook definitions with descriptive
consent titles. Shared Python code recognizes native patches and bounded Codex
transcript carriers. Explicit opt-outs, foreign definitions and client policy are
preserved. Claude wiring and sibling Node installers retain their previous paths.
Design: ANALYSIS_codex_hooks.md. Reproduction: E2E_TEST_codex_hooks.md.

## Evidence

- Final Node battery: 74 passed after the consent-label change.
- Unchanged Python core: 611 tests run, four skipped, zero failures.
- Each sibling: 166 shared-contract tests, five skipped; real entry-point smoke passed.
- Tarball fresh install, baseline upgrade, repeat install, installed init and
  attributed cleanup passed. Claude settings remained byte-identical across upgrade.
- User-level labels updated without changing commands or Claude configuration;
  owner accepted the result (R7). Native verdict denial and allowed retry observed.
- Source guide, preservation constraints, ADR and raw test/result artifacts are
  under the F-091 paths. Document check must remain CLEAN before integration.

## Integration and release boundary

The six implementation findings are corrected and the independent scoped closure
review returned PASS. The release review also returned PASS after test fixtures
were isolated from real CODEX_HOME configuration; the golden baseline is unchanged.
Release gates record 121 Node tests passed and 611 Python tests with four skips.

Native evidence now covers completed SessionStart/UserPromptSubmit callbacks with
both output markers, plus reported live verdict denial/retry and constraint recall
before a disposable patch. All four definitions are trusted/enabled in the local
client. POSIX, minimum client version and native interpreter/timeout failure cases
remain unverified; notes state the tested Windows client explicitly.

Prepared versions: code 1.53.0, KB 1.35.1, marketing 0.30.1, Course 0.1.0-beta.19.
GUIDE_release requires owner approval of their concrete notes before tagging.
The current npm login returned E401 and web login was started; user authentication
is still required. Merge from the clean integration worktree, verify main/tags on
origin, then publish exact tagged content through publish_all.bat. Preserve the
dirty primary checkout. No release is claimed until registry verification.
