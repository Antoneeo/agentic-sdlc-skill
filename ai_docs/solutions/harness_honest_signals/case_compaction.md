# Caso: dopo una compattazione, metà dello scopo di un lavoro attivo non è nel riassunto

Data: 2026-11-14. Sessione coordinatrice, client Claude Code (app desktop). Copia ripulita per un repository pubblico: nomi di prodotto, identificativi e dettagli di sicurezza sono sostituiti da `[REDACTED: <tipo>]`. Il milestone è chiamato `Milestone-X`.

Tutte le citazioni sotto sono testuali, salvo le sostituzioni dichiarate. Il riassunto di compattazione è in inglese perché così lo ha prodotto il client.

## 1. Che cosa conteneva il riassunto di compattazione su Milestone-X

Il riassunto nomina Milestone-X in quattro punti. Li riporto tutti; non ce ne sono altri.

Nella sezione «Files and Code Sections», fra i documenti accettati:

> **devPNT accepted this stretch:** `use_cases_[REDACTED: slug del milestone]` v1.2; `threat_model_[REDACTED: slug del milestone]` v1.1 and v1.2; […]. Rejected: Milestone-X D-IC `[REDACTED: id]` and `[REDACTED: id]`. **Pending for [REDACTED: nome del proprietario]:** Milestone-X D-IC `[REDACTED: id]`.

Nella sezione «Problem Solving»:

> **Milestone-X:** facts from source (reported, not verified by me): [REDACTED: dettaglio di prodotto — descrive: una regola sulle licenze degli utenti]; in a [REDACTED: nome di prodotto] the [REDACTED: nome di prodotto] receives sibling-chat titles but cannot search their notes in four cases ([REDACTED: dettaglio di prodotto — elenca i quattro casi]).

Nella sezione «Pending Tasks», fra le domande aperte per il proprietario:

> 8. Milestone-X: no sibling-chat titles when the [REDACTED: nome di prodotto] cannot search their notes? (then present D-IC `[REDACTED: id]`).

Nell'elenco delle sessioni aperte: il solo nome della sessione che lavora su Milestone-X.

**Ciò che il riassunto dice di Milestone-X è quindi un solo argomento:** i titoli e la ricerca delle note delle chat «sorelle». Era l'argomento discusso nelle ore prima della compattazione. Il riassunto non dice che cosa Milestone-X è, né che cosa contiene oltre a quell'argomento.

## 2. Che cosa conteneva la vision, e dove

Documento governato in devPNT, chiave `milestone_vision_[REDACTED: slug del milestone]`, versione approvata. Raggiungibile con una sola chiamata (`devpnt_md_request_documentation`, `LATEST`).

Sezione «Problema», testuale salvo le sostituzioni:

> Due casi reali, oggi:
>
> 1. **La [REDACTED: nome di prodotto] non sa che cosa la persona possiede.** […]
> 2. **La compattazione perde dettagli.** «Evitare che la compattazione automatica comporti la perdita di dettagli importanti.» Oggi il riassunto è l'unica cosa che resta dei messaggi sostituiti, e il loro testo non è più recuperabile.

Sezione «North star», testuale salvo le sostituzioni:

> **La [REDACTED: nome di prodotto] sa che cosa la persona ha in [REDACTED: nome di prodotto] — quanti progetti di ciascun tipo, quante note di ciascun tipo — anche quando non li ha davanti. E quando una conversazione lunga viene compattata, i dettagli importanti restano in note che la persona vede e gestisce. Vale anche per una chat che dura anni.**

Sezione «Portata», secondo punto, testuale:

> - **Note di dettagli ricordati** alla compattazione di una chat.

La vision ha dunque due metà. Il riassunto ne conservava una parte della prima. La seconda metà è la risposta alla domanda del proprietario.

## 3. La domanda del proprietario e la prima risposta

Domanda, testuale:

> la feature per l'aggiunta dei dettagli da salvare alle note in fase di compattazione è stata fatta?

Che cosa ha fatto la coordinatrice prima di rispondere, nell'ordine [NON TESTUALE — dalla sequenza delle chiamate agli strumenti nella conversazione]: una ricerca testuale nel registro dei difetti, nel registro dei lavori e nella cartella della vision; una ricerca nel codice; un elenco dei documenti e dei file di codice che nominano la compattazione; una ricerca nel registro dei difetti con un altro termine; la lettura dell'intestazione di un documento di analisi (Spike) trovato così. Non ha letto la vision di Milestone-X.

Prima risposta, testuale salvo le sostituzioni (la parte su un altro lavoro è omessa):

> No, non è fatta: oggi la compattazione non scrive nessuna nota. L'ho ricontrollato nel codice del consolidamento, dove non c'è alcun punto che ne crei una.
>
> Esiste solo la parte di progetto:
> - **Analisi** del 14 novembre ([REDACTED: nome di file]): raccomanda una nota «dettagli ricordati» per ogni compattazione, scritta insieme al riassunto e prima di togliere i messaggi.
> - **Milestone-X**: vision approvata, casi d'uso, contratto d'interfaccia e modello delle minacce accettati oggi. Manca l'analisi d'impatto, poi il progetto tecnico, poi il codice. Do per buono che la nota alla compattazione stia dentro Milestone-X: lo dicono l'analisi e il registro, non ho riletto la vision ora.
>
> Quindi il codice non parte prima di due documenti ancora da scrivere; la sessione di Milestone-X è al lavoro sul primo.

Seconda domanda del proprietario, testuale:

> ok ma ne avevamo parlato.. non c'era una milestone per quello?

Solo a questo punto la coordinatrice ha letto la vision (una chiamata) e ha risposto, testuale salvo le sostituzioni:

> Sì, la milestone c'è ed è proprio Milestone-X, quella su cui stiamo lavorando oggi. Ho riletto ora la sua vision approvata: contiene la «nota di dettagli ricordati», cioè la nota che [REDACTED: nome di prodotto] scrive da sé subito prima di una compattazione con i dettagli dei messaggi che stanno per essere sostituiti, visibile e gestibile dalla persona fra le note della chat.

Terza domanda del proprietario, testuale:

> e come mai non hai subito collegato che ti stavo chiedendo di Milestone-X?

Risposta della coordinatrice, testuale salvo le sostituzioni:

> Perché la mia conversazione era stata compattata poco prima, e nel riassunto che mi è rimasto Milestone-X compariva solo per la parte di oggi: i titoli e la ricerca nelle note delle chat sorelle. La metà sulla nota alla compattazione non c'era, quindi ho dovuto ritrovarla nel registro e nel codice invece di saperlo.
>
> […]
>
> L'errore mio è stato un altro: alla prima domanda dovevo rileggere subito la vision di Milestone-X, che è un documento solo, invece di cercare nel codice e risponderti con un «do per buono». L'ho fatto solo alla tua seconda domanda.

## 4. Che cosa il caso misura

- La risposta di fatto («non è fatta») era giusta alla prima domanda. Ciò che mancava era il legame con il lavoro attivo, e la certezza: «do per buono» al posto di una citazione.
- Costo: cinque ricerche e una lettura al posto di una lettura; due domande del proprietario al posto di una.
- La vision era raggiungibile con una chiamata per chiave. Il nome del milestone era nel riassunto. Nulla nel metodo diceva di rileggerla alla ripresa.
- Alla ripresa dopo la compattazione l'orientamento di inizio sessione è stato emesso (README, indice, router delle guide, registro dei lavori). Non contiene le vision dei lavori attivi, né un rimando a rileggerle.

## 5. Che cosa manca in questo file

- Il testo intero del riassunto di compattazione: riportati solo i passi che nominano Milestone-X.
- Il testo delle vision al di fuori dei tre passi citati.
- Gli argomenti esatti delle ricerche: descritti, non citati.
