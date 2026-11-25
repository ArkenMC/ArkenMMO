# Research: MMO classes, skill trees, casting, levelling, rebirths

Game design research that feeds the (not yet written) feature brief. Parts 1-4 are **sourced facts**. Parts 5-10 are a **proposal**: none of its numbers come from a source, and none have been playtested.

## Target version
**Paper 26.3** (`pom.xml`: `paper-api 26.3.build.205-stable`), Paper API only, no NMS, vanilla client. No ItemsAdder or ModelEngine research here. Resource packs and GUI art are covered by a separate note.

## Summary
- Each class gets **3 branches**, bought node by node in a chest GUI. One branch can reach its ultimate; a second can reach its keystone.
- **Level cap 50**, **26 tree points**, one free core skill, quadratic XP curve (about 47 h to cap under the stated assumption).
- Cast with **3-click combos** (4 assignable spell slots), ultimate on **swap-hands (F)** with a charge meter.
- **User decision:** the utility class is the **Captain** (Vanguard / Standard-Bearer / Warchanter), modelled on LOTRO's Captain with Minstrel flavour.
- **User decision:** a player picks a class **once**, normally after another plugin's tutorial, which opens the selection by command. Switching is out of scope, but data is stored per class.
- Respec is free out of combat. Rebirth is optional and per class.

## How far to trust the sources
- Several primary sites refused the fetch tool: UESP (403), the ESO forums (403), eso-hub (403), lotro-wiki.com (bot check), Fandom (402). Where a fact rests only on a **search-result summary** it is marked **[S]**. **[F]** means the page itself was fetched, through a summarising model, so re-check exact numbers before quoting them.
- **[U]** means unverified.

---

## 1. Wynncraft (facts)

### Classes and archetypes
- Five main classes: Archer, Warrior, Mage, Assassin, Shaman, plus cosmetic donor counterparts. Progress is per character, and players can have several. [F] [Classes](https://wynncraft.wiki.gg/wiki/Classes)
- Three archetypes per class [F] [Version 2.0](https://wynncraft.wiki.gg/wiki/Version_2.0): Warrior (Fallen, Battle Monk, Paladin), Archer (Boltslinger, Sharpshooter, Trapper), Mage (Riftwalker, Light Bender, Arcanist), Assassin (Shadestepper, Trickster, Acrobat), Shaman (Summoner, Ritualist, Acolyte). That page may predate later changes.
- Archetypes have their own mechanics. Archer examples: Boltslinger builds move speed on hits, Sharpshooter builds "Focus" from hits at 5+ blocks, Trapper places delayed traps. [F] [Archer tree](https://wynncraft.wiki.gg/wiki/Archer/Ability_Tree)

### Ability Tree
Sources: [F] [Ability Tree](https://wynncraft.wiki.gg/wiki/Ability_Tree), [F] [Warrior tree](https://wynncraft.wiki.gg/wiki/Warrior/Ability_Tree)
- Over 70 abilities per class, on several GUI pages.
- **Ability Points (AP):** 1 at combat level 1, 50 at level 120. The grant is front-loaded: 5 AP by level 8, 10 by 17, 20 by 34, 30 by 56, 40 by 84. (Some ranks can borrow 2-4 AP early.)
- **Costs:** 1 AP (spell unlocks, small upgrades, new effects) or 2 AP (major, archetype-core and ultimate nodes), colour coded.
- **Connections:** only a node connected to one you own can be taken. You can move down or sideways, not back up. The base spells are themselves tree nodes.
- **Gates:** some nodes need a prerequisite ability, a minimum count in an archetype, or both. Warrior ultimates need combat level 90 plus 14-17 in the archetype; Archer ultimates need level 90, 16 in the archetype and cost 2 AP.
- **Exclusivity:** some nodes "block" others, often as pairs (Enraged Blow and Radiance; Sacred Surge and Bloodlust). Mixing archetypes is otherwise allowed.
- **Reset:** costs 3 Ability Shards (from daily/weekly objectives and a quest), used in town. A newly bought node can be undone while the menu is still open. A free-edit mode lasts until you leave the safe area.
- Ultimates are charged by using abilities (Ultimate Meter, per the Archer page).

### Casting and mana
- Spells are 3-click combos. Mage: Meteor R-L-L (50 mana), Teleport R-R-R (25), Heal R-L-R (35), Ice Snake R-R-L (30). [F] [Mage](https://wynncraft.wiki.gg/wiki/Mage) (page is old; costs may differ now)
- Archer starts with a **left** click: Arrow Bomb L-R-R (45), Escape L-L-L (20), Arrow Storm L-R-L (35), Arrow Shield L-L-R (30). [F] [Archer tree](https://wynncraft.wiki.gg/wiki/Archer/Ability_Tree)
- **Repeat-cast penalty:** casting the same spell several times in quick succession raises its cost each time. [F] [Identifications](https://wynncraft.wiki.gg/wiki/Identifications)
- Mana regen and mana steal are item stats ("+X/5s", "+X/3s"). Same source. Base max mana and base regen: **[U]**.

### Level curve and skill points
- Cap 120 (plus a bonus level 121). XP to advance from a level [F] [Combat Level](https://wynncraft.wiki.gg/wiki/Combat_Level): L1 150, L2 320, L10 1,850, L20 5,730, L30 16,600, L50 145,000, L70 1,040,400, L90 5,533,840, L100 14,418,250, L106 31,035,290, L120 1,145,146,860. This is roughly exponential, with a huge last step.
- XP sources: quests, mobs (3% less per level of difference), dungeons, raids, boss altars, discoveries, caves. Nearby party members get 20% of kill XP. Same source.
- **Skill Points** (attributes, separate from AP): 2 per level, 200 total at level 101. Five stats (Strength, Dexterity, Intelligence, Defence, Agility), 100 manual cap per stat, 150 with items, with diminishing percentages. Intelligence raises max mana and reduces spell cost (up to 50%). Free reset in towns. [F] [Skill Points](https://wynncraft.wiki.gg/wiki/Skill_Points)

---

## 2. Elder Scrolls Online (facts)
- Each class has **three class skill lines**. Since Update 46 (June 2025, "subclassing") up to two can be swapped for other classes' lines; at least one original stays. [S] [subclassing test server coverage](https://eso-hub.com/en/news/eso-subclassing-power-shifts-and-player-concerns-so-far-on-the-test-server), [S] [U46 notes](https://hacktheminotaur.com/eso-guides/eso-update-46-complete-patch-notes-subclassing-new-zone-gear-sets-more/)
- Skills are **actives, passives and ultimates**, unlocked by skill line level and bought with skill points. [S] [UESP Skills](https://en.uesp.net/wiki/Online:Skills)
- **Morphs:** after a skill reaches rank IV, 1 skill point turns it into one of **two** variants; only one at a time. The morph ranks up again. [S] same
- **Ultimates** use a separate resource that builds in combat; casting empties it (UESP notes one exception). Light or heavy attack hits grant 3 Ultimate per second for 9 s. [S] [UESP Skills](https://en.uesp.net/wiki/Online:Skills), [S] [UESP Light Attack](https://en.m.uesp.net/wiki/Online:Light_Attack). Maximum pool: **[U]**.
- **Skill line XP:** a class line advances only if one of its actives or its ultimate is slotted on the active bar when XP is earned; more slotted skills means faster progress. The bar holds five regular skills plus an ultimate. [S] [UESP Skills](https://en.uesp.net/wiki/Online:Skills), [official guide URL](https://www.elderscrollsonline.com/en-us/newplayerguide/skills) (age-gated on fetch). Second-bar unlock level: **[U]**.
- Skill points come from levels and collectibles (a guide: 1 point per 3 skyshards). [S] [guide](https://hacktheminotaur.com/eso-guides/how-to-get-skill-points-fast/) **[U]** for totals.
- **Champion Points (CP):** post-50 progression using the same XP activities, cap 3600, three constellations (Warfare, Fitness, Craft). Stars are passive or **slottable**; four slottable slots per constellation, swappable free out of combat. [F] [CP guide](https://arzyelbuilds.com/champion-points-guide-elder-scrolls-online/) (third party)
- **Respec:** Update 49 (March 2026) made **skill and attribute respecs free** from the UI, not usable in combat or some content, with a short cooldown. [S] [eso-hub](https://eso-hub.com/en/news/eso-u49-makes-skill-and-attribute-respecs-completely-free), [S] [official notes thread](https://forums.elderscrollsonline.com/en/discussion/689473/update-49-live-patch-notes-all-platforms), [F] [summary](https://arzyelbuilds.com/eso-update-49/). Current CP respec cost: **[U]**.

---

## 3. LOTRO (facts)

### Trait trees
- Three trees per class (blue, red, yellow); you pick one as your specialization. In the 2013 design, traits cost 1 point inside the specialization and **2 outside it**, and spending points in a line opens traits further down it. [F, 2013, may be outdated] [Trait Trees basics](https://lotrolibrary.wordpress.com/2013/12/21/trait-trees-basics/). Line meaning is loosely blue = healing/mobility, red = damage, yellow = tank/utility, varying by class.
- Since **Update 34** (Nov 2022) trait points come only from levelling: 98 at level 140, no longer from quests or deeds; all trees were reset. [S] [Update 34 notes](https://lotro-wiki.com/wiki/Update_34_-_Tuesday_November_15,_2022), [S] [Massively OP](https://massivelyop.com/2022/12/13/lotro-legendarium-why-the-new-class-trait-system-changes-are-a-bigger-deal-than-youd-think/)
- Specialization set bonuses, current per-trait costs and respec cost: **[U]**.

### Support and utility classes
| Class | Defining mechanics | Lines and role | Source |
|---|---|---|---|
| Captain | One chosen **Brother-in-Arms** ally gets extra healing, damage or protection by line; summoned **Heralds** or item **standards** (banners); **Marks** on foes that benefit allies; **battle states** (Battle-readied, Battle-hardened) to keep active; skills that react to a defeat (Rallying Cry) | Blue heal, red offensive support, yellow tank | [F] [class](https://lotrohq.com/classes/captain/), [F] [levelling](https://lotrohq.com/leveling/leveling-captain/), [F, old] [group play](https://www.tentonhammer.com/guides/lotro-captain-class-guide-group-play) |
| Minstrel | **Ballads** stack up to 3 buffs; **Anthems** need 1-3 of them without consuming; **Coda** needs 3 and consumes all; its form depends on stance (older sources: composition) | Main healer; damage line also exists | [S] [Ballad](https://lotro-wiki.com/wiki/Ballad), [S] [Coda](https://lotro-wiki.com/wiki/Coda) |
| Lore-master | Animal **pets** (one active), crowd control, many skills carry debuffs. Power sharing: **[U]** | Blue permanent pets and group buffs, red elemental damage, yellow control/debuff | [F] [levelling](https://lotrohq.com/leveling/leveling-loremaster/) |
| Burglar | **Tricks** (lasting debuffs, one per Burglar), **Riddle** (30 s mesmerise, most bosses immune), starts group **Fellowship Manoeuvres**, **stealth**, crit chains, dice-roll "gambles" | Red stealth burst, blue gambles, yellow debuff/control | [F, old] [skills](https://www.tentonhammer.com/guides/lotro-burglar-class-guide-skills-overview), [F] [levelling](https://lotrohq.com/leveling/leveling-burglar/), [F] [yellow](https://lotrohq.com/classes/burglar/yellow) |

### Captain in detail
Mostly from a Ten Ton Hammer guide last updated in 2016, so treat it as the design idea, not current LOTRO values. [F, old] [Captain skills](https://www.tentonhammer.com/guides/lotro-captain-class-guide-skills-overview)
- **Battle states:** an opener skill makes the Captain *Battle-readied*, which unlocks stronger attacks; those make him *Battle-hardened*. Current [S] descriptions give Battle-hardened 15 s with more outgoing healing and less incoming damage. [S] [Battle-readied](https://lotro-wiki.com/wiki/Battle-readied), [Battle-hardened](https://lotro-wiki.com/index.php/Battle-hardened)
- **Defeat responses:** a group of shouts unlocks when the Captain or his group kills an enemy; some attacks can also open them, so they work without a death. They include an area attack, a group heal over time, a group speed-of-attack buff and a revive.
- **Marks:** toggled debuffs: damage over time with threat, more damage taken, or returning part of allies' damage as healing.
- **Heralds and standards:** one summoned herald at a time (offence, health or resource flavour) or an archer; a planted standard instead gives stronger buffs and needs no control.
- **Shield-brother:** one chosen ally receives dedicated skills (health, damage, incoming healing).
- **Other:** group heals, a heal tied to a weapon strike, damage sharing, a short unkillable window, revives.
- The blue (healing) build is described as constant small group heals plus a mark that lets damage dealers heal themselves; it will not keep a main tank up alone. [F] [LotroHQ blue Captain](https://lotrohq.com/classes/captain/blue/)

### Minstrel in detail
- Combines Ballads, Anthems and Codas, with stances for damage (Dissonance), healing (Resonance) or both (Melody). The damage line is recommended for levelling (9/10), the healing line is rated 2/10 solo. [F] [LotroHQ Minstrel levelling](https://lotrohq.com/leveling/leveling-minstrel/)
- Up to three Ballad buffs; Anthems need but don't consume them; the Coda needs three and consumes them. [S] [Ballad](https://lotro-wiki.com/wiki/Ballad), [S] [Coda](https://lotro-wiki.com/wiki/Coda)

**Pattern:** LotroHQ rates the pure group lines poorly for solo levelling (yellow Lore-master 1/10, yellow Burglar 3/10) and says there is no reason to level a healing Minstrel, yet calls yellow Burglar's double disable required for some raid fights. These are one fan site's ratings.

---

## 4. Design lessons (sourced, then applied)
| Lesson | Source | Applied as |
|---|---|---|
| "10% or 5% damage" is not a choice; trade different strengths | [F] [Blizzard, Seeing the Forest for the Talent Trees](https://worldofwarcraft.blizzard.com/en-us/news/4055148/seeing-the-forest-for-the-talent-trees) | keystone pairs differ in playstyle |
| Obvious or mandatory picks make players copy builds; many small passives are filler and hard to judge | same | 9 nodes per branch, no +1% chains |
| Every added talent multiplies combinations to balance | same | no morphs or ranks in v1 |
| Encounters per level matter for pacing, not only the XP formula; a game that gets easier over time loses players | [S] [Raph Koster slides](https://www.raphkoster.com/wp-content/uploads/2026/07/Gritty-Systems-Design.pdf) | tune by kills per level |
| Linear curves control poorly at one end; polynomial or hybrid curves keep early levels quick | [S] [Game Developer community post](https://www.gamedeveloper.com/design/quantitative-design---how-to-define-xp-thresholds-) | quadratic curve |
| Major MMOs differ on respec friction: Wynncraft uses a shard cost, ESO made skill respecs free | sections 1 and 2 | free (there is no economy) |
| Support-only specs are weak solo | section 3 | every branch deals damage (our inference) |

---

# PROPOSAL FOR ARKENMMO (not facts)

## 5. Utility class

**Decided by the user: the Captain.** The user loves LOTRO's Captain and Minstrel and wants the Captain, with Minstrel flavour where it fits.

| Candidate | Outcome |
|---|---|
| **Captain** (battlefield commander: marks, standards, a herald, a sworn bond, war songs) | **chosen** |
| Artificer (gadgets, turrets, traps, flasks) | not chosen (was this note's first recommendation) |
| Skald (war-singer) | not a class; its song idea lives in the Captain's Warchanter branch |
| Trickster (Burglar-like) | not chosen |

### Captain identity
A commander who wins by **choosing targets, holding ground and timing orders**, with a company beside him. He must be as playable alone as in a group: every branch deals damage, every "allies" effect includes the Captain, and a herald stands in as company.

| | Warrior | Captain |
|---|---|---|
| Wins by | own strength: soaking hits, area damage, duelling | marks, standards, companion, timing and songs |
| Signature | taunt, shields, leaps, executes | defeat-response "Opening", Verses and Coda |
| Group value | holds aggro (Guardian) | buffs and heals the group; no taunt |

Names are our own. Don't copy LOTRO skill names.

**Opening (free class mechanic, our version of defeat responses and battle states):** the Captain gains an Opening for 10 s when an enemy he damaged or marked in the last 5 s is defeated, or from a skill that says so. Maximum one. Skills with an **(O)** bonus spend it automatically. Skills are never locked without it, so boss fights and quiet moments still work.

Branches:
| Class | Branch 1 | Branch 2 | Branch 3 |
|---|---|---|---|
| Warrior | Guardian (tank) | Berserker (area damage) | Duelist (single target, parry) |
| Archer | Marksman (range, charged shots) | Skirmisher (speed) | Hunter (elements, wolf) |
| Mage | Pyromancer (damage) | Frostweaver (control) | Lifebinder (healing) |
| Captain | Vanguard (marks, Openings; like LOTRO's red line) | Standard-Bearer (standard, herald, bond; protection) | Warchanter (Verses, anthem, coda; healing or war songs) |

The earlier Warrior "Warlord" group branch overlapped the Captain and is replaced by Duelist.

## 6. Skill tree structure

### Shape (identical for all 12 branches)
| Node | Tier | Type | Cost | Connected from | Level gate | Points already in branch |
|---|---|---|---|---|---|---|
| n1 | 1 | active (entry) | 1 | root | 1 | 0 |
| n2 | 2 | passive | 1 | n1 | 1 | - |
| n3 | 2 | passive | 1 | n1 | 1 | - |
| n4 | 3 | active | 2 | n2 or n5 | 8 | - |
| n5 | 3 | passive (bridge) | 1 | n4 or n6 | 8 | - |
| n6 | 3 | active | 2 | n3 or n5 | 8 | - |
| n7 | 4 | keystone A | 3 | n4 | 18 | 5 |
| n8 | 4 | keystone B | 3 | n6 | 18 | 5 |
| n9 | 5 | **ultimate** | 4 | n7 or n8 | 30 | 10 |

- A node is buyable when **any one** connected node is owned, plus its level and branch-point gates. Connections go downward, except the n5 sideways links.
- **n7 and n8 block each other.** This is the only hard lock.
- A branch costs at most 15 points. The cheapest ultimate costs 14 (10 spent plus 4), and two cost 28, more than the 26 available. So only **one ultimate** is possible, with no extra rule. A typical build is 14-15 in the main branch and 11-12 in a second (enough for its keystone).
- No cross-branch surcharge (unlike old LOTRO): the gates already reward depth.
- No ranks or morphs in v1. A later version could add ESO-style two-way morphs as a node sub-menu.
- Each class also has a free **core skill** at level 1, outside the branches. With the first point, a new player has two actives immediately.

### Chest GUI (9x6)
One branch at a time. Treat it as a virtual **9 wide x 9 tall** grid and show 5 rows. **View A** is virtual rows 0-4 (tiers 1-3), **view B** rows 4-8 (tiers 3-5). Tier 3 appears in both so the player keeps context. Raw slot = `(virtualRow - viewTop) * 9 + col`.

Legend: digits are nodes (1 = n1), `-` and `|` connectors, `.` empty.
```
col     0 1 2 3 4 5 6 7 8
row 0   . . - - 1 - - . .     view A starts
row 1   . . | . . . | . .
row 2   . . 2 . . . 3 . .
row 3   . . | . . . | . .
row 4   . . 4 - 5 - 6 . .     view B starts
row 5   . . | . . . | . .
row 6   . . 7 . . . 8 . .
row 7   . . | . . . | . .
row 8   . . - - 9 - - . .
```
Footer (inventory row 6): 45 back, 46/47/48 branch tabs, 49 info (level, free points, points per branch), 50 scroll up, 51 scroll down, 52 spell loadout, 53 reset.

- Node states: locked (names the missing gate), available, owned, blocked by keystone. Each must differ by icon or name and lore, not colour alone.
- A connector lights up when both its ends are owned.
- Click an available node, then click again to confirm.
- Loadout screen: assign any owned active (including core) to the 4 combo slots. A newly bought active fills the first empty slot automatically. The ultimate binds itself to F.

## 7. Skill list (first draft, all numbers are starting values)

### Shared rules
- **P (Power)** = `6 + 0.5 * (level - 1)` (6 at L1, 30.5 at L50). Damage and healing are percentages of P, in Minecraft health points (2 = 1 heart). Gear scaling is out of scope.
- **Basic attack** = 100% P with the class weapon (Warrior sword/axe, Archer bow, Mage wand item, Captain commander's weapon, visually distinct from the Warrior's), replacing vanilla damage for class weapons.
- **Max health** = `20 + 0.4 * (level - 1)`.
- **Mana:** 100 for every class, +4/s (+8/s after 5 s out of combat). Recasting the same spell within 4 s adds +25% of base cost per repeat, up to +100%.
- **Ultimate charge:** 0-100. +4 per damaging hit or heal you land, +2 per hit taken, each at most once per 0.5 s. Damage from the ultimate gives none. Decays 5/s after 15 s out of combat.
- Cost is written `mana / cooldown`. "Ult" costs a full meter. P = passive, A = active, U = ultimate. m = blocks.
- "Slow 30%" = movement attribute modifier. "Stun" = mobs stop acting; players and bosses get Slow 60% instead.
- Allies = party members (until parties exist: nearby players, no PvP assumed).
- Marks below feasibility notes: `*` = read section 7.5 before building.

### 7.1 Warrior. Core: **Cleave** (A, 20 / 4 s): 130% P to all enemies in a 3.5 m, 120-degree cone.

**Guardian**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Shield Bash | 110% P to a target in 3.5 m, stun 1 s | 20 / 8 s |
| n2 | 2 | P | Iron Hide | take 8% less damage | - |
| n3 | 2 | P | Stalwart | +4 max health, 20% knockback resistance | - |
| n4 | 3 | A | Challenging Shout* | mobs within 8 m target you for 5 s; you take 20% less damage meanwhile | 25 / 14 s |
| n5 | 3 | P | Second Wind | falling below 30% health heals 20% of max; once per 60 s | - |
| n6 | 3 | A | Bulwark* | shield absorbing 250% P for 6 s | 30 / 18 s |
| n7 | 4 | P | Keystone: Thornwall | reflect 25% of melee damage taken (reflected damage cannot reflect) | - |
| n8 | 4 | P | Keystone: Protector | allies within 6 m take 12% less damage; you take 25% of the prevented amount | - |
| n9 | 5 | U | Unbreakable | 8 s: take 60% less damage and cannot drop below 1 health | Ult |

**Berserker**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Leaping Strike* | leap up to 8 m; landing deals 120% P in 3 m | 25 / 8 s |
| n2 | 2 | P | Bloodthirst | basic hits heal 4% of damage dealt | - |
| n3 | 2 | P | Fury | each hit: +4% attack speed for 4 s, 5 stacks | - |
| n4 | 3 | A | Whirlwind | 3 pulses over 1.5 s, 60% P each, 4 m | 35 / 10 s |
| n5 | 3 | P | Relentless | each kill restores 10 mana | - |
| n6 | 3 | A | Execute | 180% P single target; 300% below 30% health | 30 / 9 s |
| n7 | 4 | P | Keystone: Reckless | deal 20% more and take 12% more damage | - |
| n8 | 4 | P | Keystone: Blood Price | when mana is short, pay the rest in health (1 health per 4 mana, not below 1) | - |
| n9 | 5 | U | Rampage | 10 s: +30% damage, +20% move speed, kills add 1 s (max +5 s) | Ult |

**Duelist**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Lunge* | dash up to 5 m toward the aimed enemy and strike for 130% P | 20 / 6 s |
| n2 | 2 | P | Footwork | +8% move speed, +8% attack speed | - |
| n3 | 2 | P | Focus | +12% damage while only one enemy is within 5 m | - |
| n4 | 3 | A | Riposte | 2 s stance: the first melee or arrow hit is reduced 80%; if melee, strike back for 200% P | 25 / 10 s |
| n5 | 3 | P | Opportunist | +15% damage when hitting an enemy from behind or while it is slowed | - |
| n6 | 3 | A | Hamstring | 150% P, Slow 40% for 4 s | 20 / 8 s |
| n7 | 4 | P | Keystone: Perfect Parry | a Riposte that takes a hit refunds its mana and resets Lunge | - |
| n8 | 4 | P | Keystone: Single Combat | +20% damage to the enemy you last hit with a skill, -15% to all others | - |
| n9 | 5 | U | Thousand Cuts | 3 s: 12 strikes of 60% P on the aimed enemy (moves to another within 5 m if it dies); you take 50% less damage meanwhile | Ult |

### 7.2 Archer. Core: **Vault*** (A, 15 / 6 s): launch yourself backward about 7 m; the landing does no fall damage.

**Marksman**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Power Shot | fast arrow, 200% P | 25 / 6 s |
| n2 | 2 | P | Eagle Eye | +12% arrow damage beyond 12 m | - |
| n3 | 2 | P | Steady Aim | after 1.5 s without moving, +10% damage | - |
| n4 | 3 | A | Piercing Shot | arrow passes through up to 5 enemies, 160% P | 30 / 9 s |
| n5 | 3 | P | Weak Spot | 15% chance for 150% damage | - |
| n6 | 3 | A | Hunter's Mark* | target glows 10 s and takes 15% more damage from you | 20 / 12 s |
| n7 | 4 | P | Keystone: Sniper | +25% damage beyond 18 m, -10% within 8 m | - |
| n8 | 4 | P | Keystone: Spotter | Hunter's Mark benefits all allies and refunds 15 mana if the target dies marked | - |
| n9 | 5 | U | Deadeye | 1.5 s aim (taking damage does not cancel), then a 60 m beam through enemies, 600% P | Ult |

**Skirmisher**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Volley | 5 arrows in a spread, 60% P each (max 2 hit one target) | 25 / 6 s |
| n2 | 2 | P | Fleet Foot | +10% move speed | - |
| n3 | 2 | P | Momentum | arrow hits give +3% damage for 4 s, 5 stacks | - |
| n4 | 3 | A | Rapid Fire | 10 arrows over 2 s, 35% P each | 35 / 12 s |
| n5 | 3 | P | Light Step | take 50% less fall damage; 8% chance to dodge a hit | - |
| n6 | 3 | A | Tumble* | dash 5 m in your held movement direction; next arrow within 3 s deals +50% | 15 / 7 s |
| n7 | 4 | P | Keystone: Ricochet | arrow hits bounce to 1 enemy within 5 m for 40% (no further bounce) | - |
| n8 | 4 | P | Keystone: Acrobat | Vault and Tumble have 2 charges | - |
| n9 | 5 | U | Arrow Storm* | 5 s channel: 8 arrows per second where you aim, 30% P each; may walk | Ult |

**Hunter**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Flame Arrow | 120% P, burns for 20% P per second, 4 s | 20 / 6 s |
| n2 | 2 | P | Tracker | hit enemies below 40% health glow for 5 s | - |
| n3 | 2 | P | Survivalist | regain 1% max health per second out of combat | - |
| n4 | 3 | A | Wolf Companion* | summon a wolf for 30 s: 50% P bites, health 40% of yours | 40 / 45 s |
| n5 | 3 | P | Barbed Heads | 20% chance: bleed 15% P per second, 3 s | - |
| n6 | 3 | A | Frost Arrow | 110% P, Slow 40% in 3 m for 4 s | 25 / 10 s |
| n7 | 4 | P | Keystone: Packleader | second wolf, each at 70% damage; wolves share your damage bonuses | - |
| n8 | 4 | P | Keystone: Elementalist | Flame and Frost Arrow cooldowns -30%; +20% damage to enemies burning or slowed by you | - |
| n9 | 5 | U | Wild Hunt* | 12 s: 4 spectral (glowing) wolves, 40% P bites; you gain +20% move speed | Ult |

### 7.3 Mage. Core: **Blink*** (A, 25 / 5 s): teleport up to 10 m where you look, stopping before walls.

**Pyromancer**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Fireball* | projectile, 160% P in 2.5 m | 25 / 3 s |
| n2 | 2 | P | Kindling | fire spells burn for 12% P per second, 3 s | - |
| n3 | 2 | P | Inner Heat | +8% damage while above 70% mana | - |
| n4 | 3 | A | Flame Wave | 8 m cone, 150% P, knockback | 30 / 8 s |
| n5 | 3 | P | Ash Siphon | a burning enemy dying restores 8 mana | - |
| n6 | 3 | A | Meteor* | after 1.2 s, 280% P in 4 m at the aimed point (24 m) | 50 / 14 s |
| n7 | 4 | P | Keystone: Wildfire | burn spreads to 2 enemies within 4 m when its victim dies | - |
| n8 | 4 | P | Keystone: Combustion | every 4th fire spell hit consumes the burn for +80% damage | - |
| n9 | 5 | U | Cataclysm* | 6 meteors over 4 s in an 8 m area, 180% P each | Ult |

**Frostweaver**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Ice Lance | 140% P bolt, 20 m, Slow 30% for 3 s | 20 / 3 s |
| n2 | 2 | P | Chill Touch | your slows last 1 s longer | - |
| n3 | 2 | P | Frost Armor | melee attackers get Slow 25% for 2 s; take 5% less damage | - |
| n4 | 3 | A | Frost Nova | 100% P in 5 m, root (Slow 100%) 2 s; players and bosses Slow 60% | 30 / 14 s |
| n5 | 3 | P | Shatter | +15% damage to slowed or rooted enemies | - |
| n6 | 3 | A | Blizzard | 6 s zone (24 m range, 5 m radius): 40% P per second, Slow 30% | 40 / 16 s |
| n7 | 4 | P | Keystone: Permafrost | 3 slows from you on one enemy within 8 s root it 1.5 s; once per 15 s per enemy | - |
| n8 | 4 | P | Keystone: Glacier | Frost Nova also gives a shield of 150% P for 5 s | - |
| n9 | 5 | U | Absolute Zero* | 10 m: 250% P, stun 4 s (players and bosses Slow 60%) | Ult |

**Lifebinder**
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Mending Light | heal 120% P to the aimed ally (20 m), or yourself if none | 30 / 3 s |
| n2 | 2 | P | Gentle Soul | +12% healing done | - |
| n3 | 2 | P | Radiance | your heals restore 25% P over 4 s extra (refreshes, no stacking) | - |
| n4 | 3 | A | Sanctuary | 8 s circle (4 m): allies heal 25% P per second | 40 / 18 s |
| n5 | 3 | P | Smite | spell damage dealt heals the most hurt ally within 10 m for 25% of it | - |
| n6 | 3 | A | Sunburst | 6 m around you: 120% P damage to enemies, 70% P heal to allies | 35 / 9 s |
| n7 | 4 | P | Keystone: Guardian Spirit | overhealing becomes a shield, up to 100% P, 6 s | - |
| n8 | 4 | P | Keystone: Zealot | Sunburst +50% damage; Mending Light healing -15% | - |
| n9 | 5 | U | Divine Grace | allies within 15 m heal to full, lose harmful effects and take 30% less damage for 5 s | Ult |

### 7.4 Captain. Core: **Rallying Strike** (A, 25 / 6 s): strike for 110% P and heal yourself and allies within 8 m for 30% P. **(O)** the heal is doubled.

The **Opening** mechanic (section 5) is free. "Allies" always includes the Captain, and effects that name allies also reach his herald. A Captain has at most one **Mark**, one **standard**, one **herald** and one **bond** at a time; a new one replaces the old. All end on quit, death or world change.

**Vanguard** (marks and Openings)
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Quarry Mark* | 80% P at up to 20 m; Mark for 12 s: it takes 12% more damage from you and allies | 20 / 8 s |
| n2 | 2 | P | Hardened Resolve | spending an Opening: for 8 s take 10% less damage and heal 15% more | - |
| n3 | 2 | P | Lead from the Front | +8% damage, and another +8% against your marked enemy | - |
| n4 | 3 | A | Press the Attack | 2 strikes of 90% P on up to 2 enemies within 3.5 m; hitting your marked enemy grants an Opening (once per 10 s) | 25 / 7 s |
| n5 | 3 | P | Gallant Example | spending an Opening restores 15 mana | - |
| n6 | 3 | A | Scattering Shout | 100% P to enemies within 6 m. **(O)** 200% P and stun 1.5 s | 30 / 12 s |
| n7 | 4 | P | Keystone: Searing Mark | your marked enemy takes 20% P per second; you heal for 25% of that | - |
| n8 | 4 | P | Keystone: Mark of Renewal | allies heal for 8% of the damage they deal to your marked enemy | - |
| n9 | 5 | U | Final Verdict* | aimed enemy: 300% P, and for 10 s it takes 30% more damage from you and allies; if it dies in that time, allies within 15 m heal 30% of max health and you gain an Opening | Ult |

**Standard-Bearer** (ground and company)
| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | Plant Standard* | planting hits enemies within 3 m for 100% P; for 15 s, allies within 7 m deal 10% more damage | 30 / 20 s |
| n2 | 2 | P | Tall Colours | standard radius +2 m, duration +5 s | - |
| n3 | 2 | P | Close Ranks | take 10% less damage within your standard or within 6 m of your herald | - |
| n4 | 3 | A | Call Herald* | a herald fights beside you for 45 s: 45% P melee every 1.5 s, health 60% of yours | 40 / 45 s |
| n5 | 3 | P | Steadfast Company | herald has 40% more health; your standard heals allies 8% P per second | - |
| n6 | 3 | A | Sworn Bond | bond the aimed ally (20 m), else your herald, else yourself, for 30 s: a 150% P shield (6 s) and +12% damage; if bonded to another, you get +6% | 25 / 20 s |
| n7 | 4 | P | Keystone: Champion Herald | herald deals 50% more damage and stays until defeated; its cooldown starts then | - |
| n8 | 4 | P | Keystone: Oathkeeper | while bonded, you and your bonded take 10% less damage within 20 m, and your heals on yourself also heal them for 50% | - |
| n9 | 5 | U | Banner Unbroken* | great standard for 10 s, 10 m: allies deal 20% more and take 25% less damage; the first lethal hit on each leaves them at 20% health | Ult |

**Warchanter** (Minstrel flavour: build Verses, sing, finish)
**Verses:** at most 3, lasting 15 s, refreshed whenever one is gained. War Ballad is exempt from the repeat-cast penalty.

| Node | Tier | Type | Skill | Effect | Cost |
|---|---|---|---|---|---|
| n1 | 1 | A | War Ballad | 110% P to the aimed enemy (16 m); gain 1 Verse | 12 / 3 s |
| n2 | 2 | P | Stirring Melody | per Verse held: +4% damage and 2% less damage taken | - |
| n3 | 2 | P | Long Refrain | Verses last 10 s longer | - |
| n4 | 3 | A | Anthem of Courage | needs 1 Verse, consumes none: allies within 12 m heal 40% P per Verse over 6 s | 30 / 12 s |
| n5 | 3 | P | Clear Voice | heal 10% more; Anthem also gives +15% move speed for 6 s | - |
| n6 | 3 | A | Coda | needs 1 Verse, consumes all: per Verse, 90% P to enemies within 8 m and 30% P healing to allies there | 25 / 6 s |
| n7 | 4 | P | Keystone: Song of Mending | Anthem and Coda heal 40% more; Coda deals 30% less damage | - |
| n8 | 4 | P | Keystone: Song of Battle | Coda deals 35% more damage and heals 30% less | - |
| n9 | 5 | U | Song of the Dawn | 10 s, 12 m: allies heal 25% P per second, deal 15% more damage and lose harmful effects every 2 s; you hold 3 Verses and Coda consumes none | Ult |

Balance notes: Warchanter wants Ballad, Anthem and Coda on 3 of the 4 slots, which is deliberate but should be playtested (alternating Ballad with others must feel good by combo). "Damage taken" debuffs (Quarry Mark, Final Verdict) don't stack across Captains; the strongest applies. Damage and healing buffs of the same name don't stack either.

Solo check: Vanguard gets Openings from kills and from Press the Attack on bosses; Standard-Bearer's buffs apply to himself and his herald, and Sworn Bond falls back to herald or self; Warchanter has ranged and area damage plus self-healing.

### 7.5 Feasibility (everything marked `*`, plus shared mechanics)
Method signatures checked in the 26.3 Javadocs: `Input` (`isForward/Backward/Left/Right/Jump/Sneak/Sprint`), `PlayerInputEvent#getInput`, `Player#getCurrentInput`; `World#rayTrace`, `rayTraceEntities`, `getNearbyLivingEntities`, `getNearbyEntities`, `spawnArrow`; `LivingEntity#getTargetEntity`, `rayTraceEntities`, `knockback`, `setNoDamageTicks`, `addPotionEffect`, and `heal`, `setAbsorptionAmount`, `damage(double, DamageSource)`; `Entity#setVelocity`, `setGlowing`, `teleport`, `teleportAsync`, `setVisibleByDefault`, `setPersistent`, `setInvisible`; `Player#showEntity`; `Mob#setTarget`, `setAware`, `getPathfinder`; `EntityTargetLivingEntityEvent` (cancellable, `setTarget`); `AttributeInstance#addTransientModifier`, `removeModifier(Key)`; `Attribute.MOVEMENT_SPEED, ATTACK_SPEED, MAX_HEALTH, KNOCKBACK_RESISTANCE, JUMP_STRENGTH, MAX_ABSORPTION, SAFE_FALL_DISTANCE, FALL_DAMAGE_MULTIPLIER`; `EntityDamageEvent#setDamage(double)`, `getDamageSource` (`DamageModifier` is deprecated); `MobGoals#removeAllGoals`, `Pathfinder#moveTo`. A signature existing does **not** prove the in-game behaviour.

| Mechanic | Approach | Doubt |
|---|---|---|
| Stun / root | mobs `setAware(false)` and restore; root = transient speed modifier, plus jump strength 0 for players | Unaware mobs still move when pushed. Boss AI (Ender Dragon, Wither, Warden) is **[U]**: treat as immune. Restore on unload, death and disable, or mobs stay frozen |
| Taunt | `setTarget`, then cancel/redirect target events | Mobs only. Brain-driven mobs (piglins, Warden, breeze etc.) may ignore it **[U]** |
| Shields (Bulwark, Glacier, Guardian Spirit) | plugin-tracked pool subtracted in the damage event | Preferred over vanilla absorption, which involves `MAX_ABSORPTION` (clamping behaviour **[U]**) |
| Lethal-damage prevention | lower the damage in the damage event | Void and `/kill` should be exempt. No downed/revive state is proposed |
| Leap, Vault, Tumble, Lunge | `setVelocity`; cancel the next fall damage with a flag | Distances need tuning (client ping). Tumble direction from `getCurrentInput()`. Anti-cheat plugins may flag it |
| Blink | block ray trace, check 2-block headroom, `teleport` | none significant |
| Hunter's Mark, Tracker, Captain marks | `setGlowing` | Glow is **visible to everyone**; per-player glow was not verified in the API **[U]**. Colour needs scoreboard teams |
| Damage-taken debuffs | plugin map read in the damage event | none |
| Standards | display entities plus one shared ticking task; non-persistent | Visuals only: distance checks are plugin code |
| Herald | a non-persistent goal-based `Mob`: remove its vanilla goals (`com.destroystokyo.paper.entity.ai.MobGoals#removeAllGoals`), move it with `getPathfinder().moveTo(...)`, apply attacks as plugin damage with the Captain as cause | Signatures checked ([MobGoals](https://jd.papermc.io/paper/26.3/com/destroystokyo/paper/entity/ai/MobGoals.html), [Pathfinder](https://jd.papermc.io/paper/26.3/com/destroystokyo/paper/entity/Pathfinder.html)); behaviour is **[U]**: which mob type works cleanly, whether brain-based AI ignores goal removal (so avoid such mobs), follow quality, and teleport-to-owner. Must not burn, drop items, give XP, pick up items or survive quit. Prototype before building n4, n7 |
| Projectiles (arrows, fireball, meteor) | vanilla or display projectiles tagged in PDC; do all damage and AoE yourself | **Never** `createExplosion`; suppress vanilla fire, block damage, potion effects and arrow pickup. Meteor is visual only |
| Companion wolves | spawn a `Wolf`, set owner, non-persistent, plugin-set stats | Vanilla AI controls its target selection and teleporting; tuning is **[U]**. Must not give XP or item drops, or survive quit |
| Opening | on entity death, check recent damage or mark entries per Captain | Deaths from other causes also count if the Captain tagged the enemy; passive mobs must not grant it (farming) |
| Ally detection for Sworn Bond | aimed-entity ray trace filtered to allies | depends on the party decision |
| Channels, delayed casts | scheduled task, cancel on quit, death, world change | none |
| Lose harmful effects | `removePotionEffect` per harmful type, and clear plugin debuffs | none |
| Double jump, flight | **not used** | would need flight toggling, which conflicts with anti-cheat |

Particles and sounds go through `Effects.play(id)` and `sounds.yml`.

## 8. Casting input (vanilla client)
| Option | Pros | Cons |
|---|---|---|
| **3-click combos** | 4 spells without hotbar space; feels like Wynncraft; works with any held weapon | Learning curve; clicks also attack and interact; latency; spell count capped |
| Hotbar spell items | Obvious; item cooldown overlay (`setCooldown`) | Uses 4+ slots; swaps away from the weapon; items need protection against drop, move, death |
| Number keys as casts (cancel `PlayerItemHeldEvent`, which is cancellable) | Fast, one key | Blocks normal hotbar use; scroll wheel also fires it; needs a combat-mode toggle |
| Swap-hands, F (`PlayerSwapHandItemsEvent`, cancellable) | One rebindable key, clean event | Only one action; blocks off-hand swapping while holding a class weapon |
| Sneak + click or F (`PlayerToggleSneakEvent`, current input) | Simple, adds variants | Only a few combos; interferes with sneaking (edges, shields, blocks) |
| Drop key, Q (`PlayerDropItemEvent`) | Extra key | Risk of item loss; fires in other contexts; players dislike it |
| Movement input sequences (`PlayerInputEvent`) | Keys are readable server-side | Collides with normal movement; accidental casts |
| Client keybind mods | best feel | excluded: vanilla client |

**Recommendation**
- While holding the class weapon, combos are 3 clicks with at most 1 s between clicks. Warrior, Mage and Captain start with **R**. Archer starts with **L** (mirrored, as in Wynncraft), so a normal bow shot never starts a combo.
- Slots: 1 = R-L-R, 2 = R-R-R, 3 = R-L-L, 4 = R-R-L. Archer swaps L and R.
- **F** casts the ultimate when the meter is full. Sneak + F casts nothing and lets the normal swap happen.
- Action bar shows the partial combo (`R - L - ?`), mana and ultimate charge, plus failures ("not enough mana", "cooldown 3 s"). A failed cast costs nothing.
- Later option, not v1: a per-player "quick cast" mode on number keys.

**Input pitfalls**
- `PlayerInteractEvent` can fire once per hand; filter on the main hand. It can arrive "cancelled" for air clicks, so don't use `ignoreCancelled = true` for it ([Javadoc](https://jd.papermc.io/paper/26.3/org/bukkit/event/player/PlayerInteractEvent.html)).
- The client has no "left click air" action: Bukkit infers it from the arm swing ([SPIGOT-1955](https://hub.spigotmc.org/jira/si/jira.issueviews:issue-html/SPIGOT-1955/SPIGOT-1955.html), old). Other actions can therefore look like a left click. Whether drop (Q) or a right-click use does so on 26.3 is **[U]**. De-duplicate per tick across interact, attack (`PrePlayerAttackEntityEvent`) and swing (`PlayerArmSwingEvent`; its parent `PlayerAnimationEvent` is deprecated, so listen to the subclass).
- Right-clicking air with an **empty hand** sends no event ([SPIGOT-410](https://hub.spigotmc.org/jira/browse/SPIGOT-410), old). Combos require a held weapon, so this is fine.
- Right-clicks on entities use a different event; containers, doors and villagers must keep working (don't count those clicks).
- **Prototype first:** bow drawing during Archer combos (R draws the bow; an arrow released mid-combo must be handled in the shoot event), the click-repeat rate when right is held, shields or other usable weapon items, and trident-like items. All **[U]**. If the bow fights the combos, the fallback is a non-bow item that fires plugin arrows.
- The weapon's attack cooldown must not stop a click from counting towards a combo.

## 9. Levelling, XP, respec, rebirth

### Curve
Cap **50**. With `n = level - 1`: **XP to next level = `100 + 50n + 5n^2`**.

| Level | XP to next | Total XP to reach | Tree points | Est. time* | Moment |
|---|---|---|---|---|---|
| 1 | 100 | 0 | 1 | 0 | core skill plus first branch active |
| 2 | 155 | 100 | 2 | ~1 min | first passive |
| 5 | 380 | 770 | 5 | ~9 min | room for a second branch's entry active |
| 8 | 695 | 2,205 | 8 | ~25 min | tier 3; one branch can be filled to tier 3 |
| 10 | 955 | 3,720 | 10 | ~41 min | full 4-slot loadout is comfortable |
| 18 | 2,395 | 15,980 | 13 | ~3 h | keystone |
| 20 | 2,855 | 20,995 | 14 | ~4 h | |
| 30 | 5,755 | 61,770 | 18 | ~11.5 h | **ultimate** |
| 40 | 9,655 | 136,045 | 22 | ~25 h | |
| 49 | 14,020 | 239,800 | 25 | ~44 h | |
| 50 | cap | 253,820 | 26 | ~47 h | rebirth available |

\*Assumes a flat **90 XP per minute** (about 6 kills of 15 XP). Real rates will rise with better skills and harder mobs and vary a lot by world. These are targets to tune, not predictions.

### Points and per-level rewards
- 1 tree point at **every level 1-10** (10), then at levels **12, 15, 17, 20, 22, 25, 27, 30, 32, 35, 37, 40, 42, 45, 47, 50** (16). Total 26.
- Every level also gives health and Power growth and a full heal and mana, so levels without a point still matter.
- **No manual attribute points in v1.** Wynncraft has them, but they add a second allocation system and trap choices before gear exists.

### XP sources
| Source | Starting value | Notes |
|---|---|---|
| Common hostiles (zombie, skeleton, spider...) | 10-15 | per-type table in config |
| Dangerous hostiles (creeper, enderman, blaze, witch, raiders) | 20-30 | |
| Elites (ravager, evoker, piglin brute, elder guardian) | 100-300 | |
| Bosses (Wither, Ender Dragon, Warden) | 1,500-3,000 | shared by contributors |
| Passive mobs | 0 | |
| Spawner, trial-spawner, egg, command and bred or built mobs | 0-25% | check the spawn reason; anti-farm |
| First-time discoveries (biome, structure) | 50-500 | optional, once per class run |
| Quests, dungeons | later | no such system exists yet |

- Credit every player who dealt at least 10% of the damage, or healed or shielded a contributor in the last 10 s. Without that, support builds fall behind.
- If parties are added: full XP split by a factor such as `(1 + 0.2 * (members - 1)) / members`, within 48 m.
- No mob-level penalty in v1 (vanilla mobs have no levels). Optional diminishing returns for many kills in one small area.
- Class XP is separate from vanilla XP. Don't take over the XP bar; it is needed for enchanting and anvils.
- Weak point: vanilla mobs have about 20 health, while P grows about five times. Without mob scaling or level zones, high levels become trivial. This needs a design decision.

### Class selection (user decisions)
**Decided:** a player picks a class **once**. Switching is not in scope. Selection is normally shown once, after a tutorial run by another plugin, so a command opens it and that plugin triggers it.

Proposed behaviour:
- Command **`/class open <player>`**, permission **`arkenmmo.class.open`** (default: op). The console has it, so the tutorial plugin can dispatch the command as the console with the player's name. This needs no compile-time dependency between the plugins.
- Ordinary players can't open selection themselves, so they can't skip the tutorial.
- Take a player argument with Brigadier `ArgumentTypes.player()`, resolve the `PlayerSelectorArgumentResolver` with the command source and take the first result ([Paper docs](https://docs.papermc.io/paper/dev/command-api/arguments/entity-player/)). It must work with a non-player sender.
- If the player already has a class: change nothing and tell the sender. Offline or unknown player: report failure to the sender.
- The selection GUI shows the four classes, then a **confirm screen** that says the choice is permanent.
- Closing the GUI chooses nothing. Running the command again reopens it. Recheck "has no class" at the moment of confirming, then save immediately.
- A player without a class gains no class XP and has no skills.
- On success: save, then give the core skill, the first tree point and the class weapon (once only; how a lost weapon is replaced needs a decision).
- The other plugin gets no result back from a dispatched command beyond whether it ran. If it must know that a class was chosen, add a small custom event or API later; confirm that need first.

**Keep switching easy to add later** (design for it, don't build it):
- Save a profile of `activeClass` plus a **map of progress per class id** (level, XP, rebirths, owned nodes, loadout), even though it holds one entry for now. Nothing about progress sits directly on the player.
- One responsibility per class: class definitions; the choose-once rule (the **only** place that sets `activeClass`); selection GUI; command (parses and delegates); profile storage; XP and levels; tree rules; tree GUI; loadout; input detection (combos only produce a slot number); casting (cost, cooldown, ultimate); mana and charge; one executor per skill behaviour; applying and removing a class's passive effects.
- That last part needs a clean "remove" from the start (it is also needed for respec and quit), so switching later means: remove, change `activeClass`, apply.

### Respec
- **Full respec: free**, out of combat (10 s without damage dealt or taken), 60 s cooldown. Refunds all points and clears the loadout.
- **Undo:** nodes bought since the menu was opened can be right-clicked to refund, in any order that leaves the tree connected and all gates met.
- No single refund of older nodes in v1 (it needs more dependency logic).
- Respec must not reset cooldowns; it sets ultimate charge to 0.
- Respec removes the herald, standard, mark, bond, wolves and other active effects.

### Rebirth (optional, per class)
- At level 50, confirmed twice. Resets that class to level 1 with an empty tree.
- Maximum **5**. Each rebirth `R` gives: +2% damage and healing, +1 max health, a title/prefix and cosmetic.
- **Rebirth 1 only: +1 permanent tree point** (27 total, still below the 28 needed for two ultimates).
- XP requirement: multiply by `1 + 0.25R`; XP gain gets `+10% * R`. So each run is somewhat longer (net about 1.14, 1.25, 1.35, 1.43, 1.50 times the first).
- Rebirth should add something new, not only a longer grind. Later candidates: a **mastery slot** (one slottable passive from a short list per rebirth, like ESO's slottable stars), or morph variants unlocked by rank. Not in v1.
- Level and rebirth gates apply to the current run.
- No economy: no costs or sellable rewards.

## 10. Decisions the brief needs from the user
Already decided: the utility class is the Captain; class choice is once only, opened by command.

1. Class choice is permanent: should there be an admin reset for mistakes later? (Not proposed now.) And if a classless player disconnects mid-selection, is rerunning the command by the tutorial plugin enough, or should the GUI reopen on join?
2. PvP: this draft assumes **none**. PvP needs separate numbers and rules.
3. Parties: build now, or treat nearby players as allies?
4. Mob scaling: custom mob levels, level zones, or vanilla only (and a flatter P curve)?
5. Cap 50, 5 rebirths and roughly 47 h per run: acceptable?
6. May skill damage replace vanilla weapon and enchantment damage for class weapons?
7. Scope: suggest shipping the framework plus tiers 1-3 (core plus n1-n6) for all four classes first, then keystones and ultimates. The full list is 112 skills (4 core plus 108 nodes).

## Version notes
- Game facts are as of 2026-11-25 sources; many pages are older. Wynncraft and ESO change often.
- API checks are against the **26.3** Javadocs (the live pages showed a newer 26.3 build than the pinned 205 on at least one page).
- `AttributeInstance#getDefaultValue` is deprecated since 26.1. Use `Key`-based modifier methods; the UUID ones are deprecated for removal. In `AbstractArrow`, knockback strength methods are deprecated and do nothing.
- `setPierceLevel`, `setPickupStatus`, owner/tame methods, display entity methods, `removePotionEffect`, entity spawn reason and the drop event were **not** re-read in this research; the coder should confirm them at compile time.

## Pack file layout
Not applicable. No resource pack content is covered here.

## Plugin side (suggested)
- Data-driven skills: id, class, branch, node, type, cost, cooldown and numbers in config; behaviour in code. The tree shape is one shared template (sections 6 and 7).
- Derive free points from level, rebirths and owned nodes rather than storing a counter. On load, if the saved tree is no longer valid (config changed), refund it.
- Player progress can live in the player PDC ([docs](https://docs.papermc.io/paper/dev/pdc/)); the offline view is read-only. A database suits leaderboards or offline edits.
- One shared tick task for mana, cooldown display and constructs, which stops when idle.
- Skill damage: use `damage(amount, DamageSource)` with the player as cause, guard against recursive on-hit procs (reflect, bounce, Smite), and handle no-damage ticks so multi-hit skills land.
- Use transient attribute modifiers with namespaced keys, applied and removed in one place (respec, quit, disable).
- Follow the single-responsibility split in section 9, and register `/class open` through the Brigadier lifecycle.

## Pitfalls
- Passives that trigger on damage can loop; mark plugin-caused damage.
- Heralds, wolves and standing zones can be used for AFK farming: no XP when the owner has not acted for 60 s.
- Healing, splash and AoE need an ally/enemy filter that spares pets, villagers, armor stands and other players' tamed animals.
- Respect protection plugins: skill damage and movement (leap, lunge, blink) should honour what a normal attack or pearl would be allowed to do.
- In the tree GUI, cancel every click and drag, including shift-clicks and number keys from the player inventory, and identify the GUI by its holder, not its title.

## Sources
Linked inline. Main ones:
- https://wynncraft.wiki.gg/wiki/Ability_Tree , /Warrior/Ability_Tree , /Archer/Ability_Tree , /Mage , /Classes , /Version_2.0 , /Combat_Level , /Skill_Points , /Identifications
- https://en.uesp.net/wiki/Online:Skills (search summary only)
- https://arzyelbuilds.com/champion-points-guide-elder-scrolls-online/ , https://arzyelbuilds.com/eso-update-49/
- https://eso-hub.com/en/news/eso-u49-makes-skill-and-attribute-respecs-completely-free
- https://lotrolibrary.wordpress.com/2013/12/21/trait-trees-basics/ , https://lotrohq.com/leveling/leveling-captain/ , /leveling-loremaster/ , /leveling-burglar/ , /leveling-minstrel/
- https://lotrohq.com/classes/captain/blue/ , https://www.tentonhammer.com/guides/lotro-captain-class-guide-skills-overview
- https://docs.papermc.io/paper/dev/command-api/arguments/entity-player/
- https://worldofwarcraft.blizzard.com/en-us/news/4055148/seeing-the-forest-for-the-talent-trees
- https://jd.papermc.io/paper/26.3/

## Hand-off
Order: the user answers the open questions in section 10, the orchestrator writes the brief, then plugin-coder and designers work in parallel. This work calls for no tests (user instruction).

**Proposed contract IDs** (for the orchestrator to fix in the brief):
- Classes: `warrior`, `archer`, `mage`, `captain`.
- Branches: `warrior.guardian|berserker|duelist`, `archer.marksman|skirmisher|hunter`, `mage.pyromancer|frostweaver|lifebinder`, `captain.vanguard|standard_bearer|warchanter`.
- Command `/class open <player>`; permission `arkenmmo.class.open`.
- Skills: `<class>.<skill_name>` in snake case, apostrophes dropped (`warrior.cleave`, `archer.hunters_mark`, `captain.plant_standard`). The node position (n1-n9) is data, not part of the ID, so skills can move. Keystones: `warrior.thornwall`.
- Sound events (shared first set): `class_select`, `class_level_up`, `class_rebirth`, `skill_unlock`, `skill_unlock_denied`, `skill_tree_reset`, `combo_click_left`, `combo_click_right`, `cast_fail`, `ultimate_ready`, `captain_opening_ready`, `captain_verse_gain`; per active or ultimate `skill_<class>_<name>`.
- Effect IDs: `class_select`, `class_level_up`, `class_rebirth`, `ultimate_ready`, `captain_opening_ready`; per active or ultimate `skill_<class>_<name>`, with suffixes `_impact` or `_zone` where needed (e.g. `skill_mage_meteor_impact`).
- Item model keys and GUI art: left to the GUI art research note. This design needs icons for 112 skills (placeholders are fine at first), node states, lit and unlit connectors, footer buttons, 4 class weapons, 4 class icons plus confirm/cancel for the selection GUI, the Captain's standard and great standard, and a way to tell the herald apart (its look depends on the mob type chosen in the prototype).

| Who | Next |
|---|---|
| **model-designer** | Pipeline per the GUI art note. Assets as listed above, only after the brief fixes keys. Paths, sizes and formats are not covered here |
| **sound-designer** | The sound events above in `sounds.yml` with vanilla fallbacks; shared set first. Pack paths and formats are not covered here |
| **vfx-designer** | `effects.yml` presets for the IDs above. Telegraph delayed AoE (Meteor, Cataclysm) and zone radii (standards, songs) to match the numbers in section 7; respect performance limits for multi-hit and zone skills |
| **plugin-coder** | 1) one-time class selection with `/class open`, per-class profile storage, level and XP; 2) tree model and GUI (section 6); 3) input (section 8), prototyping the bow and left-click cases first; 4) mana, cooldowns, ultimate charge; 5) skills by tier, handling section 7.5 doubts; 6) respec, then rebirth. All balance numbers in config |
