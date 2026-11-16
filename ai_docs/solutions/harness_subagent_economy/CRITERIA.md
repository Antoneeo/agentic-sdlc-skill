# F-100 replay — criteria (written before the doctrine)

A cold reader is put in the orchestrator's place with a neutral fixture (`build_replay.py`,
the fixture is in the script) and the method: `dispatch.md` and `team.md` whole, old text
from the base ref against the new text in the working tree. Two readers per text, same
model (light tier, named in RESULTS.md), fresh context each, no other material.

A reader passes a criterion only when its answer does what the criterion says in words;
silence fails it. Each criterion is scored per reader.

- **C1 — an unproven read is not work.** T1's result (verify passed; the report says the
  guides were read and gives no evidence of a whole read) is not passed to review or
  accepted until the whole read is shown: the subagent is asked for it, or the task goes out
  again. Accepting it, or reviewing it as is, fails.
- **C2 — the correction goes to the context that holds the guides.** T2's two review
  findings are sent back to subagent s2, resumed, not to a new subagent. A new subagent, or
  the orchestrator fixing them itself, fails.
- **C3 — the brief asks for the read back.** T3's brief asks the subagent to report, for
  each guide, its total lines and the last line read (or an equivalent: lines read out of
  total). "Read the guides whole" alone fails.
- **C4 — two failed rounds move the task; the guides set the split.** T0 (economy, two
  rounds in a row stopped partway through the accessibility guide) is not sent to the economy
  tier a third time: it goes to a higher tier, or is split by guide set. And T3, which names
  the same guide, is not given to economy with it in one brief: a higher tier, or a split by
  guide set (each part naming fewer guides). A split by files or components alone, with every
  part still naming all guides, fails. Both halves are needed to pass.
- **C5 — the cost is in the question, the choice left.** The team question set the reader
  writes (Part B) states what several sessions cost against one session with subagents (they
  reread what another context holds; reports cross as notes or files) and what they buy (work
  the owner opens and steers), offers the default, and recommends no shape. A question set with
  no cost, or one that steers the owner to a shape, fails.

Expected: red under the old text (the doctrine states none of C1–C5 except the whole read
itself), green under the new: every criterion passed by both new-text readers.

## Revision before the new-text run (2026-11-16)

Fixture v1 leaked two answers: s1's report declared "lines 1-400" (so the partial read was
handed to the reader, where in the field case nobody reported it), and the client was
described as resuming a subagent "with what it already read still in its context". Both
old-text readers passed C1 and C2 on those hints (`raw_answers_v1.md`). Fixture v2 removes
both: s1 reports "Read GUIDE_forms.md and GUIDE_design_tokens.md", s2 reports no line, and
the client "can send a further message to a subagent it started earlier, by its id". C1 is
reworded to the v2 state (an unproven read, not a declared partial one); C2–C5 unchanged.
Both texts are scored on v2 only.

## Revision after design review round 1 (2026-11-16)

The design moved the cost information from the reply after the owner's choice into the team
question itself (R2: «informazione sul costo nella domanda sul team»), and made it two-sided.
Part B of the fixture (v3) now asks the reader to write the team question set; C5 is reworded
to match. C1–C4 and Part A unchanged from v2. Both texts are re-run on v3; the v2 old-text
answers stay as a record.

## Revision after design review round 2 (2026-11-16)

The design states no threshold for sizing guides before a first dispatch (no measurement
supports one) and bounds it instead: two consecutive failed rounds on a task, a partial read
counting as one, move it to a higher tier or a split. C4 was scoring an unmeasured judgement
against a fixture where nothing had failed. Fixture v4 adds T0, an economy task that stopped
partway through a guide twice; C4 now scores that bound, on T0 and on T3 that names the same
guide. C1-C3, C5 and the rest of the fixture unchanged from v3. Both texts re-run on v4.
