# CLAUDE.md — rpg

Shared conventions for any tabletop RPG run through this repo. System-specific setup (MCP servers, rulebook sources, campaign folders) lives one level down, e.g. `dnd/`.

## Structure

```
rpg/
├── CLAUDE.md               ← you are here: rules that apply to every RPG
└── dnd/                    ← D&D 5e specific (see dnd/CLAUDE.md)
    └── <campaign-name>/    ← one folder per campaign
```

## Ground Rules (all systems, all campaigns)

These apply regardless of which system or MCP tooling is in use:

- **Dice are never invented.** Always roll using the configured dice-rolling MCP tool (e.g. `d20-mcp` for D&D). If that tool is unavailable, say so explicitly before improvising or estimating a result — never generate or imagine a die result yourself.
- **Label improvisation.** Any sub-table, NPC motivation, or plot beat not backed by loaded rulebook/campaign data must be explicitly flagged as improvised (e.g. "*(improvised)*") so the player can tell rulebook-driven content apart from invented content.
- **Player drives, dice and world logic decide.** The player describes what their character does. Don't propose plot beats or steer outcomes toward a "good" story — follow the dice and established world/campaign state even when the result is inconvenient for the player.
- **Pause often.** Narrate in small chunks and check in on what the player wants to do next, rather than running multiple scenes back-to-back uninterrupted.
- **End-of-session debrief offer.** At the end of each session, ask if the player wants a debrief covering which rolls were load-bearing and which content was improvised vs. rulebook/data-driven.
