---
unit: F-066
analysis: ANALYSIS_merge_review.md
---
# Request record: F-066 Merge review brief and human E2E test script

FIXTURE for the F-067 AC2 replay: rebuilt after the fact from the F-066 session
transcript by the F-067 author (who also authored F-066). Under F-067's own rule this
is a late record; quotations are verbatim from the transcript, which is not in the
repository — the transcription itself is author-attested (T2 residual).

### R1 — 2026-10-12 — opening request
> non usare devpnt in questo progetto.
> Dobbiamo fare un miglioramento.
> I miei progettisti si lamentano che non sanno di cosa fare la merge review a valle di una pull request. Mi chiedono se rivedere tutte le modifiche anche ad ai_docs.
>
> Secondo me è importante individuare cosa serve realmente ai progettisti integratori per la review merge request e fornire di default un documento esplicito e dedicato.
>
> Il documento potrebbe anche contenere una sezione dedicata al test umano E2E o forse meglio serve un altro documento per i test E2E da fornire ai tester umani per le verifiche.

### R2 — 2026-10-12 — elicitation: one or two documents
Context (agent): "Merge review e test E2E umano: uno o due documenti?"
> per il test, serve anche nel caso in cui non sia osservabile per verificare che non ci siano regressioni nel funzionamento

### R3 — 2026-10-12 — elicitation: E2E timing
Context (agent): "Quando eseguono i tester umani il loro E2E rispetto al merge?"
> Dopo il merge (staging)

### R4 — 2026-10-12 — elicitation: level
Context (agent): "Quale livello di triage produce il documento di merge review?"
> Solo L3 (Recommended)

### R5 — 2026-10-12 — elicitation: ceremony cost
Context (agent): "Ceremony budget (Non-Goal 'No ceremony ratchet'): accetti il costo di un nuovo artefatto L3 obbligatorio?"
> Accetto, costo dichiarato

### R6 — 2026-10-12 — design approval
Context (agent): "Approvi il design, così passo al RED dei test e all'implementazione?"
> Si

### R7 — 2026-10-12 — measured cost confirmed
Context (agent): "Costo misurato della doctrine (byte UTF-8): SKILL.md +1149 (letto sempre), templates.md +3258 (letto solo quando serve), hybrid.md +232. Per ogni L3: 2 documenti di 1-2 pagine e un comando da circa 3 s. Confermi il costo dichiarato?"
> Confermo il costo

### R8 — 2026-10-12 — r25 ruling, first answer
Context (agent): "Registro delle rulings, riga r25 … La propongo ADMIT con due basi … Come decidi?"
> non saprei

### R9 — 2026-10-12 — r25 ruling
Context (agent): "Mi confermi ADMIT con le due basi? Rispondi \"sì\", oppure indicami l'alternativa."
> si

### R10 — 2026-10-12 — cost re-confirmed after the closure-review fixes
Context (agent): "Confermi il nuovo costo +1184 / +3258 / +370?"
> confermo

### R11 — 2026-10-13 — merge to main
Context (agent): "Avvio ora l'elicitazione di F-067 o preferisci prima mergiare F-066?"
> prima fai il merge di F-066 su main
