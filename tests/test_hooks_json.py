"""hooks.json wiring: each hook fires for both dm20 tool-name prefixes and its script exists."""
from __future__ import annotations

import json
import re
import unittest

from helpers import PLUGIN, PREFIXES

HOOKS = json.loads((PLUGIN / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]


def scripts_for(event: str, tool_name: str) -> set[str]:
    out = set()
    for entry in HOOKS.get(event, []):
        if re.fullmatch(entry.get("matcher", ".*"), tool_name):
            for h in entry["hooks"]:
                m = re.search(r"scripts/(\w+\.py)", h["command"])
                if m:
                    out.add(m.group(1))
    return out


class HooksJson(unittest.TestCase):
    def test_every_hook_script_exists(self) -> None:
        for event, entries in HOOKS.items():
            for entry in entries:
                for h in entry["hooks"]:
                    for script in re.findall(r"scripts/(\w+\.py)", h["command"]):
                        with self.subTest(event=event, script=script):
                            self.assertTrue((PLUGIN / "scripts" / script).is_file())

    def test_party_hooks_match_both_prefixes(self) -> None:
        want = {
            "party_resolve_action": {"check_resolve_leads.py", "check_narration_rules.py"},
            "party_push": {"check_narration_rules.py"},
        }
        for tool, scripts in want.items():
            for prefix, pre in PREFIXES.items():
                with self.subTest(tool=tool, prefix=prefix):
                    self.assertLessEqual(scripts, scripts_for("PreToolUse", pre + tool))

    def test_party_hooks_skip_other_tools(self) -> None:
        for pre in PREFIXES.values():
            got = scripts_for("PreToolUse", pre + "get_game_state")
            self.assertFalse(got & {"check_resolve_leads.py", "check_narration_rules.py"}, got)

    def test_campaign_guard_runs_on_every_dm20_tool(self) -> None:
        for pre in PREFIXES.values():
            for tool in ("update_game_state", "get_game_state", "party_push"):
                with self.subTest(prefix=pre, tool=tool):
                    self.assertIn("guard_active_campaign.py", scripts_for("PreToolUse", pre + tool))
        self.assertNotIn("guard_active_campaign.py", scripts_for("PreToolUse", "Bash"))

    def test_campaign_tracker_runs_after_loaders_only(self) -> None:
        for pre in PREFIXES.values():
            for tool in ("load_campaign", "create_campaign"):
                with self.subTest(prefix=pre, tool=tool):
                    self.assertIn("guard_active_campaign.py", scripts_for("PostToolUse", pre + tool))
            self.assertNotIn("guard_active_campaign.py", scripts_for("PostToolUse", pre + "update_game_state"))

    def test_privacy_guard_runs_on_bash(self) -> None:
        self.assertIn("guard_campaign_privacy.py", scripts_for("PreToolUse", "Bash"))


if __name__ == "__main__":
    unittest.main()
