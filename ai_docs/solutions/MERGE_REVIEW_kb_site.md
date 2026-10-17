---
feature: F-072
analysis: ANALYSIS_kb_site.md
base: main
---
# Merge review: docs site

## Purpose

`docs_site.py` writes a static, offline, read-only website showing the user what the agent reads to
orient itself and resume work. It serves the Vision's "keep understanding durable across sessions"
(ANALYSIS `## Feature Vision`; ruling r29). One generator, page and battery are shared by the four
packages.

## What to review

# Review map -- 69 files against origin/main (merge-base c2e9d333e11f)

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `.gitignore` | M | +3/-0 | REVIEW | review |
| `CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `README.md` | M | +9/-2 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +3/-0 | REVIEW | review |
| `distributions/course-creator/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/package.json` | M | +5/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/app.js` | A | +1126/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/index.html` | A | +17/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/strings.js` | A | +322/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/docs_site/style.css` | A | +288/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/docs_site.py` | A | +1282/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_files.py` | M | +7/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +7/-1 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_docs_site.py` | A | +1015/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +2/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/package.json` | M | +5/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/app.js` | A | +1126/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/index.html` | A | +17/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/strings.js` | A | +322/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/docs_site/style.css` | A | +288/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/docs_site.py` | A | +1282/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_files.py` | M | +7/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +7/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_docs_site.py` | A | +1015/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/README.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/package.json` | M | +5/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/app.js` | A | +1126/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/index.html` | A | +17/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/strings.js` | A | +322/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/docs_site/style.css` | A | +288/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/docs_site.py` | A | +1282/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_files.py` | M | +7/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +7/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_docs_site.py` | A | +1015/-0 | REVIEW | review |
| `package.json` | M | +5/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/app.js` | A | +1126/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/index.html` | A | +17/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/strings.js` | A | +322/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/docs_site/style.css` | A | +288/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/docs_site.py` | A | +1282/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` | M | +7/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +7/-1 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_docs_site.py` | A | +1015/-0 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +4/-4 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_kb_site.md` | A | +470/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_kb_site.md` | A | +200/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/MERGE_REVIEW_kb_site.md` | A | +178/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/PROPOSAL_vision_v9_state_view.md` | A | +193/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/architecture.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/existing_features.md` | M | +1/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +9/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/project_vision.md` | M | +64/-14 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/vision/rulings.md` | M | +5/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/HANDOFF_kb_site.md` | A | +27/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/requests/REQUEST_kb_site.md` | A | +149/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/BLIND_VISION_REVIEW_2026-07-27.md` | M | +38/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +26/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_kb_site_design.md` | A | +142/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_kb_site/probe.py` | A | +377/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/INDEX.md` | M | +1/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/audit/handoff.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/memory/INDEX.md` | M | +9/-5 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 49 files (+16317/-7); DESIGN 10 files (+1125/-21); EVIDENCE 6 files (+759/-0); GENERATED 4 files (+12/-6)

The 36 REVIEW rows under `distributions/` are byte-identical copies of the six files under
`skills/agentic-sdlc-skill/`. `shared_files.py` reports "28 shared files are identical across all
four distributions", so review the six originals plus each distribution's `package.json`,
`SKILL.md`, `README.md`, `CHANGELOG.md` and `shared_files.py`.
`PROPOSAL_vision_v9_state_view.md`, `project_vision.md` (v9) and the design-review documents came
from the specification commits already on this branch (dd46dca and earlier). They are not part of
this implementation.

## Already verified

- **Closure review, 4 rounds, final verdict PASS.** Two REVIEW_LOG rows of 2026-10-17: "F-072 implementation
  diff" (rounds 1-2, FAIL -> PASS) and "F-072 owner-requested additions R24-R26" (rounds 3-4,
  FAIL -> PASS). Tier closure, deep, the same fresh-context subagent (rung 1), opened with the
  REVIEW MANDATE block. Round 4 ran beyond the cap on the owner's instruction (REQUEST R27).
  - Round 1 raised 2 BLOCK and 9 WARN; all were fixed and its notes list each one.
  - Round 2, scoped, gave PASS on every finding. The reviewer re-ran the four batteries and mutated
    each fix in a scratch copy; every mutant went red.
  - One new WARN from round 2 (N1: the side-bar Map kept the Everything view) was fixed after the
    verdict and checked as in the next item.
- **Tests and checks, run on the final tree (2026-10-17, HEAD dd46dca + working tree) after the last
  code edit:**
  - all four batteries `OK` (code 334 tests, 1 skipped; kb 525, 15 skipped; mkt 346, 14 skipped;
    course 341, 19 skipped), with `python -m unittest discover -s <skill>/scripts -p "test_*.py"`
    in each skill folder;
  - `node --check app.js` passes;
  - `shared_files.py` reports ok;
  - `sdlc_check.py check` and `check --hybrid` both report CLEAN.
- **Design gate:** closed by the owner after five rounds (REQUEST_kb_site.md R23;
  `audit/reviews/REVIEW_kb_site_design.md`).
- **Owner decisions** are in `audit/requests/REQUEST_kb_site.md`:
  - R10 and R13: per-item counts;
  - R11 and R12: Vision v9;
  - R13 and R15: the cost of the `SKILL.md` line. It is now 130 bytes, under the "about 160"
    accepted; r29 records the figure;
  - R14: one shared family file;
  - R17: page names and empty pages;
  - R20: the purpose;
  - R22 and R23: the chronology and the audit pages;
  - R24 and R25: each analysis read as its chain (Vision, use cases, flows and interfaces, risks,
    solution study, design and tests, merge brief and E2E script, Diary) and the Vision's North
    Star above the home page;
  - R26: the owner found the guides missing; the answer is a Guides page of its own;
  - R27: the fourth review round.
- **Probe:** `harness_kb_site/probe.py --root .` exits 0 on this repository. The site's counts match
  it: 6 open workstreams, 59 analyses, 298 catalog documents.
- **Rendering:** the three fixture sites were rendered from `file://` in headless Edge by the author
  and by the reviewer, with no console errors. The author walked the map, fact panels and search
  over local http with the owner watching in the browser pane.
- **Packaging:** `npm pack --dry-run` lists the five runtime files in each package and no `test_*.py`.
  The reviewer ran it in round 1; the file lists have not changed since.
- **Not covered by any review:** two document fixes made after the round-4 PASS (the spec's
  address list; the Diary's wording on R26, with R27 recorded). No code changed after it.

## Your judgement

- **Deviation from the design:** criterion 3, the chronology, is not met. The reader waits for
  F-073's dated-entry rules (branch `doctrine-chronology`, still handoff only). Until then the page
  says in one line that dated events appear as documents record them, and "Lately" on the home is
  empty. Ruling r29 and the CHANGELOGs describe the chronology as a page that waits for F-073.
  - Decision: merge now with the chronology empty, or hold the merge until F-073 lands.
- **Spec amended during implementation, on the owner's requests:** R24-R26 (criterion 15, the Home
  and Rules/Guides paragraphs, the pages table), each recorded verbatim and reviewed in rounds 3-4.
- **Changes beyond the spec's letter, made on the owner's request during the session:**
  - map navigation: a topic click opens the close-up, zoom buttons, a collapsible legend, system
    cursors;
  - a layout for windows narrower than 1000 px (the spec promises 1024 px);
  - labels on every node wherever they fit without collision.
  None of them adds data, counts or ordering.
- **Open questions for the owner:**
  - Is the one-topic close-up readable by someone who does not know the skill? The owner raised it.
    A two-column redesign is proposed and not applied.
  - Is the map readable and fast at about 6,240 nodes, with the labels now computed for every node?
    This is CANNOT VERIFY here.
- **Accepted residuals:**
  - The statement-mark test enumerates `f.text` reads, not bracket reads.
  - `orientation_sources` matches four roles by position; a fifth `orient_docs` source turns the
    battery red rather than reaching the home.
  - The page is checked in Chromium only.
  - The North Star banner, the `?at=` landing and the side-bar Map reset are covered by the E2E
    script only (S11, S14, S15); `chainStrip` is tested in Node.
  - `build_guides` names the router path itself instead of taking it from `orient_docs`.
- **CANNOT VERIFY**, for the owner's field run on the work machine: per-item counts, passages and
  inferred classes on the field knowledge base; the map at about 6,240 nodes; Firefox; the full
  interactive walk. All of these are in `E2E_TEST_kb_site.md`.
- **Release:** one release across the four packages, after F-073. CHANGELOGs are prepared under
  `[Unreleased - 1.41.0]`, `[Unreleased - 1.24.0]`, `[Unreleased - 0.19.0]` and
  `[Unreleased - 0.1.0-beta.5]`. The versions are not bumped (`GUIDE_release.md`).

## Merge notes

- **Generated files** (`ai_docs/INDEX.md`, `audit/handoff.md`, `memory/INDEX.md`,
  `strategic/features_history.md`): on a conflict, regenerate with `sdlc_check.py index`; never
  resolve them by hand.
- **`audit/audit_plan.md`:** was marked on a dirty tree, so it carries a UTC timestamp. After a
  squash or rebase merge, re-run `sdlc_check.py mark` on the integration branch.
- **`.gitignore`:** gains `.docs-site/`, the default output folder.
- **`audit/HANDOFF_kb_site.md` stays open.** Its next step is the chronology reader once F-073 is
  merged, then the field run and the release. It also lists what the owner set aside for later:
  a page explaining the skills, and a validator check on the analysis's chain headings.
- **Testers:** hand them `solutions/E2E_TEST_kb_site.md` (S1-S16). S13 (chronology) waits for
  F-073.
- **Scope boundary:** in Hybrid projects the devPNT GUI already shows milestones, plans and
  governed artifacts; this site reads only the filesystem and stays Standalone-first.
