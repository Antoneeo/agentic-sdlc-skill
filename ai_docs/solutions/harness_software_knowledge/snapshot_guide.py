"""Refresh the new guide snapshot from exact AST spans; old snapshots stay intact."""
from pathlib import Path
import ast
import hashlib

ROOT = Path(__file__).resolve().parents[3]
selected = {
 'skills/agentic-sdlc-skill/scripts/knowledge.py': ['memory_records', 'memory_recall', 'memory_validate', 'kb_check_claims', '_kb_read_bytes', '_kb_capture_lock', '_kb_project_id', '_kb_software_integrity', 'kb_capture_source', 'kb_software_findings', 'kb_cmd_evidence', 'kb_export_closure', 'kb_import_plan', 'kb_validate_surface', 'kb_cmd_check'],
 'distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py': ['cmd_index', 'run_check', 'main'],
 'distributions/course-creator/skills/course-creator/scripts/sdlc_check.py': ['main'],
}
parts=['# Shared project memory — exact software-evidence source excerpts\n\nCaptured from the implementation checkout; symbols label verbatim bodies, not execution evidence.\n']
for rel, names in selected.items():
 text=(ROOT/rel).read_text(encoding='utf-8')
 lines=text.splitlines(keepends=True)
 nodes={node.name:node for node in ast.parse(text).body if isinstance(node,(ast.FunctionDef,ast.ClassDef))}
 for name in names:
  node=nodes[name]
  start=min([node.lineno]+[x.lineno for x in getattr(node,'decorator_list',[])])
  parts.append('\n## '+rel+':'+name+'\n\n```python\n'+''.join(lines[start-1:node.end_lineno])+'```\n')
dest=ROOT/'ai_docs/reference/.sources/shared-project-memory-software-evidence.md'
dest.write_text(''.join(parts),encoding='utf-8',newline='\n')
print(hashlib.sha256(dest.read_bytes()).hexdigest())
