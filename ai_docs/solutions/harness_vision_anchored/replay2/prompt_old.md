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

- **Protect the Vision:** every decision must stay aligned with expected benefits, the actors it serves (and the UX they expect), non-goals and success signals.

## What a Vision IS

A Vision states **what is to be obtained — the benefit — while leaving the most
degrees of freedom possible. It binds nothing that does not obstruct that
benefit.**
