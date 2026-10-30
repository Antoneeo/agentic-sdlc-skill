---
feature: F-087
analysis: ANALYSIS_owner_design_approval.md
base: main
---
# Merge review: il proprietario approva il design L3 prima del lavoro

## Purpose
Dopo il PASS finale della review del design, un'unità L3 si ferma e il proprietario approva il design prima che il lavoro cominci. Serve l'obiettivo della Vision di rendere visibile una divergenza prima dell'implementazione: il revisore giudica se il design regge, solo il proprietario sa se è quello che voleva (REQUEST_owner_design_approval.md#R1). Costo accettato in #R3.

## What to review
Tabella stampata da `sdlc_check.py review-map --base origin/main` il 2026-10-30, dopo la review di chiusura e prima di questo brief. Le copie in `distributions/*` di `review.md`, `sdlc_core.py`, `shared_files.py`, `test_design_approval.py` e dei manifest sono identiche all'originale in `skills/agentic-sdlc-skill/` (`test_drift` in tutte e quattro): basta leggerne una.

| Path | Status | +/- | Class | What to do |
|---|---|---|---|---|
| `CHANGELOG.md` | M | +2/-0 | REVIEW | review |
| `README.md` | M | +1/-1 | REVIEW | review |
| `distributions/course-creator/CHANGELOG.md` | M | +6/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/SKILL.md` | M | +2/-2 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/review.md` | M | +28/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/sdlc_core.py` | M | +54/-14 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/shared_manifest.json` | M | +4/-3 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/scripts/test_design_approval.py` | A | +219/-0 | REVIEW | review |
| `distributions/course-creator/skills/course-creator/templates.md` | M | +3/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/CHANGELOG.md` | M | +2/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/README.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/review.md` | M | +28/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_core.py` | M | +54/-14 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/shared_manifest.json` | M | +4/-3 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/test_design_approval.py` | A | +219/-0 | REVIEW | review |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md` | M | +3/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/CHANGELOG.md` | M | +2/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/SKILL.md` | M | +1/-1 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/review.md` | M | +28/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/sdlc_core.py` | M | +54/-14 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/shared_manifest.json` | M | +4/-3 | REVIEW | review |
| `distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/test_design_approval.py` | A | +219/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/SKILL.md` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/elicitation.md` | M | +2/-2 | REVIEW | review |
| `skills/agentic-sdlc-skill/evals/scenarios/design_approved_before_code.md` | A | +18/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/review.md` | M | +28/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/sdlc_core.py` | M | +54/-14 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_files.py` | M | +1/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/shared_manifest.json` | M | +4/-3 | REVIEW | review |
| `skills/agentic-sdlc-skill/scripts/test_design_approval.py` | A | +219/-0 | REVIEW | review |
| `skills/agentic-sdlc-skill/templates.md` | M | +4/-1 | REVIEW | review |
| `ai_docs/audit/audit_plan.md` | M | +2/-2 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/ANALYSIS_owner_design_approval.md` | A | +189/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/solutions/E2E_TEST_owner_design_approval.md` | A | +50/-0 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/strategic/skill_family_agent_workflows.md` | M | +1/-1 | DESIGN | reference the code is checked against; read the changed parts (the brief states which review covered them) |
| `ai_docs/audit/requests/REQUEST_owner_design_approval.md` | A | +47/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/audit/reviews/REVIEW_LOG.md` | M | +2/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_owner_design_approval/probe.py` | A | +130/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_owner_design_approval/replay_baseline_2026-10-30.md` | A | +26/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/solutions/harness_owner_design_approval/replay_new_2026-10-30.md` | A | +20/-0 | EVIDENCE | spot-check that what the brief cites exists (verdicts, owner statements); do not re-review |
| `ai_docs/memory/INDEX.md` | M | +3/-1 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |
| `ai_docs/strategic/features_history.md` | M | +1/-0 | GENERATED | skip; rewritten by `index` (a CLEAN `check` proves it) or, for SHADOW_ mirrors, exported from devPNT |

Totals: REVIEW 35 files (+1274/-79); DESIGN 4 files (+242/-3); EVIDENCE 5 files (+225/-0); GENERATED 2 files (+4/-1)

## Already verified
- **Design.** REVIEW_LOG 2026-10-30, `ANALYSIS_owner_design_approval.md`, tier design: FAIL → PASS (provisional) → PASS, 3 round. Ha coperto l'ANALYSIS, il testo proposto per `review.md` e il probe.
- **Approvazione del proprietario** del design, con la regola stessa: REQUEST_owner_design_approval.md#R7.
- **Closure.** REVIEW_LOG 2026-10-30, F-087 closure, tier closure: PASS, poi una re-review mirata delle correzioni: PASS. Ha confrontato `review.md` con il testo approvato parola per parola, ricavato di nuovo i chiamanti per P1–P3, hashato le copie condivise, fatto girare il probe sulla baseline (5 RED, 7 guardie).
- **Test**, sull'albero non committato dopo l'ultima modifica al codice:

  | Comando | Risultato |
  |---|---|
  | `python -m unittest discover -s <scripts> -p "test_*.py"`, nelle quattro skill | code 573, kb 900, course 598, mkt 575: OK |
  | `python ai_docs/solutions/harness_owner_design_approval/probe.py` | 12 OK (baseline: 5 RED) |
  | `node scripts/test_*.js` | 3 OK |
  | `validate --root .` | 0 errori, nessun nuovo `[note]` |

- **Replica comportamentale** (`harness_owner_design_approval/`): baseline RED, l'agente scriveva codice dopo il PASS. Skill nuova: base GREEN sul criterio di accettazione, non presidiata GREEN, correzione PARZIALE. Nella correzione lo stop ha tenuto, ma il fixture non ha la lista dei report che il proprietario nomina, e l'agente ha chiesto prima di rivedere.

## Your judgement
- **Il testo della regola** in `review.md`: è quello che hai approvato (#R7).
- **Residui dichiarati** (ANALYSIS §Functional Spec, T1): l'advisory non verifica che la voce `design approved` venga dopo il PASS, né che approvi davvero il design presentato; le unità E3 di marketing non ricevono l'advisory, lì vale lo stato `APPROVED` della strategia.
- **Late upgrader**: un progetto utente con un L3 iniziato dal 2026-10-31 con una skill precedente riceve un `[note]` permanente finché il proprietario non registra una voce `design approved` (ANALYSIS §Popolazioni a riposo). Non cambia nessun esito.
- **Could not verify:** il gate con un hook reale (verificato con il test `Gate`); le trascrizioni delle repliche, di cui resta il resoconto dell'autore controllato sui file.
- **Decisioni ancora dovute:** il merge; il rilascio di tutte e quattro le skill, perché `review.md` e `sdlc_core.py` sono condivisi.

## Merge notes
- **File generati** (`handoff.md`, `memory/INDEX.md`): in caso di conflitto rigenerali con `sdlc_check.py index`, mai a mano.
- **Base:** il branch parte da 337943ab, cioè `origin/main` dopo il rilascio course 0.1.0-beta.15.
- **Merged** to `main` on 2026-10-30 by fast-forward (#R9).
