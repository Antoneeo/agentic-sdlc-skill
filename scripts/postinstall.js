#!/usr/bin/env node

const fs = require('fs');
const {
  SKILL_SOURCE, CLIENTS, clientDetected, skillTarget, copyRecursive,
  wireGlobalOrientHook, detectPython,
} = require('./lib');

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
    const installed = installSkill(client);
    // F-042: wire the machine-global orientation hook — the install IS the
    // consent, so no question is ever asked. Claude Code only (the one client
    // whose hook shape a fixture pins); removal is a standing opt-out the
    // marker remembers. A convenience must never fail an npm install: wrapped.
    if (client.key === 'claude' && installed) {
      try {
        const r = wireGlobalOrientHook({ client, python: detectPython() });
        if (r.code === 'wired') {
          console.log('🔗 Session orientation wired for every project on this machine');
          console.log(`   (${r.target}).`);
          console.log('   Agents now start oriented on any project with a docs root; projects');
          console.log('   without one see nothing. To opt out, remove that hook entry — it');
          console.log('   will not be re-added.');
        } else if (r.code === 'broken') {
          console.log('⚠️  A session-orientation hook exists but the validator it names does');
          console.log('   not resolve, so it has been emitting nothing. Correct its command to:');
          console.log(`     ${r.command}`);
        } else if (r.code === 'no-python') {
          console.log('ℹ️  Python not found: session orientation not wired (wire it later per');
          console.log('   ENFORCEMENT.md §4).');
        } else if (r.code === 'malformed' || r.code === 'write-failed'
                   || r.code === 'unsafe-path') {
          console.log(`⚠️  Session orientation not wired (${r.code}). Wire it by hand per`);
          console.log('   ENFORCEMENT.md §4.');
        }
        // already / opted-out / unverifiable / no-validator: silent — an
        // install must not nag (the opt-out is the user's standing choice).
      } catch (e) { /* never fail the install for a convenience */ }
    }
  }
}

if (!detected) {
  console.log('ℹ️  No specific AI CLI detected globally, but you can still use the skill.');
}

console.log('\nTo initialize a project with the SDLC protocol, run:');
console.log('👉 npx agentic-sdlc-init');
console.log('------------------------------------\n');
