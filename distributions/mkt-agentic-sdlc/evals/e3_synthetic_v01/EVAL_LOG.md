# EVAL LOG — e3_synthetic_v01 (Caffè Brancaleone)

Run date: 2026-07-09. Executor: Claude (Fable 5) following skill files only.
Client: subagent playing Marco Brancaleone (CLIENT_PERSONA.md + CLIENT_DOSSIER.md).
Success signals under test: M-VISION `milestone_vision_skill_v1_validation` v1.0.

## Findings

| ID | Phase | What happened | Class | Fix applied |
|---|---|---|---|---|

Classes: SKILL-GAP (doctrine unclear/wrong), TEMPLATE-GAP, VALIDATOR-GAP,
ELICITATION-VIOLATION (skill broke its own rules), CLIENT-FRICTION (persona
trigger fired), RESIDUAL (accepted, not fixed).

## Phase journal

### Phase 1 — Intake & Triage

- Level declared: E3 (no prior strategy exists; full plan requested). Correct
  per Rule Zero (an E2 without strategy context escalates anyway).
- Fixture init via `mkt-sdlc-init` worked; seeds + INDEX generated clean.

### Phase 2 — Discovery

- Wave 1 executed in 3 rounds, 3-4 questions each. Zero persona triggers
  fired: no jargon complaints, no overload complaints. Vagueness-first was
  neutralized by pre-authorizing "non lo so" and asking precision inline —
  note: this pattern ("se non l'avete mai misurato, va bene non lo so") is
  NOT in elicitation.md; candidate calibration addition.
- 21 FACT rows captured to ledger. All Wave-1 items covered; deliverable
  language inferred (Italian) without asking — dossier unambiguous.
- MKT_VISION drafted and gate-passed in one round. Client attached 2 riders
  (capacity-bounded objectives; competitor set = specialty online only) —
  folded into the APPROVED vision as a rider block. Note: skill has no
  explicit rule on recording gate riders inside the vision doc; candidate
  calibration addition (small).
- Client demand "numeri, non slide" logged for packaging tone (phase 9).

### Phase 3 — Research

- 4 parallel sweeps (sizing, competitors, VoC, channel benchmarks) via
  general-purpose subagents with ledger-shaped output contracts. ~190 real
  web fetches total. deep-research skill NOT used (manual playbook path) —
  residual stands.
- Ledger grew EV-22..EV-52 (31 rows): BENCHMARKs with URL+date+second
  source, reasoned estimates correctly classed ASSUMPTION with ranges.
- Sweep quality high: staleness flags, geography flags, methodology
  conflicts surfaced (Renub), one competitor verified CLOSED, two sites
  down on observation day (used Wayback + third-party cross-check).
- Finding: researcher output contract ("every number needs URL+date, two
  sources for budget-driving numbers, mark ESTIMATE") worked as specified in
  research.md — no invented numbers detected on spot-check.
- Finding (TEMPLATE-GAP candidate): no template/home for pre-assembly SWOT
  or situation synthesis; created ad-hoc `strategy/SITUATION_SWOT.md`.
  Candidate: add SITUATION_SWOT template to templates.md.

### Phase 4 — Situation Analysis

- ICP_PERSONAS (3 personas, every trait EV-traced or labeled indirect),
  THREAT_MAP (4 competitive + 6 plan risks with mitigations), SITUATION_SWOT
  (PESTEL/5F declared-skipped per frameworks.md rule).
- Research surfaced a question Wave 1 could not have anticipated: does
  Brancaleone print roast dates? (category trigger #1 [EV-43]). Queued for
  Wave 2 — legitimate second-round trigger per elicitation.md ("real fork").

### Phase 5 — Objectives

- Wave 2 (4 domande) incl. la domanda-fork emersa dalla ricerca (data di
  tostatura sul sito) → legittima seconda ondata, non formalità.
- 4 obiettivi SMART (O1 raddoppio, O2 misurabilità-precondizione, O3 email,
  O4 Q4), ognuno con target+data+owner+why EV-tracciato. Gate PASS in un
  round; cliente ha aggiunto rider (O1 clausola onestà; O4 confezioni da
  progettare) + nuovo FACT EV-57. Nessun trigger persona.

### Phase 6 — Strategy

- STRATEGY draftata, poi **CMO review adversariale** (subagent fresco,
  read-only, batteria R1-R14 + conformance).
- Round 1: **FAIL, 5 BLOCK + 6 WARN** — TUTTI reali. Difetti veri catturati:
  O2 non servito da alcun pilastro (R14); EV-32 citato AL CONTRARIO
  (settembre "costa metà" — falso); 3 numeri non tracciati laundered sotto
  citazioni reali ("dal 2018", "20-30 euro", "tre generazioni"); roast-to-
  order asserito ma mai stabilito e in conflitto con EV-51. → **success
  signal 2+4 dimostrati: il gate becca il plausibile-ma-vuoto.**
- Fix: 2 nuovi FACT (EV-58/59 per fatti realmente detti da Marco), 1 BENCHMARK
  (EV-60), riscrittura pilastri/positioning; roast-to-order rimosso (non
  inventato). Re-review round 2: **PASS**, 5 BLOCK verificati curati, 3 WARN
  residui (conteggio swap-test + LPDC droppato, tagline "mostra online" =
  capacità non consegnata, 2 citazioni imprecise) → fixati. REVIEW_LOG tenuto.
- **Gate cliente:** approvato TUTTO tranne un rework acuto — il positioning
  "prezzo onesto/12-22 euro" lo faceva suonare LOW-COST; cliente ha imposto
  freschezza+qualità davanti, prezzo come conseguenza. La CMO review NON
  aveva colto la low-cost-trap (R11 non copre "positioning price-led").
  → CANDIDATE CALIBRATION: aggiungere red-flag "posizionamento guidato dal
  prezzo / trappola low-cost" a review.md.

### Phase 7 — Tactics

### Phase 8 — Action

### Phase 9 — Control & Packaging

### Phase 7 — Tactics

- Wave 3 (capacità esecutiva) SKIPPED-with-reason: già coperta da Wave 1/2
  (4h Marco + 8h Giulia, no paid, Shopify, Klaviyo target, budget). Testa la
  skip-path di elicitation.md — corretto non re-interrogare.
- TACTICAL_PLAN: budget 1.400/mese, funnel 3 canali acquisizione. budget +
  funnel PULITI al primo colpo. Riconciliazione build-up vs O1 esplicita.
- trace WARN: O2 (obiettivo-precondizione) senza canale di spesa → riga
  enabler budget 0. CALIBRATION: convenzione "enabler row" da documentare.
- ledger check: 6 ERROR — BENCHMARK qualitativi con source=path invece di URL.
  Il guard è GIUSTO (research.md esige URL); esecutore ha tagliato l'angolo →
  fix URL reali. CALIBRATION: rafforzare "URL, non rimando a doc" in research.md.

### Phase 8 — Action

- ACTION_90D day-level (sett 1-2) + week-level (3-12), vincoli calendario
  (Ferragosto, Marco assente ott-nov) rispettati.

### Phase 9 — Control & Packaging

- MEASUREMENT_PLAN (KPI tree tutti O#, kill/scale pre-fissati), MARKETING_PLAN
  assemblato (SOSTAC, exec summary, assumptions in pagina 1, appendice ledger),
  ONE_PAGER.
- **Review CMO finale**: PASS, 0 BLOCK, 3 WARN onesti (prezzo Bugan non
  tracciato; uplift CVR "basso rischio" ottimista sopra benchmark; floor O1
  senza cuscino) → tutti fixati. check finale CLEAN.
- **Gate finale cliente: FIRMATO.** "uno che ti scrive anche il caso in cui
  va male è uno di cui mi fido" — success signal 4 (credibilità professionale).

## Seeded-defect verification (A8)

Metodo: copia fixture pulita, iniezione, guard, verifica ERROR/BLOCK, revert.
Baseline copia = CLEAN prima dell'iniezione.

| Defect | Guard | Result |
|---|---|---|
| D1 budget sum rotto (450→400) | mkt_check budget | ERROR ✓ (somma 1350 vs 1400) |
| D2 funnel rotto (Meta cust 4→9) | mkt_check funnel | ERROR ✓ (9 vs 4,14 + CAC mismatch) |
| D3 orphan tactic (O1→O9) | mkt_check trace | ERROR ✓ (O9 non definito) |
| D4 ghost ref [EV-99] | mkt_check ledger | ERROR ✓ (non trovato) |
| D5 benchmark senza URL (EV-26) | mkt_check ledger | ERROR ✓ |
| D6 KPI row rimossa (O3) | mkt_check trace | ERROR ✓ (O3 senza KPI) |
| D7 positioning generico | CMO review R1/R11 | BLOCK ✓ (swap fallisce su TUTTI e 6; reviewer ha pure colto lo strawman-PASS) |
| D8 assunzione lavata ("con certezza 60M") | CMO review R2/R3 | BLOCK ✓ (untraced + certezza su ASSUMPTION) |

**Risultato A8: 8/8 difetti catturati. Nessun falso CLEAN. Success signal 2 dimostrato.**

## Calibration backlog (A9) — findings ripiegati nella skill

1. review.md: aggiungere red-flag "posizionamento price-led / trappola low-cost"
   (il cliente l'ha colto, non la CMO review R11) + nota R1 "lo swap test deve
   testare la FRASE PUBBLICATA, non una formulazione diversa" (strawman colto in A8).
2. elicitation.md: pattern "pre-autorizza il non-lo-so" sulle domande numeriche
   (ha evitato friction, non era codificato).
3. templates.md: template SITUATION_SWOT (mancava un home per la sintesi
   Situation) + convenzione "enabler row budget 0" per obiettivi-precondizione
   + nota "registrare i rider del gate cliente nell'header del doc approvato".
4. research.md: rafforzare "BENCHMARK richiede l'URL vero, non un rimando a un
   doc di ricerca che lo aggrega".

## A9 — calibration applied (skill files, not fixture)

1. review.md: R1 rewritten (test the PUBLISHED statement); +R11b (low-cost
   trap / price-led positioning); +R15 (strawman swap-test). [from D7 + client gate]
2. elicitation.md: "pre-authorize I-don't-know on numeric asks". [from Wave 1]
3. research.md: BENCHMARK Source must be the real URL, not a research-doc pointer. [from ledger ERRORs]
4. templates.md: SITUATION_SWOT template; enabler-row (budget 0) convention;
   gate-rider recording in the approved doc header. [from phases 4/6/7]

Post-calibration: mkt_check self-tests 15/15 green; init.js template extraction
OK; npm pack dry-run clean (16 files, 31.4 kB).

## Verdict vs M-VISION success signals

1. **E3 9 phases, skill-only, real research** — MET. All phases ran; ~190 web
   fetches across 4 sweeps; driven by the skill files.
2. **Validator catches seeded defects, no false CLEAN** — MET. 8/8 caught
   (6 mechanical + 2 review). A8 table above.
3. **Elicitation stays within its rules** — MET. 3 waves, ≤4 q/round, zero
   jargon, zero analysis outsourced; no persona trigger fired.
4. **Deliverable passes CMO battery + client judges it credible** — MET. Final
   review PASS; client signed ("uno che ti scrive anche il caso in cui va male
   è uno di cui mi fido").
5. **Findings folded back, tests green** — MET. 4 calibrations applied; suite green.

**Overall: PASS.** The skill produced a professional, ledger-grounded,
mechanically-consistent, adversarially-reviewed marketing plan for a realistic
SMB, and its own guards + review gates caught every seeded defect.

## Residuals / not tested

- deep-research skill path (research.md "preferred engine") — eval used the
  manual fallback playbook (parallel general-purpose subagents). The engine
  substitution point works; the named skill itself unexercised.
- E2 campaign path — out of scope this milestone (v2).
- PDF/deck/xlsx export offer (phase 9) — described, not exercised.
- 3 residual ledger warns (EV-07/09/41: B2B price/margin, directional online
  size) — genuine background context, left un-pruned by choice.
