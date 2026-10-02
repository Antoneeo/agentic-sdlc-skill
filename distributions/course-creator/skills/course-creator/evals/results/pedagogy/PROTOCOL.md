# Production comparison and review-gate probe
2026-09-27. Production scope only: course planning and complete content under an approved brief, not bootstrap or the full L3 workflow. No learner-control sessions or human participants.

## Assignment and access
- Producer /root/pedagogy_producer_a used baseline F060; /root/pedagogy_producer_b used the pedagogical revision. Both inherited the parent model with no model/reasoning override. Brief and raw policy were byte-identical; producers received no rubric or sibling results.
- Both prompts said: Use course-creator at the supplied SKILL.md path and relevant supports to fulfil the exact request in BRIEF.md, raw policy.md. Write COURSE_PLAN.md and complete course text in the assigned output directory. This fixture evaluates planning/production only; treat the brief as approved benefit/scope. Do not bootstrap, run independent reviewers or learner simulations, edit the skill, browse, or read parent directories/rubrics/other runs. No other governance files required. Preserve a process note without self-grading. The fixture source alias ai_docs/solutions/courses/tickets/policy.md#priorita is permitted.
- Differences in producer prompts were only the skill path and output directory. BRIEF.md contains the exact ordinary request, including audience, decision need, policy facts, self-study mode and at-most-eight-slide constraint. No names of pedagogical methods, worked-example demand or transfer/check instructions were injected into that request.
- File-access limits are instructions, not an OS sandbox per agent. The process notes report compliance; no independent syscall log establishes isolation. One matched pair is diagnostic, not a statistically powered experiment or a claim across models.

## Artifacts and mapping
Raw outputs in run-a/run-b; criterion frozen before production in CRITERIA_FROZEN.md; producer-used changed supports frozen in baseline-skill/revised-skill-at-production. Other unchanged supports remain in the containing skill; process notes name actual reads. Snapshot files are historical evidence and are not installed by npm.

The evaluator /root/pedagogy_blind_judge received packet-17 = run-a, packet-63 = run-b, packet-42 = constructed control; this mapping was withheld during judgement. Paths exposing run identity were removed from the judge copies; raw outputs retained. Control-project contains a valid structural fixture with category definitions and recall-only questions despite promising judgement. Its specialist validator returns zero errors/warnings. Source fixture is fictional, not an approved real organizational policy.

An evaluator-packet correction removed the control-design sentence from JUDGE_CRITERIA.md while retaining criteria 1–8 and acceptance. The original frozen criteria remain preserved. If the judge had already read them, its report records awareness that a control might be inadequate; this limits blinding. No number of passes or failures was required.

## Textual handoff
packet-63/learner-handoff.html contains exact learner-content blocks and transitions extracted into readable HTML sections, without hidden speaker notes. The round-trip assertion preserves all eight learner blocks exactly. This tests a text-only representation and semantic completeness, not graphic layout, presentation delivery, PPTX export or all renderers.

## Replay
From the repository root run the course distribution's scripts/sdlc_check.py course intro --root distributions/course-creator/skills/course-creator/evals/results/pedagogy/control-project. A structural PASS is the intended setup, not a semantic PASS. For fresh production reruns supply BRIEF.md and policy.md to independent sessions using the frozen/current skill as specified above, with the same model and access; judge anonymously against JUDGE_CRITERIA.md before exposing the mapping. Generative outputs may vary. Preserve all results, including successful baselines and failed revisions.
