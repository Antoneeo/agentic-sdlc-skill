---
description: Prototipo di viewer HTML statico che mostra all'utente il grafo kb, la discesa e le affermazioni con fonte, come li vede l'agente.
status: DRAFT
domain: code
---
# Spike: viewer grafico della kb

## Question to answer
Si può dare all'utente, senza mod e su ogni client, la vista che l'agente ottiene usando kb-agentic: argomenti, gerarchia, discesa di recall, affermazioni con stato e fonte?

## Time-box
2026-10-16, una sessione. Corpus reale: `kb_field_test_eclosion` (7 argomenti, 28 affermazioni, 5 fonti GIVEN + 1 RULING). Codice in `solutions/spike_kb_viewer/`, non mergeable.

## What was tried
- `export.py` importa `knowledge.py`/`sdlc_core.py` della distribuzione kb (`kb_collect_topics`, `kb_parse_claims`, `load_frontmatter`, `kb_graph_check`) e non riscrive regole di formato; l'unica logica propria è l'estratto per locatori `#L<a>-<b>`.
- `template.html`: una pagina sola, nessuna dipendenza (niente d3), dati incorporati. Layout a livelli (un nodo sotto il suo genitore più profondo), ricerca su nome/sinonimi/descrizione/affermazioni con il percorso radice › … › argomento, dettaglio con genitori/figli, sinonimi, lacune, affermazioni in vigore e sostituite, salto alla sostitutiva, estratto della fonte con le righe citate e il sidecar.
- Aperta nel browser integrato dell'app desktop: ricerca e selezione funzionano.

## Answer / Outcome
Sì. Una pagina statica generata dal checker basta e non serve un mod: funziona con qualsiasi browser, quindi con ogni client. Nell'app desktop la pagina va scritta dentro la cartella del progetto, perché il pannello browser mostra i file esterni come snapshot statiche.

Limiti visti:
- solo i locatori `#L` hanno estratto, mentre `#p=…@…` e gli offset no;
- la ricerca è testuale e non segue la discesa semantica dell'agente (mostra il percorso, non lo sceglie);
- il layout a livelli regge decine di nodi, non centinaia.

## Consequences
Per la produzione è un L3: nuovo comando della CLI condivisa, comportamento visibile, tre distribuzioni.
- **Dati:** un export JSON nel checker (`graph --json` o `export --json`), unico proprietario dei formati; i locatori non-`#L` vanno risolti lì.
- **Vista:** template in `viewer/` dentro la skill, da aggiungere al `"files"` di ogni `package.json`; un comando scrive la pagina in una cartella esclusa da git, non in `ai_docs/`.
- **Vision (Non-Goal di lavoro):** `kb_graph_check` vieta la superficie di stato per nodo. Il viewer mostra struttura, affermazioni e lacune del singolo nodo e non le aggrega mai: niente conteggi, colori di copertura o maturità per nodo.
- Poi la vista milestone di agentic-sdlc, con lo stesso schema.
