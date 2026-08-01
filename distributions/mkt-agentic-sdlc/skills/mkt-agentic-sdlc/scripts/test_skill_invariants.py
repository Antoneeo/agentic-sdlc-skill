#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Static skill-invariant battery (M4 Unit 4) -- the deterministic release gate.

Asserts the skill's OWN doctrine invariants: every M4 unit output is present and
wired, support-file pointers resolve, and the generated indexes are idempotent.
Stdlib only, zero-LLM, zero-network, zero-subprocess -- a failing eval is always
a real regression, never flakiness (P-TM T9). Runs as part of
`python -m unittest discover -s scripts -p "test_*.py"`.
"""
import contextlib
import io
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sdlc_core as sc  # noqa: E402  spine behaviour comes from the core
import entry_point  # noqa: E402
entry_point.load()  # importing the overlay is what REGISTERS this distribution's profile
dist = sc            # ...which the core then answers for: one place, whatever the overlay is called

# file sits at skills/agentic-sdlc-skill/scripts/ -> parents[1] = skill dir,
# parents[3] = repo root where ai_docs/ lives (matches test_plan.py:229).
SKILL_DIR = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[3]


def read(rel):
    return sc.read_text(SKILL_DIR / rel)


def setUpModule():
    """Pin the docs root for this battery's fixtures.

    The marketing overlay defaults to `mkt_docs`, so a shared battery that builds
    `ai_docs` fixtures must say which root it means instead of inheriting whichever
    distribution happens to be installed."""
    global _SAVED_DOCS_DIR
    _SAVED_DOCS_DIR = sc.docs_dir()
    sc.set_docs_dir("ai_docs")


def tearDownModule():
    sc.set_docs_dir(_SAVED_DOCS_DIR)


def requires(capability):
    """Guard a PROFILE-specific assertion.

    Only OPTIONAL capabilities can be skipped: `test_profile_declares_every_spine_
    capability` refuses a profile that drops a spine one, so editing your own profile
    is never a way out of the doctrine -- only a way to declare an overlay this
    distribution genuinely does not have. A skip here is a declared decision, visible
    in one line of the entry point, not a silently absent test.
    """
    def decorate(fn):
        return unittest.skipUnless(
            dist.has_capability(capability),
            f"{dist.profile()['skill_name']} does not claim the '{capability}' overlay",
        )(fn)
    return decorate


class SharedProfileInvariants(unittest.TestCase):
    """Run identically in every distribution: the profile itself is the subject."""

    def test_profile_declares_every_spine_capability(self):
        missing = dist.REQUIRED_CAPABILITIES - dist.profile()["capabilities"]
        self.assertEqual(missing, set(),
                         "a distribution may not drop spine doctrine by editing its own "
                         f"profile; missing: {sorted(missing)}")

    def test_profile_claims_no_unknown_capability(self):
        known = dist.REQUIRED_CAPABILITIES | dist.OPTIONAL_CAPABILITIES
        unknown = dist.profile()["capabilities"] - known
        self.assertEqual(unknown, set(),
                         f"unknown capability claimed: {sorted(unknown)} -- add it to "
                         "OPTIONAL_CAPABILITIES in the core, so every distribution sees it")

    def test_every_declared_support_file_exists(self):
        for rel in dist.profile()["support_files"]:
            self.assertTrue((SKILL_DIR / rel).is_file(),
                            f"profile declares {rel}, which is not on disk")

    def test_every_support_file_on_disk_is_declared(self):
        """The other direction: an undeclared file is doctrine nothing points at."""
        declared = set(dist.profile()["support_files"]) | {"SKILL.md"}
        on_disk = {p.name for p in SKILL_DIR.glob("*.md")}
        self.assertEqual(on_disk - declared, set(),
                         "support files exist but are not in the profile: either wire them "
                         "or delete them")

    def test_the_skill_name_matches_the_manifest(self):
        head = read("SKILL.md").split("---")[1]
        self.assertIn(f"name: {dist.profile()['skill_name']}", head,
                      "the profile and SKILL.md disagree about which skill this is")


class SkillInvariants(unittest.TestCase):

    def test_orient_registered(self):
        self.assertTrue(hasattr(sc, "cmd_orient"))
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(sc.main(["orient", "--root", d]), 0)

    def test_enforcement_sections_present(self):
        t = read("ENFORCEMENT.md")
        self.assertIn("## 4. SessionStart hook", t)
        self.assertIn("## 5. Skill eval battery", t)

    def test_skill_consult_trigger(self):
        t = read("SKILL.md")
        self.assertIn("consult the guide router", t)
        self.assertIn("Consult (before acting)", t)

    def test_rule_zero_declares_router_verdict(self):
        """F-016 move A: the consult lives on the ALWAYS-executed path. Rule Zero
        makes the router lookup a DECLARED output, so 'did not look' is
        distinguishable from 'looked, no match'. L1 stays exempt."""
        t = read("SKILL.md")
        self.assertIn("router verdict", t)
        self.assertIn("router: no match", t)
        head = t.split("## Write Triggers")[0]
        self.assertIn("router verdict", head,
                      "the router verdict must be declared in Rule Zero, "
                      "not only later in the workflow")

    def test_phase1_reads_guide_router(self):
        """F-016 move B: Phase 1 (the only always-run read step) reads the guide
        router, not just README + INDEX."""
        t = read("SKILL.md")
        self.assertIn("`ai_docs/reference/INDEX.md` (the guide router)", t)
        self.assertIn("reference/INDEX.md", read("templates.md"),
                      "the README template must seed the router as a must-read")

    @requires("comprehension_guides")
    def test_code_guide_trigger_has_a_phase(self):
        """F-016 move D: the source_kind: code Write-Triggers row must name a real
        phase. Phase 'any' is nobody's phase -- the duty then never fires."""
        t = read("SKILL.md")
        row = [ln for ln in t.splitlines()
               if "`source_kind: code`" in ln and ln.lstrip().startswith("|")]
        self.assertTrue(row, "Write-Triggers row for source_kind: code missing")
        self.assertNotIn("| any |", row[0])
        self.assertIn("Comprehension checkpoint", t)

    def test_enforcement_hook_is_recommended_default(self):
        """F-016 move C: the orient hook is the only non-prompt backstop -- it is
        a recommended default, no longer merely optional."""
        t = read("ENFORCEMENT.md")
        self.assertIn("recommended default", t)
        self.assertNotIn("## 4. SessionStart hook (orientation, optional)", t)

    def test_parallel_handoff_wired(self):
        """F-019: the handoff is a workstream REGISTRY (one row per open
        workstream, parallel-safe), with volatile resume logistics in ephemeral
        HANDOFF_[feature].md files deleted at closure. Durable narrative stays in
        the ANALYSIS Diary (DRY)."""
        unit = dist.profile()["unit_noun"]
        skill = read("SKILL.md")
        self.assertIn(f"HANDOFF_[{unit}].md", skill)
        self.assertIn("workstream registry", skill)
        tpl = read("templates.md")
        self.assertIn(f"HANDOFF_[{unit}].md", tpl)
        self.assertIn("resume logistics", tpl,
                      "the Diary/logistics boundary must be stated in the template")
        # A shipped format change without a migration clause strands existing projects
        # -- but only a distribution that HAS shipped one owes the clause.
        if dist.has_capability("legacy_narrative_handoff"):
            self.assertIn("pre-1.17", skill)
            self.assertIn("pre-1.17", tpl)

    def test_vision_discipline_wired(self):
        """F-018: a Vision is a gate, and the discipline that makes it verifiable
        by a cold reader is single-sourced in vision.md and reachable from the
        Vision Gate phase, the Write-Triggers row and the template."""
        v = read("vision.md")
        for anchor in ("## What a Vision IS", "deletion test",
                       "## 1. The nine properties", "## 4. Minimum operable sections",
                       "## 6. The blind check"):
            self.assertIn(anchor, v, f"vision.md missing {anchor}")
        self.assertIn("benefit", read("elicitation.md"),
                      "elicitation must ask for the benefit, not accept a mechanism")
        skill = read("SKILL.md")
        self.assertIn("blind check", skill,
                      "the Vision Gate must route promotion through the blind check")
        self.assertIn("vision.md", skill)
        self.assertIn("vision.md", read("templates.md"),
                      "the Vision template must point at the drafting discipline")

    @requires("question_discipline")
    def test_question_discipline_wired(self):
        """F-026: a question to the user is legal only if searched-first (search
        named) and it names the blocked decision. Wired in the file that owns it
        AND on the always-read path -- a rule only L3-phase-3 readers see never
        reaches the L1/L2 question."""
        e = read("elicitation.md")
        for anchor in ("## The question discipline", "Searched first",
                       "names what is blocked", "Generic confirmation",
                       "Preference-fishing", "Default non-blocking",
                       "Blocking is reserved"):
            self.assertIn(anchor, e, f"elicitation.md missing {anchor}")
        skill = read("SKILL.md")
        head = skill.split("## Write Triggers")[0]
        self.assertIn("question discipline", head,
                      "the legality test must be reachable from Rule Zero, "
                      "not only from the phase-3 round")

    @requires("architect_pass")
    def test_architect_pass_wired(self):
        """F-020: the architect pass runs at L3 between elicitation and the
        Impact -- capabilities ruled against the platform before files are
        listed. Wired end to end: discipline file, phase-3 invocation, the
        ANALYSIS section that records it, and the review clause that checks it."""
        a = read("architect.md")
        for anchor in ("## 1. State the feature as capabilities, not as files",
                       "## 2. Rule each capability against the platform",
                       "## 4. Decide the unit of change", "MISSING",
                       "Feature-shaped platform", "Silent degradation"):
            self.assertIn(anchor, a, f"architect.md missing {anchor}")
        skill = read("SKILL.md")
        self.assertIn("Architect before you list files", skill,
                      "phase 3 must invoke the pass before the Impact")
        phase3 = skill.split("### 3. Request Analysis")[1].split("### 4.")[0]
        self.assertIn("architect.md", phase3)
        self.assertLess(phase3.index("Architect before you list files"),
                        phase3.index("Blast-radius enumeration"),
                        "the architect pass precedes the blast radius: "
                        "capabilities are ruled before files are listed")
        minsec = skill.split("Minimum sections:")[1].splitlines()[0]
        self.assertIn("Capability Ledger", minsec,
                      "the ledger must be named on the L3 minimum-sections line "
                      "itself, not merely somewhere in the file")
        tpl = read("templates.md")
        self.assertIn("## Capability Ledger", tpl)
        self.assertLess(tpl.index("## Capability Ledger"),
                        tpl.index("## Impact"),
                        "the ledger section precedes Impact, which it feeds")
        self.assertIn("Capability Ledger", read("review.md"),
                      "the closure review must map the ledger, or the pass is "
                      "authored and never checked")

    @requires("architect_pass")
    def test_component_map_wired(self):
        """F-020b: the pass is only repeatable across sessions if what gets built
        lands in a durable inventory. The Component Map is that inventory, and its
        write trigger is the component's BIRTH -- keyed on the stack, a new
        component never fires it and the map rots silently."""
        self.assertIn("## Component Map", read("templates.md"),
                      "the architecture template must carry the map")
        a = read("architect.md")
        self.assertIn("## Component Map", a,
                      "the pass must READ the map before searching the code")
        self.assertIn("Component Map", read("review.md"),
                      "a built component missing from the map must be a finding")
        skill = read("SKILL.md")
        rows = [ln for ln in skill.splitlines()
                if "Component Map" in ln and ln.lstrip().startswith("|")]
        self.assertTrue(rows, "Write-Triggers row for the Component Map missing")
        self.assertIn("BORN", rows[0],
                      "the trigger must key on the component's birth, not on a "
                      "stack change the birth would never fire")
        self.assertIn("DISCOVERED", rows[0],
                      "a component the pass merely FINDS must also land in the "
                      "map: marking the area ANALYZED while the map stays silent "
                      "lets the next feature rule it MISSING and build it twice")
        self.assertIn("DISCOVERED", read("review.md"),
                      "the discovered-component duty needs its mirror finding")
        # dogfood: this repo's own architecture doc carries a real map
        arch_p = REPO / "ai_docs" / "strategic" / "architecture.md"
        if arch_p.is_file():
            self.assertIn("## Component Map", sc.read_text(arch_p))

    @requires("architect_pass")
    def test_unmapped_never_grounds_missing(self):
        """F-020c: on a project the methodology just arrived in, the map is nearly
        all silence. Silence is UNREAD, not EMPTY -- reading it as empty designs a
        duplicate of the existing codebase. The incremental licence covers writing
        the inventory, never comprehension of what the change touches."""
        a = read("architect.md")
        self.assertIn("Empty-map MISSING", a,
                      "the anti-pattern must be named to be reviewable")
        self.assertIn("never ground a MISSING", a)
        self.assertIn("cache of evidence somebody already paid for", a,
                      "the map is a cache of evidence, not a substitute for it")
        self.assertIn("never the STANDARD of one", a,
                      "a cache hit may not lower the evidence bar for a verdict")
        self.assertIn("Understanding is never deferred", a,
                      "the licence defers the artifact, not the comprehension")
        skill = read("SKILL.md")
        self.assertIn("No full-codebase sweep is required before the first feature",
                      skill, "an unbounded up-front sweep is skipped silently, "
                             "which is worse than an incremental map")
        self.assertIn("audit/audit_plan.md` FIRST", skill,
                      "the scope ledger precedes the documents built on it")
        self.assertIn("ANALYZED", read("review.md"),
                      "an unfalsifiable MISSING on unmapped ground must be a finding")
        self.assertIn("unread, not empty", read("templates.md"),
                      "the map template must declare its own coverage limit")

    @requires("architect_pass")
    def test_backstops_are_advisory_not_a_gate(self):
        """F-020e: the accepted ceremony budget was a SIGNAL. --strict turns
        warnings into exit 1 and ENFORCEMENT recommends it in CI, so routing the
        architect-pass checks through `warnings` would ship a blocking gate the
        owner never accepted. They must be advisories, inert under --strict."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            sol = root / "ai_docs" / "solutions"
            sol.mkdir(parents=True)
            vis = root / "ai_docs" / "vision"
            vis.mkdir()
            for name in sc.VISION_FILES:
                (vis / name).write_text(f"# {name}\nStatus: APPROVED (by owner)\n",
                                        encoding="utf-8")
            (sol / "ANALYSIS_x.md").write_text(
                "---\nid: F-1\nfeature: X\nstatus: COMPLETED\nlevel: L3\n"
                "start_date: 2026-08-01\nend_date: 2026-08-02\n---\n"
                "# X\n## Objective\no\n## Feature Vision\nv\n## Impact\ni\n"
                "## Security and Threat Model\ns\n## Action Plan\n- [x] a\n"
                "## Test Strategy\nt\n## Diary\nd\n", encoding="utf-8")
            sc.cmd_index(root)  # generated indexes present: isolate the advisory
            self.assertEqual(sc.cmd_validate(root, strict=True), 0,
                             "a missing Capability Ledger must not fail --strict: "
                             "an advisory that reddens CI is a gate under another name")
        a = read("architect.md")
        self.assertIn("not even under `--strict`", a,
                      "the doctrine must state the escalation honestly")

    def test_map_refs_scoped_to_the_where_column(self):
        """R3 BLOCK (found by two independent reviewers): harvesting refs from
        the WHOLE architecture.md let the canonical template's own
        '## Directory Structure' backticks satisfy the mark-counter-check, so it
        was inert on every project that filled that section in."""
        arch = ("# A\n## Directory Structure\n- `billing/` — invoices\n\n"
                "## Component Map\n\n| Component | Capability | Contract | Where |\n"
                "|---|---|---|---|\n| Api | serve | h() | `src/api.py#h` |\n")
        self.assertEqual(sc.map_where_refs(arch), ["src/api.py"],
                         "only the Where column counts; a Directory Structure "
                         "backtick must not silence the check")
        self.assertIsNone(sc.map_where_refs("# A\n## Other\n- `x/y.py`\n"),
                          "no Component Map at all -> None, not an empty claim")
        self.assertEqual(sc.map_where_refs(
            "## Component Map\n\n| Component | Capability |\n|---|---|\n| A | b |\n"), [],
            "a map with no Where column maps nothing -> [], not None")
        # symbol stripped and separators normalized, so a file-area row can match
        arch2 = arch.replace("`src/api.py#h`", "`src\\api.py#h`")
        self.assertEqual(sc.map_where_refs(arch2), ["src/api.py"])

    def test_prose_is_never_reported_as_rot(self):
        """R3: `Next.js`/`Node.js`/`OrderStore.save` were reported as rotting
        paths. A false rot trains the reader to ignore the channel."""
        for token in ("Next.js", "Node.js", "Vue.js", "React.js",
                      "OrderStore.save", "app.core", "1.18.0"):
            self.assertEqual(sc._map_refs(f"`{token}`"), [],
                             f"'{token}' is prose, not a file ref")
        # the exclusion is scoped to the .js framework-name case ONLY: a blanket
        # CamelCase rule silences exactly what React/C#/Java projects map
        for real in ("run_behavioral.py", "init.js", "src/a.py#F", "README.md",
                     "App.tsx", "Program.cs", "Main.java", "Cargo.toml"):
            self.assertTrue(sc._map_refs(f"`{real}`"),
                            f"'{real}' is a real ref and must stay checked")

    def test_new_checks_never_redden_strict_ci(self):
        """R3 BLOCK: the 'level missing' guard shipped as a WARNING, which
        --strict escalates to exit 1 -- the exact defect the advisories bucket
        was invented for, reintroduced one round later. Bootstrap DRAFT visions
        had the same problem: the skill mandates DRAFT, so --strict was red on
        every freshly bootstrapped project."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            vis = root / "ai_docs" / "vision"
            vis.mkdir()
            for name in sc.VISION_FILES:      # bootstrap state: DRAFT by mandate
                (vis / name).write_text(f"# {name}\nStatus: DRAFT\n", encoding="utf-8")
            (root / "ai_docs" / "solutions" / "ANALYSIS_old.md").write_text(
                "---\nid: F-9\nfeature: Legacy\nstatus: COMPLETED\n"
                "start_date: 2024-01-01\nend_date: 2024-02-01\n---\n"
                "# L\n## Objective\no\n## Feature Vision\nv\n## Impact\ni\n"
                "## Security and Threat Model\ns\n## Action Plan\n- [x] a\n"
                "## Test Strategy\nt\n## Diary\nd\n", encoding="utf-8")
            sc.cmd_index(root)
            self.assertEqual(sc.cmd_validate(root, strict=True), 0,
                             "a pre-1.18 analysis with no `level:` and a bootstrap "
                             "DRAFT vision must not fail --strict")

    def test_router_stub_written_with_zero_guides(self):
        """R3 BLOCK: Rule Zero makes reading the router mandatory and forbids
        faking `no match`, but `index` refused to write it without guides -- so
        the required verdict was unsatisfiable on every new project."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "reference").mkdir(parents=True)
            sc.cmd_index(root)
            gidx = root / "ai_docs" / "reference" / "INDEX.md"
            self.assertTrue(gidx.is_file(), "the router must exist even with zero guides")
            self.assertIn("no match", sc.read_text(gidx),
                          "the stub must name the honest verdict")
            # ...but with guides PRESENT a missing router is still an ERROR: the
            # agent's mandatory lookup would find nothing and legally declare
            # 'absent', so the guide governing the work is never consulted
            (root / "ai_docs" / "reference" / "GUIDE_x.md").write_text(
                "---\ndescription: when to do x\nstatus: CURRENT\nsource_kind: document\n"
                "source: s\ndistilled_from: ai_docs/reference/.sources/x.md\n"
                "source_hash: abc\n---\n# Guide: X\n## How to do X\n[source: x.md#a]\ndo x\n",
                encoding="utf-8")
            gidx.unlink()
            self.assertEqual(sc.cmd_validate(root), 1,
                             "guides without a router must be an ERROR, not an advisory")
        self.assertIn("router: absent", read("guides.md"),
                      "a third legal verdict is needed for a genuinely missing router")

    def test_design_review_gate_wired(self):
        """F-021: in Standalone the ANALYSIS was reviewed only as an INPUT to the
        closure review -- i.e. after the code existed. The design gate fires at
        the END of Phase 3, before implementation, and is logged."""
        r = read("review.md")
        for anchor in ("## When a review is due", "Design review", "Closure review",
                       "declared self-pass", "capped at 3", "REVIEW_LOG.md"):
            self.assertIn(anchor, r, f"review.md missing {anchor}")
        skill = read("SKILL.md")
        self.assertIn("Design review gate", skill)
        before, after = dist.profile()["design_gate_between"]
        p3 = skill.index(before)
        p4 = skill.index(after)
        self.assertTrue(p3 < skill.index("Design review gate") < p4,
                        "the gate must sit after the design exists and before the work is "
                        "executed -- a design review after implementation is the closure review")
        self.assertTrue([ln for ln in skill.splitlines()
                         if "REVIEW_LOG.md" in ln and ln.lstrip().startswith("|")],
                        "Write-Triggers row for the review log missing")
        self.assertIn("REVIEW_LOG.md", read("templates.md"))
        # behavior: the backstop nags only where it should
        due = {"level": "L3", "status": "IN_PROGRESS", "start_date": "2026-07-28"}
        self.assertTrue(sc.design_review_due(due))
        self.assertTrue(sc.design_review_due({**due, "status": "COMPLETED"}))
        self.assertFalse(sc.design_review_due({**due, "status": "PLANNED"}),
                         "the review is due at the END of Phase 3: a design still "
                         "being drafted is not late")
        self.assertFalse(sc.design_review_due({**due, "level": "L2"}))
        self.assertFalse(sc.design_review_due({**due, "start_date": "2026-07-01"}),
                         "work predating the gate is grandfathered")
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "audit" / "reviews").mkdir(parents=True)
            self.assertFalse(sc.review_logged(root, "ANALYSIS_x.md"),
                             "no log file -> not logged")
            (root / sc.review_log_rel()).write_text(
                "| date | doc_key | tier | reviewer | r | r | verdict | n |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| 2026-07-28 | ANALYSIS_x.md | design | subagent | 3 | 3 | PASS | 1 |\n"
                # a CLOSURE row that says 'design' in its reviewer cell: the
                # fixture that made the old whole-row match pass vacuously
                "| 2026-07-28 | ANALYSIS_y.md + diff | closure | subagent - "
                "conformance to the design | 1 | 1 | PASS | 1 |\n"
                "| 2026-07-28 | ANALYSIS_w.md | design (late) | self-pass "
                "(declared; no subagent facility) | 2 | 2 | FAIL | 1 |\n",
                encoding="utf-8")
            self.assertTrue(sc.review_logged(root, "ANALYSIS_x.md"))
            self.assertFalse(sc.review_logged(root, "ANALYSIS_y.md"),
                             "a closure row is not a design review, even when the "
                             "word 'design' appears elsewhere in it")
            self.assertTrue(sc.review_logged(root, "ANALYSIS_w.md"),
                            "'design (late)' is a design review, and a FAIL row counts")
            self.assertFalse(sc.review_logged(root, "ANALYSIS_z.md"))
            # a longer sibling must not satisfy a shorter name's gate
            self.assertFalse(sc.review_logged(root, "ANALYSIS_"),
                             "substring matching lets a sibling ANALYSIS pass")
            # the tier column is located by header, not assumed at index 2
            (root / sc.review_log_rel()).write_text(
                "| # | date | doc_key | tier | reviewer | r | v | n |\n"
                "|---|---|---|---|---|---|---|---|\n"
                "| 1 | 2026-07-28 | ANALYSIS_x.md | design | subagent | 1 | PASS | 1 |\n",
                encoding="utf-8")
            self.assertTrue(sc.review_logged(root, "ANALYSIS_x.md"),
                            "an extra leading column must not produce a permanent, "
                            "unclearable 'you skipped the review'")

    def test_design_review_advisory_end_to_end(self):
        """F-021 closure review F2: the unit tests never exercised cmd_validate,
        so a reviewer's mutation run showed the advisory could be DELETED and the
        battery stayed green. This asserts the wiring itself: it fires, --hybrid
        suppresses it (devPNT owns that slot), and it never moves an exit code."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "solutions").mkdir(parents=True)
            vis = root / "ai_docs" / "vision"
            vis.mkdir()
            for name in sc.VISION_FILES:   # otherwise --strict fails on unrelated warnings
                (vis / name).write_text(f"# {name}\nStatus: APPROVED (by owner)\n",
                                        encoding="utf-8")
            (root / "ai_docs" / "solutions" / "ANALYSIS_f.md").write_text(
                "---\nid: F-1\nfeature: F\nstatus: IN_PROGRESS\nlevel: L3\n"
                "start_date: 2026-08-01\n---\n# F\n## Objective\no\n"
                "## Feature Vision\nv\n## Capability Ledger\n| a |\n## Impact\ni\n"
                "## Security and Threat Model\ns\n## Action Plan\n- [ ] a\n"
                "## Test Strategy\nt\n## Diary\nd\n", encoding="utf-8")
            sc.cmd_index(root)

            def out(**kw):
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    rc = sc.cmd_validate(root, **kw)
                return rc, buf.getvalue()

            rc, text = out()
            self.assertIn("no design-review row", text,
                          "the advisory must fire on an L3 in implementation")
            self.assertEqual(rc, 0, "advisories never move the exit code")
            rc, text = out(hybrid=True)
            self.assertNotIn("no design-review row", text,
                             "--hybrid: devPNT's gate owns the slot, so firing here "
                             "is a permanent unfixable false positive")
            rc, text = out(strict=True)
            self.assertNotIn("no design-review row", text.split("Validation:")[1],
                             "summary sanity")
            self.assertEqual(rc, 0, "--strict must not escalate this advisory")
            # cmd_check must FORWARD hybrid: reverting that forwarding was one of
            # the four mutations that shipped green
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                sc.cmd_check(root, hybrid=True)
            self.assertNotIn("no design-review row", buf.getvalue(),
                             "cmd_check must pass hybrid through to cmd_validate")

    def test_audit_plan_paths_confined(self):
        """R2 BLOCK-1: audit_plan.md is document content, so `stale`/`mark` must
        confine its paths BEFORE walking. An absolute row ('/' -- what init.js
        used to seed) made `root / rel` the drive and crashed relative_to()."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "ai_docs" / "audit").mkdir(parents=True)
            (root / "ai_docs" / "audit" / "audit_plan.md").write_text(
                "# Audit Plan\n\n| Path | Status | Reference | Notes |\n|---|---|---|---|\n"
                "| / | ANALYZED | 2020-01-01T00:00:00Z | |\n"
                "| ../escape | ANALYZED | 2020-01-01T00:00:00Z | |\n", encoding="utf-8")
            self.assertEqual(sc.cmd_stale(root), 0,
                             "hostile rows must be rejected, not walked (and never crash)")
            self.assertEqual(sc.cmd_mark(root, ["../outside"]), 1,
                             "mark must refuse to write an out-of-tree area into the plan")
        seeder = sc.read_text(REPO / "scripts" / "init.js")
        if seeder:
            self.assertNotIn("| / | PENDING", seeder,
                             "the seeded audit-plan row must be '.', not the drive root")

    def test_no_advisory_on_a_fresh_project(self):
        """R2 WARN-3: a brand-new project must come out silent. An advisory on
        day zero, about a placeholder the seeder just wrote, trains the reader to
        ignore the channel -- worse than the rot it reports."""
        tpl = read("templates.md")
        m = re.search(r"^## Component Map$(.*?)^## Architectural Patterns",
                      tpl, re.M | re.S)
        self.assertTrue(m, "architecture template lost its Component Map section")
        adv = []
        sc.check_component_map(REPO, "## Component Map\n" + m.group(1), adv)
        self.assertEqual(adv, [], f"the shipped template must validate silently: {adv}")

    def test_map_refs_no_false_rot(self):
        """R2 N2: a generic extension heuristic turns prose into rot warnings.
        A false 'the map is rotting' is the worst outcome -- it teaches readers
        to ignore the channel."""
        prose = ["app.core", "OrderStore.save", "1.18.0", "agentic-sdlc-init",
                 "https://example.com/x.py", "some prose"]
        for token in prose:
            self.assertEqual(sc._map_refs(f"`{token}`"), [],
                             f"'{token}' is prose, not a path ref")
        for real in ("src/a.py#Foo", "README.md", "scripts\\init.js"):
            self.assertTrue(sc._map_refs(f"`{real}`"), f"'{real}' is a real ref")

    @requires("architect_pass")
    def test_ledger_backstop_bypasses_closed(self):
        """R2 WARN-4: two zero-cost bypasses -- delete the optional `level:` line,
        or mention the heading inside an HTML comment."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            sol = root / "ai_docs" / "solutions"
            sol.mkdir(parents=True)
            body = ("# X\n## Objective\no\n## Feature Vision\nv\n## Impact\ni\n"
                    "## Security and Threat Model\ns\n## Action Plan\n- [x] a\n"
                    "## Test Strategy\nt\n## Diary\nd\n")
            front = ("---\nid: F-1\nfeature: X\nstatus: IN_PROGRESS\n{lvl}"
                     "start_date: 2026-08-01\n---\n")
            (sol / "ANALYSIS_a.md").write_text(front.format(lvl="") + body, encoding="utf-8")
            (sol / "ANALYSIS_b.md").write_text(
                front.format(lvl="level: L3\n") + body
                + "<!-- TODO: write the ## Capability Ledger later -->\n", encoding="utf-8")
            out = []
            sc.cmd_validate(root)
            txt = "\n".join(out)  # noqa: F841 - output asserted via the checks below
            metas = {p.name: meta for p, meta, _ in sc.list_analyses(root)}
            self.assertFalse(sc.ledger_due(metas["ANALYSIS_a.md"]),
                             "a missing level cannot be due -- but it MUST warn")
            self.assertTrue(sc.ledger_due(metas["ANALYSIS_b.md"]))
        # The behaviour lives in the shared core; the entry point is thin by design.
        self.assertIn("'level' missing", sc.read_text(SKILL_DIR / "scripts" / "sdlc_core.py"),
                      "dropping `level:` must not be a free way out of the level's checks")
        # Heading detection, asserted on the FUNCTION (advisories never move the
        # exit code, so a test that only checks rc is green on broken code -- the
        # previous version of this test was exactly that theater).
        body = "# X\n## Objective\no\n"
        self.assertTrue(sc.has_ledger_heading(body + "## Capability Ledger\n| a |\n"))
        self.assertFalse(sc.has_ledger_heading(body + "<!-- ## Capability Ledger -->\n"),
                         "a commented-out heading is not a ledger")
        self.assertFalse(sc.has_ledger_heading(body + "<!-- draft\n## Capability Ledger\n"),
                         "an UNTERMINATED comment must not hide the heading either")
        # ...but an unterminated marker must not nuke a REAL ledger that follows
        self.assertTrue(sc.has_ledger_heading(
            body + "we write `<!--` inline here\n\n## Capability Ledger\n| a |\n"),
            "an inline '<!--' mention must not swallow the rest of the document")
        self.assertTrue(sc.has_ledger_heading(
            body + "```\n<!-- unclosed example\n```\n\n## Capability Ledger\n| a |\n"),
            "an unclosed comment inside a fenced block is an EXAMPLE, not a comment")
        self.assertFalse(sc.has_ledger_heading(body + "### Capability Ledger\n"),
                         "the section is '##', anchored")

    @requires("architect_pass")
    def test_ledger_due_gating(self):
        """F-020d: the ledger warning fires ONLY for active L3 analyses born
        after the pass shipped. Closed history and pre-pass in-flight work
        never nag (the lazy-convert doctrine, same as the pre-1.17 handoff)."""
        due = {"level": "L3", "status": "IN_PROGRESS", "start_date": "2026-07-28"}
        self.assertTrue(sc.ledger_due(due))
        self.assertTrue(sc.ledger_due({**due, "status": "PLANNED"}))
        self.assertTrue(sc.ledger_due({**due, "status": "COMPLETED"}),
                        "status must NOT gate: closure flips the ANALYSIS to "
                        "COMPLETED before `check` runs, so a status filter "
                        "silences the backstop at the only mandated moment")
        self.assertFalse(sc.ledger_due({**due, "start_date": "2026-07-19"}),
                         "pre-pass work is grandfathered -- by date, the only guard")
        self.assertFalse(sc.ledger_due({**due, "level": "L2"}),
                         "the pass is L3-only")
        self.assertFalse(sc.ledger_due({**due, "level": ""}))
        # malformed / quoted / unpadded dates must not silently decide the gate
        self.assertFalse(sc.ledger_due({**due, "start_date": ""}))
        self.assertFalse(sc.ledger_due({**due, "start_date": "28/07/2026"}),
                         "a non-ISO date must not fire on a lexicographic compare")
        self.assertTrue(sc.ledger_due({**due, "start_date": "'2026-08-01'"}),
                        "a YAML-quoted date must not grandfather forever")
        self.assertFalse(sc.ledger_due({**due, "start_date": "2026-7-01"}),
                         "an unpadded pre-epoch date must not read as post-epoch")

    @requires("architect_pass")
    def test_component_map_rot_detected(self):
        """F-020d: a map row whose 'Where' ref no longer resolves, or whose
        #symbol was renamed away, is flagged -- the source_hash equivalent the
        map lacked. Healthy rows stay silent; non-path backticks are ignored."""
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / "src").mkdir()
            (root / "src" / "core.py").write_text(
                "class Notifier:\n    pass\n", encoding="utf-8")
            def warns(where):
                """Rot findings only -- the 'inert map' notice is asserted apart."""
                text = ("## Component Map\n\n"
                        "| Component | Capability it owns | Contract | Where |\n"
                        "|---|---|---|---|\n"
                        f"| Notifier | notify | fire-and-forget | {where} |\n")
                w = []
                sc.check_component_map(root, text, w)
                return [m for m in w if "no checkable path" not in m]
            self.assertEqual(warns("`src/core.py#Notifier`"), [],
                             "a healthy row must stay silent")
            self.assertTrue(warns("`src/gone.py#Notifier`"),
                            "a dead path must warn")
            self.assertTrue(warns("`src/core.py#OldName`"),
                            "a renamed-away symbol must warn")
            self.assertEqual(warns("`bare-name` and `Notifier`"), [],
                             "non-path backticks are prose, not refs")
            self.assertTrue(warns("`../outside/core.py#X`"),
                            "an escaping ref is rejected, fail-closed")
            self.assertEqual(warns("`src/*.py#Notifier`"), [],
                             "glob refs resolve too")
            self.assertEqual(warns("`src\\core.py#Notifier`"), [],
                             "a Windows-separator ref must be normalized, "
                             "not silently skipped as uncheckable")
            self.assertTrue(warns("`src/core.py#Notif`"),
                            "substring symbol matching is a false PASS: the "
                            "match must be on a word boundary")
            self.assertEqual(warns("`https://example.com/core.py`"), [],
                             "a URL is not a repo path")
            self.assertTrue(warns("`core.md#X`"),
                            "an unqualified file-shaped ref must warn, not be "
                            "skipped -- that skip left 9 of this repo's own "
                            "18 refs unchecked")
            # a literal bracket in a path (Next.js dynamic route) is not a glob
            (root / "app").mkdir()
            (root / "app" / "[id].tsx").write_text("export const Page = 1\n",
                                                   encoding="utf-8")
            self.assertEqual(warns("`app/[id].tsx#Page`"), [],
                             "a literal-bracket path that exists must not be "
                             "reported as rot via glob interpretation")
            # inert-check detection: rows present, no checkable ref anywhere
            inert = ("## Component Map\n\n| Component | Capability | Contract | Where |\n"
                     "|---|---|---|---|\n| Notifier | notify | fire | see the code |\n")
            w = []
            sc.check_component_map(root, inert, w)
            self.assertTrue(w, "a map whose rows carry no checkable path is an "
                               "inert check reported as a clean one")
            # the 'Where' column is located by header, not assumed last
            five = ("## Component Map\n\n"
                    "| Component | Capability | Contract | Where | Owner |\n"
                    "|---|---|---|---|---|\n"
                    "| Notifier | notify | fire | `src/gone.py` | team |\n")
            w = []
            sc.check_component_map(root, five, w)
            self.assertTrue(w, "a map with extra columns must still be checked")

    @requires("architect_pass")
    def test_architect_scenarios_present(self):
        """F-020d: the pass's execution is exercised by the behavioral layer --
        one scenario for running the pass at all, one for the brownfield trap
        (map silence must not ground a MISSING)."""
        sys.path.insert(0, str(SKILL_DIR / "evals"))
        import run_behavioral as rb  # noqa: E402
        sdir = SKILL_DIR / "evals" / "scenarios"
        for name, must in (("architect_rules_before_impact.md", "Capability Ledger"),
                           ("unmapped_never_grounds_missing.md", "Component Map")):
            p = sdir / name
            self.assertTrue(p.is_file(), f"scenario missing: {name}")
            s = rb.load_scenario(str(p))   # parses, or the driver exits non-zero
            self.assertTrue(s["expected"], f"{name}: empty 'expected'")
            crit = [ln for ln in s["pass_criteria"].splitlines() if ln.strip().startswith("-")]
            self.assertGreaterEqual(len(crit), 3,
                                    f"{name}: pass criteria gutted to {len(crit)} bullet(s)")
            self.assertIn(must, s["pass_criteria"],
                          f"{name} must assert on {must}, or it tests nothing about the pass")

    def test_skill_proactive_trigger(self):
        t = read("SKILL.md")
        self.assertIn("PROPOSE distilling a guide", t)
        self.assertIn("Propose proactively", t)

    def test_guides_consume_and_proactive(self):
        t = read("guides.md")
        self.assertIn("## 0. Consuming a guide", t)
        self.assertIn("### Proactive trigger", t)

    @requires("subagent_dispatch")
    def test_dispatch_guide_note(self):
        self.assertIn("Guide consumption under dispatch", read("dispatch.md"))

    @requires("comprehension_guides")
    def test_comprehension_guide_wiring(self):
        """Code-comprehension guides (source_kind: code) are wired end to end:
        the autonomous trigger in guides.md, the SKILL.md moment + Write-Triggers
        row, and the template field."""
        guides = read("guides.md")
        self.assertIn("Comprehension trigger", guides)
        self.assertIn("source_kind", guides)
        skill = read("SKILL.md")
        self.assertIn("source_kind: code", skill)
        self.assertIn("Comprehend (code, autonomous)", skill)
        self.assertIn("source_kind", read("templates.md"))

    def test_skill_worktree_hygiene(self):
        t = read("SKILL.md")
        self.assertIn("Isolate the work", t)
        self.assertIn("Branch/worktree hygiene", t)

    def test_support_files_wired(self):
        """Anti-orphan (mechanized 'orphaned discipline never fires', M2):
        every expected support file exists AND is referenced in SKILL.md, and
        any *.md added beside SKILL.md is also referenced (no silent orphan)."""
        skill_md = read("SKILL.md")
        # The entry point's FILENAME differs per distribution (mkt_check.py): derive it,
        # or this shared test asserts one distribution's identity in all three.
        entry = Path(entry_point.load().__file__).name
        expected = list(dist.profile()["support_files"]) + [
            f"scripts/{entry}", "scripts/sdlc_core.py"]
        for rel in expected:
            self.assertTrue((SKILL_DIR / rel).is_file(),
                            f"expected support file missing: {rel}")
            self.assertIn(Path(rel).name, skill_md,
                          f"support file not referenced in SKILL.md (dangling): {rel}")
        for p in SKILL_DIR.glob("*.md"):
            if p.name == "SKILL.md":
                continue
            self.assertIn(p.name, skill_md,
                          f"orphan support file (exists, not referenced): {p.name}")

    @unittest.skipUnless((REPO / "ai_docs" / "INDEX.md").is_file(),
                         "this distribution's repo is not governed by the core document model")
    def test_indexes_idempotent(self):
        """Generated indexes are current: build_* output == on-disk, computed
        WITHOUT writing (never calls cmd_index). A stale index fails here; the
        fix is `sdlc_check.py index` before release -- the intended gate."""
        hist = REPO / "ai_docs" / "strategic" / "features_history.md"
        if hist.is_file():
            self.assertEqual(sc.norm_text(sc.build_index(REPO)),
                             sc.norm_text(sc.read_text(hist)),
                             "features_history.md stale: run sdlc_check.py index")
        if sc.list_canonical_docs(REPO):
            manifest = REPO / "ai_docs" / "INDEX.md"
            self.assertEqual(sc.norm_text(sc.build_manifest(REPO)),
                             sc.norm_text(sc.read_text(manifest)),
                             "INDEX.md stale: run sdlc_check.py index")
        if sc.list_guides(REPO):
            gidx = REPO / "ai_docs" / "reference" / "INDEX.md"
            self.assertEqual(sc.norm_text(sc.build_guide_index(REPO)),
                             sc.norm_text(sc.read_text(gidx)),
                             "reference/INDEX.md stale: run sdlc_check.py index")

    # --- TS9 (static half): the domain router is internally consistent --------
    # The router is doctrine: no code executes it, so nothing but this test stands
    # between a self-contradicting table and an agent following it.

    def _router_rows(self):
        rows = []
        for line in read("routing.md").splitlines():
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) == 5 and not set("".join(cells)) <= set("-: "):
                rows.append(cells)
        return [r for r in rows if r[0] not in ("Request",)]

    def test_router_is_reached_only_from_the_level_test_and_only_with_a_sibling(self):
        skill = read("SKILL.md")
        self.assertIn("routing.md", skill, "the router must be reachable from the contract")
        self.assertRegex(skill, r"L1 never reaches it",
                         "an L1 that pays for routing is the ceremony budget broken")
        routing = read("routing.md")
        self.assertIn("fail open", routing.lower(),
                      "detection that cannot answer must not block the work")

    def test_every_code_branch_row_evaluates_every_step(self):
        for row in self._router_rows():
            request, s1, s2, s3, lens = row
            if s1 != "code":
                continue  # decided at step 1: later steps are correctly never reached
            self.assertTrue(s2 and s2 != "—", f"row '{request}' skips step 2")
            self.assertTrue(s3 and s3 != "—", f"row '{request}' skips step 3")
            self.assertIn(lens.strip("*").lower(), ("code", "knowledge"),
                          f"row '{request}' leaves the code branch to a lens it cannot reach")

    def test_at_least_one_row_turns_on_step_three(self):
        self.assertTrue(
            any("build-consumed" in r[3].lower() for r in self._router_rows()),
            "a step no worked example exercises is a step nobody will run",
        )

    def test_the_reverse_pair_routes_differently(self):
        """The pair that made step 2 necessary: same fidelity, different deliverable."""
        rows = {r[0]: r[4].strip("*").lower() for r in self._router_rows()}
        guide = next((v for k, v in rows.items() if "comprehension guide" in k), None)
        customer = next((v for k, v in rows.items() if "customers' admins" in k), None)
        self.assertEqual(guide, "code")
        self.assertEqual(customer, "knowledge")

    def test_every_domain_has_a_risk_slot(self):
        """The slot is translated per domain, never dropped -- asserted on the data."""
        for name, rules in sc.DOMAINS.items():
            self.assertTrue(rules["risk_section"], f"{name} has no risk section")
            self.assertTrue(rules["risk_label"].startswith("## "), f"{name}'s label is not a heading")

    def test_behavioral_driver_no_llm(self):
        """Mechanized T4: the behavioral driver must never call a model,
        the network, or a subprocess."""
        src = (SKILL_DIR / "evals" / "run_behavioral.py").read_text(encoding="utf-8")
        forbidden = ["subprocess", "os.system", "eval(", "exec(", "urllib",
                     "http", "requests", "openai", "anthropic", "socket"]
        for tok in forbidden:
            self.assertNotIn(tok, src, f"driver must not reference {tok} (T4)")


if __name__ == "__main__":
    unittest.main()
