# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Normalise a downloaded picture into the module binary folder.

Usage: optimize_asset.py SOURCE TARGET_DIR NAME MAX_WIDTH

Vector files and anything with MAX_WIDTH 0 are copied verbatim. Raster files
are downscaled to MAX_WIDTH and re-encoded as JPEG, or as PNG when the source
carries transparency.
"""
# This is a standalone maintenance script, not Odoo server code.
# pylint: disable=print-used

import shutil
import sys
from pathlib import Path

from PIL import Image

JPEG_QUALITY = 82


def main():
    source, target_dir, name, max_width = sys.argv[1:5]
    source = Path(source)
    target_dir = Path(target_dir)
    max_width = int(max_width)

    try:
        image = Image.open(source)
    except Exception:
        image = None

    if image is None or max_width == 0:
        suffix = ".svg" if image is None else (image.format or "png").lower()
        target = target_dir / f"{name}.{suffix.lstrip('.')}"
        shutil.copyfile(source, target)
        print(f"{target.name} ({target.stat().st_size // 1024} KiB, verbatim)")
        return

    has_alpha = image.mode in ("RGBA", "LA") or (
        image.mode == "P" and "transparency" in image.info
    )
    if image.width > max_width:
        height = round(image.height * max_width / image.width)
        image = image.resize((max_width, height), Image.LANCZOS)

    if has_alpha:
        target = target_dir / f"{name}.png"
        image.convert("RGBA").save(target, "PNG", optimize=True)
    else:
        target = target_dir / f"{name}.jpg"
        image.convert("RGB").save(
            target, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True
        )

    print(f"{target.name} ({target.stat().st_size // 1024} KiB, {image.width}px)")


if __name__ == "__main__":
    main()
