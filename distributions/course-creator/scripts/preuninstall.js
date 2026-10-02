#!/usr/bin/env node
"use strict";
const { CLIENTS, skillTarget, ownedMarker, uninstallOwned,
  removeGlobalOrientHooks } = require('./lib');

const ownedTargets = CLIENTS.map(skillTarget).filter(ownedMarker);
try { removeGlobalOrientHooks(ownedTargets); } catch (e) { /* convenience only */ }
for (const target of ownedTargets) {
  const result = uninstallOwned(target);
  console.log(`${result.code}: ${target} (${result.removed} owned files removed; ` +
    `${result.preserved} retained)`);
}
