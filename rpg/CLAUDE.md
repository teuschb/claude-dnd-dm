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
- **Never label content as improvised or prepared.** No "*(improvised)*" tags, no "that was in the module" remarks; the player can't and shouldn't tell the difference. Log every improvised NPC, place and motive in the campaign records so it stays consistent. Never invent an outcome the dice or the world state didn't produce: roll on the improvisation toolkit (`dnd/IMPROV_TOOLKIT.md`) instead.
- **Let it fail.** Failed rolls fail for real and the result stands. Routine actions by competent characters just succeed, with no manufactured friction. Never curate encounters toward safe or winnable outcomes either.
- **Announce advantage or disadvantage before rolling**, and say why.
- **Never reveal DCs, stakes tables or complication-die results** to players. State what a failure would cost, in plain words, before a risky roll.
- **Never auto-decline a held reaction.** Keep it open however long it takes. A logged "owner OK" isn't proof it was resolved; ask the player.
- **Player drives, dice and world logic decide.** The player describes what their character does. Don't propose plot beats or steer outcomes toward a "good" story — follow the dice and established world/campaign state even when the result is inconvenient for the player.
- **Pause often.** Narrate in small chunks and check in on what the player wants to do next, rather than running multiple scenes back-to-back uninterrupted.
- **End-of-session debrief offer.** At the end of each session, ask if the player wants a debrief covering which rolls were load-bearing and what they want more or less of.
