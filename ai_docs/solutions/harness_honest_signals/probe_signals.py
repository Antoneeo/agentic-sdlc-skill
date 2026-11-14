"""F-096 probes, report points 2 and 4.

P2  A CURRENT guide holding the three recorded sentences about a state that no
    longer holds (case_guide_false.md) passes `check` CLEAN -- and the verdict
    says what CLEAN does not cover.
P4  `orient` carries, at every session start, the constant line saying what to
    re-read before answering about an open unit when working from a summary
    (REQUEST_honest_signals.md R7: constant, no read of the hook event).

Exit 0 = both hold; exit 1 = at least one does not.

Usage: python probe_signals.py <path to sdlc_check.py>
"""
import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path

# The three state sentences, verbatim from case_guide_false.md (commit 6aadb806).
FALSE_SENTENCES = (
    "pubblicato dal proxy, in forma provvisoria** (2026-11-14)",
    "codice del 2026-11-14, non ancora in produzione",
    "Rimozione del file del proxy: non ancora fatta (da annotare qui con la data).",
)
LOG_ROW = "| 2026-11-14 | File rimosso dopo il deploy: lo serve ora l'applicazione | owner |"


def run(checker, *args):
    res = subprocess.run([sys.executable, str(checker), *args],
                         capture_output=True, text=True, encoding="utf-8")
    return res.returncode, res.stdout + res.stderr


def build_tree(tmp):
    ai = Path(tmp) / "ai_docs"
    ref = ai / "reference"
    (ref / ".sources").mkdir(parents=True)
    snapshot = "# Source\n\nIndicazioni del proprietario sul server di produzione.\n"
    (ref / ".sources" / "server.md").write_text(snapshot, encoding="utf-8")
    digest = hashlib.sha256(snapshot.encode("utf-8")).hexdigest()
    body = "\n\n".join(f"**{s}** Testo operativo." for s in FALSE_SENTENCES)
    (ref / "GUIDE_server.md").write_text(
        "---\n"
        "description: Consult before operating on the production server.\n"
        "status: CURRENT\n"
        "source_kind: document\n"
        "source: Owner indications, 2026-10-29\n"
        "distilled_from: ai_docs/reference/.sources/server.md\n"
        f"source_hash: {digest}\n"
        "---\n# Guide: production server\n\n"
        "[source: server.md#source]\n" + body +
        "\n\n## Registro delle modifiche\n\n| Data | Modifica | Chi |\n|---|---|---|\n"
        + LOG_ROW + "\n", encoding="utf-8")
    (ai / "README.md").write_text("# ai_docs\n\n1. `reference/INDEX.md`\n", encoding="utf-8")
    (ai / "audit").mkdir()
    (ai / "audit" / "HANDOFF_x.md").write_text(
        "---\nworkstream: F-001 Server\nlevel: L3\nbranch: main\nstatus: PROGRESS\n"
        "since: 2026-11-14\nnext: close the node\ndetails: -\nupdated: 2026-11-14\n---\n# HANDOFF\n",
        encoding="utf-8")


def main():
    checker = Path(sys.argv[1]).resolve()
    ok = True
    with tempfile.TemporaryDirectory() as tmp:
        build_tree(tmp)
        run(checker, "index", "--root", tmp)
        rc, out = run(checker, "check", "--root", tmp)
        clean = "check: CLEAN" in out
        scoped = any(line.startswith("[scope]") for line in out.splitlines())
        print(f"P2 guide with three false state sentences -> check CLEAN: {clean}")
        print(f"P2 the verdict states what CLEAN does not cover ([scope] line): {scoped}")
        ok &= clean and scoped

        rc, out = run(checker, "orient", "--root", tmp)
        resume = "work from a summary" in out.lower()
        print(f"P4 orient carries the resume rule (constant line): {resume}")
        ok &= resume and rc == 0
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
