Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**Published on npm (verified `npm view --prefer-online` 2026-08-25):** code 1.26.1,
kb **1.4.8**, mkt 0.4.7. `v1.16.0` was tagged and never published — it stays as
history, and no pushed tag is ever moved. kb 1.4.2 was bumped and never published
either; the registry goes 1.4.1 → 1.4.3.

**kb 1.4.8 released 2026-08-25** (F-035 provenance chains + pointer integrity, tag
`kb-v1.4.8`, merged to main as a fast-forward). First release tagged with a
package-scoped name: the three packages version independently, so a bare `vX.Y.Z` is
ambiguous against the code lens's own tags. code and mkt were unchanged and were
skipped by `publish_all.bat` rather than re-published.

**Trap recorded the day it bit:** `npm view` answers from a metadata cache, so the
script's post-publish verify printed the PREVIOUS version and read as a failure when
the publish had in fact succeeded. `--prefer-online` is now on every `npm view` in
`publish_all.bat`. When in doubt, `npm view <pkg> versions --json --prefer-online`
settles it.

Companion workstream still owed in the devPNT repo: the governed D-IC artifact
(sequence D-UC → D-IC → P-TM → E-ISP), from F-032.
