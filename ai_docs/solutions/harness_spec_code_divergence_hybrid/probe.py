#!/usr/bin/env python3
"""F-081 probe: the not-yet-honored marker in a Hybrid project.

Builds a throw-away project (one topic, one source, zero or more devPNT shadows
under `solutions/`) and runs the shared claim checks (`knowledge.kb_check_claims`,
identical in all four packages) and export.

  --baseline  asserts the as-is facts the design rests on (GREEN before F-081;
              A1 and A3 turn RED once F-081 ships -- that flip is the evidence):
    A1  `not-yet-honored-by -> SHADOW_<doc_key>` is refused, even with a citing shadow
    A2  an ordinary relation pointing at a SHADOW_ name is refused
    A3  the code lens's Write Triggers row scopes the marker to "(Standalone)"
  default     asserts F-081's behavior (RED before, GREEN after):
    B1  marker -> SHADOW_<key>, highest-version shadow cites the claim: no finding
    B2  marker -> SHADOW_<key> with no shadow on disk: an error naming the pattern
    B3  the highest version (v1.10 over v1.9, numeric) does not cite: an error
        naming that file, even though an older version cites
    B4  only a longer key's shadow exists (SHADOW_<key>_extra_v1.0.md): an error
    B5  a versioned target (SHADOW_<key>_v1.2) is refused by grammar
    B6  export drops a SHADOW_ marker, every other line unchanged
    B7  the doctrine names SHADOW_<doc_key> where the grammar binds (code Write
        Triggers row, kb distillation + templates) and the row no longer says
        "(Standalone)"
Exit 0 = all green; 1 = some assertion red (printed).

    python ai_docs/solutions/harness_spec_code_divergence_hybrid/probe.py [--baseline] [--root .]
"""
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
KEY = "eisp_export_schedule"
MARK = "not-yet-honored-by -> SHADOW_" + KEY
CITES = ("<!-- SHADOW generated from devPNT (%s v1.0) - do not edit by hand -->\n"
         "# E-ISP\n\nDeferred: claim %s (nightly export) is not yet honored.\n" % (KEY, CID))
SILENT = "<!-- SHADOW generated from devPNT -->\n# E-ISP\n\nnothing here\n"


def project(tmp, about, shadows=None):
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
    if shadows:
        (docs / "solutions").mkdir()
        for name, text in shadows.items():
            (docs / "solutions" / name).write_text(text, encoding="utf-8")
    return docs


def findings(about, shadows=None):
    with tempfile.TemporaryDirectory() as tmp:
        errors, warnings, _ = knowledge.kb_check_claims(project(tmp, about, shadows))
        return errors + warnings


def shadow(version, text):
    return {"SHADOW_%s_v%s.md" % (KEY, version): text}


def row():
    lines = [ln for ln in (CODE / "SKILL.md").read_text(encoding="utf-8").splitlines()
             if ln.startswith("| `topics/` claim marked `not-yet-honored-by")]
    return lines[0] if lines else ""


def baseline():
    return [
        ("A1 SHADOW_ target refused", any("about" in f or "ANALYSIS_" in f
                                          for f in findings(MARK, shadow("1.0", CITES)))),
        ("A2 relation -> SHADOW_ refused", any("about" in f for f in findings(
            "depends-on -> SHADOW_" + KEY, shadow("1.0", CITES)))),
        ("A3 row scoped (Standalone)", "(Standalone)" in row()),
    ]


def export_drops():
    with tempfile.TemporaryDirectory() as tmp:
        docs = project(tmp, "depends-on -> export; " + MARK, shadow("1.0", CITES))
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
    newest_silent = dict(shadow("1.9", CITES), **shadow("1.10", SILENT))
    newest_cites = dict(shadow("1.9", SILENT), **shadow("1.10", CITES))
    doctrine = [CODE / "SKILL.md", KB / "distillation.md", KB / "templates.md"]
    return [
        ("B1 cited shadow clean", findings(MARK, shadow("1.0", CITES)) == []
         and findings(MARK, newest_cites) == []),
        ("B2 missing shadow refused", any("SHADOW_%s_v" % KEY in f for f in findings(MARK))),
        ("B3 highest version must cite", any("SHADOW_%s_v1.10.md" % KEY in f and CID in f
                                             for f in findings(MARK, newest_silent))),
        ("B4 longer key is not this key", any("SHADOW_%s_v" % KEY in f for f in findings(
            MARK, {"SHADOW_%s_extra_v1.0.md" % KEY: CITES}))),
        ("B5 versioned target refused", any("about" in f for f in findings(
            MARK + "_v1.2", shadow("1.2", CITES)))),
        ("B6 export drops the marker", export_drops()),
        ("B7 doctrine names SHADOW_<doc_key>",
         all("SHADOW_<doc_key>" in p.read_text(encoding="utf-8") for p in doctrine)
         and "(Standalone)" not in row()),
    ]


checks = baseline() if "--baseline" in sys.argv else target()
red = 0
for label, ok in checks:
    red += not ok
    print("%-40s %s" % (label, "GREEN" if ok else "RED"))
sys.exit(1 if red else 0)
