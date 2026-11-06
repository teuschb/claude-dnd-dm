---
name: claude-dnd-dm
description: Run D&D 5e (SRD 2024) campaigns with Claude Code as the Dungeon Master, solo in chat or multiplayer in Party Mode. SRD-only rules content; no Player's Handbook or Monster Manual content beyond SRD 5.2.
---

# claude-dnd-dm

A setup for running D&D 5e (SRD 2024) with **Claude Code as the Dungeon Master**: solo in chat, or multiplayer with players joining from their phones.

Nothing here is a program you run directly. It is a folder of instructions, rules references and hooks that Claude Code reads, plus two MCP servers that give it real game state and real dice:

- **dm20-protocol** (fork of [BNDYH/dm20-protocol](https://github.com/BNDYH/dm20-protocol), in this repo's `.mcp.json` as `teuschb/dm20-protocol`): campaigns, characters, combat, quests, rulebook lookup, and **Party Mode**, a small web server where each player gets a private link, posts what their character does, and reads the DM's narration.
- **d20-mcp** ([saidsurucu/d20-mcp](https://github.com/saidsurucu/d20-mcp)): the only source of dice rolls, so every roll is real and auditable.

## Scope: SRD-only

Everything in this repo is either original work or material from the System Reference Document 5.2 (SRD 5.2), used under Creative Commons Attribution 4.0. That means, in the SRD's own terms:

- **Included:** 9 species, 12 classes with 1 subclass each, 4 backgrounds, 17 feats, 339 spells, 341 monsters, 262 magic items. See `AUDIT.md` for the exact verified counts.
- **Not included:** Player's Handbook or Monster Manual content beyond SRD 5.2. No additional subclasses, backgrounds, feats, or spells from the full PHB, and no Product Identity monsters or items beyond the SRD. If a creature, spell, feat, or item is not in SRD 5.2, it is not in this repo.

This work is not affiliated with, endorsed by, or sponsored by Wizards of the Coast LLC. "D&D" and "Dungeons & Dragons" are used here only descriptively to identify the game system the SRD covers.

## Setup

1. Install [Claude Code](https://claude.com/claude-code) and [uv](https://docs.astral.sh/uv/) (`brew install uv`); both MCP servers run through `uvx`.
2. Clone this repo and open Claude Code in it. Approve the two project MCP servers when prompted (`claude mcp list` should show both connected).
3. Ask Claude to start a campaign, e.g. *"Let's start a new solo D&D campaign."* It will follow "Campaign Creation Workflow" in `rpg/dnd/CLAUDE.md`: load the SRD 2024 rules, create the campaign, copy in the templates, build your character with you, and ask how you want campaigns saved (see "Saving your campaigns" in `README.md`).

## How it works

- `rpg/CLAUDE.md`: ground rules for any RPG (dice are never invented, the player drives, pause often).
- `rpg/dnd/CLAUDE.md`: the D&D setup: MCP servers, session start/stop, Party Mode technique, rulebook loading.
- `rpg/dnd/DM_CORE.md`: DM rules for a solo campaign.
- `rpg/dnd/templates/party-campaign/DM_LOOP.md`: DM rules for a multiplayer campaign: lead with what the player did, state positions in combat, pause for reactions, public vs private messages, pacing, difficulty. Each rule in it came from something that actually went wrong at a real table.
- `rpg/dnd/scripts/hooks/`: Claude Code hooks (wired in `.claude/settings.json`). One asks before campaign data goes to a public repo. The others block a Party Mode message before it's sent if it breaks the checklist, e.g. it doesn't open with the acting player's action, uses banned jargon, shows a DC, or leaves out the combat position list.
- `rpg/dnd/SRD_2024_*.md` + `rpg/dnd/rulebook_cache/srd_2024/`: SRD-only rules references and a cached copy of the SRD 5.2 data, so lookups work offline.
- `rpg/dnd/templates/`: starter files for a new campaign (SRD-only rulebook overlays, encounter log, feedback ledger, secret arc, setting).

## Playing

- **Solo:** just play in the chat. Each session, Claude reloads the campaign and rulebooks (`templates/solo-campaign/CLAUDE.md` has the one-minute start).
- **Multiplayer (Party Mode):** Claude runs `start_party_mode`, which prints a private link (and QR code) per player. Players on your Wi-Fi can use them directly; for phones elsewhere, expose port 8080 (e.g. `tailscale funnel --bg 8080`). Then tell Claude *"check now"* or *"watch for 2 hours"*, and it answers posts as they arrive.

Party Mode only runs while your Claude Code session is open, so it suits play-by-post in bursts: sessions over an evening or a few days, not an always-on server.

## What is included

- The DM workflow and narration rules (`DM_CORE.md`, `DM_LOOP.md`, `IMPROV_TOOLKIT.md`)
- Campaign starter templates (`CAMPAIGN_ARC.md`, `ENCOUNTER_LOG.md`, `PLAYER_FEEDBACK.md`, `setting.md`)
- Three narration/privacy hooks in `rpg/dnd/scripts/hooks/`
- SRD-only reference files and the SRD 5.2 cache in `rpg/dnd/rulebook_cache/srd_2024/`
- MCP server configuration in `.mcp.json` (dm20-protocol fork, d20-mcp)

## Attribution

This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.

The original DM workflow, templates, and hooks in this repo are Ben Teusch's own work, licensed under the MIT License (see `LICENSE`).
