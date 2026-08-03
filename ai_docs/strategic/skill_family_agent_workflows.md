---
description: How the three skills differ in the way an AGENT actually works under each — from a full three-way doctrine inventory. For the owner; body in Italian.
status: CURRENT
---
# La famiglia di skill: come lavora un agente sotto ognuna

**Per chi**: il proprietario, e chiunque debba scegliere quale skill installare o
capire perché un agente si comporta diversamente in tre progetti.
**Risponde a**: "cosa fa *concretamente* di diverso un agente sotto ogni lente".
**Non risponde a**: come sono impacchettate (`architecture.md`) o perché la famiglia
esiste (`project_vision.md`).
**Fonte**: inventario sistematico di ogni file di dottrina delle tre distribuzioni
(2026-08-01), non memoria di sessione.
**Documento derivato**: le sue fonti sono `skills/` e `distributions/`. Cambia la
dottrina → questo documento e il `README.md` della distribuzione toccata sono
stale finché non li aggiorni; `stale` lo segnala sulle righe corrispondenti di
`audit/audit_plan.md`, e `mark` è l'ultimo passo della chiusura, mai il primo.

## L'idea in una riga

Le tre skill condividono **lo stesso processo** (la spina, byte-identica e vigilata
dal drift guard) e differiscono in **una sola cosa fondamentale**: *a che cosa le
affermazioni dell'agente devono essere fedeli*. Tutto il resto — i documenti, i
gate, il vocabolario, i controlli — discende da quella scelta.

| | agentic-sdlc | kb-agentic | mkt-agentic-sdlc |
|---|---|---|---|
| **Fedele a** | il codice di QUESTO repo | i documenti che TU fornisci | l'evidenza di mercato |
| **Unità di lavoro** | feature (`F-`) | topic (`K-`) | engagement (`E1/E2/E3`) |
| **Triage** | L1 / L2 / L3 / Spike (grana: **file** — ~10 righe, ≤3 file) | L1 / L2 / L3 / Spike (grana: **conoscenza**, mai file — una riga di claim → propagazione di un fatto già assestato → nuova unità di conoscenza) | E1 / E2 / E3 / Research Spike |
| **Fasi L3/E3** | 5 (audit → vision → analisi → sviluppo → chiusura) | 5 (+ dentro la 4: l'algoritmo di ingestione) | **9** (spina SOSTAC) |
| **La domanda dell'agente** | "cosa rompe questo cambiamento?" | "cosa sappiamo già, quanto è certo, da dove viene?" | "quale evidenza sostiene questa scelta?" |
| **Il peccato capitale** | modificare a istinto senza orientarsi | spacciare conoscenza del modello per fonte | inventare un numero |
| **Slot di rischio (obbligatorio, il validator lo esige)** | `## Security and Threat Model` | `## Sources and Verification` | `## Threat Map / Plan Risks` |
| **Albero documenti** | `ai_docs/` | `ai_docs/` + `corpus/` + `topics/` | `mkt_docs/` (vision/strategy/tactics/deliverables) — `ai_docs/` su albero migrato con `migrate` |
| **File di dottrina propri** | `architect.md`, `tdd.md`, `debugging.md` | `taxonomy.md`, `distillation.md`, `reconciliation.md` | `frameworks.md`, `research.md` |
| **Comandi validator propri** | (spina, entry sottile) | `graph`, `corpus`, `claim-id`, `anchor`, `export`, `import` | `ledger`, `budget`, `funnel`, `trace` |
| **Cosa valida in più** | struttura + Component Map anti-rot | **il grafo e i claim** (span, digest, id, simmetrie, cicli) | **l'aritmetica** (budget ±1%, funnel ±5%, catena obiettivo→tattica→KPI) |

## La spina comune (identica byte per byte, su tutte e tre)

Qualunque lente sia attiva, l'agente:

1. **Triaga e dichiara** (Rule Zero): livello + verdetto del guide router in una
   riga (`Level: L3 · router: no match`) — tre soli verdetti legali, così "non ho
   guardato" è indistinguibile da "ho guardato, niente" solo se menti per iscritto.
2. **Si orienta prima di creare**: registro dei workstream (`handoff.md`, una riga
   per lavoro aperto, ≤20 righe), indici generati (mai scritti a mano — il
   validator fallisce su uno editato), guide operative con fedeltà alla fonte
   (snapshot verbatim + hash, `stale` rileva il drift).
3. **Passa i gate**: Vision gate (DRAFT informa, APPROVED vincola — promozione solo
   tua, dopo il blind check); **design review indipendente prima di implementare**
   e closure review prima di dichiarare DONE — scala di indipendenza a 3 pioli
   (subagent fresco > run one-shot > self-pass dichiarato, illegittimo se esistono
   i primi due), cap a 3 round poi i findings aperti arrivano a te, una riga di log
   per ogni review, PASS invalido su "non ho trovato niente" (serve il conformance
   statement).
4. **Rispetta la question discipline**: ogni domanda a te è legale solo se (a) ha
   cercato prima e nomina la ricerca col risultato, e (b) nomina la decisione
   bloccata. Mai "procedo?", mai pesca di preferenze, mai ri-chiedere il registro.
   Default non-bloccante: assunzione dichiarata (da cosa è presa + l'alternativa
   esclusa), presentata in batch.
5. **Chiude meccanicamente**: `check` CLEAN, documenti nello stesso commit del
   lavoro, decisione esplicita di merge (mai branch orfani), riga del registro
   rimossa e HANDOFF volatile cancellato.
6. **Può delegare** (dispatch opt-in): piano validato o niente dispatch
   (`plan validate`, confinamento fail-closed), `verify` stampato mai eseguito,
   escalation di tier solo dopo 2 fail consecutivi.

## agentic-sdlc — la lente del codice

Ciò che solo qui l'agente fa:

- **Architect pass prima dell'Impact** (`architect.md`): la feature enunciata come
  *capability* (verbi su nomi di dominio, zero file), ogni capability giudicata
  EXISTS / INADEQUATE / MISSING contro la Component Map + una ricerca reale
  (testo prima, grafo dei simboli poi — cerchi un nome che non conosci ancora).
  Regola dura: **la mappa silenziosa su un'area non letta non giustifica mai un
  MISSING** — altrimenti costruisci due volte. Un MISSING scoperto durante un L2 è
  esso stesso un trigger di escalation.
- **Blast radius come dovere d'autore**: per ogni simbolo con firma cambiata o >1
  chiamante, l'elenco COMPLETO dei consumatori (call hierarchy, mai grep),
  ancorato all'identità del simbolo, scritto nell'Impact — così la review non
  scopre "manca un consumatore" un round alla volta.
- **TDD di default** (L2/L3): UN test che fallisce, visto fallire, prima del
  codice; l'esenzione va scritta nel Diary ("un'esenzione non registrata è
  indistinguibile dal dimenticarsene").
- **Debugging col circuit breaker** (`debugging.md`): riproduci → isola → causa
  radice via grafo dei simboli → fix alla causa → test di regressione *verificato
  fallire sul codice vecchio*. **3 run consecutivi senza progresso → STOP**, metodo
  sistematico, poi consegna (riproduzione minima, cosa escluso, ipotesi migliore).
  Componente che si rompe ripetutamente → mai una quarta patch: guida di
  comprensione + refactor proposto come L3 a sé.
- **Guide di comprensione DAL codice**, scritte autonomamente (unico silent-write
  permesso): snapshot = estratti verbatim etichettati `path:symbol`, ogni claim
  tracciabile, aggiornate nella stessa chiusura che cambia il codice descritto.
- **Component Map viva**: riga nuova anche per un componente semplicemente
  *scoperto* esplorando — e il validator la tiene anti-rot (ogni path/simbolo
  nella colonna Where deve risolversi).

## kb-agentic — la lente della conoscenza

Qui l'agente non scrive software: **costruisce un secondo cervello sui documenti
che gli dai**. Due assi tenuti separati: l'**astrazione** (argomento composto da
argomenti — negli archi del grafo) e la **certezza** (quanto il corpus sostiene
un'affermazione — nelle righe di claim). L'algoritmo di ingestione:

**1. Intake — la fonte diventa intoccabile.** Ogni documento entra verbatim in
`corpus/given/`, content-addressed con **hash raw dei byte** (non quello
LF-normalizzato delle guide: una coppia 0D0A/0A ostile collideerebbe); versione
nuova = append con `supersedes:` nel sidecar, mai sovrascrittura. I non-testuali
ricevono l'**estrazione canonica conservata** (`.txt`, pagine separate da
form-feed, estrattore registrato): è a QUEI byte che puntano gli offset. Parlato →
nota `origin: elicited`; sintesi → `derived_from:`; ruling → `basis:`. **Una nota
senza nessuno dei tre è "conoscenza del modello travestita da fonte" e il
validator la rifiuta.**
Su corpus binari grandi vale la variante **estrazione-come-artefatto** (F-029): in
`given/` entra solo l'estrazione, `sha256:` è il suo digest — l'immutabilità resta
imposta sui byte che i locator indirizzano — e l'originale resta dov'è, registrato
come `original_path:` + `original_sha256:`. Quei due campi sono **registrati e mai
verificati**, e il limite va scritto dove stanno: 233 MB di PDF non entrano nel
docs root per proteggere byte che nessun locator tocca.

**2. Estrazione — l'unità è il claim.** Righe
`id | claim | valid | qty | about | source | prov | state`. L'**id** =
hash(posizione+quantità), **mai del testo** — una riformulazione LLM non conia
identità nuove. Il **locator** (`p=17@412-509`) è verificato: il validator apre
l'estrazione e controlla che lo span esista; `anchor <path> <frase>` lo produce
(F-029), matchando gli spazi come `\s+` perché l'estrazione PDF spezza le frasi a
metà riga. **Copri i gate, non solo i poteri**: per ogni riga che dice cosa il
soggetto *può fare*, chiedi alla fonte cosa deve valere prima — default-off,
licenza, versione minima, dipendenza. La regola è *chiedi*, mai *produci*: fonte
che non enuncia un gate → nessuna riga, e un gate sospettato ma non trovato è un
`gaps:`. `valid` half-open ("fino al 1/3" e
"dal 1/3" NON confliggono); `qty` tipizzata (effort in giorni-persona, costo in
UNA valuta — misto **rifiuta di sommare**, niente cambi offline); `about` per le
relazioni. L'estrattore **non inventa nulla**: ciò che la fonte non asserisce
diventa `gaps:`, mai una riga.
**La fonte si esaurisce, non si campiona** (F-031). "Non inventa nulla" è un
pavimento, e un estrattore che si ferma quando niente di ciò che ha scritto è
falso si ferma a pagina venti di un manuale di duecento — con tutte le righe
corrette: è il difetto osservato sul campo. Quindi una fonte lunga si legge a
**finestre limitate** (30 pagine di default, un task di piano ciascuna: il ledger
del `PLAN_` è il registro che sopravvive alla sessione, e non se ne costruisce un
secondo), e ogni finestra si chiude avanzando `extracted_through:` sul sidecar
dell'artefatto. È quel campo a rendere falsificabile "ho finito": claim senza
copertura registrata → errore; una claim che indirizza oltre la copertura
dichiarata → contraddizione; copertura corta rispetto alla fine → warning finché
non ci arriva. Il limite sta scritto dove sta il campo: **niente dimostra che una
pagina sia stata letta**; cambia che la scorciatoia ora va scritta per passare. E
esaustivo vuol dire *letto*, mai *una riga per pagina*: una pagina che non
asserisce nulla non produce nulla.

**3. Collocazione — cinque verdetti** (`taxonomy.md`): discesa sull'indice
generato seguendo OGNI parent (poligerarchia), sinonimi nell'indice ("listino"
trova `pricing`). EXISTS → riconcilia; INADEQUATE → figlio; **MISSING solo dopo
aver interrogato il grafo**; GENERALIZES → escalation (riparentare è un'unità di
lavoro; una radice nuova si ferma da te); UNPLACED → quarantena non ordinata.
Simile-ma-forse-diverso → **fratello con la riga di distinzione scritta**; se non
riesci a scriverla, è lo stesso concetto. Cicli **rifiutati alla scrittura**
(risalita antenati); nodi fusi → tombstone con `redirect_to:`, mai cancellati.

**4. Riconciliazione — la macchina rileva e trattiene, MAI decide.** Cinque esiti:
nuovo / **conferma** (fonte appesa alla riga, mai una seconda riga — la base si
rafforza, non si allunga) / raffinamento (vecchia riga `SUPERSEDED`, testo
intatto) / coesistenza (scope disgiunti) / **conflitto** → tutto il set
`CONTESTED`, **simmetrico** (girare una cella a mano fa fallire il check — il
laundering più economico). Risolve solo **informazione nuova**: una fonte più
recente, o un tuo **ruling con `basis:`** — il fatto che conosci e il corpus no.
Senza basis niente ruling (una preferenza non è un fatto). Il ruling supera
l'intero set, ed è **sfidabile**: un documento successivo riapre il caso col tuo
basis accanto.

**5. Escalation — in blocco a fine giro**, mai a raffica, ognuna in forma legale
(claim del set, fonti riapribili, date, provenienze, perché la macchina non può
decidere). L'ingestione non si ferma mai a farti domande.

Deliberatamente **assente**: qualsiasi stato di copertura per nodo — `gaps:` dice
cosa manca a QUEL nodo, e niente lo colleziona (il Non-Goal work-management). I
check emettono findings, mai righe di stato. Una **fonte** invece registra fin
dove è stata letta, ma sul proprio sidecar e da nessun'altra parte: l'indice del
corpus stampa quel fatto per **ogni** artefatto, anche per quelli finiti, perché
l'elenco del solo "cosa è indietro" è esattamente il cruscotto che il metodo
rifiuta (r9).

Provato sul corpus Eclosion: 5 specifiche, 7 topic, 26 claim, un conflitto vero
(capacità <100 vs 200–300, stessa data) rilevato, trattenuto, risolto dal tuo
ruling.

**Portabilità della conoscenza (F-030).** `export` impacchetta un sottografo
**insieme ai byte che le sue claim citano** — una chiusura, non una selezione: una
claim la cui fonte non si può riaprire è conoscenza del modello che arriva per
un'altra strada, e il validator del progetto di destinazione la rifiuterebbe.
L'export tira dentro anche la controparte di ogni set `CONTESTED` (la simmetria è
imposta, mezzo set è un albero che non passa i suoi controlli) e **lo dichiara**.
`import` è **additivo**: non sovrascrive mai un nodo, non cancella mai nulla, e
calcola tutto prima di scrivere un byte. Le claim già presenti si riconoscono
**per id**, non confrontando testi, perché `kb_claim_id` esclude il testo: stesso
artefatto content-addressed allo stesso span = stesso id in qualunque progetto.
La conoscenza attraversa il confine di progetto, **l'autorità no**: un ruling
importato arriva come `prov: IMPORTED`, conserva il suo `basis:` originale, deve
dichiarare `imported_from:`, e **non può superare una riga locale** finché non lo
ratifichi tu con una nota e un basis tuoi (ruling del proprietario, 2026-08-03).

## mkt-agentic-sdlc — la lente del mercato

Qui la fedeltà è all'**evidenza**, e l'agente percorre **nove fasi SOSTAC** con
cinque tipi di gate (Vision, USER, REVIEW, VALIDATOR, FINAL):

intake/triage → discovery (Wave 1) → **ricerca** → analisi della situazione →
obiettivi (Wave 2, **gate utente**) → strategia (**review gate** + gate utente) →
tattiche (Wave 3, **gate validator**) → azione → controllo e packaging (**review
finale** + `check` CLEAN).

- **L'evidence ledger è la spina dorsale**: ogni numero ha una classe — `FACT`
  (detto da te / dati primari, **e solo quelle due origini**), `BENCHMARK` (**URL
  reale + data obbligatori**), `ASSUMPTION` (**range obbligatorio**, mai
  stima puntuale, + confidenza + cosa cambia se è sbagliata) — e un id `[EV-nn]`
  che il validator risolve su ogni documento. **"Vedi VOC.md" non è una fonte per
  nessuna delle tre**: il validator lo rifiuta su un BENCHMARK (nessun `http`) e
  ora anche su un FACT che punta a un documento dell'ingaggio — classificare una
  ricerca come FACT era l'unica via per far entrare un numero senza URL, perché
  FACT è l'unica classe che la regola dell'URL non raggiunge (trovato dal field
  test 2026-08-02). Chi cita il cliente come origine resta esente: i suoi dati
  primari possono benissimo essere un file che ti ha passato lui. **Nessun numero dalla memoria del
  modello** — nemmeno se lo asserisci tu senza fonte: diventa FACT tuo, dichiarato.
  Due fonti indipendenti per ogni numero che guida budget o obiettivi.
- **Elicitazione a ondate con la regola cardinale**: si chiede solo ciò che
  possiedi tu (prezzo, margine, budget, capacità, red line, *semi* di competitor);
  tutto il resto si **ricerca** — chiederti "chi sono i tuoi competitor e come sei
  posizionato?" è esternalizzarti il lavoro della skill. ≤4 domande per round,
  linguaggio piano (mai "ICP" — "descrivi il tuo miglior cliente"), e il **"non lo
  so" pre-autorizzato** dentro le domande numeriche — toglie la pressione a
  inventare.
- **Quattro sweep di ricerca obbligatori** (E3): market sizing bottom-up, scan
  competitor (le LORO parole dal LORO sito, canali osservati, mai lettura del
  pensiero), voice-of-customer (citazioni verbatim con URL — le persona tracciano
  qui), benchmark di canale (senza, il funnel è finzione).
- **Framework come lenti, mai moduli**: SWOT sempre (ogni cella cita `[EV-nn]`);
  posizionamento alla Dunford con lo **swap test** — sostituisci il nome del
  competitor top nella frase di posizionamento: se regge ancora, il posizionamento
  è BOCCIATO; messaging house dove un pilastro senza proof point è uno slogan;
  split budget 70/20/10 di default, deviazioni argomentate; **kill/scale per
  canale fissati PRIMA del lancio** — "un piano senza control loop è una brochure"
  (BLOCK in review).
- **Il validator rifà i conti sulla prosa**: `budget` (somma allocazioni = totale,
  ±1%), `funnel` (Clicks=Budget/CPC, Leads=Clicks×CVR, Customers=Leads×Close%,
  CAC=Budget/Customers, ±5%, ogni cella ricomputata dalle celle a monte),
  `trace` (ogni tattica serve un obiettivo definito, ogni obiettivo ha un KPI —
  un orfano è un errore), `ledger` (integrità + risoluzione dei riferimenti).
- **Legge la spina condivisa traducendola** (sezione propria in `SKILL.md`): i file
  condivisi (`review.md`, `dispatch.md`, `guides.md`) sono scritti nel vocabolario
  neutro della famiglia, quindi dove dicono `sdlc_check.py` l'agente mkt legge
  `mkt_check.py`, e dove dicono "Phase 3 / Phase 5 closure" legge fase 6 (review
  della strategia) e fase 9 (control & packaging) del suo workflow a nove. **Le
  procedure vincolano come scritte; traducono solo i nomi** — è l'unica lente che
  ha bisogno di questo strato, perché è l'unica con fasi e docs root propri
  (`mkt_docs/` di default, `ai_docs/` su albero migrato con `migrate`).
- **L'Honesty Contract**: rifiuto pre-scritto di promettere risultati di mercato —
  la garanzia è il rigore del processo (zero numeri inventati, coerenza interna,
  misurabilità), mai l'esito.
- I deliverable parlano **la lingua del mercato target**; la struttura resta
  templata così il validator può fare il parsing.

## Dove sono Vision, UC, TM, ISP, TDD? (niente è sparito)

Quei nomi sono il vocabolario **Hybrid** (devPNT). Ogni lente riempie gli stessi
slot di governance con la propria carta:

| Slot (devPNT) | agentic-sdlc Standalone | kb-agentic Standalone | mkt-agentic-sdlc Standalone |
|---|---|---|---|
| M-VISION | milestone di `vision/roadmap.md` | idem | `MKT_VISION.md` (gate di fase 2) |
| D-UC (casi d'uso) | `## Use Cases` nell'ANALYSIS | idem | `ICP_PERSONAS.md` |
| P-TM (threat model) | `## Security and Threat Model` | `## Sources and Verification` | `THREAT_MAP.md` |
| E-ISP (impact/strategia) | `## Capability Ledger` + `## Impact` | idem (taxonomy ledger) | `STRATEGY.md` |
| E-TDD (design/piano) | corpo di design + `## Action Plan` | idem | `TACTICAL_PLAN.md` |
| E-TP (test/misura) | `## Test Strategy` | idem | `MEASUREMENT_PLAN.md` |

Regola che li tiene coerenti: **un master solo per artefatto** — in Hybrid il DB
vince e lo shadow (`SHADOW_[doc_key]_vX.Y.md`) si rigenera; in Standalone il
documento filesystem è l'autorità. Il design review gate è lo stesso slot nelle
due forme: si esegue UNA volta, mai due.

## Quando convivono nello stesso progetto

- **Un solo albero, un solo default**: `default_domain:` nel README della docs
  root; ogni artefatto può dichiarare la sua lente (`domain:`). Qualunque
  validator della famiglia dà **lo stesso verdetto** sullo stesso albero.
- **Il router** (`routing.md`, letto solo se c'è una sorella installata): per ogni
  L2/L3/Spike, il test di fedeltà — *a cosa deve essere fedele questo lavoro?*
  Con la deroga market-facing: scopo persuasivo verso il mercato → mkt,
  qualunque sia la fonte. Due fedeltà = due unità di lavoro (regola dello split).
  In dubbio, fail-open sulla lente caricata. `vision/` sta sopra lo split.
- **DRY fra lenti**: un fatto ha una casa sola; le altre lo **citano, mai lo
  copiano** — un fatto ricopiato è un finding di review. I nomi ambigui per lente
  ("threat model", "vision", `handoff.md`) si qualificano sempre.
- **La spina non può divergere**: 15 file condivisi byte-identici verificati dal
  drift guard a ogni build; i check portabili (`marketing.budget` su un documento
  kb con una tabella di budget, `knowledge.sources` altrove) si importano per
  nome e **aggiungono findings, mai autorità**.
