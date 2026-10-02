# Course Creator: collegamento a distill

Per il manutentore: verificare che la produzione e la review usino la disciplina testuale esistente senza duplicarla. Il risultato riguarda il collegamento e una slide; non certifica l'intero corso o apprendimento umano.

## Esito e limiti
Design e diff: PASS indipendente. Due file di istruzioni modificati; distill resta separata, senza path personali o copia di regole. Il reviewer ha confermato il fallback standalone e la fedeltà fattuale distinta. La prova fresca ha letto distill e restituito una formulazione più esplicita con note separate. La rassicurazione sulle sigle rimane: il test non dimostra che ogni frase sia necessaria, né che distill elimini tutte le debolezze editoriali. La disponibilità di distill nel catalogo del produttore impedisce di attribuire causalmente la lettura al solo nuovo rinvio.

La condizione di assenza è stata controllata sul testo della skill e chiesta come caso ipotetico: non è stata eseguita in un client senza distill. Suite della distribuzione 245 test OK / 19 skip, prima e dopo la modifica. Quick_validate della skill-creator non eseguibile per PyYAML assente; nessuna installazione. Il controllo globale del repository resta separato.

## Review del design
# Design review — PASS
Per l'agente che implementa F-060: procedere al solo collegamento distill. Questa review valuta il design corrente; il diff e le prove successive richiedono la review prevista. Non certifica l'efficacia didattica.

## Baseline verificata
Nel pacchetto originale `D:/SoftwareDev/skill_sdlc/agentic-sdlc-skill/distributions/course-creator/skills/course-creator/`:
- `SKILL.md:75-79` prescrive testo completo, review semantica del materiale effettivo, chiarezza e fedeltà; non prescrive lettura/applicazione di distill. Il verbo “distilling” a riga 49 riguarda guide e non invoca la skill.
- `slide_content.md:68-72` prescrive già review della superficie reale: testo visibile, transizioni, didascalie e narrazione guidata.
- La frase contestata esiste in `repo/ai_docs/solutions/courses/agentic-sdlc-kb-agentic/SLIDE_CONTENT.md:30`. L'assenza del richiamo è un fatto distinto dal difetto locale; non prova che ogni produzione precedente fallisse o che distill eliminerà il problema.

## Conformità del design
Locatori seguenti relativi a `repo/ai_docs/solutions/ANALYSIS_course_slide_content.md`.
- UC1/autore e UC2/corsista: righe 24-26, 32; lettore approvato, contratto in produzione, completezza conservata. Coprono `VISION_course_creator.md:24,42`.
- UC3/revisore: righe 26,34; applicazione alla superficie effettiva, inclusa narrazione. Limiti del PASS coerenti con Vision:35,47.
- UC4/autore in ambiente senza distill: righe 27,36; dichiarazione e review esistente mantengono lo standalone della Vision:58.
- Autorità unica e rischio duplicazione: righe 24,28,32,45-46; rinvio nominale, nessuna copia della dottrina. Distill installata v0.8.0 §§2,5,7 resta proprietaria del metodo.
- Compressione, falsa applicazione e sovrascrittura: righe 26-27,51,57; completezza, dichiarazione di assenza e confronto protetto.
- Proporzionalità: righe 15,28,61; nessun nuovo gate L1, schema o dipendenza; prove limitate a instradamento e risultato locale.

Nessun finding bloccante. Da verificare nel diff: conservazione della fedeltà fattuale separata e rinvii dei supporti all'unico contratto. Prove future non ancora eseguite; nessun giudizio sul gate globale.

## Review del diff
# Scoped diff review — PASS
Per l'agente che chiude il collegamento distill: il diff dei due file rispetta il design approvato. Questa review autorizza la conclusione del controllo testuale, non certifica prove diagnostiche o apprendimento umano.

Confrontati i file staged in `repo/distributions/course-creator/skills/course-creator/` con gli omonimi originali in `D:/SoftwareDev/skill_sdlc/agentic-sdlc-skill/distributions/course-creator/skills/course-creator/`.

Nessun finding bloccante.

- `SKILL.md:75` richiede lettura e applicazione della skill disponibile, conserva in Course Creator pedagogia, fedeltà e completezza; non copia la dottrina di distill.
- `SKILL.md:77` governa l'assenza o illeggibilità: dichiarazione del limite, review preesistente, nessun PASS distill inventato o installazione. Il rinvio alla stessa sezione a riga 83 include questo percorso: l'applicazione del metodo dipende dalla disponibilità stabilita sopra.
- `SKILL.md:83` conserva esplicitamente la review distinta della fedeltà fattuale e applica la review testuale alla superficie del corsista.
- `slide_content.md:5,70,72` rinvia all'unico contratto e mantiene testo visibile, transizioni, didascalie e narrazione guidata nel materiale da esaminare.
- `SKILL.md:77` esclude nuovi artefatti per corso e gate L1. Il diff non cambia schema, parser, packaging o distill.

La prova diagnostica di applicazione è ancora pendente e non è compresa nel PASS. La suite comunicata dal coordinatore non è stata rieseguita da questo reviewer; il controllo strutturale generico non eseguito per PyYAML assente resta un limite distinto.

SHA256 dei file esaminati:
- SKILL.md: `C04986257E006A5D9563F45C52EC1803AE999891E842DD3763565210D08A2840`
- slide_content.md: `E92F229D4F2D1F0331AE3780BB2BB042B6721C1E70F9FE97A3A2EA54CF51704B`

## Prova fresca /root/distill_link_probe
## Testo visibile agli allievi

### Che cosa imparerai a fare

Imparerai a ritrovare le conoscenze salvate nel progetto e la fonte da cui provengono.

Userai un requisito documentato per decidere quale modifica fare al software e con quale test verificarla. Non serve memorizzare le sigle.

Lavoreremo su un caso inventato. Per decidere una modifica in un progetto reale, dovrai usare le fonti di quel progetto.

## Note di produzione e revisione — non mostrare agli allievi

Level: L1 · router: non applicabile a L1. Correzione locale della formulazione: obiettivo, prerequisiti, fatti e percorso restano quelli forniti. Nessun file del repository modificato.

Contratto compilato prima della riscrittura:
- Lettore: sviluppatori italiani che usano agenti di coding e non conoscono agentic-sdlc o kb-agentic. Non spiegare che cosa sia un agente; non presupporre conoscenza delle due skill.
- Azione immediata: indicare le due attività che si eserciteranno e scegliere le fonti del proprio progetto per una decisione reale. Questa apertura annuncia capacità da insegnare; non basta da sola a farle acquisire.
- Payload: [B] Il corso insegna a ritrovare conoscenze salvate nel progetto insieme alla fonte. [B] Insegna a usare un requisito documentato per decidere una modifica software e il relativo test. [B] Il caso didattico è inventato. [B] Le decisioni reali devono usare le fonti del proprio progetto. [D] Memorizzare sigle non è un obiettivo.
- Livello: risponde a «Che cosa eserciterò in questo corso e su quali fonti lavorerò?». Non risponde a «Come si struttura l'intero corso?» (fuori incarico), né a «Quali comandi e documenti devo usare?» (da insegnare nel seguito).
- Forma: testo per esseri umani, un titolo e tre brevi paragrafi, massimo 90 parole; frasi complete, nessuna nota di produzione nella copia allievo.

Revisione del testo iniziale: primo periodo B, ma «traccia utile», «nota insufficiente» e «cambiamento osservabile» non esplicitano le operazioni fornite dal brief; secondo periodo D; terzo periodo B. Nessun blocco interamente superfluo o fuori livello. Perdite rispetto al brief: recupero della conoscenza salvata insieme alla fonte, requisito documentato e test non erano espliciti. La riscrittura li rende visibili.

Verifica locale: ciascuna delle quattro asserzioni B e dell'asserzione D compare nella copia; nessuna nuova promessa di efficacia, procedura o proprietà delle skill. Il testo dichiara risultati futuri e distingue il caso inventato dalle decisioni reali. Budget e struttura rispettati. Gate distill e controllo di fedeltà eseguiti dall'autore; nessuna revisione indipendente o prova su allievi eseguita per questa correzione L1. Nessun contenuto didattico trasferito nelle note.

Skill effettivamente lette:
- `C:/Users/apint/Documents/Codex/2026-09-27/che-fine-hanno-fatto-le-skills/work/distill-link/repo/distributions/course-creator/skills/course-creator/SKILL.md`
- `C:/Users/apint/.codex/skills/distill/SKILL.md`
- `C:/Users/apint/.codex/plugins/cache/openai-curated-remote/superpowers/6.4.2/skills/using-superpowers/SKILL.md` — letta; il suo SUBAGENT-STOP ne esclude l'applicazione a questo incarico delegato.

Misura: 44 → 60 parole; token stimati 71 → 93 (euristica caratteri/4, non tokenizzazione del modello). La maggiore lunghezza esplicita le operazioni richieste; nessun contenuto è stato spostato.



Risposta al caso ipotetico: dichiarare distill assente/illeggibile, continuare la review propria di chiarezza e fedeltà fattuale, non dichiarare il passaggio distill e non installarla automaticamente. Queste sono istruzioni comprese, non un'esecuzione osservata in assenza.
