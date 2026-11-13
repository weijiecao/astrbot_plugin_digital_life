"""Data-directory ownership for the unified plugin.

The lock prevents two unified instances from sharing one database. It cannot
detect the legacy plugin unless the legacy module is loaded in this process;
that is checked separately and blocks capture/injection instead of writing.
"""

from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path


class OwnershipError(RuntimeError):
    pass


def legacy_plugin_active(context=None) -> bool:
    """Best-effort detection of the old astrbot_plugin_memory_shadow Star."""
    for name in list(sys.modules):
        if name == "astrbot_plugin_memory_shadow" or name.startswith(
                "astrbot_plugin_memory_shadow."):
            return True
    if context is None:
        return False
    for attr in ("plugin_manager", "_plugin_manager", "star_manager",
                 "_star_manager"):
        manager = getattr(context, attr, None)
        if manager is None:
            continue
        for key in ("plugins", "_plugins", "loaded_plugins", "stars"):
            loaded = getattr(manager, key, None)
            if isinstance(loaded, dict):
                if any("astrbot_plugin_memory_shadow" in str(name)
                       for name in loaded):
                    return True
            elif isinstance(loaded, (list, tuple, set)):
                if any("astrbot_plugin_memory_shadow" in str(name)
                       for name in loaded):
                    return True
        getter = getattr(manager, "get_loaded_plugins", None)
        if callable(getter):
            try:
                loaded = getter()
            except Exception:
                loaded = None
            if any("astrbot_plugin_memory_shadow" in str(name)
                   for name in (loaded or [])):
                return True
    return False


class DataDirectoryLock:
    """A cross-process exclusive lock plus an in-process guard."""

    _guard = threading.Lock()
    _held: set[str] = set()

    def __init__(self, base: Path, owner: str = "astrbot_plugin_digital_life"):
        self.base = Path(base)
        self.owner = owner
        self.path = self.base / ".digital_life.owner"
        self.key = str(self.path.resolve())
        self.handle = None
        self.acquired = False

    def acquire(self) -> None:
        with self._guard:
            if self.key in self._held:
                raise OwnershipError("data directory already owned in this process")
            self._held.add(self.key)
        try:
            self.base.mkdir(parents=True, exist_ok=True)
            handle = open(self.path, "a+b")
            self.handle = handle
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            self._lock(handle)
            handle.seek(0)
            handle.truncate()
            payload = json.dumps({"owner": self.owner, "pid": os.getpid(),
                                  "acquired_at": time.time()},
                                 ensure_ascii=False).encode("utf-8")
            handle.write(payload)
            handle.flush()
            self.acquired = True
        except Exception as exc:
            self._release_handle()
            with self._guard:
                self._held.discard(self.key)
            if isinstance(exc, OwnershipError):
                raise
            raise OwnershipError("cannot lock %s: %s" % (self.path, exc)) from exc

    @staticmethod
    def _lock(handle) -> None:
        if os.name == "nt":
            import msvcrt
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise OwnershipError("data directory is locked by another process") from exc
        else:
            import fcntl
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise OwnershipError("data directory is locked by another process") from exc

    @staticmethod
    def _unlock(handle) -> None:
        try:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass

    def _release_handle(self) -> None:
        handle, self.handle = self.handle, None
        self.acquired = False
        if handle is None:
            return
        try:
            self._unlock(handle)
        finally:
            try:
                handle.close()
            except Exception:
                pass

    def release(self) -> None:
        self._release_handle()
        with self._guard:
            self._held.discard(self.key)
