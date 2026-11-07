#!/usr/bin/env python3
"""Data-dir setup for the dnd-dm plugin: opt a project in, seed the SRD cache.

Used by bin/dm20 (seeding on start) and by the new-campaign skill:

    python3 dnd_setup.py optin [--data-dir rpg/dnd] [--project DIR]

`optin` writes `.claude/dnd-dm.json` (only when --data-dir differs from the
default, or the file is missing), creates the data dir, writes its default
.gitignore if none exists, and seeds the SRD cache. It prints the resolved data
dir. dm20 keeps its storage path from the moment it starts, so after `optin`
the dm20 MCP server must be reconnected (/mcp -> Reconnect) before any campaign
is created.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dnd_paths  # noqa: E402

MARKER = ".dnd-dm-seed-hash"   # in <data dir>/rulebook_cache/, outside srd_2024/


def cache_hash(src: Path) -> str:
    h = hashlib.sha256()
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        h.update(str(f.relative_to(src)).encode() + b"\0")
        h.update(f.read_bytes() + b"\0")
    return h.hexdigest()


def seed_cache(data: Path) -> int:
    """Copy the plugin's SRD cache into the data dir. Returns the number of files written.

    Skipped when the content-hash marker matches. Otherwise byte-compares and writes
    only files that are missing or differ. Never deletes anything.
    """
    src = dnd_paths.PLUGIN_ROOT / "rulebook_cache" / "srd_2024"
    if not src.is_dir():
        return 0
    cache = data / "rulebook_cache"
    dst = cache / "srd_2024"
    marker = cache / MARKER
    digest = cache_hash(src)
    if dst.is_dir() and marker.is_file() and marker.read_text(encoding="utf-8").strip() == digest:
        return 0
    written = 0
    for f in sorted(p for p in src.rglob("*") if p.is_file()):
        target = dst / f.relative_to(src)
        if target.is_file() and target.read_bytes() == f.read_bytes():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(f, target)
        written += 1
    cache.mkdir(parents=True, exist_ok=True)
    marker.write_text(digest + "\n", encoding="utf-8")
    return written


def ensure_gitignore(data: Path) -> None:
    target = data / ".gitignore"
    template = dnd_paths.PLUGIN_ROOT / "templates" / "data-dir.gitignore"
    if not target.exists() and template.is_file():
        shutil.copyfile(template, target)


def optin(root: Path, data_dir_setting: str | None) -> Path:
    cfg = dnd_paths.config_path(root)
    if data_dir_setting and data_dir_setting != dnd_paths.DEFAULT_DATA_DIR or not cfg.exists():
        cfg.parent.mkdir(parents=True, exist_ok=True)
        cfg.write_text(json.dumps({"data_dir": data_dir_setting or dnd_paths.DEFAULT_DATA_DIR}, indent=2) + "\n", encoding="utf-8")
    data = dnd_paths.data_dir(root)
    existed = data.exists()
    data.mkdir(parents=True, exist_ok=True)
    if not existed:
        ensure_gitignore(data)
    seed_cache(data)
    return data


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("optin")
    o.add_argument("--data-dir")
    o.add_argument("--project")
    a = ap.parse_args()
    root = Path(a.project).resolve() if a.project else dnd_paths.project_root()
    print(f"data dir: {optin(root, a.data_dir)}")
    print(f"config: {dnd_paths.config_path(root)}")
    print("NEXT: reconnect the dm20 MCP server (/mcp -> dm20-protocol -> Reconnect) before create_campaign.")
