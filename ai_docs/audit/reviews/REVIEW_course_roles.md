# Course Creator: author, readers and independent reviewer

For the maintainer: assess the role wiring and its bounded verification. The user approved the role organization. The principal owns canonical content; each tested profile has a sequential reader and separate no-course control; the didactic reviewer judges the preserved evidence. Independent readers and reviewer reuse existing gates.

## Verification scope
Design and instruction diff reviewed independently. Distribution suite: 245 tests, 19 skipped, OK. The fresh session /root/course_roles_forward received the exercise below and revised skill, without this design, expected criteria or reviewer output. It prepared assignments and correction/fallback steps; it did not launch a set of agents or execute an entire course. Thus this verifies interpretation of the handoff, not end-to-end orchestration or learning. Earlier sequential reader tests remain separate evidence and are not repeated or re-scored here. The canonical course and PPTX are unchanged.

The generic quick_validate checker was not rerun: the same environment previously lacked PyYAML. No dependencies installed. The repository-wide freshness gate remains separate from the scoped suite.

## design-review.md
# Review indipendente del design dei ruoli

Per l'autore/coordinatore: decidere se implementare l'incremento descritto in `repo/ai_docs/solutions/ANALYSIS_course_slide_content.md` (A). Questa review verifica compatibilità dei ruoli e gap della baseline; esclude rigenerazione del corso/PPTX, audit globale e validazione dell'efficacia. Il lettore conosce già il design; il report conserva verdetto, evidenze e limiti. Reviewer: `/root/course_roles_review`, contesto indipendente, round 1, 2026-09-27.

**PASS — nessun finding bloccante nel design circoscritto.**

Il gap è verificato nel testo attuale: `simulation.md:15` assegna all'autore il confronto delle risposte con grafo e progressione; `:17` ammette la valutazione dell'autore; `:19` gli assegna lo scoring finale. `SKILL.md:71,81,83` prevede già review indipendente e simulazioni fresche. L'handoff esplicito al revisore risolve quindi un'ambiguità reale senza creare un ulteriore gate. `templates.md:190–204` registra le due prove, ma non attribuisce autore e reviewer: l'aggiornamento previsto completa la tracciabilità.

Conformità ai bisogni e ai vincoli approvati:

- UC1/autore: A §IC1 e Functional Spec 9,12 mantengono una sola responsabilità sul canonico; eventuali bozze parallele hanno confini dichiarati.
- UC2/corsista: A Functional Spec 5–8,10 conserva progressione e prefisso accessibile; dopo correzione serve un lettore fresco. Il controllo resta una sessione aggiuntiva separata.
- UC3/revisore: A Functional Spec 10–11 e §IC2 assegnano evidenze, valutazione e ricontrollo a chi non ha scritto il materiale. Il lettore non produce il verdetto.
- UC4/ambiente senza distill: A Functional Spec 4 e §IC3 preservano la continuità con limite dichiarato, coerentemente con `SKILL.md:77`.
- Beneficio e non-obiettivi dichiarati in A §Feature Vision: spiegazioni progressive e autonomia sono realizzati dai punti precedenti; §Impact esclude modifiche al corso, PPTX, parser e skill condivise.

I rischi di A §Security and Threat Model hanno risposte localizzate: contaminazione e falsa indipendenza in Spec 7,9–11; narrazione forzata in 5; aiuti durante la prova in `simulation.md:13`; doppia autorità e perdita di completezza in Spec 1–4,13; concorrenza in 9,12 e protezione della copia nel threat model. Le fonti restano dati secondo `SKILL.md` Rule Zero.

Il rinvio a `review.md` conserva disponibilità, autorizzazioni, capacità e limite dei round. `dispatch.md` §What may be delegated preserva l'autore degli artefatti governati; il PLAN opt-in riguarda produzione delegata.

Limiti: implementazione e prova di instradamento restano da eseguire. I risultati storici, la Vision completa e l'efficacia umana non sono verificati da questa review.

## closure-review.md
# Review indipendente del diff dei ruoli

Per l'autore/coordinatore: decidere se integrare i tre file staged contro il design approvato. **PASS — nessun finding bloccante nel diff esaminato.** Reviewer `/root/course_roles_review`, contesto indipendente, round 1, 2026-09-27.

Confronto eseguito con `git diff --no-index` fra `repo/distributions/course-creator/skills/course-creator/` nello stage e `D:/SoftwareDev/skill_sdlc/agentic-sdlc-skill/distributions/course-creator/skills/course-creator/`. Riferimento: `ai_docs/solutions/ANALYSIS_course_slide_content.md`, Functional Spec 9–12 e Impact. Non sono stati modificati file della skill durante questa review.

Il richiamo anticipato in `SKILL.md:75` è coerente con `simulation.md:3`: i ruoli si assegnano prima della produzione; il diagnostico richiede una bozza. La tabella descrive i materiali delle diverse fasi, non impone un corso completo prima della sua scrittura.

`simulation.md:11–13,31,33,35` separa responsabilità e giudizio: il principale integra e corregge; il lettore riferisce e tenta il compito; il reviewer valuta riscontri, scoring e accettazione. Le tre assegnazioni precedenti all'autore sono sostituite. Il principale può leggere le evidenze per correggere senza diventare il valutatore indipendente.

`simulation.md:15` richiede un lettore distinto e un controllo aggiuntivo per ciascun profilo testato, consentendo esecuzione in batch. `templates.md:206` impedisce di estendere il PASS a profili o unità non testati. Il numero dei ruoli non viene confuso con quello delle sessioni.

`simulation.md:17,19` conserva freschezza dopo correzione, versione dei materiali, precedenti finding, limite dei round e fallback tramite `review.md`. Il test non eseguito resta dichiarato; una self-review ammessa e dichiarata dal protocollo non viene presentata come indipendente. `templates.md:195–196,206` rende attribuibili autore, reviewer e retest.

`simulation.md:19` mantiene bozze parallele opzionali e delimitate, integrazione unica e confine sugli artefatti governati di `dispatch.md`. `simulation.md:7,13` riusa il reviewer e i gate esistenti, preservando la proporzionalità L1/L2. Nessun nuovo PLAN è richiesto per semplici lettori/reviewer.

SHA-256 dei byte staged esaminati:

| File | SHA-256 |
|---|---|
| SKILL.md | `60F19FF1B5F4A30D25DC7A362BFB6EBC1C1A781C665A7CF9A71CD6D8F759EB5B` |
| simulation.md | `03EABDA629846D6B1C9806BE55841E7A6380B168BEBDDE4A0A20F2ACA83C1D99` |
| templates.md | `945B1DE3B9342F7B31D8D75F4983778AB036618289D1792E0631A2613634DD57` |

Questo PASS riguarda compatibilità documentale e responsabilità operative nei byte indicati. Non attesta l'esito della prova di instradamento separata, della suite, dell'integrazione nel repository originale o della rigenerazione del corso/PPTX.

## verification-brief.md
# Verification handoff exercise

Apply the staged course-creator skill to organize the checks for a self-study course draft about investigating why an existing software setting was chosen. The approved course has two learner profiles: developers accustomed to coding agents and support specialists familiar with the product but unfamiliar with software-development terminology. A graph, plan, sources and complete source draft exist. You are the principal responsible for that draft.

Prepare the actual short assignment prompts you would send and explain how you would deliver material, collect results and handle corrections. Treat this as a routing rehearsal: do not launch agents or modify the course. You may use named placeholders for artifact paths and session IDs because no full course is supplied in this exercise. The client supports independent sessions but allows only two children to run concurrently.

Then handle two developments:
1. A participant says the second slide relies on an unexplained object. You amend that slide and its transition. Describe the affected assignments and evidence to keep.
2. On another client no independent session or one-shot execution is available. State what can still be delivered and how the missing checks are represented.

Write only work/course-roles/forward-handoff.md. Do not inspect design/review notes, expected criteria or earlier task outputs.

## criteria.md
# Frozen criteria

This is an instruction-application probe, not executed multi-agent course validation or evidence of learning. Score the handoff on actual content, not the count of role names.

1. Principal owns graph, plan, scope and canonical writes; no default author per slide.
2. Two independent readers receive profile-specific prior knowledge and only released learner-visible units, without graph, solutions, author discussion or each other's responses. The one-shot client/concurrency limit does not cause full-packet leakage.
3. An independent didactic reviewer receives graph, sources, complete material, criteria/key and preserved reader evidence. Reviewer judges; author implements. Existing review gate is reused.
4. A separate no-course control per tested profile is preserved for final transfer comparison; it is not the reviewer or a former reader. Three core roles do not imply exactly three total sessions.
5. After correction, material is versioned, findings preserved and a fresh reader receives the affected prefix; same independent reviewer may assess the correction without becoming the reader. Round limits remain those of review.md.
6. No independent facility: honest not-run reader test, review fallback truthfully labelled under review.md, no fake independent PASS. No autonomous installation or services.

Residual ambiguities are findings. A pass establishes only that this handoff exercise applies the role contract; prior course defects remain outside its scope.

## forward-handoff.md
# Verification routing handoff

For the principal coordinating checks of the approved self-study draft about investigating why a software setting was chosen. Use this handoff to assign separate contexts, preserve their evidence and route corrections. It covers production verification within the existing L3 course workflow; it does not redesign the approved course or execute a test. Paths and session IDs in angle brackets are placeholders to resolve before dispatch. No course project or guide router was supplied, so no project-router verdict or completed gate is claimed.

## Packets and session order

The principal remains the sole integrator of the complete source, learning path, graph and plan. Readers diagnose their experience; they neither write slides nor decide readiness. A separate didactic reviewer judges the evidence against the approved design and frozen criteria.

Before dispatch, freeze `<v1/hash>`, both approved profiles, objectives, a new-case transfer task for each profile, private criteria/key, tools and permitted external sources. Criteria must identify observable comprehension, a plausible insufficient answer and the explanation expected to enable the objective. Use the same task and access conditions for each profile's reader/control pair. Keep criteria, keys and anticipated answers outside their packets.

Create separate delivery areas: `<reader-dev>`, `<reader-support>`, `<control-dev>` and `<control-support>`. Each reader area starts with only its profile's established prerequisites and the first learner-visible unit. Extract exact copy, captions, explanations and transitions from `<slide_content-v1>`; essential self-study reasoning must be visible. Do not expose complete source, future units, graph, author notes or solutions to unanswered checks. Both controls receive only their profile, task and allowed external evidence. Restrict file/tool access where possible; document instruction-only withholding if technical isolation is unavailable. Exposed future material or answers contaminates the run and requires a fresh session.

| Batch | Session 1 | Session 2 |
|---|---|---|
| 1 | `<R-dev-v1>`: developer reader | `<R-support-v1>`: support reader |
| 2 | `<C-dev-v1>`: developer control | `<C-support-v1>`: support control |
| 3 | `<D-v1>`: independent didactic reviewer | Available for later correction work |

Finish or suspend a batch before starting another; never exceed two running children. Preserve separate histories. Readers never receive one another's responses; no reader or control becomes the reviewer. Choose an independent reviewer at the client's deep capability tier, preferably a different model where available. Record any constrained tier choice under `review.md`.

## Assignment prompts

**Developer reader — `<R-dev-v1>`**

> You are an independent reader of a self-study course about investigating why an existing software setting was chosen. Your approved profile is `<developer-profile>`: developers accustomed to coding agents. Use only the established prerequisites in that profile and material explicitly delivered to this session. Start with `<reader-dev/unit-01-v1>`. After each unit, briefly state what you think the course or current issue concerns, what this unit adds, and any reference or inference you cannot follow from the prefix you have seen. On the opening, report whether the situation and promised usefulness are intelligible; mastery is not expected. Stop after your response and wait for the next unit. Do not seek future units, design files or answers. Do not rewrite the course or grade its readiness. After the last unit I will supply the final task; attempt it using the allowed tools/sources `<dev-access>` and cite course passages you used. Return your responses as session output.

**Support reader — `<R-support-v1>`**

> You are an independent reader of a self-study course about investigating why an existing software setting was chosen. Your approved profile is `<support-profile>`: support specialists familiar with the product but unfamiliar with software-development terminology. Use only the established prerequisites in that profile and material explicitly delivered to this session. Start with `<reader-support/unit-01-v1>`. After each unit, briefly state what you think the course or current issue concerns, what this unit adds, and any reference or inference you cannot follow from the prefix you have seen. On the opening, report whether the situation and promised usefulness are intelligible; mastery is not expected. Stop after your response and wait for the next unit. Do not seek future units, design files or answers. Do not rewrite the course or grade its readiness. After the last unit I will supply the final task; attempt it using the allowed tools/sources `<support-access>` and cite course passages you used. Return your responses as session output.

**Next reveal — send separately to each reader after preserving its response**

> Read `<next-unit-path/version>` together with your previously delivered prefix. Give the same short reading response, then wait.

Do not explain the material, supply corrective hints or adapt the authored teaching during a diagnostic run. A comprehensible question that the course will answer later is not automatically a defect.

**Final reader task — instantiate once per profile**

> Attempt `<frozen-profile-transfer-task>` using `<profile-access>`. Provide your answer and cite the course passages you used. Do not consult solutions or evaluate your own score.

**No-course control — send separately to `<C-dev-v1>` and `<C-support-v1>`**

> Use `<approved-profile>` and its established prerequisites. Attempt `<frozen-profile-transfer-task>` with `<profile-access>`. You receive no course or reading dialogue. Return your answer and evidence references without grading yourself. Do not access course, design, criteria, solutions or another participant's output.

Instantiate this control prompt with the exact profile, task and access used by its corresponding reader. The task tests investigation on a new setting case; it must not disclose the desired reasoning or merely ask for course terminology.

**Didactic reviewer — `<D-v1>`**

> Independently review `<v1/hash>` against `<approved-Vision/design>`, `<profiles/objectives>`, `<graph>`, `<COURSE_PLAN>`, `<complete-source>` and `<source-records/locators>`. Apply `learning_design.md`, `simulation.md` and `review.md` from `<course-creator-skill-dir>`; use `distill` review mode for the actual learner surface while retaining separate factual-fidelity checks. Evaluate `<verbatim-reader-and-control-evidence>` against `<frozen-criteria/key>` with `<version/access-manifest>`. Locate the first unsupported prerequisite, unclear referent or broken connection in each reader's prefix; later explanations cannot erase earlier defects. Check useful before/after capability, explanatory reasoning, aligned transfer evidence and rejection of the plausible insufficient answer. Compare each profile's two final attempts. Return actionable findings with passage and response locators, unmet criterion, severity, scope, limitations and a readiness verdict. Mark unverifiable claims `CANNOT VERIFY`. Remain read-only; return the verdict as your final output. This is the existing content/closure review, not an additional gate.

## Collection and correction

Archive exact prompts, each response before the next reveal, unit order, delivered bytes or immutable locators, material hashes, session roles/IDs, tools, permissions and access limits. Record both profile comparisons and limitations in `<SIMULATION_REPORT>`; record reviewer identity, tier, findings and verdict in `<REVIEW_LOG>`. Intermediate reflection prompts may help learning, so final performance does not establish unprompted learning or causal course benefit. Control success makes course-assisted success inconclusive. Keep `efficacy not verified` regardless of a simulated PASS.

For the slide-two report, preserve the participant's original wording, slide-two version and prefix available at that moment. The principal locates the first unexplained object and amends its explanation and transition in the canonical source, checks the surrounding entry/exit dependencies, and updates affected graph/plan/objective/source links. Save `<v2/hash>` and the actual diff; retain v1 evidence unchanged.

Assign fresh readers `<R-dev-v2>` and `<R-support-v2>` to the affected prefix, starting at the opening and continuing through the changed transition and its receiving unit. Both profiles share the changed slide and have different prerequisites, so test both. Use the same neutral reader prompts with v2 delivery paths; do not disclose the old complaint or correction. Old readers cannot establish a fresh first encounter. A prefix-only retest verifies only that prefix. To claim a new final reader/control comparison for v2, continue fresh readers through the full packet and task, then run fresh matched controls in the next batch. Preserve the old controls as historical evidence; do not present a v1 course attempt as v2 evidence.

Send the reviewer this scoped correction prompt:

> Recheck `<finding-ID>` against `<v1-to-v2-diff>`, changed source/graph/plan links and `<fresh-v2-prefix-evidence>`. Return `ADDRESSED`, `NOT ADDRESSED` or `CONTESTED` with evidence for each finding, and identify any new blocker caused by the correction. Scope your verdict to the material actually reread and tested. Do not infer readiness from a participant saying “understood.”

Keep this inside the existing review's three-round limit. Retain the initial and final verdicts and round evidence in its log record. If findings remain after round three, surface them with the artifact rather than claiming closure or opening an unlimited review loop.

## Client without independent execution

The principal can still deliver the complete source, graph/plan links, source checks, structural validation results, prepared packets and an explicitly adversarial self-review against the same rubric. Delivery remains possible with disclosed limitations and open findings.

Record `Status: not run — simulated test not run; client has neither independent sessions nor one-shot execution` for both profiles' reader/control tests. Do not invent session IDs, attempts, scores or independent verdicts. Log the review fallback as `self-pass (declared; absent — the client has no such facility)` with actual scope, findings and capability information. An author role-play does not replace the missing tests. Keep `efficacy not verified` and distinguish any mechanical check result from the unavailable independent learner and reviewer evidence.

## probe-verdict.md
# Handoff probe assessment

Parent assessment against criteria.md frozen before the forward session. This assesses the contents of proposed assignments, not executed learner tests. Result: the six routing criteria are satisfied in this exercise. Independent design and diff review are separate evidence.

1. Principal ownership: “Packets and session order” reserves the canonical source, path, graph and plan to the principal; reader prompts prohibit authoring and readiness judgement.
2. Per-profile isolation: separate developer/support prompts, distinct delivery areas, one unit then wait; no graph, future source, notes or answer key. Batch table uses two children without merging histories. Technical versus instruction-only isolation is stated.
3. Reviewer judgement: didactic-reviewer prompt receives approved design, graph, complete text, sources, criteria/key, manifests and reader/control evidence. It returns localised findings and verdict; correction remains with the principal and reuses the existing gate.
4. Controls: distinct C-dev and C-support sessions have the same profile/task/access as their respective readers, with no course or reading dialogue. Reviewer is a fifth child session, not a control or reader. Counts are explicit.
5. Revision: slide-two change produces v2/hash, preserved v1 evidence, fresh readers for both affected profiles and scoped reviewer recheck under the three-round limit. A prefix result is not presented as a full-course comparison.
6. Absence: both reader/control tests are not run; self-review is truthfully labelled absent-facility fallback, with no invented session IDs or independent PASS. Delivery of source remains possible.

The response was read in full, including the reviewer assignment. One fresh session is evidence that the revised instructions can be applied to these conditions, not proof of stable compliance across agents or clients. The exercise did not execute the assignments, edit a course, revise slides or verify human learning. The source course and PPTX remain pending.

## Instruction hashes
```json
{
  "SKILL.md": "60f19ff1b5f4a30d25dc7a362bfb6ebc1c1a781c665a7cf9a71cd6d8f759eb5b",
  "simulation.md": "03eabda629846d6b1c9806be55841e7a6380b168bebdde4a0a20f2aca83c1d99",
  "templates.md": "945b1de3b9342f7b31d8d75f4983778ab036618289d1792e0631a2613634dd57"
}
```
