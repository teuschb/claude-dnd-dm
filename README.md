# claude-dnd-dm

A setup for running D&D 5e (SRD 2024) with **Claude Code as the Dungeon Master**: solo in chat, or multiplayer with players joining from their phones.

Nothing here is a program you run directly. It's a folder of instructions, rules references and hooks that Claude Code reads, plus two MCP servers that give it real game state and real dice:

- **[dm20-protocol](https://github.com/teuschb/dm20-protocol)** (fork of [BNDYH/dm20-protocol](https://github.com/BNDYH/dm20-protocol)): campaigns, characters, combat, quests, rulebook lookup, and **Party Mode**, a small web server where each player gets a private link, posts what their character does, and reads the DM's narration.
- **[d20-mcp](https://github.com/saidsurucu/d20-mcp)**: the only source of dice rolls, so every roll is real and auditable.

## How it works

- `rpg/CLAUDE.md`: ground rules for any RPG (dice are never invented, the player drives, pause often).
- `rpg/dnd/CLAUDE.md`: the D&D setup: MCP servers, session start/stop, Party Mode technique, rulebook loading.
- `rpg/dnd/DM_CORE.md`: DM rules for a solo campaign.
- `rpg/dnd/templates/party-campaign/DM_LOOP.md`: DM rules for a multiplayer campaign: lead with what the player did, state positions in combat, pause for reactions, public vs private messages, pacing, difficulty. Each rule in it came from something that actually went wrong at a real table.
- `rpg/dnd/scripts/hooks/`: Claude Code hooks (wired in `.claude/settings.json`). One keeps campaign data out of public repos (below). The others block a Party Mode message before it's sent if it breaks the checklist, e.g. it doesn't open with the acting player's action, uses banned jargon, shows a DC, or leaves out the combat position list.
- `rpg/dnd/SRD_2024_*.md` + `rpg/dnd/rulebook_cache/srd_2024/`: rules references and a cached copy of the SRD 2024 data, so lookups work offline.
- `rpg/dnd/templates/`: starter files for a new campaign (rulebook overlays that fix gaps in the SRD data, encounter log, feedback ledger, secret arc, setting).

## Setup

1. Install [Claude Code](https://claude.com/claude-code) and [uv](https://docs.astral.sh/uv/) (`brew install uv`); both MCP servers run through `uvx`.
2. Clone this repo and open Claude Code in it. Approve the two project MCP servers when prompted (`claude mcp list` should show both connected).
3. Ask Claude to start a campaign, e.g. *"Let's start a new solo D&D campaign."* It will follow "Campaign Creation Workflow" in `rpg/dnd/CLAUDE.md`: load the SRD 2024 rules, create the campaign, copy in the templates, and build your character with you.

## Your campaigns stay private

This repo is public, so **your campaign never goes in it.** Everything Claude creates for a campaign (characters, the DM's secret arc, session notes) lands in `rpg/dnd/campaigns/<name>/`, which is gitignored here. Committing or pushing this repo, or a fork of it, can't publish your game.

- By default a campaign lives only on your machine.
- To keep it in git (backup, history, another computer), ask Claude to save it. It turns the campaign folder into its own **private** GitHub repo, separate from this one, with the player-link secrets left out.
- A Claude Code hook (`rpg/dnd/scripts/hooks/guard_campaign_privacy.py`) blocks Claude from force-adding campaign files here, creating a public campaign repo, or pushing while a campaign's repo is public.

## Playing

- **Solo:** just play in the chat. Each session, Claude reloads the campaign and rulebooks (`templates/solo-campaign/CLAUDE.md` has the one-minute start).
- **Multiplayer (Party Mode):** Claude runs `start_party_mode`, which prints a private link (and QR code) per player. Players on your Wi-Fi can use them directly; for phones elsewhere, expose port 8080 (e.g. `tailscale funnel --bg 8080`). Then tell Claude *"check now"* or *"watch for 2 hours"*, and it answers posts as they arrive. Players can turn on notifications with the bell button.

Party Mode only runs while your Claude Code session is open, so it suits play-by-post in bursts: sessions over an evening or a few days, not an always-on server. Running the watch loop from a fresh session keeps usage down (every wake-up resends the whole conversation).

## Layout

```
.mcp.json                 MCP servers (dm20-protocol pinned to a commit, d20-mcp)
.claude/settings.json     the narration hooks
rpg/
  CLAUDE.md               ground rules for every RPG
  dnd/
    CLAUDE.md             D&D setup and Party Mode
    AGENTS.md             condensed version for other agents
    DM_CORE.md            solo DM rules
    SRD_2024_*.md         rules references
    scripts/hooks/        narration checks
    templates/            new-campaign starter files
    campaigns/            your campaigns land here (gitignored; each can be its own private repo)
    rulebook_cache/       cached SRD 2024 data
```

## Credits and licenses

- dm20-protocol is MIT-licensed; this setup uses a fork with Party Mode fixes.
- This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.
