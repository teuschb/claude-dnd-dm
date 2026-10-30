# CLAUDE.md — rpg/dnd

D&D 5e campaigns, solo or multiplayer (Party Mode). Claude acts as Dungeon Master; state lives in `dm20-protocol`, dice are rolled by `d20-mcp`. Read `../CLAUDE.md` first — it has the ground rules that apply to every campaign here.

## Structure

```
rpg/dnd/
├── CLAUDE.md               ← you are here
├── AGENTS.md               ← condensed version for non-Claude-Code agents (no Party Mode)
├── DM_CORE.md              ← DM rules for solo campaigns
├── IMPROV_TOOLKIT.md       ← random names, NPC wants, obstacles
├── SRD_2024_*.md           ← rules references (class features, monsters, magic items)
├── templates/              ← starter files for a new campaign (see "Campaign Creation Workflow")
├── scripts/hooks/          ← narration checks run before every Party Mode message (see "Hooks")
├── campaigns/              ← dm20-protocol's own storage root (DM20_STORAGE_DIR)
│   └── {campaign-name}/    ← campaign.json, characters.json, sessions/, etc.
├── events/                 ← dm20-protocol adventure log (shared across campaigns)
├── library/                ← imported PDF/homebrew rulebooks (gitignored, can be large)
└── rulebook_cache/         ← cached SRD API responses (srd_2024 committed, the rest gitignored)
```

`campaigns/` and `events/` are gitignored by default, because this framework started as a public repo: characters, the secret arc and session notes would otherwise be one push away from being published. That also means they're **not backed up** until the player picks a setup in "Saving Campaigns". `campaigns/*/party/` (player-link secrets) is ignored in every setup. `library/` (PDFs/homebrew) and `rulebook_cache/` for non-SRD sources (5etools, open5e, custom) are gitignored too — regenerable/bulky.

`rulebook_cache/srd_2024/` is the exception — it **is** committed. It's small (official SRD only), and committing it means a rules lookup fetched once is available afterward to any session that can't reach the SRD API directly, like a remote/sandboxed or phone session. See "Network Access" below.

## MCP Servers

Both are configured in the repo-root `.mcp.json` (project-scoped, so `git clone` + approve gets you set up):

- **dm20-protocol** — campaign/character/combat/quest state, rulebook lookup (SRD 2014/2024, PDFs). Runs from the fork `teuschb/dm20-protocol`, pinned by commit SHA in `.mcp.json`; the fork adds the Party Mode fixes these docs rely on (`party_push`, secret player links, live sheets, Web Push, limited-use feature tracking). `DM20_STORAGE_DIR` is set to `${CLAUDE_PROJECT_DIR}/rpg/dnd`, so all its data lands under this folder.
- **d20-mcp** — dice rolling only (`roll`, `roll_detailed`, `roll_batch`, `validate_syntax`).

First use in a freshly cloned repo requires approving the project's MCP servers — Claude Code will prompt for this. Both run through `uvx`, so install [uv](https://docs.astral.sh/uv/) first.

## Which rules file to read

- **Party Mode campaign:** that campaign's `DM_LOOP.md` (loop rules) + `DM_LOOP_OPS.md` (tool quirks, bookkeeping). Start from `templates/party-campaign/`.
- **Solo campaign:** `DM_CORE.md` (campaign-agnostic DM rules, no Party Mode) + that campaign's own `CLAUDE.md`. Start from `templates/solo-campaign/`. The Party Mode checklist below doesn't apply to solo play.
- Both keep an `ENCOUNTER_LOG.md` and `PLAYER_FEEDBACK.md` in the campaign folder.

## Session Start / Stop Checklist (Party Mode)

Party Mode is **session-based, not always-on.** The party web server runs *inside* the dm20-protocol MCP process, which is a child of the Claude Code session — so closing the laptop kills the server and the DM together. That's fine: campaign state is plain files on disk, so a teardown loses nothing (and if campaigns are backed up to git, nothing is lost even if the disk is). `party/` is gitignored and its links regenerate on the next `start_party_mode`.

### Start (~2 minutes)

1. `load_campaign(name="<campaign>")`.
2. **Reload rulebooks — they do NOT persist across sessions.** `load_rulebook(source="srd", version="2024")`, then each overlay in `campaigns/<campaign>/rulebooks/custom/` via `load_rulebook(source="custom", path=...)`. Order: species_corrections → class_progression → feats → background_additions → spells.
3. `start_party_mode` — prints player URLs + QR paths. **Player links are secret per-campaign tokens** (secret in `campaigns/<c>/party/.token_secret.json`, gitignored). They stay the same across restarts. A lost/leaked link: `party_refresh_token("<character name>")` rotates just that player's.
4. Optional, for phones off your LAN: expose port 8080 publicly, e.g. `tailscale funnel --bg 8080`.
5. Arm a `Monitor` on `party/actions.jsonl` for `'"status": "pending"'` (use `tail -n 0 -F`, capital F: the file may not exist yet on a clean feed). Monitors expire after 30 min, so re-arm on expiry.
6. `get_game_state` and read the campaign's `CAMPAIGN_ARC.md` before narrating anything. If it's missing or unfilled, write it first (Campaign Creation Workflow step 6).

**Cost note:** every wake-up resends the whole conversation, so idle polling for days in one long session burns usage fast. Run the DM loop on demand ("check now", or "watch for N hours") from a fresh session rather than leaving it polling.

### Stop

1. `stop_party_mode`
2. If you opened a public tunnel, close it (e.g. `tailscale funnel --https=443 off`, verify with `tailscale funnel status`).
3. `TaskStop` the Monitor; `ScheduleWakeup(stop: true)` if a `/loop` is running.
4. At a **session** boundary (not every teardown): archive the feed — `mkdir -p party/sessions/session_NN && mv party/responses.jsonl party/actions.jsonl party/sessions/session_NN/` — then `add_session_note`, level every PC one step (milestone: every session at levels ~1–3, less often after that; see `DM_CORE.md`), and update `game_state.notes`.

### Keeping the laptop awake mid-session

Prefer **lid open + `caffeinate -dimsu`** (Ctrl-C when done). It's scoped to that process, so it can't be forgotten. (`sudo pmset -a disablesleep 1` survives a closed lid, but it's global and persists across reboots — undo with `sudo pmset -a disablesleep 0`.)

### Network Access

`load_rulebook(source="srd")` calls out to the official SRD API (`dnd5eapi.co`). Remote/cloud/sandboxed Claude Code sessions (including phone/web access) may sit behind an outbound proxy that blocks that domain — a genuine 403, not a bug. A locally-installed Claude Code session on a laptop has no such restriction.

Since `rulebook_cache/srd_2024/` is committed, do any new-content lookups from a laptop session, then commit. Later sessions, including network-restricted ones, reuse the cache. If `srd` is unreachable and there's no cache to fall back on, don't silently substitute `5etools` (broader, non-SRD, mixes 2014/2024 content) without saying so — ask first.

### Running Party Mode as DM — narration technique

The party web UI shows each player only their OWN submissions plus the DM's narration — players never see each other's raw messages. So every `party_resolve_action` narrative must convey what the acting player just did, up front, or the rest of the table is lost. But **translate register**:

- **In-character speech or action** ("I say to the guard: '…'", "I draw my club") → quote the dialogue verbatim / describe the action directly in the narration.
- **An OOC action-declaration to the DM** ("let's build the fire-starter", "I'll take the rear") → render it as in-fiction narration in your own words. Don't quote it back as though the character said it aloud.

### Running Party Mode as DM — act directly, don't ask

When a party-mode session is live and Claude is the DM, **act directly**: pop the action, resolve it with a real DM response, apply sheet/state changes, build out the world (locations, NPCs, quests) as needed. Don't end updates to the human with "want me to…?" for the obvious next step, and don't hold a drafted reply waiting for approval — connected players are waiting. Keep the human informed with a one-line note per exchange. Only surface a real fork the human must decide (a rules call they've reserved, something destructive or outward-facing) or a genuine escalation (a player asking for the human).

## Hooks

`.claude/settings.json` runs these checks (`party_resolve_action` runs both; `party_push` runs only the narration check):

- `scripts/hooks/check_resolve_leads.py` (`party_resolve_action` only) — the narrative must lead with what the acting PC did (names come from `characters.json` plus the campaign's `lead_aliases.json` for companions).
- `scripts/hooks/check_narration_rules.py` (`party_resolve_action` and `party_push`) — no words from the campaign's `narration_rules.json` banned list, and in combat a position list plus a `reactions: ...` note in `dm_notes`.

On a false positive, fix the narrative, not the hook. Deliberate exceptions: `[words-exempt: why]` or `[positions-exempt: why]` in `dm_notes`.

A third hook, `scripts/hooks/guard_campaign_privacy.py`, runs before every Bash command. When a `git push` targets a public (or unverifiable) remote of a repo holding campaign data, or a `gh repo` command makes a repo public while campaign data is in git, it asks the human to approve and says what would become readable. It never blocks, and it skips a repo whose owner already chose public (`git config dnd.campaignsPublic true` in that repo). See "Saving Campaigns".

## Rulebook state doesn't persist across sessions

`load_campaign` does not reload a campaign's rulebooks from `rulebooks/manifest.json`. Every session re-runs `load_rulebook` for the SRD base and each overlay before relying on `get_class_info`, `get_race_info` or `search_rules`.

`get_class_info` doesn't render feature text (a rendering bug; `get_race_info` is fine). Use `SRD_2024_PLAYER_OPTIONS.md` for class and subclass features (levels 1–20, all subclasses, all 12 classes).

`load_rulebook(source="srd", version="2024")` reads `rulebook_cache/srd_2024/` (species grant no ability bonuses); overlays load after it and win. `create_character` isn't yet verified against 2024: pass ability scores as `manual` with explicit values and hand-verify scores, Speed, HP and AC against `SRD_2024_PLAYER_OPTIONS.md`. `armor_class` is never computed from DEX (it's whatever you pass, default 10).

## Dice rule — important

dm20-protocol has its own `roll_dice` tool. **Don't use it.** Per the ground rules in `../CLAUDE.md`, all dice rolls go through `d20-mcp` exclusively, so there's one auditable source of randomness. If `d20-mcp` isn't connected, say so before rolling anything.

## Rules Edition

Campaigns here standardize on the **SRD 2024** ruleset (`rules_version="2024"` at `create_campaign`, then `load_rulebook(source="srd", version="2024")`), plus the 5 custom overlays in `templates/rulebooks/custom/`, which fill gaps and correct the SRD API data.

## Campaign Creation Workflow

1. Confirm `d20-mcp` and `dm20-protocol` are both connected (`claude mcp list`, or a live tool call to each).
2. `load_rulebook(source="srd", version="2024")`.
3. `create_campaign(name=..., description=..., rules_version="2024")` — ask the player(s) for name/setting/tone rather than assuming.
4. Copy the starter files into `campaigns/<name>/`:
   - `templates/rulebooks/custom/*.json` → `campaigns/<name>/rulebooks/custom/`, then load them (order above).
   - Party Mode: everything in `templates/party-campaign/`. Solo: `templates/solo-campaign/CLAUDE.md`.
   - Both: `templates/ENCOUNTER_LOG.md`, `templates/PLAYER_FEEDBACK.md`, `templates/CAMPAIGN_ARC.md`, `templates/setting.md`. Fill in the names, and fill `setting.md` with the player(s): tone, guardrails, world, each PC's hooks.
5. `create_character(...)` — ask for species, class, and background before calling. Use `d20-mcp` for any ability-score or creation rolls (e.g. `4d6kh3` × 6 if the player wants rolled stats).
6. **Write the campaign arc before session 1.** Fill in every section of `CAMPAIGN_ARC.md`: the hidden truth, the layers the party uncovers in order, the cast (want, flaw, secret), the session-by-session menu with several doors into each beat, the clock that advances when the party doesn't interfere, the planned close of each chapter, and at least three endings. Build it from `setting.md` and each PC's backstory hooks, sized to the level range the table expects. Without it, play drifts into wandering around and asking questions, so don't start session 1 until it's written. If the player wants to be surprised, write it without showing them and just say it's done.
7. If `git config dnd.campaignStorage` is unset, walk the player through "Saving Campaigns" before the first session.

**At every session start**, if `CAMPAIGN_ARC.md` is missing, still has template placeholders (`<...>`, `_(...)_`), or has empty sections, write it per step 6 before narrating anything. This catches campaigns that skipped it.

## Saving Campaigns

Campaigns are gitignored by default, so a new campaign is **not backed up**. Backup matters for two things: losing the disk, and running the DM from more than one place (a phone or claude.ai/code web session works from a fresh clone and only sees campaigns that were pushed). Multiplayer doesn't need git: players connect to the DM's machine through their links.

Ask once per clone (the answer is recorded in `git config dnd.campaignStorage`, which is local and never committed). Explain the consequences in plain words, and confirm with the human before creating any GitHub repo. Ask in this order:

**1. "Do you want a separate repo just for your campaign data?"** Recommended: the game data and the framework stay apart, and the framework can be updated from upstream without touching it.
- Create it **private**: `gh repo create dnd-campaigns --private`, then confirm `gh repo view dnd-campaigns --json visibility` says `PRIVATE`.
- Set it up outside this clone (default `~/dnd-campaigns`) and symlink it in. dm20 creates `campaigns/` and `events/` on startup, so move anything already there:
  ```bash
  D=~/dnd-campaigns; mkdir -p "$D" && cd "$D" && git init -b main
  cp <framework>/rpg/dnd/templates/campaign-data.gitignore .gitignore
  mv <framework>/rpg/dnd/campaigns "$D/campaigns" && mv <framework>/rpg/dnd/events "$D/events"
  ln -s "$D/campaigns" <framework>/rpg/dnd/campaigns && ln -s "$D/events" <framework>/rpg/dnd/events
  git add -A && git commit -m "Campaign data" && git remote add origin <url from gh> && git push -u origin main
  ```
  Then restart Claude Code so dm20 picks up the moved folders. `git config dnd.campaignStorage separate`.
- Everything except `party/` is backed up, spoilers included: the arc and hidden notes are exactly what's worth keeping, and the repo is private. Commit and push from `~/dnd-campaigns` at session end.

**2. If not: "Keep it all in this repo, as a private repo of your own?"** This clone points at the public framework repo, which they can't push to. Making it theirs means a **new private repo, not a GitHub fork** (a fork of a public repo is always public):
```bash
git remote rename origin upstream          # keep pulling framework updates
gh repo create <name> --private --source . --remote origin --push
```
Confirm it says `PRIVATE`, then ask: **back up the campaign data in it, or keep it on this machine only?**
- Back up: delete the "Campaign data" block (`campaigns` and `events`) from `rpg/dnd/.gitignore` and commit. `party/` stays ignored. `git config dnd.campaignStorage same-repo`.
- Local only: leave the ignore as is. `git config dnd.campaignStorage local`.

**3. If they don't want a private repo,** say plainly what public means: anyone can read the characters, the DM's secret arc and every spoiler in it, and the session notes, including the players themselves. Then ask once more: **keep campaigns gitignored (not backed up), or publish them?** Their answer is final; don't re-ask.
- Gitignored: `git config dnd.campaignStorage local`.
- Publish: delete the "Campaign data" block from `rpg/dnd/.gitignore`, then `git config dnd.campaignsPublic true` (the privacy hook skips repos marked this way) and `git config dnd.campaignStorage public`.

Sharing with a co-DM: keep the repo private and add them as a collaborator (`gh api -X PUT repos/<owner>/<repo>/collaborators/<user> -f permission=push`).

## Slash Commands

dm20-protocol's upstream installer also ships `/dm:start`, `/dm:action`, `/dm:combat` (a Narrator/Arbiter persona). This setup runs dm20 from `.mcp.json` without those files, so the ground rules in `../CLAUDE.md` govern DM behavior.
