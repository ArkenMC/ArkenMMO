---
name: mmo-design-sources
description: Game-design research (Wynncraft, ESO, LOTRO, lessons) - which URLs fetch, dead ends, and 26.3 API facts checked for class skills
metadata:
  type: reference
---

Findings live in `docs/research/mmo-classes-levelling.md` (written 2026-11-25). Don't re-research; read it.

## Fetch works (checked 2026-11-25)
- https://wynncraft.wiki.gg/wiki/Ability_Tree | AP 1@L1..50@L120, node costs 1-2, reset 3 shards | volatile
- https://wynncraft.wiki.gg/wiki/Warrior/Ability_Tree and /Archer/Ability_Tree | archetype gates, blocking pairs, L90 ultimates, Archer combos | volatile
- https://wynncraft.wiki.gg/wiki/Mage | spell combos and mana costs (old page) | volatile
- https://wynncraft.wiki.gg/wiki/Combat_Level | XP table, XP sources | volatile
- https://wynncraft.wiki.gg/wiki/Skill_Points , /Classes , /Version_2.0 , /Identifications | stats, classes, repeat-cast cost | volatile
- https://arzyelbuilds.com/champion-points-guide-elder-scrolls-online/ , /eso-update-49/ | CP system, free respec (U49, 2026-03) | volatile
- https://lotrohq.com/classes/<class>/ and /leveling/leveling-<class>/ | LOTRO lines and mechanics | volatile
- https://www.tentonhammer.com/guides/lotro-burglar-class-guide-skills-overview , lotro-captain-class-guide-group-play | old mechanics | volatile
- https://lotrolibrary.wordpress.com/2013/12/21/trait-trees-basics/ | 1/2 point costs (2013) | stable
- https://worldofwarcraft.blizzard.com/en-us/news/4055148/seeing-the-forest-for-the-talent-trees | talent design lessons | stable

- https://lotrohq.com/classes/captain/blue/ , /leveling/leveling-minstrel/ | Captain healing line, Minstrel lines and ratings | volatile
- https://docs.papermc.io/paper/dev/command-api/arguments/entity-player/ | ArgumentTypes.player(), PlayerSelectorArgumentResolver#resolve(source).getFirst() | stable
- jd 26.3 com/destroystokyo/paper/entity/ai/MobGoals (removeAllGoals, addGoal) and entity/Pathfinder (moveTo overloads) | stable

User decisions (2026-11-25, until in a brief): utility class = Captain (loves LOTRO Captain + Minstrel); class picked once, no switching yet but per-class data and single responsibility; selection opened by a command another (tutorial) plugin triggers; no tests.

## Dead ends
UESP (403), forums.elderscrollsonline.com (403), eso-hub.com (403), alcasthq.com (403), massivelyop article (403), lotro-wiki.com and fibrojedi subdomain (bot check), *.fandom.com (402), wynncraft.wiki.gg/wiki/Spells (404). WebSearch summaries of these still work.

## Paper 26.3 Javadocs (signature checks 2026-11-25, stable)
- org.bukkit.Input: isForward/Backward/Left/Right/Jump/Sneak/Sprint; PlayerInputEvent#getInput; Player#getCurrentInput
- Cancellable: PlayerSwapHandItemsEvent, PlayerItemHeldEvent, PlayerToggleSneakEvent, PrePlayerAttackEntityEvent, PlayerArmSwingEvent (extends deprecated PlayerAnimationEvent), EntityTargetLivingEntityEvent
- AttributeInstance: addTransientModifier, removeModifier(Key); getDefaultValue deprecated 26.1; Attribute has JUMP_STRENGTH, MAX_ABSORPTION, SAFE_FALL_DISTANCE, FALL_DAMAGE_MULTIPLIER
- Mannequin extends LivingEntity (setProfile, setImmovable); Mob#setTarget/setAware/getPathfinder
- EntityDamageEvent DamageModifier deprecated; setDamage(double), getDamageSource
- HumanEntity#setCooldown(ItemStack|Material|Key,int); ClickType includes SWAP_OFFHAND, DROP, NUMBER_KEY
- Large pages (Player, World, Entity, LivingEntity) are 150k-640k chars; WebFetch reads 100k per `offset`
