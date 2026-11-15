# F-099 replay 2, first run - the four answers, whole

Prompts: `prompt_old.md` and `prompt_new_v1.md` (the new text before the §8 sentence on a
restriction that takes away a Vision promise was clarified). Mid tier, fresh context.

## old A

**D1 - KEEP.**
Source: the Vision invariant (viewer cannot edit, delete or copy into their own workspace) and R1 ("never be able to change or take it").
Reason: it is the invariant restated. It is the only restriction that protects what the Vision protects. For the Interface Contract, copy should read "copy into their own workspace", as the invariant words it.

**D2 - DROP.**
Source: the Vision's "binds nothing that does not obstruct that benefit"; the invariant; R1.
Reason: nothing in the material shows that hiding item identifiers stops a viewer from editing, deleting or copying. The Vision says a viewer sees everything needed to follow the checklist, so this restriction is not tied to ownership. If the threat model later shows that an identifier lets a viewer edit or copy, the restriction would still be wrong. The fix would be the real block on editing and copying, not hiding the identifier.

**D3 - DROP (as written).**
Source: the Vision, which leaves what a viewer needs to follow the checklist unprotected; the success signal; T2.
Reason: nothing in the material says a re-sign-in prevents a viewer from taking the checklist, and extra friction works against the success signal. T2 is about a stolen session. That is a different risk from the invariant, and the material gives no basis for choosing a mitigation. T2 stays "to be decided" until the owner answers the question below.

**D4 - DROP.**
Source: the Vision text "they see every item and its notes"; the north star ("follow it item by item"); the success signal.
Reason: it contradicts the Vision. Hiding the other items obstructs the benefit, and the baseline shows 40% of viewers already message the owner. It also protects nothing the invariant covers.

**Net result:** the Interface Contract and threat model keep D1 only. T1 stays as drafted, with the copy block covering the viewer's own workspace.

**Questions for the owner:**
1. Does a viewer exporting the checklist as a file count as "taking" it? If yes, it joins the invariant and D3 gets a real reason. If no, export stays open, and T2 can only be sized as a stolen-session risk to the owner's account. Pros of "export is taking": a stronger guarantee of ownership. Cons: viewers lose offline or print use, which may raise the owner-message rate.
2. Is T2 in scope for this unit, or tracked separately as a session-security matter?

## old B

**D1: keep.**
- Source: the Vision invariant (edit, delete or copy by a viewer is out) and request R1 ("never change or take it").
- Reason: it is the exact invariant. It also matches T1, whose mitigations (copy refused, editor closed) enforce it.

**D2: drop.**
- Source: the Vision's rule that what a viewer needs to follow the checklist is not protected.
- Reason: nothing in the material says an item identifier lets a viewer edit, delete or copy. Hiding identifiers binds a freedom without protecting the invariant. It also risks breaking error messages and exports a viewer needs. It could return only if a real link to edit, delete or copy access is shown.

**D3: change.**
- Source: T2 in the threat model (a stolen session exports checklists in bulk, mitigation undecided), plus the invariant.
- Reason: as written it does two jobs.
  - Interface Contract: replace it with an outcome-level rule. A viewer cannot obtain a copy of the checklist through export. This follows from D1 and the invariant, and it names no mechanism.
  - Threat model: move re-authentication to T2 as one candidate mitigation, not yet decided. It is a mechanism, so it does not belong in the contract.

**D4: drop.**
- Source: the Vision says viewers "see every item and its notes", and the north star is following "item by item".
- Reason: showing only the current item obstructs the benefit. Viewers would likely ask the owner what comes next, which works against the success signal (fewer than 40% messaging the owner). It also protects nothing under the invariant.

**Questions for the owner**
1. Can viewers export at all today? If so, does an export count as "taking" the checklist (a copy outside the product), or is it only an owner-side function? The answer decides whether D3 stays as a viewer outcome rule or becomes owner-only.
2. For T2, whose session is at risk, the owner's or a viewer's? Is a re-sign-in before export acceptable friction for the owner, or should the mitigation be something else (rate limit, no bulk export)?
3. Is an item identifier ever shown in a way that exposes access to someone else's checklist? If not, D2 stays dropped.

## new A (prompt_new_v1)

**D1 - KEEP.**
Source: the Vision invariant, "can a viewer edit the checklist, delete it or copy it into their own workspace? If no, admitted." R1 says the same ("never be able to change or take it"), and T1 covers copy.
Reason: the restriction asks exactly the invariant's three verbs and nothing more. For the threat model, T1's mitigation (copy refused, editor closed to viewers) is consistent with it.

**D2 - CHANGE: keep as an open doubt, do not delete.**
Source: none. No Vision clause, no owner words in R1 and no threat in the model names item identifiers.
Reason: the method says a restriction with no source is "a doubt to ask the owner, or a threat to write down, never a deletion". It is also not a protection the Vision asked for. I would not carry it into the Interface Contract as a binding "never" until it is sourced. If the owner wants it, write it as a threat (for example, identifiers enabling enumeration or guessing of other items) and size the mitigation to that threat.

**D3 - KEEP, with source T2.**
Source: T2, a stolen session exporting checklists in bulk.
Reason: a fresh sign-in is a proportionate answer to what T2 requires, because a thief holding only the session cannot pass it. Complete T2 with this mitigation, which closes its "to be decided". It does not touch following items, so it does not ration the benefit or the success signal. The wording is broader than the threat: it covers every export, not only bulk. I would keep it as written and have the owner confirm that scope.

**D4 - DROP.**
Source: none, and it contradicts the Vision. The Vision says what a viewer needs to follow the checklist "is not protected: they see every item and its notes". The success signal (viewers finish without messaging the owner) also depends on seeing the whole list.
Reason: this is the method's own example of a stricter restriction ("a guest cannot edit the plan" does not become "a guest sees no plan"). It takes away what the Vision promises, so it goes to the owner whatever its source. Tighten back to the test: viewers see every item and its notes.

**Questions for the owner**
1. Is D2 wanted? If so, what threat or request does it answer? Pro: it may limit enumeration. Con: without a source it is scope, and an unsourced rule may ration the benefit.
2. May a viewer export a checklist at all? Export looks like "taking" it under R1, yet the invariant only refuses edit, delete and copy into a workspace. Allowing it with re-sign-in (D3) matches the invariant. Refusing it is stricter than the Vision and would need your decision on the Vision.
3. Should D3's re-sign-in apply to every export, or only bulk ones, which is what T2 requires?

## new B (prompt_new_v1)

**D1 - keep.** Source: the Vision invariant, whose test is "can a viewer edit the checklist, delete it or copy it into their own workspace? If no, admitted". R1 says "never be able to change or take it", and T1 covers the copy case. The draft asks exactly what the test asks, so it goes into the Interface Contract (IC) unchanged. T1's mitigation, "copy refused, editor closed to viewers", stays as the threat model's counterpart.

**D2 - change: hold as an open doubt, do not bind it, do not delete it.** No source supports it. The Vision clause, R1 and the threats T1/T2 are silent on identifiers. The method says a restriction with no source is a doubt to ask the owner, or a threat to write down, never a deletion. As written it goes beyond the sources, because "any page, export or error message" is far broader than anything they ask. I would keep it out of the IC and the threat model until the owner answers. If they name a threat, such as identifier enumeration, I would write it as T3 and size the restriction to it.

**D3 - change: keep, and attach it to T2, scoped to bulk export.** Source: T2, "a stolen session exports checklists in bulk", where the mitigation is still "to be decided". A fresh sign-in is a reasonable answer to T2, because a thief holding only the session cannot pass it. The test is what stopping the threat requires. That is bulk export, not every single export, so I would word it as bulk export. It takes nothing the Vision promises, since following the checklist item by item does not need export.

**D4 - drop.** It contradicts the Vision directly: "What a viewer needs to follow the checklist is not protected: they see every item and its notes." It also works against the north star, which has viewers following "item by item", and against the success signal, viewers finishing without messaging the owner. No source asks for it. It is stricter than the invariant, which only forbids edit, delete and copy. It rations the benefit, so it must not enter the IC or the threat model.

**Questions for the owner**
1. D2: is there a threat behind hiding internal item identifiers? Pro of asking: no invented protection. Con: it costs a round trip. If there is none, D2 is dropped as scope.
2. Is a viewer's export of a single checklist itself a "taking" the Vision forbids, or allowed? The answer decides whether D3 covers only bulk export or all export, and whether D1 needs an explicit export clause.
3. Is the re-sign-in in D3 acceptable to you for T2, or do you prefer another mitigation, such as a rate limit?
