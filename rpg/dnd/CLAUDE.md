# CLAUDE.md — rpg/dnd

D&D 5e campaigns, solo or multiplayer (Party Mode). Claude acts as Dungeon Master; state lives in `dm20-protocol`, dice are rolled by `d20-mcp`. Read `../CLAUDE.md` first — it has the ground rules that apply to every campaign here.

## Structure

```
rpg/dnd/
├── CLAUDE.md               ← you are here
├── AGENTS.md               ← condensed version for non-Claude-Code agents (no Party Mode)
├── DM_CORE.md              ← DM rules for solo campaigns
├── SRD_2024_*.md           ← rules references (class features, monsters, magic items)
├── templates/              ← starter files for a new campaign (see "Campaign Creation Workflow")
├── scripts/hooks/          ← narration checks run before every Party Mode message (see "Hooks")
├── campaigns/              ← dm20-protocol's own storage root (DM20_STORAGE_DIR)
│   └── {campaign-name}/    ← campaign.json, characters.json, sessions/, etc. (gitignored; optionally its own private repo)
├── events/                 ← dm20-protocol adventure log (shared across campaigns, gitignored)
├── library/                ← imported PDF/homebrew rulebooks (gitignored, can be large)
└── rulebook_cache/         ← cached SRD API responses (srd_2024 committed, the rest gitignored)
```

**Campaign data never goes in this repo.** This framework is a public repo, so `campaigns/` and `events/` are gitignored: characters, the secret arc and session notes would otherwise be one push away from being published. To keep a campaign in git, give it its own private repo (see "Saving a Campaign"). `library/` (PDFs/homebrew) and `rulebook_cache/` for non-SRD sources (5etools, open5e, custom) are gitignored too — regenerable/bulky.

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

Party Mode is **session-based, not always-on.** The party web server runs *inside* the dm20-protocol MCP process, which is a child of the Claude Code session — so closing the laptop kills the server and the DM together. That's fine: campaign state is plain files on disk, so a teardown loses nothing (and with a private campaign repo, nothing is lost even if the disk is). `party/` is gitignored and its links regenerate on the next `start_party_mode`.

### Start (~2 minutes)

1. `load_campaign(name="<campaign>")`.
2. **Reload rulebooks — they do NOT persist across sessions.** `load_rulebook(source="srd", version="2024")`, then each overlay in `campaigns/<campaign>/rulebooks/custom/` via `load_rulebook(source="custom", path=...)`. Order: species_corrections → class_progression → feats → background_additions → spells.
3. `start_party_mode` — prints player URLs + QR paths. **Player links are secret per-campaign tokens** (secret in `campaigns/<c>/party/.token_secret.json`, gitignored). They stay the same across restarts. A lost/leaked link: `party_refresh_token("<character name>")` rotates just that player's.
4. Optional, for phones off your LAN: expose port 8080 publicly, e.g. `tailscale funnel --bg 8080`.
5. Arm a `Monitor` on `party/actions.jsonl` for `'"status": "pending"'` (use `tail -n 0 -F`, capital F: the file may not exist yet on a clean feed). Monitors expire after 30 min, so re-arm on expiry.
6. `get_game_state` and read the campaign's `CAMPAIGN_ARC.md` before narrating anything.

**Cost note:** every wake-up resends the whole conversation, so idle polling for days in one long session burns usage fast. Run the DM loop on demand ("check now", or "watch for N hours") from a fresh session rather than leaving it polling.

### Stop

1. `stop_party_mode`
2. If you opened a public tunnel, close it (e.g. `tailscale funnel --https=443 off`, verify with `tailscale funnel status`).
3. `TaskStop` the Monitor; `ScheduleWakeup(stop: true)` if a `/loop` is running.
4. At a **session** boundary (not every teardown): archive the feed — `mkdir -p party/sessions/session_NN && mv party/responses.jsonl party/actions.jsonl party/sessions/session_NN/` — then `add_session_note`, level every PC one step (milestone), and update `game_state.notes`.

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

`.claude/settings.json` runs two checks before every `party_resolve_action` / `party_push`:

- `scripts/hooks/check_resolve_leads.py` — the narrative must lead with what the acting PC did (names come from `characters.json` plus the campaign's `lead_aliases.json` for companions).
- `scripts/hooks/check_narration_rules.py` — no words from the campaign's `narration_rules.json` banned list, and in combat a position list plus a `reactions: ...` note in `dm_notes`.

On a false positive, fix the narrative, not the hook. Deliberate exceptions: `[words-exempt: why]` or `[positions-exempt: why]` in `dm_notes`.

A third hook, `scripts/hooks/guard_campaign_privacy.py`, runs before every Bash command and blocks git/gh commands that would publish campaign data (see "Saving a Campaign"). It has no exemption marker on purpose: if it blocks something the human really wants, tell them and let them run it themselves.

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
   - Both: `templates/ENCOUNTER_LOG.md`, `templates/PLAYER_FEEDBACK.md`, `templates/CAMPAIGN_ARC.md`, `templates/setting.md`. Fill in the names.
5. `create_character(...)` — ask for species, class, and background before calling. Use `d20-mcp` for any ability-score or creation rolls (e.g. `4d6kh3` × 6 if the player wants rolled stats).
6. Ask whether they want the campaign saved to a private GitHub repo (see "Saving a Campaign"). Default is no: it stays on this machine only.

## Saving a Campaign

The framework repo is public, so the campaign never goes in it: `campaigns/` is gitignored, and the privacy hook blocks force-adding it. A campaign is saved in **its own private repo**, inside its folder:

```bash
cd rpg/dnd/campaigns/<name>
cp ../../templates/campaign.gitignore .gitignore   # keeps party/ secrets out
git init -b main && git add -A && git commit -m "Start <name>"
gh repo create <name> --private --source . --push
```

- **Always `--private`.** Never `--public`, and never change an existing campaign repo to public; the hook blocks both. The arc holds spoilers, and the sheets and notes are the players' table.
- Before the first push, confirm with the human (it creates a GitHub repo), then verify: `gh repo view <name> --json visibility` must say `PRIVATE`.
- Afterward, commit and push from the campaign folder at session end. The framework repo's own `git status` never shows campaign files; that's expected.
- Sharing with a co-DM: keep it private and add them as a collaborator (`gh api -X PUT repos/<owner>/<name>/collaborators/<user> -f permission=push`).
- If someone forks this framework on GitHub, the fork is public, and none of the above changes: campaigns still live only in their own private repos.

## Slash Commands

dm20-protocol's upstream installer also ships `/dm:start`, `/dm:action`, `/dm:combat` (a Narrator/Arbiter persona). This setup runs dm20 from `.mcp.json` without those files, so the ground rules in `../CLAUDE.md` govern DM behavior.
