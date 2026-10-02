"""Structural course checks; teaching quality remains a human judgement."""
import sys
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import course_check
import sdlc_check


class CourseChecks(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.docs = self.root / "ai_docs"
        self.course = self.docs / "solutions/courses/intro"
        self.course.mkdir(parents=True)
        self.put("vision/features/VISION_course_intro.md",
                 "---\ndomain: course\nstatus: APPROVED\n---\n# Intro\nStatus: APPROVED\n")
        self.put("solutions/ANALYSIS_course_intro.md",
                 "---\nid: C-1\ndomain: course\nstatus: IN_PROGRESS\nstart_date: 2026-09-27\n---\n"
                 "## Use Cases / User Needs\n### UC1\nLearn the topic.\n"
                 "## Interface Contract\n### IC1\nRead module.\n"
                 "## Learning and Content Risks\n### C-1\nA prerequisite may be missing.\n")
        self.art("D-UC.md", "| UC ID | Profile | Starting knowledge | Evidence | Need |\n"
                 "|---|---|---|---|---|\n| UC1 | novice | none | interview | use topic |\n")
        self.art("D-IC.md", "| Flow ID | Surface | Conditions | Feedback channel |\n"
                 "|---|---|---|---|\n| IC1 | module | browser | not available |\n")
        self.art("P-TM.md", "| Risk ID | Vector | Mitigation | Residual |\n"
                 "|---|---|---|---|\n| C-1 | omitted prerequisite | teach first | low |\n")
        self.art("CONCEPT_GRAPH.md",
                 "| Concept ID | Prerequisites | Profile | Initial state | Evidence | Source | Objectives |\n"
                 "|---|---|---|---|---|---|---|\n"
                 "| CO1 | - | novice | DA_INSEGNARE | - | ai_docs/solutions/courses/intro/sources.md#claim1 | O1 |\n")
        self.art("COURSE_PLAN.md", "Course version: 1.0\nEfficacy: efficacy not verified\nFeedback flow: IC1\n"
                 "| Module ID | Profile | Objective ID | Concepts | Explanation | Sources | Check | Next |\n"
                 "|---|---|---|---|---|---|---|---|\n"
                 "| M1 | novice | O1 | CO1 | ai_docs/solutions/courses/intro/modules/M1.md#explanation | "
                 "ai_docs/solutions/courses/intro/sources.md#claim1 | "
                 "ai_docs/solutions/courses/intro/modules/M1.md#check | end |\n")
        self.art("SIMULATION_REPORT.md", "Status: not run\nReason: independent agents unavailable.\n")
        self.art("sources.md", "# Sources\n## claim1\nEvidence from a reopenable document.\n")
        self.art("modules/M1.md", "# M1\n## explanation\nExplanation for novice.\n## check\nWhat did you learn?\n")

    def put(self, rel, content):
        path = self.docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def art(self, rel, content):
        path = self.course / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def findings(self):
        return course_check.validate_course(self.root, self.course)

    def reasons(self):
        return "\n".join(f.reason for f in self.findings())

    def test_valid_course_and_audio_explanation(self):
        self.assertFalse([f for f in self.findings() if f.severity == "ERROR"])
        (self.course / "assets").mkdir()
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        (self.course / "assets/lesson.pdf").write_bytes(b"pdf")
        (self.course / "assets/lesson.pptx").write_bytes(b"slides")
        self.art("COURSE_PLAN.md", plan.replace(
            "modules/M1.md#explanation", "assets/lesson.pdf#page=2"))
        self.assertFalse([f for f in self.findings() if f.severity == "ERROR"])
        self.art("COURSE_PLAN.md", plan.replace(
            "modules/M1.md#explanation", "assets/lesson.pptx#slide=2"))
        self.assertFalse([f for f in self.findings() if f.severity == "ERROR"])
        (self.course / "assets/lesson.mp3").write_bytes(b"audio")
        self.art("COURSE_PLAN.md", plan.replace(
            "modules/M1.md#explanation", "assets/lesson.mp3#00:01:00"))
        self.assertFalse([f for f in self.findings() if f.severity == "ERROR"])

    def test_missing_or_draft_vision_and_analysis(self):
        vision = self.docs / "vision/features/VISION_course_intro.md"
        vision.unlink()
        self.assertIn("Vision", self.reasons())
        self.put("vision/features/VISION_course_intro.md",
                 "---\ndomain: course\nstatus: DRAFT\n---\n# Draft\n")
        self.assertIn("APPROVED", self.reasons())
        (self.docs / "solutions/ANALYSIS_course_intro.md").unlink()
        self.assertIn("ANALYSIS", self.reasons())

    def test_missing_artifact_and_unknown_ids(self):
        (self.course / "P-TM.md").unlink()
        self.assertIn("P-TM.md", self.reasons())
        self.art("D-UC.md", "| UC ID | Profile | Starting knowledge | Evidence | Need |\n"
                 "|---|---|---|---|---|\n| UC9 | novice | none | interview | use topic |\n")
        self.assertIn("UC9", self.reasons())

    def test_graph_unknown_cycle_and_late_prerequisite(self):
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph.replace("| CO1 | - |", "| CO1 | CO9 |"))
        self.assertIn("CO9", self.reasons())
        self.art("CONCEPT_GRAPH.md", graph +
                 "| CO2 | CO1 | novice | DA_INSEGNARE | - | ai_docs/solutions/courses/intro/sources.md#claim1 | O2 |\n")
        self.assertTrue(any(f.item == "CO2" for f in self.findings()))  # not taught yet
        self.art("CONCEPT_GRAPH.md", graph.replace("| CO1 | - |", "| CO1 | CO2 |") +
                 "| CO2 | CO1 | novice | DA_INSEGNARE | - | ai_docs/solutions/courses/intro/sources.md#claim1 | O2 |\n")
        self.assertIn("cycle", self.reasons().lower())
        # The same graph without a cycle still rejects an untaught prerequisite.
        self.art("CONCEPT_GRAPH.md", graph.replace("| CO1 | - |", "| CO1 | CO2 |") +
                 "| CO2 | - | novice | DA_INSEGNARE | - | ai_docs/solutions/courses/intro/sources.md#claim1 | O2 |\n")
        self.assertIn("taught after", self.reasons())

    def test_inline_prerequisite_order_and_proven_concept(self):
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph +
                 "| CO2 | CO1 | novice | DA_INSEGNARE | - | ai_docs/solutions/courses/intro/sources.md#claim1 | O1 |\n")
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("| CO1 |", "| CO1, CO2 |"))
        self.assertFalse([f for f in self.findings() if f.severity == "ERROR"])
        self.art("COURSE_PLAN.md", plan.replace("| CO1 |", "| CO2, CO1 |"))
        self.assertIn("taught after", self.reasons())
        self.art("CONCEPT_GRAPH.md", graph.replace("DA_INSEGNARE", "PROVATO").replace(
            "| - | novice | PROVATO | - |",
            "| - | novice | PROVATO | ai_docs/solutions/courses/intro/D-UC.md#evidence-1 |"))
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "\n## evidence-1\nAn observed result for novice.\n")
        self.art("COURSE_PLAN.md", plan.replace("| CO1 |", "| - |"))
        self.assertNotIn("concept has no teaching module", self.reasons())

    def test_provato_requires_evidence_and_references_exist(self):
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph.replace("DA_INSEGNARE", "PROVATO"))
        self.assertIn("PROVATO", self.reasons())
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("modules/M1.md#explanation", "missing.md#x"))
        self.assertIn("missing.md", self.reasons())

    def test_profile_objective_feedback_and_module_links(self):
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("| M1 | novice | O1 |",
                                                "| M1 | expert | O9 |"))
        self.assertIn("objective not defined", self.reasons())
        self.assertIn("profile differs", self.reasons())
        self.art("COURSE_PLAN.md", plan.replace("| end |", "| M9 |"))
        self.assertIn("next module does not exist", self.reasons())
        self.art("D-IC.md", "| Flow ID | Surface | Conditions | Feedback channel |\n"
                 "|---|---|---|---|\n| IC1 | module | browser |  |\n")
        self.assertIn("feedback channel", self.reasons())

    def test_empty_tables_are_not_a_course(self):
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph.rsplit("| CO1", 1)[0])
        self.art("COURSE_PLAN.md", plan.rsplit("| M1", 1)[0])
        self.assertIn("concept table missing or empty", self.reasons())
        self.assertIn("module table missing or empty", self.reasons())

    def test_code_workstream_name_does_not_create_a_course(self):
        self.put("solutions/ANALYSIS_course_creator.md",
                 "---\nid: F-058\nstatus: IN_PROGRESS\n---\n# Skill implementation\n")
        self.assertFalse(any("course_creator" in f.file
                             for f in course_check.validate_all(self.root)))

    def test_same_concept_has_independent_states_for_two_profiles(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | CO1 demonstrated | observation | use topic |\n"
                 "\n## expert-evidence\nExpert demonstrated CO1.\n")
        self.art("CONCEPT_GRAPH.md",
                 (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8") +
                 "| CO1 | - | expert | PROVATO | "
                 "ai_docs/solutions/courses/intro/D-UC.md#expert-evidence | "
                 "ai_docs/solutions/courses/intro/sources.md#claim1 | O1 |\n")

        findings = self.findings()

        self.assertEqual([f for f in findings if f.severity == "ERROR"], [])

    def test_unknown_profile_in_graph_and_plan_is_rejected(self):
        for name in ("CONCEPT_GRAPH.md", "COURSE_PLAN.md"):
            self.art(name, (self.course / name).read_text(encoding="utf-8")
                     .replace("novice", "undefined-audience"))

        findings = self.findings()

        for name in ("CONCEPT_GRAPH.md", "COURSE_PLAN.md"):
            self.assertTrue(any(f.file.endswith(name) and
                                "not defined in D-UC" in f.reason for f in findings),
                            findings)

    def test_module_cannot_borrow_another_profiles_prerequisite(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | none | interview | use topic |\n")
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph +
                 "| CO2 | CO1 | expert | DA_INSEGNARE | - | "
                 "ai_docs/solutions/courses/intro/sources.md#claim1 | O2 |\n")
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        module = plan.splitlines()[-1]
        self.art("COURSE_PLAN.md", plan.replace("| end |", "| M2 |") +
                 module.replace("| M1 | novice | O1 | CO1 |",
                                "| M2 | expert | O2 | CO2 |") + "\n")

        findings = self.findings()

        self.assertTrue(any("prerequisite CO1 does not exist for profile expert"
                            in f.reason for f in findings), findings)

    def test_duplicate_profile_concept_and_use_case_pairs_are_rejected(self):
        for name in ("D-UC.md", "CONCEPT_GRAPH.md"):
            body = (self.course / name).read_text(encoding="utf-8")
            self.art(name, body + body.splitlines()[-1] + "\n")

        findings = self.findings()

        for name in ("D-UC.md", "CONCEPT_GRAPH.md"):
            self.assertTrue(any(f.file.endswith(name) and "duplicate" in f.reason
                                for f in findings), findings)

    def test_same_concept_cannot_change_prerequisites_between_profiles(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | none | interview | use topic |\n")
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        row = graph.splitlines()[-1]
        self.art("CONCEPT_GRAPH.md", graph +
                 row.replace("| CO1 | - | novice |", "| CO1 | CO2 | expert |") + "\n" +
                 row.replace("| CO1 | - | novice |", "| CO2 | - | expert |") + "\n")

        findings = self.findings()

        self.assertTrue(any("prerequisites differ between profiles" in f.reason
                            for f in findings), findings)

    def test_each_profile_must_be_taught_its_unproven_concepts(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | uncertain | interview | use topic |\n")
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph +
                 graph.splitlines()[-1].replace("novice", "expert") + "\n")

        findings = self.findings()

        self.assertTrue(any("no teaching module for profile expert" in f.reason
                            for f in findings), findings)

    def test_prerequisite_order_is_checked_separately_for_each_profile(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | uncertain | interview | use topic |\n")
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        base_row = graph.splitlines()[-1]
        self.art("CONCEPT_GRAPH.md", graph +
                 base_row.replace("novice", "expert") + "\n" +
                 base_row.replace("| CO1 | - |", "| CO2 | CO1 |") + "\n" +
                 base_row.replace("| CO1 | - | novice |", "| CO2 | CO1 | expert |") + "\n")
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        module = plan.splitlines()[-1]
        header = plan.rsplit(module, 1)[0]
        ordered = header + module.replace("| CO1 |", "| CO1, CO2 |")
        ordered = ordered.replace("| end |", "| M2 |") + "\n" + module.replace(
            "| M1 | novice | O1 | CO1 |", "| M2 | expert | O1 | CO1, CO2 |") + "\n"
        self.art("COURSE_PLAN.md", ordered)
        self.assertEqual([f for f in self.findings() if f.severity == "ERROR"], [])

        self.art("COURSE_PLAN.md", ordered.replace(
            "| M2 | expert | O1 | CO1, CO2 |", "| M2 | expert | O1 | CO2, CO1 |"))
        findings = self.findings()

        self.assertTrue(any("taught after its dependent concept for profile expert"
                            in f.reason for f in findings), findings)

    def test_proven_prerequisite_for_one_profile_does_not_exempt_another(self):
        self.art("D-UC.md", (self.course / "D-UC.md").read_text(encoding="utf-8") +
                 "| UC1 | expert | CO1 demonstrated | observation | use topic |\n"
                 "\n## expert-evidence\nExpert demonstrated CO1.\n")
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        base_row = graph.splitlines()[-1]
        expert_row = base_row.replace("| novice | DA_INSEGNARE | - |",
            "| expert | PROVATO | ai_docs/solutions/courses/intro/D-UC.md#expert-evidence |")
        self.art("CONCEPT_GRAPH.md", graph + expert_row + "\n" +
                 base_row.replace("| CO1 | - |", "| CO2 | CO1 |") + "\n")
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("| CO1 |", "| CO2 |"))

        findings = self.findings()

        self.assertTrue(any("taught after its dependent concept for profile novice"
                            in f.reason for f in findings), findings)

    def test_documented_ci_bundle_runs_course_validation(self):
        skill = Path(__file__).resolve().parent.parent
        instructions = (skill / "ENFORCEMENT.md").read_text(encoding="utf-8")
        recipe = instructions.split("## 2. Check in CI", 1)[1].split("Then add", 1)[0]
        scripts = re.findall(r"`(scripts/[a-z_]+\.py)`", recipe)
        bundle = self.root / "ci-tools"
        bundle.mkdir()
        for rel in scripts:
            shutil.copyfile(skill / rel, bundle / Path(rel).name)
        command = [sys.executable, "-B", "-I", str(bundle / "sdlc_check.py"),
                   "course", "intro", "--root", str(self.root)]

        valid = subprocess.run(command, capture_output=True, text=True)

        self.assertEqual(valid.returncode, 0, valid.stdout + valid.stderr)
        self.assertIn("course: 0 error(s)", valid.stdout)
        (self.course / "CONCEPT_GRAPH.md").unlink()
        invalid = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(invalid.returncode, 1, invalid.stdout + invalid.stderr)
        self.assertIn("CONCEPT_GRAPH.md missing file", invalid.stdout)
        self.assertNotIn("Traceback", invalid.stderr)

    def test_required_columns_rows_and_trace_fields(self):
        self.art("D-UC.md", "| UC ID |\n|---|\n| UC1 |\n")
        self.assertIn("missing or empty table", self.reasons())
        self.art("D-UC.md", "| UC ID | Profile | Starting knowledge | Evidence | Need |\n"
                 "|---|---|---|---|---|\n| UC1 | novice | none |\n")
        self.assertIn("missing or empty table", self.reasons())
        graph = (self.course / "CONCEPT_GRAPH.md").read_text(encoding="utf-8")
        self.art("CONCEPT_GRAPH.md", graph.replace(
            "ai_docs/solutions/courses/intro/sources.md#claim1 | O1", "- | O1"))
        self.assertIn("source missing", self.reasons())
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("| CO1 |", "| - |"))
        self.assertIn("concepts missing", self.reasons())

    def test_symlinked_course_metadata_is_not_read(self):
        outside = self.root.parent / (self.root.name + "_metadata.md")
        outside.write_text("---\ndomain: course\n---\n", encoding="utf-8")
        self.addCleanup(outside.unlink)
        link = self.docs / "solutions/ANALYSIS_course_escape.md"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.assertIn("unsafe course metadata", "\n".join(
            f.reason for f in course_check.validate_all(self.root)))

    def test_path_traversal_and_external_symlink_are_rejected(self):
        plan = (self.course / "COURSE_PLAN.md").read_text(encoding="utf-8")
        self.art("COURSE_PLAN.md", plan.replace("modules/M1.md#explanation", "../outside.md#x"))
        self.assertIn("unsafe", self.reasons().lower())
        outside = self.root.parent / (self.root.name + "_secret.md")
        outside.write_text("# secret", encoding="utf-8")
        self.addCleanup(outside.unlink)
        link = self.course / "link.md"
        try:
            link.symlink_to(outside)
        except OSError:
            self.skipTest("symlinks unavailable")
        self.art("COURSE_PLAN.md", plan.replace("modules/M1.md#explanation",
                                                 "ai_docs/solutions/courses/intro/link.md#secret"))
        self.assertIn("unsafe", self.reasons().lower())

    def test_entry_point_composes_course_checks(self):
        self.assertEqual(sdlc_check.main(["course", "intro", "--root", str(self.root)]), 0)
        (self.course / "CONCEPT_GRAPH.md").unlink()
        self.assertEqual(sdlc_check.main(["course", "intro", "--root", str(self.root)]), 1)
        self.assertEqual(sdlc_check.main(["validate", "--root", str(self.root)]), 1)


if __name__ == "__main__":
    unittest.main()
