// Baseline experiment only. Actual shipped files, isolated user homes, no real settings.
const fs = require('fs');
const os = require('os');
const path = require('path');
const assert = require('assert/strict');
const {execFileSync} = require('child_process');
const repo = path.resolve(process.argv[2]);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'sdlc-codex-hooks-probe-'));
const pkg = path.join(tmp, 'package');
const home = path.join(tmp, 'home');
try {
  const manifest = JSON.parse(fs.readFileSync(path.join(repo, 'package.json')));
  for (const rel of ['package.json', ...manifest.files]) {
    const from = path.join(repo, rel);
    if (!fs.existsSync(from)) continue;
    fs.mkdirSync(path.dirname(path.join(pkg, rel)), {recursive:true});
    fs.cpSync(from, path.join(pkg, rel), {recursive:true});
  }
  const env = {...process.env, HOME:home, USERPROFILE:home,
    CLAUDE_CONFIG_DIR:path.join(home,'.claude'), CODEX_HOME:path.join(home,'.codex'),
    GEMINI_HOME:path.join(home,'.gemini'), ANTIGRAVITY_HOME:path.join(home,'.antigravity'),
    AGENTIC_SDLC_KB_ROOT:path.join(home,'.agentic-sdlc')};
  const output = execFileSync(process.execPath,[path.join(pkg,'scripts/postinstall.js')],{env,encoding:'utf8'});
  const claude = JSON.parse(fs.readFileSync(path.join(env.CLAUDE_CONFIG_DIR,'settings.json')));
  const count = Object.values(claude.hooks).flatMap(g=>g.flatMap(x=>x.hooks)).length;
  assert.equal(count,4); // positive control: Python and wiring work in this sandbox
  const installed = fs.existsSync(path.join(env.CODEX_HOME,'skills','agentic-sdlc','SKILL.md'));
  const configured = fs.existsSync(path.join(env.CODEX_HOME,'hooks.json'));
  assert(installed);
  assert.equal(configured,false);
  console.log(JSON.stringify({probe:'npm_postinstall',codex_skill_installed:installed,
    codex_hooks_configured:configured,claude_hook_handlers:count,
    parity_invariant:'RED',detected_codex:output.includes('Detected: Codex AI')}));
  if (process.argv.includes('--assert-parity')) assert(configured,'Codex hooks missing after install');
} finally {
  const rel = path.relative(os.tmpdir(),tmp);
  if (!rel.startsWith('sdlc-codex-hooks-probe-') || rel.includes(path.sep)) throw Error('Unsafe cleanup');
  fs.rmSync(tmp,{recursive:true,force:true});
}
