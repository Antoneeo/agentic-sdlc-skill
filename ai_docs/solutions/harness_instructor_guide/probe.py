"""F-086 probes: what course_check does with an instructor-led course.

Run from the repository root:
    python ai_docs/solutions/harness_instructor_guide/probe.py

Each assertion states the behaviour F-086 requires. On the baseline (course-creator
0.1.0-beta.14) the RED probes fail and the guard probes pass; after the change all pass.
The fixture reproduces the field case of REQUEST_instructor_guide.md#R1 (course
`agente-personale-skills`): instructor-led, no INSTRUCTOR_GUIDE.md, a unit that still
says "versione 1.0" while the course is at 1.2.
"""
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[3] / "distributions/course-creator/skills/course-creator/scripts"
sys.path.insert(0, str(SCRIPTS))
import test_slide_content  # noqa: E402  (reuses the shipped valid-course fixture)

GUIDE = """# Instructor guide: Intro
Course version: 1.2
Feedback flow: IC1

## Before the course
Open the shared folder and check the demo runs. Feedback goes through D-IC IC1.

## Schedule
| Session | Duration | Modules |
|---|---|---|
| 1 | 60 min | M1 |

## Reserved material
S03 is the solution of S02: never project it.

## When something deviates
| Risk ID | In class it looks like | Instructor action | Fallback material |
|---|---|---|---|
| C-1 | learners lack the prerequisite | teach CO1 first | ai_docs/solutions/courses/intro/demo/FALLBACK.md |

## After the course
Delete the shared copies; collect feedback through IC1.

## Materials
| Material | Path | Seen by | Used in |
|---|---|---|---|
| Demo project | ai_docs/solutions/courses/intro/demo/ | instructor | S01 |
| Fallback transcript | ai_docs/solutions/courses/intro/demo/FALLBACK.md | instructor | S01 |
"""


class InstructorLed(unittest.TestCase):
    def setUp(self):
        self.content = test_slide_content.AuthoredContent()
        self.content.setUp()
        self.addCleanup(self.content.doCleanups)
        self.fixture = self.content.fixture
        self.course = self.fixture.course

    def build(self, mode="instructor-led", unit_text="", guide=None, demo=True):
        source = self.content.source().replace("Course version: 1.0", "Course version: 1.2").replace(
            "Delivery mode: self-study", f"Delivery mode: {mode}")
        source = source.replace("Authored material for check.", "Authored material for check. " + unit_text, 1)
        self.content.activate(source)
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.fixture.art("COURSE_PLAN.md", plan.replace("Course version: 1.0", "Course version: 1.2"))
        if demo:
            self.fixture.art("demo/FALLBACK.md", "# Fallback\nRecorded answer.\n")
        if guide is not None:
            self.fixture.art("INSTRUCTOR_GUIDE.md", guide)

    def errors(self):
        return [f"{f.file} {f.item}: {f.reason}" for f in self.fixture.findings() if f.severity == "ERROR"]

    def mentions(self, needle):
        return [e for e in self.errors() if needle in e]

    # RED on the baseline
    def test_red_instructor_led_without_guide_is_an_error(self):
        self.build()
        self.assertTrue(self.mentions("INSTRUCTOR_GUIDE"), self.errors())

    def test_red_stale_course_version_in_unit_text_is_an_error(self):
        self.build(unit_text="Scrivi a IC1 indicando il corso, versione 1.0, e il modulo.", guide=GUIDE)
        self.assertTrue(self.mentions("1.0"), self.errors())

    def test_red_listed_material_missing_from_package_is_an_error(self):
        self.build(guide=GUIDE, demo=False)
        self.assertTrue(self.mentions("FALLBACK.md"), self.errors())

    def test_red_guide_version_must_match_plan(self):
        self.build(guide=GUIDE.replace("Course version: 1.2", "Course version: 1.0"))
        self.assertTrue(self.mentions("INSTRUCTOR_GUIDE"), self.errors())

    def test_red_solution_unit_not_reserved_is_an_error(self):
        self.build(guide=GUIDE.replace("S03 is the solution of S02: never project it.", "Nothing to hide."))
        self.assertTrue(self.mentions("S03"), self.errors())

    def test_red_deviation_risk_not_in_threat_model_is_an_error(self):
        self.build(guide=GUIDE.replace("| C-1 | learners", "| C-9 | learners"))
        self.assertTrue(self.mentions("C-9"), self.errors())

    def test_red_schedule_module_not_in_plan_is_an_error(self):
        self.build(guide=GUIDE.replace("| 60 min | M1 |", "| 60 min | M7 |"))
        self.assertTrue(self.mentions("M7"), self.errors())

    def test_red_material_outside_project_is_an_error(self):
        # Amended by REQUEST #R10: a material may live anywhere in the project, never outside it.
        self.build(guide=GUIDE.replace("| ai_docs/solutions/courses/intro/demo/ |", "| ../outside/ |"))
        self.assertTrue(self.mentions("../outside/"), self.errors())

    def test_red_stale_version_next_to_course_name_is_an_error(self):
        # #R8: the course name (title "Intro" or slug "intro") counts like the word corso/course.
        self.build(unit_text="Feedback su Intro, versione 1.0.", guide=GUIDE)
        self.assertTrue(self.mentions("1.0"), self.errors())

    def test_red_cited_path_outside_course_folder_is_an_error(self):
        self.build(guide=GUIDE.replace(
            "Feedback goes through D-IC IC1.",
            "Feedback goes through D-IC IC1. Read ai_docs/vision/features/VISION_course_intro.md#intro first."))
        self.assertTrue(self.mentions("VISION_course_intro.md"), self.errors())

    # Guards: must hold before and after
    def test_guard_self_study_needs_no_guide(self):
        self.build(mode="self-study")
        self.assertEqual(self.errors(), [])

    def test_guard_third_party_version_is_not_flagged(self):
        self.build(unit_text="Serve Python versione 3.12 o successiva.", guide=GUIDE)
        self.assertEqual(self.errors(), [])

    def test_guard_slug_inside_another_word_does_not_count(self):
        # Slug "intro" must match as a whole word: "Introduzione" is not the course name.
        self.build(unit_text="Introduzione: Python versione 3.12.", guide=GUIDE)
        self.assertEqual(self.errors(), [])

    def test_guard_complete_instructor_led_course_is_clean(self):
        self.build(unit_text="Scrivi a IC1 indicando il corso, versione 1.2, e il modulo.", guide=GUIDE)
        self.assertEqual(self.errors(), [])


class PopulationAtRest(unittest.TestCase):
    def test_guard_this_repository_courses_stay_clean(self):
        # C-001 (self-study, 4.0-content) had 0 findings on the baseline; F-086 adds none.
        import course_check
        self.assertEqual(course_check.validate_all(Path(__file__).resolve().parents[3]), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
