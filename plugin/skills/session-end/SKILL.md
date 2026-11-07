---
name: session-end
description: End a D&D session cleanly - write the session note as story prose, update quests and game-state notes, level up if due, log encounter verdicts and player feedback, archive the party feed, and offer the player debrief. Use for "end the session", "wrap up", "save the session", or when you reach a natural stopping point.
---

# Session end

Core rules: load `dnd-dm:dm` first if it isn't loaded. Tool names are bare; call them by their namespaced plugin names.

## Solo and party

1. `add_session_note` — a title plus real story prose (what happened, in story voice; loot amounts inside the prose), not a checklist. This is the one durable, human-readable record of what happened: write it so the campaign can be retold later (a title plus a few paragraphs). `treasure_found` is fixed in the fork; still write loot in the prose summary.
2. `update_quest` for every quest touched; refresh `game_state.notes` (≤ ~600 chars: where we are + open threads; it is overwritten every time and keeps no history); level up if it's a leveling session (every session at levels 1–3, then per the pacing in `dnd-dm:level-up`).
3. Append encounter verdicts to the campaign's `ENCOUNTER_LOG.md`; append any player feedback to `PLAYER_FEEDBACK.md`.
4. Offer the end-of-session debrief from the ground rules (which rolls were load-bearing and what they want more or less of), and every ~2 sessions run the three-question check-in in `PLAYER_FEEDBACK.md`.

Call the session end yourself at a natural stopping point.

## Party Mode only

Also, at a session boundary: `stop_party_mode` and close any public tunnel, `TaskStop` the Monitor, archive the feed (`mkdir -p party/sessions/session_NN && mv party/responses.jsonl party/actions.jsonl party/sessions/session_NN/`); details in `dnd-dm:party-mode`. Then `add_session_note` (prose summary, loot inside the prose), `update_quest` for every quest touched. The bookkeeping notes are in the campaign's `DM_LOOP_OPS.md`:

- The live scene (location, date, last exchange, hidden DM truth for the current situation) lives in dm20 `game_state` — read it with `get_game_state` if you've lost the thread.
- Don't hand-edit `sessions/session-NNN.json` while the campaign is loaded, for the same reason as `characters.json`: never hand-edit campaign JSON while the campaign is loaded in any running dm20 (any Claude session); the next tool save silently overwrites it. For subclass, spell slots and structured features use `update_character` (`subclass`, `spell_slots`, `add_features`). If a raw edit is unavoidable: stop every session that loaded it (`stop_party_mode` / full MCP restart), edit, then `load_campaign`.
