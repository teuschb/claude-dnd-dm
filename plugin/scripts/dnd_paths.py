#!/usr/bin/env python3
"""Single resolver for where a project keeps its D&D data.

Used by bin/dm20 (the MCP wrapper) and by every hook script, so they always
agree on the data dir.

Project root: CLAUDE_PROJECT_DIR if set, else the hook payload's "cwd" (hooks
only), else the process cwd.

A project is a D&D project only if it opted in (see is_dnd_project). Otherwise the
plugin creates nothing in it.

Data dir: `.claude/dnd-dm.json` in the project, {"data_dir": "rpg/dnd"}
(relative to the project root, or absolute). Default: <project>/dnd.

Run directly (`python3 dnd_paths.py [--json]`) to print the resolved paths.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

CONFIG_REL = Path(".claude") / "dnd-dm.json"
DEFAULT_DATA_DIR = "dnd"
PLUGIN_ROOT = Path(__file__).resolve().parents[1]


def project_root(payload_cwd: str | None = None) -> Path:
    for candidate in (os.environ.get("CLAUDE_PROJECT_DIR"), payload_cwd, os.getcwd()):
        if candidate:
            return Path(candidate).expanduser().resolve()
    return Path.cwd()


def config_path(root: Path) -> Path:
    return root / CONFIG_REL


def data_dir(root: Path | None = None) -> Path:
    root = root or project_root()
    setting = DEFAULT_DATA_DIR
    cfg = config_path(root)
    try:
        value = json.loads(cfg.read_text(encoding="utf-8")).get("data_dir")
        if isinstance(value, str) and value.strip():
            setting = value.strip()
    except (OSError, ValueError, AttributeError):
        pass
    path = Path(setting).expanduser()
    return path if path.is_absolute() else root / path


def is_dnd_project(root: Path | None = None) -> bool:
    """Opt-in test: `.claude/dnd-dm.json` exists, or `<data dir>/campaigns` already exists.

    A bare unrelated `dnd/` folder does not count.
    """
    root = root or project_root()
    return config_path(root).is_file() or (data_dir(root) / "campaigns").is_dir()


def idle_dir() -> Path:
    """Storage for dm20 in projects that haven't opted in (nothing is created in the project)."""
    base = os.environ.get("CLAUDE_PLUGIN_DATA")
    if base:
        return Path(base) / "idle"
    import tempfile
    return Path(tempfile.gettempdir()) / "dnd-dm-idle"


def plugin_version() -> str:
    try:
        return json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8")).get("version", "0")
    except (OSError, ValueError):
        return "0"


if __name__ == "__main__":
    root = project_root()
    info = {"project_root": str(root), "data_dir": str(data_dir(root)), "plugin_root": str(PLUGIN_ROOT),
            "is_dnd_project": is_dnd_project(root)}
    if "--json" in sys.argv:
        print(json.dumps(info))
    else:
        print(info["data_dir"])
