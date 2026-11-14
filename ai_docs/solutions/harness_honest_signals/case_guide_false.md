# Caso: guida operativa rimasta falsa alla chiusura di un nodo, con il controllo CLEAN

Commit sorgente: `6aadb806` (stato alla chiusura del nodo) e `a25e4eff` (dopo la correzione), entrambi del 2026-11-14. I testi della guida sono copie di `git show <commit>:<percorso>`; nulla è stato letto dall'albero di lavoro.

## Come leggere questa copia

- Le copie sono redatte: nomi di persone, prodotti, host, domini, percorsi di server, contenitori, servizi, pacchetti, variabili, identificativi e ogni dettaglio di sicurezza sono sostituiti da `[REDACTED: <tipo>]`.
- Dopo un testo redatto, la frase introdotta da «descrive:» è una caratterizzazione scritta da chi ha fatto la copia: dice di che GENERE di cosa parlava il testo. Non è una citazione.
- Sono riprodotte alla lettera le frasi di stato che rendevano falsi i paragrafi, le date, i verbi e tutto il testo non sensibile.
- Il filone a cui appartiene il nodo chiuso è indicato come `Filone-44`: la numerazione prosegue quella del caso del registro (`case_registry_40.md`), dove questo filone non ha riga. La corrispondenza con il nome vero non è in questo file.

## La guida

- Percorso: `ai_docs/reference/GUIDE_[REDACTED: argomento].md`
- Che cos'è: una guida operativa per un server di produzione, sotto `ai_docs/reference/`.
- Lunghezza: 129 righe in `6aadb806`, 130 in `a25e4eff`.
- Differenza tra i due commit su questo file (`git diff --stat`): 3 righe inserite, 2 tolte, in due punti: i due paragrafi qui sotto e il registro in fondo.

Frontmatter (identico nei due commit: tra i due cambiano solo le righe 95, 97 e la riga aggiunta al registro in fondo):

```yaml
---
description: [REDACTED: descrizione] — descrive: a che cosa serve la guida (come l'agente accede al server di produzione, che cosa può e non può fare, regole operative, preparazione da zero, revoca, diagnosi, registro delle modifiche) e quando va letta (prima di ogni sessione che opera sul server e prima di cambiarne le credenziali o la configurazione di accesso)
status: CURRENT
source_kind: document
source: Indicazioni di [REDACTED: persona] e setup eseguito nella sessione del 2026-10-29
source_version: 2026-11-01
distilled_from: ai_docs/reference/.sources/[REDACTED: nome di file].md
source_hash: [REDACTED: impronta]
---
```

## Stato alla chiusura del nodo

Il nodo è stato chiuso mentre i due paragrafi erano come nel commit `6aadb806`. Copia redatta, da `git show 6aadb806:<percorso>`, righe 95 e 97–106.

Primo paragrafo (riga 95):

> **`[REDACTED: nome di file]` pubblicato dal proxy, in forma provvisoria** (2026-11-14). `[REDACTED: URL]` risponde 200 `application/json` (pacchetto `[REDACTED: nome di pacchetto app]`, [REDACTED: dettaglio di sicurezza] — descrive: quale chiave è dichiarata nel file): lo serve un terzo file non versionato del volume `[REDACTED: nome di volume]`, `[REDACTED: percorso sul server]`, accanto ai due di `[REDACTED: servizio]`. Non è nel repo né nel compose: chi rigenera il proxy o ricrea il volume lo perde. Per toglierlo: `[REDACTED: comando sul server]`, poi `[REDACTED: comando sul server]`. Resta aperto: riportarlo nel repo come rotta dell'applicazione, [REDACTED: dettaglio di sicurezza] — descrive: con quale chiave; il reindirizzamento dall'indirizzo senza `www` non è stato fatto ([REDACTED: id di backlog]). Fatto riportato dalla sessione dello Spike [REDACTED: argomento] (`[REDACTED: percorso di documento]`); la coordinatrice ha verificato da fuori solo la risposta 200.

Secondo paragrafo (riga 97, con la tabella delle righe 99–104):

> **[REDACTED: funzione di prodotto] — descrive: nome della funzione rilasciata (Filone-44 U1, codice del 2026-11-14, non ancora in produzione).** Il modulo `[REDACTED: nome di modulo]` legge quattro variabili di `[REDACTED: file di configurazione]`; vuote, la funzione è spenta e nulla cambia:
>
> | Variabile | Valore da mettere | Significato |
> |---|---|---|
> | `[REDACTED: variabile 1]` | `[REDACTED: host]` | [REDACTED: dettaglio di prodotto] — descrive: a che cosa serve il valore e che cosa accade se è vuoto |
> | `[REDACTED: variabile 2]` | `[REDACTED: host]` | [REDACTED: dettaglio di sicurezza] — descrive: quali richieste sono trattate e quali sono escluse |
> | `[REDACTED: variabile 3]` | `[REDACTED: nome di pacchetto app]` | [REDACTED: dettaglio di prodotto] — descrive: dove compare il valore |
> | `[REDACTED: variabile 4]` | [REDACTED: dettaglio di sicurezza] — descrive: quale valore è in uso oggi, con un'impronta abbreviata | [REDACTED: dettaglio di sicurezza] — descrive: formato del valore e comportamento con valori non validi |

Capoverso che segue la tabella (riga 106). Non era tra i due richiesti; è riportato perché è **identico nei due commit** e contiene anch'esso una frase di stato:

> **[REDACTED: dettaglio di sicurezza] — descrive: un valore da togliere da una variabile prima della pubblicazione su uno store**: [REDACTED: dettaglio di sicurezza] — descrive: quale valore resta, un effetto di cache nei browser, conferme da ottenere presso due fornitori terzi prima di impostare una variabile, con rimando a un paragrafo del disegno tecnico. Dopo il deploy la rotta dell'applicazione sostituisce il file provvisorio del proxy, che va tolto su ordine di [REDACTED: persona] con i due comandi qui sopra ([REDACTED: comandi sul server]): finché c'è, vince il proxy. Rimozione del file del proxy: non ancora fatta (da annotare qui con la data). Verifica dopo il deploy: `[REDACTED: comando]`, sezioni [REDACTED: nomi di sezione].

## Riga aggiunta al registro in fondo alla guida

La tabella del registro in fondo alla guida ha le colonne `| Data | Modifica | Chi |`. Questa è la sola riga presente in `a25e4eff` e assente in `6aadb806` (da `git diff 6aadb806 a25e4eff -- <percorso>`, secondo blocco, riga con `+`):

```
| 2026-11-14 | File `[REDACTED: percorso sul server]` rimosso da [REDACTED: persona] dopo il deploy di `6aadb806`: `[REDACTED: nome di file]` lo serve ora l'applicazione (`[REDACTED: nome di modulo]`, variabili `[REDACTED: variabile 3]` e `[REDACTED: variabile 4]`); attivo il 301 da `[REDACTED: host]` a `www` (`[REDACTED: variabile 1]`, `[REDACTED: variabile 2]`); copia `[REDACTED: nome di file]` in `[REDACTED: percorso sul server]` | [REDACTED: persona], passi del rilascio di Filone-44 U1 ([REDACTED: id di richiesta]) |
```

La riga immediatamente precedente, presente in entrambi i commit, porta la stessa data:

```
| 2026-11-14 | `[REDACTED: nome di file]` servito dal proxy: file `[REDACTED: percorso sul server]` nel volume `[REDACTED: nome di volume]` di `[REDACTED: contenitore]`, non versionato; [REDACTED: dettaglio di sicurezza] — descrive: che cosa NON è stato modificato nell'accesso al server | sessione dello Spike [REDACTED: argomento], su parole di [REDACTED: persona] ([REDACTED: id di richiesta]) |
```

## Output del controllo, testuale, visto dalla coordinatrice alla chiusura

```
[ok] workstream registry regenerated: [percorso]/ai_docs/audit/handoff.md
[warn] 40 open workstreams: the registry is meant to stay under 20. Nothing was truncated -- closing one is the fix.
[ok] project memory regenerated: [percorso]/ai_docs/memory/INDEX.md
Validation: 0 errors, 407 warnings, 22 advisories.
[note] advisories are freshness signals: never fail a build, not even --strict.

===== stale =====
[info] hybrid mode: audit-plan staleness is delegated to devPNT/KL, skipping.

check: CLEAN (validate rc=0, stale rc=0)
```

[Le prime righe dell'output di validate non sono state conservate: la coordinatrice ne ha letto solo la coda.]

## Dopo la correzione

Gli stessi due paragrafi nel commit `a25e4eff`. Copia redatta, da `git show a25e4eff:<percorso>`, righe 95 e 97–106.

Primo paragrafo (riga 95). Cambia solo l'apertura, fino alla prima parentesi chiusa; il resto è identico a prima:

> **`[REDACTED: nome di file]` pubblicato dal proxy: forma provvisoria, RITIRATA il 2026-11-14** (file rimosso da [REDACTED: persona] dopo il deploy di `6aadb806`; da allora lo serve l'applicazione, vedi il paragrafo seguente; il resto di questo paragrafo descrive lo stato precedente). `[REDACTED: URL]` risponde 200 `application/json` (pacchetto `[REDACTED: nome di pacchetto app]`, [REDACTED: dettaglio di sicurezza] — descrive: quale chiave è dichiarata nel file): lo serve un terzo file non versionato del volume `[REDACTED: nome di volume]`, `[REDACTED: percorso sul server]`, accanto ai due di `[REDACTED: servizio]`. Non è nel repo né nel compose: chi rigenera il proxy o ricrea il volume lo perde. Per toglierlo: `[REDACTED: comando sul server]`, poi `[REDACTED: comando sul server]`. Resta aperto: riportarlo nel repo come rotta dell'applicazione, [REDACTED: dettaglio di sicurezza] — descrive: con quale chiave; il reindirizzamento dall'indirizzo senza `www` non è stato fatto ([REDACTED: id di backlog]). Fatto riportato dalla sessione dello Spike [REDACTED: argomento] (`[REDACTED: percorso di documento]`); la coordinatrice ha verificato da fuori solo la risposta 200.

Secondo paragrafo (riga 97). Cambia l'apertura in grassetto e si aggiunge una frase sul rilascio; la frase sul modulo e la tabella sono identiche a prima:

> **[REDACTED: funzione di prodotto] — descrive: nome della funzione rilasciata (Filone-44 U1, in produzione dal 2026-11-14 con `6aadb806`).** Rilascio eseguito da [REDACTED: persona]: [REDACTED: passi sul server di produzione] — descrive: cinque passi separati da punto e virgola (indirizzi di ritorno provati presso fornitori terzi; le quattro variabili aggiunte al file di configurazione, con una copia di riserva; il comando di deploy, con una indisponibilità del sito di circa quattro minuti durante l'avvio; file del proxy rimosso e proxy rigenerato; verifica da fuori con due strumenti). Il modulo `[REDACTED: nome di modulo]` legge quattro variabili di `[REDACTED: file di configurazione]`; vuote, la funzione è spenta e nulla cambia:
>
> | Variabile | Valore da mettere | Significato |
> |---|---|---|
> | `[REDACTED: variabile 1]` | `[REDACTED: host]` | [REDACTED: dettaglio di prodotto] — descrive: a che cosa serve il valore e che cosa accade se è vuoto |
> | `[REDACTED: variabile 2]` | `[REDACTED: host]` | [REDACTED: dettaglio di sicurezza] — descrive: quali richieste sono trattate e quali sono escluse |
> | `[REDACTED: variabile 3]` | `[REDACTED: nome di pacchetto app]` | [REDACTED: dettaglio di prodotto] — descrive: dove compare il valore |
> | `[REDACTED: variabile 4]` | [REDACTED: dettaglio di sicurezza] — descrive: quale valore è in uso oggi, con un'impronta abbreviata | [REDACTED: dettaglio di sicurezza] — descrive: formato del valore e comportamento con valori non validi |

Capoverso che segue la tabella (riga 106): **non modificato** dalla correzione. In `a25e4eff` contiene ancora, alla lettera:

> Dopo il deploy la rotta dell'applicazione sostituisce il file provvisorio del proxy, che va tolto su ordine di [REDACTED: persona] con i due comandi qui sopra ([REDACTED: comandi sul server]): finché c'è, vince il proxy. Rimozione del file del proxy: non ancora fatta (da annotare qui con la data).

mentre il primo paragrafo dello stesso commit dice «RITIRATA il 2026-11-14 (file rimosso da [REDACTED: persona] …)» e la riga di registro dice «rimosso».

## Frasi di stato a confronto

| Punto della guida | In `6aadb806` (alla chiusura) | In `a25e4eff` (dopo) |
|---|---|---|
| Primo paragrafo, apertura | «pubblicato dal proxy, in forma provvisoria** (2026-11-14)» | «pubblicato dal proxy: forma provvisoria, RITIRATA il 2026-11-14**» |
| Secondo paragrafo, apertura | «codice del 2026-11-14, non ancora in produzione» | «in produzione dal 2026-11-14 con `6aadb806`» |
| Capoverso dopo la tabella | «Rimozione del file del proxy: non ancora fatta (da annotare qui con la data).» | identico |
| Registro in fondo | riga del 2026-11-14 «servito dal proxy» | la stessa, più la riga del 2026-11-14 «rimosso … dopo il deploy» |
| Frontmatter `status` | `CURRENT` | `CURRENT` |
| Frontmatter `source_version` | `2026-11-01` | `2026-11-01` |

## Sequenza dei fatti

Dal registro della coordinatrice:

1. Rilascio in produzione eseguito dal proprietario.
2. La coordinatrice aggiunge la riga di registro in fondo alla guida.
3. Il proprietario approva la chiusura del nodo.
4. La coordinatrice esegue `index` e `check --hybrid`: CLEAN; nodo DONE.
5. Più tardi il proprietario chiede se quanto fatto sul server sia stato salvato in una guida; la coordinatrice rilegge e trova i due paragrafi falsi.
6. Il proprietario: «ma come mai non tieni aggiornate le guide senza che io te lo ricordi?»
7. I due paragrafi vengono riscritti.

Nota sulla fonte git: i passi 2 e 7 sono nello stesso commit (`a25e4eff`). Lo stato intermedio — riga di registro aggiunta, paragrafi ancora come in `6aadb806` — è esistito solo nell'albero di lavoro e non è recuperabile da git: [NON TESTUALE — da registro della coordinatrice].

## Seguito, stesso giorno

La frase rimasta falsa dopo la prima correzione («Rimozione del file del proxy: non ancora fatta (da annotare qui con la data)») non è stata trovata dalla coordinatrice, che aveva riscritto i due paragrafi cercandoli per il loro inizio. L'ha trovata l'agente incaricato di preparare questa copia, confrontando i due commit. La coordinatrice l'ha riscritta subito dopo. Quindi la correzione fatta a mano, mirata alle frasi già note, ha lasciato a sua volta una frase falsa: tre frasi sullo stato di prima, due trovate dopo la domanda del proprietario, una trovata per caso da un terzo lettore. Il controllo dei documenti era CLEAN in tutti e tre i momenti.
