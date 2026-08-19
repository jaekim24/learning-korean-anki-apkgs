#!/usr/bin/env python3
"""Build every v2 deck into build/.

Audio is cached in build/audio/, so the first run downloads ~480 clips and
later runs are effectively instant unless deck text changed.
"""

import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

DECKS = [
    "d00_hangul",
    "d01_minimal_pairs",
    "d02_batchim",
    "d03_core_vocab",
    "d04_particles_cloze",
    "d05_conjugation",
    "d06_sentence_patterns",
]


def main():
    sys.path.insert(0, os.path.join(HERE, "decks"))
    print("Building %d decks...\n" % len(DECKS))
    for name in DECKS:
        importlib.import_module(name).main()
    print("\nDone. Import the .apkg files in build/ in numeric order.")


if __name__ == "__main__":
    main()
