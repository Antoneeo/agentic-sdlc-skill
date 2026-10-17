# F-063 / F-064 verification and benefit measurement

2026-10-04. For the project owner and next implementer. Implementation follows the
approved design on `codex/software-knowledge`; the Vision is unchanged. **The
comparative run does not meet F-063 FS7's reduction in reconstruction work.** F-063
remains IN_PROGRESS for that result; do not present implementation PASS as benefit.

## Mechanical verification

Final suite result is recorded in `harness_software_knowledge/implementation/`.
The test commands exercise the actual runtime, not a replacement implementation.
The new shared battery has 35 cases; its one skipped symlink case needs Windows
creation privilege, while the Windows junction case executes. Original regression
batteries retain their platform/domain skips. Final compatibility rerun:

| Distribution | Tests run | Skipped | Result |
|---|---:|---:|---|
| Software | 263 | 2 | PASS |
| KB | 449 | 16 | PASS |
| Marketing | 286 | 15 | PASS |
| Course | 280 | 20 | PASS |

Logs: `implementation/accepted-0.txt` through `accepted-3.txt`, exit 0 each.

Node installer batteries: software 53/53, KB 50/50, marketing 50/50, course 4 passed
and one skipped. Software's two installer subprocesses crashed with Windows
0xC0000409 inside the sandbox on two attempts; the unchanged battery passed outside
the sandbox using its temporary simulated homes. Other batteries passed normally.
No installation into the user's real skill folders was performed.

All four npm dry runs contain the five common resources and exclude tests/evals:
34 software, 30 KB, 33 marketing and 39 course package files. The shared guard
compares 28 files across four copies. Four new behavioral scenarios parse and seed
using the existing driver; parsing alone is not a behavioral PASS.

Review: R1 found two blocking integrity/publication defects and one diagnostic
visibility issue; three regressions reproduced them, fixes passed, R2 PASS.
See `REVIEW_software_knowledge_code_2026-10-04.md`. Legacy KB diagnosis wording
was preserved after its unchanged regression caught the difference.

Authoring budgets, measured as UTF-8 with LF: software entry delta **955 bytes**
(limit 1,800); memory **9,455 bytes** (11,000); distillation, taxonomy,
reconciliation and common templates **39,467 bytes** combined (48,000).
Portability loads only for import/export. These are text budgets, not token or
time savings.

## Two-session comparison

Rubric and fixtures were frozen before candidate execution in
`harness_software_knowledge/BEHAVIOR_RUBRIC.md`. Variants: F-057 at
`2d5a5c67402487200fe5df3929d0b093fad6e761`, that baseline with instructions only,
and the implemented candidate. Each has two distinct fresh agent contexts with
the same inputs and tasks. Session two receives retained project knowledge and
current files, without the first conversation or its metrics. Four cases are
bundled within each session, not separately timed. After session one, the retry
budget changes 3→1, the identity file is renamed and its old test-result file removed.

| Variant | S1 seconds | S2 seconds | Total seconds | S1/S2 opened paths | S1/S2 project files written |
|---|---:|---:|---:|---:|---:|
| F-057 baseline | 200.1 | 261 | 461.1 | 17 / 20 | 7 / 7 |
| Instructions only | 391.6 | 320 | 711.6 | 30 / 33 | 29 / 17 |
| Candidate | 546.7 | 535 | 1081.7 | 48 / 47 | 36 / 20 |

Counts are unique deliberate paths from each agent's explicit self-report, normalized
for separators and excluding the metrics file from project writes. They are not
syscall instrumentation or write-operation counts. All variants reopen eight input
files in S1 and seven in S2. Token counts are unavailable, not estimated. Raw metrics
and normalized counts are in `behavior/<variant>/sessionN_metrics.json` and
`behavior/comparison.json`. Wall time includes differing tool use and is exploratory.

All three second-session answers retain the four required distinctions:

- Eclosion's core PASS and 370 reported passing tests do not verify the complete
  click; two card cases were excluded and the later guard was not covered.
- Current retry budget is one when the provided configuration is passed; no
  explicit delay exists in the supplied function. Callback duration remains unknown.
- Five attempts with exponential delay remain approved DESIGN, implementation pending.
- The renamed function still selects original_id. The removed result remains
  historical; byte equality does not establish a fresh test or end-to-end behavior.

The baseline and instructions-only agent reran small local probes; the candidate
used static interpretation and explicitly reported no software test execution.
Eclosion itself was never rerun: frozen reports are received evidence. The author
read all three current Spike answers and checked their conditions against the inputs;
no task-level correction to those four answers was required. This is not an exhaustive
semantic audit of every captured claim.

Candidate S2 reused the project-property hierarchy, code/configuration dependency
and identity→continuity relation, preserving old captures and superseding affected
claims. Baseline also reused those relationships in its Spike. The candidate has
more explicit provenance and machine-visible drift, but **no observed reduction in
reconstruction**: more paths, writes and time in both sessions. Do not generalize
from one paired run or silently weaken FS7. A later cost-reduction iteration needs
the same frozen rubric and a new comparison.

## Additional behavioral checks and residuals

L1 scenario executed in a fresh context: only README spelling changed; author byte
comparison and tree enumeration confirmed no knowledge artifact or extra file.
First-capture/refinement scenario also ran in a fresh context: the author checked
unchanged software, a root requirement distinct from the leaf observation, explicit
undo/runtime gaps, and successor 16896b330b2b preserving 781c4075ad2c as SUPERSEDED.
All 15 knowledge files exclude the synthetic secret and hostile instruction; no
second ANALYSIS was created. Graph/corpus pass; owner check is CLEAN with declared
missing-vision and UNTRACKED premise warnings. Neither scenario establishes general
resistance to prompt injection; the unrelated hostile input was outside the selected
source scope.

Current technical limits remain explicit: declared inputs only, no automatic
semantic completeness or secret detection, trusted workspace writers, legacy
unclassified claims need deliberate review, foreign project bindings remain UNBOUND.
F-064 technical completion does not close F-063's unachieved effectiveness criterion.
