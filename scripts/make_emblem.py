"""Draw a shield-and-padlock emblem as a transparent PNG for the ASCII panel.

Used in place of a photo. To switch to your own face later, follow the photo
steps in the template docs (prep_photo.py writes source-prepped.png) and run
make_ascii_svg.py without --src.

    python scripts/make_emblem.py        # writes emblem.png
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
W, H = 600, 780


def shield_path(cx: float, top: float, w: float, h: float, n: int = 120) -> list[tuple[float, float]]:
    """Classic heater-shield outline: flat-ish top with a dip, curved sides to a point."""
    pts = []
    half = w / 2
    # top edge with a gentle dip in the middle
    for i in range(n + 1):
        t = i / n
        x = cx - half + w * t
        y = top + 26 * np.sin(np.pi * t) ** 2
        pts.append((x, y))
    def side(t: float) -> tuple[float, float]:
        # straight for the first 40%, then an elliptical curve into the point
        y = top + h * t
        if t <= 0.4:
            return half, y
        u = (t - 0.4) / 0.6
        return half * np.sqrt(max(0.0, 1 - u ** 1.6)), y

    for i in range(1, n + 1):                # right side down to the point
        dx, y = side(i / n)
        pts.append((cx + dx, y))
    for i in range(n - 1, 0, -1):            # left side back up
        dx, y = side(i / n)
        pts.append((cx - dx, y))
    return pts


def main() -> None:
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    lum = Image.new("L", (W, H), 0)
    mask = Image.new("L", (W, H), 0)

    cx, top = W / 2, 30
    outer = shield_path(cx, top, 540, 720)
    inner = shield_path(cx, top + 38, 456, 616)

    ImageDraw.Draw(mask).polygon(outer, fill=255)

    d = ImageDraw.Draw(lum)
    d.polygon(outer, fill=235)                     # bright rim
    d.polygon(inner, fill=60)                      # dim field

    # vertical shading on the field so the ASCII ramp has depth
    grad = np.linspace(1.3, 0.45, H)[:, None] * np.ones((1, W))
    arr = np.array(lum, dtype=np.float32)
    field = arr == 60
    arr[field] = np.clip(arr[field] * grad[field], 0, 255)
    lum = Image.fromarray(arr.astype(np.uint8))
    d = ImageDraw.Draw(lum)

    # padlock: shackle + body + keyhole
    bw, bh = 260, 210
    bx, by = cx - bw / 2, 330
    d.rounded_rectangle([cx - 92, 160, cx + 92, by + 60], radius=92, outline=250, width=38)
    d.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=250)
    d.ellipse([cx - 30, by + 50, cx + 30, by + 110], fill=10)
    d.polygon([(cx - 17, by + 96), (cx + 17, by + 96), (cx + 26, by + 170), (cx - 26, by + 170)], fill=10)

    lum = lum.filter(ImageFilter.GaussianBlur(1.2))
    img = Image.merge("RGBA", (lum, lum, lum, mask))
    out = ROOT / "emblem.png"
    img.save(out)
    print(f"wrote {out.name}")


if __name__ == "__main__":
    main()
