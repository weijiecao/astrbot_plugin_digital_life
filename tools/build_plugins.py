"""Build installable AstrBot plugin zips for the combined digital-life system.

Produces:
  dist/astrbot_plugin_digital_memory_store-<version>.zip
  dist/astrbot_plugin_memory_shadow-<version>.zip
  dist/SHA256SUMS.txt
  dist/RELEASE.json

The memory-shadow zip is self-contained: it vendors the memory engine, native
input, output, consolidator and console packages inside the plugin directory.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
STORE = ROOT / "astrbot_plugin_digital_memory_store"
SHADOW = ROOT / "astrbot_plugin_memory_shadow"
SHARED = ROOT / "shared"
SHARED_PACKAGES = ("astrbot_memory_input", "memory_engine", "memory_output",
                   "v1_5_consolidator", "dlm_console")
EXCLUDE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo", ".git",
                                 ".github", ".venv", "build", "dist",
                                 "*.egg-info", ".pytest_cache", ".mypy_cache")
EXCLUDE_NAMES = {"测试前功能清单.md", "项目节点进度.md"}


def _version(plugin: Path) -> str:
    for line in (plugin / "metadata.yaml").read_text(encoding="utf-8").splitlines():
        if line.startswith("version:"):
            return line.split(":", 1)[1].strip()
    raise ValueError("metadata.yaml is missing version: " + str(plugin))


def _files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*") if path.is_file())


def _zip(plugin_dir: Path, archive: Path) -> None:
    archive.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as handle:
        for path in _files(plugin_dir):
            if path.name in EXCLUDE_NAMES:
                continue
            rel = path.relative_to(plugin_dir.parent).as_posix()
            info = zipfile.ZipInfo(rel, date_time=(2026, 11, 13, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            handle.writestr(info, path.read_bytes())


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_store() -> dict:
    version = _version(STORE)
    archive = DIST / ("astrbot_plugin_digital_memory_store-%s.zip" % version)
    _zip(STORE, archive)
    return {"name": "astrbot_plugin_digital_memory_store", "version": version,
            "archive": archive.name, "sha256": _sha256(archive),
            "files": len(_files(STORE)), "bytes": archive.stat().st_size}


def build_shadow() -> dict:
    version = _version(SHADOW)
    archive = DIST / ("astrbot_plugin_memory_shadow-%s.zip" % version)
    with tempfile.TemporaryDirectory(prefix="dl-shadow-build-") as temp:
        package = Path(temp) / "astrbot_plugin_memory_shadow"
        shutil.copytree(SHADOW, package, ignore=EXCLUDE)
        for name in SHARED_PACKAGES:
            source = SHARED / name
            if not source.is_dir():
                raise FileNotFoundError("missing shared package: " + name)
            shutil.copytree(source, package / name, ignore=EXCLUDE)
        _zip(package, archive)
    return {"name": "astrbot_plugin_memory_shadow", "version": version,
            "archive": archive.name, "sha256": _sha256(archive),
            "files": len(zipfile.ZipFile(archive).namelist()),
            "bytes": archive.stat().st_size}


def verify_shadow(archive: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="dl-shadow-check-") as temp:
        with zipfile.ZipFile(archive) as handle:
            handle.extractall(temp)
        package = Path(temp) / "astrbot_plugin_memory_shadow"
        sys.path.insert(0, str(package))
        try:
            import astrbot_memory_input  # noqa: F401
            import dlm_console  # noqa: F401
            import memory_engine  # noqa: F401
            import memory_output  # noqa: F401
            import v1_5_consolidator  # noqa: F401
        finally:
            sys.path.pop(0)
        for rel in ("views/console/index.html", "views/console/app.js",
                    "console_api.py", "metadata.yaml"):
            if not (package / rel).is_file():
                raise AssertionError("missing shadow asset: " + rel)


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir(parents=True)
    store = build_store()
    shadow = build_shadow()
    verify_shadow(DIST / shadow["archive"])
    checksums = DIST / "SHA256SUMS.txt"
    checksums.write_text(
        "%s  %s\n%s  %s\n" % (store["sha256"], store["archive"],
                              shadow["sha256"], shadow["archive"]),
        encoding="utf-8")
    manifest = {"tag": "v" + shadow["version"], "plugins": [store, shadow],
                "checksums": checksums.name}
    (DIST / "RELEASE.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
