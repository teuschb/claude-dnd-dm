"""Integration: bin/dm20 loads the fixture campaign, the SRD base and the custom overlays.

Starts the real pinned dm20 over MCP stdio, so it needs `uvx` (and network
the first time, to build the pinned environment; `plugin/bin/dm20 --prewarm`
does that ahead). Skipped when uvx is missing or DND_DM_SKIP_DM20=1.
"""
from __future__ import annotations

import json
import os
import shutil
import unittest

from helpers import CAMPAIGN, PLUGIN, FixtureProject, start_dm20

SHIPPED_OVERLAYS = ["species_corrections", "class_progression", "feats", "spells"]  # session-start order
# an entry each overlay carries, and the source dm20 must report for it once the overlay is loaded
# (later sources win, so these resolve to the overlay rather than the SRD base)
OVERLAY_PROBES = {
    "species_corrections": ("Goliath", "race"),
    "class_progression": ("Barbarian", "class"),
    "feats": ("Alert", "feat"),
    "spells": ("Acid Arrow", "spell"),
}
SKIP = os.environ.get("DND_DM_SKIP_DM20") == "1" or not shutil.which("uvx")


def ok(text: str) -> bool:
    head = text.lstrip()[:120].lower()
    return not (head.startswith(("❌", "⚠️", "error")) or "not found" in head)


@unittest.skipIf(SKIP, "uvx not available (or DND_DM_SKIP_DM20=1)")
class Dm20Load(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.fx = FixtureProject()
        custom = cls.fx.campaign / "rulebooks" / "custom"
        for name in SHIPPED_OVERLAYS:  # what new-campaign copies in
            shutil.copy2(PLUGIN / "templates" / "rulebooks" / "custom" / f"srd_2024_{name}.json", custom)
        cls.client = start_dm20(cls.fx.root, cls.fx.tmp)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client.close()
        cls.fx.__exit__()

    def call(self, tool: str, **args) -> str:
        err, text = self.client.call(tool, **args)
        self.assertFalse(err, text[:300])
        self.assertTrue(ok(text), f"{tool}: {text[:300]}")
        return text

    def test_1_wrapper_used_the_project_data_dir(self) -> None:
        log = (self.fx.tmp / "wrapper.log").read_text(encoding="utf-8")
        self.assertIn("mode=project", log)
        self.assertIn(f"storage={self.fx.data}", log)
        self.assertTrue((self.fx.data / "rulebook_cache" / "srd_2024").is_dir(), "SRD cache was not seeded")

    def test_2_load_campaign_rulebooks_and_overlays(self) -> None:
        self.assertIn(CAMPAIGN, self.call("list_campaigns"))
        self.assertIn(f"Loaded campaign: '{CAMPAIGN}'", self.call("load_campaign", name=CAMPAIGN))
        self.call("load_rulebook", source="srd", version="2024")
        # before the campaign's own overlay loads, its content doesn't exist
        self.assertIn("No results", self.call("search_rules", query="Lantern Warden"))

        paths = [f"custom/srd_2024_{n}.json" for n in SHIPPED_OVERLAYS] + ["custom/fixture_keep_feats.json"]
        for path in paths:
            with self.subTest(path=path):
                self.assertIn(f"Loaded custom rulebook: {path}", self.call("load_rulebook", source="custom", path=path))

        manifest = json.loads((self.fx.campaign / "rulebooks" / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["active_sources"]), 1 + len(paths), manifest)
        self.assertEqual(manifest["active_sources"][0]["type"], "srd")

        for overlay, (name, kind) in OVERLAY_PROBES.items():
            with self.subTest(overlay=overlay):
                source = "custom-srd-2024-" + overlay.replace("_", "-")
                self.assertIn(f"**{name}** ({kind}) — _{source}_", self.call("search_rules", query=name))
        self.assertIn("**Lantern Warden** (feat) — _custom-fixture-keep-feats_",
                      self.call("search_rules", query="Lantern Warden"))
        self.assertIn("**Speed:** 35 ft.", self.call("get_race_info", name="Goliath"))

    def test_2b_missing_overlay_is_an_error(self) -> None:
        err, text = self.client.call("load_rulebook", source="custom", path="custom/not_there.json")
        self.assertTrue(err or not ok(text), text[:200])

    def test_3_campaign_records_read_back(self) -> None:
        chars = self.call("list_characters")
        for name in ("Mira Ashdown", "Bram Von Holt"):
            self.assertIn(name, chars)
        mira = self.call("get_character", name_or_id="Mira Ashdown")
        self.assertIn("Ranger", mira)
        self.assertIn("lamp room", self.call("get_game_state"))

    def test_4_overlays_survive_a_restart(self) -> None:
        manifest_path = self.fx.campaign / "rulebooks" / "manifest.json"
        before = manifest_path.read_text(encoding="utf-8")
        custom = [s for s in json.loads(before)["active_sources"] if s["type"] == "custom"]
        self.assertTrue(custom and all(s.get("path", "").startswith("custom/") for s in custom), before)

        self.client.close()
        type(self).client = start_dm20(self.fx.root, self.fx.tmp)
        # the fresh server restores the manifest at startup; that must not rewrite it
        self.assertEqual(manifest_path.read_text(encoding="utf-8"), before)
        self.assertIn(f"Loaded campaign: '{CAMPAIGN}'", self.call("load_campaign", name=CAMPAIGN))
        # no load_rulebook calls: the overlays come back from the manifest
        self.assertIn("**Lantern Warden** (feat) — _custom-fixture-keep-feats_",
                      self.call("search_rules", query="Lantern Warden"))
        self.assertIn("**Speed:** 35 ft.", self.call("get_race_info", name="Goliath"))
        self.assertEqual(manifest_path.read_text(encoding="utf-8"), before)


@unittest.skipIf(SKIP, "uvx not available (or DND_DM_SKIP_DM20=1)")
class Dm20IdleProject(unittest.TestCase):
    def test_project_that_has_not_opted_in_gets_nothing_written(self) -> None:
        with FixtureProject() as fx:
            shutil.rmtree(fx.root / ".claude")
            shutil.rmtree(fx.root / "rpg")
            client = start_dm20(fx.root, fx.tmp)
            try:
                client.call("list_campaigns")
            finally:
                client.close()
            self.assertEqual(list(fx.root.iterdir()), [])
            self.assertIn("mode=idle", (fx.tmp / "wrapper.log").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
