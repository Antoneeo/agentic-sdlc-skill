---
id: F-027
feature: Field-test defects — lens identity, FACT laundering, verdict return path
status: COMPLETED
level: L3
start_date: 2026-08-02
end_date: 2026-08-02
---

# ANALYSIS — Field-test defects

## Objective

Close the three defects a cold-agent field test surfaced in the packages published on
2026-08-02 (code 1.20.2, kb 1.0.0, mkt 0.3.0), and close the holes that let each one
ship. Every defect is a *guard that did not guard*, not a missing feature.

## Use Cases / User Needs

- **A user installing kb or mkt** gets a multi-lens routing note that names the lens
  they installed, so the note can be acted on rather than corrected.
- **A marketing engagement's reader** can trust that a number classed `FACT` came from
  the client, not from research that skipped the URL its class would have owed.
- **An orchestrator running a review gate** receives the verdict where it actually
  arrives, instead of stalling on a delivery channel that failed silently.

## Capability Ledger

| Capability | Verdict | Where it lives |
|---|---|---|
| Name each family lens by its skill directory and lens word | **EXISTS, INADEQUATE** | `routing.md` holds the authoritative table (byte-identical, drift-guarded); `init.js` restated it as literals |
| Reject a ledger row whose class does not match its evidence | **EXISTS, INADEQUATE** | `mkt_check.py` `run_ledger` enforced it for `BENCHMARK` and `ASSUMPTION`, never for `FACT` |
| Deliver a review verdict to its requester | **MISSING** | `review.md` said what a verdict must contain, never where it travels |

## Impact

| Path | Change | Why |
|---|---|---|
| `scripts/lib.js` ×3 | MODIFY | `lensTable()`/`selfLens()`/`siblingLenses()` parsed from `routing.md`; exported as lazy getters |
| `scripts/init.js` ×3 | MODIFY | consume the derived table; drop the `SIBLING_LENSES` literal and the hardcoded self row |
| `scripts/test_clients.js` ×3 | MODIFY | assert the note names THIS lens with no duplicates; derive `A_SIBLING` from `lib`, not from the file under test |
| `mkt_check.py` | MODIFY | `FACT` with no source, or sourced to one of our own documents, is an error; client-origin cells exempt |
| `test_mkt_check.py` | MODIFY | one test per rejection branch, plus three client-origin rows that must still pass |
| `research.md` (mkt) | MODIFY | state the two legal `FACT` origins and why the class is the weak flank |
| `review.md` ×3 + manifests | MODIFY | the verdict travels as the reviewer's final output; cross-referenced from `## Reviewing` |
| `strategic/skill_family_agent_workflows.md` | MODIFY | derived doc: its ledger clause attributed the "see VOC.md" rejection to `BENCHMARK` alone |

Blast radius: `lib.js` is required by `init.js`, `postinstall.js`, `preuninstall.js` and
`test_clients.js` in every distribution. The lens lookup is therefore **lazy**: only a
consumer that asks for `SELF_LENS`/`SIBLING_LENSES` reads `routing.md`, so uninstalling
an installation that lost that file still works.

## Security and Threat Model

| Threat | Answer |
|---|---|
| A wrong `routing.md` silently changes every distribution's self-identity (it is drift-guarded to be *identical*, not *correct*) | a duplicate row for one skill name is refused with `routing.md lists 'X' more than once`; a missing row and a reordered table both throw |
| The `FACT` rule pushes an author to misclassify their client's own Markdown data file as a `BENCHMARK` with an invented URL | a Source cell that opens by naming the client (`user`/`client`/`owner`, and the Italian forms) is exempt |
| The `FACT` rule reads as mechanical enforcement when it is a tripwire (`'our VoC deck'`, `'research/VOC.txt'` still pass) | recorded here and in the Diary; `research.md` states the rule so the author knows it before the validator speaks |

## Test Strategy

- **Mutation-tested guard**: re-introducing the literal self row makes `test_clients.js`
  fail with the field-observed symptom (`it listed: agentic-sdlc/code, agentic-sdlc/code`).
- **One test per branch** on the `FACT` rule — the field-test row tripped both at once,
  so either branch could have been deleted with the suite still green.
- **End-to-end**: three fresh `init` runs, one per distribution, asserting each note
  names its own lens exactly once with no duplicates.
- **Fault injection**: `routing.md` removed (lib still loads, `SELF_LENS` throws);
  duplicate row injected (refused).

## Diary / Current State

**2026-08-02 — closed.** Three defects, all found by cold agents operating the published
skills, none by a static pass. Root cause is the same in two of them: an authoritative
table existed (`routing.md`; the ledger class rules) and a second copy of it was
maintained by hand next to the first. The fix deletes the copy rather than aligning it.

The independent closure review returned **FAIL** with one BLOCK and seven WARNs, and
every one was real: the derived family doc still carried the old ledger clause, the
first `FACT` regex rejected a client's own `.md` file, the `SELF_LENS` IIFE made
`routing.md` a hard dependency of *uninstall*, the sibling lens words were still
literals one row from the ones just removed, and a duplicate `routing.md` row won
silently. All eight are closed in this unit.

Residual, deliberately: the `FACT` check is a tripwire on the observed spellings, not a
proof — `'our VoC deck'` still passes. Making it a proof means deciding what a source
cell may contain, which is a doctrine change, not a validator patch.
