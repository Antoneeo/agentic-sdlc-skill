# Hook source snapshot — baseline 74c1833f

Code excerpts, no user settings/transcript content. LF normalized for hashing.

## installation

Source: `scripts/lib.js:73-148`

```text
    label: 'Claude Code',
    cmd: 'claude',
    home: process.env.CLAUDE_CONFIG_DIR || path.join(os.homedir(), '.claude'),
    envVar: 'CLAUDE_CONFIG_DIR',
    reload: 'Restart Claude Code to load it. Invoke via Skill tool as "agentic-sdlc".',
  },
  {
    key: 'gemini',
    label: 'Gemini CLI',
    cmd: 'gemini',
    home: process.env.GEMINI_HOME || path.join(os.homedir(), '.gemini'),
    envVar: 'GEMINI_HOME',
    reload: 'Run "gemini skills reload" or restart Gemini CLI to load it.',
  },
  {
    key: 'codex',
    label: 'Codex AI',
    cmd: 'codex',
    home: process.env.CODEX_HOME || path.join(os.homedir(), '.codex'),
    envVar: 'CODEX_HOME',
    reload: 'Restart Codex to load it. Invoke it as "$agentic-sdlc" or by asking for Agentic SDLC.',
  },
  {
    // Google Antigravity 2.0 discovers global agent skills under
    // ~/.gemini/config/skills/ -- the SAME home the legacy Gemini CLI claims.
    // To avoid a shared-home double-install (P-TM T1), this entry sets:
    //  - skillsSubdir 'config/skills': distinct target from gemini's ~/.gemini/skills
    //  - homeMarker on ~/.gemini/config/skills: detection never fires on bare
    //    ~/.gemini (which every Antigravity user has); only the Antigravity skills
    //    dir, the `agy` CLI, or ANTIGRAVITY_HOME count as "Antigravity installed".
    key: 'antigravity',
    label: 'Google Antigravity',
    cmd: 'agy',
    home: process.env.ANTIGRAVITY_HOME || path.join(os.homedir(), '.gemini'),
    envVar: 'ANTIGRAVITY_HOME',
    skillsSubdir: 'config/skills',
    homeMarker: path.join(
      process.env.ANTIGRAVITY_HOME || path.join(os.homedir(), '.gemini'),
      'config',
      'skills',
    ),
    reload: 'Restart Antigravity, or run "agy skills reload", to load it. Invoke by asking for Agentic SDLC.',
  },
];

function commandExists(cmd) {
  try {
    execSync(`${cmd} --version`, { stdio: 'ignore' });
    return true;
  } catch (e) {
    return false;
  }
}

function clientDetected(client) {
  // An entry may override the fs-existence probe with a `homeMarker` (a more
  // specific path than the bare home) so two clients sharing a home dir do not
  // both fire on its mere existence. Entries without a marker check `home`
  // exactly as before (backward-compatible).
  const homePathToCheck = client.homeMarker || client.home;
  return commandExists(client.cmd)
    || Boolean(process.env[client.envVar])
    || fs.existsSync(homePathToCheck);
}

function skillTarget(client) {
  // An entry may override the default `skills` sub-path with `skillsSubdir`
  // (split on '/' to keep cross-platform path.join correctness). Entries
  // without it resolve to <home>/skills/agentic-sdlc exactly as before.
  const subdir = client.skillsSubdir ? client.skillsSubdir.split('/') : ['skills'];
  return path.join(client.home, ...subdir, INSTALLED_SKILL_NAME);
}

function copyRecursive(src, dest) {
  if (typeof fs.cpSync === 'function') {
    fs.cpSync(src, dest, { recursive: true, force: true });
```

## installation-entry

Source: `scripts/postinstall.js:1-116`

```text
#!/usr/bin/env node

const fs = require('fs');
const {
  SKILL_SOURCE, CLIENTS, clientDetected, skillTarget, copyRecursive,
  wireGlobalOrientHook, wireGlobalRemindHook, wireGlobalVerdictHook, wireGlobalRecallHook,
  detectPython,
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
        // F-046: the per-turn reminder, wired alongside and never instead of
        // the session hook. `orient` decays; this one re-arms one constant line
        // every prompt, and its first duty is the one that was missing -- decide
        // whether the skill governs the work and, if so, load it once, because
        // an unread protocol cannot be applied. Owner-accepted per-turn cost:
        // ai_docs/vision/rulings.md r19.
        const rr = wireGlobalRemindHook({ client, python: detectPython() });
        if (rr.code === 'wired') {
          console.log('🔗 Per-turn protocol reminder wired for every project on this machine');
          console.log(`   (${rr.target}). One constant line per prompt; remove that hook`);
          console.log('   entry to opt out — it will not be re-added.');
        }
        // F-076: the guide-verdict check -- refuses an edit when the session
        // declared no guide-router verdict, or never read a guide it names.
        // Silent on projects without guides; owner-accepted per-edit cost:
        // ai_docs/vision/rulings.md r34.
        const rv = wireGlobalVerdictHook({ client, python: detectPython() });
        if (rv.code === 'wired') {
          console.log('🔗 Guide-verdict check wired for every project on this machine');
          console.log(`   (${rv.target}). Edits wait for the Rule-Zero router verdict in projects`);
          console.log('   with guides; remove that hook entry to opt out — it will not be re-added.');
        }
        // F-085: the constraint recall -- before an edit of a file bound by a
        // constraint of the open L3 unit the session works on, the agent gets
        // those constraints in its context. Context only, never a decision;
        // silent everywhere else. Per-edit cost: the lines, owner-accepted in
        // REQUEST_working_model.md R12 (b); ~0.25 s per edit, R15.
        const rc = wireGlobalRecallHook({ client, python: detectPython() });
        if (rc.code === 'wired') {
          console.log('🔗 Constraint recall wired for every project on this machine');
          console.log(`   (${rc.target}). In an L3 unit, an edit of a file its constraints bind`);
          console.log('   shows them first; remove that hook entry to opt out — it will not be re-added.');
        }
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
```

## ownership

Source: `scripts/lib.js:478-654`

```text
    const rel = path.relative(String(parent), String(child));
    return rel !== '' && !rel.startsWith('..') && !path.isAbsolute(rel);
  } catch (e) {
    return false;
  }
}

// The marker lives under the family's agent-global root (the same root the
// validator's AGENTIC_SDLC_KB_ROOT seam names), read at call time so the test
// battery's stubbed env applies. Every helper is fail-open: a broken marker
// must never break an install, and a failed marker write never undoes a wire.
function orientMarkerPath() {
  const root = process.env.AGENTIC_SDLC_KB_ROOT
    || path.join(os.homedir(), '.agentic-sdlc');
  return path.join(root, 'orient-hook-wired');
}
function orientMarkerTargets() {
  try {
    return fs.readFileSync(orientMarkerPath(), 'utf8')
      .split(/\r?\n/).map((s) => s.trim()).filter(Boolean);
  } catch (e) {
    return [];
  }
}
function orientMarkerHas(target) {
  return orientMarkerTargets().some((t) => pathsEqual(t, target));
}
function orientMarkerAdd(target) {
  try {
    if (orientMarkerHas(target)) return;
    fs.mkdirSync(path.dirname(orientMarkerPath()), { recursive: true });
    fs.appendFileSync(orientMarkerPath(), target + String.fromCharCode(10), 'utf8');
  } catch (e) { /* fail-open */ }
}
function orientMarkerRemove(target) {
  try {
    const rest = orientMarkerTargets().filter((t) => !pathsEqual(t, target));
    if (rest.length) {
      fs.writeFileSync(orientMarkerPath(), rest.join(String.fromCharCode(10)) + String.fromCharCode(10), 'utf8');
    } else {
      fs.rmSync(orientMarkerPath(), { force: true });
    }
  } catch (e) { /* fail-open */ }
}

// Wire the machine-global hook into client.home/settings.json — exactly ONE
// file (user level has no local split; the path is machine-local by nature).
// Codes follow the wireOrientHook contract, plus `opted-out`.
function wireGlobalOrientHook(options) {
  const client = options.client;
  const python = options.python;

  const validator = path.join(skillTarget(client), 'scripts', ORIENT_ENTRY_POINT);
  if (!fs.existsSync(validator)) return { code: 'no-validator', validator };
  if (!python) return { code: 'no-python', validator };
  if (ORIENT_UNSAFE_IN_PATH.test(validator)) return { code: 'unsafe-path', validator };
  const command = orientHookCommand(python, validator, false);

  const target = path.join(client.home, 'settings.json');
  const state = orientSettingsState(target);
  if (!state.ok) return { code: 'malformed', target, why: state.why, command };

  const existing = findOrientHook(state.settings);
  if (existing) {
    const found = orientHookValidator(existing);
    if (found === null || !path.isAbsolute(found)) {
      // No cwd exists at user level, so an unresolvable token is "cannot
      // tell" — left alone, never remembered as ours.
      return { code: 'unverifiable', target, existing, command };
    }
    if (fs.existsSync(found)) {
      // A hand-wired live hook, once removed, deserves the same respect as
      // one this installer wrote: remember the target.
      orientMarkerAdd(target);
      return { code: 'already', target, command: existing };
    }
    return { code: 'broken', target, existing, command };
  }

  if (orientMarkerHas(target)) return { code: 'opted-out', target };

  const settings = state.settings;
  if (!settings.hooks) settings.hooks = {};
  if (!Array.isArray(settings.hooks.SessionStart)) settings.hooks.SessionStart = [];
  settings.hooks.SessionStart.push({
    hooks: [{
      type: 'command',
      command,
      timeout: ORIENT_HOOK_TIMEOUT,
      statusMessage: 'Loading docs orientation...',
    }],
  });
  try {
    fs.mkdirSync(path.dirname(target), { recursive: true });
    fs.writeFileSync(target, JSON.stringify(settings, null, 2) + String.fromCharCode(10), 'utf8');
  } catch (e) {
    return { code: 'write-failed', target, command, error: e.message };
  }
  orientMarkerAdd(target);
  return { code: 'wired', target, command };
}

// Uninstall symmetry: removing the skill dirs would leave any global hook
// naming them wired-and-DEAD. So, across EVERY settings target the marker
// remembers (a hook wired under CLAUDE_CONFIG_DIR=/x must be cleaned from a
// shell without that env) unioned with the current client.home, remove ONLY
// the SessionStart entries whose validator token resolves INTO a root being
// removed. Foreign or unverifiable entries are never touched. The marker line
// is cleared ONLY when an entry was actually removed — when the user had
// already removed the hook, the line stays and the opt-out survives uninstall,
// reinstall, and sibling-lens uninstalls.
function removeGlobalOrientHooks(removedRoots) {
  return removeGlobalHookEntries(removedRoots, {
    event: 'SessionStart',
    re: / orient(\s|$)/,
    markerTargets: orientMarkerTargets,
    markerRemove: orientMarkerRemove,
  });
}

// The pruning loop shared by every hook this installer wires (F-076): only the
// `spec.event` entries whose command matches `spec.re` AND whose validator
// token resolves INTO a removed root are ours; the marker line is cleared only
// when an entry was actually removed. Returns the targets touched.
function removeGlobalHookEntries(removedRoots, spec) {
  const targets = [];
  const claude = CLIENTS.find((c) => c.key === 'claude');
  if (claude) targets.push(path.join(claude.home, 'settings.json'));
  for (const t of spec.markerTargets()) {
    if (!targets.some((x) => pathsEqual(x, t))) targets.push(t);
  }
  const removedFrom = [];
  for (const target of targets) {
    try {
      const state = orientSettingsState(target);
      if (!state.ok || !fs.existsSync(target)) continue;
      const hooks = state.settings.hooks;
      if (!hooks || !Array.isArray(hooks[spec.event])) continue;
      let removedHere = false;
      const ours = (h) => {
        const cmd = h && typeof h.command === 'string' ? h.command : '';
        if (!(ORIENT_ENTRY_POINTS.some((n) => cmd.includes(n)) && spec.re.test(cmd))) return false;
        const tok = orientHookValidator(cmd);
        if (tok === null || !path.isAbsolute(tok)) return false;   // cannot attribute: keep
        return removedRoots.some((root) => pathInside(tok, root));
      };
      const kept = [];
      for (const group of hooks[spec.event]) {
        if (!group || typeof group !== 'object') { kept.push(group); continue; }
        if (Array.isArray(group.hooks)) {
          const inner = group.hooks.filter((h) => {
            if (ours(h)) { removedHere = true; return false; }
            return true;
          });
          if (inner.length) kept.push({ ...group, hooks: inner });
          else if (inner.length !== group.hooks.length) { /* emptied: prune */ }
          else kept.push(group);
        } else if (ours(group)) {
          removedHere = true;                      // direct-object shape: prune
        } else {
          kept.push(group);
        }
      }
      if (!removedHere) continue;
      state.settings.hooks[spec.event] = kept;
      if (!kept.length) delete state.settings.hooks[spec.event];
      if (state.settings.hooks && !Object.keys(state.settings.hooks).length) {
        delete state.settings.hooks;
      }
      fs.writeFileSync(target, JSON.stringify(state.settings, null, 2) + String.fromCharCode(10), 'utf8');
      spec.markerRemove(target);
      removedFrom.push(target);
    } catch (e) { /* fail-open per target: never abort an uninstall */ }
  }
  return removedFrom;
}

```

## transcript-facts

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2703-2752`

```text
def transcript_facts(path):
    """What the session transcript shows about the verdict duty, or None when it
    cannot be read within the bounds.

    Returns {"assistant": entries parsed, "sidechain": a subagent's own transcript
    (Claude Code marks every entry of one `isSidechain`), "declared": a router verdict seen,
    "trivial": a level-1 declaration seen (`Level: L1`, `E1`), "named": guides the verdicts name,
    "read": guide names that appeared in a non-edit tool's input}."""
    facts = {"assistant": 0, "sidechain": False, "declared": False, "trivial": False,
             "named": set(), "read": set()}
    try:
        p = Path(path)
        if not p.is_file() or p.stat().st_size > VERDICT_MAX_BYTES:
            return None
        with p.open("rb") as fh:
            for raw in fh:
                if len(raw) > VERDICT_LINE_MAX or b'"assistant"' not in raw:
                    continue
                try:
                    entry = json.loads(raw.decode("utf-8", errors="replace"))
                except ValueError:
                    continue
                if not isinstance(entry, dict) or entry.get("type") != "assistant":
                    continue
                content = (entry.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                facts["assistant"] += 1
                if entry.get("isSidechain") is True:
                    facts["sidechain"] = True
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        for line in str(block.get("text") or "").splitlines():
                            d = _DECLARATION_RE.match(line)
                            if d and d.group(2):
                                facts["trivial"] = True
                            m = _VERDICT_ROUTER_RE.search(line)
                            if m and (d or _VERDICT_LINE_RE.match(line)):
                                facts["declared"] = True
                                if not _VERDICT_NONE_RE.match(m.group(1)):
                                    facts["named"].update(_GUIDE_NAME_RE.findall(m.group(1)))
                    elif (block.get("type") == "tool_use"
                          and block.get("name") not in VERDICT_EDIT_TOOLS):
                        facts["read"].update(_GUIDE_NAME_RE.findall(
                            json.dumps(block.get("input"), ensure_ascii=False)))
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return facts
```

## transcript-work

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:3105-3150`

```text
def transcript_work(path):
    """What the session transcript shows about the work, or None when it cannot be
    read within the verdict hook's bounds: {"assistant": entries parsed,
    "sidechain": a subagent's transcript, "level": the last declared level ("1",
    "2", "3") or None, "touched": normalized absolute paths this session read or
    wrote}."""
    work = {"assistant": 0, "sidechain": False, "level": None, "touched": set()}
    try:
        p = Path(path)
        if not p.is_file() or p.stat().st_size > VERDICT_MAX_BYTES:
            return None
        with p.open("rb") as fh:
            for raw in fh:
                if len(raw) > VERDICT_LINE_MAX or b'"assistant"' not in raw:
                    continue
                try:
                    entry = json.loads(raw.decode("utf-8", errors="replace"))
                except ValueError:
                    continue
                if not isinstance(entry, dict) or entry.get("type") != "assistant":
                    continue
                content = (entry.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                work["assistant"] += 1
                if entry.get("isSidechain") is True:
                    work["sidechain"] = True
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "text":
                        for letter, one, other in _DECLARATION_RE.findall(
                                str(block.get("text") or "")):
                            if letter.upper() == "L":
                                work["level"] = one or other
                    elif block.get("type") == "tool_use" and block.get("name") in _WORK_TOOLS:
                        inp = block.get("input") or {}
                        target = inp.get("file_path") or inp.get("notebook_path")
                        if isinstance(target, str) and target:
                            try:
                                work["touched"].add(_norm_rel(Path(target).resolve().as_posix()))
                            except (OSError, ValueError):
                                pass
    except (OSError, ValueError, TypeError, AttributeError):
        return None
    return work
```

## verdict-reason

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2755-2792`

```text
def verdict_reason(payload, root=None, docs_name=None):
    """The refusal line for this edit event, or None when the edit may proceed.
    Without a root, the project is the one holding the edited file (hook_project)."""
    if payload.get("tool_name") not in VERDICT_EDIT_TOOLS or payload.get("agent_id"):
        return None
    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    transcript = payload.get("transcript_path")
    if not isinstance(target, str) or not target or not transcript:
        return None
    root = hook_project(target, root, docs_name)
    if root is None:
        return None  # two docs roots side by side: cannot tell which governs
    try:
        Path(target).resolve().relative_to(root)
    except (ValueError, OSError):
        return None  # outside the project: not this check's concern
    ref = ai_path(root, "reference")
    if not ref.is_dir():
        return None
    guides = {g.name for g in ref.glob("GUIDE_*.md") if g.is_file()}
    if not guides:
        return None
    facts = transcript_facts(transcript)
    if not facts or not facts["assistant"]:
        return None  # unreadable, oversized or an unknown format: cannot tell
    if facts["sidechain"]:
        return None  # a subagent works under its orchestrator's verdict
    if not (facts["declared"] or facts["trivial"]):
        return ("[sdlc verdict] No guide-router verdict in this session; this project has "
                f"guides ({docs_dir()}/reference/INDEX.md). Declare it with the level, e.g. "
                "\"Level: L2 · router: no match\" or \"router: GUIDE_x.md -> read\" "
                "(L1: \"Level: L1\"), then retry.")
    unread = sorted((facts["named"] & guides) - facts["read"])
    if unread:
        return (f"[sdlc verdict] The router verdict names {', '.join(unread)}, not read in "
                "this session. Read it, then retry.")
    return None
```

## constraints-hook-context

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:3173-3225`

```text
def constraints_hook_context(payload, root=None, docs_name=None):
    """The context to recall before this edit, or None (FS6): an edit tool, outside
    a subagent, on a file of a project whose open L3 code unit binds it (or the
    unit's own ANALYSIS, about to name a path a P row binds -- UC6), by a session
    that worked on that unit and last declared L3."""
    if payload.get("tool_name") not in VERDICT_EDIT_TOOLS or payload.get("agent_id"):
        return None
    tool_input = payload.get("tool_input") or {}
    target = tool_input.get("file_path") or tool_input.get("notebook_path")
    transcript = payload.get("transcript_path")
    if not isinstance(target, str) or not target or not transcript:
        return None
    root = hook_project(target, root, docs_name)
    if root is None or not ai_path(root, "solutions").is_dir():
        return None
    found = file_constraints(root, target)
    rel = project_relative(root, target)
    named = _path_tokens(_hook_new_text(tool_input), False)
    if named and rel and rel.startswith(_norm_rel(f"{docs_dir()}/solutions/ANALYSIS_")):
        for p, meta, text in open_code_units(root):
            if _norm_rel(f"{docs_dir()}/solutions/{p.name}") != rel:
                continue
            items = parse_constraints(text)
            bound = [c for c in items if c["kind"] == "P"
                     and not c["released"] and c["bindings"] & named]
            if bound and not any(f[0] == p for f in found):
                found.append((p, meta, bound, unread_sections(text, items)))
    if not found:
        return None
    work = transcript_work(transcript)
    if not work or not work["assistant"] or work["sidechain"] or work["level"] != "3":
        return None
    # One budget for the whole recall, whatever the number of units; a P line and
    # its evidence line are kept together or left out together.
    out, budget = [], CONSTRAINTS_HOOK_LINES
    for p, meta, items, unread in found:
        if not (_unit_documents(root, p) & work["touched"]):
            continue
        home = f"solutions/{p.name}"
        unit = meta.get("id") or p.stem
        out.append(_clip(f"[sdlc constraints] {unit} — {home}"))
        shown = 0
        for c in items:
            chunk = constraint_lines(home, [c], False)
            if len(chunk) > budget:
                break
            out.extend(chunk)
            budget -= len(chunk)
            shown += 1
        if shown < len(items):
            out.append(_clip(f"More: sdlc_check.py constraints --unit {unit}"))
        out.append(_clip(constraints_sentence(unread)))
    return "\n".join(out) if out else None
```

## cmd-verdict

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2795-2814`

```text
def cmd_verdict(args):
    """PreToolUse hook: print a JSON refusal or nothing. Always 0 -- exit 2 would
    block blind, and the wired command adds `; exit 0` for validators that cannot
    run this at all (missing, or older than it)."""
    if not args.hook:
        return 0
    try:
        payload = read_hook_payload()
        if payload is None:
            return 0
        root = Path(args.root).resolve() if args.root else None
        reason = verdict_reason(payload, root, getattr(args, "docs_dir", None))
        if reason:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": reason}}, ensure_ascii=False))
    except Exception:
        pass
    return 0
```

## cmd-constraints-hook

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:3228-3244`

```text
def cmd_constraints_hook(args):
    """PreToolUse hook: print a context-only JSON or nothing. Always 0 -- exit 2
    would block the edit, and the wired command adds `; exit 0` for validators
    that cannot run this at all (T2)."""
    try:
        payload = read_hook_payload()
        if payload is None:
            return 0
        root = Path(args.root).resolve() if args.root else None
        context = constraints_hook_context(payload, root, getattr(args, "docs_dir", None))
        if context:
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "additionalContext": context}}, ensure_ascii=False))
    except Exception:
        pass
    return 0
```

## -orient-hook-commands

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2368-2378`

```text
def _orient_hook_commands(root):
    """Yield (command, at_user_level, place) across every known client config:
    the three project-relative files, then the machine-global user settings --
    the file the installer wires (F-042), without which a fixed machine's
    projects would read as unwired forever. `place` is a display label, never a
    home path (F-075 prints it)."""
    for rel in ORIENT_HOOK_CONFIG_FILES:
        for cmd in _orient_entries_in(Path(root) / rel):
            yield cmd, False, rel
    for cmd in _orient_entries_in(_orient_user_settings_path()):
        yield cmd, True, "user settings"
```

## orient-wiring

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2405-2418`

```text
def orient_wiring(root):
    """{client: {command: place}} for the LIVE orient entries, per client.

    Per client because two clients never read each other's settings: a Codex
    entry beside a Claude Code one is two clients oriented once each, not one
    session oriented twice. Identical command strings count once. A dead entry
    delivers no copy and is left out (F-075 FS3)."""
    out = {}
    for cmd, at_user_level, place in _orient_hook_commands(root):
        if not _orient_entry_live(root, cmd, at_user_level):
            continue
        client = "codex" if place.startswith(".codex") else "claude"
        out.setdefault(client, {}).setdefault(cmd.strip(), place)
    return out
```

## orient-hook-state

Source: `skills/agentic-sdlc-skill/scripts/sdlc_core.py:2421-2437`

```text
def orient_hook_state(root):
    """'wired' | 'dead' | 'unwired'.

    A matching entry whose tokens name no validator is "cannot tell" and counts
    as wired (the lib.js contract: never report broken on cannot-tell). 'dead'
    requires every matching entry to name a validator that does not resolve:
    the client runs ALL SessionStart hooks -- project-level AND user-level
    merge -- so one live entry at either level still orients the session
    (any-resolves aggregation across levels). Relative tokens resolve against
    the project root (the vendored-validator convention); a USER-level relative
    token has no cwd to resolve against and is treated as cannot-tell."""
    matched = False
    for cmd, at_user_level, _place in _orient_hook_commands(root):
        matched = True
        if _orient_entry_live(root, cmd, at_user_level):
            return "wired"
    return "dead" if matched else "unwired"
```

## sibling-kb-agentic-skill

Source: `distributions/kb-agentic-skill/scripts/postinstall.js:1-74`

```text
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

console.log('\n--- KB Agentic Skill Discovery ---');

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

console.log('\nTo initialize a project with the KB Agentic protocol, run:');
console.log('👉 npx kb-agentic-init');
console.log('------------------------------------\n');
```

## sibling-mkt-agentic-sdlc

Source: `distributions/mkt-agentic-sdlc/scripts/postinstall.js:1-74`

```text
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

console.log('\n--- Marketing Agentic SDLC Skill Discovery ---');

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

console.log('\nTo initialize a project with the marketing protocol, run:');
console.log('👉 npx mkt-sdlc-init');
console.log('------------------------------------\n');
```

## sibling-course-creator

Source: `distributions/course-creator/scripts/postinstall.js:1-16`

```text
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
```
