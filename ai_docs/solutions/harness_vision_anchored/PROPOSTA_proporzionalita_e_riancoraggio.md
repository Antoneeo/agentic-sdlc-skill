# Proposta: proporzionalità dei requisiti e riancoraggio alla vision dopo FAIL ripetuti

Origine: un caso di un altro progetto, 2026-11-15 (il materiale del caso è tenuto fuori dal repository). L'invariante della vision chiedeva che chi esegue un workflow protetto non ottenga la **definizione intera**. D-IC, P-TM e nodo l'hanno stretto in «nessuna chiave in nessun errore». Quattro giri di revisione sono falliti per mancanza di meccanismo, e nessuno ha messo in dubbio il requisito. Al giro 5 il requisito è stato riportato al test della vision ed è arrivato il PASS.

Due modifiche, ciascuna in due posti: la dottrina devPNT (fonte del blocco gestito in `CLAUDE.md`) e la skill `agentic-sdlc`. Il testo è in inglese come i documenti di destinazione.

Replay sul caso di origine: con il testo attuale, i giri 1–4 restano FAIL e il requisito non si discute mai. Con il testo nuovo, la modifica 1 ferma l'allargamento di S2.6 alla stesura del D-IC: «nessuna chiave» va oltre «definizione intera». Se l'allargamento fosse passato comunque, la modifica 2 obbliga al giro 2 a rileggere MV§7, e la domanda sarebbe arrivata a te due giri prima.

---

## Modifica 1: proporzionalità (il controllo guarda anche verso l'eccesso)

### 1a. Dottrina devPNT, §4.2 «Vision Alignment Gate». Nuovo punto fra il 3 e il 4

> 3b. **Proportionality check (the gate cuts both ways).** Divergence is not only scope added; it is also a constraint made stricter than the vision clause it serves. For every requirement in the artifact that *restricts* (a protection, a prohibition, a closed list, a "never"), name the M-VISION clause that justifies it and state that clause's own test. If the requirement demands more than that test — it forbids what the test allows, or it is stricter than the test's wording ("the full definition" becoming "any key") — it is a divergence, routed like any other: tighten the requirement back to the test, or bring the stricter reading to the user as a vision-level decision. Check in particular whether the extra strictness takes away something the vision promises elsewhere (an invariant that says what must stay available). A protection that the vision did not ask for is not "extra safety". It is unauthorized scope that rations a benefit.

### 1b. Skill, `SKILL.md` §1 «Audit and Alignment», Hybrid, dopo «If the request adds unauthorized scope, treat it as a Vision divergence.»

> - A requirement stricter than the Vision clause it cites is a divergence too: every restriction names its clause and does not exceed that clause's test (devPNT §4.2, proportionality check). Over-protection that takes away something the Vision promises is unauthorized scope, even when it is labelled safety.

(Facoltativo: la stessa riga nel ramo Standalone, sopra, perché la regola non dipende da devPNT.)

---

## Modifica 2: riancoraggio dopo FAIL ripetuti sulla stessa classe

### 2a. Dottrina devPNT, §4.5 «Procedure», punto 4. Da inserire dopo «FAIL → revise the draft and re-review.»

> **Re-anchor before the second revision of the same class.** When a review FAILs for the second time on findings of the same class (the same requirement, surface or property, even if the instances differ), do not add another mechanism first. Re-read the M-VISION clause the requirement traces to and ask whether the requirement is proportionate to that clause's test (§4.2, proportionality check). If it is not, the fix is to the requirement — routed to its owner (the user for a D-IC or vision-level reading) — not another round on the artifact. Record the outcome of this question in the review's notes either way. The rounds a gate spends hunting the instances of an over-broad requirement are rounds that grow complexity without serving the vision.

### 2b. Skill, `review.md`, dopo il paragrafo «Rounds are capped at 3…» (riga 183–185)

> **Re-anchor on the second FAIL of the same class.** Two FAILs on findings of the same class mean the requirement may be wrong, not only the artifact. Before the next revision, re-read the Vision clause the requirement serves and check it against that clause's test. If the requirement exceeds the test, take the question to whoever owns the requirement (the owner, for a Vision-level reading) instead of adding mechanism. Write the answer in the REVIEW_LOG notes. A third round that only adds mechanism to an unexamined requirement is a red flag.

---

## Da decidere

1. Approvi il testo?
2. Chi lo applica: tu nella sorgente di devPNT e del pacchetto della skill, o io sulla copia locale della skill (`~/.claude/skills/agentic-sdlc`)? Il blocco devPNT in `CLAUDE.md` va cambiato nella sorgente, altrimenti devPNT lo riscrive.
