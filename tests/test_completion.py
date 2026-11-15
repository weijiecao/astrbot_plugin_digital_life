"""Use a fresh process to verify the self-contained plugin, not source imports."""

import os
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.build_unified_plugin import build, DIST


class CompletionPackageTests(unittest.TestCase):
    def test_packaged_completion_suite(self):
        manifest = build()
        with tempfile.TemporaryDirectory(prefix="digital-life-completion-") as temp:
            with zipfile.ZipFile(DIST / manifest["archive"]) as archive:
                archive.extractall(temp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(Path(__file__).with_name("completion_suite.py")),
                    str(Path(temp) / "astrbot_plugin_digital_life"),
                ],
                text=True,
                capture_output=True,
                timeout=120,
            )
            print(result.stdout + result.stderr)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
