#!/usr/bin/env python3
"""
Korean Hangul Anki Deck Generator with Audio

Creates Anki decks for Korean consonants and vowels with pronunciation audio.
Usage: python3 korean_hangul.py
"""

import genanki
import os
import tempfile
import shutil
from pathlib import Path

# Deck and Model IDs (arbitrary unique numbers)
DECK_ID = 1837523948
MODEL_ID = 1482931024  # Changed because we added a field

# Global to store audio files for cleanup
created_audio_files = []


class KoreanCard:
    """Represents a single Korean alphabet card."""

    def __init__(self, korean_char, pronunciation, description="", examples="", audio_word=""):
        self.korean_char = korean_char
        self.pronunciation = pronunciation
        self.description = description
        self.examples = examples
        self.audio_word = audio_word  # Full syllable for TTS

    def to_note(self, model, audio_dir):
        """Convert to genanki Note with audio file."""
        audio_filename = None

        if self.audio_word:
            from gtts import gTTS
            tts = gTTS(text=self.audio_word, lang='ko')
            audio_filename = f"{self.audio_word}.mp3"
            audio_path = os.path.join(audio_dir, audio_filename)
            tts.save(audio_path)
            created_audio_files.append(audio_path)

        # Format audio field for Anki - just the filename
        audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

        return genanki.Note(
            model=model,
            fields=[
                self.korean_char,
                self.pronunciation,
                self.description,
                self.examples,
                audio_field,
            ],
        )


# Korean Consonants (Ja-eum) - combined with vowel for audio
CONSONANTS = [
    # Basic consonants
    KoreanCard("ㄱ", "g/k", "giyeok - soft 'g' as in 'goat', 'k' at end of syllable", "가 (ga), 악 (ak)", "가"),
    KoreanCard("ㄴ", "n", "nieun - 'n' as in 'no'", "나 (na), 안 (an)", "나"),
    KoreanCard("ㄷ", "d/t", "digeut - soft 'd' as in 'day', 't' at end of syllable", "다 (da), 앋 (at)", "다"),
    KoreanCard("ㄹ", "r/l", "rieul - flap 'r' between vowels, 'l' at end of syllable", "라 (ra), 알 (al)", "라"),
    KoreanCard("ㅁ", "m", "mieum - 'm' as in 'mother'", "마 (ma), 암 (am)", "마"),
    KoreanCard("ㅂ", "b/p", "bieup - soft 'b' as in 'boy', 'p' at end of syllable", "바 (ba), 압 (ap)", "바"),
    KoreanCard("ㅅ", "s/sh", "siot - 's' as in 'see', 'sh' before i/y", "사 (sa), 앗 (at)", "사"),
    KoreanCard("ㅇ", "ng/-", "ieung - silent at start, 'ng' at end of syllable", "아 (a), 앙 (ang)", "아"),
    KoreanCard("ㅈ", "j/ch", "jieut - 'j' as in 'jam', 'ch' at end of syllable", "자 (ja)", "자"),
    KoreanCard("ㅊ", "ch", "chieut - 'ch' as in 'church'", "차 (cha)", "차"),
    KoreanCard("ㅋ", "k", "kieuk - strong 'k' as in 'kite'", "카 (ka)", "카"),
    KoreanCard("ㅌ", "t", "tieut - strong 't' as in 'top'", "타 (ta)", "타"),
    KoreanCard("ㅍ", "p", "pieup - strong 'p' as in 'pop'", "파 (pa)", "파"),
    KoreanCard("ㅎ", "h", "hieut - 'h' as in 'house'", "하 (ha)", "하"),

    # Double (tense) consonants
    KoreanCard("ㄲ", "kk", "ssanggiyeok - tense 'gg', held longer", "까 (kka)", "까"),
    KoreanCard("ㄸ", "tt", "ssangdigeut - tense 'dd'", "따 (tta)", "따"),
    KoreanCard("ㅃ", "pp", "ssangbieup - tense 'bb'", "빠 (ppa)", "빠"),
    KoreanCard("ㅆ", "ss", "ssangsiot - tense 'ss'", "싸 (ssa)", "싸"),
    KoreanCard("ㅉ", "jj", "ssangjieut - tense 'jj'", "짜 (jja)", "짜"),
]

# Korean Vowels (Mo-eum) - combined with ㅇ for audio
VOWELS = [
    # Basic vowels
    KoreanCard("ㅏ", "a", "a - like 'a' in 'father'", "아 (a), 가 (ga)", "아"),
    KoreanCard("ㅓ", "eo", "eo - like 'u' in 'cup' or 'o' in 'song'", "어 (eo), 거 (geo)", "어"),
    KoreanCard("ㅗ", "o", "o - like 'o' in 'more' or 'so'", "오 (o), 고 (go)", "오"),
    KoreanCard("ㅜ", "u", "u - like 'oo' in 'moon'", "우 (u), 구 (gu)", "우"),
    KoreanCard("ㅡ", "eu", "eu - like 'oo' in 'book' but shorter, unrounded lips", "으 (eu), 그 (geu)", "으"),
    KoreanCard("ㅣ", "i", "i - like 'ee' in 'see'", "이 (i), 기 (gi)", "이"),
    KoreanCard("ㅐ", "ae", "ae - like 'e' in 'bed'", "애 (ae), 개 (gae)", "애"),
    KoreanCard("ㅔ", "e", "e - like 'e' in 'bed' (similar to ㅐ)", "에 (e), 게 (ge)", "에"),

    # Y-vowels (with y sound)
    KoreanCard("ㅑ", "ya", "ya - like 'ya' in 'yacht'", "야 (ya), 갸 (gya)", "야"),
    KoreanCard("ㅕ", "yeo", "yeo - like 'yo' in 'yonder'", "여 (yeo), 겨 (gyeo)", "여"),
    KoreanCard("ㅛ", "yo", "yo - like 'yo' in 'yoga'", "요 (yo), 교 (gyo)", "요"),
    KoreanCard("ㅠ", "yu", "yu - like 'you' in 'you'", "유 (yu), 규 (gyu)", "유"),
    KoreanCard("ㅖ", "ye", "ye - like 'ye' in 'yes'", "예 (ye), 계 (gye)", "예"),

    # W-vowels (compound vowels)
    KoreanCard("ㅘ", "wa", "wa - like 'wa' in 'water'", "와 (wa), 과 (gwa)", "와"),
    KoreanCard("ㅙ", "wae", "wae - like 'wa' in 'wait'", "왜 (wae)", "왜"),
    KoreanCard("ㅚ", "oe/we", "oe - like 'we' in 'wedding'", "외 (oe)", "외"),
    KoreanCard("ㅝ", "weo", "weo - like 'wo' in 'wonder'", "워 (weo)", "워"),
    KoreanCard("ㅞ", "we", "we - like 'we' in 'west'", "웨 (we)", "웨"),
    KoreanCard("ㅟ", "wi", "wi - like 'wi' in 'wizard'", "위 (wi)", "위"),
    KoreanCard("ㅢ", "ui", "ui - 'ui' as in 'ruit' or 'wee'", "의 (ui)", "의"),
]


def create_model():
    """Create the Anki card model template."""
    return genanki.Model(
        MODEL_ID,
        "Korean Hangul Model",
        fields=[
            {"name": "Korean"},
            {"name": "Pronunciation"},
            {"name": "Description"},
            {"name": "Examples"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Hangul Card",
                "qfmt": """
<div style="text-align: center; font-size: 80px; padding: 50px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 80px; padding: 30px;">
    {{Korean}}
</div>
<div style="text-align: center; padding: 20px;">
    {{Audio}}
</div>
<hr style="margin: 20px 0;">
<div style="text-align: center; font-size: 40px; color: #2196F3; font-weight: bold; padding: 20px;">
    {{Pronunciation}}
</div>
<div style="text-align: center; font-size: 18px; color: #666; padding: 10px; margin: 10px auto; max-width: 500px; background: #f5f5f5; border-radius: 8px;">
    {{Description}}
</div>
{{#Examples}}
<div style="text-align: center; font-size: 22px; padding: 15px; margin-top: 20px;">
    <strong>Examples:</strong> {{Examples}}
</div>
{{/Examples}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
}
        """,
    )


def generate_deck(output_file="decks/01_korean_hangul.apkg"):
    """Generate the Anki deck with audio files and save to file."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "01. Korean Hangul - 한글")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        # Add consonants
        for card in CONSONANTS:
            deck.add_note(card.to_note(model, audio_dir))

        # Add vowels
        for card in VOWELS:
            deck.add_note(card.to_note(model, audio_dir))

        # Generate the package with media files
        package = genanki.Package(deck)

        # Add media files using the actual file paths
        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(CONSONANTS)} consonants")
        print(f"  - {len(VOWELS)} vowels")
        print(f"  - {len(CONSONANTS) + len(VOWELS)} total cards")
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
