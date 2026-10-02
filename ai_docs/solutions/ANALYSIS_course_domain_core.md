---
id: F-059
feature: Profilo course nel validatore condiviso
status: COMPLETED
level: L3
start_date: 2026-09-26
end_date: 2026-09-27
---
# Analisi: profilo course nel core

## Objective
Registrare `domain: course` nel core condiviso, prima che F-058 spedisca la skill `course-creator`. Questo componente è una unità separata: il contratto del dominio è consumato da tutte le lenti che invocano il validatore del core e può essere distribuito prima della nuova skill. Non integra ancora gli entry point specialistici né valida il grafo dei prerequisiti o gli artefatti di un singolo corso; quelli appartengono a F-058.

## Feature Vision
Autorità: `ai_docs/vision/project_vision.md` (APPROVED) e `ai_docs/vision/features/VISION_course_creator.md` (APPROVED). Il beneficio servito è riconoscere il proprietario didattico e applicarne il rischio nel core comune, senza chiedere a un documento didattico il rischio di un documento software, KB o marketing. Il dominio course ha un proprietario; importare controlli di altre lenti può aggiungere findings, mai togliere quelli propri. La parità fra gli entry point resta da realizzare e verificare in F-058.

## Use Cases / User Needs
`domain: course` è **NEW**; `ai_docs/`, `domain:` e i tre domini attuali sono **EXISTS**.

| ID | Attore della Vision di progetto | Bisogno | Beneficio |
|---|---|---|---|
| UC1 | Practitioner in a non-code domain | Validare un'analisi didattica con il rischio del proprio dominio tramite il core condiviso | Metodo fedele al dominio |
| UC2 | Team lead needing governance | Ottenere dal core lo stesso verdetto e indice per un albero misto, indipendentemente dalla copia del core | Un'unica autorità documentale |
| UC3 | Solo developer using an AI agent | Non cambiare il verdetto dei progetti senza dichiarazione course | Compatibilità e costo proporzionato |

## Functional Spec
1. Un documento con `domain: course`, o un progetto con `default_domain: course`, è riconosciuto come course; non emette più il warning «domain not recognized» e richiede `## Learning and Content Risks`. La mancanza di quella sezione è errore.
2. Documenti code, knowledge e marketing mantengono le proprie sezioni di rischio e il proprio verdetto. Un dominio davvero sconosciuto mantiene il fallback visibile al default del progetto.
3. Il profilo dichiara `C-` come prefisso convenzionale degli ID; l'unicità è verificata entro il dominio, senza nuova imposizione del prefisso. L'indice delle analisi prodotto dal core espone course come dominio quando un artefatto dichiara una lente; le tre copie del core producono gli stessi byte a parità di input. Questo non afferma parità con l'indice specialistico di marketing.
4. Nessun artefatto course o controllo sui grafi viene introdotto dal core: il componente registra la categoria e il rischio obbligatorio, e conserva la composizione dei controlli portabili esistenti. Le istruzioni di authoring (`templates.md`) e la pubblicazione del dominio agli utenti appartengono a F-058; F-059 prepara il contratto interno prima del rilascio della skill.

## Interface Contract
L'attore invoca `cmd_validate` o `build_index` del core contro il singolo albero `ai_docs/`, direttamente o attraverso un entry point che li compone già. Il flusso resta core → risoluzione del dominio del documento → regola di rischio → risultato e indice esistenti. Il nuovo input è `domain: course` o il default di progetto; il feedback mostra il rischio mancante come errore e un dominio sconosciuto come warning. `mkt_check.py` oggi usa un proprio `run_validate` e un proprio `cmd_index`: integrarli è compito di F-058. Nessun nuovo comando, servizio o schermata in F-059.

## Capability Ledger
`ai_docs/strategic/architecture.md` identifica il core e il drift guard. Prova eseguita: `python ai_docs/solutions/harness_course_domain_core/probe.py --expect before` PASS, `--expect after` FAIL; oggi un default course torna code e `resolve_domain` marca course sconosciuto. Il probe isola il fatto comportamentale da cui dipende il design.

| Capacità | Verdetto | Contratto e prova |
|---|---|---|
| Risolvere il proprietario documentale course | INADEQUATE | `sdlc_core.py#DOMAINS`, `#project_default_domain`, `#resolve_domain`: tre domini registrati, course assente; aggiunta nel registro condiviso |
| Applicare un rischio specifico per dominio | EXISTS | `sdlc_core.py#cmd_validate` usa `DOMAINS[domain][risk_section]`; il nuovo profilo entra nello stesso flusso |
| Verificare l'identità delle copie | EXISTS | `shared_files.py#SHARED_FILES` e `shared_manifest.json` sorvegliano core e batteria in ogni distribuzione |

## Impact
Nessuna firma pubblica cambia. In ogni riga C/K/M si intendono **tre percorsi distinti**: C=`skills/agentic-sdlc-skill`, K=`distributions/kb-agentic-skill/skills/kb-agentic-skill`, M=`distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc`.

| Percorsi | Modifica | Responsabilità |
|---|---|---|
| C/K/M `scripts/sdlc_core.py` | MODIFY `DOMAINS` | Registrare course, `C-`, rischio didattico; `project_default_domain(root)`, `resolve_domain(meta, default)` e `cmd_validate(root, strict=False, hybrid=False)` mantengono le firme |
| C/K/M `scripts/test_domain_rules.py` | MODIFY test di mixed tree e rischio | Provare le quattro lenti, il rischio course, gli ID e la compatibilità legacy |
| C/K/M `scripts/shared_manifest.json` | GENERATE | Registrare hash identici del core e della batteria condivisa |
| `ai_docs/solutions/harness_course_domain_core/probe.py` | ADD | Confronto eseguibile prima/dopo sul fatto portante |

Blast radius enumerato con `rg -n` su `skills/`, `scripts/`, `distributions/` (`*.py`, `*.js`): in ciascuna delle tre copie core, `project_default_domain` e `resolve_domain` sono chiamate da `build_index` e `cmd_validate`; `DOMAINS` è letto dalle due risoluzioni, da `cmd_validate` e da `test_skill_invariants.py`. `cmd_validate` è chiamato da `cmd_check` e `main` nel core, da `knowledge.py#kb_cmd_validate`, e dalle batterie `test_domain_rules.py`, `test_merge_safety.py`, `test_plan.py`, `test_session_start.py`, `test_skill_invariants.py` in C/K/M. `mkt_check.py#run_validate` e `#cmd_index` restano entry point specialistici distinti, da integrare in F-058. Non è disponibile un indice semantico di questo repository: la ricerca testuale è la copertura dichiarata, da ricontrollare in review. Le firme restano uguali e nessun consumatore richiede una modifica di chiamata. Popolazioni a riposo: un progetto già contenente `domain: course` passa da warning+regole code a regole course; un progetto che introduce `default_domain: course` trasferisce anche le analisi senza dichiarazione esplicita al nuovo regime. Nessuna migrazione automatica; il nuovo errore di rischio assente è intenzionale e spiegato nel rilascio. Documenti senza dichiarazione e senza default di progetto restano code.

## Security and Threat Model
Il cambiamento interpreta solo frontmatter locale: nessun nuovo I/O, rete o dato personale. Rischi: fallback silenzioso a code per course, deriva fra copie del core, nuova regola che contamina domini storici. Mitigazioni: test del fallback e del rischio per ciascun dominio; drift guard su tre copie; prova RED/GREEN dell'input course. Un file con dominio sconosciuto continua a produrre warning, senza falsa convalida course.

## Action Plan
- [x] Riprodurre il comportamento attuale e il risultato desiderato in un probe che fallisce oggi.
- [x] Review indipendente del design (PASS); risultato F-059 approvato dal proprietario il 2026-09-27.
- [x] Implementare il profilo nei tre core e la batteria condivisa; rigenerare i manifest.
- [x] Eseguire probe, batterie di dominio, drift e verifica delle tre copie del core; la parità dell'entry point marketing resta in F-058.
- [x] Review indipendente del diff (PASS al secondo round, 2026-09-27); documentazione architetturale aggiornata e F-059 chiusa prima di F-058.

## Test Strategy
Il probe deve invertire il proprio risultato (`--expect before` verde oggi, `--expect after` rosso oggi e verde dopo). La batteria prova dominio course dichiarato/default, rischio mancante/presente, prefisso convenzionale `C-` nel profilo, unicità degli ID entro course, indice uguale fra copie del core, tre domini esistenti e unknown fallback. Il drift guard verifica gli hash delle tre copie. I test su un corpus storico senza `domain:` né default course non devono cambiare output. La parità degli entry point, incluso marketing, è un criterio di F-058.

## Diary / Current State
2026-09-26: unità separata da F-058 per contratto condiviso e più consumatori. Probe iniziale: before PASS, after FAIL. La review indipendente ha trovato che `mkt_check.py` sostituisce `validate` e `index`: le affermazioni di parità tra entry point sono state tolte da F-059 e assegnate a F-058. Nessuna modifica al core ancora eseguita.

2026-09-27: implementazione avviata sul branch `codex/course-creator`. RED: probe `--expect after` fallito e quattro test course della batteria falliti; GREEN: probe e 19/19 test in ciascuna delle tre distribuzioni. Copie e manifest condivisi aggiornati; `shared_files.py` conferma 22/22 file identici, `test_skill_invariants.py` 64/64. Review indipendente del diff richiesta, non ancora conclusa. La parità dell'entry point marketing è ancora responsabilità F-058.

2026-09-27: review indipendente del diff PASS con un WARN sui test diretti di unicità ID e visibilità nell'indice course. Aggiunti i due test, ricopiati nelle tre distribuzioni; re-review PASS senza finding aperti. Le tre batterie sono ora 21/21 ciascuna, probe GREEN, regressione golden 6/6 e drift 22/22. La documentazione derivata e la chiusura restano da completare.

2026-09-27: il proprietario ha approvato F-059. Aggiornata la mappa del core in `ai_docs/strategic/architecture.md`; nessun ADR nuovo, perché la registrazione course segue il registro DOMAINS esistente senza introdurre pattern o dipendenze. F-059 chiusa; F-058 resta proprietaria del validatore didattico, dell'entry point marketing e della pubblicazione della quarta distribuzione.
