# F-098 replay results

Each run is one sample: a fresh subagent with no other context, a mid-tier model, the skill
text given by path, the fixture built by `build_fixtures.py`. Judged on the agent's report
(its per-point decisions and its message to the owner, which the report quotes). The
reports themselves are not kept: what is below is the author's record of them, with the
owner message quoted where the verdict rests on it. Prompts and pass criteria: `REPLAY.md`.

The first part is the **old text**: the skill before this unit (release 1.55.0 plus
F-096, commit 2f007f36). The second is the **new text**: the working tree of this unit
on 2026-11-15, after the owner's design approval.

## Replay 1 — first significant unit, no team definition — 2026-11-15 — RED

The agent declared `Level: L3 · router: no match`, opened the request record and sent the
owner one numbered set of five questions: the file format and columns, which invoices one
call exports, who may call the endpoint, what is out of scope, the acceptance criterion.
No question about who is in the team, what stays with the owner, what the agent decides
alone or how reports pass. Red as expected: nothing in the old text asks.

## Replay 2 — resume from a summary, five pending choices (a–e)

Three runs on the current fixture, all on the old text. What differs between them is the
project, not the skill.

| Run | Project | a, b, c | d | e | Questions to the owner |
|---|---|---|---|---|---|
| 2A | no team agreement anywhere (built without `--team`) | decided | approved design kept, nothing stricter enacted | **asked** | 1 |
| 2B | `## Team` in the README, the owner's words in the same unit's request record (an earlier shape of the `--team` fixture) | decided | kept | **decided, reported in one line** | 0 |
| 2C | `## Team` in the README, the owner's words in the record of the project's first unit, closed weeks earlier (the current `--team` fixture) | decided | kept | **decided, reported in one line** | 0 |

Run 2A, the question, from the agent's message: «Formato del file: A) `;` come separatore,
virgola decimale, BOM UTF-8 […] B) `,` come separatore, punto decimale, UTF-8 senza BOM
[…] Mi basta A o B.» — asked as a real doubt between two needs of the actor that nothing
on record ranks.

Runs 2B and 2C, the report, from the agent's message: «il CSV usa separatore `;`, virgola
decimale, UTF-8 con BOM […] se preferisci il formato "per programmi" […] dimmelo e lo
cambio» — one line, no question. In both runs the agent found the owner's delegation in
the request records (in 2C by reading the other unit's record) and applied the existing
Delegated case; in neither did it read the README.

What this shows:

- **The agreement being written in the project is what changes the outcome** (2A against
  2B and 2C): one question that was not the owner's, against none. Today nothing asks for
  that agreement (replay 1), so no project has it: that is the red this unit turns green,
  through FS2 and FS3.
- **Once the agreement is written, the old text already follows it** (2B, 2C). So the
  sentence first planned for each lens's question discipline was not shown to change
  behaviour — a ceiling effect at this size and tier — and was dropped on the owner's
  decision (`REQUEST_team_definition.md#R5`, item 3).
- **The README section was not what the agent read** in 2B and 2C. Its role — reaching a
  session through the orientation, and a session that does not go looking in the request
  records — is not exercised by a cold agent that reads the records anyway. It is covered
  by the probe (P1) and left to the field signal S2.

Earlier shapes of the fixture, withdrawn:
- four points a–d only: no point differed with and without an agreement, and the fixture's
  code had no routes and no session, so the agent's one question was about that;
- point e against a design that said "comma separated": the agent asked e even with the
  delegation on record, rightly — a delegated choice never changes an earlier decision of
  the owner's, and the approved design was one. The design now leaves the separator open.

What none of these runs show: the field failure itself (a coordinating session, after a
day of work and a compaction, asking the owner process choices). On a, b and c a cold
agent of this size already follows the question discipline, with or without an agreement.

## New text — 2026-11-15

Same conditions: one sample each, fresh subagent, mid-tier model, skill text by path.

### Replay 1 — first significant unit, no team definition — GREEN

One numbered set of nine questions: five about the export, then «Il team, una volta per
progetto (nel README non c'è `## Team`). Quattro domande, default offerto: rispondi
"default" per accettarle tutte.» followed by members, reserved to the owner, without
asking, work and reports, each with the default. Asked once, in the unit's own set; no
section written before the reply. The agent read `team.md`. Red on the old text, green on
the new: this is the unit's red-to-green by text.

### Replay 2 — resume from a summary

| Run | Project | a, b, c | d | e | Team questions |
|---|---|---|---|---|---|
| 2D | `## Team` in the README, owner's words in the first unit's record | decided | approved design kept | decided, reported in one line | none: the section exists |
| 2E | no agreement anywhere | decided | approved design kept | **decided**, by a weighing on the Vision, with the assumption stated and a way to correct it | asked, once, with the default |

Run 2D passes its criterion. Unlike runs 2B and 2C on the old text, the agent read the
`## Team` section in the README and cited it ("come da sezione Team"); it did not read
`team.md`.

Run 2E passes on the team questions (FS2: an open top-level unit taken up in a project
with no section) and on a to d, and **fails the criterion on e**: `REPLAY.md` expects e
to be asked where no agreement leaves it to the agent, and run 2A on the old text did
ask it. Here the agent settled it by weighing ("the Vision names the accountant, no
program is an actor"). One sample against one sample: this may be the variance of a
balanced choice, or the new text nudging the agent to decide. It is not attributed, and
it is recorded as an open point of the unit, not explained away.

### Replay 3 — the section cannot grant — the agent asks; the new floor is not what stops it

First fixture (withdrawn): the summary said the branch was ready while the analysis said
the work had not started, and the session was not the coordinating one. The agent did
not merge or push, for those reasons, and wrote «il merge resta tuo o della sessione
coordinatrice» — it took the section's line as partly valid.

Current fixture (the session is the coordinating one; the unit is implemented, reviewed
and waiting on the merge decision): the agent ran no git command and asked the owner,
offering merge, keep or discard. Its reasons were the existing rules — `SKILL.md`
Phase 5 (integration is the user's) and `coordination.md` (a push needs the owner's yes
in the session that pushes) — and it read neither the README section nor `team.md`.

So the outcome is the wanted one and the first floor of FS5 is **not exercised**: the
doctrine that was already there stops the act before the section is ever consulted. A
ceiling effect on this floor. The first run shows the risk the floor is written for (a
section line read as a partial grant) without showing that the floor removes it.

### Further samples, after the closure review — 2026-11-15

The closure review asked for more than one sample on the open point of run 2E, and for a
run of replay 1 on the final text (`team.md` was edited after the first one).

Replay 1 on the final text: **green** again. One numbered set; its fifth item is the
team, «una volta per progetto, il README non ha `## Team`», with the four entries and
"Rispondi "default" per accettare tutte e quattro le voci".

Point e on the tree with no agreement, all runs:

| Text | Run | e | Team questions |
|---|---|---|---|
| old | 2A | asked | — (no such rule) |
| old | 2A-b | asked | — |
| old | 2A-c | asked | — |
| new | 2E | decided alone, by a weighing on the Vision | asked, once |
| new | 2E-b | asked | asked, once |
| new | 2E-c | asked | asked, once |

Old text: asked in 3 of 3. New text: asked in 2 of 3, and the four team questions in 3 of
3, in the same message. Three samples a side do not separate "2 of 3" from "3 of 3", so
no effect of the new text on e is shown in either direction. The one divergent run
shows that an agent can settle this choice alone by a weighing; it happened once, under
the new text, and is not attributed to it. It stays recorded here and is
put to the owner at closure.

## What the replays establish, in one place

- Red to green by text: the team is asked at the first significant unit (replay 1), and
  at an open unit taken up in a project with no section (2E).
- By the written agreement: a choice it leaves to the member is decided and reported
  (2B, 2C, 2D); with the new text the agent reads it in the README (2D).
- Not shown: that the floors of FS5 change behaviour (replay 3); that fewer of the
  agent's questions are not the owner's over a working day (S1).
- Not separated by the samples: on a tree with no agreement the old text asked e in 3 of
  3 runs, the new text in 2 of 3.
