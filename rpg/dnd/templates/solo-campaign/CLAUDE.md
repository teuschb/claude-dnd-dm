# CLAUDE.md — <Campaign Name>

Solo campaign (one PC, **no Party Mode**) on **SRD 2024** (`rules_version="2024"`).

**DM rules for this campaign: `../../DM_CORE.md`** (pacing, real difficulty, quest
craft, NPC prep, solo combat, leveling, session end). Also here:
`ENCOUNTER_LOG.md` (before/after-fight checklist + verdict log) and
`PLAYER_FEEDBACK.md` (ledger + check-in ritual). Never label content as
improvised or prepared (`rpg/CLAUDE.md`).

## Session start (solo — ~1 minute)
1. `load_campaign(name="<Campaign Name>")`.
2. Reload rulebooks (they do NOT persist across sessions). In this order:
   1. `load_rulebook(source="srd", version="2024")`
   2. `load_rulebook(source="custom", path="custom/srd_2024_species_corrections.json")`
   3. `load_rulebook(source="custom", path="custom/srd_2024_class_progression.json")`
   4. `load_rulebook(source="custom", path="custom/srd_2024_feats.json")`
   5. `load_rulebook(source="custom", path="custom/srd_2024_background_additions.json")`
   6. `load_rulebook(source="custom", path="custom/srd_2024_spells.json")`

   Later sources win, so the overlays override the SRD base. Loading a rulebook
   rewrites `rulebooks/manifest.json`; that file is only a record — if this
   campaign has its own private repo, don't commit the churn if it only
   lost/gained overlay entries.
3. `get_game_state`, then read `CAMPAIGN_ARC.md` (if it's missing or still has
   template placeholders, write it first; see "Campaign Creation Workflow" step 6
   in `../../CLAUDE.md`), then skim `PLAYER_FEEDBACK.md` open questions. No
   `start_party_mode`, no Tailscale funnel, no Monitor/`/loop` — just play in chat.
4. At the end follow DM_CORE "Session end" (session note, quests, encounter log,
   player feedback).

## Rules-data status

- `load_rulebook(source="srd", version="2024")` loads 2024 data from
  `rulebook_cache/srd_2024/`: 12 classes, 12 subclasses,
  9 species (Dwarf, Elf, Gnome, Goliath, Halfling, Human, Orc, Tiefling,
  Dragonborn), 24 subspecies, 339 spells, 341 monsters, 17 feats, 4 backgrounds,
  182 items.
- `update_character` sets `subclass`, `spell_slots` and structured `add_features`.

**Known gaps:**
- `get_class_info` doesn't render class-feature text (rendering bug). Use
  `../../SRD_2024_PLAYER_OPTIONS.md` (full levels 1–20 + subclasses, all 12 classes).
- `create_character` auto-population should now respect 2024 but is **unverified** —
  keep hand-verifying ability scores, features, speed and HP against
  `SRD_2024_PLAYER_OPTIONS.md` on the next new character.
- Rulebooks don't persist across sessions (step 2 above).
- The overlays in `rulebooks/custom/` are copies of `rpg/dnd/templates/rulebooks/custom/`;
  mirror any correction back to the template.

## Hidden plan
`CAMPAIGN_ARC.md` (DM-only, spoilers): the hidden truth, clocks/schedule, chapter closes, encounter sketches, leveling milestones. Written in full before session 1; read it at session start after `get_game_state`.

## Campaign notes
- Setting/tone: see `setting.md`. Current scene and any clocks live in
  `game_state.notes`.
