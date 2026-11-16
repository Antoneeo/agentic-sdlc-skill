# F-100 replay — results

Readers: Sonnet 5.5 (light tier, explicit), fresh context each, two per text and fixture,
given only the prompt (`build_replay.py`: the fixture, then `dispatch.md` and `team.md` whole,
old text from the release commit `c67e5792` against the working tree). Criteria in
`CRITERIA.md`, written before the doctrine; its three revision notes record each change to the
fixture and why. Raw answers: `raw_answers_v1.md` … `raw_answers_v4.md`.

| Fixture | Text | C1 | C2 | C3 | C4 | C5 |
|---|---|---|---|---|---|---|
| v1 (leaked C1, C2) | old A / B | pass / pass | pass / pass | partial / fail | fail / fail | fail / fail |
| v2 | old A / B | fail / fail | pass / pass | fail / fail | fail / fail | fail / fail (old Part B) |
| v3 | old A / B | fail / fail | pass / pass | fail / fail | fail / fail | fail / fail |
| v4 | old A / B | fail / fail | pass / pass | fail / partial | **pass / pass** | fail / fail |
| v4 | **new A / B** | **pass / pass** | pass / pass | **pass / pass** | pass / pass | **pass / pass** |

Reading:

- **Red under the old text, green under the new: C1, C3, C5** — the read reported and checked
  (FS2) and the cost in the team question (FS5). On v4 one old reader asked for "line counts"
  unprompted after the fixture's T0 showed a context running out: scored partial (no last line
  read, no check against the real length).
- **C4 is green under both texts on v4.** Once a failure is in front of them, both old readers
  moved T0 up a tier and gave T3 to a higher tier. FS3 writes down that judgement and adds what
  they did not do by themselves: the split by guide set (both new readers split T3; no old
  reader did, one called a split "a scope decision about the plan") and the carry-over of a
  twice-failed guide. C4 is not evidence that FS3 is needed; R1's measurement is.
- **C2 is green under both texts on every fixture** once the fixture names the messaging
  facility. FS4's evidence is R1's measurement alone (ruling r55).
- **The proxy, declared:** the replay measures whether the doctrine makes an orchestrator do what
  the field report measured as cheaper. It does not measure tokens.
