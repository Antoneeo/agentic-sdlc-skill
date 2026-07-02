#!/usr/bin/env node

const fs = require('fs');
const { SKILL_SOURCE, CLIENTS, clientDetected, skillTarget, copyRecursive } = require('./lib');

function installSkill(client) {
  if (!fs.existsSync(SKILL_SOURCE)) {
    console.log(`⚠️  Skill source not found at ${SKILL_SOURCE}; skipping ${client.label} install.`);
    return false;
  }
  const target = skillTarget(client);
  try {
    fs.mkdirSync(target, { recursive: true });
    copyRecursive(SKILL_SOURCE, target);
    console.log(`📦 Installed ${client.label} skill at: ${target}`);
    console.log(`   ${client.reload}`);
    return true;
  } catch (err) {
    console.log(`⚠️  Failed to install ${client.label} skill: ${err.message}`);
    console.log(`   Manual install: copy "${SKILL_SOURCE}" to "${target}".`);
    return false;
  }
}

console.log('\n--- Agentic SDLC Skill Discovery ---');

let detected = false;
for (const client of CLIENTS) {
  if (clientDetected(client)) {
    console.log(`✅ Detected: ${client.label}`);
    detected = true;
    installSkill(client);
  }
}

if (!detected) {
  console.log('ℹ️  No specific AI CLI detected globally, but you can still use the skill.');
}

console.log('\nTo initialize a project with the SDLC protocol, run:');
console.log('👉 npx agentic-sdlc-init');
console.log('------------------------------------\n');
