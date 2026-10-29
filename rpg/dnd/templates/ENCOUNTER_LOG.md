# <Campaign Name> — Encounter Log

dm20 has no tool that saves encounters (`encounters.json` stays empty), so the DM
keeps this by hand. Purpose: make the "real teeth" difficulty calibration
checkable after the fact instead of vibes. Append one entry per fight or
mid-size social/skill challenge. Plain file — safe to edit while the campaign is
loaded (dm20 never touches it).

## Before the fight (60 seconds)
1. `build_encounter_tool(party_size, party_level, difficulty)` for a starting
   composition. **Caveat:** it uses the 2014 DMG XP budgets; the campaign is SRD
   2024. Treat it as a sanity check, not gospel — cross-check monster CR vs
   `SRD_2024_MONSTERS.md`. Never award XP (milestone leveling).
2. Pick the target: `easy / medium / hard / deadly`. Default for a real fight:
   **hard**, unless the table wants it gentler.
3. Write 2–3 interactive terrain features and each enemy's **goal, tactics, and
   retreat/surrender condition** — combat should not be HP trading.
4. Non-lethal/talk paths must cost comparable *weight* (see `DM_LOOP.md` or `DM_CORE.md`).

## After the fight (2 minutes)
Fill the entry below while it's fresh. The last line is the point: **verdict**.

---

## Entry template
```
### <Fight name> — Session <n>, <in-game date>
- Party: <PCs + levels>   Target: <difficulty>   Builder said: <budget/result>
- Enemies: <name ×n, CR, source>
- Terrain features: <1> / <2> / <3>
- Enemy goals & tactics: <...>   Retreat/surrender when: <...>
- Outcome: <rounds> rounds; PCs downed: <who, when>; resources burned: <slots, HP, items>
- Non-combat path taken/offered: <...>
- **Verdict:** too easy | about right | too hard — <one line why>
- Adjust next time: <...>
```

---

## Entries
_(none yet — first real fight goes here)_
