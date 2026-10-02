Se dovessi spiegarlo a un nuovo collega, userei Orione come progetto ipotetico. In una chat senza metodo chiediamo all’agente di leggere un manuale e risolvere un problema: può dare una buona risposta, ma alla sessione successiva dobbiamo spesso ricostruire quali fonti ha letto, quale versione valeva e perché è stata presa una decisione. Con `kb-agentic` e `agentic-sdlc` mi aspetterei di conservare, rispettivamente, la conoscenza ricavata dalle fonti e il percorso che giustifica una modifica al software. Non ho consultato le due skill, quindi questa è una descrizione del modo in cui lavorerei, non delle loro regole formali.

Per un manuale di Orione partirei identificando titolo, versione e ambito. Leggerei le sezioni pertinenti, separando ciò che il manuale afferma dalle mie deduzioni. Se un collega chiede, per esempio, quanto dura una richiesta, formulerei una risposta circoscritta e citerei la sezione e la versione che la sostengono. Se la fonte non copre un caso, lo direi: una risposta citabile deve permettere al collega di ritrovare l’affermazione e verificarne i limiti.

Se due regole sembrano in conflitto, controllerei prima se parlano dello stesso caso: prodotto, versione, ambiente, destinatario ed eventuali eccezioni. Poi cercherei indicazioni esplicite su precedenza o sostituzione. Non sceglierei automaticamente la regola più recente. Se il conflitto resta, registrerei entrambe le formulazioni e chiederei una decisione a chi possiede la regola, evitando di presentare come certa una risposta che le fonti non consentono.

Per cambiare il timeout partirei dal beneficio atteso: quale problema vive l’utente e come sapremo che il cambiamento lo risolve? Verificherei il comportamento attuale, dove viene definito il timeout e chi dipende da quel valore. Definirei il comportamento desiderato e i casi limite, pianificherei la modifica, la implementerei e proverei sia il caso che motivava il lavoro sia gli effetti sugli altri chiamanti. In chiusura aggiornerei la documentazione pertinente e conserverei evidenza delle verifiche. Prima di chiamarlo “finito”, confronterei il risultato con il beneficio iniziale, non soltanto con il fatto che i test passano.

Intendo *Standalone* come lavoro mantenuto nei documenti e nel repository del progetto; con *devPNT* mi aspetterei anche un sistema dedicato per piani e artefatti soggetti a proposta e approvazione. Dovrei leggere le istruzioni effettive per dire quali documenti, strumenti e passaggi siano obbligatori nei due modi.

| Quando riprendiamo Orione | Ricostruzione che si evita | Verifica che resta necessaria |
|---|---|---|
| Dopo una settimana | Riscoprire fonti, decisione sul timeout e stato del lavoro | Controllare se codice, documenti e test corrispondono ancora allo stato registrato |
| Dopo un mese | Ricostruire dalle chat il motivo della scelta e le alternative considerate | Verificare versioni delle fonti, nuove dipendenze e validità dei risultati |
| Dopo anni | Ricostruire da zero storia e motivazioni di una regola o scelta tecnica | Rivalidare le assunzioni rispetto al prodotto e ai bisogni attuali |

Per avviare un caso analogo, leggerei in sola lettura un documento del mio progetto: ne controllerei versione e stato, estrarrei le affermazioni pertinenti con i loro riferimenti e verificherei se esistono fonti successive. Userei quei riferimenti per orientare l’indagine, senza inviare qui il documento né presumere che sia ancora valido.

**Materiali usati:** soltanto il testo del compito e conoscenze generali sul lavoro con fonti, modifiche software e verifiche. Nessun file, pacchetto corso o fonte online.

**Passaggi poco chiari:** le procedure esatte prescritte da `kb-agentic` e `agentic-sdlc`; i criteri formali per distinguere Standalone da devPNT; gli artefatti e le approvazioni richiesti per il caso del timeout.
