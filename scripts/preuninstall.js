#!/usr/bin/env node

const fs = require('fs');
const {
  CLIENTS, skillTarget, removeGlobalOrientHooks, removeGlobalCommandHooks,
} = require('./lib');

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

// F-076: the per-turn reminder and the guide-verdict check name the same skill
// dirs; left behind they exit 2 (Python cannot open the file), which blocks the
// prompt or the edit. The verdict entry is also wired `; exit 0`, because npm 7+
// may not run this script at all.
const COMMAND_HOOK_NAMES = {
  UserPromptSubmit: 'per-turn reminder',
  PreToolUse: 'guide-verdict check',
};
try {
  for (const { target, event } of removeGlobalCommandHooks(CLIENTS.map(skillTarget))) {
    console.log(`🧹 Removed the ${COMMAND_HOOK_NAMES[event] || event} hook entry (${target}).`);
  }
} catch (e) { /* never abort an uninstall for a convenience */ }

CLIENTS.forEach(removeSkill);
