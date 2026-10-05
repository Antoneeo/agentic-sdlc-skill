from pathlib import Path
import json, hashlib
BASE = Path(__file__).resolve().parents[3]
INPUTS = BASE / 'inputs'
HERE = Path(__file__).resolve().parent

def load(path, name):
    scope = {}
    exec(compile(path.read_text(encoding='utf-8-sig'), str(path), 'exec'), scope)
    return scope[name]

def run_retry(fn, config, answers):
    calls = []
    values = iter(answers)
    def operation():
        value = next(values)
        calls.append(value)
        return value
    return {'result': fn(operation, config), 'calls': len(calls)}

attempt = load(INPUTS / 'retry.py', 'attempt')
identity = load(INPUTS / 'card_identity.py', 'identity')
config = json.loads((INPUTS / 'retry-config.json').read_text(encoding='utf-8-sig'))
current = run_retry(attempt, config, [False, False, True])
legacy_fixture = run_retry(attempt, {'attempts': 3}, [False, False, True])
immediate_success = run_retry(attempt, config, [True])
selected = identity({'original_id': 'A', 'current_id': 'B'})
negative_controls = []
for name, wrong in [('current_limit_three', current == {'result': True, 'calls': 3}), ('current_identity_B', selected == 'B')]:
    try:
        assert wrong, name
    except AssertionError:
        negative_controls.append({'assertion': name, 'result': 'EXPECTED_FAILURE'})
    else:
        raise AssertionError('negative control unexpectedly passed: ' + name)
assert config == {'attempts': 1}
assert current == {'result': False, 'calls': 1}
assert legacy_fixture == {'result': True, 'calls': 3}
assert immediate_success == {'result': True, 'calls': 1}
assert selected == 'A'
paths = ['retry.py', 'retry-config.json', 'retry-test.txt', 'retry-proposal.md', 'card_identity.py', 'TEST_m145_card_continuity.md', 'REVIEW_m145_card_trace_core.md']
result = {'scope': 'Local current inputs only; no external service or complete card click', 'inputs_sha256': {str(INPUTS / p): hashlib.sha256((INPUTS / p).read_bytes()).hexdigest() for p in paths}, 'current_config': config, 'current_false_false_true': current, 'old_three_attempt_fixture': legacy_fixture, 'immediate_success': immediate_success, 'identity': selected, 'negative_controls': negative_controls, 'limits': ['No latency/network/deployment proof', 'No consumer or rename integration enumeration', 'Eclosion reports read, not executed']}
(HERE / 'reverify_result.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, indent=2))
