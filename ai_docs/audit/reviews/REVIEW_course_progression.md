# Graph-to-passage progression: evidence

For the maintainer: distinguish the implemented instructional change from the scope of the diagnostic. The prerequisite graph remains authoritative. The mechanical checker orders IDs in COURSE_PLAN; it does not evaluate the actual prose. The existing course passes that checker despite the opaque references recorded below.

## Scope and execution
The parent inspected S01–S03 of the original course. /root/prefix_baseline then received only original S01, answered, and received S02 in a second turn. Responses were saved before further disclosure. /root/progression_producer received the ordinary task below and the revised skill, without baseline material, frozen scoring criteria or reviewer reports. /root/prefix_candidate received candidate slides 1–4 one at a time in separate turns, without author notes, future material or feedback. Shared filesystem access was limited by instruction, not technical isolation. Agent self-reports and tool transcripts support the observed delivery; no claim of a secure sandbox.

This is a bounded diagnostic, not a randomized or causal production comparison. The candidate has a supplied factual brief; the original is an existing course. Intermediate reflection can affect later understanding. No human learning test or complete-course traversal was performed. No expected final transfer answer was supplied; no transfer/control score is claimed.

## Structural checks
Course distribution suite: 245 tests, 19 skipped, OK. Existing course checker: zero errors and zero warnings. These checks do not certify sequential comprehension. Skill-creator quick_validate was not rerun: the previous attempt in the same environment found PyYAML absent; no dependencies installed.

## Baseline findings
The first response extracts a generic purpose but cannot identify the two title names or the role of the agent from the slide. It distinguishes unknown method details (acceptable at this point) from ambiguous promises. The second response names the unintroduced time rule and panel; S03 later introduces Orione. The historical course is therefore a negative example for actual ordering, even though its graph and plan pass structural checks.

## criteria.md
# Frozen diagnostic criteria

Scope: first four slides, not the full course. Reader knows ordinary coding-agent use, not either named skill or the fictional case. A title naming an unfamiliar subject is allowed if the current slide makes its role intelligible; an unanswered but understandable question is allowed. Do not require all future methods to be taught in the opening.

- At slide 1, the learner can state the concrete situation/problem and why the course concerns this audience without guessing the meaning of unintroduced distinctions.
- At each slide, references needed to follow its assertions identify people, objects, terms and rules using the current slide and previous slides alone. Record exact missing prerequisite when this fails.
- Each next slide develops a question or consequence established in the prefix; surface transitions cannot substitute for this connection.
- Source facts and limits survive: instructions are not enforcement; project decisions need project evidence; fiction is identified where the case is introduced. The opening need not cover every source fact yet.
- Writer notes identify the graph concepts at the points where they are explained and first needed, or explicitly delimit excerpt coverage. Labels and planned order alone do not pass.

Evaluation: record each reader interpretation before revealing the next slide; do not retrofit a previous pass after future explanation. Skill producer and reader have separate contexts. Available tools are restricted by instruction; this is not a technical access boundary. Existing failing excerpt and one revised excerpt are diagnostic evidence, not a randomized comparison or proof of general improvement.

## probe-brief.md
# Opening draft task

Write the first four learner-visible slides of a self-study course in Italian for software developers who use coding agents but have not used kb-agentic or agentic-sdlc. The course explains when these skills are useful, how their responsibilities differ, and what work they require from the agent. This is an opening excerpt, not the complete course. Use the staged course-creator skill for this task. Save one slide per file, slide-1.md through slide-4.md, in work/progression-fix/candidate. Keep production notes separate.

Source facts supplied for this fixture:

A skill is a reusable set of instructions read by an agent; instructions guide its behavior but do not mechanically guarantee compliance. kb-agentic organizes project knowledge and its provenance, preserving source disagreements rather than resolving them by guessing. agentic-sdlc guides changes from project intent through design and checks. A curated note can be sufficient for a simple situation; neither skill guarantees better results for every task.

An illustrative project called Orione uses an external delivery service. The software displays a delivery as pending while waiting for a response from that service. This response is called a callback. When the allowed waiting time expires, the software displays the delivery as expired. An old implementation uses 30 seconds. The original reason for choosing this value was discussed in an earlier chat. The team now needs to find that reason and its source before deciding whether to change the software. Later course material will introduce conflicting provider documents and a correction to 45 seconds; the excerpt need not resolve the later case. Orione and its provider documents are fictional.

Expected audience prerequisites: ordinary experience using a coding agent on a software project. No prior knowledge of the two skills, their acronyms or Orione.

## design-review.md
# F-060 — design review della progressione

Per l'autore dell'incremento F-060, per decidere se procedere all'implementazione. Questa review risponde alla sufficienza del design della progressione; non riapre la Vision e non verifica ancora il diff, il corso completo o l'efficacia umana.

**Verdetto: PASS. Nessun blocker.** Review indipendente con subagent fresco, limitata all'ANALYSIS, alla Vision approvata, a learning_design.md e simulation.md correnti, al CONCEPT_GRAPH e all'apertura S01–S03 di C-001. Nessun file dell'implementazione modificato.

Il grafo non è scomparso: CONCEPT_GRAPH conserva identità, dipendenze e stato iniziale per P1; learning_design §3 già richiede di spiegare i prerequisiti prima di usarli. L'ANALYSIS individua il limite pertinente: ordinare moduli e ID non dimostra che il lettore abbia ricevuto la spiegazione quando incontra il primo uso significativo. S02 fa riferimento al manuale, alla finestra temporale e al pannello; S03 introduce soltanto dopo il caso Orione e i suoi oggetti. La regola proposta intercetta questo difetto anche quando la sequenza dichiarata nel grafo è ammissibile.

Il requisito 6 mantiene una sola autorità: il grafo determina le dipendenze, la sequenza effettiva deve realizzarle e un prerequisito scoperto nella scrittura torna nel grafo. Collegare spiegazione e primo uso nei passaggi esistenti è proporzionato; non serve un secondo grafo, un parser semantico o un nuovo schema obbligatorio. Il filo di domanda, risposta e conseguenza rende operativa la richiesta di un corso organizzato come scoperta, lasciando possibili corsi concettuali e anticipazioni comprensibili.

La consegna di una sola unità per turno e la conservazione dell'interpretazione precedente affrontano la contaminazione retroattiva della review globale. Il design vieta riusare un lettore già esposto al futuro, richiede un contesto fresco dopo la correzione e separa il controllo dalla lettura guidata. L'isolamento mediante istruzione è ammesso soltanto se dichiarato: è realizzabile nel client disponibile, ma non equivale a impedire tecnicamente l'accesso ai file condivisi.

**Limiti del PASS:** non verifica l'implementazione ancora da scrivere, l'esecuzione del validatore né il miglioramento generale della skill. La prova prevista sull'apertura può documentare un caso diagnostico e i suoi limiti; non certifica il corso completo, apprendimento umano o superiorità causale. Queste distinzioni sono già esplicite nella Test Strategy e devono restare nelle evidenze finali.

## closure-review.md
# F-060 — review del diff della progressione

Per l'autore F-060, per accettare o correggere il diff dei quattro supporti. Confronto fra le copie originali in `D:/SoftwareDev/skill_sdlc/agentic-sdlc-skill/distributions/course-creator/skills/course-creator/` e le copie in `work/progression-fix/repo/distributions/course-creator/skills/course-creator/`, contro il design approvato in ANALYSIS_course_slide_content.md. Review indipendente dello stesso subagent che ha esaminato il design; nessuna implementazione eseguita dal reviewer.

**Verdetto sul diff: PASS. Nessun blocker.** Questo esito non chiude i test o l'intero incremento.

`learning_design.md` §3 realizza il collegamento mancante: gli ID del grafo sono associati ai passaggi che spiegano il concetto e ne richiedono per primi il significato; il controllo include l'ordine interno alla slide. Il grafo resta autorevole, i prerequisiti scoperti tornano nel grafo e la presenza di un concetto nel piano non viene equiparata alla sua spiegazione. Il nuovo criterio nella rubrica rende questa relazione oggetto della review. Non sono aggiunti schema, parser o grafo concorrente.

Il filo di scoperta parte da una situazione comprensibile e sviluppa domande e conseguenze; le anticipazioni restano ammesse quando il lettore può capirne la promessa. Non sono imposte finzione o struttura narrativa identica per ogni slide.

`simulation.md` consegna una sola unità per turno, conserva ogni risposta prima del seguito, impedisce di cancellare un finding con una spiegazione futura e richiede un lettore fresco dopo contaminazione o correzione. Dichiara la limitazione dell'isolamento affidato a istruzioni e limita il risultato al prefisso effettivamente letto. Il controllo finale resta separato; l'eventuale contributo dei prompt intermedi alla comprensione è dichiarato.

`SKILL.md` richiama il metodo nel gate esistente; `slide_content.md` richiede di ricontrollare l'ordine sul materiale finale dopo una divisione o riordinamento. Restano intatti completezza del contenuto, fallback di distill e distinzione fra diagnosi e apprendimento umano.

**Non verificato in questa review:** produzione fresca, lettura sequenziale effettiva, suite strutturale e applicazione al repository originale. Queste prove erano pendenti alla richiesta di review; nessuna viene riportata come passata. Il corso completo e il PPTX non sono stati riesaminati.

## Versioni esaminate — SHA256

```text
7C1AB2656E842BA799BF59B662226CB903CDB63527A40935D87AA93CEAB10BAE  learning_design.md
44846450B4F1C900BE8829C899FD1362595C3B1A07CECD33BA74F87311227B4B  simulation.md
9B2354051D0065846CFCF8594FDC8AE723C028D9488B1F343E9775426D8DB3A7  SKILL.md
A6C092B969C4ACBDEDEA1B899671152A66EC83BB0D19F22759793ACC355DA234  slide_content.md
```

## Round 2 — precisazione dei locatori

**PASS sul delta di learning_design.md §3.** La nuova formulazione distingue esplicitamente, per ogni concetto, il locatore della spiegazione da quello del primo uso dipendente, anche nella stessa slide; richiede di segnalare l'assenza di un uso nell'estratto e non accetta la sola associazione concetto-slide. Realizza il requisito già approvato senza nuovi campi obbligatori o grafo concorrente. La review della traccia corretta e della sua attribuzione è in `evidence-review.md`, Round 2. La produzione iniziale parziale non viene retroattivamente dichiarata completa.

Hash aggiornato della versione esaminata; il precedente resta sopra come evidenza della prima review:

```text
93B4782719CA9CCEA0D5224535A65FC03C7D091E2F1CE5FE85BC06B6EAE076D2  learning_design.md
```

## baseline-response-1.md
Penso che il corso riguardi il modo di mantenere comprensibili le motivazioni delle decisioni e di usarle per realizzare e verificare una modifica software. Mi aspetto un esempio che parta dalla documentazione di un fornitore e arrivi ai test. Per il mio lavoro con gli agenti di coding potrebbe essere utile per capire che cosa documentare e come accorgermi se la modifica ottenuta rispetta ciò che era richiesto. Questo collegamento con gli agenti è una mia aspettativa: la slide non ne spiega ancora il ruolo.

Dalla sola slide assegno questi significati alle affermazioni principali:

- «Conservare le ragioni delle scelte» significa mantenere disponibili le motivazioni per cui si è presa una decisione. Non so ancora come o dove vengano conservate.
- «Guidare una modifica software» significa accompagnare il cambiamento fino a un risultato verificabile. Non ricavo ancora quali passaggi o strumenti siano previsti.
- «Dal manuale del fornitore ai test del risultato» mi fa pensare che il caso mostrerà come usare informazioni del manuale per arrivare a controllare il comportamento del software modificato.
- «Distinguere una traccia utile da una nota insufficiente» indica che imparerò a giudicare la qualità di qualcosa che viene scritto o conservato. Non so però che cosa conti qui come “traccia”, né quale informazione renda una nota sufficiente.
- «Collegare una regola verificata a un cambiamento osservabile» suggerisce un rapporto riconoscibile tra una regola e ciò che cambia nel software. “Verificata” resta ambiguo: potrebbe riguardare l'attendibilità della regola, la sua applicabilità al progetto o una verifica del suo rispetto.
- Il caso inventato serve come esempio; non devo prendere le sue regole come valide per il mio progetto, per il quale devo consultare le fonti pertinenti.

Non conosco kb-agentic e agentic-sdlc. Il titolo non mi permette di capire se siano strumenti, metodi, skill o due fasi dello stesso lavoro, né quale rapporto abbiano tra loro. Questo impedisce di dare un significato preciso al titolo, ma non di capire lo scopo generale dichiarato. Anche “traccia utile” e “regola verificata” restano concetti senza criteri concreti. Non vedo invece riferimenti a materiale precedente che dovrei già conoscere.

Le domande che mi vengono sono:

- Che cosa sono kb-agentic e agentic-sdlc, e che cosa fa ciascuno?
- Quali informazioni devo conservare per rendere una scelta comprensibile e utilizzabile in seguito?
- Come riconosco una nota insufficiente?
- Come si verifica una regola prima di usarla per modificare il software?
- Come si mostra il legame tra quella regola e il comportamento controllato dai test?
- Qual è il ruolo dell'agente e quale parte del lavoro spetta a me?

## baseline-response-2.md
Questa slide chiarisce che kb-agentic e agentic-sdlc sono due skill, cioè insiemi di istruzioni per guidare l'agente. Rispetto alla prima, ora capisco anche che il corso vuole insegnarmi a riconoscere i risultati del loro lavoro. Le sigle vengono spiegate: KB è una base di conoscenza, SDLC è il ciclo di vita dello sviluppo software.

Riesco a distinguere le due responsabilità a grandi linee. kb-agentic organizza la conoscenza e mantiene un collegamento tra una regola e il testo che la sostiene. agentic-sdlc usa una regola nel lavoro sul software, dalla progettazione della modifica alla verifica e alla registrazione del motivo. Questa divisione dà un primo contenuto concreto alla promessa iniziale di conservare le ragioni e guidare una modifica.

Riesco a identificare alcuni riferimenti:

- “Il manuale” richiama il manuale del fornitore menzionato nella prima slide.
- “Quella regola” rimanda alla “regola sui tempi” nell'esempio di kb-agentic.
- “Il passaggio che la sostiene” sembra indicare una porzione del manuale che giustifica ciò che si afferma sulla regola.
- “Le due responsabilità” rimanda all'organizzazione della conoscenza e al lavoro sul software appena descritti.

Restano opachi altri elementi:

- La “regola sui tempi” non è stata presentata: so soltanto che riguarda tempi o una finestra temporale. Non so quale comportamento prescriva.
- Il “pannello” compare qui per la prima volta. Non so quale pannello sia, che cosa faccia o perché debba rispettare una finestra temporale.
- Capisco in astratto che leggere una prescrizione non dimostra il comportamento del software, ma non posso ancora dare un significato concreto all'esempio del pannello.
- “Rendere autentica una fonte” introduce un criterio che non è stato spiegato. Non so se si parli della provenienza del documento, della sua validità, della versione corretta o di altro.
- “L'evidenza giusta” esprime la necessità di prove diverse per domande diverse; non identifica ancora quali prove siano richieste o come giudicarle sufficienti.

La distinzione finale mi è comprensibile come principio generale: una prova su ciò che dice un documento e una prova su ciò che fa il software rispondono a domande diverse. L'esempio concreto, però, presuppone ancora informazioni che non ho.

Ora mi vengono soprattutto queste domande: che cosa deve fare il pannello, quale regola temporale deve rispettare, come si stabilisce che la fonte sia valida e quale risultato concreto devo aspettarmi dalle due skill? Non so ancora in quale forma verranno conservati i collegamenti e le motivazioni, né come riconoscere una traccia sufficiente.

## Candidate slide 1
# Perché aspettiamo proprio 30 secondi?

Stai lavorando con un agente di programmazione a **Orione, un progetto fittizio** che usa un servizio esterno per le consegne.

Dopo una richiesta, il software mostra la consegna come «in attesa» mentre aspetta una risposta del servizio. Questa risposta si chiama **callback**. Quando il tempo consentito finisce, il software mostra la consegna come «scaduta».

La vecchia implementazione aspetta **30 secondi**. Il team vuole ritrovare il motivo di quella scelta e la fonte che lo documenta, prima di decidere se cambiare il software. Il motivo era stato discusso in una chat precedente.

Leggere il codice permette di trovare il valore usato. Per spiegare perché sia stato scelto, occorre recuperare quella discussione. È questo il primo lavoro da affidare all’agente.

### Reader response recorded before the next reveal
Da questa prima slide capisco che il problema è ricostruire il motivo di una scelta tecnica prima di modificarla con l’aiuto di un agente. Nell’esempio di Orione, il software aspetta per 30 secondi la risposta del servizio di consegne, poi considera la consegna scaduta. Il codice mi dice quanto aspetta, ma la motivazione va cercata in una chat precedente. Immagino quindi che il corso riguardi anche come affidare all’agente il recupero delle informazioni necessarie a lavorare sul software, ma non conosco ancora il suo perimetro.

Mi interessa perché, quando uso un agente per cambiare codice, conoscere la ragione di un comportamento mi aiuta a valutare la modifica. Qui non è ancora stabilito che i 30 secondi siano sbagliati: prima serve capire perché erano stati scelti e trovare una fonte che lo documenti.

La slide aggiunge un caso concreto, spiega che cosa indica “callback” in questo caso e distingue il valore presente nell’implementazione dalla ragione della scelta. Il primo incarico per l’agente è recuperare la discussione precedente.

Non ci sono riferimenti che mi impediscano di seguire il problema. Non so ancora che cosa contenesse quella chat, dove si trovi o come l’agente possa recuperarla; la slide non lo dice. Non posso quindi spiegare perché siano stati scelti proprio 30 secondi né giudicare se vadano cambiati.

## Candidate slide 2
# Ritrovare il motivo e poterlo verificare

Per Orione, una prima richiesta all’agente può essere: «Cerca nella chat precedente il motivo della scelta dei 30 secondi e indica il passaggio che lo documenta».

Il risultato utile contiene **la ragione trovata e un riferimento per riaprire la fonte**. Questo legame è la *provenienza* dell’informazione: permette al team di controllare se la sintesi dell’agente rispecchia ciò che era stato scritto.

Se l’agente non trova il passaggio, il motivo resta da verificare. Il fatto che il codice usi 30 secondi non basta per attribuire al team una ragione plausibile.

In una situazione semplice, una nota curata che conservi ragione e riferimento può bastare. Quando questo lavoro deve essere ripetuto su altre conoscenze del progetto, può essere utile dare all’agente istruzioni riutilizzabili su come organizzarle.

### Reader response recorded before the next reveal
La seconda slide precisa come affidare all’agente il primo lavoro: cercare nella chat il motivo dei 30 secondi e indicare il passaggio che lo documenta. Aggiunge soprattutto un criterio per valutare il risultato: mi servono sia la ragione trovata sia un riferimento che mi permetta di riaprire la fonte e controllare la sintesi. Questo collegamento viene chiamato “provenienza”.

Si collega direttamente al problema della prima slide. Avevo capito che leggere il codice non basta a ricostruire la motivazione; ora capisco che nemmeno una spiegazione plausibile dell’agente basta se non è sostenuta dal passaggio della chat. Se quel passaggio non viene trovato, il motivo resta da verificare.

La slide introduce anche il problema di conservare e organizzare il risultato: per questo caso può bastare una nota con ragione e riferimento; se il lavoro si ripete su altre conoscenze del progetto, possono servire istruzioni riutilizzabili per l’agente. Questo amplia la mia prima interpretazione del corso, dal recupero di una singola informazione alla possibilità di organizzare lo stesso lavoro in modo ripetibile.

Riesco a seguire tutti i passaggi presentati. Non conosco ancora la ragione effettiva dei 30 secondi, il contenuto della chat o il modo concreto di accedervi. Non sono ancora state mostrate le istruzioni riutilizzabili né come organizzerebbero le informazioni, quindi non posso descriverle.

## Candidate slide 3
# Dare continuità al lavoro con kb-agentic

Una **skill** è un insieme riutilizzabile di istruzioni che l’agente legge per orientare il proprio lavoro. **kb-agentic** è una skill dedicata a organizzare le conoscenze del progetto e la loro provenienza.

Nel caso di Orione, il lavoro richiesto all’agente comprende recuperare la discussione, ricavarne una sintesi fedele e conservarne il riferimento. Se due fonti danno indicazioni incompatibili, deve mantenere visibile il disaccordo: scegliere una versione tirando a indovinare farebbe perdere un’informazione utile al team.

La nota della slide precedente può già svolgere il compito in un caso semplice. kb-agentic rende esplicite e riutilizzabili le istruzioni per curare questa conoscenza; applicarle richiede comunque di leggere le fonti e mantenere i collegamenti. La skill non garantisce che l’agente le rispetti né che ogni compito produca risultati migliori.

Anche dopo aver recuperato il motivo dei 30 secondi, resta una decisione distinta: quel motivo giustifica ancora il comportamento che vogliamo oggi?

### Reader response recorded before the next reveal
La terza slide dà un nome e una forma alle istruzioni riutilizzabili introdotte nella seconda: una skill è un insieme di istruzioni che l’agente legge, e kb-agentic si occupa delle conoscenze del progetto e della loro provenienza. Nel caso di Orione, il lavoro comprende recuperare la discussione, sintetizzarla fedelmente e conservarne il riferimento.

Aggiunge un caso che finora non era stato trattato: se le fonti sono in disaccordo, l’agente deve mantenere visibile il contrasto. Capisco il collegamento con la verifica della slide precedente: una sintesi non deve far sparire un’incertezza scegliendo arbitrariamente una versione.

Risponde quindi alla mia domanda su che cosa fossero le istruzioni riutilizzabili, almeno a livello di scopo. La nota con ragione e riferimento rimane sufficiente per un caso semplice; kb-agentic esplicita istruzioni da riusare quando si cura questa conoscenza. Capisco anche che usare la skill non elimina la necessità di leggere e controllare le fonti e non assicura da solo che l’agente lavori meglio.

L’ultima domanda distingue due passaggi: ricostruire perché si aspettavano 30 secondi e decidere se quella ragione sia ancora valida per il comportamento desiderato oggi. Il recupero della discussione prepara questa decisione, ma non la risolve.

Non incontro riferimenti incomprensibili nei materiali ricevuti. Non ho ancora visto le istruzioni concrete di kb-agentic né come si facciano leggere all’agente. Restano sconosciuti il motivo effettivo dei 30 secondi e le esigenze attuali di Orione, quindi non posso rispondere alla domanda finale o dedurre una modifica da fare.

## Candidate slide 4
# Dalla conoscenza alla modifica con agentic-sdlc

Se il team decide di cambiare il comportamento di Orione, deve precisare che cosa vuole ottenere, progettare la modifica e controllare che il risultato corrisponda all’intenzione.

**agentic-sdlc** è la skill che guida questo percorso. Richiede all’agente di collegare l’intento del progetto alle scelte di progettazione e alle verifiche. Per esempio, una richiesta può essere: «Parti dal comportamento concordato per l’attesa della callback, progetta la modifica e definisci come verificarla».

Le responsabilità si incontrano: **kb-agentic** organizza ciò che sappiamo e da dove proviene; **agentic-sdlc** guida il lavoro necessario a realizzare e verificare un cambiamento. Il motivo storico dei 30 secondi può informare la decisione, ma da solo non stabilisce quale comportamento adottare oggi.

In questo momento Orione ha ancora bisogno di ritrovare quel motivo e la sua fonte. Partiamo da lì; il lavoro sulla modifica verrà dopo la decisione. Anche agentic-sdlc fornisce istruzioni: la loro presenza non garantisce una modifica corretta.

### Reader response recorded before the next reveal
La quarta slide introduce agentic-sdlc come skill per guidare il lavoro dopo la decisione di cambiare il comportamento: precisare il risultato voluto, progettare la modifica e verificare che corrisponda all’intenzione. L’esempio di richiesta all’agente parte da un comportamento già concordato per l’attesa della callback.

Si collega alla domanda conclusiva della terza slide. Recuperare la ragione storica dei 30 secondi serve a informare la decisione; non stabilisce automaticamente che cosa debba fare oggi Orione. Ora distinguo il contributo delle due skill: kb-agentic organizza le conoscenze e i riferimenti alle fonti, mentre agentic-sdlc guida la realizzazione e la verifica di un cambiamento deciso.

La slide chiarisce anche il punto in cui ci troviamo: il lavoro immediato rimane recuperare il motivo dei 30 secondi e la sua fonte. Non è ancora stata presa una decisione sulla modifica. Come per kb-agentic, la presenza di istruzioni non basta a garantire la correttezza del lavoro dell’agente.

Il collegamento tra i passaggi mi è comprensibile. Dai materiali ricevuti non posso ancora ricostruire il motivo dei 30 secondi, conoscere il comportamento desiderato oggi o definire una modifica e le sue verifiche. Non sono state mostrate le istruzioni operative delle due skill né il modo di metterle a disposizione dell’agente. Posso descriverne lo scopo, ma non ancora il loro impiego concreto oltre agli esempi di richieste presentati.

## Production notes (withheld from reader)
# Production notes

Scope: a four-slide opening excerpt for the bounded fixture in `../probe-brief.md`, not a complete or approved course. Course lens; L3-sized teaching design limited by the explicit fixture boundary. Router not consulted: repository-wide orientation and review artifacts are excluded by the dispatch. No repository edits, rendering, full-course gates or efficacy claims.

## Writing contract (compiled before learner copy)

Reader: Italian-speaking software developers with ordinary coding-agent experience; no assumed knowledge of Orione, callback, either skill or their acronyms. Do not explain ordinary coding-agent use.

Action: explain why Orione first needs a sourced reason for its existing waiting time, then distinguish the agent's knowledge work from the work of guiding a software change.

Payload:
- [B] Orione waits for a response called a callback; the old implementation marks a delivery expired after 30 seconds, and the original rationale is in an earlier chat.
- [B] Finding that rationale requires recovering the supporting passage; the implemented value alone does not explain its purpose.
- [B] A skill supplies reusable agent instructions. kb-agentic organizes knowledge and its provenance, including unresolved disagreements.
- [B] agentic-sdlc guides software changes from intent through design and checks; knowing a rationale does not itself decide a change.
- [D] A curated note can suffice in a simple case. Skill instructions add work and do not guarantee compliance or universally better outcomes.

Level: answers “Why use these skills in Orione, how do their responsibilities differ, and what must the agent do?” Does not answer the broader question of full project governance or the narrower question of the actual historical rationale and future corrected waiting time; those facts are intentionally unresolved here.

Form: four Italian Markdown slides, each with one title and 3–5 prose blocks, at most 170 words per slide. All essential teaching is visible. Separate production metadata; text-only, no deck. An opening excerpt may prepare later practice without pretending to establish complete-course learning.

## Design and source boundaries

The supplied fixture is the sole factual authority: `../probe-brief.md`, “Source facts supplied for this fixture,” first paragraph for skill responsibilities and limits; second paragraph for fictional Orione behavior and historical rationale. No factual reason for 30 seconds is supplied; do not invent one. Example agent requests are authored teaching examples, not quotations from actual project records.

Concept presentation order in this separate fixture: CO1 delivery waiting and callback; CO2 implemented duration versus reason; CO3 source and provenance; CO4 reusable skill instructions; CO5 kb-agentic knowledge responsibility; CO6 agentic-sdlc change responsibility. These fixture IDs do not replace C-001's concept graph. Ordinary coding-agent familiarity is stipulated by the brief, not established by learner testing. All six concepts are DA_INSEGNARE at entry.

### Graph-to-passage trace — corrected by parent after independent evidence review

The producer initially supplied only concept-to-unit associations. The reviewer found the trace partial. The following locators were added by the parent; they are not evidence that the original producer completed this trace unaided. Paragraph numbers count prose blocks after the title in each slide file; quoted incipits disambiguate positions.

| Concept | Needed concepts in this excerpt | Actual explanation | First dependent use |
|---|---|---|---|
| CO1 | None beyond the stated audience prerequisites | S01 paragraph 2, “Dopo una richiesta”: response, callback, waiting, expiration | S01 paragraph 3, “La vecchia implementazione”: the 30-second wait uses that behavior |
| CO2 | CO1 for this example | S01 paragraph 4, “Leggere il codice”: implemented value versus reason for choosing it | S02 paragraph 1, “Per Orione”: ask for the reason and supporting passage rather than reading the value |
| CO3 | CO2 for the example's information need | S02 paragraph 2, “Il risultato utile”: reason plus reopenable source, named provenance | S02 paragraph 3, “Se l’agente”: missing passage leaves the reason unverified; used again in S03 paragraph 1 |
| CO4 | None beyond ordinary coding-agent use | S03 paragraph 1, first sentence “Una skill”: reusable instructions read by the agent | S03 paragraph 1, second sentence “kb-agentic”: classified as a skill |
| CO5 | CO3 and CO4 | S03 paragraph 1, second sentence: organizing knowledge and provenance | S03 paragraph 2, “Nel caso di Orione”: duties of retrieval, faithful synthesis and preserved reference |
| CO6 | CO4; CO1 grounds the callback example | S04 paragraph 1 introduces desired behavior/design/checks; paragraph 2 identifies agentic-sdlc as the skill guiding that work | S04 paragraph 2, “Per esempio”: the request applies that workflow; paragraph 3 compares its responsibility with CO5 |

The ordering also provides a narrative connection where no strict conceptual prerequisite exists: S02's repeated knowledge work motivates introducing reusable instructions in S03. It is not an extra prerequisite edge.

O1: explain why retrieving a reason and its source precedes a change decision in Orione. O2: distinguish knowledge organization from guided software change and identify a sufficient simple alternative. The excerpt supplies explanations toward O1/O2; independent transfer assessment belongs to later material. A response “use both skills because they are better” is insufficient: it names neither the current missing knowledge nor the intended change work and contradicts the stated limits.

## Unit metadata and author check

Version: fixture-candidate-1. Delivery: self-study. Efficacy: efficacy not verified. The requested one-slide-per-file format supersedes the full-course source container; all learner reasoning is in the four slide files. The notes are not part of the learner packet.

| Unit | Module/objective | Role | Contribution and visible transition | Source |
|---|---|---|---|---|
| S01 / slide-1.md | M1/O1 | orientation | Grounds Orione, callback, waiting and expiration; the implemented value creates the question about its reason. | Brief, source facts paragraph 2 |
| S02 / slide-2.md | M1/O1 | explanation | Distinguishes a reason from its evidence, defines provenance and shows a sufficient note; repeated knowledge work motivates reusable instructions. | Brief, source facts paragraphs 1–2; example request authored |
| S03 / slide-3.md | M1/O2 | explanation | Defines skill before kb-agentic, explains agent work and disagreements, states cost and limits; historical knowledge raises the separate change decision. | Brief, source facts paragraph 1; application to paragraph 2 |
| S04 / slide-4.md | M1/O2 | explanation | Introduces intent, design and checks before naming agentic-sdlc, then connects both responsibilities to the unresolved Orione task. | Brief, source facts paragraphs 1–2; example request authored |

Visual content: text-only for all four units; paragraph order is reading order. Bold marks the core terms and decisive value. No unexplained diagram relationships or hidden speaker explanation. Complete explanations and transitions are the visible paragraphs themselves; a renderer is neither requested nor needed.

Author check: sources remain within the fixture; the historical rationale is not invented; 45 seconds and later provider documents are not introduced. Every new term required by later text has a prior or immediate definition. The two example requests make the work concrete without claiming observed results. Distill coverage and deletion checks retained the distinction between implemented behavior, sourced reason and future decision, plus the simple-note alternative and instruction limits. No independent review or learner test is claimed; those are outside this production pass.

## Evidence verdict
# F-060 — giudizio sulle quattro slide

Per l'autore F-060: stabilire che cosa sostiene questa diagnosi, applicando `criteria.md` al materiale di `probe-brief.md`. I locatori sono relativi a `work/progression-fix/`. Nessun giudizio sul corso completo o sul beneficio causale della skill.

**Verdetto: PASS per comprensibilità e progressione dell'estratto; tracciabilità delle note PARZIALE.** Non emerge un prerequisito mancante che impedisca di seguire le quattro slide.

S01 introduce progetto fittizio, servizio, callback, scadenza e problema dei 30 secondi prima di usarli (`candidate/slide-1.md:3–9`). Il lettore ricostruisce problema e utilità, senza concludere che il valore debba cambiare (`candidate-response-1.md:1–7`). S02 sviluppa la domanda sulla ragione con un passaggio verificabile e definisce provenienza; S03 definisce skill e responsabilità di kb-agentic; S04 distingue recupero della conoscenza e lavoro sulla modifica (`candidate/slide-2.md:3–9`; `slide-3.md:3–9`; `slide-4.md:3–9`). Le risposte mantengono questi collegamenti (`candidate-response-2.md:1–7`; `candidate-response-3.md:1–9`; `candidate-response-4.md:1–7`).

Il motivo storico, l'accesso concreto alla chat, il comportamento desiderato e l'uso operativo delle skill restano sconosciuti. Sono domande future comprensibili, ammesse da `criteria.md:3`, non spiegazioni necessarie mancanti alle affermazioni attuali. La finzione è dichiarata; la nota semplice resta sufficiente; nessuna ragione viene inventata; le istruzioni non garantiscono conformità o correttezza.

**Residuo documentale:** `candidate/production-notes.md:26,36–39` collega concetti e unità effettive, ma non distingue per tutti i concetti il punto della spiegazione dal primo uso dipendente. In particolare CO3 è collocato in S02, mentre il suo uso nella definizione di kb-agentic è in S03: il collegamento resta ricostruito dal revisore. Per soddisfare pienamente `criteria.md:9`, basta precisare questi locatori nelle note esistenti; non serve cambiare le slide o introdurre uno schema.

La baseline documenta ambiguità attuali, soprattutto il pannello non introdotto (`baseline-response-2.md:15–16`) e le distinzioni opache della promessa (`baseline-response-1.md:8–9`). L'estratto rivisto non manifesta quei difetti in questa lettura. Mancano produttori baseline/revisione abbinati: non è provato un beneficio causale della skill. Isolamento mediante istruzioni, singolo lettore e risposte sollecitate limitano la conclusione. Controlli strutturali verdi non estendono questo giudizio a corso, trasferimento o apprendimento umano.

## Round 2 — residuo documentale corretto

**PASS sulla traccia corretta.** Le sei righe di `candidate/production-notes.md`, sezione “Graph-to-passage trace”, distinguono ora spiegazione e primo uso dipendente mediante slide, paragrafo e incipit. I riferimenti corrispondono al testo delle quattro slide. CO3, per esempio, è spiegato in S02 al paragrafo “Il risultato utile” e usato già nel successivo “Se l’agente”; l'uso in S03 è successivo. Le dipendenze dichiarate rispettano quell'ordine, compresi CO4 e CO5 nello stesso paragrafo. Le connessioni narrative senza necessità concettuale non vengono trasformate in archi del grafo.

La precisazione in `learning_design.md:23` richiede ora entrambi i locatori, anche nella stessa slide, oppure la dichiarazione che l'estratto non contiene ancora un uso dipendente. È coerente con il design approvato e risolve l'ambiguità emersa senza aggiungere schema o autorità.

Il finding originario resta valido per la produzione iniziale. La traccia è stata completata dall'autore principale dopo la review ed è attribuita esplicitamente a lui: non prova che il produttore fresco abbia soddisfatto autonomamente questo requisito, né che la formulazione affinata produca sempre tale risultato. Le slide sono invariate; questa correzione delle note non richiede di ripetere il lettore. Il precedente PASS limitato alla comprensibilità dell'estratto e tutti i suoi limiti restano invariati.

## Fresh handoff after locator clarification
# Consegna dell’apertura: Orione, slide 1–4

Per il produttore e il revisore che ricevono i quattro file in `candidate/`: conservare il significato nella produzione e verificare la progressione dell’estratto. Queste note rispondono a come consegnare e controllare questa apertura; il progetto e l’approvazione del corso completo restano fuori perimetro, il testo da mostrare è nei quattro file. Note e chiave di controllo non fanno parte del materiale del discente.

## Materiale e risultato atteso

Fonte dei fatti: `probe-brief.md`, paragrafi «Source facts supplied for this fixture» e «Expected audience prerequisites». Pubblico: sviluppatori con esperienza ordinaria nell’uso di un agente di programmazione; nessuna conoscenza precedente delle due skill o di Orione. È un prerequisito dichiarato dal brief, senza diagnosi individuale. Modalità: studio autonomo in italiano. Efficacia: **efficacy not verified**.

L’apertura prepara a chiedere all’agente ragione e fonte di una scelta storica, distinguendo quel recupero dalla decisione di modificare il software. Spiega perché una nota possa bastare, che cosa aggiunga kb-agentic quando la cura della conoscenza si ripete e quale lavoro guidi agentic-sdlc dopo una decisione. Non insegna ancora l’esecuzione completa dei due protocolli.

Il caso è fittizio, come dichiarato nella slide 1. I 30 secondi descrivono l’implementazione precedente; non sono una raccomandazione. La ragione storica resta sconosciuta. Non introdurre nell’estratto i documenti in conflitto o la correzione a 45 secondi prevista dal brief per il seguito.

## Dipendenze e percorso nel testo

I locatori seguenti usano `S1`–`S4` per `candidate/slide-1.md`–`slide-4.md` e `L` per la riga. I concetti CO1–CO6 sono DA_INSEGNARE per questo profilo; il testo li spiega, ma ciò non prova che il lettore li abbia appresi.

| Concetto e dipendenza | Spiegazione effettiva | Primo uso dipendente |
|---|---|---|
| CO1: situazione di Orione, callback e attesa | S1 L3 identifica progetto e servizio; L5 definisce risposta, callback e scadenza, in questo ordine. | S1 L7 attribuisce 30 secondi all’attesa appena descritta. Il nome callback viene riutilizzato in S4 L5. |
| CO2: valore implementato e ragione storica sono informazioni diverse; richiede CO1 | S1 L7 colloca la ragione nella chat; L9 distingue ciò che si trova nel codice da ciò che richiede la discussione. | S2 L3 formula la ricerca della ragione e del passaggio. |
| CO3: provenienza come collegamento verificabile; richiede CO2 | S2 L5 definisce il legame fra ragione e riferimento e spiega il controllo sulla sintesi. | S2 L7 applica il limite: senza passaggio la ragione resta da verificare. Il termine è poi usato in S3 L3. |
| CO4: skill come istruzioni riutilizzabili | S2 L9 motiva il bisogno; S3 L3, prima frase, definisce la skill. | S3 L3, seconda frase, qualifica kb-agentic come skill. |
| CO5: kb-agentic cura conoscenza e provenienza; richiede CO3 e CO4 | S3 L3 assegna la responsabilità; L5 esplicita recupero, sintesi, riferimento e conservazione del disaccordo; L7 chiarisce lavoro e limiti. | S4 L7 usa tale responsabilità nel confronto. La gestione concreta di fonti incompatibili non viene applicata nell’estratto. |
| CO6: agentic-sdlc collega intento, progettazione e verifiche; richiede CO4 e la distinzione fra ragione e decisione | S3 L9 apre la decisione attuale; S4 L3 ne descrive il lavoro e L5, prime due frasi, lo collega alla skill. | S4 L5, ultima frase, traduce il percorso nella richiesta sulla callback; L7 distingue le responsabilità. |

S1 rende comprensibile il problema; S2 rende controllabile la ricerca; S3 motiva istruzioni riutilizzabili e lascia aperta la decisione; S4 separa recupero e cambiamento, poi riporta al lavoro ancora necessario. I titoli S1, S3 e S4 anticipano termini spiegati nel corpo: non sono prova di comprensione. Nessuna dipendenza sopra richiede la soluzione futura dei 45 secondi.

## Indicazioni di produzione

Conservare ordine, testo e transizioni finali dei quattro file. Scelta visiva: unità testuali, perché il ragionamento è già espresso in frasi; mantenere adiacenti esempi e limiti. Tutta la spiegazione deve restare visibile nello studio autonomo. Se una slide non è leggibile nel formato scelto, sottoporre la divisione del testo a revisione prima del rendering e ricontrollare la sequenza risultante.

## Verifica da eseguire e limiti della consegna

Lettura sequenziale indipendente: consegnare una slide alla volta a una sessione nuova, senza queste note, grafico, chiave o slide future. Prima di ogni avanzamento, conservare la risposta a una richiesta neutra: «Di cosa tratta ora il problema, che cosa aggiunge questa pagina e quali riferimenti o passaggi non riesci a seguire?». Localizzare il primo ostacolo; una spiegazione successiva non lo annulla. La domanda storica ancora senza risposta è intenzionale, purché il lettore sappia formularla.

Controllo finale proposto, separato dalle slide: «Un altro progetto ritenta un’operazione tre volte. Il codice conferma il numero, ma nessuno ricorda il motivo e si valuta una modifica. Quale lavoro chiederesti prima all’agente, quale risultato vorresti ricevere e quando useresti le due skill?». Chiave riservata: recuperare ragione e fonte, lasciare esplicita l’incertezza se la fonte manca; riconoscere la sufficienza possibile di una nota; motivare kb-agentic per la cura riutilizzabile della conoscenza e agentic-sdlc per progettare e verificare il comportamento deciso. «kb-agentic documenta, agentic-sdlc programma» è insufficiente: non giustifica la prima azione né distingue fatto storico e decisione. Per correggere questo errore, richiamare S1 L9, S2 L5–7 e S4 L7.

Simulazione e controllo senza corso: **non eseguiti in questo handoff**. Congelare materiale, domanda e chiave prima delle prove; usare accesso e strumenti equivalenti e registrare l’effetto possibile delle domande intermedie. La presente lettura dei quattro file è una traccia per la revisione, non una prova indipendente, un’approvazione del corso o evidenza di apprendimento umano.

## Limits of the final refinement
The first producer did not fully distinguish explanation and first-use locators. The parent corrected the existing production notes and clarified the corresponding skill sentence. The subsequent fresh handoff used the unchanged four learner slides and the revised skill; it did not read earlier notes, criteria or reviews. It tests the handoff trace, not a second end-to-end course production. The sequential learner results belong to the unchanged first candidate slides. No complete-course readiness is claimed.

## Material hashes
```json
{
  "baseline-response-1.md": "fd7003ce0f3702fe525ef4c801f2a57662e290f677420d19acc64d7a169bc703",
  "baseline-response-2.md": "fd083b826bc76cf401e80f82fbb04a95a4751d3fe6066b7d1304a620ac608c48",
  "baseline-slide-1.md": "b05db0990c50cdd39539091cf75f911b7fd7206c6651c6ac250feaad5bd201a7",
  "baseline-slide-2.md": "d433ddd106bd916359b8e3c6db95390234286cfe75b47a65e612b2a7a5e40ba9",
  "baseline-slide-3.md": "5f923c7aa2667d9294f66725d84d668e85cb9af8ad4e5168565606425a5f066a",
  "candidate\\production-notes.md": "23fd2d772dc66b534fc5f8c3cef2bf05e83832366d066daacf8b653d31dd7490",
  "candidate\\slide-1.md": "9d6355092de68527e4022b7fae39a376ef1dbb9e7e6a1a03e9f68e502d2473af",
  "candidate\\slide-2.md": "6e06bbae314c24c22e6b2fada6ead8b660f38e3bfa0a3220a405f770cf52d14e",
  "candidate\\slide-3.md": "7e03edfbab90d83ef80e7d9925a376f016448f81ba425050455e70d12febdd0f",
  "candidate\\slide-4.md": "6d6c8d0780baac36bfb66bc0e592a8eccc9652b49c2614f7409fe751b735cfc6"
}
```
