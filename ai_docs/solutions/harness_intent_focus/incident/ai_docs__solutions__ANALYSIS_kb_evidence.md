---
id: F-064
feature: Natura dei claim ed evidenze software nel motore KB comune
description: Design dei formati compatibili, acquisizione mirata, riverifica e propagazione nel motore KB condiviso.
status: COMPLETED
end_date: 2026-10-04
level: L3
domain: code
topics: [software-knowledge, shared-memory, evidence]
start_date: 2026-10-04
branch: codex/software-knowledge
---
# Natura dei claim ed evidenze software

Per implementatore e reviewer: realizzare l'estensione del motore KB da cui dipende
[F-063](ANALYSIS_software_knowledge.md). Questo documento possiede formati, firme,
diagnostica e compatibilità; F-063 possiede i trigger SDLC e la valutazione d'uso.
Design approvato dall'owner e implementazione verificata. Non prescrive metadata software
nei corpus non software. Nessuna nuova dipendenza o servizio.

## Objective

Distinguere la natura delle affermazioni e rendere controllabile il legame fra
evidenza conservata e file osservati, riusando corpus, claim, grafo e derivazioni.
Unità separata per `architect.md` §4: contratto dati pubblico e quattro distribuzioni
consumatrici; può essere rilasciata prima del raccordo SDLC F-063.

## Feature Vision

Autorità: [M-VISION comune](../vision/features/VISION_software_knowledge.md), invariata;
`vision/project_vision.md` e rulings r2/r3/r4/r10/r11/r24. Questa unità serve le garanzie
di natura, evidenza, riconciliazione e aggiornamento. Non genera conoscenza dal codice,
non certifica verità o copertura semantica, non introduce stati di avanzamento dei topic.
Costo d'adozione e valutazione: F-063, sezione Costo. Nessun obbligo per L1.

## Orientamento e prove

Standalone: il server devPNT restituisce `D:/SoftwareDev/chatPNT`, non questa root.
Base `2d5a5c67402487200fe5df3929d0b093fad6e761`; guida letta: `GUIDE_shared_project_memory.md`.
Il motore è `skills/agentic-sdlc-skill/scripts/knowledge.py`, distribuito in quattro copie.
P1–P10 in `harness_software_knowledge/probe.py`, rieseguiti il 2026-10-04: 10/10.
P4/P5 fondano il formato opzionale; P6/P9 il legame alla sorgente; P7/P10 i confini
da preservare; P8 la propagazione. Sono caratterizzazioni del presente, non test del candidato.
La mappa dei simboli e il delta testuale sono in `harness_software_knowledge/design_inventory.json`.

## Use Cases / User Needs

Superfici EXISTS: topic, claim, corpus, graph/check/stale, export/import. NEW:
colonna `kind`, metadata software, `capture-source` ed `evidence`.

| ID | Bisogno | Beneficio della Vision |
|---|---|---|
| KUC1 | Agente/reviewer distinguono intento e osservazione sullo stesso concetto | Decisioni leggibili e proprietà preservate |
| KUC2 | Agente conserva una prova selezionata e ritrova la versione osservata | Evidenze riapribili con limiti |
| KUC3 | Agente riconosce il sostegno da riverificare dopo cambiamenti | Conoscenza superata riconoscibile |
| KUC4 | Manutentore aggiorna le distribuzioni e riapre corpus precedenti/importati | Riuso KB senza sistema parallelo |

## Functional Spec

| ID | Comportamento e accettazione |
|---|---|
| KFS1 | La natura esplicita resta indipendente da provenienza, riconciliazione e approvazione; dati precedenti non classificati restano tali |
| KFS2 | L'acquisizione seleziona una fonte, conserva esattamente l'estratto e la provenienza della versione letta; una seconda acquisizione identica non duplica la fonte |
| KFS3 | Variazione, assenza, appartenenza a un altro progetto e integrità violata sono distinguibili; nessuno di questi eventi decide la verità dell'affermazione |
| KFS4 | Una derivazione espone la dipendenza da prove cambiate; una corroborazione indipendente può sostenere ancora il claim, conservando visibili le prove precedenti |
| KFS5 | Consultazione e diagnostica non scrivono; acquisizione non modifica claim, gerarchia o stato di riconciliazione |
| KFS6 | Ledger legacy, ID e autorità importata restano compatibili; un bundle include le dipendenze delle evidenze senza leggere file della macchina esportatrice |

## Interface Contract

| Flusso | Responsabilità attraversate | Feedback |
|---|---|---|
| KUC1 | Agente → autore del claim → ledger → controllo grafo | Natura dichiarata o assente, errore di formato, conflitto e successori |
| KUC2 | Agente → selezione già letta → acquisitore → corpus | Percorsi creati/riusati, origine e intervallo; rifiuto prima di pubblicare un riferimento |
| KUC3 | Agente → selezione topic → controllo evidenze → catene di derivazione | Claim, fonte, motivo e limiti della riverifica; nessun verdetto semantico automatico |
| KUC4 | Manutentore → distribuzione comune → entry point; agente → export/import | Stesso formato e risultato in ogni lente; prove estere non associate implicitamente al checkout |

## Capability Ledger

| Capacità | Stato | Proprietario e limite |
|---|---|---|
| Ledger e riconciliazione | INADEQUATE | `kb_parse_claims`, `kb_check_claims`; P4/P5: natura non rappresentata |
| Fonte immutabile e locatori | EXISTS | `kb_corpus_check`, `kb_check_locator`; P7/P10: digest e confine docs |
| Collegamento al file osservato | INADEQUATE | `kb_corpus_check`; P6: `original_sha256` non confrontato |
| Dipendenze delle sintesi | EXISTS | `kb_time_cycle`; P8: catena da supersessione esplicita |
| Distribuzione e portabilità | INADEQUATE | `shared_files.py`, `kb_export_closure`, `kb_import_plan`; aggiungere formato e chiusura delle derivazioni |

## Impact

Mappa per ogni percorso, incluse copie, test e consumatori verificati senza edit:
[DESIGN_software_knowledge_files.md](DESIGN_software_knowledge_files.md).
Questo documento decide l'unità **KB** di quella mappa; F-063 decide l'unità **SDLC**.
Non cambiare `sdlc_core.py`, risoluzione docs-root, funzione degli ID o indici del grafo.

### Metodi comuni e autonomia dell'unità

F-064 comprende anche l'estrazione di Topic Recall, Capture Moment e Revision dalla
skill KB in `memory.md`, i rinvii nelle skill e nei metodi, e i test che leggono quelle
clausole. Preserva i trigger/domande specifici KB e l'unicità della clausola canonica
di revisione. I tre test locali nominati nella mappa verificano distintamente
proprietario comune, puntatori e garanzie KB; E7 esercita le copie comuni.
F-063 aggiunge in seguito soltanto trigger e vincoli del lavoro software.

Distillation, taxonomy e portability delimitano le proprie classificazioni L2/L3
agli incarichi KB: nelle altre lenti decide il router con il rispettivo Rule Zero.
Il metodo comune non crea un secondo incarico o triage. Prima di applicare F-063,
verificare lo stato F-064 isolato: riferimenti e ancore tutti risolvibili, support list,
profile e pack completi, batterie pertinenti verdi nelle quattro distribuzioni.

### Formato del claim

Conservare `CLAIM_COLUMNS` con le otto colonne attuali. Aggiungere
`TYPED_CLAIM_COLUMNS = CLAIM_COLUMNS + ("kind",)` e `CLAIM_KINDS` con esattamente
`OBSERVATION`, `REQUIREMENT`, `HYPOTHESIS`, `DESIGN`.
Il parser accetta solo i due header completi e le rispettive arità, mai colonne ignote
o righe miste. Una tabella legacy restituisce le stesse chiavi di oggi; una tipizzata
aggiunge `kind`. Un valore assente nel legacy significa non classificato, mai OBSERVATION.
`claim_schema: 2` nel topic richiede l'header tipizzato; valore diverso da 1/2 è errore.
Nuovi topic software dichiarano schema 2. Il non software può continuare con schema 1.

La natura non entra nell'ID: `kb_claim_id(path, locator, qty_key)` resta invariato.
Le collisioni si risolvono con prove/locatori realmente distinti, mai alterando quantità
o aggiungendo sale arbitrario. Un progetto realizzato produce un'osservazione con prova
nuova; non cambia in place il kind DESIGN. Classificare una riga legacy richiede lettura
della fonte; nessuna migrazione automatica. `prov` conserva le sue cinque classi.
Fra righe entrambe tipizzate, CONTESTED e SUPERSEDED richiedono lo stesso kind;
requisito non soddisfatto e osservazione divergente coesistono, con relazione descritta.
Un collegamento con legacy non classificato è segnalato come non verificabile, non promosso.

### Evidenza software nel corpus esistente

Nuova acquisizione: solo file UTF-8 del progetto, intervallo di righe esplicito,
ruolo `code|test|config|result`, dimensione origine massima 16 MiB. Un solo buffer
di byte produce digest dell'intero file ed estratto: il file non viene riletto fra i due.
CRLF resta CRLF; una riga termina solo con LF, come la contano `grep -n` e git
(`\f`, `\v`, `\r` isolato, U+0085 e U+2028 sono contenuto); intervallo inclusivo 1-based e non vuoto.
I locatori del claim indirizzano l'estratto conservato, non le righe mobili del checkout.

Metadata nuovi, tutti obbligatori se presente uno dei campi `software_*`:

| Campo | Contratto |
|---|---|
| `software_schema` | `1` |
| `software_project_id` | UUID canonico uguale a `knowledge_project_id` nel README del docs-root per confrontare il checkout |
| `software_path` | Percorso POSIX relativo al project root risolto dall'entry point; nessuna inferenza da `docs.parent` |
| `software_sha256` | SHA256 raw dei byte dell'intero file al momento della cattura |
| `software_lines` | `A-B`, estremi inclusivi validati durante la cattura |
| `software_role` | Uno dei quattro ruoli sopra; un file test non equivale al suo risultato |

La sidecar mantiene `sha256`, `date`, `provenance: GIVEN`, `extractor: utf8-lines-v1`.
`extracted_through` resta assente finché l'agente non ha distillato l'estratto: la copia
non equivale alla lettura. Nessun `original_path` viene aggiunto per questa acquisizione.
Eventuale revisione Git/configurazione/ambiente è descritta nella nota derivata che usa
le fonti; non sostituisce i digest e non è interrogata tramite comandi della fonte.

Nome: `source-<sha256 estratto>-<sha256 binding>.txt`; entrambi i digest interi.
Binding = JSON UTF-8 canonico (chiavi ordinate, separatori compatti) dei sei campi
software più `derived_from` normalizzato e ordinato. La sidecar ha lo stesso nome +
`.meta.md`. Il nome conserva identità di contenuto e provenienza anche se lo stesso
estratto compare in file, righe o versioni diverse. Date/coverage non entrano nel binding.
`supersedes` non viene scritto dalla cattura: richiede la riconciliazione motivata.

`knowledge_project_id` nasce al primo `capture-source` se manca: UUID casuale nel
frontmatter di `<docs>/README.md`, preservando corpo e campi. Un ID già presente non
si sostituisce; malformato o duplicato è errore. La chiusura rigenera il catalogo README.
Clone/worktree conserva l'ID; import di un bundle non importa il README né adotta l'ID
estero. Non è un'identità di sicurezza: corpus e checkout restano materiale non fidato.

### Catene, corroborazioni e diagnostica

I `;` in `source` sono corroborazioni indipendenti (OR). `derived_from` sono premesse
congiunte (AND): una prova che richiede codice + test + esito si rappresenta con UNA
nota derivata da tutti e tre, citata dal claim. Non si elencano i tre come corroborazioni.
Una fonte derivata può a sua volta fondarsi su altre note; il controllo percorre la
chiusura transitiva, rileva cicli e dangling, e non si ferma al primo hop.

| Stato calcolato della prova | Condizione | Conseguenza |
|---|---|---|
| MATCHED | Binding locale e byte di tutti gli input collegati invariati | Solo corrispondenza degli input dichiarati; nessuna certificazione del comportamento |
| CHANGED | Digest attuale diverso | Riverificare entro le condizioni della prova |
| UNAVAILABLE | File assente/non leggibile o rename non riconciliato | Prova storica riapribile, confronto attuale impossibile |
| UNBOUND | ID locale assente/diverso | Non aprire il percorso software; servono prove del progetto ricevente |
| UNTRACKED | Fonte legacy senza binding o premessa non collegata | Limite esplicito; nessuna attualità inferita |
| INVALID | Schema/digest conservato/percorso/catena non valido | Errore d'integrità; non usare la catena |

La proiezione contiene ogni fonte e motivo, non un solo colore. Un ramo AND richiede
tutte le premesse MATCHED; un ramo non collegato mantiene UNTRACKED anche accanto a
una premessa MATCHED. Per OR basta una catena completa MATCHED, ma rimangono visibili
le alternative cambiate/non disponibili. CONTESTED e SUPERSEDED non diventano utilizzabili
per questo: stato, natura, condizioni e freschezza sono colonne separate.
La scelta di quali input sostengono davvero una proprietà resta dell'agente/reviewer.
Un hash non trova dipendenze omesse, nuove call site o condizioni d'ambiente non registrate:
F-063 impone l'analisi d'impatto prima del riuso dopo una modifica pertinente.

### Firme e responsabilità in knowledge.py

Tutti i percorsi concreti delle quattro copie sono nella mappa dei file.

| Simbolo | Cambiamento e integrazione |
|---|---|
| `kb_parse_claims(text)` | Due header/arità; vecchio return `(rows, errors)` preservato; tutti i consumatori usano chiavi nominate |
| `kb_check_claims(root)` | Valida kind/schema e transizioni tipizzate; return `(errors, warnings, notes)` invariato |
| `kb_corpus_check(root)` | Valida forma dei binding e nome/digest; non apre software locale da questa API priva del project root |
| `kb_source_graph(docs)` NEW | Restituisce `(reverse_edges, node_meta, superseded_sources, dangling)`; estrazione del grafo oggi locale a `kb_time_cycle` |
| `kb_derivation_dependents(reverse_edges, node_meta, seeds)` NEW | Restituisce tuple ordinate `(owner, seed, via)`; visita finita, tombstone non emesso ma attraversato |
| `kb_time_cycle(docs)` | Usa i due helper; firma e quattro chiavi di output attuali invariate; nessuno stato nuovo scritto |
| `kb_software_meta(meta)` NEW | `dict` normalizzato o `None` se nessun campo software; `ValueError` su presenza parziale/forma invalida |
| `kb_project_id(docs, *, create=False)` NEW | UUID o `None`; crea soltanto dalla cattura, mai da check/import; errore su README malformato |
| `kb_capture_source(project, docs, rel, start, end, role, derived_from=())` NEW | `(artifact_rel, sidecar_rel, created)`; validazioni complete prima della pubblicazione; nessun claim generato |
| `kb_software_findings(project, docs, topics=())` NEW | `{errors, sources, claims}`; fonti `(rel,status,reason)`, claim `(topic,id,kind,state,supports)` con supports per fonte; read-only |
| `kb_cmd_evidence(project, docs, topics=(), json_output=False)` NEW | Stampa la proiezione; CLI nuova con semantica exit sotto |
| `kb_cmd_capture_source(project, docs, args)` NEW | Unico adattatore dei parametri di acquisizione; stampa percorsi/created, gestisce errori senza traceback |
| `kb_validate_surface(docs, full=False, project=None)` | Parametro opzionale finale; `full` compone diagnostica evidenze se presenti. Senza project, nessuna inferenza: UNBOUND |
| `kb_cmd_check(root, docs, strict=False, hybrid=False)` | Aggiunge diagnostica evidenze; propaga errori, non trasforma drift in falsità o nuovo gate legacy |
| `kb_cmd_stale(root, docs, hybrid=False)` | Stessa raccolta per i soli finding evidenze; semantica exit del core preservata |
| `kb_export_closure(docs, slugs)` | Include chiusura transitiva `derived_from` + sidecar; fonte assente/escape/ciclo impedisce un bundle incompleto; return invariato |
| `kb_import_plan(bundle, docs)` | Non ignora errori del parser tipizzato; preserva binding esteri, senza riscrivere ID o leggere path software; return invariato |
| `kb_cmd_help()`; `main(argv=None)`; `INTERCEPTED` | Espongono/distribuiscono i due nuovi comandi; forward-by-default preservato |

Il grafo condiviso normalizza ref docs-relative e bare name secondo il contratto attuale,
ma rifiuta escape/link prima di leggere. L'aggiunta di questa guardia interessa anche
export: nomi esterni precedentemente tollerati diventano finding, non copie implicite.
Tutti i testi CLI seguono il formato inglese esistente; nessuna UI o nuova libreria i18n.

### CLI e scritture

`capture-source PATH --lines A:B --role ROLE [--derived-from REF ...] --root PROJECT`
usa anche `--docs-dir`. `REF` è un artefatto docs-relative esistente e confinato;
non accetta URL, comandi o riferimenti esterni. È l'unico nuovo comando che scrive.
`evidence [--topics slug,slug] [--json] --root PROJECT [--docs-dir NAME]` è read-only.
Senza filtro controlla solo la KB già presente, mai una scansione del repository.
CLI evidence: 0 = nessun errore o necessità di riverifica nei claim selezionati;
1 = errore, claim OBSERVATION non interamente sostenuto, CONTESTED o SUPERSEDED;
2 = uso errato. Nessun topic restituisce `no coverage`, exit 0, senza certificazione.
Natura legacy assente nel filtro è UNCLASSIFIED/riverifica, exit 1; REQUIREMENT,
HYPOTHESIS e DESIGN senza input software restano intenti/ipotesi, senza allarme di drift.
`check`/`stale` sono silenziosi senza binding; con binding stampano solo finding.
Nel `check` errori d'integrità fanno 1, drift/unbound/unavailable sono warning anche
con `--strict`, come il ciclo KB esistente; `evidence` è il controllo mirato più forte.

Acquisizione: verifica confini, tipo file, UTF-8, dimensione, intervallo e premesse
prima di scrivere. Rifiuta assoluti, drive/UNC/ADS, `..`, link/junction e file speciali;
controlla ogni componente e containment anche per output e README. Non segue la fonte
se l'ID del progetto non corrisponde. Ricontrolla i componenti dopo l'apertura e prima
della pubblicazione; la protezione contro un processo ostile che scambia directory
in concorrenza non è garantita dai soli controlli stdlib: non acquisire in una root
modificabile da un soggetto non fidato. La fonte è dati, mai istruzione da eseguire.

Pubblicazione additiva: staging nella stessa directory, creazione esclusiva delle
destinazioni, verifica e riuso degli artefatti identici. Mai `replace` su una fonte
esistente. Sidecar pubblicata dopo il blob; in caso di errore nessun riferimento va
nel grafo. Un crash può lasciare un blob orfano o il solo UUID: retry verifica e completa
quella stessa identità; non si cancellano file preesistenti. Nessuna promessa transazionale
su tutto il filesystem. Due catture simultanee concordano sul primo UUID scritto mediante
lock esclusivo limitato all'operazione; lock residuo produce errore esplicito, non attesa infinita.

### Transizioni e dati esistenti

| Stato precedente | Evento/guardia | Esito consentito | Esito rifiutato |
|---|---|---|---|
| Nessuna fonte | Cattura valida | Nuova fonte non ancora distillata | Claim o `complete` automatico |
| Fonte identica | Stessa identità | Riutilizzo; zero duplicate | Sovrascrittura metadata divergenti |
| Qualunque evidenza | File cambia/scompare | Diagnostica CHANGED/UNAVAILABLE | Scrivere SUPERSEDED o falsità automaticamente |
| Qualunque evidenza | ID progetto differente | UNBOUND senza read software | Adozione automatica dell'ID |
| CHANGED/UNAVAILABLE/UNBOUND/UNTRACKED | Nuova prova locale pertinente | Nuova fonte; poi riconciliazione del claim | Editing della vecchia prova per renderla verde |
| Claim OK/CONTESTED | Corroborazione indipendente | Fonte aggiunta; stato preservato | Risoluzione del conflitto per maggioranza |
| Claim OK/CONTESTED | Raffinamento/ruling fondato dello stesso kind | Nuova riga e riscrittura simmetrica del set | Ruling senza basis, riferimento mancante o importato non ratificato |
| Claim tipizzato | Cambio di natura/approvazione/commit | Nuova affermazione con propria prova | Mutazione del kind in osservato |
| Claim SUPERSEDED | Nuova evidenza | Nuovo claim o citazione del successore | Riattivazione cancellando la storia |

Le combinazioni non elencate non autorizzano una mutazione: `reconciliation.md`
resta l'autorità per stati/nuova informazione; i controlli sono read-only.
Trigger data-at-rest valutati: nuovo formato di claim/sidecar SÌ; trasferimento di
invarianti read/write NO; divieto di backfill NO; ritiro di sanitize/authorize NO.
Popolazioni: ledger a otto colonne resta leggibile; fonti senza binding restano storiche;
corpus non software resta silenzioso; import resta UNBOUND; nessuna migrazione richiesta.
Tool precedenti rifiutano schema 2 (P5): aggiornare il lettore prima di creare tabelle
tipizzate. Non fare downgrade cancellando kind; conservare il nuovo lettore e i file.

## Security and Threat Model

| Rischio | Requisito verificabile |
|---|---|
| Lettura/scrittura fuori progetto | Confinamento di ogni hop, input e output; nessuna lettura locale da binding estero |
| Istruzioni ostili o segreti selezionati | L'agente seleziona/minimizza prima della cattura; nessuna esecuzione del testo. Nessun rilevatore automatico di segreti viene promesso |
| Corruzione o acquisizione interrotta | Digest e binding controllati, esclusività e retry; nessun claim pubblicato dall'acquisitore |
| Evidenza storica spacciata per corrente | Natura/state/prove separati; digest non certifica semantica; controlli di impatto F-063 |
| Regressioni di corpus/authority | ID e legacy invariati; import non promuove provenienza o appartenenza |

## Action Plan

1. Formato tipizzato e compatibilità: parser/check + casi legacy e transizioni.
2. Acquisizione e binding: cattura additiva, confini e idempotenza.
3. Proiezione evidenze: grafo condiviso, composizione CLI e chiusura export/import.
4. Estrarre procedure e template comuni, adattare i tre test KB e delimitare il triage
   nei metodi; distribuire nei quattro pacchetti. Verificare questo stato autonomo
   prima che F-063 consumi il contratto e aggiunga i trigger SDLC.
Incrementi implementati; test precedenti preservati. Risultati e limiti nel rapporto
`audit/reviews/TEST_software_knowledge_2026-10-04.md`.

## Test Strategy

Nuova batteria condivisa `scripts/test_software_knowledge.py`, import del motore reale,
fixture temporanee, nessuna rete. Usare nomi e risultati seguenti come accettazione:

| Gruppo | Prove richieste |
|---|---|
| E1 schema | Header8 invariato; header9 tipizzato; arità corta/lunga e kind ignoto rifiutati; ID invariato; schema2/header8 rifiutato; transizioni cross-kind rifiutate |
| E2 capture | CRLF/UTF8, span e limite16MiB; doppia cattura stessi byte/path; stesso estratto su file/versioni diverse; idempotenza; collisione/orfano/retry; UUID concorrente |
| E3 boundaries | `../`, assoluto, UNC, drive-relative, ADS, symlink/junction e special file; README/output link; nessun file esterno letto/scritto; file cambia durante cattura |
| E4 evidence | Dirty edit senza commit, delete/rename, input config/dipendenza, missing/unreadable; file test distinto da esito; vecchio schema UNTRACKED |
| E5 chain | Tre hop, AND con una premessa cambiata, OR con un sostegno indipendente nuovo, ciclo/dangling, superseded/contested non usabile; nessuna scrittura da check |
| E6 portability | Export porta tutte le premesse; import estero UNBOUND senza accesso ai suoi path; root non standard; clone stesso ID; corpus non software invariato |
| E7 distribution | CLI/seam marketing; quattro copie identiche; stato F-064 senza F-063 con link/ancore risolvibili, clausole comuni uniche e test KB preservati; installazione solo software completa, dev-only escluso dal pack |

Comandi di accettazione per ogni skill directory della mappa: `python -m unittest
discover -s scripts -p "test_*.py"`; a root e nelle tre distribuzioni `node --test
scripts/test_clients.js`; `npm pack --dry-run --json --ignore-scripts` confrontato con
allowlist e risorse richieste; drift guard nelle quattro copie. Test mirati prima delle
batterie complete. La verifica d'uso su Eclosion appartiene a F-063, non a questi assert.

## Current State

Design completato, review indipendente congiunta F-063/F-064 R2 PASS senza rilievi
residui. Rapporto: `audit/reviews/REVIEW_software_knowledge_design_2026-10-04.md`.
Motore e metodi comuni implementati e verificati prima dei trigger F-063. Review del
diff R1 FAIL, tre rilievi corretti, R2 PASS; tutte le batterie finali delle quattro
distribuzioni passano. Risultati, skip, packaging e limiti sono in
`audit/reviews/TEST_software_knowledge_2026-10-04.md`; conformance in
`audit/reviews/REVIEW_software_knowledge_code_2026-10-04.md`.
F-064 COMPLETED riguarda il contratto tecnico; F-063 resta IN_PROGRESS per FS7.

## Diary

- 2026-10-04: unità estratta da F-063 per il contratto condiviso; design richiesto
  dall'owner, baseline P1–P10 confermata. Review tecnica da registrare prima di consegnare.
- 2026-10-04: R1 ha rilevato il rinvio a procedure assegnate soltanto alla successiva
  F-063. Portate estrazione, rinvii e relativi test in questa unità; introdotta verifica
  dello stato intermedio e delimitato il triage incorporato nei metodi promossi.
- 2026-10-04: R2 PASS: confine F-064 autonomo e consumatori dottrinali verificati.
- 2026-10-04: owner autorizza applicazione e diff finale. Implementati schema tipizzato,
  cattura e diagnostica; test RED/GREEN nel harness. Promossi metodi e template comuni
  prima dei trigger F-063; una omissione nel naming CLI KB corretta senza ridurre test.
