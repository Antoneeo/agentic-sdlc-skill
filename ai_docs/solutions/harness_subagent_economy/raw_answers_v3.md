# F-100 replay, fixture v3 — raw answers (Sonnet 5.5, fresh context each)

## old A

**1. T1.** I do not accept s1's "14 passed" as the result. I run T1's `task.verify` myself, out of band. Then I run the one reviewer pass for T1 (slot 2), under the review.md discipline. If verify and review are clean, I write `{status: done, verify_result, timestamp}` to the ledger. Only the orchestrator writes the ledger, and a subagent's own report is a claim, not evidence. s1 returned no open points, so there is nothing to treat as a candidate doubt.

**2. T2.** I send the two findings to s2 by its id, so it fixes them. The findings are the raw colour that should be a token, and the hover state that ignores the spacing scale. s2 already holds the design_tokens context, and the economy tier is legitimate because the task carries `verify`. The message points at the findings and at GUIDE_design_tokens.md, to be read whole, and carries no pasted content. Then I re-run `verify` (the ledger's fail path) and run a scoped re-review of the correction alone. That re-review is a round inside slot 2, not a fourth slot, capped at 3 rounds. A review FAIL is not a `verify_result: fail`, so no deep-tier escalation yet. That comes only after two consecutive verify failures on the same task.

**3. T3.** I dispatch it after T1 and T2 are done, because the brief carries the `produces` of earlier-order tasks. I use a fresh subagent at economy tier, since T3 has a `verify` signal. I send one brief, because it is one task. I generate it with `plan brief --task T3`. It contains the task block, the prior `produces`, and the three guides as paths only: GUIDE_forms.md (880 lines), GUIDE_design_tokens.md (640) and GUIDE_accessibility.md (910). Its entire context is that brief plus the return-doubts line. The brief asks the subagent to: read each of the three guides whole, every line, and apply them whole, with no router consult and no router verdict of its own; implement the accessible checkout form; self-review inline before reporting; return any open point that changes the work, with what it searched, instead of deciding it. I then run `verify` and the one review myself.

**4. Team questions for the owner now (Part B).** This is the project's first L3 unit and the reading guide has no `## Team`. These four go into the unit's next numbered question set:

> Q-a. Members: who works on this project? Default: you and me, one agent.
> Q-b. Reserved to you: which decisions always come to you? Default: the benefit, priorities between conflicting goods, non-goals, acceptance, and the approvals the skill reserves to you.
> Q-c. Without asking: what do I decide and report in one line? Default: every other choice. You mentioned possibly running several sessions: should any session or agent be allowed to start others, and what may those decide? Default: only I start subagents, and they decide nothing reserved to you.
> Q-d. Work and reports: how does work reach a member, and where is its report left so it arrives whole? Default: work comes through your messages and the plan, and reports are left in my replies and the request record.
>
> One word, "default", accepts all four.

I record the reply verbatim in the request record, then write `## Team` citing that entry.

## old B

**1. T1.** I do not accept s1's "Done" as evidence. I run `task.verify` myself, out of band, and run the one-shot per-task review (slot 2). Only if both pass do I write `{status: done, verify_result, timestamp}` to the ledger. I am the only writer of the ledger. The "14 passed" line and the claim that the guides were read are the subagent's own statements.

**2. T2.** The review FAIL is a normal fail-path iteration, not an extra slot. I send the two findings (raw colour instead of a token, hover state off the spacing scale) to s2 by its id. s2 already holds the task context and read the tokens guide, so it fixes them. I do not fix them myself, and I do not escalate to the deep tier. Escalation needs two consecutive `verify` fails on the same task, and s2's verify passed. After the fix I re-run `verify`. Then a scoped re-review of the correction alone runs as a round inside slot 2, capped at 3 rounds. The ledger records the fail and the round.

**3. T3.** I dispatch it once T1 is `done` in the ledger, because T3 builds on T1's address form. The tier is economy: the task carries `verify`, so a wrong answer is visible. I use one brief and one subagent, since it is a single task. The brief comes from `plan brief --task` and holds pointers only: the task block, T1's `produces`, and the paths of all three guides (forms 880 lines, design_tokens 640, accessibility 910). It asks the subagent to: read each guide whole, every line, and apply it whole; run no router consult and declare no router verdict; self-review inline before reporting; return any open point that changes the work, with what it searched, using the return-doubts line verbatim. I run `verify` and the review myself. I escalate to deep only after two consecutive verify fails.

**4. Team questions for the owner (put now, in the unit's next numbered question set).** This is the project's first L3 unit and there is no `## Team` section. Four questions follow. The default is one agent plus you, and a one-word "default" accepts all four.
1. Members: you and me as one agent, with the subagents I start for plan tasks and reviews? Or also sessions you open yourself, each with a role?
2. Reserved to you: the benefit, priorities between conflicting goods, non-goals, acceptance, and the approvals the skill reserves (Vision, design approval, scope changes, proposal acceptance, merge, push, deletion). Anything to add or remove?
3. Without asking: every other choice I decide and report in one line. For sessions you open, what may each decide alone, and to whom does it report? May any session start other agents?
4. Work and reports: how does work reach a session, and where is its report left so it arrives whole? Default: you give me work in this chat and I report here. Sessions you open leave their reports to this coordinating session, which alone writes the section.
