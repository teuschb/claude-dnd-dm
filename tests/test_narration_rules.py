"""check_narration_rules.py: banned words, internal ids, "beat", DCs, combat positions and reactions."""
from __future__ import annotations

import json
import os
import shutil
import time
import unittest

from helpers import PREFIXES, FixtureProject, tool_payload

SCRIPT = "check_narration_rules.py"
TOOLS = ("party_resolve_action", "party_push")


class NarrationRules(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = FixtureProject()
        self.addCleanup(self.fx.__exit__)
        self.mira = self.fx.pc("Mira Ashdown")
        self.fx.add_action("act_101", self.mira["id"], "I check the lamp.")

    def run_check(self, narrative: str, *, tool: str = "party_resolve_action", notes: str = "",
                  private=None, prefix: str = "plugin", via: str = "env"):
        ti = {"action_id": "act_101", "narrative": narrative, "dm_notes": notes}
        if private is not None:
            ti["private_messages"] = private
        return self.fx.run_hook(SCRIPT, tool_payload(tool, ti, prefix=prefix), via=via)

    def assertAllowed(self, r) -> None:
        self.assertEqual(r.returncode, 0, r.stderr)

    def assertBlocked(self, r, *fragments: str) -> None:
        self.assertEqual(r.returncode, 2, f"expected a block; stderr={r.stderr!r}")
        for f in fragments:
            self.assertIn(f, r.stderr)

    # -- plain words ---------------------------------------------------------
    def test_clean_narrative_passes_for_every_tool_prefix_and_lookup(self) -> None:
        for tool in TOOLS:
            for prefix in PREFIXES:
                for via in ("env", "cwd"):
                    with self.subTest(tool=tool, prefix=prefix, via=via):
                        self.assertAllowed(self.run_check("Mira checks the lamp. It burns steady.",
                                                          tool=tool, prefix=prefix, via=via))

    def test_banned_word_blocks_for_every_tool_prefix_and_lookup(self) -> None:
        for tool in TOOLS:
            for prefix in PREFIXES:
                for via in ("env", "cwd"):
                    with self.subTest(tool=tool, prefix=prefix, via=via):
                        self.assertBlocked(self.run_check("Mira checks the lamp above the quay.",
                                                          tool=tool, prefix=prefix, via=via),
                                           '"quay" is on the banned-jargon list', '"the dock"')

    def test_banned_word_matches_inflections_and_case(self) -> None:
        self.assertBlocked(self.run_check("Mira looks down at the Quays."), '"quay"')

    def test_banned_word_inside_another_word_passes(self) -> None:
        self.assertAllowed(self.run_check("Mira hears the antiquay bell."))  # \b before the word

    def test_banned_word_in_private_message_blocks(self) -> None:
        for private in ({"p1": "You smell the bilge."}, json.dumps({"p1": "You smell the bilge."}),
                        "You smell the bilge."):
            with self.subTest(private=type(private).__name__):
                self.assertBlocked(self.run_check("Mira checks the lamp.", private=private), '"bilge"')

    def test_words_exempt_skips_word_checks(self) -> None:
        self.assertAllowed(self.run_check("Mira checks the quay (DC 12).", notes="[words-exempt: quoting a sign]"))

    def test_internal_ids_block(self) -> None:
        self.assertBlocked(self.run_check("Mira checks the lamp (act_101)."), "internal id")
        self.assertBlocked(self.run_check("Mira checks the lamp.", private={"p1": "re res_7"}), "internal id")

    def test_beat_as_pacing_term_blocks_but_verb_passes(self) -> None:
        self.assertBlocked(self.run_check("Mira checks the lamp. A beat of silence."), '"beat"')
        self.assertAllowed(self.run_check("Mira checks the lamp. Waves beat the rocks."))

    def test_dc_blocks_in_public_only(self) -> None:
        self.assertBlocked(self.run_check("Mira checks the lamp (DC 12)."), "a DC is shown")
        self.assertAllowed(self.run_check("Mira checks the lamp.", private={"p1": "That was DC 12."}))

    # -- combat ----------------------------------------------------------------
    def test_out_of_combat_needs_no_positions(self) -> None:
        self.assertAllowed(self.run_check("Mira attacks: 14+5 hit for 6."))

    def test_combat_resolve_needs_positions(self) -> None:
        self.fx.set_combat(True)
        self.assertBlocked(self.run_check("Mira draws her bow."), "Where everyone is")
        self.assertAllowed(self.run_check("Mira draws her bow. Where everyone is: Mira by the door."))
        self.assertAllowed(self.run_check("Mira draws her bow.", notes="[positions-exempt: scene cut]"))

    def test_combat_push_needs_no_positions(self) -> None:
        self.fx.set_combat(True)
        self.assertAllowed(self.run_check("The fog rolls in.", tool="party_push"))

    def test_combat_roll_needs_reactions_note(self) -> None:
        self.fx.set_combat(True)
        text = "Mira attacks: 14+5 hit for 6. Where everyone is: all adjacent."
        self.assertBlocked(self.run_check(text), "reactions")
        self.assertAllowed(self.run_check(text, notes="reactions: none possible"))
        self.assertAllowed(self.run_check(text, tool="party_push"))  # push isn't a resolve

    def test_combat_blank_narrative_passes(self) -> None:
        self.fx.set_combat(True)
        self.assertAllowed(self.run_check("", private={"p1": "Your turn."}))

    # -- which campaign's rules -----------------------------------------------
    def test_rules_come_from_the_campaign_that_owns_the_action(self) -> None:
        other = self.fx.data / "campaigns" / "Second Keep"
        shutil.copytree(self.fx.campaign, other)
        (other / "narration_rules.json").write_text(json.dumps({"banned_words": {"lamp": "light"}}))
        (other / "party" / "actions.jsonl").write_text(
            json.dumps({"id": "act_202", "player_id": self.mira["id"], "text": "x", "status": "pending"}) + "\n")
        old = time.time() - 600  # the owning campaign is not the most recent one
        os.utime(other / "party" / "actions.jsonl", (old, old))

        r = self.fx.run_hook(SCRIPT, tool_payload("party_resolve_action",
                                                  {"action_id": "act_202", "narrative": "Mira checks the lamp."}))
        self.assertBlocked(r, '"lamp"')
        # an action id in neither log falls back to the most recent campaign (Fixture Keep)
        r = self.fx.run_hook(SCRIPT, tool_payload("party_push", {"narrative": "Mira checks the lamp."}))
        self.assertAllowed(r)

    def test_no_party_log_allows(self) -> None:
        shutil.rmtree(self.fx.campaign / "party")
        self.assertAllowed(self.run_check("Mira checks the quay."))

    def test_not_a_dnd_project_allows(self) -> None:
        shutil.rmtree(self.fx.root / ".claude")  # data dir falls back to <project>/dnd, which doesn't exist
        self.assertAllowed(self.run_check("Mira checks the quay."))

    def test_broken_rules_file_allows(self) -> None:
        (self.fx.campaign / "narration_rules.json").write_text("{not json")
        r = self.run_check("Mira checks the quay.")
        self.assertAllowed(r)
        self.assertIn("skipped", r.stderr)


if __name__ == "__main__":
    unittest.main()
