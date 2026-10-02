"""Structural scenario and routing checks; agent runs are recorded separately."""
from pathlib import Path
import unittest
import importlib.util


REPO = Path(__file__).resolve().parents[5]
SIBLINGS = (
    REPO / "skills/agentic-sdlc-skill",
    REPO / "distributions/kb-agentic-skill/skills/kb-agentic-skill",
    REPO / "distributions/mkt-agentic-sdlc/skills/mkt-agentic-sdlc",
)
SCENARIOS = Path(__file__).parent / "scenarios"


class CourseRouting(unittest.TestCase):
    def test_fourth_distribution_is_guarded(self):
        path = SIBLINGS[0] / "scripts/shared_files.py"
        spec = importlib.util.spec_from_file_location("course_shared_files", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(len(module.DISTRIBUTION_SKILL_DIRS), 4)
        self.assertIn("distributions/course-creator/skills/course-creator",
                      module.DISTRIBUTION_SKILL_DIRS)

    def test_each_existing_skill_reaches_course_router(self):
        for skill in SIBLINGS:
            with self.subTest(skill=skill):
                contract = (skill / "SKILL.md").read_text(encoding="utf-8")
                self.assertIn("`course-creator`", contract)

    def test_shared_router_has_decisive_course_branch(self):
        routers = [(skill / "routing.md").read_text(encoding="utf-8")
                   for skill in SIBLINGS]
        self.assertEqual(len(set(routers)), 1)
        routing = routers[0]
        self.assertIn("| course | `course-creator` |", routing)
        self.assertIn("**course**. Decided", routing)
        self.assertIn("course", routing.split("## 2. Worked verdicts", 1)[1])

    def test_scenarios_have_observable_learning_criteria(self):
        names = {path.stem for path in SCENARIOS.glob("*.md")}
        self.assertEqual(names, {"novice_without_sources", "missing_prerequisite",
                                 "generic_explanation", "feedback_method_defect", "slide_content_handoff", "pedagogical_method"})
        for path in SCENARIOS.glob("*.md"):
            with self.subTest(path=path.name):
                body = path.read_text(encoding="utf-8")
                for heading in ("## Prompt", "## Expected", "## Pass criteria"):
                    self.assertIn(heading, body)
                self.assertGreaterEqual(body.split("## Pass criteria", 1)[1].count("\n- "), 3)


if __name__ == "__main__":
    unittest.main()
