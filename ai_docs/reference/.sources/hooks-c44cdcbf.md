# Hook source excerpts — F-091 implementation

Working tree based on 74c1833f; captured 2026-11-04 after closure-review corrections. Source excerpts, not native acceptance evidence.

## wireCodexHook

Source: scripts/lib.js
```javascript
function wireCodexHook(spec, options) {
  const validator = path.join(skillTarget(options.client), 'scripts', ORIENT_ENTRY_POINT);
  if (!fs.existsSync(validator)) return { code: 'no-validator', validator };
  if (!options.python) return { code: 'no-python', validator };
  if (ORIENT_UNSAFE_IN_PATH.test(validator)) return { code: 'unsafe-path', validator };
  const sources = hookSources(options);
  if (sources.error) return { code: sources.error, target: sources.target };
  for (const source of sources.sources) {
    const groups = source.settings.hooks && source.settings.hooks[spec.event];
    if (groups !== undefined && !Array.isArray(groups)) return { code: 'malformed', target: source.target };
    for (const group of groups || []) {
      for (const handler of (Array.isArray(group.hooks) ? group.hooks : [group])) {
        const command = (process.platform === 'win32' && (handler.commandWindows || handler.command_windows)) || handler.command || '';
        const invocation = decodeHookInvocation(command);
        const matches = invocation ? invocation.argv[0] === spec.sub.split(' ')[0]
          : ORIENT_ENTRY_POINTS.some(n => command.includes(n)) && spec.re.test(command);
        if (!matches) continue;
        if (group.enabled === false || handler.enabled === false) return { code: 'opted-out', target: source.target };
        const found = orientHookValidator(command);
        if (!found || !path.isAbsolute(found)) return { code: 'unverifiable', target: source.target };
        if (!fs.existsSync(found)) return { code: 'broken', target: source.target };
        if (!codexHookEquivalent(spec, group, handler, command, invocation))
          return { code: 'unverifiable', target: source.target };
        markerAddOf(spec, source.target);
        return { code: 'already', target: source.target, command };
      }
    }
  }
  // Absent sources still carry opt-outs (including an entirely deleted TOML file).
  for (const target of sources.targets) {
    if (markerHasOf(spec, target)) return { code: 'opted-out', target };
  }
  const profile = hookProfile(options.client);
  return wireCommandHookInto({...spec, matcher: spec.event === 'PreToolUse' ? '^apply_patch$' : undefined},
    path.join(options.client.home, profile.file), options.python, validator,
    hookHandler(spec, options.client, options.python, validator));
}
```

## codexHookEquivalent

Source: scripts/lib.js
```javascript
function codexHookEquivalent(spec, group, handler, command, invocation) {
  if (handler.type !== 'command') return false;
  const matcher = group.matcher;
  if (spec.event === 'PreToolUse' ? matcher !== '^apply_patch$' : matcher != null && matcher !== '') return false;
  const expected = spec.sub.split(' ');
  if (invocation) return JSON.stringify(invocation.argv) === JSON.stringify(expected);
  // Recognizing a validator is ownership evidence, not proof of equivalent dispatch.
  const tokens = [...command.matchAll(/"([^"]*)"|'([^']*)'|(\S+)/g)].map(m => m[1] ?? m[2] ?? m[3]);
  const validator = orientHookValidator(command);
  return tokens.length === expected.length + 2 && tokens[1] === validator &&
    JSON.stringify(tokens.slice(2)) === JSON.stringify(expected);
}

// The legacy Claude builder remains unchanged. Codex normalizes child exit codes
// without shell-specific `exit` syntax; stdin/stdout are passed through verbatim.
const CODEX_HOOK_WRAPPER = "import base64,json,subprocess,sys;d=json.loads(base64.b64decode(sys.argv[2]));subprocess.run([sys.executable,d['validator'],*d['argv']],input=sys.stdin.buffer.read())";
```

## hookHandler

Source: scripts/lib.js
```javascript
function hookHandler(spec, client, python, validator) {
  const data = Buffer.from(JSON.stringify({client: client.key, validator, argv: spec.sub.split(' ')})).toString('base64');
  const interpreter = /^[\w.-]+$/.test(python) ? python : '"' + python + '"';
  const handler = {type:'command', command: interpreter + ' -c "' + CODEX_HOOK_WRAPPER + '" agentic-sdlc-hook-v1 ' + data,
    timeout:spec.timeout,
    statusMessage: {
      orient: 'SDLC: load project context when the session starts',
      remind: 'SDLC: remind the agent to follow the development protocol',
      verdict: 'SDLC: block edits missing triage or required guide reads',
      constraints: 'SDLC: recall applicable constraints before editing',
    }[spec.sub.split(' ')[0]]};
  if (spec.sub === 'orient') handler.additionalContextLimit = 0; // orient itself caps output at 9,500 chars
  return handler;
}
```

## hookSources

Source: scripts/lib.js
```javascript
function hookSources(options) {
  const sources = [], targets = [];
  const cwd = options.cwd || process.cwd();
  for (const dir of [options.client.home, path.join(cwd, '.codex')]) {
    for (const name of ['hooks.json', 'config.toml']) {
      const target = path.join(dir, name);
      targets.push(target);
      if (!fs.existsSync(target)) continue;
      try {
        const settings = name.endsWith('.json') ? JSON.parse(fs.readFileSync(target,'utf8').replace(/^\uFEFF/,'')) :
          JSON.parse(execFileSync(options.python,['-c',
            "import json,sys,tomllib;print(json.dumps(tomllib.load(open(sys.argv[1],'rb'))))",target],
            {encoding:'utf8',timeout:5000,stdio:['ignore','pipe','pipe']}));
        if (!settings || typeof settings !== 'object' || Array.isArray(settings) ||
            (settings.hooks !== undefined && (!settings.hooks || typeof settings.hooks !== 'object' || Array.isArray(settings.hooks))))
          return {error:'malformed',target};
        for (const groups of Object.values(settings.hooks || {})) {
          if (!Array.isArray(groups)) return {error:'malformed',target};
          for (const group of groups) {
            if (!group || typeof group !== 'object' || Array.isArray(group) ||
                (group.hooks !== undefined && !Array.isArray(group.hooks))) return {error:'malformed',target};
            for (const handler of group.hooks || [group]) {
              if (!handler || typeof handler !== 'object' || Array.isArray(handler) ||
                  ['command','commandWindows','command_windows'].some(key =>
                    handler[key] !== undefined && typeof handler[key] !== 'string')) return {error:'malformed',target};
            }
          }
        }
        if ((settings.features && settings.features.hooks === false) || settings.allow_managed_hooks_only === true)
          return {error:'disabled-by-policy',target};
        sources.push({target,settings});
      } catch (_) { return {error:name.endsWith('.toml') ? 'unverifiable' : 'malformed',target}; }
    }
  }
  return {sources,targets};
}

// Uninstall twin for the constant-command hooks: one {target, event, name} per
// removal, so the uninstaller can say what it removed.
```

## decodeHookInvocation

Source: scripts/lib.js
```javascript
function decodeHookInvocation(command) {
  const middle = ' -c "' + CODEX_HOOK_WRAPPER + '" agentic-sdlc-hook-v1 ';
  const at = String(command || '').indexOf(middle);
  if (at < 1) return null;
  if (!/^[\w.-]+$|^"[^"$`\r\n]+"$/.test(command.slice(0, at))) return null;
  const encoded = command.slice(at + middle.length);
  if (!/^[A-Za-z0-9+/]+={0,2}$/.test(encoded)) return null;
  try {
    const data = JSON.parse(Buffer.from(encoded, 'base64').toString('utf8'));
    if (data.client !== 'codex' || typeof data.validator !== 'string' ||
        !Array.isArray(data.argv) || !data.argv.every(x=>typeof x === 'string') ||
        !['orient','remind','verdict','constraints'].includes(data.argv[0])) return null;
    return data;
  } catch (_) { return null; }
}
```

## removeGlobalHookEntries

Source: scripts/lib.js
```javascript
function removeGlobalHookEntries(removedRoots, spec) {
  const targets = [];
  const claude = CLIENTS.find((c) => c.key === 'claude');
  if (claude) targets.push(path.join(claude.home, 'settings.json'));
  const codex = CLIENTS.find((c) => c.key === 'codex');
  if (codex) targets.push(path.join(codex.home, 'hooks.json'));
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
        const invocation = decodeHookInvocation(cmd);
        if (!(invocation ? spec.re.test(' ' + invocation.argv.join(' ')) :
          ORIENT_ENTRY_POINTS.some((n) => cmd.includes(n)) && spec.re.test(cmd))) return false;
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

## wrapper

Source: scripts/lib.js
```javascript
const CODEX_HOOK_WRAPPER = "import base64,json,subprocess,sys;d=json.loads(base64.b64decode(sys.argv[2]));subprocess.run([sys.executable,d['validator'],*d['argv']],input=sys.stdin.buffer.read())";
```

## hook-edits

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def hook_edits(payload):
    """Parse the complete native apply_patch syntax without executing it.

    Unknown or incomplete input yields no partial target set. Move checks both
    the old and new paths; file membership is evaluated by the existing gate.
    """
    command = (payload.get("tool_input") or {}).get("command")
    if not isinstance(command, str) or len(command.encode("utf-8")) > VERDICT_LINE_MAX:
        return None
    lines = command.strip().splitlines()
    if not lines or lines[0] != "*** Begin Patch" or lines[-1] != "*** End Patch":
        return None
    edits, current, mode, changed = [], None, None, False
    for line in lines[1:-1]:
        match = re.fullmatch(r"\*\*\* (Add|Update|Delete) File: (.+)", line)
        if match:
            if current is not None and mode != "Delete" and not changed:
                return None
            mode, value = match.groups()
            target = _hint_path(value, payload.get("cwd"))
            if not target:
                return None
            current = {"path": target, "new_text": ""}
            edits.append(current)
            changed = False
        elif line.startswith("*** Move to: ") and current is not None and mode == "Update" and not changed:
            target = _hint_path(line[len("*** Move to: "):], payload.get("cwd"))
            if not target:
                return None
            current = {"path": target, "new_text": ""}
            edits.append(current)
        elif current is not None and mode != "Delete" and (
                line.startswith(("+", "-", " ", "@@")) or line == "*** End of File"):
            if mode == "Add" and not line.startswith("+"):
                return None
            if line.startswith(("+", "-")):
                changed = True
            if line.startswith("+"):
                current["new_text"] += line[1:] + "\n"
        else:
            return None
    if current is not None and mode != "Delete" and not changed:
        return None
    return edits or None
```

## shell-read-paths

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def shell_read_paths(command, cwd, workdir=None):
    """Literal Get-Content/cat reads only: no shell expansion or execution."""
    if not isinstance(command, str) or re.search(r"[$`\r\n;|&<>\x00]", command):
        return None
    token_re = re.compile(r"\s*(?:'([^']*)'|\"([^\"]*)\"|([^\s'\"]+))")
    tokens, pos = [], 0
    while pos < len(command.rstrip()):
        match = token_re.match(command, pos)
        if not match:
            return None
        token = next(x for x in match.groups() if x is not None)
        tokens.append(token)
        pos = match.end()
    if not tokens or tokens[0].lower() not in ("get-content", "cat"):
        return None
    paths, i = [], 1
    while i < len(tokens):
        token = tokens[i]
        if tokens[0].lower() == "get-content" and token.lower() in ("-literalpath", "-path", "-raw"):
            if token.lower() != "-raw" and i + 1 == len(tokens):
                return None
        elif tokens[0].lower() == "get-content" and token.lower() == "-totalcount":
            i += 1
            if i == len(tokens) or not tokens[i].isdigit():
                return None
        elif tokens[0] == "cat" and token == "--":
            pass
        elif token.startswith("-") or re.search(r"[*?\[\],]", token):
            return None
        else:
            base = _hint_path(workdir, cwd) if workdir else cwd
            resolved = _hint_path(token, base)
            if not resolved:
                return None
            paths.append(resolved)
        i += 1
    return paths or None
```

## -codex-literal-calls

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def _codex_literal_calls(code):
    """Recognize a small non-executable JS carrier grammar, otherwise nothing."""
    if not isinstance(code, str):
        return []
    calls, pos = [], 0
    pattern = re.compile(r"\s*(?:text\(\s*)?await\s+tools\.exec_command\((\{.*?\})\)\s*\)?\s*;?", re.DOTALL)
    field = re.compile(r'\s*(?:"(cmd|workdir)"|(cmd|workdir))\s*:\s*("(?:[^"\\]|\\.)*")\s*(,|$)')
    while pos < len(code.rstrip()):
        match = pattern.match(code, pos)
        if not match:
            return []
        obj, off, args = match[1][1:-1], 0, {}
        while off < len(obj.rstrip()):
            item = field.match(obj, off)
            if not item or (item[1] or item[2]) in args:
                return []
            try:
                args[item[1] or item[2]] = json.loads(item[3])
            except ValueError:
                return []
            off = item.end()
        if "cmd" not in args:
            return []
        calls.append(args)
        pos = match.end()
    return calls
```

## transcript-events

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def transcript_events(path):
    """Yield legacy assistant blocks, plus normalized recognized Codex blocks.

    This is read-only and bounded by the existing transcript limits. Historical
    cwd is taken from host metadata, never guessed from the present process.
    """
    cwd = None
    with Path(path).open("rb") as fh:
        for raw in fh:
            if len(raw) > VERDICT_LINE_MAX:
                continue
            try:
                entry = json.loads(raw.decode("utf-8", errors="replace"))
            except ValueError:
                continue
            if not isinstance(entry, dict):
                continue
            if entry.get("type") == "assistant":
                yield entry
                continue
            data = entry.get("payload")
            if not isinstance(data, dict):
                continue
            if entry.get("type") in ("session_meta", "turn_context"):
                if isinstance(data.get("cwd"), str):
                    cwd = data["cwd"]
                continue
            if entry.get("type") != "response_item":
                continue
            blocks = []
            if data.get("type") == "message" and data.get("role") == "assistant":
                blocks = [{"type": "text", "text": x.get("text", "")}
                          for x in (data.get("content") if isinstance(data.get("content"), list) else []) if isinstance(x, dict) and x.get("type") == "output_text"]
            elif data.get("type") in ("function_call", "custom_tool_call"):
                name = data.get("name")
                calls = []
                if name in ("exec_command", "Bash"):
                    try:
                        args = json.loads(data.get("arguments", "{}"))
                    except (ValueError, TypeError):
                        args = None
                    if isinstance(args, dict):
                        calls = [args]
                elif name == "exec":
                    calls = _codex_literal_calls(data.get("input"))
                elif name == "apply_patch":
                    command = data.get("input")
                    if command is None:
                        try:
                            command = json.loads(data.get("arguments", "{}" )).get("command")
                        except (ValueError, TypeError, AttributeError):
                            pass
                    for edit in hook_edits({"tool_input": {"command": command}, "cwd": cwd}) or []:
                        blocks.append({"type": "tool_use", "name": "Write", "input": {"file_path": edit["path"]}})
                for args in calls:
                    for target in shell_read_paths(args.get("cmd", args.get("command")), cwd, args.get("workdir")) or []:
                        blocks.append({"type": "tool_use", "name": "Read", "input": {"file_path": target}})
            if blocks:
                yield {"type": "assistant", "isSidechain": bool(entry.get("agent_id") or data.get("agent_id")),
                       "message": {"content": blocks}}
```

## -codex-hook-config

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def _codex_hook_config(root):
    """Observable Codex policy across sources; no trust or execution assertion."""
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    disabled, unverified, disabled_entries = False, False, False
    for directory in (home, Path(root) / ".codex"):
        for name in ("hooks.json", "config.toml"):
            p = directory / name
            if not p.exists():
                continue
            try:
                if not p.is_file() or p.stat().st_size > ORIENT_HOOK_CONFIG_CAP:
                    raise ValueError("unreadable configuration")
                text = p.read_text(encoding="utf-8-sig")
                if p.suffix == ".toml":
                    import tomllib
                    data = tomllib.loads(text)
                else:
                    data = json.loads(text)
                if not isinstance(data, dict):
                    raise ValueError("unknown configuration shape")
                features = data.get("features", {})
                hooks = data.get("hooks", {})
                if not isinstance(features, dict) or not isinstance(hooks, dict):
                    raise ValueError("unknown policy or hooks shape")
                disabled |= features.get("hooks") is False or data.get("allow_managed_hooks_only") is True
                groups = hooks.get("SessionStart", data.get("SessionStart", []))
                if not isinstance(groups, list):
                    raise ValueError("unknown hook groups")
                for group in groups:
                    if not isinstance(group, dict):
                        raise ValueError("unknown hook group")
                    inner = group.get("hooks", [group])
                    if not isinstance(inner, list) or not all(isinstance(h, dict) for h in inner):
                        raise ValueError("unknown handlers")
                    disabled_entries |= group.get("enabled") is False or any(h.get("enabled") is False for h in inner)
            except Exception:
                unverified = True
    policy = "disabled-by-policy" if disabled else "unverified" if unverified else "enabled"
    return {"policy": policy, "disabled_entries": disabled_entries}
```

## -orient-hook-commands

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def _orient_hook_commands(root):
    """Yield (command, at_user_level, place) across every known client config:
    the three project-relative files, then the machine-global user settings --
    the file the installer wires (F-042), without which a fixed machine's
    projects would read as unwired forever. `place` is a display label, never a
    home path (F-075 prints it)."""
    codex_policy = _codex_hook_config(root)["policy"]
    for rel in ORIENT_HOOK_CONFIG_FILES:
        if rel.startswith(".codex/") and codex_policy != "enabled":
            continue
        for cmd in _orient_entries_in(Path(root) / rel):
            yield cmd, False, rel
    for cmd in _orient_entries_in(_orient_user_settings_path()):
        yield cmd, True, "user settings"
    if codex_policy != "enabled":
        return
    home = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")
    for name in ("hooks.json", "config.toml"):
        for cmd in _orient_entries_in(home / name):
            yield cmd, True, "codex user " + name
        for cmd in _orient_entries_in(Path(root) / ".codex" / name) if name == "config.toml" else ():
            yield cmd, False, ".codex/" + name
```

## -orient-entry-live

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def _orient_entry_live(root, cmd, at_user_level):
    """True unless the entry names a validator that does not resolve.

    A matching entry whose tokens name no validator is "cannot tell" and counts
    as live (the lib.js contract: never report broken on cannot-tell). Relative
    tokens resolve against the project root (the vendored-validator
    convention); a USER-level relative token has no cwd to resolve against and
    is treated as cannot-tell."""
    invocation = _decode_hook_invocation(cmd)
    token = invocation["validator"] if invocation else None
    for m in _ORIENT_HOOK_TOKEN_RE.finditer(cmd):
        tok = m.group(1) if m.group(1) is not None else m.group(2)
        if any(tok.endswith(n) for n in ORIENT_HOOK_ENTRY_POINTS):
            token = tok
            break
    if token is None:
        return True
    tp = Path(token)
    if not tp.is_absolute():
        if at_user_level:
            return True
        tp = Path(root) / tp
    return tp.exists()
```

## verdict-reason

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def verdict_reason(payload, root=None, docs_name=None):
    """The refusal line for this edit event, or None when the edit may proceed.
    Without a root, the project is the one holding the edited file (hook_project)."""
    if payload.get("tool_name") == "apply_patch" and not payload.get("agent_id"):
        for edit in hook_edits(payload) or []:
            reason = verdict_reason({**payload, "tool_name": "Edit", "tool_input": {
                "file_path": edit["path"], "new_string": edit["new_text"]}}, root, docs_name)
            if reason:
                return reason
        return None
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

Source: skills/agentic-sdlc-skill/scripts/sdlc_core.py
```python
def constraints_hook_context(payload, root=None, docs_name=None):
    """The context to recall before this edit, or None (FS6): an edit tool, outside
    a subagent, on a file of a project whose open L3 code unit binds it (or the
    unit's own ANALYSIS, about to name a path a P row binds -- UC6), by a session
    that worked on that unit and last declared L3."""
    if payload.get("tool_name") == "apply_patch" and not payload.get("agent_id"):
        lines = []
        for edit in hook_edits(payload) or []:
            context = constraints_hook_context({**payload, "tool_name": "Edit", "tool_input": {
                "file_path": edit["path"], "new_string": edit["new_text"]}}, root, docs_name)
            for line in (context or "").splitlines():
                if line not in lines:
                    lines.append(line)
        if len(lines) > CONSTRAINTS_HOOK_LINES:
            lines = lines[:CONSTRAINTS_HOOK_LINES - 1] + [lines[-1]]
        return "\n".join(lines) or None
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

## budgets

```python
VERDICT_MAX_BYTES = 256 * 1024 * 1024  # a larger transcript: cannot afford to tell
VERDICT_LINE_MAX = 1024 * 1024         # assistant lines are small; skip the rest unparsed
CONSTRAINTS_HOOK_LINES = 15
```

## postinstall

Source: scripts/postinstall.js
```javascript
    if (client.key === 'codex' && installed) {
      const python = detectPython();
      for (const [name, wire] of [['orientation', wireGlobalOrientHook], ['reminder', wireGlobalRemindHook],
        ['guide-verdict check', wireGlobalVerdictHook], ['constraint recall', wireGlobalRecallHook]]) {
        try {
          const result = wire({client, python});
          console.log(`Codex ${name}: ${result.code}${result.target ? ' (' + result.target + ')' : ''}.`);
        } catch (_) { console.log(`Codex ${name}: configuration failed; existing settings preserved.`); }
      }
      console.log('Configured Codex hooks require human trust. Check the per-hook results above and review them with /hooks in a local Codex session.');
      console.log('Client policy, disabled hooks or cloud orchestration may prevent execution; no trust or policy setting was changed.');
    }
```

## init

Source: scripts/init.js
```javascript
const codexClient = detectedClients.find(c => c.key === 'codex');
if (codexClient) {
  const result = wireGlobalOrientHook({client: codexClient, python: detectedPython, cwd});
  console.log(`Codex user orientation: ${result.code}. Review configured hooks with /hooks; trust is not changed.`);
  if (result.code === 'no-validator') console.log('Run agentic-sdlc-install-skill first to configure Codex hooks.');
}
```

## consent-label

Installed desktop 26.1029.7803.0, webview/assets/async/154206.0ace5905ae.js (read-only inspection).
```javascript
function i(e,s,t){let o=e.statusMessage?.trim();return o?t.formatMessage(a.numberedHookTitle,{index:s+1,statusMessage:o}):t.formatMessage(a.fallbackHookTitle,{index:s+1})}
```
