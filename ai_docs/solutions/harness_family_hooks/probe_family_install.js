#!/usr/bin/env node
// Probe (F-092): what each lens's postinstall wires at user level when the family
// is installed in sequence, and when kb-agentic is installed alone. Runs every
// postinstall as a child process in a throwaway HOME; touches nothing real.
// Usage: node ai_docs/solutions/harness_family_hooks/probe_family_install.js
const fs = require('fs'), os = require('os'), path = require('path');
const { execFileSync } = require('child_process');
const repo = path.resolve(__dirname, '..', '..', '..');
const LENSES = {
  'agentic-sdlc': path.join(repo, 'scripts', 'postinstall.js'),
  'kb-agentic': path.join(repo, 'distributions', 'kb-agentic-skill', 'scripts', 'postinstall.js'),
  'mkt-agentic-sdlc': path.join(repo, 'distributions', 'mkt-agentic-sdlc', 'scripts', 'postinstall.js'),
  'course-creator': path.join(repo, 'distributions', 'course-creator', 'scripts', 'postinstall.js'),
};
function run(order) {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'f092-'));
  try {
    fs.mkdirSync(path.join(home, '.claude', 'skills'), { recursive: true });
    const env = { ...process.env, HOME: home, USERPROFILE: home, AGENTIC_SDLC_KB_ROOT: path.join(home, 'kbroot') };
    for (const k of ['CLAUDE_CONFIG_DIR', 'GEMINI_HOME', 'CODEX_HOME', 'ANTIGRAVITY_HOME', 'AGENTIC_SDLC_SKILLS_DIRS']) delete env[k];
    for (const lens of order) execFileSync(process.execPath, [LENSES[lens]], { env, stdio: 'ignore' });
    const p = path.join(home, '.claude', 'settings.json');
    const hooks = fs.existsSync(p) ? (JSON.parse(fs.readFileSync(p, 'utf8')).hooks || {}) : {};
    const wired = {};
    for (const [event, groups] of Object.entries(hooks)) for (const g of groups) for (const h of (g.hooks || [g])) {
      const m = /[\\/]([^\\/"]+)[\\/]scripts[\\/][a-z_]+\.py"?\s+(\S+)/.exec(h.command || '');
      if (m) (wired[event + ' ' + m[2]] = wired[event + ' ' + m[2]] || []).push(m[1]);
    }
    const kb = path.join(home, 'kbroot');
    const markers = fs.existsSync(kb) ? fs.readdirSync(kb).sort() : [];
    return { order, wired, markers };
  } finally { fs.rmSync(home, { recursive: true, force: true }); }
}
const out = [run(['agentic-sdlc', 'kb-agentic', 'mkt-agentic-sdlc', 'course-creator']),
             run(['kb-agentic', 'agentic-sdlc']),
             run(['kb-agentic']), run(['mkt-agentic-sdlc'])];
console.log(JSON.stringify(out, null, 2));
