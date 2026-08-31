#!/usr/bin/env python3
"""Build every v3 unit into build/.

One .apkg per unit, with a subdeck per HTSK lesson inside it. Audio is cached
in build/audio/, so the first run downloads the clips and later runs are
effectively instant unless sentence text changed.
"""

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from korean import compose

# Units are added here as their content is written.
UNITS = [1]


def main():
    print("Building %d unit(s)...\n" % len(UNITS))
    for unit in UNITS:
        mod = importlib.import_module("units.unit%d" % unit)
        compose.build_unit(unit, mod.LESSONS)
    print("\nDone. Import the .apkg files in build/ in unit order.")


if __name__ == "__main__":
    main()
