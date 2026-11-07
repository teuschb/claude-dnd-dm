---
name: party-mode
description: Run a multiplayer D&D campaign in dm20 Party Mode - start and stop the party server, give players private links, expose it over the network (Tailscale), keep the laptop awake, watch the action queue, narrate and resolve player actions, and the narration hooks that check each message. Use for "start party mode", "check now", "watch for 2 hours", "stop party mode", or any multiplayer session where players post from their phones.
---

# Party Mode

Core rules: load `dnd-dm:dm` first if it isn't loaded. Tool names are bare; call them by their namespaced plugin names. Do the common start steps (load campaign, reload rulebooks, game state and arc) from `dnd-dm:session-start` first.

The DM loop rules for the table live in the campaign's own `DM_LOOP.md` (loop rules, the pre-send checklist, combat, pacing) and `DM_LOOP_OPS.md` (tool quirks, bookkeeping). The master copies are `${CLAUDE_PLUGIN_ROOT}/templates/party-campaign/DM_LOOP.md` and `DM_LOOP_OPS.md`; if the campaign folder lacks them, copy them in and fill in the names. Read the campaign's `DM_LOOP.md` before resolving any player action, and `DM_LOOP_OPS.md` at session start and whenever a tool misbehaves. Each rule in them came from something that actually went wrong at a real table.

Party Mode is **session-based, not always-on.** The party web server runs *inside* the dm20-protocol MCP process, which is a child of the Claude Code session — so closing the laptop kills the server and the DM together. That's fine: campaign state is plain files on disk, so a teardown loses nothing (and if campaigns are backed up to git, nothing is lost even if the disk is). `party/` is gitignored and its links regenerate on the next `start_party_mode`.

## Start (~2 minutes)

Steps 1, 2 and 6 of the old checklist (load campaign, reload rulebooks, `get_game_state` + the arc) are the common steps in `dnd-dm:session-start`. Then:

3. `start_party_mode` — prints player URLs + QR paths. **Player links are secret per-campaign tokens** (secret in `campaigns/<c>/party/.token_secret.json`, gitignored). They stay the same across restarts. A lost/leaked link: `party_refresh_token("<character name>")` rotates just that player's.
4. Optional, for phones off your LAN: expose port 8080 publicly, e.g. `tailscale funnel --bg 8080`.
5. Arm a `Monitor` on `party/actions.jsonl` for `'"status": "pending"'` (use `tail -n 0 -F`, capital F: the file may not exist yet on a clean feed). Monitors expire after 30 min, so re-arm on expiry.
6. `get_game_state` and read the campaign's `CAMPAIGN_ARC.md` before narrating anything. If it's missing or unfilled, write it first (`dnd-dm:new-campaign`, Campaign Creation Workflow step 6).

**Cost note:** every wake-up resends the whole conversation, so idle polling for days in one long session burns usage fast. Run the DM loop on demand ("check now", or "watch for N hours") from a fresh session rather than leaving it polling. Never auto-pause a loop the owner started; they say stop.

## Stop

1. `stop_party_mode`
2. If you opened a public tunnel, close it (e.g. `tailscale funnel --https=443 off`, verify with `tailscale funnel status`).
3. `TaskStop` the Monitor; `ScheduleWakeup(stop: true)` if a `/loop` is running.
4. At a **session** boundary (not every teardown): archive the feed — `mkdir -p party/sessions/session_NN && mv party/responses.jsonl party/actions.jsonl party/sessions/session_NN/` — then `add_session_note`, level every PC one step (milestone: every session at levels ~1–3, less often after that; see `dnd-dm:level-up`), and update `game_state.notes`. Full session-end bookkeeping: `dnd-dm:session-end`.

## Keeping the laptop awake mid-session

Prefer **lid open + `caffeinate -dimsu`** (Ctrl-C when done). It's scoped to that process, so it can't be forgotten. (`sudo pmset -a disablesleep 1` survives a closed lid, but it's global and persists across reboots — undo with `sudo pmset -a disablesleep 0`.)

## Network access

Players on the same Wi-Fi can use their links directly. For phones elsewhere, expose port 8080 (step 4). Remote/sandboxed sessions may not reach the SRD API; see "Network access" in `dnd-dm:rules`.

## Narration technique

The party web UI shows each player only their OWN submissions plus the DM's narration — players never see each other's raw messages. So every `party_resolve_action` narrative must convey what the acting player just did, up front, or the rest of the table is lost. But **translate register**:

- **In-character speech or action** ("I say to the guard: '…'", "I draw my club") → quote the dialogue verbatim / describe the action directly in the narration.
- **An OOC action-declaration to the DM** ("let's build the fire-starter", "I'll take the rear") → render it as in-fiction narration in your own words. Don't quote it back as though the character said it aloud.

## Act directly, don't ask

When a party-mode session is live and Claude is the DM, **act directly**: pop the action, resolve it with a real DM response, apply sheet/state changes, build out the world (locations, NPCs, quests) as needed. Don't end updates to the human with "want me to…?" for the obvious next step, and don't hold a drafted reply waiting for approval — connected players are waiting. Keep the human informed with a one-line note per exchange. Only surface a real fork the human must decide (a rules call they've reserved, something destructive or outward-facing) or a genuine escalation (a player asking for the human).

## Hooks

The plugin's hooks run these checks (`party_resolve_action` runs both; `party_push` runs only the narration check). They match both the plugin tool names (`mcp__plugin_dnd-dm_dm20-protocol__...`) and the older project-scoped names:

- `scripts/check_resolve_leads.py` (`party_resolve_action` only) — the narrative must lead with what the acting PC did (names come from `characters.json` plus the campaign's `lead_aliases.json` for companions).
- `scripts/check_narration_rules.py` (`party_resolve_action` and `party_push`) — no words from the campaign's `narration_rules.json` banned list, and in combat a position list plus a `reactions: ...` note in `dm_notes`.

On a false positive, fix the narrative, not the hook. Deliberate exceptions: `[words-exempt: why]` or `[positions-exempt: why]` in `dm_notes` (and `[lead-exempt: why]` for the leads check).

A third hook, `scripts/guard_campaign_privacy.py`, runs before every Bash command and asks before campaign data is pushed to a public repo. See "Saving Campaigns" in `dnd-dm:new-campaign`.
