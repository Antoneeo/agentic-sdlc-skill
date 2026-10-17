"""F-073 probe: the proposed dated-entry readers, run against this repository.

Usage:  python -I probe_rules.py <repo_root> [--red]

Read-only. Every assertion is printed as PASS/FAIL. With --red the grammar is
negated (the date is no longer required at the start of an opener) and the
assertions that depend on it must FAIL: a probe that cannot fail proves nothing.

What it establishes for ANALYSIS_doctrine_chronology.md:
  P1  the Diary opener grammar reads every dated form observed in the corpus;
  P2  a continuation paragraph is never read as an entry;
  P3  how many Diaries would get the "undated text before the first entry" finding,
      split by the epoch gate (only analyses started on/after the epoch are checked);
  P4  every request-record heading in the corpus matches the heading grammar;
  P5  `next:` lengths in this repository's HANDOFF files against the threshold;
  P6  the project-notes paragraphs that already carry a date, and in which form.
"""
import re
import sys
from pathlib import Path

RED = "--red" in sys.argv
ROOT = Path([a for a in sys.argv[1:] if not a.startswith("--")][0])
sys.path.insert(0, str(ROOT / "skills" / "agentic-sdlc-skill" / "scripts"))
import sdlc_core as c  # noqa: E402

ISO = r"\d{4}-\d{2}-\d{2}"
# Opener (normative; the doctrine cites this regex): at column 0, optional list
# marker, optional heading marks, optional bold, the ISO date, an optional closing
# bold, then a word boundary. The date FIRST is the whole rule; markup is tolerated.
# Round 1 (B1): an opener must also START A BLOCK -- the line above is blank, absent
# or a heading, or the line itself is a list item or a heading -- so a hard-wrapped
# prose line that happens to begin with a date is never an event. (A separator after
# the date was tried and rejected: 52 real openers read `DATE (qualifier)` or
# `DATE word`, e.g. "2026-10-02 release closure: ...".)
OPENER = re.compile(r"^(?:([-*]) |(#{3,4}) )?(\*\*)?(" + ISO + r")\b(.*)$")
if RED:  # negated: a date anywhere in the line opens an entry, no block rule
    OPENER = re.compile(r"^(?:([-*]) |(#{3,4}) )?(\*\*)?.*?(" + ISO + r")(.*)$")
SEP = re.compile(r"^(?:\*\*)?\s*(?:[—–:-])?\s*")
REQ = re.compile(r"^### (R\d+) [—–-] (" + ISO + r") [—–-] (.+)$")
EPOCH = "2026-10-18"   # the day the rule would ship; nothing started before it is checked
NEXT_CAP = 240


def label_of(bold, rest):
    rest = SEP.sub("", rest, count=1)
    if bold and "**" in rest:
        rest = rest.split("**", 1)[0]
    else:
        rest = re.split(r"(?<=[.!?])\s", rest, maxsplit=1)[0]
    return rest.strip(" .:—–-*")[:120]


def is_opener(lines, i):
    m = OPENER.match(lines[i])
    if not m:
        return None
    prev = lines[i - 1] if i else ""
    starts_block = (not prev.strip() or prev.startswith("#") or m.group(1) or m.group(2))
    return m if (starts_block or RED) else None


def dated_entries(body):
    """[(date, label, line_index)] for each entry opener in a section body."""
    lines = (body or "").splitlines()
    out = []
    for i in range(len(lines)):
        m = is_opener(lines, i)
        if m:
            out.append((m.group(4), label_of(m.group(3), m.group(5)), i))
    return out


def preface(body):
    """Text before the first opener, comments and blank lines removed."""
    text = re.sub(r"<!--.*?-->", "", body or "", flags=re.S)
    found = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if is_opener(lines, i):
            break
        if line.strip():
            found.append(line.strip())
    return found


results = []


def check(name, cond, detail=""):
    results.append(cond)
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))


# P1/P2 -- fixed cases taken from the corpus forms
cases = {
    "**2026-08-02 — opened.** Standalone, devPNT off.": ("2026-08-02", "opened"),
    "2026-09-26: la prima Vision ha avuto blind review PASS. Il resto.": ("2026-09-26", "la prima Vision ha avuto blind review PASS"),
    "- 2026-06-13: Analisi avviata. Decisione: integrare.": ("2026-06-13", "Analisi avviata"),
    "- **2026-07-28** — opened. devPNT off.": ("2026-07-28", "opened"),
    "### 2026-10-01 — round 2": ("2026-10-01", "round 2"),
}
for line, want in cases.items():
    got = dated_entries(line)
    check(f"P1 opener read: {line[:32]!r}", bool(got) and got[0][:2] == want,
          str(got[0][:2]) if got else "no entry")
continuations = [
    "**Round 3 (the cap) — FAIL; the v4 above disposes every finding.**",
    "**Owner note, 2026-08-02 — the skill is made to be used by an agent.**",
    "The release of 2026-10-17 shipped four packages.",
    "  - 2026-08-03: an indented bullet inside an entry",
    'a hard-wrapped prose line ends here and the next one begins with\n2026-08-01 — a date, mid-paragraph',
    'the owner said ("vai",\n2026-08-01) with the fixes incorporated',
    "**2026-08-01x** not a date boundary",
]
for line in continuations:
    check(f"P2 continuation not an entry: {line[:32]!r}", not dated_entries(line))

# P3 -- the preface finding over the real corpus
checked = flagged = legacy_flagged = total = entries = 0
for p in sorted((ROOT / "ai_docs" / "solutions").glob("ANALYSIS_*.md")):
    text = c.read_text(p)
    meta = c.load_frontmatter(text.splitlines())
    body = c.section_body(text, ("## Diary", "## Diario"))
    if body is None:
        continue
    total += 1
    entries += len(dated_entries(body))
    has_preface = bool(preface(body))
    started = (meta.get("start_date") or "").strip().strip("'\"")
    if started >= EPOCH:
        checked += 1
        flagged += has_preface
    else:
        legacy_flagged += has_preface
print(f"P3 Diaries={total} entries={entries} checked(after epoch)={checked} "
      f"flagged={flagged} legacy-with-preface(never checked)={legacy_flagged}")
check("P3 no analysis started before the epoch is checked", checked == 0)
check("P3 the corpus yields dated entries", entries > 200, str(entries))

# P4 -- request-record headings
bad = []
n = 0
for p in sorted((ROOT / "ai_docs" / "audit" / "requests").glob("REQUEST_*.md")):
    for line in c.read_text(p).splitlines():
        if line.startswith("### "):
            n += 1
            if not REQ.match(line):
                bad.append(f"{p.name}: {line[:60]}")
check(f"P4 request headings match ({n})", not bad and n > 0, "; ".join(bad[:3]))
check("P4 a malformed heading is caught", not REQ.match("### R4-nota — 2026-10-01 — x"))

# P5 -- next: lengths
lens = []
for p in sorted((ROOT / "ai_docs" / "audit").glob("HANDOFF_*.md")):
    meta = c.load_frontmatter(c.read_text(p).splitlines())
    lens.append((len(str(meta.get("next") or "")), p.name))
lens.sort()
print("P5 next: lengths", [n for n, _ in lens])
check(f"P5 no next: in this repository exceeds {NEXT_CAP}", all(n <= NEXT_CAP for n, _ in lens),
      str(lens[-1]))

# P6 -- project notes: which paragraphs already carry a date, and how
notes = c.read_text(ROOT / "ai_docs" / "audit" / "project_notes.md")
paras = [b.strip() for b in re.split(r"\n\s*\n", notes) if b.strip()]
opened = [b for b in paras if dated_entries(b.splitlines()[0])]
inline = [b for b in paras if not dated_entries(b.splitlines()[0]) and re.search(ISO, b.splitlines()[0])]
print(f"P6 project-notes paragraphs={len(paras)} opener-dated={len(opened)} "
      f"date-later-in-first-line={len(inline)}")
for b in inline:
    print("     ", b.splitlines()[0][:80])

print(f"\n{sum(results)}/{len(results)} PASS" + ("  (RED run: failures expected)" if RED else ""))
sys.exit(0 if all(results) else 1)
