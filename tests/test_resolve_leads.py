"""check_resolve_leads.py: lead with the acting character, carry their dialogue, aliases."""
from __future__ import annotations

import shutil
import unittest

from helpers import PREFIXES, FixtureProject, tool_payload

SCRIPT = "check_resolve_leads.py"


class ResolveLeads(unittest.TestCase):
    def setUp(self) -> None:
        self.fx = FixtureProject()
        self.addCleanup(self.fx.__exit__)
        self.mira = self.fx.pc("Mira Ashdown")["id"]
        self.bram = self.fx.pc("Bram Von Holt")["id"]
        self.fx.add_action("act_1", self.mira, "I wave at the cat on the wall.")
        self.fx.add_action("act_2", self.mira, 'I say "good morning to you, little cat".')
        self.fx.add_action("act_3", self.bram, "I light the lamp.")
        self.fx.add_action("act_4", self.mira, "Let's head down to the shore.")
        self.fx.add_action("act_5", self.mira, "DM, please advance the story.")
        self.fx.add_action("act_6", self.mira, "I nod. “Hi there.” “Where is the lighthouse keeper tonight?”")

    def run_check(self, action_id: str, narrative: str, notes: str = "", prefix: str = "plugin", via: str = "env"):
        ti = {"action_id": action_id, "narrative": narrative, "dm_notes": notes}
        return self.fx.run_hook(SCRIPT, tool_payload("party_resolve_action", ti, prefix=prefix), via=via)

    def assertAllowed(self, r) -> None:
        self.assertEqual(r.returncode, 0, r.stderr)

    def assertBlocked(self, r, *fragments: str) -> None:
        self.assertEqual(r.returncode, 2, f"expected a block; stderr={r.stderr!r}")
        for f in fragments:
            self.assertIn(f, r.stderr)

    # -- naming the acting character ---------------------------------------------
    def test_naming_the_pc_passes_and_omitting_blocks_for_both_prefixes_and_lookups(self) -> None:
        for prefix in PREFIXES:
            for via in ("env", "cwd"):
                with self.subTest(prefix=prefix, via=via):
                    self.assertAllowed(self.run_check("act_1", "Mira waves at the cat. It blinks.",
                                                      prefix=prefix, via=via))
                    self.assertBlocked(self.run_check("act_1", "The cat on the wall blinks slowly.",
                                                      prefix=prefix, via=via),
                                       "doesn't name the acting character")

    def test_surname_possessive_and_player_name_count(self) -> None:
        self.assertAllowed(self.run_check("act_1", "Ashdown waves. The cat blinks."))
        self.assertAllowed(self.run_check("act_1", "Mira's wave earns a slow blink."))
        self.assertAllowed(self.run_check("act_1", "Player One's ranger waves. The cat blinks."))

    def test_alias_from_lead_aliases_counts(self) -> None:
        self.assertAllowed(self.run_check("act_1", "Skree circles as the wave goes up. The cat blinks."))

    def test_alias_belongs_to_its_own_pc_only(self) -> None:
        self.assertBlocked(self.run_check("act_3", "Skree circles. The lamp catches."), "bram / holt")

    def test_name_particles_are_not_aliases(self) -> None:
        self.assertBlocked(self.run_check("act_3", "Von lights it. The lamp catches."))
        self.assertAllowed(self.run_check("act_3", "Holt lights the lamp. It catches."))

    def test_name_after_the_opening_blocks(self) -> None:
        late = "The wind rises over the keep. " * 12 + "Mira waves."
        self.assertBlocked(self.run_check("act_1", late), "opening")

    def test_party_declaration_lets_any_pc_or_the_group_lead(self) -> None:
        self.assertAllowed(self.run_check("act_4", "Bram leads the way to the shore."))
        self.assertAllowed(self.run_check("act_4", "The group heads down to the shore."))
        self.assertBlocked(self.run_check("act_4", "Gulls wheel over the shore."))

    # -- dialogue -------------------------------------------------------------------
    def test_dropped_quote_blocks(self) -> None:
        self.assertBlocked(self.run_check("act_2", "Mira greets the cat. It yawns."), "the player wrote dialogue")

    def test_quote_verbatim_or_close_paraphrase_passes(self) -> None:
        self.assertAllowed(self.run_check("act_2", 'Mira says, "Good morning to you, little cat." It yawns.'))
        self.assertAllowed(self.run_check("act_2", "Mira wishes the little cat a good morning. It yawns."))

    def test_curly_quotes_and_short_lines(self) -> None:
        # "Hi there." is under three words, so only the second line counts
        self.assertBlocked(self.run_check("act_6", "Mira nods. Hi there, she says."), "the player wrote dialogue")
        self.assertAllowed(self.run_check("act_6", "Mira nods: where is the keeper tonight?"))

    # -- allowed without checks -----------------------------------------------------
    def test_exemptions(self) -> None:
        self.assertAllowed(self.run_check("act_1", ""))
        self.assertAllowed(self.run_check("act_1", "*(The DM sends a private message.)*"))
        self.assertAllowed(self.run_check("act_1", "The cat blinks.", notes="[lead-exempt: scene reset]"))
        self.assertAllowed(self.run_check("act_5", "The tide turns."))  # director command
        self.assertAllowed(self.run_check("act_999", "The cat blinks."))  # unknown action

    def test_missing_characters_file_allows(self) -> None:
        (self.fx.campaign / "characters.json").unlink()
        r = self.run_check("act_1", "The cat blinks.")
        self.assertAllowed(r)
        self.assertIn("skipped", r.stderr)

    def test_not_a_dnd_project_allows(self) -> None:
        shutil.rmtree(self.fx.root / ".claude")
        self.assertAllowed(self.run_check("act_1", "The cat blinks."))


if __name__ == "__main__":
    unittest.main()
