#!/usr/bin/env python3
"""00 - Hangul by derivation.

DISPOSABLE. Use for three days, then suspend the deck. Hangul is not a list to
memorize, it is a system to derive: consonants are pictures of the mouth making
the sound, and adding a stroke adds aspiration. Once you can read, these cards
are dead weight -- any hangul card still in rotation at week three means you are
reading by lookup instead of by sight.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import letter_model

# (letter, sound, name, derivation, example syllable used for audio)
CONSONANTS = [
    ("ㄱ", "g / k", "기역 giyeok", "The back of the tongue humped up to the soft palate -- the shape is that tongue, seen from the side.", "가"),
    ("ㅋ", "k (aspirated)", "키읔 kieuk", "ㄱ plus one stroke. In hangul, an added stroke means an added puff of air.", "카"),
    ("ㄲ", "kk (tense)", "쌍기역 ssanggiyeok", "ㄱ doubled. Doubling means tense: no puff of air, throat tightened.", "까"),
    ("ㄴ", "n", "니은 nieun", "The tongue tip pressed to the ridge behind the top teeth, seen from the side.", "나"),
    ("ㄷ", "d / t", "디귿 digeut", "ㄴ with a lid. Same tongue position, but the airflow is stopped.", "다"),
    ("ㅌ", "t (aspirated)", "티읕 tieut", "ㄷ plus a stroke -- the aspirated partner.", "타"),
    ("ㄸ", "tt (tense)", "쌍디귿 ssangdigeut", "ㄷ doubled -- the tense partner.", "따"),
    ("ㅁ", "m", "미음 mieum", "The mouth, drawn as a square. Lips closed.", "마"),
    ("ㅂ", "b / p", "비읍 bieup", "ㅁ with the top opened -- lips closed, then released.", "바"),
    ("ㅍ", "p (aspirated)", "피읖 pieup", "The aspirated lip sound, built on the same mouth square.", "파"),
    ("ㅃ", "pp (tense)", "쌍비읍 ssangbieup", "ㅂ doubled -- the tense partner.", "빠"),
    ("ㅅ", "s / sh", "시옷 siot", "The teeth, drawn as a peak. Air hissing between them.", "사"),
    ("ㅈ", "j", "지읒 jieut", "ㅅ with a lid -- the same hiss, but stopped first.", "자"),
    ("ㅊ", "ch (aspirated)", "치읓 chieut", "ㅈ plus a stroke -- the aspirated partner.", "차"),
    ("ㅆ", "ss (tense)", "쌍시옷 ssangsiot", "ㅅ doubled -- the tense partner.", "싸"),
    ("ㅉ", "jj (tense)", "쌍지읒 ssangjieut", "ㅈ doubled -- the tense partner.", "짜"),
    ("ㅇ", "silent / ng", "이응 ieung", "The throat, drawn as a circle. Silent as a syllable's first letter; 'ng' at the bottom.", "아"),
    ("ㅎ", "h", "히읗 hieut", "The throat circle plus strokes -- breath pushed out of it.", "하"),
    ("ㄹ", "r / l", "리을 rieul", "The tongue flicking off the ridge. A tapped 'r' between vowels, an 'l' at the end.", "라"),
]

# The three source strokes, then everything built from them.
VOWELS = [
    ("ㅣ", "i", "이", "A standing human. One of the three source strokes.", "이"),
    ("ㅡ", "eu", "으", "The flat earth. One of the three source strokes. Say it with lips spread, not rounded.", "으"),
    ("ㅏ", "a", "아", "Human ㅣ with a mark to the right (toward the sun / outward, so it is a 'bright' vowel).", "아"),
    ("ㅓ", "eo", "어", "Human ㅣ with a mark to the left -- inward, so it is a 'dark' vowel.", "어"),
    ("ㅗ", "o", "오", "Earth ㅡ with a mark above it. Bright vowel.", "오"),
    ("ㅜ", "u", "우", "Earth ㅡ with a mark below it. Dark vowel.", "우"),
    ("ㅑ", "ya", "야", "ㅏ with a doubled mark. A doubled mark always adds a 'y' glide.", "야"),
    ("ㅕ", "yeo", "여", "ㅓ with a doubled mark -- adds the 'y' glide.", "여"),
    ("ㅛ", "yo", "요", "ㅗ with a doubled mark -- adds the 'y' glide.", "요"),
    ("ㅠ", "yu", "유", "ㅜ with a doubled mark -- adds the 'y' glide.", "유"),
    ("ㅐ", "ae", "애", "ㅏ + ㅣ written together. In modern speech nearly identical to ㅔ.", "애"),
    ("ㅔ", "e", "에", "ㅓ + ㅣ written together. In modern speech nearly identical to ㅐ.", "에"),
    ("ㅒ", "yae", "얘", "ㅑ + ㅣ. Rare.", "얘"),
    ("ㅖ", "ye", "예", "ㅕ + ㅣ.", "예"),
    ("ㅘ", "wa", "와", "ㅗ + ㅏ. Both bright vowels -- they combine.", "와"),
    ("ㅝ", "wo", "워", "ㅜ + ㅓ. Both dark vowels -- they combine.", "워"),
    ("ㅚ", "oe", "외", "ㅗ + ㅣ. Sounds like 'we' in modern Seoul speech.", "외"),
    ("ㅟ", "wi", "위", "ㅜ + ㅣ.", "위"),
    ("ㅙ", "wae", "왜", "ㅘ + ㅣ. Merged with ㅚ and ㅞ for most speakers.", "왜"),
    ("ㅞ", "we", "웨", "ㅝ + ㅣ. Merged with ㅚ and ㅙ for most speakers.", "웨"),
    ("ㅢ", "ui", "의", "ㅡ + ㅣ. Said 'ui' at the start of a word, often 'i' or 'e' elsewhere.", "의"),
]


def main():
    b = Build("00_hangul", "Korean v2::00 Hangul (disposable)")
    model = letter_model()

    for letter, sound, name, derivation, example in CONSONANTS:
        b.add(model, [letter, sound, name, derivation, example, b.audio(example)], tags=["hangul", "consonant"])

    for letter, sound, name, derivation, example in VOWELS:
        b.add(model, [letter, sound, name, derivation, example, b.audio(example)], tags=["hangul", "vowel"])

    b.write()


if __name__ == "__main__":
    main()
