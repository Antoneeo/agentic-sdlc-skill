<!-- SHADOW generated from devPNT (e_tdd_review_input_hardening v1.0) - do not edit by hand -->
# E-TDD: Review-Input Hardening (M2.A7) — per-file design

**Derives from:** E-ISP `e_isp_review_input_hardening` v2.0 (ACCEPTED). M-VISION `milestone_vision_execution_disciplines` v1.2 (APPROVED). D-UC `UC4`.
**Node:** M2.A7. **Change type:** doc-only refinement of the code-review discipline. No code. **State model: N/A** — no lifecycle/status/mode field touched.

## Conformance statement (dogfood the E-ISP v2.0 output-evidence rule)
Input constraints for this E-TDD = Vision (M-VISION) + UC (D-UC UC4) + parent E-ISP v2.0. Each mapped to where this design satisfies it:

| Constraint | Satisfied by (evidence) |
|---|---|
| E-ISP Impact Map = 3 MODIFY files (review.md, SKILL.md, templates.md) | Module Change Plan §1–§3 cover all 3, 1:1; nothing else touched (REVIEW_LOG / dispatch.md / elicitation.md / SKILL.md §5 are E-ISP *no-edit consumers* → correctly absent here). |
| E-ISP §Requesting requirement (hand Vision+UC+TM) | §1 review.md §Requesting insertion. |
| E-ISP §Reviewing requirement (conformance statement, PASS-invalid-on-"found-nothing", scoped) | §1 review.md §Reviewing insertion, with the scope guard (analysis/design reviews only). |
| E-ISP author-trace leg (SKILL.md §3) | §2 SKILL.md insertion. |
| E-ISP Standalone use-cases home (templates.md cue) | §3 templates.md ANALYSIS insertion. |
| M-VISION signal #4 (review discipline defined once, reused) | all review-discipline text lives in review.md (single def); SKILL.md/templates.md point/support, no second definition. |
| M-VISION Non-Goal (no enforcement theater / no new validator check) | conformance requirement scoped + conditional (not blanket); zero validator entries; templates.md cue inert (ANALYSIS_SECTIONS allowlist permits extras). |
| UC4 (request + receive) | §Requesting = request side; §Reviewing = reviewer-output side. |
| P-TM T2 (bloat) / T4 (DRY) | line deltas below within ~90-line/pointer budgets; single home review.md. |

## Integration & data flow (the loop — single-homed in review.md)
```
elicitation.md (user-needs) ─┐
project_vision / M-VISION ────┼─▶ SKILL.md §3 authoring rule: build + trace Impact ON {Vision, UC, TM}
templates.md "## Use Cases" ──┘                    │
                                                   ▼
              review.md §Requesting: hand reviewer {Vision, UC/D-UC, TM} + artifact
                                                   ▼
              review.md §Reviewing: emit conformance statement (each constraint → evidence | finding);
                                    PASS invalid on "found nothing"   [analysis/design reviews only]
                                                   ▼
              REVIEW_LOG.md ## Notes  (audit home, free-text — no schema change)
```

## Module Change Plan

### 1. `skills/agentic-sdlc-skill/review.md` — MODIFY (§Requesting + §Reviewing)
**§Requesting** — after the existing `- **The actual diff**: …` bullet, ADD:
```
- **For an impact/solution-analysis review, the constraints it derives from**:
  the **Vision** (Hybrid: the `M-VISION`; Standalone: `project_vision.md`/`roadmap.md`
  + the ANALYSIS Vision-Alignment), the **use-cases / user-needs** (Hybrid: `D-UC`;
  Standalone: the ANALYSIS `## Use Cases / User Needs`), and the **threat model**
  (Hybrid: `P-TM`; Standalone: the ANALYSIS `## Security and Threat Model`). Hand these
  *in addition to* the design artifact — the reviewer checks the artifact **against**
  them, not only for internal consistency.
```
**§Reviewing** — after the `- No praise padding.` bullet, ADD:
```
- **Conformance statement (impact/solution-analysis & design reviews only — not a
  plain code-diff review).** When the artifact under review carries Vision / use-case
  / threat-model constraints, your output MUST map each constraint to its evidence: for
  every use-case/user-need, every threat, and every applicable Vision benefit/Non-Goal,
  state WHERE the artifact satisfies it (section or `file:line`) or raise it as a
  finding. A PASS/approve is **not valid on "found nothing"** — the conformance
  statement is the proof the check ran; an unfalsifiable "I checked" is the review
  theater this discipline exists to prevent (the reviewer-side twin of §Receiving's
  silent-drop rule). Plain code reviews stay findings-only.
```
Rationale: closes the input (§Requesting) + output-evidence (§Reviewing) halves of E-ISP v2.0 in the single home (DRY/T4). Line budget: **+~16-18 lines** (7-line §Requesting bullet + 9-line §Reviewing bullet + blank-line spacing → review.md 58→~74-76, still under the ~90 ceiling, T2). NB: the E-ISP v2.0's "+~6-8 lines" estimate was an under-count; this corrected figure is what implementation follows.

### 2. `skills/agentic-sdlc-skill/SKILL.md` — MODIFY (§3 Request Analysis)
After the `- Minimum sections: …` line (~L185), ADD a bullet:
```
- Build the Impact/solution **on** the Vision, the use-cases/user-needs and the
  Security & Threat Model — read and trace to them first, and state the trace
  (which use-case / threat / benefit each part serves) so the closure review
  (`review.md`) can verify conformance. Do not draft the Impact in isolation.
```
Rationale: the author-trace leg (E-ISP loop step b); a pointer to review.md, no restatement (DRY / progressive disclosure, T2).

### 3. `skills/agentic-sdlc-skill/templates.md` — MODIFY (ANALYSIS template)
Between `## Feature Vision` (comment ends ~L155) and `## Impact` (L157), INSERT:
```
## Use Cases / User Needs
<!-- who needs this and why: the concrete use-cases / user-needs the change serves
     (the Standalone home for what Hybrid keeps in D-UC). Derived from the elicitation
     round; the Impact below must cover each, and the closure review checks coverage. -->
```
Rationale: the Standalone use-cases home (E-ISP BLOCK fix). Inert to the validator — `sdlc_check.py` ANALYSIS_SECTIONS allowlists required sections and permits extras → no validator change. +1 section cue (T2).

## Developer testing strategy
Doc-only change; no unit tests. Verification = closure gate `python skills/agentic-sdlc-skill/scripts/sdlc_check.py check --hybrid` CLEAN (review.md/SKILL.md/templates.md are not canonical-manifest docs; the templates.md ANALYSIS extra section is inert) + the skill eval battery `python -m unittest discover -s skills/agentic-sdlc-skill/scripts -p "test_*.py"` green (skill invariants unaffected). **TDD exemption:** pure-doc change (recorded, per `tdd.md`).

## Packaging
`review.md`, `SKILL.md`, `templates.md` are ALL already in `package.json` `files` (shipped) — no allowlist change. No version bump here (the release unit owns the triple-bump, `GUIDE_release`).
