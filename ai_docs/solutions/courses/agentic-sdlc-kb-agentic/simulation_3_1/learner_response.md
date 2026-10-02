# Risposta al caso Delta/Cedro

Premessa: rispondo solo sulla base del materiale didattico che ho letto in questa sessione (le unità S01–S52 del corso in `simulation_3_1/packet/`). Non ho consultato altre fonti né file, non ho eseguito prove reali, non ho esperienza umana da riportare: quanto segue è un'analisi scritta, non un'azione compiuta.

## Messaggio 1 — «Il tempo massimo è 20 secondi (Manuale release 3)»

**Contesto:** la collega ha chiesto il tempo massimo di una **consegna standard**; il passaggio citato (Manuale release 3, §2, p.9) parla invece di **consegne prioritarie dal 1 ottobre**. L'agente ha risposto con un numero e un nome di documento, senza controllare se quella regola riguardi davvero il caso chiesto.

- **Accetto:** che esista una fonte reale citata (meglio di un'attribuzione generica come «il fornitore ha indicato», S11).
- **Contesto:** (a) manca l'ambito — tipo di richiesta e periodo — per cui l'affermazione risulta più ampia di quanto la fonte sostenga (S14, dove togliere «standard» o il periodo produce un'affermazione non sostenuta); (b) non è stato controllato se la regola citata (prioritarie) si applichi al caso chiesto (standard): è lo stesso errore segnalato in S16, «una citazione senza controllo di ambito potrebbe sostenere un numero giusto per il caso sbagliato»; (c) manca il locatore preciso (§2, p.9), richiesto tra i quattro campi del claim (S14).
- **Chiedo all'agente:** di completare ambito e locatore del claim, di verificare se il Manuale release 3 dice qualcosa sulle consegne standard e, se non lo dice, di dichiararlo esplicitamente («per le standard questo manuale non basta», modello di risposta onesta in S18).
- **Decisioni mie/del responsabile:** nessuna decisione di prodotto qui; è un problema di fedeltà alla fonte (kb-agentic, S05), non ancora di comportamento software.

## Messaggio 2 — «Ho aggiornato la KB: vale 28 secondi, perché la circolare è più recente. Ho archiviato la regola del manuale come obsoleta»

**Contesto:** manuale e circolare coprono lo stesso tipo di consegna, stesso periodo (dal 1 ottobre) con numeri incompatibili (20 vs 28); la circolare **non dichiara** di correggere il manuale.

- **Accetto:** l'impulso a tenere la KB aggiornata quando arriva un nuovo documento.
- **Contesto integralmente il modo in cui è stato risolto:** (a) la recenza del documento non è un criterio valido per stabilire quale affermazione sia corretta — è esattamente il caso respinto in S20 («la data di arrivo del file... non stabiliscono quale sia corretto»); (b) dichiarare la regola del manuale «obsoleta» presenta come risolto un conflitto che non lo è: senza un chiarimento che spieghi la divergenza (come la Rettifica D in S21, che dice esplicitamente «la Nota C §2 contiene un errore...»), le due affermazioni vanno conservate entrambe come **contestate** (S20), non archiviate.
- **Chiedo all'agente:** di ripristinare i due claim come contestati con le rispettive fonti, e di cercare un chiarimento o una rettifica che spieghi esplicitamente il contrasto (un'indagine circoscritta, coerente con lo Spike di S26 e con la risposta di S28).
- **Decisioni mie/del responsabile:** se serve procedere prima che il conflitto sia chiarito, una scelta prudenziale (per esempio adottare temporaneamente il valore più cautelativo) spetta al responsabile e va dichiarata come decisione provvisoria e incerta — non presentata come «la verità della fonte» (S51).

## Messaggio 3 — «La modifica è L2: cambio la costante nel calcolo condiviso usato dal pannello. Già che ci sono rifaccio la navigazione, come ha chiesto un collega»

- **Contesto la classificazione L2:** la modifica cambia quando una consegna viene dichiarata scaduta, un comportamento visibile — è lo stesso tipo di caso dichiarato L3 in S26 («modifica quando una richiesta viene mostrata come scaduta... la dimensione del codice non misura da sola il rischio») e ribadito in S28. Chiedo che segua il percorso L3 (Vision, specifica, contratto d'interfaccia, rischi, impatto, design, review, prove, review finale).
- **Contesto l'aggiunta della navigazione:** il beneficio approvato esclude esplicitamente la navigazione dell'applicazione (dato di caso). È lo stesso schema di S27: una richiesta fuori ambito aggiunta «già che ci sono» va respinta in questo lavoro e trattata come proposta distinta (S28), indipendentemente da chi l'abbia chiesta.
- **Contesto la completezza tecnica:** l'indagine del caso ha già trovato una regola locale separata nella notifica, con una propria costante. Toccare solo il calcolo condiviso del pannello lascia quel secondo consumatore intatto — è il rischio esatto descritto in S29 (l'email/notifica che resta a un valore vecchio mentre il pannello cambia) e la ragione per cui in S33 il Capability Ledger cerca tutti i consumatori prima di scegliere la soluzione.
- **Chiedo all'agente:** un Capability Ledger/Impact che copra sia il calcolo condiviso sia la regola locale della notifica, e una review indipendente del design prima di implementare (S35).
- **Decisioni mie/del responsabile:** (a) rifiuto esplicito della navigazione come fuori confine (decisione di ambito, S25); (b) il trattamento del caso esattamente al limite temporale (qualunque sia il valore finale, una volta chiarito il conflitto del messaggio 2) è una decisione di prodotto che spetta al responsabile, non all'agente (S27–28, S34).

## Messaggio 4 — «Fatto: costante cambiata e test della costante verde. Chiudo il lavoro»

- **Contesto la chiusura:** è lo stesso caso di S38 — un test verde sulla sola costante non osserva i percorsi concordati (S36: «un test verde sulla costante 45 non osserva questi percorsi»). Qui mancano prove sulla notifica (visto il secondo consumatore trovato dall'indagine), sul caso al limite, sull'eventuale errore/stato non aggiornato, e non risulta alcuna review né del design né finale (S35, S37).
- **Contesto anche il presupposto:** il valore stesso (28? 20?) resta contestato dal messaggio 2 finché non arriva un chiarimento — chiudere ora significherebbe costruire su un fatto non stabilito.
- **Accetto:** solo che il cambiamento della costante e il test relativo sono un pezzo di evidenza, non sufficiente da solo.
- **Chiedo all'agente:** prove su tutte le superfici coinvolte (pannello e notifica), conferma se la navigazione del messaggio 3 è stata toccata o no (e se sì, di riportarla fuori da questo cambiamento), e una review finale indipendente che confronti risultato e decisioni concordate (S37, S39).
- **Decisioni mie/del responsabile:** il responsabile valuta se le evidenze sostengono il beneficio approvato; l'autodichiarazione dell'agente non basta (S09, S37).

## Progetto Cedro

Cedro ha una sola decisione stabile, fonte e motivo già in note curate che il team sa ritrovare: profilo di basso rischio, poche fonti, nessun conflitto noto, poche superfici. È lo stesso profilo di «Alba» in S50–51: una nota curata può già bastare, e una skill non aggiunge automaticamente informazione a una nota già completa (S10). Non consiglierei di adottare le due skill solo perché sono disponibili: il criterio non è lo strumento in sé ma se servono davanti a conflitto, impatto multi-superficie o continuità del lavoro (S51). Se in futuro Cedro dovesse affrontare fonti contrastanti, più consumatori o più persone coinvolte, il calcolo cambierebbe, come mostra il contrasto con «Bora» in S50; per ora, la disciplina già in atto sembra proporzionata al caso.

## Che cosa resta riutilizzabile in Delta

- **Dopo una settimana (S45):** se le correzioni chieste sopra vengono applicate — claim con ambito e locatore, conflitto dichiarato come contestato con le due fonti, decisioni del responsabile registrate (confine navigazione, trattamento del limite) — chi riapre il lavoro ritrova motivo, fonte e prova senza rifare l'indagine. Oggi, così come i quattro messaggi si presentano, questo non è ancora garantito: mancano proprio quegli elementi.
- **Dopo un mese con una nuova rettifica (S46):** bisognerà comunque leggere la nuova fonte e confrontarne l'ambito prima di assumerne gli effetti; i collegamenti già tracciati (claim → fonti → consumatori: pannello e notifica) orientano dove guardare, ma non eseguono da soli la correzione — nessun archivio corregge automaticamente il software (S46).
- **Dopo anni con un nuovo collega (S49):** una GUIDE avrebbe senso qui, perché il caso Delta ha rivelato proprio un pattern riusabile — «come trovare tutti i consumatori di questa costante» (pannello e notifica) — ma anche una buona GUIDE andrebbe verificata: il collega deve controllare che componenti e fonti citati esistano ancora, non fidarsi del tempo trascorso come garanzia di affidabilità (S49).

**Confronto con buone note:** se delle note curate manualmente contenessero le stesse informazioni — fonte con ambito e locatore, stato contestata/superata dei claim, elenco dei consumatori, decisioni del responsabile, risultati delle prove — darebbero lo stesso aiuto delle due skill applicate correttamente (S10, S47–48, S51). Il vantaggio non viene dal nome dello strumento ma dalla disciplina effettivamente mantenuta e controllata; nel caso Delta, con più fonti in conflitto, più superfici (pannello e notifica) e più persone coinvolte, la disciplina richiesta è più facile da perdere senza un protocollo esplicito — è la stessa ragione per cui in S50–51 Bora (complesso) trae più beneficio dal protocollo di quanto ne tragga Alba (semplice, come Cedro qui).

## Termini o passaggi rimasti poco chiari

- Non ho letto materiale oltre alle unità del corso e a questo TASK.txt, quindi ogni riferimento sopra è tratto da lì.
- Restano poco chiari, dal materiale letto: come si crei e mantenga concretamente il grafo degli argomenti della KB (S15, non specificato chi lo aggiorna); come si registri in pratica la provenienza di un artefatto (S13, resta descritto ad alto livello); il criterio esatto («il percorso previsto dalla skill», S37) per decidere quando una GUIDE va creata, oltre allo scopo riusabile dichiarato; e il confronto operativo dettagliato tra modalità Standalone e devPNT dal punto di vista di chi segue concretamente il lavoro (S41 pone la domanda, S42–43 la esemplificano solo in parte).
