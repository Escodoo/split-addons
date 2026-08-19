# Copyright 2026 Escodoo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Compatibility wrapper. The old knockout pass damaged the client logos.

Run restore_client_logos.py instead: it re-downloads the official white-card
assets used on splitstudio.tv.
"""
# pylint: disable=print-used

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from restore_client_logos import main

if __name__ == "__main__":
    print("knockout is retired; restoring official white-card logos instead")
    main()
