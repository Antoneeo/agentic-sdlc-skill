---
description: Per il team di sviluppo: vantaggi di kb-agentic e agentic-sdlc rispetto all'uso di un agente senza memoria e processo di progetto.
status: CURRENT
domain: knowledge
---

# Da agente di sessione a collaboratore con memoria di progetto

## Il problema nell'uso standard

Un agente AI può essere molto efficace durante una singola conversazione. Legge file, ragiona su un problema, propone modifiche e risponde alle domande. Ma il suo contesto è limitato e temporaneo. In una sessione successiva potrebbe non avere più i documenti studiati, le ragioni di una scelta o gli errori che hanno portato a scartare un'alternativa. Il team deve allora ripetere le spiegazioni o affidarsi a riassunti incompleti.

Mettere tutti i manuali, le decisioni e la cronologia del progetto nel prompt non risolve il problema: occupa il contesto con informazioni che in quel momento non servono. La domanda utile è un'altra: **come può l'agente ritrovare la conoscenza pertinente quando ne ha bisogno, e come può lasciarne di nuova al termine del lavoro?**

`kb-agentic` e `agentic-sdlc` affrontano insieme questa domanda. Conservano la conoscenza nei documenti del progetto e danno all'agente un metodo per consultarla, verificarla e aggiornarla. Il patrimonio documentale può crescere tra le sessioni senza dover entrare per intero nella finestra di contesto di ciascuna. Per il team, il risultato cercato è la continuità: **l'amnesia di una sessione non deve diventare amnesia del progetto**.

## Il folder di progetto: la condizione pratica

Per costruire questa continuità serve **un folder persistente che Claude o Codex apra come progetto di lavoro**. In quel folder il team organizza la conoscenza che vuole rendere disponibile all'agente: documenti, fonti, decisioni, guide e stato delle attività. È il progetto, non la cronologia di una chat, a custodire ciò che deve sopravvivere alle sessioni. Lo stesso folder può essere riaperto da un altro agente o da un collega, che trova i materiali al loro posto.

Le skill si installano nell'agente; **i contenuti che producono vivono nel folder del progetto**. Al suo interno `ai_docs/` raccoglie Vision, analisi, guide, indici e handoff; per il lavoro di conoscenza si aggiungono fonti, note e argomenti della KB. I file di istruzioni del progetto, come `CLAUDE.md` o `AGENTS.md`, aiutano l'agente a orientarsi in quel folder. Può essere il repository del software oppure un progetto dedicato alla conoscenza del team: ciò che conta è riaprire lo stesso patrimonio organizzato, non partire ogni volta da una cartella vuota.

Non occorre inserire tutti quei file nel prompt. L'agente legge indici e guide per scegliere cosa aprire, poi torna alle fonti pertinenti. Un manuale molto grande può avere nel progetto l'estrazione consultabile e il riferimento verificabile all'originale conservato altrove; la continuità richiede che anche quel riferimento rimanga accessibile. In questo senso possiamo parlare di una **«persona AI» di progetto**: non perché l'agente abbia ricordi personali continui, ma perché lavora ogni volta sullo stesso patrimonio di conoscenza, che il team può far crescere e correggere.

## Che cosa cambia nel lavoro quotidiano

| Situazione | Uso standard dell'agente | Con le due skill |
|---|---|---|
| Arriva un nuovo agente o inizia una nuova sessione | Si ricostruiscono contesto e decisioni dalla conversazione o da una ricerca libera. | Si apre lo stesso folder di progetto; l'agente si orienta tramite Vision, indici, guide, stato del lavoro e fonti pertinenti. |
| Si studia un manuale lungo | Le informazioni lette rischiano di sparire dal contesto; un riassunto può perdere condizioni e provenienza. | `kb-agentic` lavora per porzioni, registra l'avanzamento e collega le affermazioni a passaggi verificabili della fonte. |
| Due fonti si contraddicono | L'agente può scegliere implicitamente quella che trova per prima o che ricorda meglio. | Il conflitto resta visibile; una nuova fonte o una decisione motivata lo risolve senza cancellare la storia. |
| Si avvia una modifica software | L'agente può partire dal file più evidente e scoprire tardi vincoli, dipendenze o rischi. | `agentic-sdlc` calibra il processo sul rischio, verifica l'allineamento alla Vision e analizza l'impatto prima dell'implementazione. |
| Si risolve un problema difficile | La soluzione resta spesso nella chat o in una nota troppo breve per essere riusata. | Una GUIDE, quando è giustificata, conserva il modello operativo acquisito: fonti, vincoli, passaggi e ragioni delle scelte. |

Il vantaggio non dipende dal fatto che l'agente *ricordi già* ogni cosa. Dipende dalla sua capacità di trovare l'informazione giusta, riconoscerne stato e provenienza e usarla senza riempire il contesto di materiale irrilevante.

## `kb-agentic`: conoscenza che resta consultabile

`kb-agentic` è la disciplina per acquisire documenti e conoscenza di progetto. Mantiene distinguibili le fonti originali, le informazioni estratte, le interpretazioni e le decisioni delle persone. Organizza le affermazioni in una mappa di argomenti e ne conserva i riferimenti: quando l'agente risponde su un tema del progetto, può cercare nel patrimonio documentale e risalire a ciò che sostiene la risposta.

Questo conta soprattutto nel tempo. Un manuale può cambiare, una decisione può essere superata, due fonti possono riferirsi a versioni diverse. La skill prevede modi per rilevare conoscenza obsoleta, rendere espliciti i conflitti e rivedere i documenti perché descrivano lo stato corrente. Permette inoltre di lavorare su fonti grandi in finestre di lettura successive, registrando fin dove si è arrivati: il limite del contesto determina **quanto leggere alla volta**, non quanto il progetto possa conservare.

## `agentic-sdlc`: la conoscenza guida il cambiamento

`agentic-sdlc` applica un processo specifico al lavoro software. Il primo passo è il triage: una correzione banale richiede poco, mentre un cambiamento con impatto o rischio significativo richiede analisi, progetto e verifica più approfonditi. La **Vision** mantiene visibile il beneficio atteso e aiuta a riconoscere le modifiche che deviano dall'obiettivo.

Nel percorso governato con devPNT, tre artefatti osservano il cambiamento da prospettive complementari prima di scegliere la soluzione:

- **D-UC, casi d'uso:** chi ha bisogno di che cosa e perché.
- **D-IC, contratto d'interazione:** attraverso quali superfici e flussi gli attori useranno o percepiranno il cambiamento.
- **P-TM, modello delle minacce:** che cosa può andare storto su quelle superfici e quali protezioni servono.

Tutti e tre restano collegati al beneficio della Vision. L'**E-ISP** traduce questa comprensione in una mappa dell'impatto e in una proposta di soluzione; l'**E-TDD** descrive come realizzarla, file per file. Le review indipendenti controllano il progetto prima del codice e l'implementazione prima della chiusura. L'approvazione delle scelte di prodotto e delle proposte governate resta alle persone. Senza devPNT, la skill conserva un percorso Standalone nei file `ai_docs/`: gli artefatti e la governance hanno una forma diversa, ma la disciplina di analisi e verifica rimane.

## Il ciclo che fa crescere la competenza

Immaginiamo una richiesta che tocca un componente già studiato mesi prima. In un uso standard, l'agente potrebbe rifare l'indagine, ripetere un'alternativa già scartata e chiedere al team perché il codice ha una certa forma. Con le skill, consulta la decisione precedente e la GUIDE del componente, verifica che siano ancora valide, poi progetta la modifica alla luce del beneficio atteso e dei consumatori reali. Alla chiusura aggiorna la conoscenza che il cambiamento ha reso obsoleta e registra l'esperienza riutilizzabile emersa.

Questo è il rendimento del tempo speso per capire: una buona GUIDE non dice soltanto «fare attenzione al componente». Conserva **come funziona, dove sono i vincoli, quale errore si è incontrato, perché una soluzione è stata scelta e come verificarla**. La sessione successiva può partire da quella competenza invece di ricostruirla da zero.

Il ciclo funziona se il team mantiene una disciplina concreta: lavorare nello stesso folder di progetto, acquisire le fonti, distinguere fatti e decisioni, aggiornare ciò che cambia, consultare prima di agire e verificare il risultato. Installare le skill da solo non trasforma ogni chat in conoscenza affidabile. Sono queste pratiche, rese ripetibili dalle skill, a far crescere la memoria di progetto e la qualità del lavoro dell'agente.

## Cosa aspettarsi

Le due skill non attribuiscono all'agente memoria personale continua o giudizio umano. Offrono al team una **memoria esterna, consultabile e verificabile** e un **processo proporzionato al rischio** per usarla nel lavoro software. L'obiettivo è che un agente che arriva oggi possa ritrovare ciò che il team ha imparato ieri, applicarlo al problema presente e lasciare il progetto più comprensibile per chi arriverà domani.

### Riferimenti per approfondire

- [Processo e modalità Standalone di `agentic-sdlc`](../../skills/agentic-sdlc-skill/SKILL.md)
- [Metodo di acquisizione e consultazione di `kb-agentic`](../../distributions/kb-agentic-skill/skills/kb-agentic-skill/SKILL.md)
- [Processo congiunto `agentic-sdlc` × devPNT](process_agentic_sdlc_devpnt.md)
- [Differenze operative tra le skill della famiglia](skill_family_agent_workflows.md)
