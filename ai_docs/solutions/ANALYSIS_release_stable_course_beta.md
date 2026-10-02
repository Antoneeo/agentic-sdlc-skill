---
id: F-062
feature: Stable family release and course beta
description: Release preparation, channel separation, verification and publication record.
status: IN_PROGRESS
level: L3
domain: code
start_date: 2026-10-02
end_date:
---
# Stable family release and course beta

## Objective
Release the pending software, knowledge and marketing changes on npm latest;
release course-creator as an explicit beta. Antonio authorized commit and publication
on 2026-10-02. Work remains in the primary main checkout. Course content production
C-001 stays open and is not certified by releasing its authoring skill.

## Feature Vision
The approved project Vision's shared-core family and proportional governance guide
this maintenance increment. The approved VISION_course_creator governs the course
capability. No Vision change or claim of demonstrated human learning is introduced.

## Use Cases / User Needs
- Maintainer publishes the stable packages and the course beta without accidentally
  promoting the beta to latest.
- Early adopter deliberately selects the beta and sees its experimental limits.
- Next maintainer can distinguish published versions from completed local tests.

## Functional Spec
1. Bump software to 1.37.0, knowledge to 1.20.0, marketing to 0.15.0 and course to
   0.1.0-beta.1. Registry latest is currently 1.36.0 / 1.19.0 / 0.14.0; course returns
   E404. Recheck target versions before publication.
2. course package publishConfig declares beta. Publisher reads each package's tag,
   defaults to latest for stable packages, passes it to publish and verifies that tag.
3. Re-run all four Python suites, package allowlists, course client installer tests
   and temporary-project initialization. Existing synthetic debugging results remain
   bounded evidence, not generalized efficacy measurements.
4. Reconcile audit references only after reviewing changed surfaces and derived
   documents. Legacy nonfatal warnings remain disclosed; do not fabricate past reviews.
5. Commit release files deliberately. Exclude ongoing course presentation/rendering
   work and local dependencies. Publish an export of the exact tagged commit if that
   work leaves main dirty; an export has no unrelated user edits.

## Interface Contract
The maintainer invokes the existing publisher. Stable consumers use latest; beta
consumers explicitly select beta. Publication failures return failure. npm browser
authorization remains human-owned and, if required, publication remains pending.

## Capability Ledger
| Capability | Verdict | Evidence |
|---|---|---|
| Stable publication | EXISTS | publish_all.bat :pub / :verify |
| Separate course beta | INADEQUATE | publisher currently uses bare npm publish and queries latest for every package |
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
6. Commit on main, tag each package, push; publish exact committed packages and verify
   registry versions and tags. Record a genuine authentication blocker if encountered.

## Test Strategy
Publisher mock executes the real batch file with a fake npm command in a temporary
PATH. Assert stable latest, beta course, existing-version skip and verification failure.
Python tests, course Node client tests, dry-run packing and temporary initialization
exercise deployed contracts. Post-publication registry queries check all versions and
the course beta tag; latest must not point at this prerelease. Preserve logs in the
release harness, outside npm allowlists.

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
