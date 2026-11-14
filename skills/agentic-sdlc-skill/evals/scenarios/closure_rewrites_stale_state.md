---
id: closure_rewrites_stale_state
expected: at closure the agent re-reads the impacted guide whole, rewrites every sentence about the earlier state, and names the guide in the closure message
---
## Setup
- ai_docs/reference/INDEX.md: Guide router. GUIDE_server.md -- consult before operating on the production server.
- ai_docs/reference/GUIDE_server.md: Guide Server, status CURRENT. Paragraph 1 opens "File served by the proxy, in provisional form (2026-11-14)". Paragraph 2 opens "Redirect feature (unit U1, code of 2026-11-14, not yet in production)". A paragraph after a table ends "Removal of the proxy file: not yet done (to be noted here with the date)". The guide ends with a change log table `| Date | Change | Who |`.
- The owner has just released unit U1 to production and removed the proxy file; the application now serves the file.
- `sdlc_check.py check` on this tree prints `check: CLEAN`.
## Prompt
The release of U1 is done: I deployed it and removed the proxy file. Close the unit.
## Pass criteria
- The agent reads GUIDE_server.md from its first line to its last before editing it: the release changed what the guide describes, so the guide is impacted even though no step forced the agent to open it.
- All THREE sentences about the earlier state are rewritten to the current one ("provisional form", "not yet in production", "not yet done"). Rewriting two and leaving the third is a fail: that is the recorded case.
- A row added to the change log is not offered as the correction: the sentences above it are changed.
- The closure message carries the line `re-read whole: ai_docs/reference/GUIDE_server.md` (or the same with more documents). A closure with no `re-read whole:` line is a fail.
- The agent does not present `check: CLEAN` as evidence that the guide is true: the `[scope]` line says the check covers form only.
- Variant, nothing impacted: the same prompt on a tree whose guide says nothing about the release ends with `re-read whole: none impacted`.
- Variant, a guide whose source did not change: GUIDE_server.md is `source_kind: document` and the owner handed no new source. The three sentences are still rewritten, through the guide's own route (`guides.md` §6) — the agent says the correction rests on the owner's words in the request record; leaving the sentences because "the source hash is unchanged" is a fail.
- Variant, a document too large to absorb: the same release on a tree whose impacted guide is several thousand lines the closure cannot re-read and rewrite. The agent marks it `status: SUPERSEDED` and says so; leaving it `CURRENT` with the false sentences is a fail.
