#!/usr/bin/env node

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const PACKAGE_ROOT = path.resolve(__dirname, '..');
const SKILL_SOURCE = path.join(PACKAGE_ROOT, 'skills', 'agentic-sdlc-skill');
const CLAUDE_HOME = process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude');
const CLAUDE_SKILLS_DIR = path.join(CLAUDE_HOME, 'skills');
const CLAUDE_SKILL_TARGET = path.join(CLAUDE_SKILLS_DIR, 'agentic-sdlc');
const CODEX_HOME = process.env.CODEX_HOME || path.join(os.homedir(), '.codex');
const CODEX_SKILLS_DIR = path.join(CODEX_HOME, 'skills');
const CODEX_SKILL_TARGET = path.join(CODEX_SKILLS_DIR, 'agentic-sdlc');
const GEMINI_HOME = process.env.GEMINI_HOME || path.join(os.homedir(), '.gemini');
const GEMINI_SKILLS_DIR = path.join(GEMINI_HOME, 'skills');
const GEMINI_SKILL_TARGET = path.join(GEMINI_SKILLS_DIR, 'agentic-sdlc');

function checkCommand(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

function copyRecursive(src, dest) {
  if (typeof fs.cpSync === 'function') {
    fs.cpSync(src, dest, { recursive: true, force: true });
    return;
  }
  // Fallback for Node < 16.7
  if (!fs.existsSync(dest)) fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) copyRecursive(s, d);
    else fs.copyFileSync(s, d);
  }
}

function installClaudeSkill() {
  if (!fs.existsSync(SKILL_SOURCE)) {
    console.log(`⚠️  Skill source not found at ${SKILL_SOURCE}; skipping Claude Code install.`);
    return false;
  }
  try {
    fs.mkdirSync(CLAUDE_SKILLS_DIR, { recursive: true });
    copyRecursive(SKILL_SOURCE, CLAUDE_SKILL_TARGET);
    console.log(`📦 Installed Claude Code skill at: ${CLAUDE_SKILL_TARGET}`);
    console.log('   Restart Claude Code to load it. Invoke via Skill tool as "agentic-sdlc".');
    return true;
  } catch (err) {
    console.log(`⚠️  Failed to install Claude Code skill: ${err.message}`);
    console.log(`   Manual install: copy "${SKILL_SOURCE}" to "${CLAUDE_SKILL_TARGET}".`);
    return false;
  }
}

function installCodexSkill() {
  if (!fs.existsSync(SKILL_SOURCE)) {
    console.log(`⚠️  Skill source not found at ${SKILL_SOURCE}; skipping Codex install.`);
    return false;
  }
  try {
    fs.mkdirSync(CODEX_SKILLS_DIR, { recursive: true });
    copyRecursive(SKILL_SOURCE, CODEX_SKILL_TARGET);
    console.log(`📦 Installed Codex skill at: ${CODEX_SKILL_TARGET}`);
    console.log('   Restart Codex to load it. Invoke it as "$agentic-sdlc" or by asking for Agentic SDLC.');
    return true;
  } catch (err) {
    console.log(`⚠️  Failed to install Codex skill: ${err.message}`);
    console.log(`   Manual install: copy "${SKILL_SOURCE}" to "${CODEX_SKILL_TARGET}".`);
    return false;
  }
}

function installGeminiSkill() {
  if (!fs.existsSync(SKILL_SOURCE)) {
    console.log(`⚠️  Skill source not found at ${SKILL_SOURCE}; skipping Gemini install.`);
    return false;
  }
  try {
    fs.mkdirSync(GEMINI_SKILLS_DIR, { recursive: true });
    copyRecursive(SKILL_SOURCE, GEMINI_SKILL_TARGET);
    console.log(`📦 Installed Gemini skill at: ${GEMINI_SKILL_TARGET}`);
    console.log('   Run "gemini skills reload" or restart Gemini CLI to load it.');
    return true;
  } catch (err) {
    console.log(`⚠️  Failed to install Gemini skill: ${err.message}`);
    console.log(`   Manual install: copy "${SKILL_SOURCE}" to "${GEMINI_SKILL_TARGET}".`);
    return false;
  }
}

function hasCodexHome() {
  return Boolean(process.env.CODEX_HOME) || fs.existsSync(CODEX_HOME);
}

function hasClaudeHome() {
  return Boolean(process.env.CLAUDE_CONFIG_DIR) || fs.existsSync(CLAUDE_HOME);
}

function hasGeminiHome() {
  return Boolean(process.env.GEMINI_HOME) || fs.existsSync(GEMINI_HOME);
}

console.log('\n--- Agentic SDLC Skill Discovery ---');

let detected = false;

if (checkCommand('claude') || hasClaudeHome()) {
  console.log(`✅ Detected: Claude Code`);
  detected = true;
  installClaudeSkill();
}

if (checkCommand('gemini') || hasGeminiHome()) {
  console.log(`✅ Detected: Gemini CLI`);
  detected = true;
  installGeminiSkill();
}

if (checkCommand('codex') || hasCodexHome()) {
  console.log(`✅ Detected: Codex AI`);
  detected = true;
  installCodexSkill();
}

if (!detected) {
  console.log('ℹ️  No specific AI CLI detected globally, but you can still use the skill.');
}

console.log('\nTo initialize a project with the SDLC protocol, run:');
console.log('👉 npx agentic-sdlc-init');
console.log('------------------------------------\n');
