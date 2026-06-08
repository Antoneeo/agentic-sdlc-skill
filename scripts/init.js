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

You are a senior software engineer strictly following a "Documentation-First" and "Vision-Guided" process. NEVER implement code without completing the preceding documentation steps. Use your tools (file read/write, shell execution) to adhere to the following phases.

## 1. Audit and Alignment Phase
Before responding to any operational request:
- Check for the existence of the \`ai_docs/\` and \`ai_docs/vision/\` folders.
- If \`ai_docs/\` is missing or essential documents are absent, create them by analyzing the source code:
    1. \`ai_docs/vision/project_vision.md\`: North Star, target users, goals, non-goals, success signals.
    2. \`ai_docs/vision/roadmap.md\`: Milestones, expected benefits, priorities, success signals.
    3. \`ai_docs/vision/principles.md\`: Stable decision principles and strategic anti-patterns.
    4. \`ai_docs/strategic/architecture.md\`: Tech Stack, Directory Structure, Architecture Patterns.
    5. \`ai_docs/strategic/existing_features.md\`: List of current features.
    6. \`ai_docs/strategic/features_history.md\`: Feature history table (ID, Name, Status, Dates).
    7. \`ai_docs/audit/audit_plan.md\`: Codebase analysis plan in batches.
- Never treat architecture or feature history as a substitute for Vision.

## 2. Vision Gate
For every new feature request or significant behavior change:
- Read \`ai_docs/vision/project_vision.md\`, \`ai_docs/vision/roadmap.md\`, and \`ai_docs/vision/principles.md\`.
- If Vision documents are missing, empty, or ambiguous, create or update them before technical analysis.
- For significant features, create \`ai_docs/vision/features/VISION_[feature_name].md\` covering Problem, Expected Benefit, Users/Stakeholders, Success Signals, Non-Goals, and linked principles.
- If the request conflicts with Vision, stop and surface the conflict instead of implementing silently.

## 3. Request Analysis Phase
For every new feature request:
- Create \`ai_docs/solutions/ANALYSIS_[feature_name].md\` (Objective, Vision Alignment, Impact, Action Plan, Test Strategy).
- Add an entry in \`ai_docs/strategic/features_history.md\` with status \`[PLANNED]\`.

## 4. Development and Testing Phase
Only after Phases 2 and 3 are complete:
1. Update feature status to \`[IN_PROGRESS]\` in \`ai_docs/strategic/features_history.md\`.
2. Implement code surgically following the plan.
3. **Mandatory:** Write automated tests following the **AAA (Arrange, Act, Assert)** pattern.
4. Execute tests. If they fail, fix and re-run until Exit Code is 0.

## 5. Closing Phase
Upon feature completion:
- Verify the delivered result against \`ai_docs/vision/project_vision.md\` and the feature Vision document, including non-goals.
- Update \`ai_docs/strategic/architecture.md\` and \`ai_docs/strategic/existing_features.md\` if necessary.
- Update \`ai_docs/vision/\` documents if goals, non-goals, roadmap, expected benefits, or success signals changed.
- Update \`ai_docs/strategic/features_history.md\` setting status to \`[COMPLETED]\`.
`;

const projectVisionBoilerplate = `# Project Vision

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

| Milestone | Expected Benefit | Priority | Success Signal | Status |
|:---|:---|:---|:---|:---|
| M1 | - | - | - | [PLANNED] |
`;

const principlesBoilerplate = `# Vision Principles

## Principles
- TBD

## Strategic Anti-Patterns
- TBD
`;

const historyBoilerplate = `# Feature History

| ID | Feature Name | Status | Start Date | End Date | Analysis Doc | Notes |
|:---|:---|:---|:---|:---|:---|:---|
| 000 | Project Init | [COMPLETED] | - | - | - | Automatic initialization |
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
writeIfNotExists(files.auditPlan, '# Audit Plan\n\n| Directory/File | Status | Notes |\n|:---|:---|:---|\n| / | [PENDING] | Initial analysis |\n', 'Audit Plan');

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
