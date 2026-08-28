#!/usr/bin/env node

const fs = require('fs');
const { CLIENTS, skillTarget, removeGlobalOrientHooks } = require('./lib');

function removeSkill(client) {
  const target = skillTarget(client);
  if (!fs.existsSync(target)) return;
  try {
    fs.rmSync(target, { recursive: true, force: true });
    console.log(`🧹 Removed ${client.label} skill at: ${target}`);
  } catch (err) {
    console.log(`⚠️  Could not remove ${target}: ${err.message}`);
  }
}

// F-042: BEFORE the skill dirs go, remove the global orientation hooks that
// name them — otherwise every future session carries a hook whose validator no
// longer exists, the wired-and-DEAD state the check note calls the worst of
// the three. Surgical (only entries attributable to the removed dirs; the
// marker's opt-out lines survive when nothing was removed) and fail-open (an
// uninstall must never abort on a settings file).
try {
  const removedFrom = removeGlobalOrientHooks(CLIENTS.map(skillTarget));
  for (const target of removedFrom) {
    console.log(`🧹 Removed the session-orientation hook entry (${target}).`);
  }
} catch (e) { /* never abort an uninstall for a convenience */ }

CLIENTS.forEach(removeSkill);
