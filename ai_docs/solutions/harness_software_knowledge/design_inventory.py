"""Read-only AST/text impact inventory for the F-063/F-064 design.

Output is JSON on stdout. No imports of product modules and no product writes.
AST name/attribute references are candidates, not a whole-program resolver:
wildcard re-exports and dynamic imports are recorded separately for review.
"""
import ast
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SYMBOLS = (
    "CLAIM_COLUMNS", "kb_parse_claims", "kb_check_claims", "kb_corpus_check",
    "kb_time_cycle", "kb_export_closure", "kb_import_plan", "kb_validate_surface",
    "kb_cmd_check", "kb_cmd_stale", "kb_cmd_help", "INTERCEPTED", "SHARED_FILES",
    "knowledge.main",
)
DOCTRINE = re.compile(r"Topic Recall|Capture Moment|never append a delta|## Revision|"
                     r"RevisionDoctrineTests|TestRecallDoctrine|TestCaptureDoctrine", re.I)


def scan():
    proc = subprocess.run(
        ["rg", "--files", "-g", "*.py", "-g", "*.js", "-g", "*.json", "-g", "*.md"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True)
    files = sorted(set(p.replace("\\", "/") for p in proc.stdout.splitlines()))
    self_rel = Path(__file__).resolve().relative_to(ROOT).as_posix()
    authoring_only = {self_rel, str(Path(self_rel).with_name("design_files.py")).replace("\\", "/"),
                      str(Path(self_rel).with_name("capture_case.py")).replace("\\", "/")}
    # The runtime, developer batteries and shipped entry points are the consumer
    # population; ai_docs evidence is an additional, explicitly separate population.
    product = [p for p in files if p.startswith(("skills/", "distributions/", "scripts/"))]
    evidence = [p for p in files if p.startswith("ai_docs/") and p.endswith(".py") and p not in authoring_only]
    py = [p for p in product + evidence if p.endswith(".py")]
    refs = {s: [] for s in SYMBOLS}
    text_refs = {s: [] for s in SYMBOLS}
    failures, imports, hashes, signatures = [], [], {}, {}
    doctrine_refs = []
    for rel in product + evidence:
        raw = (ROOT / rel).read_bytes()
        txt = raw.decode("utf-8-sig")
        hashes[rel] = hashlib.sha256(raw).hexdigest()
        for n, line in enumerate(txt.splitlines(), 1):
            if DOCTRINE.search(line):
                doctrine_refs.append({"path": rel, "line": n, "text": line.strip()})
        for s in SYMBOLS:
            for n, line in enumerate(txt.splitlines(), 1):
                if re.search(r"(?<![\w])" + re.escape(s) + r"(?![\w])", line):
                    text_refs[s].append({"path": rel, "line": n, "text": line.strip()})
        if not rel.endswith(".py"):
            continue
        try:
            tree = ast.parse(txt, filename=rel)
        except SyntaxError as exc:
            failures.append({"path": rel, "error": str(exc)})
            continue

        class Visitor(ast.NodeVisitor):
            def __init__(self):
                self.scope = []

            def visit_FunctionDef(self, node):
                if rel.endswith("/knowledge.py") and not self.scope:
                    signatures[node.name] = ast.unparse(node.args)
                self.scope.append(node.name)
                self.generic_visit(node)
                self.scope.pop()

            visit_AsyncFunctionDef = visit_FunctionDef

            def visit_ClassDef(self, node):
                self.scope.append(node.name)
                self.generic_visit(node)
                self.scope.pop()

            def add(self, name, node):
                if name in refs and isinstance(node.ctx, ast.Load):
                    refs[name].append({"path": rel, "line": node.lineno,
                                       "consumer": ".".join(self.scope) or "<module>"})

            def visit_Name(self, node):
                self.add(node.id, node)

            def visit_Attribute(self, node):
                self.add(node.attr, node)
                if isinstance(node.value, ast.Name) and node.value.id == "knowledge":
                    self.add("knowledge." + node.attr, node)
                self.generic_visit(node)

            def visit_ImportFrom(self, node):
                if node.module in ("knowledge", "sdlc_check", "shared_files"):
                    imports.append({"path": rel, "line": node.lineno,
                                    "module": node.module,
                                    "names": [a.name for a in node.names]})

        Visitor().visit(tree)
    delta = {}
    for s in SYMBOLS:
        locations = {(r["path"], r["line"]) for r in refs[s]}
        delta[s] = [r for r in text_refs[s] if (r["path"], r["line"]) not in locations]
    return {
        "scope": "rg-discovered source/docs in skills, distributions, scripts; Python evidence in ai_docs separately",
        "limits": "AST references by name/attribute; no execution or cross-module identity proof. Text-only declarations, prose, strings and wildcard exports must be inspected; dynamic calls are not certified absent.",
        "coverage": {"product_files_text": len(product), "evidence_python_files": len(evidence),
                     "python_files_ast": len(py), "python_parse_failures": failures,
                     "excluded_design_authoring_scripts": sorted(authoring_only)},
        "signatures": signatures, "ast_references": refs,
        "text_only_delta": delta, "re_exports": imports, "input_sha256": hashes,
        "doctrine_text_references": doctrine_refs,
        "doctrine_limits": "Separate text probe for transferred Markdown clauses and their test classes, across the same file population. Includes producers, pointers and tests; it is not an API call graph or proof of absence of paraphrases.",
    }


if __name__ == "__main__":
    print(json.dumps(scan(), indent=2, ensure_ascii=False))
