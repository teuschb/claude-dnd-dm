#!/usr/bin/env python3
"""Regenerate tests/fixtures/project from a real dm20 run.

dm20 writes the campaign files itself (create_campaign, create_character,
update_game_state), so the fixture is always in the format the pinned dm20
reads. Then the test-only files are added: narration_rules.json,
lead_aliases.json and a tiny custom overlay.

Run after bumping the dm20 pin in plugin/bin/dm20:

    python3 tests/fixtures/make_fixture.py

Needs uvx and network access the first time (to build the pinned dm20).
"""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from helpers import CAMPAIGN, DATA_REL, FIXTURE, start_dm20  # noqa: E402

CHARACTERS = [
    # name, class, race, player: "Von" exercises the hook's skip-list for name particles
    ("Mira Ashdown", "Ranger", "Human", "Player One"),
    ("Bram Von Holt", "Cleric", "Dwarf", "Player Two"),
]
# Copied into the fixture so dm20 has a campaign-local custom rulebook with
# content that exists nowhere else (the load test searches for it).
FIXTURE_OVERLAY = {
    "$schema": "dm20-protocol/rulebook-v1",
    "name": "Fixture Keep test overlay",
    "version": "1.0",
    "content": {
        "feats": [{
            "index": "lantern-warden", "name": "Lantern Warden", "source": "fixture-keep",
            "desc": ["Origin Feat", "Fixture-only feat used by the dnd-dm plugin tests."],
        }],
    },
}


def call(client, tool: str, **args) -> str:
    err, text = client.call(tool, **args)
    if err or text.lstrip().startswith(("❌", "⚠️", "Error")):
        raise SystemExit(f"{tool} failed: {text[:300]}")
    return text


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="dnd-dm-fixture-") as tmp:
        tmp = Path(tmp).resolve()
        project = tmp / "project"
        (project / ".claude").mkdir(parents=True)
        (project / ".claude" / "dnd-dm.json").write_text(json.dumps({"data_dir": str(DATA_REL)}) + "\n")
        client = start_dm20(project, tmp)
        try:
            call(client, "create_campaign", name=CAMPAIGN, description="Test fixture for the dnd-dm plugin.",
                 setting="A lighthouse keep on a grey coast.", rules_version="2024")
            call(client, "load_rulebook", source="srd", version="2024")  # create_character needs it
            for name, cls, race, player in CHARACTERS:
                call(client, "create_character", name=name, character_class=cls, class_level=1, race=race,
                     player_name=player)
            call(client, "update_game_state", current_location="The keep's lamp room", current_session=1,
                 party_level=1, in_combat=False)
        finally:
            client.close()

        src = project / DATA_REL / "campaigns" / CAMPAIGN
        if FIXTURE.exists():
            shutil.rmtree(FIXTURE)
        dest = FIXTURE / DATA_REL / "campaigns" / CAMPAIGN
        shutil.copytree(src, dest, ignore=shutil.ignore_patterns("party", "*.log"))
        (FIXTURE / ".claude").mkdir(parents=True)
        shutil.copy2(project / ".claude" / "dnd-dm.json", FIXTURE / ".claude" / "dnd-dm.json")

    chars = json.loads((dest / "characters.json").read_text(encoding="utf-8"))
    mira = next(c for c in chars.values() if c["name"] == "Mira Ashdown")
    (dest / "lead_aliases.json").write_text(json.dumps({
        "_comment": "Test fixture: Mira commands a hawk called Skree.",
        mira["id"]: ["skree"],
    }, indent=2) + "\n")
    (dest / "narration_rules.json").write_text(json.dumps({
        "banned_words": {"bilge": "the bottom of the boat", "quay": "the dock"},
    }, indent=2) + "\n")
    custom = dest / "rulebooks" / "custom"
    custom.mkdir(parents=True, exist_ok=True)
    (custom / "fixture_keep_feats.json").write_text(json.dumps(FIXTURE_OVERLAY, indent=2) + "\n")
    print(f"wrote {FIXTURE}")
    for p in sorted(FIXTURE.rglob("*")):
        if p.is_file():
            print("  ", p.relative_to(FIXTURE))


if __name__ == "__main__":
    main()
