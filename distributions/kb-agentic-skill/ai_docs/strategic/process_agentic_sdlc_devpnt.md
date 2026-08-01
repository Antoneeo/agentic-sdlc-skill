---
description: The joint agentic-sdlc × devPNT governance process — pipeline, documents, human vs agent reviews, mandatory checks, and why it works. Read to understand how a change goes from idea to release.
status: CURRENT
---
# Processo congiunto — agentic-sdlc × devPNT

> **L'umano decide, l'agente dimostra, la macchina impedisce l'errore.**

Due sistemi lavorano insieme. La skill **agentic-sdlc** è **il processo** — cosa fare, in che ordine, con quali documenti. **devPNT** è **la macchina** — storage versionato, proposte con Accept/Reject, piani, e i reviewer indipendenti. La skill possiede il processo; devPNT lo rafforza, non lo sostituisce. Un solo triage (Rule Zero), una sola verità.

Legenda dei gate: **◆ umano** = giudizio (insostituibile) · **● agente** = verifica indipendente, fresh-context, read-only.

---

## 1. Due strati, un processo

| agentic-sdlc — il processo | devPNT — la macchina |
|---|---|
| Funziona anche da solo (**Standalone**). | Amplifica la governance; mai obbligatoria. |
| Rule Zero: ogni richiesta triata L1/L2/L3/Spike. | Documenti **versionati** + proposte Accept/Reject in GUI. |
| Fasi: Vision Gate → analisi → piano → impl → closure. | Piani **Master** (strategico) + **Action** (tattico). |
| Ciclo di vita dei documenti + `check --hybrid` a chiusura. | Reviewer indipendenti + guardie **fail-closed**. |

Seam: la skill = processo, devPNT = machinery. Hybrid = i due insieme; se devPNT non c'è, si degrada a Standalone senza perdere capacità.

---

## 2. La pipeline — ordine fisso (L3)

Ogni stadio produce qualcosa e passa un gate.

| # | Stadio | Gate | Cosa |
|---|---|---|---|
| 00 | **Triage — Rule Zero** | ◆ umano dichiara | L1 banale · L2 piccola · L3 significativa · Spike. Sicurezza mai L1. Nel dubbio, si sale. |
| 01 | **Vision Gate → `M-VISION`** | ◆ approva umano | Beneficio, success signals, scope-in, non-goals. Ordine **fisso**: M-VISION approvata → *poi* il milestone. Stella polare immutabile-se-non-discussa. |
| 02 | **Milestone + `Action Plan`** | — | Nodo di piano. Ogni artefatto governato è **appeso a un nodo** — orfano = strutturalmente impossibile (node-linkage fail-closed). |
| 03 | **`D-UC` + `P-TM`** | — | Use cases (cosa serve all'utente) + threat model. Prima dell'E-ISP. |
| 04 | **`E-ISP`** — impatto & soluzione | ● deep + ◆ accept | Impact map che nomina **ogni file** + blast radius ri-derivato. Il deep reviewer (§4.5) ri-deriva l'impatto, legge VISION+UC+TM, **prima** che la proposta arrivi all'umano. |
| 05 | **`E-TDD`** — design tecnico | ● light + ◆ accept | Progetto per-file con firme e anchor. Shadow esportato **prima** dell'impl. Light reviewer (§4.5): copertura E-ISP→E-TDD, firme reali, state table. |
| 06 | **Implementazione** | — | Codice/doc **conformi** all'E-TDD. Il **sorgente**, mai la copia deployata. |
| 07 | **Code Review — §4.6** | ● deep | Diff reale vs E-TDD (conformità) + correttezza/sicurezza, **prima** di DONE. Coglie il drift silenzioso. |
| 08 | **Closure** | ◆ chiude umano | `check --hybrid` CLEAN · test/lint · `REVIEW_LOG` loggato · ADR se scelta architetturale · nodo → DONE. Docs nello stesso commit del codice. |

---

## 3. I documenti coinvolti

| Artefatto | Cosa | Quando | Chi lo verifica |
|---|---|---|---|
| `M-VISION` | Beneficio, scope, non-goals del milestone | 1 per milestone | ◆ umano (Vision Gate) |
| `D-UC` | Casi d'uso — cosa serve e perché | 1 per epic | ◆ umano |
| `P-TM` | Threat model — minacce + mitigazioni | 1 per epic | ● deep §4.5 |
| `E-ISP` | Impact map (ogni file) + blast radius | 1 per unità di cambio | ● deep §4.5 + ◆ accept |
| `E-TDD` | Design per-file, firme, integrazione | 1 per unità | ● light §4.5 + ◆ accept |
| `ADR` | Il *perché* di una decisione architetturale | quando c'è una scelta | ● light §4.5 |
| `SHADOW_*` | Mirror filesystem dell'E-TDD accettato | prima dell'impl | — |
| `Master/Action Plan` | Roadmap strategica + tattico per nodo | sempre | — |
| `REVIEW_LOG` | Una riga per ogni review — misura il gate | a ogni gate | — |

**Standalone (senza devPNT):** l'`ANALYSIS_[feature].md` raccoglie Vision-Alignment + Use Cases + Impact + Threat Model in un unico file; i piani stanno nell'ANALYSIS stessa. Stessi controlli, un solo documento.

---

## 4. Chi revisiona — uomo e agenti

### ◆ Umano — il giudizio
- **Vision Gate:** approva `M-VISION` e `D-UC` — vision e bisogno utente sono human-owned.
- **Sole approver:** ogni proposta si accetta/rifiuta nella GUI. L'agente **non auto-accetta mai**.
- **Decisioni di vision:** cambio di scope o amendment = discussione esplicita.

### ● Agente — la verifica (fresh context · read-only · advisory)
- **§4.5 Design Gate** (prima di proporre): `E-ISP`/`P-TM` → deep; `E-TDD`/`ADR` → light.
- **§4.6 Code Gate** (prima di DONE): diff vs `E-TDD` → deep.
- Regola: *"refute, don't admire"*. Ogni finding con evidence `file:line`. Verdetto **PASS|FAIL**, cap 3 round.

**Confine (Poka-Yoke):** il reviewer non ha strumenti di write/propose/resolve. Il **PASS** alza la qualità di ciò che arriva all'umano — **non** è un auto-accept.

---

## 5. I controlli obbligatori

- **Orientation** — prima di toccare il codice: mappa (summaries/semantica) per evitare duplicazione (anti-DRY) e danni collaterali (anti-collateral). Il codice è il territorio, non la mappa.
- **Design depth** — l'E-ISP nomina **ogni** file impattato; l'E-TDD ha un blocco per-file con firme. Regola dura: **"no file named, no design"**.
- **Input completo** — autore **e** reviewer leggono `VISION` + `UC` + `TM`, non solo la Vision. L'impatto traccia a use case specifici e copre ogni superficie di minaccia.
- **Vision Alignment** — ogni artefatto avanza un beneficio dichiarato della M-VISION e non viola nessun Non-Goal. Lo scope creep silenzioso è BLOCK.
- **Conformance statement** — il verdetto mappa **ogni vincolo → dove soddisfatto (evidence) | finding**. Un **PASS è invalido su "found nothing"**: la review **prova** la copertura, non la asserisce.
- **Node-linkage** — un artefatto governato senza `node_id` viene **rifiutato** (fail-closed). Niente artefatti orfani.
- **Closure gate** — `check --hybrid` CLEAN · test verdi · `REVIEW_LOG` aggiornato · shadow rigenerato · docs nello stesso commit del codice.

---

## 6. Perché funziona

- **Separazione dei compiti.** Il giudizio (vision, approvazione) resta umano; la verifica (ri-derivare l'impatto, controllare la conformità) è dell'agente. Quattro occhi *strutturali*, non un self-pass — che è cieco alle proprie omissioni per costruzione.
- **Fresh context = vera indipendenza.** Il reviewer non ha scritto l'artefatto: quella distanza è il suo valore. Ri-derivando la verità trova le omissioni invisibili all'autore — il file dimenticato, il chiamante che si rompe, la minaccia senza risposta.
- **Poka-Yoke / fail-closed.** Le guardie rendono l'errore *impossibile*, non solo scoraggiato: ordine M-VISION→milestone, node-linkage, "no file named no design". Un uso sbagliato diventa difficile da scrivere, non solo spiegato a parole.
- **Conformità provata, non asserita.** Il conformance statement + "PASS invalido su found-nothing" uccidono il review-teatro: un "ho controllato" non falsificabile diventa una matrice vincolo→evidenza, auditabile.
- **Catena di tracciabilità durabile.** M-VISION → D-UC/P-TM → E-ISP → E-TDD → codice → diff: ogni anello linkato + versionato + loggato. Sopravvive alla compattazione del contesto e al cambio di sessione.

### Prova viva — la sessione che ha scritto questo processo
La modifica "review che legge *e prova* Vision+UC+TM" è stata costruita **dal processo stesso** (dogfooding). Tre BLOCK reali, catturati prima dell'umano — che un self-review avrebbe mancato:

- **`M2.A7` — home mancante.** Il check "use-case coverage" era scritto Standalone-first, ma in Standalone gli use-case non avevano casa (0 hit skill-wide) → il check sarebbe stato a vuoto.
- **`M45` — contraddizione di doctrine.** La regola output resa universale toccava l'agente §4.6 ma non il §4.6 *doctrine* → la doctrine avrebbe contraddetto il suo stesso reviewer.
- **`E-TDD` — schema violato.** Diagramma ASCII invece del Mermaid obbligatorio per un cambio multi-modulo.

> Il valore non è la burocrazia. È che ogni **PASS** porta la prova — e ciò che arriva all'umano è già stato smontato una volta.
