"""Draw every preset of effects.yml, using the plugin's compiled Shapes class for the points.

Needs target/classes (mise run vfx-previews builds it first). Writes target/vfx-points/<effect>.csv
and design/vfx-previews/<effect>.png. Colours are the layers' own, so the picture is close to the
game's palette; particle sprites, size over time and motion are not simulated.
"""
import subprocess
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import yaml

ROOT = Path(__file__).resolve().parents[2]
POINTS_DIR = ROOT / "target/vfx-points"
PREVIEW_DIR = ROOT / "design/vfx-previews"
# Stand-in colours for particles whose look comes from the client's own sprite
SPRITES = {"sweep_attack": "#e8e8e8", "crit": "#d8b878", "poof": "#a8a8a8",
           "dust_plume": "#b0a090", "block": "#7a5a3a"}


def shape_line(effect, index, layer):
    """The same defaults as LayerParser."""
    if layer["shape"] == "arc":
        radius, y = layer.get("radius", 1), layer.get("y", 0)
        numbers = [layer.get("start-angle", 0), layer.get("sweep", 360), radius,
                   layer.get("end-radius", radius), y, layer.get("end-y", y)]
    else:
        numbers = layer["from"] + layer["to"]
    fields = [effect, index, layer["shape"], layer.get("points", 1), layer.get("delay-ticks", 0),
              layer.get("duration-ticks", 1), layer.get("motion", "none").upper(), layer.get("lift", 0)]
    return "\t".join(str(value) for value in fields + numbers)


def colour(layer):
    if layer.get("block") == "minecraft:redstone_block":
        return "#c01808"
    return layer.get("color", SPRITES.get(layer["particle"], "#ffffff"))


def export(presets):
    lines = [shape_line(effect, i, layer)
             for effect, preset in presets.items() for i, layer in enumerate(preset["layers"])]
    result = subprocess.run(
        ["java", "-cp", str(ROOT / "target/classes"), str(ROOT / "design/vfx-scripts/ExportPoints.java")],
        input="\n".join(lines) + "\n", capture_output=True, text=True, check=True)
    points = defaultdict(list)
    for row in result.stdout.splitlines():
        effect, tick, x, y, z, layer = row.split(",")
        points[effect].append((int(tick), float(x), float(y), float(z), int(layer)))
    return points


def plot(effect, layers, points):
    figure = plt.figure(figsize=(16, 9), facecolor="#202830")
    views = [("3D, from behind the caster", None), ("top (facing up)", (1, 3)), ("front", (1, 2))]
    for column, (title, axes) in enumerate(views, start=1):
        axis = figure.add_subplot(2, 3, column, projection="3d" if axes is None else None)
        axis.set_facecolor("#202830")
        for tick, x, y, z, layer in points:
            style = dict(color=colour(layers[layer]), s=60 if layers[layer]["particle"] == "sweep_attack" else 14)
            if axes is None:
                axis.scatter(x, z, y, **style)
            else:
                row = (tick, x, y, z)
                axis.scatter(row[axes[0]], row[axes[1]], **style)
        if axes is None:
            axis.view_init(elev=28, azim=-90)
            axis.set(xlim=(4.5, -4.5), ylim=(-4.5, 4.5), zlim=(0, 4))
            axis.set_box_aspect((9, 9, 4))
        else:
            # Looking along +z, the caster's right (-x) is on the right of the picture
            axis.set_xlim(4.5, -4.5)
            axis.set_ylim((-4.5, 4.5) if axes[1] == 3 else (0, 4))
            axis.set_aspect("equal")
            axis.grid(alpha=0.2)
            axis.plot(0, 0, marker="+", color="white", markersize=10)
        axis.set_title(title, color="white")
        axis.tick_params(colors="white", labelsize=7)
    # Second row: the top view as it fills in, coloured only by what has appeared so far
    last = max(point[0] for point in points)
    for column, tick in enumerate((0, last // 2, last), start=4):
        axis = figure.add_subplot(2, 3, column)
        axis.set_facecolor("#202830")
        for when, x, y, z, layer in points:
            if when <= tick:
                axis.scatter(x, z, color=colour(layers[layer]), s=14)
        axis.set(xlim=(4.5, -4.5), ylim=(-4.5, 4.5))
        axis.set_aspect("equal")
        axis.grid(alpha=0.2)
        axis.set_title(f"top, up to tick {tick}", color="white")
        axis.tick_params(colors="white", labelsize=7)
    figure.suptitle(f"{effect}: {len(points)} particles over {last + 1} tick(s)", color="white")
    figure.tight_layout()
    figure.savefig(PREVIEW_DIR / f"{effect}.png", dpi=80, facecolor=figure.get_facecolor())
    plt.close(figure)


def main():
    presets = yaml.safe_load((ROOT / "src/main/resources/effects.yml").read_text(encoding="utf-8"))
    presets.pop("limits", None)
    points = export(presets)
    POINTS_DIR.mkdir(parents=True, exist_ok=True)
    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)
    for effect, preset in presets.items():
        rows = [",".join(str(value) for value in point) for point in points[effect]]
        (POINTS_DIR / f"{effect}.csv").write_text("tick,x,y,z,layer\n" + "\n".join(rows) + "\n", encoding="utf-8")
        plot(effect, preset["layers"], points[effect])
        radius = max((x * x + z * z) ** 0.5 for _, x, _, z, _ in points[effect])
        print(f"{effect}: {len(rows)} particles, ticks 0-{max(p[0] for p in points[effect])}, "
              f"max horizontal radius {radius:.2f}")


if __name__ == "__main__":
    main()
