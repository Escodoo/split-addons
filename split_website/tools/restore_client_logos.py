# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Restore official client logos as opaque white cards.

The studio site ships JPEG/PNG logos that already sit on a white plate. A
previous knockout pass punched that plate out and left black marks (plus
jagged halos) on the dark homepage. This script downloads the official
files again and flattens any transparency onto white.
"""
# This is a standalone maintenance script, not Odoo server code.
# pylint: disable=print-used

import sys
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parent))
from optimize_asset import flatten_on_white

ASSETS = Path(__file__).resolve().parent / "assets.tsv"
BINARY_DIR = (
    Path(__file__).resolve().parent.parent
    / "static"
    / "src"
    / "binary"
    / "ir_attachment"
)
USER_AGENT = "Mozilla/5.0 (compatible; split_website/restore)"


def _download(url):
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return response.read()


def main():
    BINARY_DIR.mkdir(parents=True, exist_ok=True)
    restored = 0
    for raw_line in ASSETS.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line.startswith("#"):
            continue
        name, max_width, url = raw_line.split("\t")
        if not name.startswith("client_"):
            continue
        payload = _download(url)
        target = BINARY_DIR / f"{name}.png"
        flatten_on_white(payload, target, int(max_width))
        restored += 1
    print(f"restored {restored} client logos")


if __name__ == "__main__":
    main()
