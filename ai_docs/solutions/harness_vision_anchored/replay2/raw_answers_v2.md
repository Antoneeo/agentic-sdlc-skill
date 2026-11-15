# F-099 replay 2, second run (prompt_new.md) - the two answers, whole

## new v2 A

**D1: keep.**
- Source: the Vision invariant, "can a viewer edit the checklist, delete it or copy it into their own workspace? If no, admitted." It also rests on R1: "they must never be able to change or take it."
- Reason: the wording matches the invariant's test exactly and asks nothing more.
- For the threat model, T1's mitigation (copy refused, editor closed to viewers) stays and cites this same clause.

**D2: change, from a restriction to an open question for the owner.**
- Source: none. No Vision clause, no owner words in R1, and no threat in the model names item identifiers.
- Reason: hiding identifiers takes nothing the Vision promises, because following the checklist doesn't depend on seeing them. The method says never to delete an unsourced restriction like this. It is either a doubt to ask the owner or a threat to write down.
- I'm not writing it into the Interface Contract as a binding rule until the owner answers.

**D3: change. Keep it as T2's mitigation, narrowed to bulk export.**
- Source: T2, "a stolen session exports checklists in bulk." The mitigation is currently "to be decided."
- Reason: stopping that threat only requires re-authentication when a session exports many checklists at once. Re-authenticating on every export is stricter than the threat's test.
- Whether a viewer may export a single checklist at all is a separate question, because it overlaps "take it." That goes to the owner.

**D4: drop.**
- Source: none. It also contradicts the Vision: "they see every item and its notes."
- Reason: viewing only the current item takes away what the Vision promises, and it works against the success signal. That signal is viewers finishing without messaging the owner, from a baseline of 40% who message at least once. The method says a restriction like this is out as written, whatever its source.
- It enters the design only if the owner chooses it. I'm telling the owner here that I dropped it.

**Questions for the owner**
1. Should item identifiers stay hidden from viewers in pages, exports and errors? A Vision clause or a threat would be needed to make it binding.
   - Pro: less internal detail is exposed.
   - Con: it is unsourced scope and could make errors harder to report.
2. May a viewer export a single checklist? If yes, re-sign-in applies only to bulk export. If no, export is a form of "taking" and falls under D1.
3. Do you want "a viewer sees only the current item" as a deliberate change to the Vision's promise? I dropped it and will not carry it unless you choose it.

## new v2 B

**D1: keep.**
Source: the Vision invariant ("can a viewer edit the checklist, delete it or copy it into their own workspace? If no, admitted"), R1 ("never be able to change or take it"), and threat T1 (copy).
Reason: the draft asks exactly the invariant's three actions and nothing more. It goes to the Interface Contract as written, and to the threat model as the mitigation for T1 (copy refused, editor closed to viewers).

**D2: keep, as an unsourced restriction, and bring it to the owner.**
Source: none. No Vision clause, R1 wording or threat in T1/T2 names it.
Reason: hiding identifiers takes nothing the Vision promises, because viewers still see every item and its notes. The method says a restriction with no source and no cost to the Vision is a doubt to ask the owner or a threat to write down, never a deletion. Until the owner answers, it stays marked "no source" in the Interface Contract. It should not be presented as a protection the Vision asked for.

**D3: change.**
Source: threat T2 (a stolen session exports in bulk), whose mitigation is still "to be decided".
Reason: re-sign-in does stop a stolen session, so it can be T2's mitigation. As drafted it covers every export, which is stricter than what stopping bulk export requires. Narrow it: re-authentication is asked only for bulk export. A viewer exporting a single checklist is not asked. Record it in the threat model as T2's mitigation, and note that the scope is the threat's test and nothing wider.

**D4: drop.**
Source: none.
Reason: the Vision says a viewer sees every item and its notes. The success signal is that viewers finish without messaging the owner (baseline: 40% message the owner), and "current item only" removes the view they need. A restriction that takes away what the Vision promises is out as written, even with a threat behind it. It enters the design only if the owner chooses it. I am telling the owner now, in this message.

**Questions for the owner**
1. D2: do you want internal identifiers hidden from viewers? If yes, what is the reason or threat?
2. D3/T2: whose session is the stolen one (owner or viewer), and may viewers export at all?
3. D4: do you want a current-item-only view? It conflicts with the Vision clause that viewers see every item.
