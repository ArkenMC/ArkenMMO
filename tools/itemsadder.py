"""Build target/itemsadder-arkenmmo.zip: the pack as an ItemsAdder content folder.

Run via `mise run itemsadder`. resourcepack/ stays the only source of the art: its assets/ are
copied to arkenmmo/resourcepack/assets/ (ItemsAdder's "merge a resource pack" layout, which also
keeps the minecraft-namespace overrides), next to the item configs in itemsadder/contents/arkenmmo/.
pack.mcmeta and pack.png are left out because ItemsAdder writes its own.

ItemsAdder's item `tooltip_style: arkenmmo:tooltip/<name>` reads its images from
assets/arkenmmo/textures/tooltip/<name>_{background,frame}.png, not from the vanilla
gui/sprites/tooltip/ folder, so the item tooltips (ITEM_TOOLTIPS) are copied there as well.

On the server: unzip into plugins/ItemsAdder/contents/ (giving contents/arkenmmo/), then /iazip.
"""
import sys
import zipfile
from pathlib import Path

ASSETS = Path("resourcepack/assets")
CONTENT = Path("itemsadder/contents/arkenmmo")
OUTPUT = Path("target/itemsadder-arkenmmo.zip")
FIXED_TIME = (1980, 1, 1, 0, 0, 0)
TOOLTIP_SPRITES = ASSETS / "arkenmmo/textures/gui/sprites/tooltip"
ITEM_TOOLTIPS = ("emerald", "accessory")


def entries():
    for path in sorted(p for p in ASSETS.rglob("*") if p.is_file()):
        yield f"arkenmmo/resourcepack/assets/{path.relative_to(ASSETS).as_posix()}", path
    for name in ITEM_TOOLTIPS:
        for path in sorted(TOOLTIP_SPRITES.glob(f"{name}_*.png*")):
            yield f"arkenmmo/resourcepack/assets/arkenmmo/textures/tooltip/{path.name}", path
    for path in sorted(p for p in CONTENT.rglob("*") if p.is_file()):
        yield f"arkenmmo/{path.relative_to(CONTENT).as_posix()}", path


def main() -> int:
    if not ASSETS.is_dir():
        print(f"{ASSETS} not found; nothing to pack.")
        return 1
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with zipfile.ZipFile(OUTPUT, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for name, path in entries():
            entry = zipfile.ZipInfo(name, FIXED_TIME)
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o644 << 16
            zf.writestr(entry, path.read_bytes())
            count += 1
    print(f"{OUTPUT}  {count} file(s)  {OUTPUT.stat().st_size} bytes")
    print("Unzip into plugins/ItemsAdder/contents/ on the server, then run /iazip.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
