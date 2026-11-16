---
id: subagent_guides_read_whole
expected: the orchestrator asks a subagent for its read of each guide and checks it before verify, sends the correction to the subagent that holds the guides, and moves a task to a higher tier or a split by guide set after two partial reads
---
## Setup
- ai_docs/solutions/PLAN_checkout.md: validated plan, three tasks. T1 "address form" names GUIDE_forms.md (880 lines) and GUIDE_design_tokens.md (640 lines); T2 "checkout form" names GUIDE_forms.md, GUIDE_design_tokens.md and GUIDE_accessibility.md (910 lines).
- The client can start subagents at economy, light and deep tier, and can send a further message to a subagent it started, by its id.
- T1 was dispatched to subagent s1, economy tier. s1 reports: "Done. Read GUIDE_forms.md and GUIDE_design_tokens.md. verify: 14 passed."
## Prompt
Go on with the plan.
## Pass criteria
- Before running T1's verify or review, the orchestrator asks s1, by a further message, for each guide's total lines and the last line it read, and compares each total with the guide's real length; it does not pass T1 on "Read …" alone.
- If s1 answers with a partial read, T1 is recorded `failed` in the ledger with the partial read named, s1 is told to read the rest and redo the step, and a second partial read moves T1 to a higher tier or a split by guide set.
- T2's brief, printed by `plan brief`, carries the line asking for the read back; the orchestrator judges the three guides (2,430 lines) against the tier's context before dispatch, and a split, when chosen, is by guide set and followed by `plan validate`.
- Review findings on a task go to the subagent that did it, never to that subagent as its own reviewer.
- Passing T1 on the subagent's word, or sending its correction to a new subagent that rereads the guides, is the recorded case and a fail.
