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
che gli dai**. Il flusso di ingestione: intake (originale conservato verbatim,
content-addressed, con estrazione canonica) → estrazione di **claim** (asserzioni
falsificabili, ognuna con locator verificabile nel byte esatto della fonte) →
**taxonomy pass** (collocazione nel grafo dei topic: EXISTS / INADEQUATE /
MISSING / GENERALIZES / UNPLACED) → **riconciliazione**: conferma rafforza la
riga, raffinamento la sostituisce, e un conflitto **non viene mai deciso dalla
macchina** — resta CONTESTED, simmetrico, finché un'informazione nuova (un
documento più recente, o un tuo ruling con `basis:` — un fatto che conosci, mai
una preferenza) lo risolve.

In pratica: gli chiedi "quanto effort implica questo capitolato?" e lui somma le
righe `qty` con le fonti accanto; gli dai una specifica nuova e ti dice cosa
conferma, cosa raffina, cosa contraddice — col conflitto in faccia, mai risolto
in silenzio. Il validator verifica span, digest, simmetrie e grafo (`graph`,
`corpus`, `claim-id`).

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
