"""Replay synthetic Claude/Codex event shapes through the CURRENT validator.

No settings or private transcript data are copied. Codex message shape was
observed by inspecting keys/types only in Codex desktop 0.166.0-alpha.6.
"""
import json
import os
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

repo = Path(sys.argv[1]).resolve()
sys.path.insert(0, str(repo / 'skills/agentic-sdlc-skill/scripts'))
import sdlc_core as core

with tempfile.TemporaryDirectory(prefix='sdlc-codex-events-') as temp:
    root = Path(temp)
    ref = root / 'ai_docs/reference'
    ref.mkdir(parents=True)
    (ref / 'GUIDE_probe.md').write_text('---\ndescription: probe\nstatus: CURRENT\n---\n# G\n',encoding='utf-8')
    (root / 'src').mkdir()
    target = root / 'src/a.py'
    transcript = root / 'transcript.jsonl'
    base = {'tool_name':'Edit','tool_input':{'file_path':str(target)},
            'cwd':str(root),'transcript_path':str(transcript),'hook_event_name':'PreToolUse'}
    claude = {'type':'assistant','message':{'role':'assistant','content':[{'type':'text','text':'Working.'}]}}
    codex = {'type':'response_item','payload':{'type':'message','role':'assistant',
             'content':[{'type':'output_text','text':'Working.'}]}}
    transcript.write_text(json.dumps(claude)+'\n',encoding='utf-8')
    control = core.verdict_reason(base,root=root)
    assert control and 'No guide-router verdict' in control
    patch_event = {**base,'tool_name':'apply_patch','tool_input':{'command':
        '*** Begin Patch\n*** Update File: src/a.py\n@@\n-a\n+b\n*** End Patch'}}
    assert core.verdict_reason(patch_event,root=root) is None
    transcript.write_text(json.dumps(codex)+'\n',encoding='utf-8')
    facts = core.transcript_facts(str(transcript))
    assert facts['assistant'] == 0
    assert core.verdict_reason(base,root=root) is None
    assert core.transcript_work(str(transcript))['assistant'] == 0
    print(json.dumps({'probe':'verdict','claude_control':'denied','codex_patch':'silent',
                      'codex_transcript_assistant_entries':facts['assistant'],'parity_invariant':'RED'}))

    codexhome = root/'codexhome'
    codexhome.mkdir()
    entry = str(repo/'skills/agentic-sdlc-skill/scripts/sdlc_check.py')
    (codexhome/'hooks.json').write_text(json.dumps({'hooks':{'SessionStart':[{'hooks':[
        {'type':'command','command':f'python "{entry}" orient'}]}]}}),encoding='utf-8')
    with patch.dict(os.environ,{'CODEX_HOME':str(codexhome),
                              'AGENTIC_SDLC_USER_SETTINGS':str(root/'missing-claude-settings.json')}):
        state = core.orient_hook_state(root)
    assert state == 'unwired'
    print(json.dumps({'probe':'orient_detection','codex_user_hook_exists':True,
                      'detected_state':state,'parity_invariant':'RED'}))
    if '--assert-parity' in sys.argv:
        assert facts['assistant'] > 0, 'Codex transcript not understood'
