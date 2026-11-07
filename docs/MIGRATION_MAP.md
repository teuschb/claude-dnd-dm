# Migration map: old project layout -> plugin layout

Every instruction in the old files is accounted for below. "Old" refers to commit `f515f82` on `main` (`git show f515f82:<path>`). "Skill" paths are under `plugin/skills/`; `${PLUGIN}` is `plugin/`.

Conventions applied everywhere: bare tool names stay bare in prose, and the `dm` skill states the namespaced form (`mcp__plugin_dnd-dm_dm20-protocol__<tool>`, `mcp__plugin_dnd-dm_d20-mcp__<tool>`); "the data dir" replaces `rpg/dnd`; pointers to `../CLAUDE.md`, `../../DM_CORE.md`, `rpg/dnd/...` became pointers to the skills / bundled files.

## Files

| Old file | New location | Notes |
|---|---|---|
| `CLAUDE.md` (root) | removed | Only pointed to the two CLAUDE.md files below; replaced by SessionStart context + `dm` skill |
| `SKILL.md` (root) | `README.md` + `plugin/.claude-plugin/plugin.json` description | Scope/attribution text kept in README; setup replaced by plugin install |
| `.mcp.json` | `plugin/.mcp.json` + `plugin/bin/dm20` | dm20 pin `7725cb32...` now in `bin/dm20`; `DM20_STORAGE_DIR` set there |
| `.claude/settings.json` (hooks) | `plugin/hooks/hooks.json` | matchers cover plugin and old tool names; commands use `${CLAUDE_PLUGIN_ROOT}` |
| `.gitignore` (root) | `.gitignore` (root, unchanged) | |
| `rpg/.gitignore` (`Imports/`) | dropped | Personal-folder ignore for the old project layout; no counterpart in a plugin |
| `rpg/dnd/.gitignore` | `plugin/templates/data-dir.gitignore` | Written into a new data dir by `bin/dm20`; adds `library/` and `rulebook_cache/` ignores (the cache is now seeded, not committed per project) |
| `rpg/dnd/templates/campaign-data.gitignore` | `plugin/templates/campaign-data-repo.gitignore` | Also ignores `rulebook_cache/` |
| `rpg/CLAUDE.md` | `skills/dm/SKILL.md` (Ground rules, full text) + `scripts/session_context.py` (compact version, always on) | See section below |
| `rpg/dnd/CLAUDE.md` | split across `dm`, `new-campaign`, `session-start`, `party-mode`, `rules` skills | See section below |
| `rpg/dnd/AGENTS.md` | `skills/dm`, `rules`, `new-campaign` | Condensed duplicate of CLAUDE.md for non-Claude agents. **Support for non-Claude agents is explicitly dropped**: there is no AGENTS.md in the plugin. Unique statements listed below |
| `rpg/dnd/DM_CORE.md` | `skills/dm/DM_CORE.md` (bundled); "Leveling" -> `skills/level-up`, "Session end" -> `skills/session-end` | See section below |
| `rpg/dnd/IMPROV_TOOLKIT.md` | `skills/dm/IMPROV_TOOLKIT.md` | Verbatim |
| `rpg/dnd/SRD_2024_*.md` (3) | `plugin/reference/` | Moved, not edited (git rename) |
| `rpg/dnd/rulebook_cache/srd_2024/` | `plugin/rulebook_cache/srd_2024/` | Moved; `bin/dm20` seeds a copy into `<data dir>/rulebook_cache/srd_2024/` |
| `rpg/dnd/templates/*` | `plugin/templates/*` | Moved; reference rewrites listed below |
| `rpg/dnd/scripts/hooks/*.py` | `plugin/scripts/*.py` | Data-dir resolution via `dnd_paths.py`; behavior unchanged |
| (new) | `plugin/scripts/dnd_paths.py`, `session_context.py`, `bin/dm20`, `hooks/hooks.json` | |

## `rpg/CLAUDE.md` (ground rules)

| Old section / rule | New location |
|---|---|
| Intro: shared conventions for any RPG; structure tree | `dm` skill ("Where things live") |
| Dice are never invented | `dm` Ground rules; `session_context.py` |
| Never label content as improvised or prepared (incl. "roll on the improvisation toolkit") | `dm` Ground rules (points to `skills/dm/IMPROV_TOOLKIT.md`); `session_context.py` |
| Let it fail | `dm`; `session_context.py` |
| Announce advantage or disadvantage before rolling | `dm`; `session_context.py` |
| Never reveal DCs, stakes tables or complication-die results | `dm`; `session_context.py` |
| Never auto-decline a held reaction | `dm`; `session_context.py` |
| Player drives, dice and world logic decide | `dm`; `session_context.py` |
| Pause often | `dm`; `session_context.py` |
| End-of-session debrief offer | `dm`; `session_context.py`; `session-end` step 4 |

## `rpg/dnd/CLAUDE.md`

| Old section | New location |
|---|---|
| Structure (tree, "campaigns/ and events/ are gitignored by default ... not backed up", `party/` ignored in every setup, `library/`/`rulebook_cache/` ignored) | `dm` "Where things live" |
| "`rulebook_cache/srd_2024/` is committed ... lookup fetched once is available afterward" | `rules` "Network access" (adapted: the cache ships in the plugin and is seeded into the data dir; new lookups are cached in the data dir, not committed) |
| MCP Servers (dm20 fork pin, fork adds Party Mode fixes, `DM20_STORAGE_DIR`, d20-mcp tools; approve servers; needs uv) | `dm` "MCP servers and tool names" (approval step no longer applies: plugin servers start when the plugin is enabled) |
| Which rules file to read (party / solo / both keep ENCOUNTER_LOG and PLAYER_FEEDBACK) | `dm` "Which rules file to read" |
| Session Start / Stop: intro (session-based, server is a child of the session, closing the laptop kills both) | `party-mode` |
| Start steps 1 (`load_campaign`), 2 (reload rulebooks, order) | `session-start` common steps 1-2 |
| Start step 3 (`start_party_mode`, secret tokens, `party_refresh_token`), 4 (tunnel), 5 (Monitor `tail -n 0 -F`, 30-min expiry) | `party-mode` "Start" 3-5 |
| Start step 6 (`get_game_state`, read `CAMPAIGN_ARC.md`, write it if missing) | `session-start` step 3; repeated in `party-mode` Start 6 |
| Cost note (idle polling burns usage; run on demand) | `party-mode` "Start" |
| Stop 1-4 (stop_party_mode, close tunnel, TaskStop/ScheduleWakeup, session-boundary archive + note + level + notes) | `party-mode` "Stop"; archive/note bookkeeping also in `session-end` |
| Keeping the laptop awake (caffeinate, pmset) | `party-mode` |
| Network Access | `rules` "Network access"; one line in `party-mode` |
| Narration technique (translate register) | `party-mode` "Narration technique" |
| Act directly, don't ask | `party-mode` "Act directly, don't ask" |
| Hooks (leads, narration, guard; false positives; exemptions; privacy hook skip rule) | `party-mode` "Hooks"; guard details also in `new-campaign/saving-campaigns.md`; user-facing description in `README.md` |
| Rulebook state doesn't persist across sessions | `session-start` step 2 |
| `get_class_info` doesn't render feature text -> use SRD_2024_PLAYER_OPTIONS.md | `session-start`, `rules`, `level-up` |
| `load_rulebook(srd 2024)` reads the cache; overlays load after and win | `session-start` step 2; `rules` "Edition and overlays" |
| `create_character` not verified against 2024; pass `manual` scores; hand-verify; `armor_class` never computed from DEX | `new-campaign` step 5; `level-up` "Hand-verify" |
| Dice rule - important | `dm` "Dice rule" |
| Rules Edition (SRD 2024 + overlays) | `new-campaign` "Rules Edition"; `rules` "Edition and overlays". The old text said "5 custom overlays"; the repo ships 4 (the 5th, background additions, was removed per AUDIT.md), so the new text says 4 |
| Campaign Creation Workflow 1-7 and the "at every session start" arc check | `new-campaign` (verbatim steps); arc check repeated in `session-start` step 3 |
| Saving Campaigns (options 1-3, `git config dnd.*`, private repo creation, symlink commands, co-DM sharing) | `new-campaign/saving-campaigns.md`, rewritten relative to the data dir. Option 2 ("this clone points at the public framework repo") became "your project's own repo": the same new-private-repo-not-fork advice applies when the project has a public remote |
| Slash Commands (dm20 `/dm:*` persona files not installed) | `dm` "Slash commands" |

## `rpg/dnd/AGENTS.md`

The file existed to give non-Claude-Code agents a condensed version of the instructions. That use case is dropped with the move to a Claude Code plugin.

Almost all of it duplicates `rpg/dnd/CLAUDE.md` and is covered above. The statements unique to it:

| Statement | New location |
|---|---|
| "do the first `load_rulebook(source="srd")` ... from a session with real network access" | `rules` "Network access" |
| "Every campaign adds the overlays from `templates/rulebooks/custom/` (copy them into the campaign's `rulebooks/custom/`)" | `new-campaign` step 4 |
| Campaign Creation Workflow condensed (steps 1-5) | `new-campaign` (full version) |
| "This install skipped dm20's bundled `/dm:*` slash-command persona files" | `dm` "Slash commands" |
| "Dice rule: if d20-mcp isn't connected, say so" | `dm` "Dice rule" |

## `rpg/dnd/DM_CORE.md`

| Section | New location |
|---|---|
| Header / read order | `skills/dm/DM_CORE.md` (read order now: `dm` skill -> `session-start` -> DM_CORE -> campaign `CLAUDE.md`) |
| Ground rules; Pacing and difficulty; Quests; Combat (solo); dm20 cautions | `skills/dm/DM_CORE.md`, unchanged except the SRD_2024_PLAYER_OPTIONS.md pointer |
| Leveling - milestone (2 bullets) | `skills/level-up/SKILL.md` "Milestone" (DM_CORE keeps a pointer) |
| Session end 1-4 | `skills/session-end/SKILL.md` "Solo and party" 1-4 (DM_CORE keeps a pointer) |

## `rpg/dnd/templates/party-campaign/DM_LOOP.md` and `DM_LOOP_OPS.md`

Kept as templates (they are copied into each campaign and filled in); `party-mode` tells Claude to read the campaign's copy and where the master lives. Edits (all reference rewrites, no rule changed):

| Old text | New text |
|---|---|
| hooks "in `rpg/dnd/scripts/hooks/`" | "in the dnd-dm plugin's `scripts/` (wired in its `hooks/hooks.json`)" |
| "`rpg/dnd/IMPROV_TOOLKIT.md`" | "`IMPROV_TOOLKIT.md` (bundled with the `dnd-dm:dm` skill)" |
| "`rpg/dnd/SRD_2024_PLAYER_OPTIONS.md`" (x2) | "`SRD_2024_PLAYER_OPTIONS.md` (lookup order in the `dnd-dm:rules` skill)" |
| "the 5 custom overlays" | "the 4 custom overlays" |

`DM_LOOP_OPS.md`: unchanged. Its dm20 quirks are also what `session-end` and `level-up` refer to.

## Other templates

| File | Change |
|---|---|
| `solo-campaign/CLAUDE.md` | `../../DM_CORE.md` -> "load the `dnd-dm:dm` skill; the DM_CORE rules are in its `DM_CORE.md`"; `rpg/CLAUDE.md` -> ground rules in the `dnd-dm:dm` skill; `../../CLAUDE.md` -> `dnd-dm:new-campaign`; `DM_CORE "Session end"` -> `dnd-dm:session-end`; `../../SRD_2024_PLAYER_OPTIONS.md` -> lookup order in `dnd-dm:rules`; `rpg/dnd/templates/rulebooks/custom/` -> the plugin's `templates/rulebooks/custom/` |
| `ENCOUNTER_LOG.md` | DM_CORE.md / SRD_2024_MONSTERS.md references now name the skill that holds them |
| `party-campaign/lead_aliases.json` | `_comment` points at the plugin's `scripts/check_resolve_leads.py` |
| `CAMPAIGN_ARC.md`, `PLAYER_FEEDBACK.md`, `setting.md`, `narration_rules.json`, `rulebooks/custom/*.json` | unchanged |

## Hook scripts

| Script | Change |
|---|---|
| `check_narration_rules.py`, `check_resolve_leads.py` | `CAMPAIGNS` now `<data dir>/campaigns` via `dnd_paths.py` (project root from `CLAUDE_PROJECT_DIR`, else the hook payload's `cwd`); the tool-name check is a suffix test, so old and plugin names both work |
| `guard_campaign_privacy.py` | repos checked: the repo the data dir sits in (if it tracks `campaigns/`/`events/` files) and the repo a symlinked `campaigns`/`events` resolves into. Still ask-mode, never blocks, allows on internal errors; the `dnd.campaignsPublic` skip is unchanged |

## Changes after the first QA pass

| Change | Where |
|---|---|
| Project is D&D only when opted in (`.claude/dnd-dm.json` or `<data dir>/campaigns` exists); otherwise idle storage, nothing created | `dnd_paths.py`, `bin/dm20`, `session_context.py`; procedure in `new-campaign` "Step 0" |
| Seeding keyed on a content hash, writes only missing/different files, marker outside `srd_2024/` | `scripts/dnd_setup.py` |
| Human-is-DM carve-out | `session_context.py`, `dm` Ground rules |
| `DM_LOOP.md`: queue check before any `party_push`; optional always-watching loop; Monitor re-arm rule | `templates/party-campaign/DM_LOOP.md` (each-loop-pass item 1, cadence item 4) |
| Not added: `treasure_found` quirk (fixed at dm20 pin 7725cb3: models.py "fix 18") and the private-reply-vanishes quirk (reconnect replay keeps private type at the pin: server.py "fix 14") | `DM_LOOP_OPS.md` unchanged |
| `DM_LOOP.md` "Ambiguous compliance" rule reworded by the owner: take the reading the established fiction supports; ask in one line only if the fiction doesn't settle it | `templates/party-campaign/DM_LOOP.md` |
