#!/usr/bin/env node

const fs = require('fs');
const { CLIENTS, skillTarget } = require('./lib');

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

CLIENTS.forEach(removeSkill);
