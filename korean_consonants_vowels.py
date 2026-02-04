#!/usr/bin/env python3
"""
Korean Consonants & Vowels Identification Anki Deck Generator

Creates Anki decks for practicing identification of Korean consonants and vowels.
Usage: python3 korean_consonants_vowels.py
"""

import genanki
import os
import tempfile
import shutil

# Deck and Model IDs
DECK_ID = 1837523962
MODEL_ID = 1482931037

# Global to store audio files for cleanup
created_audio_files = []


class IdentificationCard:
    """Represents a consonant or vowel identification card."""

    def __init__(self, character, type_name, name, pronunciation, description, audio_word=""):
        self.character = character
        self.type_name = type_name  # "Consonant" or "Vowel"
        self.name = name
        self.pronunciation = pronunciation
        self.description = description
        self.audio_word = audio_word

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

        audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

        return genanki.Note(
            model=model,
            fields=[
                self.character,
                self.type_name,
                self.name,
                self.pronunciation,
                self.description,
                audio_field,
            ],
        )


# Basic Consonants (Ja-eum)
BASIC_CONSONANTS = [
    IdentificationCard("ㄱ", "Consonant", "Giyeok (기역)", "g/k", "Basic 'g' sound as in 'go', becomes 'k' at end of syllable", "가"),
    IdentificationCard("ㄴ", "Consonant", "Nieun (니은)", "n", "'n' sound as in 'no'", "나"),
    IdentificationCard("ㄷ", "Consonant", "Digeut (디귿)", "d/t", "Basic 'd' sound as in 'day', becomes 't' at end of syllable", "다"),
    IdentificationCard("ㄹ", "Consonant", "Rieul (리을)", "r/l", "Flap 'r' between vowels, 'l' at end of syllable", "라"),
    IdentificationCard("ㅁ", "Consonant", "Mieum (미음)", "m", "'m' sound as in 'mother'", "마"),
    IdentificationCard("ㅂ", "Consonant", "Bieup (비읍)", "b/p", "Basic 'b' sound as in 'boy', becomes 'p' at end of syllable", "바"),
    IdentificationCard("ㅅ", "Consonant", "Siot (시옷)", "s/sh", "'s' sound as in 'see', 'sh' before i/y", "사"),
    IdentificationCard("ㅇ", "Consonant", "Ieung (이응)", "ng/-", "Silent at start, 'ng' at end of syllable", "아"),
    IdentificationCard("ㅈ", "Consonant", "Jieut (지읒)", "j/ch", "'j' sound as in 'jam', becomes 'ch' at end", "자"),
    IdentificationCard("ㅊ", "Consonant", "Chieut (치읓)", "ch", "'ch' sound as in 'church'", "차"),
    IdentificationCard("ㅋ", "Consonant", "Kieuk (키읔)", "k", "Strong 'k' as in 'kite'", "카"),
    IdentificationCard("ㅌ", "Consonant", "Tieut (티읕)", "t", "Strong 't' as in 'top'", "타"),
    IdentificationCard("ㅍ", "Consonant", "Pieup (피읖)", "p", "Strong 'p' as in 'pop'", "파"),
    IdentificationCard("ㅎ", "Consonant", "Hieut (히읗)", "h", "'h' sound as in 'house'", "하"),
]

# Double (Tense) Consonants
DOUBLE_CONSONANTS = [
    IdentificationCard("ㄲ", "Consonant", "Ssanggiyeok (쌍기역)", "kk", "Tense 'gg', held longer with more emphasis", "까"),
    IdentificationCard("ㄸ", "Consonant", "Ssangdigeut (쌍디귿)", "tt", "Tense 'dd', held longer with more emphasis", "따"),
    IdentificationCard("ㅃ", "Consonant", "Ssangbieup (쌍비읍)", "pp", "Tense 'bb', held longer with more emphasis", "빠"),
    IdentificationCard("ㅆ", "Consonant", "Ssangsiot (쌍시옷)", "ss", "Tense 'ss', held longer with more emphasis", "싸"),
    IdentificationCard("ㅉ", "Consonant", "Ssangjieut (쌍지읒)", "jj", "Tense 'jj', held longer with more emphasis", "짜"),
]

# Basic Vowels (Mo-eum)
BASIC_VOWELS = [
    IdentificationCard("ㅏ", "Vowel", "A (아)", "a", "Like 'a' in 'father'", "아"),
    IdentificationCard("ㅓ", "Vowel", "Eo (어)", "eo", "Like 'u' in 'cup' or 'o' in 'song'", "어"),
    IdentificationCard("ㅗ", "Vowel", "O (오)", "o", "Like 'o' in 'more' or 'so'", "오"),
    IdentificationCard("ㅜ", "Vowel", "U (우)", "u", "Like 'oo' in 'moon'", "우"),
    IdentificationCard("ㅡ", "Vowel", "Eu (으)", "eu", "Like 'oo' in 'book' but shorter, unrounded lips", "으"),
    IdentificationCard("ㅣ", "Vowel", "I (이)", "i", "Like 'ee' in 'see'", "이"),
    IdentificationCard("ㅐ", "Vowel", "Ae (애)", "ae", "Like 'e' in 'bed'", "애"),
    IdentificationCard("ㅔ", "Vowel", "E (에)", "e", "Like 'e' in 'bed' (similar to ㅐ)", "에"),
]

# Y-Vowels (Vowels with y sound)
Y_VOWELS = [
    IdentificationCard("ㅑ", "Vowel", "Ya (야)", "ya", "Like 'ya' in 'yacht'", "야"),
    IdentificationCard("ㅕ", "Vowel", "Yeo (여)", "yeo", "Like 'yo' in 'yonder'", "여"),
    IdentificationCard("ㅛ", "Vowel", "Yo (요)", "yo", "Like 'yo' in 'yoga'", "요"),
    IdentificationCard("ㅠ", "Vowel", "Yu (유)", "yu", "Like 'you' in 'you'", "유"),
    IdentificationCard("ㅖ", "Vowel", "Ye (예)", "ye", "Like 'ye' in 'yes'", "예"),
]

# W-Vowels (Compound Vowels)
W_VOWELS = [
    IdentificationCard("ㅘ", "Vowel", "Wa (와)", "wa", "Like 'wa' in 'water'", "와"),
    IdentificationCard("ㅙ", "Vowel", "Wae (왜)", "wae", "Like 'wa' in 'wait'", "왜"),
    IdentificationCard("ㅚ", "Vowel", "Oe (외)", "oe", "Like 'we' in 'wedding'", "외"),
    IdentificationCard("ㅝ", "Vowel", "Weo (워)", "weo", "Like 'wo' in 'wonder'", "워"),
    IdentificationCard("ㅞ", "Vowel", "We (웨)", "we", "Like 'we' in 'west'", "웨"),
    IdentificationCard("ㅟ", "Vowel", "Wi (위)", "wi", "Like 'wi' in 'wizard'", "위"),
    IdentificationCard("ㅢ", "Vowel", "Ui (의)", "ui", "Like 'ui' as in 'ruit' or 'wee'", "의"),
]


def create_model():
    """Create the Anki card model template."""
    return genanki.Model(
        MODEL_ID,
        "Korean Consonant Vowel ID Model",
        fields=[
            {"name": "Character"},
            {"name": "Type"},
            {"name": "Name"},
            {"name": "Pronunciation"},
            {"name": "Description"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Identify Consonant/Vowel",
                "qfmt": """
<div style="text-align: center; padding: 40px;">
    <div style="font-size: 16px; color: #666; margin-bottom: 20px;">
        What is this {{Type}}?
    </div>
    <div style="font-size: 100px; padding: 30px;">
        {{Character}}
    </div>
</div>
                """,
                "afmt": """
<div style="text-align: center; padding: 30px;">
    <div style="font-size: 100px; padding: 30px; color: #2196F3;">
        {{Character}}
    </div>
    <div style="padding: 20px;">
        {{Audio}}
    </div>
    <hr style="margin: 20px 0;">
    <div style="font-size: 28px; color: #666; margin-bottom: 10px;">
        {{Type}}
    </div>
    <div style="font-size: 36px; font-weight: bold; margin-bottom: 20px;">
        {{Name}}
    </div>
    <div style="font-size: 32px; color: #2196F3; font-weight: bold; margin-bottom: 15px;">
        {{Pronunciation}}
    </div>
    <div style="font-size: 18px; color: #666; padding: 15px; margin: 15px auto; max-width: 550px; background: #f5f5f5; border-radius: 8px;">
        {{Description}}
    </div>
</div>
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
}
.consonant {
    color: #E53935;
}
.vowel {
    color: #1E88E5;
}
        """,
    )


def generate_deck(output_file="decks/00_korean_consonants_vowels.apkg"):
    """Generate the Anki deck with audio files and save to file."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "00. Korean Consonants & Vowels ID - 자음 모음 식별")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        # Add all consonants
        for card in BASIC_CONSONANTS + DOUBLE_CONSONANTS:
            deck.add_note(card.to_note(model, audio_dir))

        # Add all vowels
        for card in BASIC_VOWELS + Y_VOWELS + W_VOWELS:
            deck.add_note(card.to_note(model, audio_dir))

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        total_cards = len(BASIC_CONSONANTS) + len(DOUBLE_CONSONANTS) + len(BASIC_VOWELS) + len(Y_VOWELS) + len(W_VOWELS)
        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(BASIC_CONSONANTS)} basic consonants")
        print(f"  - {len(DOUBLE_CONSONANTS)} double consonants")
        print(f"  - {len(BASIC_VOWELS)} basic vowels")
        print(f"  - {len(Y_VOWELS)} y-vowels")
        print(f"  - {len(W_VOWELS)} w-vowels")
        print(f"  - {total_cards} total cards")
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
