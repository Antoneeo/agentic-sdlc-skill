# Complete teaching content and distinguishable value

Read before producing or substantially revising course material. The primary deliverable is `SLIDE_CONTENT.md`, a complete textual source for every slide. A deck, outline, topic list or collection of speaker notes does not replace it. Optional rendering consumes this document and must not invent the explanation, examples, answers or visual meaning.

## Acceptance of value — every course

For each taught profile, establish a credible starting situation, a useful change in understanding/decision/ability, the explanation that enables it, and an observable transfer task. A learner must reason about a new case, not merely repeat the course's labels. Identify a plausible shortcut (for example, a definition sheet) and what the course adds for this learner. A course may be valuable to a beginner and redundant to an expert: do not invent a deficit or promise universal novelty.

Trace each module to that change. Each slide serves the progression; it need not make a separate benefit claim. If the reviewer cannot identify the change, explanatory contribution and transfer evidence, revise the course before calling it ready. Populated fields and longer text are not evidence of value.

For a method/tool course, apply both the method and a fair alternative to the same conditions. Show the additional explicit mechanism, its cost, limits and a case where the alternative is sufficient. Equivalent instructions may produce equivalent results; instructions guide an agent, they do not mechanically guarantee compliance. Do not manufacture failures or measured advantages.

## Versioned contract

New and substantially revised courses declare `Content contract: slide-content-v1` in `COURSE_PLAN.md`. The fixed source is `SLIDE_CONTENT.md` in the same course directory. The source version matches the plan. Its module/objective IDs come from the plan; references use the safe located paths described in `templates.md`.

If the person explicitly requests non-slide teaching (such as an audio course), use `Content contract: text-content-v1`, explain that request in `Format exception:` in the plan, and write `COURSE_CONTENT.md` with the same schema using U01, U02, etc. The exception changes the units, not the requirement to author all teaching material. Never infer the exception simply to avoid writing slide content.

Undeclared legacy courses, including PPTX courses, receive a migration WARN. This is compatibility, not permission to deliver a new course under the old contract. Unknown or empty declarations are errors. The validator checks structure and traceability; source fidelity, sufficiency and distinguishable value require independent review.

## Source schema

Use the exact English metadata keys and headings below; authored prose may use the learner's language. Repeat the unit block for every slide, in teaching order. Use stable S-prefixed IDs (U for the explicit exception). Each metadata key occurs once. Do not leave placeholders.

```markdown
# <Course title>
Course version: <matches COURSE_PLAN>
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| <plan profile> | <starting task and evidence or uncertainty> | <useful changed decision or understanding> | <specific explanatory bridge> | ai_docs/.../SLIDE_CONTENT.md#s03 | <plausible shortcut and what it leaves unexplained for this profile> |

## S01
Module: M1
Objective: O1
Role: explanation
Title: <exact slide title>
Value contribution: <why this step is needed for the module objective>

### Learner content
<Exact visible text, including captions, labels, examples, numbers and table cells. No instructions to “explain X” in place of X.>

### Complete explanation
<Fully authored meaning, reasoning, example and relevant limit. In guided delivery this is the exact narrative to speak; in self-study all essential reasoning also appears in Learner content.>

### Visual content
<Exact objects, labels, relationships and reading order. Or an explicit text-only choice with a reason. Styling is left to the renderer; teaching meaning is not.>

### Transition
<Authored bridge to the next idea, or an explicit ending.>

### Sources
- ai_docs/.../sources.md#claim-1
```

`Delivery mode` is `self-study` or `instructor-led`. `Role` is `orientation`, `explanation`, `check`, `solution` or `closing`. A check may cover several modules/objectives; do not force one separate exercise per module. A check adds `Solution: S04` (or U04); the referenced unit is a subsequent `solution` covering all the check’s module/objective pairs, and contains the actual answer, rationale and correction path in its authored content. Put fictional-case labels in learner-visible copy, not only in production notes. A necessary definition, inference or caveat cannot exist only in notes for a self-study course.

For a shared explanation or cumulative check, add optional `Covers: M2/O2; M3/O3` metadata listing the additional module/objective pairs beyond the primary `Module`/`Objective`. Every pair must match the plan. A shared unit may serve separate module rows for different profiles without duplicating content, provided its explanation is suitable for all those profiles. A cumulative solution covers every pair assessed by its check. Review the actual check and answer for every declared objective; a coverage label alone is not proof.

`COURSE_PLAN` Explanation and Check locators point into this canonical source, at an explanatory unit and check respectively covering that module/objective. Historical lessons may remain as background but are not competing authorities for the revised course. Extra sources and optional renderings can link to the primary text.

## Release review and rendering handoff

Review the actual learner surface: self-study uses Learner content plus visible transitions and captions; guided delivery additionally uses the authored spoken explanation. Separate solutions from the learner test packet. Give a renderer enough detail to construct every unit without writing new teaching material. If splitting a dense slide is necessary, update the canonical units/IDs first. Return semantic changes to this source before regenerating a deck.

An independent reviewer must identify: the before/after capability for every profile; the module passages responsible; the transfer question and an answer requiring those ideas; any missing inference; factual support and limits. A terminology-only course, decorative contrast, unfair baseline or unanswered check fails semantic acceptance even when `course_check.py` passes. A successful review or model simulation still does not demonstrate human learning.
