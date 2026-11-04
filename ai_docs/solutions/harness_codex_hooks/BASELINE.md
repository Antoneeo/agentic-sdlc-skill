# Baseline probe provenance

`probe_install.cjs` and `probe_events.py` were run against baseline Git 74c1833f,
package 1.52.0, before implementation. Their assertions intentionally describe the
missing Codex behavior. Run them against that revision; they are not candidate
acceptance tests. The raw baseline results are retained beside them.

Candidate acceptance uses test_install_upgrade.py, probe_native.py, probe_init.py
and the Node/Python batteries. See validation_summary.json for their boundaries.
All result paths identify disposable local fixtures, not portable install paths.
