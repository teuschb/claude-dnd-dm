# SRD 2024 Player Options — Reference

Fetched directly from the official free SRD 5.2 API (dnd5eapi.co) because 
dm20-protocol's built-in `get_race_info`/`get_class_info` tools don't surface 
full trait/feature descriptions (a bug in the installed tool, not a data gap).

**Known dm20-protocol bugs fixed via the custom rulebook overlays**
(`templates/rulebooks/custom/`):
1. Species data was silently 2014-era (Half-Elf/Half-Orc instead of Goliath/Orc) —
   fixed by `srd_2024_species_corrections.json`.
2. Class **level-by-level features** were also silently 2014-era (e.g. Ranger got
   2014's "Natural Explorer" instead of 2024's Weapon Mastery/Deft Explorer) even
   though class shells (hit die, saves, subclass names) were correctly 2024 —
   fixed by `srd_2024_class_progression.json`, rebuilt from the live API for all
   12 classes, levels 1–20 (overlay v2.0).
3. The SRD only ships 4 backgrounds (Acolyte, Criminal, Sage, Soldier); the other
   12 from the full 2024 PHB (Artisan, Charlatan, Entertainer, Farmer, Guard,
   Guide, Hermit, Merchant, Noble, Sailor, Scribe, Wayfarer) were added via
   `srd_2024_background_additions.json` from a manually-verified transcription.

**Remaining known gap:** dm20-protocol doesn't model background-granted ability
score increases or Origin Feats at all (a 2024 PHB mechanic) — these get applied
manually when finalizing a character sheet instead of automatically. Spell-slot
tables per class level also aren't populated by the overlay (the live API's
slot-table endpoint is broken), so caster spell slots need to be set manually
too until that's fetched from an authoritative source.

## Species (Races)

**The 9 official SRD 2024 species for this campaign are:** Dragonborn, Dwarf, Elf, Gnome,
**Goliath**, Halfling, Human, **Orc**, Tiefling.

dm20-protocol's built-in SRD 2024 race data has a bug — it was silently loading 2014-era
species (Half-Elf, Half-Orc) instead of the real 2024 list. Fixed via a custom rulebook
overlay (`templates/rulebooks/custom/srd_2024_species_corrections.json`)
adding real Goliath and Orc data. **Half-Elf and Half-Orc are house-ruled out of this
campaign** — they're 2014 leftovers, not valid 2024 options, and won't be offered or used
for character creation here even though the tool would still technically accept them.

### Dragonborn
**Size:** Medium  **Speed:** 30 ft.

- **Darkvision (60 ft.):** You have Darkvision with a range of 60 feet.
- **Draconic Flight:** When you reach character level 5, you can channel draconic magic to give yourself temporary flight. As a Bonus Action, you sprout spectral wings on your back that last for 10 minutes or until you retract the wings (no action required) or have the Incapacitated condition. During that time, you have a Fly Speed equal to your Speed. Your wings appear to be made of the same energy as your Breath Weapon. Once you use this trait, you can't use it again until you finish a Long Rest.

### Dwarf
**Size:** Medium  **Speed:** 30 ft.

- **Darkvision (120 ft.):** You have Darkvision with a range of 120 feet.
- **Dwarven Resilience:** You have Resistance to Poison damage. You also have Advantage on saving throws you make to avoid or end the Poisoned condition.
- **Dwarven Toughness:** Your Hit Point maximum increases by 1, and it increases by 1 again whenever you gain a level.
- **Stonecunning:** As a Bonus Action, you gain Tremorsense with a range of 60 feet for 10 minutes. You must be on a stone surface or touching a stone surface to use this Tremorsense. The stone can be natural or worked.
You can use this Bonus Action a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest.

### Elf
**Size:** Medium  **Speed:** 30 ft.

- **Darkvision (60 ft.):** You have Darkvision with a range of 60 feet.
- **Elven Lineage:** You are part of a lineage that grants you supernatural abilities. Choose a lineage from the Elven Lineages table. You gain the level 1 benefit of that lineage.
When you reach character levels 3 and 5, you learn a higher-level spell, as shown on the table.
You always have that spell prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast the spell using any spell slots you have of the appropriate level.
Elven Lineages
Drow
Level 1. The range of your Darkvision increases to 120 feet. You also know the Dancing Lights cantrip.
Level 3. Faerie Fire
Level 5. Darkness
High Elf
Level 1. You know the Prestidigitation cantrip. Whenever you finish a Long Rest, you can replace that cantrip with a different cantrip from the Wizard spell list.
Level 3. Detect Magic
Level 5. Misty Step
Wood Elf
Level 1. Your Speed increases to 35 feet. You also know the Druidcraft cantrip.
Level 3. Longstrider
Level 5. Pass without Trace
Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait (choose the ability when you select the lineage).
- **Fey Ancestry:** You have Advantage on saving throws you make to avoid or end the Charmed condition.
- **Keen Senses:** You have proficiency in the Insight, Perception, or Survival skill.
- **Trance:** You don't need to sleep, and magic can't put you to sleep. You can finish a Long Rest in 4 hours if you spend those hours in a trancelike meditation, during which you retain consciousness.

### Gnome
**Size:** Small  **Speed:** 30 ft.

- **Darkvision (60 ft.):** You have Darkvision with a range of 60 feet.
- **Gnomish Cunning:** You have Advantage on Intelligence, Wisdom, and Charisma saving throws.
- **Gnomish Lineage:** You are part of a lineage that grants you supernatural abilities. Choose one of the following options; whichever one you choose, Intelligence, Wisdom, or Charisma is your spellcasting ability for the spells you cast with this trait (choose the ability when you select the lineage):
Forest Gnome. You know the Minor Illusion cantrip. You also always have the Speak with Animals spell prepared. You can cast it without a spell slot a number of times equal to your Proficiency Bonus, and you regain all expended uses when you finish a Long Rest. You can also use any spell slots you have to cast the spell.
Rock Gnome. You know the Mending and Prestidigitation cantrips. In addition, you can spend 10 minutes casting Prestidigitation to create a Tiny clockwork device (AC 5, 1 HP), such as a toy, fire starter, or music box. When you create the device, you determine its function by choosing one effect from Prestidigitation; the device produces that effect whenever you or another creature takes a Bonus Action to activate it with a touch. If the chosen effect has options within it, you choose one of those options for the device when you create it.
For example, if you choose the spell's ignite-extinguish effect, you determine whether the device ignites or extinguishes fire; the device doesn't do both. You can have three such devices in existence at a time, and each falls apart 8 hours after its creation or when you dismantle it with a touch as a Utilize action.

### ~~Half-Elf~~ / ~~Half-Orc~~ — excluded
2014 leftovers, not real 2024 species. Not offered or used for character creation in this campaign.

### Goliath
**Size:** Medium  **Speed:** 35 ft.

- **Giant Ancestry:** You are descended from Giants. Choose one benefit (Cloud's Jaunt: teleport 30 ft as a Bonus Action; Fire's Burn: +1d10 Fire on hit; Frost's Chill: +1d6 Cold on hit and slow target; Hill's Tumble: knock a Large-or-smaller target prone on hit; Stone's Endurance: reaction to reduce damage taken; Storm's Thunder: reaction to deal 1d8 Thunder to a nearby attacker). Usable a number of times equal to your Proficiency Bonus, regained on a Long Rest.
- **Large Form:** Starting at level 5, become Large as a Bonus Action for 10 minutes — Advantage on Strength checks, +10 ft Speed. Once per Long Rest.
- **Powerful Build:** Advantage on checks to end the Grappled condition; count as one size larger for carrying capacity.

### Orc
**Size:** Medium  **Speed:** 30 ft.

- **Adrenaline Rush:** Dash as a Bonus Action, gaining Temporary HP equal to Proficiency Bonus. Uses equal to Proficiency Bonus, regained on a Short or Long Rest.
- **Darkvision (120 ft.):** You have Darkvision with a range of 120 feet.
- **Relentless Endurance:** When reduced to 0 HP but not killed outright, drop to 1 HP instead. Once per Long Rest.

### Halfling
**Size:** Small  **Speed:** 30 ft.

- **Brave:** You have Advantage on saving throws you make to avoid or end the Frightened condition.
- **Halfling Nimbleness:** You can move through the space of any creature that is a size larger than you, but you can't stop in the same space.
- **Luck:** When you roll a 1 on the d20 of a D20 Test, you can reroll the die, and you must use the new roll.
- **Naturally Stealthy:** You can take the Hide action even when you are obscured only by a creature that is at least one size larger than you.

### Human
**Size:** Medium  **Speed:** 30 ft.

- **Resourceful:** You gain Heroic Inspiration whenever you finish a Long Rest.
- **Skillful:** You gain proficiency in one skill of your choice.
- **Versatile:** You gain an Origin feat of your choice (see "Feats"). Skilled is recommended.

### Tiefling
**Size:** Small or Medium (your choice)  **Speed:** 30 ft.

- **Darkvision (60 ft.):** You have Darkvision with a range of 60 feet.
- **Fiendish Legacy:** You are the recipient of a legacy that grants you supernatural abilities. Choose a legacy from the Fiendish Legacies table. You gain the level 1 benefit of the chosen legacy.
When you reach character levels 3 and 5, you learn a higher-level spell, as shown on the table.
You always have that spell prepared. You can cast it once without a spell slot, and you regain the ability to cast it in that way when you finish a Long Rest. You can also cast the spell using any spell slots you have of the appropriate level.
Intelligence, Wisdom, or Charisma is your spell-casting ability for the spells you cast with this trait (choose the ability when you select the legacy).
Fiendish Legacies
Abyssal.
Level 1. You have Resistance to Poison damage. You also know the Poison Spray cantrip.
Level 3. Ray of Sickness
Level 5. Hold Person
Chthonic.
Level 1. You have Resistance to Necrotic damage. You also know the Chill Touch cantrip.
Level 3. False Life
Level 5. Ray of Enfeeblement
Infernal.
Level 1. You have Resistance to Fire damage. You also know the Fire Bolt cantrip.
Level 3. Hellish Rebuke
Level 5. Darkness
- **Otherworldly Presence:** You know the Thaumaturgy cantrip. When you cast it with this trait, the spell uses the same spellcasting ability you use for your Fiendish Legacy trait.


## Classes

### Barbarian
**Hit Die:** d12  **Saves:** STR, CON

**Proficiencies:** Light Armor, Medium Armor, Shields, Simple Weapons, Martial Weapons, Saving Throw: STR, Saving Throw: CON
**Choose:** Choose 2: Animal Handling, Athletics, Intimidation, Nature, Perception, or Survival
**Starting Equipment:** Choose A or B: (A) Greataxe, 4 Handaxes, Explorer's Pack, 15 GP; or (B) 75 GP

**Class table (Rages / Rage Damage / Weapon Mastery by level):**
| Level | PB | Features | Rages | Rage Damage | Weapon Mastery |
|---|---|---|---|---|---|
| 1 | +2 | Rage, Unarmored Defense, Weapon Mastery | 2 | +2 | 2 |
| 2 | +2 | Danger Sense, Reckless Attack | 2 | +2 | 2 |
| 3 | +2 | Barbarian Subclass, Primal Knowledge | 3 | +2 | 2 |
| 4 | +2 | Ability Score Improvement | 3 | +2 | 3 |
| 5 | +3 | Extra Attack, Fast Movement | 3 | +2 | 3 |
| 6 | +3 | Subclass Feature | 4 | +2 | 3 |
| 7 | +3 | Feral Instinct, Instinctive Pounce | 4 | +2 | 3 |
| 8 | +3 | Ability Score Improvement | 4 | +2 | 3 |
| 9 | +4 | Brutal Strike | 4 | +3 | 3 |
| 10 | +4 | Subclass Feature | 4 | +3 | 4 |
| 11 | +4 | Relentless Rage | 4 | +3 | 4 |
| 12 | +4 | Ability Score Improvement | 5 | +3 | 4 |
| 13 | +5 | Improved Brutal Strike | 5 | +3 | 4 |
| 14 | +5 | Subclass Feature | 5 | +3 | 4 |
| 15 | +5 | Persistent Rage | 5 | +3 | 4 |
| 16 | +5 | Ability Score Improvement | 5 | +4 | 4 |
| 17 | +6 | Improved Brutal Strike | 6 | +4 | 4 |
| 18 | +6 | Indomitable Might | 6 | +4 | 4 |
| 19 | +6 | Epic Boon | 6 | +4 | 4 |
| 20 | +6 | Primal Champion | 6 | +4 | 4 |

**Features (all levels):**
- **Rage** (level 1): You can imbue yourself with a primal power called Rage, a force that grants you extraordinary might and resilience. You can enter it as a Bonus Action if you aren't wearing Heavy Armor. You can enter your Rage the number of times shown for your Barbarian level in the Rages column. You regain one expended use when you finish a Short Rest, and you regain all expended uses when you finish a Long Rest.
  While active: **Damage Resistance** — Resistance to Bludgeoning, Piercing, and Slashing damage. **Rage Damage** — bonus damage on Strength-based weapon/Unarmed Strike hits, per the Rage Damage column. **Strength Advantage** — Advantage on Strength checks and saving throws. **No Concentration or Spells** — can't maintain Concentration or cast spells. **Duration** — lasts until the end of your next turn, ends early if you don Heavy Armor or are Incapacitated; extend it each round by making an attack roll against an enemy, forcing an enemy to save, or taking a Bonus Action to extend it. Maintainable up to 10 minutes total.
- **Unarmored Defense** (level 1): While not wearing armor, base AC = 10 + Dexterity + Constitution modifiers. A Shield doesn't break this benefit.
- **Weapon Mastery** (level 1): Use the mastery properties of two kinds of Simple or Martial Melee weapons of your choice (e.g. Greataxes and Handaxes). Change one choice whenever you finish a Long Rest. Gain more kinds at higher levels per the Weapon Mastery column.
- **Danger Sense** (level 2): Advantage on Dexterity saving throws unless Incapacitated.
- **Reckless Attack** (level 2): On your first attack roll of the turn, you can attack recklessly: Advantage on Strength-based attack rolls until the start of your next turn, but attack rolls against you have Advantage during that time.
- **Barbarian Subclass** (level 3): Choose Path of the Berserker, Path of the Wild Heart, Path of the World Tree, or Path of the Zealot. You gain each subclass feature at your Barbarian level or lower.
- **Primal Knowledge** (level 3): Gain proficiency in another skill from the level-1 Barbarian skill list. While raging, you can make an ability check using Acrobatics, Intimidation, Perception, Stealth, or Survival as a Strength check instead of its normal ability.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Extra Attack** (level 5): Attack twice instead of once when you take the Attack action.
- **Fast Movement** (level 5): Speed +10 ft while not wearing Heavy Armor.
- **Feral Instinct** (level 7): Advantage on Initiative rolls.
- **Instinctive Pounce** (level 7): As part of the Bonus Action to enter Rage, you can move up to half your Speed.
- **Brutal Strike** (level 9): If you use Reckless Attack, you can forgo Advantage on one Strength-based attack roll (that roll mustn't have Disadvantage). If it hits, the target takes an extra 1d10 damage of the weapon/Unarmed Strike's type, and you cause one Brutal Strike effect of your choice: **Forceful Blow** — target pushed 15 ft away, you can then move up to half Speed toward it without Opportunity Attacks; **Hamstring Blow** — target's Speed -15 ft until start of your next turn (only the most recent Hamstring Blow applies).
- **Relentless Rage** (level 11): If you drop to 0 HP while raging and don't die outright, make a DC 10 Constitution save; success sets your HP to twice your Barbarian level instead. DC +5 each subsequent use, resets to 10 on a Short or Long Rest.
- **Improved Brutal Strike** (level 13): Adds two more Brutal Strike effects: **Staggering Blow** — target has Disadvantage on its next save and can't make Opportunity Attacks until start of your next turn; **Sundering Blow** — before the start of your next turn, the next attack roll by another creature against the target gets a +5 bonus (only one Sundering Blow bonus at a time).
- **Persistent Rage** (level 15): When you roll Initiative, you can regain all expended Rage uses (once per Long Rest). Your Rage now lasts 10 minutes automatically without needing to extend it each round; ends early only on Unconscious (not just Incapacitated) or donning Heavy Armor.
- **Improved Brutal Strike** (level 17): Brutal Strike's extra damage increases to 2d10, and you can apply two different Brutal Strike effects at once.
- **Indomitable Might** (level 18): If your Strength check or save total is less than your Strength score, use that score instead.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Irresistible Offense recommended.
- **Primal Champion** (level 20): Strength and Constitution scores each increase by 4, to a maximum of 25.

**Subclass — Path of the Berserker:** Barbarians who walk the Path of the Berserker direct their Rage primarily toward violence. Their path is one of untrammeled fury, and they thrill in the chaos of battle as they allow their Rage to seize and empower them.
- **Frenzy** (level 3): If you use Reckless Attack while raging, deal extra damage to the first target hit on your turn with a Strength-based attack — roll a number of d6s equal to your Rage Damage bonus (same damage type as the weapon/Unarmed Strike).
- **Mindless Rage** (level 6): Immunity to Charmed and Frightened while raging; either condition ends on you when you enter Rage.
- **Retaliation** (level 10): When you take damage from a creature within 5 ft, you can use a Reaction to make one melee attack against it.
- **Intimidating Presence** (level 14): As a Bonus Action, each creature of your choice in a 30-ft Emanation must make a Wisdom save (DC 8 + Strength modifier + Proficiency Bonus); on a failure, Frightened 1 minute, repeating the save at the end of each of its turns. Once per Long Rest, restorable by expending a use of Rage (no action required).

**Subclass — Path of the Wild Heart:** Barbarians who follow the Path of the Wild Heart view themselves as kin to animals. These Barbarians learn magical means to communicate with animals, and their Rage heightens their connection to animals as it fills them with supernatural might.
- **Animal Speaker** (level 3): Cast Beast Sense and Speak with Animals, but only as Rituals. Wisdom is your spellcasting ability for them.
- **Rage of the Wilds** (level 3): Whenever you activate your Rage, choose one: **Bear** — Resistance to every damage type except Force, Necrotic, Psychic, and Radiant while raging; **Eagle** — when you activate Rage, take the Disengage and Dash actions as part of that Bonus Action, and while raging you can take a Bonus Action to take both actions again; **Wolf** — while raging, allies have Advantage on attack rolls against any enemy of yours within 5 ft of you.
- **Aspect of the Wilds** (level 6): Choose one (changeable on a Long Rest): **Owl** — Darkvision 60 ft, or +60 ft range if you already have it; **Panther** — Climb Speed equal to your Speed; **Salmon** — Swim Speed equal to your Speed.
- **Nature Speaker** (level 10): Cast Commune with Nature, but only as a Ritual. Wisdom is your spellcasting ability for it.
- **Power of the Wilds** (level 14): Whenever you activate your Rage, choose one: **Falcon** — Fly Speed equal to your Speed while raging if unarmored; **Lion** — while raging, enemies within 5 ft of you have Disadvantage on attack rolls against targets other than you or another Barbarian with this option active; **Ram** — while raging, a melee hit against a Large-or-smaller creature can give it the Prone condition.

**Subclass — Path of the World Tree:** Barbarians who follow the Path of the World Tree connect with the cosmic tree Yggdrasil through their Rage. This tree grows among the Outer Planes, connecting them to each other and the Material Plane. These Barbarians draw on the tree's magic for vitality and as a means of dimensional travel.
- **Vitality of the Tree** (level 3): **Vitality Surge** — when you activate Rage, gain Temp HP equal to your Barbarian level. **Life-Giving Force** — at the start of each turn while raging, choose another creature within 10 ft to gain Temp HP equal to a number of d6s (equal to your Rage Damage bonus) added together; unused Temp HP vanishes when Rage ends.
- **Branches of the Tree** (level 6): Whenever a creature you can see starts its turn within 30 ft of you while raging, you can take a Reaction to summon spectral branches around it — Strength save (DC 8 + Strength modifier + Proficiency Bonus) or be teleported to an unoccupied space within 5 ft of you (or nearest unoccupied space); you can then reduce its Speed to 0 until end of the current turn.
- **Battering Boots** (level 10): During your turn, your reach is 10 ft greater with any Melee weapon with the Heavy or Versatile property; on a hit with such a weapon on your turn, you can activate the Push or Topple mastery property in addition to a different mastery property you're using.
- **Travel along the Tree** (level 14): When you activate Rage, and as a Bonus Action while raging, teleport up to 60 ft to an unoccupied space you can see. Once per Rage, extend the range to 150 ft and bring up to six willing creatures within 10 ft of you, each teleporting to an unoccupied space of your choice within 10 ft of your destination.

**Subclass — Path of the Zealot:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

---

### Bard
**Hit Die:** d8  **Saves:** DEX, CHA
  **Spellcasting:** CHA

**Proficiencies:** Light Armor, Simple Weapons, Saving Throw: DEX, Saving Throw: CHA
**Choose:** Choose any 3 skills
**Choose:** Three musical instruments of your choice
**Starting Equipment:** Choose A or B: (A) Leather Armor, 2 Daggers, a Musical Instrument, Entertainer's Pack, 19 GP; or (B) 90 GP

**Class table (Bardic Die / Cantrips / Prepared Spells by level; spell slots 1-9 follow standard full-caster progression):**
| Level | PB | Features | Bardic Die | Cantrips | Prepared |
|---|---|---|---|---|---|
| 1 | +2 | Bardic Inspiration, Spellcasting | d6 | 2 | 4 |
| 2 | +2 | Expertise, Jack of All Trades | d6 | 2 | 5 |
| 3 | +2 | Bard Subclass | d6 | 2 | 6 |
| 4 | +2 | Ability Score Improvement | d6 | 3 | 7 |
| 5 | +3 | Font of Inspiration | d8 | 3 | 9 |
| 6 | +3 | Subclass Feature | d8 | 3 | 10 |
| 7 | +3 | Countercharm | d8 | 3 | 11 |
| 8 | +3 | Ability Score Improvement | d8 | 3 | 12 |
| 9 | +4 | Expertise | d8 | 3 | 14 |
| 10 | +4 | Magical Secrets | d10 | 4 | 15 |
| 11 | +4 | — | d10 | 4 | 16 |
| 12 | +4 | Ability Score Improvement | d10 | 4 | 16 |
| 13 | +5 | — | d10 | 4 | 17 |
| 14 | +5 | Subclass Feature | d10 | 4 | 17 |
| 15 | +5 | — | d12 | 4 | 18 |
| 16 | +5 | Ability Score Improvement | d12 | 4 | 18 |
| 17 | +6 | — | d12 | 4 | 19 |
| 18 | +6 | Superior Inspiration | d12 | 4 | 20 |
| 19 | +6 | Epic Boon | d12 | 4 | 21 |
| 20 | +6 | Words of Creation | d12 | 4 | 22 |

**Features (all levels):**

- **Bardic Inspiration** (level 1): You can supernaturally inspire others through words, music, or dance. This inspiration is repre- sented by your Bardic Inspiration die, which is a d6.
  Using Bardic Inspiration. As a Bonus Action, you can inspire another creature within 60 feet of your- self who can see or hear you. That creature gains
one of your Bardic Inspiration dice. A creature can have only one Bardic Inspiration die at a time.
  Once within the next hour when the creature fails a D20 Test, the creature can roll the Bardic Inspira- tion die and add the number rolled to the d20, po- tentially turning the failure into a success. A Bardic Inspiration die is expended when it's rolled.
  Number of Uses. You can confer a Bardic Inspira- tion die a number of times equal to your Charisma modifier (minimum of once), and you regain all ex- pended uses when you finish a Long Rest.
  At Higher Levels. Your Bardic Inspiration die changes when you reach certain Bard levels, as shown in the Bardic Die column of the Bard Fea- tures table. The die becomes a d8 at level 5, a d10 at level 10, and a d12 at level 15.
- **Spellcasting** (level 1): You have learned to cast spells through your bardic arts. See "Spells" for the rules on spellcasting. The information below details how you use those rules with Bard spells, which appear in the Bard spell list later in the class's description.
  Cantrips. You know two cantrips of your choice from the Bard spell list. Dancing Lights and Vicious Mockery are recommended.
  Whenever you gain a Bard level, you can replace one of your cantrips with another cantrip of your choice from the Bard spell list.
  When you reach Bard levels 4 and 10, you learn another cantrip of your choice from the Bard spell list, as shown in the Cantrips column of the Bard Features table.
  Spell Slots. The Bard Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you fin- ish a Long Rest.
  Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose four level 1 spells from the Bard spell list. Charm Person, Color Spray, Dissonant Whispers, and Healing Word are recommended.
  The number of spells on your list increases as you gain Bard levels, as shown in the Prepared Spells column of the Bard Features table. Whenever that number increases, choose additional spells from the Bard spell list until the number of spells on your list matches the number on the table. The chosen spells must be of a level for which you have spell slots.
For example, if you're a level 3 Bard, your list of
prepared spells can include six spells of levels 1 and 2 in any combination.
  If another Bard feature gives you spells that you always have prepared, those spells don't count against the number of spells you can prepare with this feature, but those spells otherwise count as Bard spells for you.
  Changing Your Prepared Spells. Whenever you gain a Bard level, you can replace one spell on your list with another Bard spell for which you have spell slots.
  Spellcasting Ability. Charisma is your spellcast- ing ability for your Bard spells.
  Spellcasting Focus. You can use a Musical Instru- ment as a Spellcasting Focus for your Bard spells.
- **Expertise** (level 2): You gain Expertise (see "Rules Glossary") in two of your skill proficiencies of your choice. Performance and Persuasion are recommended if you have profi- ciency in them.
  At Bard level 9, you gain Expertise in two more of your skill proficiencies of your choice.
- **Jack of All Trades** (level 2): You can add half your Proficiency Bonus (round down) to any ability check you make that uses a skill proficiency you lack and that doesn't otherwise use your Proficiency Bonus.
  For example, if you make a Strength (Athletics) check and lack Athletics proficiency, you can add half your Proficiency Bonus to the check.
- **Bard Subclass** (level 3): You gain a Bard subclass of your choice — College of Dance, College of Glamour, College of Lore, or College of Valor. A subclass is a specialization that grants you features at certain Bard levels. For the rest of your career, you gain each of your subclass's features that are of your Bard level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Font of Inspiration** (level 5): You now also regain all expended Bardic Inspiration uses on a Short Rest (not just Long Rest). You can also expend a spell slot (no action required) to regain one expended use of Bardic Inspiration.
- **Countercharm** (level 7): If you or a creature within 30 ft fails a save against an effect that would apply Charmed or Frightened, you can take a Reaction to force a reroll of that save with Advantage.
- **Expertise** (level 9, second application): Gain Expertise in two more skill proficiencies of your choice (see level 2 Expertise above for the first application).
- **Magical Secrets** (level 10): Whenever the Prepared Spells number increases (including this level), you can choose new prepared spells from the Bard, Cleric, Druid, or Wizard spell lists; they count as Bard spells for you. You can also replace a prepared spell with one from those lists.
- **Superior Inspiration** (level 18): When you roll Initiative, regain expended Bardic Inspiration uses until you have at least two.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Spell Recall recommended.
- **Words of Creation** (level 20): You always have Power Word Heal and Power Word Kill prepared. When you cast either, you can target a second creature within 10 ft of the first target.

**Subclass — College of Lore:** Bards of the College of Lore collect spells and secrets from diverse sources, such as scholarly tomes, mystical rites, and peasant tales. The college's members gather in libraries and universities to share their lore with one another. They also meet at festivals or affairs of state, where they can expose corruption, unravel lies, and poke fun at self-important figures of authority.
- **Bonus Proficiencies** (level 3): You gain proficiency with three skills of your choice.
- **Cutting Words** (level 3): When a creature that you can see within 60 feet of yourself makes a damage roll or succeeds on an ability check or attack roll, you can take a Reaction to expend one use of your Bardic Inspiration; roll your Bardic Inspiration die, and subtract the number rolled from the creature's roll, reducing the damage or potentially turning the success into a failure.
- **Magical Discoveries** (level 6): You learn two spells of your choice from the Cleric, Druid, or Wizard spell list (or any combination). A spell you choose must be a cantrip or a spell for which you have spell slots. You always have the chosen spells prepared, and whenever you gain a Bard level, you can replace one of the spells with another that meets these requirements.
- **Peerless Skill** (level 14): When you make an ability check or attack roll and fail, you can expend one use of Bardic Inspiration; roll the Bardic Inspiration die, and add the number rolled to the d20, potentially turning a failure into a success. On a failure, the Bardic Inspiration isn't expended.

**Subclass — College of Dance:**
- **Dazzling Footwork** (level 3): While you aren't wearing armor or wielding a Shield: Dance Virtuoso (Advantage on Charisma (Performance) checks involving dancing); Unarmored Defense (base AC = 10 + Dexterity + Charisma modifiers); Agile Strikes (when you expend a use of Bardic Inspiration as part of an action/Bonus Action/Reaction, you can make one Unarmed Strike as part of it); Bardic Damage (use Dexterity for Unarmed Strike attack rolls, and can deal Bludgeoning damage equal to a Bardic Inspiration die roll + Dexterity modifier instead of normal damage, without expending the die).
- **Inspiring Movement** (level 6): When an enemy you can see ends its turn within 5 feet of you, you can take a Reaction and expend one use of Bardic Inspiration to move up to half your Speed; one ally within 30 feet can also move up to half their Speed as a Reaction. None of this movement provokes Opportunity Attacks.
- **Tandem Footwork** (level 6): When you roll Initiative (and lack the Incapacitated condition), you can expend one use of Bardic Inspiration; roll the die, and you and each ally within 30 feet who can see or hear you gain a bonus to Initiative equal to the number rolled.
- **Leading Evasion** (level 14): When subjected to an effect allowing a Dexterity save for half damage, you take no damage on a success and half on a failure instead. Creatures within 5 feet of you making the same save can share this benefit. Doesn't work if you're Incapacitated.

**Subclass — College of Glamour:**
- **Beguiling Magic** (level 3): You always have Charm Person and Mirror Image prepared. Immediately after casting an Enchantment or Illusion spell with a spell slot, you can force a creature within 60 feet to make a WIS save vs your spell save DC. Fail: Charmed or Frightened (your choice) 1 min, repeats save at end of turns. Once per Long Rest, restorable by expending a Bardic Inspiration use.
- **Mantle of Inspiration** (level 3): As a Bonus Action, expend a Bardic Inspiration use and roll the die; choose creatures within 60 ft up to your CHA modifier (min. 1); each gains Temp HP equal to 2x the roll, then can use a Reaction to move up to their Speed without Opportunity Attacks.
- **Mantle of Majesty** (level 6): You always have Command prepared. As a Bonus Action, cast it without a spell slot, taking on an unearthly appearance for 1 min or until Concentration ends; during this time you can cast Command again as a Bonus Action without a slot, and Charmed creatures auto-fail their save. Once per Long Rest, restorable with a level 3+ slot.
- **Unbreakable Majesty** (level 14): As a Bonus Action, assume a majestic presence for 1 min or until Incapacitated; whenever a creature hits you with an attack roll for the first time on a turn, it must succeed a CHA save vs your spell save DC or the attack misses instead. Once per Short/Long Rest.

**Subclass — College of Valor:**
- **Combat Inspiration** (level 3): A creature holding a Bardic Inspiration die from you can use it for: Defense (Reaction when hit by an attack, add the roll to AC against that attack, possibly causing a miss) or Offense (immediately after hitting with an attack, add the roll to the damage).
- **Martial Training** (level 3): Gain proficiency with Martial Weapons and training with Medium Armor and Shields; can use a Simple or Martial weapon as a Spellcasting Focus for Bard spells.
- **Extra Attack** (level 6): Attack twice instead of once when you take the Attack action; can cast a cantrip with a casting time of an action in place of one of those attacks.
- **Battle Magic** (level 14): After casting a spell with a casting time of an action, make one weapon attack as a Bonus Action.

---

### Cleric
**Hit Die:** d8  **Saves:** WIS, CHA
  **Spellcasting:** WIS

**Proficiencies:** Light Armor, Medium Armor, Shields, Simple Weapons, Saving Throw: WIS, Saving Throw: CHA
**Choose:** Choose 2: History, Insight, Medicine, Persuasion, or Religion
**Starting Equipment:** Choose A or B: (A) Chain Shirt, Shield, Mace, Holy Symbol, Priest's Pack, 7 GP; or (B) 110 GP

**Class table (Channel Divinity / Cantrips / Prepared Spells by level; spell slots 1-9 follow standard full-caster progression):**
| Level | PB | Features | Channel Divinity | Cantrips | Prepared |
|---|---|---|---|---|---|
| 1 | +2 | Spellcasting, Divine Order | — | 3 | 4 |
| 2 | +2 | Channel Divinity | 2 | 3 | 5 |
| 3 | +2 | Cleric Subclass | 2 | 3 | 6 |
| 4 | +2 | Ability Score Improvement | 2 | 4 | 7 |
| 5 | +3 | Sear Undead | 2 | 4 | 9 |
| 6 | +3 | Subclass Feature | 3 | 4 | 10 |
| 7 | +3 | Blessed Strikes | 3 | 4 | 11 |
| 8 | +3 | Ability Score Improvement | 3 | 4 | 12 |
| 9 | +4 | — | 3 | 4 | 14 |
| 10 | +4 | Divine Intervention | 3 | 5 | 15 |
| 11 | +4 | — | 3 | 5 | 16 |
| 12 | +4 | Ability Score Improvement | 3 | 5 | 16 |
| 13 | +5 | — | 3 | 5 | 17 |
| 14 | +5 | Improved Blessed Strikes | 3 | 5 | 17 |
| 15 | +5 | — | 3 | 5 | 18 |
| 16 | +5 | Ability Score Improvement | 3 | 5 | 18 |
| 17 | +6 | Subclass Feature | 3 | 5 | 19 |
| 18 | +6 | — | 4 | 5 | 20 |
| 19 | +6 | Epic Boon | 4 | 5 | 21 |
| 20 | +6 | Greater Divine Intervention | 4 | 5 | 22 |

**Features (all levels):**
- **Spellcasting** (level 1): Cantrips — know 3 of your choice from the Cleric list (Guidance, Sacred Flame, Thaumaturgy recommended); replace one on each level-up; learn another at levels 4 and 10. Prepared Spells — start with 4 level-1 spells (Bless, Cure Wounds, Guiding Bolt, Shield of Faith recommended); the list grows per the table; can be freely re-chosen on a Long Rest. Wisdom is your spellcasting ability; a Holy Symbol works as a Spellcasting Focus.
- **Divine Order** (level 1): Choose one sacred role — **Protector** (proficiency with Martial weapons, training with Heavy armor) or **Thaumaturge** (one extra Cleric cantrip; bonus equal to your Wisdom modifier, minimum +1, to Intelligence (Arcana or Religion) checks).
- **Channel Divinity** (level 2): Two uses (regain one on a Short Rest, all on a Long Rest; more at higher levels per the table). If an effect needs a save, DC = your spell save DC. Effects known at level 2:
  - **Divine Spark**: as a Magic action, target a creature within 30 ft — roll 1d8 + Wisdom modifier, and either restore that many HP to it or force a Constitution save (fail: Necrotic or Radiant damage, your choice, equal to the total; success: half, rounded down). Extra d8 at Cleric levels 7 (2d8), 13 (3d8), 18 (4d8).
  - **Turn Undead**: as a Magic action, each Undead of your choice within 30 ft makes a Wisdom save; on a failure, Frightened + Incapacitated for 1 minute (tries to flee you each turn); ends early on damage, your own Incapacitated condition, or your death.
- **Cleric Subclass** (level 3): Choose Life, Light, Trickery, or War Domain. You gain each subclass feature at your Cleric level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Sear Undead** (level 5): Whenever you use Turn Undead, roll a number of d8s equal to your Wisdom modifier (minimum 1d8); each Undead that fails its save takes Radiant damage equal to the total (doesn't end the turn effect).
- **Blessed Strikes** (level 7): Choose one (if you'd get either option twice from an older-book subclass, only apply it once): **Divine Strike** — once per turn on a weapon attack hit, extra 1d8 Necrotic or Radiant damage (your choice); **Potent Spellcasting** — add your Wisdom modifier to damage dealt by Cleric cantrips.
- **Divine Intervention** (level 10): As a Magic action, choose any Cleric spell of level 5 or lower that doesn't require a Reaction; cast it without a spell slot or Material components. Once per Long Rest.
- **Improved Blessed Strikes** (level 14): Whichever Blessed Strikes option you chose improves — **Divine Strike** extra damage becomes 2d8; **Potent Spellcasting** lets you grant Temp HP equal to twice your Wisdom modifier to yourself or a creature within 60 ft when a Cleric cantrip deals damage.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Fate recommended.
- **Greater Divine Intervention** (level 20): When using Divine Intervention, you may choose Wish as the spell; doing so means you can't use Divine Intervention again until you finish 2d4 Long Rests.

**Subclass — Life Domain:** The Life Domain focuses on the positive energy that helps sustain all life in the multiverse. Clerics who tap into this domain are masters of healing, using that life force to cure many hurts.
  Existence itself relies on the positive energy associated with this domain, so a Cleric of almost any religious tradition might choose it. This domain is particularly associated with agricultural deities, gods of healing or endurance, and gods of home and community. Religious orders of healing also seek the magic of this domain.
- **Life Domain Spells** (level 3, and levels 5/7/9): Always prepared — Aid, Bless, Cure Wounds, Lesser Restoration (L3); Mass Healing Word, Revivify (L5); Aura of Life, Death Ward (L7); Greater Restoration, Mass Cure Wounds (L9).
- **Disciple of Life** (level 3): When a spell you cast with a spell slot restores HP to a creature, that creature regains additional HP equal to 2 plus the spell slot's level.
- **Preserve Life** (level 3): As a Magic action, present your Holy Symbol and expend a use of Channel Divinity to evoke healing energy equal to 5x your Cleric level; choose Bloodied creatures within 30 ft (can include you) and divide the HP among them. Can't restore a creature above half its HP maximum.
- **Blessed Healer** (level 6): Immediately after casting a spell with a spell slot that restores HP to a creature other than yourself, you regain HP equal to 2 plus the spell slot's level.
- **Supreme Healing** (level 17): When you would roll dice to restore HP with a spell or Channel Divinity, don't roll — use the highest possible number for each die instead.

**Subclass — Light Domain:** The Light Domain emphasizes the divine power to bring about blazing fire and revelation. Clerics who wield this power are enlightened souls infused with radiance and the power of their deities' discerning vision, charged with chasing away lies and burning away darkness.
- **Light Domain Spells** (level 3, and levels 5/7/9): Always prepared — Burning Hands, Faerie Fire, Scorching Ray, See Invisibility (L3); Daylight, Fireball (L5); Arcane Eye, Wall of Fire (L7); Flame Strike, Scrying (L9).
- **Radiance of the Dawn** (level 3): As a Magic action, present your Holy Symbol and expend a use of Channel Divinity to emit a flash of light in a 30-ft Emanation; dispels any magical darkness there. Each creature you choose there makes a Constitution save — fail: 2d10 + Cleric level Radiant damage; success: half.
- **Warding Flare** (level 3): When a creature you can see within 30 ft makes an attack roll, use a Reaction to impose Disadvantage on it. Uses equal to your Wisdom modifier (minimum once), regained on a Long Rest.
- **Improved Warding Flare** (level 6): Warding Flare uses regain on a Short or Long Rest instead of only Long Rest; whenever you use it, you can also give the triggering attack's target Temp HP equal to 2d6 + your Wisdom modifier.
- **Corona of Light** (level 17): As a Magic action, emit an aura of sunlight for 1 minute (or until dismissed, no action required) — Bright Light in a 60-ft radius, Dim Light 30 ft further. Enemies in the Bright Light have Disadvantage on saves against your Radiance of the Dawn and any spell dealing Fire or Radiant damage. Uses equal to your Wisdom modifier (minimum once), regained on a Long Rest.

**Subclass — Trickery Domain:** The Trickery Domain offers magic of deception, illusion, and stealth. Clerics who wield this magic are a disruptive force in the world, puncturing pride, mocking tyrants, freeing captives, and flouting hollow traditions. They prefer subterfuge and pranks to direct confrontation.
- **Trickery Domain Spells** (level 3, and levels 5/7/9): Always prepared — Charm Person, Disguise Self, Invisibility, Pass without Trace (L3); Hypnotic Pattern, Nondetection (L5); Confusion, Dimension Door (L7); Dominate Person, Modify Memory (L9).
- **Blessing of the Trickster** (level 3): As a Magic action, grant yourself or a willing creature within 30 ft Advantage on Dexterity (Stealth) checks; lasts until you finish a Long Rest or use this feature again.
- **Invoke Duplicity** (level 3): As a Bonus Action, expend a use of Channel Divinity to create a perfect visual illusion of yourself (intangible, doesn't occupy its space) in an unoccupied space within 30 ft; lasts 1 minute, ends early if dismissed (no action) or you're Incapacitated. While it persists: **Cast Spells** — cast as though you were in the illusion's space (using your own senses); **Distract** — when you and the illusion are both within 5 ft of a creature that can see it, you have Advantage on attack rolls against that creature; **Move** — as a Bonus Action, move the illusion up to 30 ft to an unoccupied space within 120 ft of you.
- **Trickster's Transposition** (level 6): Whenever you take the Bonus Action to create or move the Invoke Duplicity illusion, you can instead teleport to swap places with it.
- **Improved Duplicity** (level 17): **Shared Distraction** — you and allies attacking a creature within 5 ft of the illusion have Advantage; **Healing Illusion** — when the illusion ends, you or a creature of your choice within 5 ft of it regains HP equal to your Cleric level.

**Subclass — War Domain:** War has many manifestations. It can make heroes of ordinary people. It can be desperate and horrific, with acts of cruelty and cowardice eclipsing instances of excellence and courage. Clerics who tap into the magic of the War Domain excel in battle, inspiring others to fight the good fight or offering acts of violence as prayers.
- **War Domain Spells** (level 3, and levels 5/7/9): Always prepared — Guiding Bolt, Magic Weapon, Shield of Faith, Spiritual Weapon (L3); Crusader's Mantle, Spirit Guardians (L5); Fire Shield, Freedom of Movement (L7); Hold Monster, Steel Wind Strike (L9).
- **Guided Strike** (level 3): When you or a creature within 30 ft misses with an attack roll, expend a use of Channel Divinity to give that roll a +10 bonus (Reaction required if benefiting another creature).
- **War Priest** (level 3): As a Bonus Action, make one attack with a weapon or Unarmed Strike. Uses equal to your Wisdom modifier (minimum once), regained on a Short or Long Rest.
- **War God's Blessing** (level 6): Expend a use of Channel Divinity to cast Shield of Faith or Spiritual Weapon without a spell slot; cast this way, the spell doesn't need Concentration — instead it lasts 1 minute, ending early if you recast it, become Incapacitated, or die.
- **Avatar of Battle** (level 17): You gain Resistance to Bludgeoning, Piercing, and Slashing damage (unconditional — no magic-weapon exception stated in the source text).

---

### Druid
**Hit Die:** d8  **Saves:** INT, WIS
  **Spellcasting:** WIS

**Proficiencies:** Light Armor, Shields, Simple Weapons, Herbalism Kit, Saving Throw: INT, Saving Throw: WIS
**Choose:** Choose 2: Arcana, Animal Handling, Insight, Medicine, Nature, Perception, Religion, or Survival
**Starting Equipment:** Choose A or B: (A) Leather Armor, Shield, Sickle, Druidic Focus (Quarterstaff), Explorer's Pack, Herbalism Kit, 9 GP; or (B) 50 GP

**Class table (Wild Shape uses / Cantrips / Prepared Spells by level; spell slots 1-9 follow standard full-caster progression):**
| Level | PB | Features | Wild Shape | Cantrips | Prepared |
|---|---|---|---|---|---|
| 1 | +2 | Spellcasting, Druidic, Primal Order | — | 2 | 4 |
| 2 | +2 | Wild Shape, Wild Companion | 2 | 2 | 5 |
| 3 | +2 | Druid Subclass | 2 | 2 | 6 |
| 4 | +2 | Ability Score Improvement | 2 | 3 | 7 |
| 5 | +3 | Wild Resurgence | 2 | 3 | 9 |
| 6 | +3 | Subclass Feature | 3 | 3 | 10 |
| 7 | +3 | Elemental Fury | 3 | 3 | 11 |
| 8 | +3 | Ability Score Improvement | 3 | 3 | 12 |
| 9 | +4 | — | 3 | 3 | 14 |
| 10 | +4 | Subclass Feature | 3 | 4 | 15 |
| 11 | +4 | — | 3 | 4 | 16 |
| 12 | +4 | Ability Score Improvement | 3 | 4 | 16 |
| 13 | +5 | — | 3 | 4 | 17 |
| 14 | +5 | Subclass Feature | 3 | 4 | 17 |
| 15 | +5 | Improved Elemental Fury | 3 | 4 | 18 |
| 16 | +5 | Ability Score Improvement | 3 | 4 | 18 |
| 17 | +6 | — | 4 | 4 | 19 |
| 18 | +6 | Beast Spells | 4 | 4 | 20 |
| 19 | +6 | Epic Boon | 4 | 4 | 21 |
| 20 | +6 | Archdruid | 4 | 4 | 22 |

**Features (all levels):**

- **Druidic** (level 1): You know Druidic, the secret language of Druids. While learning this ancient tongue, you also unlocked the magic of communicating with animals; you always have the Speak with Animals spell prepared.
  You can use Druidic to leave hidden messages. You and others who know Druidic automatically spot such a message. Others spot the message's presence with a successful DC 15 Intelligence (Investigation) check but can't decipher it without magic.
- **Primal Order** (level 1): You have dedicated yourself to one of the following sacred roles of your choice.
  Magician. You know one extra cantrip from the Druid spell list. In addition, your mystical connection to nature gives you a bonus to your Intelligence (Arcana or Nature) checks. The bonus equals your Wisdom modifier (minimum bonus of +1).
  Warden. Trained for battle, you gain proficiency with Martial weapons and training with Medium armor.
- **Spellcasting** (level 1): You have learned to cast spells through studying the mystical forces of nature. See "Spells" for the rules on spellcasting. The information below details how you use those rules with Druid spells, which appear on the Druid spell list later in the class's description.
  Cantrips. You know two cantrips of your choice from the Druid spell list. Druidcraft and Produce Flame are recommended.
  Whenever you gain a Druid level, you can replace one of your cantrips with another cantrip of your choice from the Druid spell list.
  When you reach Druid levels 4 and 10, you learn another cantrip of your choice from the Druid spell list, as shown in the Cantrips column of the Druid Features table.
  Spell Slots. The Druid Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest.
  Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose four level 1 spells from the Druid spell list. Animal Friendship, Cure Wounds, Faerie Fire, and Thunderwave are recommended.
  The number of spells on your list increases as you gain Druid levels, as shown in the Prepared Spells column of the Druid Features table. Whenever that number increases, choose additional spells from the Druid spell list until the number of spells on your list matches the number on the table. The chosen spells must be of a level for which you have spell slots. For example, if you're a level 3 Druid, your list of prepared spells can include six spells of levels 1 and 2 in any combination.
  If another Druid feature gives you spells that you always have prepared, those spells don't count against the number of spells you can prepare with this feature, but those spells otherwise count as Druid spells for you.
  Changing Your Prepared Spells. Whenever you finish a Long Rest, you can change your list of prepared spells, replacing any of the spells with other Druid spells for which you have spell slots.
  Spellcasting Ability. Wisdom is your spellcasting ability for your Druid spells.
  Spellcasting Focus. You can use a Druidic Focus as a Spellcasting Focus for your Druid spells.
- **Wild Companion** (level 2): You can summon a nature spirit that assumes an animal form to aid you. As a Magic action, you can expend a spell slot or a use of Wild Shape to cast the Find Familiar spell without Material components.
  When you cast the spell in this way, the familiar is Fey and disappears when you finish a Long Rest.
- **Wild Shape** (level 2): The power of nature allows you to assume the form of an animal. As a Bonus Action, you shape-shift into a Beast form that you have learned for this feature (see "Known Forms" below). You stay in that form for a number of hours equal to half your Druid level or until you use Wild Shape again, have the Incapacitated condition, or die. You can also leave the form early as a Bonus Action.
  Number of Uses. You can use Wild Shape twice. You regain one expended use when you finish a Short Rest, and you regain all expended uses when you finish a Long Rest.
  You gain additional uses when you reach certain Druid levels, as shown in the Wild Shape column of the Druid Features table.
  Known Forms. You know four Beast forms for this feature, chosen from among Beast stat blocks that have a maximum Challenge Rating of 1/4 and that lack a Fly Speed (see "Animals" in "Monsters" for stat block options). The Rat, Riding Horse, Spider, and Wolf are recommended. Whenever you finish a Long Rest, you can replace one of your known forms with another eligible form.
  When you reach certain Druid levels, your number of known forms and the maximum Challenge Rating for those forms increases, as shown in the Beast Shapes table. In addition, starting at level 8, you can adopt a form that has a Fly Speed.
  When choosing known forms, you may look in other sources for eligible Beasts if the Game Master permits you to do so.

Beast Shapes
Druid Level / Known Forms / Max CR / Fly Speed
2 / 4 / 1/4 / No
4 / 6 / 1/2 / No
8 / 8 / 1 / Yes

  Rules While Shape-Shifted. While in a form, you retain your personality, memories, and ability to speak, and the following rules apply:
Temporary Hit Points. When you assume a Wild Shape form, you gain a number of Temporary Hit Points equal to your Druid level.
Game Statistics. Your game statistics are replaced by the Beast's stat block, but you retain your creature type; Hit Points; Hit Point Dice; Intelligence, Wisdom, and Charisma scores; class features; languages; and feats. You also retain your skill and saving throw proficiencies and use your Proficiency Bonus for them, in addition to gaining the proficiencies of the creature. If a skill or saving throw modifier in the Beast's stat block is higher than yours, use the one in the stat block.
No Spellcasting. You can't cast spells, but shapeshifting doesn't break your Concentration or otherwise interfere with a spell you've already cast.
Objects. Your ability to handle objects is determined by the form's limbs rather than your own. In addition, you choose whether your equipment falls in your space, merges into your new form, or is worn by it. Worn equipment functions as normal, but the GM decides whether it's practical for the new form to wear a piece of equipment based on the creature's size and shape. Your equipment doesn't change size or shape to match the new form, and any equipment that the new form can't wear must either fall to the ground or merge with the form. Equipment that merges with the form has no effect while you're in that form.
- **Druid Subclass** (level 3): You gain a Druid subclass of your choice — Circle of the Land, Circle of the Moon, Circle of the Sea, or Circle of the Stars. For the rest of your career, you gain each of your subclass's features that are of your Druid level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Wild Resurgence** (level 5): Once per turn, if you have no Wild Shape uses left, you can give yourself one by expending a spell slot (no action required). Also, once per Long Rest, you can expend one Wild Shape use (no action required) to gain a level 1 spell slot.
- **Elemental Fury** (level 7): Choose one — **Potent Spellcasting** (add your Wisdom modifier to Druid cantrip damage) or **Primal Strike** (once per turn on a weapon or Wild Shape attack hit, extra 1d8 Cold, Fire, Lightning, or Thunder damage, chosen on the hit).
- **Improved Elemental Fury** (level 15): Your Elemental Fury choice improves — **Potent Spellcasting**: a Druid cantrip with range 10+ ft gets +300 ft range; **Primal Strike**: extra damage increases to 2d8.
- **Beast Spells** (level 18): While in Wild Shape, you can cast spells, except any with a specified-cost or consumed Material component.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Dimensional Travel recommended.
- **Archdruid** (level 20): **Evergreen Wild Shape** — when you roll Initiative with no Wild Shape uses left, regain one. **Nature Magician** — convert unexpended Wild Shape uses into a single spell slot (2 spell levels per use, no action required), once per Long Rest. **Longevity** — you age only 1 year for every 10 that pass.

**Subclass — Circle of the Land:** The Circle of the Land comprises mystics and sages who safeguard ancient knowledge and rites. These Druids meet within sacred circles of trees or standing stones to whisper primal secrets in Druidic. The circle's wisest members preside as the chief priests of their communities.
- **Circle of the Land Spells** (level 3): Whenever you finish a Long Rest, choose one type of land — arid, polar, temperate, or tropical — and always have that land's spells prepared: Arid (Blur, Burning Hands, Fire Bolt at L3; Fireball at L5; Blight at L7; Wall of Stone at L9); Polar (Fog Cloud, Hold Person, Ray of Frost at L3; Sleet Storm at L5; Ice Storm at L7; Cone of Cold at L9); Temperate (Misty Step, Shocking Grasp, Sleep at L3; Lightning Bolt at L5; Freedom of Movement at L7; Tree Stride at L9); Tropical (Acid Splash, Ray of Sickness, Web at L3; Stinking Cloud at L5; Polymorph at L7; Insect Plague at L9).
- **Land's Aid** (level 3): As a Magic action, expend a Wild Shape use and choose a point within 60 ft; a 10-ft-radius Sphere of vitality-giving flowers and life-draining thorns appears there. Each creature you choose in the Sphere makes a CON save vs your spell save DC — fail: 2d6 Necrotic; success: half. One creature you choose in the area regains 2d6 HP. Both numbers increase by 1d6 at Druid levels 10 (3d6) and 14 (4d6).
- **Natural Recovery** (level 6): Cast one prepared Circle Spell (level 1+) without expending a slot, once per Long Rest. Also, on a Short Rest, recover spell slots with a combined level up to half your Druid level (round up, none level 6+) — once per Long Rest.
- **Nature's Ward** (level 10): Immune to the Poisoned condition; Resistance to a damage type tied to your current land choice — Arid: Fire; Polar: Cold; Temperate: Lightning; Tropical: Poison.
- **Nature's Sanctuary** (level 14): As a Magic action, expend a Wild Shape use to create a 15-ft Cube of spectral trees/vines on the ground within 120 ft, lasting 1 minute or until you're Incapacitated or die; you and allies there have Half Cover, and allies also gain your current Nature's Ward Resistance. As a Bonus Action, move the Cube up to 60 ft to ground within 120 ft of you.

**Subclass — Circle of the Moon:**
- **Circle Forms** (level 3): Channels lunar magic into your Wild Shape forms. Your maximum CR equals your Druid level ÷ 3 (rounded down). Armor Class: while in the form, your AC equals 13 + your Wisdom modifier if that total is higher than the Beast's AC. Temporary Hit Points: you gain Temp HP equal to 3x your Druid level.
- **Circle of the Moon Spells** (level 3): You always have prepared — Cure Wounds, Moonbeam, Starry Wisp (level 3); Conjure Animals (level 5); Fount of Moonlight (level 7); Mass Cure Wounds (level 9). You can cast these while in Wild Shape form.
- **Improved Circle Forms** (level 6): While in Wild Shape — Lunar Radiance: each attack in Wild Shape can deal its normal damage type or Radiant damage (choose each time you hit). Increased Toughness: add your Wisdom modifier to Constitution saving throws.
- **Moonlight Step** (level 10): As a Bonus Action, teleport up to 30 ft to an unoccupied space you can see, with Advantage on your next attack roll before end of turn. Uses equal to your Wisdom modifier (minimum once), regained on a Long Rest; also regainable by expending a level 2+ spell slot.
- **Lunar Form** (level 14): Improved Lunar Radiance — once per turn, deal an extra 2d10 Radiant damage on a hit with a Wild Shape attack. Shared Moonlight — whenever you use Moonlight Step, also teleport one willing creature within 10 ft of you to an unoccupied space within 10 ft of your destination.

**Subclass — Circle of the Sea:**
- **Circle of the Sea Spells** (level 3): You always have prepared — Fog Cloud, Gust of Wind, Ray of Frost, Thunderwave (level 3); Lightning Bolt, Water Breathing (level 5); Control Water, Ice Storm (level 7); Conjure Elemental, Hold Monster (level 9).
- **Wrath of the Sea** (level 3): As a Bonus Action, expend a Wild Shape use to create a 5-ft Emanation lasting 10 minutes. When manifested and on subsequent turns as a Bonus Action, choose a creature in the Emanation — CON save vs your spell save DC or take Cold damage (d6s equal to your Wisdom modifier, minimum one) and be pushed up to 15 ft away if Large or smaller.
- **Aquatic Affinity** (level 6): The Wrath of the Sea Emanation increases to 10 ft; you also gain a Swim Speed equal to your Speed.
- **Stormborn** (level 10): Your Wrath of the Sea confers two more benefits while active — Flight (Fly Speed equal to your Speed) and Resistance (to Cold, Lightning, and Thunder damage).
- **Oceanic Gift** (level 14): Manifest Wrath of the Sea's Emanation around a willing creature within 60 ft instead of yourself; that creature gains all benefits, using your spell save DC and Wisdom modifier. You can manifest it around both yourself and another creature by expending two Wild Shape uses instead of one.

**Subclass — Circle of the Stars:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

---

### Fighter
**Hit Die:** d10  **Saves:** STR, CON

**Proficiencies:** All armor, Shields, Simple Weapons, Martial Weapons, Saving Throw: STR, Saving Throw: CON
**Choose:** Choose 2: Acrobatics, Animal Handling, Athletics, History, Insight, Intimidation, Perception, or Survival
**Starting Equipment:** Choose A, B, or C: (A) Chain Mail, Greatsword, Flail, 8 Javelins, Dungeoneer's Pack, 4 GP; (B) Studded Leather Armor, Scimitar, Shortsword, Longbow, 20 Arrows, Quiver, Dungeoneer's Pack, 11 GP; or (C) 155 GP

**Class table (Second Wind / Weapon Mastery uses by level):**
| Level | PB | Features | Second Wind | Weapon Mastery |
|---|---|---|---|---|
| 1 | +2 | Fighting Style, Second Wind, Weapon Mastery | 2 | 3 |
| 2 | +2 | Action Surge (1), Tactical Mind | 2 | 3 |
| 3 | +2 | Fighter Subclass | 2 | 3 |
| 4 | +2 | Ability Score Improvement | 3 | 4 |
| 5 | +3 | Extra Attack, Tactical Shift | 3 | 4 |
| 6 | +3 | Ability Score Improvement | 3 | 4 |
| 7 | +3 | Subclass Feature | 3 | 4 |
| 8 | +3 | Ability Score Improvement | 3 | 4 |
| 9 | +4 | Indomitable (1), Tactical Master | 3 | 4 |
| 10 | +4 | Subclass Feature | 4 | 5 |
| 11 | +4 | Two Extra Attacks | 4 | 5 |
| 12 | +4 | Ability Score Improvement | 4 | 5 |
| 13 | +5 | Indomitable (2), Studied Attacks | 4 | 5 |
| 14 | +5 | Ability Score Improvement | 4 | 5 |
| 15 | +5 | Subclass Feature | 4 | 5 |
| 16 | +5 | Ability Score Improvement | 4 | 6 |
| 17 | +6 | Action Surge (2), Indomitable (3) | 4 | 6 |
| 18 | +6 | Subclass Feature | 4 | 6 |
| 19 | +6 | Epic Boon | 4 | 6 |
| 20 | +6 | Three Extra Attacks | 4 | 6 |

**Features (all levels):**
- **Fighting Style** (level 1): Gain a Fighting Style feat of your choice (Defense recommended); replaceable with a different Fighting Style feat on any level-up.
- **Second Wind** (level 1): As a Bonus Action, regain 1d10 + your Fighter level HP. 2 uses (regain one on Short Rest, all on Long Rest; more uses at higher levels per the table).
- **Weapon Mastery** (level 1): Use the mastery property of three kinds of Simple or Martial weapons of your choice; change one choice on a Long Rest. More kinds at higher levels per the table.
- **Action Surge** (level 2): On your turn, take one additional action (not the Magic action). Once per Short/Long Rest; twice per rest (but only once per turn) starting at level 17.
- **Tactical Mind** (level 2): When you fail an ability check, you can expend a Second Wind use — roll 1d10 and add to the check, potentially turning it into a success. If it still fails, the use isn't expended.
- **Fighter Subclass** (level 3): Choose Battle Master, Champion, Eldritch Knight, or Psi Warrior. Gain each subclass feature at your Fighter level or lower.
- **Ability Score Improvement** (levels 4, 6, 8, 12, 14, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Extra Attack** (level 5): Attack twice instead of once when you take the Attack action.
- **Tactical Shift** (level 5): Whenever you activate Second Wind with a Bonus Action, move up to half your Speed without provoking Opportunity Attacks.
- **Indomitable** (level 9): If you fail a save, reroll it with a bonus equal to your Fighter level (must use the new roll). Once per Long Rest; twice per Long Rest starting at level 13; three times starting at level 17.
- **Tactical Master** (level 9): When attacking with a weapon whose mastery property you can use, you can substitute the Push, Sap, or Slow property for that attack.
- **Two Extra Attacks** (level 11): Attack three times instead of once when you take the Attack action.
- **Studied Attacks** (level 13): If you miss a creature with an attack roll, you have Advantage on your next attack roll against that creature before the end of your next turn.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Combat Prowess recommended.
- **Three Extra Attacks** (level 20): Attack four times instead of once when you take the Attack action.

**Subclass — Battle Master:** Battle Masters are students of the art of battle, learning martial techniques passed down through generations. The most accomplished Battle Masters are well-rounded figures who combine their carefully honed combat skills with academic study in the fields of history, theory, and the arts.
- **Combat Superiority** (level 3): Learn 3 maneuvers of your choice (see Maneuver Options below); learn 2 more at levels 7, 10, and 15 (and can swap one known maneuver each time). You have 4 Superiority Dice (d8s, regained on a Short or Long Rest); +1 die at level 7 (5 total) and level 15 (6 total). Maneuver save DC = 8 + Strength or Dexterity modifier (your choice) + Proficiency Bonus.
- **Student of War** (level 3): Gain proficiency with one type of Artisan's Tools and one skill from the level-1 Fighter skill list.
- **Know Your Enemy** (level 7): As a Bonus Action, learn whether a creature within 30 ft has any Immunities/Resistances/Vulnerabilities, and what they are. Once per Long Rest; restorable by expending a Superiority Die (no action required).
- **Improved Combat Superiority** (level 10): Superiority Die becomes a d10.
- **Relentless** (level 15): Once per turn when using a maneuver, roll 1d8 and use that instead of expending a Superiority Die.
- **Ultimate Combat Superiority** (level 18): Superiority Die becomes a d12.
  - **Maneuver Options** (alphabetical): **Ambush** — add a Superiority Die to a Dexterity (Stealth) check or Initiative roll. **Bait and Switch** — swap places with a willing creature within 5 ft (5 ft movement, no Opportunity Attacks); roll the die, you or the creature gets that bonus to AC until your next turn. **Commander's Strike** — replace one attack to let a willing creature use its Reaction to attack, adding the die to its damage on a hit. **Commanding Presence** — add the die to a Charisma (Intimidation, Performance, or Persuasion) check. **Disarming Attack** — on a hit, add the die to damage; target makes a Strength save or drops an item. **Distracting Strike** — on a hit, add the die to damage; the next attack against the target before your next turn has Advantage. **Evasive Footwork** — Bonus Action Disengage, add the die to your AC until your next turn. **Feinting Attack** — Bonus Action, Advantage on your next attack this turn against a target within 5 ft; if it hits, add the die to damage. **Goading Attack** — on a hit, add the die to damage; target fails a Wisdom save or has Disadvantage on attacks against others until end of your next turn. **Lunging Attack** — Bonus Action Dash; if you moved 5+ ft in a line before a melee hit this turn, add the die to damage. **Maneuvering Attack** — on a hit, add the die to damage; a willing creature can Reaction-move half its Speed without Opportunity Attacks from your target. **Menacing Attack** — on a hit, add the die to damage; target fails a Wisdom save or is Frightened until end of your next turn. **Parry** — Reaction on being damaged by a melee attack, reduce damage by the die roll + Strength or Dexterity modifier. **Precision Attack** — on a miss, roll the die and add to the attack roll, possibly turning it into a hit. **Pushing Attack** — on a hit, add the die to damage; Large-or-smaller target fails a Strength save or is pushed 15 ft away. **Rally** — Bonus Action, an ally within 30 ft gains Temp HP equal to the die roll + half your Fighter level (round down). **Riposte** — Reaction when a creature misses you with a melee attack, make a melee attack against it, adding the die to damage on a hit. **Sweeping Attack** — on a melee hit, a second creature within 5 ft of the target (and your reach) that the original roll would also hit takes damage equal to the die roll (same type). **Tactical Assessment** — add the die to an Intelligence (History or Investigation) or Wisdom (Insight) check. **Trip Attack** — on a hit, add the die to damage; Large-or-smaller target fails a Strength save or is Prone.

**Subclass — Champion:** A Champion focuses on the development of martial prowess in a relentless pursuit of victory. Champions combine rigorous training with physical excellence to deal devastating blows, withstand peril, and garner glory. Whether in athletic contests or bloody battle, Champions strive for the crown of the victor.
- **Improved Critical** (level 3): Weapon and Unarmed Strike attacks score a Critical Hit on a roll of 19 or 20.
- **Remarkable Athlete** (level 3): Advantage on Initiative rolls and Strength (Athletics) checks. Immediately after scoring a Critical Hit, move up to half your Speed without Opportunity Attacks.
- **Additional Fighting Style** (level 7): Gain another Fighting Style feat of your choice.
- **Heroic Warrior** (level 10): During combat, give yourself Heroic Inspiration whenever you start your turn without it.
- **Superior Critical** (level 15): Critical Hit range expands to 18-20.
- **Survivor** (level 18): **Defy Death** — Advantage on Death Saving Throws; rolling 18-20 counts as rolling a 20. **Heroic Rally** — at the start of each turn, regain 5 + Constitution modifier HP if Bloodied and at 1+ HP.

**Subclass — Eldritch Knight:** Eldritch Knights combine the martial mastery common to all Fighters with a careful study of magic. Their spells both complement and extend their combat skills, providing additional protection to shore up their armor and also allowing them to engage many foes at once with explosive magic.
- **Spellcasting** (level 3): Cantrips — know 2 from the Wizard list (Ray of Frost, Shocking Grasp recommended), replaceable on level-up; learn a 3rd at level 10. Prepared Spells — start with 3 level-1 Wizard spells (Burning Hands, Jump, Shield recommended); grows per the Eldritch Knight Spellcasting table below; replace one on any level-up. Intelligence is your spellcasting ability; an Arcane Focus works as a Spellcasting Focus.
  | Fighter Level | Prepared | Slots 1 | 2 | 3 | 4 |
  |---|---|---|---|---|---|
  | 3 | 3 | 2 | — | — | — |
  | 4-6 | 4 | 3 | — | — | — |
  | 7-9 | 5-6 | 4 | 2 | — | — |
  | 10-12 | 7-8 | 4 | 3 | — | — |
  | 13-15 | 9-10 | 4 | 3 | 2 | — |
  | 16-18 | 11 | 4 | 3 | 3 | — |
  | 19-20 | 12-13 | 4 | 3 | 3 | 1 |
- **War Bond** (level 3): A 1-hour ritual (doable during a Short Rest) bonds you to a weapon within reach (fails if another Fighter is bonded to it, or it's a magic item someone else is attuned to). While bonded, you can't be disarmed of it unless Incapacitated, and can summon it to your hand as a Bonus Action if it's on the same plane. Up to two bonded weapons at once, but only one summonable at a time; bonding a third breaks one of the other two.
- **War Magic** (level 7): When you take the Attack action, replace one attack with a casting of a Wizard cantrip with a casting time of an action.
- **Eldritch Strike** (level 10): On a weapon hit, the target has Disadvantage on its next save against a spell you cast before the end of your next turn.
- **Arcane Charge** (level 15): When you use Action Surge, teleport up to 30 ft to an unoccupied space you can see (before or after the additional action).
- **Improved War Magic** (level 18): When you take the Attack action, replace two attacks with a casting of a level 1 or 2 Wizard spell with a casting time of an action.

**Subclass — Psi Warrior:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

---

### Monk
**Hit Die:** d8  **Saves:** STR, DEX
  **Note:** the previous version of this entry had an incorrect Proficiencies line (an apparent stale-cache artifact); corrected below from the verbatim PDF.

**Proficiencies:** Simple Weapons, Martial Weapons with the Light property, Saving Throw: STR, Saving Throw: DEX
**Choose:** Choose 2: Acrobatics, Athletics, History, Insight, Religion, or Stealth
**Choose:** One type of Artisan's Tools or one Musical Instrument
**Starting Equipment:** Choose A or B: (A) Spear, 5 Daggers, Artisan's Tools or Musical Instrument (same as chosen above), Explorer's Pack, 11 GP; or (B) 50 GP

**Class table (Martial Arts Die / Focus Points / Unarmored Movement by level):**
| Level | PB | Features | Martial Arts | Focus Points | Unarmored Movement |
|---|---|---|---|---|---|
| 1 | +2 | Martial Arts, Unarmored Defense | 1d6 | — | — |
| 2 | +2 | Monk's Focus, Unarmored Movement, Uncanny Metabolism | 1d6 | 2 | +10 ft |
| 3 | +2 | Deflect Attacks, Monk Subclass | 1d6 | 3 | +10 ft |
| 4 | +2 | Ability Score Improvement, Slow Fall | 1d6 | 4 | +10 ft |
| 5 | +3 | Extra Attack, Stunning Strike | 1d8 | 5 | +10 ft |
| 6 | +3 | Empowered Strikes, Subclass Feature | 1d8 | 6 | +15 ft |
| 7 | +3 | Evasion | 1d8 | 7 | +15 ft |
| 8 | +3 | Ability Score Improvement | 1d8 | 8 | +15 ft |
| 9 | +4 | Acrobatic Movement | 1d8 | 9 | +15 ft |
| 10 | +4 | Heightened Focus, Self-Restoration | 1d8 | 10 | +20 ft |
| 11 | +4 | Subclass Feature | 1d10 | 11 | +20 ft |
| 12 | +4 | Ability Score Improvement | 1d10 | 12 | +20 ft |
| 13 | +5 | Deflect Energy | 1d10 | 13 | +20 ft |
| 14 | +5 | Disciplined Survivor | 1d10 | 14 | +25 ft |
| 15 | +5 | Perfect Focus | 1d10 | 15 | +25 ft |
| 16 | +5 | Ability Score Improvement | 1d10 | 16 | +25 ft |
| 17 | +6 | Subclass Feature | 1d12 | 17 | +25 ft |
| 18 | +6 | Superior Defense | 1d12 | 18 | +30 ft |
| 19 | +6 | Epic Boon | 1d12 | 19 | +30 ft |
| 20 | +6 | Body and Mind | 1d12 | 20 | +30 ft |

**Features (all levels):**
- **Martial Arts** (level 1): Mastery of Unarmed Strikes and "Monk Weapons" (Simple Melee weapons; Martial Melee weapons with the Light property). While unarmed or wielding only Monk Weapons, unarmored, and shieldless: **Bonus Unarmed Strike** — make an Unarmed Strike as a Bonus Action. **Martial Arts Die** — roll it in place of normal Unarmed Strike/Monk Weapon damage (die size grows per the table). **Dexterous Attacks** — use Dexterity instead of Strength for attack/damage rolls (and Grapple/Shove save DC) with Unarmed Strikes and Monk weapons.
- **Unarmored Defense** (level 1): While unarmored and shieldless, base AC = 10 + Dexterity + Wisdom modifiers.
- **Monk's Focus** (level 2): Focus Points (count per the table) fuel three known features (expended points return on a Short or Long Rest; DC for saves = 8 + Wisdom modifier + Proficiency Bonus): **Flurry of Blows** — expend 1 to make two Unarmed Strikes as a Bonus Action. **Patient Defense** — Bonus Action Disengage; expend 1 to also Dodge. **Step of the Wind** — Bonus Action Dash; expend 1 to also Disengage and double your jump distance this turn.
- **Unarmored Movement** (level 2): Speed +10 ft while unarmored and shieldless; grows per the table.
- **Uncanny Metabolism** (level 2): When you roll Initiative, regain all Focus Points and roll your Martial Arts die to regain that many + your Monk level in HP. Once per Long Rest.
- **Deflect Attacks** (level 3): Reaction on being hit by an attack dealing Bludgeoning/Piercing/Slashing damage — reduce that damage by 1d10 + Dexterity modifier + Monk level. If reduced to 0, you can expend 1 Focus Point to redirect force at a creature within 5 ft (melee) or within 60 ft and not behind Total Cover (ranged) — Dexterity save or take damage equal to two Martial Arts die rolls + Dexterity modifier (same type as the original attack).
- **Monk Subclass** (level 3): Choose Warrior of Mercy, Warrior of Shadow, Warrior of the Elements, or Warrior of the Open Hand. Gain each subclass feature at your Monk level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Slow Fall** (level 4): Reaction when you fall — reduce fall damage by 5x your Monk level.
- **Extra Attack** (level 5): Attack twice instead of once when you take the Attack action.
- **Stunning Strike** (level 5): Once per turn on hitting with a Monk weapon or Unarmed Strike, expend 1 Focus Point — target makes a Constitution save; fail: Stunned until start of your next turn; success: Speed halved until then, and the next attack against it before then has Advantage.
- **Empowered Strikes** (level 6): Unarmed Strike damage can be Force damage or its normal type, your choice.
- **Evasion** (level 7): On a Dexterity save for half damage, take none on success and half on failure. Doesn't work while Incapacitated.
- **Acrobatic Movement** (level 9): While unarmored and shieldless, move along vertical surfaces and across liquids on your turn without falling.
- **Heightened Focus** (level 10): Improves the three Monk's Focus features — **Flurry of Blows**: 3 Unarmed Strikes instead of 2. **Patient Defense**: gain Temp HP equal to two Martial Arts die rolls when used. **Step of the Wind**: bring a willing Large-or-smaller creature within 5 ft along with you (no Opportunity Attacks for its movement).
- **Self-Restoration** (level 10): At the end of each of your turns, remove Charmed, Frightened, or Poisoned from yourself (choose one). Also, forgoing food/drink doesn't cause Exhaustion.
- **Deflect Energy** (level 13): Deflect Attacks now works against any damage type, not just Bludgeoning/Piercing/Slashing.
- **Disciplined Survivor** (level 14): Proficiency in all saving throws. On a failed save, you can expend 1 Focus Point to reroll it (must use the new roll).
- **Perfect Focus** (level 15): When you roll Initiative without using Uncanny Metabolism, regain Focus Points up to 4 if you have 3 or fewer.
- **Superior Defense** (level 18): At the start of your turn, expend 3 Focus Points for Resistance to all damage except Force, lasting 1 minute or until Incapacitated.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Irresistible Offense recommended.
- **Body and Mind** (level 20): Dexterity and Wisdom scores each increase by 4, to a maximum of 25.

**Subclass — Warrior of Mercy:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

**Subclass — Warrior of Shadow:** Warriors of Shadow practice stealth and subterfuge, harnessing the power of the Shadowfell. They are at home in darkness, able to draw gloom around themselves to hide, leap from shadow to shadow, and take on a wraithlike form.
- **Shadow Arts** (level 3): **Darkness** — spend 1 Focus Point to cast Darkness (no components; you can see in it; move its area up to 60 ft at the start of each of your turns). **Darkvision** — 60 ft, or +60 ft if you already have it. **Shadowy Figments** — know Minor Illusion (Wisdom as spellcasting ability).
- **Shadow Step** (level 6): While entirely in Dim Light/Darkness, Bonus Action to teleport up to 60 ft to an unoccupied space you can see that's also in Dim Light/Darkness; Advantage on your next melee attack before end of turn.
- **Improved Shadow Step** (level 11): Spend 1 Focus Point when using Shadow Step to remove the Dim Light/Darkness start/end requirement; can make an Unarmed Strike immediately after teleporting.
- **Cloak of Shadows** (level 17): As a Magic action while entirely in Dim Light/Darkness, expend 3 Focus Points to shroud yourself for 1 minute (or until Incapacitated or you end your turn in Bright Light): **Invisibility** — Invisible condition. **Partially Incorporeal** — move through occupied spaces as Difficult Terrain (shunted to last unoccupied space if you end turn in one). **Shadow Flurry** — use Flurry of Blows without spending Focus Points.

**Subclass — Warrior of the Elements:** Warriors of the Elements tap into the power of the Elemental Planes. Harnessing their supernatural focus, these Monks momentarily tame the energy of the Elemental Chaos to empower themselves in and out of battle.
- **Elemental Attunement** (level 3): At the start of your turn, expend 1 Focus Point to imbue yourself for 10 minutes (or until Incapacitated): **Reach** — Unarmed Strike reach +10 ft. **Elemental Strikes** — Unarmed Strike hits can deal Acid/Cold/Fire/Lightning/Thunder instead of normal damage; when you do, target makes a Strength save or is moved up to 10 ft toward/away from you.
- **Manipulate Elements** (level 3): Know the Elementalism spell (Wisdom as spellcasting ability).
- **Elemental Burst** (level 6): As a Magic action, expend 2 Focus Points — 20-ft-radius Sphere within 120 ft, one damage type of your choice (Acid/Cold/Fire/Lightning/Thunder). Dexterity save; fail: damage equal to three Martial Arts die rolls; success: half.
- **Stride of the Elements** (level 11): While Elemental Attunement is active, also gain a Fly Speed and Swim Speed equal to your Speed.
- **Elemental Epitome** (level 17): While Elemental Attunement is active: **Damage Resistance** — Resistance to one chosen type (Acid/Cold/Fire/Lightning/Thunder), changeable at the start of each turn. **Destructive Stride** — using Step of the Wind grants +20 ft Speed for the turn; a chosen creature takes one Martial Arts die roll of damage (your choice of type) when you enter a space within 5 ft of it (once per creature per turn). **Empowered Strikes** — once per turn, extra damage equal to one Martial Arts die roll (same type as the strike) on an Unarmed Strike hit.

**Subclass — Warrior of the Open Hand:** Warriors of the Open Hand are masters of unarmed combat. They learn techniques to push and trip their opponents and manipulate their own energy to protect themselves from harm.
- **Open Hand Technique** (level 3): On a Flurry of Blows hit, impose one: **Addle** — target can't make Opportunity Attacks until start of its next turn. **Push** — Strength save or pushed up to 15 ft away. **Topple** — Dexterity save or Prone.
- **Wholeness of Body** (level 6): As a Bonus Action, roll your Martial Arts die and regain that many + your Wisdom modifier HP (minimum 1). Uses equal to your Wisdom modifier (minimum once), regained on a Long Rest.
- **Fleet Step** (level 11): When you take a Bonus Action other than Step of the Wind, you can also use Step of the Wind immediately after it.
- **Quivering Palm** (level 17): On an Unarmed Strike hit, expend 4 Focus Points to start imperceptible vibrations lasting a number of days equal to your Monk level (harmless unless ended). End them (an action, or by forgoing one Attack-action attack) while on the same plane as the target — Constitution save; fail: 10d12 Force damage; success: half. Only one creature affected at a time; can end harmlessly with no action.

---

### Paladin
**Hit Die:** d10  **Saves:** WIS, CHA
  **Spellcasting:** CHA

**Proficiencies:** All armor, Shields, Simple Weapons, Martial Weapons, Saving Throw: WIS, Saving Throw: CHA
**Choose:** Choose 2: Athletics, Insight, Intimidation, Medicine, Persuasion, or Religion
**Starting Equipment:** Choose A or B: (A) Chain Mail, Shield, Longsword, 6 Javelins, Holy Symbol, Priest's Pack, 9 GP; or (B) 150 GP

**Class table (Channel Divinity / Prepared Spells by level; spell slots 1-5 follow standard half-caster progression):**
| Level | PB | Features | Channel Divinity | Prepared |
|---|---|---|---|---|
| 1 | +2 | Lay on Hands, Spellcasting, Weapon Mastery | — | 2 |
| 2 | +2 | Fighting Style, Paladin's Smite | — | 3 |
| 3 | +2 | Channel Divinity, Paladin Subclass | 2 | 4 |
| 4 | +2 | Ability Score Improvement | 2 | 5 |
| 5 | +3 | Extra Attack, Faithful Steed | 2 | 6 |
| 6 | +3 | Aura of Protection | 2 | 6 |
| 7 | +3 | Subclass Feature | 2 | 7 |
| 8 | +3 | Ability Score Improvement | 2 | 7 |
| 9 | +4 | Abjure Foes | 2 | 9 |
| 10 | +4 | Aura of Courage | 2 | 9 |
| 11 | +4 | Radiant Strikes | 3 | 10 |
| 12 | +4 | Ability Score Improvement | 3 | 10 |
| 13 | +5 | — | 3 | 11 |
| 14 | +5 | Restoring Touch | 3 | 11 |
| 15 | +5 | Subclass Feature | 3 | 12 |
| 16 | +5 | Ability Score Improvement | 3 | 12 |
| 17 | +6 | — | 3 | 14 |
| 18 | +6 | Aura Expansion | 3 | 14 |
| 19 | +6 | Epic Boon | 3 | 15 |
| 20 | +6 | Subclass Feature | 3 | 15 |

**Features (all levels):**

- **Lay On Hands** (level 1): Your blessed touch can heal wounds. You have a pool of healing power that replenishes when you finish a Long Rest. With that pool, you can restore a total number of Hit Points equal to five times your Paladin level.
  As a Bonus Action, you can touch a creature (which could be yourself) and draw power from the pool of healing to restore a number of Hit Points to that creature, up to the maximum amount remaining in the pool.
  You can also expend 5 Hit Points from the pool of healing power to remove the Poisoned condition from the creature; those points don't also restore Hit Points to the creature.
- **Spellcasting** (level 1): You have learned to cast spells through prayer and meditation. See "Spells" for the rules on spellcasting. The information below details how you use those rules with Paladin spells, which appear in the Paladin spell list later in the class's description.
  Spell Slots. The Paladin Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest.
  Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose two level 1 Paladin spells. Heroism and Searing Smite are recommended.
  The number of spells on your list increases as you gain Paladin levels, as shown in the Prepared Spells column of the Paladin Features table. Whenever that number increases, choose additional Paladin spells until the number of spells on your list matches the number in the Paladin Features table. The chosen spells must be of a level for which you have spell slots. For example, if you're a level 5 Paladin, your list of prepared spells can include six Paladin spells of level 1 or 2 in any combination.
  If another Paladin feature gives you spells that you always have prepared, those spells don't count against the number of spells you can prepare with this feature, but those spells otherwise count as Paladin spells for you.
  Changing Your Prepared Spells. Whenever you finish a Long Rest, you can replace one spell on your list with another Paladin spell for which you have spell slots.
  Spellcasting Ability. Charisma is your spellcasting ability for your Paladin spells.
  Spellcasting Focus. You can use a Holy Symbol as a Spellcasting Focus for your Paladin spells.
- **Weapon Mastery** (level 1): Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice with which you have proficiency, such as Longswords and Javelins.
Whenever you finish a Long Rest, you can change the kinds of weapons you chose. For example, you could switch to using the mastery properties of Halberds and Flails.
- **Fighting Style** (level 2): You gain a Fighting Style feat of your choice (see "Feats" for feats). Instead of choosing one of those feats, you can choose the option below.
  Blessed Warrior. You learn two Cleric cantrips of your choice (see the Cleric class's section for a list of Cleric spells). Guidance and Sacred Flame are recommended. The chosen cantrips count as Paladin spells for you, and Charisma is your spellcasting ability for them. Whenever you gain a Paladin level, you can replace one of these cantrips with another Cleric cantrip.
- **Paladin's Smite** (level 2): You always have the Divine Smite spell prepared. In addition, you can cast it without expending a spell slot, but you must finish a Long Rest before you can cast it in this way again.
- **Channel Divinity** (level 3): You can channel divine energy directly from the Outer Planes, using it to fuel magical effects. You start with one such effect: Divine Sense, which is described below. Other Paladin features give additional Channel Divinity effect options. Each time you use this class's Channel Divinity, you choose which effect from this class to create.
  You can use this class's Channel Divinity twice. You regain one of its expended uses when you finish a Short Rest, and you regain all expended uses when you finish a Long Rest. You gain an additional use when you reach Paladin level 11.
  If a Channel Divinity effect requires a saving throw, the DC equals the spell save DC from this class's Spellcasting feature.
  Divine Sense. As a Bonus Action, you can open your awareness to detect Celestials, Fiends, and Undead. For the next 10 minutes or until you have the Incapacitated condition, you know the location of any creature of those types within 60 feet of yourself, and you know its creature type. Within the same radius, you also detect the presence of any place or object that has been consecrated or desecrated, as with the Hallow spell.
- **Paladin Subclass** (level 3): Choose Oath of Devotion, Oath of Glory, Oath of the Ancients, or Oath of Vengeance. Gain each subclass feature at your Paladin level or lower. Each oath's tenets and the level-3 features are the culmination of a Paladin's training.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Extra Attack** (level 5): Attack twice instead of once when you take the Attack action.
- **Faithful Steed** (level 5): You always have Find Steed prepared, and can cast it once without a spell slot (regained on a Long Rest).
- **Aura of Protection** (level 6): 10-ft Emanation (inactive while Incapacitated) — you and allies inside gain a bonus to saving throws equal to your Charisma modifier (minimum +1). With multiple Paladins present, a creature benefits from only one such aura at a time (its choice).
- **Abjure Foes** (level 9): As a Magic action, expend a Channel Divinity use; target a number of creatures within 60 ft equal to your Charisma modifier (minimum one) — Wisdom save or Frightened for 1 minute or until it takes damage; while Frightened this way, it can only move, take an action, OR take a Bonus Action on its turns (not more than one).
- **Aura of Courage** (level 10): You and allies are immune to Frightened while in your Aura of Protection (entering while already Frightened suppresses the condition there).
- **Radiant Strikes** (level 11): Melee weapon or Unarmed Strike hits deal an extra 1d8 Radiant damage.
- **Restoring Touch** (level 14): When using Lay on Hands, you can also remove Blinded, Charmed, Deafened, Frightened, Paralyzed, or Stunned — 5 HP from the pool per condition removed (doesn't also heal).
- **Aura Expansion** (level 18): Aura of Protection becomes a 30-ft Emanation.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Truesight recommended.

**Subclass — Oath of Devotion:** The Oath of Devotion binds Paladins to the ideals of justice and order. These Paladins meet the archetype of the knight in shining armor. They hold themselves to the highest standards of conduct, and some—for better or worse—hold the rest of the world to the same standards.
  Tenets: Let your word be your promise. Protect the weak and never fear to act. Let your honorable deeds be an example.
- **Oath of Devotion Spells** (level 3, and levels 5/9/13/17): Always prepared — Protection from Evil and Good, Shield of Faith (L3); Aid, Zone of Truth (L5); Beacon of Hope, Dispel Magic (L9); Freedom of Movement, Guardian of Faith (L13); Commune, Flame Strike (L17).
- **Sacred Weapon** (level 3): When you take the Attack action, expend a Channel Divinity use to imbue a Melee weapon you're holding for 10 minutes (or until reused) — add your Charisma modifier to attack rolls with it (minimum +1); on a hit, its damage type can be Radiant instead of normal. It sheds Bright Light 20 ft + Dim Light 20 ft further. Ends early at will (no action) or if you stop carrying it.
- **Aura of Devotion** (level 7): You and allies are immune to Charmed while in your Aura of Protection (entering while already Charmed suppresses it there).
- **Smite of Protection** (level 15): Whenever you cast Divine Smite, you and allies gain Half Cover while in your Aura of Protection until the start of your next turn.
- **Holy Nimbus** (level 20): As a Bonus Action, imbue your Aura of Protection for 10 minutes (or until dismissed, no action) — **Holy Ward**: Advantage on saves forced by a Fiend or Undead. **Radiant Damage**: enemies starting their turn in the aura take Radiant damage equal to your Charisma modifier + Proficiency Bonus. **Sunlight**: the aura is filled with Bright Light that counts as sunlight. Once per Long Rest; restorable by expending a level 5 spell slot (no action).

**Subclass — Oath of Glory:** Paladins who take the Oath of Glory believe they and their companions are destined to achieve glory through deeds of heroism. They train diligently and encourage their companions, so they're all ready when destiny calls.
  Tenets: Endeavor to be known by your deeds. Face hardships with courage. Inspire others to strive for glory.
- **Inspiring Smite** (level 3): Immediately after casting Divine Smite, expend a Channel Divinity use to distribute Temp HP (total = 2d8 + your Paladin level) among creatures within 30 ft (can include you), split however you like.
- **Oath of Glory Spells** (level 3, and levels 5/9/13/17): Always prepared — Guiding Bolt, Heroism (L3); Enhance Ability, Magic Weapon (L5); Haste, Protection from Energy (L9); Compulsion, Freedom of Movement (L13); Legend Lore, Yolande's Regal Presence (L17).
- **Peerless Athlete** (level 3): As a Bonus Action, expend a Channel Divinity use — for 1 hour, Advantage on Strength (Athletics) and Dexterity (Acrobatics) checks, and Long/High jump distance +10 ft (costs movement as normal).
- **Aura of Alacrity** (level 7): Speed +10 ft. Allies entering your Aura of Protection for the first time on a turn, or starting their turn there, gain +10 ft Speed until the end of their next turn.
- **Glorious Defense** (level 15): Reaction when you or a creature within 10 ft is hit by an attack roll — grant a bonus to its AC against that attack equal to your Charisma modifier (minimum +1), possibly causing a miss; if it misses, you can make one weapon attack against the attacker (if in range) as part of this Reaction. Uses equal to your Charisma modifier (minimum once), regained on a Long Rest.
- **Living Legend** (level 20): As a Bonus Action, gain for 1 minute — **Charismatic**: Advantage on all Charisma checks. **Saving Throw Reroll**: Reaction to reroll a failed save (must use new roll). **Unerring Strike**: once per turn, turn a missed weapon attack roll into a hit. Once per Long Rest; restorable by expending a level 5 spell slot (no action).

**Subclass — Oath of the Ancients:** The Oath of the Ancients is as old as the first elves. Paladins who swear this oath cherish the light; they love the beautiful and life-giving things of the world more than any principles of honor, courage, and justice. They adorn their armor and clothing with images of growing things—leaves, antlers, or flowers—to reflect their commitment to preserving life and light.
  Tenets: Kindle the light of hope. Shelter life. Delight in art and laughter.
- **Nature's Wrath** (level 3): As a Magic action, expend a Channel Divinity use — each creature you choose within 15 ft makes a Strength save or is Restrained 1 minute (repeats save at end of its turns, ending on success).
- **Oath of the Ancients Spells** (level 3, and levels 5/9/13/17): Always prepared — Ensnaring Strike, Speak with Animals (L3); Misty Step, Moonbeam (L5); Plant Growth, Protection from Energy (L9); Ice Storm, Stoneskin (L13); Commune with Nature, Tree Stride (L17).
- **Aura of Warding** (level 7): You and allies have Resistance to Necrotic, Psychic, and Radiant damage while in your Aura of Protection.
- **Undying Sentinel** (level 15): When reduced to 0 HP but not killed outright, drop to 1 HP instead and regain HP equal to 3x your Paladin level; once per Long Rest. Also, you can't be magically aged and stop visibly aging.
- **Elder Champion** (level 20): As a Bonus Action, imbue your Aura of Protection for 1 minute (or until dismissed, no action) — **Diminish Defiance**: enemies in the aura have Disadvantage on saves against your spells and Channel Divinity options. **Regeneration**: regain 10 HP at the start of each of your turns. **Swift Spells**: cast action-casting-time spells as a Bonus Action instead. Once per Long Rest; restorable by expending a level 5 spell slot (no action).

**Subclass — Oath of Vengeance:** The Oath of Vengeance is a solemn commitment to punish those who have committed grievously evil acts. When evil armies slaughter helpless villagers, when a tyrant defies the will of the gods, when a thieves' guild grows too violent, when a dragon rampages through the countryside—at times like these, paladins arise and swear an Oath of Vengeance to set right what has gone wrong.
  Tenets: Show the wicked no mercy. Fight injustice and its causes. Aid those harmed by injustice.
- **Oath of Vengeance Spells** (level 3, and levels 5/9/13/17): Always prepared — Bane, Hunter's Mark (L3); Hold Person, Misty Step (L5); Haste, Protection from Energy (L9); Banishment, Dimension Door (L13); Hold Monster, Scrying (L17).
- **Vow of Enmity** (level 3): When you take the Attack action, expend a Channel Divinity use to swear vengeance on a creature within 30 ft — Advantage on attack rolls against it for 1 minute or until reused. Transferable (no action) to a different creature within 30 ft if the original drops to 0 HP first.
- **Relentless Avenger** (level 7): On hitting with an Opportunity Attack, reduce the target's Speed to 0 until end of the current turn, then move up to half your Speed as part of the same Reaction, without provoking Opportunity Attacks.
- **Soul of Vengeance** (level 15): Immediately after a creature under your Vow of Enmity hits or misses with an attack roll, you can take a Reaction to make a melee attack against it if in range.
- **Avenging Angel** (level 20): As a Bonus Action, gain for 10 minutes (or until dismissed, no action) — **Flight**: spectral wings, Fly Speed 60 ft, can hover. **Frightful Aura**: enemies starting their turn in your Aura of Protection fail a Wisdom save or are Frightened 1 minute (or until damaged); attacks against a Frightened creature this way have Advantage. Once per Long Rest; restorable by expending a level 5 spell slot (no action).

---

### Ranger
**Hit Die:** d10  **Saves:** STR, DEX
  **Spellcasting:** WIS

**Proficiencies:** Light Armor, Medium Armor, Shields, Simple Weapons, Martial Weapons, Saving Throw: DEX, Saving Throw: STR
**Choose:** Choose 3: Animal Handling, Athletics, Insight, Investigation, Nature, Perception, Stealth, or Survival
**Starting Equipment:** Choose A or B: (A) Studded Leather Armor, Scimitar, Shortsword, Longbow, 20 Arrows, Quiver, Druidic Focus (sprig of mistletoe), Explorer's Pack, 7 GP; or (B) 150 GP

**Class table (Favored Enemy uses / Prepared Spells by level; spell slots 1-5 follow standard half-caster progression):**
| Level | PB | Features | Favored Enemy | Prepared |
|---|---|---|---|---|
| 1 | +2 | Spellcasting, Favored Enemy, Weapon Mastery | 2 | 2 |
| 2 | +2 | Deft Explorer, Fighting Style | 2 | 3 |
| 3 | +2 | Ranger Subclass | 2 | 4 |
| 4 | +2 | Ability Score Improvement | 2 | 5 |
| 5 | +3 | Extra Attack | 3 | 6 |
| 6 | +3 | Roving | 3 | 6 |
| 7 | +3 | Subclass Feature | 3 | 7 |
| 8 | +3 | Ability Score Improvement | 3 | 7 |
| 9 | +4 | Expertise | 4 | 8 |
| 10 | +4 | Tireless | 4 | 8 |
| 11 | +4 | Subclass Feature | 4 | 10 |
| 12 | +4 | Ability Score Improvement | 4 | 10 |
| 13 | +5 | Relentless Hunter | 5 | 11 |
| 14 | +5 | Nature's Veil | 5 | 11 |
| 15 | +5 | Subclass Feature | 5 | 12 |
| 16 | +5 | Ability Score Improvement | 5 | 12 |
| 17 | +6 | Precise Hunter | 6 | 14 |
| 18 | +6 | Feral Senses | 6 | 14 |
| 19 | +6 | Epic Boon | 6 | 15 |
| 20 | +6 | Foe Slayer | 6 | 15 |

**Features (all levels):**

- **Favored Enemy** (level 1): You always have the Hunter's Mark spell prepared. You can cast it twice without expending a spell slot, and you regain all expended uses of this ability when you finish a Long Rest.
  The number of times you can cast the spell without a spell slot increases when you reach certain Ranger levels, as shown in the Favored Enemy column of the Ranger Features table.
- **Spellcasting** (level 1): You have learned to channel the magical essence of nature to cast spells. See "Spells" for the rules on spellcasting. The information below details how you use those rules with Ranger spells, which appear in the Ranger spell list later in the class's description.
  Spell Slots. The Ranger Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest.
  Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose two level 1
Ranger spells. Cure Wounds and Ensnaring Strike are recommended.
  The number of spells on your list increases as you gain Ranger levels, as shown in the Prepared Spells column of the Ranger Features table. Whenever that number increases, choose additional Ranger spells until the number of spells on your list matches the number in the Ranger Features table. The chosen spells must be of a level for which you have spell slots. For example, if you're a level 5 Ranger, your list of prepared spells can include six Ranger spells of level 1 or 2 in any combination.
  If another Ranger feature gives you spells that you always have prepared, those spells don't count against the number of spells you can prepare with this feature, but those spells otherwise count as Ranger spells for you.
Changing Your Prepared Spells. Whenever you finish a Long Rest, you can replace one spell on your list with another Ranger spell for which you have spell slots.
  Spellcasting Ability. Wisdom is your spellcasting ability for your Ranger spells.
  Spellcasting Focus. You can use a Druidic Focus as a Spellcasting Focus for your Ranger spells.
- **Weapon Mastery** (level 1): Your training with weapons allows you to use the mastery properties of two kinds of weapons of your choice with which you have proficiency, such as Longbows and Shortswords.
  Whenever you finish a Long Rest, you can change the kinds of weapons you chose. For example, you could switch to using the mastery properties of Scimitars and Longswords.
- **Deft Explorer** (level 2): Thanks to your travels, you gain the following benefits.
  Expertise. Choose one of your skill proficiencies with which you lack Expertise. You gain Expertise in that skill.
  Languages. You know two languages of your choice from the language tables in "Character Creation."
- **Fighting Style** (level 2): You gain a Fighting Style feat of your choice (see "Feats"). Instead of choosing one of those feats, you can choose the option below.
  Druidic Warrior. You learn two Druid cantrips of your choice (see the Druid class's section for a list of Druid spells). Guidance and Starry Wisp are recommended. The chosen cantrips count as Ranger spells for you, and Wisdom is your spellcasting ability for them. Whenever you gain a Ranger level, you can replace one of these cantrips with another Druid cantrip.
- **Ranger Subclass** (level 3): Choose Beast Master, Fey Wanderer, Gloom Stalker, or Hunter. Gain each subclass feature at your Ranger level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Extra Attack** (level 5): Attack twice instead of once when you take the Attack action.
- **Roving** (level 6): Speed +10 ft while not wearing Heavy Armor; also gain a Climb Speed and Swim Speed equal to your Speed.
- **Expertise** (level 9): Choose two skill proficiencies you lack Expertise in; gain Expertise in them.
- **Tireless** (level 10): **Temporary Hit Points** — as an action, gain 1d8 + Wisdom modifier Temp HP (minimum 1); uses equal to your Wisdom modifier (minimum once), regained on a Long Rest. **Decrease Exhaustion** — your Exhaustion level (if any) decreases by 1 on finishing a Short Rest.
- **Relentless Hunter** (level 13): Taking damage can't break your Concentration on Hunter's Mark.
- **Nature's Veil** (level 14): As a Bonus Action, give yourself the Invisible condition until the end of your next turn. Uses equal to your Wisdom modifier (minimum once), regained on a Long Rest.
- **Precise Hunter** (level 17): Advantage on attack rolls against the creature currently marked by your Hunter's Mark.
- **Feral Senses** (level 18): Gain Blindsight with a range of 30 ft.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Dimensional Travel recommended.
- **Foe Slayer** (level 20): Hunter's Mark's damage die becomes a d10 instead of a d6.

**Subclass — Beast Master:** A Beast Master forms a mystical bond with a special animal, drawing on primal magic and a deep connection to the natural world.
- **Primal Companion** (level 3): Summon a primal beast (choose stat block: Beast of the Land, Beast of the Sea, or Beast of the Sky, and the kind of animal appropriate to it) — Friendly to you and allies, obeys your commands, vanishes if you die. **The Beast in Combat**: acts on your turn — moves and uses its Reaction on its own, but only takes the Dodge action unless you use a Bonus Action to command another action from its stat block, or you sacrifice one of your own Attack-action attacks to command its Beast's Strike action. If you're Incapacitated, it acts fully on its own. **Restoring or Replacing**: if it died within the last hour, a Magic action + spell slot touching it revives it in 1 minute at full HP; on a Long Rest, you can summon a different beast (old one vanishes) in an unoccupied space within 5 ft.
- **Exceptional Training** (level 7): When commanding an action via Bonus Action, you can also command Dash, Disengage, Dodge, or Help as its Bonus Action. Its damage-dealing hits can be Force damage or normal type, your choice.
- **Bestial Fury** (level 11): Beast's Strike action can be used twice when commanded. First hit each turn on a creature under your Hunter's Mark deals extra Force damage equal to that spell's bonus damage.
- **Share Spells** (level 15): When you cast a spell targeting only yourself, you can also affect your Primal Companion if it's within 30 ft.

**Subclass — Fey Wanderer:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

**Subclass — Gloom Stalker:** Gloom Stalkers are at home in the darkest places, wielding magic drawn from the Shadowfell to combat enemies that lurk in darkness.
- **Dread Ambusher** (level 3): **Ambusher's Leap** — Speed +10 ft until end of turn, at the start of the first turn of each combat. **Dreadful Strike** — once per turn on a weapon hit, extra 2d6 Psychic damage; uses equal to your Wisdom modifier (minimum once), regained on a Long Rest. **Initiative Bonus** — add your Wisdom modifier to Initiative rolls.
- **Gloom Stalker Spells** (level 3, and levels 5/9/13/17): Always prepared — Disguise Self (L3); Rope Trick (L5); Fear (L9); Greater Invisibility (L13); Seeming (L17).
- **Umbral Sight** (level 3): Darkvision 60 ft, or +60 ft if you already have it. While entirely in Darkness, you're Invisible to creatures relying on Darkvision to see you there.
- **Iron Mind** (level 7): Proficiency in Wisdom saving throws (or, if you already have it, Intelligence or Charisma, your choice).
- **Stalker's Flurry** (level 11): Dreadful Strike's damage becomes 2d8. When you use it, also choose one: **Sudden Strike** — another attack with the same weapon against a different creature within 5 ft of the original target and in range; **Mass Fear** — the target and each creature within 10 ft make a Wisdom save or are Frightened until the start of your next turn.
- **Shadowy Dodge** (level 15): Reaction when a creature makes an attack roll against you — impose Disadvantage on it; regardless of hit or miss, you can then teleport up to 30 ft to an unoccupied space you can see.

**Subclass — Hunter:** You stalk prey in the wilds and elsewhere, using your abilities as a Hunter to protect nature and people everywhere from forces that would destroy them.
- **Hunter's Lore** (level 3): While a creature is marked by your Hunter's Mark, you know whether it has any Immunities/Resistances/Vulnerabilities, and what they are.
- **Hunter's Prey** (level 3): Choose one (swappable on a Short or Long Rest): **Colossus Slayer** — once per turn, a weapon hit deals an extra 1d8 damage if the target is missing any HP; **Horde Breaker** — once per turn on a weapon attack, make another attack with the same weapon against a different creature within 5 ft of the original target, within range, that you haven't attacked this turn.
- **Defensive Tactics** (level 7): Choose one (swappable on a Short or Long Rest): **Escape the Horde** — Opportunity Attacks against you have Disadvantage; **Multiattack Defense** — a creature that hits you with an attack has Disadvantage on all its other attack rolls against you that turn.
- **Superior Hunter's Prey** (level 11): Once per turn when you damage a creature marked by Hunter's Mark, also deal that spell's extra damage to a different creature you can see within 30 ft of the first.
- **Superior Hunter's Defense** (level 15): Reaction when you take damage — gain Resistance to that damage type (and any other damage of the same type) until the end of the current turn.

---

### Rogue
**Hit Die:** d8  **Saves:** DEX, INT
  **Note:** the previous version of this entry had an incorrect Proficiencies line (an apparent stale-cache artifact); corrected below from the verbatim PDF.

**Proficiencies:** Light Armor, Simple Weapons, Martial Weapons with the Finesse or Light property, Tool: Thieves' Tools, Saving Throw: DEX, Saving Throw: INT
**Choose:** Choose 4: Acrobatics, Athletics, Deception, Insight, Intimidation, Investigation, Perception, Persuasion, Sleight of Hand, or Stealth
**Starting Equipment:** Choose A or B: (A) Leather Armor, 2 Daggers, Shortsword, Shortbow, 20 Arrows, Quiver, Thieves' Tools, Burglar's Pack, 8 GP; or (B) 100 GP

**Class table (Sneak Attack damage by level):**
| Level | PB | Features | Sneak Attack |
|---|---|---|---|
| 1 | +2 | Expertise, Sneak Attack, Thieves' Cant, Weapon Mastery | 1d6 |
| 2 | +2 | Cunning Action | 1d6 |
| 3 | +2 | Rogue Subclass, Steady Aim | 2d6 |
| 4 | +2 | Ability Score Improvement | 2d6 |
| 5 | +3 | Cunning Strike, Uncanny Dodge | 3d6 |
| 6 | +3 | Expertise | 3d6 |
| 7 | +3 | Evasion, Reliable Talent | 4d6 |
| 8 | +3 | Ability Score Improvement | 4d6 |
| 9 | +4 | Subclass Feature | 5d6 |
| 10 | +4 | Ability Score Improvement | 5d6 |
| 11 | +4 | Improved Cunning Strike | 6d6 |
| 12 | +4 | Ability Score Improvement | 6d6 |
| 13 | +5 | Subclass Feature | 7d6 |
| 14 | +5 | Devious Strikes | 7d6 |
| 15 | +5 | Slippery Mind | 8d6 |
| 16 | +5 | Ability Score Improvement | 8d6 |
| 17 | +6 | Subclass Feature | 9d6 |
| 18 | +6 | Elusive | 9d6 |
| 19 | +6 | Epic Boon | 10d6 |
| 20 | +6 | Stroke of Luck | 10d6 |

**Features (all levels):**
- **Expertise** (level 1): Gain Expertise in two skill proficiencies of your choice (Sleight of Hand and Stealth recommended); two more at level 6.
- **Sneak Attack** (level 1): Once per turn, deal extra damage (per the table) to a creature you hit with a Finesse or Ranged weapon attack, if you have Advantage on the roll — or don't need Advantage if an ally without the Incapacitated condition is within 5 ft of the target and you don't have Disadvantage. Damage type matches the weapon.
- **Thieves' Cant** (level 1): Know Thieves' Cant and one other language of your choice.
- **Weapon Mastery** (level 1): Use the mastery properties of two kinds of weapons you're proficient with (e.g. Daggers and Shortbows); change your choices on a Long Rest.
- **Cunning Action** (level 2): Bonus Action Dash, Disengage, or Hide.
- **Rogue Subclass** (level 3): Choose Arcane Trickster, Assassin, Soulknife, or Thief. Gain each subclass feature at your Rogue level or lower.
- **Steady Aim** (level 3): As a Bonus Action (if you haven't moved this turn), gain Advantage on your next attack roll this turn; your Speed becomes 0 until end of turn.
- **Ability Score Improvement** (levels 4, 8, 10, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Cunning Strike** (level 5): When dealing Sneak Attack damage, forgo some Sneak Attack dice (removed before rolling) to add an effect immediately after damage; save DC = 8 + Dexterity modifier + Proficiency Bonus. **Poison** (cost 1d6, requires a Poisoner's Kit on you): Constitution save or Poisoned 1 minute (repeats save at end of its turns). **Trip** (cost 1d6): Large-or-smaller target fails a Dexterity save or is Prone. **Withdraw** (cost 1d6): move up to half your Speed immediately after the attack without Opportunity Attacks.
- **Uncanny Dodge** (level 5): Reaction when a visible attacker hits you — halve that attack's damage (round down).
- **Evasion** (level 7): On a Dexterity save for half damage, take none on success and half on failure. Doesn't work while Incapacitated.
- **Reliable Talent** (level 7): Treat a d20 roll of 9 or lower as a 10 on ability checks using a skill or tool proficiency you have.
- **Improved Cunning Strike** (level 11): Use up to two Cunning Strike effects per Sneak Attack, paying each die cost.
- **Devious Strikes** (level 14): New Cunning Strike options — **Daze** (cost 2d6): Constitution save or, on its next turn, the target can only move, or take an action, or take a Bonus Action (not more than one). **Knock Out** (cost 6d6): Constitution save or Unconscious 1 minute or until damaged (repeats save at end of its turns). **Obscure** (cost 3d6): Dexterity save or Blinded until end of its next turn.
- **Slippery Mind** (level 15): Proficiency in Wisdom and Charisma saving throws.
- **Elusive** (level 18): No attack roll can have Advantage against you unless you're Incapacitated.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of the Night Spirit recommended.
- **Stroke of Luck** (level 20): If you fail a d20 Test, turn that roll into a 20. Once per Short or Long Rest.

**Subclass — Arcane Trickster:** Some Rogues enhance their fine-honed skills of stealth and agility with spells, learning magical tricks to aid them in their trade. Some Arcane Tricksters use their talents as pickpockets and burglars, while others are pranksters.
- **Spellcasting** (level 3): Cantrips — know Mage Hand plus 2 more from the Wizard list (Mind Sliver, Minor Illusion recommended); replace any but Mage Hand on level-up; learn a 4th at level 10. Prepared Spells — start with 3 level-1 Wizard spells (Charm Person, Disguise Self, Fog Cloud recommended); grows per the table below; replace one on level-up. Intelligence is your spellcasting ability; an Arcane Focus works as a Spellcasting Focus.
  | Rogue Level | Prepared | Slots 1 | 2 | 3 | 4 |
  |---|---|---|---|---|---|
  | 3 | 3 | 2 | — | — | — |
  | 4-6 | 4 | 3 | — | — | — |
  | 7-9 | 5-6 | 4 | 2 | — | — |
  | 10-12 | 7-8 | 4 | 3 | — | — |
  | 13-15 | 9-10 | 4 | 3 | 2 | — |
  | 16-18 | 11 | 4 | 3 | 3 | — |
  | 19-20 | 12-13 | 4 | 3 | 3 | 1 |
- **Mage Hand Legerdemain** (level 3): Cast Mage Hand as a Bonus Action, make the hand Invisible, control it as a Bonus Action, and make Dexterity (Sleight of Hand) checks through it.
- **Magical Ambush** (level 9): If Invisible when you cast a spell on a creature, it has Disadvantage on its save against that spell this turn.
- **Versatile Trickster** (level 13): When using the Trip Cunning Strike option, you can also apply it to another creature within 5 ft of your Mage Hand.
- **Spell Thief** (level 17): Reaction immediately after a creature's spell targets or includes you in its area — Intelligence save vs your spell save DC; fail: negate the effect against you and steal the spell (if level 1+ and castable by you) for 8 hours (original caster can't cast it during that time). Once per Long Rest.

**Subclass — Assassin:** An Assassin's training focuses on using stealth, poison, and disguise to eliminate foes with deadly efficiency. While some Rogues who follow this path are hired killers, spies, or bounty hunters, the capabilities of this subclass are equally useful for adventurers facing a variety of monstrous enemies.
- **Assassinate** (level 3): **Initiative** — Advantage on Initiative rolls. **Surprising Strikes** — during the first round of combat, Advantage on attack rolls against any creature that hasn't taken a turn; a Sneak Attack hit that round deals extra damage (weapon's type) equal to your Rogue level.
- **Assassin's Tools** (level 3): Gain a Disguise Kit and Poisoner's Kit, with proficiency in both.
- **Infiltration Expertise** (level 9): **Masterful Mimicry** — unerringly mimic a studied (1+ hour) person's speech and/or handwriting. **Roving Aim** — Steady Aim no longer reduces your Speed to 0.
- **Envenom Weapons** (level 13): Poison Cunning Strike also deals 2d6 Poison damage on a failed save, ignoring Poison Resistance.
- **Death Strike** (level 17): A Sneak Attack hit in the first round of combat forces a Constitution save (DC 8 + Dexterity modifier + Proficiency Bonus); fail: damage doubled against the target.

**Subclass — Soulknife:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

**Subclass — Thief:** A mix of burglar, treasure hunter, and explorer, you are the epitome of an adventurer. In addition to improving your agility and stealth, you gain abilities useful for delving into ruins and getting maximum benefit from the magic items you find there.
- **Fast Hands** (level 3): As a Bonus Action — Dexterity (Sleight of Hand) check to pick a lock/disarm a trap with Thieves' Tools or pick a pocket; or take the Utilize action; or take the Magic action for a magic item that needs it.
- **Second-Story Work** (level 3): **Climber** — Climb Speed equal to your Speed. **Jumper** — use Dexterity instead of Strength for jump distance.
- **Supreme Sneak** (level 9): New Cunning Strike option — **Stealth Attack** (cost 1d6): if Invisible from the Hide action, this attack doesn't end that condition if you end the turn behind Three-Quarters or Total Cover.
- **Use Magic Device** (level 13): **Attunement** — attune to up to 4 magic items. **Charges** — roll 1d6 when using a charge-consuming property; on a 6, no charge spent. **Scrolls** — use any Spell Scroll with Intelligence as spellcasting ability; cantrips/level-1 spells cast reliably, higher-level spells need an Intelligence (Arcana) check (DC 10 + spell level) or the scroll disintegrates.
- **Thief's Reflexes** (level 17): Take two turns in the first round of combat — first at normal Initiative, second at Initiative − 10.

---

### Sorcerer
**Hit Die:** d6  **Saves:** CON, CHA
  **Spellcasting:** CHA

**Proficiencies:** Simple Weapons, Saving Throw: CON, Saving Throw: CHA
**Choose:** Choose 2: Arcana, Deception, Insight, Intimidation, Persuasion, or Religion
**Starting Equipment:** Choose A or B: (A) Spear, 2 Daggers, Arcane Focus (crystal), Dungeoneer's Pack, 28 GP; or (B) 50 GP

**Class table (Sorcery Points / Cantrips / Prepared Spells by level; spell slots 1-9 follow standard full-caster progression):**
| Level | PB | Features | Sorcery Points | Cantrips | Prepared |
|---|---|---|---|---|---|
| 1 | +2 | Spellcasting, Innate Sorcery | — | 4 | 2 |
| 2 | +2 | Font of Magic, Metamagic | 2 | 4 | 4 |
| 3 | +2 | Sorcerer Subclass | 3 | 4 | 6 |
| 4 | +2 | Ability Score Improvement | 4 | 5 | 7 |
| 5 | +3 | Sorcerous Restoration | 5 | 5 | 9 |
| 6 | +3 | Subclass Feature | 6 | 5 | 10 |
| 7 | +3 | Sorcery Incarnate | 7 | 5 | 11 |
| 8 | +3 | Ability Score Improvement | 8 | 5 | 12 |
| 9 | +4 | — | 9 | 5 | 14 |
| 10 | +4 | Metamagic | 10 | 6 | 15 |
| 11 | +4 | — | 11 | 6 | 16 |
| 12 | +4 | Ability Score Improvement | 12 | 6 | 16 |
| 13 | +5 | — | 13 | 6 | 17 |
| 14 | +5 | Subclass Feature | 14 | 6 | 17 |
| 15 | +5 | — | 15 | 6 | 18 |
| 16 | +5 | Ability Score Improvement | 16 | 6 | 18 |
| 17 | +6 | Metamagic | 17 | 6 | 19 |
| 18 | +6 | Subclass Feature | 18 | 6 | 20 |
| 19 | +6 | Epic Boon | 19 | 6 | 21 |
| 20 | +6 | Arcane Apotheosis | 20 | 6 | 22 |

**Features (all levels):**

- **Innate Sorcery** (level 1): An event in your past left an indelible mark on you, infusing you with simmering magic. As a Bonus Action, you can unleash that magic for 1 minute, during which you gain the following benefits: - The spell save DC of your Sorcerer spells increases by 1.
- You have Advantage on the attack rolls of Sorcerer spells you cast.
You can use this feature twice, and you regain all expended uses of it when you finish a Long Rest.
- **Spellcasting** (level 1): Drawing from your innate magic, you can cast spells. See "Spells" for the rules on spellcasting. The information below details how you use those rules with Sorcerer spells, which appear in the Sorcerer spell list later in the class’s description.
Cantrips. You know four Sorcerer cantrips of your choice. Light, Prestidigitation, Shocking Grasp, and Sorcerous Burst are recommended. Whenever you gain a Sorcerer level, you can replace one of your cantrips from this feature with another Sorcerer cantrip of your choice.
When you reach Sorcerer levels 4 and 10, you learn another Sorcerer cantrip of your choice, as shown in the Cantrips column of the Sorcerer Features table.
Spell Slots. The Sorcerer Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest.
Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose two level 1 Sorcerer spells. Burning Hands and Detect Magic are recommended.
The number of spells on your list increases as you gain Sorcerer levels, as shown in the Prepared Spells column of the Sorcerer Features table. Whenever that number increases, choose additional Sorcerer spells until the number of spells on your list matches the number in the Sorcerer Features table. The chosen spells must be of a level for which you have spell slots. For example, if you’re a level 3 Sorcerer, your list of prepared spells can include six Sorcerer spells of level 1 or 2 in any combination.
If another Sorcerer feature gives you spells that you always have prepared, those spells don’t count against the number of spells you can prepare with this feature, but those spells otherwise count as Sorcerer spells for you.
Changing Your Prepared Spells. Whenever you gain a Sorcerer level, you can replace one spell on your list with another Sorcerer spell for which you have spell slots.
Spellcasting Ability. Charisma is your spellcasting ability for your Sorcerer spells.
Spellcasting Focus. You can use an Arcane Focus as a Spellcasting Focus for your Sorcerer spells.
- **Font of Magic** (level 2): You can tap into the wellspring of magic within yourself. This wellspring is represented by Sorcery Points, which allow you to create a variety of magical effects.
You have 2 Sorcery Points, and you gain more as you reach higher levels, as shown in the Sorcery Points column of the Sorcerer Features table. You can’t have more Sorcery Points than the number shown in the table for your level. You regain all expended Sorcery Points when you finish a Long Rest.
You can use your Sorcery Points to fuel the options below, along with other features, such as Metamagic, that use those points.
Converting Spell Slots to Sorcery Points. You can expend a spell slot to gain a number of Sorcery Points equal to the slot’s level (no action required).
Creating Spell Slots. As a Bonus Action, you can transform unexpended Sorcery Points into one spell slot. The Creating Spell Slots table shows the cost of creating a spell slot of a given level, and it lists the minimum Sorcerer level you must be to create a slot. You can create a spell slot no higher than level 5.
Any spell slot you create with this feature vanishes when you finish a Long Rest.
Creating Spell Slots Spell Slot Level | Sorcery Point Cost | Min. Sorcerer Level
1 | 2 | 2
2 | 3 | 3
3 | 5 | 5
4 | 6 | 7
5 | 7 | 9
- **Metamagic** (level 2): Because your magic flows from within, you can alter your spells to suit your needs; you gain two Metamagic options of your choice from "Metamagic Options" later in this class’s description. You use the chosen options to temporarily modify spells you cast. To use an option, you must spend the number of Sorcery Points that it costs.
You can use only one Metamagic option on a spell when you cast it unless otherwise noted in one of those options.
Whenever you gain a Sorcerer level, you can replace one of your Metamagic options with one you don’t know. You gain two more options at Sorcerer level 10 and two more at Sorcerer level 17.
- **Sorcerer Subclass** (level 3): Choose Aberrant Sorcery, Clockwork Sorcery, Draconic Sorcery, or Wild Magic Sorcery. Gain each subclass feature at your Sorcerer level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Sorcerous Restoration** (level 5): On finishing a Short Rest, regain expended Sorcery Points up to half your Sorcerer level (round down). Once per Long Rest.
- **Sorcery Incarnate** (level 7): If you have no Innate Sorcery uses left, you can still activate it by spending 2 Sorcery Points when you take the Bonus Action. While Innate Sorcery is active, you can use up to two Metamagic options per spell cast.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Dimensional Travel recommended.
- **Arcane Apotheosis** (level 20): While Innate Sorcery is active, use one Metamagic option per turn without spending Sorcery Points.

**Metamagic Options** (alphabetical; you know 2 starting at level 2, +2 more at level 10, +2 more at level 17; only one option per spell unless noted):
- **Careful Spell** (1 SP): When casting a spell forcing a save, a number of creatures up to your Charisma modifier (minimum one) auto-succeed and take no damage even on a normally-half-damage success.
- **Distant Spell** (1 SP): Double a spell's range (5+ ft), or change Touch range to 30 ft.
- **Empowered Spell** (1 SP; usable even after another Metamagic option this casting): Reroll a number of damage dice up to your Charisma modifier (minimum one); must use new rolls.
- **Extended Spell** (1 SP): Double a spell's duration (1 minute or longer) up to a max of 24 hours; if it requires Concentration, gain Advantage on saves to maintain it.
- **Heightened Spell** (2 SP): One target of a save-forcing spell has Disadvantage on that save.
- **Quickened Spell** (2 SP): Change an action-casting-time spell to a Bonus Action this casting; can't do this if you've already cast a level 1+ spell this turn, and can't cast another level 1+ spell this turn after.
- **Seeking Spell** (1 SP; usable even after another Metamagic option this casting): On a missed spell attack roll, reroll the d20 and must use the new roll.
- **Subtle Spell** (1 SP): Cast without Verbal, Somatic, or Material components (except Material components that are consumed or have a specified cost).
- **Transmuted Spell** (1 SP): Change a spell's damage type (from Acid, Cold, Fire, Lightning, Poison, or Thunder) to another type on that list.
- **Twinned Spell** (1 SP): For a spell that can be upcast to target an extra creature (like Charm Person), increase its effective level by 1 instead of spending a slot for that purpose.

**Subclass — Aberrant Sorcery:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

**Subclass — Clockwork Sorcery:** *Confirmed unavailable even in this source PDF — the page literally says "See the Player's Handbook." This is a genuine content gap, not a transcription failure.*

**Subclass — Draconic Sorcery:** Your innate magic comes from the gift of a dragon. Perhaps an ancient dragon facing death bequeathed some of its magical power to you or your ancestor. You might have absorbed magic from a site infused with dragons' power. Or perhaps you handled a treasure taken from a dragon's hoard that was steeped in draconic power. Or you might have a dragon for an ancestor.
- **Draconic Resilience** (level 3): Max HP +3 (and +1 per Sorcerer level thereafter). While unarmored, base AC = 10 + Dexterity + Charisma modifiers.
- **Draconic Spells** (level 3, and levels 5/7/9): Always prepared — Alter Self, Chromatic Orb, Command, Dragon's Breath (L3); Fear, Fly (L5); Arcane Eye, Charm Monster (L7); Legend Lore, Summon Dragon (L9).
- **Elemental Affinity** (level 6): Choose Acid, Cold, Fire, Lightning, or Poison — gain Resistance to it, and add your Charisma modifier to one damage roll of a spell you cast that deals that type.
- **Dragon Wings** (level 14): As a Bonus Action, sprout wings for 1 hour (or until dismissed, no action) — Fly Speed 60 ft. Once per Long Rest; restorable by spending 3 Sorcery Points (no action).
- **Dragon Companion** (level 18): Cast Summon Dragon without a Material component; also once without a spell slot (regained on a Long Rest). You can forgo Concentration when casting it, capping the duration at 1 minute instead.

**Subclass — Wild Magic Sorcery:** Your innate magic stems from the forces of chaos that underlie the order of creation. You or an ancestor might have endured exposure to raw magic, perhaps through a planar portal leading to Limbo or the Elemental Planes. Perhaps you were blessed by a fey being or marked by a demon. Or your magic could be a fluke with no apparent cause. However it came to be, this magic churns within you, waiting for any outlet.
- **Wild Magic Surge** (level 3): Once per turn, immediately after casting a Sorcerer spell with a spell slot, roll 1d20; on a 20, roll on the Wild Magic Surge table (below). A resulting spell effect can't be modified by Metamagic.
- **Tides of Chaos** (level 3): Give yourself Advantage on one D20 Test before rolling. Then you must cast a Sorcerer spell with a spell slot (which auto-triggers a Wild Magic Surge table roll) or finish a Long Rest before using this again.
- **Bend Luck** (level 6): Reaction immediately after another visible creature rolls a d20 for a D20 Test — spend 1 Sorcery Point, roll 1d4, apply it as a bonus or penalty (your choice) to that roll.
- **Controlled Chaos** (level 14): Whenever you roll on the Wild Magic Surge table, roll twice and use either result.
- **Tamed Surge** (level 18): Immediately after casting a Sorcerer spell with a spell slot, choose any Wild Magic Surge table effect (except the final row) instead of rolling; if it involves a roll, you must make it. Once per Long Rest.
  - **Wild Magic Surge table** (d100): **01-04** Roll on this table at the start of each turn for 1 minute (ignore this result on later rolls). **05-08** A Friendly creature appears in a random unoccupied space within 60 ft for 1 minute (DM-controlled); roll 1d4: 1 Modron Duodrone, 2 Flumph, 3 Modron Monodrone, 4 Unicorn. **09-12** Regain 5 HP at the start of each turn for 1 minute. **13-16** Creatures have Disadvantage on saves against your next save-requiring spell within 1 minute. **17-20** You're subjected to a 1-minute effect (roll 1d8): 1 faint ethereal music audible to you/creatures within 5 ft; 2 size increases one category; 3 grow a feather beard until you sneeze; 4 must shout when speaking; 5 illusory butterflies within 10 ft; 6 an eye on your forehead grants Advantage on Wisdom (Perception); 7 pink bubbles float from your mouth when speaking; 8 skin turns vibrant blue for 24 hrs or until Remove Curse. **21-24** For 1 minute, your action-casting-time spells become Bonus-Action casting time. **25-28** Transported to the Astral Plane until the end of your next turn, then return to your space (or nearest unoccupied). **29-32** Next damage-dealing spell within 1 minute uses max damage on each die instead of rolling. **33-36** Resistance to all damage for 1 minute. **37-40** Turn into a potted plant until start of your next turn (Incapacitated, Vulnerable to all damage; reverts if reduced to 0 HP). **41-44** For 1 minute, teleport up to 20 ft as a Bonus Action each turn. **45-48** You and up to 3 chosen creatures within 30 ft are Invisible for 1 minute (ends per-creature after an attack roll, damage, or spellcast). **49-52** A spectral shield grants +2 AC and immunity to Magic Missile for 1 minute. **53-56** Take one extra action this turn. **57-60** Cast a random spell (no Concentration needed even if it normally requires it, lasts full duration) — roll 1d10: 1 Confusion, 2 Fireball, 3 Fog Cloud, 4 Fly (random creature within 60 ft), 5 Grease, 6 Levitate (self), 7 Magic Missile (as level 5), 8 Mirror Image, 9 Polymorph (self; failed save turns you into a Goat), 10 See Invisibility. **61-64** For 1 minute, flammable unattended objects you touch ignite (1d4 Fire, burning). **65-68** If you die within the next hour, revive as if by Reincarnate. **69-72** Frightened until end of your next turn (DM determines source). **73-76** Teleport up to 60 ft to an unoccupied space you can see. **77-80** A random creature within 60 ft is Poisoned for 1d4 hours. **81-84** Radiate Bright Light 30 ft for 1 minute; creatures ending their turn within 5 ft are Blinded until end of their next turn. **85-88** Up to 3 chosen creatures within 30 ft take 1d10 Necrotic; you regain HP equal to the total dealt. **89-92** Up to 3 chosen creatures within 30 ft take 4d10 Lightning. **93-96** You and all creatures within 30 ft have Vulnerability to Piercing for 1 minute. **97-00** Roll 1d6: 1 regain 2d10 HP; 2 an ally within 300 ft regains 2d10 HP; 3 regain your lowest-level expended spell slot; 4 an ally within 300 ft regains their lowest-level expended spell slot; 5 regain all expended Sorcery Points; 6 all of row 17-20's effects happen simultaneously.

---

### Warlock
**Hit Die:** d8  **Saves:** WIS, CHA
  **Spellcasting:** CHA

**Proficiencies:** Light Armor, Simple Weapons, Saving Throw: WIS, Saving Throw: CHA
**Choose:** Choose 2: from Arcana, Deception, History, Intimidation, Investigation, Nature, or Religion
**Starting Equipment:** Choose A or B: (A) Leather Armor, Sickle, 2 Daggers, Arcane Focus (orb), Book (occult lore), Scholar's Pack, 15 GP; or (B) 100 GP

**Class table (Eldritch Invocations / Cantrips / Prepared Spells / Pact Magic slots & level by level):**
| Level | PB | Features | Invocations | Cantrips | Prepared | Slots | Slot Level |
|---|---|---|---|---|---|---|---|
| 1 | +2 | Eldritch Invocations, Pact Magic | 1 | 2 | 2 | 1 | 1 |
| 2 | +2 | Magical Cunning | 3 | 2 | 3 | 2 | 1 |
| 3 | +2 | Warlock Subclass | 3 | 2 | 4 | 2 | 2 |
| 4 | +2 | Ability Score Improvement | 3 | 3 | 5 | 2 | 2 |
| 5 | +3 | — | 5 | 3 | 6 | 2 | 3 |
| 6 | +3 | Subclass Feature | 5 | 3 | 7 | 2 | 3 |
| 7 | +3 | — | 6 | 3 | 8 | 2 | 4 |
| 8 | +3 | Ability Score Improvement | 6 | 3 | 9 | 2 | 4 |
| 9 | +4 | Contact Patron | 7 | 3 | 10 | 2 | 5 |
| 10 | +4 | Subclass Feature | 7 | 4 | 10 | 2 | 5 |
| 11 | +4 | Mystic Arcanum (6th) | 7 | 4 | 11 | 3 | 5 |
| 12 | +4 | Ability Score Improvement | 8 | 4 | 11 | 3 | 5 |
| 13 | +5 | Mystic Arcanum (7th) | 8 | 4 | 12 | 3 | 5 |
| 14 | +5 | Subclass Feature | 8 | 4 | 12 | 3 | 5 |
| 15 | +5 | Mystic Arcanum (8th) | 9 | 4 | 13 | 3 | 5 |
| 16 | +5 | Ability Score Improvement | 9 | 4 | 13 | 3 | 5 |
| 17 | +6 | Mystic Arcanum (9th) | 9 | 4 | 14 | 4 | 5 |
| 18 | +6 | — | 10 | 4 | 14 | 4 | 5 |
| 19 | +6 | Epic Boon | 10 | 4 | 15 | 4 | 5 |
| 20 | +6 | Eldritch Master | 10 | 4 | 15 | 4 | 5 |

**Features (all levels):**

- **Eldritch Invocations** (level 1): You have unearthed Eldritch Invocations, pieces of forbidden knowledge that imbue you with an abiding magical ability or other lessons. You gain one invocation of your choice, such as Pact of the Tome. Invocations are described in the "Eldritch Invocation Options" section later in this class's description.
Prerequisites. If an invocation has a prerequisite, you must meet it to learn that invocation. For example, if an invocation requires you to be a level 5+ Warlock, you can select the invocation once you reach Warlock level 5.
Replacing and Gaining Invocations. Whenever you gain a Warlock level, you can replace one of your invocations with another one for which you qualify. You can't replace an invocation if it's a prerequisite for another invocation that you have.
When you gain certain Warlock levels, you gain more invocations of your choice, as shown in the Invocations column of the Warlock Features table.
You can't pick the same invocation more than once unless its description says otherwise.
- **Pact Magic** (level 1): Through occult ceremony, you have formed a pact with a mysterious entity to gain magical powers.
The entity is a voice in the shadows—its identity unclear—but its boon to you is concrete: the ability to cast spells. See "Spells" for the rules on spellcasting.
The information below details how you use those rules with Warlock spells, which appear in the Warlock spell list later in the class's description.
Cantrips. You know two Warlock cantrips of your choice. Eldritch Blast and Prestidigitation are recommended.
Whenever you gain a Warlock level, you can replace one of your cantrips from this feature with another Warlock cantrip of your choice.
When you reach Warlock levels 4 and 10, you learn another Warlock cantrip of your choice, as shown in the Cantrips column of the Warlock Features table.
Spell Slots. The Warlock Features table shows how many spell slots you have to cast your Warlock spells of levels 1–5. The table also shows the level of those slots, all of which are the same level. You regain all expended Pact Magic spell slots when you finish a Short or Long Rest.
For example, when you're a level 5 Warlock, you have two level 3 spell slots. To cast the level 1 spell Charm Person, you must spend one of those slots, and you cast it as a level 3 spell.
Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To start, choose two level 1 Warlock spells. Charm Person and Hex are recommended.
The number of spells on your list increases as you gain Warlock levels, as shown in the Prepared Spells column of the Warlock Features table. Whenever that number increases, choose additional Warlock spells until the number of spells on your list matches the number in the table. The chosen spells must be of a level no higher than what's shown in the table's Slot Level column for your level. When you reach level 6, for example, you learn a new Warlock spell, which can be of levels 1–3.
If another Warlock feature gives you spells that you always have prepared, those spells don't count against the number of spells you can prepare with this feature, but those spells otherwise count as Warlock spells for you.
Changing Your Prepared Spells. Whenever you gain a Warlock level, you can replace one spell on your list with another Warlock spell of an eligible level.
Spellcasting Ability. Charisma is the spellcasting ability for your Warlock spells.
Spellcasting Focus. You can use an Arcane Focus as a Spellcasting Focus for your Warlock spells.
- **Magical Cunning** (level 2): You can perform an esoteric rite for 1 minute. At the end of it, you regain expended Pact Magic spell slots but no more than a number equal to half your maximum (round up). Once you use this feature, you can't do so again until you finish a Long Rest.
- **Warlock Subclass** (level 3): Choose Archfey Patron, Celestial Patron, Fiend Patron, or Great Old One Patron. Gain each subclass feature at your Warlock level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Contact Patron** (level 9): You always have Contact Other Plane prepared, and can cast it without a spell slot and auto-succeed its save (to contact your patron specifically). Once per Long Rest.
- **Mystic Arcanum** (level 11, then 13/15/17): Choose a Warlock spell as your arcanum — level 6 at 11, plus level 7/8/9 at 13/15/17 respectively. Cast each once without a spell slot; regained on a Long Rest. Replace an arcanum spell (same level) on any level-up.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Fate recommended.
- **Eldritch Master** (level 20): Using Magical Cunning now regains all expended Pact Magic spell slots (not just half).

**Subclass — Archfey Patron:** Your pact draws on the power of the Feywild. When you choose this subclass, you might make a deal with an archfey, such as the Prince of Frost; the Queen of Air and Darkness, ruler of the Gloaming Court; Titania of the Summer Court; or an ancient hag. Or you might call on a spectrum of Fey, weaving a web of favors and debts. Whoever they are, your patron is often inscrutable and whimsical.
- **Archfey Spells** (level 3, and levels 5/7/9): Always prepared — Calm Emotions, Faerie Fire, Misty Step, Phantasmal Force, Sleep (L3); Blink, Plant Growth (L5); Dominate Beast, Greater Invisibility (L7); Dominate Person, Seeming (L9).
- **Steps of the Fey** (level 3): Cast Misty Step without a spell slot a number of times equal to your Charisma modifier (minimum once), regained on a Long Rest. Whenever cast, add one option: **Refreshing Step** — you or a creature within 10 ft gains 1d10 Temp HP; **Taunting Step** — creatures within 5 ft of the space you left make a Wisdom save or have Disadvantage on attacks against others until start of your next turn.
- **Misty Escape** (level 6): Cast Misty Step as a Reaction to taking damage. Adds two more Steps of the Fey options: **Disappearing Step** — Invisible until start of next turn or until you attack/damage/cast; **Dreadful Step** — creatures within 5 ft of the space you left or arrived in (your choice) make a Wisdom save or take 2d10 Psychic damage.
- **Beguiling Defenses** (level 10): Immune to Charmed. Reaction immediately after a visible creature hits you — halve that damage (round down) and force a Wisdom save vs your spell save DC on the attacker; fail: it takes Psychic damage equal to the damage you took. Once per Long Rest; restorable by expending a Pact Magic slot (no action).
- **Bewitching Magic** (level 14): Immediately after casting an Enchantment or Illusion spell (action + spell slot), cast Misty Step as part of the same action without a spell slot.

**Subclass — Celestial Patron:** Your pact draws on the Upper Planes, the realms of everlasting bliss. You might enter an agreement with an empyrean, a couatl, a sphinx, a unicorn, or another heavenly entity. Or you might call on numerous such beings as you pursue goals aligned with theirs. Your pact allows you to experience a hint of the holy light that illuminates the multiverse.
- **Celestial Spells** (level 3, and levels 5/7/9): Always prepared — Aid, Cure Wounds, Guiding Bolt, Lesser Restoration, Light, Sacred Flame (L3); Daylight, Revivify (L5); Guardian of Faith, Wall of Fire (L7); Greater Restoration, Summon Celestial (L9).
- **Healing Light** (level 3): A pool of d6s (count = 1 + your Warlock level). As a Bonus Action, heal yourself or a creature within 60 ft by expending up to your Charisma modifier's worth of dice (minimum one); roll and restore that total. Pool refills on a Long Rest.
- **Radiant Soul** (level 6): Resistance to Radiant damage. Once per turn, when a spell you cast deals Radiant or Fire damage, add your Charisma modifier to that damage against one target.
- **Celestial Resilience** (level 10): Gain Temp HP (= Warlock level + Charisma modifier) whenever you use Magical Cunning or finish a Short/Long Rest; up to 5 creatures you choose each gain Temp HP equal to half your Warlock level + Charisma modifier.
- **Searing Vengeance** (level 14): When you or an ally within 60 ft is about to make a Death Save, you can instead have them regain HP equal to half their max and end Prone; each creature you choose within 30 ft of them takes 2d8 + Charisma modifier Radiant damage and is Blinded until end of the current turn. Once per Long Rest.

**Subclass — Fiend Patron:** Your pact draws on the Lower Planes, the realms of perdition. You might forge a bargain with a demon lord, an archdevil, or another fiend that is especially mighty. That patron's aims are evil-the corruption or destruction of all things, ultimately including you-and your path is defined by the extent to which you strive against those aims.
- **Dark One's Blessing** (level 3): When you (or an ally within 10 ft) reduces an enemy to 0 HP, gain Temp HP equal to your Charisma modifier + Warlock level (minimum 1).
- **Fiend Spells** (level 3, and levels 5/7/9): Always prepared — Burning Hands, Command, Scorching Ray, Suggestion (L3); Fireball, Stinking Cloud (L5); Fire Shield, Wall of Fire (L7); Geas, Insect Plague (L9).
- **Dark One's Own Luck** (level 6): After seeing an ability check or save roll (but before its effects), add 1d10. Uses equal to your Charisma modifier (minimum once, max once per roll), regained on a Long Rest.
- **Fiendish Resilience** (level 10): Choose a damage type (not Force) on finishing a Short or Long Rest; gain Resistance to it until you choose differently.
- **Hurl Through Hell** (level 14): Once per turn on hitting with an attack, force a Charisma save vs your spell save DC — fail: target vanishes into the Lower Planes, taking 8d10 Psychic damage (unless a Fiend) and is Incapacitated until end of your next turn, then returns to its space (or nearest unoccupied). Once per Long Rest; restorable by expending a Pact Magic slot (no action).

**Subclass — Great Old One Patron:** When you choose this subclass, you might bind yourself to an unspeakable being from the Far Realm or an elder god—a being such as Tharizdun, the Chained God; Zargon, the Returner; Hadar, the Dark Hunger; or Great Cthulhu. Or you might invoke several entities without yoking yourself to one. The motives of these beings are incomprehensible, and the Great Old One might be indifferent to your existence. But the secrets you've learned nevertheless allow you to draw strange magic from it.
- **Awakened Mind** (level 3): As a Bonus Action, form a telepathic link with a creature within 30 ft, usable across a number of miles equal to your Charisma modifier (minimum 1); lasts minutes equal to your Warlock level, ends early if you link to someone else.
- **Great Old One Spells** (level 3, and levels 5/7/9): Always prepared — Detect Thoughts, Dissonant Whispers, Phantasmal Force, Tasha's Hideous Laughter (L3); Clairvoyance, Hunger of Hadar (L5); Confusion, Summon Aberration (L7); Modify Memory, Telekinesis (L9).
- **Psychic Spells** (level 3): Change a damage-dealing Warlock spell's type to Psychic; cast Enchantment/Illusion Warlock spells without Verbal/Somatic components.
- **Clairvoyant Combatant** (level 6): When forming an Awakened Mind bond, force a Wisdom save vs your spell save DC — fail: that creature has Disadvantage attacking you, and you have Advantage attacking it, for the bond's duration. Once per Short/Long Rest; restorable by expending a Pact Magic slot (no action).
- **Eldritch Hex** (level 10): Always have Hex prepared; when cast, the chosen-ability target also has Disadvantage on saves of that ability for the spell's duration.
- **Thought Shield** (level 10): Immune to telepathy unless you allow it. Resistance to Psychic damage; a creature dealing Psychic damage to you takes the same amount back.
- **Create Thrall** (level 14): Cast Summon Aberration without Concentration (capping duration at 1 minute); the summoned Aberration gets Temp HP equal to your Warlock level + Charisma modifier, and its first hit each turn on a creature under your Hex deals extra Psychic damage equal to Hex's bonus damage.

---

### Wizard
**Hit Die:** d6  **Saves:** INT, WIS
  **Spellcasting:** INT

**Proficiencies:** Simple Weapons, Saving Throw: INT, Saving Throw: WIS
**Choose:** Choose 2: Arcana, History, Insight, Investigation, Medicine, or Religion
**Starting Equipment:** Choose A or B: (A) 2 Daggers, Arcane Focus (Quarterstaff), Robe, Spellbook, Scholar's Pack, 5 GP; or (B) 55 GP

**Class table (Cantrips / Prepared Spells by level; spell slots 1-9 follow standard full-caster progression):**
| Level | PB | Features | Cantrips | Prepared |
|---|---|---|---|---|
| 1 | +2 | Spellcasting, Ritual Adept, Arcane Recovery | 3 | 4 |
| 2 | +2 | Scholar | 3 | 5 |
| 3 | +2 | Wizard Subclass | 3 | 6 |
| 4 | +2 | Ability Score Improvement | 4 | 7 |
| 5 | +3 | Memorize Spell | 4 | 9 |
| 6 | +3 | Subclass Feature | 4 | 10 |
| 7 | +3 | — | 4 | 11 |
| 8 | +3 | Ability Score Improvement | 4 | 12 |
| 9 | +4 | — | 4 | 14 |
| 10 | +4 | Subclass Feature | 5 | 15 |
| 11 | +4 | — | 5 | 16 |
| 12 | +4 | Ability Score Improvement | 5 | 16 |
| 13 | +5 | — | 5 | 17 |
| 14 | +5 | Subclass Feature | 5 | 18 |
| 15 | +5 | — | 5 | 19 |
| 16 | +5 | Ability Score Improvement | 5 | 21 |
| 17 | +6 | — | 5 | 22 |
| 18 | +6 | Spell Mastery | 5 | 23 |
| 19 | +6 | Epic Boon | 5 | 24 |
| 20 | +6 | Signature Spells | 5 | 25 |

**Features (all levels):**

- **Arcane Recovery** (level 1): You can regain some of your magical energy by studying your spellbook. When you finish a Short Rest, you can choose expended spell slots to recover.
The spell slots can have a combined level equal to no more than half your Wizard level (round up), and none of the slots can be level 6 or higher.
For example, if you’re a level 4 Wizard, you can recover up to two levels’ worth of spell slots, regaining either one level 2 spell slot or two level 1 spell slots.
Once you use this feature, you can’t do so again until you finish a Long Rest.
- **Ritual Adept** (level 1): You can cast any spell as a Ritual if that spell has the Ritual tag and the spell is in your spellbook. You needn’t have the spell prepared, but you must read from the book to cast a spell in this way.
- **Spellcasting** (level 1): As a student of arcane magic, you have learned to cast spells. See "Spells" for the rules on spellcasting.
The information below details how you use those rules with Wizard spells, which appear in the Wizard spell list later in the class’s description.
Cantrips. You know three Wizard cantrips of your choice. Light, Mage Hand, and Ray of Frost are recommended.
Whenever you finish a Long Rest, you can replace one of your cantrips from this feature with another Wizard cantrip of your choice.
another Wizard cantrip of your choice, as shown in the Cantrips column of the Wizard Features table.
Spellbook. Your wizardly apprenticeship culminated in the creation of a unique book: your spellbook. It is a Tiny object that weighs 3 pounds, contains 100 pages, and can be read only by you or someone casting Identify. You determine the book’s appearance and materials, such as a gilt-edged tome or a collection of vellum bound with twine.
The book contains the level 1+ spells you know. It starts with six level 1 Wizard spells of your choice.
Detect Magic, Feather Fall, Mage Armor, Magic Missile, Sleep, and Thunderwave are recommended.
Whenever you gain a Wizard level after 1, add two Wizard spells of your choice to your spellbook. Each of these spells must be of a level for which you have spell slots, as shown in the Wizard Features table.
The spells are the culmination of arcane research you do regularly.
Spell Slots. The Wizard Features table shows how many spell slots you have to cast your level 1+ spells. You regain all expended slots when you finish a Long Rest.
Prepared Spells of Level 1+. You prepare the list of level 1+ spells that are available for you to cast with this feature. To do so, choose four spells from your spellbook. The chosen spells must be of a level for which you have spell slots.
The number of spells on your list increases as you gain Wizard levels, as shown in the Prepared Spells column of the Wizard Features table. Whenever that number increases, choose additional Wizard spells until the number of spells on your list matches the number in the table. The chosen spells must be of a level for which you have spell slots. For example, if you’re a level 3 Wizard, your list of prepared spells can include six spells of levels 1 and 2 in any combination, chosen from your spellbook.
If another Wizard feature gives you spells that you always have prepared, those spells don’t count against the number of spells you can prepare with this feature, but those spells otherwise count as Wizard spells for you.
Changing Your Prepared Spells. Whenever you finish a Long Rest, you can change your list of prepared spells, replacing any of the spells there with spells from your spellbook.
Spellcasting Ability. Intelligence is your spellcasting ability for your Wizard spells.
Spellcasting Focus. You can use an Arcane Focus or your spellbook as a Spellcasting Focus for your Wizard spells.
- **Scholar** (level 2): While studying magic, you also specialized in another field of study. Choose one of the following skills in which you have proficiency: Arcana, History, Investigation, Medicine, Nature, or Religion.
You have Expertise in the chosen skill.
- **Wizard Subclass** (level 3): Choose Abjurer, Diviner, Evoker, or Illusionist. Gain each subclass feature at your Wizard level or lower.
- **Ability Score Improvement** (levels 4, 8, 12, 16): Gain the Ability Score Improvement feat or another feat you qualify for.
- **Memorize Spell** (level 5): On finishing a Short Rest, study your spellbook and swap one prepared level 1+ spell for another from the book.
- **Spell Mastery** (level 18): Choose a level 1 and a level 2 spell in your spellbook with a casting time of an action. Always prepared; cast either at its lowest level without a spell slot (a slot is needed to cast higher). Swap either spell (same level) on a Long Rest.
- **Epic Boon** (level 19): Gain an Epic Boon feat or another feat you qualify for; Boon of Spell Recall recommended.
- **Signature Spells** (level 20): Choose two level 3 spells in your spellbook. Always prepared; cast each once at level 3 without a spell slot (regained on a Short or Long Rest; a slot is needed to cast higher or to reuse before then).

**Subclass — Abjurer:** Your study of magic is focused on spells that block, banish, or protect—ending harmful effects, banishing evil influences, and protecting the weak. Abjurers are sought when baleful spirits require exorcism, when important locations must be guarded against magical spying, and when portals to other planes of existence must be closed. Adventuring parties value Abjurers for the protection they provide their companions against a variety of hostile magic and other attacks.
- **Abjuration Savant** (level 3): Add 2 Abjuration spells (level 2 or lower) to your spellbook for free; add one more free Abjuration spell (of an eligible level) each time you gain access to a new spell slot level.
- **Arcane Ward** (level 3): When casting an Abjuration spell with a slot, create a ward on yourself (lasts until a Long Rest) with HP max = 2x your Wizard level + Intelligence modifier; it absorbs damage you take (apply your Resistances/Vulnerabilities first) until it hits 0 HP, after which you take the remainder. Casting an Abjuration spell with a slot restores 2x the slot’s level to the ward’s HP; alternatively, as a Bonus Action, expend a slot for the same restoration. Can only be created once per Long Rest.
- **Projected Ward** (level 6): Reaction when a creature within 30 ft you can see takes damage — your Arcane Ward absorbs it instead (same Resistance/Vulnerability and overflow rules).
- **Spell Breaker** (level 10): Always have Counterspell and Dispel Magic prepared; can cast Dispel Magic as a Bonus Action, adding your Proficiency Bonus to its check. Casting either with a slot that fails to stop the target spell doesn’t expend the slot.
- **Spell Resistance** (level 14): Advantage on saves against spells; Resistance to spell damage.

**Subclass — Diviner:** The counsel of a Diviner is sought by those who seek a clearer understanding of the past, present, and future. As a Diviner, you strive to part the veils of space, time, and consciousness. You work to master spells of discernment, remote viewing, supernatural knowledge, and foresight.
- **Divination Savant** (level 3): Add 2 Divination spells (level 2 or lower) to your spellbook for free; add one more free Divination spell (of an eligible level) each time you gain access to a new spell slot level.
- **Portent** (level 3): On finishing a Long Rest, roll two d20s and record them; before any d20 Test (yours or a creature’s you can see), you can substitute one recorded roll instead (once per turn). Unused rolls are lost on your next Long Rest.
- **Expert Divination** (level 6): Casting a Divination spell with a level 2+ slot regains a spell slot of lower level than the one spent (max level 5).
- **The Third Eye** (level 10): As a Bonus Action, choose one until your next Short/Long Rest: **Darkvision** (120 ft); **Greater Comprehension** (read any language); **See Invisibility** (cast it without a slot). Once per Short/Long Rest.
- **Greater Portent** (level 14): Portent now rolls three d20s instead of two.

**Subclass — Evoker:** Your studies focus on magic that creates powerful elemental effects such as bitter cold, searing flame, rolling thunder, crackling lightning, and burning acid. Some Evokers find employment in military forces, serving as artillery to blast armies from afar. Others use their power to protect others, while some seek their own gain.
- **Evocation Savant** (level 3): Add 2 Evocation spells (level 2 or lower) to your spellbook for free; add one more free Evocation spell (of an eligible level) each time you gain access to a new spell slot level.
- **Potent Cantrip** (level 3): A creature that avoids your damaging cantrip (miss or successful save) still takes half damage, with no other cantrip effect.
- **Sculpt Spells** (level 6): When casting an Evocation spell affecting other visible creatures, choose a number of them equal to 1 + the spell’s level — they auto-succeed their save and take no damage on a would-be-half-damage success.
- **Empowered Evocation** (level 10): Add your Intelligence modifier to one damage roll of an Evocation spell you cast.
- **Overchannel** (level 14): Casting a damage-dealing spell (slot level 1-5) can deal maximum damage instead of rolling. First use each Long Rest: no cost. Subsequent uses before a Long Rest: take 2d12 Necrotic damage per spell slot level (ignores Resistance/Immunity), increasing by 1d12 per additional use.

**Subclass — Illusionist:** You specialize in magic that dazzles the senses and tricks the mind, and the illusions you craft make the impossible seem real.
- **Illusion Savant** (level 3): Add 2 Illusion spells (level 2 or lower) to your spellbook for free; add one more free Illusion spell (of an eligible level) each time you gain access to a new spell slot level.
- **Improved Illusions** (level 3): Cast Illusion spells without Verbal components; Illusion spells with range 10+ ft get +60 ft range. Also know Minor Illusion (doesn’t count against cantrips known, or learn a different cantrip if already known) — cast it as a Bonus Action, and create both a sound and an image with one casting.
- **Phantasmal Creatures** (level 6): Always have Summon Beast and Summon Fey prepared; casting either can change its school to Illusion (spectral appearance) and be cast without a spell slot (halves the summoned creature’s HP). Once per Long Rest for the no-slot casting.
- **Illusory Self** (level 10): Reaction when hit by an attack roll — interpose an illusory duplicate, causing an automatic miss (illusion then dissipates). Once per Short/Long Rest; restorable by expending a level 2+ spell slot (no action).
- **Illusory Reality** (level 14): When casting an Illusion spell with a slot, as a Bonus Action while it’s ongoing, make one inanimate nonmagical object part of the illusion real for 1 minute (can’t deal damage or impose conditions).

---

## Warlock Eldritch Invocations

Not modeled by dm20-protocol (no character-creation hook for choosing them —
Warlocks aren't in this campaign anyway, but keeping for reference/future use).
Eligible Warlock level noted where relevant.

- **Agonizing Blast** (2+): Add Charisma modifier to a damaging cantrip's damage rolls. Repeatable (different cantrip each time).
- **Armor of Shadows**: Cast Mage Armor on yourself at will.
- **Ascendant Step** (5+): Cast Levitate on yourself at will.
- **Devil's Sight** (2+): See normally in Dim Light and Darkness within 120 feet.
- **Devouring Blade** (12+, requires Thirsting Blade): Thirsting Blade's Extra Attack becomes two extra attacks.
- **Eldritch Mind**: Advantage on Concentration saves.
- **Eldritch Smite** (5+, requires Pact of the Blade): Once per turn, expend a Pact Magic slot on a pact-weapon hit for extra 1d8 Force damage per slot level (+Prone if Huge or smaller).
- **Eldritch Spear** (2+): A damaging cantrip's range increases by 30 ft per Warlock level. Repeatable.
- **Fiendish Vigor** (2+): Cast False Life on yourself at will, always max Temp HP.
- **Gaze of Two Minds** (5+): Bonus Action to perceive through a willing touched creature's senses.
- **Gift of the Depths** (5+): Waterbreathing + Swim Speed = Speed; cast Water Breathing once per Long Rest free.
- **Gift of the Protectors** (9+, requires Pact of the Tome): Named creatures in your Book of Shadows drop to 1 HP instead of 0, once per Long Rest.
- **Investment of the Chain Master** (5+, requires Pact of the Chain): Familiar gets Fly/Swim Speed 40ft, Bonus Action attack command, Necrotic/Radiant damage option, your spell save DC, and Resistance you can grant it.
- **Lessons of the First Ones** (2+): Gain one Origin feat. Repeatable (different feat each time).
- **Lifedrinker** (9+, requires Pact of the Blade): Once per turn on pact-weapon hit, extra 1d6 Necrotic/Psychic/Radiant damage + expend a Hit Die to heal.
- **Mask of the Many Faces** (2+): Cast Disguise Self at will.
- **Master of Myriad Forms** (5+): Cast Alter Self at will.
- **Misty Visions** (2+): Cast Silent Image at will.
- **One with Shadows** (5+): In Dim Light/Darkness, cast Invisibility on yourself at will.
- **Otherworldly Leap** (2+): Cast Jump on yourself at will.
- **Pact of the Blade**: Bonus Action to conjure/bond a pact weapon; use Charisma for its attacks; choose its damage type.
- **Pact of the Chain**: Learn Find Familiar (cast free); special forms available (Imp, Pseudodragon, Quasit, etc.); can sacrifice an attack for familiar's Reaction attack.
- **Pact of the Tome**: Conjure a Book of Shadows with 3 cantrips + 2 ritual level-1 spells from any class list, always prepared.
- **Repelling Blast** (2+): A damaging attack-roll cantrip can push a Large-or-smaller target 10 ft on hit. Repeatable.
- **Thirsting Blade** (5+, requires Pact of the Blade): Attack twice with pact weapon on Attack action.
- **Visions of Distant Realms** (9+): Cast Arcane Eye at will.
- **Whispers of the Grave** (7+): Cast Speak with Dead at will.
- **Witch Sight** (15+): Truesight, range 30 ft.
