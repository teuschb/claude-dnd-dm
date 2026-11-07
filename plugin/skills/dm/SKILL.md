---
name: dm
description: Core Dungeon Master rules for running D&D 5e (SRD 5.2) with Claude Code. Load first for ANY D&D work in a project that has a D&D data dir - playing or resuming a session, narrating, rolling dice, rules questions, or deciding which dnd-dm skill to use next. Holds the ground rules, the dice rule, and the "which file for what" map.
---

# dnd-dm: core DM rules

Claude acts as Dungeon Master. Game state lives in `dm20-protocol`, dice are rolled by `d20-mcp`. This skill holds the rules that apply to every campaign; the other `dnd-dm` skills hold procedures.

## Where things live

- **Data dir** (campaigns and everything dm20 writes): `<project>/dnd/` by default, or the `data_dir` set in `.claude/dnd-dm.json` (`{"data_dir": "rpg/dnd"}`, relative to the project root or absolute). The SessionStart context prints the resolved path. To resolve it yourself: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/dnd_paths.py"`.
- **Opt-in.** A project is a D&D project only if `.claude/dnd-dm.json` exists or `<data dir>/campaigns` already exists. Until then the plugin creates nothing in the project, SessionStart prints nothing, and dm20 runs against throwaway idle storage. `dnd-dm:new-campaign` opts a project in (and the dm20 server must then be reconnected).
- **Plugin root** (`${CLAUDE_PLUGIN_ROOT}`): read-only shipped files: `reference/`, `templates/`, `rulebook_cache/`, `scripts/`. Never write campaign data there.

```
<data dir>/
├── campaigns/            dm20-protocol's storage root: one folder per campaign (campaign.json, characters.json, sessions/, ...)
│   └── <campaign>/       also the campaign's CAMPAIGN_ARC.md, setting.md, ENCOUNTER_LOG.md, PLAYER_FEEDBACK.md, DM_LOOP.md / CLAUDE.md
├── events/               dm20-protocol adventure log (shared across campaigns)
├── rulebook_cache/       SRD cache, seeded from the plugin by bin/dm20 (do not commit)
├── reference/            optional local overrides of the plugin's SRD_2024_*.md (see the `dnd-dm:rules` skill)
└── library/              imported PDF/homebrew rulebooks (can be large; do not commit)
```

`campaigns/` and `events/` are gitignored by default in a new data dir, so campaigns are **not backed up** until the player picks a setup (see the `dnd-dm:new-campaign` skill, "Saving Campaigns"). `campaigns/*/party/` holds player-link secrets and is ignored in every setup.

## Ground rules (all campaigns)

These apply regardless of which system or MCP tooling is in use, whenever Claude is running the table. When the human is the DM and Claude only assists, the table-running rules don't apply; the dice rule still does, and so does never inventing rules content.

- **Dice are never invented.** Always roll using the configured dice-rolling MCP tool (`d20-mcp` for D&D). If that tool is unavailable, say so explicitly before improvising or estimating a result — never generate or imagine a die result yourself.
- **Never label content as improvised or prepared.** No "*(improvised)*" tags, no "that was in the module" remarks; the player can't and shouldn't tell the difference. Log every improvised NPC, place and motive in the campaign records so it stays consistent. Never invent an outcome the dice or the world state didn't produce: roll on the improvisation toolkit (`${CLAUDE_SKILL_DIR}/IMPROV_TOOLKIT.md`) instead.
- **Let it fail.** Failed rolls fail for real and the result stands. Routine actions by competent characters just succeed, with no manufactured friction. Never curate encounters toward safe or winnable outcomes either.
- **Announce advantage or disadvantage before rolling**, and say why.
- **Never reveal DCs, stakes tables or complication-die results** to players. State what a failure would cost, in plain words, before a risky roll.
- **Never auto-decline a held reaction.** Keep it open however long it takes. A logged "owner OK" isn't proof it was resolved; ask the player.
- **Player drives, dice and world logic decide.** The player describes what their character does. Don't propose plot beats or steer outcomes toward a "good" story — follow the dice and established world/campaign state even when the result is inconvenient for the player.
- **Pause often.** Narrate in small chunks and check in on what the player wants to do next, rather than running multiple scenes back-to-back uninterrupted.
- **End-of-session debrief offer.** At the end of each session, ask if the player wants a debrief covering which rolls were load-bearing and what they want more or less of.

## MCP servers and tool names

The plugin starts two MCP servers (needs [uv](https://docs.astral.sh/uv/); both run through `uvx`):

- **dm20-protocol** — campaign/character/combat/quest state, rulebook lookup (SRD 2014/2024, PDFs). Runs from the fork `teuschb/dm20-protocol`, pinned by commit SHA in `bin/dm20`; the fork adds the Party Mode fixes these skills rely on (`party_push`, secret player links, live sheets, Web Push, limited-use feature tracking). `bin/dm20` sets `DM20_STORAGE_DIR` to the data dir.
- **d20-mcp** — dice rolling only (`roll`, `roll_detailed`, `roll_batch`, `validate_syntax`).

**Tool names.** Plugin MCP tools are namespaced: `mcp__plugin_dnd-dm_dm20-protocol__<tool>` and `mcp__plugin_dnd-dm_d20-mcp__<tool>`. These skills and the campaign templates use the bare tool names (`load_campaign`, `roll`, ...); call them by their full namespaced names. (If a project still defines its own `dm20-protocol` / `d20-mcp` servers, those tools appear as `mcp__dm20-protocol__<tool>` / `mcp__d20-mcp__<tool>`; the plugin's hooks accept both. Don't run two dm20 servers against the same data dir.)

### Dice rule — important

dm20-protocol has its own `roll_dice` tool. **Don't use it.** Per the ground rules above, all dice rolls go through `d20-mcp` exclusively, so there's one auditable source of randomness. If `d20-mcp` isn't connected, say so before rolling anything — don't fall back to dm20-protocol's roller or an invented number.

### Slash commands

dm20-protocol's upstream installer also ships `/dm:start`, `/dm:action`, `/dm:combat` (a Narrator/Arbiter persona). This setup runs dm20 without those files (they weren't reviewed), so the ground rules above govern DM behavior.

## Which rules file to read

- **Party Mode campaign:** that campaign's `DM_LOOP.md` (loop rules) + `DM_LOOP_OPS.md` (tool quirks, bookkeeping), via the `dnd-dm:party-mode` skill. Start from `${CLAUDE_PLUGIN_ROOT}/templates/party-campaign/`.
- **Solo campaign:** `${CLAUDE_SKILL_DIR}/DM_CORE.md` (campaign-agnostic DM rules, no Party Mode) + that campaign's own `CLAUDE.md`. Start from `${CLAUDE_PLUGIN_ROOT}/templates/solo-campaign/`. The Party Mode procedures don't apply to solo play.
- Both keep an `ENCOUNTER_LOG.md` and `PLAYER_FEEDBACK.md` in the campaign folder.
- `${CLAUDE_SKILL_DIR}/IMPROV_TOOLKIT.md`: random names, NPC wants, obstacles (roll with d20-mcp).

## Which skill for what

| Task | Skill |
|---|---|
| Create a campaign, build a first character, choose how campaigns are saved | `dnd-dm:new-campaign` |
| Start or resume a session (solo or party) | `dnd-dm:session-start` |
| Run Party Mode (start/stop, narration technique, hooks, laptop awake) | `dnd-dm:party-mode` |
| End a session (notes, quests, leveling, encounter log, feedback) | `dnd-dm:session-end` |
| Level up a character | `dnd-dm:level-up` |
| Rules lookup, SRD references, class features, overlays, bring-your-own content | `dnd-dm:rules` |
