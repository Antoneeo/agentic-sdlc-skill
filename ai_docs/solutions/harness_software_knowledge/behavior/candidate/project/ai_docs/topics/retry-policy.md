---
topic: retry-policy
description: Tentativi configurati, arresto e proposta approvata di backoff
parents: [software-properties]
owns: [retry-policy/properties]
synonyms: [retry, tentativi, attempts, configurazione, backoff, proposta approvata]
gaps:
  - Caricamento config nei chiamanti e servizi reali non forniti.
  - Nessun test source o log grezzo; tutto falso, zero tentativi ed eccezioni non eseguiti.
  - Parametri dei ritardi esponenziali e implementazione del design mancanti.
  - Il PASS fornito usa attempts=3; nessuna esecuzione disponibile per la configurazione corrente attempts=1.
claim_schema: 2
status: CURRENT
---
# Tentativi configurati, arresto e proposta approvata di backoff

## Claims

| id | claim | valid | qty | about | source | prov | state | kind |
|---|---|---|---|---|---|---|---|---|
| ed7529803c5c | Il valore di configurazione catturato è attempts=3. | if versione catturata il 2026-10-04 | 3 attempts count | - | corpus/given/source-898a80b765d5d2169c8f5db93fca941627b94be4e681307302345dd05294e5e1-fbba7af07ce1b2ad333491ea024532cb72f90121bb4ea19dae074971e65ade9b.txt#p=1@0-15 | GIVEN | SUPERSEDED 8a2c2a590ef0 | OBSERVATION |
| f579af228875 | Il risultato fornito riporta PASS con attempts=3 e due falsi seguiti da vero. | if versione catturata il 2026-10-04 | - | - | corpus/given/source-e3ceac7c82d50a3f6a5d26bbb6872d97daf0429cb9ef5c320dfd6dd201bdfeba-181d2eeeefc0a6400827d3c53a9f6742536a7d72719891ddc71308703f9ec260.txt#p=1@0-81 | GIVEN | OK | OBSERVATION |
| fe81bb4c27b5 | Il risultato locale dichiara assenza di chiamate a servizi esterni. | if versione catturata il 2026-10-04 | - | - | corpus/given/source-e3ceac7c82d50a3f6a5d26bbb6872d97daf0429cb9ef5c320dfd6dd201bdfeba-181d2eeeefc0a6400827d3c53a9f6742536a7d72719891ddc71308703f9ec260.txt#p=1@82-109 | GIVEN | OK | OBSERVATION |
| a3cf8c487f67 | Il limite è letto da config["attempts"] e non fissato dal corpo della funzione. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L10-10 | DERIVED | SUPERSEDED 3547ad67a440 | OBSERVATION |
| cf3fdca6a96c | Nel caso locale documentato con attempts=3 e sequenza falsa/falsa/vera, il successo arriva alla terza chiamata. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L11-11 | DERIVED | SUPERSEDED b244f34e9684 | OBSERVATION |
| 3b6aae6dc920 | Secondo la lettura statica il primo valore truthy provoca ritorno immediato True. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L12-12 | DERIVED | SUPERSEDED cec28e64d739 | OBSERVATION |
| 4a2ef53d0481 | Secondo la lettura statica, esauriti i tentativi senza successo la funzione ritorna False. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L13-13 | DERIVED | SUPERSEDED 86c13846163a | OBSERVATION |
| e6e3c025289c | Il corpo non aggiunge attese e non intercetta eccezioni; operation resta una dipendenza non descritta. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L14-14 | DERIVED | SUPERSEDED b094373754b3 | OBSERVATION |
| 57647275bed3 | Preservare limite configurato, arresto al primo successo e False all’esaurimento. | if versione catturata il 2026-10-04 | - | - | corpus/notes/retry-policy.md#L15-15 | DERIVED | SUPERSEDED 01ecf6b74dd8 | REQUIREMENT |
| 8cbe4c563a35 | Il design approvato prevede cinque tentativi. | if versione catturata il 2026-10-04 | 5 attempts count | - | corpus/given/retry-proposal-9f23ebb4.txt#p=1@18-35 | GIVEN | OK | DESIGN |
| 987cdc1555d1 | Il design approvato prevede ritardi esponenziali. | if versione catturata il 2026-10-04 | - | - | corpus/given/retry-proposal-9f23ebb4.txt#p=1@36-60 | GIVEN | OK | DESIGN |
| 00dac20b6be6 | La proposta è approvata come design. | if versione catturata il 2026-10-04 | - | - | corpus/given/retry-proposal-9f23ebb4.txt#p=1@61-79 | GIVEN | OK | DESIGN |
| c26ac671370b | L’implementazione della proposta è ancora pending. | if versione catturata il 2026-10-04 | - | - | corpus/given/retry-proposal-9f23ebb4.txt#p=1@81-104 | GIVEN | OK | OBSERVATION |

| 8a2c2a590ef0 | La configurazione corrente fornita contiene attempts=1. | if input correnti verificati il 2026-10-04 | 1 attempts count | - | corpus/given/source-11d417822122f262f9ab3af7b8b379337f13a6cc3d82af66dc541f09b4a3dbab-fe7f15122f4a5a7aaeb11c9bdd6716fd2d739551735631d3c2fae7b730a84932.txt#L1-1 | GIVEN | OK | OBSERVATION |
| 3547ad67a440 | Il limite è letto da config["attempts"] e non fissato nel corpo della funzione. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L11-11 | DERIVED | OK | OBSERVATION |
| b244f34e9684 | Il PASS a tre chiamate resta documentato per la fixture attempts=3; non verifica il budget corrente a uno. | if fixture storica attempts=3 | - | - | corpus/notes/retry-policy-current.md#L17-17 | DERIVED | OK | OBSERVATION |
| cec28e64d739 | La lettura statica mostra ritorno immediato True al primo risultato truthy. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L13-13 | DERIVED | OK | OBSERVATION |
| 86c13846163a | La lettura statica mostra False a budget esaurito e propagazione delle eccezioni. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L14-14 | DERIVED | OK | OBSERVATION |
| b094373754b3 | Il corpo non introduce ritardi o backoff; operation può avere durata ed effetti propri non descritti. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L15-15 | DERIVED | OK | OBSERVATION |
| 01ecf6b74dd8 | Preservare limite configurato, arresto al primo successo e False all’esaurimento. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L16-16 | DERIVED | OK | REQUIREMENT |
| 2bd18d77260c | Passando attempts=1 al frammento corrente, al massimo una chiamata: un primo falso porta a False senza raggiungere la terza chiamata. | if input correnti verificati il 2026-10-04 | - | - | corpus/notes/retry-policy-current.md#L12-12 | DERIVED | OK | OBSERVATION |

## Responsabilità e riverifica

`inputs/retry.py:attempt(operation, config)` decide il controllo; `inputs/retry-config.json` determina il budget corrente a uno. La modifica del JSON invalida indirettamente la precedente conclusione di successo al terzo tentativo, anche con codice immutato. Leggere corpus/notes/retry-policy-current.md; la nota precedente e le catture restano storia. DESIGN cinque tentativi/backoff resta DESIGN approvato con implementazione pending: non sostituisce le osservazioni sul frammento corrente.
