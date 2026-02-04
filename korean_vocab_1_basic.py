#!/usr/bin/env python3
"""
Korean Basic Vocabulary Deck (Top 100+)

Foundational vocabulary for everyday use.
Categories: Greetings, Pronouns, Family, Verbs, Adjectives, Common Nouns
Usage: python3 korean_vocab_1_basic.py
"""

import sys
import os
import tempfile
import shutil

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import (
    DECK_IDS, MODEL_IDS, generate_audio, created_audio_files, create_colored_html
)

# Deck info
DECK_ID = DECK_IDS["vocab_1"]
MODEL_ID = MODEL_IDS["word"]


# Helper to create vocab entry with word pairs
def v(korean, english, roman, example, ex_trans, word_pairs=None):
    """Create a vocabulary entry with optional word pairs for color alignment."""
    return (korean, english, roman, example, ex_trans, word_pairs)


# Basic vocabulary with word pairs for color alignment
BASIC_VOCAB = [
    # ===== GREETINGS =====
    v("안녕하세요", "Hello", "annyeonghaseyo", "안녕하세요! 만나서 반갑습니다.", "Hello! Nice to meet you.",
      [("안녕하세요!", "Hello!"), ("만나서", "to meet"), ("반갑습니다.", "nice to meet you.")]),
    v("안녕히 가세요", "Goodbye (to person leaving)", "annyeonghi gaseyo", "안녕히 가세요!", "Goodbye! (said by person staying)",
      [("안녕히 가세요!", "Goodbye!")]),

    v("감사합니다", "Thank you (formal)", "gamsahamnida", "도와주셔서 감사합니다.", "Thank you for helping.",
      [("도와주셔서", "for helping"), ("감사합니다.", "thank you.")]),
    v("고맙습니다", "Thank you", "gomapseumnida", "정말 고맙습니다.", "Thank you very much.",
      [("정말", "very much"), ("고맙습니다.", "thank you.")]),
    v("죄송합니다", "I'm sorry (formal)", "joesonghamnida", "늦어서 죄송합니다.", "Sorry I'm late.",
      [("늦어서", "for being late"), ("죄송합니다.", "sorry.")]),
    v("미안합니다", "I'm sorry", "mianhamnida", "기다려서 미안합니다.", "Sorry for waiting.",
      [("기다려서", "for waiting"), ("미안합니다.", "sorry.")]),
    v("네", "Yes", "ne", "네, 알겠습니다.", "Yes, I understand.",
      [("네,", "Yes,"), ("알겠습니다.", "I understand.")]),
    v("아니요", "No", "aniyo", "아니요, 괜찮습니다.", "No, it's okay.",
      [("아니요,", "No,"), ("괜찮습니다.", "it's okay.")]),
    v("실례합니다", "Excuse me", "sillyehamnida", "실례합니다, 화장실이 어디예요?", "Excuse me, where is the restroom?",
      [("실례합니다,", "Excuse me,"), ("화장실이", "restroom"), ("어디예요?", "where is?")]),

    # ===== PRONOUNS =====
    v("저", "I/me (humble)", "jeo", "저는 학생이에요.", "I am a student.",
      [("저는", "I"), ("학생이에요.", "am a student.")]),
    v("나", "I/me (casual)", "na", "나는 지금 집에 가.", "I'm going home now.",
      [("나는", "I"), ("지금", "now"), ("집에", "home"), ("가.", "go.")]),
    v("너", "You (casual)", "neo", "너는 누구니?", "Who are you?",
      [("너는", "you"), ("누구니?", "who?")]),
    v("우리", "We / Us / My", "uri", "우리 아빠", "My dad / Our dad",
      [("우리", "My/Our"), ("아빠", "dad")]),
    v("이분", "This person (honorific)", "ibun", "이분은 제 선생님이에요.", "This person is my teacher.",
      [("이분은", "This person"), ("제", "my"), ("선생님이에요.", "is teacher.")]),
    v("것", "Thing", "geot", "이것은 무엇입니까?", "What is this thing?",
      [("이것은", "This"), ("무엇입니까?", "what is?")]),
    v("무엇", "What", "mueot", "무엇을 원하세요?", "What would you like?",
      [("무엇을", "What"), ("원하세요?", "would you like?")]),
    v("뭐", "What (casual)", "mwo", "뭐 할까요?", "What should we do?",
      [("뭐", "What"), ("할까요?", "should we do?")]),

    # ===== FAMILY =====
    v("가족", "Family", "gajok", "저희 가족은 4명이에요.", "Our family has 4 people.",
      [("저희", "Our"), ("가족은", "family"), ("4명이에요.", "has 4 people.")]),
    v("어머니", "Mother (formal)", "eomeoni", "어머니께서 요리하셨어요.", "Mother cooked.",
      [("어머니께서", "Mother"), ("요리하셨어요.", "cooked.")]),
    v("아버지", "Father (formal)", "abeoji", "아버지께서 회사에 가셨어요.", "Father went to work.",
      [("아버지께서", "Father"), ("회사에", "to work"), ("가셨어요.", "went.")]),
    v("엄마", "Mom (casual)", "eomma", "엄마, 배고파요.", "Mom, I'm hungry.",
      [("엄마,", "Mom,"), ("배고파요.", "I'm hungry.")]),
    v("아빠", "Dad (casual)", "appa", "아빠, 언제 와요?", "Dad, when are you coming?",
      [("아빠,", "Dad,"), ("언제", "when"), ("와요?", "are coming?")]),
    v("형", "Older brother (male speaker)", "hyeong", "형이 도와줬어요.", "Older brother helped me.",
      [("형이", "Older brother"), ("도와줬어요.", "helped me.")]),
    v("오빠", "Older brother (female speaker)", "oppa", "오빠가 샀어요.", "Older brother bought it.",
      [("오빠가", "Older brother"), ("샀어요.", "bought.")]),
    v("누나", "Older sister (male speaker)", "nuna", "누나가 예뻐요.", "Older sister is pretty.",
      [("누나가", "Older sister"), ("예뻐요.", "is pretty.")]),
    v("언니", "Older sister (female speaker)", "eonni", "언니가 갔어요.", "Older sister left.",
      [("언니가", "Older sister"), ("갔어요.", "left.")]),
    v("동생", "Younger sibling", "dongsaeng", "동생이 한 명 있어요.", "I have one younger sibling.",
      [("동생이", "Younger sibling"), ("한 명", "one"), ("있어요.", "have.")]),
    v("할머니", "Grandmother", "halmeoni", "할머니 댁에 갈 거예요.", "Going to grandmother's house.",
      [("할머니", "grandmother's"), ("댁에", "house"), ("갈 거예요.", "going to.")]),
    v("할아버지", "Grandfather", "harabeoji", "할아버지가 좋아하세요.", "Grandfather likes it.",
      [("할아버지가", "Grandfather"), ("좋아하세요.", "likes.")]),

    # ===== BASIC VERBS =====
    v("가다", "To go", "gada", "학교에 가요.", "Going to school.",
      [("학교에", "to school"), ("가요.", "going.")]),
    v("오다", "To come", "oda", "친구가 와요.", "A friend is coming.",
      [("친구가", "A friend"), ("와요.", "is coming.")]),
    v("있다", "To exist / To have", "itda", "집에 있어요.", "(Someone) is at home.",
      [("집에", "at home"), ("있어요.", "is.")]),
    v("없다", "To not exist / To not have", "eopda", "돈이 없어요.", "I don't have money.",
      [("돈이", "money"), ("없어요.", "don't have.")]),
    v("하다", "To do", "hada", "숙제를 해요.", "Doing homework.",
      [("숙제를", "homework"), ("해요.", "doing.")]),
    v("먹다", "To eat", "meokda", "밥을 먹어요.", "Eating rice/a meal.",
      [("밥을", "rice/meal"), ("먹어요.", "eating.")]),
    v("마시다", "To drink", "masida", "물을 마셔요.", "Drinking water.",
      [("물을", "water"), ("마셔요.", "drinking.")]),
    v("자다", "To sleep", "jada", "지금 자요.", "Sleeping now.",
      [("지금", "now"), ("자요.", "sleeping.")]),
    v("일어나다", "To wake up / To get up", "ireonada", "7시에 일어나요.", "Waking up at 7.",
      [("7시에", "at 7"), ("일어나요.", "waking up.")]),
    v("보다", "To see / To watch", "boda", "TV를 봐요.", "Watching TV.",
      [("TV를", "TV"), ("봐요.", "watching.")]),
    v("듣다", "To hear / To listen", "deutda", "음악을 들어요.", "Listening to music.",
      [("음악을", "music"), ("들어요.", "listening.")]),
    v("읽다", "To read", "ikda", "책을 읽어요.", "Reading a book.",
      [("책을", "book"), ("읽어요.", "reading.")]),
    v("쓰다", "To write / To use", "sseuda", "글을 써요.", "Writing text.",
      [("글을", "text"), ("써요.", "writing.")]),
    v("만나다", "To meet", "mannada", "친구를 만나요.", "Meeting a friend.",
      [("친구를", "a friend"), ("만나요.", "meeting.")]),
    v("사랑하다", "To love", "saranghada", "너를 사랑해.", "I love you.",
      [("너를", "you"), ("사랑해.", "love.")]),
    v("좋아하다", "To like", "joahada", "김치를 좋아해요.", "I like kimchi.",
      [("김치를", "kimchi"), ("좋아해요.", "like.")]),
    v("살다", "To live", "salda", "서울에 살아요.", "Living in Seoul.",
      [("서울에", "in Seoul"), ("살아요.", "living.")]),
    v("배우다", "To learn", "baeuda", "한국어를 배워요.", "Learning Korean.",
      [("한국어를", "Korean"), ("배워요.", "learning.")]),
    v("가르치다", "To teach", "gareuchida", "영어를 가르쳐요.", "Teaching English.",
      [("영어를", "English"), ("가르쳐요.", "teaching.")]),
    v("일하다", "To work", "ilhada", "회사에서 일해요.", "Working at a company.",
      [("회사에서", "at a company"), ("일해요.", "working.")]),
    v("공부하다", "To study", "gongbuhada", "도서관에서 공부해요.", "Studying at the library.",
      [("도서관에서", "at the library"), ("공부해요.", "studying.")]),
    v("운동하다", "To exercise", "undonghada", "매일 운동해요.", "Exercising every day.",
      [("매일", "every day"), ("운동해요.", "exercising.")]),
    v("요리하다", "To cook", "yorihada", "엄마가 요리해요.", "Mom cooks.",
      [("엄마가", "Mom"), ("요리해요.", "cooks.")]),
    v("사다", "To buy", "sada", "사과를 샀어요.", "Bought apples.",
      [("사과를", "apples"), ("샀어요.", "bought.")]),
    v("팔다", "To sell", "palda", "가게에서 팔아요.", "Selling at a store.",
      [("가게에서", "at a store"), ("팔아요.", "selling.")]),
    v("주다", "To give", "juda", "선물을 줘요.", "Giving a present.",
      [("선물을", "a present"), ("줘요.", "giving.")]),
    v("받다", "To receive", "batda", "편지를 받았어요.", "Received a letter.",
      [("편지를", "a letter"), ("받았어요.", "received.")]),
    v("찾다", "To find / To look for", "chajda", "지갑을 찾아요.", "Looking for a wallet.",
      [("지갑을", "a wallet"), ("찾아요.", "looking for.")]),
    v("열다", "To open", "yeolda", "문을 열어요.", "Opening the door.",
      [("문을", "the door"), ("열어요.", "opening.")]),
    v("닫다", "To close", "datda", "창문을 닫아요.", "Closing the window.",
      [("창문을", "the window"), ("닫아요.", "closing.")]),
    v("앉다", "To sit", "anda", "의자에 앉아요.", "Sitting on a chair.",
      [("의자에", "on a chair"), ("앉아요.", "sitting.")]),
    v("서다", "To stand", "seoda", "버스에서 서요.", "Standing on the bus.",
      [("버스에서", "on the bus"), ("서요.", "standing.")]),
    v("뛰다", "To run", "twida", "공원에서 뛰어요.", "Running in the park.",
      [("공원에서", "in the park"), ("뛰어요.", "running.")]),
    v("걷다", "To walk", "geotda", "학교에 걸어가요.", "Walking to school.",
      [("학교에", "to school"), ("걸어가요.", "walking.")]),
    v("놀다", "To play / To hang out", "nolda", "친구들이랑 놀아요.", "Hanging out with friends.",
      [("친구들이랑", "with friends"), ("놀아요.", "hanging out.")]),
    v("전화하다", "To call (phone)", "jeonhwahada", "친구한테 전화해요.", "Calling a friend.",
      [("친구한테", "a friend"), ("전화해요.", "calling.")]),
    v("기다리다", "To wait", "gidarida", "버스를 기다려요.", "Waiting for the bus.",
      [("버스를", "the bus"), ("기다려요.", "waiting.")]),
    v("원하다", "To want", "wonhada", "무엇을 원하세요?", "What do you want?",
      [("무엇을", "what"), ("원하세요?", "do you want?")]),

    # ===== BASIC ADJECTIVES =====
    v("크다", "To be big", "keuda", "집이 커요.", "The house is big.",
      [("집이", "The house"), ("커요.", "is big.")]),
    v("작다", "To be small", "jakda", "방이 작아요.", "The room is small.",
      [("방이", "The room"), ("작아요.", "is small.")]),
    v("좋다", "To be good / To be nice", "jota", "날씨가 좋아요.", "The weather is good.",
      [("날씨가", "The weather"), ("좋아요.", "is good.")]),
    v("나쁘다", "To be bad", "nappeuda", "사람이 나빠요.", "The person is bad.",
      [("사람이", "The person"), ("나빠요.", "is bad.")]),
    v("많다", "To be many / To be much", "manta", "사람이 많아요.", "There are many people.",
      [("사람이", "people"), ("많아요.", "are many.")]),
    v("적다", "To be few", "jeokda", "돈이 적어요.", "There's little money.",
      [("돈이", "money"), ("적어요.", "is little.")]),
    v("높다", "To be high", "nopda", "산이 높아요.", "The mountain is high.",
      [("산이", "The mountain"), ("높아요.", "is high.")]),
    v("길다", "To be long", "gilda", "머리가 길어요.", "Hair is long.",
      [("머리가", "Hair"), ("길어요.", "is long.")]),
    v("짧다", "To be short", "jjalba", "치마가 짧아요.", "The skirt is short.",
      [("치마가", "The skirt"), ("짧아요.", "is short.")]),
    v("예쁘다", "To be pretty", "yeppeuda", "꽃이 예뻐요.", "The flower is pretty.",
      [("꽃이", "The flower"), ("예뻐요.", "is pretty.")]),
    v("맛있다", "To be delicious", "masitda", "음식이 맛있어요.", "The food is delicious.",
      [("음식이", "The food"), ("맛있어요.", "is delicious.")]),
    v("덥다", "To be hot (weather)", "deopda", "여름은 더워요.", "Summer is hot.",
      [("여름은", "Summer"), ("더워요.", "is hot.")]),
    v("춥다", "To be cold (weather)", "chupda", "겨울은 추워요.", "Winter is cold.",
      [("겨울은", "Winter"), ("추워요.", "is cold.")]),
    v("바쁘다", "To be busy", "bappeuda", "오늘 바빠요.", "Today is busy.",
      [("오늘", "Today"), ("바빠요.", "is busy.")]),
    v("즐겁다", "To be enjoyable / fun", "jeulgeopda", "시간이 즐거워요.", "The time is enjoyable.",
      [("시간이", "The time"), ("즐거워요.", "is enjoyable.")]),
    v("편하다", "To be comfortable", "pyeonhada", "의자가 편해요.", "The chair is comfortable.",
      [("의자가", "The chair"), ("편해요.", "is comfortable.")]),
    v("아프다", "To be sick / To be in pain", "apeuda", "머리가 아파요.", "My head hurts.",
      [("머리가", "My head"), ("아파요.", "hurts.")]),
    v("괜찮다", "To be okay / To be fine", "gwaenchanta", "괜찮아요?", "Are you okay?",
      [("괜찮아요?", "Are you okay?")]),
    v("행복하다", "To be happy", "haengbokada", "저는 행복해요.", "I am happy.",
      [("저는", "I"), ("행복해요.", "am happy.")]),
    v("슬프다", "To be sad", "seupeuda", "영화가 슬퍼요.", "The movie is sad.",
      [("영화가", "The movie"), ("슬퍼요.", "is sad.")]),
    v("화나다", "To be angry", "hwanaada", "화가 났어요.", "I got angry.",
      [("화가", "Anger"), ("났어요.", "happened.")]),
    v("재미있다", "To be fun / interesting", "jaemiitda", "게임이 재미있어요.", "The game is fun.",
      [("게임이", "The game"), ("재미있어요.", "is fun.")]),
    v("쉽다", "To be easy", "swipda", "문제가 쉬워요.", "The problem is easy.",
      [("문제가", "The problem"), ("쉬워요.", "is easy.")]),
    v("어렵다", "To be difficult / hard", "eoryeopda", "한국어가 어려워요.", "Korean is difficult.",
      [("한국어가", "Korean"), ("어려워요.", "is difficult.")]),

    # ===== COMMON NOUNS =====
    v("집", "Home / House", "jip", "집에 가요.", "Going home.",
      [("집에", "home"), ("가요.", "going.")]),
    v("학교", "School", "hakgyo", "학교에 가요.", "Going to school.",
      [("학교에", "to school"), ("가요.", "going.")]),
    v("회사", "Company / Office", "hoesa", "회사에 가요.", "Going to the office.",
      [("회사에", "to the office"), ("가요.", "going.")]),
    v("식당", "Restaurant", "sikdang", "식당에서 밥을 먹어요.", "Eating at a restaurant.",
      [("식당에서", "at a restaurant"), ("밥을 먹어요.", "eating.")]),
    v("병원", "Hospital", "byeongwon", "병원에 가요.", "Going to the hospital.",
      [("병원에", "to the hospital"), ("가요.", "going.")]),
    v("가게", "Store / Shop", "gage", "가게에서 사요.", "Buying at a store.",
      [("가게에서", "at a store"), ("사요.", "buying.")]),
    v("커피숍", "Coffee shop", "keopisyop", "커피숍에서 커피를 마셔요.", "Drinking coffee at a coffee shop.",
      [("커피숍에서", "at a coffee shop"), ("커피를", "coffee"), ("마셔요.", "drinking.")]),
    v("도서관", "Library", "doseogwan", "도서관에서 책을 읽어요.", "Reading books at the library.",
      [("도서관에서", "at the library"), ("책을", "books"), ("읽어요.", "reading.")]),
    v("공원", "Park", "gongwon", "공원에서 산책해요.", "Walking in the park.",
      [("공원에서", "in the park"), ("산책해요.", "walking.")]),
    v("화장실", "Restroom / Bathroom", "hwajangsil", "화장실이 어디예요?", "Where is the restroom?",
      [("화장실이", "restroom"), ("어디예요?", "where is?")]),
    v("방", "Room", "bang", "제 방이에요.", "This is my room.",
      [("제", "my"), ("방이에요.", "room.")]),
    v("책", "Book", "chaek", "책을 읽어요.", "Reading a book.",
      [("책을", "a book"), ("읽어요.", "reading.")]),
    v("휴대폰", "Cell phone", "hyuedaepon", "휴대폰이 있어요.", "I have a cell phone.",
      [("휴대폰이", "cell phone"), ("있어요.", "have.")]),
    v("컴퓨터", "Computer", "keompyuteo", "컴퓨터를 써요.", "Using a computer.",
      [("컴퓨터를", "a computer"), ("써요.", "using.")]),
    v("지갑", "Wallet", "jigap", "지갑을 잃어버렸어요.", "Lost the wallet.",
      [("지갑을", "the wallet"), ("잃어버렸어요.", "lost.")]),
    v("가방", "Bag", "gabang", "가방이 있어요.", "I have a bag.",
      [("가방이", "bag"), ("있어요.", "have.")]),
    v("자동차", "Car", "jadongcha", "자동차를 몰아요.", "Driving a car.",
      [("자동차를", "a car"), ("몰아요.", "driving.")]),
    v("버스", "Bus", "beoseu", "버스를 타요.", "Taking the bus.",
      [("버스를", "the bus"), ("타요.", "taking.")]),
    v("지하철", "Subway", "jihacheol", "지하철을 타요.", "Taking the subway.",
      [("지하철을", "the subway"), ("타요.", "taking.")]),
    v("택시", "Taxi", "taeksi", "택시를 타요.", "Taking a taxi.",
      [("택시를", "a taxi"), ("타요.", "taking.")]),
]


def create_model():
    """Create card model for vocabulary with color alignment support."""
    return genanki.Model(
        MODEL_ID,
        "Korean Vocab Model",
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
                "name": "Korean Vocab Card",
                "qfmt": """
<div style="text-align: center; font-size: 60px; padding: 40px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 60px; padding: 30px;">
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
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 650px; background: #fafafa; border-radius: 12px; border: 1px solid #e0e0e0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
    <div style="font-size: 22px; padding: 10px; line-height: 2; color: #2c3e50; font-weight: 500;">
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


def generate_deck(output_file="decks/04_korean_vocab_1_basic.apkg"):
    """Generate the basic vocabulary deck with color alignment."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "04. Korean Basic Vocabulary - 기본 어휘")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for entry in BASIC_VOCAB:
            if len(entry) == 6:
                korean, english, roman, example, ex_trans, word_pairs = entry
            else:
                korean, english, roman, example, ex_trans = entry
                word_pairs = None

            # Generate colored HTML
            if word_pairs:
                korean_colored, english_colored = create_colored_html(word_pairs)
            else:
                korean_colored, english_colored = "", ""

            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[korean, english, roman, example, ex_trans, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(BASIC_VOCAB)} vocabulary cards")
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
