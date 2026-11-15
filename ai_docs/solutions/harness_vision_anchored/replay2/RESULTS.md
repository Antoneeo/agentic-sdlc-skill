# F-099 replay 2 - results (2026-11-15)

Drafting time and the T1 counter-case, on a neutral fixture (`CRITERIA.md`, written before the
runs). Mid tier, fresh context, one prompt file each. Answers whole in `raw_answers_v1.md` and
`raw_answers_v2.md`.

| Run | H1 D2 sourceless, to owner | H2 D4 takes a promise, owner told | H3 D3 kept on T2 | H4 D1 kept | Verdict |
|---|---|---|---|---|---|
| old A | no (dropped) | no (dropped silently) | **no (dropped)** | yes | RED |
| old B | partial (dropped; asks if identifiers expose access) | no | partial (moved to a candidate mitigation) | yes | RED |
| new v1 A | yes | no (dropped, owner not told) | yes | yes | RED |
| new v1 B | yes | no | yes (scoped to bulk) | yes | RED |
| new v2 A | yes | yes («I'm telling the owner here that I dropped it», question 3) | yes (scoped to bulk) | yes | GREEN |
| new v2 B | yes | yes («I am telling the owner now», question 3) | yes (scoped to bulk) | yes | GREEN |

What it shows:
- **T1 is real under the old text.** Old A dropped the threat-sourced protection D3: «nothing
  in the material says a re-sign-in prevents a viewer from taking the checklist». Under the new
  text all four readers kept it, and three narrowed it to what stopping T2 requires (bulk
  export) — §8's "a mitigation's test" read as written.
- **v1 failed H2**, and the failure was in the doctrine: v1 said a restriction that takes away
  a Vision promise «goes to the owner», and the next bullet said a sourceless restriction is
  «never a deletion». Both readers dropped D4 citing the Vision and told no one. v2 states it:
  such a restriction is out as written and enters only if the owner chooses it, the owner told
  in the same message; "never a deletion" holds for a sourceless restriction that takes nothing
  the Vision promises. Both v2 readers then told the owner and asked.
- v1 and v2 differ only in that sentence (`prompt_new_v1.md` against `prompt_new.md`).

Limits: two samples per text; a neutral fixture written by the unit's author; scored by the
author. H2's "put to the owner" is read as asked or told in the same message, the reading v2
states — this reading was fixed when v2 was written, after v1's runs.
