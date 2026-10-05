"""Snapshot planned files before edits; produce this task's diff at closure."""
import difflib
import json
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent / "implementation"
EXTRA = (
    "ai_docs/audit/reviews/REVIEW_software_knowledge_code_2026-10-04.md",
    "ai_docs/audit/reviews/TEST_software_knowledge_2026-10-04.md",
    "ai_docs/solutions/ANALYSIS_kb_evidence.md", "ai_docs/solutions/ANALYSIS_software_knowledge.md",
    "ai_docs/audit/HANDOFF_kb_evidence.md", "ai_docs/audit/HANDOFF_software_knowledge.md",
    "ai_docs/audit/reviews/REVIEW_LOG.md", "ai_docs/audit/audit_plan.md",
    "ai_docs/INDEX.md", "ai_docs/memory/INDEX.md", "ai_docs/reference/INDEX.md",
    "ai_docs/strategic/features_history.md", "ai_docs/audit/handoff.md",
)


def main():
    HERE.mkdir(exist_ok=True)
    archive = HERE / "before.zip"
    if sys.argv[1] == "snapshot":
        if archive.exists():
            raise SystemExit("baseline exists; refusing replacement")
        table = (ROOT / "ai_docs/solutions/DESIGN_software_knowledge_files.md").read_text(encoding="utf-8").split("## Blast radius")[0]
        paths = sorted(set([line.split("`", 2)[1] for line in table.splitlines()
                            if line.startswith("| `")] + list(EXTRA)))
        with zipfile.ZipFile(archive, "x", zipfile.ZIP_DEFLATED) as z:
            for rel in paths:
                if (ROOT / rel).is_file():
                    z.write(ROOT / rel, rel)
        (HERE / "paths.json").write_text(json.dumps(paths, indent=2), encoding="utf-8")
        print("baseline:", len(paths), "paths")
    else:
        paths = sorted(set(json.loads((HERE / "paths.json").read_text(encoding="utf-8")) + list(EXTRA)))
        table = (ROOT / "ai_docs/solutions/DESIGN_software_knowledge_files.md").read_text(encoding="utf-8").split("## Blast radius")[0]
        additions = {ln.split("`", 2)[1] for ln in table.splitlines()
                     if ln.startswith("| `") and "| ADD |" in ln}
        parts, changed = [], []
        with zipfile.ZipFile(archive) as z:
            for rel in paths:
                old = z.read(rel) if rel in z.namelist() and rel not in additions else b""
                new = (ROOT / rel).read_bytes() if (ROOT / rel).is_file() else b""
                if old == new:
                    continue
                changed.append(rel)
                parts.extend(difflib.unified_diff(old.decode("utf-8-sig").splitlines(True),
                    new.decode("utf-8-sig").splitlines(True), fromfile="a/" + rel,
                    tofile="b/" + rel))
        (HERE / "software-knowledge.diff").write_text("".join(parts), encoding="utf-8")
        (HERE / "changed.json").write_text(json.dumps(changed, indent=2), encoding="utf-8")
        print("task diff:", len(changed), "files")


if __name__ == "__main__":
    main()
