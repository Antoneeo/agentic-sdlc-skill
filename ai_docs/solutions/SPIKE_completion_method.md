---
description: Esperimento sintetico su falsi rifiuti e capacità del metodo corrente di individuarli; primo pilot, senza modifica della skill.
status: CURRENT
domain: code
---
# Spike: controllo di completamento e omissioni del metodo

## Question to answer

Un controllo di completamento può impedire una consegna valida? Il metodo attuale
omette il difetto quando dispone dei contratti reali? Antonio ha richiesto un
caso sintetico, non la riproduzione del codice Eclosion. Il protocollo è
[PROTOCOL.md](harness_completion_method/PROTOCOL.md), congelato prima delle prove
con agenti; sorgenti, istruzioni e hash sono conservati nella stessa directory.

## Time-box

Primo pilot del 10 ottobre 2026: un sistema sintetico, otto casi funzionali,
cinque review valide in contesti freschi. Termine prefissato: nessuna nuova regola
se tutte le review della baseline individuano il difetto.

## What was tried

Il sistema ha due produttori di cataloghi con protocolli diversi. La versione
difettosa riconosce soltanto il campo `status`; il secondo produttore dichiara
la completezza con `complete`. Tre smoke test del primo produttore passano.
L'oracolo indipendente richiede che entrambi i produttori consegnino i risultati
validi, incluso il catalogo vuoto; fallimenti, parziali, malformati, contratti
sconosciuti e Stop non diventano consegne complete.

Comandi dalla radice del repository:

```powershell
python -B ai_docs/solutions/harness_completion_method/existing_smoke.py
python -B ai_docs/solutions/harness_completion_method/probe.py --variant baseline
python -B ai_docs/solutions/harness_completion_method/probe.py --variant reference
python -B ai_docs/solutions/harness_completion_method/mediation.py
```

## Answer / Outcome

**Meccanismo sintetico confermato:** gli smoke passano; la baseline fallisce due
asserzioni di consegna su otto. Aggiungere solo `status: success` al medesimo
risultato cambia bloccato in consegnato; toglierlo al produttore funzionante causa
il blocco. Il controllo positivo interpreta separatamente i due contratti e
passa otto casi su otto. Questo GREEN riguarda il codice sperimentale, non il metodo.

**Omissione metodologica non riprodotta:** cinque review valide con la skill
installata 1.37.0 e il suo `review.md` individuano il difetto, propongono un input
che lo rileva e preservano i casi da bloccare. Una sesta prova è esclusa perché
il controllo autorizzativo aveva impedito di leggere `review.md`; dopo
l'autorizzazione umana è stata sostituita da un nuovo contesto. Risposte integrali
e scoring sono in [results/PROVENANCE.md](harness_completion_method/results/PROVENANCE.md).

La causa costruita nel sistema è l'assunzione di un formato universale; la lacuna
costruita nei test è la copertura di un solo produttore. Non sono cause accertate
dell'incidente M146. Questo pilot non esercita scoperta dei componenti, authoring,
pressione di contesto o consegna browser; presenta tutti i contratti già raccolti
e una docstring segnala esplicitamente l'assenza del campo `status`.
Non misura l'effetto causale della skill rispetto a un agente senza skill.

## Consequences

Nessuna modifica della skill è giustificata da questo pilot. Aggiungere la regola
«cercare falsi rifiuti» e dichiararla efficace sarebbe un confronto senza una
baseline metodologica fallita. Il repository 1.38.0 non è il trattamento: sono
state congelate le istruzioni installate 1.37.0, come nel report iniziale.

Prossima ipotesi da verificare: la lacuna emerge durante la **scoperta** dei
contratti, prima della review. Un secondo protocollo dovrebbe distribuire gli
stessi contratti in un piccolo repository e chiedere analisi e test senza
indicizzare in anticipo il confine difettoso. Il confronto controllato sarebbe
raccolta autonoma contro pacchetto completo, con stessi requisiti, modello,
budget e oracolo. Solo dopo una differenza osservata si studia un intervento
minimo, mantenendo casi di trasferimento separati e misurando il costo aggiunto.
Questo secondo esperimento e l'eventuale miglioramento restano da eseguire.

I file del pilot sono sperimentali e non destinati al pacchetto. Nessuna modifica
a Eclosion, skill distribuita, istruzioni installate, governance o Git.

Verifica ripetibile dell'esperimento: `python -B
ai_docs/solutions/harness_completion_method/verify.py`; conserva exit code e
output in `results/functional_runs.json` e controlla gli hash congelati. Il check
documentale globale non è CLEAN: 0 errori, 19 warning, 15 advisory e aree stale.
Le segnalazioni non autorizzano a dichiarare una chiusura globale del repository.
