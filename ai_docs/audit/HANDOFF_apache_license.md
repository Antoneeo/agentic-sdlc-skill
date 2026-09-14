---
workstream: F-055 Apache-2.0 with NOTICE (four packages, two repositories)
level: L3
branch: feat/apache-license
status: DONE, AWAITING PUBLISH
since: 2026-09-13
next: publish_all.bat from the repo root (owner's act, 2FA opens a browser per package; all three changed), then npm publish in distill-skill (2FA); then npm view returns code 1.34.0, kb 1.17.0, mkt 0.12.0, distill 0.9.0
details: ANALYSIS_apache_license.md · harness_apache_license/probe.py
updated: 2026-09-14
---

## Resume logistics

Committed and released on `main` in both repositories: tags `v1.34.0`, `kb-v1.17.0`,
`mkt-v0.12.0` here and `v0.9.0` in `distill-skill`. Only the npm publish remains, and it is
the owner's (2FA). Delete this file once `npm view` shows the four versions.

Re-run the executed claims with `python ai_docs/solutions/harness_apache_license/probe.py`
from the repository root.
