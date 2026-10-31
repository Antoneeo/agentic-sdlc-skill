# F-088 replay cases — chatPNT M155, 2026-10-23 → 2026-10-31

Each case is a recorded episode of several sessions working on one repository (chatPNT,
`D:\SoftwareDev\chatPNT`), one of them coordinating («Agentic SDLC situazione»). Sources are
that project's `ai_docs/audit/requests/REQUEST_ui_uniform_style.md` (cited `UUS#R<n>`),
`ai_docs/audit/HANDOFF_m155_w8.md` and its git history. Quotations are data.

The replay question, the same for every case: **under the doctrine text given, is the
observed behaviour a violation, or a situation the text tells an agent how to handle?**
Answer FLAGGED with the line that does it, or NOT FLAGGED.

## C1 — the same request-record numbers used by three sessions
Waves 5, 6 and 8 each appended entries to the one shared record at the same time and
numbered them R156–R158 independently. UUS#R158 notes «R156 è usato due volte (ondata 6 e
ondata 5)»; UUS#R161: «Le voci R159–R161 dell'ondata 6 erano state scritte come R156–R158
mentre le sessioni delle ondate 5 e 8 usavano gli stessi numeri: rinumerate dalla sessione
dell'ondata 6.» An entry cited by number before the renumbering points at another session's
decision.

## C2 — a delegate overrides an earlier decision of the owner
The owner delegated to the coordinating session the approval of design boards and «le
risposte consigliate» (UUS#R169, confirmed R174). Under it the coordinator chose to remove
`embeddable_chat.html` (UUS#R176). That choice superseded, for the whole file, the owner's
own decision M150.A4.4b of 2026-10-18. A design document (E-ISP 6d v1.0) was accepted on it.
The next day the coordinator withdrew: «ritiro la mia scelta […] Sostituirebbe la decisione
M150.A4.4b di Antonio per l'intero file, quindi decide lui» (UUS#R177).

## C3 — an authorization given in one session, an act needed in another
The owner wrote to the coordinating session «autorizzo l'ondata 8 e la pubblicazione sulla
tela» (UUS#R223). The wave-8 session, which had to publish, had the publication refused by
its own permission check; the owner then wrote «ti avevo già detti di si prima» (UUS#R226),
and the coordinator published itself, «con l'autorizzazione esplicita di Antonio nella propria
sessione». No text tells a session whether a relayed «Antonio autorizza» counts.

## C4 — a decision taken on a fact that turned out false
The coordinator decided Q5 of increment 5h (UUS#R243). The next entry: «la Q5 della 5h,
decisa in R243, partiva da un fatto sbagliato, e la coordinatrice la decide di nuovo»; it
verified three facts first and decided again as a new entry (UUS#R244). R243 was not edited.

## C5 — a part stops mid-closure and nobody knows
Before accepting an ADR, the coordinator «ha trovato tutte le sessioni M155 ferme: l'ondata 5
si era fermata alle 13:31 a metà della chiusura della 5e, e la coordinatrice l'ha fatta
ripartire» (UUS#R234). Nothing the stopped session had written said which closure steps were
done.

## C6 — one development container, many sessions restarting it
The local container `chatpnt_local` serves the main checkout. Restarts were asked and done by
several sessions (UUS#R100, R106, R110, R111, R115, R127, R128). The owner delegated restarts
on the premise «riavvia chatpnt_local quanto vuoi, non c'è nessuno che lo usa a perte te»
(UUS#R133, 2026-10-27); from 2026-10-28 waves 5, 6 and 8 ran at once. A restart kills the
probe or suite another session is running against the same container.

## C7 — the main checkout holds two sessions' code
At HEAD 8f968794, files of increment 5c (`_ec_ui.html`, two templates, a test) were modified
and uncommitted in the main checkout (HANDOFF_m155_w8 §«Ordine del codice», p.1) while other
waves wrote there. The owner later approved «Il codice dell'ondata 6 […] parte subito nel
checkout principale, mentre la 5h scrive solo documenti» (UUS#R246): the container mounts the
main checkout, so code under test must be there, one writer at a time.

## C8 — one commit carries several sessions' work
Commit a7f51a08 (2026-10-31) «chore: commit the work of the other sessions (M146 declaration
preview, VPS access, MinIO, spikes, vision)»: 33+ files of at least six units, plus the
generated `handoff.md`, `INDEX.md`, `memory/INDEX.md`, `reference/INDEX.md`,
`features_history.md` «regenerated (sdlc_check index)». Nothing listed, before the commit,
which file belonged to which unit, which were generated, or whether each unit's HANDOFF and
request record were in.

## C0 — a generated file written by hand (not located)
Named «(a)» by the first F-088 session; no episode was found in the M155 records. Kept as the
control case: the current doctrine already forbids it («never by hand»; `validate` errors).
