#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agentic SDLC — the CODE domain entry point.

Thin by design. Every behaviour lives in `sdlc_core.py`, the spine shipped
verbatim in every distribution of the family; this file only says which domain
this distribution implements and which portable checks it can run. Command
names, flags, output and exit codes are unchanged — an existing project sees the
same tool it always had.

Both files must sit in the same directory. If you copy the validator into a CI
image, copy BOTH (`ENFORCEMENT.md` §2 has the recipe); copying this one alone
fails at import, loudly and immediately, which is the intended failure.

Usage is `sdlc_core.py`'s: check / validate / index / stale / mark / gate /
orient / plan.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    import sdlc_core
except ImportError as exc:  # pragma: no cover - exercised by TS12, not by unit tests
    sys.stderr.write(
        "[ERROR] sdlc_check.py cannot find sdlc_core.py next to it: " + str(exc) + "\n"
        "        The validator ships as TWO files since the multi-domain core.\n"
        "        Copy both, or run sdlc_core.py directly.\n")
    sys.exit(1)

# Re-export the core's surface: existing importers (`import sdlc_check as sc`)
# and the test batteries reach for these names on this module.
from sdlc_core import *            # noqa: F401,F403
from sdlc_core import _map_refs    # noqa: F401  underscore helper used by the batteries

# The domain this distribution implements. It does NOT decide any document's
# owning domain -- that is resolved per project (`default_domain:` in
# ai_docs/README.md) and per artifact (`domain:`), so the same tree gets the same
# verdict from every installed distribution. What this constant does decide is
# which portable checks are available to import by name here.
DOMAIN = "code"

sdlc_core.set_entry_point(DOMAIN, provides=("code", "knowledge"))


# --- portable checks shipped by this distribution ---------------------------
# Opt-in per document via `checks:`. They may only ADD findings: a document that
# imports one still owes its own domain everything it owed before, so importing a
# check can never be a way to be validated less.

@sdlc_core.portable_check("code.threat_model")
def _code_threat_model(rel, meta, text):
    """The security section names a real surface, or justifies claiming none."""
    section = sdlc_core.section_body(text, ("## Security and Threat Model", "## Security"))
    if section is None:
        return []  # the owning domain already reports a missing section; no double finding
    surfaces = ("external input", "authn", "authz", "auth", "crypto", "network",
                "personal data", "filesystem", "supply chain")
    low = section.lower()
    if any(s in low for s in surfaces):
        return []
    if "no security impact" in low or "no new security" in low:
        if len(section.split()) < 15:
            return [("warning", "'no security impact' is declared, not justified: "
                                "say which surfaces you checked and why none is touched")]
        return []
    return [("warning", "no security surface named (external input, authN/authZ, crypto, "
                        "network, personal data, filesystem, supply chain) and no justified "
                        "claim that none is touched")]


@sdlc_core.portable_check("knowledge.sources")
def _knowledge_sources(rel, meta, text):
    """A knowledge artifact says what it was written from AND how that was verified."""
    section = sdlc_core.section_body(text, ("## Sources and Verification",))
    if section is None:
        return []
    findings = []
    if not re.search(r"(?m)^\s*[-*|]|\bhttps?://|\.(?:md|pdf|docx?|csv|xlsx?)\b", section):
        findings.append(("warning", "no source is named: a distillation whose origin cannot "
                                    "be reopened is model knowledge, not knowledge work"))
    if not re.search(r"verif|cross-check|checked against|confirmed", section, re.I):
        findings.append(("warning", "sources are listed but not verified: say how each was "
                                    "confirmed, or mark explicitly what could not be"))
    return findings


def main(argv=None):
    return sdlc_core.main(argv)


if __name__ == "__main__":
    sys.exit(main())
