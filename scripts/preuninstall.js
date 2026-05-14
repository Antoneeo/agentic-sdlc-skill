#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const CLAUDE_HOME = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const CLAUDE_SKILL_TARGET = path.join(CLAUDE_HOME, 'skills', 'agentic-sdlc');
const CODEX_HOME = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
const CODEX_SKILL_TARGET = path.join(CODEX_HOME, 'skills', 'agentic-sdlc');

function removeSkill(target, label) {
  if (!fs.existsSync(target)) return;
  try {
    fs.rmSync(target, { recursive: true, force: true });
    console.log(`🧹 Removed ${label} skill at: ${target}`);
  } catch (err) {
    console.log(`⚠️  Could not remove ${target}: ${err.message}`);
  }
}

removeSkill(CLAUDE_SKILL_TARGET, 'Claude Code');
removeSkill(CODEX_SKILL_TARGET, 'Codex');
