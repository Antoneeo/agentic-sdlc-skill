---
workstream: F-051 the mandatory-read diet (the Hybrid seam moves out of SKILL.md into a triggered support file)
level: L3
branch: main
status: DONE, UNRELEASED
since: 2026-09-11
next: owner's integration call; the NAMED FOLLOW-UP is the same extraction for kb and mkt, which still carry their Hybrid material inline
details: ANALYSIS_mandatory_read_diet.md; harness_mandatory_read_diet/probe.py; ADR_2026-09-11_mandatory_read_diet.md
updated: 2026-09-11
---

## Resume logistics

Implemented, uncommitted on `main`: the Hybrid seam moved verbatim from
`SKILL.md` to `skills/agentic-sdlc-skill/hybrid.md`, a pointer carrying the
trigger and the consequence in its place, `hybrid.md` declared in the lens
profile, the package allowlist, the README bullet and the Runtime Shape tree;
one new battery test; two inbound citations repointed. Live figure at the time
of writing (run `benefit` rather than trusting this line):

```
Read cost of agentic-sdlc-skill: SKILL.md 45279 bytes (every session)
+ 165684 bytes of support files (read on trigger)
```

Standalone read: 50,001 → 45,279 bytes, **−4,722 B (−9.4%)**. Hybrid read:
45,279 + 6,657 = 51,936 bytes, **+1,935 B (+3.9%)** — a Standalone saving paid
for by a small Hybrid surcharge, stated because the Vision's ceremony clause
requires relocated cost to be counted.

## What the two reviews changed

Closure PASS (0 BLOCK), design FAIL (4 BLOCK). The move itself was never in
doubt — both reviewers proved conservation mechanically, one as a multiset of
lines (0 lost, 0 multiplicity deficits), the other byte-exactly. What failed was
everything around it:

1. **Inbound citations.** The weighing enumerated tests and REVIEW_LOG and never
   asked WHO CITES the moved sections. `ENFORCEMENT.md` said "see the SKILL.md
   shadow discipline" and shipped that way; a comment in the shared spine named
   `SKILL.md`'s ownership matrix. Inbound citations are the blast-radius axis
   specific to a relocation, and they are now in the Impact table.
2. **The accounting was one-sided.** The saving is −9.4% for a Standalone
   session, not the 11.9% gross, and the Hybrid session's mandatory read went
   UP — which the first draft never said.
3. **A probe that could not fail, for the third unit running.** P2c claimed to
   pin "the pointer names what is lost" while matching the word `ownership`,
   which the pointer's own content inventory contains. The design reviewer
   deleted the entire consequence paragraph and the probe stayed green. It is
   now anchored after the filename, on the consequence sentence itself.
4. **A number that did not reproduce.** "51 REVIEW_LOG hits for hybrid" was a
   repo-wide file count; the log has 15 lines / 20 occurrences. The conclusion
   held — all of them concern the `--hybrid` flag — but the evidence row did not.

Also folded: the pointer now prices the skip with the rule that matters most —
**never auto-accept a devPNT proposal** now lives in exactly one place in the
package — and `hybrid.md` was rebuilt so the moved region is one contiguous,
character-identical block rather than two rejoined halves, which is what makes
the byte-level conservation probe meaningful.

## Named follow-up, not an intention

kb and mkt still carry their Hybrid material inline. Same extraction, same probe
shape, separate unit — deliberately not done blind here, and recorded here so it
has a referent.
