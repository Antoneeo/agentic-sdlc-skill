# Vision Feature: Agentic SDLC vNext

## Problema
- La skill corrente impone un workflow uniforme anche per task piccoli.
- La proposta v2 introduce buone idee, ma non e' integrata nel pacchetto corrente e rischia di rendere devPNT un prerequisito implicito.
- Claude, Codex e Gemini non ricevono oggi gli stessi file runtime: l'installazione nativa copia solo la cartella `skills/agentic-sdlc-skill/`.

## Beneficio Atteso
- Rendere `agentic-sdlc` piu' proporzionale, verificabile e portabile.
- Conservare una modalita' Standalone completa basata su `ai_docs/`.
- Aggiungere una modalita' Hybrid in simbiosi con devPNT, dove `M-VISION`, Master Plan e Action Plan guidano milestone e sviluppo.

## Utenti o Stakeholder
- Sviluppatori che usano Claude Code, Codex, Gemini CLI, Cursor o tool simili.
- Team che vogliono governance locale leggera e integrazione devPNT quando disponibile.

## Segnali di Successo
- Il nome pubblico resta `agentic-sdlc`.
- I support file sono installati nella skill runtime e citati da `SKILL.md`.
- L'installer gestisce Claude, Codex e Gemini in modo coerente.
- Il workflow distingue task L1/L2/L3/Spike senza azzoppare la modalita' autonoma.
- In Hybrid, la skill legge e rispetta la `M-VISION` devPNT prima di design e codice.

## Non-Obiettivi / Fuori Scope
- Non rendere devPNT obbligatorio.
- Non introdurre un sistema ALM completo.
- Non copiare `agentic-sdlc-v2` senza adattamento.

## Vincoli e Principi Collegati
- Vision before solution.
- Lightweight governance.
- No silent double source of truth between devPNT and `ai_docs/`.
