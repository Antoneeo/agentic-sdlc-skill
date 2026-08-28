Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**Unreleased kb fix awaiting owner merge (branch `fix/kb-quoting-recency`, off main):**
fifth and sixth field data, 2026-08-28, same external corpus -- (a) YAML-quoted
`original_path:` values (paths with spaces) produced 102 FALSE dangling-pointer
warns; root cause: `load_frontmatter` keeps values verbatim by design and the
consumers never unquoted -- fixed with `kb_unquote` at the three reading sites
(original_path, supersedes x2 incl. the corpus-INDEX display; a quoted
`supersedes:` would have silently MISSED a supersession, worse than the reported
warn-noise). (b) The orient recency line fell back to mtime IN SILENCE whenever
a note's `date:` failed to parse (quoted dates did) -- "0 days old" on a note
dated days earlier, against SKILL.md's date-first promise; now quoted dates
parse, dated stamps win same-day ties, and an mtime-decided line SAYS SO
(`; mtime -- date: not parsed`). Releasable as kb 1.10.1; `feat/kb-time-cycle`
(F-044, design committed) must merge this in before GREEN -- its collector
parses the same fields.

**Published on npm (registry-verified 2026-08-28):** code **1.28.0**, kb **1.10.0**,
mkt **0.6.0** -- kb 1.10.0 (tag `kb-v1.10.0`) carries F-043: the revision doctrine
(documents read as current state; full re-read, never append a delta). Before that,
same day: kb 1.9.0 (tag `kb-v1.9.0`) carries F-042: install-time global orient
hook (user-level settings; removal = standing per-target opt-out; surgical uninstall)
+ the user-aware, user-language check note; live-verified on the dev machine (update
wired hook + marker). Second field datum, same day: an external session
self-discovered `remind` in 1.9.0, tested it, honored the opt-in and asked the
owner a COMPREHENSIBLE consent question -- the exact UX F-042 was ruled to
produce. Evidence stream for the vision's unit 3. Third datum, same day (the strongest): an external
session's post-mortem on a 12-document realignment -- delta-append revisions left
pre-call sentences standing as printed truth, and the session itself named the
claim-ledger cascade (claim superseded -> citing documents mechanically stale)
as the designed answer to exactly that failure. Discipline half shipped as
F-043 (the kb `## Revision` doctrine + remind clause). **Declared follow-up (durable
home):** the code AND mkt lenses share the revision failure surface on their own
triage rows (mkt's vocabulary is E-rows) and can port the doctrine sentence when
they next release; the kb SKILL.md section is the reference text. The mechanical
half stays unit 3. Fourth field datum, same day: an external session VALIDATED
1.10.0 against its own post-mortem (doctrine lands at the right points; the
mechanical gap correctly left to unit 3) and filed one cosmetic item, half-true
on inspection: `--help` DOES print the overlay block (graph/corpus/.../remind),
but the argparse USAGE LINE and the unknown-command ERROR path list only the
nine spine commands. **Backlog (small):** after the spine's unknown-command
error, the kb overlay dispatch appends one pointer line to the overlay commands
-- forward-by-default intact (the spine still rules validity); the usage first
line stays spine-owned (lens-neutral by design). The F-042 JS touches ALL THREE packages' lifecycle scripts --
code and mkt have a concrete reason to release soon. Before that: kb 1.8.0 (tag
`kb-v1.8.0`) carries F-041: the check wiring/dead-hook
notes (spine x3, parked in code/mkt CHANGELOGs for their next release) + the kb
`remind` per-turn opt-in. Field datum the same day: an external session's check
surfaced its missing orient hook via the new note and offered the wiring -- the
note doing exactly its designed job. Before that: kb **1.7.0** — kb 1.7.0 (tag `kb-v1.7.0`) carries the second brain's
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
