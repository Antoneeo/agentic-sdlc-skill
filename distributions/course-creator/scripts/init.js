#!/usr/bin/env node
"use strict";
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
const { SKILL_SOURCE, INSTALLED_SKILL_NAME, SELF_LENS, SIBLING_LENSES,
  CLIENTS, clientDetected, skillTarget, wireOrientHook, detectPython } = require('./lib');

const root = process.cwd();
const seed = new Map([
  ['ai_docs/README.md', `---\ndefault_domain: course\n---\n# Project knowledge and course work\n\nRead vision/project_vision.md, INDEX.md and reference/INDEX.md first.\n`],
  ['ai_docs/vision/project_vision.md', `---\ndescription: Project benefit and boundaries.\nstatus: DRAFT\n---\n# Project Vision\nStatus: DRAFT\n\n## Expected Benefit\n<Discuss with the owner.>\n`],
  ['ai_docs/vision/roadmap.md', `---\ndescription: Project learning and delivery roadmap.\nstatus: DRAFT\n---\n# Roadmap\nStatus: DRAFT\n`],
  ['ai_docs/vision/principles.md', `---\ndescription: Decisions that constrain project work.\nstatus: DRAFT\n---\n# Principles\nStatus: DRAFT\n`],
  ['ai_docs/strategic/architecture.md', `---\ndescription: Verified component inventory.\nstatus: CURRENT\n---\n# Architecture\n\n## Component Map\n| Component | Capability it owns | Contract | Where |\n|---|---|---|---|\n\n## Architectural Patterns\n<Add only verified patterns.>\n`],
  ['ai_docs/strategic/existing_features.md', `---\ndescription: Existing capabilities verified in this project.\nstatus: CURRENT\n---\n# Existing Features\n`],
  ['ai_docs/audit/audit_plan.md', `# Audit Plan\n\n| Area | State | Reference | Notes |\n|---|---|---|---|\n| . | PENDING | - | Initial analysis |\n`],
]);
function writeIfAbsent(rel, content) {
  const dest = path.join(root, rel);
  if (fs.existsSync(dest)) return false;
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, content, 'utf8');
  console.log(`Created ${rel}`);
  return true;
}
for (const [rel, content] of seed) writeIfAbsent(rel, content);
for (const dir of ['ai_docs/vision/features', 'ai_docs/reference', 'ai_docs/solutions/courses',
  'ai_docs/audit/reviews']) fs.mkdirSync(path.join(root, dir), { recursive: true });

const pointer = `# Course Creator project protocol\n\nUse the installed \`course-creator\` skill when the deliverable teaches a defined learner. It applies Agentic SDLC in Standalone mode: triage, project and course Vision, ANALYSIS, progressive explanations, sourced facts, independent diagnostic testing and a truthful efficacy label. Course files live in \`ai_docs/solutions/courses/<slug>/\`. Read \`ai_docs/README.md\` and the skill before working.\n\nInstall if missing: \`npm i -g @antoneeo/course-creator@beta && course-creator-install-skill\`.\n`;
const pointers = { claude: 'CLAUDE.md', gemini: 'GEMINI.md', codex: 'AGENTS.md',
  antigravity: 'AGENTS.md' };
const detected = CLIENTS.filter(clientDetected);
for (const client of detected) writeIfAbsent(pointers[client.key], pointer);
writeIfAbsent('.cursorrules', pointer);
const siblings = new Map();
for (const client of detected) {
  const parent = path.dirname(skillTarget(client));
  for (const [name, lens] of Object.entries(SIBLING_LENSES)) {
    if (fs.existsSync(path.join(parent, name))) siblings.set(name, lens);
  }
}
if (siblings.size) {
  const rows = [`- \`${INSTALLED_SKILL_NAME}\` — the **${SELF_LENS}** lens`,
    ...[...siblings].map(([name, lens]) => `- \`${name}\` — the **${lens}** lens`)];
  writeIfAbsent('AGENTIC_MULTI_LENS.md',
    `# Agentic SDLC family routing\n\nRead \`routing.md\` to choose the owner of each deliverable; \`memory.md\` is shared.\n\n${rows.join('\n')}\n`);
}
const python = detectPython();
for (const client of detected.filter(c => c.key === 'claude')) {
  const result = wireOrientHook({ cwd: root, client, python, docsLabel: 'ai_docs' });
  console.log(`Claude SessionStart orientation: ${result.code}`);
}
if (python) {
  try {
    execFileSync(python, [path.join(SKILL_SOURCE, 'scripts/sdlc_check.py'),
      'index', '--root', root], { stdio: 'ignore' });
    console.log('Generated ai_docs indexes.');
  } catch (e) { console.log('Run sdlc_check.py index when Python is available.'); }
}
console.log('Course Creator initialization complete.');
