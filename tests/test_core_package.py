"""运行安装包中的核心模块，不依赖另一个工作目录。"""

import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from tools.build_unified_plugin import build, DIST, ROOT


class CorePackageTests(unittest.TestCase):
    def test_inherited_core_against_package(self):
        manifest = build()
        with tempfile.TemporaryDirectory(prefix="digital-life-core-") as temp:
            with zipfile.ZipFile(DIST / manifest["archive"]) as archive:
                archive.extractall(temp)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "verification/run_core_package.py"),
                    str(Path(temp) / "astrbot_plugin_digital_life"),
                ],
                text=True,
                capture_output=True,
                timeout=120,
            )
            print(result.stdout + result.stderr)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
