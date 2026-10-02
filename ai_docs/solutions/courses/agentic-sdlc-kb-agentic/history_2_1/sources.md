# Fonti del corso

Questa pagina è il registro unico delle affermazioni sulle skill per la versione 2.1-content, con riuso dello snapshot fissato per 1.0-draft. I file indicati sono gli originali riapribili nel repository al 2026-09-27. Poiché alcuni erano modificati nel working tree, `source_snapshot_2026-09-27.zip` (SHA-256 `f3e5cdf6f88df2f06fe35ccdddd63143b8c7a41653c93f79b1e2d1e01d7887c8`) ne conserva **i byte esatti usati per questo corso**, con gli stessi percorsi interni e i locatori di sezione qui elencati. La tabella SHA-256 identifica ciascuna versione: se un originale cambia, si riapre la copia nello snapshot e si rivaluta l'affermazione prima di aggiornare il corso. Lo snapshot è un archivio di prova, non una seconda fonte da modificare. Il progetto narrativo «Orione» è un esempio ipotetico, non una misurazione di produttività. I confronti con l'uso ordinario sono spiegazioni causali condizionate alla conservazione e alla consultazione delle informazioni, non dati sperimentali.

| Fonte nello snapshot e nel repository | SHA-256 dei byte insegnati |
|---|---|
| `ai_docs/strategic/skills_vs_standard_agents_team.md` | `d17c9c35c2d3d4b847418ade83f45a3c6a81999e22a5aa85c1942f752784b934` |
| `skills/agentic-sdlc-skill/SKILL.md` | `e99110d7a8b3ea20bca625f247258feb1d8217649b1e6fbdaa1e5eb6f81e1b5c` |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md` | `ffed7491d06ac7a05df091fe0df86fe7b9e8eb267653b90e95d22f3be30db22e` |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md` | `441b8014f0d6c00e672e5a53ddcedb3be292431f932c6162c742ff7972eb1d1e` |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/taxonomy.md` | `97753b4377f019203aaba5db82032de998f33bc975724e6f6f259648190b6912` |
| `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md` | `271c71470e7f925b5263c055df5f15bfb8c7be1d43b47587f912cca6cf6e9323` |
| `skills/agentic-sdlc-skill/hybrid.md` | `b1bd55495c3b05c5966c8ea23c0a9d2cfb1ad9abcc04ba96e40dad80878a9cc3` |
| `skills/agentic-sdlc-skill/review.md` | `4070617586e559e1713bd8558c23823c3c3470585321928a00079ded41938404` |
| `skills/agentic-sdlc-skill/guides.md` | `e1cd7071256604eb0844ba3740cf69c70dcca94992cb9427d2c4a5d196c7f56e` |
| `skills/agentic-sdlc-skill/routing.md` | `99dbd353f3f642893dbfeba1279ee7c97c0b2d3b60b003ea190e660d493f2c53` |
| `ai_docs/vision/project_vision.md` | `8282a133cdbff998b9c36ded19b64dd58ff996c02868ef1a98a2d2d13179a184` |
| `ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md` | `4d642cb84dca8b3a7e64f69d8ebab2a10290f0cca15932eef3375ff2a4cebfc0` |

## claim-1

La chat non è la sede durevole garantita per fonti e decisioni di un progetto; la continuità richiede un folder persistente che l'agente possa riaprire. Fonte del problema e del patto d'uso: `ai_docs/strategic/skills_vs_standard_agents_team.md`, sezioni «Il problema nell'uso standard» e «Il folder di progetto». È un'esigenza e un modello operativo dichiarato dal progetto, non una legge universale su tutti i client AI.

## claim-2

Le skill vivono nell'ambiente dell'agente e scrivono la memoria in `ai_docs/` del progetto; gli indici aiutano a scegliere cosa leggere. Fonti: `skills/agentic-sdlc-skill/SKILL.md`, sezioni «Operating Modes», «ai_docs documents: two indexes + lifecycle» e «Operative Guides»; `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md`, sezioni «Operating Modes» e «Topic Recall — the answer-side consult».

## claim-3

`kb-agentic` conserva un artefatto di fonte e la sua provenienza prima di estrarre affermazioni; la lettura di fonti grandi può avanzare per finestre. Fonte: `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md`, sezioni «1. Intake — everything becomes a file first» e «3. Extraction discipline».

## claim-4

La conoscenza è registrata come affermazioni con fonte e stato dentro nodi di argomento; il grafo serve a collocarle e ritrovarle. Fonti: `distributions/kb-agentic-skill/skills/kb-agentic-skill/distillation.md`, sezione «2. The claim — one falsifiable assertion»; `distributions/kb-agentic-skill/skills/kb-agentic-skill/taxonomy.md`, sezioni «0. The graph, in one paragraph» e «6. The same descent, answer mode».

## claim-5

Due claim incompatibili **nello stesso ambito di validità** restano visibili come contestati finché una fonte nuova o una decisione umana basata su un fatto li risolve; claim riferiti a periodi non sovrapposti possono invece coesistere. Il lavoro di revisione raggiunge chi cita claim superati. Fonti: `distributions/kb-agentic-skill/skills/kb-agentic-skill/reconciliation.md`, sezioni «1. Five outcomes — the agent classifies, the machine verifies» e «2. Resolution — only new information»; `distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md`, sezione «Revision — the full re-read».

## claim-6

`agentic-sdlc` distingue L1, L2, L3 e Spike; L3 richiede Vision, analisi, piano, verifica e chiusura. Fonte: `skills/agentic-sdlc-skill/SKILL.md`, sezione «Rule Zero: Triage».

## claim-7

La Vision approvata esplicita beneficio e confini e viene letta prima del design; una divergenza va esposta alla persona. Fonti: `skills/agentic-sdlc-skill/SKILL.md`, sezione «2. Vision Gate»; `ai_docs/vision/project_vision.md`, sezioni «North Star» e «Core Problem».

## claim-8

Nel percorso Standalone l'ANALYSIS contiene use case, Functional Spec quando dovuta, Interface Contract, threat model e Capability Ledger prima dell'Impact; in Hybrid D-UC, D-IC e P-TM sono governati separatamente, mentre Functional Spec e Capability Ledger stanno nell'E-ISP sopra l'Impact. Fonti: `skills/agentic-sdlc-skill/SKILL.md`, sezione «3. Request Analysis»; `skills/agentic-sdlc-skill/hybrid.md`, sezione «Coexistence with devPNT (the Hybrid seam)».

## claim-9

L'Impact lega soluzione, superfici e rischi; la review indipendente del design precede l'implementazione e quella del risultato precede la chiusura. Fonte: `skills/agentic-sdlc-skill/SKILL.md`, sezioni «3. Request Analysis» e «5. Closure»; `skills/agentic-sdlc-skill/review.md`, sezione «When a review is due».

## claim-10

Una GUIDE giustificata conserva un modello operativo con provenienza e viene consultata nel lavoro successivo; non basta una frase generica di cautela. Fonti: `skills/agentic-sdlc-skill/SKILL.md`, sezione «Operative Guides»; `skills/agentic-sdlc-skill/guides.md`, sezioni «0. Consuming a guide (consult before acting)» e «3. Fidelity rules (mandatory, the D5 constraint)».

## claim-11

La lente knowledge governa la fedeltà alle fonti; la lente code governa il cambiamento software. Standalone è completo, devPNT aggiunge governance quando configurato per il progetto. Fonti: `skills/agentic-sdlc-skill/routing.md`, sezione «The router»; `skills/agentic-sdlc-skill/hybrid.md`, sezione «Hybrid in symbiosis with devPNT»; `ai_docs/vision/project_vision.md`, sezione «North Star».

## claim-12

Se fonti, decisioni e GUIDE vengono registrate, consultate e aggiornate nello stesso folder, le sessioni successive possono riusarle senza caricare l'intero corpus nel contesto. È l'inferenza didattica che il corso illustra a settimana, mese e anni, non una misura causale già ottenuta sul team. Fonti per i meccanismi: claim 2, 4, 5 e 10 di questa pagina; Vision approvata `ai_docs/vision/features/VISION_course_agentic-sdlc-kb-agentic.md`, sezione «Valore nel tempo da rendere comprensibile».

## claim-13

Confronto didattico, non risultato sperimentale: una richiesta dettagliata di note può già conservare motivo e provenienza; istruzioni equivalenti possono ottenere gli stessi passaggi di una skill. Il contributo specifico del protocollo è esplicitare e riusare quei requisiti (provenienza, revisione, design e verifica). È un'inferenza dai meccanismi dei claim 1, 2, 5, 8, 9 e 12, non la prova di superiorità di un agente. Gli obblighi nelle istruzioni non garantiscono da soli la conformità dell'esecuzione. Esempi Alba/Bora e Orione interamente inventati; nessun guadagno di produttività misurato.
