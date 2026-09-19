"""Evidence for the integration design; writes only inside a temporary fixture.

Run with --negative-control to falsify the behavioral assertions deliberately.
This probes validator behavior, not whether an agent follows written instructions.
"""
import argparse
import contextlib
import importlib.util
import io
from pathlib import Path
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[3]
KB = ROOT / 'distributions/kb-agentic-skill/skills/kb-agentic-skill'
sys.path.insert(0, str(KB / 'scripts'))
spec = importlib.util.spec_from_file_location('integration_kb', KB / 'scripts/sdlc_check.py')
kb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(kb)


def quiet(fn, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = fn(*args)
    return rc, out.getvalue()


def main():
    negative = argparse.ArgumentParser()
    negative.add_argument('--negative-control', action='store_true')
    flip = negative.parse_args().negative_control
    with tempfile.TemporaryDirectory(prefix='sdlc-kb-design-') as tmp:
        root = Path(tmp)
        docs = root / 'ai_docs'
        docs.mkdir()
        (docs / 'README.md').write_text('# Reading guide\n', encoding='utf-8')
        kb.sdlc_core.set_docs_dir('ai_docs')
        quiet(kb.kb_cmd_index, root, docs)
        absent = not (docs / 'topics').exists() and not (docs / 'corpus').exists()
        print('P1: kb index leaves absent topics/ and corpus/ absent:', absent)
        failures = [absent != (not flip)]
        (docs / 'topics').mkdir()
        (docs / 'topics/broken.md').write_text(
            '---\nslug: broken\ndescription: Probe node\nstatus: CURRENT\n'
            'parents: [broken]\nsynonyms: []\n---\n# Broken\n', encoding='utf-8')
        quiet(kb.kb_cmd_index, root, docs)
        core_rc, core_text = quiet(kb.sdlc_core.cmd_check, root)
        kb_rc, kb_text = quiet(kb.kb_cmd_check, root, docs)
        graph_errors, _ = kb.kb_graph_check(docs)
        extra = bool(graph_errors) and all(e in kb_text for e in graph_errors)
        extra = extra and any(e not in core_text for e in graph_errors) and kb_rc != 0
        print('P2: kb check adds graph errors not reported by core check:', extra)
        print('    core rc:', core_rc, 'kb rc:', kb_rc, 'graph errors:', graph_errors)
        failures.append(extra != (not flip))
        (docs / 'architecture').mkdir()
        (docs / 'architecture/ADR_probe.md').write_text(
            '# Decision\nThe recorded timeout is 30 seconds.\n', encoding='utf-8')
        (docs / 'corpus/notes').mkdir(parents=True)
        (docs / 'corpus/notes/decision.md').write_text(
            '---\nderived_from: architecture/ADR_probe.md\n---\n'
            '# Decision note\nThe ADR records a 30 second timeout.\n', encoding='utf-8')
        topic = docs / 'topics/broken.md'
        table = ('---\nslug: broken\ndescription: Probe node\nstatus: CURRENT\n'
                 'parents: []\nsynonyms: []\n---\n# Decision\n\n## Claims\n'
                 '| id | claim | valid | qty | about | source | prov | state |\n'
                 '|---|---|---|---|---|---|---|---|\n'
                 '| | The ADR records a 30 second timeout. | - | - | - | '
                 '{source} | DERIVED | OK |\n')
        topic.write_text(table.format(source='corpus/notes/decision.md#L5-5'), encoding='utf-8')
        errors, _, _ = kb.kb_check_claims(docs)
        cycle = kb.kb_time_cycle(docs)
        _, _, dangling = kb.kb_time_cycle_warns(cycle)
        valid_chain = not errors and not dangling
        topic.write_text(table.format(source='architecture/ADR_probe.md#L2-2'), encoding='utf-8')
        invalid_errors, _, _ = kb.kb_check_claims(docs)
        rejects_direct = any('derived_from' in e for e in invalid_errors)
        p3 = valid_chain and rejects_direct
        print('P3: note-backed DERIVED accepted; direct ADR without metadata rejected:', p3)
        failures.append(p3 != (not flip))
        print('Assertions failed:', sum(failures))
        return int(any(failures))


if __name__ == '__main__':
    sys.exit(main())
