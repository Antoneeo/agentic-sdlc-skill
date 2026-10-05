import json
import runpy
import hashlib
from datetime import datetime, timezone
from pathlib import Path

project = Path(__file__).resolve().parents[3]
attempt = runpy.run_path(str(project / 'inputs/retry.py'))['attempt']
identity = runpy.run_path(str(project / 'inputs/card_identity.py'))['identity']
config = json.loads((project / 'inputs/retry-config.json').read_text())
results = []
def check(name, actual, expected):
    assert actual == expected, (name, actual, expected)
    results.append({'check': name, 'actual': actual, 'expected': expected, 'status': 'PASS'})

def run(values, settings):
    calls = []
    iterator = iter(values)
    def operation():
        calls.append(len(calls) + 1)
        return next(iterator)
    return attempt(operation, settings), len(calls)

check('config corrente', config, {'attempts': 1})
check('due falsi poi vero con config corrente', run([False, False, True], config), (False, 1))
check('fixture storica esplicita a tre tentativi', run([False, False, True], {'attempts': 3}), (True, 3))
check('arresto al primo successo', run([True], config), (True, 1))
check('esaurimento tentativi corrente', run([False] * 5, config), (False, 1))
check('zero tentativi', run([], {'attempts': 0}), (False, 0))
card = {'original_id': 'A', 'current_id': 'B'}
check('identita originale', identity(card), 'A')
try:
    identity({'current_id': 'B'})
except KeyError as exc:
    check('original_id mancante', str(exc), "'original_id'")
else:
    raise AssertionError('KeyError non propagato')
def fail_operation():
    raise RuntimeError('local fixture')
try:
    attempt(fail_operation, config)
except RuntimeError as exc:
    check('eccezione propagata', str(exc), 'local fixture')
else:
    raise AssertionError('RuntimeError non propagato')
for name, actual, wrong in [
    ('vecchia config non piu corrente', config, {'attempts': 3}),
    ('controllo negativo tentativi', run([False] * 5, config), (False, 5)),
    ('controllo negativo identita', identity(card), 'B'),
]:
    try:
        assert actual == wrong
    except AssertionError:
        results.append({'check': name, 'status': 'EXPECTED_FAIL', 'actual': actual, 'negated_expectation': wrong})
    else:
        raise AssertionError('Il controllo negativo non fallisce')
sources = ['inputs/retry.py', 'inputs/retry-config.json', 'inputs/card_identity.py']
print(json.dumps({
    'observed_at': datetime.now(timezone.utc).isoformat(),
    'scope': 'fixture locali, nessun servizio esterno, nessun click card',
    'sources': {path: hashlib.sha256((project / path).read_bytes()).hexdigest() for path in sources},
    'results': results,
}, ensure_ascii=False, indent=2))
