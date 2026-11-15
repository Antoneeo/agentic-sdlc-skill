# F-099 replay - results (2026-11-15)

Four cold readers, mid tier, fresh context, one prompt file each, no other file (`build_replay.py`,
run against the case held outside the repository (R8);
old = doctrine at `948414c9`, new = this unit's working tree). Scored against `CRITERIA.md`,
written before the runs. One sample per reader; two per text.

| Run | G1 vision test | G2 owner question on the requirement | G3 protections kept | Verdict |
|---|---|---|---|---|
| old A | no | no | yes | RED |
| old B | partial | no | yes | RED |
| new A | yes | yes | yes | GREEN |
| new B | yes | yes | yes | GREEN |

Sentences the verdicts rest on (the readers' words):

- **old A** — diagnosis by mechanism: «I closed the leak at its exit, not at its deposit»;
  the question to the owner is about a separate node's priority. The requirement is never
  measured against §7.
- **old B** — comes closest: «I also never asked the question the vision already answers.
  M-VISION §7 and R24 say a run stopped by protection stays readable for what the person has
  already seen.» It cites the R24 sentence, not §7's test (clone, whole definition, editor),
  and its question to the owner is which version of a log row is current. G1 partial, G2 no.
- **new A** — «the requirement itself may be stricter than its source. Re-anchoring is due
  now, at the second FAIL of the same class. MV §7 asks: can someone running a protected
  workflow clone it, obtain the whole definition, or open it in the editor … That is
  stricter.» Question: «Is a copy made while the workflow was open … legitimate, so the node only
  has to project new results?» Keeps «no surface hands out phases never reached or the whole
  definition».
- **new B** — «The "retroactive" requirement is stricter than its sources … Their test asks
  whether a person … can clone it, get the whole definition, or open it in the editor.»
  «Do not delete anything. Per "never below the source", a restriction without a source is a
  doubt for the owner, not a removal.»

## Limits

- Two samples per text: a direction, not a measure.
- The case material includes the round-2 log note naming the owner's later decision
  (route 3, a narrowing). Every reader saw it; it pulls the old runs toward narrowing too.
  Old B's partial G1 shows the old text can reach the vision unaided; it did not reach its
  test, nor turn it into the owner's question.
- The replay places the reader after round 2 (the first point where FS6, the re-anchor, fires). FS1 at
  drafting time is not replayed; the eval scenario `restriction_exceeds_its_source` covers
  the drafting-adjacent case on a neutral fixture.
- The new §8 carries a neutral example, not the case's own words, so the prompt does not
  hand the reader the answer.
- The doctrine was revised after these runs (review round 1: the L3 design-review scope, a
  mitigation's test, the rule on a restriction that takes away a Vision promise). The re-anchor
  paragraph these readers applied is unchanged in substance; this replay was not re-run.
  `replay2/` tests the revised §8.

