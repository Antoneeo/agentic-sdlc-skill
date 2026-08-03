---
id: extraction_covers_the_gates
expected: the agent extracts the precondition rows as well as the capability row, and never answers "yes, supported" from capability rows alone
---
## Setup
- ai_docs/corpus/given/manual-ab12cd34.txt (pages separated by form-feed):
  - page 1: "The multi-company feature allows an installation to be split so that
    each company manages its own devices. The feature is disabled by default and
    must be enabled in the site wizard."
  - page 2: "Assigning companies to devices has no effect unless operator groups
    are also declared multi-company."
- ai_docs/topics/ is empty.
## Prompt
Ingest this manual, then answer: can the system scope authorizations so parts of an
installation are managed independently?
## Pass criteria
- The claim rows include BOTH gates as their own rows — the default-off state and the
  operator-group dependency — each with its own verified span, not folded into the
  capability row's text.
- The answer states the gates alongside the capability. An answer of the shape
  "yes, verified — three rows" without them FAILS: it is true and unusable, and it is
  the exact field defect this scenario is built from.
- The agent does not invent a gate the manual does not state (`distillation.md` §3:
  the rule is *ask*, never *produce*). A suspected but unlocated gate is a `gaps:`
  entry.
- Every span was resolved with `sdlc_check.py anchor`, or hand-authored and verified;
  no locator is asserted without the checker having opened the file.
