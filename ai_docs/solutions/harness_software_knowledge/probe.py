"""F-063: characterize existing KB capabilities; no product writes.

Run normally, then with --negative-control to invert each asserted observation.
Fixtures are temporary. This is evidence for analysis, not implementation acceptance.
"""
import argparse
import contextlib
import hashlib
import io
import json
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "skills/agentic-sdlc-skill/scripts"))
import knowledge as kb


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative-control", action="store_true")
    args = parser.parse_args()
    results = []

    def expect(name, condition, detail):
        passed = not condition if args.negative_control else condition
        results.append({"id": name, "pass": bool(passed), "detail": detail})

    with tempfile.TemporaryDirectory(prefix="f063-") as temp:
        project = Path(temp)
        docs = project / "ai_docs"

        def put(path, text):
            target = docs / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text, encoding="utf-8")
            return target

        put("README.md", "# Fixture\n")
        put("reference/GUIDE_retry.md", "---\ndescription: Retry behavior\n---\n# Retry\nquasarneedle\n")
        with contextlib.redirect_stdout(io.StringIO()):
            kb.kb_refresh_indexes(docs)
        expect("P1", (docs / "memory/INDEX.md").exists() and not (docs / "topics").exists(),
               "Indexing an original creates the memory catalog, without creating topics.")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            kb.memory_recall(docs, "quasarneedle")
        expect("P2", "No metadata match" in output.getvalue(),
               "A body-only term does not match recall metadata.")

        source = put("corpus/given/retry.txt", "Retry limit is three.\n")
        original = project / "runtime.py"
        original.write_text("RETRIES = 3\n", encoding="utf-8")
        digest = hashlib.sha256(source.read_bytes()).hexdigest()
        original_digest = hashlib.sha256(original.read_bytes()).hexdigest()
        put("corpus/given/retry.txt.meta.md",
            f"---\nsha256: {digest}\noriginal_path: {original.as_posix()}\n"
            f"original_sha256: {original_digest}\nextracted_through: complete\n---\n")
        put("topics/runtime.md", "---\nslug: runtime\ndescription: Runtime behavior\nparents: []\n---\n# Runtime\n")
        claim_id = kb.kb_claim_id("corpus/given/retry.txt", "L1-1")
        table = ("## Claims\n| id | claim | valid | qty | about | source | prov | state |\n"
                 "|---|---|---|---|---|---|---|---|\n"
                 f"| {claim_id} | Retry limit is three. | - | - | - | corpus/given/retry.txt#L1-1 | GIVEN | OK |\n")
        put("topics/retry.md", "---\nslug: retry\ndescription: Retry policy\nparents: [runtime]\ngaps: Timeout behavior unexamined\n---\n# Retry\n" + table)
        errors, warnings = kb.kb_graph_check(docs)
        ce, cw, _ = kb.kb_check_claims(docs)
        expect("P3", not errors and not ce and "runtime" in kb.kb_build_topic_index(docs),
               "A parent/child topic fixture and a source-anchored claim validate.")
        rows, pe = kb.kb_parse_claims(table)
        expect("P4", not pe and len(rows) == 1 and "kind" not in rows[0]
               and rows[0]["prov"] == "GIVEN" and rows[0]["state"] == "OK",
               "The current claim schema has provenance and lifecycle, no kind field.")
        altered = table.replace("| state |", "| state | kind |").replace(
            "| GIVEN | OK |", "| GIVEN | OK | OBSERVED |")
        _, pe = kb.kb_parse_claims(altered)
        expect("P5", bool(pe), "Adding a kind column to the existing schema is rejected.")

        before_corpus = kb.kb_corpus_check(docs)
        before_cycle = kb.kb_time_cycle(docs)
        original.write_text("RETRIES = 7\n", encoding="utf-8")
        after_corpus = kb.kb_corpus_check(docs)
        after_cycle = kb.kb_time_cycle(docs)
        expect("P6", before_corpus == ([], []) and after_corpus == before_corpus
               and after_cycle == before_cycle and not any(after_cycle.values()),
               "Changing only the linked live original produces no corpus/time-cycle finding in this fixture.")
        source.write_text("Retry limit is seven.\n", encoding="utf-8")
        errors, _ = kb.kb_corpus_check(docs)
        expect("P7", any("digest changed" in x for x in errors),
               "Mutating the preserved source bytes does produce a corpus digest error.")
        source.write_text("Retry limit is three.\n", encoding="utf-8")
        put("corpus/notes/inference.md", "---\nderived_from: [corpus/given/retry.txt]\n---\nRetry inference.\n")
        replacement = put("corpus/given/retry-new.txt", "Retry limit is seven.\n")
        put("corpus/given/retry-new.txt.meta.md", "---\nsha256: "
            + hashlib.sha256(replacement.read_bytes()).hexdigest()
            + "\nsupersedes: retry.txt\nextracted_through: complete\n---\n")
        cycle = kb.kb_time_cycle(docs)
        expect("P8", any(owner == "corpus/notes/inference.md" and ground == "corpus/given/retry.txt"
                         for owner, ground, _ in cycle["chain"]),
               "An explicit source supersession reaches its derived note.")
        with contextlib.redirect_stdout(io.StringIO()):
            kb.kb_refresh_indexes(docs)
        original.write_text("RETRIES = 11\n", encoding="utf-8")
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = kb.memory_validate(docs)
        expect("P9", status == 0,
               "The document catalog remains current when only code outside the docs root changes.")
        put("topics/retry.md", "# Retry\n" + table.replace(
            "corpus/given/retry.txt#L1-1", "../runtime.py#L1-1"))
        errors, _, _ = kb.kb_check_claims(docs)
        expect("P10", any("escapes the docs root" in x for x in errors),
               "A direct claim source outside ai_docs is rejected; evidence needs the existing corpus boundary.")

    inputs = [Path(__file__), REPO / "skills/agentic-sdlc-skill/scripts/knowledge.py",
              REPO / "skills/agentic-sdlc-skill/scripts/sdlc_core.py"]
    hashes = {p.relative_to(REPO).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
              for p in inputs}
    print(json.dumps({"python": sys.version, "input_sha256": hashes,
                      "negative_control": args.negative_control, "results": results}, indent=2))
    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
