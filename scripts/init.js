#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const cwd = process.cwd();

// Helper for command checking
function checkCommand(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

// 1. Path definitions
const directories = [
  path.join(cwd, 'ai_docs'),
  path.join(cwd, 'ai_docs', 'vision'),
  path.join(cwd, 'ai_docs', 'vision', 'features'),
  path.join(cwd, 'ai_docs', 'strategic'),
  path.join(cwd, 'ai_docs', 'audit'),
  path.join(cwd, 'ai_docs', 'solutions')
];

const files = {
  projectVision: path.join(cwd, 'ai_docs', 'vision', 'project_vision.md'),
  roadmap: path.join(cwd, 'ai_docs', 'vision', 'roadmap.md'),
  principles: path.join(cwd, 'ai_docs', 'vision', 'principles.md'),
  architecture: path.join(cwd, 'ai_docs', 'strategic', 'architecture.md'),
  existingFeatures: path.join(cwd, 'ai_docs', 'strategic', 'existing_features.md'),
  featuresHistory: path.join(cwd, 'ai_docs', 'strategic', 'features_history.md'),
  auditPlan: path.join(cwd, 'ai_docs', 'audit', 'audit_plan.md'),
  handoff: path.join(cwd, 'ai_docs', 'audit', 'handoff.md'),
  claudeConfig: path.join(cwd, 'CLAUDE.md'),
  geminiConfig: path.join(cwd, 'GEMINI.md'),
  codexAgents: path.join(cwd, 'AGENTS.md'),
  cursorRules: path.join(cwd, '.cursorrules')
};

// 2. Operational Protocol (System Prompt)
const protocolContent = `# "Agentic SDLC" Operational Protocol

You are a senior software engineer following a Documentation-First and Vision-Guided process. The process is proportional to risk: do not apply heavyweight governance to trivial work, but never bypass Vision, security, or design gates for significant changes.

## 0. Triage First
Classify every operational request:
- L1 Trivial: small local fix, no API/dependency/behavior expansion. Implement with relevant tests; no new docs.
- L2 Small: clear root cause, up to 3 files, low risk. Provide mini-analysis in the response; test.
- L3 Significant: public contract, user-visible behavior, security-sensitive area, new dependency, architectural impact, or more than 3 files. Use the full workflow below.
- Spike: time-boxed exploration; document result in \`ai_docs/solutions/SPIKE_[topic].md\`; production work must be reclassified.

Security-sensitive areas are never L1.

## 1. Mode Selection
- Standalone: if devPNT is unavailable, use \`ai_docs/\` as the complete source of truth.
- Hybrid/devPNT: if devPNT is available and configured for this project, use it for governed state. The devPNT M-VISION is the milestone north star, Master Plan is strategic roadmap, Action Plan is tactical execution, and governed artifacts live in devPNT.
- Do not create silent double truth. In Hybrid, \`ai_docs/\` is human-readable context, fallback, handoff, or shadow; devPNT governs plans and versioned artifacts.

## 2. Audit and Alignment
For L3 or explicit audit requests:
- Check \`ai_docs/\`, \`ai_docs/vision/\`, \`ai_docs/strategic/\`, \`ai_docs/audit/\`, and \`ai_docs/solutions/\`.
- If missing, create them by analyzing the codebase in batches.
- Never treat architecture or feature history as a substitute for Vision.

## 3. Vision Gate
Standalone:
- Read \`ai_docs/vision/project_vision.md\`, \`roadmap.md\`, and \`principles.md\`.
- Vision documents start as \`Stato: DRAFT\`; DRAFT informs but does not block an explicit user request.
- \`Stato: APPROVED\` is binding: surface conflicts before implementation.

Hybrid/devPNT:
- Read the active M-VISION before design or code.
- Verify the request advances a stated benefit or success signal.
- If request, local Vision, and M-VISION diverge, stop and surface the conflict.

## 4. Request Analysis
For L3 in Standalone:
- Create or update \`ai_docs/solutions/ANALYSIS_[feature].md\`.
- Include Objective, Feature Vision, Impact, Security and Threat Model, Action Plan, Test Strategy, and Diary/Current State.

For L3 in Hybrid:
- Restore Master Plan, Action Plan, and related devPNT artifacts.
- Use devPNT for D-UC, P-TM, E-ISP, E-TDD, E-TP, ADR, and plan updates.
- Use Markdown shadows only as readable mirrors, never as the authoritative source over devPNT.

## 5. Development and Testing
Only after the required gate for the triage level:
1. Implement surgically following the plan.
2. Write or update automated tests where possible, using AAA for unit tests.
3. Run tests/lint/smoke checks. If the environment cannot run them, document the alternative verification.
4. After 3 consecutive test runs without progress, stop and ask for guidance.

## 6. Closing
- Verify the result against local Vision or devPNT M-VISION.
- Update only documents actually impacted.
- In Hybrid, propose ADR/KL updates when architectural facts changed.
- Keep docs and code in the same commit/PR.
`;

const projectVisionBoilerplate = `# Project Vision
Stato: DRAFT

## North Star
- TBD

## Target Users
- TBD

## Goals
- TBD

## Non-Goals
- TBD

## Success Signals
- TBD
`;

const roadmapBoilerplate = `# Vision Roadmap
Stato: DRAFT

| Milestone | Expected Benefit | Priority | Success Signal | Status |
|:---|:---|:---|:---|:---|
| M1 | - | - | - | [PLANNED] |
`;

const principlesBoilerplate = `# Vision Principles
Stato: DRAFT

## Principles
- TBD

## Strategic Anti-Patterns
- TBD
`;

const historyBoilerplate = `<!-- GENERATED by agentic-sdlc - update manually only if the project does not use sdlc_check.py index. -->
# Feature History

| ID | Feature Name | Level | Status | Start Date | End Date | Analysis Doc |
|:---|:---|:---|:---|:---|:---|:---|
`;

console.log('🚀 Initializing Agentic SDLC workflow (Discovery Mode)...');

// 3. Directory creation
directories.forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
    console.log(`📁 Created directory: ${path.relative(cwd, dir)}`);
  }
});

// 4. Basic file writing
const writeIfNotExists = (filePath, content, description) => {
  if (!fs.existsSync(filePath)) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`📄 Created file: ${path.relative(cwd, filePath)} (${description})`);
    return true;
  } else {
    console.log(`⏭️  Skipped: ${path.relative(cwd, filePath)} already exists.`);
    return false;
  }
};

writeIfNotExists(files.projectVision, projectVisionBoilerplate, 'Project Vision Boilerplate');
writeIfNotExists(files.roadmap, roadmapBoilerplate, 'Vision Roadmap Boilerplate');
writeIfNotExists(files.principles, principlesBoilerplate, 'Vision Principles Boilerplate');
writeIfNotExists(files.architecture, '# Project Architecture\n\n- Stack:\n- Patterns:\n', 'Architecture Boilerplate');
writeIfNotExists(files.existingFeatures, '# Existing Features\n\n- \n', 'Features Boilerplate');
writeIfNotExists(files.featuresHistory, historyBoilerplate, 'History Table');
writeIfNotExists(files.auditPlan, '# Audit Plan\n\nStates: PENDING | ANALYZED | SKIPPED.\n\n| Percorso | Stato | Riferimento | Note |\n|---|---|---|---|\n| / | PENDING | - | Initial analysis |\n', 'Audit Plan');

// 5. Client Discovery and Configuration
console.log('\n--- Environment Analysis ---');

if (checkCommand('claude')) {
  console.log('✅ Claude Code detected.');
  writeIfNotExists(files.claudeConfig, protocolContent, 'Claude Configuration');
}

if (checkCommand('gemini')) {
  console.log('✅ Gemini CLI detected.');
  writeIfNotExists(files.geminiConfig, protocolContent, 'Gemini Configuration');
}

if (checkCommand('codex')) {
  console.log('✅ Codex AI detected.');
  writeIfNotExists(files.codexAgents, protocolContent, 'Codex AGENTS.md');
}

// Cursor/Windsurf (always recommended)
writeIfNotExists(files.cursorRules, protocolContent, 'Cursor/Windsurf Rules');

console.log('\n✅ Setup completed successfully!');
console.log('💡 Next steps:');
console.log('   1. If using Claude Code, start it: it will read CLAUDE.md.');
console.log('   2. If using Gemini CLI, commands will use GEMINI.md.');
console.log('   3. If using Codex, restart/open the project so it reads AGENTS.md.');
console.log('   4. Start analyzing the codebase following ai_docs/audit/audit_plan.md.');
