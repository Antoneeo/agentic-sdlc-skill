---
description: F-055 - relicense the skill packages from MIT to Apache-2.0 with a NOTICE, so a redistributed skill carries its author's attribution while every use inside a user's own project stays unconditional; also ships the license text no package carries today.
status: COMPLETED
feature: F-055
id: F-055
start_date: 2026-09-13
end_date: 2026-09-13
level: L3
branch: feat/apache-license
---
# ANALYSIS: Apache-2.0 with NOTICE (F-055)

## Precedent placement

Against `vision/rulings.md`: **r15** ADMIT (packaging, installation, distribution) — the
license a package ships under, and the files stating it, are distribution; **r14** exempt
(defect fix) — every package declares `"license": "MIT"` and none ships the text (P3: zero
`LICENSE` files). No REJECT row matches; no command, check, template or doctrine changes.

## Ceremony budget

No step, field or check is added to a user's process at any level. Costs outside it: one
`SKILL.md` frontmatter line per lens (`license: Apache-2.0`, about 20 bytes, loaded with the
skill and counted by `sdlc_check.py benefit`); `LICENSE` (11 KB) and `NOTICE` in each
installed folder, which skill loaders do not read and `benefit` (`*.md` only) does not
count; one license check in each repository's dev tests, not shipped.

## Objective

Relicense `@antoneeo/agentic-sdlc-skill`, `@antoneeo/kb-agentic-skill`,
`@antoneeo/mkt-agentic-sdlc-skill` (this repository) and `@antoneeo/distill-skill` (its
own repository) from MIT to Apache-2.0 with a NOTICE, from their next versions.
Apache-2.0 attaches its conditions to redistribution (§4): a copy passed on carries the
License (§4(a)), and a modified version keeps the NOTICE's attribution notices
(§4(c)–(d)). Using a skill in one's own project owes nothing.

The license is the copyright holder's decision; the owner's attribution interest is not
claimed as a Vision benefit. What the Vision governs is that every package ships its terms
(r15) and that the terms never condition what *The user's guarantee* protects.

## Feature Vision

`vision/project_vision.md` — Status APPROVED (v8).

- **Goal "installable, upgradable and maintainable … packaging, distribution … part of the
  product"**: each package, and each installed copy, states its terms.
- **Team lead Actor** (one process on the clients the team uses): an organisation adopts a
  dependency through its license; a standard OSI license whose text ships in the package
  clears that step, and Apache-2.0 adds the explicit patent grant (§3) MIT lacks.
- **The user's guarantee**: nothing it enumerates — creating, reading, editing or
  validating documents, their number, any outcome reached locally, continued access —
  meets a condition, because §4's conditions attach to redistribution only. The two cases
  where a user's published repository could be read as redistribution are closed by an
  explicit permission of the copyright holder (B3): documents the skills create or
  template in that project, and a copy of the validator and its tests placed there to
  check that project's own documents (`ENFORCEMENT.md` §2); where it is published and how
  it stays there: Interface Contract, T6.
- **Non-Goals**: no work-management surface; no second triage authority; the ceremony
  above is disclosed and nothing lands at L1; no coupling — Apache-2.0 is a license, and
  `license:` is a field the clients' skill layout defines, which that rule does not reach.
- **Success Signals**: #2 — `check` is already NOT CLEAN on this branch's base (stale audit
  areas, pre-existing); this change adds no finding. #5 unchanged.

Out of scope: published versions stay MIT (a granted license is not revocable, so it is
stated instead); per-file license headers; attribution text in user projects; the publish
(owner's step, `GUIDE_release.md`); the standalone `kb-agentic-skill` and `mkt_agentic_sdlc`
checkouts, which do not produce the packages. Actors: Solo developer, Team lead.

## Use Cases / User Needs

Buckets: *npm package page* (the README, `GUIDE_release.md`) EXISTS · *installed skill
folder* (README: "the full skill folder") EXISTS · *validator* (`ENFORCEMENT.md` §2)
EXISTS · *templates* (`templates.md`, extracted by `init.js`) EXISTS · `LICENSE`,
`NOTICE` NEW.

- **UC1 — Solo developer installs and uses a skill.** Nothing new is asked of them; the
  installed skill folder states its license. Traces to: Goal *installable, maintainable*;
  the user's guarantee.
- **UC2 — Team lead clears the dependency** from the npm package page, the repository or
  the tarball: a standard license, its text, its notice. Traces to: Team lead Actor; Goal
  *packaging is part of the product*.
- **UC3 — Solo developer or Team lead copies the validator into their repository for CI**
  and publishes that repository: no step is added and nothing is owed. Traces to: the
  user's guarantee (validation); `ENFORCEMENT.md` §2.
- **UC4 — Solo developer or Team lead publishes a repository whose `ai_docs/` started from
  the templates**: the documents are theirs. Traces to: the user's guarantee (documents).

## Functional Spec

Behavior:

- **B1** Every package version after this change carries the Apache-2.0 text and a NOTICE
  at its package root and beside `SKILL.md` in its skill folder, and says `Apache-2.0`
  wherever it states a license: its package metadata, its `SKILL.md` frontmatter and, for
  distill, its plugin manifest.
- **B2** Installing any of the four packages places `LICENSE` and `NOTICE` beside
  `SKILL.md` in each client's skill directory.
- **B3** Each README has a `## License` section stating: Apache-2.0 and the copyright line;
  whoever redistributes the skill, or a version they modified, keeps `LICENSE` and
  `NOTICE`; "Using the skill in your own project carries no obligation" — the documents it
  creates or templates there are the user's, and so is a copy of the validator and its
  tests placed in that project to check its own documents (distill, which ships neither,
  states the first clause only); the last version released under MIT.
- **B4** A NOTICE carries attribution only. The family text, identical in all six places in
  this repository:

  ```text
  Agentic SDLC skill family
  Copyright 2026 Antonio Pinto

  This product includes software developed by Antonio Pinto
  (https://github.com/Antoneeo/agentic-sdlc-skill).
  ```

  distill's is the same with `distill` and `https://github.com/Antoneeo/distill`.

Cases: an installed copy (no package metadata) still states its license in `SKILL.md`; a
CRLF checkout is not a different license text; a user on an installed MIT version keeps
MIT until they update; the NOTICE never carries the permission, because every line of it
binds downstream modified versions (§4(d)) and a fork's README would not hold the grant
it pointed to; a future package that drops a file from its tarball or alters the text
fails the tests, not a user.

Acceptance criteria:

- **AC1** The published tarball of each package contains `LICENSE` and `NOTICE` at its root
  and in its skill folder.
- **AC2** Installing each of the four packages leaves `LICENSE` and `NOTICE` in every
  installed skill folder.
- **AC3** Every `LICENSE` in both repositories is the canonical Apache-2.0 text, line
  endings aside.
- **AC4** Every place a package states its license says `Apache-2.0`.
- **AC5** Each README carries B3.
- **AC6** Each CHANGELOG carries an unreleased entry naming the change and the last MIT
  version.
- **AC7** The product's own tests pass in both repositories, and the family's shared-file
  guard covers `LICENSE` and `NOTICE`.

## Interface Contract

Surfaces: the npm package page (README, license metadata); the repository page (it detects
a root `LICENSE`); the tarball, where license scanners look first; the installed skill
folder; `SKILL.md` frontmatter (read by skill indexes and agents); distill's Claude plugin
manifest.

Flow: owner release (`GUIDE_release.md`) → tarball filtered by the `files` allowlist →
`npm install` → `postinstall` → the package's `lib.js` copies the skill folder → each
client's skill directory carries `LICENSE` + `NOTICE`. Distill's plugin route installs the
same folder from its repository.

Idioms reused: the Apache convention names `LICENSE` and `NOTICE`, without extension —
which also keeps them outside the `*.md` orphan checks. Each README's license text stays
where it is: root and kb replace the one-line `MIT (c)` under `## Created By` with a
`## License` section placed right after it; mkt and distill keep their `## License`.

The permission's publication point is the README, read before install on the npm page and
the repository. The installed folder carries `LICENSE` + `NOTICE` only: a user holding just
the folder owes nothing for local use (§4 binds redistribution), and the grant exists
whether or not they read it. Feedback to a software actor: the release battery's
`npm pack` listing.

Flag: an omitted `files` entry silently drops a file from the tarball (P1), answered by
the tests (T4).

## Capability Ledger

| Capability | Verdict | Component / gap | Evidence |
|---|---|---|---|
| state the license terms inside every published package | INADEQUATE | every `package.json` declares MIT; no license text exists in either repository; `files` is an allowlist | P3 red: 0 `LICENSE` found; P1: nothing unlisted is packed except a root `LICENSE` |
| carry a package's skill folder into every client | EXISTS | each package's `scripts/lib.js#copyRecursive` (four installers, same body), called by its `scripts/postinstall.js` on the skill folder | P2, all four packages: files placed in the folder reach every client home |
| keep the family's shared files identical | EXISTS | `skills/<lens>/scripts/shared_files.py#SHARED_FILES` + `test_drift.py` beside it | read `test_the_copies_are_identical_to_each_other`; digests ignore line endings |
| assert what a package declares against what it ships | EXISTS, extended | lens batteries: pattern of `test_the_installed_skill_says_which_version_it_is`; distill: `scripts/test_clients.js` bump-point sync test | read both: frontmatter regex + package metadata; the lens test skips on installed copies |

Guides: `GUIDE_release.md` consulted; no high-complexity component modelled, so no comprehension guide is due.

## Impact

This repository:

| Path | Change | Why |
|---|---|---|
| `LICENSE`, `NOTICE` (repository root = code package root) | ADD | B1; repository license detection |
| `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/{LICENSE,NOTICE}` | ADD | B1: tarball root |
| `skills/agentic-sdlc-skill/`, `distributions/kb-agentic-skill/skills/kb-agentic-skill/`, `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/` — `{LICENSE,NOTICE}` each | ADD | B1, B2 |
| `package.json`, `distributions/{kb-agentic-skill,mkt-agentic-sdlc}/package.json` | MODIFY | `license`; `files` += `NOTICE`, `skills/<name>/LICENSE`, `skills/<name>/NOTICE` (npm packs a root `LICENSE` unasked, P1) |
| `skills/<lens>/SKILL.md` ×3 | MODIFY | frontmatter `license: Apache-2.0` |
| `README.md` ×3 | MODIFY | B3; the installed-folder bullet (root, kb) and the Runtime Shape tree (root) list the two files |
| `CHANGELOG.md` ×3 | MODIFY | `[Unreleased - 1.34.0]`, `[Unreleased - 1.17.0]`, `[Unreleased - 0.12.0]` |
| `skills/<lens>/scripts/shared_files.py` ×3 (shared) | MODIFY | `SHARED_FILES` += `LICENSE`, `NOTICE` |
| `skills/<lens>/scripts/shared_manifest.json` ×3 | REGENERATE | `shared_files.py --update` |
| `skills/<lens>/scripts/test_skill_invariants.py` ×3 (shared) | MODIFY | the `ShippedLicense` tests (five, one behaviour each) |
| `ai_docs/` | ADD, MODIFY | this analysis, `harness_apache_license/probe.py`, `audit/HANDOFF_apache_license.md`, `REVIEW_LOG.md` row, regenerated indexes |

`distill-skill` repository (no `ai_docs/`: this analysis is its design record): ADD
`LICENSE`, `NOTICE`, `skills/distill/{LICENSE,NOTICE}`; MODIFY `package.json` (`license`,
`files`), `.claude-plugin/plugin.json` (`license`), `skills/distill/SKILL.md` (frontmatter),
`README.md`, `CHANGELOG.md` (`[Unreleased - 0.9.0]`), `scripts/test_clients.js` (the license
check; its bump-point test's "ONE file … the only file a client gets" becomes three files).

Blast radius, enumerated with grep (no symbol-graph index covers either repository):

- `SHARED_FILES` — `shared_files.py`: `cross_distribution_report`, `current`, `report`,
  `_cli`; `test_drift.py`: the missing, diverged, manifest-coverage, entry-point and
  cross-distribution tests. Two more paths of the same shape; no consumer changes.
- `SKILL.md` frontmatter readers — `lib.js` (`^name:`), `test_the_skill_name_matches_the_manifest`
  (`name:`), the version tests (`^version:`, lens and distill), `benefit` (byte size): none
  matches a `license:` line.
- Skill-folder content checks — `test_every_support_file_on_disk_is_declared` and
  `test_support_files_wired` glob `*.md`, so extensionless files are outside them.
- Package READMEs are read by no lens test; distill's bump-point test reads its README for
  the version string only.

## Security and Threat Model

Surfaces: filesystem only — each installer copies two more static files through its
unchanged `copyRecursive`. No input parsing, network, credentials, cryptography or personal
data. The substantive risks are to the license contract:

| # | Threat | Answer |
|---|---|---|
| T1 | Relicensing without the right to | one author name across the full history of both repositories and of the standalone kb and mkt checkouts (`git log --format=%an`); co-authored commits name Claude models, which hold no rights, and Anthropic's terms assign any rights in outputs to the user |
| T2 | Published MIT versions stay MIT and can be forked without a NOTICE | accepted and disclosed: B3 and each CHANGELOG name the last MIT version |
| T3 | A redistributor drops the NOTICE | for a modified version, a breach of §4(d); for a verbatim copy, the NOTICE is part of the Work passed on. By construction it sits in the folder every copy, install and fork carries |
| T4 | A `files` omission ships a package without its terms | tests: every file present and listed; release `npm pack` check |
| T5 | A non-canonical or corrupted `LICENSE` (ambiguous terms, misdetection) | tests: LF-normalized canonical SHA-256 |
| T6 | Terms reaching what the user's guarantee protects | §4 conditions only redistribution; B3 permission for created or templated documents and the vendored validator; tests keep the permission in each README |
| T7 | Two places state different licenses | lens tests: package metadata equals `SKILL.md`; distill test: `package.json`, `plugin.json` and `SKILL.md` agree |
| T8 | The §3 patent grant and its termination on litigation | accepted: the grant reaches only claims a contribution itself infringes, whatever the owner holds; the termination protects users |

## Action Plan

1. RED: add the license test to the code lens battery and to distill's `test_clients.js`; both fail.
2. Add the twelve `LICENSE`/`NOTICE` files (a pair at each package root and in each skill folder); edit the three `package.json` and `SKILL.md`.
3. `SHARED_FILES` += `LICENSE`, `NOTICE`; carry `shared_files.py` and the test to kb and mkt; `shared_files.py --update` in each lens.
4. GREEN: the three batteries.
5. READMEs and CHANGELOGs ×3.
6. distill: license files, manifests, README, CHANGELOG, test; `npm test` green; `npm pack`.
7. Verify: probe harness green over the four packages and both repositories, `npm pack` ×4, `sdlc_check.py check` adds no finding, `sdlc_check.py index`.
8. Closure review (moment 2) on both diffs; hand the commit and the release to the owner.

## Test Strategy

- **Lens tests** (`ShippedLicense`, shared battery, one behaviour each, skipped on an
  installed copy): package metadata and `SKILL.md` both say `Apache-2.0`; both `LICENSE`
  (package root, skill folder) hash, LF-normalized, to the canonical SHA-256; the root
  `NOTICE` equals the skill-folder one; `files` lists `NOTICE`, `skills/<name>/LICENSE` and
  `skills/<name>/NOTICE`; the README contains "Using the skill in your own project carries
  no obligation". Each red first. Covers AC1, AC3–AC5, T4–T7.
- **distill tests** (`test_clients.js`): the same five, with `plugin.json` in the first.
  Each red first. Covers AC1, AC3–AC5 for distill.
- **Batteries** for code, kb and mkt — the drift guard holds the three skill-folder NOTICEs
  identical (B4), the lens tests the root ones — and distill `npm test` (AC7).
- **Probe harness** `harness_apache_license/probe.py`: P1 the packaging mechanism; P2 a
  sandboxed install of each of the four packages (AC2); P3 the canonical text in both
  repositories (AC3); plus `npm pack --dry-run --json` on the four real packages (AC1).
- **Read check**: the CHANGELOG entries (AC6).

## Diary

- 2026-09-13 — L3, router `GUIDE_release.md`. Probes before design: P1, P2 green; P3 red (no
  license text today). Base `790b90c`, distill `847488c`. Design review PASS in two rounds.
- 2026-09-13 — Implemented on both branches, nothing committed. Batteries: code 202, kb 388
  (14 skipped), mkt 220 (13 skipped), distill 60; probe harness 54 checks, all claims hold;
  `npm pack` ×4 carries both pairs; `validate` findings identical to the base. Each license test
  was seen red before its code: five loops in the code lens, the carried class red ×5 in kb and
  mkt before their files, five loops in distill. Closure review PASS; `check` stays NOT CLEAN on
  the base's stale areas only. No architectural decision, so no ADR. Next: the owner's commit.
- 2026-09-14 — Owner-requested after the closure review: the four READMEs and CHANGELOGs ask, as
  a request and not a license condition, for a mention when a skill is used in commercial work,
  with a ready-made badge. B3 and the user's guarantee are unchanged; this addition is unreviewed.
