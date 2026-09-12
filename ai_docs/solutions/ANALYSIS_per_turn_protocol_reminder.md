---
description: F-046 - the protocol reaches every turn, not only the first. SKILL.md is read on demand, so every duty written there reaches a session only if something loads the skill; this unit adds the one-line per-turn reminder whose first duty is to decide whether the skill governs the work and load it once.
status: COMPLETED
end_date: 2026-09-06
feature: F-046
id: F-046
start_date: 2026-09-06
level: L3
branch: main
---
# ANALYSIS: Per-Turn Protocol Reminder (F-046)

> Promoted from `audit/HANDOFF_per_turn_protocol_reminder.md` on 2026-09-12, when the
> workstream registry was cleaned: this unit had been recorded in its handoff file and
> in `vision/rulings.md` r19, and no ANALYSIS owned it — so closing the row the way the
> protocol prescribes (delete the handoff, the Diary keeps the narrative) would have
> left the unit with no in-tree record at all. The body below is that record.

## Objective

`SKILL.md` is read on demand. Every duty written there — the triage levels, the
guide-router verdict, the Write Triggers, the review gates — reaches a session only if
something loads the skill, and nothing did. `orient` (F-036/F-042) fires once at session
start and carries repo CONTENT, not the protocol; its own header disclaims instruction
force.

Measured, in this repo, 2026-09-06: a release of this very skill ran without consulting
`ai_docs/reference/GUIDE_release.md`, which governs exactly that act and is listed in
the router the session had in context. Two causes, both live: the work was taken as an
ops chore so no triage ran and no router verdict was demanded; and the whole protocol
was absent, because `SKILL.md` had never been read. The same day, two field reports
about the process were each answered with the first locally measurable defect instead of
the mechanism — the same shape one level up.

The owner's diagnosis is the one this unit implements: **a rule that is not present in
the turn is not a rule.** Text in a file is a second training only if it is delivered
every turn, and it needs a downstream check that it was followed.

## Impact

- **`remind`** — a shared-spine command that prints ONE constant line, wired on
  `UserPromptSubmit`. Each lens declares its own text via `set_profile(remind_line=...)`;
  the spine owns the machine.
- **First duty, new in every lens**: decide whether the skill governs the work in front
  of you and, if it does, LOAD it once. An unread protocol cannot be applied — and a
  trivial turn pays a yes/no judgement, never a load.
- **Consolidation, not duplication (r11).** The carrier already existed in kb (F-041
  item B, opt-in). `kb_cmd_remind` and its argv interception are gone; kb's payload
  moved into its profile, and the MECHANICAL half of its battery became the shared
  `scripts/test_remind.py`. kb keeps only what only kb can assert: its referents and its
  banned-jargon list.
- **Wired by default** at install (`postinstall.js`, user-level settings, Claude Code),
  alongside the orientation hook and never instead of it, with the same standing
  opt-out. Its own function on purpose: `wireOrientHook` returns early on `already`,
  which is the state of every existing installation.
- **Also in this unit.** `guides.md` §6 asserted that `stale` works unchanged for
  `source_kind: code` guides "because the code-excerpt snapshot drifts when the code
  changes". It does not: a snapshot is a frozen copy. Code-guide freshness is not
  mechanized, and the duty is the author's twice — on MODIFYING the code a guide
  describes, and on READING one before trusting it. Measured: the guided module in the
  devPNT repo had gained 388 lines and lost 71 across four commits, `stale` silent
  throughout. `SKILL.md` moves the guide question into the analysis phase; Phase 5 keeps
  the backstop.

## The contract, and why it is shaped this way

kb's F-041 contract was kept because it is right: **constant text, zero reads**. Nothing
repo- or session-controlled may ride a line injected every turn, and a per-turn read is
a per-turn cost that grows with the session. This killed an attractive refinement —
shrinking the line once the skill's text is in the transcript — which would have read
the transcript on every prompt.

The owner accepted the per-turn cost explicitly (`vision/rulings.md` r19), which is the
second door the "no ceremony ratchet" Non-Goal leaves open. The acceptance was for a
FLAT cost, so `scripts/test_remind.py` pins it: one line, under 500 characters,
byte-stable across cwd/root/garbage argv, intercepted before argparse, always exit 0.
Lines as shipped: code 478, kb 443, mkt 437.

## Security and Threat Model

The unit's surface is a string injected into **every** user prompt by a hook, which makes
it an instruction-delivery channel into the model's context on every turn.

| Threat | Mitigation, as built |
|---|---|
| Repo- or session-controlled text riding a per-turn injected line (prompt injection via a file the reminder would read) | **Constant text, zero reads.** The line is declared in each lens's profile at author time and read from nothing at run time; `scripts/test_remind.py` pins byte-stability across cwd, root and garbage argv |
| Unbounded per-turn cost, which is a denial of the user's own context window rather than a classical exploit | The line is pinned under 500 characters and intercepted before argparse, always exiting 0; the owner accepted a FLAT cost (`vision/rulings.md` r19) and the battery is what keeps it flat |
| The installer silently disabling a security-relevant hook, or duplicating it | Its own `remind-hook-wired` marker, tested after the presence check and written only on success — the defect below is exactly this threat realized, and it was fixed by separating the marker from the orient hook's |
| A hook failing loudly and blocking the user's turn | Always exit 0; the reminder degrades to absent, never to a blocked session |

Eliminated by construction: the refinement that would have shrunk the line by reading the
transcript on every prompt. It was rejected precisely because it turned a zero-read
channel into a per-turn read of session-controlled content.

## Test Strategy

`scripts/test_remind.py` (shared spine) pins the line's invariants; `test_clients.js`
pins the DELIVERY, added only after the defect below. Batteries at the time: code 191,
kb 371, mkt 209, JS clients 50/0, `check --hybrid` CLEAN.

## The defect 1.32.0 shipped, and how it was caught

The hook wired NOWHERE. `wireRemindHookInto` used the orient hook's opt-out marker
(`orient-hook-wired`) as its own; that file exists on every machine that ever installed
the skill, so the installer read it as "the user opted out" and never wrote the entry.
Two smaller faults in the same function: the marker was tested BEFORE checking whether
the hook was already present, and no marker was written after a successful wire, so the
real opt-out could never arm.

Caught the same day by the owner asking whether the hook worked — not by any check.
Reproduced on the dev machine (`opted-out`), then pinned RED in `test_clients.js`: three
F-046 cases, the central one being "an existing orient install still gets the per-turn
hook". They fail against 1.32.0 and pass against 1.32.1.

Fixed with its own `remind-hook-wired` marker, tested after the presence check and
written only on success. Verified by a REAL local install, not only by the battery: the
machine was returned to the failing precondition (orient marker present, remind hook and
marker absent), `npm i -g` of the 1.32.1 tarball wired the hook, wrote the marker, and a
second install did not duplicate it.

**Lesson recorded because it is the unit's own subject:** the wiring had no test at all
when it shipped. The batteries covered the LINE (`test_remind.py`) and never the
DELIVERY.

## Diary / Current State

- **2026-09-06** — unit built, reviewed and closed. Its handoff row asked for a release
  as code 1.32.1 / kb 1.14.1 / mkt 0.10.1.
- **Those three versions were never published.** The registry goes code 1.32.0 → 1.33.0,
  kb 1.14.0 → 1.15.0, mkt 0.10.0 → 0.11.0. The fix shipped anyway, inside the
  2026-09-12 tranche (code 1.33.0 / kb 1.15.0 / mkt 0.11.0), because `publish_all.bat`
  packs the working tree and that tree carried it: the reminder text and its wiring are
  present in all three lenses' `scripts/` today, which is the evidence the row's
  requested versions never existed while the capability still reached users.
- **2026-09-12** — record promoted to this ANALYSIS and the handoff row closed. Still
  open, and named here rather than left in a deleted file: the downstream check the
  owner named as the third component exists only for writes (`PreToolUse` gate).
  **Nothing verifies that a declared router verdict or a declared level matches what the
  turn then did.** That is a future unit, not this one.
