#!/usr/bin/env python3
"""Course lens entry point: shared SDLC and memory, plus course structure."""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sdlc_core
import knowledge
import course_check


sdlc_core.set_entry_point("course", provides=("code", "knowledge", "course"),
                          script="sdlc_check.py")
sdlc_core.set_profile(
    skill_name="course-creator", unit_noun="course",
    support_files=("slide_content.md", "templates.md", "learning_design.md", "source_check.md",
                   "simulation.md", "feedback.md", "elicitation.md", "ENFORCEMENT.md",
                   "memory.md", "review.md", "routing.md", "vision.md", "guides.md",
                   "dispatch.md"),
    capabilities=("triage", "write_triggers", "workstream_registry", "vision_gate",
                  "design_review_gate", "guide_router", "worktree_hygiene",
                  "question_discipline"),
    design_gate_between=("### 3. Course Design", "### 4. Production and Testing"),
    remind_line=("load course-creator when the deliverable teaches; declare triage and "
                 "guide-router verdict. Define the learner profile and prerequisites before "
                 "writing explanations. Reopen sources for factual claims. A simulator is "
                 "diagnostic; real learning remains unverified until supported by feedback."),
)


def _report(findings, strict=False):
    for finding in findings:
        print(f"[{finding.severity}] {finding.file} [{finding.item}]: {finding.reason}")
    errors = sum(f.severity == "ERROR" for f in findings)
    warnings = sum(f.severity == "WARN" for f in findings)
    print(f"course: {errors} error(s), {warnings} warning(s)")
    return 1 if errors or (strict and warnings) else 0


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


if __name__ == "__main__":
    sys.exit(main())
