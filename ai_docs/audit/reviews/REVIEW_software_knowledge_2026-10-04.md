# F-063 — Review della Vision e dell'analisi iniziale

Date: 2026-10-04. Autore dell'analisi: sessione GPT-6, modalità Default;
identificativo del modello autore non esposto. Reviewer: gpt-6-astra, high,
contesto fresco, read-only. Nessuna review certifica implementazione o efficacia.

## Vision — blind check

Reviewer `vision_gate`, nessun accesso a file o strumenti: testo dell'owner e casi
forniti nel prompt. Verdict **PASS**, nessun blocker. Testo della Vision invariato.
Le citazioni seguenti sono gli ancoraggi usati dal reviewer, non nuovi requisiti.

| Caso | Esito | Ancoraggio alla Vision |
|---|---|---|
| Riutilizzare topic/claim e acquisire conoscenza nel lavoro | ACCEPT | «Riutilizzare le capacità di kb-agentic»; «La copertura cresce attraverso il lavoro» |
| Grafi separati per milestone, fusione soltanto a fine progetto | REJECT | «un grafo di conoscenza comune […] riutilizzabile fra milestone e sessioni» |
| Mappare tutto prima di qualsiasi modifica | REJECT | «Mappare preventivamente tutto il repository» è un non-obiettivo |
| Limitarsi a un catalogo di path documentali | REJECT | «concetti e relazioni a diversi livelli di astrazione» |
| Design approvato presentato come comportamento osservato | REJECT | «Una proposta non implementata non viene presentata come comportamento esistente» |
| Requisito e comportamento divergenti, distinti e fondati | ACCEPT | «Distinguere funzionamento osservato, requisiti»; niente «contraddizioni silenziose» |
| Codice modificato rende la conoscenza da riverificare, non automaticamente falsa | ACCEPT | «identifica ciò che deve ancora verificare»; la segnalazione da sola non esaurisce l'aggiornamento |
| Motore parallelo giustificato dalla velocità | REJECT | «senza creare un sistema parallelo» |
| Casi diversi con baseline, errori, ricostruzione e rilavorazioni | ACCEPT | «su casi diversi, misurando correttezza, lavoro di ricostruzione e rilavorazioni» |
| Catturare indiscriminatamente tutte le righe e i documenti | REJECT | Non-obiettivo del riversamento indiscriminato |
| Aree ignote visibili senza obbligo di completarle | ACCEPT | «le aree inesplorate restano riconoscibili»; «approfondire soltanto ciò che serve» |
| Dossier obbligatorio completo per ogni intervento, presentato come continuità | REJECT | «approfondire soltanto ciò che serve» e non-obiettivo della burocrazia |

Restano scelte di design, non lacune bloccanti della Vision: selezione della
conoscenza, rappresentazione delle fonti e dei contrasti, individuazione delle
affermazioni toccate, riverifica, campione e baseline della valutazione.

## Evidenze dell'autore

Preaudit dell'analisi: 303 righe su budget 350; 13 riferimenti di percorso
risolti, zero mancanti; 5 use case, 7 requisiti funzionali, 6 rischi.
Caratterizzazione: dieci osservazioni sul motore reale, exit 0. Inversione di
ciascuna aspettativa: dieci esiti negativi, exit 1 atteso. Input e hash registrati
in `ai_docs/solutions/harness_software_knowledge/baseline.json` e
`negative-control.json`. Le prove non misurano il beneficio della nuova capacità.

## Analisi iniziale — review indipendente

Reviewer `analysis_review`, gpt-6-astra high, fresh context, read-only;
modalità dichiarata dal reviewer: Default. Oggetto: affidabilità dell'analisi
iniziale come input alla progettazione, non progetto esecutivo completo.

R1: **PASS**, 0 BLOCK, 2 WARN, 0 CANNOT_VERIFY. Il reviewer ha riletto Vision,
ruling, fonti KB, codice e packaging; rieseguito le dieci osservazioni e il
controllo negativo; verificato gli hash dei tre input contro gli esiti archiviati.
Il controllo negativo inverte le aspettative: prova che gli assert falliscono
quando la condizione attesa è negata, non una mutation analysis del prodotto.

| Finding | Evidenza R1 | Correzione dell'autore |
|---|---|---|
| W1 — riuso procedurale troppo generico | Capability Ledger / Raccordo: il metodo KB non nominava Topic Recall e The Capture Moment già esistenti | Fonte SKILL KB esplicitata; raccordo nomina entrambi e distingue cattura delle decisioni dal nuovo legame evidenza/versione |
| W2 — T3 senza caso futuro dedicato | Test Strategy copriva confini/import, senza esercitare fonti ostili e segreti | Caso con istruzione ostile e segreto sintetico: mancata esecuzione, minimizzazione prima intake, nessuna propagazione indesiderata |

### Conformance statement R1

Riferimenti alle sezioni dell'ANALYSIS, che possiede i requisiti; questa tabella
registra dove il reviewer li ha verificati, senza duplicarne la definizione.

| Vincolo | Evidenza verificata |
|---|---|
| UC1 | FS1/3/6; flusso UC1; caso sessione fredda |
| UC2 | FS2/3/5; Modello concettuale; caso proposta non implementata |
| UC3 | FS3/4; P6–P9; flusso UC3; casi modifica e rename/delete |
| UC4 | FS5/6; Raccordo; caso due interventi; W1 per precisione del riuso |
| UC5 | FS7; flusso UC5; confronto baseline/istruzioni/candidato |
| FS1 | Objective e grafo unico; ledger gerarchia; caso tra sessioni |
| FS2 | Modello concettuale, P4/P5 e popolazione legacy |
| FS3 | Evidenze, condizioni/configurazioni, test distinto dall'esito e indisponibilità |
| FS4 | P6–P9; Action Plan su revisioni non committate, rename/delete e dipendenze |
| FS5 | Riconciliazione, coesistenza fra requisito e comportamento, nessuna sostituzione automatica |
| FS6 | Crescita sul lavoro, L1 e selezione prima dell'intake |
| FS7 | Test Strategy: rubriche e soglie prima dell'esecuzione, nessuna efficacia rivendicata |
| T1 | FS2/5, dimensioni indipendenti, proposta approvata non implementata |
| T2 | FS3/4, copia/codice e cascata, dati preesistenti |
| T3 | Requisito esplicito; W2 sulla prova futura |
| T4 | P10, confinamento, import offline, rename/delete |
| T5 | Quattro distribuzioni, legacy e packaging |
| T6 | Gaps locali, assenza board, costo misurato, L1 invariato |
| Beneficio e attori | Objective, UC1–UC5, FS1/5 e flussi; milestone come contesti |
| Garanzie di natura, evidenza, riconciliazione e aggiornamento | FS2–FS5, modello e risultati P4–P9 |
| Riuso KB | Motore/grafo unico e packaging, W1 per precisione del metodo |
| Nessuna mappatura preventiva / riversamento | FS6 e selezione prima intake |
| Nessuna sintesi non verificabile | FS3, modello delle evidenze, conservazione della protezione P7 |
| Nessuna burocrazia | Feature Vision: niente secondo dossier, L1 protetto, costo da misurare |
| Grafo concettuale distinto da dipendenze | Modello concettuale |
| Efficacia su casi diversi | Test Strategy, beneficio non ancora dimostrato |
| r2/r3/r4/r10/r11/r24 e Standalone | Feature Vision, riuso del core, rivalutazione dell'estensione, un solo triage |

Il reviewer ha confermato che schema, firme, consumatori completi, transizioni e
costo concreto restano dichiaratamente da progettare; il PASS non li certifica.

R2, circoscritta alle correzioni: **PASS**, W1 e W2 **ADDRESSED**; nessun nuovo
BLOCK/WARN/CANNOT_VERIFY. Riscontri nella versione esaminata: fonte KB e Raccordo
(righe 75 e 203), caso T3 (riga 291). L'analisi passa da 303 a 311 righe,
entro il budget 350; nessun probe o file del prodotto è cambiato fra i round.

## Correzione del flusso di alimentazione — review circoscritta

Su rilievo dell'owner, esplicitate ingestione, aggiunta e aggiornamento nel flusso.
Lo stesso reviewer ha riletto il delta: **PASS**, nessun finding. UC4, FS5, il
contratto, il diagramma e il nuovo caso di prova coprono acquisizione durante le
fasi, confronto con il grafo comune, aggiunta, aggiornamento tracciato, coesistenza,
conflitto e riverifica. Selezione delle fonti, natura delle affermazioni e limiti
restano espliciti; nessuna capacità proposta è dichiarata implementata.
Analisi: 331 righe. Vision, runtime e probe invariati; probe non rieseguiti per
questa correzione documentale. Il PASS riguarda soltanto il delta descritto.
