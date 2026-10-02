# Learning design: from audience to explanation

Read for a new course or a change in audience, objectives or module order. Keep the course Vision's benefit in view. A list of topics is not a learning path.

## 1. Learner profiles

For each audience, record what they will do with the knowledge, their context and constraints, terminology they understand, and evidence about their starting knowledge. A job title or self-rating is weak evidence. A short diagnostic task, concrete example of prior work, or interview answer can establish a narrower claim. Mark each concept `PROVATO`, `INCERTO` or `DA_INSEGNARE`. If evidence is missing, keep it uncertain.

## 2. Concept dependency graph

List the concepts needed to realize the Vision, each with a stable `CO<n>` ID and reopenable source. Draw `A → B` only when understanding A is necessary to understand or use B, not merely because A is traditionally taught first. Ask whether an apparent prerequisite can be explained briefly inside B; if so, avoid an extra module. Detect cycles and missing nodes with `course_check.py`. The graph in project memory maps topics and source ownership; this graph maps instructional prerequisites and has separate authority.

Record state and evidence for each (concept, profile) using `templates.md`.
Profiles come from `D-UC.md`; a demonstrated prerequisite for one audience does
not establish it for another. A repeated concept keeps the same prerequisites,
while its initial state, evidence and teaching objectives may differ by profile.

## 3. Modules as a progression

For each module choose an observable comprehension or use objective. List the concepts required and the prior modules that teach them. Write a one-paragraph *explanation plan* before choosing a quiz: starting point familiar to the learner, new idea, example, boundary or counterexample, transition to the next idea. A module may cover several concepts when the explanation remains coherent. Split a module when the learner needs a genuine intermediate understanding to proceed.

## 4. Write and review the explanation

Write for the named learner rather than a generic reader. Define terms before relying on them. Show why a step follows from earlier knowledge. Use an example drawn from the learner's actual task where possible, and a counterexample when it exposes a likely misconception. Write the complete textual source first using `slide_content.md`, including its distinguishable-value acceptance criteria for every course. Optional delivery formats derive from that source. Review the explanation aloud or with an independent reader: where would this learner ask “why?”, and what prerequisite did the sentence assume? Revise the explanation itself before adding more exercises.

## 5. Check understanding

Choose a check that could fail for the misunderstanding the explanation is meant to resolve. A recognition question may be too weak for a use objective. Define a correction path: which paragraph, example or module changes if a learner gets it wrong? Exercise density is not a quality metric; use as many as the objective and delivery context require.

A course that teaches definitions must still enable a useful new distinction or decision for its audience. Review the transfer task against a plausible shortcut such as a glossary: what reasoning does the explanation add? Record uncertainty about prior knowledge; do not invent superiority or efficacy.
