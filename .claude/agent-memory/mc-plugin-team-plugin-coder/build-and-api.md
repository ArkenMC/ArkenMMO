---
name: build-and-api
description: Sandbox workaround for mise build and verified Paper 26.3 facts from the classes feature
metadata:
  type: reference
---

Verified 2026-11-25.

- Sandbox: `mise run build` fails with "Read-only file system" (mise state/cache dirs). Fix (stable): `MISE_STATE_DIR="$TMPDIR/mise-state" MISE_CACHE_DIR="$TMPDIR/mise-cache" mise run build`.
- Worktree isolation guard refuses Bash heredocs that write many files, `$(...)` with long paths and some compound commands. Use the Write tool and Java `@argfile`s.
- Compiles clean on paper-api 26.3.build.205-stable (stable; source: build + sources jar in ~/.m2): `ResourcePackInfo.resourcePackInfo(UUID, URI, String)`, `Player#sendResourcePacks(ResourcePackRequest)`, `PlayerResourcePackStatusEvent#getID/getStatus`, `ArgumentTypes.player()` with `PlayerSelectorArgumentResolver#resolve(source)`, `DataComponentTypes.ITEM_MODEL/ITEM_NAME/LORE/TOOLTIP_STYLE`, `ItemStack.of`, `Inventory#getHolder(false)`.
- `\uXXXX` escapes in double-quoted YAML survive `YamlConfiguration` + MiniMessage `<!shadow><white><font:arkenmmo:gui>` (checked by a one-off Java run on messages.yml).
- User rule for ArkenMMO: no tests of any kind for the classes feature (see docs/briefs/classes.md).

Verified 2026-11-26 (skill menus).

- Compiles on 26.3.build.205-stable (stable): `DataComponentTypes.TOOLTIP_DISPLAY` + `TooltipDisplay.tooltipDisplay().hideTooltip(true).build()`, `PersistentDataType.LIST.strings()`, nested `PersistentDataType.TAG_CONTAINER`.
- `YamlConfiguration` + MiniMessage run without a server: check shipped text with a single-file Java program, classpath from `mvn dependency:build-classpath` (put `-cp` in a Java `@argfile`).
- Worktree guard also refuses multi-file inline Python and commands mixing `git show` with redirects and variables: write scripts to the scratchpad and run them with `python3 -I`.
