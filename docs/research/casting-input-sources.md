# Casting input: what sources say (for the prototype)

## Target version
**Paper 26.3**. Checked 2026-11-26. Deliberately short: sources only, while plugin-coder prototypes (P1). The prototype's observations **win** over this note. Builds on `mmo-classes-levelling.md` section 8.

## Summary
1. Left click in air is inferred from the arm swing, and **dropping an item also swings**: delay or filter it.
2. `PlayerInteractEvent` fires per hand, and air clicks arrive pre-cancelled.
3. Held right click repeating every 4 ticks is only weakly sourced.
4. A bow draws only with an arrow (or in creative); release fires.
5. Whether left clicks arrive **while drawing** is the key Archer question.

## Version notes
Most behaviour reports below are old or name no version. Nothing was verified in a 26.3 client. I did not check the 26.1-26.3 changelogs for swing or attack packet changes.

## Findings
| Topic | Finding | Strength |
|---|---|---|
| Interact event | Potentially fired once per hand; air interactions start cancelled; check `useItemInHand()` / `useInteractedBlock()`, `isCancelled()` is deprecated; `getHand()` may be null for physical | [26.3 Javadoc](https://jd.papermc.io/paper/26.3/org/bukkit/event/player/PlayerInteractEvent.html) |
| Swing | `io.papermc.paper.event.player.PlayerArmSwingEvent`: cancellable, `getHand()` | [26.3 Javadoc](https://jd.papermc.io/paper/26.3/io/papermc/paper/event/player/PlayerArmSwingEvent.html) |
| False left click | The client sends a swing when it throws an item, **before** the drop or container click packet, so a `LEFT_CLICK_AIR` appears first. The report also covers throwing from an inventory. Its fix: handle the click one tick later and discard it if `PlayerDropItemEvent` fired meanwhile | [MagicBottle #34](https://github.com/Vontus/MagicBottle/issues/34), third party, no version given. [SPIGOT-5632](https://hub.spigotmc.org/jira/si/jira.issueviews:issue-html/SPIGOT-5632/SPIGOT-5632.html), old (search summary only; page 403) |
| Right-click repeat | A client use delay of 4 ticks while held | **Weak:** mod descriptions in a search summary. No official source |
| Bow | Holding use draws, release shoots, switching hotbar slot cancels; needs an arrow in the inventory unless creative; full charge about 1 s | [Wiki](https://minecraft.wiki/w/Bow) |
| Release | `io.papermc.paper.event.player.PlayerStopUsingItemEvent`: `getItem()`, `getTicksHeldFor()`; no cancel method listed | [26.3 Javadoc](https://jd.papermc.io/paper/26.3/io/papermc/paper/event/player/PlayerStopUsingItemEvent.html) |
| Shot | `EntityShootBowEvent`: cancellable, `getForce()` up to 1.0, `getConsumable()`; `setConsumeItem` is deprecated and not functional; its docs suggest `Player#updateInventory()` when the client may disagree about arrows | [26.3 Javadoc](https://jd.papermc.io/paper/26.3/org/bukkit/event/entity/EntityShootBowEvent.html) |

## Prototype checklist (all unverified)
- One physical left click on air, block and entity: which of interact, `PrePlayerAttackEntityEvent` and swing fire, in what order, how many times.
- Holding left on a block (repeated swings; one report mentions per-tick swings in creative, seen only in a search summary).
- Q, Ctrl+Q, throwing from the inventory: no combo click may be counted.
- Right click on blocks, doors, containers and villagers: does a swing follow and get counted as L?
- Holding right with each class weapon: repeat rate, and whether repeats should count. A time debounce cannot tell a 4-tick repeat from very fast clicking.
- **Archer:** my recollection, with **no source**, is that the vanilla client ignores attack while it is using an item. If so, an L pressed while R is still held never reaches the server, and mirrored combos need R released first. Test L-R-L at normal speed.
- Archer: which events fire for a very short R tap (a weak arrow?), cancelling the shot mid-combo, arrow count staying in sync, and no arrows in the inventory (does the R still produce an event?).
- Latency: clicks bunched into the same tick.

## Pack file layout
Not applicable.

## Plugin side
One input class that turns all sources into at most one L or R per physical click; de-duplicate per tick; ignore the off hand. The rest is the prototype's call.

## Pitfalls
- `ignoreCancelled = true` hides air clicks.
- Reacting immediately to `LEFT_CLICK_AIR` counts drops.
- If the bow fights the combos, the draft's fallback is a non-bow item firing plugin arrows. The user decided the Archer starter is a bow, so that fallback needs their approval.

## Sources
Linked in the table.

## Hand-off
**Contract IDs:** none.

| Who | Next |
|---|---|
| **plugin-coder** | Run the checklist in P1 and record results; the user tries it in game |
| **model-designer, sound-designer, vfx-designer** | Nothing |
