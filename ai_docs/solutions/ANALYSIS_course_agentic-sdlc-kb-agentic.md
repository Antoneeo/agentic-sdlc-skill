---
id: C-001
feature: Corso su kb-agentic e agentic-sdlc
domain: course
level: L3
status: IN_PROGRESS
start_date: 2026-09-27
end_date:
---
# Course Analysis: kb-agentic e agentic-sdlc

## Objective
Spiegare perché le due skill, con distill come supporto alla comunicazione, trasformano lavoro disperso in patrimonio durevole e verificabile; insegnare alla persona a giudicarne beneficio, costo e uso, poi i meccanismi e le prescrizioni. Revisione4.0 richiesta da Antonio il2026-10-04, non nuovo corso o pubblico.

## Feature Vision
Autorità: ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md APPROVED. Serviti Expected Benefit e promesse1–6. Nessun emendamento: review indipendente conferma why-first, supporto distill e compattazione preparata nel perimetro della continuità. Le indicazioni dell’autore sono nel REPORT_indicazioni_revisione_2026-10-04.md. Elicitazione aggiuntiva omessa: richieste e vincoli sono già espliciti nella conversazione e nel report.

## Use Cases / User Needs
P1 è la persona sviluppatrice o responsabile tecnico che lavora con agenti. kb-agentic, agentic-sdlc, distill, ai_docs e devPNT sono EXISTS; Orione e gli altri casi sono NEW fittizi; agente ingegnere è METAPHOR, non promessa di riaddestramento.
### UC1 — Motivare l’adozione e scegliere una cartella persistente; confronto con alternative
Traccia alla Vision: promessa1 e Expected Benefit.

### UC2 — Giudicare fonte, ambito e conflitto riportati dall’agente
Traccia alla Vision: promessa2.

### UC3 — Giudicare livello, proposta e chiusura della modifica, decidendo i punti riservati alla persona
Traccia alla Vision: promessa3.

### UC4 — Distinguere contributi e modalità e spiegare valore cumulativo e ripresa
Traccia alla Vision: promesse4 e6.

### UC5 — Chiedere sul proprio documento una risposta con fonte e una modifica solo ipotizzata e giudicarne i limiti
Traccia alla Vision: promessa5.

## Functional Spec
Fonte primaria SLIDE_CONTENT 4.0-content, slide-content-v1,42unità in7moduli. Prima difetti comuni e beneficio, poi meccanismi e prescrizioni. Storia degli ordini fittizi: chiave stabile riconosciuta dal fornitore, conferma incerta, notifica separata; il fix sbagliato crea una nuova chiave. Tutte le informazioni necessarie sono nel testo visibile. Check e soluzione separati; applicazione al proprio progetto facoltativa, nessuna modifica reale richiesta. Contesto mirato e frase dell’autore prima della compattazione insegnati come preparazione/verifica, non come garanzia o legge universale. Efficacia non verificata. Testi di moduli sono puntatori, non fonte concorrente; vecchioPPTX storico.

## Interface Contract
### IC1 — COURSE_PLAN e SLIDE_CONTENT self-study
Flusso: Lettura ordinata, spiegazioni visibili e soluzione dopo il tentativo. Dettaglio e feedback in D-IC.md; nessun servizio nuovo.

### IC2 — sources e riferimenti alle fonti
Flusso: Fonte riapribile nello snapshot; esempi visibilmente inventati. Dettaglio e feedback in D-IC.md; nessun servizio nuovo.

### IC3 — Verifiche e soluzioni del testo
Flusso: Giudizio della persona e correzione con rinvio alla spiegazione. Dettaglio e feedback in D-IC.md; nessun servizio nuovo.

### IC4 — Applicazione facoltativa S42
Flusso: Documento accessibile non riservato, sola lettura, modifica soltanto ipotizzata; caso fittizio alternativo. Dettaglio e feedback in D-IC.md; nessun servizio nuovo.

## Capability Ledger
| Capability | Existing or missing | Evidence and consequence |
|---|---|---|
| Fonte completa e grafo | EXISTS | distributions/course-creator/skills/course-creator/slide_content.md e learning_design.md; riusare schema e rubric |
| Controlli strutturali | EXISTS | distributions/course-creator/skills/course-creator/scripts/course_check.py; non certificano qualità didattica |
| Reader/reviewer distinti | EXISTS | Strumento collaboration disponibile; contesti freschi e limiti per istruzioni |
| Nuovo packet | INADEQUATE | simulation_3_1/packet contiene vecchia versione; nuovo estratto verificabile in simulation_4_0 |

## Impact
Il piano per ogni file è in DESIGN_revisione_4_0.md, già sottoposto a review indipendente. Nessun codice runtime, Vision o PPTX modificato. revise_4_0.py e align_4_0.py sono record di produzione interni: testo esplicito, archiviazione della versione precedente, snapshot e derivati. Non sono strumenti distribuiti e non certificano semantica. Fonti per distill preservate nello snapshot, non nuova dipendenza di installazione.

## Learning and Content Risks
### C-1 — Versione o citazione errata
Mitigazione: Fonti riaperte e snapshot; controllo fattuale separato. Residuo: Una nuova release può richiedere revisione.

### C-2 — Prerequisito presunto dal ruolo
Mitigazione: Definizioni prima dell’uso; grafo e diagnostica. Residuo: Baseline reale non misurata.

### C-3 — Sigle o esercizi al posto della spiegazione
Mitigazione: Ragione causale e confronto concreto nel testo. Residuo: La review non prova apprendimento umano.

### C-4 — Accumulo letto come produttività garantita
Mitigazione: Scenari condizionati, confronto equo e limiti. Residuo: Beneficio non misurato sul team.

### C-5 — Contaminazione o simulazione scambiata per prova umana
Mitigazione: Sessioni distinte, accesso comparabile e limiti dichiarati. Residuo: Isolamento dei reader solo per istruzioni.

### C-6 — devPNT scambiato per requisito
Mitigazione: Standalone completo e prodotto opzionale in S32. Residuo: Nessun test di servizi esterni.

### C-7 — Feedback diretto assente
Mitigazione: D-IC not available; correzioni e riscontri in FEEDBACK_REPORT. Residuo: Silenzio non prova comprensione.

### C-8 — Persona addestrata a sostituire l’agente
Mitigazione: Check su uscita del tool o richiesta della persona. Residuo: Simulatore agente può avere competenze superiori.

### C-9 — Perdita da compattazione
Mitigazione: Richiesta e verifica del salvataggio prima della compattazione. Residuo: Nessuna garanzia di continuità senza perdite.

### C-10 — Riuso di conoscenza obsoleta
Mitigazione: Distinguere storia e validità, dipendenti da rivedere. Residuo: Recupero e manutenzione possono fallire.

## Action Plan
1. Orientamento e confronto con Vision e indicazioni.
2. Design e review indipendente prima della produzione.
3. Archivio3.2, testo4.0, piano, grafo, fonti e contratti aggiornati.
4. Verifica struttura, fonte, lettura progressiva del prefisso e trasferimento con controllo.
5. Review didattica/diff indipendente, correzioni e riesame proporzionato.
6. Indici e gate, handoff; consegnare testo per lettura dell’autore. Nessun nuovo PPTX finché testo da verificare.

## Test Strategy
Gate course e repository, hash snapshot, metadata e rinvii; validazione meccanica distinta dalla review semantica. Reader P1: prefisso iniziale incrementale poi packet senza soluzioni per trasferimento; dichiarare la copertura campionata. Controllo senza corso: medesimi compiti, fonti esterne e permessi. Criteri congelati prima degli esiti. Reviewer separato applica learning_design.md e fonte; nessuna misura di apprendimento umano o superiorità causale. Consultare SIMULATION_REPORT per esiti effettivi, non desumerli dal piano.

## Diary / Current State
Storia precedente preservata in history_3_2/ANALYSIS_course_agentic-sdlc-kb-agentic.md. Il2026-10-04 l’autore richiede la correzione del corso secondo il report. Review design gpt-6-astra indipendente: FAIL con2BLOCK e3WARN, poi PASS dopo correzioni UC5/IC4, rischi, causalità, criterioO1 e builder. Review materiale: grafo e distinzioni promesse corretti, citazioni e baseline precisate; PASS finale su materiale, conformance e diagnosi. Gate course:0errori/0warning. Tentativi e limiti in SIMULATION_REPORT e simulation_4_0/REVIEW.md: controllo già capace, nessun beneficio causale dimostrato. Il2026-10-05 Antonio richiede le slide: consegnato PPTX4.0 con43slide, contenuti visibili integrali e note del relatore distinte. Verifica package/layout/import, confronto testo/fonti e ispezione di tutte43slide superati; PowerPoint nativo non eseguito. Evidenze in presentations/course-creator-session/work/ppt-4.0/. C-001 resta IN_PROGRESS per riscontri dell’autore. Nessun commit, pubblicazione o nuova regola di course-creator.
