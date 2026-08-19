#!/usr/bin/env python3
"""05 - Conjugation as rules, not as stored forms.

v1's tense deck held ~100 verbs x several tenses as individually memorized
forms. But Korean conjugation is nearly regular: three rules plus seven
irregular classes generate all of it. This deck drills the *transformation* and
names the rule on the back, so the learner ends up with a generator instead of a
lookup table -- and it costs about sixty cards instead of six hundred.

Each irregular class also gets "trap" cards: verbs that look like they belong to
the class and are actually regular. Those are where the errors live.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import transform_model

PRESENT = "→ 해요체 (polite present)"
PAST = "→ past tense"
FORMAL = "→ 합니다체 / -세요"

HARMONY = ("Drop 다 to get the stem. If the stem's last vowel is ㅏ or ㅗ, add 아요. "
           "Otherwise add 어요. 하다 is the one exception: it becomes 해요.")

# (dictionary form, task, answer, rule note, tag)
ITEMS = [
    # --- The three regular rules ---
    ("먹다", PRESENT, "먹어요", "Stem 먹-, last vowel ㅓ (not ㅏ/ㅗ) → 어요. " + HARMONY, "regular"),
    ("읽다", PRESENT, "읽어요", "Stem 읽-, last vowel ㅣ → 어요.", "regular"),
    ("앉다", PRESENT, "앉아요", "Stem 앉-, last vowel ㅏ → 아요.", "regular"),
    ("받다", PRESENT, "받아요", "Stem 받-, last vowel ㅏ → 아요.", "regular"),
    ("웃다", PRESENT, "웃어요", "Stem 웃-, last vowel ㅜ → 어요. Only ㅏ and ㅗ take 아요.", "regular"),
    ("좋다", PRESENT, "좋아요", "Stem 좋-, last vowel ㅗ → 아요.", "regular"),
    ("하다", PRESENT, "해요", "하다 is irregular on its own and becomes 해요. Every 하다 compound follows it.", "regular"),
    ("공부하다", PRESENT, "공부해요", "Any noun + 하다 conjugates like 하다 → 해요.", "regular"),
    ("일하다", PRESENT, "일해요", "Noun + 하다 → 해요.", "regular"),

    # --- Contractions: stem already ends in a vowel ---
    ("가다", PRESENT, "가요", "Stem 가- already ends in ㅏ, so 가 + 아요 merges into just 가요.", "contraction"),
    ("서다", PRESENT, "서요", "서 + 어요 merges to 서요. Identical vowels always collapse into one.", "contraction"),
    ("오다", PRESENT, "와요", "오 + 아요 → 와요. ㅗ and ㅏ fuse into ㅘ.", "contraction"),
    ("보다", PRESENT, "봐요", "보 + 아요 → 봐요, the same ㅗ + ㅏ = ㅘ fusion.", "contraction"),
    ("주다", PRESENT, "줘요", "주 + 어요 → 줘요. ㅜ and ㅓ fuse into ㅝ.", "contraction"),
    ("배우다", PRESENT, "배워요", "배우 + 어요 → 배워요, the same ㅜ + ㅓ = ㅝ fusion.", "contraction"),
    ("마시다", PRESENT, "마셔요", "마시 + 어요 → 마셔요. ㅣ and ㅓ fuse into ㅕ.", "contraction"),
    ("기다리다", PRESENT, "기다려요", "기다리 + 어요 → 기다려요, the same ㅣ + ㅓ = ㅕ fusion.", "contraction"),
    ("되다", PRESENT, "돼요", "되 + 어요 → 돼요. This is why 되요 is always a spelling mistake.", "contraction"),

    # --- ㅂ irregular ---
    ("춥다", PRESENT, "추워요", "ㅂ irregular: before a vowel, ㅂ becomes 우. 춥 → 추우 + 어요 → 추워요.", "irr-b"),
    ("덥다", PRESENT, "더워요", "ㅂ irregular: 덥 → 더우 + 어요 → 더워요.", "irr-b"),
    ("쉽다", PRESENT, "쉬워요", "ㅂ irregular: 쉽 → 쉬우 + 어요 → 쉬워요.", "irr-b"),
    ("어렵다", PRESENT, "어려워요", "ㅂ irregular: 어렵 → 어려우 + 어요.", "irr-b"),
    ("무겁다", PRESENT, "무거워요", "ㅂ irregular: 무겁 → 무거우 + 어요.", "irr-b"),
    ("돕다", PRESENT, "도와요", "ㅂ irregular, but 돕다 and 곱다 take 오 rather than 우: 도오 + 아요 → 도와요.", "irr-b"),
    ("입다", PRESENT, "입어요", "TRAP: 입다 is REGULAR. It ends in ㅂ but does not change. Compare 춥다 → 추워요.", "irr-b"),
    ("좁다", PRESENT, "좁아요", "TRAP: 좁다 is REGULAR despite the ㅂ. Last vowel ㅗ → 아요.", "irr-b"),
    ("잡다", PRESENT, "잡아요", "TRAP: 잡다 is REGULAR despite the ㅂ.", "irr-b"),

    # --- ㄷ irregular ---
    ("듣다", PRESENT, "들어요", "ㄷ irregular: before a vowel, ㄷ becomes ㄹ. 듣 → 들 + 어요.", "irr-d"),
    ("걷다", PRESENT, "걸어요", "ㄷ irregular: 걷 → 걸 + 어요. (걷다 = to walk.)", "irr-d"),
    ("묻다", PRESENT, "물어요", "ㄷ irregular: 묻 → 물 + 어요. (묻다 = to ask.)", "irr-d"),
    ("받다", PAST, "받았어요", "TRAP: 받다 is REGULAR despite the ㄷ. It never becomes 발-.", "irr-d"),
    ("닫다", PRESENT, "닫아요", "TRAP: 닫다 is REGULAR despite the ㄷ.", "irr-d"),
    ("믿다", PRESENT, "믿어요", "TRAP: 믿다 is REGULAR despite the ㄷ.", "irr-d"),

    # --- ㅅ irregular ---
    ("짓다", PRESENT, "지어요", "ㅅ irregular: the ㅅ simply disappears before a vowel. 짓 → 지 + 어요.", "irr-s"),
    ("낫다", PRESENT, "나아요", "ㅅ irregular: 낫 → 나 + 아요. The two vowels do NOT contract here.", "irr-s"),
    ("붓다", PRESENT, "부어요", "ㅅ irregular: 붓 → 부 + 어요.", "irr-s"),
    ("웃다", PAST, "웃었어요", "TRAP: 웃다 is REGULAR despite the ㅅ. The ㅅ stays.", "irr-s"),
    ("씻다", PRESENT, "씻어요", "TRAP: 씻다 is REGULAR despite the ㅅ.", "irr-s"),
    ("벗다", PRESENT, "벗어요", "TRAP: 벗다 is REGULAR despite the ㅅ.", "irr-s"),

    # --- ㄹ irregular (deletion) ---
    ("살다", FORMAL, "삽니다", "ㄹ irregular: the stem's ㄹ drops before ㄴ, ㅂ, ㅅ. 살 + ㅂ니다 → 삽니다.", "irr-l"),
    ("살다", PRESENT, "살아요", "ㄹ verbs are REGULAR in 해요체 -- 아요/어요 does not start with ㄴ/ㅂ/ㅅ, so nothing drops.", "irr-l"),
    ("알다", FORMAL, "아세요", "ㄹ irregular: 알 + 으세요 → 아세요, the ㄹ dropping before ㅅ.", "irr-l"),
    ("만들다", FORMAL, "만듭니다", "ㄹ irregular: 만들 + ㅂ니다 → 만듭니다.", "irr-l"),
    ("길다", FORMAL, "깁니다", "ㄹ irregular: 길 + ㅂ니다 → 깁니다.", "irr-l"),

    # --- 르 irregular ---
    ("모르다", PRESENT, "몰라요", "르 irregular: 르 → ㄹ라/ㄹ러, doubling the ㄹ. 모르 → 몰ㄹ + 아요 → 몰라요.", "irr-reu"),
    ("부르다", PRESENT, "불러요", "르 irregular: 부르 → 불ㄹ + 어요 → 불러요.", "irr-reu"),
    ("빠르다", PRESENT, "빨라요", "르 irregular: 빠르 → 빨ㄹ + 아요 → 빨라요.", "irr-reu"),
    ("다르다", PRESENT, "달라요", "르 irregular: 다르 → 달ㄹ + 아요 → 달라요.", "irr-reu"),
    ("고르다", PRESENT, "골라요", "르 irregular: 고르 → 골ㄹ + 아요 → 골라요.", "irr-reu"),
    ("따르다", PRESENT, "따라요", "TRAP: 따르다 is NOT 르-irregular. It just drops 으: 따ㄹ + 아요 → 따라요, no doubled ㄹ.", "irr-reu"),

    # --- 으 irregular (deletion) ---
    ("쓰다", PRESENT, "써요", "으 irregular: the 으 drops. With no vowel before it, default to 어요. 쓰 → ㅆ + 어요 → 써요.", "irr-eu"),
    ("크다", PRESENT, "커요", "으 irregular: 크 → ㅋ + 어요 → 커요.", "irr-eu"),
    ("바쁘다", PRESENT, "바빠요", "으 irregular: drop 으, then look at the vowel BEFORE it. 바 has ㅏ → 아요. 바빠요.", "irr-eu"),
    ("아프다", PRESENT, "아파요", "으 irregular: the preceding vowel is ㅏ → 아요. 아파요.", "irr-eu"),
    ("예쁘다", PRESENT, "예뻐요", "으 irregular: the preceding vowel is ㅖ, not ㅏ/ㅗ → 어요. 예뻐요.", "irr-eu"),
    ("슬프다", PRESENT, "슬퍼요", "으 irregular: the preceding vowel is ㅡ, not ㅏ/ㅗ → 어요. 슬퍼요.", "irr-eu"),

    # --- ㅎ irregular ---
    ("그렇다", PRESENT, "그래요", "ㅎ irregular: the ㅎ drops and the vowel becomes ㅐ. 그렇 → 그래요.", "irr-h"),
    ("어떻다", PRESENT, "어때요", "ㅎ irregular: 어떻 → 어때요. This is where 어때요? comes from.", "irr-h"),
    ("빨갛다", PRESENT, "빨개요", "ㅎ irregular: 빨갛 → 빨개요. Nearly all colour adjectives do this.", "irr-h"),
    ("하얗다", PRESENT, "하얘요", "ㅎ irregular: 하얗 → 하얘요.", "irr-h"),
    ("좋다", PAST, "좋았어요", "TRAP: 좋다 is REGULAR. It is the one common ㅎ-final word that does not change.", "irr-h"),
    ("넣다", PRESENT, "넣어요", "TRAP: 넣다 is REGULAR despite the ㅎ.", "irr-h"),

    # --- Past tense: derived from the 해요 form, not learned separately ---
    ("먹어요", PAST, "먹었어요", "Past = take the 해요 form, drop 요, add ㅆ어요. 먹어 + ㅆ어요 → 먹었어요.", "past"),
    ("가요", PAST, "갔어요", "가 + ㅆ어요 → 갔어요. The same one rule, applied to a contracted stem.", "past"),
    ("해요", PAST, "했어요", "해 + ㅆ어요 → 했어요.", "past"),
    ("와요", PAST, "왔어요", "와 + ㅆ어요 → 왔어요.", "past"),
    ("추워요", PAST, "추웠어요", "추워 + ㅆ어요 → 추웠어요. Irregulars need no separate past rule.", "past"),
    ("몰라요", PAST, "몰랐어요", "몰라 + ㅆ어요 → 몰랐어요.", "past"),
    ("마셔요", PAST, "마셨어요", "마셔 + ㅆ어요 → 마셨어요.", "past"),
]


def main():
    b = Build("05_conjugation", "Korean v2::05 Conjugation (rules)")
    model = transform_model()

    for prompt, task, answer, rule, tag in ITEMS:
        b.add(model, [prompt, task, answer, rule, b.audio(answer)], tags=["conjugation", tag])

    b.write()


if __name__ == "__main__":
    main()
