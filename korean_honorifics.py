#!/usr/bin/env python3
"""
Korean Honorifics System

Speech levels, honorific vocabulary, and honorific verb endings.
Usage: python3 korean_honorifics.py
"""

import sys
import os
import tempfile
import shutil

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import (
    generate_audio, created_audio_files, DECK_IDS, MODEL_IDS, create_colored_html
)

# Deck info
DECK_ID = DECK_IDS["honorifics"]
MODEL_ID = MODEL_IDS["grammar"]


# Honorific data: (plain, honorific, meaning, usage, example, word_pairs)
# word_pairs is optional list of (korean, english) tuples for colored alignment
HONORIFICS = [
    # ===== HONORIFIC VERBS =====
    ("먹다", "드시다/잡수시다", "To eat", "Honorific for elders/superiors", "할아버지께서 드셨어요 (Grandfather ate)",
     [("할아버지께서", "Grandfather"), ("드셨어요", "ate")]),
    ("자다", "주무시다", "To sleep", "Honorific for elders", "할머니께서 주무셨어요 (Grandmother slept)",
     [("할머니께서", "Grandmother"), ("주무셨어요", "slept")]),
    ("있다", "계시다", "To be/exist (people)", "Honorific existence", "선생님께서 계셔요 (Teacher is here)",
     [("선생님께서", "Teacher"), ("계셔요", "is here")]),
    ("없다", "안 계시다", "To not exist", "Honorific negative", "할머니는 안 계셔요 (Grandmother isn't here)",
     [("할머니는", "Grandmother"), ("안 계셔요", "isn't here")]),
    ("오다", "오시다", "To come", "Honorific approach", "사장님이 오셨어요 (Boss came)",
     [("사장님이", "Boss"), ("오셨어요", "came")]),
    ("가다", "가시다", "To go", "Honorific departure", "선생님이 가셨어요 (Teacher left)",
     [("선생님이", "Teacher"), ("가셨어요", "left")]),
    ("말하다", "말씀하시다", "To speak/say", "Honorific speech", "할아버지께서 말씀하셨어요 (Grandfather spoke)",
     [("할아버지께서", "Grandfather"), ("말씀하셨어요", "spoke")]),
    ("보다", "보시다", "To see", "Honorific viewing", "어머님께서 보셨어요 (Mother saw)",
     [("어머님께서", "Mother"), ("보셨어요", "saw")]),
    ("묻다", "여쭙다", "To ask", "Honorific inquiry", "선생님께 여쭤어요 (Asked teacher)",
     [("선생님께", "to teacher"), ("여쭤어요", "asked")]),
    ("주다", "드리다", "To give", "Honorific giving", "어머니께 드려요 (Give to mother)",
     [("어머니께", "to mother"), ("드려요", "give")]),
    ("받다", "받으시다", "To receive", "Honorific receiving", "사장님께 받으셨어요 (Received from boss)",
     [("사장님께", "from boss"), ("받으셨어요", "received")]),
    ("만나다", "뵙다", "To meet", "Honorific meeting", "선생님을 뵈었어요 (Met teacher)",
     [("선생님을", "teacher"), ("뵈었어요", "met")]),
    ("들다", "들으시다", "To hear/listen", "Honorific listening", "할아버지께 들으셨어요 (Grandfather heard)",
     [("할아버지께", "Grandfather"), ("들으셨어요", "heard")]),
    ("죽다", "돌아가시다", "To die", "Euphemism for death", "할아버지께서 돌아가셨어요 (Grandfather passed away)",
     [("할아버지께서", "Grandfather"), ("돌아가셨어요", "passed away")]),
    ("아프다", "편찮으시다", "To be sick", "Honorific illness", "어머님께서 편찮으셔요 (Mother is sick)",
     [("어머님께서", "Mother"), ("편찮으셔요", "is sick")]),
    ("이다", "이시다", "To be (identity)", "Honorific copula", "이분은 선생님이셨어요 (This person was teacher)",
     [("이분은", "This person"), ("선생님이셨어요", "was teacher")]),

    # ===== HONORIFIC NOUNS =====
    ("집", "댁", "House", "Someone else's house", "선생님 댁에 가요 (Going to teacher's house)",
     [("선생님", "teacher's"), ("댁에", "house"), ("가요", "going")]),
    ("밥", "진지", "Rice/meal", "Elder's meal", "할머니 진지를 드셨어요 (Grandmother ate)",
     [("할머니", "Grandmother"), ("진지를", "meal"), ("드셨어요", "ate")]),
    ("나이", "연세", "Age", "Elder's age", "할아버지 연세가 어떻게 되세요? (How old is grandfather?)",
     [("할아버지", "Grandfather"), ("연세가", "age"), ("어떻게 되세요?", "how is?")]),
    ("이름", "성함", "Name", "Honorific name", "성함이 어떻게 되세요? (What is your name?)",
     [("성함이", "name"), ("어떻게 되세요?", "what is?")]),
    ("생일", "생신", "Birthday", "Elder's birthday", "어머니 생신이 언제예요? (When is mother's birthday?)",
     [("어머니", "mother's"), ("생신이", "birthday"), ("언제예요?", "when is?")]),
    ("얼굴", "용안", "Face", "Very formal", "용안을 뵙었어요 (Saw your face)",
     [("용안을", "your face"), ("뵙었어요", "saw")]),
    ("말", "말씀", "Words/speech", "Honorific speech", "말씀을 잘 들었어요 (Heard your words well)",
     [("말씀을", "words"), ("잘 들었어요", "heard well")]),
    ("아내", "부인", "Wife", "Someone's wife", "김 사장님 부인 (CEO Kim's wife)",
     [("김", "Kim"), ("사장님", "CEO"), ("부인", "wife")]),
    ("남편", "선생님", "Husband", "Someone's husband", "이 선생님 남편 (Mr./Teacher Lee's husband)",
     [("이", "Lee"), ("선생님", "Mr./Teacher"), ("남편", "husband")]),
    ("딸", "따님", "Daughter", "Someone's daughter", "따님이 예쁘시네요 (Your daughter is pretty)",
     [("따님이", "Your daughter"), ("예쁘시네요", "is pretty")]),
    ("아들", "아드님", "Son", "Someone's son", "아드님이 컸네요 (Your son grew up)",
     [("아드님이", "Your son"), ("컸네요", "grew up")]),
    ("회사", "회사", "Company (no change)", "For someone's workplace", "이름이 회사예요 (Myeong's company)",
     [("이름이", "Myeong's"), ("회사예요", "is company")]),
    ("가족", "가식", "Family (archaic)", "Rarely used now", "가식 (family - old word)", []),

    # ===== HONORIFIC TITLES =====
    ("선생님", "Teacher", "General honorific", "Teachers, doctors, lawyers", "김 선생님 (Teacher/Mr. Kim)",
     [("김", "Kim"), ("선생님", "Teacher/Mr.")]),
    ("교수님", "Professor", "Academic honorific", "University professors", "박 교수님 (Professor Park)",
     [("박", "Park"), ("교수님", "Professor")]),
    ("사장님", "President/CEO", "Business honorific", "Company presidents", "이 사장님 (President Lee)",
     [("이", "Lee"), ("사장님", "President")]),
    ("과장님", "Manager", "Job title honorific", "Middle management", "김 과장님 (Manager Kim)",
     [("김", "Kim"), ("과장님", "Manager")]),
    ("부장님", "Department head", "Job title honorific", "Senior management", "박 부장님 (Dept. Head Park)",
     [("박", "Park"), ("부장님", "Dept. Head")]),
    ("선배님", "Senior", "School/work senior", "Older student/colleague", "선배님 (Senior)",
     [("선배님", "Senior")]),
    ("후배님", "Junior", "School/work junior", "Younger student/colleague", "후배님 (Junior)",
     [("후배님", "Junior")]),
    ("어머님", "Mother (honorific)", "Other's mother", "Respectful address", "어머님 (Mother - respectful)",
     [("어머님", "Mother")]),
    ("아버님", "Father (honorific)", "Other's father", "Respectful address", "아버님 (Father - respectful)",
     [("아버님", "Father")]),
    ("할머님", "Grandmother", "Elder woman", "Unknown elderly woman", "할머님 (Grandmother)",
     [("할머님", "Grandmother")]),
    ("할아버님", "Grandfather", "Elder man", "Unknown elderly man", "할아버님 (Grandfather)",
     [("할아버님", "Grandfather")]),

    # ===== HONORIFIC ENDINGS =====
    ("~(으)시", "Honorific verb ending", "Subject honorific", "Used after verb stem", "가시다 (go-honorific), 오시다 (come-honorific)",
     [("가시다", "go-honorific"), ("오시다", "come-honorific")]),
    ("~습니다", "Formal polite ending", "Formal speech level", "With strangers/formal situations", "갑니다 (go), 먹습니다 (eat)",
     [("갑니다", "go"), ("먹습니다", "eat")]),
    ("~아/어요", "Informal polite ending", "Polite speech level", "Most common polite", "가요 (go), 먹어요 (eat)",
     [("가요", "go"), ("먹어요", "eat")]),
    ("~(이)에요/가에요", "Copula ending", "Is/am/are (polite)", "Identifying someone/something", "학생이에요 (am a student)",
     [("학생", "student"), ("이에요", "am")]),
    ("~아/어", "Casual ending", "Informal speech", "Friends, younger people", "가 (go), 먹어 (eat)",
     [("가", "go"), ("먹어", "eat")]),
    ("~군요/는군요", "Exclamation ending", "Expressing realization", "Noticing something", "좋군요 (Oh, it's good)",
     [("좋군요", "it's good")]),
    ("~네요", "Realization ending", "Noticing something", "New information", "예쁘네요 (Oh, you're pretty)",
     [("예쁘네요", "you're pretty")]),
    ("~죠/~지요", "Confirmation ending", "Asking for agreement", "Seeking confirmation", "그렇죠 (Right?)",
     [("그렇죠", "Right?")]),

    # ===== PRONOUN CHANGES =====
    ("나", "저", "I/me (humble)", "Self-reference in formal situations", "저는 학생이에요 (I am a student)",
     [("저는", "I"), ("학생", "student"), ("이에요", "am")]),
    ("너", "자기/당신", "You (limited use)", "Korean avoids 'you' directly", "자기 (dear), 당신 (spouse/written)",
     [("자기", "dear"), ("당신", "spouse")]),
    ("우리", "저희", "We (humble)", "Humble we", "저희 가족 (my family - humble)",
     [("저희", "my"), ("가족", "family")]),
    ("이분", "This person (honorific)", "This person here", "Pointing to someone politely", "이분은 누구세요? (Who is this person?)",
     [("이분은", "This person"), ("누구세요?", "who is?")]),
    ("그분", "That person (honorific)", "That person", "Someone mentioned", "그분은 선생님이셨어요 (That person was a teacher)",
     [("그분은", "That person"), ("선생님이셨어요", "was a teacher")]),
    ("저분", "That person over there (honorific)", "Person at distance", "Far away", "저분은 할머니시네요 (That person is a grandmother)",
     [("저분은", "That person"), ("할머니시네요", "is a grandmother")]),

    # ===== HONORIFIC EXAMPLES =====
    ("아버지 가셨어요", "Father went", "Honorific motion", "Subject honorific + 가다", "아버지께서 가셨어요 (Father went - honorific)",
     [("아버지께서", "Father"), ("가셨어요", "went")]),
    ("어머니 드셨어요", "Mother ate", "Honorific eating", "Subject honorific + 드시다", "어머니께서 진지를 드셨어요 (Mother ate)",
     [("어머니께서", "Mother"), ("진지를", "meal"), ("드셨어요", "ate")]),
    ("할아버지 주무셨어요", "Grandfather slept", "Honorific sleep", "Subject honorific + 주무시다", "할아버지께서 주무셨어요 (Grandfather slept)",
     [("할아버지께서", "Grandfather"), ("주무셨어요", "slept")]),
    ("선생님 계셔요", "Teacher is here", "Honorific existence", "Subject honorific + 계시다", "선생님께서 교실에 계셔요 (Teacher is in the classroom)",
     [("선생님께서", "Teacher"), ("교실에", "in the classroom"), ("계셔요", "is")]),
]

# Speech Levels explanation
SPEECH_LEVELS = [
    ("Formal High (하십시오체)", "~습니다/ㅂ니다", "With strangers, formal situations", "갑니다 (go), 먹습니다 (eat)"),
    ("Formal Low (해요체)", "~아/어요", "Polite, most common", "가요 (go), 먹어요 (eat)"),
    ("Plain (해라체)", "~다/ㄴ다", "Writing, casual", "간다 (go), 먹는다 (eat)"),
    ("Casual (해체)", "~아/어", "Close friends, younger", "가 (go), 먹어 (eat)"),
]


def create_model():
    """Create card model for honorifics."""
    return genanki.Model(
        MODEL_ID,
        "Korean Honorific Model",
        fields=[
            {"name": "PlainForm"},
            {"name": "HonorificForm"},
            {"name": "Meaning"},
            {"name": "Usage"},
            {"name": "Example"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Honorific Card",
                "qfmt": """
<div style="padding: 12px; background: #f5f5f5; border-radius: 8px; margin: 10px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">Plain Form → Honorific Form</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 30px;">
    {{PlainForm}}
</div>
<div style="text-align: center; font-size: 40px; color: #2196F3;">
    → {{HonorificForm}}
</div>
                """,
                "afmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 13px; color: #666;">Plain Form → Honorific Form</strong>
</div>
<div style="text-align: center; font-size: 45px; padding: 25px;">
    {{PlainForm}}
</div>
<div style="text-align: center; font-size: 35px; color: #2196F3; padding: 10px;">
    → {{HonorificForm}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
<hr style="margin: 12px 0;">
<div style="text-align: center; font-size: 24px; color: #333; font-weight: bold; padding: 10px;">
    {{Meaning}}
</div>
<div style="text-align: center; font-size: 14px; color: #666; padding: 10px; margin: 10px auto; max-width: 550px; background: #e3f2fd; border-radius: 6px;">
    <strong>Usage:</strong> {{Usage}}
</div>
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 650px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 22px; padding: 10px; line-height: 1.8; color: #2c3e50; font-weight: 600;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 16px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{#Example}}
{{^KoreanColored}}
<div style="text-align: center; font-size: 16px; padding: 12px; margin: 12px auto; max-width: 600px; background: #f9f9f9; border-radius: 8px;">
    <strong>Example:</strong> {{Example}}
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


def generate_deck(output_file="decks/10_korean_honorifics.apkg"):
    """Generate the honorifics deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "10. Korean Honorifics - 존댓말")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        # Add honorific words
        for item in HONORIFICS:
            # Handle both old format (5-tuple) and new format (6-tuple with word_pairs)
            if len(item) == 6:
                plain, honorific, meaning, usage, example, word_pairs = item
            else:
                plain, honorific, meaning, usage, example = item
                word_pairs = []

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = "", ""
            if word_pairs:
                korean_colored, english_colored = create_colored_html(word_pairs)

            # Generate audio for honorific form
            audio_text = honorific.split('/')[0] if '/' in honorific else honorific
            audio_filename = generate_audio(audio_text, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[plain, honorific, meaning, usage, example, korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Add speech levels (no word_pairs for these)
        for level, ending, usage, example in SPEECH_LEVELS:
            # Generate audio for example
            audio_filename = generate_audio(example, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[level, ending, usage, "", example, "", "", audio_field],
            )
            deck.add_note(note)

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        total = len(HONORIFICS) + len(SPEECH_LEVELS)
        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(HONORIFICS)} honorific word cards")
        print(f"  - {len(SPEECH_LEVELS)} speech level cards")
        print(f"  - Total: {total} cards")
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
