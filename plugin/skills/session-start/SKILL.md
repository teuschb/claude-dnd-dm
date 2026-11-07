---
name: session-start
description: Start or resume a D&D session, solo or Party Mode - load the campaign, reload the SRD rulebooks and overlays (they do not persist across sessions), read game state and the secret campaign arc, check player feedback. Use for "let's play", "continue the campaign", "resume session", "start session N", or before narrating anything in an existing campaign.
---

# Session start

Core rules: load `dnd-dm:dm` first if it isn't loaded. Tool names are bare; call them by their namespaced plugin names. Campaign folders are under the data dir (`<data dir>/campaigns/<campaign>/`).

## Common steps (solo and party)

1. `load_campaign(name="<campaign>")`.
2. **Reload rulebooks — they do NOT persist across sessions.** `load_campaign` does not reload a campaign's rulebooks from `rulebooks/manifest.json`. Every session re-runs `load_rulebook` for the SRD base and each overlay before relying on `get_class_info`, `get_race_info` or `search_rules`. In this order:
   1. `load_rulebook(source="srd", version="2024")`
   2. `load_rulebook(source="custom", path="custom/srd_2024_species_corrections.json")`
   3. `load_rulebook(source="custom", path="custom/srd_2024_class_progression.json")`
   4. `load_rulebook(source="custom", path="custom/srd_2024_feats.json")`
   5. `load_rulebook(source="custom", path="custom/srd_2024_spells.json")`

   (The overlays live in `campaigns/<campaign>/rulebooks/custom/`; any campaign-specific overlays there load after these.) Later sources win, so the overlays override the SRD base. `load_rulebook(source="srd", version="2024")` reads `rulebook_cache/srd_2024/` in the data dir (species grant no ability bonuses). Loading a rulebook rewrites `rulebooks/manifest.json`; that file is only a record — if the campaign has its own private repo, don't commit the churn if it only lost/gained overlay entries.
3. `get_game_state` and read the campaign's `CAMPAIGN_ARC.md` before narrating anything. If it's missing, still has template placeholders (`<...>`, `_(...)_`), or has empty sections, write it first (the `dnd-dm:new-campaign` skill, Campaign Creation Workflow step 6). Then skim `PLAYER_FEEDBACK.md` open questions.
4. If `git config dnd.campaignStorage` is unset, walk the player through "Saving Campaigns" (`dnd-dm:new-campaign`) before the first session.

`get_class_info` doesn't render feature text (a rendering bug; `get_race_info` is fine). Use `SRD_2024_PLAYER_OPTIONS.md` for class and subclass features (see the `dnd-dm:rules` skill for where it lives).

## Solo branch (about one minute)

After the common steps: no `start_party_mode`, no Tailscale funnel, no Monitor or `/loop` — just play in chat. Read the solo rules: `${CLAUDE_PLUGIN_ROOT}/skills/dm/DM_CORE.md` and the campaign's own `CLAUDE.md` (copied from `${CLAUDE_PLUGIN_ROOT}/templates/solo-campaign/CLAUDE.md`). At the end follow the `dnd-dm:session-end` skill.

## Party branch

After the common steps (1, 2 and 3 above), continue with the `dnd-dm:party-mode` skill's Start section (`start_party_mode`, tunnel, Monitor), and read the campaign's `DM_LOOP.md` and `DM_LOOP_OPS.md` before resolving any action. The party start has the same steps as the old "Session Start / Stop Checklist": load campaign, reload rulebooks, start party mode, optional tunnel, arm the Monitor, read game state and the arc.
