# Shared project memory: source excerpts

Captured for F-057 from the working tree. Symbols are the lookup keys; line numbers are not stable.

## skills/agentic-sdlc-skill/scripts/knowledge.py:MEMORY_DIRS

```python
MEMORY_DIRS = ("vision", "reference", "architecture", "functional", "strategic",
               "solutions", "research", "strategy", "tactics", "deliverables",
               "spikes", "topics", "corpus/notes")
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_memory_safe

```python
def _memory_safe(docs, path):
    """Reject links (including Windows junctions) and paths outside the docs root."""
    try:
        path.resolve().relative_to(docs.resolve())
        for p in (path, *path.parents):
            if p == docs.parent:
                break
            if p.is_symlink() or (hasattr(p, "is_junction") and p.is_junction()):
                return False
        return True
    except (OSError, ValueError, RuntimeError):
        return False
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:memory_records

```python
def memory_records(docs):
    """Live metadata, not claims or work states. Never traverse raw corpus or logs."""
    paths = []
    readme = docs / "README.md"
    default = "code"
    if readme.is_file() and _memory_safe(docs, readme):
        paths.append(readme)
        meta = sdlc_core.load_frontmatter(sdlc_core.read_text(readme).splitlines())
        default = kb_unquote(meta.get("default_domain")) or default
    for dirname in MEMORY_DIRS:
        folder = docs / dirname
        if not folder.is_dir() or not _memory_safe(docs, folder):
            continue
        for base, dirs, files in os.walk(folder, followlinks=False):
            dirs[:] = sorted(d for d in dirs if not d.startswith((".", "harness_"))
                             and _memory_safe(docs, Path(base) / d))
            for name in files:
                p = Path(base) / name
                if (p.suffix.lower() == ".md" and name not in ("INDEX.md", "features_history.md")
                        and _memory_safe(docs, p)):
                    paths.append(p)
    records = []
    for p in sorted(set(paths), key=lambda p: p.relative_to(docs).as_posix()):
        raw = p.read_bytes()
        text = raw.decode("utf-8", errors="replace")
        meta = sdlc_core.load_frontmatter(text.splitlines())
        title = next((line[2:].strip() for line in text.splitlines()
                      if line.startswith("# ")), p.stem)
        records.append((p.relative_to(docs).as_posix(),
                        kb_unquote(meta.get("domain")) or default,
                        ", ".join(_as_list(meta.get("topics", ""))),
                        kb_unquote(meta.get("description")) or title,
                        hashlib.sha256(raw).hexdigest()))
    return records
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_memory_table

```python
def _memory_table(records):
    def cell(value):
        return " ".join(value.split()).replace("|", "&#124;").replace("<", "&lt;")
    lines = ["| Path | Domain | Topics | Description | SHA256 |", "|---|---|---|---|---|"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in records]
    return "\n".join(lines) + "\n"
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:memory_build_index

```python
def memory_build_index(docs):
    return ("# Project memory (generated discovery catalog)\n\n"
            "Regenerate with the installed validator's index command. Paths are relative "
            "to the docs root. Read each source for authority, validity and status; "
            "a catalog entry is not a verified fact.\n\n" + _memory_table(memory_records(docs)))
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:memory_index

```python
def memory_index(docs):
    out = docs / "memory" / "INDEX.md"
    if not _memory_safe(docs, out):
        print("[ERROR] unsafe memory/INDEX.md output path; nothing written there")
        return 1
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(memory_build_index(docs))
    print("[ok] project memory regenerated: %s" % out)
    return 0
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:memory_validate

```python
def memory_validate(docs):
    out = docs / "memory" / "INDEX.md"
    if not _memory_safe(docs, out):
        print("[ERROR] unsafe memory/INDEX.md path")
        return 1
    if out.is_file() and sdlc_core.norm_text(sdlc_core.read_text(out)) != \
            sdlc_core.norm_text(memory_build_index(docs)):
        print("[ERROR] memory/INDEX.md not aligned: run the validator's index command")
        return 1
    return 0
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:memory_recall

```python
def memory_recall(docs, query):
    words = query.casefold().split()
    rows = [r for r in memory_records(docs)
            if all(w in " ".join(r[:4]).casefold() for w in words)]
    print("# Project memory: live metadata lookup (read sources before deciding)")
    print(_memory_table(rows) if rows else "No metadata match; this is not proof of no knowledge.")
    return 0
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_refresh_indexes

```python
def kb_refresh_indexes(docs):
    """Derived indexes without invoking any domain's main index command."""
    for dirname, builder in (("topics", kb_build_topic_index), ("corpus", kb_build_corpus_index)):
        out = docs / dirname / "INDEX.md"
        if not _memory_safe(docs, out):
            print("[ERROR] unsafe %s/INDEX.md output path" % dirname)
            return 1
        if (docs / dirname).is_dir():
            out.write_text(builder(docs), encoding="utf-8")
            print("[ok] %s index regenerated: %s" % (dirname, out))
    return memory_index(docs)
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_validate_surface

```python
def kb_validate_surface(docs, full=False):
    """Additive seam for marketing: preserve its own validator and report."""
    rc = max(memory_validate(docs), _kb_extra_validate(docs))
    if full and ((docs / "topics").is_dir() or (docs / "corpus").is_dir()):
        cycle = kb_time_cycle(docs)
        rc = max(rc, kb_cmd_graph(docs, cycle), kb_cmd_corpus(docs, cycle))
    return rc
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_kb_root

```python
def _kb_root(args):
    """Resolve the PROJECT root exactly as the spine's main does, so --docs-dir,
    the env seam and the two-roots-refuse behaviour hold on intercepted commands.
    Same call, same order: resolve_docs_dir(args, root) -> (discovered, name).
    Spine cmd_* take the project root; kb helpers take the docs root under it."""
    discovered, name = sdlc_core.resolve_docs_dir(args, getattr(args, "root", None))
    sdlc_core.set_docs_dir(name)
    root = (Path(args.root).resolve() if args.root
            else (discovered or sdlc_core.find_project_root()))
    return root, root / name
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_cmd_index

```python
def kb_cmd_index(root, docs):
    rc = sdlc_core.cmd_index(root)
    return max(rc, kb_refresh_indexes(docs)) if rc == 0 else rc
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_cmd_validate

```python
def kb_cmd_validate(root, docs, strict=False, hybrid=False):
    rc = sdlc_core.cmd_validate(root, strict=strict, hybrid=hybrid)
    return max(rc, kb_validate_surface(docs))
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_cmd_check

```python
def kb_cmd_check(root, docs, strict=False, hybrid=False):
    # The spine's check owns its banners and summary line: reuse it whole, so a
    # tree with no kb surface gets byte-identical output. The kb checks run
    # after, and only when the surface exists.
    rc = sdlc_core.cmd_check(root, strict=strict, hybrid=hybrid)
    rc = max(rc, _kb_extra_validate(docs), memory_validate(docs))
    if (docs / "topics").is_dir() or (docs / "corpus").is_dir():
        cycle = kb_time_cycle(docs)
        print("===== graph =====")
        rc = max(rc, kb_cmd_graph(docs, cycle))
        print("===== corpus =====")
        rc = max(rc, kb_cmd_corpus(docs, cycle))
    return rc
```

## skills/agentic-sdlc-skill/scripts/sdlc_check.py:main

```python
def main(argv=None):
    return knowledge.main(argv)
```

## distributions/kb-agentic-skill/skills/kb-agentic-skill/scripts/sdlc_check.py:main

```python
def main(argv=None):
    return knowledge.main(argv)
```

## distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py:cmd_index

```python
def cmd_index(root):
    content = build_index(root)
    out = sdlc_core.ai_path(root) / "INDEX.md"
    out.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {out.relative_to(root).as_posix()}")
    # F-028: the workstream registry is generated here too. This entry point does
    # not reuse the spine's cmd_index, so wiring it explicitly is what keeps the
    # doctrine ("generated by mkt_check.py index") from being false in this lens.
    return max(sdlc_core.rc_registry(root), knowledge.kb_refresh_indexes(root / sdlc_core.docs_dir()))
```

## distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py:main

```python
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # Spine commands are the core's, identical in every distribution: hand over
    # every subcommand this overlay does not explicitly intercept, untouched,
    # rather than keeping a hand-copied list of spine names here -- which is how
    # `migrate` got dropped while SKILL.md kept promising it.
    if argv and not argv[0].startswith("-") and argv[0] not in OVERLAY_COMMANDS:
        return knowledge.main(argv)

    parser = argparse.ArgumentParser(prog="mkt_check.py", description=__doc__,
        epilog="Shared memory commands: recall QUERY, graph, corpus, claim-id, anchor, "
               "export, import, stale, orient. Use COMMAND --help for options.")
    parser.add_argument("command", choices=list(OVERLAY_COMMANDS))
    parser.add_argument("file", nargs="?", default=None,
                        help="optional target file for budget/funnel")
    parser.add_argument("--root", default=None, help="project root (contains the docs root)")
    parser.add_argument("--docs-dir", dest="docs_dir", default=None,
                        help="name of the documentation root (default: mkt_docs; "
                             "use --docs-dir ai_docs on a project that has migrated "
                             "to the family's single tree)")
    parser.add_argument("--strict", action="store_true",
                        help="warnings also fail the exit code")
    args = parser.parse_args(argv)

    # Resolve the docs root fresh on EVERY invocation, from this distribution's own
    # default: the core keeps it in module state, and an entry point that inherited
    # whatever a previous call left behind would be answering the wrong question.
    try:
        discovered, name = sdlc_core.resolve_docs_dir(args, args.root)
    except sdlc_core.AmbiguousDocsRoot as exc:
        print("[ERROR] %s" % exc)
        return 1
    root = find_root(args.root or discovered, name)
    if root is None:
        print(f"[ERROR] no {sdlc_core.docs_dir()}/ directory found "
              "(use --root or run mkt-sdlc-init)")
        return 2

    if args.command == "index":
        return cmd_index(root)

    runners = {
        "validate": lambda: run_validate(root),
        "ledger": lambda: run_ledger(root),
        "budget": lambda: run_budget(root, args.file),
        "funnel": lambda: run_funnel(root, args.file),
        "trace": lambda: run_trace(root),
    }
    if args.command == "check":
        rep = run_check(root)
    else:
        rep = runners[args.command]()
        rep.print(args.command)

    code = rep.exit_code(strict=args.strict)
    if args.command in ("validate", "check"):
        code = max(code, knowledge.kb_validate_surface(root / sdlc_core.docs_dir(),
                                                       full=args.command == "check"))
    if code == 0:
        print(f"[OK] {args.command} clean "
              f"({len(rep.warnings)} warning(s))" if rep.warnings else f"[OK] {args.command} clean")
    else:
        print(f"[FAIL] {args.command}: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    if args.command == "check":
        # This overlay REPLACES the spine's cmd_check, so the F-041 wiring note
        # must be re-attached here: it is check-layer behaviour, whoever owns
        # the check (fail-open and informational -- never the exit code).
        sdlc_core.print_orient_hook_note(root)
    return code
```
