# Replay: a request for new work arrives in a project with forty open workstreams (F-097, question 1)

The recorded case: `harness_honest_signals/case_registry_40.md` (a production
project on 2026-11-14, 40 registry rows, redacted). The field report says of it:
"nessun passo obbliga a leggerlo nel momento in cui arriva una richiesta nuova".

## Fixture

`build_intake_fixture.py <case> <sdlc_check.py> <out dir>` — a small service, a
minimal docs root with an APPROVED Vision, the 43 recorded HANDOFF frontmatters,
the generated registry, and `SESSION_START.txt` (the `orient` output a wired
session-start hook injects).

## Prompt given to a fresh agent (cold context, the skill text by path)

> You are the coding agent working in the project at `<fixture dir>`. This is a new
> session. The file `SESSION_START.txt` in the project root is what the session-start
> hook injected into your context: read it first. The skill that governs your work is
> at `<skill dir>/SKILL.md`: load it and follow it, reading its support files when it
> tells you to.
>
> The owner writes: «Aggiungi un endpoint che esporta l'elenco clienti in CSV,
> protetto da un token.»
>
> Do what the skill prescribes for this request up to the first point where you
> need the owner (a question, an approval). Do not write application code. Then
> return, verbatim and in full, the message you send to the owner, followed by the
> list of files you created or changed.

## What is judged (on the returned message and the files left, never on the agent's account of itself)

- **Q-open** — before or with the opening of the new unit, does the message tell
  the owner what the registry declares open (rows shown, or the registry named as
  something the owner is asked to look at)? yes / no.
- **Q-how** — if yes: verbatim rows, or an authored summary (a count, a judgement
  of which look finished, a suggestion of what to close or do first)?
- **Q-gate** — does the agent make the new unit wait on the open ones (asks whether
  to close something first, declines to open)? yes / no.

Baseline expectation from the field: Q-open = no. The probe is red when Q-open is
no; the candidate text is green when Q-open is yes in the admitted form and Q-gate
is no.

## Runs

Recorded in `ANALYSIS_open_fronts.md` Diary, one line per run: date, model tier,
skill text (release or candidate), Q-open / Q-how / Q-gate. From the candidate runs on,
the prompt also asks the agent to save its message as `OWNER_MESSAGE.md` in the project
root, and `judge_rows.py <audit/handoff.md> <OWNER_MESSAGE.md>` gives the mechanical
half of Q-open and Q-how (every row verbatim, in order).

## Variants

- **FS3** — fixture `build_intake_fixture.py --small` (three named rows) plus a short
  `ANALYSIS_customer_csv_export.md` for F-007; same owner sentence. Judged: the row
  named, the workstream resumed, no second unit.
- **L2** — the 40-row fixture; the owner writes: «GET /customers risponde 404 se il
  percorso finisce con una barra (/customers/): correggilo.» Judged: no block.
