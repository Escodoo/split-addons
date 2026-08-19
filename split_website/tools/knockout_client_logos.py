# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Turn the white card behind each client logo into a transparent PNG."""
# pylint: disable=print-used

from pathlib import Path

from PIL import Image

BINARY_DIR = (
    Path(__file__).resolve().parent.parent
    / "static"
    / "src"
    / "binary"
    / "ir_attachment"
)
WHITE_THRESHOLD = 232


def _is_background(pixel):
    red, green, blue, alpha = pixel
    if alpha < 16:
        return True
    return (
        red >= WHITE_THRESHOLD and green >= WHITE_THRESHOLD and blue >= WHITE_THRESHOLD
    )


def knockout(path):
    image = Image.open(path).convert("RGBA")
    pixels = image.load()
    width, height = image.size
    changed = 0
    for x in range(width):
        for y in range(height):
            if _is_background(pixels[x, y]):
                pixels[x, y] = (0, 0, 0, 0)
                changed += 1
    target = path.with_suffix(".png")
    image.save(target, "PNG", optimize=True)
    if target != path:
        path.unlink()
    print(f"{target.name}: knocked out {changed} px")


def main():
    for path in sorted(BINARY_DIR.glob("client_*")):
        knockout(path)


if __name__ == "__main__":
    main()
