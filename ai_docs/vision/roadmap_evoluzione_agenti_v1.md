---
description: "Roadmap di evoluzione di agentic-sdlc: esecuzione a subagent operativi e strato di documentazione per la formazione degli agenti. Input per la prossima milestone."
status: SUPERSEDED
superseded_by: ai_docs/vision/roadmap_evoluzione_agenti.md
supersedes: null
target_version: "1.7.0"
---

<!--
  PERCORSO SUGGERITO NEL REPO:  ai_docs/vision/roadmap_evoluzione_agenti.md
  (in alternativa, scomponibile in due file VISION_ separati sotto
   ai_docs/vision/features/ — vedi nota in fondo)

  STATO: DRAFT = ipotesi di milestone. Da promuovere ad APPROVED solo
  con conferma umana, coerentemente con il Vision Gate della skill.
-->

# Roadmap evoluzione — Agenti operativi e Formazione dell'agente

## 1. Obiettivo della milestone

Far evolvere `agentic-sdlc` colmando due lacune, una condivisa con superpowers e una che **nessuna delle due skill possiede oggi**:

1. **Esecuzione a subagent operativi** — la capacità di delegare l'implementazione a agenti freschi per task, con review tra un task e l'altro (ciò che superpowers ha di buono e ad agentic-sdlc manca).
2. **Guide operative da indicazioni dell'utente** — una sotto-skill che, a partire da indicazioni fornite dall'utente (testo o documenti), genera *guide operative* affinché l'agente/subagent operi secondo quelle indicazioni (assente sia in agentic-sdlc sia in superpowers).

Principio guida della milestone: **assorbire il valore senza snaturare l'identità Documentation-First**. Ogni novità si innesta nell'architettura `ai_docs/` esistente ed eredita frontmatter canonico, manifest e lifecycle. Nulla diventa un tool "a lato".

## 2. Tesi centrale: le due feature si rinforzano

Le due feature non sono indipendenti. Superpowers è costretta a **stipare tutto il contesto dentro ogni piano/task**, perché non ha un luogo dove mantenerlo. Lo strato di guide operative (`ai_docs/reference/`) fornisce invece **indicazioni riutilizzabili, versionate e validate** a cui puntare i subagent.

Conseguenza — e qui è una **necessità, non un'ottimizzazione**: un implementer subagent *non eredita il contesto* della sessione, quindi non "sa" a quali indicazioni l'utente vuole che si attenga. Un puntamento del tipo *"leggi `reference/GUIDE_x.md` prima di toccare quel modulo"* è ciò che gliele porta nel contesto e gli impedisce di operare a modo suo (o di inventare, dove le indicazioni riguardano qualcosa che non padroneggia). Le guide operative sono quindi l'infrastruttura che rende **affidabili** i subagent nel nostro impianto: le indicazioni sono mantenute una volta sola, non ricopiate in ogni piano.

---

## 3. Feature A — Esecuzione a subagent operativi

**Cosa.** Strategia di esecuzione che dispatcha un subagent fresco per task, con review tra un task e l'altro (conformità alla spec + qualità) e una review ampia finale.

**Posizionamento.** Modalità di esecuzione **opzionale per L3**, non default. La skill non deve cambiare natura: gli L1/L2 e gli L3 same-session restano la norma. Innesto: file di supporto `references/subagent_execution.md` richiamato dalla Fase 4 (Sviluppo e Test).

**Degradazione pulita (requisito).** Dove i subagent non esistono (es. interfaccia di chat), la modalità ricade automaticamente sull'esecuzione same-session senza perdita di capacità. La skill deve dichiarare esplicitamente quando non può usarli.

**Tocco distintivo rispetto a superpowers.** Il **validatore (`sdlc_check.py`) gira tra un task e l'altro**, non solo alla fine: la coerenza documentale (`check`) diventa parte del ciclo di review per-task invece di essere un gate finale.

**Prerequisito duro.** I subagent richiedono il "piano eseguibile" granulare (vedi Backlog #6): path esatti, interfacce consumes/produces, step con codice e comandi. Questo piano vive come **artefatto di processo in `solutions/`** (discovery-by-grep), mentre l'`ANALYSIS` resta il registro di decisione. A/B sono un pacchetto: subagent senza piano granulare non funzionano.

**Ambiente.** Runtime pieno in Claude Code / Cowork. Non disponibile in chat (si progetta e si scrive qui, si esegue là).

---

## 4. Feature B — Guide operative da indicazioni dell'utente

**Definizione (funzionale, non tematica).** Una guida operativa è la resa, in forma operativa, di **indicazioni che l'utente fornisce** — come testo o come documenti — affinché l'agente/subagent operi secondo quelle indicazioni. Nient'altro la definisce.

Ciò che la guida *tratta* è **irrilevante ai fini del design**: può essere una libreria, una regola non scontata su come implementare una certa cosa in *questo* software, una convenzione di dominio, una prassi aziendale, o qualcosa che col codice non c'entra affatto. Ogni tentativo di categorizzare il contenuto (software/non-software, esterno/interno, post-cutoff…) è una tassonomia mascherata e va evitato: la sotto-skill non ha bisogno di sapere in che categoria cade l'input.

Ciò che distingue questa guida dalla documentazione di progetto **non è l'argomento ma l'origine e lo scopo**:
- Documentazione di progetto → la genera l'agente **guardando il codice** (descrive com'è fatto il sistema).
- Guida operativa (questa feature) → la genera l'agente a partire da **ciò che l'utente decide di fornirgli**, per **vincolare/abilitare il modo in cui l'agente opera**.

Quindi non c'è un confine tematico da tracciare tra le due: una regola su come implementare qualcosa in quel software, se è l'utente a fornirla, è una guida operativa — anche se "riguarda il software" — perché l'origine è l'utente e lo scopo è governare l'operato dell'agente.

Né agentic-sdlc né superpowers hanno questo strato: entrambe documentano il *lavoro*. Questa è l'aggiunta originale, e si affianca ai due tipi esistenti (*vision* → perché/cosa; *ANALYSIS* → le decisioni su una feature).

**I due soli pilastri (entrambi funzionali, nessuno tematico).**

1. **Scopo = criterio di ammissione.** Esiste una guida quando l'utente vuole che l'agente operi secondo certe indicazioni e le fornisce (testo o documenti). La guida le rende operative. È l'unico test; non serve altro.

2. **Fedeltà = vincolo non negoziabile.** La guida rende operativo **solo ciò che l'utente ha fornito**, senza inventare. Se il modello prova a "distillare" qualcosa che non padroneggia, rischia di **inventarlo** sovrapponendo pattern simili visti in training, producendo una guida autorevole e sbagliata che ogni agente poi eredita. Quindi: la **fonte dell'utente è l'unica verità ammessa** (non un input da arricchire con conoscenza pregressa del modello); il transform è "estrai, struttura e rendi operativo **solo ciò che l'utente ha dato**", non "riassumi ed espandi"; ciò che la fonte non copre va **marcato come non-coperto**, mai colmato per inferenza; tracciabilità obbligatoria tra *ciò che la guida cita dalla fonte* e *ciò che eventualmente inferisce*.

**Carattere operativo (forma suggerita, NON imposta).** La guida non è un riassunto, è un manuale d'uso. Repertorio di sezioni **tra cui la generazione sceglie quelle che il materiale dell'utente sostiene** (non un modulo da riempire):
- come si fa *<questo>*
- come si controlla che sia fatto bene
- cosa **non** si deve fare
- a cosa fare attenzione
- quali sono i principi fondamentali
- … (altre, secondo ciò che la fonte sostiene)

Principio: le sezioni sono **plasmate dal contenuto fornito**. Obbligarle tutte ovunque produrrebbe guide gonfie con sezioni vuote — l'opposto dell'utilità. La sotto-skill non parte da un template fisso: parte dal materiale dell'utente, capisce cosa contiene, e sceglie le sezioni che quel materiale può realmente sostenere.

*(Esempi puramente illustrativi della varietà possibile, senza alcun ruolo definitorio: una libreria/API, una regola implementativa non scontata, un linguaggio, una prassi aziendale, una convenzione di dominio. Sono alcuni tra infiniti; non incasellano l'input.)*

**Posizionamento.** Le guide popolano `ai_docs/reference/`, che è **già** una directory canonica manifestata dal validatore. La sotto-skill ne diventa il generatore. Ereditano gratis: frontmatter canonico (`description`/`status`), ingresso in `INDEX.md`, e — vantaggio unico — il **lifecycle**: quando le indicazioni fornite cambiano, la guida si marca `SUPERSEDED` e si rigenera.

**Il transform (bozza di pipeline).**
1. L'utente fornisce le indicazioni (testo o documenti).
2. Proposta di **scomposizione in topic** → l'utente conferma.
3. Estrazione **fonte-ancorata**: solo ciò che è nel materiale fornito; il resto marcato come lacuna.
4. Resa in guida operativa scegliendo, **per ciascun topic, solo le sezioni del repertorio che la fonte sostiene**.
5. Scrittura secondo i principi delle skill: imperativo dove serve, esempi, sezione "quando consultare questa guida", progressive disclosure.
6. Output: un **indice/router** + una guida per topic, ciascuna con frontmatter di **provenienza** (vedi sotto).

**Frontmatter di provenienza (proposta).** Oltre a `description`/`status`, campi come `source` (identificazione di ciò che l'utente ha fornito), `source_version` (quando la fonte è versionata), `distilled_from` (file/percorso). Così lo `stale` può segnalare una guida disallineata rispetto a una fonte aggiornata — freschezza legata alla fonte, non solo al tempo.

**Decisione già presa.** Si generano **guide-documento in `ai_docs/reference/`**, NON skill installabili. Le skill uscirebbero dal repo e dalla governance; le guide restano versionate, manifestate e validate. Coerente con Documentation-First.

---

## 5. Backlog dei gap rispetto a superpowers (contesto)

Ordinato per valore e coerenza con l'identità. Le feature A e B sopra sono la priorità dichiarata dall'utente; questo backlog è il contorno.

| # | Gap | Tier | Innesto proposto |
|---|---|---|---|
| 1 | TDD esplicito (red/green/refactor) | 1 | Sotto-disciplina obbligatoria L2/L3 in Fase 4 + sezione template |
| 2 | Systematic debugging | 1 | `references/debugging.md`, richiamato su bug L2/L3; si lega al circuit breaker |
| 3 | Elicitation collaborativa della spec | 1 | Front-end della Fase 3 per L3 (NO hard-gate universale: resta il triage) |
| 4 | Code review disciplinato (ricevere review) | 1 | Disciplina trasversale in Fase 5 o `references/code_review.md` |
| 5 | Esecuzione a subagent | 2 | **= Feature A** |
| 6 | Piano "eseguibile" granulare | 2 | Prerequisito di A; artefatto di processo in `solutions/` |
| 7 | Attivazione proattiva a inizio sessione | 2 | Hook `SessionStart`: legge `INDEX.md` + handoff, annuncia il triage |
| 8 | Git worktree + chiusura branch | 3 | Igiene di workflow; la chiusura branch si sposa con Fase 5 |
| 9 | Eval harness per la skill stessa | 3 | Processo di sviluppo: evals di triggering/aderenza per evitare regressioni |

**Da NON importare:** `verification-before-completion` (già coperto meglio dal gate `check` della Fase 5) e `writing-skills` (fuori dominio).

**Cautela di stile.** Non adottare il linguaggio `You MUST` / `<EXTREMELY-IMPORTANT>` / tabelle "Red Flags" di superpowers come default: è la filosofia opposta a "il prompt non è enforcement + spiega il perché". Unica eccezione difendibile: le tabelle anti-razionalizzazione applicate **solo** ai gate security-critical (dove "questo cambiamento è troppo piccolo per un'analisi" *deve* essere fermato).

---

## 6. Decisioni aperte

- **A — default per gli L3 grossi o sempre opt-in esplicito?** (Proposta: opt-in esplicito.)
- **A — granularità minima del piano eseguibile** perché un subagent context-free abbia successo senza sovraccaricare la scrittura del piano.
- **B — come garantire la fedeltà alla fonte** (vincolo non negoziabile): revisione umana obbligatoria, auto-check dell'agente con citazioni tracciabili, o un mix graduato in base al rischio di invenzione (più alto quando le indicazioni riguardano qualcosa che il modello non padroneggia, più basso quando la fonte *è* la regola)?
- **B — trattamento delle lacune**: come rappresentare in guida ciò che la fonte non copre, così che l'agente lettore sappia dove NON fidarsi (sezione "non coperto dalla fonte"? marcatore inline?).
- **B — granularità dei topic**: chi decide la scomposizione, e aggiornamento incrementale quando la fonte cambia (rigenerare tutto vs solo i topic impattati).
- **B — provenienza nel frontmatter**: definire i campi (`source`, `source_version`, `distilled_from`) e se il validatore debba verificarne la presenza e segnalare via `stale` il disallineamento tra `source_version` della guida e versione realmente importata dal progetto.
- **Interazione A×B**: convenzione con cui un piano/task punta a una guida di `reference/` (campo dedicato nel task? riferimento esplicito nell'ANALYSIS?).

---

## 7. Sequenza di adozione proposta (a massimo ROI)

1. **Tier 1 a basso attrito**: TDD esplicito → systematic debugging → elicitation spec → code review.
2. **Feature B** (formazione dell'agente): valore originale e indipendente da Claude Code; utilizzabile fin da subito.
3. **Feature A + #6** (subagent + piano eseguibile), come pacchetto e come modalità opzionale, prioritariamente se il lavoro avviene in Claude Code / Cowork.
4. **#7 e #9** (attivazione proattiva; eval harness) a consolidamento.

Nota: la Feature B ha senso *prima* della A, perché A ne trae beneficio diretto (vedi §2).

---

## Nota sulla scomposizione

Questo documento raccoglie due feature più il backlog. Coerentemente con la stessa logica di decomposizione della skill (una VISION per feature indipendente), è legittimo scinderlo in:
- `ai_docs/vision/features/VISION_subagent_execution.md`
- `ai_docs/vision/features/VISION_agent_training_docs.md`

mantenendo questo file come roadmap-ombrello. Da decidere in fase di promozione da DRAFT ad APPROVED.
