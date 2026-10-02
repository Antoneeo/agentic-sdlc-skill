"""Run the actual publisher against fake npm; no registry writes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

REPO = Path(__file__).resolve().parents[3]
PACKAGES = [('.', '1.37.0', 'latest'),
            ('distributions/kb-agentic-skill', '1.20.0', 'latest'),
            ('distributions/mkt-agentic-sdlc', '0.15.0', 'latest'),
            ('distributions/course-creator', '0.1.0-beta.1', 'beta')]

class PublisherTests(unittest.TestCase):
    def run_mock(self, mode):
        with tempfile.TemporaryDirectory(prefix='publisher-mock-') as temp:
            root = Path(temp)
            shutil.copyfile(REPO / 'publish_all.bat', root / 'publish_all.bat')
            for rel, version, channel in PACKAGES:
                target = root / rel
                target.mkdir(parents=True, exist_ok=True)
                (target / 'package.json').write_text(json.dumps({
                    'version': version, 'publishConfig': {'tag': channel} if channel=='beta' else {}}))
            fake = root / 'fake'
            fake.mkdir()
            (fake / 'npm.cmd').write_text('@echo off\r\n"' + os.sys.executable +
                '" "' + str(fake / 'npm.py') + '" %*\r\n', encoding='utf-8')
            (fake / 'npm.py').write_text('''import json, os, sys
from pathlib import Path
args=sys.argv[1:]; pkg=json.loads(Path('package.json').read_text())
with open(os.environ['MOCK_LOG'],'a') as log: log.write(json.dumps(args)+'\\n')
if args[:2]==['pkg','get']:
 print(json.dumps(pkg['version'] if args[2]=='version' else pkg['publishConfig'].get('tag', {})))
elif args[0]=='view':
 if args[2]=='version':
  if os.environ['MOCK_MODE']=='skip': print(pkg['version'])
  else: sys.exit(1)
 else: print('wrong' if os.environ['MOCK_MODE']=='verify-fail' else pkg['version'])
elif args[0]=='publish':
 sys.exit(1 if os.environ['MOCK_MODE']=='publish-fail' else 0)
elif args[:2]==['dist-tag','ls']:
 if os.environ['MOCK_MODE']=='tags-fail': sys.exit(1)
 if os.environ['MOCK_MODE']=='tags-empty': sys.exit(0)
 print('beta: '+pkg['version'])
 if os.environ['MOCK_MODE']=='beta-promoted': print('latest: '+pkg['version'])
''', encoding='utf-8')
            env = dict(os.environ, PATH=str(fake)+os.pathsep+os.environ['PATH'],
                       MOCK_LOG=str(root/'calls.jsonl'), MOCK_MODE=mode)
            result = subprocess.run(['cmd', '/d', '/c', str(root/'publish_all.bat')],
                input='y\n', cwd=root, env=env, capture_output=True, text=True,
                errors='replace', timeout=55)
            calls = [json.loads(line) for line in (root/'calls.jsonl').read_text().splitlines()]
            return result, calls

    def test_channels(self):
        result, calls = self.run_mock('publish')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertEqual([c for c in calls if c[0]=='publish'],
            [['publish','--tag','latest']]*3+[['publish','--tag','beta']])
        self.assertEqual([c[2] for c in calls if c[0]=='view' and c[2]!='version'],
                         ['dist-tags.latest']*3+['dist-tags.beta'])

    def test_skip_existing_version(self):
        result, calls = self.run_mock('skip')
        self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
        self.assertFalse(any(c[0]=='publish' for c in calls))
        self.assertTrue(all('@' in c[1][1:] for c in calls if c[0]=='view' and c[2]=='version'))

    def test_failed_publish_stops(self):
        result, calls = self.run_mock('publish-fail')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(sum(c[0]=='publish' for c in calls), 1)

    def test_failed_verify_does_not_report_success(self):
        result, _ = self.run_mock('verify-fail')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('All four published.', result.stdout)

    def test_beta_also_on_latest_is_rejected(self):
        result, _ = self.run_mock('beta-promoted')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('All four published.', result.stdout)

    def test_tag_query_failure_is_rejected(self):
        result, _ = self.run_mock('tags-fail')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('All four published.', result.stdout)

    def test_empty_tag_query_is_rejected(self):
        result, _ = self.run_mock('tags-empty')
        self.assertNotEqual(result.returncode, 0)
        self.assertNotIn('All four published.', result.stdout)

if __name__ == '__main__':
    unittest.main()
