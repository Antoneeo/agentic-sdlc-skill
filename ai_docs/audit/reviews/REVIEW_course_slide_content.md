# F-060 review and validation evidence
Date: 2026-09-27
Author: primary agent in the owner's working chat
Design reviewer: /root/review_slide_contract, gpt-6-astra high, independent of author
Semantic reviewer: /root/review_content_value, fresh context

## Design review
FAIL → PASS, round 2. Four findings accepted: new support omitted from npm Impact; ambiguous migration of legacy PPTX; missing general-value semantic acceptance; baseline evidence outside the repository. Corrected manifest plan, uniform legacy WARN, conceptual-course transfer test and runnable existing fixture command. Re-review confirmed UC1–UC4, Vision and threats T1–T4 coverage. Design passed before implementation.

## Code and doctrine review
FAIL → PASS, round 2. Two regressions accepted: requiring a separate check for every module violated the approved Vision, and a single module association prevented shared explanations across profiles. Optional Covers pairs now preserve cumulative checks and shared units with objective validation. Solutions cover all assessed pairs. Positive and negative integration tests added. Reviewer reran 30 course/content tests (3 symlink skips), 5 profile tests, and inspected the actual npm archive, matching the new support and validator bytes after newline normalization. No unresolved code findings.

## Semantic acceptance
Conceptual course fixture: PASS. Detailed independent record and authored output are in distributions/course-creator/skills/course-creator/evals/results/slide_content_handoff/. This was a production-contract test with an approved brief, not a complete project workflow or learner/control simulation.

C-001, 52-slide source: FAIL → PASS after limiting M3's question to A–B and B–C, both answered. Also corrected the primary explanation locator, source version label and M6's attribution to the rettifica. Final residual editorial wording 'fatto supportato dal manuale' was changed in both learner copy and explanation to 'fatto supportato dalla rettifica'; exact replacement verified by author.

Conformance: M1 explains notes versus repeatable instructions; M2 provenance; M3 scope, conflict and revision; M4 benefit/risk; M5 visible behavior, design and proof; M6 ownership; M7 maintenance and proportionate choice. S50/S51 transfer asks the learner to retain Alba's adequate note and identify Bora's conflict, dependent decision and checks, acknowledging equivalent instructions. This requires reasoned choices, not repetition of labels. All essential reasoning is visible in the self-study packet; visuals do not require the renderer to invent meaning. Sources reviewed against the registry, not an independent re-audit of snapshot bytes. Near transfer only; no human efficacy claim.

## Executed validation
- Python unittest discover over the course distribution scripts: 245 tests, OK, 19 skipped (environment/optional integration tests, including Windows symlink privilege).
- Behavioral scenario/routing suite: 4 tests, OK.
- Node client suite: 4 passed, 1 skipped (Windows symlink privilege).
- Specialist course validator C-001: 0 errors, 0 warnings.
- Actual npm pack with --ignore-scripts --offline and workspace-local cache: slide_content.md included; checked by author and independent reviewer. No publish.
- Root index regenerated. Aggregate check: validate rc=0, stale rc=1; historical documentation warnings remain. The feature stays IN_PROGRESS / closure pending; this is not a claim of a clean repository.

## Limits and final application
C-001's new learner/control simulation is not run; the old 1.0-draft simulation is retained as historical evidence and never promoted to the 2.0-content revision. Human efficacy remains unverified. Installation/publication is outside this change.

Only files differing from the recorded initial snapshot are eligible for application. The apply script checks every original file hash (and absence for additions) before any copy, backs up overwritten bytes, and records receipts in the working chat's work directory. No reset, branch change, commit or deletion of original content is authorized by this operation.
