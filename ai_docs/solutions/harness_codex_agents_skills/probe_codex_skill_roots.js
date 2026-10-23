#!/usr/bin/env node
// F-082 probe: where does a given Codex CLI load user skills from, and how does it
// treat the same skill name in two roots? Behavioural evidence for the ANALYSIS
// (Execute-Before-Specify), re-runnable on any machine.
//
//   node probe_codex_skill_roots.js <path-to-codex-binary>
//
// Each scenario runs `codex debug prompt-input` (renders the model-visible prompt
// locally, no model call) with a THROWAWAY CODEX_HOME. The `.agents/skills` root is
// NOT redirectable: on Windows, Codex 0.164.0 resolves it from the real user profile
// and ignores HOME/USERPROFILE (measured: a temp HOME hides the probe). So the probe
// skill for that root is written under the REAL home, as one uniquely named folder,
// and removed in `finally` together with any `.agents`/`skills` parent this script
// created. It counts how many times the probe skill appears in the rendered skills
// list and compares with the expected count.
//
// Scenario S0 is the RED control: no probe skill is placed, so the expected count is
// 0 -- run with --negate to flip every expectation and watch every scenario fail,
// which shows the counter can fail.
//
// Requires a Codex that has `debug prompt-input` (0.164.0 has it; 0.112.0 does not).
// No auth is needed. `service_tier` is overridden because some real configs carry a
// value newer CLIs reject; the throwaway config is empty anyway.

const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');

const codex = process.argv[2];
const negate = process.argv.includes('--negate');
if (!codex) {
  console.error('usage: node probe_codex_skill_roots.js <codex-binary> [--negate]');
  process.exit(2);
}

const NAME = 'zz-f075-probe';
const REAL_HOME = os.homedir();
const AGENTS_SKILLS = path.join(REAL_HOME, '.agents', 'skills');
if (fs.existsSync(path.join(AGENTS_SKILLS, NAME))) {
  console.error(`refusing to run: ${path.join(AGENTS_SKILLS, NAME)} already exists`);
  process.exit(2);
}
// Parents this run creates, removed at the end only if this run created them.
const createdParents = [path.join(REAL_HOME, '.agents'), AGENTS_SKILLS]
  .filter((d) => !fs.existsSync(d));

function writeSkill(dir, note) {
  fs.mkdirSync(dir, { recursive: true });
  // No BOM: Codex 0.164.0 silently skips a SKILL.md whose frontmatter starts with one.
  fs.writeFileSync(path.join(dir, 'SKILL.md'),
    `---\nname: ${NAME}\ndescription: F-082 probe (${note}). Never use.\n---\n# probe\n`);
}

function link(target, at) {
  fs.mkdirSync(path.dirname(at), { recursive: true });
  fs.symlinkSync(target, at, process.platform === 'win32' ? 'junction' : 'dir');
}

const SCENARIOS = [
  { id: 'S0', what: 'control: no probe skill anywhere', expect: 0, place() {} },
  { id: 'S1', what: '$HOME/.agents/skills only', expect: 1,
    place() { writeSkill(path.join(AGENTS_SKILLS, NAME), 'agents'); } },
  { id: 'S2', what: '$CODEX_HOME/skills only (legacy target)', expect: 1,
    place(h) { writeSkill(path.join(h, '.codex', 'skills', NAME), 'codex-home'); } },
  { id: 'S3', what: 'real copies in both roots (upgrade without cleanup)', expect: 2,
    place(h) {
      writeSkill(path.join(AGENTS_SKILLS, NAME), 'agents');
      writeSkill(path.join(h, '.codex', 'skills', NAME), 'codex-home');
    } },
  { id: 'S4', what: 'real copy in .agents, legacy path is a link to it', expect: 1,
    place(h) {
      const real = path.join(AGENTS_SKILLS, NAME);
      writeSkill(real, 'agents');
      link(real, path.join(h, '.codex', 'skills', NAME));
    } },
  // S5 separates "deduplicated by real path" from "link not followed" (S4 alone gives
  // listed=1 either way): the only copy is a real folder OUTSIDE every skills root,
  // reached through a link at the legacy path. Listed once only if links are followed.
  { id: 'S5', what: 'legacy path is the only entry, a link to a folder outside all roots', expect: 1,
    place(h) {
      const real = path.join(h, 'outside', NAME);
      writeSkill(real, 'outside');
      link(real, path.join(h, '.codex', 'skills', NAME));
    } },
  // S6: a dangling legacy link (what an uninstall that removed only the real copy
  // leaves behind) must not break skill loading: listed 0, exit code 0.
  { id: 'S6', what: 'legacy path is a dangling link', expect: 0,
    place(h) {
      const real = path.join(h, 'gone', NAME);
      writeSkill(real, 'gone');
      link(real, path.join(h, '.codex', 'skills', NAME));
      fs.rmSync(path.join(h, 'gone'), { recursive: true, force: true });
    } },
];

let failed = 0;
for (const s of SCENARIOS) {
  const home = fs.mkdtempSync(path.join(os.tmpdir(), 'f075-home-'));
  const cwd = fs.mkdtempSync(path.join(os.tmpdir(), 'f075-cwd-'));
  try {
    fs.mkdirSync(path.join(home, '.codex'), { recursive: true });
    s.place(home);
    const env = { ...process.env, CODEX_HOME: path.join(home, '.codex') };
    const r = spawnSync(process.platform === 'win32' ? `"${codex}"` : codex, ['debug', 'prompt-input', '-c', 'service_tier="fast"', 'hi'],
      { cwd, env, encoding: 'utf8', shell: process.platform === 'win32', timeout: 120000 });
    if (r.status !== 0) {
      console.log(`${s.id} ERROR rc=${r.status}: ${(r.stderr || '').trim().slice(0, 200)}`);
      failed++;
      continue;
    }
    const count = (r.stdout.match(new RegExp(`${NAME}: `, 'g')) || []).length;
    const expect = negate ? (s.expect === 0 ? 1 : 0) : s.expect;
    const ok = count === expect;
    if (!ok) failed++;
    console.log(`${s.id} ${ok ? 'PASS' : 'FAIL'} listed=${count} expected=${expect} -- ${s.what}`);
  } finally {
    // Unlink the legacy link first, so removing the temp home never follows it.
    const legacy = path.join(home, '.codex', 'skills', NAME);
    try { if (fs.lstatSync(legacy).isSymbolicLink()) fs.unlinkSync(legacy); } catch (e) { /* absent */ }
    fs.rmSync(path.join(AGENTS_SKILLS, NAME), { recursive: true, force: true });
    fs.rmSync(home, { recursive: true, force: true });
    fs.rmSync(cwd, { recursive: true, force: true });
  }
}
for (const d of createdParents.reverse()) {
  try { fs.rmdirSync(d); } catch (e) { /* not empty or absent: leave it */ }
}
process.exit(failed ? 1 : 0);
