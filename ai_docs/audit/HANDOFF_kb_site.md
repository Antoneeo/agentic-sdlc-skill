---
workstream: F-072 docs site (static site generated from ai_docs, shared by the family)
level: L3
branch: feat/kb-site-spec
status: IN_PROGRESS
since: 2026-10-16
next: field run of the probe and the site on the owner's work machine (released in 1.42.0)
details: ANALYSIS_kb_site.md · REQUEST_kb_site.md · E2E_TEST_kb_site.md · MERGE_REVIEW_kb_site.md · harness_kb_site/probe.py
updated: 2026-10-17
---

## Resume logistics

Implemented, chronology included. Code: `skills/agentic-sdlc-skill/scripts/docs_site.py`,
`docs_site/` beside it, battery `scripts/test_docs_site.py`; all three are shared spine files, so
edit them in `skills/agentic-sdlc-skill/`, copy to the three distributions and run
`shared_files.py --update` in each.

Chronology: `docs_site.chronology(docs, pages)` reads F-073's openers with the validator's
readers (`section_lines` + `entry_openers`, `request_entries`, `parse_review_log`,
`adr_date`, `knowledge.frontmatter_date`); tests in `Criterion03Chronology`.

Set aside by the owner for later (2026-10-17): a page explaining the skills (to be weighed against the check rule: it is the skill's text, not the project's); a validator check that an analysis uses the canonical chain headings. In Hybrid the devPNT GUI already shows milestones, plans and governed artifacts, so the site stays Standalone-first.

Field run: on the owner's work machine, `harness_kb_site/probe.py --root <field project>`
then `docs_site.py --root <field project>`, and walk `solutions/E2E_TEST_kb_site.md`.
