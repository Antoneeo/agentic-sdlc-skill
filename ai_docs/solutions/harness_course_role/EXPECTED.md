# Frozen expectations (written before any run)

Probe for F-060: does the method's review rubric reject checks that ask the person to perform the agent's operations?

Fixtures: F1=S11, F2=S14, F3=S17, F4=S23, F5=S27, F6=S38 (verbatim, C-001 3.0-content); F7 = a rewritten S17 where the person judges the agent's answer.

- packet_old (current learning_design §1, §4, §7): RED expected. The reviewer does not reject F3, F4 or F5 because the required result belongs to the agent. Other findings may appear; they do not count.
- packet_new (same sections plus the person-act additions): GREEN expected. F3, F4 and F5 fail on the learner's-act criterion; F1, F6 and F7 do not fail on it. F2 is an explanation: it must not fail on that criterion (explaining a mechanism is admitted).

A result counts only when the reviewer's reason names who produces the required result. Same model, same prompt, same fixtures and profile for both runs; only RUBRIC.md differs. Isolation is by instruction only.

## Addendum before run new2 (written after runs old and new, before run new2)

Run new admitted F5 (S27, assign triage levels) as a decision reserved to a tech lead. packet_new2 adds that a classification the tool produces stays a tool output even when a decision depends on it. Expectation for new2: F3, F4 and F5 fail on the learner's-act criterion; F1, F2, F6, F7 do not.

## Addendum before runs new3 and controls (written after the design review, before any of these runs)

packet_new3 = new2 plus three design-review corrections: the act/operation split is read from the approved course Vision (F-4); a prediction confronted with the tool's actual output is admitted (F-5); the Learner's act row applies only to courses on a tool, agent or delegated process (F-1).
- new3 on F1–F7: same as new2 — F3, F4, F5 fail on learner's act; F1, F2, F6, F7 do not.
- packet_ctrl_operate (learner operates git/SQL, no agent): C1 (write the query yourself) and C2 (predict git status, then compare) do NOT fail on learner's act.
- packet_ctrl_concept (conceptual HTTP history course): C3 does NOT fail on learner's act; the reviewer treats the row as not applicable.

## Addendum before run new4 (written after design review round 2, before run new4)

packet_new4 = new3 plus: the course Vision may narrow what §1 admits; the row's scope names the operative property ("performs operations for the learner"); the prediction admission yields to a Vision that reserves the output to the tool. Expectation for new4 on F1–F7: same as new3 (F3, F4, F5 fail on learner's act; F1, F2, F6, F7 do not). This is a regression run; the prediction clause itself is not exercised by any run where the row applies.

## Addendum before runs new5a and new5b (written after run new4, before them)

Run new4 admitted F5 by reading PROFILE ('the technical lead, who must judge … decisions') as making the level a reserved decision. packet_new5 adds to the row: a level, category or verdict assigned with no tool output shown is a tool output even when the learner's role owns the dependent decision. Two independent runs (new5a, new5b), same prompt, to expose reviewer variance. Expectation for both: F3, F4, F5 fail on learner's act; F1, F2, F6, F7 do not.

## Addendum before the Vision-profile runs (written after new5b, before them)

Text tuning on F5 has stopped (circuit breaker: F5 rejected 3 of 6 runs). The rule names the approved course Vision as the authority for the split, so these runs replace PROFILE.md with verbatim excerpts of the amended C-001 Vision (learners and role paragraph, the success signal on checks, the Non-Goal). Runs: new5_vision_a, new5_vision_b (new5 rubric), old_vision (current method rubric).
- new5_vision_a/b: F3, F4, F5 fail on learner's act; F1, F2, F6, F7 do not.
- old_vision: no expectation on F3–F5; it measures how much the amended Vision alone decides without the method change.
