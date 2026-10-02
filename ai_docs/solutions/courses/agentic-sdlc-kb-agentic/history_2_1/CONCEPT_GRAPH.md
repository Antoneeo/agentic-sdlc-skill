# Grafo dei prerequisiti didattici

Questo grafo ordina ciò che P1 deve capire per seguire il corso. Non è il grafo degli argomenti di `kb-agentic`: quello colloca conoscenza di progetto, questo stabilisce dipendenze fra spiegazioni. P1 comprende sviluppatore e responsabile tecnico nel percorso comune; la conoscenza di partenza delle skill non è stata misurata. `INCERTO` non significa già appreso.

| Concept ID | Prerequisites | Profile | Initial state | Evidence | Source | Objectives |
|---|---|---|---|---|---|---|
| CO1 | - | P1 | INCERTO | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-1 | O1 |
| CO2 | CO1 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-2 | O1 |
| CO3 | CO2 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-3 | O2 |
| CO4 | CO3 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-4 | O2 |
| CO5 | CO4 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-5 | O3 |
| CO6 | CO2 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-6; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-7 | O4 |
| CO7 | CO6 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-8 | O5 |
| CO8 | CO7 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-9; ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-10 | O5 |
| CO9 | CO5; CO8 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-11 | O6 |
| CO10 | CO9 | P1 | DA_INSEGNARE | - | ai_docs/solutions/courses/agentic-sdlc-kb-agentic/sources.md#claim-12 | O7 |

## Legami che contano

- CO1 → CO2: la memoria esterna ha senso soltanto dopo aver visto il limite della chat come deposito del progetto.
- CO3 → CO4 → CO5: prima si conserva la fonte, poi si ricavano claim rintracciabili, poi si può capire che cosa cambia quando due claim confliggono.
- CO6 → CO7 → CO8: prima il beneficio e il livello del cambiamento, poi bisogni/interazione/rischi, infine Impact, design, review e GUIDE.
- CO5 e CO8 → CO9 → CO10: la collaborazione fra le due skill e il valore nel tempo si capiscono dopo aver visto come entrambe conservano e correggono conoscenza.

Le dipendenze indicano necessità di comprensione, non un numero obbligatorio di lezioni. Un prerequisito incerto viene spiegato nel modulo in cui compare prima del suo dipendente, oppure dichiarato come limite se una prova reale lo smentisce.
