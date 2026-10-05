# Shared project memory — exact software-evidence source excerpts

Captured from the implementation checkout; symbols label verbatim bodies, not execution evidence.

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

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_check_claims

```python
def kb_check_claims(root):
    """All mechanical claim checks over topics/*.md. Returns (errors, warnings,
    notes) as message lists. Findings only — never per-node status lines."""
    errors, warnings, notes = [], [], []
    topics = root / "topics"
    if not topics.is_dir():
        return errors, warnings, notes
    all_ids = {}     # id -> "file:line"
    all_rows = {}    # id -> (row, rel)
    # Frontmatter is now resolved for every row, GIVEN included, so a ledger
    # citing one artifact from 80 rows would otherwise stat and decode that
    # artifact's sidecar 80 times. Keyed by the cited path, per run.
    fm_cache = {}

    def _declaring_frontmatter(rel):
        if rel not in fm_cache:
            fm_cache[rel] = _note_frontmatter(root, rel)
        return fm_cache[rel]
    per_file_rows = []
    for p in sorted(topics.glob("*.md")):
        rel = "topics/" + p.name
        text = sdlc_core.read_text(p)
        rows, perrs = kb_parse_claims(text)
        meta = sdlc_core.load_frontmatter(text.splitlines()) or {}
        schema = kb_unquote(meta.get("claim_schema", "1"))
        if schema not in ("1", "2"):
            errors.append("%s: claim_schema must be 1 or 2" % rel)
        if schema == "2":
            section = text.split(CLAIM_HEADING, 1)[-1].split("\n## ", 1)[0]
            header = next((ln for ln in section.splitlines() if ln.strip().startswith("|")), "")
            if tuple(c.strip().lower() for c in header.strip().strip("|").split("|")) != TYPED_CLAIM_COLUMNS:
                errors.append("%s: claim_schema 2 requires the typed header" % rel)
        for line, msg in perrs:
            errors.append("%s:%d: %s" % (rel, line, msg))
        per_file_rows.append((rel, rows))
        for row in rows:
            where = "%s:%d" % (rel, row["_line"])
            if "kind" in row and row["kind"] not in CLAIM_KINDS:
                errors.append("%s: kind must be %s" % (where, "/".join(CLAIM_KINDS)))
            # --- source: resolve, confine, span-check ---
            sources = [s.strip() for s in row["source"].split(";") if s.strip()]
            if not sources:
                errors.append("%s: claim has no source" % where)
                continue
            first = sources[0]
            for src in sources:
                if "#" not in src:
                    errors.append("%s: source %r has no locator" % (where, src))
                    continue
                path_s, loc = src.rsplit("#", 1)
                target = sdlc_core.confine_under(root, path_s)
                if target is None:
                    errors.append("%s: source %r escapes the docs root" % (where, src))
                    continue
                if not target.is_file():
                    errors.append("%s: source %r does not resolve — a claim whose "
                                  "origin cannot be reopened is model knowledge"
                                  % (where, src))
                    continue
                kb_check_locator(target, loc, where, errors)
            # --- provenance ---
            prov = row["prov"]
            # Resolved ONCE, for every provenance: the non-GIVEN classes read it
            # for their required field, and GIVEN reads it to notice that the
            # artifact declares a weaker chain than the row claims.
            meta, meta_where = (None, "")
            if "#" in first:
                meta, meta_where = _declaring_frontmatter(first.rsplit("#", 1)[0])
            if prov not in PROVENANCES:
                errors.append("%s: prov %r not in %s" % (where, prov, "/".join(PROVENANCES)))
            elif prov in ("DERIVED", "RULING", "ELICITED", "IMPORTED"):
                if meta is None:
                    pass  # unresolvable source already reported
                elif prov == "DERIVED" and not meta.get("derived_from"):
                    errors.append("%s: DERIVED claim's source (%s) carries no "
                                  "'derived_from:' — model knowledge disguised as "
                                  "a source" % (where, meta_where))
                elif prov == "RULING" and not meta.get("basis"):
                    errors.append("%s: RULING source (%s) carries no 'basis:' — a "
                                  "preference is not a fact; no basis, no ruling"
                                  % (where, meta_where))
                elif prov == "IMPORTED" and not meta.get("imported_from"):
                    # F-030: IMPORTED exists so a foreign decision cannot pass for
                    # a local one. Without the origin the class says nothing and
                    # the row is a RULING with the label filed off.
                    errors.append("%s: IMPORTED source (%s) carries no "
                                  "'imported_from:' — the class exists to name "
                                  "whose decision this was; unnamed, it is a "
                                  "RULING in disguise" % (where, meta_where))
            elif prov == "GIVEN":
                # F-035: a row resting on an OCR, a transcription or a
                # translation is not the same evidence as one resting on a
                # deterministic text layer. The sidecar could say so only in
                # prose, and prose is not a check -- which is how three rows
                # whose evidence was a reading of an image passed as GIVEN.
                declared = ((meta or {}).get("provenance") or "").strip()
                if declared and declared.upper() != "GIVEN":
                    warnings.append(
                        "%s: prov GIVEN, but %s declares 'provenance: %s' — the "
                        "row reads as first-hand evidence and its artifact does "
                        "not. File the row at the provenance the chain actually "
                        "has, or correct the sidecar" % (where, meta_where, declared))
            # --- grammar cells ---
            try:
                kb_parse_scope(row["valid"])
            except ValueError as e:
                errors.append("%s: %s" % (where, e))
            try:
                qk = kb_qty_key(row["qty"])
            except ValueError as e:
                errors.append("%s: %s" % (where, e))
                qk = None
            if row["about"] not in ("", "-"):
                m = re.match(r"^([a-z0-9-]+) -> ([a-z0-9-]+)$", row["about"])
                if not m:
                    errors.append("%s: about must be '<predicate> -> <slug>' or '-'"
                                  % where)
            # --- atomicity hint (F-047): a row atomic as provenance can be
            # plural as meaning. Text cannot PROVE plurality, so this is a
            # note — never a warning or an error, never the exit code.
            hints = [h for h in KB_BUNDLE_HINTS if h in row["claim"]]
            if hints:
                notes.append("%s: claim text of %s reads like more than one "
                             "assertion (matched %s) — one row asserts one "
                             "thing; if it is a bundle, split it "
                             "(distillation.md section 3, reconciliation.md "
                             "section 'Splitting a bundled row'). Heuristic "
                             "only: a genuinely "
                             "single assertion needs no change"
                             % (where, row["id"] or "(id pending)",
                                ", ".join(repr(h) for h in hints)))
            # --- id: recompute, or note fill-pending ---
            if not row["id"]:
                notes.append("%s: id missing — fill-pending, run "
                             "'sdlc_check.py claim-id --fill %s'" % (where, rel))
            elif qk is not None and "#" in first:
                path_s, loc = first.rsplit("#", 1)
                expect = kb_claim_id(path_s, loc, qk)
                if row["id"] != expect:
                    errors.append("%s: id %s does not recompute from its first "
                                  "source (+qty) — expected %s; the text may be "
                                  "corrected freely, the provenance may not be "
                                  "moved silently" % (where, row["id"], expect))
            if row["id"]:
                if row["id"] in all_ids:
                    # F-035: one message served two different defects. Same id
                    # with the SAME text is a copied row. Same id with DIFFERENT
                    # text is a collision: kb_claim_id hashes path#locator#qty
                    # and excludes the text on purpose, so two distinct
                    # assertions about one span cannot be told apart. The source
                    # and qty do NOT discriminate -- the id already implies them.
                    prev_row = all_rows[row["id"]][0]

                    def _cell(r, k):
                        return (r[k] or "").strip()

                    def _first_src(r):
                        return (r["source"] or "").split(";")[0].strip()

                    same_text = _cell(prev_row, "claim") == _cell(row, "claim")
                    same_span = (_first_src(prev_row) == _first_src(row)
                                 and _cell(prev_row, "qty") == _cell(row, "qty"))
                    if same_text:
                        errors.append("%s: duplicate id %s (also at %s) — uniqueness "
                                      "is global across topics/" % (where, row["id"],
                                                                    all_ids[row["id"]]))
                    elif same_span:
                        # F-047: recommending a merge here was a trap — merging
                        # distinct assertions manufactures a bundled row, trading
                        # this mechanical error for a semantic one no check sees.
                        errors.append(
                            "%s: id %s collides with the row at %s — two "
                            "DIFFERENT rows cite the same span with the same "
                            "qty, and the id function cannot separate them (it "
                            "hashes path#locator#qty and excludes the text on "
                            "purpose). Narrow each locator to the sub-span that "
                            "carries its own assertion — narrow spans make "
                            "atomic rows id-distinct (on a stored .txt, "
                            "p=<page>@<a>-<b> reaches below a line). Merge ONLY "
                            "if the two rows state the same single assertion; "
                            "merging distinct assertions trades this mechanical "
                            "error for a semantic one no check can see — do not "
                            "edit the qty to break the tie"
                            % (where, row["id"], all_ids[row["id"]]))
                    else:
                        # Same id, different text AND different span: the id
                        # cannot have been computed from both rows, so it was
                        # hand-typed or left stale after a source was repointed.
                        # Saying "they cite the same span" here would name a
                        # cause that is provably not this one.
                        errors.append(
                            "%s: id %s is also on the row at %s, which cites a "
                            "different span — the id was not computed from this "
                            "row (hand-typed, or left stale after its source "
                            "moved). Run 'sdlc_check.py claim-id --fill %s'"
                            % (where, row["id"], all_ids[row["id"]], rel))
                else:
                    all_ids[row["id"]] = where
                    all_rows[row["id"]] = (row, rel)
    # --- state machine integrity, global ---
    for _, rows in per_file_rows:
        for row in rows:
            if not row["id"]:
                continue
            where = all_ids.get(row["id"], row["id"])
            state = row["state"]
            if state == "OK":
                continue
            m = re.match(r"^(CONTESTED|SUPERSEDED) ([0-9a-f, ]+)$", state)
            if not m:
                errors.append("%s: state must be OK, 'CONTESTED <id>[,..]' or "
                              "'SUPERSEDED <id>[,..]': %r" % (where, state))
                continue
            kind = m.group(1)
            targets = [t.strip() for t in m.group(2).split(",") if t.strip()]
            for t in targets:
                other = all_rows.get(t)
                if other is None:
                    errors.append("%s: %s points at id %s which resolves to no row "
                                  "— deleting one side of a disagreement breaks "
                                  "the check, it does not clean up" % (where, kind, t))
                    continue
                orow, _ = other
                if row.get("kind") and orow.get("kind"):
                    if row["kind"] != orow["kind"]:
                        errors.append("%s: %s cannot connect different claim kinds (%s / %s)"
                                      % (where, kind, row["kind"], orow["kind"]))
                elif row.get("kind") or orow.get("kind"):
                    warnings.append("%s: related legacy claim %s has unclassified kind; re-verify"
                                    % (where, t))
                if kind == "SUPERSEDED" and orow["prov"] == "IMPORTED":
                    # F-030, owner ruling 2026-08-03: knowledge crosses a project
                    # boundary, authority does not. An IMPORTED row carries another
                    # owner's decision; letting it supersede a local row would make
                    # that decision binding here without anyone here granting it.
                    # Re-ratify first: write your own ruling note with your own
                    # basis and flip the row to RULING.
                    errors.append("%s: SUPERSEDED by %s, which is IMPORTED — a "
                                  "foreign decision cannot settle a local row. "
                                  "Re-ratify it (own note, own 'basis:', prov "
                                  "RULING) or resolve this some other way"
                                  % (where, t))
                if kind == "CONTESTED":
                    if orow["state"].startswith("SUPERSEDED"):
                        errors.append("%s: CONTESTED points at SUPERSEDED row %s — "
                                      "the set must be rewritten when a member is "
                                      "superseded" % (where, t))
                    elif not (orow["state"].startswith("CONTESTED")
                              and row["id"] in orow["state"]):
                        errors.append("%s: CONTESTED is not symmetric — %s does not "
                                      "name %s back; one flipped cell must never "
                                      "silently end a disagreement"
                                      % (where, t, row["id"]))
    return errors, warnings, notes
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_kb_read_bytes

```python
def _kb_read_bytes(base, rel, limit=None):
    path = _kb_safe_path(base, rel)
    before = path.stat()
    if not stat.S_ISREG(before.st_mode):
        raise ValueError("not a regular file: %s" % rel)
    if limit is not None and before.st_size > limit:
        raise ValueError("source exceeds %d bytes" % limit)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    with os.fdopen(os.open(path, flags), "rb") as source:
        opened = os.fstat(source.fileno())
        if not stat.S_ISREG(opened.st_mode):
            raise ValueError("not a regular source")
        data = source.read() if limit is None else source.read(limit + 1)
        after = os.fstat(source.fileno())
    current = _kb_safe_path(base, rel).stat()
    signature = lambda s: (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns)
    if any(signature(s) != signature(before) for s in (opened, after, current)):
        raise ValueError("source changed during capture: %s" % rel)
    if limit is not None and len(data) > limit:
        raise ValueError("source exceeds %d bytes" % limit)
    return data
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_kb_capture_lock

```python
@contextlib.contextmanager
def _kb_capture_lock(docs):
    lock = _kb_safe_path(docs, ".software-capture.lock")
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    except FileExistsError:
        raise ValueError("capture lock exists; another capture may be active; inspect before removing a stale lock")
    try:
        os.close(fd)
        yield
    finally:
        _kb_safe_path(docs, lock.name).unlink()
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_kb_project_id

```python
def _kb_project_id(docs, create):
    path = _kb_safe_path(docs, "README.md")
    raw = _kb_read_bytes(docs, "README.md") if path.exists() else b""
    meta = _kb_software_frontmatter(raw)
    pid = kb_unquote(meta.get("knowledge_project_id"))
    if "knowledge_project_id" in meta:
        if not pid or str(uuid.UUID(pid)) != pid:
            raise ValueError("knowledge_project_id must be one canonical UUID")
        return pid
    if not create:
        return None
    pid = str(uuid.uuid4())
    newline = b"\r\n" if b"\r\n" in raw else b"\n"
    entry = b"knowledge_project_id: " + pid.encode("ascii") + newline
    bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
    body = raw[len(bom):]
    if body.splitlines()[:1] == [b"---"]:
        offset = body.index(b"\n") + 1
        updated = bom + body[:offset] + entry + body[offset:]
    else:
        updated = bom + b"---" + newline + entry + b"---" + newline + body
    # README is mutable; source artifacts below never use replace. Refuse an
    # external edit noticed since our read instead of overwriting it.
    fd, stage = tempfile.mkstemp(prefix=".knowledge-id-", dir=docs)
    try:
        with os.fdopen(fd, "wb") as out:
            out.write(updated)
        current = _kb_read_bytes(docs, "README.md") if path.exists() else b""
        if current != raw:
            raise ValueError("README changed during identity creation; retry")
        _kb_safe_path(docs, "README.md")
        os.replace(stage, path)
    finally:
        if os.path.exists(stage):
            os.unlink(stage)
    return pid
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:_kb_software_integrity

```python
def _kb_software_integrity(docs, rel, meta):
    binding = kb_software_meta(meta)
    recorded = (meta.get("sha256") or "").strip()
    if binding or recorded:
        raw = _kb_read_bytes(docs, rel)
        digest = hashlib.sha256(raw).hexdigest()
        if recorded != digest:
            raise ValueError("stored source digest mismatch: raw-byte digest changed since ingest")
    if binding is None:
        return None
    entries = [_kb_relative(e) for e in _kb_df_entries(meta.get("derived_from"))]
    if Path(rel).name != _kb_binding_name(binding, digest, entries):
        raise ValueError("source name does not match content/binding")
    return binding
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_capture_source

```python
def kb_capture_source(project, docs, rel, start, end, role, derived_from=()):
    """Select bytes; store evidence, never a claim or an extraction-complete flag."""
    import datetime
    rel = _kb_relative(rel)
    if kb_unquote(rel.strip()) != rel:
        raise ValueError("source path cannot round-trip through metadata")
    if role not in SOFTWARE_ROLES or not (isinstance(start, int) and isinstance(end, int)
                                         and 1 <= start <= end):
        raise ValueError("capture requires role code/test/config/result and an inclusive 1-based span")
    docs = Path(docs).absolute()
    docs_rel = docs.relative_to(Path(project).absolute()).as_posix()
    _kb_safe_path(project, docs_rel + "/README.md")
    _kb_safe_path(docs, "corpus/given/source.txt")
    # Validate UUID/README syntax before reading the requested software file.
    kb_project_id(docs)
    raw = _kb_read_bytes(project, rel, SOFTWARE_MAX_BYTES)
    try:
        lines = raw.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        raise ValueError("capture requires UTF-8 source bytes")
    if end > len(lines):
        raise ValueError("capture span extends beyond source lines")
    extract = "".join(lines[start-1:end]).encode("utf-8")
    entries = sorted(set(_kb_relative(str(e)) for e in derived_from))
    for entry in entries:
        if any(c in entry for c in ",[]") or kb_unquote(entry.strip()) != entry:
            raise ValueError("derived_from path cannot round-trip through metadata")
        try:
            _kb_read_bytes(docs, entry)
        except OSError as exc:
            raise ValueError("derived_from cannot be reopened: %s" % entry) from exc
    digest = hashlib.sha256(extract).hexdigest()
    with _kb_capture_lock(docs):
        binding = dict(zip(SOFTWARE_FIELDS, (
            "1", _kb_project_id(docs, True), rel, hashlib.sha256(raw).hexdigest(),
            "%d-%d" % (start, end), role)))
        name = _kb_binding_name(binding, digest, entries)
        artifact, side = "corpus/given/" + name, "corpus/given/" + name + ".meta.md"
        _kb_safe_path(project, rel)
        meta = dict(sha256=digest, date=datetime.date.today().isoformat(),
                    provenance="GIVEN", extractor="utf8-lines-v1", **binding)
        if entries:
            meta["derived_from"] = "[" + ", ".join(entries) + "]"
        side_path = _kb_safe_path(docs, side)
        if side_path.exists():
            existing = _kb_software_frontmatter(_kb_read_bytes(docs, side))
            _kb_software_integrity(docs, artifact, existing)
            if (kb_software_meta(existing) != binding
                    or sorted(set(_kb_df_entries(existing.get("derived_from")))) != entries
                    or existing.get("provenance") != "GIVEN"
                    or existing.get("extractor") != "utf8-lines-v1"):
                raise ValueError("existing sidecar has different acquisition metadata")
            return artifact, side, False
        _kb_publish(docs, artifact, extract)
        side_bytes = ("---\n" + "\n".join(k + ": " + v for k, v in meta.items()) + "\n---\n").encode("utf-8")
        _kb_publish(docs, side, side_bytes)
        return artifact, side, True
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_software_findings

```python
def kb_software_findings(project, docs, topics=()):
    """Read-only evidence projection. MATCHED proves only declared byte inputs.

    supports are {source, status, reason, premises:[support,...]}; AND within a
    derivation, OR across a claim's supports. State and kind are never rewritten.
    """
    rev, metas, superseded, dangling = kb_source_graph(docs)
    forward = {}
    for source, dependents in rev.items():
        for owner in dependents:
            forward.setdefault(owner, []).append(source)
    errors, sources, cache = [], {}, {}
    try:
        pid = kb_project_id(docs) if project is not None else None
    except (OSError, ValueError) as exc:
        pid = None
        errors.append("project identity: %s" % exc)
    bad_owners = {owner for owner, _ in dangling}

    def support(rel, active=()):
        if rel in active or len(active) >= 200:
            errors.append("derivation cycle: %s" % " -> ".join(active + (rel,)))
            return dict(source=rel, status="INVALID", reason="derivation cycle", premises=[])
        if rel in cache:
            return cache[rel]
        status, reason, premises = "UNTRACKED", "no software binding", []
        try:
            meta = metas.get(rel)
            if meta is None:
                meta = _kb_source_meta(docs, rel)
            if "_error" in meta:
                raise ValueError(meta["_error"])
            if rel in bad_owners:
                raise ValueError("derived_from missing or cannot resolve: %s" % rel)
            binding = _kb_software_integrity(docs, rel, meta)
            if binding:
                if pid != binding["software_project_id"]:
                    status, reason = "UNBOUND", "project identity absent or different; software path not opened"
                else:
                    try:
                        live = _kb_safe_path(project, binding["software_path"])
                        info = live.stat()
                        if not stat.S_ISREG(info.st_mode):
                            raise ValueError("not a regular software file")
                        # A captured input is bounded. Growing beyond that bound
                        # proves drift without reading an unbounded new file.
                        matched = (info.st_size <= SOFTWARE_MAX_BYTES and
                                   hashlib.sha256(_kb_read_bytes(project, binding["software_path"], SOFTWARE_MAX_BYTES)).hexdigest()
                                   == binding["software_sha256"])
                        status = "MATCHED" if matched else "CHANGED"
                        reason = "declared file bytes match" if matched else "declared file bytes changed; re-verify"
                    except OSError:
                        status, reason = "UNAVAILABLE", "declared software file missing or unreadable"
            parents = sorted(forward.get(rel, ()))
            # A source outside the preloaded corpus may itself be a derivation.
            if not parents and meta.get("derived_from"):
                for entry in _kb_df_entries(meta["derived_from"]):
                    target = _kb_resolve_source(docs, entry)
                    if target is None:
                        raise ValueError("derived_from missing: %s" % entry)
                    parents.append(target)
            premises = [support(p, active + (rel,)) for p in parents]
            if premises:
                states = [p["status"] for p in premises] + ([status] if binding else [])
                status = next((s for s in ("INVALID", "CHANGED", "UNAVAILABLE", "UNBOUND", "UNTRACKED") if s in states), "MATCHED")
                reason = "all declared premises match" if status == "MATCHED" else "a declared premise needs re-verification"
            if rel in superseded or meta.get("status") == "SUPERSEDED":
                status, reason = "UNTRACKED", "historical source is superseded; follow its successor"
        except (OSError, ValueError) as exc:
            status, reason = "INVALID", str(exc)
            errors.append("%s: %s" % (rel, exc))
        item = dict(source=rel, status=status, reason=reason, premises=premises)
        sources[rel] = (rel, status, reason)
        cache[rel] = item
        return item

    claims = []
    all_topics = {}
    try:
        folder = _kb_safe_path(docs, "topics/.probe").parent
        for path in sorted(folder.glob("*.md")):
            if path.name == "INDEX.md":
                continue
            text = _kb_read_bytes(docs, "topics/" + path.name).decode("utf-8-sig")
            meta = _kb_software_frontmatter(text.encode("utf-8"))
            slug = kb_unquote(meta.get("topic")) or path.stem
            if slug in all_topics:
                errors.append("duplicate topic: %s" % slug)
            all_topics[slug] = (path, text, kb_parse_claims(text)[0])
    except (OSError, ValueError) as exc:
        errors.append("topics: %s" % exc)
    wanted = set(topics) if topics else set(all_topics)
    for missing in sorted(wanted - set(all_topics)):
        errors.append("no such topic: %s" % missing)
    for slug in sorted(wanted & set(all_topics)):
        path, text, rows = all_topics[slug]
        _, parse_errors = kb_parse_claims(text)
        errors.extend("%s:%s: %s" % (slug, ln, msg) for ln, msg in parse_errors)
        meta = _kb_software_frontmatter(text.encode("utf-8"))
        schema = kb_unquote(meta.get("claim_schema", "1"))
        if schema not in ("1", "2") or (schema == "2" and any("kind" not in r for r in rows)):
            errors.append("%s: invalid claim_schema or missing typed kind column" % slug)
        for row in rows:
            for src in row["source"].split(";"):
                try:
                    rel, loc = src.strip().rsplit("#", 1)
                    target = _kb_safe_path(docs, rel)
                    if LOC_PAGE_RE.match(loc):
                        _kb_safe_path(docs, str(Path(rel).with_suffix(".txt")).replace("\\", "/"))
                    if not target.is_file():
                        raise ValueError("source missing")
                    kb_check_locator(target, loc, slug, errors)
                except (OSError, ValueError) as exc:
                    errors.append("%s: invalid source %r: %s" % (slug, src, exc))
            supports = [support(rel) for rel in kb_claim_sources(row)]
            kind = row.get("kind", "UNCLASSIFIED")
            if kind not in CLAIM_KINDS and kind != "UNCLASSIFIED":
                errors.append("%s: invalid claim kind %s" % (slug, kind))
            claims.append((slug, row["id"], kind, row["state"], supports))
    # Orphan bindings are still checkable; no repository scan, just known corpus.
    if not topics:
        for rel, meta in sorted(metas.items()):
            if any(k.startswith("software_") for k in meta):
                support(rel)
    return {"errors": sorted(set(errors)), "sources": sorted(sources.values()), "claims": claims}
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_cmd_evidence

```python
def kb_cmd_evidence(project, docs, topics=(), json_output=False):
    report = kb_software_findings(project, docs, topics)
    if json_output:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Evidence: declared inputs only; no semantic or completeness certification.")
        def show_support(item, depth=1):
            print("%s%s %s: %s" % ("  " * depth, item["status"], item["source"], item["reason"]))
            for premise in item["premises"]:
                show_support(premise, depth + 1)
        if not report["claims"]:
            print("no coverage: no selected claims")
        for slug, cid, kind, state, supports in report["claims"]:
            print("%s %s kind=%s state=%s" % (slug, cid, kind, state))
            for item in supports:
                show_support(item)
        for error in report["errors"]:
            print("[ERROR] %s" % error)
    needs_review = any(kind == "UNCLASSIFIED" or state != "OK"
                       or (kind == "OBSERVATION" and not any(s["status"] == "MATCHED" for s in supports))
                       for _, _, kind, state, supports in report["claims"])
    return 1 if report["errors"] or needs_review else 0
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_export_closure

```python
def kb_export_closure(docs, slugs):
    """(topics, artifacts, added_for_conflicts, errors).

    Closure in two directions, because a partial export produces a target whose
    own checks fail:
      * every artifact a selected claim cites travels with it -- a claim whose
        source cannot be reopened is model knowledge arriving by another route;
      * every row a CONTESTED row points at travels too, since the symmetry
        check refuses a set that lost half its members. When such a row lives in
        an unselected topic, that topic is ADDED and reported, never dropped.
    """
    all_topics = kb_collect_topics(docs)
    errors = []
    for s in slugs:
        if s not in all_topics:
            errors.append("no such topic: %s" % s)
    if errors:
        return {}, [], [], errors
    selected = dict((s, all_topics[s]) for s in slugs)
    # id -> slug, over the WHOLE graph, so a conflict partner is findable
    owner_of = {}
    for slug, (_p, _t, rows) in all_topics.items():
        for r in rows:
            if r["id"]:
                owner_of[r["id"]] = slug
    added = []
    pending = list(selected)
    while pending:
        slug = pending.pop()
        for r in selected[slug][2]:
            m = re.match(r"^(CONTESTED|SUPERSEDED) ([0-9a-f, ]+)$", r["state"].strip())
            if not m:
                continue
            for ref in [x.strip() for x in m.group(2).split(",") if x.strip()]:
                other = owner_of.get(ref)
                if other is None:
                    errors.append("claim %s in topic '%s' points at id %s, which "
                                  "no topic owns: export would carry a broken set"
                                  % (r["id"] or "(no id)", slug, ref))
                elif other not in selected:
                    selected[other] = all_topics[other]
                    added.append(other)
                    pending.append(other)
    artifacts, seen, active = [], set(), set()

    def include(rel, required=True):
        if rel in active:
            errors.append("derivation cycle at %s" % rel)
            return
        if rel in seen:
            return
        try:
            path = _kb_safe_path(docs, rel)
            if not path.is_file():
                if required:
                    errors.append("missing source: %s" % rel)
                return
            active.add(rel)
            seen.add(rel)
            artifacts.append(rel)
            meta = _kb_source_meta(docs, rel)
            _kb_software_integrity(docs, rel, meta)
            side = _kb_safe_path(docs, rel + ".meta.md")
            if side.is_file() and rel + ".meta.md" not in seen:
                seen.add(rel + ".meta.md")
                artifacts.append(rel + ".meta.md")
            # A transitive premise needs its canonical extraction too, not just
            # sources directly named in claim cells.
            if path.suffix and path.suffix != ".txt":
                include(rel[:-len(path.suffix)] + ".txt", required=False)
            for entry in _kb_df_entries(meta.get("derived_from")):
                source = _kb_resolve_source(docs, entry)
                if source is None:
                    errors.append("%s: derived_from cannot resolve %s" % (rel, entry))
                else:
                    include(source)
        except (OSError, ValueError) as exc:
            errors.append("%s: %s" % (rel, exc))
        finally:
            active.discard(rel)

    for slug, (_p, _t, rows) in sorted(selected.items()):
        _, perrs = kb_parse_claims(_t)
        errors.extend("%s:%s: %s" % (slug, line, msg) for line, msg in perrs)
        for r in rows:
            for rel in kb_claim_sources(r):
                include(rel)
    return selected, artifacts, added, errors
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_import_plan

```python
def kb_import_plan(bundle, docs):
    """(writes, skipped_topics, dedup, errors) -- computed BEFORE anything is
    written, because an import that half-applies leaves a tree whose checks fail
    and whose owner cannot tell what landed."""
    errors, writes, skipped, dedup = [], [], [], []
    man = bundle / BUNDLE_MANIFEST
    if not man.is_file():
        return [], [], [], ["not a kb bundle: no %s in %s" % (BUNDLE_MANIFEST, bundle)]
    meta = sdlc_core.load_frontmatter(sdlc_core.read_text(man).splitlines()) or {}
    if str(meta.get("kb_bundle", "")).strip() != "1":
        return [], [], [], ["%s carries no 'kb_bundle: 1'" % BUNDLE_MANIFEST]

    known_ids = set()
    target = kb_collect_topics(docs)
    for _slug, (_p, _t, rows) in target.items():
        for r in rows:
            if r["id"]:
                known_ids.add(r["id"])

    for p in sorted(bundle.rglob("*")):
        if not p.is_file() or p.name == BUNDLE_MANIFEST:
            continue
        rel = p.relative_to(bundle).as_posix()
        if rel == "README.md":
            continue  # a bundle never adopts the exporter project identity
        try:
            _kb_safe_path(bundle, rel)
            _kb_safe_path(docs, rel)
        except (OSError, ValueError) as exc:
            errors.append("%s: %s" % (rel, exc))
            continue
        dst = sdlc_core.confine_under(docs, rel)
        if dst is None:
            errors.append("bundle entry %r escapes the docs root — refusing the "
                          "whole import, not just this file" % rel)
            continue
        if dst.is_file() and not rel.startswith("topics/"):
            if kb_sha256_bytes(dst) != kb_sha256_bytes(p):
                errors.append("%s exists with different bytes (target %s… vs "
                              "bundle %s…): content-addressed names must mean "
                              "equal content" % (rel, kb_sha256_bytes(dst)[:8],
                                                 kb_sha256_bytes(p)[:8]))
            continue
        if rel.startswith("topics/") and dst.is_file():
            skipped.append(rel)
            continue
        writes.append((rel, p, dst))

    for rel, p, _dst in writes:
        if not rel.startswith("topics/"):
            continue
        rows, perrs = kb_parse_claims(sdlc_core.read_text(p))
        errors.extend("%s:%s: %s" % (rel, line, msg) for line, msg in perrs)
        for r in rows:
            if r["id"] and r["id"] in known_ids:
                dedup.append(r["id"])
    return writes, skipped, dedup, errors
```

## skills/agentic-sdlc-skill/scripts/knowledge.py:kb_validate_surface

```python
def kb_validate_surface(docs, full=False, project=None):
    """Additive seam for marketing: preserve its own validator and report."""
    rc = max(memory_validate(docs), _kb_extra_validate(docs))
    if full and ((docs / "topics").is_dir() or (docs / "corpus").is_dir()):
        cycle = kb_time_cycle(docs)
        rc = max(rc, kb_cmd_graph(docs, cycle), kb_cmd_corpus(docs, cycle))
        rc = max(rc, _kb_evidence_diagnostics(project, docs))
    return rc
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
        rc = max(rc, _kb_evidence_diagnostics(root, docs))
    return rc
```

## distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py:cmd_index

```python
def cmd_index(root):
    if sdlc_core.docs_dir() == "ai_docs":
        return max(sdlc_core.cmd_index(root),
                   knowledge.kb_refresh_indexes(root / "ai_docs"))
    content = build_index(root)
    out = sdlc_core.ai_path(root) / "INDEX.md"
    out.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {out.relative_to(root).as_posix()}")
    # F-028: the workstream registry is generated here too. This entry point does
    # not reuse the spine's cmd_index, so wiring it explicitly is what keeps the
    # doctrine ("generated by mkt_check.py index") from being false in this lens.
    return max(sdlc_core.rc_registry(root), knowledge.kb_refresh_indexes(root / sdlc_core.docs_dir()))
```

## distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc/scripts/mkt_check.py:run_check

```python
def run_check(root):
    rep = Report()
    checks = [("validate", run_validate)]
    if sdlc_core.docs_dir() != "ai_docs" or has_marketing_engagement(root):
        checks += [("ledger", run_ledger), ("budget", run_budget),
                   ("funnel", run_funnel), ("trace", run_trace)]
    for title, fn in checks:
        sub = fn(root)
        sub.print(title)
        rep.merge(sub)
    return rep
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
               "capture-source, evidence, export, import, stale, orient. Use COMMAND --help for options.")
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
        if sdlc_core.docs_dir() == "ai_docs":
            code = max(code, sdlc_core.cmd_validate(root, strict=args.strict))
        code = max(code, knowledge.kb_validate_surface(root / sdlc_core.docs_dir(),
                                                       full=args.command == "check", project=root))
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

## distributions/course-creator/skills/course-creator/scripts/sdlc_check.py:main

```python
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "course":
        parser = argparse.ArgumentParser(prog="sdlc_check.py course")
        parser.add_argument("command", choices=("course",))
        parser.add_argument("slug")
        parser.add_argument("--root")
        parser.add_argument("--strict", action="store_true")
        args = parser.parse_args(argv)
        root = Path(args.root).resolve() if args.root else sdlc_core.find_project_root()
        if root is None:
            print("[ERROR] no project root found")
            return 2
        return _report(course_check.validate_course(
            root, root / "ai_docs/solutions/courses" / args.slug), strict=args.strict)
    if not argv or argv[0] not in ("validate", "check"):
        return knowledge.main(argv)
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("command")
    parser.add_argument("--root")
    parser.add_argument("--strict", action="store_true")
    args, _ = parser.parse_known_args(argv)
    rc = knowledge.main(argv)
    if sdlc_core.docs_dir() != "ai_docs":
        return rc
    root = Path(args.root).resolve() if args.root else sdlc_core.find_project_root()
    if root is None:
        return rc
    return max(rc, _report(course_check.validate_all(root), strict=args.strict))
```
