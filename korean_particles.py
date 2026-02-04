#!/usr/bin/env python3
"""
Korean Grammar Particles Deck

Essential Korean grammatical particles for sentence structure.
Usage: python3 korean_particles.py
"""

import sys
import os
import tempfile
import shutil
from typing import List, Tuple, Optional

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import (
    generate_audio, created_audio_files, DECK_IDS, MODEL_IDS, create_colored_html
)

# Deck info
DECK_ID = DECK_IDS["particles"]
MODEL_ID = MODEL_IDS["grammar"]


# Particles: (name, particle, usage_rule, examples, notes, word_pairs)
# word_pairs: optional list of (korean_word, english_word) for color alignment
PARTICLES = [
    # ===== TOPIC PARTICLE =====
    ("Topic Particle", "은/는 (eun/neun)",
     "After consonants: 은 | After vowels: 는",
     "저는 학생이에요. (I am a student.)\n친구는 집에 가요. (Friend goes home.)",
     "Marks the topic of the sentence. What you're talking about.",
     [("저는", "I (topic)"), ("학생이에요", "am a student")]),

    ("Topic Particle Consonant", "은 (eun)",
     "After words ending in consonant",
     "학생은 학교에 가요. (The student goes to school.)\n책은 on the desk.",
     "Used after consonants. Example: 학생은 (the student, as topic)",
     [("학생은", "The student"), ("학교에", "to school"), ("가요", "goes")]),

    ("Topic Particle Vowel", "는 (neun)",
     "After words ending in vowel",
     "저는 한국 사람이에요. (I am Korean.)\n친구는 의사예요. (Friend is a doctor.)",
     "Used after vowels. Example: 저는 (I, as topic)",
     [("저는", "I (topic)"), ("한국", "Korean"), ("사람이에요", "am a person")]),

    # ===== SUBJECT PARTICLE =====
    ("Subject Particle", "이/가 (i/ga)",
     "After consonants: 이 | After vowels: 가",
     "고양이가 예뻐요. (The cat is pretty.)\n비가 와요. (Rain is falling.)",
     "Marks the subject/agent of the sentence.",
     [("고양이가", "The cat"), ("예뻐요", "is pretty")]),

    ("Subject Particle Consonant", "이 (i)",
     "After words ending in consonant",
     "책이 있어요. (There is a book.)\n물이 좋아요. (Water is good.)",
     "Used after consonants. Example: 책이 (book)",
     [("책이", "Book"), ("있어요", "exists/there is")]),

    ("Subject Particle Vowel", "가 (ga)",
     "After words ending in vowel",
     "사과가 맛있어요. (Apple is delicious.)\n친구가 왔어요. (Friend came.)",
     "Used after vowels. Example: 사과가 (apple)",
     [("사과가", "Apple"), ("맛있어요", "is delicious")]),

    # ===== OBJECT PARTICLE =====
    ("Object Particle", "을/를 (eul/reul)",
     "After consonants: 을 | After vowels: 를",
     "밥을 먹어요. (Eat rice.)\n물을 마셔요. (Drink water.)",
     "Marks the object of the action.",
     [("밥을", "rice"), ("먹어요", "eat")]),

    ("Object Particle Consonant", "을 (eul)",
     "After words ending in consonant",
     "책을 읽어요. (Read a book.)\n밥을 먹어요. (Eat rice.)",
     "Used after consonants. Example: 밥을 (rice)",
     [("책을", "book"), ("읽어요", "read")]),

    ("Object Particle Vowel", "를 (reul)",
     "After words ending in vowel",
     "사과를 먹어요. (Eat apple.)\n우유를 마셔요. (Drink milk.)",
     "Used after vowels. Example: 사과를 (apple)",
     [("사과를", "apple"), ("먹어요", "eat")]),

    # ===== LOCATION PARTICLES =====
    ("Location Particle (at/to)", "에 (e)",
     "Location + action verb OR destination",
     "학교에 가요. (Going to school.)\n집에 있어요. (At home.)",
     "Used with 'go', 'come', 'exist' verbs. NOT used with 'have'.",
     [("학교에", "to school"), ("가요", "go")]),

    ("Location Particle (from)", "에서 (eseo)",
     "Starting point / Where action occurs",
     "학교에서 공부해요. (Studying at school.)\n집에서 왔어요. (Came from home.)",
     "Where an action happens OR where something comes from.",
     [("학교에서", "at school"), ("공부해요", "study")]),

    ("Direction Particle (from)", "에서부터 (eseobuteo)",
     "Emphasizes starting point",
     "9시에서부터 일해요. (Working from 9 o'clock.)",
     "Emphasized form of 에서 for starting point.",
     [("9시에서부터", "From 9 o'clock"), ("일해요", "work")]),

    ("Direction Particle (to)", "까지 (kkaji)",
     "Ending point / limit",
     "집까지 걸어가요. (Walk home.)\n3시까지 기다려요. (Wait until 3.)",
     "Up to / until a point in time or place.",
     [("집까지", "Until home"), ("걸어가요", "walk")]),

    # ===== POSSESSIVE PARTICLE =====
    ("Possessive Particle", "의 (ui)",
     "Pronounced as [에] (e) most times",
     "제 집 (My house)\n친구의 책 (Friend's book)",
     "Shows possession/relationship. Often shortened with pronouns.",
     [("제", "my"), ("집", "house")]),

    ("Possessive Shortened", "제 (je) / 내 (nae)",
     "Shortened forms of 저의/나의",
     "제 친구 (My friend - humble)\n내 이름 (My name - casual)",
     "Polite: 제 (je) from 저의. Casual: 내 (nae) from 나의.",
     [("제", "my"), ("친구", "friend")]),

    # ===== AND / WITH PARTICLES =====
    ("And Particle (formal)", "와/과 (wa/gwa)",
     "After vowels: 와 | After consonants: 과",
     "빵과 우유 (Bread and milk)\n책과 펜 (Book and pen)",
     "Formal way to say 'and'. Used for nouns.",
     [("빵과", "Bread and"), ("우유", "milk")]),

    ("And Particle Casual 1", "하고 (hago)",
     "Works with any noun",
     "빵하고 우유 (Bread and milk)\n친구하고 갔어요 (Went with friend)",
     "Casual 'and'. Also means 'with someone'.",
     [("빵하고", "Bread and"), ("우유", "milk")]),

    ("And Particle Casual 2", "(이)랑 (i/rang)",
     "After consonants: 이랑 | After vowels: 랑",
     "사과랑 바나나 (Apple and banana)",
     "Very casual 'and/with'. Similar to 하고.",
     [("사과랑", "Apple and"), ("바나나", "banana")]),

    # ===== TO/FOR SOMEONE =====
    ("To/For Particle", "에게 / 한테 (ege/hante)",
     "에게: formal | 한테: casual",
     "친구에게 줬어요. (Gave to friend - formal)",
     "Direction of giving/communication.",
     [("친구에게", "to friend"), ("줬어요", "gave")]),

    ("To/For Particle (from)", "에게서 / 한테서 (egeseo/hantese)",
     "Source of receiving",
     "부모님에게서 받았어요. (Received from parents.)",
     "Where something comes from (person).",
     [("부모님에게서", "from parents"), ("받았어요", "received")]),

    # ===== COMPARISON PARTICLES =====
    ("Comparison Particle", "보다 (boda)",
     "Than",
     "한국이 일본보다 커요. (Korea is bigger than Japan.)",
     "Used for comparisons. Comes after the thing being compared.",
     [("한국이", "Korea"), ("일본보다", "than Japan"), ("커요", "is bigger")]),

    ("Like / As Particle", "처럼 (cheoreom)",
     "Like / Similar to",
     "물처럼 (Like water)\n가족처럼 (Like family)",
     "Means 'like' or 'similar to'.",
     [("물", "water"), ("처럼", "like")]),

    ("As If Particle", "같이 (gachi)",
     "Like / Together with",
     "천사 같아요. (Like an angel.)\n친구같이 (Like a friend)",
     "Means 'like' or can mean 'together'.",
     [("천사", "angel"), ("같아요", "like")]),

    # ===== ONLY PARTICLE =====
    ("Only Particle", "만 (man)",
     "Only / Just",
     "물만 주세요. (Only water please.)\n저만 가요. (Only I go.)",
     "Means 'only' or 'just'. Goes after the noun.",
     [("물만", "Only water"), ("주세요", "please give")]),

    ("Also / Too Particle", "도 (do)",
     "Also / Too",
     "저도 갈 거예요. (I will go too.)\n사과도 좋아요. (Like apples too.)",
     "Means 'also' or 'too'. Replaces particle if there is one.",
     [("저도", "I too"), ("갈 거예요", "will go")]),

    ("Even Particle", "조차 (jocha)",
     "Even",
     "친구조차 몰라요. (Even friends don't know.)",
     "Emphasized 'even'. Used in negative contexts usually.",
     [("친구조차", "Even friends"), ("몰라요", "don't know")]),

    ("Even Particle 2", "까지 (kkaji)",
     "Even / Up to",
     "아이까지 울어요. (Even the child is crying.)",
     "Can mean 'even' in some contexts.",
     [("아이까지", "Even the child"), ("울어요", "cries")]),

    # ===== SINCE / BECAUSE =====
    ("Since / Because Casual", "(이)나서 (i/naseo)",
     "Because / Since",
     "배고파서 밥을 먹어요. (Eat because hungry.)",
     "Reason clause. Note: 아/어 + 서",
     [("배고파서", "Because hungry"), ("밥을", "rice"), ("먹어요", "eat")]),

    ("Since Particle", "(으)니까 (eu/nikka)",
     "Because / Since (emphasized)",
     "배고프니까 밥을 먹어요. (Since hungry, eat.)",
     "Stronger reason than 아/어서. Often used for suggestions.",
     [("배고프니까", "Since hungry"), ("밥을", "rice"), ("먹어요", "eat")]),

    ("Because Formal", "기 때문에 (gi ttaemune)",
     "Because (formal)",
     "비가 오기 때문에 안 가요. (Not going because of rain.)",
     "Formal reason marker. More emphatic.",
     [("비가", "rain"), ("오기 때문에", "because comes"), ("안 가요", "not go")]),

    # ===== OTHER PARTICLES =====
    ("But / However Particle", "만 (man)",
     "But",
     "작지만 좋아요. (Small but good.)",
     "Means 'but' or 'however'. Connects contrasting ideas.",
     [("작지만", "Small but"), ("좋아요", "good")]),

    ("Or Particle", "이나 (ina) / 나 (na)",
     "Or (approximate)",
     "물이나 주세요. (Water or something please.)",
     "Used when making suggestions or showing uncertainty.",
     [("물이나", "Water or"), ("주세요", "please give")]),

    ("Each / Every Particle", "마다 (mada)",
     "Every / Each",
     "매일마다 (Every single day)\n사람마다 (Each person)",
     "Means 'every' or 'each'. Added to time words.",
     [("매일", "every day"), ("마다", "each")]),

    ("Approximately Particle", "쯤 (jjeum)",
     "About / Approximately",
     "3시쯤 만나요. (Meet around 3.)",
     "Means 'about' or 'approximately'.",
     [("3시쯤", "around 3"), ("만나요", "meet")]),

    ("Starting From Particle", "부터 (buteo)",
     "From / Starting with",
     "9시부터 시작해요. (Starts from 9.)",
     "Shows starting point in time or sequence.",
     [("9시부터", "From 9"), ("시작해요", "start")]),

    # ===== INSTRUMENTAL PARTICLES =====
    ("By / With Particle", "(으)로 (eu/ro)",
     "By means of / With",
     "펜으로 써요. (Write with a pen.)\n버스로 가요. (Go by bus.)",
     "Shows means, method, or material. After ㄹ consonant: 로",
     [("펜으로", "with a pen"), ("써요", "write")]),

    # ===== QUESTION WORDS + PARTICLES =====
    ("Who (subject)", "누구 (nugu) + 가 (ga)",
     "누가 (nuga)",
     "누가 왔어요? (Who came?)",
     "Subject particle changes to 가 after 누구",
     [("누가", "Who"), ("왔어요", "came")]),

    ("Who (with)", "누구 (nugu) + 한테 (hante)",
     "누구한테 (nuguhante)",
     "누구한테 줄까요? (Who should I give it to?)",
     "With whom / to whom",
     [("누구한테", "To whom"), ("줄까요", "shall give")]),

    ("What (object)", "무엇 (mueot) + 을 (eul)",
     "무엇을 (mueoseul) → 뭘 (mwol)",
     "뭘 먹을까요? (What should we eat?)",
     "Shrunk form commonly used",
     [("뭘", "What"), ("먹을까요", "shall eat")]),

    ("When", "언제 (eonje)",
     "No particle needed",
     "언제 갈 거예요? (When will you go?)",
     "Question word for time",
     [("언제", "When"), ("갈 거예요", "will go")]),

    ("Where", "어디 (eodi)",
     "에 (e) for going, 에서 (eseo) for from/at",
     "어디에 가요? (Where going?)",
     "Question word for place",
     [("어디에", "Where to"), ("가요", "go")]),

    ("Why", "왜 (wae)",
     "No particle needed",
     "왜 안 왔어요? (Why didn't you come?)",
     "Question word for reason",
     [("왜", "Why"), ("안 왔어요", "didn't come")]),

    ("How", "어떻게 (eotteoke)",
     "No particle needed",
     "어떻게 왔어요? (How did you come?)",
     "Question word for method",
     [("어떻게", "How"), ("왔어요", "came")]),
]


def create_model():
    """Create card model for grammar particles with colored word alignment."""
    return genanki.Model(
        MODEL_ID,
        "Korean Particle Model",
        fields=[
            {"name": "ParticleName"},
            {"name": "Particle"},
            {"name": "Rule"},
            {"name": "Examples"},
            {"name": "Notes"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Particle Card",
                "qfmt": """
<div style="padding: 20px; background: #f5f5f5; border-radius: 10px; margin: 15px; text-align: center;">
    <strong style="font-size: 18px; color: #666;">{{ParticleName}}</strong>
</div>
<div style="text-align: center; font-size: 70px; padding: 40px;">
    {{Particle}}
</div>
                """,
                "afmt": """
<div style="padding: 15px; background: #f5f5f5; border-radius: 10px; margin: 10px; text-align: center;">
    <strong style="font-size: 16px; color: #666;">{{ParticleName}}</strong>
</div>
<div style="text-align: center; font-size: 60px; padding: 30px;">
    {{Particle}}
</div>
<div style="text-align: center; padding: 15px;">
    {{Audio}}
</div>
<hr style="margin: 15px 0;">
<div style="text-align: center; font-size: 18px; padding: 12px; margin: 10px auto; max-width: 550px; background: #e3f2fd; border-radius: 8px;">
    <strong>Rule:</strong> {{Rule}}
</div>
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 700px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 26px; padding: 10px; line-height: 1.8; color: #2c3e50; font-weight: 600;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
<div style="text-align: center; font-size: 16px; padding: 15px; margin: 15px auto; max-width: 600px; background: #f9f9f9; border-radius: 8px; white-space: pre-line;">
    <strong>Examples:</strong>
    {{Examples}}
</div>
{{#Notes}}
<div style="text-align: center; font-size: 14px; color: #666; padding: 10px; margin: 10px auto; max-width: 550px; border-left: 4px solid #2196F3; background: #fffde7;">
    <em>{{Notes}}</em>
</div>
{{/Notes}}
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


def generate_deck(output_file="decks/06_korean_particles.apkg"):
    """Generate the particles deck with colored word alignment."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "06. Korean Particles - 조사")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for item in PARTICLES:
            # Handle both old format (5 items) and new format (6 items with word_pairs)
            if len(item) == 6:
                name, particle, rule, examples, notes, word_pairs = item
            else:
                name, particle, rule, examples, notes = item
                word_pairs = None

            # Generate colored HTML from word_pairs
            korean_colored = ""
            english_colored = ""
            if word_pairs:
                korean_colored, english_colored = create_colored_html(word_pairs)

            # Generate audio (just the particle part)
            audio_text = particle.split()[0] if ' ' in particle else particle
            audio_filename = generate_audio(audio_text, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[name, particle, rule, examples, notes, korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        print(f"Deck created: {output_file}")
        print(f"  - {len(PARTICLES)} particle cards")
        print(f"  - {len(created_audio_files)} audio files")
        print("\nImport this file into Anki: File -> Import...")

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(audio_dir)
        except:
            pass


if __name__ == "__main__":
    generate_deck()
