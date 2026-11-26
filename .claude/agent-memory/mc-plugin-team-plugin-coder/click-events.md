---
name: click-events
description: How Paper 26.3 raises click events (server source and Javadocs); what is still unverified without a client
metadata:
  type: reference
---

Verified 2026-11-26 (stable for 26.3). Source: PaperMC/Paper `main` (gradle.properties mcVersion=26.3), `paper-server/patches/sources/net/minecraft/` (`server/network/ServerGamePacketListenerImpl`, `server/level/ServerPlayerGameMode`, `world/entity/player/Player` `.java.patch`) and jd.papermc.io/paper/26.3.

- The swing packet is `ServerboundPunchPacket` (`handlePunch`): `LEFT_CLICK_AIR` if a block+entity ray trace misses (or hits an entity beyond reach, non-creative), then `PlayerArmSwingEvent`. A block or reachable entity gives no AIR event; adventure mode gets `LEFT_CLICK_BLOCK` from here.
- Otherwise `LEFT_CLICK_BLOCK` comes from the digging packet; entity hits give `PrePlayerAttackEntityEvent` (also when `willAttack()` is false).
- `handleUseItem` fires `RIGHT_CLICK_AIR`, or `RIGHT_CLICK_BLOCK` if its own ray hits a block; it skips a repeat of the block event already fired by use-item-on.
- Entity right-click: `handleInteract` fires `PlayerInteractAtEntityEvent`. It inherits `PlayerInteractEntityEvent`'s HandlerList, so one handler on the parent gets both.
- Deprecated: `PlayerAnimationEvent`, `Material#isInteractable`.
- Unverified (client side): when the client sends punch (after right-click use, drop, while mining), held-right repeat rate, bow draw vs left clicks.
- 26.2 (checked 2026-11-26, stable; github PaperMC/Paper branch `ver/26.2`, `ServerGamePacketListenerImpl.java.patch`, second page of WebFetch at offset 100000): the swing packet is `ServerboundSwingPacket` (`handleAnimate`), with the same LEFT_CLICK_AIR and PlayerArmSwingEvent logic.
- Applied in `casting/` (rules: docs/architecture.md "Casting input").
