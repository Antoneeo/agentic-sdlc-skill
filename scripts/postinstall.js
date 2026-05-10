#!/usr/bin/env node

const { execSync } = require('child_process');

function checkCommand(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

console.log('\n--- Agentic SDLC Skill Discovery ---');

const agents = [
  { name: 'Claude Code', cmd: 'claude' },
  { name: 'Gemini CLI', cmd: 'gemini' },
  { name: 'Codex AI', cmd: 'codex' }
];

let detected = false;
agents.forEach(agent => {
  if (checkCommand(agent.cmd)) {
    console.log(`✅ Detected: ${agent.name}`);
    detected = true;
  }
});

if (!detected) {
  console.log('ℹ️  No specific AI CLI detected globally, but you can still use the skill.');
}

console.log('\nTo initialize a project with the SDLC protocol, run:');
console.log('👉 npx agentic-sdlc-init');
console.log('------------------------------------\n');
