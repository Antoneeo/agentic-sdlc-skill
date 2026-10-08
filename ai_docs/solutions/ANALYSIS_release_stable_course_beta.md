---
id: F-062
feature: Stable family release and course beta
description: Release preparation, channel separation, verification and publication record.
status: COMPLETED
level: L3
domain: code
start_date: 2026-10-02
end_date: 2026-10-08
---
# Stable family release and course beta

## Objective
Publish the reviewed family increments using GUIDE_release.md: code 1.38.0,
KB 1.21.0, marketing 0.16.0 and course 0.1.0-beta.2. Antonio requested execution
on 2026-10-08 and requires default Course installation to receive its newest
version. Course retains beta and is explicitly promoted to latest after publication.
Use the isolated release branch and exact tagged export. C-001 content stays open;
releasing its authoring skill does not certify course readiness or human learning.

## Feature Vision
The approved project Vision's shared-core family and proportional governance guide
this maintenance increment. The approved VISION_course_creator governs the course
capability. No Vision change or claim of demonstrated human learning is introduced.

## Use Cases / User Needs
- Maintainer publishes the stable packages and explicitly promotes the newest
  Course version to latest under the owner's 2026-10-08 ruling.
- Course users receive the newest version through default install or beta and see
  its experimental limits.
- Next maintainer can distinguish published versions from completed local tests.

## Functional Spec
1. Bump software to 1.38.0, knowledge to 1.21.0, marketing to 0.16.0 and course to
   0.1.0-beta.2. Preflight baseline: 1.37.0 / 1.20.0 / 0.15.0 and course beta.1.
   Recheck each target version before publication.
2. course package publishConfig declares beta. Publisher reads each package's tag,
   defaults to latest for stable packages, passes it to publish and verifies that tag.
3. Re-run all four Python suites, package allowlists, course client installer tests
   and temporary-project initialization. Existing synthetic debugging results remain
   bounded evidence, not generalized efficacy measurements.
   Run the existing publisher's beta verification before explicit Course promotion.
   Then add latest to course beta.2 and verify both beta and latest directly. The
   unchanged publisher guard can reject a rerun after intentional promotion;
   direct registry version/hash/channel evidence certifies the final state.
4. Reconcile audit references only after reviewing changed surfaces and derived
   documents. Legacy nonfatal warnings remain disclosed; do not fabricate past reviews.
5. Commit release files deliberately. Exclude ongoing course presentation/rendering
   work and local dependencies. Publish an export of the exact tagged commit if that
   work leaves main dirty; an export has no unrelated user edits.

## Interface Contract
The maintainer invokes the existing publisher, then explicitly promotes Course
to latest. Default and beta Course installs resolve to its newest published version.
Publication failures return failure. npm browser
authorization remains human-owned and, if required, publication remains pending.

## Capability Ledger
| Capability | Verdict | Evidence |
|---|---|---|
| Stable publication | EXISTS | publish_all.bat :pub / :verify |
| Explicit Course publication and promotion | EXISTS | publisher :channel selects beta; owner-authorized npm dist-tag add selects latest after stock verification |
| Version metadata and package allowlists | EXISTS | four package.json, gemini-extension.json, SKILL.md and CHANGELOG.md files |
| Shared-core drift detection | EXISTS | shared_files.py: 22 identical files across four distributions |

## Impact
| Files | Change and rationale |
|---|---|
| publish_all.bat | :pub and :verify keep their two-argument signatures; resolve publishConfig.tag locally, use version-specific existence check, publish/verify intended channel; fail verification explicitly |
| ai_docs/solutions/harness_release_stable_beta/test_publisher.py | execute real batch with mock npm; validate routing, skips and failure propagation |
| ai_docs/solutions/harness_release_stable_beta/verify_packages.py and its RESULTS/verification/test logs, ai_docs/audit/HANDOFF_release_stable_course_beta.md | package/scratch checks and truthful publication resume state |
| distributions/course-creator/scripts/init.js, scripts/test_clients.js beneath that package | generated install pointer explicitly selects beta; existing init test verifies it |
| distributions/course-creator/skills/course-creator/ENFORCEMENT.md | describe per-turn reminder as manual in this beta, matching the actual installer |
| package.json, gemini-extension.json, skills/agentic-sdlc-skill/SKILL.md, CHANGELOG.md | software version and release entry |
| distributions/kb-agentic-skill/{package.json,gemini-extension.json,CHANGELOG.md}, skills/kb-agentic-skill/SKILL.md beneath that package | knowledge version and release entry |
| distributions/mkt-agentic-sdlc/{package.json,gemini-extension.json,CHANGELOG.md}, skills/mkt-agentic-sdlc/SKILL.md beneath that package | marketing version and release entry |
| distributions/course-creator/{package.json,gemini-extension.json,CHANGELOG.md,README.md}, skills/course-creator/SKILL.md beneath that package | beta version, publishConfig.tag and explicit installation/limitations |
| ai_docs/reference/GUIDE_release.md and its source snapshot | accepted release instruction amended for beta and clean commit export |
| ai_docs/strategic/architecture.md, audit/audit_plan.md, audit/project_notes.md, audit/reviews/REVIEW_LOG.md | package location, actual review references and release evidence |
| ANALYSIS_evidence_driven_debugging.md, ANALYSIS_course_slide_content.md and their HANDOFF files | close implemented units after gate passes; retain C-001 content handoff |
| ai_docs generated indexes and feature history | regenerate from authoritative originals |

Batch labels have no external API callers: all :pub/:verify call sites are in
publish_all.bat and retain their existing arguments. No application data migration
or retired protection. Existing presentation/work trees remain outside this release.

## Security and Threat Model
Public release is immutable; inspect npm pack allowlists and export the tagged commit.
Do not disclose npm credentials or automate browser authorization. prerelease version
alone does not choose beta: explicit publish tag and channel verification are required.
No force push or moved existing tag. Filesystem packaging does not include local
course sources, internal governance, eval artifacts or dependencies.

## Action Plan
1. Independent design review of this increment before publisher edits.
2. Apply beta routing, version metadata and documentation changes.
3. Run publisher mocks (channel, skip and failure), four-suite tests and package smoke.
4. Independent closure review of release diff and previously uncommitted integration.
5. Refresh audit references and indexes, require plain and Hybrid gates CLEAN.
6. Commit on the release branch, tag each package, fast-forward origin/main; publish
   exact committed packages, promote Course latest and verify registry hashes/tags.
   Record authentication expiry separately from pending registry processing.

## Test Strategy
Publisher mock executes the real batch file with a fake npm command in a temporary
PATH. Assert stable latest, beta course, existing-version skip and verification failure.
Python tests, course Node client tests, dry-run packing and temporary initialization
exercise deployed contracts. Post-publication registry queries check all versions and
the course beta and latest tags, both at beta.2 under the owner's current ruling.
Preserve evidence in the release harness, outside npm allowlists.

## Diary / Current State
2026-10-02: design drafted. Three stable suites, three pack allowlists and three init
smokes passed. Shared core: 22 files identical. Plain check rc=1 due to stale area
references; validate has zero errors and 18 legacy warnings. Hybrid rc=0 skips staleness
and does not substitute for Standalone closure. Course full suite is running.
Design review PASS (fresh context, different model gpt-6-astra). Two WARNs resolved:
harness path named; all four verify callers must propagate subroutine failure.

Release and integration reviews PASS. Beta init pointer, manual-hook documentation
and JSON example corrected and independently reread. All four suites, course clients
(4 pass/1 skip), four package allowlists and fresh init+scratch check pass. Publisher
mocks 4/4 pass, including omitted stable tag and verification failure. No runtime
architecture introduced by the release maintenance; existing F-058 ADR remains.

Final suites: 228/414/251/245 tests, 49 skips across 1,138 enumerated; no failures.
Four package allowlists and fresh-project checks pass. npm login succeeded; target
versions are absent on the registry. Evidence in harness_release_stable_beta.

Standalone repository check CLEAN after reviewed audit references refreshed.
F-060 and F-061 implementation closure recorded; F-062 publication still pending.
Commit 3e56773 and four tags pushed to main; npm accepted all packages. Public
tarballs match their publication SHA1. Direct dist-tag endpoint shows three stable
targets, but npm also assigned latest to the first course beta. Removal authorized
by the beta-only scope completed browser authorization, but registry DELETE returned
E400. Owner decision on the residual alias is pending; beta-only closure remains open.
Explicit channel isolation was added to the existing verification after a failing
mock demonstrated false success. Seven mocks now pass, including failed or empty
tag queries. Independent guard review PASS; conditional manual-removal hint resolves
its WARN. Release tags stay on 3e56773.


2026-10-08: owner requested GUIDE_release.md execution and superseded beta-only
Course policy: default installation must receive its newest version. Guide/source
and Course README updated; no publisher runtime change. Independent release
review PASS, one packed-count WARN corrected, scoped re-review PASS. Fresh suites
1162 tests/49 skips, publisher 7 pass, Node clients 53 pass plus Course 4 pass/1 skip;
four pack/init/scratch checks pass twice, final plain and Hybrid gates CLEAN.
Release commit 61eb56e and tags v1.38.0/kb-v1.21.0/mkt-v0.16.0/
course-v0.1.0-beta.2 are on origin/main and all point to that commit. Exact git
archive exported; expected package hashes recorded. First publish auth expired;
retry after owner browser confirmation accepted all four packages. Stock verify
timed out while registry was still processing (old code latest remained).
All four public tarballs match the exact tagged export in both SHA1 and SHA512.
Direct dist-tag reads confirm latest 1.38.0 / 1.21.0 / 0.16.0; Course beta and
latest both point to 0.1.0-beta.2 after owner browser authorization (rc 0).
The stock verification timeout was registry processing, resolved by direct public
verification without republishing. F-062 is COMPLETED under the current owner
channel policy. Durable hashes and tag evidence: harness_release_stable_beta/
publication_2026-10-08.json. C-001 remains open.
