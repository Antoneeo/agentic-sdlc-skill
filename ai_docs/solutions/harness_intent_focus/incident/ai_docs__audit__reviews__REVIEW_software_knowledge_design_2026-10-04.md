# F-063 / F-064 — Review del design delle modifiche

Per owner e implementatore: valutare la progettazione nei due ANALYSIS e nella
mappa DESIGN_software_knowledge_files.md. Questo rapporto registra verifiche e
correzioni del design; efficacia del candidato e conformance del futuro diff restano
verifiche successive. Non sostituisce l'accettazione del costo da parte dell'owner.

Reviewer: `software_design_review`, agente separato con contesto fresco, read-only,
`gpt-6-astra high`, deep tier. Sessione invocante e modalità visibile al reviewer:
Default. Nessuna scrittura, implementazione o operazione devPNT da parte del reviewer.

## Verifiche indipendenti

- Baseline P1–P10: 10/10 PASS; controllo negativo: 10/10 fallimenti attesi.
- Inventario rigenerato coincidente: 108 file Python, zero errori AST; confronto
  testuale su 362 file di prodotto e 21 harness Python; hash degli input invariati.
- I due snapshot Eclosion corrispondono ai digest registrati. Sono rapporti ricevuti,
  non prove rieseguite né certificazione del checkout corrente di Eclosion.
- L'AST enumera riferimenti per nome/attributo, non è un resolver globale. La revisione
  ha rilevato il diverso contratto dei test che consumano le clausole Markdown.

## R1 — FAIL

| ID | Severità | Problema fondato | Correzione del design |
|---|---|---|---|
| D1 | BLOCK | Tre test KB richiedono le clausole in SKILL.md; il trasferimento a memory.md li romperebbe | Mappa estesa a test_kb_revision.py, test_kb_recall.py, test_kb_capture.py, con metodi precisi; nuovo proprietario verificato, ancore/garanzie KB e unicità canonica preservate |
| D2 | BLOCK | F-064 distribuiva metodi che rimandavano a procedure previste solo nella successiva F-063 | F-064 possiede estrazione, rinvii, support list e test; righe KB+SDLC separano le due modifiche; verifica esplicita dello stato intermedio autonomo |
| D3 | WARN | I metodi promossi contengono classificazioni KB che potrebbero avviare un secondo processo nel lavoro software | Scope KB dichiarato per quelle classificazioni; router/lente conservano triage; caso first_capture richiede assenza di seconda ANALYSIS o riclassificazione |

Evidenze D1: classi RevisionDoctrineTests, TestRecallDoctrine, TestCaptureDoctrine
nei tre moduli sotto `distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/`.
D2: memory.md attuale non possiede Revision; il vecchio riparto la assegnava a F-063.
D3: taxonomy §4, distillation §3 e portability §5. Tutti e tre i finding sono reali.

Il nuovo probe `doctrine_text_references` conserva 39 riferimenti, distinti dal call
graph delle API. La mappa rende conto anche dei consumatori invariati. Nessuna
clausola di garanzia è rimossa per evitare il fallimento di un test.

## Conformance statement R1

| Vincolo | Evidenza nel design e limite |
|---|---|
| UC1 / FS1,3,6 | F-063 modello concettuale, trigger e caso a freddo: discesa, fonti e gaps senza ricostruire la cronologia |
| UC2 / FS2,3,5 | F-064 formato/transizioni: natura distinta da prov/state; legacy non classificato; nessuna promozione per approvazione |
| UC3 / FS3,4 | Binding e diagnostica distinguono cambio/assenza/progetto; F-063 richiede impatto indiretto oltre gli hash |
| UC4 / FS2,3,5,6 | Flusso completo di selezione, ingestione, aggiunta e riconciliazione durante il lavoro; implementabilità documentale corretta tramite D1/D2 |
| UC5 / FS7 | Costo e prove su baseline/sole istruzioni/candidato, due sessioni fresche; beneficio ancora da misurare |
| Cinque flussi F-063 | Interface Contract e casi di valutazione coprono ogni UC, feedback e limiti; UC4 comprende scrittura e aggiornamento |
| KUC1 / KFS1 | Due header, schema opzionale, ID invariato; consumatori attuali usano chiavi nominate |
| KUC2 / KFS2,5 | Un buffer, estratto immutabile e binding, pubblicazione additiva e retry; nessun claim automatico |
| KUC3 / KFS3,4 | Derivazione AND, corroborazione OR, chiusura transitiva; MATCHED non certifica semantica |
| KUC4 / KFS6 | Quattro distribuzioni, entry point/packaging, legacy e import UNBOUND; autonomia corretta tramite D2 |
| Quattro flussi F-064 | Responsabilità, feedback, CLI ed exit code dichiarati per ledger, acquisizione, diagnostica e portabilità |
| T1 | Kind indipendente e prova nuova per osservare il comportamento |
| T2 | Binding, propagazione e limite esplicito per dipendenze non registrate |
| T3 | Selezione/minimizzazione prima della cattura; nessuna esecuzione o detector promesso |
| T4 | Ogni hop confinato, nessun accesso a binding estero; limite TOCTOU dichiarato |
| T5 | E1/E6/E7, firme conservate e drift guard; consumatori dottrinali aggiunti con D1 |
| T6 | L1 esente, nessun censimento/board; budget e costo dichiarati; triage delimitato con D3 |
| Vision: continuità | Grafo di progetto riusabile, proprietà e relazioni, casi freddi e secondo intervento |
| Vision: garanzie epistemiche | Natura, provenienza, condizioni, stato e prove conservati; riconciliazione senza cancellazioni silenziose |
| Vision: riuso KB | Stesso corpus, ledger, grafo e knowledge.py; helper estratti dal ciclo esistente |
| Non-obiettivi | Cattura mirata, nessuna mappatura/bulk/sintesi non verificabile; proprietà prima delle dipendenze; costo da accettare e misurare |
| R2/R3 | Lookup/diagnostica delle prove, nessuna gestione o graduatoria del lavoro |
| R4/R24 | Estensione oltre F-057 dichiarata nuova; non eredita l'accettazione del costo |
| R10/R11 | Un solo motore/metodo, triage della lente proprietaria reso esplicito con D3 |
| Eclosion | Fallimento osservato della ripresa distinto dai controlli verdi del nucleo; nessuna conclusione sul percorso completo |

Nessun CANNOT_VERIFY ulteriore sulla baseline. Test ed efficacia del candidato
restano futuri, come dichiarato nei documenti.

## R2 — PASS

Il reviewer ha riletto i tre documenti aggiornati e verificato D1/D2/D3: tutti
ADDRESSED, nessun BLOCK, WARN o CANNOT_VERIFY residuo nel delta. Inventario rigenerato
identico, 39 riferimenti dottrinali e 83 percorsi unici nella mappa; copertura e hash
del motore invariati. Probe runtime non ripetuti perché il prodotto non è cambiato.

| Vincoli interessati | Conformance sul delta |
|---|---|
| UC1/UC4, FS1/FS5, KUC4/KFS6, T5 | Controlli preservati sul nuovo proprietario; F-064 verificabile prima dei trigger F-063 |
| FS6, T6, R10 | Nessuna seconda autorità di triage; caso first_capture verifica la proprietà |
| Vision un solo grafo/motore, R11 | Estrazione comune prima dell'integrazione, nessun sistema parallelo |
| Vision continuità fondata | Quattro README e sintesi workflow aggiornati alla chiusura sul comportamento realmente implementato |
| Costo, R4/R24, non-obiettivo burocrazia | Budget e costo operativo espliciti; accettazione dell'owner non presunta |
| Altri UC/FS, contratti, T1–T4 e garanzie epistemiche | Matrice R1 ancora valida; formati, ID, binding, AND/OR, confini e limiti invariati |

Esito: design tecnicamente pronto per la valutazione dell'owner. Nessun esito del
candidato, beneficio misurato o autorizzazione automatica all'implementazione implicato.
