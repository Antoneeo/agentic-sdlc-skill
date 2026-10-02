"""F-059: executable before/after probe for the shared course-domain contract."""

import argparse
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CORE = ROOT / "skills" / "agentic-sdlc-skill" / "scripts"
sys.path.insert(0, str(CORE))
import sdlc_core as core  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--expect", choices=("before", "after"), required=True)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as temp:
        readme = Path(temp) / "ai_docs" / "README.md"
        readme.parent.mkdir(parents=True)
        readme.write_text("---\ndefault_domain: course\n---\n", encoding="utf-8")
        default = core.project_default_domain(Path(temp))
        resolved = core.resolve_domain({"domain": "course"}, "code")

    observed = (default, resolved)
    expected = (("code", ("code", "course")) if args.expect == "before"
                else ("course", ("course", None)))
    assert observed == expected, f"expected {expected!r}; observed {observed!r}"
    print(f"PASS {args.expect}: {observed!r}")


if __name__ == "__main__":
    main()
