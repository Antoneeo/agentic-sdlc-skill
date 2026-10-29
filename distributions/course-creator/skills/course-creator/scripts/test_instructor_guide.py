"""Instructor-led delivery package and course-version mentions (F-086)."""
import unittest
import test_slide_content

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


class InstructorGuide(unittest.TestCase):
    def setUp(self):
        self.content = test_slide_content.AuthoredContent()
        self.content.setUp()
        self.addCleanup(self.content.doCleanups)
        self.fixture = self.content.fixture
        self.course = self.fixture.course

    def build(self, mode="instructor-led", unit_text="", guide=None, demo=True, version="1.2"):
        source = self.content.source().replace("Course version: 1.0", f"Course version: {version}").replace(
            "Delivery mode: self-study", f"Delivery mode: {mode}")
        source = source.replace("Authored material for check.", "Authored material for check. " + unit_text, 1)
        self.content.activate(source)
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.fixture.art("COURSE_PLAN.md", plan.replace("Course version: 1.0", f"Course version: {version}"))
        if demo:
            self.fixture.art("demo/FALLBACK.md", "# Fallback\n## answer\nRecorded answer.\n")
        if guide is not None:
            self.fixture.art("INSTRUCTOR_GUIDE.md", guide.replace("Course version: 1.2", f"Course version: {version}")
                             if version != "1.2" else guide)

    def errors(self):
        return [f"{f.file} {f.item}: {f.reason}" for f in self.fixture.findings() if f.severity == "ERROR"]

    def assertFlags(self, needle):
        self.assertTrue([e for e in self.errors() if needle in e], self.errors())

    def guide(self, old, new):
        self.assertIn(old, GUIDE)
        return GUIDE.replace(old, new)

    # Rule 1: obligation
    def test_instructor_led_without_guide_is_an_error(self):
        self.build()
        self.assertFlags("INSTRUCTOR_GUIDE.md")

    def test_self_study_needs_no_guide_but_a_present_one_is_checked(self):
        self.build(mode="self-study")
        self.assertEqual(self.errors(), [])
        self.build(mode="self-study", guide=self.guide("| C-1 |", "| C-9 |"))
        self.assertFlags("C-9")

    def test_unknown_mode_keeps_the_existing_error_only(self):
        self.build(mode="deck")
        self.assertEqual([e for e in self.errors() if "INSTRUCTOR_GUIDE" in e], [])
        self.assertFlags("unknown delivery mode")

    def test_complete_instructor_led_course_is_clean(self):
        self.build(unit_text="Scrivi a IC1 indicando il corso, versione 1.2, e il modulo.", guide=GUIDE)
        self.assertEqual(self.errors(), [])

    # Rule 2: header
    def test_guide_header_must_match_plan(self):
        for old, new in (("Course version: 1.2", "Course version: 1.0"), ("Feedback flow: IC1", "Feedback flow: IC2"),
                         ("Feedback flow: IC1\n", "")):
            with self.subTest(old=old, new=new):
                self.build(guide=self.guide(old, new))
                self.assertFlags("INSTRUCTOR_GUIDE.md")

    # Rule 3: sections
    def test_missing_empty_or_duplicate_section_is_an_error(self):
        for old, new in (("## After the course\nDelete the shared copies; collect feedback through IC1.\n", ""),
                         ("Open the shared folder and check the demo runs. Feedback goes through D-IC IC1.", ""),
                         ("## After the course\n", "## Schedule\nSee above.\n\n## After the course\n"),
                         ("Course version: 1.2\n", "Course version: 1.2\nCourse version: 1.2\n"),
                         ("| C-1 | learners lack the prerequisite | teach CO1 first | "
                          "ai_docs/solutions/courses/intro/demo/FALLBACK.md |\n", ""),
                         ("| 1 | 60 min | M1 |\n", ""),
                         ("| 1 | 60 min | M1 |", "| 1 |  | M1 |")):
            with self.subTest(old=old):
                self.build(guide=self.guide(old, new))
                self.assertFlags("INSTRUCTOR_GUIDE.md")

    # Rules 4-5: the package
    def test_listed_material_missing_from_package_is_an_error(self):
        self.build(guide=GUIDE, demo=False)
        self.assertFlags("FALLBACK.md")

    def test_material_must_stay_inside_the_course_folder(self):
        for path in ("ai_docs/vision/", "ai_docs/solutions/courses/intro/../../../vision/",
                     "C:/outside/demo/", "/etc/"):
            with self.subTest(path=path):
                self.build(guide=self.guide("| ai_docs/solutions/courses/intro/demo/ |", f"| {path} |"))
                self.assertFlags(f"'{path}'")

    def test_material_folder_form_matches_what_it_is(self):
        for path in ("ai_docs/solutions/courses/intro/demo", "ai_docs/solutions/courses/intro/demo/FALLBACK.md/"):
            with self.subTest(path=path):
                self.build(guide=self.guide("| ai_docs/solutions/courses/intro/demo/ |", f"| {path} |"))
                self.assertFlags(f"'{path}'")

    def test_material_symlink_cannot_leave_the_course_folder(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as outside:
            self.build(guide=GUIDE, demo=False)
            try:
                (self.course / "demo").symlink_to(Path(outside), target_is_directory=True)
            except OSError:
                self.skipTest("symlink privilege unavailable")
            (Path(outside) / "FALLBACK.md").write_text("# Fallback\n", encoding="utf-8")
            self.assertFlags("outside the course folder")

    def test_material_path_takes_no_locator_and_a_valid_viewer(self):
        for old, new in (("| ai_docs/solutions/courses/intro/demo/ | instructor |",
                          "| ai_docs/solutions/courses/intro/demo/FALLBACK.md#answer | instructor |"),
                         ("| ai_docs/solutions/courses/intro/demo/ | instructor |",
                          "| ai_docs/solutions/courses/intro/demo/ | everyone |")):
            with self.subTest(new=new):
                self.build(guide=self.guide(old, new))
                self.assertFlags("INSTRUCTOR_GUIDE.md")

    def test_cited_path_must_be_in_the_package_and_its_locator_must_exist(self):
        anchor = "Feedback goes through D-IC IC1."
        for cite in ("ai_docs/vision/features/VISION_course_intro.md#intro",
                     "ai_docs/solutions/courses/intro/demo/FALLBACK.md#missing",
                     "ai_docs/solutions/courses/intro/demo/GONE.md"):
            with self.subTest(cite=cite):
                self.build(guide=self.guide(anchor, f"{anchor} Read {cite}."))
                self.assertFlags(cite.partition("#")[0].rsplit("/", 1)[1])
        self.build(guide=self.guide(anchor, f"{anchor} Read ai_docs/solutions/courses/intro/demo/FALLBACK.md#answer."))
        self.assertEqual(self.errors(), [])

    def test_citation_in_the_guide_header_is_checked(self):
        self.build(guide=self.guide("Feedback flow: IC1\n", "Feedback flow: IC1\nSee ai_docs/vision/GONE.md\n"))
        self.assertFlags("GONE.md")

    def test_citation_is_read_as_a_whole_path(self):
        anchor = "Feedback goes through D-IC IC1."
        self.build(guide=self.guide(anchor, f"{anchor} Read **ai_docs/solutions/courses/intro/demo/FALLBACK.md**."))
        self.assertEqual(self.errors(), [])
        for cite in ("../../ai_docs/solutions/courses/intro/demo/FALLBACK.md",
                     "/abs/ai_docs/solutions/courses/intro/demo/FALLBACK.md"):
            with self.subTest(cite=cite):
                self.build(guide=self.guide(anchor, f"{anchor} Read {cite}."))
                self.assertEqual(self.errors(), [])  # not an ai_docs/ citation: a declared review residual

    # Rule 6: reserved material
    def test_solution_unit_must_be_named_whole_as_reserved(self):
        for text in ("Nothing to hide.", "S030 is not the solution."):
            with self.subTest(text=text):
                self.build(guide=self.guide("S03 is the solution of S02: never project it.", text))
                self.assertFlags("S03")

    # Rule 7: deviations
    def test_deviation_risk_and_fallback(self):
        self.build(guide=self.guide("| C-1 | learners", "| C-9 | learners"))
        self.assertFlags("C-9")
        self.build(guide=self.guide("| teach CO1 first | ai_docs/solutions/courses/intro/demo/FALLBACK.md |",
                                    "| teach CO1 first | ai_docs/solutions/courses/intro/sources.md |"))
        self.assertFlags("sources.md")
        self.build(guide=self.guide("| teach CO1 first | ai_docs/solutions/courses/intro/demo/FALLBACK.md |",
                                    "| teach CO1 first | - |"))
        self.assertEqual(self.errors(), [])

    # Rule 8: schedule
    def test_schedule_module_must_exist_in_plan(self):
        self.build(guide=self.guide("| 60 min | M1 |", "| 60 min | M1, M7 |"))
        self.assertFlags("M7")

    # Rule 9: course version mentioned in the text
    def test_stale_course_version_in_text_is_an_error(self):
        for text in ("Scrivi a IC1 indicando il corso, versione 1.0, e il modulo.",
                     "Feedback su Intro, versione 1.0.", "Course intro, version: v1.0;",
                     "Il corso è alla versione 1.2-draft."):
            with self.subTest(text=text):
                self.build(unit_text=text, guide=GUIDE)
                self.assertFlags("S02")

    def test_dotted_letters_and_trailing_dash_are_compared(self):
        for text in ("Il corso, versione 1.x.", "Il corso, versione 1.2-."):
            with self.subTest(text=text):
                self.build(unit_text=text, guide=GUIDE)
                self.assertFlags("S02")

    def test_legacy_course_gets_no_new_rule(self):
        # Rule 10: no content contract, no delivery mode, nothing new to require or compare.
        self.fixture.art("INSTRUCTOR_GUIDE.md", "# Broken guide\n")
        self.fixture.art("modules/M1.md", "# M1\n## explanation\nIl corso Intro, versione 9.9.\n## check\nWhat?\n")
        self.assertEqual([f for f in self.fixture.findings() if f.severity == "ERROR"], [])

    def test_matching_or_unrelated_versions_are_not_flagged(self):
        for text in ("Serve Python versione 3.12 o successiva.", "Introduzione: Python versione 3.12.",
                     "Il corso, versione 1.2.", "Il corso usa la versione 2 dello schema.",
                     "Course intro, version v1.2)"):
            with self.subTest(text=text):
                self.build(unit_text=text, guide=GUIDE)
                self.assertEqual(self.errors(), [])

    def test_version_with_suffix_compares_exactly(self):
        self.build(mode="self-study", version="4.0-content", unit_text="Il corso, versione 4.0-content.")
        self.assertEqual(self.errors(), [])
        self.build(mode="self-study", version="4.0-content", unit_text="Il corso, versione 4.0.")
        self.assertFlags("4.0")

    def test_stale_version_in_guide_body_is_an_error(self):
        self.build(guide=self.guide("Delete the shared copies;", "Course versione 1.0: delete the shared copies;"))
        self.assertFlags("INSTRUCTOR_GUIDE.md")

    def test_text_content_contract_is_covered(self):
        self.build()
        path = self.course / "COURSE_PLAN.md"
        plan = path.read_text(encoding="utf-8").replace("slide-content-v1", "text-content-v1").replace(
            "SLIDE_CONTENT", "COURSE_CONTENT").replace("#s0", "#u0")
        source = (self.course / "SLIDE_CONTENT.md").read_text(encoding="utf-8").replace(
            "SLIDE_CONTENT", "COURSE_CONTENT").replace("#s0", "#u0").replace("## S0", "## U0").replace(
            "Solution: S03", "Solution: U03").replace("Authored material for check.",
                                                      "Authored material for check. Il corso, versione 1.0.", 1)
        (self.course / "SLIDE_CONTENT.md").unlink()
        self.fixture.art("COURSE_CONTENT.md", source)
        self.fixture.art("COURSE_PLAN.md", "Format exception: Owner requested an audio lesson.\n" + plan)
        self.assertFlags("INSTRUCTOR_GUIDE.md")
        self.assertFlags("U02")


if __name__ == "__main__":
    unittest.main()
