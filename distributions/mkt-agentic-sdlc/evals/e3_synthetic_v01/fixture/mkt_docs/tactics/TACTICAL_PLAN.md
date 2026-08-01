---
description: Piano tattico — canali, budget mensile a regime, funnel di acquisizione.
status: CURRENT
plan_status: APPROVED
---
# Tactical Plan — Caffè Brancaleone

Budget modellato = mese a REGIME (da ottobre) [EV-10]. I mesi estivi
(fondamenta) spendono meno in paid: dettaglio temporale in ACTION_90D.md.
Rispetta l'istinto budget del cliente: ~2/3 su canali collaudati (ricerca
Google + email/owned), paid a briglia corta [EV-55].

Total budget: 1400

## Channel Plan
| Channel | Objective | KPI | Budget | Owner |
|---|---|---|---|---|
| Misurazione & tracking (enabler) | O2 | 100% spesa paid tracciata a ordine [EV-17] | 0 | consulente |
| Google Search | O1 | CAC <= 25 [EV-26] | 450 | consulente+Giulia |
| Google Shopping/PMax | O1 | ROAS >= 3 [EV-28] | 350 | consulente+Giulia |
| Meta Ads (freddo, leash) | O1 | CAC <= 90, kill se non rende [EV-24][EV-55] | 350 | consulente |
| Email/CRM (Klaviyo) | O3 | email >= 15% ricavi online [EV-29] | 50 | Giulia |
| Contenuti/foto organici | O1 | 3 post/sett, foto reali [EV-19] | 80 | Giulia |
| Confezioni regalo Q4 | O4 | pronte 1 nov [EV-57]; welcome 10% + free-ship allineati alle table stakes [EV-49] | 120 | Marco+Giulia |

L'enabler O2 (misurazione) è una riga a budget 0: precondizione a costo
interno che fa da gate su tutto il paid, non un canale di spesa.

## Budget Allocation
| Channel | Budget | Share |
|---|---|---|
| Google Search | 450 | 32% |
| Google Shopping/PMax | 350 | 25% |
| Meta Ads | 350 | 25% |
| Email/CRM (Klaviyo) | 50 | 4% |
| Contenuti/foto | 80 | 6% |
| Confezioni regalo Q4 | 120 | 9% |

Collaudato+owned (Search+Shopping+Email+Contenuti) = 930 = 66% (~2/3, come
richiesto [EV-55]); paid sperimentale (Meta) = 350 = 25%; Q4 stagionale 120.

## Funnel Model
| Channel | Budget | CPC | Clicks | CVR % | Leads | Close % | Customers | CAC |
|---|---|---|---|---|---|---|---|---|
| Google Search | 450 | 0.55 [EV-26] | 818 | 12 | 98 | 22 [EV-30] | 22 | 20.45 |
| Google Shopping/PMax | 350 | 0.40 [EV-27] | 875 | 8 | 70 | 20 [EV-28] | 14 | 25.00 |
| Meta Ads | 350 | 0.90 [EV-24] | 389 | 6 | 23 | 18 | 4 | 87.50 |

Chain: Clicks=Budget/CPC; Leads=Clicks*CVR%; Customers=Leads*Close%;
CAC=Budget/Customers. CVR% = visita->intento carrello, Close% = carrello->
ordine; il netto click->ordine (Search 2,7%, Shopping 1,6%, Meta 1,0%) resta
dentro i benchmark CVR sito food IT 1,5-3% [EV-30] e Shopping food ~2% [EV-28].

## Order build-up vs O1 (riconciliazione obbligatoria)

Il funnel paid da solo NON raggiunge O1: va sommato ad owned e uplift sito.

| Fonte ordini/mese a regime | Ordini | Base |
|---|---|---|
| Baseline attuale (traffico esistente ~3.000 visite [EV-05], CVR ~3%) | 90-100 | [EV-03] |
| Uplift CVR sito (data di tostatura in scheda + UX) da ~3% a ~4-4,5% [EV-30][EV-43] | +30-45 | stima, rischio medio |
| Nuovi da acquisizione paid (Search 22 + Shopping 14 + Meta 4) | +40 | funnel sopra |
| Email/flow su lista 1.200 + riacquisti (>70% categoria [EV-34]) | +20-30 | [EV-29][EV-12] |
| **Totale a regime** | **180-215 (atteso ~190)** | **>= O1 target 180-200** |

L'obiettivo O1 è raggiunto SE: (a) l'uplift CVR sito si materializza — leva a
costo ~zero ma **rischio medio**: il target 4-4,5% supera il soffitto del
benchmark generico 1,5-3% [EV-30], giustificato solo dal fatto che il sito
gira GIÀ al soffitto (~3% osservato [EV-05][EV-03]) e la data di tostatura in
scheda attacca il trigger n.1 [EV-43]; (b) i test paid di settembre reggono i
CAC (rischio medio — clausola di onestà O1 [EV-55]).

**Sensibilità:** il floor del build-up (90+30+40+20 = 180) coincide col floor
di O1 — cioè nessun cuscino se ANCHE una leva owned resta al minimo. Il
landing onesto atteso è ~190 (punto medio), con 180 come pavimento dichiarato.
Se (b) fallisce, il totale scende a ~150-175 e O1 slitta, dichiarato.

## Channel selection rationale

- **Search + Shopping** (collaudati, alta intenzione): intercettano chi già
  cerca caffè specialty; CPC IT/EU bassi [EV-26][EV-27]; priorità budget per
  istinto cliente [EV-55]. Owner Giulia+consulente (8h/sett [EV-11]).
- **Meta** (freddo): unico modo di raggiungere il "curioso" che non cerca
  ancora [EV-45]; CPM IT ~7-10 EUR e CPC blended ~1 [EV-22][EV-23], CVR paid
  social e-comm 2,8-3,6% [EV-25]; CAC atteso ~87 >> margine primo ordine
  (~21 EUR: AOV 38 [EV-04] x 55% [EV-08]) → si paga solo sul riacquisto
  [EV-29][EV-34], quindi leash + kill (THREAT_MAP). Test in estate/inizio
  autunno prima del picco CPM [EV-32].
- **Email/owned**: il canale a margine più alto (costo vivo ~zero), grande
  del lavoro come da vision — flow che convertono ~10x le campagne [EV-29].
- **Esclusi**: TikTok (vincolo [EV-19]); influencer a pagamento (fuori budget
  e capacità 12h/sett [EV-11]); marketplace terzi (erode margine e brand).
