# The doctrine deltas F-080 adds, verbatim; bytes are UTF-8 of the added text.
D = [
("D1", "kb distillation.md §2 about bullet (appended)", False,
 " Several relations share one cell, separated by `; `. One predicate is reserved: `not-yet-honored-by -> ANALYSIS_<name>` says the code does not yet honor this specification claim and names the analysis that records the deferred fix, which must cite the claim id (`check` verifies both). It states the code's relation to the claim, not what the source asserts: the code-lens unit that defers or makes the fix writes or removes it, never a knowledge unit. It has no reverse direction, and nothing lists or selects claims by it. Export drops it: it describes this project's code."),
("D2", "kb templates.md claim-table about line (appended)", False,
 " Several share one cell, separated by `; `; `not-yet-honored-by -> ANALYSIS_<name>` marks a claim the code does not yet honor (`distillation.md` §2)."),
("D3", "kb SKILL.md Topic Recall, The act. (appended)", True,
 " A claim marked `not-yet-honored-by -> ANALYSIS_<name>` is cited as what the specification requires and the code does not yet do, naming that analysis — never as current behavior."),
("D4", "shared memory.md claims sentence (inserted)", False,
 " cite a claim marked `not-yet-honored-by` as not yet true of the code, naming its analysis;"),
("D5", "code SKILL.md Write Triggers row (new)", True,
 "| `topics/` claim marked `not-yet-honored-by -> ANALYSIS_<name>` (Standalone) | An L3 defers fixing code that contradicts a claim in `topics/`: mark the claim and cite its id in the ANALYSIS (`check` verifies both). The L2/L3 change that makes the code honor it removes the marker in the same commit; L1 is exempt. Nothing lists marked claims. | 3 / 5 |\n"),
("D6", "code templates.md Diary comment (appended)", False,
 "\n     A deferred fix of code contradicting a `topics/` claim cites the claim id here (SKILL.md Write Triggers)."),
("D7", "kb reconciliation.md §3 (new paragraph)", False,
 "\nA superseded row keeps its `not-yet-honored-by` marker with its text. Copy the marker to each successor that still states behavior the code does not have; the analysis citing the predecessor's id satisfies the successor.\n"),
("D8", "kb portability.md §2 (new bullet)", False,
 "- **Not the `not-yet-honored-by` markers.** They describe this project's code, so the export drops them and says so, without a number.\n"),
]
always = sum(len(t.encode()) for _, _, a, t in D if a)
total = sum(len(t.encode()) for _, _, _, t in D)
for k, w, a, t in D:
    print("%s %4d %s %s" % (k, len(t.encode()), "every load" if a else "on trigger", w))
print("total", total, "| read in every session:", always)
