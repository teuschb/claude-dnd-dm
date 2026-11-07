# SRD scope check — Nov 5, 2026 (paths updated for the plugin layout)

**Plugin layout note.** Since the repo was restructured as a Claude Code plugin marketplace, the files audited below moved without content changes: `rpg/dnd/SRD_2024_*.md` → `plugin/reference/`, `rpg/dnd/rulebook_cache/` → `plugin/rulebook_cache/`, `rpg/dnd/templates/` → `plugin/templates/`. The counts below were re-derived from the moved files (see the verification block at the end of this file); no rules content was added in the restructure.

**This is a scope check, not legal advice.** It records what was verified, by script, when the public SRD-only version of claude-dnd-dm was built from the original repo (https://github.com/teuschb/claude-dnd-dm, commit cc18b53). It is not a legal opinion and does not guarantee that no issue remains; see "What was NOT verified" below.

## Source of truth for SRD scope

The repo's own SRD source, `plugin/rulebook_cache/srd_2024/` (data from dnd5eapi.co `/api/2024`, the System Reference Document 5.2), was treated as the SRD 5.2 allowlist. Anything not in that cache was treated as non-SRD and removed, unless it was original work (DM instructions, templates, hooks).

## Verified counts in this public version

| Item | Count | How verified |
|---|---|---|
| Monsters in `SRD_2024_MONSTERS.md` (`###` headings) | 341 | Generated from the 341 `monsters_*.json` cache files; heading count checked by script |
| Magic items in `SRD_2024_MAGIC_ITEMS.md` (`###` headings) | 262 | Generated from the 262 `magic-items_*.json` cache files; heading count checked by script |
| Species in `SRD_2024_PLAYER_OPTIONS.md` | 9 | Dragonborn, Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling (cache `species.json`) |
| Classes | 12 | Trimmed class-progression overlay, all 12 kept |
| Subclasses | 12 | Berserker, Lore, Life, Land, Champion, Open Hand, Devotion, Hunter, Thief, Draconic, Fiend, Evoker (cache `subclasses_*.json`) |
| Backgrounds | 4 | Acolyte, Criminal, Sage, Soldier (cache `backgrounds.json`); no background overlay file ships |
| Feats in `srd_2024_feats.json` | 17 | Trimmed from 75 to the 17 in cache `feats.json` |
| Spells in `srd_2024_spells.json` | 339 | See "Spells" below; count checked by script |
| JSON files in the tree that parse | 1,575 of 1,575 | `python json.load` over every `*.json` in the tree, 0 failures |
| Images / PDFs / `.git` / `campaigns/` / `events/` | None | `find` check, 0 hits |

## What was removed or replaced

- `plugin/reference/SRD_2024_MONSTERS.md` (old: 489 monsters, 176 not in the SRD cache, including full Mind Flayer / Mind Flayer Arcanist / Death Tyrant stat blocks; footer admitted transcribing "All 202 pages of the SRD 2024 Monster Manual" from aidedd.org) — **deleted and regenerated from the SRD cache: 341 monsters.**
- `plugin/reference/SRD_2024_MAGIC_ITEMS.md` (old: 311 items including Wand of Orcus, Deck of Many Things, Orb of Dragonkind, Blackrazor, Book of Exalted Deeds / Vile Darkness, Hand of Vecna) — **deleted and regenerated from the SRD cache: 262 items, using SRD names Mysterious Deck and Dragon Orb.**
- `plugin/reference/SRD_2024_PLAYER_OPTIONS.md` (old: 48 subclasses, full PHB class text) — **deleted and regenerated from the SRD cache plus the trimmed overlays: 9 species, 12 classes, 12 subclasses, 4 backgrounds, 17 feats.** No text was copied from the old file for non-SRD subclasses.
- `plugin/templates/rulebooks/custom/srd_2024_background_additions.json` (12 PHB backgrounds; the file itself said "not in the free SRD") — **deleted entirely.** The overlay load order in the session-start procedure (now the `dnd-dm:session-start` skill) and in `plugin/templates/solo-campaign/CLAUDE.md` was updated to species_corrections → class_progression → feats → spells.
- `srd_2024_feats.json` — trimmed 75 → 17 (the SRD feats only).
- `srd_2024_class_progression.json` — trimmed 48 → 12 subclasses. The generic subclass-choice feature text in the original overlay listed all four PHB subclasses per class; that text was replaced with the single SRD subclass per class, so no non-SRD subclass names remain in the overlay or in the generated player file.
- `srd_2024_spells.json` — trimmed to 339 SRD spells. See "Spells" below.
- `srd_2024_species_corrections.json` (Goliath & Orc) — **kept unchanged**; both species are in SRD 5.2.

## Spells — how the 339 were reached

The old overlay had 354 spells. Matching it against the 339-spell SRD cache:

- 314 spells matched the SRD cache by exact name, or by a naming variant where the SRD uses a generic name and the PHB overlay used a named one. Those 9 variants were kept with the SRD canonical name and index: Melf's Acid Arrow → Acid Arrow; Tasha's Hideous Laughter → Hideous Laughter; Tenser's Floating Disk → Floating Disk; Nystul's Magic Aura → Arcanist's Magic Aura; Leomund's Tiny Hut → Tiny Hut; Evard's Black Tentacles → Black Tentacles; Bigby's Hand → Arcane Hand; Mordenkainen's Magnificent Mansion → Magnificent Mansion; Mordenkainen's Sword → Arcane Sword.
- 25 SRD spells were missing from the old overlay entirely and were built from the SRD cache JSON (level, school, casting time, range, duration, components, description, classes).
- 40 PHB-only spells were dropped: Blade Ward, Friends, Mind Sliver, Thorn Whip, Thunderclap, Toll the Dead, Word of Radiance, Armor of Agathys, Arms of Hadar, Compelled Duel, Hail of Thorns, Thunderous Smite, Witch Bolt, Wrathful Smite, Arcane Vigor, Beast Sense, Cloud of Daggers, Cordon of Arrows, Crown of Madness, Summon Beast, Aura of Vitality, Blinding Smite, Conjure Barrage, Crusader's Mantle, Elemental Weapon, Feign Death, Hunger of Hadar, Lightning Arrow, Summon Fey, Summon Undead, Aura of Purity, Fount of Moonlight, Grasping Vine, Staggering Smite, Banishing Smite, Circle of Power, Conjure Volley, Destructive Wave, Steel Wind Strike, Swift Quiver.

314 + 25 = 339. The dropped spells appear nowhere as spell entries in this tree.

## Forbidden-term grep

A case-insensitive grep of the whole tree (excluding `.git`, which does not ship) for: beholder, mind flayer, illithid, "wand of orcus", "deck of many things", "orb of dragonkind", blackrazor, "forgotten realms", "dragon delves", "death at sunset", aasimar, artificer, strahd, tiamat.

Remaining hits, and why each is there:

1. **"Tiamat" — 3 lines, all inside the SRD Dragon Orb entry.** Two lines are in the generated `SRD_2024_MAGIC_ITEMS.md` Dragon Orb description and one is in the source cache file `magic-items_dragon-orb.json`. This is SRD 5.2's own text for that item, as returned by the official SRD API ("advance the worship of Tiamat", "Dragon deities such as Tiamat are unaffected"). It was not added from any PHB or Monster Manual source, and the item itself (Dragon Orb) is in SRD 5.2. Kept deliberately, as removing SRD text would make the entry inaccurate.
2. **Name-only mentions in this file and in `README.md`'s "Not included" list** (e.g. Beholder, Mind Flayer, Wand of Orcus) — names only, with no stat block, description, or mechanics. They exist so a reader can see what was deliberately excluded.
3. **No other hits.** In particular, there are no hits for illithid, blackrazor, forgotten realms, dragon delves, death at sunset, aasimar, artificer, or strahd anywhere in the shipped tree outside this audit note and the README exclusion list.

Related false positives checked and cleared:

- "Assassin" appears in the SRD cache as the SRD monster *Assassin* and the SRD poison *Assassin's Blood*. That is SRD content, not the Rogue subclass of the same name, which is not in this tree.
- "Friends" appears only inside "Animal Friendship" (an SRD spell); "Thunderclap" appears only as a Bronze Dragon action name in SRD monster data; "Grasping Vine" appears only as descriptive wording inside the SRD spell Ensnaring Strike. None of the three is a spell entry in this tree.
- Non-SRD subclass names (e.g. Path of the Wild Heart, College of Dance, Circle of the Moon, Battle Master, Oath of Vengeance, Soulknife, Abjurer) appear nowhere in this tree after the subclass-choice sanitization described above.

## What was NOT verified

- **No legal review.** This check is mechanical (counts, allowlist matching, grep). It does not establish that every word of SRD-derived text is correctly attributed, or that paraphrased class-feature text in the trimmed overlays is free of PHB wording. A lawyer, or a careful line-by-line read of the trimmed overlays against the SRD PDF, would be the next step before a paid listing.
- **No live play test.** The MCP servers, Party Mode web server, and hooks were not run end to end in this build; the build only verified files, JSON validity, and counts. The DM workflow files were copied verbatim from the original, so a live test on the original author's machine is still the right final check.
- **Source-data quirks carried over as-is.** The SRD API's magic-item descriptions flatten tables into running text (the Mysterious Deck entry is the worst case: its card table arrives as a single run-on block). That is a limitation of the source data, not added content, and was left as-is rather than rewritten by hand.
- **Attribution.** SRD 5.2 CC-BY attribution is included in `README.md`, `LICENSE` (attribution section), and in the header of each generated `SRD_2024_*.md` file.

## Re-verification after the plugin restructure

Counts re-derived from the files at their new paths (`plugin/reference/`, `plugin/templates/rulebooks/custom/`, `plugin/rulebook_cache/srd_2024/`):

- Monsters (`###` headings in `SRD_2024_MONSTERS.md`): 341
- Magic items (`###` headings in `SRD_2024_MAGIC_ITEMS.md`): 262
- Spells in `srd_2024_spells.json`: 339
- Feats in `srd_2024_feats.json`: 17
- Subclasses / species / backgrounds in the cache: 12 / 9 / 4

The per-file diff of every moved file against the pre-restructure commit is empty (git detected them as pure renames).
