#!/usr/bin/env python3
"""02 - Batchim sound change (spelling vs. sound).

The single thing that strands beginners after hangul: Korean is not spelled the
way it is said. 좋아요 is said 조아요, 한국말 is said 한궁말, 십만 is said 심만.
A learner who trusts the letters mishears every one of these and concludes that
Korean is "too fast".

Audio on the front, spelling on the back -- so the ear leads and the eye
corrects, which is the order these rules have to be learned in.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import audio_only_model

LIAISON = "Liaison (연음): a final consonant slides into the next syllable when that syllable starts with ㅇ."
H_DROP = "ㅎ deletion: ㅎ goes silent between a vowel and a vowel."
NASAL = "Nasalization (비음화): ㄱ/ㄷ/ㅂ turn into ㅇ/ㄴ/ㅁ before ㄴ or ㅁ."
LIQUID = "Liquid assimilation (유음화): ㄴ next to ㄹ becomes ㄹ, giving a double ㄹㄹ."
ASPIR = "Aspiration (격음화): ㅎ merges with a following ㄱ/ㄷ/ㅈ/ㅂ to make ㅋ/ㅌ/ㅊ/ㅍ."
TENSE = "Tensification (경음화): after a ㄱ/ㄷ/ㅂ stop, a following plain consonant goes tense."
NEUTRAL = "Final neutralization: only ㄱ ㄴ ㄷ ㄹ ㅁ ㅂ ㅇ can actually close a syllable; everything else collapses to one of them."
N_INSERT = "ㄴ insertion: a ㄴ appears between a consonant-final part and a following 이/야/여/요/유 sound."

# (spelling, how it is actually said, english, rule)
ITEMS = [
    ("한국어", "한구거", "Korean language", LIAISON),
    ("밥이", "바비", "rice (as subject)", LIAISON),
    ("음악을", "으마글", "music (as object)", LIAISON),
    ("직업이", "지거비", "occupation (as subject)", LIAISON),
    ("책을", "채글", "book (as object)", LIAISON),

    ("좋아요", "조아요", "it's good / I like it", H_DROP),
    ("많이", "마니", "a lot, many", H_DROP),
    ("싫어요", "시러요", "I don't like it", H_DROP),
    ("괜찮아요", "괜차나요", "it's okay", H_DROP),

    ("한국말", "한궁말", "the Korean language", NASAL),
    ("학년", "항년", "school year, grade", NASAL),
    ("감사합니다", "감사함니다", "thank you", NASAL),
    ("십만", "심만", "one hundred thousand", NASAL),
    ("있는", "인는", "that exists / which has", NASAL),
    ("앞문", "암문", "front door", NASAL),
    ("작년", "장년", "last year", NASAL),

    ("연락", "열락", "contact, getting in touch", LIQUID),
    ("신라", "실라", "Silla (the old kingdom)", LIQUID),
    ("설날", "설랄", "Lunar New Year", LIQUID),
    ("일 년", "일련", "one year", LIQUID),

    ("좋다", "조타", "to be good", ASPIR),
    ("축하", "추카", "congratulations", ASPIR),
    ("많다", "만타", "to be many", ASPIR),
    ("입학", "이팍", "entering a school", ASPIR),
    ("못해요", "모태요", "I can't do it", ASPIR),

    ("학교", "학꾜", "school", TENSE),
    ("식당", "식땅", "restaurant", TENSE),
    ("갑자기", "갑짜기", "suddenly", TENSE),
    ("젓가락", "젇까락", "chopsticks", TENSE),
    ("숙제", "숙쩨", "homework", TENSE),

    ("옷", "옫", "clothes", NEUTRAL),
    ("꽃", "꼳", "flower", NEUTRAL),
    ("부엌", "부억", "kitchen", NEUTRAL),
    ("밖", "박", "outside", NEUTRAL),

    ("꽃잎", "꼰닙", "flower petal", N_INSERT),
    ("무슨 요일", "무슨 뇨일", "what day of the week", N_INSERT),
]


def main():
    b = Build("02_batchim", "Korean v2::02 Batchim sound change")
    model = audio_only_model()

    for spelling, said, english, rule in ITEMS:
        note = "Written 「%s」 · said 「%s」<br><br>%s" % (spelling, said, rule)
        b.add(model, [b.audio(spelling), spelling, english, "", note], tags=["batchim"])

    b.write()


if __name__ == "__main__":
    main()
