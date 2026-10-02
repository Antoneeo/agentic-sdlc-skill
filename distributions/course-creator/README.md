# Course Creator — beta

`course-creator` helps an AI agent create a course for a defined learner. It maps what the learner already knows, orders concepts by prerequisite, writes explanations in progressive modules, and links factual statements to reopenable sources. Independent fresh learner agents can expose confusing steps; their results are diagnostic. The course is labeled **efficacy not verified** until enough evidence from real learners supports a narrower claim.

The package is the fourth lens of the Agentic SDLC family. It uses the shared `ai_docs/` project memory and governance. Version 0.1.0-beta.1 supports Standalone mode. This is an experimental beta: the authoring method and artifact contracts may change; human learning efficacy has not been established. Its course artifacts remain readable without the skill.

## Install and initialize

```sh
npm install -g @antoneeo/course-creator@beta
course-creator-install-skill
cd YOUR_PROJECT
course-creator-init
```

The installer detects Claude Code, Gemini CLI, Codex and Google Antigravity. Initialization creates absent `ai_docs/` files and a project protocol pointer; it does not overwrite existing project documents. Use `python <skill_dir>/scripts/sdlc_check.py check --root .` to validate the shared SDLC and course structures.

Using the skill in your own project carries no obligation to publish your course or its sources. See [LICENSE](LICENSE) for the software terms and [NOTICE](NOTICE) for attribution.

## Primary course output

New courses deliver a complete textual source for every slide (`SLIDE_CONTENT.md`), with exact learner copy, full explanations, examples, visual contents, transitions and answers. PPTX and other renderings are optional. Explicit non-slide requests retain a complete textual source for their units. Every course must show distinguishable value for its audience through an explanatory contribution and a transfer task; structure or simulated success does not establish human efficacy. See `skills/course-creator/slide_content.md`.

Course design now uses outcome-first evidence, teaching/assessment alignment, visible worked reasoning, proportionate support, cognitive-load management and retrieval opportunities. `learning_design.md` records the pedagogical sources and the source-informed semantic review rubric; a locator table or structural PASS is not proof of learning.

