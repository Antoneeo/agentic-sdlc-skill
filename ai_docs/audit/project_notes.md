Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**Published on npm (publish_all.bat polling verify, 2026-08-28):** code **1.28.0**,
kb **1.7.0**, mkt **0.6.0** — kb 1.7.0 (tag `kb-v1.7.0`) carries the second brain's
units 1-2: F-039 recall reflex + F-040 capture moment; code and mkt unchanged,
skipped by the script. Before that: F-038 (gated-rung vocabulary + mandated ask,
tag `v1.28.0`, merged to main) in all three. Before that: F-036 (init wires the
SessionStart orientation hook) in 1.27.0/1.5.0/0.5.0, then the README front pages and
the publish-verify poll in the .1s — the first three-package release since the packages
began versioning independently. `v1.16.0` was tagged and never published — it stays as
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
`npm view <pkg> versions --json --prefer-online` still settles it. Third bite,
different organ (2026-08-26): the per-package 2FA flow waits on an ENTER before the
last publish — a run abandoned at that prompt looks complete while the remaining
package never shipped (mkt 0.6.0 landed 2 minutes after the other two, on a second
pass). The registry `time` field settles WHEN each version actually landed.

Companion workstream still owed in the devPNT repo: the governed D-IC artifact
(sequence D-UC → D-IC → P-TM → E-ISP), from F-032.
