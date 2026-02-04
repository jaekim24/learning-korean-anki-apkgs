#!/usr/bin/env python3
"""
Korean Verb Conjugation - Present Tense

Learn present tense conjugations for common Korean verbs.
Polite formal, Polite informal, Plain form, Casual.
Usage: python3 korean_verbs_present.py
"""

import sys
import os
import tempfile
import shutil

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import (
    generate_audio, created_audio_files, DECK_IDS, MODEL_IDS,
    create_colored_html
)

# Deck info
DECK_ID = DECK_IDS["verbs_present"]
MODEL_ID = MODEL_IDS["grammar"]


# Verbs with conjugations and word alignment examples:
# (dictionary_form, stem, type, polite_formal, polite_informal, plain, casual, meaning, word_pairs)
VERBS = [
    # ===== ㅏ verbs (add 아요/아) =====
    ("가다", "가", "regular", "갑니다", "가요", "간다", "가", "To go",
     [("학교에", "to school"), ("가요", "go")]),
    ("나가다", "나가", "regular", "나갑니다", "나가요", "나간다", "나가", "To go out",
     [("밖으로", "outside"), ("나가요", "go out")]),
    ("사다", "사", "regular", "삽니다", "사요", "산다", "사", "To buy",
     [("사과를", "apple"), ("사요", "buy")]),
    ("자다", "자", "regular", "잡니다", "자요", "잔다", "자", "To sleep",
     [("밤에", "at night"), ("자요", "sleep")]),
    ("서다", "서", "regular", "섭니다", "서요", "선다", "서", "To stand",
     [("버스에서", "from the bus"), ("서요", "stand")]),
    ("앉다", "앉", "regular", "앉습니다", "앉아요", "앉는다", "앉아", "To sit",
     [("의자에", "on the chair"), ("앉아요", "sit")]),
    ("찾다", "찾", "regular", "찾습니다", "찾아요", "찾는다", "찾아", "To find / look for",
     [("지갑을", "wallet"), ("찾아요", "look for")]),
    ("웃다", "웃", "regular", "웃습니다", "웃어요", "웃는다", "웃어", "To laugh",
     [("친구와", "with friend"), ("웃어요", "laugh")]),
    ("만나다", "만나", "regular", "만납니다", "만나요", "만난다", "만나", "To meet",
     [("친구를", "friend"), ("만나요", "meet")]),
    ("심심하다", "심심하", "하-djective", "심심합니다", "심심해요", "심심하다", "심심해", "To be bored",
     [("오늘은", "today"), ("심심해요", "am bored")]),

    # ===== ㅓ verbs (add 어요/어) =====
    ("먹다", "먹", "regular", "먹습니다", "먹어요", "먹는다", "먹어", "To eat",
     [("밥을", "rice/meal"), ("먹어요", "eat")]),
    ("보다", "보", "irregularㅂ", "봅니다", "봐요", "본다", "봐", "To see / watch",
     [("TV를", "TV"), ("봐요", "watch")]),
    ("죽다", "죽", "regular", "죽습니다", "죽어요", "죽는다", "죽어", "To die",
     [("식물이", "plant"), ("죽어요", "dies")]),
    ("살다", "살", "ㄹ-drop", "삽니다", "살아요", "산다", "살아", "To live",
     [("서울에", "in Seoul"), ("살아요", "live")]),
    ("들다", "들", "ㄹ-drop", "듭니다", "들어요", "든다", "들어", "To lift / enter",
     [("물건을", "object"), ("들어요", "lift")]),
    ("좋다", "좋", "ha-droppingㅎ", "좋습니다", "좋아요", "좋다", "좋아", "To be good",
     [("날씨가", "weather"), ("좋아요", "is good")]),
    ("나쁘다", "나쁘", "eu-droppingㅂ", "나쁩니다", "나빠요", "나쁘다", "나빠", "To be bad",
     [("날씨가", "weather"), ("나빠요", "is bad")]),
    ("크다", "크", "eu-droppingㅂ", "큽니다", "커요", "크다", "커", "To be big",
     [("집이", "house"), ("커요", "is big")]),
    ("작다", "작", "regular", "작습니다", "작아요", "작은다", "작아", "To be small",
     [("방이", "room"), ("작아요", "is small")]),
    ("어렵다", "어렵", "ㅂ-irregular", "어렵습니다", "어려워요", "어렵다", "어려워", "To be difficult",
     [("시험이", "exam"), ("어려워요", "is difficult")]),
    ("쉽다", "쉽", "ㅂ-irregular", "쉽습니다", "쉬워요", "쉽다", "쉬워", "To be easy",
     [("문제가", "problem"), ("쉬워요", "is easy")]),
    ("덥다", "덥", "ㅂ-irregular", "덥습니다", "더워요", "덥다", "더워", "To be hot (weather)",
     [("여름은", "summer"), ("더워요", "is hot")]),
    ("춥다", "춥", "ㅂ-irregular", "춥습니다", "추워요", "춥다", "추워", "To be cold (weather)",
     [("겨울은", "winter"), ("추워요", "is cold")]),
    ("많다", "많", "ㅂ-irregular", "많습니다", "많아요", "많다", "많아", "To be many",
     [("사람이", "people"), ("많아요", "are many")]),
    ("적다", "적", "ㅂ-irregular", "적습니다", "적어요", "적다", "적어", "To be few",
     [("돈이", "money"), ("적어요", "is little")]),

    # ===== ㅗ verbs (add 아요) =====
    ("오다", "오", "regular", "옵니다", "와요", "온다", "와", "To come",
     [("친구가", "friend"), ("와요", "comes")]),
    ("보내다", "보내", "regular", "보냅니다", "보내요", "보낸다", "보내", "To send",
     [("편지를", "letter"), ("보내요", "send")]),
    ("놀다", "놀", "regular", "놉니다", "놀아요", "논다", "놀아", "To play",
     [("공원에서", "at the park"), ("놀아요", "play")]),
    ("고프다", "고프", "eu-droppingㅂ", "고픕니다", "고파요", "고프다", "고파", "To be hungry (old)",
     [("배가", "stomach"), ("고파요", "am hungry")]),
    ("예쁘다", "예쁘", "eu-droppingㅂ", "예쁩니다", "예뻐요", "예쁘다", "예뻐", "To be pretty",
     [("꽃이", "flower"), ("예뻐요", "is pretty")]),
    ("기쁘다", "기쁘", "eu-droppingㅂ", "기쁩니다", "기뻐요", "기쁘다", "기뻐", "To be glad",
     [("마음이", "mind/heart"), ("기뻐요", "am glad")]),
    ("바쁘다", "바쁘", "eu-droppingㅂ", "바쁩니다", "바빠요", "바쁘다", "바빠", "To be busy",
     [("오늘은", "today"), ("바빠요", "am busy")]),

    # ===== ㅜ verbs (add 어요) =====
    ("주다", "주", "regular", "줍니다", "줘요", "준다", "줘", "To give",
     [("선물을", "gift"), ("줘요", "give")]),
    ("배우다", "배우", "regular", "배웁니다", "배워요", "배운다", "배워", "To learn",
     [("한국어를", "Korean"), ("배워요", "learn")]),
    ("운동하다", "운동하", "하-verb", "운동합니다", "운동해요", "운동한다", "운동해", "To exercise",
     [("매일", "every day"), ("운동해요", "exercise")]),
    ("전화하다", "전화하", "하-verb", "전화합니다", "전화해요", "전화한다", "전화해", "To call (phone)",
     [("친구에게", "to friend"), ("전화해요", "call")]),
    ("청소하다", "청소하", "하-verb", "청소합니다", "청소해요", "청소한다", "청소해", "To clean",
     [("방을", "room"), ("청소해요", "clean")]),
    ("요리하다", "요리하", "하-verb", "요리합니다", "요리해요", "요리한다", "요리해", "To cook",
     [("저녁을", "dinner"), ("요리해요", "cook")]),
    ("사랑하다", "사랑하", "하-verb", "사랑합니다", "사랑해요", "사랑한다", "사랑해", "To love",
     [("너를", "you"), ("사랑해", "love")]),
    ("좋아하다", "좋아하", "하-verb", "좋아합니다", "좋아해요", "좋아한다", "좋아해", "To like",
     [("김치를", "kimchi"), ("좋아해요", "like")]),
    ("싫어하다", "싫어하", "ㅅ-irregular", "싫어합니다", "싫어해요", "싫어한다", "싫어해", "To dislike",
     [("야채를", "vegetables"), ("싫어해요", "dislike")]),
    ("묻다", "묻", "regular", "묻습니다", "물어요", "묻는다", "물어", "To bury / ask",
     [("질문을", "question"), ("물어요", "ask")]),

    # ===== ㅡ verbs (add 어요) =====
    ("있다", "있", "regular", "있습니다", "있어요", "있다", "있어", "To exist / have",
     [("돈이", "money"), ("있어요", "have")]),
    ("없다", "없", "regular", "없습니다", "없어요", "없다", "없어", "To not exist / not have",
     [("시간이", "time"), ("없어요", "don't have")]),
    ("쓰다", "쓰", "regular", "씁니다", "써요", "쓴다", "써", "To write / use",
     [("편지를", "letter"), ("써요", "write")]),
    ("듣다", "듣", "ㄷ-irregular", "듣습니다", "들어요", "든다", "들어", "To hear / listen",
     [("음악을", "music"), ("들어요", "listen")]),
    ("걷다", "걷", "regular", "걷습니다", "걸어요", "걷는다", "걸어", "To walk",
     [("학교까지", "to school"), ("걸어요", "walk")]),
    ("깨닫다", "깨닫", "regular", "깨닫습니다", "깨달아요", "깨닫는다", "깨달아", "To realize",
     [("진심을", "truth"), ("깨달아요", "realize")]),
    ("슬프다", "슬프", "eu-droppingㅂ", "슬픕니다", "슬퍼요", "슬프다", "슬퍼", "To be sad",
     [("마음이", "heart"), ("슬퍼요", "am sad")]),

    # ===== ㅣ verbs (add 어요 → 여요/해요) =====
    ("가르치다", "가르치", "regular", "가릅니다", "가르쳐요", "가른다", "가르쳐", "To teach",
     [("학생을", "student"), ("가르쳐요", "teach")]),
    ("치다", "치", "regular", "칩니다", "쳐요", "친다", "쳐", "To hit / play (instrument)",
     [("피아노를", "piano"), ("쳐요", "play")]),
    ("마시다", "마시", "regular", "마십니다", "마셔요", "마신다", "마셔", "To drink",
     [("물을", "water"), ("마셔요", "drink")]),
    ("기다리다", "기다리", "regular", "기다립니다", "기다려요", "기다린다", "기다려", "To wait",
     [("버스를", "bus"), ("기다려요", "wait")]),
    ("깨다", "깨", "regular", "깹니다", "깨어요", "깬다", "깨어", "To break / wake",
     [("아침에", "in morning"), ("깨어요", "wake up")]),

    # ===== 하다 verbs (add 해요) =====
    ("하다", "하", "하-verb", "합니다", "해요", "한다", "해", "To do",
     [("숙제를", "homework"), ("해요", "do")]),
    ("공부하다", "공부하", "하-verb", "공부합니다", "공부해요", "공부한다", "공부해", "To study",
     [("영어를", "English"), ("공부해요", "study")]),
    ("일하다", "일하", "하-verb", "일합니다", "일해요", "일한다", "일해", "To work",
     [("회사에서", "at company"), ("일해요", "work")]),
    ("말하다", "말하", "하-verb", "말합니다", "말해요", "말한다", "말해", "To speak / say",
     [("진실을", "truth"), ("말해요", "say")]),
    ("생각하다", "생각하", "하-verb", "생각합니다", "생각해요", "생각한다", "생각해", "To think",
     [("계속", "continuously"), ("생각해요", "think")]),
    ("요청하다", "요청하", "하-verb", "요청합니다", "요청해요", "요청한다", "요청해", "To request",
     [("도움을", "help"), ("요청해요", "request")]),
    ("약속하다", "약속하", "하-verb", "약속합니다", "약속해요", "약속한다", "약속해", "To promise",
     [("약속을", "promise"), ("해요", "do")]),
    ("결정하다", "결정하", "하-verb", "결정합니다", "결정해요", "결정한다", "결정해", "To decide",
     [("마음을", "mind"), ("결정해요", "decide")]),
    ("준비하다", "준비하", "하-verb", "준비합니다", "준비해요", "준비한다", "준비해", "To prepare",
     [("시험을", "exam"), ("준비해요", "prepare")]),
    ("시작하다", "시작하", "하-verb", "시작합니다", "시작해요", "시작한다", "시작해", "To start",
     [("수업을", "class"), ("시작해요", "start")]),
    ("노래하다", "노래하", "하-verb", "노래합니다", "노래해요", "노래한다", "노래해", "To sing",
     [("노래를", "song"), ("해요", "do/sing")]),
    ("춤하다", "춤", "irregular", "춥니다", "춰요", "춘다", "춰", "To dance",
     [("춤을", "dance"), ("춰요", "dance")]),

    # ===== Adjectives (Descriptive verbs) =====
    ("행복하다", "행복하", "하-adj", "행복합니다", "행복해요", "행복한다", "행복해", "To be happy",
     [("저는", "I"), ("행복해요", "am happy")]),
    ("편하다", "편하", "ha-adj", "편합니다", "편해요", "편한다", "편해", "To be comfortable",
     [("의자가", "chair"), ("편해요", "is comfortable")]),
    ("불편하다", "불편하", "ha-adj", "불편합니다", "불편해요", "불편한다", "불편해", "To be uncomfortable",
     [("신발이", "shoes"), ("불편해요", "is uncomfortable")]),
    ("같다", "같", "regular", "같습니다", "같아요", "같다", "같아", "To be same / like",
     [("모양이", "shape"), ("같아요", "is same")]),
    ("다르다", "다르", "ㄹ-drop", "답니다", "달라요", "다르다", "달라", "To be different",
     [("생각이", "thought"), ("달라요", "is different")]),
    ("부르다", "부르", "ㄹ-drop", "부릅니다", "불러요", "른다", "불러", "To call / sing",
     [("노래를", "song"), ("불러요", "sing")]),
    ("마르다", "마르", "ㄹ-drop", "마릅니다", "말라요", "마른다", "말라", "To be dry",
     [("목이", "throat"), ("말라요", "is dry")]),
    ("무섭다", "무섭", "ㅂ-irregular", "무섭습니다", "무서워요", "무섭다", "무서워", "To be scary",
     [("영화가", "movie"), ("무서워요", "is scary")]),
    ("재미있다", "재미있", "ㅆ-irregular", "재미있습니다", "재미있어요", "재미있다", "재미있어", "To be fun / interesting",
     [("게임이", "game"), ("재미있어요", "is fun")]),
    ("맛있다", "맛있", "ㅆ-irregular", "맛있습니다", "맛있어요", "맛있다", "맛있어", "To be delicious",
     [("음식이", "food"), ("맛있어요", "is delicious")]),
    ("아프다", "아프", "eu-droppingㅂ", "아픕니다", "아파요", "아프다", "아파", "To be sick / hurt",
     [("머리가", "head"), ("아파요", "hurts")]),
    ("부럽다", "부럽", "ㅂ-irregular", "부럽습니다", "부러워요", "부럽다", "부러워", "To be envious",
     [("네가", "you"), ("부러워요", "am envious")]),
    ("즐겁다", "즐겁", "ㅂ-irregular", "즐겁습니다", "즐거워요", "즐겁다", "즐거워", "To be enjoyable",
     [("시간이", "time"), ("즐거워요", "is enjoyable")]),
    ("무겁다", "무겁", "ㅂ-irregular", "무겁습니다", "무거워요", "무겁다", "무거워", "To be heavy",
     [("가방이", "bag"), ("무거워요", "is heavy")]),
    ("가볍다", "가볍", "ㅂ-irregular", "가볍습니다", "가벼워요", "가볍다", "가벼워", "To be light",
     [("가방이", "bag"), ("가벼워요", "is light")]),
    ("뜨겁다", "뜨겁", "ㅂ-irregular", "뜨겁습니다", "뜨거워요", "뜨겁다", "뜨거워", "To be hot (temperature)",
     [("물이", "water"), ("뜨거워요", "is hot")]),
    ("차갑다", "차갑", "ㅂ-irregular", "차갑습니다", "차가워요", "차갑다", "차가워", "To be cold (temperature)",
     [("손이", "hand"), ("차가워요", "is cold")]),
    ("길다", "길", "ㄹ-drop", "깁니다", "길어요", "긴다", "길어", "To be long",
     [("다리가", "leg"), ("길어요", "is long")]),
    ("날씨가 좋다", "좋", "eu-droppingㅂ", "좋습니다", "좋아요", "좋다", "좋아", "Weather is good",
     [("날씨가", "weather"), ("좋아요", "is good")]),

    # ===== Special Irregular Verbs =====
    ("되다", "되", "되다-irregular", "됩니다", "돼요", "된다", "돼", "To become",
     [("선생님이", "teacher"), ("돼요", "become")]),
    ("돕다", "돕", "ㅂ-irregular-o", "돕습니다", "도와요", "돕는다", "도와", "To help (rare)",
     [("친구를", "friend"), ("도와요", "help")]),
    ("곱다", "곱", "ㅂ-irregular-o", "곱습니다", "고워요", "곱다", "고워", "To be beautiful (old)",
     [("꽃이", "flower"), ("고워요", "is beautiful")]),
]


def create_model():
    """Create card model for verb conjugations."""
    return genanki.Model(
        MODEL_ID,
        "Korean Verb Present Model",
        fields=[
            {"name": "DictionaryForm"},
            {"name": "PoliteFormal"},
            {"name": "PoliteInformal"},
            {"name": "PlainForm"},
            {"name": "Casual"},
            {"name": "Meaning"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Verb Present Card",
                "qfmt": """
<div style="padding: 15px; background: #f5f5f5; border-radius: 8px; margin: 10px; text-align: center;">
    <strong style="font-size: 16px; color: #666;">Dictionary Form (다-form)</strong>
</div>
<div style="text-align: center; font-size: 60px; padding: 30px;">
    {{DictionaryForm}}
</div>
<div style="text-align: center; font-size: 20px; color: #2196F3;">
    {{Meaning}}
</div>
                """,
                "afmt": """
<div style="padding: 12px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">Dictionary Form (다-form)</strong>
</div>
<div style="text-align: center; font-size: 55px; padding: 25px;">
    {{DictionaryForm}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
<div style="text-align: center; font-size: 20px; color: #2196F3; padding: 8px;">
    {{Meaning}}
</div>
<hr style="margin: 12px 0;">
<table style="width: 100%; border-collapse: collapse; margin: 10px 0;">
    <tr style="background: #e3f2fd;">
        <th style="padding: 10px; text-align: left; font-size: 14px;">Level</th>
        <th style="padding: 10px; text-align: left; font-size: 14px;">Conjugation</th>
    </tr>
    <tr style="border-bottom: 1px solid #ddd;">
        <td style="padding: 8px; font-weight: bold; color: #1976D2;">Polite Formal (스니다)</td>
        <td style="padding: 8px; font-size: 18px;">{{PoliteFormal}}</td>
    </tr>
    <tr style="border-bottom: 1px solid #ddd;">
        <td style="padding: 8px; font-weight: bold; color: #1976D2;">Polite Informal (아/어요)</td>
        <td style="padding: 8px; font-size: 18px;">{{PoliteInformal}}</td>
    </tr>
    <tr style="border-bottom: 1px solid #ddd;">
        <td style="padding: 8px; font-weight: bold; color: #1976D2;">Plain Form (다)</td>
        <td style="padding: 8px; font-size: 18px;">{{PlainForm}}</td>
    </tr>
    <tr>
        <td style="padding: 8px; font-weight: bold; color: #1976D2;">Casual (아/어)</td>
        <td style="padding: 8px; font-size: 18px;">{{Casual}}</td>
    </tr>
</table>
{{#KoreanColored}}
<hr style="margin: 12px 0;">
<div style="text-align: center; padding: 15px; margin: 10px auto; max-width: 600px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <strong style="font-size: 14px; color: #666;">Example Usage</strong>
    <div style="font-size: 24px; padding: 15px; line-height: 1.8;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
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


def generate_deck(output_file="decks/07_korean_verbs_present.apkg"):
    """Generate the present tense verbs deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "07. Korean Verbs Present - 현재시제")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for verb_data in VERBS:
            # Unpack verb data (with or without word_pairs)
            if len(verb_data) == 9:
                dict_form, _, _, formal, informal, plain, casual, meaning, word_pairs = verb_data
            else:
                dict_form, _, _, formal, informal, plain, casual, meaning = verb_data
                word_pairs = []

            # Generate colored HTML from word pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            # Generate audio for polite informal form
            audio_filename = generate_audio(informal, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[dict_form, formal, informal, plain, casual, meaning, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(VERBS)} verb cards")
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
