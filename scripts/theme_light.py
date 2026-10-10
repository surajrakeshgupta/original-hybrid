"""Make a light-theme copy of each SVG (foo.svg -> foo-light.svg) for GitHub's
light mode. Known GitHub-dark colours map to their GitHub-light partners;
any other colour keeps its hue and has its lightness flipped.

    python scripts/theme_light.py                 # every panel in the repo root
    python scripts/theme_light.py info-card.svg   # just these files
"""
import colorsys
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PANELS = ["tagline", "ascii-portrait", "info-card", "career-log", "toolkit", "contrib-heatmap"]

MAP = {
    "#0d1117": "#ffffff",   # page / panel background
    "#000000": "#ffffff",   # portrait panel background
    "#161b22": "#f6f8fa",   # title bar, empty heatmap cell
    "#30363d": "#d0d7de",   # borders
    "#c9d1d9": "#1f2328",   # main text
    "#8b949e": "#59636e",   # dim text
    "#6e7681": "#6e7781",
    "#58a6ff": "#0969da",   # keys, package names
    "#39d353": "#1a7f37",   # prompt green
    "#69f0a0": "#116329",   # mint highlights
    "#d29922": "#9a6700",   # commit hashes
    "#39c5cf": "#1b7c83",
    "#0e2a17": "#dafbe1",   # pill fill
    # heatmap levels (GitHub light greens)
    "#0e4429": "#9be9a8",
    "#006d32": "#40c463",
    "#26a641": "#30a14e",
}
KEEP = {"#f85149", "#bc8cff"}   # window dots and swatches read fine on white
HEX = re.compile(r"#[0-9a-fA-F]{6}\b")


def flip(c: str) -> str:
    c = c.lower()
    if c in MAP:
        return MAP[c]
    if c in KEEP:
        return c
    r, g, b = (int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    l = 0.92 - l * 0.82          # bright glyphs -> dark ink, dark -> pale
    r, g, b = colorsys.hls_to_rgb(h, max(0.0, min(1.0, l)), s)
    return "#" + "".join(f"{round(v * 255):02x}" for v in (r, g, b))


def convert(path: Path) -> Path:
    out = path.with_name(path.stem + "-light.svg")
    text = HEX.sub(lambda m: flip(m.group(0)), path.read_text(encoding="utf-8"))
    # CRT scanlines are black; on white they need to be much fainter
    text = text.replace('fill="#000" opacity="0.16"', 'fill="#000" opacity="0.04"')
    out.write_text(text, encoding="utf-8")
    return out


def main() -> None:
    files = [Path(a) for a in sys.argv[1:]] or [ROOT / f"{p}.svg" for p in PANELS]
    for f in files:
        if f.exists():
            print("wrote", convert(f).name)


if __name__ == "__main__":
    main()
