"""Expand the author-selected F-063/F-064 file plan; writes only design evidence."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "ai_docs/solutions/DESIGN_software_knowledge_files.md"
DISTS = (
    ("skills/agentic-sdlc-skill", "package.json", "scripts/sdlc_check.py"),
    ("distributions/kb-agentic-skill/skills/kb-agentic-skill", "distributions/kb-agentic-skill/package.json", "scripts/sdlc_check.py"),
    ("distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc", "distributions/mkt-agentic-sdlc/package.json", "scripts/mkt_check.py"),
    ("distributions/course-creator/skills/course-creator", "distributions/course-creator/package.json", "scripts/sdlc_check.py"),
)
plan = []


def add(path, unit, change):
    action = "MODIFY" if (ROOT / path).is_file() else "ADD"
    plan.append((path, action, unit, change))


for dist, package, entry in DISTS:
    add(dist + "/scripts/knowledge.py", "KB", "F-064: firme nella tabella del motore; parser tipizzato, capture-source/evidence, grafo derivazioni, controlli, export/import. Copia comune identica.")
    add(dist + "/scripts/test_software_knowledge.py", "KB+SDLC", "Nuova batteria SoftwareEvidenceTests(unittest.TestCase): E1–E7 F-064; trigger e confezionamento F-063. Solo sviluppo, non pubblicata.")
    add(dist + "/scripts/shared_files.py", "KB", "SHARED_FILES: aggiungere i cinque metodi/template comuni e scripts/test_software_knowledge.py. Nessuna firma modificata.")
    add(dist + "/scripts/shared_manifest.json", "KB+SDLC", "Rigenerare con shared_files.py --update dopo la sincronizzazione; nessuna modifica manuale.")
    add(dist + "/memory.md", "KB+SDLC", "F-064: estrarre recall/capture/revision comuni dal SKILL KB, con ancore risolvibili e stati del motore. Poi F-063: aggiungere trigger SDLC e distinzione cattura interna/corpus indipendente.")
    add(dist + "/routing.md", "KB+SDLC", "F-064: i metodi comuni non importano il triage KB nelle altre lenti; §3 e tabella lenti restano autorità. Poi F-063: cattura pertinente conserva owner code; bulk intake/ristrutturazione distinti.")
    add(dist + "/guides.md", "SDLC", "Comprensione: guida può rinviare a claim e relative prove; mantenere ancoraggio al codice, lettura delle fonti e proprietà da preservare.")
    add(dist + "/review.md", "SDLC", "Nel gate esistente verificare natura, catena/condizioni, conoscenza interessata e capture delta; nessun nuovo gate, verdetto o campo del log.")
    add(dist + "/distillation.md", "KB", "Promuovere sorgente KB; §1 cattura F-064, §2 kind opzionale; AND derivazione/OR corroborazione; template comuni. §3: L3 document-set si applica a incarichi KB; altre lenti conservano il proprio triage.")
    add(dist + "/taxonomy.md", "KB+SDLC", "F-064: promuovere sorgente KB, recall in memory.md; §4 L3 gerarchia vale per incarichi KB, altri classificati dal proprio owner. Poi F-063: foglie interne; radici/re-parenting espliciti, nessun board.")
    add(dist + "/reconciliation.md", "KB", "Promuovere sorgente KB; verificare natura prima di conflitto/supersessione; stessa provenienza/storia; cascata cita Revision comune in memory.md.")
    add(dist + "/portability.md", "KB", "Promuovere sorgente KB; closure derived_from, binding UNBOUND e stessa autorità importata. §5: livelli import/export specifici KB; nelle altre lenti classificazione del router/owner, input esterno mai L1.")
    add(dist + "/knowledge-templates.md", "KB", "Estrarre topic/sidecar/ruling da templates.md KB, con tabella schema2 e binding F-064. Unica definizione del formato comune, non nuovo storage.")
    add(package, "KB", "files[] include i cinque nuovi supporti nella skill di questo pacchetto; test/harness/evals restano esclusi. Nessun bump o publish in questo lavoro.")
    if "mkt-agentic" in dist:
        add(dist + "/" + entry, "KB", "set_profile support_files: cinque supporti; main(argv=None): passa project=root a kb_validate_surface; help nomina nuove CLI. Altri runner e formule invariati.")
    else:
        add(dist + "/" + entry, "KB", "set_profile support_files: aggiungere i nuovi supporti mancanti; main(argv=None) mantiene forwarding e composizione attuali, senza nuova autorità.")
    if dist.startswith("skills/"):
        add(dist + "/SKILL.md", "KB+SDLC", "F-064: support list e lettura su trigger dei metodi comuni. Poi F-063: fasi 1/3/4/5 richiamano trigger SDLC; niente nuovo triage o domanda di chiusura.")
    elif "kb-agentic-skill" in dist:
        add(dist + "/SKILL.md", "KB", "F-064: ancore Topic Recall/Capture Moment/Revision rinviano a memory.md; conservare trigger/domande specifici KB. Support list e Mechanical Enforcement nominano nuove risorse/CLI.")
    else:
        add(dist + "/SKILL.md", "KB", "Elenco delle risorse KB comuni e loro lettura su trigger, affinché i supporti spediti siano raggiungibili. Nessun nuovo workflow software per questa lente.")

add("skills/agentic-sdlc-skill/architect.md", "SDLC", "§2: usare topic/proprietà nell'orientamento; Component Map e verifica dei simboli restano autoritativi per l'impatto.")
add("skills/agentic-sdlc-skill/templates.md", "SDLC", "Commenti Impact/Test Strategy/Current State: citare claim riusati/aggiornati e limiti solo se pertinenti; nessuna nuova sezione obbligatoria.")
add("distributions/kb-agentic-skill/skills/kb-agentic-skill/templates.md", "KB", "Sostituire le tre sezioni comuni topic/sidecar/ruling con rinvio a knowledge-templates.md; template di Vision/ANALYSIS/PLAN invariati.")
kbtests = "distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/"
add(kbtests + "test_kb_revision.py", "KB", "RevisionDoctrineTests.setUp/test_seven_load_bearing_anchors/test_exemption_anchors(self): leggere clausole comuni da memory.md; test_section_exists e due pointer test verificano SKILL→memory. Conservare test_canonical_clause_appears_exactly_once_across_the_skill_dir(self), ledger/Diary/tombstone e no re-parent. normalized(path)/canonical_count(text) invariati.")
add(kbtests + "test_kb_recall.py", "KB", "TestRecallDoctrine.test_skill_md_carries_the_recall_section(self): separare clausole comuni in memory.md e trigger/ancora SKILL; test_the_verdict_form_admits_every_branch_the_descent_opened(self) legge il proprietario memory. Altri test taxonomy/description e TestOrientTopicRouter invariati; nessuna garanzia rimossa.")
add(kbtests + "test_kb_capture.py", "KB", "TestCaptureDoctrine.test_skill_md_carries_the_capture_section(self): verificare provenienza/idempotenza/riconciliazione in memory.md, domanda e closing firmato in SKILL, più rinvio risolvibile. Write Triggers e TestNotesRecency invariati. Metodi mantengono (self), normalized(path) invariato.")
for name in ("software_knowledge_eclosion", "software_knowledge_first_capture", "software_knowledge_change", "software_knowledge_l1"):
    add("skills/agentic-sdlc-skill/evals/scenarios/" + name + ".md", "SDLC", "Scenario dev-only con Setup/Prompt/Pass criteria per il driver esistente; casi e rubrica F-063, nessun runner o test di efficacia inventato.")
add("ai_docs/reference/GUIDE_shared_project_memory.md", "closure", "Aggiornare la guida al motore effettivamente implementato, nuovi riferimenti e limiti; non presentare il design come CURRENT prima del codice.")
add("ai_docs/reference/.sources/shared-project-memory-software-evidence.md", "closure", "Nuovo snapshot degli estratti di codice implementato per la guida; preservare lo snapshot precedente.")
add("ai_docs/strategic/architecture.md", "closure", "Aggiornare Component Map dei proprietari già esistenti e i contratti estesi.")
for readme in ("README.md", "distributions/kb-agentic-skill/README.md", "distributions/mkt-agentic-sdlc/README.md", "distributions/course-creator/README.md"):
    add(readme, "closure", "Alla chiusura F-064 allineare supporti distribuiti, Runtime Shape/comandi dove presenti e limiti del nuovo motore; alla chiusura F-063 descrivere solo il raccordo pertinente alla lente. Nessuna capacità futura presentata come esistente.")
add("ai_docs/strategic/skill_family_agent_workflows.md", "closure", "Alla chiusura di ciascuna unità riallineare metodi ora comuni, proprietà del triage e comportamenti effettivamente implementati; richiesta esplicita di audit_plan prima del mark sulle aree di prodotto.")
add("ai_docs/architecture/ADR_2026-10-04_software_knowledge.md", "closure", "Registrare decisione effettivamente accettata: stesso motore/grafo, formato compatibile e vincoli. Non è scritto né dichiarato Accepted dal design.")

inv = json.loads((ROOT / "ai_docs/solutions/harness_software_knowledge/design_inventory.json").read_text(encoding="utf-8-sig"))
lines = ["# F-063 / F-064 — Mappa dei file e dei consumatori", "",
         "Per implementatore e reviewer. Proposta di impatto del prodotto, non un diff implementato.",
         "Autorità: ANALYSIS_software_knowledge.md (unità SDLC) e ANALYSIS_kb_evidence.md (unità KB).",
         "Le copie condivise si modificano da un solo testo e si sincronizzano; ogni percorso è esplicito.",
         "La colonna closure riguarda documentazione da aggiornare dopo l'implementazione.", "",
         "## Module Change Plan", "", "| Path | Change | Unità | Modifica e ragione |", "|---|---|---|---|"]
for row in sorted(plan):
    lines.append("| `%s` | %s | %s | %s |" % row)
lines += ["", "## Blast radius osservato", "",
          "Enumeratore primario: AST Python per Name/Attribute, definizioni e contesto del chiamante;",
          "coverage: 108 file Python, zero parse failure. Probe testuale: 362 file di prodotto",
          "(.py/.js/.json/.md in skills/distributions/scripts) più 21 harness Python sotto ai_docs.",
          "Il JSON `harness_software_knowledge/design_inventory.json` contiene OGNI riferimento",
          "path + consumer + posizione, i re-export, il delta testuale e gli hash degli input.",
          "Le posizioni servono a riaprire l'evidenza; l'identità è path::simbolo, non il numero di riga.",
          "Per le API Python, tutti i delta sono definizioni, commenti, docstring o messaggi assert; nessun chiamante",
          "eseguibile aggiuntivo. `knowledge.main` ha cinque call site in quattro entry point.",
          "Il re-export `from knowledge import *` nel client KB è considerato: i suoi test chiamano kc.kb_*.",
          "Limite dichiarato: non è un LSP globale; reflection arbitraria e file esclusi da rg non sono",
          "certificati assenti. Lo strumento devPNT punta a un altro progetto ed è inapplicabile.", "",
          "| Simbolo | Riferimenti AST | Delta testuale | Rischio se ignorato |", "|---|---:|---:|---|"]
risks = {
    "CLAIM_COLUMNS": "Rottura della tabella legacy o arità incoerente.",
    "kb_parse_claims": "Riempimento ID, coverage, timeline, import e test potrebbero leggere righe differenti.",
    "kb_check_claims": "Graph e test potrebbero non vedere natura/transizioni o cambiare return.",
    "kb_corpus_check": "Sidecar nuove potrebbero bypassare integrità o rompere fonti legacy.",
    "kb_time_cycle": "Estrazione del grafo potrebbe mutare catene, ordine o chiavi dei rapporti esistenti.",
    "kb_export_closure": "Bundle privo delle premesse o dei partner del conflitto.",
    "kb_import_plan": "Errori di parsing ignorati o binding estero adottato implicitamente.",
    "kb_validate_surface": "Marketing potrebbe non passare project root e perdere la riverifica locale.",
    "SHARED_FILES": "Copie/promozioni non controllate o manifest incompleto.",
    "knowledge.main": "Una lente potrebbe non raggiungere i nuovi comandi.",
}
for symbol in inv["ast_references"]:
    lines.append("| `%s` | %d | %d | %s |" % (symbol, len(inv["ast_references"][symbol]),
        len(inv["text_only_delta"][symbol]), risks.get(symbol, "Dispatch o composizione dei controlli incoerente.")))
planned = {p[0] for p in plan}
consumer_files = {}
for symbol, refs in inv["ast_references"].items():
    for ref in refs:
        consumer_files.setdefault(ref["path"], set()).add(symbol)
lines += ["", "## Consumatori verificati senza edit previsto", "",
          "Restano nel perimetro di regressione; non sono omessi perché non richiedono una patch.",
          "Il set delle funzioni chiamanti è nel JSON, non ridotto a un campione.", "",
          "| Path | Simboli consumati | Azione |", "|---|---|---|"]
for path, symbols in sorted(consumer_files.items()):
    if path not in planned:
        action = "Rieseguire regressioni; mantenere contratto." if not path.startswith("ai_docs/") else "Evidenza storica: P4/P5/P6/P9 caratterizzano il vecchio comportamento; non cambiare gli assert per mascherare il delta, fissare nuova baseline separata."
        lines.append("| `%s` | %s | %s |" % (path, ", ".join("`" + s + "`" for s in sorted(symbols)), action))
lines += ["", "## Altri consumatori di contratto", "",
          "- `doctrine_text_references` nel JSON enumera separatamente tutte le corrispondenze alle clausole/ancore trasferite e alle classi dei test sulla medesima popolazione: produttori, rinvii e assert. Il call graph Python non copre questo contratto testuale; sinonimi non cercati non sono certificati assenti.",
          "- I tre test KB revision/recall/capture sono ora nel Module Change Plan. Si cambia il proprietario letto, non si indeboliscono clausole, esclusioni o unicità canonica. I controlli comuni vengono anche nella batteria condivisa E7; i tre moduli rimangono locali per i trigger KB.",
          "- Il probe dottrinale restituisce 39 righe: oltre ai file da modificare, i CHANGELOG KB/marketing sono storia da preservare; elicitation.md KB/corso cita il closing specifico KB, la cui ancora resta; test_kb_remind.py controlla il payload inline e resta invariato; harness_question_discipline/probe.py conserva il timing specifico KB. Rieseguire questi ultimi due senza cambiarne gli assert. Le quattro docstring knowledge.py richiamano l'ancora di recall conservata nel client KB.",
          "- `scripts/lib.js` e le tre copie delle distribuzioni: `TEMPLATES_PATH` continua a leggere il template della lente; il seeding non usa i tre template KB estratti. `lensTable()` continua a leggere la stessa tabella in routing.md.",
          "- `scripts/postinstall.js` e le tre copie: `installSkill(client)` copia SKILL_SOURCE; l'allowlist package.json deve includere tutti i nuovi supporti. Nessuna modifica al deployer.",
          "- `scripts/test_clients.js` e le tre copie: test TS7 packaging e install round-trip, da rieseguire in ogni package.",
          "- `scripts/test_skill_invariants.py` nelle quattro skill: il profilo e SKILL.md devono elencare ogni supporto; nessuna eccezione al test per rendere verde una distribuzione incompleta.",
          "- `evals/run_behavioral.py` del software: `load_scenario(path)`, `seed(scenario, dest)` e `main(argv)` da verificare contro gli scenari aggiunti; nessuna modifica al driver.", "",
          "## Stato intermedio obbligatorio", "",
          "Applicare prima tutte le modifiche KB e soltanto la parte F-064 delle righe KB+SDLC.",
          "Prima di F-063, ogni link/ancora dei metodi promossi deve risolversi, profile/SKILL/pack",
          "devono includere le risorse e le batterie delle quattro lenti devono passare. Nessun",
          "riferimento può richiedere un trigger SDLC ancora da implementare. Ripetere la verifica",
          "dopo F-063. Cattura interna a lavoro software già classificato: nessuna seconda",
          "ANALYSIS né riclassificazione KB; verifica comportamentale in software_knowledge_first_capture.", "",
          "## Artefatti di questa consegna", "",
          "I due ANALYSIS, questa mappa, harness/inventario/snapshot, handoff e review sono la consegna",
          "di design. Indici generati e audit_plan registrano solo questi documenti. Nel futuro diff",
          "di implementazione viaggeranno anche stato/diari dei due ANALYSIS, REVIEW_LOG e relativi",
          "HANDOFF; `sdlc_check.py index` genera INDEX, guide router, features_history, handoff registry",
          "e memory/INDEX. Non include le modifiche preesistenti del corso, release o presentazioni.", ""]
OUT.write_text("\n".join(lines), encoding="utf-8")
print(json.dumps({"file": str(OUT), "planned_product_and_closure_paths": len(plan),
                  "ast_consumer_files": len(consumer_files)}, indent=2))
