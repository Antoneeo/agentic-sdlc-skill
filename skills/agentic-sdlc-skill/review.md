# Code Review Discipline

Applies at closure of L2/L3 work, and to any independent review slot in this
skill or in a connected governance layer — devPNT's §4.5/§4.6 review gates,
and any future review step added to the workflow. This is the single
definition of how to request, receive, and perform a review; other places
that need review behavior point here instead of restating it (DRY).

## Requesting

When you hand work to a reviewer (human or agent), give them:

- **Scope**: what changed and why, in one or two lines.
- **The authoritative design artifact**: the ANALYSIS, E-TDD, or equivalent
  the change was built against — not a paraphrase of it.
- **The actual diff**: the real changed files, not a description of them.

Never ask a reviewer to "review my session" or "review what I just did"
without the artifacts above — that forces them to reconstruct scope from
conversation instead of reviewing the change itself. Say which finding
classes you want covered (correctness, security, conformance to the design,
test coverage) if the default scope is not obvious.

## Receiving

**MUST answer findings one by one — fix, or justify with evidence; why:
silent drops turn review into theater** — a review whose findings are not
tracked to a resolution gives the appearance of quality control without its
substance.

If you disagree with a finding, say so explicitly with your reasoning; never
resolve a disagreement by rewording the finding until it goes away. When the
project keeps a `REVIEW_LOG` (or equivalent), log the outcome of each
finding there.

## Reviewing

When you are the reviewer:

- Verify claims against the real source, not against the diff's own
  description of itself.
- Cite evidence as `file:line` for every finding — a finding without a
  location is not actionable.
- Keep severity honest: do not inflate a style preference to a blocker, and
  do not soften a real correctness or security issue to a nit.
- No praise padding. A review reports problems and their fixes, not a
  summary of what looks fine.

## Anti-patterns

- **Batch-dismissal**: closing out a whole findings list with one blanket
  reply instead of addressing each finding individually.
- **Rewording instead of addressing**: editing the finding's text to look
  resolved without changing the code or providing evidence it is a
  non-issue.
- **Scope-creep findings**: raising issues unrelated to the change under
  review instead of filing them separately.
