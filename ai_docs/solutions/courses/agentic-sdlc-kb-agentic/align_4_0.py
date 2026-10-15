from revise_4_0 import ROOT,C,BASE,write,table,OBJECTIVES
import re
RISKS=[('C-1','Versione o citazione errata','Fonti riaperte e snapshot; controllo fattuale separato','Una nuova release può richiedere revisione'),('C-2','Prerequisito presunto dal ruolo','Definizioni prima dell’uso; grafo e diagnostica','Baseline reale non misurata'),('C-3','Sigle o esercizi al posto della spiegazione','Ragione causale e confronto concreto nel testo','La review non prova apprendimento umano'),('C-4','Accumulo letto come produttività garantita','Scenari condizionati, confronto equo e limiti','Beneficio non misurato sul team'),('C-5','Contaminazione o simulazione scambiata per prova umana','Sessioni distinte, accesso comparabile e limiti dichiarati','Isolamento dei reader solo per istruzioni'),('C-6','devPNT scambiato per requisito','Standalone completo e prodotto opzionale in S32','Nessun test di servizi esterni'),('C-7','Feedback diretto assente','D-IC not available; correzioni e riscontri in FEEDBACK_REPORT','Silenzio non prova comprensione'),('C-8','Persona addestrata a sostituire l’agente','Check su uscita del tool o richiesta della persona','Simulatore agente può avere competenze superiori'),('C-9','Perdita da compattazione','Richiesta e verifica del salvataggio prima della compattazione','Nessuna garanzia di continuità senza perdite'),('C-10','Riuso di conoscenza obsoleta','Distinguere storia e validità, dipendenti da rivedere','Recupero e manutenzione possono fallire')]
UCS=[('UC1','Motivare l’adozione e scegliere una cartella persistente; confronto con alternative','promessa1 e Expected Benefit'),('UC2','Giudicare fonte, ambito e conflitto riportati dall’agente','promessa2'),('UC3','Giudicare livello, proposta e chiusura della modifica, decidendo i punti riservati alla persona','promessa3'),('UC4','Distinguere contributi e modalità e spiegare valore cumulativo e ripresa','promesse4 e6'),('UC5','Chiedere sul proprio documento una risposta con fonte e una modifica solo ipotizzata e giudicarne i limiti','promessa5')]
ICS=[('IC1','COURSE_PLAN e SLIDE_CONTENT self-study','Lettura ordinata, spiegazioni visibili e soluzione dopo il tentativo'),('IC2','sources e riferimenti alle fonti','Fonte riapribile nello snapshot; esempi visibilmente inventati'),('IC3','Verifiche e soluzioni del testo','Giudizio della persona e correzione con rinvio alla spiegazione'),('IC4','Applicazione facoltativa S42','Documento accessibile non riservato, sola lettura, modifica soltanto ipotizzata; caso fittizio alternativo')]
analysis='''---
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
'''
analysis+='\n'.join(f'### {u} — {need}\nTraccia alla Vision: {tr}.\n' for u,need,tr in UCS)
analysis+='''
## Functional Spec
Fonte primaria SLIDE_CONTENT 4.0-content, slide-content-v1,42unità in7moduli. Prima difetti comuni e beneficio, poi meccanismi e prescrizioni. Storia degli ordini fittizi: chiave stabile riconosciuta dal fornitore, conferma incerta, notifica separata; il fix sbagliato crea una nuova chiave. Tutte le informazioni necessarie sono nel testo visibile. Check e soluzione separati; applicazione al proprio progetto facoltativa, nessuna modifica reale richiesta. Contesto mirato e frase dell’autore prima della compattazione insegnati come preparazione/verifica, non come garanzia o legge universale. Efficacia non verificata. Testi di moduli sono puntatori, non fonte concorrente; vecchioPPTX storico.

## Interface Contract
'''+ '\n'.join(f'### {i} — {surface}\nFlusso: {cond}. Dettaglio e feedback in D-IC.md; nessun servizio nuovo.\n' for i,surface,cond in ICS)
analysis+='''
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
'''+ '\n'.join(f'### {rid} — {vector}\nMitigazione: {mit}. Residuo: {res}.\n' for rid,vector,mit,res in RISKS)
analysis+='''
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
Storia precedente preservata in history_3_2/ANALYSIS_course_agentic-sdlc-kb-agentic.md. Il2026-10-04 l’autore richiede la correzione del corso secondo il report. Review design gpt-6-astra indipendente: FAIL con2BLOCK e3WARN; correzioni circoscritte UC5/IC4, identità dei rischi, causalità chiave, criterioO1 e claimbuilder; re-review PASS con tutti i finding ADDRESSED. Produzione4.0 eseguita; verifiche e review del risultato in corso, nessuna chiusura globale o efficacia dichiarata.
'''
(ROOT/'ai_docs/solutions/ANALYSIS_course_agentic-sdlc-kb-agentic.md').write_text(analysis,encoding='utf-8')
write('D-UC.md','# Destinatari e bisogni\n\nP1: persona del team software che usa agenti, sviluppatore o responsabile tecnico. Nessuna padronanza delle skill provata dal ruolo. I bisogni canonici e la traccia alla Vision sono in ANALYSIS C-001.\n\n'+table(['UC ID','Profile','Starting knowledge','Evidence','Need'],[[u,'P1','Uso ordinario dell’agente; concetti specifici da insegnare','Vision approvata e report autore; nessuna prova individuale',need] for u,need,tr in UCS]))
write('D-IC.md','# Interazione4.0\n\nVersione4.0-content. Markdown self-study accessibile senza installazioni; la persona legge, formula richieste e giudica uscite. Nessun invio automatico né raccolta riscontri.\n\n'+table(['Flow ID','Surface','Conditions','Feedback channel'],[[i,s,cond,'not available'] for i,s,cond in ICS])+'\n\nnot available significa nessun servizio diretto. Un riscontro spontaneo può essere registrato dall’autore in FEEDBACK_REPORT con versione/modulo. Nessuna assenza di feedback dimostra comprensione.')
write('P-TM.md','# Rischi didattici\n\nGli ID canonici e le mitigazioni sono in ANALYSIS C-001. Sono preservati C-1–C-7, aggiunti C-8–C-10 per questa revisione.\n\n'+table(['Risk ID','Vector','Mitigation','Residual'],RISKS))
write('FEEDBACK_REPORT.md','# Riscontri del proprietario\n\n2026-10-04: indicazioni raccolte nel REPORT_indicazioni_revisione_2026-10-04.md. Versione3.2: valore centrale troppo spostato sul giudizio; caso timeout troppo semplice per motivare patrimonio storico; necessarie obiezioni, contributo distill e preparazione della compattazione. Versione4.0: modifica obiettivi, apertura, caso evolutivo e ripresa; verifiche ancora in corso. Non sono risultati di apprendimento umano. DIAGNOSIS_metodo_2026-10-04.md distingue applicazione insufficiente da ipotesi di lacuna generalizzabile. Nessuna modifica a course-creator automaticamente autorizzata da un difetto del corso.')
write('simulation_4_0/TASKS.md','''# Compiti congelati4.0
P1: persona del team software che usa agenti; familiarità con le skill non accertata. Ruolo umano: richieste, giudizio di uscite e decisioni. Nessun tool/file/web consentito. Stesse condizioni per learner e controllo; dati fittizi autosufficienti.

## T1
In Selene si gestiscono prenotazioni. Una vecchia decisione separa prenotazione confermata e messaggio al cliente perché una mail fallita non deve prenotare due volte. Un nuovo baco lascia il pulsante bloccato; l’agente propone di ritentare l’intera operazione con un nuovo identificatore ogni volta e chiudere dopo un test sul pulsante. Hai la decisione e il contratto accessibili in file. Formula la risposta all’agente: cosa approvi o contesti, quali ragioni e prove chiedi, e perché una disciplina di conoscenza e cambiamento può aiutare. Non redigere il design al suo posto.

## T2
In Cobalto c’è una sola regola stabile con fonte e nota breve aggiornata; in Mira molte eccezioni e decisioni cambiate nel tempo. L’agente propone il medesimo percorso completo e lettura totale per entrambi. Poi, dopo aver trovato una causa ma lasciato la scelta aperta solo nella chat, propone di compattare subito e salvare più tardi. Formula la tua risposta e motiva l’adozione o l’alternativa. Non produrre handoff, claim o livello al posto dell’agente.
''')
write('simulation_4_0/CRITERIA.md','''# Criteri congelati prima dei tentativi
T1: contesta la chiusura sul pulsante, chiede contratto e motivo della separazione, verifica stesso identificatore/operazione ed esiti reali, motiva il riuso della storia senza farne prova automatica. Insufficiente: testverdi=chiusura o piùdocumenti=sicurezza; nessun credito per produrre codice/design.
T2: giudica proporzione e alternativa sufficiente nel caso stabile, selezione invece di lettura totale, manutenzione e limiti nel caso evolutivo, salvataggio verificabile prima della compattazione, distingue causa trovata e decisione aperta. Insufficiente: skillsempreobbligatorie oppure nessun costo; nessun credito per compilareartefatti al posto dell’agente.
Per ogni criterio: evidenza citata dal tentativo, presente/assente/incerta; nessun voto aggregato inventato. Controllo già capace rende beneficio didattico inconclusivo.
''')
write('SIMULATION_REPORT.md','''# Diagnostica4.0-content
Status: pending
Efficacy: efficacy not verified

Fonte4.0 hash in simulation_4_0/source_hash.json; compiti e criteri congelati prima delle sessioni in TASKS.md/CRITERIA.md. Vecchie simulazioni preservate in history_3_2; non sono evidenza della nuova versione.
Sono previsti lettore P1 con prefissoS01–S06 incrementale, poi packet senza soluzioni per trasferimento, controllo fresco senza corso, reviewer indipendente. Copertura sequenziale limitata al prefisso: il resto non verrà dichiarato verificato progressivamente. Restrizioni di accesso per istruzioni, non isolamento tecnico. Riflessioni intermedie possono aiutare la risposta; confronto non prova apprendimento umano o causalità.
''')
