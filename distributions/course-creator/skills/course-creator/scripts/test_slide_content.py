"""Integration checks for the authored source, using the existing course fixture."""
import unittest
import test_course_check


class AuthoredContent(unittest.TestCase):
    def setUp(self):
        self.fixture = test_course_check.CourseChecks()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.course = self.fixture.course
        self.base = 'ai_docs/solutions/courses/intro/SLIDE_CONTENT.md'
        self.plan = (self.course / 'COURSE_PLAN.md').read_text(encoding='utf-8')

    def errors(self):
        return [f.reason for f in self.fixture.findings() if f.severity == 'ERROR']

    def source(self):
        text = '''# Intro
Course version: 1.0
Delivery mode: self-study
Efficacy: efficacy not verified
Feedback flow: IC1

## Course Value
| Profile | Baseline | Target capability | Teaching contribution | Observable check | Alternative and limits |
|---|---|---|---|---|---|
| novice | Counts only | Compare unequal groups | Explain denominator | BASE#s02 | Definitions do not resolve the new case |
'''.replace('BASE', self.base)
        for number, role in ((1, 'explanation'), (2, 'check'), (3, 'solution')):
            text += f'\n## S0{number}\nModule: M1\nObjective: O1\nRole: {role}\nTitle: Ratios\nValue contribution: Reason about group size\n'
            if role == 'check':
                text += 'Solution: S03\n'
            for heading in ('Learner content', 'Complete explanation', 'Visual content', 'Transition'):
                text += f'\n### {heading}\nAuthored material for {role}.\n'
            text += '\n### Sources\n- ai_docs/solutions/courses/intro/sources.md#claim1\n'
        return text

    def activate(self, source=None):
        self.fixture.art('COURSE_PLAN.md', 'Content contract: slide-content-v1\n' + self.plan.replace(
            'ai_docs/solutions/courses/intro/modules/M1.md#explanation', self.base + '#s01').replace(
            'ai_docs/solutions/courses/intro/modules/M1.md#check', self.base + '#s02'))
        self.fixture.art('SLIDE_CONTENT.md', self.source() if source is None else source)

    def test_valid_and_legacy_migration(self):
        self.assertFalse(self.errors())
        self.assertTrue(any('legacy course' in f.reason for f in self.fixture.findings()))
        self.activate()
        self.assertEqual(self.errors(), [])

    def test_new_missing_unknown_empty_and_duplicate_contracts(self):
        for declaration in ('slide-content-v1', 'mystery', ''):
            with self.subTest(declaration=declaration):
                self.fixture.art('COURSE_PLAN.md', f'Content contract: {declaration}\n' + self.plan)
                self.assertTrue(self.errors())
        self.activate()
        path = self.course / 'COURSE_PLAN.md'
        self.fixture.art('COURSE_PLAN.md', 'Content contract: slide-content-v1\n' + path.read_text(encoding='utf-8'))
        self.assertTrue(self.errors())

    def test_content_and_traceability_defects(self):
        mutations = {
            'version': ('Course version: 1.0', 'Course version: 2.0'),
            'delivery': ('Delivery mode: self-study', 'Delivery mode: deck'),
            'empty': ('Authored material for explanation.', ''),
            'module': ('Module: M1', 'Module: M99'),
            'objective': ('Objective: O1', 'Objective: O9'),
            'solution': ('Solution: S03', 'Solution: S99'),
            'earlier solution': ('Solution: S03', 'Solution: S01'),
            'profile': ('| novice |', '| expert |'),
            'value check': ('BASE#s02', 'BASE#s01'),
            'unsafe': ('ai_docs/solutions/courses/intro/sources.md#claim1', '../outside.md#secret'),
            'missing locator': ('sources.md#claim1', 'sources.md#missing'),
            'duplicate': ('## S03', '## S02'),
            'missing check': ('Role: check', 'Role: explanation'),
            'field duplicate': ('Title: Ratios', 'Title: Ratios\nTitle: Again'),
        }
        for name, (old, new) in mutations.items():
            with self.subTest(name=name):
                self.activate(self.source().replace(old.replace('BASE', self.base), new.replace('BASE', self.base)))
                self.assertTrue(self.errors(), name)

    def test_new_plan_cannot_point_at_old_or_pptx_explanation(self):
        self.activate()
        for ref in ('modules/M1.md#explanation', 'assets/lesson.pptx#slide=1'):
            self.fixture.art('COURSE_PLAN.md', 'Content contract: slide-content-v1\n' + self.plan.replace('modules/M1.md#explanation', ref))
            self.assertTrue(self.errors())

    def test_explicit_non_slide_exception(self):
        self.activate()
        path = self.course / 'COURSE_PLAN.md'
        plan = path.read_text(encoding='utf-8').replace('slide-content-v1', 'text-content-v1').replace('SLIDE_CONTENT', 'COURSE_CONTENT').replace('#s0', '#u0')
        source = self.source().replace('SLIDE_CONTENT', 'COURSE_CONTENT').replace('#s0', '#u0').replace('## S0', '## U0').replace('Solution: S03', 'Solution: U03')
        self.fixture.art('COURSE_CONTENT.md', source)
        self.fixture.art('COURSE_PLAN.md', plan)
        self.assertTrue(self.errors())
        self.fixture.art('COURSE_PLAN.md', 'Format exception: Owner requested an audio lesson.\n' + plan)
        self.assertEqual(self.errors(), [])

    def test_content_file_symlink_cannot_escape_root(self):
        import tempfile
        from pathlib import Path
        self.activate()
        target = self.course / 'SLIDE_CONTENT.md'
        target.unlink()
        with tempfile.TemporaryDirectory() as outside:
            other = Path(outside) / 'source.md'
            other.write_text(self.source(), encoding='utf-8')
            try:
                target.symlink_to(other)
            except OSError:
                self.skipTest('symlink privilege unavailable')
            self.assertTrue(any('unsafe' in reason for reason in self.errors()))

    def two_modules(self, second_profile='novice'):
        self.activate()
        path = self.course / 'COURSE_PLAN.md'
        plan = path.read_text(encoding='utf-8')
        row = next(line for line in plan.splitlines() if line.startswith('| M1 |'))
        second = row.replace('| M1 |', '| M2 |').replace('| novice |', f'| {second_profile} |').replace('| O1 |', '| O2 |').replace('| CO1 |', '| CO2 |')
        self.fixture.art('COURSE_PLAN.md', plan.replace(row, row.replace('| end |', '| M2 |') + '\n' + second))
        graph = (self.course / 'CONCEPT_GRAPH.md').read_text(encoding='utf-8')
        graph_row = next(line for line in graph.splitlines() if line.startswith('| CO1 |'))
        self.fixture.art('CONCEPT_GRAPH.md', graph + graph_row.replace('| CO1 |', '| CO2 |').replace('| novice |', f'| {second_profile} |').replace('| O1 |', '| O2 |') + '\n')
        if second_profile != 'novice':
            duc = (self.course / 'D-UC.md').read_text(encoding='utf-8')
            duc_row = next(line for line in duc.splitlines() if line.startswith('| UC1 |'))
            self.fixture.art('D-UC.md', duc + duc_row.replace('| novice |', f'| {second_profile} |') + '\n')
        source = self.source().replace('Objective: O1', 'Objective: O1\nCovers: M2/O2')
        if second_profile != 'novice':
            value_row = next(line for line in source.splitlines() if line.startswith('| novice |'))
            source = source.replace(value_row, value_row + '\n' + value_row.replace('| novice |', f'| {second_profile} |'))
        self.fixture.art('SLIDE_CONTENT.md', source)
        return source

    def test_cumulative_check_and_shared_explanation(self):
        source = self.two_modules()
        self.assertEqual(self.errors(), [])
        # Remove second-objective coverage only from the check.
        self.fixture.art('SLIDE_CONTENT.md', source.replace('Covers: M2/O2\nRole: check', 'Role: check'))
        self.assertTrue(self.errors())
        # A cumulative answer must cover everything the question assessed.
        self.fixture.art('SLIDE_CONTENT.md', source.replace('Covers: M2/O2\nRole: solution', 'Role: solution'))
        self.assertTrue(any('covering every' in reason for reason in self.errors()))

    def test_shared_units_across_profiles_and_unknown_coverage(self):
        source = self.two_modules('expert')
        self.assertEqual(self.errors(), [])
        self.fixture.art('SLIDE_CONTENT.md', source.replace('Covers: M2/O2', 'Covers: M9/O2'))
        self.assertTrue(any('coverage' in reason for reason in self.errors()))
        self.fixture.art('SLIDE_CONTENT.md', source.replace('Covers: M2/O2', 'Covers: M2/O1'))
        self.assertTrue(self.errors())


if __name__ == '__main__':
    unittest.main()
