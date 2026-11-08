#!/usr/bin/env python3
"""Guard against dm20 writing into the wrong campaign.

At startup dm20 loads the most recently modified campaign, whichever session
touched it last. With several Claude Code sessions open, a write tool called
before `load_campaign` lands in another campaign's files.

This script is three hooks, picked by its first argument:

  pre   PreToolUse on every dm20 tool. Blocks (exit 2, reason on stderr) any
        tool that writes to the active campaign until this session has called
        `load_campaign` or `create_campaign`. Tools that only read, or that don't
        touch the active campaign (rules lookups, list_campaigns, ...), pass.
  post  PostToolUse on load_campaign / create_campaign. Records, per session_id,
        which campaign this session loaded.
  (SessionStart calls forget() and default_campaign() from session_context.py.)

The record is dropped at every SessionStart except a compaction, because a
startup or resume starts a fresh dm20 process that has again loaded the most
recent campaign. (/clear gets a new session_id, so it needs a fresh load too.)

Known gap: reconnecting dm20 mid-session (/mcp) restarts the server without a
SessionStart, so the record survives while dm20 is back on the most recent
campaign.

Any internal error allows the call: a hook bug must never stall the game.
Run `python3 guard_active_campaign.py --selftest` to exercise the logic.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import dnd_paths  # noqa: E402

# dm20 tools that may run before load_campaign: they only read, or they don't
# act on the active campaign. Everything else is treated as a write, so a new
# dm20 tool is guarded by default.
ALLOWED_BEFORE_LOAD = frozenset({
    # choosing a campaign
    "list_campaigns", "load_campaign", "create_campaign", "delete_campaign", "get_campaign_info",
    # rules, dice and maths
    "search_rules", "get_class_info", "get_race_info", "get_spell_info", "get_monster_info",
    "list_rulebooks", "validate_character_rules", "roll_dice", "calculate_experience",
    "build_encounter_tool",
    # library, packs, adventures, server info
    "list_library", "get_library_toc", "search_library", "ask_books", "list_enabled_library",
    "open_library_folder", "list_packs", "validate_pack", "discover_adventures",
    "check_for_updates", "get_release_notes",
    # reads of the active campaign (wrong data, but nothing overwritten)
    "get_character", "list_characters", "get_npc", "list_npcs", "get_location", "list_locations",
    "list_quests", "get_game_state", "get_sessions", "get_events", "show_map",
    "get_party_status", "get_claudmaster_session_state",
})
LOADERS = frozenset({"load_campaign", "create_campaign"})
LOADED_RE = re.compile(r"Loaded campaign: '([^']+)'")


def state_dir() -> Path:
    base = os.environ.get("CLAUDE_PLUGIN_DATA")
    root = Path(base) if base else Path(tempfile.gettempdir()) / "dnd-dm"
    return root / "loaded_campaigns"


def marker(session_id: str) -> Path:
    safe = re.sub(r"[^A-Za-z0-9_.-]", "_", session_id)
    return state_dir() / f"{safe}.json"


def forget(session_id: str | None) -> None:
    if session_id:
        try:
            marker(session_id).unlink()
        except OSError:
            pass


def loaded_campaign(session_id: str) -> str | None:
    try:
        return json.loads(marker(session_id).read_text(encoding="utf-8")).get("campaign") or None
    except (OSError, ValueError, AttributeError):
        return None


def default_campaign(data: Path) -> str | None:
    """The campaign dm20 loads at startup (same rule as dm20's _load_current_campaign)."""
    campaigns = data / "campaigns"
    try:
        files = list(campaigns.glob("*.json")) + [d / "campaign.json" for d in campaigns.iterdir()
                                                   if d.is_dir() and (d / "campaign.json").exists()]
    except OSError:
        return None
    if not files:
        return None
    latest = max(files, key=lambda f: f.stat().st_mtime)
    return latest.parent.name if latest.name == "campaign.json" else latest.stem


def short_name(tool_name: str) -> str:
    return tool_name.rsplit("__", 1)[-1]


def response_text(resp) -> str:
    return resp if isinstance(resp, str) else json.dumps(resp, ensure_ascii=False)


def pre(payload: dict) -> int:
    tool = short_name(payload.get("tool_name", ""))
    session_id = payload.get("session_id")
    if not tool or tool in ALLOWED_BEFORE_LOAD or not session_id:
        return 0
    if not dnd_paths.is_dnd_project(dnd_paths.project_root(payload.get("cwd"))):
        return 0
    if loaded_campaign(session_id):
        return 0
    data = dnd_paths.data_dir(dnd_paths.project_root(payload.get("cwd")))
    active = default_campaign(data)
    active_txt = f" dm20 is currently on '{active}', the most recently modified campaign," if active else ""
    sys.stderr.write(
        f"Blocked {tool}: this session hasn't called load_campaign yet.{active_txt} which may not be "
        "the one you mean (another session may have touched it). Call load_campaign with the campaign "
        "you are running, then retry.\n")
    return 2


def post(payload: dict) -> int:
    tool = short_name(payload.get("tool_name", ""))
    session_id = payload.get("session_id")
    if tool not in LOADERS or not session_id:
        return 0
    text = response_text(payload.get("tool_response"))
    match = LOADED_RE.search(text)
    if match:
        name = match.group(1)
    elif "❌" in text:  # create_campaign reports its failures as text
        return 0
    else:
        name = (payload.get("tool_input") or {}).get("name")
    if not name:
        return 0
    path = marker(session_id)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"campaign": name, "tool": tool, "at": time.time()}), encoding="utf-8")
    return 0


def selftest() -> int:
    import subprocess
    with tempfile.TemporaryDirectory() as tmp:
        project = Path(tmp) / "proj"
        for name, age in (("Older", 100), ("Newest", 0)):
            d = project / "dnd" / "campaigns" / name
            d.mkdir(parents=True)
            (d / "campaign.json").write_text("{}")
            t = time.time() - age
            os.utime(d / "campaign.json", (t, t))
        env = {**os.environ, "CLAUDE_PLUGIN_DATA": str(Path(tmp) / "plugin_data"),
               "CLAUDE_PROJECT_DIR": str(project)}

        def run(mode: str, **payload) -> int:
            payload.setdefault("session_id", "s1")
            payload["tool_name"] = "mcp__plugin_dnd-dm_dm20-protocol__" + payload["tool_name"]
            return subprocess.run([sys.executable, __file__, mode], input=json.dumps(payload), env=env,
                                  text=True, capture_output=True).returncode

        checks = [
            ("write before load is blocked", run("pre", tool_name="update_game_state"), 2),
            ("party write before load is blocked", run("pre", tool_name="party_resolve_action"), 2),
            ("read before load passes", run("pre", tool_name="get_game_state"), 0),
            ("rules lookup passes", run("pre", tool_name="get_spell_info"), 0),
            ("load_campaign itself passes", run("pre", tool_name="load_campaign"), 0),
        ]
        run("post", tool_name="load_campaign", tool_input={"name": "Older"},
            tool_response=[{"type": "text", "text": "📖 Loaded campaign: 'Older'. Campaign is now active!"}])
        checks += [
            ("write after load passes", run("pre", tool_name="update_game_state"), 0),
            ("other session still blocked", run("pre", tool_name="update_game_state", session_id="s2"), 2),
        ]
        run("post", tool_name="create_campaign", session_id="s3", tool_input={"name": "X"},
            tool_response="❌ Invalid rules_version 'x'. Must be '2014' or '2024'.")
        checks.append(("failed create_campaign records nothing",
                       run("pre", tool_name="update_game_state", session_id="s3"), 2))
        os.environ["CLAUDE_PLUGIN_DATA"] = env["CLAUDE_PLUGIN_DATA"]
        forget("s1")
        checks.append(("forget() re-blocks", run("pre", tool_name="update_game_state"), 2))
        checks.append(("default campaign is the newest", default_campaign(project / "dnd"), "Newest"))
    failed = 0
    for label, got, want in checks:
        ok = got == want
        failed += not ok
        print(f"{'ok  ' if ok else 'FAIL'} {label} (got {got!r}, want {want!r})")
    return 1 if failed else 0


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "--selftest":
        return selftest()
    try:
        payload = json.load(sys.stdin)
        return {"pre": pre, "post": post}.get(mode, lambda _p: 0)(payload)
    except Exception:
        return 0


if __name__ == "__main__":
    sys.exit(main())
