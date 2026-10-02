# Learning design: teach knowledge and usable reasoning

Read before designing or substantially revising a course, and during semantic review. This file owns pedagogical decisions; `slide_content.md` owns the complete output schema. A list of topics, polished slides or a filled alignment table is not evidence that the promised understanding is taught.

## 1. Start with the learner and the promised result

Record the situation in which each audience will use the knowledge, their constraints, known terminology and evidence of prior understanding. A title or self-rating is not proof. A short diagnostic, example of prior work or interview can establish a narrower baseline; absent evidence stays uncertain. For every objective distinguish knowledge to recall, a concept to explain, a judgement to justify or a procedure to perform. Not every course teaches an operational method; its value must still be useful and distinguishable for this audience.

Write the result as a capability in context: what the learner should notice, explain, decide or do, and under which conditions. Avoid objectives such as 'cover chapter 3' or 'understand our approach' without an observable meaning. State the likely misconception or plausible shortcut and its limits without inventing learner failure.

## 2. Work backward from evidence, then build the teaching

Before planning slides, decide what would count as evidence for each promised result and what superficially plausible response would fail. Recall can establish factual knowledge; a claim about judgement requires a choice with reasons, and transfer requires a new situation. Do not inflate every small fact into an elaborate performance task. Several objectives can share one cumulative check.

Record the alignment in COURSE_PLAN using `templates.md`: objective/context -> evidence and criterion -> explanatory bridge -> example/contrast -> support and correction. At design time these are concrete descriptions; at delivery they point to authored passages. Then write the explanation plan and only afterward the detailed questions and answers. This order prevents quizzes replacing teaching while keeping assessment from becoming an afterthought. If a check asks for a distinction never taught, revise the teaching or narrow the promise.

## 3. Explain prerequisites and build a progression

For each needed concept keep a stable CO<n> ID, reopenable source and per-profile state PROVATO, INCERTO or DA_INSEGNARE. D-UC owns profile names. PROVATO requires evidence for that profile; another group's knowledge does not establish it. Repeated concepts keep the same prerequisite IDs while states and objectives may differ. Use the graph fields in `templates.md`.

An arrow A -> B means B needs A, not that textbooks traditionally teach A first. Teach uncertain prerequisites before relying on them, or state the unresolved limitation. A short prerequisite may fit inside the explanation rather than needing another module. The course graph orders learning; the KB topic graph organizes sources. Order modules and within-module concepts accordingly.

Each explanation plan starts with something familiar, introduces the new idea, shows why the next step follows, and identifies an example or boundary. End with a bridge to the next idea. Cut or merge a slide that has no identifiable role in this progression.

## 4. Make the reasoning available to the learner

For a decision or procedure, author a worked case that shows the available observations, the relevant rule, the reason for the choice and a limit or plausible alternative. Show a change in a decisive condition when it reveals why the answer changes. A list of steps or a completed artifact alone does not expose the reasoning. Provide concise, checkable explanations, not a claim to reveal an agent's private thought process.

Then give appropriate support for a learner attempt (a cue, partial example or comparison) and reduce it toward independent use. Ask the learner to explain a choice and compare it with an authored rationale. Scale support to prior knowledge and task complexity; advanced learners may not need beginner scaffolding. Do not prescribe a worked example or exercise on every slide. For conceptual objectives, a causal explanation, prediction or contrasting example can supply the bridge without pretending it is a procedure.

## 5. Manage the learning load and the delivery surface

Introduce necessary terms before using them; keep related data, diagram labels and explanations together. Remove decorative or irrelevant information. Segment a complex explanation into meaningful steps while retaining how they connect. Tailor support to the learner rather than equating more words with better teaching.

The complete source can be detailed without making every slide dense. In self-study, all essential reasoning must remain visible across the learner's units; in guided delivery, author the necessary spoken explanation. If content does not fit, divide the canonical units before rendering instead of shrinking text or hiding meaning in notes. Preserve exact examples and visual relationships through the handoff.

## 6. Use recall, practice and feedback to improve the explanation

Let learners attempt an answer before exposing the solution. Revisit a previous idea in a later part of the course when it helps connect or apply knowledge. Supply the answer, why it follows, a likely error and the passage or alternative explanation that repairs it. 'Wrong: read again' is not sufficient feedback for a reasoning objective.

When retention matters and the delivery permits it, propose a later retrieval opportunity. This is a learning recommendation, not permission to schedule messages or track people. Adjacent slides do not establish distributed practice over time, and a single successful attempt does not establish durable learning. No fixed interval or exercise quota fits every course.

## 7. Semantic acceptance — locate evidence, do not count fields

The independent reviewer inspects the actual learner packet and a separate key. For each promised capability (grouping objectives when appropriate), report:

| Check | Evidence required for a readiness verdict |
|---|---|
| Value and audience | Starting situation, useful changed understanding/action, limits of what is known about this audience. |
| Alignment | A passage teaches the knowledge/reasoning that the assessment requires; its criterion measures the promised capability. |
| Explanatory contribution | Locate the step that connects observations or prior knowledge to the conclusion; identify a likely misunderstanding it addresses. |
| Discrimination | Give a plausible but insufficient learner answer and explain why the criterion rejects it. For application/transfer promises, inspect a changed or unfamiliar case that cannot pass by repeating labels. |
| Support and correction | Locate sufficient explanation before the attempt, an authored rationale, and a correction matched to a likely error. |
| Delivery and fidelity | Necessary terms and reasoning are available in the declared mode; sources support facts and visual instructions do not delegate missing teaching to the renderer. |

Fail readiness for a promised capability if the reviewer cannot locate its teaching or suitable evidence, if the answer can be supplied by repeating headings alone when application is promised, or if the course asks for reasoning it never prepares. Cite the defect and revise the affected explanation/check; another filled field or added theory name does not resolve it. Do not demand novelty for an expert when the course is for novices, or require a method-superiority comparison in unrelated conceptual courses.

Separate three conclusions: (1) this draft meets content/design criteria; (2) this skill improved an agent's output under the tested conditions; (3) people learned and retained the capability. Review supports the first. A controlled production comparison may inform the second. Only suitable learner evidence can support the third. A no-course model may already know the answer; preserve that inconclusive outcome.

## Pedagogical foundations and their limits

The procedures above are this skill's application of these sources, accessed 2026-09-27. Frameworks guide design; they are not experimental proof that this skill works. The course author can follow this file without network access. Reopen sources when changing its factual claims.

- **Backward design and types of learning goals.** Jay McTighe, [Three Key Questions on Measuring Learning](https://ascd.org/el/articles/three-key-questions-on-measuring-learning), sections 'What Matters in a Contemporary Education?' and 'How Should We Assess the Things That Matter?' (2018). Knowledge, skill, understanding and transfer call for different evidence; the outcome determines the assessment. Used in §§1–2,7 as a design framework, not an efficacy guarantee.
- **Alignment.** Carnegie Mellon Eberly Center, [Align assessments, objectives and instructional strategies](https://www.cmu.edu/teaching/assessment/basics/alignment.html), 'What if the components ... are misaligned?' and assessment examples. Instruction, objective and assessment must target the same capability. Used in §§2,7; our locator matrix is an implementation choice.
- **Cognitive apprenticeship.** Collins, Brown and Holum, [Cognitive Apprenticeship: Making Thinking Visible](https://www.aft.org/ae/winter1991/collins_brown_holum), 'From Traditional to Cognitive Apprenticeship' and methods (1991). Modeling, support, articulation/reflection and increasing independence expose strategies that a finished answer can hide. Used in §4 for reasoning and procedure goals; not a requirement to stage a literal apprenticeship in every course.
- **Cognitive load and worked examples.** NSW Centre for Education Statistics and Evaluation, [Cognitive load theory in practice](https://education.nsw.gov.au/about-us/education-data-and-research/cese/publications/practical-guides-for-educators/cognitive-load-theory-in-practice.html), teaching strategies 1–6 (2018). Match existing knowledge, use examples for new skills, increase independence and remove irrelevant material. Used in §§3–5; this guidance does not establish a universal slide word limit.
- **Retrieval practice.** Karpicke and Blunt, [Retrieval Practice Produces More Learning than Elaborative Studying with Concept Mapping](https://learninglab.psych.purdue.edu/downloads/2011/2011_Karpicke_Blunt_Science.pdf), abstract and experiments (2011). Two experiments on science texts support retrieval benefits under their tested conditions. Used in §6; not proof of every retrieval task, this skill or universal superiority over concept maps.
- **Spacing.** RetrievalPractice.org, [Spacing](https://www.retrievalpractice.org/spacing), practice guidance by cognitive scientists. Separate learning opportunities over time rather than conflating repetition in one sitting with spaced retention. Used in §6 where delivery permits; optimal timing and actual retention require contextual evidence.
