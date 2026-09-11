---
description: F-051 - lower the price of the mandatory read without losing the process. Moves the Hybrid/devPNT seam out of SKILL.md into a triggered support file; deletes no rule, loses no trigger, and states for every candidate NOT cut why it stays.
status: COMPLETED
end_date: 2026-09-11
feature: F-051
id: F-051
start_date: 2026-09-11
level: L3
branch: main
---
# ANALYSIS: The Mandatory-Read Diet (F-051)

**Level: L3 · router: `GUIDE_release.md` → read** (a NEW support file must reach the package allowlist, which is that guide's step 2).
Elicitation: skip path — the spec is the owner's directive of 2026-09-11 ("procedi con la potatura di SKILL.md ma pesa molto bene il valore di quello che ti appresti a potare"). Probes: `harness_mandatory_read_diet/probe.py`.

## The weighing, before the cut

`benefit` (F-050) prints the cost side: **SKILL.md is 49,645 bytes every session
must read**, against a catch rate of 68% that has not moved in three releases.
But the byte count is the only measure that exists. There is **no per-paragraph
benefit measure**, so "this reads verbose" is exactly the unmeasured judgement
this sequence spent three units learning to distrust. The rule for the cut is
therefore:

> **Delete no rule. Move only what a session provably cannot use, and only where
> the trigger that summons it back is mechanical.**

### What is NOT cut, and why it earns its bytes

| Candidate | Bytes | Why it stays |
|---|---|---|
| Rule Zero triage + the rationalization table | 4,230 | The triage decides every downstream cost, and the table is the anti-self-deception device that makes "it's just a fix" recognizable as a thought to stop on |
| Write Triggers | 5,459 | The authoritative write index — one event, one destination. Without it documents silently stop being written, and nothing detects that |
| Execute-Before-Specify | 3,065 | The only rule in the file carrying a **measured** before/after: eight consecutive design-review FAILs converged to PASS in one round once claims were executed. Cutting the one thing with evidence would invert the method |
| Blast-radius enumeration | 809 | Same class, and `review.md` cites this paragraph as the owner of a finding class |
| Design review gate | 1,551 | The gate that produces the 68% the report measures |
| Claim-to-evidence (Closure) | ~1,200 | The completion-claim discipline; every review this month found an instance of it, including two of mine |
| Conditional-section triggers (Functional Spec, Interface Contract, Capability Ledger) | 3,163 | Each is an owning definition `review.md` cites as a finding class; absence would silently disarm three checks |

### What is cut, and the evidence that it is safe

| Block | Bytes | Evidence |
|---|---|---|
| `## Coexistence with devPNT (the Hybrid seam)` | 4,733 | Reachable **only** when `devpnt_*` tools are present. Zero battery pins on its content — `Coexistence`, `ownership matrix`, `Triage equivalence` and `Shadow discipline` appear in no test file in any lens (verified by extracting every line >25 chars of the block and searching all 148 test/eval files at HEAD: zero hits). No logged finding traces to it either: `REVIEW_LOG.md` has 15 lines / 20 occurrences of "hybrid", and every one is the validator's `--hybrid` FLAG or a mode note — the flag is code and stays untouched |
| Hybrid half of `## Operating Modes` | 1,197 | Same trigger, same evidence |

Both are **moved, not deleted**, into a new per-lens support file `hybrid.md`,
summoned by a pointer that states the mechanical trigger.

**The cost, counted on both sides, because the Vision's ceremony clause says
relocated cost must be counted and r8 resolves omission against the proposal:**

| Session | Before | After | Delta |
|---|---|---|---|
| **Standalone** (the common case) | 50,001 B | 45,279 B | **−4,722 B (−9.4%)** |
| **Hybrid** | 50,001 B | 45,279 + 6,657 = 51,936 B | **+1,935 B (+3.9%)** |

So this is a Standalone saving **paid for by a small Hybrid surcharge** — the
pointer and the new file's preamble are real bytes, and the gross 11.9% removed
is not the net figure. Said plainly rather than left to be discovered: the diet
helps the majority and costs the minority slightly. The alternative (leave it
inline) charges the majority for a seam it cannot reach.

**The residual risk, stated plainly**: a Hybrid session that ignores the pointer
loses the ownership matrix and may create a second source of truth in `ai_docs/`
— the exact failure that section exists to prevent. That is why the pointer
carries the trigger AND the consequence rather than just a filename, why the
battery pins that the pointer exists, and why this is a move that one commit
reverses.

## Vision Alignment

Goal 4, verbatim: *"Scale process cost to risk, in both directions … Cost
includes what the agent must read: the instructions and documents it loads are
part of the price of the process, and **lowering that price without losing the
process is real work**."* This is that Goal's first deliberate exercise. The
ceremony Non-Goal is engaged and counted (the table above), not waved past: the
Standalone read falls and the Hybrid read rises slightly. **The admission test
does not apply**: it governs proposals that add or change *what the product
does*, and this changes neither purpose nor actors nor capability — only cost —
which is the bounded maintenance exemption (ledger r14). Stated here rather than
left implicit, because r8 binds on the exempt path too. r10 (a second triage
authority) is not crossed: the triage-equivalence table still ships, the pointer
names it, and `SKILL.md`'s Rule Zero remains the single authority.

## Use Cases / User Needs

- **UC1 — the Standalone session** (the common case) stops reading 4,722 bytes of devPNT ownership rules it cannot act on.
- **UC2 — the Hybrid session** reaches the same content through a pointer whose trigger is mechanical: `devpnt_*` tools present and pointing at this project.
- **UC3 — the owner judging the next unit** sees the mandatory read fall for the first time, so `benefit`'s cost term becomes a number that can go down as well as up.

## Functional Spec

1. `SKILL.md` loses the two Hybrid blocks and gains a pointer naming the trigger, the file, and what is lost by skipping it.
2. `hybrid.md` carries the moved content **verbatim** — a move, not a rewrite. Any rewording would make this unit unreviewable as a diff.
3. The mandatory read drops measurably: `benefit` reports a smaller `SKILL.md` figure after than before.
4. No rule, trigger, table row or finding class is removed anywhere.

## Interface Contract

Trigger fired, narrowly: the agent reading `SKILL.md` is the actor, and the
surface it perceives changes — two sections become one pointer. The contract:
the pointer states the mechanical trigger (`devpnt_*` tools present), names
`hybrid.md`, and says what is lost by skipping it (the ownership matrix, the
triage equivalence, the shadow discipline). No other surface changes; the
validator's commands and outputs are untouched.

## Capability Ledger

All capabilities EXIST: the support-file pattern (eleven files today), the
pointer-with-trigger idiom (`routing.md` is read only in multi-lens installs by
exactly this mechanism), the package allowlist and README support-file list a
new file must join, and `benefit` to measure the result. Nothing is built.

## Impact

| Path | Change | What |
|---|---|---|
| `skills/agentic-sdlc-skill/SKILL.md` | MODIFY | remove the two blocks, add the triggered pointer |
| `skills/agentic-sdlc-skill/hybrid.md` | ADD | the moved content, verbatim |
| `package.json` | MODIFY | `files` allowlist — `postinstall` can only copy what the tarball carries |
| `README.md` | MODIFY | support-files bullet and Runtime Shape tree (`GUIDE_release.md` step 2) |
| `scripts/test_skill_invariants.py` **(shared battery)** | MODIFY | pin the pointer, and the conservation check below; conditional on the lens that has `hybrid.md` |
| `ENFORCEMENT.md` (code lens) | MODIFY | an **inbound citation** — it said "see the SKILL.md shadow discipline", which after the move points into a file that no longer holds it. Inbound citations are the blast-radius axis specific to a relocation, and the first draft of this analysis did not enumerate them |
| `scripts/sdlc_core.py` **(spine)** | MODIFY | same class, but shared: the comment naming `SKILL.md`'s ownership matrix drops the filename rather than repointing, so it stays true in all three lenses |
| `scripts/sdlc_check.py` (lens profile) | MODIFY | `support_files` must declare `hybrid.md`, or the battery refuses it in both directions |
| `harness_mandatory_read_diet/probe.py` | ADD | P1-P4 |
| closure artifacts | ADD/MODIFY | ADR, HANDOFF, REVIEW_LOG rows, generated manifests |

Blast radius: `SKILL.md` is per-lens (`shared_files.py` `NOT_SHARED_ON_PURPOSE`),
so kb and mkt keep their own Hybrid material — a deliberate scope limit. It is
recorded in this unit's HANDOFF as the named follow-up, not left as an intention. The shared battery runs in all three
lenses, so its new pin must not fail where `hybrid.md` does not exist.

## Security and Threat Model

No code path, no input parsing, no new execution. One surface: a new file must
join the package allowlist, or an installed skill carries a pointer to a file
that is not there — a dangling instruction, worse than the inline text it
replaced. That is why `package.json` and the README are in the Impact and pinned.

## Action Plan

1. Harness RED.
2. Move the blocks verbatim; write the pointer; update allowlist and README.
3. Battery pin; harness GREEN; three batteries; `benefit` before and after.
4. Design review, closure review.
5. Closure: ADR, REVIEW_LOG rows, registration, `mark`.

## Test Strategy

The strong assertion is a **conservation check**: every heading and every bold
lead that leaves `SKILL.md` must appear in `hybrid.md`, so the diff is provably a
move and not a quiet deletion — the one failure mode a pruning unit has. Plus:
the pointer names the trigger; `hybrid.md` is in the package allowlist (a
dangling pointer is the shipped failure); and `benefit` reports a smaller
mandatory read after than before, which is the first time this project measures a
cost going DOWN.

## Diary

- **2026-09-11 (closure) — the move is sound; everything around it was not.** Closure PASS (0 BLOCK), design FAIL (4 BLOCK), both folded. Conservation was proved twice and mechanically — as a multiset of lines and byte-exactly — so no doctrine was lost. The four blockers were: an **inbound citation** left pointing into a file that no longer holds its target (the weighing enumerated tests and the log, and never asked who CITES the moved sections — the blast-radius axis a relocation has); a **one-sided cost claim** that reported the Standalone saving and never that the Hybrid read rises; an evidence number that did not reproduce; and, for the third unit running, **a probe that could not fail** — P2c matched a word the pointer's own inventory contains, so deleting the entire consequence paragraph left it green until the reviewer mutation-tested it.
- **2026-09-11 — opened.** Driver: the owner's instruction to prune, with an explicit warning to weigh what is being pruned. The weighing is deliberately the FIRST section: seven blocks are named as not-cut with the reason each earns its bytes, and the two that go are moved rather than deleted, on the evidence that no battery pins them and no logged finding traces to them.
