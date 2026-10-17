---
workstream: F-072 docs site (static site generated from ai_docs, shared by the family)
level: L3
branch: feat/kb-site-spec
status: IN_PROGRESS
since: 2026-10-16
next: build the chronology reader once F-073's dated-entry rules are merged; then run the probe and the site on the field KB on the owner's work machine, and release the four packages
details: ANALYSIS_kb_site.md · REQUEST_kb_site.md · E2E_TEST_kb_site.md · MERGE_REVIEW_kb_site.md · harness_kb_site/probe.py
updated: 2026-10-17
---

## Resume logistics

Implemented except the chronology reader. Code: `skills/agentic-sdlc-skill/scripts/docs_site.py`,
`docs_site/` beside it, battery `scripts/test_docs_site.py`; all three are shared spine files, so
edit them in `skills/agentic-sdlc-skill/`, copy to the three distributions and run
`shared_files.py --update` in each.

Chronology: `docs_site.chronology(docs)` returns no event. When F-073 (branch
`doctrine-chronology`) is merged, implement it with that unit's date rules plus
`sdlc_core.section_body` and `parse_review_log`; the event kinds and their strings
(`event_*` in `strings.js`) and the page already exist. Add the criterion-3 tests first.

Set aside by the owner for later (2026-10-17): a page explaining the skills (to be weighed against the check rule: it is the skill's text, not the project's); a validator check that an analysis uses the canonical chain headings. In Hybrid the devPNT GUI already shows milestones, plans and governed artifacts, so the site stays Standalone-first.

Field run: on the owner's work machine, `harness_kb_site/probe.py --root <field project>`
then `docs_site.py --root <field project>`, and walk `solutions/E2E_TEST_kb_site.md`.
