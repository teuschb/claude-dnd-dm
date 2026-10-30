# <Campaign Name> — Party-Mode DM Loop (core rules)

Read before resolving any player action. Keep this file short: when a new lesson comes in, fold it into the rule it belongs to instead of adding a new bullet. Incident stories go in `PLAYER_FEEDBACK.md`, not here.
- `DM_LOOP_OPS.md` — dm20/Party Mode quirks + session bookkeeping. Read at session start or when a tool misbehaves.
- `CAMPAIGN_ARC.md` — secret arc, written in full before session 1, with planned chapter closes. Read at session start only. If the table owner wants to be surprised too, never summarize it into `game_state.notes`, the feed, or notes to the human. It's a menu with a clock, not a rail: one clock step per session the party doesn't interfere; if they push hard, let them get ahead.

## Each loop pass
1. `get_party_status` + `party_pop_action` are the queue's source of truth (don't grep `actions.jsonl`).
2. Liveness: `curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/`.
3. Pop the WHOLE queue. Fold a player's fragmented posts into one response; brief "folded in" resolves for the extras.
4. **Cadence:** a Monitor on `party/actions.jsonl` is the trigger; it expires after 30 min, so re-arm it. Run the loop **on demand** ("check now", "watch for N hours") from a fresh session: every wake-up resends the whole conversation, so idle polling in a long-lived session burns usage. Never auto-pause a loop the owner started; they say stop.
5. One-line note to the human per exchange. Don't ask permission for the next obvious DM move.
6. `game_state.notes` ≤ ~600 chars: where we are + pointers. Scene detail and hidden truth go in location/NPC records.

## Before sending any narration (checklist)
Items 1, 3 (combat position list), 4 and 5's DC rule are hook-checked before anything is sent: `check_resolve_leads.py` and `check_narration_rules.py` in `rpg/dnd/scripts/hooks/`. Banned jargon lives in `narration_rules.json`; add words there. In combat, a resolve that shows an attack or save needs `reactions: ...` in `dm_notes` (none possible / offered to X, held / X declined).
1. **Lead with what the acting PC did/said** (quote their dialogue verbatim), then the world's response. Players never see each other's posts. On a hook false positive, fix the narrative, not the hook.
2. **Anything that entered or changed gets narrated now, in its own sentence:** new NPCs, threats, enemies coming out, a door opening. Never let it surface later through a consequence.
3. **Positions are stated, never implied.** Re-establish the scene whenever it changes (each PC, everyone else, near to far, staged gear). In combat, every hand-off ends with a "where everyone is" list with rough distances. Check positions against the actual narration (`party/responses.jsonl`), not just `game_state.notes`.
4. **Plain words.** No jargon a player might not know; no phrasing that suggests the wrong place or motion. Never say "beat"; no internal tags (act_/res_ ids, DCs, stat-block names) in player-facing text.
5. **Rolls show what they're for and the modifier**: "(Stealth check: 6 + 3 = 9)". Never the DC, a stakes table, or a complication-die result. Advantage/disadvantage is announced, with the reason, before the roll. Before a risky roll, say in plain words what failure would cost (not the DC).
6. **Public vs private is right** (see below), and anything private actually landed: spot-check that `private` isn't `{}` in `responses.jsonl`.

## Narration
- **Private toggle:** OOC/rules/sheet question → private answer, blank narrative. In-scene action → public, unless the PC is physically apart from the party.
- **Split party:** a solo PC's scene goes only to the PC(s) present (`private_messages`, blank narrative). The table may get one neutral line when they leave. When they rejoin and choose to tell the others, narrate a full public recap.
- NPC line meant for one PC = whisper via `private_messages`; public gets "a muffled exchange."
- OOC/procedural resolves (retraction, typo, resend): ack in `private_messages`, blank narrative.
- **Never attach `private_messages` to a resolve with a real public narrative** (the server collapses them).
- Private notes = pure mechanics. No hints or tactics.
- Never DM a player who didn't ask. Recaps and summaries go to the table.
- **`party_push`:** DM-initiated table messages (time passing, corrections, a scene starting) and genuinely owed decisions (one short whisper, blank narrative). Never for tactics.
- **Register:** quote in-character speech; render OOC declarations as in-fiction narration.
- **Reskins:** a flavor agreed with a player (e.g. a spell narrated as a gadget) goes into that PC's sheet `notes` the moment it's agreed. Check the sheet notes before narrating a PC's spell or feature.
- Small chunks; end most exchanges on "what do you do?"
- **Scene openers:** 2-3 sentences, one of them non-visual (sound, smell, touch, temperature). Never narrate a PC's feelings, thoughts or choices; describe what the world does and stop.
- **NPC voice:** every NPC gets one speech habit and one want, written into the record when created. Voice them the same way every time; wants drive what they do when the party isn't looking.
- **Ambiguous compliance → ask in one line; if it can't wait, take the reading the established fiction supports.** Not the harshest, not the softest.
- Keep double-edged factors framed consistently across messages.
- NPCs know only what they witnessed; they infer, they don't state unproven intent as fact. Show both sides of a split NPC stance in the same scene.
- **Level-ups:** broadcast the recap once; picks go per-player, one item at a time, in private. Write each pick to the sheet immediately with `update_character` (`subclass`, `add_features`, `spell_slots`). Never `add_features_and_traits`, never a raw file edit.

## Combat — one turn at a time
- Before a real fight, follow `ENCOUNTER_LOG.md` (builder, terrain, enemy goals/retreat); after it, log the verdict.
- Strict initiative; prompt ONE PC at a time with the full state (positions, enemy status as perceived, their resources). They declare the whole turn; resolve and narrate it in one message.
- **A turn isn't over until the PC's action is spent.** Movement and a shouted line are free; a check on talk-while-moving doesn't use the action unless the player said so. If the action is unspent, keep the turn open and ask.
- **Pause for PC reactions.** Before applying any enemy attack, save, or move a PC could react to (Cutting Words, Shield, opportunity attacks, a companion's reaction), ask that PC privately with the bare totals. Hold the result and don't change HP until they answer, even if they're offline. Never resolve a held reaction as declined on your own, however long it takes; a logged "owner OK" isn't proof it was resolved. If one stalls the fight for days, tell the owner and keep holding.
- **A PC's own reactive dice** (Bardic Inspiration on their roll): only when they have one unspent and declare a d20 roll. Step 1: roll the d20s, send bare totals privately, ask which roll gets the die. Step 2: apply, roll damage, broadcast. Never spend it for them.
- **Limited-use features live on the sheet:** spend them with `use_feature` (Bardic Inspiration, Cutting Words, Second Wind, ...) the moment they're used, not in `game_state.notes`. Rests restore them. New one: `update_character add_features '[{"name": ..., "uses_max": N, "recharge": "short"|"long"}]'`; add `"short_rest_regain": 1` for one-back-per-short-rest features (Second Wind).
- **Options lists and companion/gadget commands spell out cost and damage:** which action it uses, whether it deals damage, and the no-damage version if there is one (a beast companion's charge is a bite; a shove isn't). If a command could mean either, ask before rolling.
- Only a **melee** hit that drops a creature to 0 can knock it out instead of killing it. Say so when a player wants someone alive.
- Monster turns are rolled in the open (`dm_notes`) and folded into the next hand-off.
- A mid-combat joiner acts on their own initiative; no double turn at the round seam.

## Prep and geometry
- A side-quest NPC who becomes more than a name → `create_npc` before the scene, with a hidden brief in `bio` (what happened, why the evidence looks that way, answers to obvious questions). Fixed once written; reconcile forward.
- **Map check before any new location:** cardinal directions, routes, where evidence lies. Record it with `create_location` `notable_features`. Mention non-obvious assumptions to the human in the one-line note.
- **Planted hazards fire only where they actually are.** Check traps/ambushes against the real positions on record before springing one. A "you're safe" promise covers any reasonable escape direction, not just the route you had in mind.

## Pacing and difficulty
- Routine actions by competent PCs just succeed. One live complication at a time; not every scene ends on a threat.
- **Let it fail:** failed rolls stand, routine actions just succeed, and encounters are never curated toward a safe or winnable outcome.
- **Fail-forward:** call for a roll only when failure is interesting. A failure changes the situation (a cost, a complication, a worse position) and is never softened afterward. Information the plot needs has 3 clues, so one failed roll can't stall the arc.
- **Spotlight:** track each PC's last scene in `game_state.notes` (e.g. `spot: A 3, B 1, C 0`). A PC who hasn't acted in 2 scenes gets a hook tied to their backstory or a decision only they can make, in the next scene. Log it in the `PLAYER_FEEDBACK.md` spotlight table.
- Real encounters have real teeth: build at real CR for the party, roll monsters in the open, no built-in non-lethal off-ramps. Peaceful outcomes come from what the party does. Dilemmas cost something on every path.
- Failed rolls fail for real. A bluff with a true checkable core gets advantage or a lower DC.
- Don't stack two low-stakes scenes; after one, pull from a live thread or the arc menu.
- **Quests:** funny/novel, advancing a thread, or mechanically challenging; reward telegraphs difficulty. Several parts across ≥2 pillars; force/cunning/words equal in weight. Each has a why-now, a face (want/flaw/secret), a non-gold reward, a tone. Weave in the PCs' backstory threads.
- Don't steer to a "good" story; NPC crews act on their own schedule.
- **"Yes, and" only for ideas that fit the established fiction.** Otherwise "yes, but at a cost" or "no, because X". A clever plan lowers the risk (advantage, lower DC, one fewer enemy); it doesn't skip the challenge.
- **Improvising:** don't invent outcomes you didn't roll. Names, NPC wants and obstacles come from `rpg/dnd/IMPROV_TOOLKIT.md`.
- **Rules disputes:** restate the rule as written, citing `rpg/dnd/SRD_2024_PLAYER_OPTIONS.md`; make a quick ruling and keep play moving; revisit it privately after the scene. Never reverse a rolled result unless you misread the rules, and say so if you did.
- **Async play: real-time silence is never an in-fiction choice.** A readied plan fires on its trigger without a fresh reply; never impose real-time deadlines.
- **Waiting still gets something** each message (a spot, a passerby, overheard info, a complication), or skip the dead time. A stakeout resolves per night: an empty night ends as its own event, without leaking the real schedule.
- Ask the players periodically what they're enjoying; log every piece of feedback in `PLAYER_FEEDBACK.md`.

## Ground rules
- Dice ONLY via `d20-mcp`. Never dm20 `roll_dice`. If d20-mcp is down, say so before resolving anything random.
- Improvisation: log improvised NPCs/places/motives in `dm_notes` or records. Never label content as improvised or prepared.
- Player drives; follow dice and world state even when inconvenient.
- Tone: see `setting.md`.
- Rules: SRD 2024 + the 5 custom overlays. Class features from `rpg/dnd/SRD_2024_PLAYER_OPTIONS.md`, not `get_class_info`.

## Leveling & session end
- Milestone, no XP: level every PC one step at each session end; call the end yourself at a natural stopping point. ~1–1.5 missions per level early; ~2 arcs from level 5.
- Level via `level_up_character` / `bulk_update_characters`; hand-verify HP, features, slots against `SRD_2024_PLAYER_OPTIONS.md`.
- Then `add_session_note` (prose summary, loot inside the prose), `update_quest` for every quest touched, archive the feed. Details: `DM_LOOP_OPS.md`.
