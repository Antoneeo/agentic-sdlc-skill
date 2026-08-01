---
description: How the three skills differ in the way an AGENT actually works under each — same spine, three fidelity disciplines. For the owner; body in Italian.
status: CURRENT
---
# La famiglia di skill: come lavora un agente sotto ognuna

**Per chi**: il proprietario, e chiunque debba scegliere quale skill installare o
capire perché un agente si comporta diversamente in tre progetti.
**Risponde a**: "cosa fa *concretamente* di diverso un agente sotto ogni lente".
**Non risponde a**: come sono impacchettate (architecture.md) o perché la famiglia
esiste (project_vision.md).

## L'idea in una riga

Le tre skill condividono **lo stesso processo** (la spina) e differiscono in **una
sola cosa fondamentale**: *a che cosa le affermazioni dell'agente devono essere
fedeli*. Tutto il resto — i documenti che scrive, i controlli che subisce, il
vocabolario — discende da quella scelta.

| | agentic-sdlc | kb-agentic | mkt-agentic-sdlc |
|---|---|---|---|
| **Fedele a** | il codice di QUESTO repo | i documenti che TU fornisci | l'evidenza di mercato |
| **Unità di lavoro** | feature (`F-`) | topic (`K-`) | engagement (`E1/E2/E3`) |
| **La domanda che l'agente si fa** | "cosa rompe questo cambiamento?" | "cosa sappiamo già, quanto è certo, da dove viene?" | "quale evidenza sostiene questa scelta?" |
| **Il peccato capitale** | modificare a istinto senza orientarsi | spacciare conoscenza del modello per fonte | inventare un numero |
| **Slot di rischio obbligatorio** | `## Security and Threat Model` | `## Sources and Verification` | `## Threat Map / Plan Risks` |
| **Albero documenti** | `ai_docs/` | `ai_docs/` (+ `corpus/`, `topics/`) | `mkt_docs/` (vision/strategy/tactics/deliverables) |

## La spina comune (identica, byte per byte)

Qualunque lente sia attiva, l'agente:

1. **Triaga ogni richiesta** (Rule Zero) e dichiara il livello + il verdetto del
   guide router — "L2 · router: no match" — così "non ho guardato" è
   indistinguibile da "ho guardato, niente".
2. **Consulta prima di creare**: registro dei workstream (`handoff.md`), indici
   generati, guide operative. Mai due case per lo stesso fatto.
3. **Passa i gate**: Vision gate per il lavoro significativo; design review
   indipendente prima di implementare; question discipline per ogni domanda a te
   (cercato prima + cosa blocca, assunzioni dichiarate in batch, mai "procedo?").
4. **Chiude meccanicamente**: `sdlc_check.py check` CLEAN, indici rigenerati mai
   scritti a mano, documenti nello stesso commit del lavoro che descrivono.

## agentic-sdlc — la lente del codice

Il flusso L3 di un agente: elicitazione → **architect pass** (le capability della
feature giudicate contro la Component Map: EXISTS / INADEQUATE / MISSING — "la
mappa silenziosa su un'area non letta non giustifica mai un MISSING") → ANALYSIS
con Impact file-per-file e threat model → **design review gate** (un reviewer che
non è l'autore, prima di ogni riga di codice) → implementazione con TDD →
batterie, chiusura, ADR se c'è stata una decisione architetturale.

In pratica: l'agente passa il tempo a **leggere codice prima di toccarlo** (chi
consuma questo simbolo? esiste già questa logica?) e a lasciare dietro di sé
documenti che il prossimo agente a freddo può eseguire.

## kb-agentic — la lente della conoscenza

Qui l'agente non scrive software: **costruisce un secondo cervello sui documenti
che gli dai**. Il modello poggia su due assi tenuti deliberatamente separati:
l'**astrazione** (un argomento è composto da altri — vive negli archi del grafo)
e la **certezza** (quanto il corpus sostiene un'affermazione — vive nelle righe
di claim). L'algoritmo di ingestione, per stadi:

**1. Intake — la fonte diventa intoccabile.** Ogni documento entra verbatim in
`corpus/given/`, content-addressed (il nome porta l'hash raw dei byte); una
versione nuova è un **append** col sidecar che dichiara `supersedes:`, mai una
sovrascrittura. I non-testuali (PDF, docx) ricevono l'**estrazione canonica
conservata** (`.txt` accanto all'originale, estrattore registrato): è a QUEI byte
che puntano gli offset. Ciò che dici a voce diventa nota `origin: elicited`; una
sintesi dell'agente dichiara `derived_from:`; una nota senza provenienza è
"conoscenza del modello travestita da fonte" e il validator la rifiuta.

**2. Estrazione — l'unità è il claim, non il documento.** Da ogni fonte escono
asserzioni falsificabili ("il prezzo di listino del modulo A è 12.000 EUR"),
ognuna una riga: `id | claim | valid | qty | about | source | prov | state`.
L'**id** è l'hash di posizione+quantità — mai del testo, così una riformulazione
LLM non crea doppioni. Il **locator** (`p=17@412-509`) è verificabile: il
validator apre l'estrazione conservata e controlla che lo span esista. `valid`
gestisce i fatti a scadenza (half-open: "fino al 1/3" e "dal 1/3" NON
confliggono); `qty` tipizza le cifre (effort/costo/durata) così si sommano;
`about` esprime le relazioni ("depends-on → phase-1").

**3. Collocazione (taxonomy pass) — cinque verdetti.** Il router scende il grafo
dei topic dall'indice generato (slug, descrizione, parents, sinonimi), seguendo
OGNI parent (poligerarchia): EXISTS → riconcilia; INADEQUATE → approfondisci o
figlio; MISSING → crea (ma **solo dopo aver interrogato il grafo** — la mappa non
letta non giustifica mai un MISSING); GENERALIZES → il concetto sta SOPRA nodi
esistenti: escalation, il riparenting è un'unità di lavoro, mai un effetto
collaterale; UNPLACED → quarantena non ordinata. Simile-ma-forse-diverso → nodo
fratello con la **riga di distinzione scritta**; se non riesci a scriverla, è lo
stesso concetto. I nodi fusi diventano tombstone (`redirect_to:`), mai cancellati.

**4. Riconciliazione — la macchina rileva e trattiene, mai decide.** Claim nuovo
contro righe esistenti sullo stesso soggetto: **conferma** → si appende la fonte
alla riga (mai una seconda riga: la base si rafforza, non si allunga);
**raffinamento** → riga nuova, la vecchia `SUPERSEDED`; **coesistenza** → scope
disgiunti, entrambe restano; **conflitto** → TUTTE le righe del set diventano
`CONTESTED`, simmetriche (il check fallisce se una cella viene girata a mano),
e **nessuna viene scelta**. Risolve solo informazione nuova: una fonte più
recente, o un tuo **ruling con `basis:`** — il fatto che conosci e il corpus no.
Senza basis niente ruling: una preferenza non è un fatto, e un CONTESTED aperto è
uno stato legittimo e permanente. Un ruling è sfidabile: un documento successivo
che lo contraddice riapre il caso mostrando il tuo basis accanto.

**5. Escalation — in blocco, mai a raffica.** L'ingestione non si ferma mai a
farti domande: i conflitti si accumulano e ti arrivano UNA volta, a fine giro,
ognuno in forma legale (i claim del set, fonti, date, provenienze, e perché la
macchina non può decidere).

In pratica: gli chiedi "quanto effort implica questo capitolato?" e lui
seleziona le righe `qty`, normalizza le unità e somma, con le fonti accanto; gli
dai una specifica nuova e ti dice cosa conferma, cosa raffina, cosa contraddice.
Provato sul corpus Eclosion: 5 specifiche, 7 topic, 26 claim, e un conflitto
vero (capacità <100 vs 200–300 utenti concorrenti, stessa data) rilevato,
trattenuto e risolto da un tuo ruling. Il validator (`graph`, `corpus`,
`claim-id`) verifica span, digest, id, simmetrie, cicli e raggiungibilità del
grafo.

## mkt-agentic-sdlc — la lente del mercato

Qui la fedeltà è all'**evidenza**: ogni numero che entra in un piano ha una
classe — `FACT` (detto da te o misurato), `BENCHMARK` (ricercato), `ASSUMPTION`
(dichiarata, con fonte e alternativa esclusa) — e un riferimento `[EV-nn]` nel
ledger. L'elicitazione va a **ondate** con la regola cardinale: *chiedere solo
ciò che possiedi tu in modo esclusivo* (prezzo, margine, budget, red line);
tutto il resto si ricerca, mai si chiede. Nove fasi SOSTAC: situazione →
obiettivi → strategia (gate di review) → tattiche → azione → controllo.

In pratica: l'agente intervista, ricerca, scrive strategia e piano — e il
validator **rifà i conti**: le allocazioni devono sommare al budget (±1%), il
funnel deve ricomputare (±5%), ogni tattica deve tracciare a un obiettivo e a un
KPI (`ledger`, `budget`, `funnel`, `trace`).

## Dove sono Vision, UC, TM, ISP, TDD? (niente è sparito)

Quei nomi sono il vocabolario **Hybrid** — quando devPNT governa il progetto, sono
artefatti versionati nel suo DB. In **Standalone** (nessun devPNT) lo stesso
contenuto esiste, ma vive dentro i documenti filesystem. La skill impone lo stesso
contenuto in entrambe le forme; cambia solo la casa:

| Contenuto | Standalone (filesystem) | Hybrid (devPNT) |
|---|---|---|
| Visione di prodotto | `vision/project_vision.md` | resta il master; la KL vision si rigenera da lui |
| Visione di milestone (M-VISION) | i milestone di `vision/roadmap.md` | **M-VISION** nel DB |
| Casi d'uso (D-UC) | `## Use Cases / User Needs` dentro l'ANALYSIS | **D-UC** |
| Threat model (P-TM) | `## Security and Threat Model` dentro l'ANALYSIS — obbligatoria, il validator la esige | **P-TM** |
| Impact analysis (E-ISP) | `## Capability Ledger` + `## Impact` dentro l'ANALYSIS (architect pass + mappa file-per-file) | **E-ISP** |
| Design tecnico (E-TDD) | il corpo di design dell'ANALYSIS + `## Action Plan` | **E-TDD**, con shadow `SHADOW_[doc_key]_vX.Y.md` esportato su filesystem prima di implementare |
| Piano di test (E-TP) | `## Test Strategy` dentro l'ANALYSIS | **E-TP** |

La regola che li tiene coerenti: **un master solo per artefatto** (la matrice di
ownership in `SKILL.md`) — in Hybrid il DB vince e lo shadow si rigenera; in
Standalone l'ANALYSIS è l'autorità. Il design review gate è lo stesso slot nelle
due forme: si esegue UNA volta, mai due.

## Quando convivono nello stesso progetto

- **Un solo albero, un solo default**: `default_domain:` nel README della docs
  root decide la lente di default; ogni artefatto può dichiarare la sua
  (`domain:`). Qualunque validator della famiglia dà **lo stesso verdetto** sullo
  stesso albero.
- **Il router** (`routing.md`, letto solo se c'è una lente sorella installata):
  per ogni L2/L3 l'agente decide chi possiede l'unità di lavoro col test di
  fedeltà — *a cosa deve essere fedele questo lavoro?* Codice del repo → code;
  documenti forniti → kb; evidenza di mercato → mkt. In dubbio, fail-open sulla
  lente caricata.
- **DRY fra lenti**: un fatto ha una casa sola; le altre lenti lo **citano, mai
  lo copiano**. I nomi ambigui per lente ("threat model", "vision") si
  qualificano sempre col dominio o col percorso.
- **La spina non diverge per costruzione**: 15 file condivisi byte-identici
  verificati dal drift guard; i tre validator sono lo stesso `sdlc_core.py` con
  un entry point per dominio.
