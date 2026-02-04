#!/usr/bin/env python3
"""
Korean Hangul Syllable Practice Deck

Practices reading complete syllables (consonant + vowel combinations).
Prerequisites: Hangul Alphabet deck
Usage: python3 korean_syllables.py
"""

import sys
import os
import tempfile
import shutil

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import (
    generate_audio, created_audio_files, DECK_IDS, MODEL_IDS
)

# Deck info
DECK_ID = DECK_IDS["syllables"]
MODEL_ID = MODEL_IDS["word"]


# Syllable data: (korean, romanization, breakdown, examples)
SYLLABLES = [
    # Simple CV syllables (consonant + a-vowel)
    ("가", "ga", "ㄱ + ㅏ", "가다 (to go)"),
    ("나", "na", "ㄴ + ㅏ", "나라 (country)"),
    ("다", "da", "ㄷ + ㅏ", "다리 (leg)"),
    ("라", "ra", "ㄹ + ㅏ", "라디오 (radio)"),
    ("마", "ma", "ㅁ + ㅏ", "마리 (head/counter)"),
    ("바", "ba", "ㅂ + ㅏ", "바나나 (banana)"),
    ("사", "sa", "ㅅ + ㅏ", "사과 (apple)"),
    ("자", "ja", "ㅈ + ㅏ", "자전거 (bicycle)"),
    ("카", "ka", "ㅋ + ㅏ", "카메라 (camera)"),
    ("타", "ta", "ㅌ + ㅏ", "타다 (to ride)"),
    ("파", "pa", "ㅍ + ㅏ", "파란 (blue)"),
    ("하", "ha", "ㅎ + ㅏ", "하나 (one)"),

    # Simple CV syllables with other vowels
    ("거", "geo", "ㄱ + ㅓ", "거기 (there)"),
    ("너", "neo", "ㄴ + ㅓ", "너 (you)"),
    ("더", "deo", "ㄷ + ㅓ", "더 (more)"),
    ("러", "reo", "ㄹ + ㅓ", "러서 (because)"),
    ("머", "meo", "ㅁ + ㅓ", "머리 (head)"),
    ("버", "beo", "ㅂ + ㅓ", "버스 (bus)"),
    ("서", "seo", "ㅅ + ㅓ", "서울 (Seoul)"),
    ("저", "jeo", "ㅈ + ㅓ", "저 (me/humble)"),
    ("처", "cheo", "ㅊ + ㅓ", "처음 (first)"),
    ("커", "keo", "ㅋ + ㅓ", "커피 (coffee)"),
    ("터", "teo", "ㅌ + ㅓ", "터미널 (terminal)"),
    ("퍼", "peo", "ㅍ + ㅓ", "퍼센트 (percent)"),
    ("허", "heo", "ㅎ + ㅓ", "허리 (waist)"),

    ("고", "go", "ㄱ + ㅗ", "고양이 (cat)"),
    ("노", "no", "ㄴ + ㅗ", "노래 (song)"),
    ("도", "do", "ㄷ + ㅗ", "도서관 (library)"),
    ("로", "ro", "ㄹ + ㅗ", "로봇 (robot)"),
    ("모", "mo", "ㅁ + ㅗ", "목 (neck)"),
    ("보", "bo", "ㅂ + ㅗ", "보다 (to see)"),
    ("소", "so", "ㅅ + ㅗ", "소리 (sound)"),
    ("조", "jo", "ㅈ + ㅗ", "조금 (a little)"),
    ("초", "cho", "ㅊ + ㅗ", "초콜릿 (chocolate)"),
    ("코", "ko", "ㅋ + ㅗ", "코 (nose)"),
    ("토", "to", "ㅌ + ㅗ", "토요일 (Saturday)"),
    ("포", "po", "ㅍ + ㅗ", "포도 (grape)"),
    ("호", "ho", "ㅎ + ㅗ", "호텔 (hotel)"),

    ("구", "gu", "ㄱ + ㅜ", "구름 (cloud)"),
    ("누", "nu", "ㄴ + ㅜ", "누구 (who)"),
    ("두", "du", "ㄷ + ㅜ", "두 (two)"),
    ("루", "ru", "ㄹ + ㅜ", "루트 (route)"),
    ("무", "mu", "ㅁ + ㅜ", "무 (radish)"),
    ("부", "bu", "ㅂ + ㅜ", "부엌 (kitchen)"),
    ("수", "su", "ㅅ + ㅜ", "수 (water/number)"),
    ("주", "ju", "ㅈ + ㅜ", "주다 (to give)"),
    ("추", "chu", "ㅊ + ㅜ", "추운 (cold)"),
    ("쿠", "ku", "ㅋ + ㅜ", "쿠키 (cookie)"),
    ("투", "tu", "ㅌ + ㅜ", "투자 (investment)"),
    ("푸", "pu", "ㅍ + ㅜ", "푸른 (blue/green)"),
    ("후", "hu", "ㅎ + ㅜ", "후 (after)"),

    # With ㅡ (eu)
    ("그", "geu", "ㄱ + ㅡ", "그 (he/it)"),
    ("느", "neu", "ㄴ + ㅡ", "느리다 (slow)"),
    ("드", "deu", "ㄷ + ㅡ", "드르륵 (sound)"),
    ("르", "reu", "ㄹ + ㅡ", "르르 (sound)"),
    ("므", "meu", "ㅁ + ㅡ", "믿다 (to believe)"),
    ("브", "beu", "ㅂ + ㅡ", "브랜드 (brand)"),
    ("스", "seu", "ㅅ + ㅡ", "스우 (sweater)"),
    ("즐", "jeul", "ㅈ + ㅡ", "즐겁다 (enjoyable)"),
    ("츠", "cheu", "ㅊ + ㅡ", "츨업 (graduation)"),
    ("크", "keu", "ㅋ + ㅡ", "크다 (big)"),
    ("트", "teu", "ㅌ + ㅡ", "트다 (to open)"),
    ("프", "peu", "ㅍ + ㅡ", "프랑스 (France)"),
    ("흐", "heu", "ㅎ + ㅡ", "흐르다 (to flow)"),

    # With ㅣ (i)
    ("기", "gi", "ㄱ + ㅣ", "기타 (guitar)"),
    ("니", "ni", "ㄴ + ㅣ", "니 (you)"),
    ("디", "di", "ㄷ + ㅣ", "디지털 (digital)"),
    ("리", "ri", "ㄹ + ㅣ", "리 (benefit)"),
    ("미", "mi", "ㅁ + ㅣ", "미다 (to peel)"),
    ("비", "bi", "ㅂ + ㅣ", "비 (rain)"),
    ("시", "si", "ㅅ + ㅣ", "시간 (time)"),
    ("지", "ji", "ㅈ + ㅣ", "지도 (map)"),
    ("치", "chi", "ㅊ + ㅣ", "치마 (skirt)"),
    ("키", "ki", "ㅋ + ㅣ", "키 (height/key)"),
    ("티", "ti", "ㅌ + ㅣ", "티 (tea)"),
    ("피", "pi", "ㅍ + ㅣ", "피 (blood)"),
    ("히", "hi", "ㅎ + ㅣ", "히 (HE)"),

    # Y-vowels
    ("갸", "gya", "ㄱ + ㅑ", "갸륵 (sound)"),
    ("냐", "nya", "ㄴ + ㅑ", "냐 (meow)"),
    ("댜", "dya", "ㄷ + ㅑ", "댜 (rare)"),
    ("먀", "mya", "ㅁ + ㅑ", "먀오 (meow)"),
    ("뱌", "bya", "ㅂ + ㅑ", "뱌 (rare)"),
    ("샤", "sya", "ㅅ + ㅑ", "샤워 (shower)"),
    ("자", "ja", "ㅈ + ㅑ", "자 (already)"),
    ("차", "cha", "ㅊ + ㅑ", "차 (car/tea)"),
    ("커", "kya", "ㅋ + ㅑ", "커 (rare)"),
    ("탸", "tya", "ㅌ + ㅑ", "탸 (rare)"),
    ("퍄", "pya", "ㅍ + ㅑ", "퍄 (rare)"),
    ("햐", "hya", "ㅎ + ㅑ", "햐 (rare)"),

    ("겨", "gyeo", "ㄱ + ㅕ", "겨울 (winter)"),
    ("녀", "nyeo", "ㄴ + ㅕ", "녀석 (fellow)"),
    ("뎌", "dyeo", "ㄷ + ㅕ", "뎌 (rare)"),
    ("려", "ryeo", "ㄹ + ㅕ", "여행 (travel) - 여 originally 려"),
    ("며", "myeo", "ㅁ + ㅕ", "며칠 (few days)"),
    ("벼", "byeo", "ㅂ + ㅕ", "벼 (rice plant)"),
    ("셔", "syeo", "ㅅ + ㅕ", "셔 (rare)"),
    ("져", "jyeo", "ㅈ + ㅕ", "저차 (already)"),
    ("쳐", "chyeo", "ㅊ + ㅕ", "쳐 (rare)"),
    ("켜", "kyeo", "ㅋ + ㅕ", "켜다 (to turn on)"),
    ("텨", "tyeo", "ㅌ + ㅕ", "텨 (rare)"),
    ("펴", "pyeo", "ㅍ + ㅕ", "펴다 (to spread)"),
    ("혀", "hyeo", "ㅎ + ㅕ", "혀 (tongue)"),

    # W-vowels
    ("과", "gwa", "ㄱ + ㅘ", "과일 (fruit)"),
    ("놔", "nwa", "ㄴ + ㅘ", "놔 (rare)"),
    ("돠", "dwa", "ㄷ + ㅘ", "돼지 (pig) - 돠 originally 돼"),
    ("롸", "rwa", "ㄹ + ㅘ", "롸 (rare)"),
    ("뫼", "mwa", "ㅁ + ㅘ", "뫼 (mountain)"),
    ("뵈", "bwa", "ㅂ + ㅘ", "뵙다 (to meet respectfully)"),
    ("솨", "swa", "ㅅ + ㅘ", "솨 (rare)"),
    ("좌", "jwa", "ㅈ + ㅘ", "좌석 (seat)"),
    ("콰", "kwa", "ㅋ + ㅘ", "콰 (rare)"),
    ("톼", "twa", "ㅌ + ㅘ", "톼 (rare)"),
    ("퐈", "pwa", "ㅍ + ㅘ", "퐈 (rare)"),
    ("화", "hwa", "ㅎ + ㅘ", "화가 (anger)"),

    # Common syllables with batchim (final consonant)
    ("한", "han", "ㅎ + ㅏ + ㄴ", "한국 (Korea)"),
    ("국", "guk", "ㄱ + ㅜ + ㄱ", "국가 (nation)"),
    ("문", "mun", "ㅁ + ㅜ + ㄴ", "문 (door)"),
    ("눈", "nun", "ㄴ + ㅜ + ㄴ", "눈 (eye)"),
    ("입", "ip", "ㅇ + ㅣ + ㅂ", "입 (mouth)"),
    ("식", "sik", "ㅅ + ㅣ + ㄱ", "식사 (meal)"),
    ("것", "geot", "ㄱ + ㅓ + ㅅ", "것 (thing)"),
    ("잘", "jal", "ㅈ + ㅏ + ㄹ", "잘 (well)"),
    ("을", "eul", "ㅇ + ㅡ + ㄹ", "을 (object)"),
    ("을", "eul", "ㅇ + ㅡ + ㄹ", "을 (object)"),
    ("음", "eum", "ㅇ + ㅡ + ㅁ", "음 (sound)"),
    ("운", "un", "ㅇ + ㅜ + ㄴ", "운 (luck)"),
    ("님", "nim", "ㄴ + ㅣ + ㅁ", "님 (honorific)"),
    ("집", "jip", "ㅈ + ㅣ + ㅂ", "집 (house)"),
    ("길", "gil", "ㄱ + ㅣ + ㄹ", "길 (road)"),
    ("물", "mul", "ㅁ + ㅜ + ㄹ", "물 (water)"),
    ("힘", "him", "ㅎ + ㅣ + ㅁ", "힘 (strength)"),
    ("날", "nal", "ㄴ + ㅏ + ㄹ", "날 (day/sky)"),
    ("살", "sal", "ㅅ + ㅏ + ㄹ", "살 (flesh/living)"),
    ("말", "mal", "ㅁ + ㅏ + ㄹ", "말 (word/horse)"),
    ("음", "eum", "ㅇ + ㅡ + ㅁ", "음악 (music)"),

    # Double consonants
    ("까", "kka", "ㄲ + ㅏ", "까맣다 (black)"),
    ("따", "tta", "ㄸ + ㅏ", "따다 (to pick)"),
    ("빠", "ppa", "ㅃ + ㅏ", "빠르다 (fast)"),
    ("싸", "ssa", "ㅆ + ㅏ", "싸다 (cheap)"),
    ("짜", "jja", "ㅉ + ㅏ", "짜다 (salty)"),

    ("꺄", "kkya", "ㄲ + ㅑ", "꺄야 (cute sound)"),
    ("또", "tto", "ㄸ + ㅗ", "또 (again)"),
    ("뽀", "ppo", "ㅃ + ㅗ", "뽀로로 (Pororo)"),
    ("쪼", "jjo", "ㅉ + ㅗ", "쪼개다 (to split)"),
]


def create_model():
    """Create card model for syllables."""
    return genanki.Model(
        MODEL_ID,
        "Korean Syllable Model",
        fields=[
            {"name": "Korean"},
            {"name": "Romanization"},
            {"name": "Breakdown"},
            {"name": "Example"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Syllable Card",
                "qfmt": """
<div style="text-align: center; font-size: 100px; padding: 60px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 100px; padding: 40px;">
    {{Korean}}
</div>
<div style="text-align: center; padding: 20px;">
    {{Audio}}
</div>
<hr style="margin: 20px 0;">
<div style="text-align: center; font-size: 36px; color: #2196F3; font-weight: bold; padding: 15px;">
    {{Romanization}}
</div>
<div style="text-align: center; font-size: 20px; color: #666; padding: 10px;">
    {{Breakdown}}
</div>
{{#Example}}
<div style="text-align: center; font-size: 22px; padding: 15px; margin: 15px auto; max-width: 500px; background: #f5f5f5; border-radius: 8px;">
    <strong>Example:</strong> {{Example}}
</div>
{{/Example}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
}
        """,
    )


def generate_deck(output_file="decks/02_korean_syllables.apkg"):
    """Generate the syllable practice deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "02. Korean Syllables - 음절 연습")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for korean, roman, breakdown, example in SYLLABLES:
            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[korean, roman, breakdown, example, audio_field],
            )
            deck.add_note(note)

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(SYLLABLES)} syllable cards")
        print(f"  - {len(created_audio_files)} audio files")
        print("\nImport this file into Anki: File → Import...")

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(audio_dir)
        except:
            pass


if __name__ == "__main__":
    generate_deck()
