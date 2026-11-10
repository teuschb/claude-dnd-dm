"""guard_active_campaign.py: dm20 writes are blocked until this session has loaded its campaign."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
import unittest

from helpers import CAMPAIGN, PREFIXES, SCRIPTS, FixtureProject, clean_env, tool_payload

SCRIPT = "guard_active_campaign.py"
LOADED = f"📖 Loaded campaign: '{CAMPAIGN}'. Campaign is now active!"


class GuardActiveCampaign(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = FixtureProject()

    def tearDown(self) -> None:
        self.fx.__exit__()

    def pre(self, tool: str, prefix: str = "plugin", **extra) -> subprocess.CompletedProcess:
        return self.fx.run_hook(SCRIPT, tool_payload(tool, {}, prefix=prefix, **extra), "pre")

    def post(self, tool: str, tool_input: dict, response, **extra) -> subprocess.CompletedProcess:
        payload = tool_payload(tool, tool_input, hook_event_name="PostToolUse", tool_response=response, **extra)
        return self.fx.run_hook(SCRIPT, payload, "post")

    def load(self, **extra) -> None:
        self.post("load_campaign", {"name": CAMPAIGN}, [{"type": "text", "text": LOADED}], **extra)

    def session_start(self, source: str, session_id: str = "test-session") -> subprocess.CompletedProcess:
        env = clean_env(CLAUDE_PLUGIN_DATA=str(self.fx.tmp / "plugin_data"), CLAUDE_PROJECT_DIR=str(self.fx.root))
        payload = {"hook_event_name": "SessionStart", "source": source, "session_id": session_id,
                   "cwd": str(self.fx.root)}
        return subprocess.run([sys.executable, str(SCRIPTS / "session_context.py")], input=json.dumps(payload),
                              capture_output=True, text=True, env=env, cwd=self.fx.tmp, timeout=60)

    def test_write_before_load_is_blocked_for_both_prefixes(self) -> None:
        for prefix in PREFIXES:
            for tool in ("update_game_state", "party_resolve_action", "party_push", "update_character"):
                with self.subTest(prefix=prefix, tool=tool):
                    res = self.pre(tool, prefix=prefix)
                    self.assertEqual(res.returncode, 2, res.stderr)
                    self.assertIn("load_campaign", res.stderr)
                    self.assertIn(CAMPAIGN, res.stderr)  # names the campaign dm20 is on

    def test_unknown_tool_counts_as_a_write(self) -> None:
        self.assertEqual(self.pre("some_future_tool").returncode, 2)

    def test_reads_lookups_and_loaders_pass_before_load(self) -> None:
        for tool in ("get_game_state", "list_characters", "search_rules", "get_spell_info",
                     "list_campaigns", "load_campaign", "create_campaign"):
            with self.subTest(tool=tool):
                self.assertEqual(self.pre(tool).returncode, 0)

    def test_write_after_load_passes_for_this_session_only(self) -> None:
        self.load()
        self.assertEqual(self.pre("update_game_state").returncode, 0)
        self.assertEqual(self.pre("update_game_state", session_id="other-session").returncode, 2)

    def test_create_campaign_counts_as_a_load(self) -> None:
        self.post("create_campaign", {"name": "New Hold"}, "✅ Created campaign 'New Hold'")
        self.assertEqual(self.pre("update_game_state").returncode, 0)

    def test_failed_create_campaign_records_nothing(self) -> None:
        self.post("create_campaign", {"name": "X"}, "❌ Invalid rules_version 'x'. Must be '2014' or '2024'.")
        self.assertEqual(self.pre("update_game_state").returncode, 2)

    def test_session_start_clears_the_record_except_after_compaction(self) -> None:
        self.load()
        res = self.session_start("compact")
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertEqual(self.pre("update_game_state").returncode, 0)
        for source in ("startup", "resume"):
            with self.subTest(source=source):
                self.load()
                res = self.session_start(source)
                self.assertEqual(res.returncode, 0, res.stderr)
                self.assertIn(f"'{CAMPAIGN}'", res.stdout)  # names the default campaign
                self.assertEqual(self.pre("update_game_state").returncode, 2)

    def test_names_the_most_recently_modified_campaign(self) -> None:
        newer = self.fx.data / "campaigns" / "Newer Hold"
        newer.mkdir()
        (newer / "campaign.json").write_text("{}", encoding="utf-8")
        later = time.time() + 60
        os.utime(newer / "campaign.json", (later, later))
        self.assertIn("'Newer Hold'", self.pre("update_game_state").stderr)

    def test_project_without_dnd_is_left_alone(self) -> None:
        (self.fx.root / ".claude" / "dnd-dm.json").unlink()
        shutil.rmtree(self.fx.root / "rpg")
        self.assertEqual(self.pre("update_game_state").returncode, 0)

    def test_bad_payload_allows_the_call(self) -> None:
        env = clean_env(CLAUDE_PLUGIN_DATA=str(self.fx.tmp / "plugin_data"), CLAUDE_PROJECT_DIR=str(self.fx.root))
        res = subprocess.run([sys.executable, str(SCRIPTS / SCRIPT), "pre"], input="not json",
                             capture_output=True, text=True, env=env, timeout=60)
        self.assertEqual(res.returncode, 0)

    def test_selftest_passes(self) -> None:
        res = subprocess.run([sys.executable, str(SCRIPTS / SCRIPT), "--selftest"],
                             capture_output=True, text=True, env=clean_env(), timeout=120)
        self.assertEqual(res.returncode, 0, res.stdout + res.stderr)


if __name__ == "__main__":
    unittest.main()
