"""继承核心回归：强制从实际安装包加载所有运行模块。"""

import sys
import unittest
from pathlib import Path

package = Path(sys.argv[1]).resolve()
root = Path(__file__).resolve().parent / "core"
sys.path[:0] = [str(package), str(root)]
suite = unittest.defaultTestLoader.discover(
    str(root / "tests"), top_level_dir=str(root)
)
result = unittest.TextTestRunner(verbosity=2).run(suite)
for prefix in (
    "memory_engine",
    "memory_output",
    "astrbot_memory_input",
    "v1_5_consolidator",
):
    for name, module in list(sys.modules.items()):
        if name == prefix or name.startswith(prefix + "."):
            filename = getattr(module, "__file__", None)
            if filename:
                assert Path(filename).resolve().is_relative_to(package), (
                    name,
                    filename,
                )
print("Verified: runtime modules came from the extracted installation package.")
sys.exit(not result.wasSuccessful())
