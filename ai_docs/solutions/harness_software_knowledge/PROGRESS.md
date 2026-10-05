# Implementation ledger — F-064 then F-063

Authority: ANALYSIS_kb_evidence.md, ANALYSIS_software_knowledge.md and
DESIGN_software_knowledge_files.md; owner instruction 2026-10-04: apply now and show diff.
This instruction approves implementation and its declared adoption cost.

Branch: codex/software-knowledge. The managed worktree was unwritable in the sandbox
and archived unused. Work in the original checkout, preserving unrelated course work.
Baseline planned files: implementation/before.zip; final task-only diff generated from it.

Preflight: F-064 supplies typed ledger, evidence engine and common methods to F-063.
Its standalone intermediate state must pass before SDLC triggers are added.
The accepted design is the plan; no separate superseding plan or commit is required.

1. Typed ledger: implemented; legacy IDs/schema preserved, cross-kind links refused.
2. Capture/binding and evidence/portability: implemented; 35 tests, one Windows
   symlink privilege skip, explicit junction coverage. RED/GREEN logs preserved.
3. Common methods/distribution: implemented and intermediate batteries verified
   before software triggers. Initial KB command-name omission fixed; runtime/pack
   seams exercised in all four distributions. No package version/publish change.
4. SDLC integration: implemented. Frozen behavioral comparison complete; two fresh
   contexts per variant, four cases bundled. Candidate correct but more costly,
   including session two; FS7 unachieved, F-063 remains IN_PROGRESS. Extra L1 and
   analysis-only capture/refinement cases verified in separate fresh contexts.
5. Full suites: software263/KB449/marketing286/course280, all PASS with platform/domain
   skips. Node and four package contents verified. Independent code review R1 FAIL
   (two BLOCK, one WARN) -> R2 PASS after regression fixes. F-064 COMPLETED.
   Final documentation freshness and scoped diff generated at delivery.

Automatic approval review initially rejected the F063 script over possible guides.md
overwrite. A no-write execution and equality assertion proved every existing guide
line retained with a five-line insertion; corrected phase anchor and re-reviewed
execution was approved. No blocked permission remains.

The initial test file existed just before before.zip; diff generation treats every
ADD path in the approved file map as empty-before, so its complete addition is shown.
