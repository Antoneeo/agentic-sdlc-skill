Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**Unreleased kb fix on `fix/kb-recency-source` (seventh field datum,
2026-08-28, reported against 1.11.0 same day):** the recency `date:` probe read
only the first 600 bytes of the note; a REAL frontmatter (edge lists, basis
lines) pushed the closing fence past the cap and the WHOLE probe silently
skipped -- a note dated 3 days back read "0 days old (mtime -- date: not
parsed)". The 1.11.0 disclosure marker did its designed job (made the lie
visible and NAMED the failing source -- that is what let the field session
diagnose it); the source is now fixed: `load_frontmatter` (the authoritative
reader) + `kb_unquote` + datetime-suffix-tolerant prefix. Root cause
REPRODUCED in RED before fixing (long-frontmatter fixture). Released as kb
1.11.1 (tag `kb-v1.11.1`, 2026-08-28; publish = owner's act, then poll
verify). Field lesson attached by the reporting session
itself: it had approved the mtime behavior twice on plausible reasoning
before testing it against the case in view -- evidence for the review rule
"a PASS is invalid on found-nothing" extending to APPROVALS.

**Published on npm (registry-verified 2026-08-28, second wave):** code
**1.29.0**, kb **1.11.0**, mkt **0.7.0** -- tags `v1.29.0` / `kb-v1.11.0` /
`mkt-v0.7.0`, one commit (`c97a4b5`), merged to main. kb 1.11.0 = F-044 the
time cycle + the fifth/sixth field-data fixes (YAML unquoting, recency
disclosure); code/mkt = parked F-041/F-042 + the F-043 revision-sentence port
(code: L2 row + ANALYSIS write trigger; mkt: E2 row). First field report on
1.11.0 arrived within hours: the quoting fix VERIFIED (124 -> 22 warnings,
the 22 all legitimate incomplete-ingestion warns; zero false dangling).

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
