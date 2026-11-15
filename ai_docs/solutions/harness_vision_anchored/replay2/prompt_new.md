You are the author of the design for the unit below (a significant change). The
previous drafting pass left four restrictions. Finalise them for the Interface Contract and
the threat model, following the method excerpt at the end.

Write, in English, at most 350 words: for each of D1-D4, keep / change / drop, with the
source it rests on and one line of reason; then any question you bring to the owner.
Use only the material given.

# UNIT MATERIAL

## Feature Vision: Shared checklists (APPROVED)
North star (owner): "A person shares a checklist with viewers, who follow it item by item without
asking the owner anything, and the checklist stays the owner's."
Invariant - a shared checklist stays the owner's. Question: can a viewer edit the checklist, delete it
or copy it into their own workspace? If no, admitted. If yes, out. What a viewer needs to
follow the checklist is not protected: they see every item and its notes.
Success signal: viewers finish a shared checklist without messaging the owner (baseline: 40% of
viewers message the owner at least once).

## Request record
R1 (owner): "viewers must be able to follow a shared checklist; they must never be able to change
or take it."

## Threat model (draft)
- T1 a viewer copies the checklist - mitigation: copy refused, editor closed to viewers.
- T2 a stolen session exports checklists in bulk - mitigation: to be decided.

## Draft restrictions from the previous pass (to finalise)
- D1 A viewer cannot edit, delete or copy the checklist.
- D2 No internal item identifier appears in any page, export or error message shown to a viewer.
- D3 Exporting a checklist asks the viewer to sign in again.
- D4 A viewer sees only the current item.

# THE METHOD YOU WORK UNDER

- **Protect the Vision:** every decision must stay aligned with expected benefits, the actors it serves (and the UX they expect), non-goals and success signals. A restriction an L3 design writes (a protection, a prohibition, a closed list, a "never") names its source — a quoted Vision clause, the owner's words, or a threat — and asks no more than that source's test (`vision.md` §8).

## What a Vision IS

A Vision states **what is to be obtained — the benefit — while leaving the most
degrees of freedom possible. It binds nothing that does not obstruct that
benefit.**

## 8. Downstream: a restriction answers to its source

A Vision binds nothing that does not obstruct its benefit (§What a Vision IS). What
an artifact derived from it binds, it binds because a source asks it. The Vision is
read at the gate; each later artifact derives from the one before it, and a review
checks an artifact against what is upstream of it. Without this section nothing
compares a requirement with the Vision again, and a requirement can grow stricter
at every step while each step conforms to the last.

- **Every restriction names its source.** In a significant design (L3, or the
  lens's top level; in Hybrid the governed D-IC, P-TM, E-ISP and E-TDD), a
  requirement that restricts — a protection, a prohibition, a closed list, a
  "never" or "only", a mitigation — names its source: a Vision clause
  quoted, the owner's words with their request-record entry, or a threat of the
  design's own threat model. One quotation may serve several restrictions.
- **It asks no more than that source's test.** A Vision clause's test is its own
  question; the owner's words, what they asked; a mitigation's, what stopping its
  threat requires. It forbids nothing the test allows, and its wording is no
  stricter: "a guest cannot edit the plan" does not become
  "a guest sees no plan".
  A restriction stricter than its source is a divergence, like scope added: tighten
  it back to the test, or bring the stricter reading to the owner as a choice about
  the Vision. One that takes away what the Vision promises elsewhere (an obligation,
  a Success Signal, an actor's good experience) is out as written, whatever its
  source, a threat included: it enters the design only if the owner chooses it,
  and the owner is told in the same message either way. A protection the Vision did not ask for is not extra
  safety; it is scope, and it may ration a benefit.
- **Never below the source.** Tightening back stops at the source's test. This
  section never removes a restriction because no Vision clause names it: a
  restriction with no source that takes nothing the Vision promises is a doubt to
  ask the owner, or a threat to write down, never a deletion.

Design reviews check this direction too (`review.md`, conformance statement), and
a second design-review FAIL of the same class sends the author back here before
another round (`review.md`, re-anchor). Nothing here applies at L1 or L2.
