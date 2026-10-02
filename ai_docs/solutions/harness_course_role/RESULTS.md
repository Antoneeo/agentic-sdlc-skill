# Probe results — F-060 learner's-act rule

Same model (sonnet), same prompt, same FIXTURES.md and PROFILE.md in every run; only RUBRIC.md differs. Isolation by instruction only; reviewers reported reading only their packet. Expectations frozen in EXPECTED.md before each run.

| Run | Rubric | F1 S11 | F2 S14 | F3 S17 | F4 S23 | F5 S27 | F6 S38 | F7 S17 rewritten | Outcome |
|---|---|---|---|---|---|---|---|---|---|
| old | current learning_design §1, §4, §7 | NOT READY (unanchored «luglio», excerpt limit) | READY | READY | READY | READY | READY | READY | RED as expected: no unit rejected because the required result belongs to the agent. |
| new | + person-act paragraph, §4 sentence, §7 row | READY | READY | NOT READY, learner's act | NOT READY, learner's act | READY, read as a decision reserved to a tech lead | READY | READY | Partial: F5 admitted. Same weakness as the Vision blind check round 3 (undefined reserved decision). |
| new2 | new + a tool classification stays a tool output; reserved decisions are those the tool hands to a person | READY | READY | NOT READY, learner's act | NOT READY, learner's act (conflict verdict named in §1) | NOT READY, learner's act (triage level assigned with no agent declaration) | READY | READY | GREEN: matches EXPECTED.md addendum on all seven units. |
| new3 | new2 + design-review corrections (split read from course Vision, prediction admitted, row scoped to tool courses) | READY | READY | NOT READY, learner's act | NOT READY, learner's act | NOT READY, learner's act (level only) | READY | READY | GREEN, no regression. |
| ctrl_operate | new3 rubric; profile operates git and SQL, no agent | C1 NOT READY on Alignment and Support (fixture quality), C2 READY | | | | | | | As expected: neither fails on learner's act; row read as not applicable. |
| ctrl_concept | new3 rubric; conceptual HTTP-history course | C3 NOT READY on Support (fixture omits its solution) | | | | | | | As expected: row read as not applicable. |
| new4 | new3 + round-2 corrections (Vision may narrow, scope names operations for the learner, prediction yields to Vision) | READY | READY | NOT READY, learner's act | NOT READY, learner's act | READY, read as a tech lead's reserved decision from PROFILE | READY | READY | NOT GREEN on F5. The four changes do not touch the level example; F5 has now been admitted in 2 of 4 runs with the rule (new, new4), so the verdict on a level assigned without an agent declaration depends on the reviewer. |
| new5a | new4 + a level/category/verdict assigned with no tool output shown is a tool output | READY | READY | NOT READY, learner's act | NOT READY, learner's act | NOT READY, learner's act | READY | READY | GREEN. |
| new5b | same packet, second sample | READY | READY | NOT READY, learner's act | NOT READY, learner's act | READY, read as reserved decision; new sentence not cited | READY | READY | NOT GREEN on F5. |
| new5_vision_a | new5 rubric; PROFILE = verbatim amended C-001 Vision excerpts | READY | READY | NOT READY, learner's act | NOT READY, learner's act | NOT READY, learner's act (cites the Vision clause on levels) | READY | READY | GREEN. |
| new5_vision_b | same packet, second sample | READY | READY | NOT READY, learner's act | NOT READY, learner's act | NOT READY, learner's act | READY | READY | GREEN. |
| old_vision | current method rubric; same Vision PROFILE | NOT READY, Alignment (over-reach: reads 'what the answer must contain' as agent content) | READY | NOT READY, Alignment | NOT READY, Alignment | NOT READY, Alignment | READY | READY | The amended Vision alone rejects F3–F5 through Alignment, but also rejects F1, a legitimate judgement of the agent's output. |

The F1 finding in run old is an excerpt artefact: «luglio» is established in earlier units the reviewer did not receive. It is not counted.

Conclusion: the rule text in packet_new5/RUBRIC.md (new2, new3 and new4 superseded) is the text shipped in for `learning_design.md`. One sample per run; reviewer judgement varies, so the green result shows the text can decide these cases, not that every reviewer will. The reviewers had no answer key, so Alignment and Support rows were not assessable.

Control note: the ctrl_operate reviewer read the scope as 'an agent is involved'. For a course where the person operates the tool the row would not fail those units under either reading, so the verdict is unaffected; the narrow reading is recorded, not corrected.
Outputs (summary + verbatim decisive lines; full reports not saved): outputs/new3.md, new4.md, new5a.md, new5b.md, new5_vision_a.md, new5_vision_b.md, old_vision.md, ctrl_operate.md, ctrl_concept.md; runs old/new/new2 in outputs/runs_old_new_new2_abridged.md. Method diff: F060_method.diff.
Freeze order: EXPECTED.md addenda precede their runs by file time only; the harness folder is not yet committed, so there is no commit timestamp.

F5 stability across the six runs with the rule (new, new2, new3, new4, new5a, new5b): rejected 3, admitted 3. F3 and F4: rejected 6 of 6. Rewording the level case has not stabilized F5; the probe PROFILE stands in for the course Vision and does not contain the Vision's own clause on levels, which the rule names as the authority for the split.

Reading of the Vision-profile runs: with the course Vision the rule names as authority, the new rubric decides all seven units as expected in 2 of 2 samples. The amended Vision alone, under the current rubric, reaches the same verdicts on F3–F5 but over-rejects F1. Without a Vision clause on the specific output, the method text alone rejects claims and conflict verdicts reliably (6 of 6) and a level assigned with no agent declaration only in 3 of 6. Residual for tool courses whose Vision does not name such outputs: the reviewer's verdict on levels or categories can vary.
