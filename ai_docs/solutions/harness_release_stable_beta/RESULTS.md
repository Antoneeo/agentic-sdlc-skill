# Release verification — 2026-10-02

Stable targets: code 1.37.0, KB 1.20.0, marketing 0.15.0. Course target
0.1.0-beta.1 explicitly selects beta. Exact target registry queries return E404.

Four full Python suites passed: code 228/1 skip, KB 414/15 skip, marketing
251/14 skip, course 245/19 skip. Logs are tests_<domain>.txt. Total: 1,138
tests enumerated, 1,089 passed, 49 skipped. Node course client tests: 4 passed,
1 skipped because symlinks unavailable. Publisher real-batch mocks: 4 passed,
including omitted stable tags, explicit course beta, existing-version skip,
publish failure and verification failure. Initial mock ping.cmd incorrectly
transferred batch control; removed before the successful runs.

verify_packages.py checks every manifest allowlist path, unwanted files, metadata
versions and init plus fresh-project check. Four packages pass; packages.json
records 29/29/28/34 files. Shared drift guard: 22 byte-identical files.

Independent design, release closure and pre-existing integration reviews PASS
in fresh read-only contexts, different model. REVIEW_release_stable_course_beta.md
records corrections and scope. No human-learning efficacy or C-001 readiness claim.

Legacy 18 warnings are nonfatal: seven permitted Vision Alignment headings not
recognized by the validator, eleven historical missing headings/status fields.
They are not repaired by inventing history. Audit references are refreshed only
after integration and derived documents have been reviewed. Publication is still
pending; login completed. Course presentations and local rendering dependencies
are excluded from staging and npm packages.

Post-publication: commit 3e56773 and all four package tags are on origin. npm
accepted all four versions; public tarball SHA1 values match publication.json.
All three stable latest tags match their targets. Course beta matches 0.1.0-beta.1,
but latest also names this prerelease. Authenticated removal completed browser
authorization and returned E400. Publication is accepted; beta-only closure is open,
pending owner decision. Earlier E404 and pending-login statements describe preflight.
Seven publisher guard mocks now pass; independent guard review PASS. Its WARN
was resolved by describing manual tag removal as subject to registry acceptance.

Plain repository closure gate CLEAN (validate rc=0, stale rc=0); 18 inherited
nonfatal warnings retained. F-060/F-061 implemented units can now close.
