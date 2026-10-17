"""Freeze reproducible trial inputs before collecting participant output."""
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def prepare():
    frozen = ROOT / "instructions"
    frozen.mkdir(exist_ok=True)
    manifest = {}
    for name in ("SKILL.md", "review.md"):
        source = Path.home() / ".codex/skills/agentic-sdlc" / name
        data = source.read_bytes()
        target = frozen / name
        if target.exists() and target.read_bytes() != data:
            raise RuntimeError(f"Refusing to replace frozen instructions: {target}")
        target.write_bytes(data)
        manifest[str(target.relative_to(ROOT))] = dict(
            origin=str(source), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    source = (ROOT / "fixture.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    names = {"read_catalogue", "read_summary", "baseline_outcome", "deliver"}
    functions = [ast.get_source_segment(source, node) for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name in names]
    implementation = "from copy import deepcopy\n\n" + "\n\n".join(functions)
    # Rename only the experimental arm identifier; no participant sees 'baseline'.
    implementation = implementation.replace("baseline_outcome", "classify_outcome")
    smoke = '''from fixture import deliver, read_summary

assert deliver("read_summary", read_summary(["Atlas"])) == {"state": "delivered", "content": "Atlas"}
assert deliver("read_summary", {"status": "failed", "records": []}) == {"state": "blocked", "content": None}
assert deliver("read_summary", read_summary(["Atlas"]), stopped=True) == {"state": "stopped", "content": None}
print("3 existing smoke assertions passed")
'''
    (ROOT / "existing_smoke.py").write_text(smoke, encoding="utf-8")
    packet = '''# Catalogue delivery — review packet

## Assignment
Review the implementation for readiness against the original user need and the
design, applying the supplied methodology. Return READY or NOT_READY, the
substantive findings with evidence, and the single most useful next test (input,
expected observable output, and why). Do not edit files or execute code. Label
static deductions and checks not performed. The packet contains the complete
synthetic system; there are no other application modules to search.

## Original user need
A reader requests a catalogue or a summary. Deliver the complete available
records as text. A legitimately empty catalogue is a valid empty delivery.
Failed or unfinished reads must not be presented as completed. Stop takes
precedence. This increment has no network, permissions, persistence or retries.

## Design supplied for review
Two producers feed a shared publication boundary. The gate classifies explicit
success, failure, or unknown. Only success may publish; unknown and failure
block. Stop is checked first. Record content is joined with newlines.
The existing smoke tests cover delivery, failure and Stop. Assess whether the
increment is ready; the design and test results are evidence to assess.

## Implementation
```python
''' + implementation + '''
```

## Existing smoke tests
```python
''' + smoke + '''
```
'''
    target = ROOT / "trial_packet.md"
    if target.exists() and target.read_text(encoding="utf-8") != packet:
        raise RuntimeError("Refusing to alter frozen trial packet")
    target.write_text(packet, encoding="utf-8")
    for name in ("PROTOCOL.md", "trial_packet.md", "fixture.py", "probe.py"):
        data = (ROOT / name).read_bytes()
        manifest[name] = dict(sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
    (ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    prepare()
