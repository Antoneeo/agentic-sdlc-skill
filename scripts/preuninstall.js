#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const os = require('os');

const CLAUDE_SKILL_TARGET = path.join(os.homedir(), '.claude', 'skills', 'agentic-sdlc');

if (fs.existsSync(CLAUDE_SKILL_TARGET)) {
  try {
    fs.rmSync(CLAUDE_SKILL_TARGET, { recursive: true, force: true });
    console.log(`🧹 Removed Claude Code skill at: ${CLAUDE_SKILL_TARGET}`);
  } catch (err) {
    console.log(`⚠️  Could not remove ${CLAUDE_SKILL_TARGET}: ${err.message}`);
  }
}
