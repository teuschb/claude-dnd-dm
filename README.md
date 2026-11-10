# claude-dnd-dm

A Claude Code plugin that runs D&D 5e (SRD 2024) with **Claude as the Dungeon Master**: solo in chat, or multiplayer with players joining from their phones.

The plugin (`dnd-dm`) is a bundle of skills, hooks, rules references and two MCP servers that give Claude real game state and real dice:

- **[dm20-protocol](https://github.com/teuschb/dm20-protocol)** (fork of [BNDYH/dm20-protocol](https://github.com/BNDYH/dm20-protocol)): campaigns, characters, combat, quests, rulebook lookup, and **Party Mode**, a small web server where each player gets a private link, posts what their character does, and reads the DM's narration.
- **[d20-mcp](https://github.com/saidsurucu/d20-mcp)**: the only source of dice rolls, so every roll is real and auditable.

This repository is a plugin *marketplace* with one plugin. Your campaigns live in **your project**, not here.

## Install

Requires [Claude Code](https://claude.com/claude-code), `python3` on your PATH (the hooks and the dm20 wrapper are Python scripts), and [uv](https://docs.astral.sh/uv/) (`brew install uv`; both MCP servers run through `uvx`). If `uvx` is missing the dm20 server prints how to install it instead of failing silently.

```
/plugin marketplace add teuschb/claude-dnd-dm
/plugin install dnd-dm@claude-dnd-dm
```

Or from a shell: `claude plugin marketplace add teuschb/claude-dnd-dm` then `claude plugin install dnd-dm@claude-dnd-dm --scope project`. Project scope is recommended: the plugin is then enabled for everyone who opens that project, and its skills and MCP servers stay out of your other projects' context.

**First start is slow.** The first launch builds the pinned dm20 (and d20-mcp) environments and can take up to a minute on a slow connection, and Claude Code waits only 30 seconds for an MCP server to start. Warm the cache once after installing:

```
<plugin root>/bin/dm20 --prewarm
```

(`<plugin root>` is the plugin's install directory, shown by `claude plugin details dnd-dm`.) If a server still times out, retry with `/mcp` -> Reconnect in a session. A timed-out *plugin* server also goes into a retry lockout: for about 15 minutes a new session or `claude -p` run skips it, so use Reconnect (interactive) instead of waiting.

Then open Claude Code in the project and say, e.g. *"Let's start a new solo D&D campaign."* The `dnd-dm:new-campaign` skill loads the SRD 2024 rules, creates the campaign, copies in the templates, builds your character with you, and asks how you want campaigns saved.

## Where your campaigns live

The **data dir**, default `<project>/dnd/`. To use another folder, create `.claude/dnd-dm.json` in the project:

```json
{ "data_dir": "rpg/dnd" }
```

(relative to the project root, or an absolute path). The data dir holds `campaigns/`, `events/` (dm20's own storage), a seeded copy of the SRD cache in `rulebook_cache/`, and an optional `reference/` folder for local overrides of the rules reference files. **Opt-in.** A project is a D&D project only if `.claude/dnd-dm.json` exists or `<data dir>/campaigns` already exists. In any other project the plugin creates nothing (no `dnd/` folder, no `.gitignore`, no cache) and prints nothing at session start; dm20 runs against throwaway storage in the plugin's data directory. The `dnd-dm:new-campaign` skill opts a project in (writes `.claude/dnd-dm.json`, creates and seeds the data dir) and then asks you to reconnect the dm20 server with `/mcp` -> Reconnect, because dm20 fixes its storage path at startup. A bare, unrelated `dnd/` folder is left alone.

## What's in the plugin

```
.claude-plugin/marketplace.json   the marketplace (one plugin, source ./plugin)
plugin/
  .claude-plugin/plugin.json      name dnd-dm
  .mcp.json                       dm20-protocol (via bin/dm20) + d20-mcp
  bin/dm20                        wrapper: resolves the data dir, seeds the SRD cache, sets DM20_STORAGE_DIR, execs dm20 (pinned commit)
  hooks/hooks.json                SessionStart ground rules + three PreToolUse hooks
  scripts/                        dnd_paths.py (data-dir resolver) + the hook scripts
  skills/                         dm, new-campaign, session-start, party-mode, session-end, level-up, rules
  reference/                      SRD_2024_MONSTERS / MAGIC_ITEMS / PLAYER_OPTIONS (generated from the SRD cache)
  templates/                      starter files for a new campaign, rulebook overlays, gitignores
  rulebook_cache/srd_2024/        cached SRD 5.2 data, so lookups work offline
AUDIT.md                          SRD scope check (counts, what was removed, verification)
docs/MIGRATION_MAP.md             where every section of the old project-style layout went
tests/                            fixture-based tests for the hooks and the dm20 load (run in CI)
```

- **Skills** (namespaced `dnd-dm:`): `dm` (ground rules, dice rule, which file for what), `new-campaign`, `session-start`, `party-mode`, `session-end`, `level-up`, `rules`. Each rule in them came from something that actually went wrong at a real table.
- **Always-on rules.** A SessionStart hook prints the compact ground rules (dice are never invented, let it fail, never reveal DCs, never auto-decline a held reaction, ...) in D&D projects only.
- **Hooks.** The Party Mode hooks block a message before it is sent if it breaks the checklist: it doesn't open with the acting player's action, uses banned jargon, shows a DC, or leaves out the combat position list. A guard hook asks for approval before campaign data is pushed to a public repo (below).
- **No other agents.** The old `AGENTS.md` (a condensed copy for non-Claude agents) is dropped; this is a Claude Code plugin only.
- **Tool names.** Plugin MCP tools appear as `mcp__plugin_dnd-dm_dm20-protocol__<tool>` and `mcp__plugin_dnd-dm_d20-mcp__<tool>`.

## Scope: SRD-only

Everything in this repo is either original work or material from the System Reference Document 5.2 (SRD 5.2), used under Creative Commons Attribution 4.0. The verified scope is in `AUDIT.md`: 9 species, 12 classes with 1 subclass each, 4 backgrounds, 17 feats, 339 spells, 341 monsters, 262 magic items.

**Not included:** Player's Handbook or Monster Manual content beyond SRD 5.2. That means no additional subclasses, backgrounds, feats, or spells from the full PHB, and no Product Identity monsters or items beyond the SRD (for example, no Beholder or Mind Flayer stat blocks, no Wand of Orcus, and the SRD's renamed items are used where the SRD renames them). If it is not in SRD 5.2, it is not in this repo.

Players who own other books can add content to **their own** campaign through custom overlays; the `dnd-dm:rules` skill explains the format. That content is for private use and must not go in a public repo. The plugin ships none of it.

This work is not affiliated with, endorsed by, or sponsored by Wizards of the Coast LLC.

## Saving your campaigns (and keeping spoilers private)

Everything Claude creates for a campaign (characters, the DM's secret arc and other spoilers, session notes) lands in the data dir. When the plugin first creates the data dir it writes a `.gitignore` that **ignores `campaigns/` and `events/` by default**: pushing your project can't publish your game, but your campaign isn't backed up until you choose how.

Before your first session, Claude asks how you want to save campaigns:

1. **A separate private repo for campaign data** (recommended). It lives outside the project and is linked in, so game data and project stay apart.
2. **Your project's own repo, private**, with or without the campaign data in it. A GitHub *fork* of a public repo is always public, so Claude creates a new private repo instead of forking.
3. **Public**, if you really want it. Claude spells out what anyone could read (including your players), and asks once more before anything goes up.

Backup matters if your disk dies, or if you want to run the DM from more than one machine. Multiplayer doesn't need git: players connect to your machine through their links. The player-link secrets in each campaign's `party/` folder are never committed, whichever option you pick.

The guard hook (`plugin/scripts/guard_campaign_privacy.py`) asks for your approval before Claude pushes campaign data to a public repo or makes such a repo public, unless you already chose public in step 3. It checks the repo the data dir sits in and, if `campaigns` or `events` is a symlink to a separate repo, that repo.

## Playing

- **Solo:** just play in the chat. Each session, Claude reloads the campaign and rulebooks (`dnd-dm:session-start`).
- **Multiplayer (Party Mode):** Claude runs `start_party_mode`, which prints a private link (and QR code) per player. Players on your Wi-Fi can use them directly; for phones elsewhere, expose port 8080 (e.g. `tailscale funnel --bg 8080`). Then tell Claude *"check now"* or *"watch for 2 hours"*, and it answers posts as they arrive. Players can turn on notifications with the bell button.

Party Mode only runs while your Claude Code session is open, so it suits play-by-post in bursts: sessions over an evening or a few days, not an always-on server. Every wake-up resends the whole conversation, so usage is roughly wake-ups × context size. To keep it down:

- Run the watch loop from a fresh session, and start over (`/clear`) once it gets long. The loop tells you when it's past ~120k tokens.
- The loop waits on a background watcher instead of polling, so a quiet table costs nothing until someone posts.
- Sonnet is plenty for routine loop turns (`/model sonnet`).
- Optionally cap how large any session can grow by adding `"autoCompactWindow": 200000` to your project's `.claude/settings.json`. On 1M-context models, Claude Code otherwise compacts only near 1M tokens.

## Upgrading from the clone-the-repo version

Earlier versions were a project folder you cloned and worked inside (`rpg/dnd/...`, a root `CLAUDE.md`, `.mcp.json` and `.claude/settings.json`). To move over:

1. Install the plugin in the project you play from (above).
2. Move your existing `rpg/dnd/campaigns` and `rpg/dnd/events` into the project's data dir (`dnd/` by default), or keep them where they are and add `.claude/dnd-dm.json` with `{"data_dir": "rpg/dnd"}`.
3. Remove the old project-style entry points (the old `.mcp.json` dm20/d20 entries and the D&D hooks in `.claude/settings.json`); otherwise two dm20 servers write to the same storage.
4. Campaign files that point to `../../DM_CORE.md` or `rpg/dnd/...` paths should now name the `dnd-dm:dm` skill (DM_CORE.md is bundled in it). Tool names change to the plugin-namespaced form above.

`docs/MIGRATION_MAP.md` lists where each section of the old instruction files went.

## Tests

```bash
python3 -m unittest discover -s tests -v                       # everything (the dm20 load needs uvx)
DND_DM_SKIP_DM20=1 python3 -m unittest discover -s tests -v    # hooks only, no network, about 5 seconds
```

Every test copies `tests/fixtures/project` (one campaign, "Fixture Keep", with two PCs) into a temp dir, so no real campaign is ever read or written. They cover the narration hook (banned words, internal ids, DCs, combat positions and reactions), the lead hook (naming the acting PC, aliases, dialogue), the privacy guard (real git repos plus a fake `gh`), the `hooks.json` matchers for both tool-name prefixes, and a real dm20 run through `bin/dm20` that loads the campaign, the SRD base and the custom overlays. GitHub Actions runs the hook tests on Python 3.9 and 3.13, and the dm20 load in a separate job.

The fixture campaign is written by the pinned dm20 itself. After bumping the pin in `plugin/bin/dm20`, regenerate it with `python3 tests/fixtures/make_fixture.py` and commit the result.

## Credits and licenses

- dm20-protocol is MIT-licensed; this setup uses a fork with Party Mode fixes.
- The original DM workflow, templates, and hooks in this repo are Ben Teusch's own work, MIT-licensed (see `LICENSE`).
- This work includes material from the System Reference Document 5.2 ("SRD 5.2") by Wizards of the Coast LLC, available at https://www.dndbeyond.com/srd. The SRD 5.2 is licensed under the Creative Commons Attribution 4.0 International License, available at https://creativecommons.org/licenses/by/4.0/legalcode.
