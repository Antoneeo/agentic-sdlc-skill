"""One-shot, reviewed-scope F064 migration; not shipped."""
from pathlib import Path
import json
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / 'skills/agentic-sdlc-skill'
KB = ROOT / 'distributions/kb-agentic-skill/skills/kb-agentic-skill'
DIRS = [CODE, KB, ROOT / 'distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc', ROOT / 'distributions/course-creator/skills/course-creator']
METHODS = ['distillation.md', 'taxonomy.md', 'reconciliation.md', 'portability.md', 'knowledge-templates.md']

def read(p):
    return p.read_text(encoding='utf-8')

def write(p, text):
    p.write_text(text, encoding='utf-8', newline='\n')

def replace(text, old, new):
    assert old in text, old
    return text.replace(old, new)

text = read(KB / 'distillation.md')
text = replace(text, '## 1. Intake — everything becomes a file first', '''## 1. Intake — everything becomes a file first

For software, select the smallest relevant file span BEFORE intake, preserving its
conditions and limits. Exhaust that selected extract, not the repository. Use
`capture-source <relative-path> --lines A:B --role code|test|config|result` to preserve
exact UTF-8 bytes and the version binding. It does not extract claims or declare
reading complete. Binding fields and typed rows: `knowledge-templates.md`.
An interpretation of code is a DERIVED note citing captured extracts. A test's source
and an execution result are different evidence; an approved design is not execution.
Joint premises belong in `derived_from:` (AND); the claim's `source` alternatives
are independent corroborations (OR), as defined in `memory.md` §Software evidence.''')
text = replace(text, '(`templates.md` has the template)', '(`knowledge-templates.md` has the template)')
text = replace(text, '(`templates.md`) — `p=<n>`', '(`knowledge-templates.md`) — `p=<n>`')
text = replace(text, '## 3. Extraction discipline', '''For a typed topic set `claim_schema: 2` and append the ninth column `kind`:
`OBSERVATION | REQUIREMENT | HYPOTHESIS | DESIGN`. Kind is independent of provenance
and state: observed behavior, required property, documented uncertainty, intended
change. Legacy eight-column topics remain readable and UNCLASSIFIED; never infer
their nature from prose. Classify on a relevant revisit, with source inspection.

## 3. Extraction discipline''')
text = replace(text, 'Ingesting a document set is **L3 by Rule Zero**;', 'For independent KB assignments, ingesting a document set is **L3 by Rule Zero**;')
text = replace(text, 'correctness first.', 'correctness first. Other lenses keep their owning triage and plan; using this\nmethod alone creates no second analysis or ingestion project.')
text = replace(text, '- Zero speculation: unverified information is marked `[unverified]` or omitted — never\n  written as a claim.', '- Zero speculation: undocumented guesses are omitted or recorded as gaps. A\n  HYPOTHESIS may represent a source-documented uncertainty, explicitly as such; it\n  never asserts the suspected behavior as an OBSERVATION.')
write(CODE / 'distillation.md', text)

text = read(KB / 'taxonomy.md')
text = replace(text, "Re-parenting rewrites the graph's shape, and kb's Rule Zero makes hierarchy changes L3\n(escalation triggers, `SKILL.md`): stop, declare, and treat it as its own unit — never a\nside effect of placing one claim.", "Re-parenting rewrites the graph's shape. In independent KB assignments, kb's Rule\nZero makes hierarchy changes L3: stop, declare and treat it as its own unit. Other\nlenses classify through their owner and router; importing this method does not import\nKB triage. A hierarchy change is always explicit, never a side effect of placement.")
text = replace(text, '(`SKILL.md` §Topic Recall)', '(`memory.md` §Topic Recall)')
write(CODE / 'taxonomy.md', text)

text = read(KB / 'reconciliation.md')
text = replace(text, 'Subject-sameness is semantic judgement; no query performs it. Classify:', '''Compare nature before meaning: an OBSERVATION and a REQUIREMENT or DESIGN may
differ legitimately. Unlike kinds coexist; never CONTEST or SUPERSEDE across kinds.
Approval changes neither kind nor observed reality. UNCLASSIFIED legacy rows need
source inspection before classification, never a silent inferred migration. Within
one kind, compare subject, conditions and validity, then classify below. Provenance
still describes origin, not rank. Keep prior evidence and claim history.

Subject-sameness is semantic judgement; no query performs it. Classify:''')
text = replace(text, 'per the kb `## Revision` doctrine', 'per `memory.md` §Revision')
write(CODE / 'reconciliation.md', text)

text = read(KB / 'portability.md')
text = replace(text, '- **Every row a `CONTESTED` row points at.**', '- **Every transitive `derived_from` premise**, including sidecars and canonical\n  extractions. Missing references, escaping paths and cycles refuse the export.\n- **Every row a `CONTESTED` row points at.**')
text = replace(text, '- **All or nothing.** The whole plan is computed before a byte is written. An import that\n  half-applies leaves a tree whose checks fail and whose owner cannot tell what landed.', '- **Preflight before writing.** The whole plan is computed before a byte is written.\n  This is not a filesystem transaction: an I/O interruption may leave a partial\n  additive import. Inspect it, rerun the plan, and run `check` before use.')
text = replace(text, 'origin); an incomplete conflict set; a dangling `supersedes:`.', 'origin). `check` then detects incomplete conflict sets and dangling references;\nimport itself does not certify the graph.')
text = replace(text, 'So an imported ruling arrives as **`prov: IMPORTED`** (owner ruling, 2026-08-03):', 'The receiving agent must mark imported rulings **`prov: IMPORTED`** (owner ruling,\n2026-08-03). The additive file-copy command does not rewrite their authority:')
text = replace(text, '## 5. Triage', '''Software sidecars and their project UUID travel unchanged. An import never adopts
the source project's README identity: foreign bindings report UNBOUND without opening
local paths as if they were the source project. A clone retaining the same UUID may
match, subject to byte checks. To support a foreign claim locally, add local evidence
through normal capture and reconciliation; do not relabel its foreign binding.

## 5. Triage''')
text = replace(text, 'Exporting is L1', 'For independent KB assignments, exporting is L1')
text += '\nOther lenses use their owning router and risk scale; importing this method does not\ncreate a second KB workflow. External input remains never L1.\n'
write(CODE / 'portability.md', text)

text = read(KB / 'templates.md')
start = text.index('## ai_docs/topics/[slug].md (topic node)')
common = '# Knowledge templates — shared ledger, sources and rulings\n\n' + text[start:]
common += '''
## Typed software topic (opt-in schema 2)

Use the topic fields above, plus `claim_schema: 2`. A typed table has exactly nine
columns. Kind never replaces provenance or claim state.

```markdown
| id | claim | valid | qty | about | source | prov | state | kind |
|---|---|---|---|---|---|---|---|---|
| | A successful edit preserves the logical card identity | if save succeeds | - | - | corpus/notes/card-identity.md#L8-10 | DERIVED | OK | OBSERVATION |
```

Kinds: OBSERVATION (observed), REQUIREMENT (required), HYPOTHESIS (documented
uncertainty), DESIGN (planned). Legacy tables retain eight columns and existing IDs;
evidence reports their nature as UNCLASSIFIED until deliberately classified.

## Software binding (capture-source generated)

```yaml
sha256: <64 hex chars: exact stored extract>
software_schema: 1
software_project_id: <canonical UUID from the docs-root README>
software_path: src/card.py
software_sha256: <64 hex chars: complete file at capture time>
software_span: 20-48
software_role: code
```

All six software fields are required together. Roles: code, test, config, result.
The generated name contains both the full extract digest and a digest of its binding
and normalized premises; equal text from distinct paths/versions never collides.
Source locators address the STORED extract starting at line 1. `software_span` locates
it in the original file, not in the extract. Add `extracted_through` only after reading.
No absolute `original_path` is required. These metadata do not attest completeness,
execution, truth, signature or an authenticated project identity.

A derived note uses `derived_from: [corpus/given/<extract>.txt, ...]` for ALL joint
premises. An observation that needs code, configuration and a test result must cite
that note, not list those premises as independent corroborations in its source cell.
'''
write(CODE / 'knowledge-templates.md', common)
anchors = ['## ai_docs/topics/[slug].md (topic node)', '## ai_docs/corpus/given/[name].meta.md (source sidecar)', '## ai_docs/corpus/notes/RULING_[topic]_[date].md (practitioner ruling)']
write(KB / 'templates.md', text[:start] + '\n\n'.join(a + '\n\nUse the corresponding template in `knowledge-templates.md` (shared authority).' for a in anchors) + '\n')

text = read(KB / 'SKILL.md')
start = text.index('## Topic Recall —')
end = text.index('## Mechanical Enforcement', start)
old = text[start:end]
capture = old[old.index('- **When —'):old.index('- **The sweep is idempotent.')]
text = text[:start] + '''## Topic Recall — the answer-side consult

For KB answers, unconditional scan on domain assertions: coverage is judged ON the
scanned top rows, never before them. Exempt: pure mechanics and general knowledge
outside the project's domain, L1 gestures. Apply `memory.md` §Topic Recall for descent,
verdicts, citation scope, re-touch and dispatch; `taxonomy.md` owns the descent.

## The Capture Moment — the day's decisions reach the ledger

Use `memory.md` §Capture for source channeling, idempotence and reconciliation.
The KB-specific timing and question remain here:

''' + capture + '''- Domain decisions include values, thresholds, rules, preferences and rejected
  alternatives with reasons; commands and process state belong in the handoff.
- A fact on an existing topic is L1 under KB triage. Without an owning topic, capture
  the note now and declare placement as the next KB unit; no implicit hierarchy change.
- **Silence stays legal where no one signed off**: no closing signal, no question.

## Revision — the full re-read

Apply `memory.md` §Revision, the single shared prose-revision authority. The L2 and
Phase-4 pointers to this anchor retain their existing scope.

''' + text[end:]
text = replace(text, '## Mechanical Enforcement', '## Mechanical Enforcement\n- `scripts/sdlc_check.py capture-source`: preserve a selected software span and version.\n- `scripts/sdlc_check.py evidence`: report declared software evidence and its limits.')
write(KB / 'SKILL.md', text)

text = read(CODE / 'routing.md')
text = replace(text, 'deliverables, not the act of reading another domain\'s evidence.', "deliverables, not the act of reading another domain's evidence. Shared methods do\nnot import the KB lens's triage: standalone intake and hierarchy levels remain scoped\nto independent KB assignments; other work keeps its owning lens and plan.")
write(CODE / 'routing.md', text)

# Distribution declarations and allowlists: append missing resources only.
for directory in DIRS:
    text = read(directory / 'SKILL.md')
    addition = '''
## Shared knowledge methods (on demand)

`memory.md` is the common recall/capture/revision entry. For source intake read
`distillation.md`; for placement `taxonomy.md`; for additions and updates
`reconciliation.md`; for bundles `portability.md`. Formats live in
`knowledge-templates.md`. Read on the corresponding trigger, under this lens's triage.
'''
    if '## Shared knowledge methods (on demand)' not in text:
        text += addition
    write(directory / 'SKILL.md', text)
    entry = directory / 'scripts' / ('mkt_check.py' if directory.name == 'mkt-agentic-sdlc' else 'sdlc_check.py')
    text = read(entry)
    missing = [x for x in METHODS if '"' + x + '"' not in text]
    if missing:
        text = replace(text, '"memory.md"', '"memory.md", ' + ', '.join('"' + x + '"' for x in missing))
    if entry.name == 'mkt_check.py':
        text = replace(text, 'full=args.command == "check"', 'full=args.command == "check", project=root')
    write(entry, text)
    package_root = ROOT if directory == CODE else directory.parents[1]
    package = json.loads(read(package_root / 'package.json'))
    prefix = directory.relative_to(package_root).as_posix() + '/'
    package['files'].extend(prefix + m for m in METHODS if prefix + m not in package['files'])
    write(package_root / 'package.json', json.dumps(package, indent=2, ensure_ascii=False) + '\n')

text = read(CODE / 'scripts/shared_files.py')
text = replace(text, '    "memory.md",', '    "memory.md",\n    "scripts/test_software_knowledge.py",\n' + ''.join('    "' + f + '",\n' for f in METHODS).rstrip())
text = replace(text, 'architect/tdd/debugging | taxonomy/distillation |', 'architect/tdd/debugging |')
write(CODE / 'scripts/shared_files.py', text)

# Move doctrine guards to the common authority without dropping guarantees.
p = KB / 'scripts/test_kb_revision.py'
text = read(p).replace('self.skill = normalized(SKILL)', 'self.skill = normalized(SKILL)\n        self.memory = normalized(SKILL_DIR / "memory.md")')
text = text.replace('self.assertIn("## Revision", self.skill)', 'self.assertIn("## Revision", self.skill)\n        self.assertIn("`memory.md` §Revision", self.skill)')
text = text.replace('self.assertIn(anchor, self.skill, anchor)', 'self.assertIn(anchor, self.memory, anchor)').replace('"never the ledger", self.skill', '"never the ledger", self.memory').replace('"never re-parents", self.skill', '"never re-parents", self.memory')
write(p, text)
p = KB / 'scripts/test_kb_recall.py'
text = read(p)
text = text.replace('text = normalized(SKILL_DIR / "SKILL.md")', 'text = normalized(SKILL_DIR / "memory.md")', 2)
text = replace(text, '            "## Topic Recall — the answer-side consult",\n', '')
text = replace(text, '    def test_skill_md_carries_the_recall_section(self):', '    def test_skill_md_carries_the_recall_section(self):\n        skill = normalized(SKILL_DIR / "SKILL.md")\n        self.assertIn("## Topic Recall — the answer-side consult", skill)\n        self.assertIn("`memory.md` §Topic Recall", skill)')
write(p, text)
p = KB / 'scripts/test_kb_capture.py'
text = read(p)
start = text.index('        for anchor in (', text.index('def test_skill_md_carries_the_capture_section'))
end = text.index('    def test_write_triggers', start)
original = text[start:end]
common_anchors = ['`derived_from:` → claim `prov: DERIVED`','The sweep is idempotent','never re-captured','prov: ELICITED','RULING only when the decision resolves an existing contested set','never a decision park','never silently overwrite']
for a in common_anchors:
    original = replace(original, '            "' + a + '",\n', '')
original += '        self.assertIn("`memory.md` §Capture", text)\n        memory = normalized(SKILL_DIR / "memory.md")\n        for anchor in ' + repr(tuple(common_anchors)) + ':\n            self.assertIn(anchor, memory, anchor)\n\n'
text = text[:start] + original + text[end:]
write(p, text)

for directory in DIRS[1:]:
    for rel in METHODS + ['memory.md', 'routing.md', 'scripts/knowledge.py', 'scripts/shared_files.py', 'scripts/test_software_knowledge.py']:
        shutil.copyfile(CODE / rel, directory / rel)
for directory in DIRS:
    subprocess.run([sys.executable, str(directory / 'scripts/shared_files.py'), '--update'], check=True)
print('F064 shared methods and packaging migrated')
