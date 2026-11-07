---
name: new-campaign
description: Create a new D&D campaign (solo or Party Mode multiplayer) with Claude as DM - load the SRD 2024 rules, create the campaign and first character, copy in the starter templates, write the secret campaign arc, and choose how campaigns are saved and kept private. Use for "start a new campaign", "new solo game", "set up a party campaign", or "where are my campaigns saved / back them up".
---

# New campaign

Core rules: load the `dnd-dm:dm` skill first if it isn't loaded. Tool names below are bare; call them by their namespaced plugin names (`mcp__plugin_dnd-dm_dm20-protocol__...`, `mcp__plugin_dnd-dm_d20-mcp__...`). `<data dir>` is the project's D&D data dir (printed at session start; default `<project>/dnd`).

## Rules Edition

Campaigns standardize on the **SRD 2024** ruleset (`rules_version="2024"` at `create_campaign`, then `load_rulebook(source="srd", version="2024")`), plus the 4 custom overlays in `${CLAUDE_PLUGIN_ROOT}/templates/rulebooks/custom/`, which fill gaps and correct the SRD API data. dm20-protocol supports both 2014 and 2024; every campaign here uses 2024.

## Campaign Creation Workflow

1. Confirm `d20-mcp` and `dm20-protocol` are both connected (`claude mcp list`, or a live tool call to each).
2. `load_rulebook(source="srd", version="2024")` (the version defaults to 2014).
3. `create_campaign(name=..., description=..., rules_version="2024")` — ask the player(s) for name/setting/tone rather than assuming.
4. Copy the starter files from `${CLAUDE_PLUGIN_ROOT}/templates/` into `<data dir>/campaigns/<name>/`:
   - `templates/rulebooks/custom/*.json` → `campaigns/<name>/rulebooks/custom/`, then load them (order: species_corrections → class_progression → feats → spells; see the `dnd-dm:session-start` skill).
   - Party Mode: everything in `templates/party-campaign/`. Solo: `templates/solo-campaign/CLAUDE.md`.
   - Both: `templates/ENCOUNTER_LOG.md`, `templates/PLAYER_FEEDBACK.md`, `templates/CAMPAIGN_ARC.md`, `templates/setting.md`. Fill in the names, and fill `setting.md` with the player(s): tone, guardrails, world, each PC's hooks.
5. `create_character(...)` — ask for species, class, and background before calling. Use `d20-mcp` for any ability-score or creation rolls (e.g. `4d6kh3` × 6 if the player wants rolled stats). **`create_character` isn't yet verified against 2024:** pass ability scores as `manual` with explicit values and hand-verify scores, Speed, HP and AC against `SRD_2024_PLAYER_OPTIONS.md` (lookup order in the `dnd-dm:rules` skill). `armor_class` is never computed from DEX (it's whatever you pass, default 10).
6. **Write the campaign arc before session 1.** Fill in every section of `CAMPAIGN_ARC.md`: the hidden truth, the layers the party uncovers in order, the cast (want, flaw, secret), the session-by-session menu with several doors into each beat, the clock that advances when the party doesn't interfere, the planned close of each chapter, and at least three endings. Build it from `setting.md` and each PC's backstory hooks, sized to the level range the table expects. Without it, play drifts into wandering around and asking questions, so don't start session 1 until it's written. If the player wants to be surprised, write it without showing them and just say it's done.
7. If `git config dnd.campaignStorage` is unset, walk the player through "Saving Campaigns" (`${CLAUDE_SKILL_DIR}/saving-campaigns.md`) before the first session.

**At every session start**, if `CAMPAIGN_ARC.md` is missing, still has template placeholders (`<...>`, `_(...)_`), or has empty sections, write it per step 6 before narrating anything. This catches campaigns that skipped it. (`dnd-dm:session-start` repeats this check.)

## Saving Campaigns

Read `${CLAUDE_SKILL_DIR}/saving-campaigns.md` and follow it: it covers the separate private repo, keeping campaigns in the project's own repo, and the public option, and writes the data dir's `.gitignore`. The plugin's guard hook asks for approval before campaign data is pushed to a public repo.
