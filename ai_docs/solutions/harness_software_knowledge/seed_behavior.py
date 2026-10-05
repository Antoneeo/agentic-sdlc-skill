"""Freeze comparison inputs; four cases bundled per fresh session, no answer key."""
from pathlib import Path
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
OUT = HERE / 'behavior'
for variant in ('baseline', 'instructions', 'candidate'):
    dest = OUT / variant
    dest.mkdir(parents=True, exist_ok=False)
    skill = dest / 'skill'
    skill.mkdir()
    prefix = 'skills/agentic-sdlc-skill/'
    files = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', '2d5a5c67402487200fe5df3929d0b093fad6e761', '--', prefix], cwd=ROOT, text=True).splitlines()
    for rel in files:
        suffix = rel[len(prefix):]
        if suffix.startswith('evals/') or '/test_' in suffix:
            continue
        target = skill / suffix
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(subprocess.check_output(['git', 'show', '2d5a5c67402487200fe5df3929d0b093fad6e761:' + rel], cwd=ROOT))
    project = dest / 'project'
    inputs = project / 'inputs'
    inputs.mkdir(parents=True)
    for p in (HERE / 'eclosion').glob('*.md'):
        shutil.copyfile(p, inputs / p.name)
    (inputs / 'retry.py').write_text('def attempt(operation, config):\n    for i in range(config["attempts"]):\n        if operation():\n            return True\n    return False\n', encoding='utf-8')
    (inputs / 'retry-config.json').write_text('{"attempts": 3}\n', encoding='utf-8')
    (inputs / 'retry-test.txt').write_text('Fixture local: attempts=3, operation returns false twice then true. Result: PASS. No external service called.\n', encoding='utf-8')
    (inputs / 'retry-proposal.md').write_text('# Accepted design\nUse five attempts with exponential delays. Approved as design; implementation pending.\n', encoding='utf-8')
    (inputs / 'identity.py').write_text('def identity(card):\n    return card["original_id"]\n', encoding='utf-8')
    (inputs / 'identity-test.txt').write_text('Fixture {original_id: A, current_id: B}: identity returns A. Local PASS, not an end-to-end card click.\n', encoding='utf-8')
    (project / 'ai_docs').mkdir()
    (project / 'ai_docs/README.md').write_text('---\ndefault_domain: code\n---\n# Test project\nFour scoped cases: card continuity, retry configuration, proposed retry behavior, card identity.\n', encoding='utf-8')
    (dest / 'task1.txt').write_text('''Analizza i quattro casi in inputs: continuità della card Eclosion, tentativi e configurazione, proposta approvata, identità della card. Per ciascuno ricostruisci proprietà da preservare, comportamento osservabile e limiti delle prove. Conserva in ai_docs la comprensione utile al prossimo intervento. Nessuna modifica al software, nessun test esterno. Il tempo conta: evita lavoro estraneo ai quattro casi. Usa la skill allegata e i suoi supporti secondo i trigger. Non leggere le altre varianti o la rubrica di valutazione.\n''', encoding='utf-8')
    (dest / 'task2.txt').write_text('''Una nuova milestone deve usare le stesse proprietà. Ricostruisci dai documenti di progetto e dagli input correnti i quattro casi: si può considerare verificato il click completo Eclosion? Quanti tentativi usa oggi il runtime, e quali ritardi? La proposta approvata descrive il comportamento esistente? Quale identità preserva la card e quale prova rimane applicabile dopo i cambiamenti? Aggiorna la conoscenza pertinente, conservando fonti e limiti. Non leggere cronologia, task1 output, metriche o altre varianti. Non eseguire test esterni.\n''', encoding='utf-8')
    if variant == 'instructions':
        (skill / 'SOFTWARE_MEMORY_ADDENDUM.md').write_text('''During software analysis, capture reusable observations with sources in the existing project topic graph; distinguish observation, requirement, hypothesis and design in prose. Reconcile with existing knowledge instead of duplicating it. On changes manually re-open code/configuration/tests and mark affected knowledge for re-verification; unchanged snapshots do not prove live behavior. Keep proposal approval separate from observed implementation, preserve conditions and unknown coverage. Use existing KB formats; no new runtime or mandatory second workflow.\n''', encoding='utf-8')
    (dest / 'run.json').write_text(json.dumps({'variant': variant, 'baseline_commit': '2d5a5c67402487200fe5df3929d0b093fad6e761', 'cases': ['eclosion', 'api-config', 'approved-proposal', 'rename-delete'], 'session1': 'pending', 'session2': 'pending'}, indent=2), encoding='utf-8')
print(OUT)
