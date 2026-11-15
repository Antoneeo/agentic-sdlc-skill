# The team is asked at the first L3 unit

## Prompt

A project's reading guide (`ai_docs/README.md`) has no `## Team` section and no request record exists. The owner asks for a new course that teaches their support staff to apply the returns policy. What does the first message to the owner contain?

## Expected

The agent declares L3, opens the request record, and puts to the owner one numbered set of questions that includes the four team questions with the default offered. It asks them once and writes no `## Team` section before the reply.

## Pass criteria

- Declares the level L3 and opens `audit/requests/REQUEST_course_<slug>.md` with the owner's words.
- Asks, in the same numbered set as the course's own questions: who is in the team; which decisions stay with the owner; what each member decides without asking and to whom it reports; how work and reports pass.
- Offers the default so that one word accepts all four.
- Does not treat the simulation's roles (principal, independent readers, didactic reviewer) as the team to be asked about.
- Asks nothing about the team when the reading guide already has a `## Team` section, or when the request is below L3.
