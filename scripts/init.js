#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');
const { SKILL_SOURCE, CLIENTS, clientDetected, loadTemplates, templateFor } = require('./lib');

const cwd = process.cwd();

// 1. Directory layout (canonical ai_docs structure, including reference/)
const directories = [
  'ai_docs',
  'ai_docs/vision',
  'ai_docs/vision/features',
  'ai_docs/reference',
  'ai_docs/strategic',
  'ai_docs/audit',
  'ai_docs/solutions',
].map((d) => path.join(cwd, d));

// 2. Project protocol (thin pointer — the operating contract is the skill).
const protocolContent = `# KB Agentic — Project Protocol (pointer)

This project follows the KB Agentic Knowledge-Base & Document-First process. The full
operating contract is the \`kb-agentic\` skill (installed in your agent's
skills directory); this file is only the minimal always-on pointer.

## Rule Zero — Triage every request
- L1 Quick Fact / Snippet: small edit in existing note/doc; no new docs.
- L2 Local Note / SOP Update: specific SOP update, local research note (1-2 files). Mini-analysis in reply.
- L3 Major Knowledge Unit / Corpus: >3 files, multi-part guide creation, corpus ingestion, or KB restructuring. Full workflow via skill: Vision Gate -> Spec Elicitation -> Taxonomy Pass -> Knowledge Analysis -> Distillation -> Review -> Indexing.
- Spike: time-boxed exploration; outcome in \`ai_docs/solutions/SPIKE_[topic].md\`.
- High-risk areas (personal data, credentials, authN/authZ, security specs) are never L1.
- When in doubt, pick the higher level. Declare the chosen level when starting.

## Where things live
- Vision (gate for L3): \`ai_docs/vision/\` — \`Status: DRAFT\` informs, \`Status: APPROVED\` binds.
- Knowledge analyses: \`ai_docs/solutions/ANALYSIS_[topic].md\` (frontmatter = topic state).
- Must-reads: \`ai_docs/README.md\`; full generated manifest: \`ai_docs/INDEX.md\`.
- If devPNT is available for this project, its M-VISION / plans / governed artifacts take over (Hybrid mode — see the skill).

## Closure gate
Docs travel in the same commit/PR as the text they describe. If the project
adopts the validator, \`python <skill_dir>/scripts/sdlc_check.py check\` must be
CLEAN before declaring work done.

If the kb-agentic skill is not available in this client, ask the user to install it:
\`npm i -g @antoneeo/kb-agentic-skill && kb-agentic-install-skill\`
`;

console.log('🚀 Initializing KB Agentic workflow...');

// 3. Load templates from the single source (skill's templates.md)
let sections;
try {
  sections = loadTemplates();
} catch (err) {
  console.error(`❌ Cannot load templates: ${err.message}`);
  process.exit(1);
}

function initialAuditPlan() {
  const tpl = templateFor(sections, 'audit_plan.md');
  const lines = tpl.split('\n');
  const sepIdx = lines.findIndex((l) => /^\|[-\s|:]+\|$/.test(l.trim()));
  if (sepIdx === -1) return tpl;
  return lines.slice(0, sepIdx + 1).join('\n') + '\n| . | PENDING | - | Initial analysis |\n';
}

let seedFiles;
try {
  seedFiles = [
    ['ai_docs/README.md', templateFor(sections, 'ai_docs/README.md')],
    ['ai_docs/vision/project_vision.md', templateFor(sections, 'project_vision.md')],
    ['ai_docs/vision/roadmap.md', templateFor(sections, 'vision/roadmap.md')],
    ['ai_docs/vision/principles.md', templateFor(sections, 'principles.md')],
    ['ai_docs/strategic/architecture.md', templateFor(sections, 'architecture.md and existing_features.md', 0)],
    ['ai_docs/strategic/existing_features.md', templateFor(sections, 'architecture.md and existing_features.md', 1)],
    ['ai_docs/audit/audit_plan.md', initialAuditPlan()],
  ];
} catch (err) {
  console.error(`❌ ${err.message}`);
  process.exit(1);
}

// 4. Create directories
directories.forEach((dir) => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`📁 Created directory: ${path.relative(cwd, dir)}`);
  }
});

// 5. Write seed files (never overwrite)
const writeIfNotExists = (relPath, content, description) => {
  const filePath = path.join(cwd, relPath);
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`📄 Created file: ${relPath}${description ? ` (${description})` : ''}`);
    return true;
  }
  console.log(`⏭️  Skipped: ${relPath} already exists.`);
  return false;
};

seedFiles.forEach(([relPath, content]) => writeIfNotExists(relPath, content));

// 6. Client discovery and protocol pointers
console.log('\n--- Environment Analysis ---');

const protocolFiles = {
  claude: 'CLAUDE.md',
  gemini: 'GEMINI.md',
  codex: 'AGENTS.md',
  antigravity: 'AGENTS.md',
};

for (const client of CLIENTS) {
  if (clientDetected(client)) {
    console.log(`✅ ${client.label} detected.`);
    writeIfNotExists(protocolFiles[client.key], protocolContent, `${client.label} protocol pointer`);
  }
}

// Cursor/Windsurf (always recommended)
writeIfNotExists('.cursorrules', protocolContent, 'Cursor/Windsurf rules');

// 7. Generate ai_docs/INDEX.md
const validator = path.join(SKILL_SOURCE, 'scripts', 'sdlc_check.py');
let indexed = false;
for (const py of ['python', 'python3', 'py']) {
  try {
    execSync(`${py} "${validator}" index --root "${cwd}"`, { stdio: 'ignore' });
    console.log('📇 Generated ai_docs/INDEX.md (document manifest).');
    indexed = true;
    break;
  } catch (e) { /* try next */ }
}
if (!indexed) {
  console.log('ℹ️  Python not found: generate the manifest later with '
    + '"python <skill_dir>/scripts/sdlc_check.py index" (validate reports it until then).');
}

console.log('\n✅ Setup completed successfully!');
console.log('💡 Next steps:');
console.log('   1. Make sure the kb-agentic skill is installed (kb-agentic-install-skill).');
console.log('   2. Restart/open the project in your AI client so it reads the protocol pointer.');
console.log('   3. Start with an audit following ai_docs/audit/audit_plan.md.');
