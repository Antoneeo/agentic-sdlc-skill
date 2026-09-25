#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executed claims behind ANALYSIS_question_discipline.md (F-026, 2026-09-25 revision).

    python ai_docs/solutions/harness_question_discipline/probe.py [GIT_REF]

With no argument the probe reads the working tree; with a ref it reads that
commit's text (`git show REF:path`). Run it against the pre-revision release
commit to see it red:

    python ai_docs/solutions/harness_question_discipline/probe.py c2a3828

The deliverable is doctrine text, so the probes are text assertions over the three
lenses. They prove the WIRING of the rule, never an agent's behaviour: that
lives in the non-gating scenario `evals/scenarios/doubt_asked_when_it_emerges.md`.

P1  the silence licence is gone: no "Default non-blocking", no "answered by
    exception", and the code Rule Zero no longer says blocking is the exception.
P2  every lens has §When a doubt emerges, and a REAL doubt that passes the
    legality test is owed.
P3  the ask comes before the first write that would embed the answer; declared
    assumptions are restricted to unattended and delegated cases; a reserved
    approval is never assumed.
P4  the shared `review.md` makes an unasked doubt a finding, no longer cites
    "§Blocking is reserved", and its citations (§The form of a question, the
    Unattended path) resolve in every lens.
P5  every lens's always-read line carries the ask-when-it-emerges duty.
P6  kb: the claim-conflict hand-over keeps its own timing, and the Capture Moment
    sweep is a planned occasion; marketing: a researched ASSUMPTION is not a doubt,
    and unattended E3 work holds at DRAFT.
P7  choices are settled by weighing pros and cons, naming the option rejected; the
    form and the planned occasions give each option its pros and cons.
P8  reserved approvals and mandated stops are legal by mandate, stated in the
    section `review.md` cites.
P9  code: the skip path and "derive before asking" no longer let the repo settle
    intent.
P10 facts and owner-held data are never settled by a weighing.
P11 the shared `dispatch.md` tells a spawned subagent to return its real doubts.
P12 a weighing states each rejected option at its strongest, and options serving
    different, unranked needs of the actor are a real doubt.
"""
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
LENSES = {
    "code": "skills/agentic-sdlc-skill",
    "kb": "distributions/kb-agentic-skill/skills/kb-agentic-skill",
    "mkt": "distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc",
}


def read(rel, ref):
    if ref is None:
        text = (REPO / rel).read_text(encoding="utf-8")
    else:
        out = subprocess.run(["git", "show", f"{ref}:{rel}"], cwd=REPO,
                             capture_output=True, text=True, encoding="utf-8")
        if out.returncode != 0:
            raise SystemExit(f"cannot read {rel} at {ref}: {out.stderr.strip()}")
        text = out.stdout
    return text.replace("\r\n", "\n")


def flat(text):
    return " ".join(text.split())


def discipline(text):
    """The `## The question discipline` section only."""
    # The heading, not the file's opening line that names it in backticks.
    start = text.index("\n## The question discipline\n") + 1
    nxt = text.find("\n## ", start + 5)
    return text[start:] if nxt < 0 else text[start:nxt]


def subsection(text, heading):
    """One `### heading` block inside the discipline; empty when absent."""
    marker = f"\n### {heading}\n"
    if marker not in text:
        return ""
    start = text.index(marker) + 1
    ends = [k for k in (text.find("\n### ", start + 4), text.find("\n## ", start + 4))
            if k >= 0]
    return text[start:min(ends)] if ends else text[start:]


def rule_zero_line(skill):
    head = skill.split("## Write Triggers")[0]
    lines = [ln for ln in head.splitlines()
             if "question discipline" in ln or "legality test" in ln]
    return " ".join(lines)


def main(ref):
    results = []

    def check(pid, lens, ok, why):
        results.append((pid, lens, ok, why))

    for lens, root in LENSES.items():
        el = read(f"{root}/elicitation.md", ref)
        skill = read(f"{root}/SKILL.md", ref)
        # Phrases wrap across lines in the source: compare whitespace-collapsed.
        qd = flat(discipline(el))
        rz = flat(rule_zero_line(skill))
        skill = flat(skill)

        check("P1", lens, "answered by exception" not in qd
              and "Default non-blocking" not in qd,
              "discipline still defers doubts to the deliverable")
        if lens == "code":
            check("P1", lens, "exception, not the default" not in skill,
                  "Rule Zero still says blocking is the exception")

        check("P2", lens, "\n### When a doubt emerges\n" in el,
              "no section naming the signals of an emerged doubt")
        check("P2", lens, "real doubt that passes the legality test below is **owed**" in qd,
              "a REAL doubt that passes the legality test is not declared owed")

        check("P7", lens, "weigh the pros and cons of each option" in qd,
              "no real-indecision test (weighing each option's pros and cons)")
        check("P7", lens, "I take X over Z" in qd,
              "the weighing line does not name the option it rejects")
        # Increment 2026-09-25: an honest weighing (field run of the scenario).
        check("P12", lens, "at its strongest" in qd and "serve different needs" in qd,
              "the weighing does not state the rejected option at its strongest, or "
              "does not make unranked different needs a real doubt")
        form = flat(subsection(el, "The form of a question"))
        check("P7", lens, "each with its pros and cons" in form,
              "the form's fork does not give each option its pros and cons")
        # The planned occasions offer options too: they carry pros and cons.
        occasion = flat(el[el.find("\n## The round\n"):]) if lens != "mkt" \
            else flat(el[el.find("Question style"):el.find("\n## Wave 1")])
        check("P7", lens, "pros and cons" in occasion,
              "the planned occasion's options carry no pros and cons")
        check("P10", lens, "never settled by a weighing" in qd,
              "facts and owner-held data can be settled by a weighing")

        # Reserved approvals and mandated stops: asked by mandate, stated in the
        # section review.md cites, and never assumed when unattended.
        check("P8", lens, "legal by mandate" in form,
              "'legal by mandate' is not stated in §The form of a question")
        check("P3", lens, "never assumed" in qd,
              "a reserved approval can become a declared assumption")
        if lens == "code":
            flat_el = flat(el)
            skip = flat(el[el.find("Skip path:"):el.find("Unattended path:")])
            check("P9", lens, bool(skip) and "derivable from the repo" not in skip,
                  "code skip path still derives intent from the repo")
            check("P9", lens, "never the goal, scope or acceptance" in flat_el,
                  "'derive before asking' still lets the code answer intent")

        check("P3", lens, "before the first write that would embed" in qd,
              "no rule anchoring the ask before the write that embeds the answer")
        anchor = "Declared assumptions exist only where no question can be asked"
        tail = qd[qd.find(anchor):qd.find(anchor) + 900] if anchor in qd else ""
        check("P3", lens, bool(tail) and "Unattended" in tail and "Delegated" in tail,
              "declared assumptions not restricted to unattended/delegated")

        check("P5", lens, "when it emerges" in rz,
              "always-read line lacks the ask-when-it-emerges duty")

        rv = flat(read(f"{root}/review.md", ref))
        check("P4", lens, "An unasked doubt is a finding" in rv,
              "review.md does not make an unasked doubt a finding")
        check("P4", lens, "§Blocking is reserved" not in rv,
              "review.md cites the removed '§Blocking is reserved' heading")
        # review.md is byte-identical across lenses: what it cites must exist,
        # spelled identically, in every lens's elicitation.md.
        check("P4", lens, "`elicitation.md` §The form of a question" in rv
              and "\n### The form of a question\n" in el,
              "review.md's citation of §The form of a question does not resolve")
        check("P4", lens, "Unattended path" in flat(el),
              "review.md cites the 'Unattended path', which this lens lacks")

        dp = flat(read(f"{root}/dispatch.md", ref))
        check("P11", lens, "return it in your final output" in dp,
              "dispatch.md does not tell the subagent to return its real doubts")

        i, j = qd.find("prescribe"), qd.find("That list is closed")
        closed = qd[i:j] if 0 <= i < j else ""
        if lens == "code":
            check("P6", lens, "circuit breaker" in closed and "round cap" in closed,
                  "code lost its two closed exemptions (circuit breaker, round cap)")
        if lens == "mkt":
            check("P6", lens, "round cap" in closed,
                  "mkt lost its closed exemption (round cap)")
        if lens == "kb":
            check("P6", lens, "reconciliation.md` §4" in closed and "own timing" in qd,
                  "kb lost the claim-conflict hand-over or its mandated timing")
            check("P6", lens, "Capture Moment sweep" in qd and "each a planned occasion" in qd,
                  "kb's Capture Moment sweep is not a planned occasion")
        if lens == "mkt":
            check("P6", lens, "researched answer" in qd,
                  "mkt lacks the researched-ASSUMPTION rule")
            unatt = flat(el[el.find("Unattended path:"):el.find("\n## The question discipline\n")])
            check("P6", lens, "DRAFT" in unatt and "user gate" in unatt,
                  "mkt's unattended E3 work does not hold at DRAFT / the user gate")

    failed = [r for r in results if not r[2]]
    for pid, lens, ok, why in results:
        print(f"{'GREEN' if ok else 'RED  '} {pid} [{lens}] {'' if ok else why}")
    print(f"\n{len(results) - len(failed)}/{len(results)} green"
          f" ({'working tree' if ref is None else ref})")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
