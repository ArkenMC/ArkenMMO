# Skills stage: user decisions (2026-11-26)

From a question round with the user. The base proposal is `docs/research/mmo-classes-levelling.md`; **these decisions win over it**. Its numbers are untested starting values.

## First release
- Framework plus core skill and tiers 1-3 for all classes; **Warrior is built and tested first**. Keystones and ultimates come later.
- The Warrior skills in the draft (7.1: Cleave and n1-n6 of Guardian, Berserker, Duelist) are accepted as starting designs. Shield Bash needs no shield.
- 3 branches per class, one shared 9-node layout, keystones exclude each other, one ultimate.
- Level cap 30 (18 tree points), raised to 50 with the later skills. Draft XP pace, adjustable in config.
- PvE only. No rebirths yet.

## Combat
- 4 spells on 3-click mouse combos with the class weapon; Archer's are mirrored.
- Later ultimate: meter full, hold sneak, 5 clicks R-L-R-L-R (mirrored for Archer).
- Level-based power replaces vanilla weapon and enchantment damage for class weapons, growing about fivefold by level 50, adjustable.
- 100 mana, +4/s, +8/s after 5 s out of combat; quick repeats cost more. New actives fill empty slots; loadout menu to rearrange. Action bar shows combo, mana and failures. Values configurable.

## Weapons
- A class gets its starter weapon automatically; restored on join or respawn if missing. Starters can't be dropped, traded or stored.
- Starters: Warrior one-handed sword, Archer bow, Mage staff, Captain longsword with a pennant.
- More weapons are defined in config (ID, class, name, appearance, base strength) and given by command by admins or other plugins. Bound to the player; only given to the right class. May be kept in own inventory or ender chest, not dropped or traded.
- Weapons **show DPS**: real damage per second from level, attack speed and base strength (starter 1.0; 1.2 is 20% stronger). Skills use the same strength.

## Integrations (all optional)
- MythicMobs: handles mob levels and strength; configurable XP per MythicMob and vanilla mob. Approved as optional compile-time dependency if needed; never bundled.
- Parties: ArkenCore through PlaceholderAPI. Without it, allies are only yourself and your companions. Approved as optional compile-time dependency (`provided`, never bundled). The party placeholder was tested in game by the user.
- A MythicMob without its own XP setting gives the XP of its underlying vanilla mob.

## XP and reset
- Party XP: members within 48 blocks who recently fought, healed or protected a fighter split it with a small bonus (two get 60% each; one alone gets 100%). Without a party, 10% of damage earns full credit. Spawner mobs give none.
- Reset is free after 10 s out of combat, 60 s cooldown, with undo for purchases made while the tree is open. The reset button sits at the **bottom centre of the GUI (slot 49) on every tree page**, with its own reset-button texture. Later, resetting will cost tokens.

## GUI art
- One layout and frame, a different subdued background per class. Dark, ancient, mysterious: weathered stone, faint carvings. Locked = dull rune, available = faint edge, purchased = soft still class-colour glow with lit connectors: noticeable but not loud.
- One icon per skill (19 for Warrior): recognisable symbols carved like ancient runes. **Research MMO icon readability and carving references properly**, make original Warrior previews and get approval.
- Future keystone and ultimate places show as sealed, unreadable stones.

## For later (rebirths; don't build yet)
- The user wants rebirths. After level 50, the first rebirth permanently evolves the class into an advanced form (example: Warrior to Champion, who dual wields; Warrior wields one). Rebirths 2-5 strengthen it; a choice of forms may come later. First release only keeps data that allows this.
- Fragments: needed for the evolution, gained late. Proposal to revisit: drops from chosen MythicMobs bosses from class level 40, one per qualifying player, saved as class progress and not as items. Amount, bosses and chances are open.
- Only the first rebirth uses up fragments; 2-5 need only the level cap.
