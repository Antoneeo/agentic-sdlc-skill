"""Copy only manifest-declared shared files from the canonical skill."""
from pathlib import Path
import importlib.util
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CANON = ROOT / 'skills/agentic-sdlc-skill'
spec = importlib.util.spec_from_file_location('manifest', CANON / 'scripts/shared_files.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
for name in module.DISTRIBUTION_SKILL_DIRS:
    directory = ROOT / name
    if directory != CANON:
        for rel in module.SHARED_FILES:
            source, target = CANON / rel, directory / rel
            if not target.exists() or target.read_bytes() != source.read_bytes():
                shutil.copyfile(source, target)
    subprocess.run([sys.executable, str(directory / 'scripts/shared_files.py'), '--update'], check=True)
