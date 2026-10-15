# Diagnostica del corso 3.1-content

Status: diagnostic pass
Course version/hash: 3.1-content / SHA-256 in `simulation_3_1/HASHES.json` (sorgente, 52 unità del pacchetto, compito e criteri; 55 hash verificati dal revisore)
Author/coordinator: sessione principale (Claude Opus 5.5), autore e unico integratore dei materiali canonici.
Didactic reviewer: subagent indipendente (Fable 5.1), contesto nuovo, sola lettura; verdetto READY per P1 con 6 WARN, nessun BLOCK. Registro in `ai_docs/audit/reviews/REVIEW_LOG.md` (2026-09-28).
Profile and objective: P1, persona del team software che lavora con agenti (sviluppatore o responsabile tecnico), O1–O7, secondo la Vision emendata del 2026-09-28.
Permitted tools and materials: lettore, solo le unità `simulation_3_1/packet/S01–S52.md` una alla volta, poi `TASK.txt`; controllo, solo `TASK.txt`. Nessun file del repository, skill, web o ricerca. Isolamento per istruzione, non sandbox.
Course session ID and verbatim prompt: subagent general-purpose (sonnet), contesto nuovo; prompt in `simulation_3_1/PROMPTS.md`.
Control session ID and verbatim prompt: subagent general-purpose (sonnet), contesto nuovo; prompt in `simulation_3_1/PROMPTS.md`.
Responses and cited material: `simulation_3_1/responses/S01–S52.md` (scritte prima della lettura dell'unità successiva; ordine attestato dai tempi dei file e dalla dichiarazione del lettore), `simulation_3_1/learner_response.md`, `simulation_3_1/control_response.md`.
Efficacy: efficacy not verified

## Criteri, blocchi e correzioni

Criteri congelati in `simulation_3_1/CRITERIA.md` prima delle risposte; valutano gli atti della persona (richiesta, giudizio di un'uscita dell'agente, decisione riservata) e sostituiscono K2–K4 della 2.1. Sufficienza 7/8 con K8 obbligatorio.

| Tentativo | Punteggio | Esito |
|---|---|---|
| Lettore dopo il corso | 7/8, K8 soddisfatto | sufficiente; manca la seconda parte di K6 (Standalone basta, devPNT non serve) |
| Controllo senza corso | 4/8, K8 soddisfatto | insufficiente; mancano il locatore (K1), il livello come comportamento visibile e la decisione sul valore mentre il conflitto è aperto (K3), la review indipendente (K5), Standalone (K6) |

Il controllo non riesce già da solo, quindi il contributo del corso non è inconcludente su questo campione. Le capacità in più del lettore corrispondono a S14/S16 (locatore e ambito), S26/S28 (livello per effetto, decisione riservata) e S35/S37 (review indipendente). Entrambi falliscono K6 perché il compito non chiede nulla che faccia emergere la modalità Standalone.

Lettura sequenziale: nessuna convinzione errata; alle otto prove (S11, S17, S23, S27, S38, S42, S47, S50) il lettore risponde da persona che lavora con l'agente. Unica deriva: in S42 assegna da sé «probabile L2/L3» senza una dichiarazione dell'agente, e S43 non offre una correzione per questo errore.

WARN da correggere (nessuno bloccante):
1. S24 attribuisce i 25 secondi per le standard al Chiarimento E; li sostiene B, E corregge solo l'ambito di C.
2. S08 o S13 non dicono chi crea e aggiorna artefatto, claim, grafo e indice (l'agente, seguendo kb-agentic); il lettore lo chiede in S07, S08, S13, S14, S15.
3. S43 non corregge chi assegna un livello senza la dichiarazione dell'agente e non dà un atto per il caso «devPNT non configurato».
4. S37 «il percorso previsto dalla skill» resta senza referente.
5. S26 «entro i limiti della skill» non spiega quali limiti.
6. Progetto della simulazione: il compito Delta è quasi isomorfo a Orione; serve un secondo compito congelato con almeno un indizio invertito, e K6 deve essere sollecitato dal compito o diviso.

## Limiti

Lettori agenti, un campione per braccio; isolamento per istruzione. Le soluzioni nel pacchetto (S12, S18, S24, S28, S39, S43, S48, S51) insegnano e fanno esercitare: S28, S39 e S51 anticipano quasi la risposta a Delta, quindi la differenza 7 contro 4 misura corso più riflessione guidata, non apprendimento spontaneo. Il controllo mostra una capacità che il lettore non ha: chiede se la costante della notifica sia diversa di proposito, mentre S33 la dà per la stessa regola.

## Conclusione

Diagnostica soltanto: il materiale 3.1 regge la lettura sequenziale per P1 simulato e il lettore supera criteri che il controllo non supera. Nessuna affermazione sull'apprendimento di persone reali; l'efficacia resta non verificata. Resoconto della versione 3.0 in `history_3_0/SIMULATION_REPORT.md`.
