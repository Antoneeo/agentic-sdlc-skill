---
description: KPI tree, target, cadenza e criteri kill/scale del piano.
status: CURRENT
plan_status: APPROVED
---
# Measurement Plan — Caffè Brancaleone

## North star

**Ordini online al mese.** È la metrica che traduce direttamente l'obiettivo
del cliente (raddoppio [EV-54]) e che chiunque in azienda capisce senza
gergo. Tutto il resto è un driver di questa.

## KPI table
| Objective | KPI | Target | Benchmark | Cadence |
|---|---|---|---|---|
| O1 | ordini online/mese | 180-200 entro giu 2027 [EV-54] | baseline 90-100 [EV-03] | mensile |
| O1 | CVR sito | da ~3% a 4-4,5% | food IT 1,5-3% [EV-30] | mensile |
| O1 | CAC blended paid | <= 40 | food US 45-100 [EV-31] | settimanale |
| O2 | % spesa paid tracciata a ordine | 100% entro 31 ago | spesa cieca 2023 [EV-17] | una tantum poi continua |
| O3 | quota ricavi online da email | >= 15% a dic 2026 | flow 2,46% placed-order [EV-29] | mensile |
| O4 | ordini online dicembre 2026 | >= 160 | +60% picco [EV-14] | giornaliera nel mese |

## Kill / scale criteria
| Channel | Kill if | Scale if |
|---|---|---|
| Meta Ads | CAC > 90 dopo 700 EUR spesi (2 mesi) senza trend in calo [EV-31] | CAC < 45 a volume stabile → +50% budget entro il tetto 2.000 [EV-10] |
| Google Search | CAC > 35 dopo 900 EUR | CAC < 20 → aumentare copertura keyword |
| Google Shopping/PMax | ROAS < 2,2 (break-even food [EV-28]) dopo 700 EUR | ROAS > 4 → +budget prima del Q4 |
| Email/CRM | placed-order flow < 1% dopo pulizia lista [EV-29] | > 3% → estendere a più flow/segmenti |

Regola trasversale (clausola onestà O1 [EV-55]): se a fine settembre il paid
non regge i kill-threshold, O1 slitta e si dichiara col numero, non si insiste.

## Review cadence

- **Settimanale** (Giulia + consulente): KPI di canale (CAC, ROAS, spesa vs
  budget), spegnere ciò che sfora i kill-threshold.
- **Mensile** (con Marco, 1 ora): ordini online, CVR sito, quota email;
  decisione scale/kill. A ott-nov senza Marco [EV-56], solo Giulia+consulente.
- **Trimestrale**: revisione strategia e budget (verso il tetto 2.000 solo
  con numeri [EV-10]).
