#!/usr/bin/env python3
"""Structural checks for one course; never certifies teaching quality or learning."""
from dataclasses import dataclass
from pathlib import Path
import re


REQUIRED = ("D-UC.md", "D-IC.md", "P-TM.md", "CONCEPT_GRAPH.md",
            "COURSE_PLAN.md", "SIMULATION_REPORT.md")
SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
ID = re.compile(r"\b(?:UC\d+|IC\d+|C-\d+)\b")


@dataclass(frozen=True)
class Finding:
    file: str
    item: str
    severity: str
    reason: str


def _frontmatter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    return dict((key.strip().lower(), value.strip())
                for key, value in re.findall(r"^([\w-]+):\s*(.*)$", text[4:end], re.M))


def _table(text, required):
    lines = text.splitlines()
    for i, line in enumerate(lines[:-1]):
        if not line.startswith("|") or not re.fullmatch(r"[\s|:-]+", lines[i + 1]):
            continue
        headers = [h.strip().lower() for h in line.strip("|").split("|")]
        if not set(required).issubset(headers):
            continue
        rows = []
        for row in lines[i + 2:]:
            if not row.startswith("|"):
                break
            cells = [cell.strip() for cell in row.strip("|").split("|")]
            if len(cells) != len(headers):
                return None
            rows.append(dict(zip(headers, cells)))
        return rows
    return None


def _items(cell):
    return [part.strip() for part in re.split(r"[,;]", cell or "")
            if part.strip() and part.strip() != "-"]


def _anchor_exists(path, anchor):
    if path.suffix.lower() not in (".md", ".txt"):
        if path.suffix.lower() == ".pdf":
            return bool(re.fullmatch(r"page=[1-9]\d*", anchor))
        if path.suffix.lower() in (".pptx", ".ppt"):
            return bool(re.fullmatch(r"slide=[1-9]\d*", anchor))
        return bool(re.fullmatch(r"\d{2}:\d{2}(?::\d{2})?", anchor))
    text = path.read_text(encoding="utf-8", errors="replace")
    return any(re.sub(r"[^a-z0-9 -]", "", heading.lower()).strip().replace(" ", "-") == anchor.lower()
               for heading in re.findall(r"^#+\s+(.+)$", text, re.M))


def _content_contract(course_dir, plan, plan_rows, read, ref, add):
    """Validate authored-source structure, not its pedagogical sufficiency."""
    plan_path = course_dir / "COURSE_PLAN.md"

    def field(text, key, path, item):
        values = re.findall(r"^" + re.escape(key) + r":[ \t]*(.*)$", text, re.M)
        if len(values) != 1 or not values[0].strip() or values[0].strip() == "-":
            add(path, item, f"{key} must occur once with a value")
            return ""
        return values[0].strip()

    declarations = re.findall(r"^Content contract:[ \t]*(.*)$", plan, re.M)
    if not declarations:
        add(plan_path, "content", "legacy course: migrate to a complete textual content contract; quality is not certified", "WARN")
        return
    contract = field(plan, "Content contract", plan_path, "content")
    if contract not in ("slide-content-v1", "text-content-v1"):
        add(plan_path, "content", "unknown content contract")
        return
    prefix, name = ("S", "SLIDE_CONTENT.md") if contract == "slide-content-v1" else ("U", "COURSE_CONTENT.md")
    if prefix == "U":
        field(plan, "Format exception", plan_path, "content")
    path = course_dir / name
    text = read(path, "content")
    if text is None:
        return
    intro = text.split("\n## ", 1)[0]
    if field(intro, "Course version", path, "version") != field(plan, "Course version", plan_path, "version"):
        add(path, "version", "content version differs from COURSE_PLAN")
    if field(intro, "Delivery mode", path, "delivery") not in ("self-study", "instructor-led"):
        add(path, "delivery", "unknown delivery mode")
    for key in ("Efficacy", "Feedback flow"):
        if field(intro, key, path, key) != field(plan, key, plan_path, key):
            add(path, key, f"{key} differs from COURSE_PLAN")
    headers = ("profile", "baseline", "target capability", "teaching contribution", "observable check", "alternative and limits")
    values = _table(text, headers) or []
    expected_profiles = {row["profile"] for row in plan_rows}
    if {row["profile"] for row in values} != expected_profiles or len(values) != len(expected_profiles):
        add(path, "value", "Course Value must cover each taught profile exactly once")
    for row in values:
        if any(not row[h] or row[h] == "-" for h in headers):
            add(path, "value", "Course Value fields must be populated; semantic review still required")
        ref(row["observable check"], path, "value")
    modules = {row["module id"]: row for row in plan_rows}
    sections = re.split(r"(?m)^## (.+)\n", text)
    units = {}
    order = []
    for heading, body in zip(sections[1::2], sections[2::2]):
        if heading == "Course Value":
            continue
        if not re.fullmatch(prefix + r"[0-9]+", heading):
            add(path, heading, "unexpected unit heading")
            continue
        if heading in units:
            add(path, heading, "duplicate unit ID")
        metadata = body.split("### ", 1)[0]
        unit = {key: field(metadata, key, path, heading) for key in
                ("Module", "Objective", "Role", "Title", "Value contribution")}
        units[heading] = unit
        order.append(heading)
        unit["coverage"] = {(unit["Module"], unit["Objective"])}
        extra_coverage = re.findall(r"^Covers:[ \t]*(.*)$", metadata, re.M)
        if len(extra_coverage) > 1:
            add(path, heading, "Covers must occur at most once")
        if extra_coverage:
            pairs = _items(extra_coverage[0])
            if not pairs:
                add(path, heading, "Covers must list module/objective pairs")
            for pair in pairs:
                if not re.fullmatch(r"M\d+/O\d+", pair):
                    add(path, heading, "invalid coverage pair; expected M1/O1")
                    continue
                mid, objective = pair.split("/")
                if (mid, objective) in unit["coverage"]:
                    add(path, heading, "duplicate coverage pair")
                unit["coverage"].add((mid, objective))
        for mid, objective in unit["coverage"]:
            if mid not in modules or modules[mid]["objective id"] != objective:
                add(path, heading, "coverage module/objective differs from COURSE_PLAN")
        module = modules.get(unit["Module"])
        if not module or module["objective id"] != unit["Objective"]:
            add(path, heading, "unit module/objective differs from COURSE_PLAN")
        if unit["Role"] not in ("orientation", "explanation", "check", "solution", "closing"):
            add(path, heading, "unknown unit role")
        if unit["Role"] == "check":
            unit["Solution"] = field(metadata, "Solution", path, heading)
        parts = re.split(r"(?m)^### (.+)\n", body)
        content = list(zip(parts[1::2], parts[2::2]))
        for key in ("Learner content", "Complete explanation", "Visual content", "Transition", "Sources"):
            blocks = [b.strip() for k, b in content if k == key]
            if len(blocks) != 1 or not blocks[0] or blocks[0] == "-":
                add(path, heading, f"{key} section must occur once with content")
        for key, block in content:
            if key == "Sources":
                for source in block.strip().splitlines():
                    ref(source.removeprefix("- ").strip(), path, heading, allow_url=True)
    source_path = path.relative_to(course_dir.parents[3]).as_posix()
    for mid, row in modules.items():
        for key, roles in (("explanation", {"orientation", "explanation"}), ("check", {"check"})):
            references = _items(row[key])
            if not references:
                continue  # existing module checker reports missing fields
            for value in references:
                target, _, anchor = value.partition("#")
                uid = anchor.upper()
                unit = units.get(uid, {})
                if (target != source_path or (mid, row["objective id"]) not in unit.get("coverage", set())
                        or unit.get("Role") not in roles):
                    add(plan_path, mid, f"{key} must locate its module's canonical content unit")
    for uid, unit in units.items():
        if unit["Role"] == "check":
            solution_id = unit.get("Solution", "")
            solution = units.get(solution_id, {})
            if (solution.get("Role") != "solution"
                    or not unit["coverage"].issubset(solution.get("coverage", set()))
                    or order.index(solution_id) <= order.index(uid)):
                add(path, uid, "check needs a subsequent solution covering every module/objective")
    for row in values:
        target, _, anchor = row["observable check"].partition("#")
        unit = units.get(anchor.upper(), {})
        covered_profiles = {modules[mid]["profile"] for mid, obj in unit.get("coverage", set()) if mid in modules}
        if target != source_path or unit.get("Role") != "check" or row["profile"] not in covered_profiles:
            add(path, "value", "observable check must locate a canonical check for its profile")


def validate_course(root, course_dir):
    root = Path(root).resolve()
    docs = root / "ai_docs"
    course_dir = Path(course_dir)
    findings = []

    def add(path, item, reason, severity="ERROR"):
        try:
            name = Path(path).relative_to(root).as_posix()
        except ValueError:
            name = str(path)
        findings.append(Finding(name, item, severity, reason))

    expected_parent = docs / "solutions/courses"
    if (not SLUG.fullmatch(course_dir.name) or course_dir.parent.resolve() != expected_parent.resolve()
            or not course_dir.is_dir() or not course_dir.resolve().is_relative_to(root)):
        add(course_dir, "course", "unsafe or missing course directory/slug")
        return findings
    slug = course_dir.name

    def read(path, item):
        path = Path(path)
        try:
            if not path.resolve().is_relative_to(root):
                add(path, item, "unsafe path resolves outside project root")
                return None
            if not path.is_file():
                add(path, item, f"{item} missing file")
                return None
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            add(path, item, f"cannot read file: {exc}")
            return None

    def ref(value, artifact, item, allow_url=False):
        value = value.strip()
        if allow_url and re.fullmatch(r"https?://[^\s]+", value):
            return
        path_part, sep, anchor = value.partition("#")
        path = Path(path_part)
        if (not sep or not anchor or path.is_absolute() or ".." in path.parts
                or not path_part.startswith("ai_docs/")):
            add(artifact, item, f"unsafe or unlocated reference '{value}'")
            return
        target = root / path
        if not target.resolve().is_relative_to(root):
            add(artifact, item, f"unsafe reference '{value}' resolves outside project root")
        elif not target.is_file():
            add(artifact, item, f"reference '{value}' points to missing file")
        elif not _anchor_exists(target, anchor):
            add(artifact, item, f"reference '{value}' has no matching locator")

    vision_path = docs / f"vision/features/VISION_course_{slug}.md"
    vision = read(vision_path, "Vision")
    if vision is not None:
        meta = _frontmatter(vision)
        if meta.get("domain") != "course":
            add(vision_path, "Vision", "Vision needs explicit domain: course")
        if meta.get("status") != "APPROVED" or not re.search(
                r"(?im)^Status:\s*APPROVED\b", vision):
            add(vision_path, "Vision", "Vision must be APPROVED before course design")
    analysis_path = docs / f"solutions/ANALYSIS_course_{slug}.md"
    analysis = read(analysis_path, "ANALYSIS")
    known = {"UC": set(), "IC": set(), "C": set()}
    if analysis is not None:
        meta = _frontmatter(analysis)
        if meta.get("domain") != "course":
            add(analysis_path, "ANALYSIS", "ANALYSIS needs explicit domain: course")
        if not re.search(r"(?im)^## Learning and Content Risks\s*$", analysis):
            add(analysis_path, "ANALYSIS", "Learning and Content Risks section missing")
        for name, prefix in (("Use Cases / User Needs", "UC"),
                             ("Interface Contract", "IC"),
                             ("Learning and Content Risks", "C")):
            match = re.search(r"(?ims)^## " + re.escape(name) + r"\s*\n(.*?)(?=^## |\Z)", analysis)
            if match:
                known[prefix] = {token for token in ID.findall(match.group(1))
                                 if token.startswith(prefix + ("-" if prefix == "C" else ""))}
            if not known[prefix]:
                add(analysis_path, prefix, f"ANALYSIS has no defined {prefix} IDs")

    material = {}
    profiles = set()
    for name in REQUIRED:
        material[name] = read(course_dir / name, name)
    for name, required, column, prefix in (
            ("D-UC.md", ("uc id", "profile", "starting knowledge", "evidence", "need"), "uc id", "UC"),
            ("D-IC.md", ("flow id", "surface", "conditions", "feedback channel"), "flow id", "IC"),
            ("P-TM.md", ("risk id", "vector", "mitigation", "residual"), "risk id", "C")):
        body = material[name]
        if body is None:
            continue
        rows = _table(body, required)
        if not rows:
            add(course_dir / name, name, f"missing or empty table with {column}")
            continue
        seen = set()
        for row in rows:
            rid = row[column]
            if name == "D-UC.md":
                if row["profile"] and row["profile"] != "-":
                    profiles.add(row["profile"])
                else:
                    add(course_dir / name, rid, "profile missing")
            key = (rid, row["profile"]) if name == "D-UC.md" else rid
            if key in seen:
                add(course_dir / name, rid, "duplicate ID")
            seen.add(key)
            if rid not in known[prefix]:
                add(course_dir / name, rid, f"{rid} is not defined in ANALYSIS")
            for field in row:
                if not row[field]:
                    add(course_dir / name, rid, f"{field} missing")
            if name == "D-IC.md" and not row.get("feedback channel", ""):
                add(course_dir / name, rid, "feedback channel or explicit unavailability missing")
        for rid in known[prefix] - {row[column] for row in rows}:
            add(course_dir / name, rid, f"{rid} is not detailed here")

    graph_rows = _table(material["CONCEPT_GRAPH.md"] or "",
                        ("concept id", "prerequisites", "profile", "initial state",
                         "evidence", "source", "objectives"))
    plan_rows = _table(material["COURSE_PLAN.md"] or "",
                       ("module id", "profile", "objective id", "concepts",
                        "explanation", "sources", "check", "next"))
    if not graph_rows:
        add(course_dir / "CONCEPT_GRAPH.md", "graph", "concept table missing or empty")
        graph_rows = []
    if not plan_rows:
        add(course_dir / "COURSE_PLAN.md", "plan", "module table missing or empty")
        plan_rows = []
    graph = {}
    prerequisites = {}
    objectives = set()
    for row in graph_rows:
        cid = row["concept id"]
        key = (cid, row["profile"])
        if not re.fullmatch(r"CO\d+", cid) or key in graph:
            add(course_dir / "CONCEPT_GRAPH.md", cid, "invalid or duplicate concept ID/profile")
        deps = set(_items(row["prerequisites"]))
        if cid in prerequisites and prerequisites[cid] != deps:
            add(course_dir / "CONCEPT_GRAPH.md", cid,
                "prerequisites differ between profiles for the same concept")
        prerequisites.setdefault(cid, deps)
        graph.setdefault(key, row)
        if row["initial state"] not in ("PROVATO", "INCERTO", "DA_INSEGNARE"):
            add(course_dir / "CONCEPT_GRAPH.md", cid, "invalid initial state")
        if row["initial state"] == "PROVATO":
            evidence = row["evidence"]
            if not evidence.startswith("ai_docs/solutions/courses/" + slug + "/D-UC.md#"):
                add(course_dir / "CONCEPT_GRAPH.md", cid,
                    "PROVATO needs precise evidence in D-UC.md")
            else:
                ref(evidence, course_dir / "CONCEPT_GRAPH.md", cid)
        if not _items(row["source"]):
            add(course_dir / "CONCEPT_GRAPH.md", cid, "source missing")
        for source in _items(row["source"]):
            ref(source, course_dir / "CONCEPT_GRAPH.md", cid, allow_url=True)
        if not row["objectives"]:
            add(course_dir / "CONCEPT_GRAPH.md", cid, "no objective")
        objectives.update(_items(row["objectives"]))
        if not row["profile"]:
            add(course_dir / "CONCEPT_GRAPH.md", cid, "profile missing")
        elif row["profile"] not in profiles:
            add(course_dir / "CONCEPT_GRAPH.md", cid,
                f"profile {row['profile']} not defined in D-UC")
    for (cid, profile), row in graph.items():
        for prereq in _items(row["prerequisites"]):
            if (prereq, profile) not in graph:
                add(course_dir / "CONCEPT_GRAPH.md", cid,
                    f"prerequisite {prereq} does not exist for profile {profile}")
    visiting, done = set(), set()

    def visit(key):
        if key in visiting:
            add(course_dir / "CONCEPT_GRAPH.md", key[0], "prerequisite cycle")
            return
        if key in done or key not in graph:
            return
        visiting.add(key)
        for dep in _items(graph[key]["prerequisites"]):
            visit((dep, key[1]))
        visiting.remove(key)
        done.add(key)

    for cid in graph:
        visit(cid)
    first_taught = {}
    module_ids = [row["module id"] for row in plan_rows]
    if len(module_ids) != len(set(module_ids)) or any(
            not re.fullmatch(r"M\d+", mid) for mid in module_ids):
        add(course_dir / "COURSE_PLAN.md", "modules", "invalid or duplicate module ID")
    for position, row in enumerate(plan_rows):
        mid = row["module id"]
        if row["profile"] not in profiles:
            add(course_dir / "COURSE_PLAN.md", mid,
                f"profile {row['profile']} not defined in D-UC")
        if not _items(row["concepts"]):
            add(course_dir / "COURSE_PLAN.md", mid, "concepts missing")
        if row["objective id"] not in objectives:
            add(course_dir / "COURSE_PLAN.md", mid, "objective not defined in concept graph")
        for within, cid in enumerate(_items(row["concepts"])):
            key = (cid, row["profile"])
            if cid not in prerequisites:
                add(course_dir / "COURSE_PLAN.md", mid, f"concept {cid} missing from graph")
            elif key not in graph:
                add(course_dir / "COURSE_PLAN.md", mid,
                    f"profile differs from concept {cid}: no state for {row['profile']}")
            else:
                first_taught.setdefault(key, (position, within))
                if row["objective id"] not in _items(graph[key]["objectives"]):
                    add(course_dir / "COURSE_PLAN.md", mid,
                        f"objective not linked to concept {cid}")
        for field in ("explanation", "sources", "check"):
            values = _items(row[field])
            if not values:
                add(course_dir / "COURSE_PLAN.md", mid, f"{field} missing")
            for value in values:
                ref(value, course_dir / "COURSE_PLAN.md", mid, allow_url=field == "sources")
        for field in ("profile", "objective id", "next"):
            if not row[field]:
                add(course_dir / "COURSE_PLAN.md", mid, f"{field} missing")
        if row["next"].lower() not in ("end", "fine") and row["next"] not in module_ids:
            add(course_dir / "COURSE_PLAN.md", mid, "next module does not exist")
        expected_next = module_ids[position + 1] if position + 1 < len(module_ids) else "end"
        if row["next"].lower() != expected_next.lower():
            add(course_dir / "COURSE_PLAN.md", mid,
                f"next module must follow the declared order ({expected_next})")
    for key, row in graph.items():
        cid, profile = key
        used_at = first_taught.get(key)
        if used_at is None:
            if row["initial state"] != "PROVATO":
                add(course_dir / "COURSE_PLAN.md", cid,
                    f"concept has no teaching module for profile {profile}")
            continue
        for dep in _items(row["prerequisites"]):
            dep_key = (dep, profile)
            if dep_key in graph and graph[dep_key]["initial state"] != "PROVATO":
                if first_taught.get(dep_key, (len(plan_rows), 0)) >= used_at:
                    add(course_dir / "COURSE_PLAN.md", cid,
                        f"prerequisite {dep} is taught after its dependent concept for profile {profile}")
    plan = material["COURSE_PLAN.md"] or ""
    feedback = re.search(r"(?im)^Feedback flow:\s*(IC\d+)\s*$", plan)
    if not feedback or feedback.group(1) not in known["IC"]:
        add(course_dir / "COURSE_PLAN.md", "feedback", "feedback flow not defined in D-IC/ANALYSIS")
    if not re.search(r"(?im)^Course version:\s*\S+", plan):
        add(course_dir / "COURSE_PLAN.md", "version", "course version missing")
    efficacy = re.search(r"(?im)^Efficacy:\s*(.+)$", plan)
    if not efficacy:
        add(course_dir / "COURSE_PLAN.md", "efficacy", "efficacy status missing")
    elif efficacy.group(1).strip().lower() not in ("efficacy not verified", "efficacia non verificata"):
        feedback_file = course_dir / "FEEDBACK_REPORT.md"
        if not feedback_file.is_file():
            add(course_dir / "COURSE_PLAN.md", "efficacy",
                "verified efficacy needs real feedback; simulation alone cannot prove it")
        else:
            add(course_dir / "COURSE_PLAN.md", "efficacy",
                "human review of efficacy evidence required", severity="WARN")
    _content_contract(course_dir, plan, plan_rows, read, ref, add)
    return findings


def validate_all(root):
    root = Path(root).resolve()
    docs = root / "ai_docs"
    parent = docs / "solutions/courses"
    if not parent.resolve().is_relative_to(root):
        return [Finding("ai_docs/solutions/courses", "course", "ERROR",
                        "unsafe course directory resolves outside project root")]
    slugs = {p.name for p in parent.iterdir() if p.is_dir()} if parent.is_dir() else set()
    findings = []
    for pattern, prefix in (("solutions/ANALYSIS_course_*.md", "ANALYSIS_course_"),
                            ("vision/features/VISION_course_*.md", "VISION_course_")):
        for path in docs.glob(pattern):
            if not path.resolve().is_relative_to(root):
                findings.append(Finding(path.relative_to(root).as_posix(), prefix,
                                        "ERROR", "unsafe course metadata resolves outside project root"))
                continue
            try:
                meta = _frontmatter(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError):
                continue
            if meta.get("domain") == "course":
                slugs.add(path.stem.removeprefix(prefix))
    for slug in sorted(slugs):
        findings.extend(validate_course(root, parent / slug))
    return findings
