# <Campaign Name> — Ops Reference (dm20 / Party Mode quirks + bookkeeping)

NOT read every loop pass. Read at session start, and whenever a tool misbehaves.
Behavioral rules for the DM live in `DM_LOOP.md`.

## Pending at next session start
- _(things the next session must do first: a restart, a player to ask, a sheet to fix)_

## dm20 / Party Mode quirks

- **Player page:** shows a presence line ("DM is here" / "active N min ago"), an unread count in the tab title, a Map button when `<campaign>/maps/index.html` exists, and a 🔕/🔔 button for notifications (Web Push; on iPhone only once the page is added to the Home Screen). Tell players about the bell once.
- **The character panel live-updates** when a DM *tool* call changes a sheet. Raw-JSON hand-edits never show.
- **Never hand-edit `characters.json` (or any campaign JSON) while dm20 is running.** dm20 keeps the campaign in memory, shared by every tool call and the party server. A raw edit is invisible to players, and the next tool call that saves that character silently overwrites it. If no tool can make a change, stop and say so. The only safe hand-edit: `stop_party_mode` / full MCP restart first, edit, then reload.
- **Feature lists:** `update_character add_features` writes the structured `features` list players see. `add_features_and_traits` writes a legacy list that's invisible once a character has structured features. Use `add_features`, `remove_features`, `subclass`, `spell_slots`.
- **`private_messages` with malformed JSON** used to drop silently to `{}`; `party_push` now rejects it, but for any private message that matters, read the `private` field back from `party/responses.jsonl`.
- **Narrative + private in one resolve:** the server collapses them into one private frame. Keep `private_messages` on resolves with a blank narrative.
- **Players out of sync:** a full page reload pulls the whole backlog from `responses.jsonl`; nothing is lost server-side.
- Equipping a stacked item (e.g. "Dagger" x2) moves the whole stack to the slot. Add a separate single item for the off-hand.
- `app.js`/css changes in dm20 go live on a player hard-refresh; `server.py`/`models.py` changes need a full MCP restart.

## Session bookkeeping

- The live scene (location, date, last exchange, hidden DM truth for the current situation) lives in dm20 `game_state` — read it with `get_game_state` at the top of a pass if you've lost the thread.
- Keep `game_state.notes` updated as the running "where we are" record. It's overwritten every time and keeps no history.
- **`add_session_note`'s `summary` is the one durable, human-readable record** of what happened. Write it as real narrative prose (a title plus a few paragraphs in story voice), not a bullet recap, so the campaign can be retold later. Put loot and rewards inside the prose.
- Don't hand-edit `sessions/session-NNN.json` while the campaign is loaded, for the same reason as `characters.json`.
