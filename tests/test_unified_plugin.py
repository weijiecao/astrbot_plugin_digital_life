"""Single-plugin configuration and self-contained package checks."""

from __future__ import annotations

import asyncio
import io
import os
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from astrbot_plugin_digital_life import config  # noqa: E402
from tools import build_unified_plugin  # noqa: E402


def _install_astrbot_stubs():
    event = types.ModuleType("astrbot.api.event")

    class Filter:
        class EventMessageType:
            PRIVATE_MESSAGE = "PRIVATE_MESSAGE"

        @staticmethod
        def event_message_type(*args, **kwargs):
            return lambda func: func

        @staticmethod
        def on_llm_request(*args, **kwargs):
            return lambda func: func

    event.filter = Filter
    star = types.ModuleType("astrbot.api.star")

    class Star:
        def __init__(self, context):
            self.context = context

    star.Star = Star
    star.Context = object
    web = types.ModuleType("astrbot.api.web")
    web.json_response = lambda data=None, **kwargs: data
    web.error_response = lambda message, **kwargs: {"error": message}
    web.request = types.SimpleNamespace(query={})
    modules = {
        "astrbot": types.ModuleType("astrbot"),
        "astrbot.api": types.ModuleType("astrbot.api"),
        "astrbot.api.event": event,
        "astrbot.api.star": star,
        "astrbot.api.web": web,
    }
    sys.modules.update(modules)


class ConfigTests(unittest.TestCase):
    def test_modes_and_assist_output(self):
        collect = config.resolve({"mode": "COLLECT",
                                  "allowed_sender_ids": "u1, u2"},
                                 {"ASTRBOT_ROOT": "."})
        assist = config.resolve({"mode": "ASSIST"}, {})
        self.assertEqual(collect.allowed_senders, ("u1", "u2"))
        self.assertEqual(collect.output_mode, "off")
        self.assertTrue(collect.capture_enabled)
        self.assertEqual(assist.output_mode, "inject")
        self.assertTrue(assist.injection_enabled)

    def test_empty_allowed_means_no_capture(self):
        cfg = config.resolve({"mode": "COLLECT", "allowed_sender_ids": ""}, {})
        self.assertEqual(cfg.allowed_senders, ())

    def test_invalid_mode_is_rejected(self):
        with self.assertRaises(ValueError):
            config.resolve({"mode": "everything"}, {})

    def test_plugin_config_wins_over_env(self):
        cfg = config.resolve({"mode": "OFF"},
                             {"DIGITAL_LIFE_MODE": "ASSIST"})
        self.assertEqual(cfg.mode, "OFF")


class PackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build_unified_plugin.build()

    def test_package_is_single_self_contained_plugin(self):
        archive = ROOT / "dist" / self.manifest["archive"]
        with zipfile.ZipFile(archive) as handle:
            names = handle.namelist()
            roots = {name.split("/", 1)[0] for name in names}
            self.assertEqual(roots, {"astrbot_plugin_digital_life"})
            for required in ("astrbot_plugin_digital_life/main.py",
                             "astrbot_plugin_digital_life/config.py",
                             "astrbot_plugin_digital_life/_conf_schema.json",
                             "astrbot_plugin_digital_life/views/console/index.html",
                             "astrbot_plugin_digital_life/memory_engine/engine.py"):
                self.assertIn(required, names)
            metadata = handle.read(
                "astrbot_plugin_digital_life/metadata.yaml")
            self.assertFalse(metadata.startswith(b"\xef\xbb\xbf"))
            self.assertIn(b"name: astrbot_plugin_digital_life", metadata)
            self.assertNotIn(b"astrbot_plugin_memory_shadow", metadata)

    def test_import_and_lifecycle_off_mode(self):
        _install_astrbot_stubs()
        archive = ROOT / "dist" / self.manifest["archive"]
        with tempfile.TemporaryDirectory(prefix="unified-lifecycle-") as temp:
            with zipfile.ZipFile(archive) as handle:
                handle.extractall(temp)
            package = Path(temp) / "astrbot_plugin_digital_life"
            # build() already imported the bundled packages from its temporary
            # extraction; clear those module objects before importing this zip.
            for name in list(sys.modules):
                if name.split(".", 1)[0] in {"memory_engine", "memory_output",
                                             "v1_5_consolidator",
                                             "astrbot_memory_input", "dlm_console",
                                             "main", "console_api", "config"}:
                    sys.modules.pop(name, None)
            sys.path.insert(0, str(package))
            try:
                module = __import__("main")
                routes = []

                class Context:
                    conversation_manager = None

                    def register_web_api(self, route, handler, methods, desc):
                        routes.append(route)

                async def lifecycle():
                    await plugin.initialize()
                    self.assertEqual(plugin.status()["mode"], "OFF")
                    self.assertEqual(plugin.status()["lifecycle"], "RUNNING")
                    self.assertIsNone(plugin.pump)
                    self.assertTrue(any(route.endswith("/console/status")
                                        for route in routes))
                    await plugin.terminate()

                with patch.dict(os.environ, {"ASTRBOT_ROOT": str(Path(temp) / "instance")}):
                    plugin = module.DigitalLifePlugin(
                        Context(), {"mode": "OFF", "allowed_sender_ids": "u1"})
                    asyncio.run(lifecycle())
                self.assertEqual(plugin.status()["lifecycle"], "CLOSED")
            finally:
                sys.path.remove(str(package))


if __name__ == "__main__":
    unittest.main()
