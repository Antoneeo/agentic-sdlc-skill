# The doctrine deltas F-081 makes, verbatim as (old, new) replacements inside the
# named file; bytes are the UTF-8 change (new minus old).
D = [
("D1", "code SKILL.md Write Triggers row", True,
 "`not-yet-honored-by -> ANALYSIS_<name>` (Standalone) | An L3 defers fixing code that contradicts a claim in `topics/`: mark the claim and cite its id in the ANALYSIS (`check` verifies both).",
 "`not-yet-honored-by -> ANALYSIS_<name>` (Hybrid: `SHADOW_<doc_key>`) | An L3 defers fixing code that contradicts a claim in `topics/`: mark the claim and cite its id in the ANALYSIS, in Hybrid in the E-ISP/E-TDD and its exported shadow (`check` verifies both)."),
("D2", "kb distillation.md §2 reserved-predicate sentence", False,
 "which must cite the claim id (`check` verifies both).",
 "which must cite the claim id (`check` verifies both). In Hybrid the target is `SHADOW_<doc_key>`: the newest `solutions/SHADOW_<doc_key>_vX.Y.md` must exist and cite it."),
("D3", "kb templates.md claim-table about line", False,
 "`not-yet-honored-by -> ANALYSIS_<name>` marks",
 "`not-yet-honored-by -> ANALYSIS_<name>` (Hybrid: `SHADOW_<doc_key>`) marks"),
("D4", "kb SKILL.md Topic Recall, The act.", True,
 "A claim marked `not-yet-honored-by -> ANALYSIS_<name>` is cited as what the specification requires and the code does not yet do, naming that analysis — never as current behavior.",
 "A claim marked `not-yet-honored-by` is cited as what the specification requires and the code does not yet do, naming its target — never as current behavior."),
("D5", "shared memory.md claims sentence (x4 identical, read at orientation)", True,
 "as not yet true of the code, naming its analysis;",
 "as not yet true of the code, naming its target;"),
("D6", "kb reconciliation.md §3", False,
 "the analysis citing the predecessor's id satisfies the successor.",
 "the analysis or shadow citing the predecessor's id satisfies the successor."),
]


def size(s):
    return len(s.encode("utf-8"))


if __name__ == "__main__":
    net = always = 0
    for k, where, every, old, new in D:
        d = size(new) - size(old)
        net += d
        always += d if every else 0
        print("%s %+5d %s %s" % (k, d, "every load" if every else "on trigger", where))
    print("net %+d | read in every session: %+d" % (net, always))
