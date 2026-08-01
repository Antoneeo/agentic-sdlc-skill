"""Import the distribution's entry point, whatever it is called.

Three distributions share these batteries. `sdlc_check.py` is the code and
knowledge entry point, `mkt_check.py` the marketing one; hard-coding either name
here is how a shared test starts asserting one distribution's identity in all of
them. The core is the same file in every distribution, so what varies is only
which overlay registered its profile.
"""
import importlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

_HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY_POINTS = ("sdlc_check", "mkt_check")


def load():
    for name in ENTRY_POINTS:
        if os.path.isfile(os.path.join(_HERE, name + ".py")):
            return importlib.import_module(name)
    raise ImportError(
        "no distribution entry point found next to the batteries "
        f"(looked for: {', '.join(n + '.py' for n in ENTRY_POINTS)})")
