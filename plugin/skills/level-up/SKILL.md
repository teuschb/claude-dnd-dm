---
name: level-up
description: Level up D&D characters with milestone leveling and hand-verify the result against the SRD 2024 player options (HP, features, spell slots, ability scores). Use for "level up", "milestone level", "new level", or after any level_up_character call.
---

# Level up

Core rules: load `dnd-dm:dm` first if it isn't loaded. Tool names are bare; call them by their namespaced plugin names.

## Milestone (default; the campaign may override)

- Milestone, not XP; no per-encounter XP. Early on (about levels 1–3) level every PC one step at the end of every session; after that, level less often (roughly one step per completed arc/mission, ~2 arcs per level from level 5). Call the session end yourself at a natural stopping point.
- Level via `level_up_character` (`bulk_update_characters` for a whole party), hand-verify HP/features/slots, then re-set anything the tool can't (`update_character` extras).

## Hand-verify

`level_up_character` / `create_character` output must be hand-verified against `SRD_2024_PLAYER_OPTIONS.md` (HP, features, slots, ability scores, Speed, AC). Where that file lives: the `dnd-dm:rules` skill (lookup order; usually `${CLAUDE_PLUGIN_ROOT}/reference/SRD_2024_PLAYER_OPTIONS.md`). `get_class_info` doesn't render feature text, so don't rely on it for features.

## Writing the picks to the sheet

- Write each pick to the sheet immediately with `update_character` (`subclass`, `add_features`, `spell_slots`). Never `add_features_and_traits` (it writes a legacy list that's invisible once a character has structured features), never a raw file edit. For hand edits when no tool can make a change: stop and say so; the only safe hand-edit is after `stop_party_mode` / a full MCP restart, then reload.
- **Party Mode:** broadcast the level-up recap once; picks go per-player, one item at a time, in private.
- Limited-use features live on the sheet: new one via `update_character add_features '[{"name": ..., "uses_max": N, "recharge": "short"|"long"}]'`; add `"short_rest_regain": 1` for one-back-per-short-rest features (Second Wind). Spend with `use_feature`; rests restore them.
