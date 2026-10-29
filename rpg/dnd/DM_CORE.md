# DM_CORE — solo-campaign DM rules (no Party Mode)

Distilled from the rules learned running a multiplayer campaign
(`templates/party-campaign/DM_LOOP.md`), minus everything specific to
Party Mode (multi-player feeds, whispers, queue polling, the loop). For a solo
campaign the DM answers in normal chat. A campaign's own `CLAUDE.md` overrides
anything here.

Read order for a solo session: `rpg/CLAUDE.md` →
`rpg/dnd/CLAUDE.md` → this file → the campaign's `CLAUDE.md`.

## Ground rules
- **Dice ONLY via `d20-mcp`** (`roll expression=`). Never dm20's `roll_dice`. If
  d20-mcp is down, say so before resolving anything random.
- Player drives; follow dice and world state even when inconvenient. Don't steer
  toward a "good" story. Pre-write what NPCs/factions do on their own schedule; the
  player's timing decides what they see.
- Improvisation labelling follows `rpg/CLAUDE.md` (flag it) unless the campaign's
  `CLAUDE.md` overrides. **Log every improvised NPC/place/motive** in the NPC
  bio / location record / `game_state.notes` so it stays consistent later.
- Small chunks; pause often; end most exchanges on "what do you do?" — but not
  every exchange needs a threat or hard fork.
- Never put internal bookkeeping (DCs, stat-block names, ids) in narration; name
  NPCs in fiction. Don't use the word "beat" in narration.
- **Show roll totals** for checks/saves/attacks in parentheses so the player can
  gauge how they're doing.
- **Rules: SRD 2024** + the custom overlays in `rulebooks/custom/`. Class features
  come from `SRD_2024_PLAYER_OPTIONS.md`, not `get_class_info`.

## Pacing and difficulty (read together)
- **Under-salt routine actions:** competent characters doing reasonable things just
  succeed — no tax. A roll that beats the DC resolves cleanly. Complications come in
  waves; ONE live complication at a time. Roll a complication die (d20-mcp) at scene
  transitions instead of deciding by mood: quiet vs trouble is then a fair roll.
- **But real encounters have real teeth:** build combat at real CR for the party
  (`build_encounter_tool` as a sanity check — it uses 2014 DMG budgets; cross-check
  CR in `SRD_2024_MONSTERS.md`), roll monsters straight in the open, no built-in
  non-lethal off-ramps. A peaceful outcome must come from what the player does, not
  from a pre-decided secret. Dilemmas should cost something on every path.
- **Solo caveat:** one PC has no party to absorb a bad round. Use `hard` as the
  default target only with a companion/NPC ally or real escape options; for a lone
  character prefer `medium` fights plus tough choices, and tell the player when a
  situation is genuinely dangerous before they commit.
- Failed rolls fail for real. A bluff with a true checkable core gets advantage.
- Don't stack two low-stakes scenes; after one, pull from a live thread.

## Quests
- Every posting/side quest must be funny/novel, advance a live thread, or be
  mechanically challenging. **Reward telegraphs difficulty** (5 gp = easy, 60 gp =
  can hurt).
- Shape: multiple discrete beats touching ≥2 pillars (exploration / combat /
  roleplay) unless deliberately pure. Force / cunning / words routes carry equal
  *weight*; the clever path can't just delete the challenge.
- Every quest: a **why-now**, a **face** (NPC with a want/flaw/secret), a **non-gold
  reward** (info, ally, favour, leverage), a distinct tone, foreshadowing where it
  fits. Weave the PC's backstory hooks on purpose. Open scenes with a sensory hook
  and a question; "yes, and" clever plans.
- **Side-quest NPC becomes more than a name → `create_npc` BEFORE the scene**, hidden
  brief in `bio`: what happened in order; why any evidence looks as it does; what
  they'd say to the obvious questions (incl. "I don't remember"). Fixed once
  written — reconcile forward, never overwrite.
- **Map check before any new location:** work out directions, travel directions and
  where evidence must lie *before* prose; record via `create_location`
  `notable_features`. Re-establish the scene whenever it changes.

## Combat (solo)
- Give the full state up front (positions, enemy status as perceived, resources).
  The player declares their whole turn; resolve it and all enemy turns in one
  message, rolled in the open.
- **Before a real fight** follow the campaign's `ENCOUNTER_LOG.md` checklist
  (builder, 2–3 interactive terrain features, each enemy's goal/tactics/retreat
  condition); **after it, log the verdict** (too easy / right / too hard).
- Reactive resources (Bardic Inspiration, Shield, and other reactions used after
  seeing a roll) get a genuine two-step: roll, tell the player the bare total, let them decide,
  then apply. Never spend a resource on the player's behalf.

## dm20 cautions
- **Never hand-edit campaign JSON while the campaign is loaded** in any running
  dm20 (any Claude session): the next tool save silently overwrites it. For
  subclass, spell slots and structured features use `update_character`
  (`subclass`, `spell_slots`, `add_features`). If a raw edit
  is unavoidable: stop every session that loaded it, edit, then `load_campaign`.
- `level_up_character` / `create_character` output must be hand-verified against
  `SRD_2024_PLAYER_OPTIONS.md` (HP, features, slots, ability scores).
- `add_session_note`'s `treasure_found` is fixed in the fork; still write loot in
  the prose summary.
- Rulebooks do not persist across sessions: reload the SRD 2024 base and each
  overlay every session (order in the campaign's `CLAUDE.md`).

## Leveling — milestone (default; the campaign may override)
- Milestone, not XP; no per-encounter XP. Level one step per completed arc/mission
  (~1–1.5 missions per level early, ~2 from level 5). Call it yourself at a natural
  stopping point.
- Level via `level_up_character`, hand-verify HP/features/slots, then re-set
  anything the tool can't (`update_character` extras).

## Session end
1. `add_session_note` — a title plus real story prose (what happened, in story
   voice; loot amounts inside the prose), not a checklist.
2. `update_quest` for every quest touched; refresh `game_state.notes` (≤ ~600 chars:
   where we are + open threads); level up if a milestone was hit.
3. Append encounter verdicts to `ENCOUNTER_LOG.md`; append any player feedback to
   `PLAYER_FEEDBACK.md`.
4. Offer the end-of-session debrief from `rpg/CLAUDE.md`, and every ~2 sessions run
   the three-question check-in in `PLAYER_FEEDBACK.md`.
