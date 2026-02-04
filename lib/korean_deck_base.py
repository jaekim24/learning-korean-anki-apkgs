#!/usr/bin/env python3
"""
Shared library for Korean Anki deck generation.
Provides common utilities, card classes, and templates.
"""

import genanki
import os
import tempfile
import shutil
from typing import List, Optional, Tuple, Dict, Any
from gtts import gTTS


# =============================================================================
# COLOR PALETTE FOR WORD ALIGNMENT
# =============================================================================
ALIGNMENT_COLORS = [
    "#E53935",  # red
    "#1E88E5",  # blue
    "#43A047",  # green
    "#FB8C00",  # orange
    "#8E24AA",  # purple
    "#00ACC1",  # cyan
]


def create_colored_html(word_pairs: List[Tuple[str, str]]) -> Tuple[str, str]:
    """
    Generate color-coded HTML from word pairs.

    Args:
        word_pairs: List of (korean_word, english_word) tuples

    Returns:
        Tuple of (korean_html, english_html) with color-coded spans

    Example:
        >>> create_colored_html([("저는", "I"), ("학생이에요", "am a student")])
        ('<span style="color:#E53935">저는</span> <span style="color:#1E88E5">학생이에요</span>',
         '<span style="color:#E53935">I</span> <span style="color:#1E88E5">am a student</span>')
    """
    korean_html_parts = []
    english_html_parts = []

    for i, (kr, en) in enumerate(word_pairs):
        color = ALIGNMENT_COLORS[i % len(ALIGNMENT_COLORS)]
        korean_html_parts.append(f'<span style="color:{color}">{kr}</span>')
        english_html_parts.append(f'<span style="color:{color}">{en}</span>')

    return " ".join(korean_html_parts), " ".join(english_html_parts)


# Model ID registry to avoid conflicts
MODEL_IDS = {
    "hangul": 1482931024,
    "word": 1482931025,
    "word_colored": 1482931025,  # Same ID for compatibility
    "sentence": 1482931026,
    "grammar": 1482931027,
    "conversation": 1482931028,
    "hangul_extended": 1482931029,
    "syllables": 1482931030,
    "numbers": 1482931031,
    "time": 1482931032,
    "particles": 1482931033,
    "verbs": 1482931034,
    "honorifics": 1482931035,
    "idioms": 1482931036,
}

# Deck ID registry
DECK_IDS = {
    "consonants_vowels": 1837523962,
    "hangul": 1837523948,
    "syllables": 1837523949,
    "numbers": 1837523950,
    "vocab_1": 1837523951,
    "time": 1837523952,
    "particles": 1837523953,
    "verbs_present": 1837523954,
    "verbs_tenses": 1837523955,
    "sentences_1": 1837523956,
    "honorifics": 1832933957,
    "vocab_2": 1837523958,
    "grammar_intermediate": 1837523959,
    "idioms": 1837523960,
    "conversation_1": 1837523961,
}

# Global to store audio files for cleanup
created_audio_files = []


class KoreanCard:
    """Base class for a Korean Anki card."""

    def __init__(
        self,
        front: str,
        back: str,
        audio_text: Optional[str] = None,
        notes: str = "",
        extra: str = "",
    ):
        self.front = front
        self.back = back
        self.audio_text = audio_text
        self.notes = notes
        self.extra = extra


class KoreanWordCard(KoreanCard):
    """Card for learning Korean vocabulary words."""

    def __init__(
        self,
        korean: str,
        english: str,
        romanization: str = "",
        example: str = "",
        example_translation: str = "",
        audio_text: Optional[str] = None,
        word_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        super().__init__(korean, english, audio_text)
        self.korean = korean
        self.english = english
        self.romanization = romanization
        self.example = example
        self.example_translation = example_translation
        self.word_pairs = word_pairs or []
        # Use Korean word for audio if not specified
        if audio_text is None:
            self.audio_text = korean

    def get_colored_html(self) -> Tuple[str, str]:
        """Generate color-aligned HTML for word pairs."""
        if self.word_pairs:
            return create_colored_html(self.word_pairs)
        return "", ""


class KoreanSentenceCard(KoreanCard):
    """Card for learning Korean sentences."""

    def __init__(
        self,
        korean: str,
        english: str,
        breakdown: str = "",
        audio_text: Optional[str] = None,
        word_pairs: Optional[List[Tuple[str, str]]] = None,
    ):
        super().__init__(korean, english, audio_text)
        self.korean = korean
        self.english = english
        self.breakdown = breakdown
        self.word_pairs = word_pairs or []
        # Use full sentence for audio if not specified
        if audio_text is None:
            self.audio_text = korean

    def get_colored_html(self) -> Tuple[str, str]:
        """Generate color-aligned HTML for word pairs."""
        if self.word_pairs:
            return create_colored_html(self.word_pairs)
        return "", ""


def generate_audio(text: str, audio_dir: str) -> Optional[str]:
    """Generate TTS audio file for Korean text."""
    if not text:
        return None

    try:
        tts = gTTS(text=text, lang='ko')
        # Use a hash of the text to avoid duplicates
        import hashlib
        text_hash = hashlib.md5(text.encode('utf-8')).hexdigest()[:8]
        audio_filename = f"audio_{text_hash}.mp3"
        audio_path = os.path.join(audio_dir, audio_filename)

        # Only create if doesn't exist
        if not os.path.exists(audio_path):
            tts.save(audio_path)
            created_audio_files.append(audio_path)

        return audio_filename
    except Exception as e:
        print(f"Warning: Could not generate audio for '{text}': {e}")
        return None


def create_word_model() -> genanki.Model:
    """Create card model for vocabulary words."""
    return genanki.Model(
        MODEL_IDS["word"],
        "Korean Word Model",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Romanization"},
            {"name": "Example"},
            {"name": "ExampleTranslation"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Word Card",
                "qfmt": """
<div style="text-align: center; font-size: 60px; padding: 40px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 60px; padding: 20px;">
    {{Korean}}
</div>
<div style="text-align: center; padding: 15px;">
    {{Audio}}
</div>
{{#Romanization}}
<div style="text-align: center; font-size: 24px; color: #666; padding: 10px;">
    <em>{{Romanization}}</em>
</div>
{{/Romanization}}
<hr style="margin: 15px 0;">
<div style="text-align: center; font-size: 32px; color: #2196F3; font-weight: bold; padding: 10px;">
    {{English}}
</div>
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 600px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 24px; padding: 10px; line-height: 1.8;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{#Example}}
{{^KoreanColored}}
<div style="text-align: center; font-size: 18px; color: #444; padding: 15px; margin: 10px auto; max-width: 600px; background: #f9f9f9; border-radius: 8px;">
    <strong>Example:</strong> {{Example}}
    {{#ExampleTranslation}}
    <br><em style="color: #666;">{{ExampleTranslation}}</em>
    {{/ExampleTranslation}}
</div>
{{/KoreanColored}}
{{/Example}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    line-height: 1.6;
}
        """,
    )


def create_sentence_model() -> genanki.Model:
    """Create card model for sentences."""
    return genanki.Model(
        MODEL_IDS["sentence"],
        "Korean Sentence Model",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Breakdown"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Sentence Card",
                "qfmt": """
<div style="text-align: center; font-size: 40px; padding: 30px;">
    {{English}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 40px; padding: 20px;">
    {{English}}
</div>
<div style="text-align: center; padding: 15px;">
    {{Audio}}
</div>
<hr style="margin: 15px 0;">
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 700px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 28px; padding: 10px; line-height: 1.8; color: #2c3e50; font-weight: 600;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 20px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{^KoreanColored}}
<div style="text-align: center; font-size: 36px; color: #2196F3; font-weight: bold; padding: 15px;">
    {{Korean}}
</div>
{{#Breakdown}}
<div style="text-align: center; font-size: 16px; color: #666; padding: 10px; margin: 10px auto; max-width: 600px; background: #f5f5f5; border-radius: 8px;">
    {{Breakdown}}
</div>
{{/Breakdown}}
{{/KoreanColored}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    line-height: 1.6;
}
        """,
    )


def create_grammar_model() -> genanki.Model:
    """Create card model for grammar patterns."""
    return genanki.Model(
        MODEL_IDS["grammar"],
        "Korean Grammar Model",
        fields=[
            {"name": "Pattern"},
            {"name": "Usage"},
            {"name": "Examples"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Grammar Card",
                "qfmt": """
<div style="text-align: center; font-size: 40px; padding: 30px;">
    {{Pattern}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 40px; padding: 20px;">
    {{Pattern}}
</div>
<div style="text-align: center; padding: 15px;">
    {{Audio}}
</div>
<hr style="margin: 15px 0;">
<div style="text-align: center; font-size: 18px; padding: 15px; margin: 15px auto; max-width: 600px; background: #f5f5f5; border-radius: 8px;">
    {{Usage}}
</div>
{{#Examples}}
<div style="text-align: center; font-size: 20px; padding: 15px; margin-top: 15px;">
    <strong>Examples:</strong><br>{{Examples}}
</div>
{{/Examples}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    line-height: 1.8;
}
        """,
    )


def create_conversation_model() -> genanki.Model:
    """Create card model for conversation/dialogue practice."""
    return genanki.Model(
        MODEL_IDS["conversation"],
        "Korean Conversation Model",
        fields=[
            {"name": "Prompt"},
            {"name": "Response"},
            {"name": "Context"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Conversation Card",
                "qfmt": """
<div style="text-align: center; padding: 30px;">
{{#Context}}
<div style="font-size: 16px; color: #666; margin-bottom: 20px;">
    <em>Context: {{Context}}</em>
</div>
{{/Context}}
<div style="font-size: 32px;">
    {{Prompt}}
</div>
</div>
                """,
                "afmt": """
<div style="text-align: center; padding: 30px;">
{{#Context}}
<div style="font-size: 16px; color: #666; margin-bottom: 20px;">
    <em>Context: {{Context}}</em>
</div>
{{/Context}}
<div style="font-size: 28px; color: #2196F3; font-weight: bold; margin-bottom: 15px;">
    {{Prompt}}
</div>
<div style="padding: 15px;">
    {{Audio}}
</div>
<div style="font-size: 32px; margin-top: 20px;">
    {{Response}}
</div>
</div>
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
    line-height: 1.6;
}
        """,
    )


def generate_deck(
    deck_name: str,
    deck_id: int,
    model: genanki.Model,
    cards: List[genanki.Note],
    output_file: str,
) -> None:
    """Generate an Anki deck with media files."""
    global created_audio_files
    created_audio_files.clear()

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        deck = genanki.Deck(deck_id, deck_name)
        for card in cards:
            deck.add_note(card)

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(cards)} cards")
        print(f"  - {len(created_audio_files)} audio files")
        print()

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(audio_dir)
        except:
            pass


def add_word_note(deck, model, card: KoreanWordCard, audio_dir: str) -> genanki.Note:
    """Create a word note with optional audio and colored word alignment."""
    audio_filename = generate_audio(card.audio_text, audio_dir)
    audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

    korean_colored, english_colored = card.get_colored_html()

    return genanki.Note(
        model=model,
        fields=[
            card.korean,
            card.english,
            card.romanization,
            card.example,
            card.example_translation,
            korean_colored,
            english_colored,
            audio_field,
        ],
    )


def add_sentence_note(deck, model, card: KoreanSentenceCard, audio_dir: str) -> genanki.Note:
    """Create a sentence note with optional audio and colored word alignment."""
    audio_filename = generate_audio(card.audio_text, audio_dir)
    audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

    korean_colored, english_colored = card.get_colored_html()

    return genanki.Note(
        model=model,
        fields=[
            card.korean,
            card.english,
            card.breakdown,
            korean_colored,
            english_colored,
            audio_field,
        ],
    )
