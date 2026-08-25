Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**Published on npm (verified `npm view --prefer-online` 2026-08-25):** code **1.27.1**,
kb **1.5.1**, mkt **0.5.1** — F-036 (init wires the SessionStart orientation hook) in
1.27.0/1.5.0/0.5.0, then the README front pages and the publish-verify poll in the .1s.
First three-package release since the packages began versioning independently. `v1.16.0` was tagged and never published — it stays as
history, and no pushed tag is ever moved. kb 1.4.2 was bumped and never published
either; the registry goes 1.4.1 → 1.4.3.

**kb 1.4.8 released 2026-08-25** (F-035 provenance chains + pointer integrity, tag
`kb-v1.4.8`, merged to main as a fast-forward). First release tagged with a
package-scoped name: the three packages version independently, so a bare `vX.Y.Z` is
ambiguous against the code lens's own tags. code and mkt were unchanged and were
skipped by `publish_all.bat` rather than re-published.

**Trap recorded the day it bit, and the fix that was not enough.** `npm view` answers
from a metadata cache, so the post-publish verify printed the PREVIOUS version and read
as a failure when the publish had succeeded. `--prefer-online` was added — and it bit a
SECOND time (the 1.27.0 run reported mkt 0.4.7 when 0.5.0 had landed), because the flag
forces revalidation but cannot outrun CDN propagation of the `latest` tag. Since 1.27.1
the block **polls** until the registry agrees with the local version; the 1.27.1 run was
the first whose own output could be trusted. When in doubt,
`npm view <pkg> versions --json --prefer-online` still settles it.

Companion workstream still owed in the devPNT repo: the governed D-IC artifact
(sequence D-UC → D-IC → P-TM → E-ISP), from F-032.
