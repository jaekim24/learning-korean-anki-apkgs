#!/usr/bin/env python3
"""01 - Minimal pairs: plain vs tense vs aspirated.

This is perceptual training, not vocabulary. An English speaker's ears sort
Korean's three-way stop contrast into two English categories, so 불 / 뿔 / 풀
arrive as the same word until the categories are retrained. Ten days of this
fixes it. Skip it and every listening skill built afterward has a hole in it.

Each card plays one member of a set and shows the whole set as options -- forced
choice, no text hint on the front.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import audio_only_model

PLAIN = "Plain: relaxed throat, light voicing. The 'default' one."
TENSE = "Tense: throat squeezed, no puff of air. Sounds clipped and hard."
ASPIRATED = "Aspirated: strong puff of air, as if fogging a window."

# (set_label, [(korean, english, hint), ...])
SETS = [
    ("ㅂ / ㅃ / ㅍ", [("불", "fire", PLAIN), ("뿔", "horn", TENSE), ("풀", "grass", ASPIRATED)]),
    ("ㄷ / ㄸ / ㅌ", [("달", "moon", PLAIN), ("딸", "daughter", TENSE), ("탈", "mask", ASPIRATED)]),
    ("ㅈ / ㅉ / ㅊ", [("자다", "to sleep", PLAIN), ("짜다", "to be salty", TENSE), ("차다", "to be cold", ASPIRATED)]),
    ("ㄱ / ㄲ / ㅋ", [("개다", "to fold", PLAIN), ("깨다", "to break", TENSE), ("캐다", "to dig up", ASPIRATED)]),
    ("ㄱ / ㄲ", [("굴", "oyster", PLAIN), ("꿀", "honey", TENSE)]),
    ("ㅅ / ㅆ", [("사다", "to buy", PLAIN), ("싸다", "to be cheap", TENSE)]),
    ("ㅅ / ㅆ", [("살", "flesh; years of age", PLAIN), ("쌀", "uncooked rice", TENSE)]),
    ("ㅂ / ㅃ", [("방", "room", PLAIN), ("빵", "bread", TENSE)]),
    ("ㅂ / ㅍ", [("발", "foot", PLAIN), ("팔", "arm", ASPIRATED)]),
    ("ㅈ / ㅊ", [("종", "bell", PLAIN), ("총", "gun", ASPIRATED)]),
]

# Vowel contrasts English does not distinguish either.
VOWEL_SETS = [
    ("ㅓ / ㅗ", [("벌", "bee", "ㅓ: mouth relaxed and open, lips NOT rounded."),
                 ("볼", "cheek", "ㅗ: lips pushed forward into a tight circle.")]),
    ("ㅡ / ㅜ", [("글", "writing, text", "ㅡ: lips spread wide, almost a grimace."),
                 ("굴", "oyster", "ㅜ: lips rounded and pushed out.")]),
    ("ㅗ / ㅜ", [("소", "cow", "ㅗ: jaw lower, rounder and more open."),
                 ("수", "number", "ㅜ: jaw higher, lips tighter.")]),
    ("ㅓ / ㅏ", [("섬", "island", "ㅓ: tongue back, lips neutral, jaw only half open."),
                 ("삼", "three", "ㅏ: jaw dropped, bright and open.")]),
]


def main():
    b = Build("01_minimal_pairs", "Korean v2::01 Minimal pairs (listening)")
    model = audio_only_model()

    for label, members in SETS + VOWEL_SETS:
        options = "  ·  ".join(k for k, _, _ in members)
        for korean, english, hint in members:
            b.add(
                model,
                [b.audio(korean), korean, english, options, "%s  --  %s" % (label, hint)],
                tags=["minimal-pair"],
            )

    b.write()


if __name__ == "__main__":
    main()
