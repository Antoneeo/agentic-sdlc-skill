"""F-070 probe helper: a scratch copy of the publish inputs where only the code
package carries a "What's new", so the stubbed publish run must publish code and
refuse kb. Usage, from the repository root:  python <this file> <empty scratch dir>
"""
import shutil
import subprocess
import sys
from pathlib import Path

dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=False)
shutil.copy("publish_all.bat", dest)
shutil.copytree("scripts", dest / "scripts", ignore=shutil.ignore_patterns("test_*", "node_modules"))
for pkg in [".", "distributions/kb-agentic-skill", "distributions/mkt-agentic-sdlc",
            "distributions/course-creator"]:
    (dest / pkg).mkdir(parents=True, exist_ok=True)
    for name in ("package.json", "CHANGELOG.md", "README.md"):
        shutil.copy(Path(pkg) / name, dest / pkg / name)
log = dest / "CHANGELOG.md"
text = log.read_text(encoding="utf-8")
head = "## [1.49.0] - 2026-10-27"
assert head in text
log.write_text(text.replace(head, head + "\n\n### What's new\n\nProbe notes for users.\n", 1),
               encoding="utf-8")
subprocess.run(["node", str(dest / "scripts" / "whats_new.js"), "--root", str(dest), "--write",
                str(dest)], check=True)
print("ready", dest)
