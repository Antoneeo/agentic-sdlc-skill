"""F-098 probe: does the session orientation carry the team definition?

Usage: python probe_orient_team.py <path to a lens's sdlc_check.py>

Builds, in a temporary directory, a project whose guide router and workstream registry
are both larger than their orientation caps (the worst case for the README's room), and
runs `orient` on it three times:

  P1  README.md with a `## Team` section as its first section
      -> every line of the section is in the orientation (the README's head survives
         the cut). Preservation: must be green before and after the unit.
  P2  README.md with no `## Team` section, in a project that has opened a significant
      unit (a request record exists under audit/requests/)
      -> the orientation says the team is not defined and where the questions are.
         Red before the unit (nothing says it), green after.
  P3  README.md with a `## Team` section
      -> the "not defined" line of P2 is absent. Green before (vacuously) and after.
  P4  README.md with no `## Team` section, in a project with no request record (it has
      only ever done trivial and small work)
      -> the line is absent: such a project pays nothing. Green before (vacuously)
         and after.

Exit code 0 when P1-P4 hold, 1 otherwise; each assertion prints PASS or FAIL.
"""
import subprocess
import sys
import tempfile
from pathlib import Path

# A section at the size bound the design sets for it (TEAM_SECTION_MAX characters,
# newlines included): the claim "the section reaches the orientation whole" is probed at
# the largest section the doctrine allows, not at a convenient one.
TEAM_SECTION_MAX = 700
TEAM = [
    "## Team",
    "<!-- source: audit/requests/REQUEST_x.md#R2 (2026-11-10) -->",
    "- Members: the owner; one coordinating session; the sessions it starts for a unit.",
    "- Reserved to the owner: product choices, decisions that shape the architecture,",
    "  anything that touches production, secrets, publication; the reserved approvals.",
    "- Without asking: every other choice is the member's, decided and reported in one",
    "  line. A started session reports to the coordinating session, which reports to",
    "  the owner. Only the coordinating session starts other sessions.",
    "- Work and reports: a started session leaves its report in the unit's HANDOFF",
    "  file and names it in its last message.",
]
README_HEAD = ["---", "default_domain: code", "---", "# ai_docs - reading guide", ""]
README_TAIL = ["", "Must-reads for this project, in order.", ""] + [
    f"{i}. `strategic/doc_{i}.md` - a must-read line that takes some room in the preview."
    for i in range(1, 40)]
NOT_DEFINED = "no `## Team`"


def build(root, with_team, with_request=True):
    d = root / "ai_docs"
    (d / "reference").mkdir(parents=True)
    (d / "audit").mkdir()
    if with_request:
        (d / "audit" / "requests").mkdir()
        (d / "audit" / "requests" / "REQUEST_x.md").write_text(
            "---\nunit: F-001\n---\n# Request record: x (F-001)\n", encoding="utf-8")
    readme = README_HEAD + (TEAM if with_team else []) + README_TAIL
    (d / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")
    router = ["# Guide router", ""] + [
        f"- `GUIDE_topic_{i}.md` (CURRENT) -- consult before changing subsystem {i}, "
        "which is described at some length here." for i in range(60)]
    (root / "router.txt").write_text("\n".join(router) + "\n", encoding="utf-8")
    for i in range(30):
        (d / "audit" / f"HANDOFF_unit_{i}.md").write_text(
            "---\n"
            f"workstream: F-{100 + i} Unit number {i} with a reasonably long title\n"
            "level: L3\nbranch: feat/unit\nstatus: IN_PROGRESS\nsince: 2026-11-01\n"
            "next: Continue the implementation of the next step of the action plan.\n"
            "details: ANALYSIS_unit.md\nupdated: 2026-11-10\n---\n", encoding="utf-8")


def orient(entry, root):
    subprocess.run([sys.executable, entry, "index", "--root", str(root)],
                   capture_output=True, text=True, encoding="utf-8")
    # `index` regenerates the router from the guides (none here): write the large one
    # after it, so the orientation meets a router over its cap.
    (root / "ai_docs" / "reference" / "INDEX.md").write_text(
        (root / "router.txt").read_text(encoding="utf-8"), encoding="utf-8")
    r = subprocess.run([sys.executable, entry, "orient", "--root", str(root)],
                       capture_output=True, text=True, encoding="utf-8")
    return r.stdout


def main(argv):
    if len(argv) != 2:
        print(__doc__)
        return 2
    entry = argv[1]
    ok = True

    def check(name, cond, detail=""):
        nonlocal ok
        ok = ok and cond
        print(f"{'PASS' if cond else 'FAIL'}  {name}{('  -- ' + detail) if detail else ''}")

    with tempfile.TemporaryDirectory() as t:
        with_team = Path(t) / "with_team"
        without = Path(t) / "without"
        build(with_team, True)
        build(without, False)
        small_only = Path(t) / "small_only"
        build(small_only, False, with_request=False)
        out_with = orient(entry, with_team)
        out_without = orient(entry, without)
        out_small = orient(entry, small_only)

    check("P0 the fixture is the worst case (router, registry and README all cut)",
          out_with.count("more lines -- read") >= 3,
          f"{out_with.count('more lines -- read')} cut sections, {len(out_with)} chars")
    size = sum(len(ln) + 1 for ln in TEAM)
    check("P0b the probed section is at the size bound",
          TEAM_SECTION_MAX - 50 <= size <= TEAM_SECTION_MAX, f"{size} characters")
    missing = [ln for ln in TEAM if ln not in out_with]
    check("P1 every line of `## Team` is in the orientation", not missing,
          f"missing: {missing}" if missing else "")
    check("P2 with no `## Team`, the orientation says so", NOT_DEFINED in out_without)
    check("P3 with `## Team`, the not-defined line is absent", NOT_DEFINED not in out_with)
    check("P4 with no request record, the not-defined line is absent",
          NOT_DEFINED not in out_small)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
