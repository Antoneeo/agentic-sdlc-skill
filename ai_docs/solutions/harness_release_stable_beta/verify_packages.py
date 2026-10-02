"""Package allowlists and fresh initialization, without installing into user homes."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

REPO = Path(__file__).resolve().parents[3]
PACKAGES = [('.', 'agentic-sdlc-skill', 'sdlc_check.py'),
            ('distributions/kb-agentic-skill', 'kb-agentic-skill', 'sdlc_check.py'),
            ('distributions/mkt-agentic-sdlc', 'mkt-agentic-sdlc', 'mkt_check.py'),
            ('distributions/course-creator', 'course-creator', 'sdlc_check.py')]
records = []
for relative, skill, validator in PACKAGES:
    package = REPO / relative
    manifest = json.loads((package / 'package.json').read_text())
    with tempfile.TemporaryDirectory(prefix='release-package-') as temp:
        base = Path(temp)
        env = os.environ.copy()
        for key in ('CLAUDE_CONFIG_DIR', 'GEMINI_HOME', 'CODEX_HOME',
                    'ANTIGRAVITY_HOME', 'AGENTIC_SDLC_KB_ROOT'):
            env.pop(key, None)
        env['npm_config_cache'] = str(base / 'cache')
        packed = subprocess.run(['cmd', '/d', '/c', 'npm pack --dry-run --json'],
            cwd=package, env=env, capture_output=True, text=True, timeout=60)
        assert packed.returncode == 0, packed.stderr
        info = json.loads(packed.stdout)[0]
        paths = {item['path'] for item in info['files']}
        expected = set(manifest['files'])
        assert not expected - paths, expected - paths
        assert not [p for p in paths if any(part in p for part in
            ('test_', '__pycache__', 'evals/', 'ai_docs/', 'presentations/'))]
        frontmatter = (package/'skills'/skill/'SKILL.md').read_text().split('---')[1]
        assert 'version: '+manifest['version'] in frontmatter
        assert json.loads((package/'gemini-extension.json').read_text())['version'] == manifest['version']
        project = base / 'project'
        project.mkdir()
        home = base / 'home'
        home.mkdir()
        script = "require('os').homedir=()=>"+json.dumps(str(home))+";require("+json.dumps(str(package/'scripts/init.js'))+");"
        initialized = subprocess.run(['node', '-e', script], cwd=project, env=env,
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
        assert initialized.returncode == 0, initialized.stderr
        checked = subprocess.run(['python', str(package/'skills'/skill/'scripts'/validator),
            'check', '--root', str(project)], cwd=project, env=env,
            capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=60)
        assert checked.returncode == 0, checked.stdout+checked.stderr
        records.append({'package':manifest['name'], 'version':manifest['version'],
                        'files':len(paths), 'pack_rc':packed.returncode,
                        'init_rc':initialized.returncode, 'scratch_check_rc':checked.returncode})
print(json.dumps(records, indent=2))
