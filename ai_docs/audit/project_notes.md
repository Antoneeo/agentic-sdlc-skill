Repo is CRLF (edit as content-delta). devPNT off — Standalone. Standing Vision
battery: `audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md`, re-run on every Vision edit.

**2026-10-27 — release 1.49.0: working model (F-085 constraint view and recall hook, post-merge tier), shared knowledge layer (F-084), imported-ruling refusal (F-083), verdict and gate hook fixes.** Code 1.49.0, KB 1.32.0,
marketing 0.27.0, Course 0.1.0-beta.14; tags v1.49.0 / kb-v1.32.0 / mkt-v0.27.0 /
course-v0.1.0-beta.14 on the release commit. Publish pending (owner's 2FA).

**2026-10-27 — Verdict hook (L2, follow-up of F-085): a level quoted in prose no longer counts as a declaration; the project judged is the edited file's own, not the working directory's.** A router verdict follows the
same rule (34d3361f), and the protected-path gate resolves from the edited file too. The
closure review (REVIEW_LOG 2026-10-27, verdict/gate hook fix) found two regressions, both fixed before release:
`Level: Spike · router: …` was refused, and the gate unprotected its paths in a project with
no docs root. Markdown openers (`##`, `1.`, `•`) count; a quote that opens a line still does.

**2026-10-23 — release 1.48.0: field-report units F-075..F-081 (orientation reach, guide verdict check, kb intake hygiene, guide check, docs site naming, spec/code divergence incl. Hybrid); includes the unpublished 1.46.0 and 1.47.0.** Published and verified on the registry, each on
latest: code 1.48.0, KB 1.31.0, marketing 0.26.0, Course 0.1.0-beta.13. Tags v1.48.0 /
kb-v1.31.0 / mkt-v0.26.0 / course-v0.1.0-beta.13 on 1df13df.

**2026-10-23 — F-078 closed: Guide check section and validate advisory.**

**2026-10-19 — the docs root is not an audit area: stale ignores it, mark refuses it (it was re-marked 15 times in two days).**

**2026-10-19 — release 1.47.0: mark --note, project-notes opener check, unit ids in the chronology; includes the unpublished 1.46.0 (--zip). Tags v1.47.0 / kb-v1.30.0 / mkt-v0.25.0 / course-v0.1.0-beta.12, publish pending.** The tags were moved, before any publish, to the commit that also makes the docs root not an audit area.

**2026-10-19 — mark --note: a release or work outside an open unit writes its own dated entry (field case: releases 1.44.0-1.46.0 left none).**

**2026-10-19 — release 1.46.0 tagged, never published.** Docs site `--zip`. Tags
v1.46.0 / kb-v1.29.0 / mkt-v0.24.0 / course-v0.1.0-beta.11 on cec9661; its content ships
in 1.47.0 instead.

**2026-10-19 — release 1.45.0 completed.** Published and verified on the registry, each on
latest: code 1.45.0, KB 1.28.0, marketing 0.23.0, Course 0.1.0-beta.10 — F-071 (intent
focus and efficiency) plus the docs site's merge/E2E links and newest-first Features.
Tags on b45e132. It includes 1.44.0 (F-071, tags on 3942181), which was never published.

**2026-10-18 — release 1.43.1 completed.** Published and verified on the registry: code
1.43.1, KB 1.26.1, marketing 0.21.1, Course 0.1.0-beta.8 — the F-072 `--open` field fix,
closing F-072. Tags on 803427a.

**2026-10-18 — release 1.43.0 completed (F-074, the owner interview for every Vision).** Published and verified on the registry: code 1.43.0, KB 1.26.0, marketing 0.21.0, Course 0.1.0-beta.7, each on latest; tags v1.43.0 / kb-v1.26.0 / mkt-v0.21.0 / course-v0.1.0-beta.7 on 9f0003e. kb and Course appeared on the registry minutes after the publish (propagation, not a failure). The F-072 `--open` fix followed as patch 1.43.1 (entry above).

**2026-10-18 — release 1.42.0 completed.** Published and verified on the registry at
22:29–22:30 UTC (2026-10-17): code 1.42.0, KB 1.25.0, marketing 0.20.0, Course
0.1.0-beta.6 — the docs site (F-072), its chronology read with F-073's readers. Tags
v1.42.0 / kb-v1.25.0 / mkt-v0.20.0 / course-v0.1.0-beta.6 on daad947, published by the
owner from the clean `wt-release` worktree. `latest` names each new version. An install two
minutes after publishing failed with ETARGET again (npm metadata cache, not the package);
`--prefer-online` resolves it, and users installing later are not affected.

**2026-10-17 — release 1.41.0 completed.** Published and verified on the registry at
21:43 UTC: code 1.41.0, KB 1.24.0, marketing 0.19.0, Course 0.1.0-beta.5 (F-073; Course
now publishes on `latest` with no promotion step). Tags v1.41.0 / kb-v1.24.0 /
mkt-v0.19.0 / course-v0.1.0-beta.5 on 29d492b, published by the owner from the clean
`wt-release` worktree at that commit. `latest` names each new version; Course `beta` stays
on beta.4, as the policy says. A global install one minute after publishing failed with
ETARGET: npm metadata cache, not a failed publish (`--prefer-online` resolves it).

**2026-10-17 — release completed.** Published and verified on the registry: code
1.40.0, KB 1.23.0, marketing 0.18.0, Course 0.1.0-beta.4 (F1, F-068, F-069), tags
v1.40.0 / kb-v1.23.0 / mkt-v0.18.0 / course-v0.1.0-beta.4 on b1ed3ac. Published from
the primary checkout at that commit: the tarballs equal a `git archive` of the tag
except for CRLF line endings. `latest` names each new version; Course `beta` and
`latest` both name beta.4 (one-time owner promotion). From the next release Course
publishes on `latest` directly (2026-10-17 ruling, `GUIDE_release.md`). Next: ask the
K-02 field to time `graph` and `check`; `--only` opens only if `graph` stays slow.

**2026-10-08 — release completed.** Published and publicly verified: code 1.38.0,
KB 1.21.0, marketing 0.16.0 and Course 0.1.0-beta.2. Exact tagged export of
29455e2; all four public tarballs match SHA1 and SHA512. Stable latest aliases
name the new releases; Course beta and latest both name beta.2 under Antonio's
newest-default-install ruling. The publisher polling timeout was resolved by
direct registry verification without republishing. Fresh tests and package smokes
passed; release reviews PASS. F-062 is COMPLETED; its Diary and release harness
carry the durable record. C-001 stays open. Installed PC skills were not updated.

**2026-09-12 — what the tranche does NOT claim.** The read surface GREW in all three
lenses (+6.2% code, +8.2% kb, +7.8% mkt across all `.md`), even though the code and mkt
contracts shrank: the cost moved out of the file `benefit` prints rather than falling,
and kb received doctrine with no diet at all. The one blind A/B in the tranche returned
NULL (ceiling effect), so no claim there rests on an external criterion. Three WARNs and
four nits in F-053 were folded after the review cap and are, by the doctrine's own rule,
unreviewed — they are listed in that unit's closure REVIEW_LOG row.

**Version numbers that exist only as intentions.** `v1.16.0` (code) was tagged and never
published; kb 1.4.2 was bumped and never published (the registry goes 1.4.1 → 1.4.3);
and code 1.32.1 / kb 1.14.1 / mkt 0.10.1 were named as F-046's release and never existed
— its fix reached users inside the next tranche instead, because `publish_all.bat` packs
the working tree. No pushed tag is ever moved. Since kb 1.4.8 tags are **package-scoped**
(`kb-v1.4.8`), because the three packages version independently and a bare `vX.Y.Z` is
ambiguous against the code lens's own tags.

**The publish-verify trap, recorded the days it bit.** `npm view` answers from a metadata
cache, so a post-publish verify printed the PREVIOUS version and read as a failure when
the publish had succeeded. `--prefer-online` was added — and it bit a SECOND time (the
1.27.0 run reported mkt 0.4.7 when 0.5.0 had landed), because the flag forces
revalidation but cannot outrun CDN propagation of the `latest` tag. Since 1.27.1 the
block **polls** until the registry agrees with the local version. When in doubt,
`npm view <pkg> versions --json --prefer-online` settles it. Third bite, different organ:
the per-package 2FA flow waits on an ENTER before the last publish — a run abandoned at
that prompt looks complete while the remaining package never shipped (mkt 0.6.0 landed
two minutes after the other two, on a second pass). The registry `time` field settles
WHEN each version actually landed.

**A field lesson worth more than the fix it came from.** The kb recency probe read only
the first 600 bytes of a note, so a real frontmatter pushed the closing fence past the
cap and the whole probe silently skipped — a note dated three days back read "0 days old"
(fixed in kb 1.11.1). The reporting session had approved that behaviour twice on
plausible reasoning before testing it against the case in view: evidence that the review
rule "a PASS is invalid on found-nothing" extends to APPROVALS.

**Still owed in the devPNT repo**, not here: the governed `D-IC` artifact (sequence
D-UC → D-IC → P-TM → E-ISP), from F-032.

**2026-09-12 — registry cleanup.** Nineteen workstream rows were closed at once: each had
been verified against the npm registry, the git tags and the merge state, and each was
released or superseded while its row still said UNRELEASED, AWAITING MERGE or AWAITING
PUBLISH. Their durable narrative is in the matching `solutions/ANALYSIS_*.md` Diary, and
the deleted `HANDOFF_*.md` files are in git history at `08cd6c2`. Two exceptions worth
knowing: F-026's original branch commits (`50c5cf7`, `a0072cf`) are still NOT ancestors
of `main` although the question-discipline doctrine itself shipped in `elicitation.md`;
and F-046 had no ANALYSIS at all, so its record was promoted to
`solutions/ANALYSIS_per_turn_protocol_reminder.md` before its row was closed. The rows
had accumulated because closure deletes the file and closure had been deferred to an
"integration call" that the releases then made moot.
