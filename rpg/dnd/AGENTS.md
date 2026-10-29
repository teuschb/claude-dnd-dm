# rpg/dnd — Agent Instructions

D&D 5e campaigns, solo and Party Mode. The agent acts as Dungeon Master; state lives in `dm20-protocol`, dice are rolled by `d20-mcp`. Read `../CLAUDE.md` first — it has the ground rules that apply to every campaign here.

## Structure

```
rpg/dnd/
├── AGENTS.md                ← you are here
├── CLAUDE.md                 ← full version incl. Party Mode and fork maintenance (Claude Code)
├── campaigns/                ← dm20-protocol's own storage root (DM20_STORAGE_DIR)
│   └── {campaign-name}/      ← campaign.json, characters.json, sessions/, etc.
├── events/                   ← dm20-protocol adventure log (shared across campaigns)
├── library/                  ← imported PDF/homebrew rulebooks (gitignored, can be large)
└── rulebook_cache/           ← cached SRD API responses (srd_2024 committed, the rest gitignored)
```

`campaigns/` and `events/` are gitignored by default (this framework started as a public repo), so campaigns are **not backed up** until the player picks a setup in "Saving Campaigns" in `CLAUDE.md`: a separate private repo, this repo made private, or (their explicit choice) public. `campaigns/*/party/` holds player-link secrets and is ignored in every setup. `library/` and `rulebook_cache/` for non-SRD sources (5etools, open5e, custom) are gitignored regenerable/bulky content.

`rulebook_cache/srd_2024/` is committed — small, official-SRD-only, so a lookup fetched once (e.g. from a session with unrestricted network) is available afterward to sessions that can't reach the SRD API directly. See "Network Access" below.

## MCP Servers

Configured in the repo-root `.mcp.json`:

- **dm20-protocol** — campaign/character/combat/quest state, rulebook lookup (SRD 2014/2024, PDFs). `DM20_STORAGE_DIR` points at `rpg/dnd` via `${CLAUDE_PROJECT_DIR}`.
- **d20-mcp** — dice rolling only (`roll`, `roll_detailed`, `roll_batch`, `validate_syntax`).

### Network Access

`load_rulebook(source="srd")` calls the official SRD API (`dnd5eapi.co`). Remote/cloud/sandboxed sessions (including phone/web access, which always runs remotely) may sit behind an outbound proxy that blocks that domain — a genuine 403, not a bug. A locally-installed session on a laptop has no such restriction.

Do the first `load_rulebook(source="srd")` and any new-content lookups from a session with real network access, then commit/push — that caches the fetched content so any later session, including a restricted one, can reuse it. Don't silently substitute `5etools` (broader, non-SRD, mixes 2014/2024 content) without flagging the tradeoff — ask first.

### Dice rule — important

dm20-protocol has its own `roll_dice` tool. Don't use it. All dice rolls go through `d20-mcp` exclusively, per the ground rules in `../CLAUDE.md`. If `d20-mcp` isn't connected, say so before rolling anything — don't fall back to dm20-protocol's roller or an invented number.

## Rules Edition

Campaigns in this folder standardize on the **SRD 2024** ruleset (`rules_version="2024"` at `create_campaign`, then `load_rulebook(source="srd", version="2024")`); dm20-protocol supports both 2014 and 2024. Every campaign adds the 5 custom overlays from `templates/rulebooks/custom/` (copy them into the campaign's `rulebooks/custom/`).

## Campaign Creation Workflow

1. Confirm both MCP servers are connected.
2. `load_rulebook(source="srd", version="2024")` (the version defaults to 2014).
3. `create_campaign(name=..., description=..., rules_version="2024")` — ask the player for name/setting/tone.
4. `create_character(...)` — ask the player for race, class, and background before calling. Use `d20-mcp` for any creation rolls.

## Slash Commands

This install skipped dm20-protocol's bundled `/dm:*` slash-command persona files (they weren't reviewed). DM behavior is governed by `../CLAUDE.md`'s ground rules instead.
