---
name: rules
description: D&D 5e rules lookup for the SRD 5.2 (2024) - spells, monsters, magic items, class and subclass features, species, feats, backgrounds - plus the lookup order (dm20 first, then local reference overrides, then the plugin's SRD reference files), custom rulebook overlays, and how to add your own private content to your own campaign. Use for any rules question, stat block, spell text or class feature lookup.
---

# Rules lookup

Rules content in this plugin is SRD 5.2 only. **Never invent rules content.** If something isn't found, say it isn't in the SRD sources available; don't fill it in from memory.

## Lookup order for any rules question

1. **dm20 lookup** — `get_spell_info`, `get_monster_info`, `get_race_info`, `search_rules`, `get_class_info` (needs the rulebooks loaded this session; see `dnd-dm:session-start`). Caveat: `get_class_info` doesn't render feature text.
2. **The data dir's `reference/<file>`**, if present (local overrides; same file names as below). This is where a player puts their own, locally generated reference files.
3. **The plugin's `reference/<file>`**: `${CLAUDE_PLUGIN_ROOT}/reference/`
   - `SRD_2024_PLAYER_OPTIONS.md` — species, classes (levels 1–20), subclasses, backgrounds, feats. Use it for class and subclass features; hand-verify `level_up_character` / `create_character` output against it.
   - `SRD_2024_MONSTERS.md` — 341 monsters (CR, stat blocks).
   - `SRD_2024_MAGIC_ITEMS.md` — 262 magic items.

   These are big files: search them (grep for the heading) instead of reading them whole.

Rules disputes at the table: restate the rule as written, citing `SRD_2024_PLAYER_OPTIONS.md`; make a quick ruling and keep play moving; revisit it privately after the scene. Never reverse a rolled result unless you misread the rules, and say so if you did.

## Edition and overlays

Campaigns use **SRD 2024** (`rules_version="2024"`, `load_rulebook(source="srd", version="2024")`) plus the 4 custom overlays in `${CLAUDE_PLUGIN_ROOT}/templates/rulebooks/custom/` (species_corrections, class_progression, feats, spells), which fill gaps and correct the SRD API data. Overlays load after the SRD base and win. Mirror any correction you make to a campaign's overlay copy back into your own template copy if you keep one.

**Rules-data status.** `load_rulebook(source="srd", version="2024")` loads 2024 data from `rulebook_cache/srd_2024/`: 12 classes, 12 subclasses, 9 species (Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling, Dragonborn), 24 subspecies, 339 spells, 341 monsters, 17 feats, 4 backgrounds, 182 items. `update_character` sets `subclass`, `spell_slots` and structured `add_features`.

`build_encounter_tool` uses 2014 DMG XP budgets; cross-check CR in `SRD_2024_MONSTERS.md`.

## Network access

`load_rulebook(source="srd")` calls out to the official SRD API (`dnd5eapi.co`). Remote/cloud/sandboxed Claude Code sessions (including phone/web access) may sit behind an outbound proxy that blocks that domain — a genuine 403, not a bug. A locally-installed session on a laptop has no such restriction.

The plugin ships the SRD 2024 cache and `bin/dm20` seeds it into the data dir's `rulebook_cache/srd_2024/`, so lookups already in the cache work offline. Do any new-content lookups from a laptop session; they are cached in the data dir. If `srd` is unreachable and there's no cache to fall back on, don't silently substitute `5etools` (broader, non-SRD, mixes 2014/2024 content) without saying so — ask first.

## Bring your own content (private use only)

A player who owns other books can add content to **their own** campaign through custom overlays. The plugin itself ships none of it. This content is for the player's private use: it must not be committed to a public repo or shared.

- Format: a JSON file in `<data dir>/campaigns/<campaign>/rulebooks/custom/`, laid out like the shipped overlays in `${CLAUDE_PLUGIN_ROOT}/templates/rulebooks/custom/` (look at `srd_2024_feats.json` and `srd_2024_spells.json` for the shape of entries). Load it after the SRD base and the shipped overlays: `load_rulebook(source="custom", path="custom/<file>.json")`. Like every rulebook, it must be reloaded each session.
- For lookups beyond the overlay JSON, a player can put their own reference markdown at `<data dir>/reference/` using the same file names as the plugin's (`SRD_2024_MONSTERS.md`, ...); it is read before the plugin's copy.
- Keep it private: the data dir's `.gitignore` ignores `library/` and `rulebook_cache/`; put private overlays in a campaign that is in a private repo or ignored (see "Saving Campaigns" in `dnd-dm:new-campaign`).
