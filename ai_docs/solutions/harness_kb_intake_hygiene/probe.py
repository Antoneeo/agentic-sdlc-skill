#!/usr/bin/env python3
"""F-077 probe: kb intake hygiene, replayed on a throw-away project.

Builds a minimal project with kb-agentic's validator and asserts:
  B1  a document guide whose distilled_from is a corpus/given/ artifact passes
      `check` and `stale` while the bytes are unchanged (today: expected GREEN);
  B2  the same guide is reported [stale] once the artifact's bytes change
      (today: expected GREEN — cmd_stale reads any confined path);
  P1  a given/ artifact holding a credential-shaped line is flagged by `check`
      (today: expected RED);
  P2  the same artifact, redacted at intake and declared so, passes `check`
      (today: GREEN trivially, since nothing is flagged);
  P3  the same text living in reference/.sources/ AND corpus/given/ is reported
      (today: expected RED);
  P4  `adopt` (dry run) lists the document guides and their snapshots and
      writes nothing (today: expected RED — no such command);
  P5  a sidecar naming its original by a non-local identifier (original_ref:)
      raises no dangling-pointer warning (today: GREEN — the field is unknown);
  P6  a document guide's snapshot with a credential, on a tree with NO corpus, is
      flagged exactly once by `check` in the code, kb and marketing entry points.
Exit 0 = all green; exit 1 = some assertion red (printed).

    python ai_docs/solutions/harness_kb_intake_hygiene/probe.py [--root .]
"""
import hashlib, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(sys.argv[sys.argv.index("--root") + 1]) if "--root" in sys.argv else Path.cwd()
ENTRY = ROOT / "distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py"
DOC = "db.url=jdbc:postgresql://db.example.test/app\ndb.user=app\ndb.password=hunter2-fake\n"
RED_DOC = "db.url=jdbc:postgresql://db.example.test/app\ndb.user=app\ndb.password=[REDACTED:password]\n"


def run(*args):
    p = subprocess.run([sys.executable, str(ENTRY), *args], capture_output=True,
                       text=True, encoding="utf-8")
    return p.returncode, p.stdout + p.stderr


def sha(b):
    return hashlib.sha256(b).hexdigest()


def project(tmp, given_text, redacted=False, snapshot=False, ref=False):
    d = tmp / "ai_docs"
    for sub in ("vision", "strategic", "reference", "corpus/given", "audit"):
        (d / sub).mkdir(parents=True, exist_ok=True)
    (d / "README.md").write_text("# ai_docs\n", encoding="utf-8")
    raw = given_text.encode("utf-8")
    name = "app-%s.properties" % sha(raw)[:8]
    (d / "corpus/given" / name).write_bytes(raw)
    meta = ["---", "sha256: %s" % sha(raw), "date: 2026-10-23",
            "provenance: handed over by the team"]
    if redacted:
        meta.append("redacted_at_intake: [password]")
    if ref:
        meta.append("original_ref: wiki://team-space/app-config")
    (d / "corpus/given" / (name + ".meta.md")).write_text(
        "\n".join(meta + ["---", ""]), encoding="utf-8")
    df = "ai_docs/corpus/given/" + name
    if snapshot:
        (d / "reference/.sources").mkdir(parents=True, exist_ok=True)
        (d / "reference/.sources" / name).write_bytes(raw)
        df = "ai_docs/reference/.sources/" + name
    (d / "reference/GUIDE_app_config.md").write_text(
        "---\ndescription: Consult before changing the app configuration.\n"
        "status: CURRENT\nsource_kind: document\nsource: team config handed over\n"
        "distilled_from: %s\nsource_hash: %s\n---\n# Guide\n\n## Rule\n"
        "[source: %s#L1-3]\nThe app reads its database from db.url.\n"
        % (df, sha(raw), name), encoding="utf-8")
    run("index", "--root", str(tmp))
    return d, name


def files(tmp):
    return sorted(str(p.relative_to(tmp)) for p in tmp.rglob("*") if p.is_file())


red = 0
def report(label, ok, detail=""):
    global red
    red += not ok
    print("%-62s %s %s" % (label, "GREEN" if ok else "RED", detail))


with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    d, name = project(tmp, RED_DOC, redacted=True)
    rc, out = run("check", "--root", str(tmp))
    report("B1 guide on corpus/given: check passes", rc == 0, "" if rc == 0 else out[-600:])
    rc, out = run("stale", "--root", str(tmp))
    report("B1 guide on corpus/given: stale quiet", "[stale]" not in out and "not found" not in out)
    p = d / "corpus/given" / name
    p.write_bytes(p.read_bytes() + b"x")
    rc, out = run("stale", "--root", str(tmp))
    report("B2 changed artifact: guide reported [stale]", "[stale]" in out)

with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    project(tmp, DOC)
    rc, out = run("check", "--root", str(tmp))
    report("P1 credential in given/: flagged by check", rc != 0 and "credential" in out.lower())

with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    project(tmp, RED_DOC, redacted=True)
    rc, out = run("check", "--root", str(tmp))
    report("P2 redacted + declared: check passes", rc == 0 and "credential" not in out.lower(),
           "" if rc == 0 else out[-600:])

with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    d, name = project(tmp, RED_DOC, redacted=True, snapshot=True)
    rc, out = run("check", "--root", str(tmp))
    report("P3 same text in .sources/ and given/: reported", "same text" in out.lower()
           or "same sha256" in out.lower())

with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    project(tmp, RED_DOC, redacted=True, snapshot=True)
    before = files(tmp)
    rc, out = run("adopt", "--root", str(tmp))
    report("P4 adopt dry run: lists guide + snapshot", rc == 0 and "GUIDE_app_config.md" in out
           and ".sources/" in out, "" if rc == 0 else out[-300:])
    report("P4 adopt dry run: writes nothing", files(tmp) == before)

with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    project(tmp, RED_DOC, redacted=True, ref=True)
    rc, out = run("check", "--root", str(tmp))
    report("P5 original_ref: no dangling-pointer warning", "does not resolve" not in out)

ENTRIES = {
    "code": [ROOT / "skills/agentic-sdlc-skill/scripts/sdlc_check.py", "check"],
    "kb": [ENTRY, "check"],
    "mkt": [ROOT / "distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py",
            "check", "--docs-dir", "ai_docs"],
}
with tempfile.TemporaryDirectory() as t:
    tmp = Path(t)
    d, _ = project(tmp, DOC, snapshot=True)
    shutil.rmtree(d / "corpus")
    run("index", "--root", str(tmp))
    for lens, (entry, *args) in ENTRIES.items():
        p = subprocess.run([sys.executable, str(entry), *args, "--root", str(tmp)],
                           capture_output=True, text=True, encoding="utf-8")
        out = p.stdout + p.stderr
        n = out.count("look like a credential")
        report("P6 %s check, no corpus: snapshot flagged once" % lens,
               n == 1 and "hunter2" not in out, "(%d)" % n)

sys.exit(1 if red else 0)
