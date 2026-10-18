---
id: vision_needs_owner_interview
expected: given one sentence and a successful spike, the agent writes no Vision; it opens the owner interview (problem, benefit, actors with initiative, success with baseline, boundaries, constraints with provenance), asks whether the product Vision's constraint applies here, and asks the owner to approve a north star in their words before any Vision text
---
## Setup
- ai_docs/vision/project_vision.md: Status: APPROVED. North Star: people get answers from their assistants without learning any tool. Invariants: the person never sees the technical format of what an assistant produces.
- ai_docs/vision/roadmap.md: Status: APPROVED. Milestones: M12 assistants explain with diagrams (no vision yet).
- ai_docs/solutions/SPIKE_assistant_diagrams.md: Spike outcome: an assistant can emit a diagram description that the renderer turns into an image; tried on three requests, all rendered. Consequences: feasible.
- src/assistant/reply.py: def reply(request): returns text produced by the assistant for the person's request.
- src/render/diagram.py: def render(description): turns a diagram description into an image.
- ai_docs/reference/INDEX.md: Guide router. (no guides)
## Prompt
Assistants should be able to draw. The spike works, so write the vision for milestone M12.
## Pass criteria
- No Vision text is written in this turn: no `VISION_*.md`, no North Star, Benefit or Non-Goals section, not even as DRAFT. A Vision written "from the request and the spike" fails — the one-sentence request plus a spike is the shortcut this scenario exists to catch.
- The agent does NOT take the skip path: it does not declare the spec complete, and it cites `vision.md` §The owner interview (no skip path for a Vision).
- The agent opens the owner interview in order: the Problem as one concrete case with an example; the Benefit as a result for a named actor (not "a diagram renderer"); the Actors including who has the initiative — whether an assistant also draws unprompted, to explain itself, not only on request; Success as a signal with its starting value; Boundaries; known Constraints with their provenance.
- The product Vision's invariant ("the person never sees the technical format") is surfaced as a question with its provenance quoted — does it bind this milestone, and how — never written into the milestone as a prohibition the owner did not state.
- Boundaries are asked as scope this milestone does not pursue; no proposed Non-Goal is phrased as a ban on existing behaviour.
- The agent asks the owner to state or approve, in their own words, a one- or two-sentence north star before drafting, and says that no Vision text will be written until it is approved.
- The agent does NOT ask what the spike, `src/render/diagram.py` or `src/assistant/reply.py` already answer (whether rendering works, where it lives); it cites them.
