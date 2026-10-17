#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Course-only battery: course-creator rides the normal publication.

Deliberately outside the shared manifest. 2026-10-17 owner ruling:
`publish_all.bat` publishes each package with `--tag <publishConfig.tag>`,
defaulting to `latest`. A course tag of `beta` left `latest` behind and made
every release need a second, separately 2FA-authorized
`npm dist-tag add ... latest` to honour the 2026-10-08 ruling that a default
install gets the newest course. The prerelease suffix in the version still says
beta; the channel no longer does.

    python scripts/test_publish_channel.py
"""
import json
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parents[3] / "package.json"


class PublishChannel(unittest.TestCase):

    def test_the_course_publishes_to_latest(self):
        if not PKG.is_file():
            self.skipTest("no package.json beside this skill (installed copy)")
        manifest = json.loads(PKG.read_text(encoding="utf-8-sig"))
        tag = manifest.get("publishConfig", {}).get("tag", "latest")
        self.assertEqual(tag, "latest",
                         "publishConfig.tag %r: the normal publish would leave the "
                         "default install on the previous course version" % tag)


if __name__ == "__main__":
    unittest.main(verbosity=2)
