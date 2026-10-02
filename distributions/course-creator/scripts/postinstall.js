#!/usr/bin/env node
"use strict";
const { CLIENTS, clientDetected, skillTarget, installOwned,
  wireGlobalOrientHook, detectPython } = require('./lib');

for (const client of CLIENTS) {
  if (!clientDetected(client)) continue;
  const target = skillTarget(client);
  const result = installOwned(target);
  console.log(`${client.label}: ${result.code} (${target})`);
  if (client.key === 'claude' && result.code === 'installed') {
    try { wireGlobalOrientHook({ client, python: detectPython() }); }
    catch (e) { console.log('Session orientation can be wired from ENFORCEMENT.md.'); }
  }
}
console.log('Initialize a project with course-creator-init.');
