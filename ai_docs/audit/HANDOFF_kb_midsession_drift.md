---
workstream: F-041 KB Mid-Session Drift (field report, 2 items)
level: L3
branch: feat/kb-midsession-drift
status: DONE, AWAITING MERGE
since: 2026-08-28
next: the owner's merge call (closure PASS in 1 round, 0 BLOCK, all 5 WARN folded; batteries 179/311/197 OK)
details: ANALYSIS_kb_midsession_drift.md (+ this file: evidence verbatim)
updated: 2026-08-28
---

## The field report (verbatim, external work session, 2026-08-28)

Reported by the owner from an external session running kb-agentic on two projects:

> No, nessuno. L'unico hook configurato e' un SessionStart con matcher compact che
> stampa le istruzioni devPNT -- niente di kb-agentic, ne' globale ne' nei due progetti.
>
> E ne manca uno che dovrebbe esserci per default. ENFORCEMENT.md par.4 descrive un
> SessionStart -> sdlc_check.py orient che emette router, handoff, README e il
> promemoria di Rule Zero all'avvio, dice che dalla v1.16.0 viene installato
> automaticamente, e motiva cosi': "era opt-in e il risultato sul campo e' stato il
> difetto che questo livello esiste per prevenire". Su entrambi i progetti non c'e'.
>
> Correggo pero' la raccomandazione di prima, che era troppo ottimista. orient scatta
> una volta, all'avvio della sessione. La mia deriva e' avvenuta a meta', dopo dieci
> turni: quell'hook non l'avrebbe intercettata. [...] L'unico hook che scatta
> ripetutamente e' il PreToolUse -> gate, ed e' deliberatamente grossolano [...]
> Non e' uno strumento di disciplina, e' un lucchetto su cartelle sensibili.
>
> Quindi la risposta onesta: installare orient conviene [...] ma la deriva a meta'
> sessione oggi non ha alcun presidio meccanico, in questo toolkit. [...] se vuoi
> anche qualcosa contro la deriva, quello va inventato, non configurato.

## The two items

**A — the wiring-promise gap.** F-036 wires the orient hook at `init` only; projects
initialized BEFORE kb 1.5.0 never receive it retroactively, while ENFORCEMENT reads as
"installed automatically". Candidate fixes: (1) honesty in ENFORCEMENT ("automatic at
init; pre-existing projects: re-run init or wire per par.4"); (2) better, a mechanical
signal — the validator already runs in those projects, so `check` (or `orient` itself,
when run by hand) can WARN when no orient hook is wired in the project's settings.
Operative fix on the two affected projects is the owner's, in that session.

**B — mid-session drift has no mechanical guard, and it happened.** The drift arrived
"after ten turns"; orient fires once, the gate is a lock not a discipline. The proven
pattern sits next door: distill 0.5.0's per-turn hook — the discipline in miniature,
~50 tokens/prompt. For kb: an OPTIONAL UserPromptSubmit hook documented in ENFORCEMENT
(never default — the per-turn cost is the project's choice), carrying the kb minimum:
Rule Zero triage + the recall trigger + the capture moment, one line. The vision's
no-per-turn-hammering non-goal bans hammering the GRAPH per turn, not a static
one-line reminder; the ANALYSIS must draw that line explicitly.

## Why this matters to the vision

First real usage datum of the second brain, arrived before the planned field test:
orient alone does not hold the doctrine through a session. Feeds the same evidence
stream unit 3 (the time cycle) waits on.

## Watch out

- The "v1.16.0" in the report is the external session's paraphrase; verify what
  ENFORCEMENT par.4 actually claims and against which version before quoting it.
- Item B's hook payload must be self-contained (the distill lesson: an instruction to
  run a procedure the agent has not read is not an instruction).
