---
workstream: F-063 Conoscenza cumulativa del software
level: L3
branch: codex/software-knowledge
status: IN_PROGRESS
since: 2026-10-04
next: Modifiche applicate e review R2 PASS; FS7 aperta, il confronto non dimostra minore ricostruzione. Valutare il costo prima di ulteriori cambiamenti.
details: solutions/ANALYSIS_software_knowledge.md; solutions/ANALYSIS_kb_evidence.md; audit/reviews/TEST_software_knowledge_2026-10-04.md; audit/reviews/REVIEW_software_knowledge_code_2026-10-04.md
updated: 2026-10-04
---

## Resume state

Mandato di applicazione eseguito. Runtime, dottrina e pacchetti aggiornati; F-064
completato e tutte le batterie passano. Review del diff: R1 due BLOCK/un WARN,
corretti con regressioni; R2 PASS. Il confronto usa tre varianti e due contesti
freschi ciascuna: risposte corrette, candidato piu costoso in entrambe le sessioni.
FS7 resta aperta. Review successiva (REVIEW_LOG 2026-10-04, claude-opus-5-5): corretti link sopra la root e lettura severa dei frontmatter legacy; poi corretti due WARN minori; il terzo ritirato perche' infondato. Non cambiare il criterio per dichiarare successo; non confondere
il PASS tecnico con l'efficacia. Rubrica, metriche, fonti e limiti sono nel rapporto.

Standalone: devPNT punta a chatPNT. Vision invariata. Nessun commit/publish;
modifiche preesistenti del corso preservate. Diff dell'intervento generato da
`solutions/harness_software_knowledge/implementation_snapshot.py`, baseline locale
conservata in implementation/before.zip. Nessuna installazione nei profili reali.

## Banco di prova Eclosion

Contattato su richiesta dell'owner l'agente della chat «Correggi il documento di
stato», `01a1007c-4bfa-76b1-a5c9-241baea23f86`. Il 2026-10-04 ha indicato M145,
collegato a M139: conservare note e fonte nella sequenza storica e preservare il
prefisso; un controllo locale del buffer/finalizer non dimostra la continuità
attraverso la pausa e il click sulla card.

Snapshot dei rapporti TEST_m145_card_continuity e REVIEW_m145_card_trace_core in
`solutions/harness_software_knowledge/eclosion/`, con origine e hash in sources.json.
La baseline documenta 30/30 note prima e 0/30 alla ripresa, fonte assente, sui loop
Responses e legacy con trasporto/tool simulati. La review del nucleo lascia aperta
l'integrazione: risultati locali positivi non autorizzano a dichiararla risolta.
Qui sono stati letti i rapporti, non rieseguite le prove. Il nucleo ha raggiunto R3 PASS;
l'integrazione resta distinta. Rileggere il progetto prima di asserirne lo stato corrente.

Il caso può verificare l'aggiunta iniziale di proprietà e relazioni e il successivo
aggiornamento con nuovi esiti, mantenendo distinti requisito, osservazione e design.
La domanda a sessione fredda suggerita dall'agente è quale prova dimostri che il
click conserva note, fonte, autrice e prefisso senza rieseguire il tool. Una risposta
corretta deve riconoscere i limiti delle prove disponibili, anche se parzialmente verdi.
