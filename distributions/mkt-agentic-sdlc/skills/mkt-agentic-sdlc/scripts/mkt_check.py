#!/usr/bin/env python3
"""mkt_check.py -- the MARKETING domain entry point.

The family's shared spine lives in `sdlc_core.py`, byte-identical in every
distribution; this file is the marketing OVERLAY on top of it. It is deliberately
not thin: a marketing plan is not a set of ANALYSIS documents, so the document
model (`vision/ strategy/ tactics/ deliverables/`, the evidence ledger, the budget
and funnel arithmetic) is genuinely this domain's own and stays here. What
converges is the spine, not the paperwork.

From the overlay (unchanged behaviour, unchanged exit codes):
  check    [--root R] [--strict]   run validate + ledger + budget + funnel + trace
  validate [--root R] [--strict]   frontmatter + index freshness on canonical docs
  ledger   [--root R]              evidence ledger integrity + [EV-nn] reference resolution
  budget   [--root R] [FILE]       budget allocation sums to Total budget (+/-1%)
  funnel   [--root R] [FILE]       funnel model rows recompute (+/-5%)
  trace    [--root R]              objective -> tactic -> KPI chain
  index    [--root R]              (re)generate INDEX.md

From the shared core (new to this distribution):
  stale / mark / gate / orient / plan / migrate   -- the spine commands, identical everywhere

Both files must sit in the same directory. Copying only this one fails at import,
loudly, which is the intended failure.

Docs root: `mkt_docs/` by default. `--docs-dir ai_docs` reaches a migrated project,
which is what makes the move to the family's single tree possible at all.

Exit codes: 0 clean (warnings allowed unless --strict), 1 errors (or warnings
under --strict), 2 usage / structural problem (no docs root).

Pure stdlib. ASCII output only (Windows-console safe).
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by the copied-file test
    sys.stderr.write(
        "[ERROR] mkt_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator ships as TWO files since the multi-domain core.\n"
        "        Copy both, or run sdlc_core.py directly.\n")
    sys.exit(1)

# This distribution IS the marketing lens. The default docs root is its own; the
# core still resolves `--docs-dir` and the env seam on top of it, so a project that
# has migrated to the family's single `ai_docs/` tree is reachable from here too.
DOMAIN = "marketing"
MKT_DOCS_DIR = "mkt_docs"
sdlc_core.set_entry_point(DOMAIN, provides=("marketing",), script="mkt_check.py")
sdlc_core.set_docs_dir(MKT_DOCS_DIR)

sdlc_core.set_profile(
    skill_name="mkt-agentic-sdlc",
    unit_noun="engagement",
    support_files=("templates.md", "frameworks.md", "research.md", "elicitation.md",
                   "review.md", "routing.md", "guides.md", "vision.md", "dispatch.md",
                   "ENFORCEMENT.md"),
    capabilities=(
        # spine
        "triage", "write_triggers", "workstream_registry", "vision_gate",
        "design_review_gate", "guide_router", "worktree_hygiene",
        # marketing overlay
        "subagent_dispatch", "question_discipline",
    ),
    # The strategy is reviewed before any tactic is executed: nine phases, but the
    # ordering the gate cares about is the same one every domain owes.
    design_gate_between=("### 6. Strategy", "### 8. Action"),
)

# The subcommands this overlay implements itself. Anything else on the command
# line is handed straight to the shared core, so a spine command this file never
# heard of (as `migrate` once was) cannot be silently dropped by a stale list here.
OVERLAY_COMMANDS = ("check", "validate", "ledger", "budget", "funnel", "trace", "index")

CANONICAL_DIRS = ("vision", "strategy", "tactics", "deliverables")
VALID_STATUS = ("CURRENT", "SUPERSEDED", "DRAFT", "DEPRECATED")
LEDGER_CLASSES = ("FACT", "BENCHMARK", "ASSUMPTION")
CONFIDENCE_VALUES = ("HIGH", "MED", "MEDIUM", "LOW")
EV_REF = re.compile(r"\[(EV-\d+)\]")
# A source that points INSIDE this engagement instead of at the world: a document of
# OUR OWN under a canonical dir, or the "see X" form. Only FACT can carry it today,
# because FACT is the one class the URL rule does not reach.
INTERNAL_SOURCE_RE = re.compile(
    r"(?:\b(?:mkt_docs|ai_docs|research|strategy|tactics|deliverables|vision)/\S*\.md\b"
    r"|\b(?:see|vedi|cfr\.?)\s)", re.IGNORECASE)
# The two origins research.md sanctions for a FACT. A cell that opens by naming the
# client is exempt: their own primary data may well be a Markdown file they handed
# over, and telling its author to "reclassify as BENCHMARK and add a URL" would be
# advice to misclassify.
CLIENT_ORIGIN_RE = re.compile(
    r"^\s*(?:user|client|owner|utente|cliente|titolare|proprietario)\b", re.IGNORECASE)
OBJECTIVE_HEADING = re.compile(r"^###\s+(O\d+)\b", re.MULTILINE)
OBJECTIVE_TOKEN = re.compile(r"\bO\d+\b")
EXAMPLE_MARKER = "(example)"

BUDGET_TOLERANCE = 0.01   # ±1% on allocation sum
FUNNEL_TOLERANCE = 0.05   # ±5% on recomputed funnel cells


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, msg):
        self.errors.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def merge(self, other):
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)

    def print(self, title):
        for w in self.warnings:
            print(f"[WARN]  {title}: {w}")
        for e in self.errors:
            print(f"[ERROR] {title}: {e}")

    def exit_code(self, strict=False):
        if self.errors:
            return 1
        if strict and self.warnings:
            return 1
        return 0


# ---------------------------------------------------------------- helpers

def find_root(root_arg, docs_dir=None):
    """Resolve the project root: --root wins, else walk up from cwd.

    The docs-root NAME comes from the core (`--docs-dir`, then the env seam, then
    discovery, then this distribution's `mkt_docs`), so one project mid-migration
    cannot be validated half under one root and half under the other.
    """
    if docs_dir:
        sdlc_core.set_docs_dir(docs_dir)
    name = sdlc_core.docs_dir()
    if root_arg:
        root = Path(root_arg).resolve()
        return root if (root / name).is_dir() else None
    cur = Path.cwd().resolve()
    for candidate in (cur, *cur.parents):
        if (candidate / name).is_dir():
            return candidate
    return None


def read_text(path):
    return path.read_text(encoding="utf-8", errors="replace")


def load_frontmatter(text):
    """Return (dict, body). Tolerant: missing frontmatter -> ({}, text)."""
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    fm = {}
    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return fm, "\n".join(lines[i + 1:])
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if m:
            fm[m.group(1).strip()] = m.group(2).strip()
    return {}, text  # unterminated frontmatter: treat as body


def parse_num(cell):
    """Parse a table-cell number: strips currency symbols, spaces, commas,
    percent signs and [EV-nn] refs; supports k/M suffix. Returns float or None."""
    if cell is None:
        return None
    s = EV_REF.sub("", cell)
    s = re.sub(r"[^\dkKmM.,%-]", "", s.strip())
    s = s.replace(",", "").replace("%", "")
    if not s:
        return None
    mult = 1.0
    if s and s[-1] in "kK":
        mult, s = 1_000.0, s[:-1]
    elif s and s[-1] in "mM":
        mult, s = 1_000_000.0, s[:-1]
    try:
        return float(s) * mult
    except ValueError:
        return None


def parse_tables(text):
    """Return every markdown table as (header_cells_lower, rows) where each
    row is a dict {header_lower: cell}."""
    tables = []
    lines = text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines) \
                and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1].strip()):
            headers = [h.strip().lower() for h in line.strip("|").split("|")]
            rows = []
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) >= len(headers) - 1:  # tolerate ragged tail
                    row = {}
                    for k, h in enumerate(headers):
                        row[h] = cells[k] if k < len(cells) else ""
                    rows.append(row)
                j += 1
            tables.append((headers, rows))
            i = j
        else:
            i += 1
    return tables


def find_table(text, required_cols):
    """First table whose header contains every required column (contains-match)."""
    req = [c.lower() for c in required_cols]
    for headers, rows in parse_tables(text):
        if all(any(r in h for h in headers) for r in req):
            return headers, rows
        # exact-name pass for short names like 'kpi'
        if all(r in headers for r in req):
            return headers, rows
    return None, None


def col(row, name):
    """Fetch a cell by contains-match on the header name."""
    name = name.lower()
    if name in row:
        return row[name]
    for h, v in row.items():
        if name in h:
            return v
    return None


def is_example_row(row):
    return any(EXAMPLE_MARKER in (v or "") for v in row.values())


def close_enough(stated, computed, tol):
    if stated is None or computed is None:
        return True  # missing cells reported separately
    if computed == 0:
        return abs(stated) < 1e-9
    return abs(stated - computed) / abs(computed) <= tol


def canonical_files(root):
    docs = sdlc_core.ai_path(root)
    for d in CANONICAL_DIRS:
        base = docs / d
        if base.is_dir():
            for p in sorted(base.rglob("*.md")):
                yield p


def all_md_files(root):
    docs = sdlc_core.ai_path(root)
    for p in sorted(docs.rglob("*.md")):
        yield p


# ---------------------------------------------------------------- index

def build_index(root):
    docs = sdlc_core.ai_path(root)
    lines = [
        "# mkt_docs INDEX (generated by mkt_check.py index -- do not edit by hand)",
        "",
        "| Path | Description | Status |",
        "|---|---|---|",
    ]
    for p in canonical_files(root):
        if p.name == "INDEX.md":
            continue
        fm, body = load_frontmatter(read_text(p))
        desc = fm.get("description", "")
        status = fm.get("status", "")
        if not desc:
            h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            desc = h1.group(1).strip() if h1 else ""
        rel = p.relative_to(docs).as_posix()
        lines.append(f"| {rel} | {desc} | {status} |")
    return "\n".join(lines) + "\n"


def cmd_index(root):
    content = build_index(root)
    out = sdlc_core.ai_path(root) / "INDEX.md"
    out.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {out.relative_to(root).as_posix()}")
    # F-028: the workstream registry is generated here too. This entry point does
    # not reuse the spine's cmd_index, so wiring it explicitly is what keeps the
    # doctrine ("generated by mkt_check.py index") from being false in this lens.
    return sdlc_core.rc_registry(root)


# ---------------------------------------------------------------- validate

def run_validate(root):
    rep = Report()
    docs = sdlc_core.ai_path(root)
    # F-028: the generated registry against its HANDOFF_*.md sources. Gated on
    # source presence, so a project that has not converted sees nothing new.
    workstreams = sdlc_core.list_workstreams(root)
    if workstreams:
        hand = docs / "audit" / "handoff.md"
        if not hand.is_file():
            rep.error("audit/handoff.md missing while HANDOFF_*.md sources exist: "
                      "run 'mkt_check.py index'")
        elif sdlc_core.norm_text(read_text(hand)) !=                 sdlc_core.norm_text(sdlc_core.build_registry(root)):
            rep.error("audit/handoff.md not aligned with its HANDOFF_*.md sources: "
                      "run 'mkt_check.py index'. A merge resolved by hand is exactly "
                      "what this catches")
        if len(workstreams) > sdlc_core.REGISTRY_CAP:
            rep.warn(f"{len(workstreams)} open workstreams: the registry is meant to "
                     f"stay under {sdlc_core.REGISTRY_CAP}")
    known = {p.name for p in docs.rglob("*.md")}
    for p in canonical_files(root):
        if p.name == "INDEX.md":
            continue
        rel = p.relative_to(docs).as_posix()
        fm, _ = load_frontmatter(read_text(p))
        status = fm.get("status", "")
        if not status:
            rep.warn(f"{rel}: missing frontmatter 'status'")
        elif status.upper() not in VALID_STATUS:
            rep.warn(f"{rel}: invalid status '{status}' (expected {'|'.join(VALID_STATUS)})")
        sup = fm.get("supersedes", "")
        if sup and Path(sup).name not in known:
            rep.warn(f"{rel}: supersedes '{sup}' which does not exist under mkt_docs/")
    index_path = docs / "INDEX.md"
    if not index_path.exists():
        rep.warn("mkt_docs/INDEX.md missing -- generate with 'mkt_check.py index'")
    elif read_text(index_path) != build_index(root):
        rep.warn("mkt_docs/INDEX.md stale -- regenerate with 'mkt_check.py index'")
    return rep


# ---------------------------------------------------------------- ledger

def load_ledger(root):
    """Return (rows, report). Rows: list of dicts with id/claim/class/... keys."""
    rep = Report()
    path = sdlc_core.ai_path(root) / "research" / "evidence_ledger.md"
    if not path.exists():
        rep.error("research/evidence_ledger.md missing")
        return [], rep
    headers, rows = find_table(read_text(path), ["id", "claim", "class", "source"])
    if rows is None:
        rep.error("evidence_ledger.md: ledger table not found "
                  "(need columns ID | Claim | Class | ... | Source | ...)")
        return [], rep
    entries = []
    seen = set()
    for row in rows:
        rid = (col(row, "id") or "").strip()
        if not rid:
            continue
        if is_example_row(row):
            continue
        if not re.fullmatch(r"EV-\d+", rid):
            rep.error(f"ledger: bad ID '{rid}' (expected EV-<n>)")
            continue
        if rid in seen:
            rep.error(f"ledger: duplicate ID {rid}")
        seen.add(rid)
        entries.append(row)
    return entries, rep


def run_ledger(root):
    entries, rep = load_ledger(root)
    ids = set()
    for row in entries:
        rid = col(row, "id").strip()
        ids.add(rid)
        cls = (col(row, "class") or "").strip().upper()
        source = (col(row, "source") or "").strip()
        date = (col(row, "date") or "").strip()
        confidence = (col(row, "confidence") or "").strip().upper()
        if cls not in LEDGER_CLASSES:
            rep.error(f"ledger {rid}: class '{cls}' invalid (FACT|BENCHMARK|ASSUMPTION)")
            continue
        if cls == "BENCHMARK":
            if "http" not in source.lower():
                rep.error(f"ledger {rid}: BENCHMARK without a source URL")
            if not date:
                rep.error(f"ledger {rid}: BENCHMARK without a date")
        if cls == "FACT" and not source:
            rep.error(f"ledger {rid}: FACT without a source -- name the origin "
                      "('user, Wave 1' or the client's data file)")
        if (cls == "FACT" and source and not CLIENT_ORIGIN_RE.match(source)
                and INTERNAL_SOURCE_RE.search(source)):
            # FACT means "the client told me" or "the client's own primary data" — the
            # one class that legitimately has no URL. Pointing it at another document
            # of this engagement is how a researched observation gets in without the
            # URL its class would owe: the row cites a file that cites the source, the
            # validator resolves nothing, and "see VOC.md" is exactly the form the
            # BENCHMARK rule rejects. Observed in a cold-agent field test, 2026-08-02.
            rep.error(f"ledger {rid}: FACT sourced to an internal document ('{source}') -- "
                      "a FACT is what the client stated or their own primary data; an "
                      "observation gathered by research is a BENCHMARK and owes its URL")
        if cls == "ASSUMPTION":
            if confidence not in CONFIDENCE_VALUES:
                rep.error(f"ledger {rid}: ASSUMPTION without confidence (HIGH|MED|LOW)")
            value = (col(row, "value") or "").strip()
            if value and not re.search(r"\d\s*[-–—]\s*\d|\bto\b", value):
                rep.warn(f"ledger {rid}: ASSUMPTION value looks like a point estimate, expected a range")
    # reference resolution across every md file (ledger file itself excluded)
    referenced = set()
    ledger_path = sdlc_core.ai_path(root) / "research" / "evidence_ledger.md"
    for p in all_md_files(root):
        if p == ledger_path:
            continue
        text = read_text(p)
        for line in text.split("\n"):
            if EXAMPLE_MARKER in line:
                continue
            for m in EV_REF.finditer(line):
                referenced.add(m.group(1))
                if m.group(1) not in ids:
                    rel = p.relative_to(sdlc_core.ai_path(root)).as_posix()
                    rep.error(f"{rel}: reference [{m.group(1)}] not found in the ledger")
    for rid in sorted(ids - referenced, key=lambda x: int(x.split("-")[1])):
        rep.warn(f"ledger {rid}: never referenced by any document")
    return rep


# ---------------------------------------------------------------- budget

def default_tactical_files(root, file_arg):
    if file_arg:
        p = Path(file_arg)
        if not p.is_absolute():
            p = root / file_arg
        return [p] if p.exists() else []
    tactics = sdlc_core.ai_path(root) / "tactics"
    files = []
    if (tactics / "TACTICAL_PLAN.md").exists():
        files.append(tactics / "TACTICAL_PLAN.md")
    if tactics.is_dir():
        files.extend(sorted(tactics.glob("CAMPAIGN_*.md")))
    return files


def run_budget(root, file_arg=None):
    rep = Report()
    files = default_tactical_files(root, file_arg)
    if not files:
        rep.warn("no tactical plan found (tactics/TACTICAL_PLAN.md) -- budget check skipped")
        return rep
    for path in files:
        rel = path.name
        text = read_text(path)
        m = re.search(r"^Total budget:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
        if not m:
            rep.error(f"{rel}: 'Total budget:' line missing")
            continue
        total = parse_num(m.group(1))
        if total is None or total <= 0:
            rep.error(f"{rel}: cannot parse Total budget '{m.group(1).strip()}'")
            continue
        headers, rows = find_table(text, ["channel", "budget", "share"])
        if rows is None:
            rep.error(f"{rel}: Budget Allocation table not found (Channel | Budget | Share)")
            continue
        rows = [r for r in rows if not is_example_row(r)]
        if not rows:
            rep.error(f"{rel}: Budget Allocation table has no rows")
            continue
        alloc = 0.0
        for r in rows:
            v = parse_num(col(r, "budget"))
            if v is None:
                rep.error(f"{rel}: unparseable budget cell '{col(r, 'budget')}' "
                          f"for channel '{col(r, 'channel')}'")
            else:
                alloc += v
        if not close_enough(alloc, total, BUDGET_TOLERANCE):
            rep.error(f"{rel}: allocations sum to {alloc:g}, Total budget is {total:g} "
                      f"(tolerance 1%)")
    return rep


# ---------------------------------------------------------------- funnel

FUNNEL_CHAIN = (
    # (stated_col, compute, label)
    ("clicks", lambda b, cpc, cvr, close, r: b / cpc if cpc else None, "Budget/CPC"),
    ("leads", lambda b, cpc, cvr, close, r: (r["clicks"] * cvr / 100.0)
        if (r["clicks"] is not None and cvr is not None) else None, "Clicks*CVR%"),
    ("customers", lambda b, cpc, cvr, close, r: (r["leads"] * close / 100.0)
        if (r["leads"] is not None and close is not None) else None, "Leads*Close%"),
    ("cac", lambda b, cpc, cvr, close, r: (b / r["customers"])
        if (r["customers"] not in (None, 0) and b is not None) else None, "Budget/Customers"),
)


def run_funnel(root, file_arg=None):
    rep = Report()
    files = default_tactical_files(root, file_arg)
    if not files:
        rep.warn("no tactical plan found -- funnel check skipped")
        return rep
    for path in files:
        rel = path.name
        text = read_text(path)
        headers, rows = find_table(text, ["channel", "budget", "cpc", "cvr", "customers", "cac"])
        if rows is None:
            rep.error(f"{rel}: Funnel Model table not found "
                      "(Channel | Budget | CPC | Clicks | CVR % | Leads | Close % | Customers | CAC)")
            continue
        rows = [r for r in rows if not is_example_row(r)]
        if not rows:
            rep.error(f"{rel}: Funnel Model table has no rows")
            continue
        for r in rows:
            channel = col(r, "channel") or "?"
            budget = parse_num(col(r, "budget"))
            cpc = parse_num(col(r, "cpc"))
            cvr = parse_num(col(r, "cvr"))
            close = parse_num(col(r, "close"))
            stated = {
                "clicks": parse_num(col(r, "clicks")),
                "leads": parse_num(col(r, "leads")),
                "customers": parse_num(col(r, "customers")),
                "cac": parse_num(col(r, "cac")),
            }
            if budget is None or cpc is None:
                rep.error(f"{rel} [{channel}]: Budget/CPC missing or unparseable")
                continue
            # verify each stated cell against computation from STATED upstream
            # cells (so a single wrong cell does not cascade into four errors)
            chain_inputs = dict(stated)
            for name, compute, label in FUNNEL_CHAIN:
                computed = compute(budget, cpc, cvr, close, chain_inputs)
                if stated[name] is None:
                    rep.error(f"{rel} [{channel}]: '{name}' cell missing")
                    continue
                if computed is None:
                    continue  # upstream missing, already reported
                if not close_enough(stated[name], computed, FUNNEL_TOLERANCE):
                    rep.error(f"{rel} [{channel}]: {name}={stated[name]:g} but {label} "
                              f"= {computed:g} (tolerance 5%)")
    return rep


# ---------------------------------------------------------------- trace

def run_trace(root):
    rep = Report()
    docs = sdlc_core.ai_path(root)
    obj_path = docs / "strategy" / "OBJECTIVES.md"
    if not obj_path.exists():
        rep.warn("strategy/OBJECTIVES.md missing -- trace check skipped")
        return rep
    objectives = set(OBJECTIVE_HEADING.findall(read_text(obj_path)))
    if not objectives:
        rep.error("OBJECTIVES.md: no '### O<n> --...' headings found")
        return rep

    tactical = docs / "tactics" / "TACTICAL_PLAN.md"
    served = set()
    if tactical.exists():
        headers, rows = find_table(read_text(tactical), ["channel", "objective", "kpi"])
        if rows is None:
            rep.error("TACTICAL_PLAN.md: Channel Plan table not found "
                      "(Channel | Objective | KPI | Budget | Owner)")
        else:
            for r in rows:
                if is_example_row(r):
                    continue
                tokens = set(OBJECTIVE_TOKEN.findall(col(r, "objective") or ""))
                if not tokens:
                    rep.error(f"TACTICAL_PLAN.md [{col(r, 'channel')}]: no objective (O<n>) named")
                for t in tokens:
                    if t not in objectives:
                        rep.error(f"TACTICAL_PLAN.md [{col(r, 'channel')}]: objective {t} "
                                  "not defined in OBJECTIVES.md")
                served |= tokens & objectives
                if not (col(r, "kpi") or "").strip():
                    rep.error(f"TACTICAL_PLAN.md [{col(r, 'channel')}]: KPI cell empty")
        for o in sorted(objectives - served):
            rep.warn(f"objective {o}: no tactic serves it in TACTICAL_PLAN.md")
    else:
        rep.warn("tactics/TACTICAL_PLAN.md missing -- tactic trace skipped")

    measure = docs / "tactics" / "MEASUREMENT_PLAN.md"
    if measure.exists():
        headers, rows = find_table(read_text(measure), ["objective", "kpi", "target"])
        if rows is None:
            rep.error("MEASUREMENT_PLAN.md: KPI table not found (Objective | KPI | Target | ...)")
        else:
            measured = set()
            for r in rows:
                if is_example_row(r):
                    continue
                measured |= set(OBJECTIVE_TOKEN.findall(col(r, "objective") or ""))
            for o in sorted(objectives - measured):
                rep.error(f"objective {o}: no KPI row in MEASUREMENT_PLAN.md")
    else:
        rep.warn("tactics/MEASUREMENT_PLAN.md missing -- KPI trace skipped")
    return rep


# ---------------------------------------------------------------- check

def run_check(root):
    rep = Report()
    for title, fn in (("validate", run_validate), ("ledger", run_ledger),
                      ("budget", run_budget), ("funnel", run_funnel),
                      ("trace", run_trace)):
        sub = fn(root)
        sub.print(title)
        rep.merge(sub)
    return rep


# ---------------------------------------------------------------- main

# --- portable checks this distribution exposes -------------------------------
# The marketing arithmetic, offered to documents owned by ANOTHER domain: a
# distilled spec that carries a budget table can import `marketing.budget` and have
# it actually checked, instead of the table sitting in a document whose own
# validator has no opinion about it (UC8). Imported checks may only ADD findings.

def _report_findings(rep):
    return ([("error", m) for m in rep.errors]
            + [("warning", m) for m in rep.warnings])


@sdlc_core.portable_check("marketing.ledger")
def _check_ledger(rel, meta, text):
    root = sdlc_core.find_project_root()
    return _report_findings(run_ledger(root)) if root else []


@sdlc_core.portable_check("marketing.budget")
def _check_budget(rel, meta, text):
    root = sdlc_core.find_project_root()
    return _report_findings(run_budget(root)) if root else []


@sdlc_core.portable_check("marketing.funnel")
def _check_funnel(rel, meta, text):
    root = sdlc_core.find_project_root()
    return _report_findings(run_funnel(root)) if root else []


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    # Spine commands are the core's, identical in every distribution: hand over
    # every subcommand this overlay does not explicitly intercept, untouched,
    # rather than keeping a hand-copied list of spine names here -- which is how
    # `migrate` got dropped while SKILL.md kept promising it.
    if argv and not argv[0].startswith("-") and argv[0] not in OVERLAY_COMMANDS:
        return sdlc_core.main(argv)

    parser = argparse.ArgumentParser(prog="mkt_check.py", description=__doc__)
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
    root = find_root(args.root, args.docs_dir or MKT_DOCS_DIR)
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
    if code == 0:
        print(f"[OK] {args.command} clean "
              f"({len(rep.warnings)} warning(s))" if rep.warnings else f"[OK] {args.command} clean")
    else:
        print(f"[FAIL] {args.command}: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    return code


if __name__ == "__main__":
    sys.exit(main())
