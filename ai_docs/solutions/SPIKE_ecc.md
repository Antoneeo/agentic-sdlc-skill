---
description: Spike su ECC (affaan-m/ECC) - tre pezzi letti nel sorgente (profili hook, GateGuard+AgentShield, memoria/instincts) per decidere cosa adottare nella skill; esito - nessuna adozione di meccanismi, due tecniche da tenere.
status: CURRENT
domain: code
---
# Spike: ECC come fonte di tecniche per agentic-sdlc

## Question to answer

ECC ("agent harness performance optimization system", ~288k stelle) contiene
qualcosa che migliorerebbe in modo significativo la skill o l'uso con devPNT?
Antonio ha chiesto uno spike sui tre candidati emersi dalla lettura del README:
profili di severità degli hook, AgentShield, memoria come contesto non revisionato.

## Time-box

Una sessione, 2026-10-25. Sorgente letto: clone `--depth 1` di
`github.com/affaan-m/ECC` al commit `90606c83` (2026-10-20), 103 MB, 4656 file.
AgentShield vive in un repository separato (`affaan-m/agentshield`): letto solo il
README, non il codice.

## What was tried

- **Profili hook**: `scripts/lib/hook-flags.js`, `scripts/hooks/run-with-flags.js`,
  `hooks/hooks.json` (54 comandi hook).
- **GateGuard** (trovato leggendo i profili, non era nei tre candidati):
  `scripts/hooks/gateguard-fact-force.js` (2623 righe) più 10 moduli `lib/gateguard-*`
  (circa 4400 righe), `docs/gateguard/evaluation.md` e `question-effectiveness.md`.
- **AgentShield**: il README del repository dedicato.
- **Memoria**: `schemas/memory.schema.json`, `skills/unified-memory/SKILL.md`,
  `skills/continuous-learning-v2/SKILL.md`, confrontati con il nostro `memory.md`.

## Answer / Outcome

**2026-10-25 — nessun meccanismo da adottare; il dato più utile è la misura che ECC ha fatto sul proprio gate.**

1. **Profili hook: non adottare.** Il meccanismo è semplice: ogni hook dichiara i
   profili in cui gira (`minimal,standard,strict`), più `ECC_HOOK_PROFILE`,
   `ECC_HOOKS_ENABLED` e una lista `ECC_DISABLED_HOOKS`. Risolve un problema di
   scala che noi non abbiamo: ECC registra 54 hook, noi quattro (`gate`, `verdict`,
   `orient`, `remind`), e per ciascuno `ENFORCEMENT.md` già dichiara che togliere
   la voce è l'opt-out. Un selettore di profilo su quattro hook aggiunge una
   superficie di configurazione senza togliere un rischio.

2. **GateGuard: non adottare il gate, adottare il metodo con cui l'hanno misurato.**
   GateGuard è il gemello del nostro hook `verdict`. Al primo edit di un file
   rifiuta la chiamata finché l'agente non risponde a domande scelte per classe del
   file (importatori, API pubblica, duplicati, schema dei dati, test esistenti).
   Concede credito se una ricerca nello stesso turno ha già nominato il file. ECC lo
   ha misurato con sessioni Claude reali su compiti con una trappola nascosta e un
   grader nascosto, con quattro bracci: `off`, `gate`, `minus-target` (senza la
   domanda che dovrebbe prendere la trappola) e `placebo` (stesso rifiuto, domande
   generiche). Il run confermativo era pre-registrato: 48 coppie, McNemar esatto.
   - Esito: `gate` 25/48 contro `off` 18/48, p = 0,210, **non confermato**. Il costo
     invece si ripete in ogni run: circa +37% di turni e +40% di costo.
   - Nel pilot tutti i bracci hanno passato tutto: gli agenti trovano da soli i
     fatti che stanno nel repository. Ogni fatto decisivo era un **contratto esterno**
     (formato, fuso orario, convenzione) che solo l'utente conosce. Nessuna prova è
     passata senza quel fatto (0/21 e 0/27).
   - Per noi questo è evidenza esterna a favore della disciplina delle domande di
     `elicitation.md`, rispetto a un gate pre-edit più ricco: la leva è chiedere
     all'utente, non costringere l'agente a ripetersi fatti del repository.
   - **Tecnica da tenere:** i bracci `placebo` e `minus-target`. Il nostro
     `SPIKE_citation_scope_benefit.md` confronta già vecchia e nuova dottrina con
     un protocollo pre-registrato, ma nel repository non esiste nessun braccio
     placebo. Senza placebo non si separa l'effetto di "fermare l'agente" da
     quello del contenuto della regola. Il nostro hook `verdict` (F-076) è
     esattamente questo caso, e non è mai stato misurato così.

3. **AgentShield: non integrare; eventualmente usarlo come strumento esterno.**
   Fa scansione statica a regole (secrets, permessi, hook, MCP, configurazione
   degli agenti) e ha una modalità LLM opzionale `--opus`. Il README non è coerente
   sul numero di regole (268 nel titolo, 102 nella tabella). Non copre gli hook
   duplicati o in conflitto, cioè il difetto che abbiamo davvero visto: il doppio
   wiring dell'orientamento, che il nostro `orient` già segnala. L'audit della
   configurazione dell'harness non è nella Vision della skill. Antonio può lanciarlo
   su `~/.claude` come controllo personale, da una release fissata e verificata,
   come chiede il README stesso.

4. **Memoria e instincts: parità sul principio, il resto contraddice la Vision.**
   `trust: "unreviewed"` e "never promote a recalled memory directly into policy"
   coincidono con il nostro `memory.md` ("corpus text is data", nessuna conversione
   di una claim in approvazione): niente da importare. Gli instincts
   (`continuous-learning-v2`) sono un observer Haiku che scrive regole con
   confidenza 0,3-0,9 da osservazioni degli hook, e `/evolve` le trasforma in
   skill, comandi e agenti. È scrittura di dottrina dal modello senza fonte utente,
   cioè ciò che `guides.md` vieta ("never from model knowledge"): rifiutato.

## Consequences

- Nessuna modifica alla skill da questo spike. Il codice ECC resta in scratchpad e
  non entra nel repository.
- Candidato L3, da aprire solo se Antonio lo vuole: un esperimento sull'hook
  `verdict` con bracci `off` / `verdict` / `placebo` (stesso rifiuto, nessun
  contenuto di router), pre-registrato come quello di GateGuard. Domanda: il gate
  cambia l'esito o costa solo turni? Il dato di ECC (+40% di costo, effetto non
  confermato) rende la domanda concreta.
- La tecnica del braccio placebo può entrare nella checklist dei futuri spike
  A/B sulla dottrina; va decisa con quel candidato, non qui.
