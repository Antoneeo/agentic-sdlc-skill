# CMO Review Discipline

Applies at the Strategy gate (phase 6), the final packaging gate (phase 9),
and any independent review slot in a connected governance layer (devPNT
review gates). This is the single definition of how to request, receive, and
perform a marketing review; other places point here instead of restating it.

The reviewer is a skeptical CMO with a fresh context: different session or
subagent, read-only, given the artifacts — never "review my session".
Fallback when no independent context is available: run the battery yourself
as an explicit, separate adversarial pass, and say so (independence is
reduced).

## Requesting

Hand the reviewer:
- **Scope**: which artifact, which gate, in one or two lines.
- **The artifact itself** — full text, not a paraphrase.
- **The constraints it derives from**: the approved MKT-VISION, the
  OBJECTIVES (for strategy/tactics reviews), the ICP_PERSONAS and THREAT_MAP,
  and the **evidence ledger** — the reviewer checks the artifact **against**
  them, not only for internal consistency.
- Which finding classes to cover when the default is not obvious.

## Receiving

**Answer findings one by one — fix, or justify with evidence.** Silent drops
turn review into theater. Disagree explicitly with reasoning; never resolve a
disagreement by rewording the finding. Cap 3 rounds; then surface open
findings to the user rather than looping. If any edit is made after a PASS,
re-review: reviewed text must equal shipped text.

## Reviewing — the red-flag battery

Severity: `BLOCK` (artifact does not pass the gate) / `WARN` (ships only with
explicit user acknowledgment). Every finding cites its location.

| # | Check | Severity |
|---|---|---|
| R1 | **Swap test**: replace our name with the top competitor in the positioning STATEMENT ACTUALLY PUBLISHED (not a stronger paraphrase — test the exact sentence that ships); if it still holds for any competitor, positioning does not exclude | BLOCK |
| R2 | **Untraced number**: any figure without `[EV-nn]` | BLOCK |
| R3 | **Laundered assumption**: ASSUMPTION used as certainty in prose ("the market is worth X" vs "we assume X-Y") | BLOCK |
| R4 | **Orphan tactic**: tactic serving no objective; **orphan objective**: objective with no KPI or no serving tactic | BLOCK |
| R5 | **Broken funnel math**: chain does not recompute, or projected outcome does not meet the objective target and no gap is declared | BLOCK |
| R6 | **Missing kill/scale criteria** on any funded channel | BLOCK |
| R7 | **Stale benchmark**: >24 months old, not flagged | WARN |
| R8 | **Top-down-only TAM**: no bottom-up cross-check | WARN |
| R9 | **Invented persona**: persona trait with no VoC trace and no ASSUMPTION label | WARN |
| R10 | **Channel vs ICP mismatch**: channel scores poorly on the selection matrix with no written rationale | WARN |
| R11 | **Generic messaging**: pillar without proof points; value prop interchangeable with any competitor's | WARN |
| R11b | **Low-cost trap / price-led positioning**: the positioning leads with cheapness ("prezzo onesto", "senza pagarlo caro", price comparison as the hook) instead of leading with value and framing price as a consequence — invites the customer to leave for the next cheaper option | WARN (BLOCK if the whole prop reduces to price) |
| R12 | **Vision divergence**: artifact pursues a goal absent from the approved MKT-VISION, or violates a non-goal | BLOCK |
| R13 | **Capacity fiction**: plan requires execution capacity Wave 3 says does not exist | BLOCK |
| R14 | **SMART violation**: objective without number, date, or owner | WARN |
| R15 | **Strawman swap-test**: the swap-test verdict tests a differentiated formulation while a WEAKER, generic sentence is what actually ships as the positioning line | BLOCK |

## Conformance statement (strategy & final-plan reviews)

A PASS is **not valid on "found nothing"**. The verdict must map each
constraint to evidence: every approved objective → the strategy element
serving it → the tactics funding it → the KPI measuring it (cite sections);
every MKT-VISION benefit and non-goal → where the artifact honors it; every
material ledger ASSUMPTION → where the plan declares it. A gap in the chain
is a finding, not a footnote. Quick E1/E2 reviews stay findings-only.

## Anti-patterns

- **Praise padding** — a review reports problems and fixes.
- **Batch-dismissal** of a findings list with one blanket reply.
- **Severity inflation/deflation** — a style preference is not a BLOCK; a
  broken funnel is not a nit.
- **Scope-creep findings** — issues outside the artifact under review are
  filed separately, not mixed in.
