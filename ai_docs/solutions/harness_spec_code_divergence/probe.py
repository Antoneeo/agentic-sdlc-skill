#!/usr/bin/env python3
"""F-080 probe: a specification claim the code does not yet honor.

Builds a throw-away project (one topic, one source, one ANALYSIS) and runs the
shared claim checks (`knowledge.kb_check_claims`, identical in all four packages)
plus the code lens's `check`.

  --baseline  asserts the as-is facts the design rests on (GREEN before F-080,
              A1/A4 turn RED once F-080 ships; A2 stays GREEN because the
              reserved predicate with a slug target is still refused -- that flip is the evidence):
    A1  `about: not-yet-honored-by -> <slug>` passes with nothing behind the target
    A2  two relations in one `about` cell are refused
    A3  the code lens's `check` reaches the claim checks (a bad `about` is reported)
    A4  no doctrine file names `not-yet-honored-by`
  default     asserts F-080's behavior (RED before, GREEN after):
    B1  marker -> existing ANALYSIS that cites the claim id: no finding
    B2  marker -> missing ANALYSIS: an error naming the target
    B3  marker -> ANALYSIS that does not cite the claim id: an error
    B4  a relation and the marker together in one cell: accepted
    B5  the doctrine names the marker where it binds (kb Topic Recall, kb
        distillation + templates + reconciliation + portability, shared memory.md,
        code Write Triggers; code templates.md points at that row and is not listed)
    B6  export writes the topic without the marker, every other line unchanged
Exit 0 = all green; 1 = some assertion red (printed).

    python ai_docs/solutions/harness_spec_code_divergence/probe.py [--baseline] [--root .]
"""
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path.cwd()
CODE = ROOT / "skills/agentic-sdlc-skill"
KB = ROOT / "distributions/kb-agentic-skill/skills/kb-agentic-skill"
sys.path.insert(0, str(CODE / "scripts"))
import knowledge  # noqa: E402  shared, byte-identical in every package

SRC = "corpus/given/spec.txt#p=1@0-24"
CID = knowledge.kb_claim_id("corpus/given/spec.txt", "p=1@0-24", "")


def project(tmp, about, analysis=None):
    docs = Path(tmp) / "ai_docs"
    (docs / "topics").mkdir(parents=True)
    (docs / "corpus" / "given").mkdir(parents=True)
    (docs / "corpus" / "given" / "spec.txt").write_text(
        "The export runs nightly.\n", encoding="utf-8")
    (docs / "topics" / "export.md").write_text(
        "---\ntopic: export\ndescription: d\nparents: []\nstatus: CURRENT\n---\n\n"
        "## Claims\n\n| id | claim | valid | qty | about | source | prov | state |\n"
        "|---|---|---|---|---|---|---|---|\n"
        "| %s | The export runs nightly | - | - | %s | %s | GIVEN | OK |\n"
        % (CID, about, SRC), encoding="utf-8")
    if analysis is not None:
        (docs / "solutions").mkdir()
        (docs / "solutions" / "ANALYSIS_export_schedule.md").write_text(
            analysis, encoding="utf-8")
    return docs


def findings(about, analysis=None):
    with tempfile.TemporaryDirectory() as tmp:
        errors, warnings, _ = knowledge.kb_check_claims(project(tmp, about, analysis))
        return errors + warnings


MARK = "not-yet-honored-by -> ANALYSIS_export_schedule"
CITES = "# A\n\n**2026-10-23 — deferred.** Not yet honored: %s (nightly export).\n" % CID
DOCTRINE = [KB / "SKILL.md", KB / "distillation.md", KB / "templates.md",
            KB / "reconciliation.md", KB / "portability.md",
            CODE / "memory.md", CODE / "SKILL.md"]


def baseline():
    with tempfile.TemporaryDirectory() as tmp:
        docs = project(tmp, "about junk")
        out = subprocess.run([sys.executable, str(CODE / "scripts/sdlc_check.py"),
                              "check", "--root", str(docs.parent)],
                             capture_output=True, text=True, encoding="utf-8")
    return [
        ("A1 marker passes, target unresolved", findings("not-yet-honored-by -> f-080") == []),
        ("A2 two relations refused", any("about" in f for f in findings(
            "depends-on -> phase-1; not-yet-honored-by -> f-080"))),
        ("A3 code check reaches claims", "about must be" in out.stdout + out.stderr),
        ("A4 doctrine silent", not any("not-yet-honored-by" in p.read_text(encoding="utf-8")
                                       for p in DOCTRINE)),
    ]


def export_drops():
    with tempfile.TemporaryDirectory() as tmp:
        docs = project(tmp, "depends-on -> export; " + MARK, CITES)
        selected, artifacts, _added, errors = knowledge.kb_export_closure(docs, ["export"])
        out = Path(tmp) / "bundle"
        knowledge.kb_bundle_write(docs, out, selected, artifacts, "p")
        before = (docs / "topics" / "export.md").read_text(encoding="utf-8").splitlines()
        after = (out / "topics" / "export.md").read_text(encoding="utf-8").splitlines()
        changed = [(a, b) for a, b in zip(before, after) if a != b]
        return (not errors and len(before) == len(after) and len(changed) == 1
                and "not-yet-honored-by" not in changed[0][1]
                and "depends-on -> export" in changed[0][1])


def target():
    return [
        ("B1 cited marker clean", findings(MARK, CITES) == []),
        ("B2 missing target refused", any("ANALYSIS_export_schedule" in f
                                          for f in findings(MARK))),
        ("B3 uncited target refused", any(CID in f for f in findings(MARK, "# A\n"))),
        ("B4 relation + marker accepted",
         findings("depends-on -> export; " + MARK, CITES) == []),
        ("B6 export drops the marker", export_drops()),
        ("B5 doctrine names the marker", all("not-yet-honored-by" in p.read_text(encoding="utf-8")
                                             for p in DOCTRINE)),
    ]


checks = baseline() if "--baseline" in sys.argv else target()
red = 0
for label, ok in checks:
    red += not ok
    print("%-40s %s" % (label, "GREEN" if ok else "RED"))
sys.exit(1 if red else 0)
