# Channel Benchmarks — ricerca 2026-07-09

Fonte: sweep web reale (26 fetch). Numeri selezionati nel ledger come
EV-22..EV-32. Tabella completa e caveat sotto.

## Benchmark table

| Metric | Value/Range | Geography | Source | Year | Second source |
|---|---|---|---|---|---|
| Meta CPM Italia | ~$7.20 (range 6.00-8.50) / mediana €10.29 | IT | https://www.adamigo.ai/blog/meta-ads-cpm-cpc-benchmarks-by-country-2026 | 2026 | https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/italy |
| Meta CPC Italia | ~$1.05 | IT | https://www.adamigo.ai/blog/meta-ads-cpm-cpc-benchmarks-by-country-2026 | 2026 | non trovata (flag) |
| Meta CPC Food&Beverage | $0.52-0.78 | Global/US | https://www.get-ryze.ai/blog/meta-ads-cost-benchmarks-by-industry-2026 | 2026 | https://www.digitalapplied.com/blog/facebook-ads-benchmarks-2026-cpc-cpm-ctr-industry |
| CVR paid social e-comm | 2.81% (F&B 3.56%) | US/global | https://www.digitalapplied.com/blog/facebook-ads-benchmarks-2026-cpc-cpm-ctr-industry | 2026 | singola fonte (flag) |
| Google Search CPC e-comm | mediana EU €0.45; IT €0.50-3.00 | EU/IT | https://smarter-ecommerce.com/en/smec-market-observer/metrics/cpc/ | 2026 | https://www.andava.com/learn/italy-digital-marketing-statistics/ |
| Google Shopping/PMax CPC | Shopping €0.38 / PMax €0.40 (mediane EU); US food $0.55 | EU | https://smarter-ecommerce.com/en/smec-market-observer/metrics/cpc/ | 2026 | https://foundrycro.com/blog/google-shopping-benchmarks-by-category-2026/ |
| Shopping Food&Grocery ROAS/CVR | ROAS ~3.5x, CVR ~2.0%, break-even ROAS 2.2-3.3x | US | https://foundrycro.com/blog/google-shopping-benchmarks-by-category-2026/ | 2026 | https://www.get-ryze.ai/blog/google-ads-cost-benchmarks-by-industry-2026 (PMax EU) |
| Email F&B | campagne: open 31.2%, placed-order 0.26%; flow automatici: click 5.8%, placed-order 2.46% | Global | https://www.klaviyo.com/uk/blog/email-marketing-benchmarks-open-click-and-conversion-rates | 2026 | https://www.getresponse.com/resources/reports/email-marketing-benchmarks (IT open 44%, dato 2023 STALE) |
| Site CVR Shopify F&B | ~1.5% (top 20% >4.1%); IT e-comm 1.5-3% | Global/IT | https://www.littledata.io/ecommerce-conversion-rate | 2023 STALE | https://www.andava.com/learn/italy-digital-marketing-statistics/ (2026) |
| CAC food e-commerce | $45-100 (payback 1-3 mesi) | US (flag) | https://eightx.co/blog/average-cac-ecommerce-vertical | 2026 | https://www.upcounting.com/blog/average-ecommerce-customer-acquisition-cost |
| Stagionalità CPM Meta IT | estate €7.13 → set-ott €15.54 (~2x) | IT | https://www.superads.ai/facebook-ads-costs/cpm-cost-per-mille/italy | 2025-26 | — |

## Caveat (dal ricercatore)

- **Gap geografico**: breakdown F&B = US/global; dati Italia = media paese.
  CPM Italia ≈ metà del globale → benchmark US F&B probabilmente SOVRASTIMANO
  i costi italiani; CPC blended IT ($1.05) può sovrastimare il CPC food.
- **Fonti primarie da pesare di più**: WordStream/LocaliQ (16.446 campagne),
  smec (€650M spend EU), Superads ($3B), Klaviyo (183k brand), GetResponse.
  Aggregatori (get-ryze, digitalapplied, adamigo, andava) = panel misti.
- **Stale**: Littledata CVR Shopify = panel 2023; GetResponse email = 2023 e
  open gonfiati da Apple Mail — per pianificare usare click/placed-order Klaviyo.
- **Esclusi** (numeri non verificabili a URL): "PMax ROAS 4.1x", "Food CVR 6.22%".
- **Implicazione budget con AOV €38**: CAC US food ($45-100) supera il margine
  lordo del primo ordine anche al minimo → struttura standard: paid per
  acquisire + flow email automatici per il payback (gap campagne-vs-flow 13x).
- **Stagionalità**: CPM IT raddoppia set-ott → costruire e testare PRIMA di
  settembre; Q4 = finestra d'acquisizione più cara.
