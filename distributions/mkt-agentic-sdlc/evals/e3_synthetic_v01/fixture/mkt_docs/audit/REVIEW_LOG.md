# Review Log

| date | artifact | reviewer | findings raised | real | verdict | rounds |
|---|---|---|---|---|---|---|
| 2026-07-09 | STRATEGY.md | CMO adversarial (fresh subagent) | 11 (5 BLOCK, 6 WARN) | 11 | FAIL→fix | 1 |
| 2026-07-09 | STRATEGY.md (re-review) | CMO adversarial (fresh subagent) | 3 (all WARN) | 3 | PASS→fix | 2 |

## Round 2 (re-review) findings + resolution

Verdict PASS: all 5 BLOCK verified CURED, no new BLOCK. 3 residual WARN fixed:
- N1 swap-test conteggio "6" vs 5 righe + Le Piantagioni (prezzo più vicino) droppato → FIX: aggiunta riga LPDC, conteggio a 6.
- N2 tagline "la mostra anche online" = capacità non ancora consegnata (contraddice EV-53) → FIX: "e la porta anche online" (posizione da raggiungere).
- N3 citazioni imprecise (EV-47 per acquisto→EV-21; EV-19 stirato su urgenza) → FIX: EV-21 in segmentazione; urgenza declassata a principio di tono.
Reviewed text == shipped text (fix post-PASS re-verificati manualmente sui 3 punti).

| 2026-07-09 | MARKETING_PLAN.md + ONE_PAGER.md (finale) | CMO adversarial (fresh subagent) | 3 (all WARN) | 3 | PASS→fix | 1 |

## Review finale (piano assemblato) findings + resolution

Verdict PASS, 0 BLOCK, swap-test regge su tutti e 6, low-cost-trap NON scattata
(rider onestà rispettato), assembly fedele (nessun claim nuovo). 3 WARN fixati:
- W1 prezzo Bugan 15-40 non tracciato → FIX: EV-61 aggiunto + citato.
- W2 uplift CVR "basso rischio" ottimista (target 4-4,5% sopra benchmark 1,5-3%) → FIX: riclassificato rischio medio, spiegato (sito già al soffitto).
- W3 floor build-up = floor O1 senza cuscino → FIX: dichiarata sensibilità + landing atteso ~190 in TACTICAL, MARKETING_PLAN, ONE_PAGER.
Check finale CLEAN (3 warn = righe ledger background non citate, accettabili).

## Round 1 findings + resolution

- F1 BLOCK O2 non servito da alcun pilastro → FIX: aggiunto Pillar 1 "Misurare prima di spendere".
- F2 BLOCK EV-32 citato al contrario (settembre "costa metà" — falso) → FIX: Pillar 5 riscritto, test appena la misurazione lo consente, CPM già in salita da set, a Natale si scala.
- F3 BLOCK "dal 2018" non tracciato → FIX: aggiunta EV-58 (fondazione 2018 + data stampata dall'apertura), citata.
- F4 BLOCK "20-30 euro" in conflitto con EV-48 → FIX: allineato a 12-22 (monorigine) e 28+ (lotti speciali) [EV-48].
- F5 BLOCK "tre generazioni" non tracciato → FIX: aggiunta EV-59, citata.
- F6 WARN roast-to-order non stabilito + contraddice EV-51 → FIX: rimosso dagli unique attributes; l'unicità è la data MOSTRATA + prezzo [EV-58][EV-60].
- F7 WARN swap test incompleto → FIX: tabella completa a 5 competitor; esclusione Orso/HMC su territorio+prova, non downtime.
- F8 WARN "bacino più grande" non tracciato → FIX: rationale primario reso evidenziale (a-c); dimensione etichettata ASSUNZIONE [EV-35].
- F9 WARN CAC "supera" come certezza → FIX: "rischia di superare", benchmark US da verificare.
- F10 WARN EV-53 miscitato per il driver → FIX: driver=EV-43, gap-sito=EV-53.
- F11 WARN refuser non tra i Respinti → FIX: aggiunto ai Respinti.
