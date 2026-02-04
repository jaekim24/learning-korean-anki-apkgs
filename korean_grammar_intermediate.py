#!/usr/bin/env python3
"""
Korean Intermediate Grammar Patterns

Essential intermediate grammar for more complex expressions.
Usage: python3 korean_grammar_intermediate.py
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
DECK_ID = DECK_IDS["grammar_intermediate"]
MODEL_ID = MODEL_IDS["grammar"]


# Grammar patterns: (pattern_name, pattern_formation, usage, examples, notes, word_pairs)
# word_pairs is optional: list of [(korean_word, english_word), ...]
GRAMMAR_PATTERNS = [
    # ===== CONNECTING ENDINGS =====
    ("-고", "Verb stem + 고",
     "And then / And (sequential actions)",
     "가고 싶어요 (want to go)\n친구를 만나고 영화를 봤어요 (Met friend and watched movie)",
     "Connects two actions. First action happens, then second.",
     [("가고", "go and"), ("싶어요", "want to")]),

    ("-고 나서", "Verb stem + 고 나서",
     "After doing (then)",
     "밥을 먹고 나서 공부해요 (Study after eating)\n일어나고 나서 샤워해요 (Shower after waking up)",
     "Emphasizes completion of first action before second.",
     [("먹고", "eat and"), ("나서", "after"), ("공부해요", "study")]),

    ("-고 싶다", "Verb stem + 고 싶다",
     "Want to do",
     "가고 싶어요 (Want to go)\n보고 싶어요 (Want to see / miss someone)",
     "Expresses desire to do something.",
     [("가고", "go"), ("싶어요", "want to")]),

    ("-지만", "Verb/Adj stem + 지만",
     "But / However",
     "비가 오지만 가요 (Going despite rain)\n작지만 좋아요 (Small but good)",
     "Connects contrasting ideas.",
     [("작지만", "small but"), ("좋아요", "good")]),

    ("-든지", "Verb/Adj stem + 든지",
     "Whether or / Either",
     "오든지 안 오든지 상관없어요 (Whether they come or not, it doesn't matter)\n사과든지 배든지 먹어요 (Eat either apple or pear)",
     "Shows options or indifference to choice.",
     [("오든지", "whether come"), ("안", "not"), ("오든지", "come"), ("상관없어요", "doesn't matter")]),

    ("-(이)랑", "Noun + (이)랑",
     "With / And (casual)",
     "친구랑 갔어요 (Went with friend)\n사과랑 바나나를 샀어요 (Bought apple and banana)",
     "Same as 과/와 but more casual. Means 'with' for people.",
     [("친구랑", "with friend"), ("갔어요", "went")]),

    ("-아/어서", "Verb/Adj stem + 아/어서",
     "Because / So (reason)",
     "배고파서 먹어요 (Eating because hungry)\n더워서 에어컨을 켜요 (Turn on AC because hot)",
     "Reason clause. Cannot use with imperative/proposition.",
     [("배고파서", "hungry so"), ("먹어요", "eat")]),

    # ===== REASON & CAUSE =====
    ("-(으)니까", "Verb/Adj stem + (으)니까",
     "Because / Since (stronger reason)",
     "시간이 없으니까 빨리 가요 (Going quickly because no time)\n배가 아프니까 병원에 가요 (Going to hospital because stomach hurts)",
     "Stronger reason. Can be used for suggestions.",
     [("시간이", "time"), ("없으니까", "no because"), ("빨리", "quickly"), ("가요", "go")]),

    ("-기 때문에", "Verb/Adj stem + 기 때문에",
     "Because of (formal)",
     "비가 오기 때문에 안 가요 (Not going because of rain)\n아프기 때문에 학교에 못 가요 (Can't go to school because of sickness)",
     "Formal reason marker. Noun + 때문이에도 works.",
     [("비가", "rain"), ("오기", "come"), ("때문에", "because"), ("안", "not"), ("가요", "go")]),

    ("때문에", "Noun + 때문에",
     "Because of (noun)",
     "교통 사고 때문에 늦었어요 (Was late because of traffic accident)\n날씨 때문에 안 가요 (Not going because of weather)",
     "Reason with a noun as cause.",
     [("교통 사고", "traffic accident"), ("때문에", "because of"), ("늦었어요", "was late")]),

    # ===== ABILITY & POSSIBILITY =====
    ("-을 수 있다", "Verb stem + 을 수 있다",
     "Can / Able to / Possible",
     "갈 수 있어요 (Can go)\n먹을 수 있어요 (Can eat)\n할 수 있어요 (Can do)",
     "After vowels: ㄹ 수 있다. After consonants: 을 수 있다.",
     [("갈", "go"), ("수", "able to"), ("있어요", "can")]),

    ("-을 수 없다", "Verb stem + 을 수 없다",
     "Cannot / Unable to",
     "갈 수 없어요 (Cannot go)\n먹을 수 없어요 (Cannot eat)",
     "Negative of -을 수 있다.",
     [("갈", "go"), ("수", "able to"), ("없어요", "cannot")]),

    ("-도 되다", "Verb stem + 도 되다",
     "It's okay to / May / Can",
     "들어가도 돼요 (May enter)\n먹어도 돼요 (It's okay to eat)\n와도 돼요 (Can come)",
     "Asking for permission or saying something is allowed.",
     [("들어가도", "enter"), ("돼요", "may/okay")]),

    ("-으면 안 되다", "Verb stem + (으)면 안 되다",
     "Must not / Should not",
     "들어가면 안 돼요 (Must not enter)\n먹으면 안 돼요 (Should not eat)",
     "Prohibition. Something is not allowed.",
     [("들어가면", "if enter"), ("안", "not"), ("돼요", "allowed")]),

    ("-어야 하다", "Verb stem + 어야 하다",
     "Must / Have to / Should",
     "가야 해요 (Must go)\n먹어야 해요 (Have to eat)\n해야 해요 (Must do)",
     "Obligation. Something must be done.",
     [("가야", "must go"), ("해요", "do/must")]),

    ("-어도 되다", "Verb stem + 어도 되다",
     "It's okay even if / May",
     "안 가도 돼요 (It's okay not to go)\n먹어도 돼요 (You may eat)",
     "Permission. Something is acceptable.",
     [("안", "not"), ("가도", "go even if"), ("돼요", "okay")]),

    # ===== EXPERIENCE =====
    ("-어 본 적이 있다", "Verb stem + 어 본 적이 있다",
     "Have done before / Have experience",
     "한국에 가 본 적이 있어요 (Have been to Korea before)\n김치를 먹어 본 적이 있어요 (Have eaten kimchi before)",
     "Talking about past experiences.",
     [("가", "go"), ("본", "tried"), ("적이", "experience"), ("있어요", "have")]),

    ("-어 본 적이 없다", "Verb stem + 어 본 적이 없다",
     "Have never done before",
     "한국에 가 본 적이 없어요 (Have never been to Korea)\n비행기를 타 본 적이 없어요 (Have never ridden a plane)",
     "No experience of doing something.",
     [("가", "go"), ("본", "tried"), ("적이", "experience"), ("없어요", "don't have")]),

    ("-어 보다", "Verb stem + 어 보다",
     "Try doing something",
     "입어 봐요 (Try it on - clothes)\n먹어 봐요 (Try eating)\n가 봐요 (Try going)",
     "Attempt something for the first time.",
     [("입어", "wear"), ("봐요", "try")]),

    # ===== PROGRESS & CONTINUATION =====
    ("-고 있다", "Verb stem + 고 있다",
     "Currently doing (action in progress)",
     "가고 있어요 (Currently going)\n먹고 있어요 (Currently eating)\n하고 있어요 (Currently doing)",
     "Present progressive - action happening now.",
     [("가고", "going"), ("있어요", "currently doing")]),

    ("-아/어 있다", "Verb stem + 아/어 있다",
     "State resulting from action",
     "앉아 있어요 (Sitting - state)\n서 있어요 (Standing - state)\n누워 있어요 (Lying down - state)",
     "Describes continuing state after action.",
     [("앉아", "sit"), ("있어요", "state of")]),

    ("-아/어 오다", "Verb stem + 아/어 오다",
     "Has been doing (coming up to now)",
     "살아 왔어요 (Have been living)\n일해 왔어요 (Have been working)",
     "Action continuing from past until now.",
     [("살아", "live"), ("왔어요", "have been doing")]),

    ("-아/어 가다", "Verb stem + 아/어 가다",
     "Continuing into future",
     "살아 가요 (Will continue living)\n공부해 가요 (Continue studying)",
     "Action continuing into the future.",
     [("살아", "live"), ("가요", "continue to")]),

    # ===== ATTEMPT =====
    ("-어 보다", "Verb stem + 어 보다",
     "Try / Attempt",
     "입어 봐요 (Try on - clothes)\n열어 봐요 (Try opening)\n가 봐요 (Try going)",
     "Attempt an action. Used when trying something.",
     [("열어", "open"), ("봐요", "try")]),

    # ===== CHANGE & TRANSFORMATION =====
    ("-아/어 지다", "Adj stem + 아/어 지다",
     "To become (passive change)",
     "커졌어요 (Got bigger - 크다)\n작아졌어요 (Got smaller - 작다)\n좋아졌어요 (Became good - 좋다)",
     "State change - something became different.",
     [("커", "big"), ("졌어요", "became")]),

    ("-게 되다", "Verb stem + 게 되다",
     "Came to be / Ended up (passive)",
     "가게 되었어요 (Ended up going)\n하게 되었어요 (Came to do)",
     "Something happened beyond control or circumstance.",
     [("가게", "go"), ("되었어요", "ended up")]),

    # ===== SIMULTANEOUS ACTIONS =====
    ("-으면서", "Verb stem + (으)면서",
     "While / At the same time",
     "먹으면서 봐요 (Watch while eating)\n일하면서 공부해요 (Study while working)",
     "Two actions happening simultaneously.",
     [("먹으면서", "while eating"), ("봐요", "watch")]),

    # ===== CONDITIONALS =====
    ("-으면", "Verb/Adj stem + (으)면",
     "If / When",
     "가면 만나요 (If go, will meet)\n오면 알려줘요 (If come, will let know)\n비가 오면 안 가요 (If rains, won't go)",
     "Conditional - if something happens, then...",
     [("가면", "if go"), ("만나요", "will meet")]),

    ("-든지", "Verb/Adj stem + 든지",
     "No matter / Regardless",
     "오든지 안 오든지 (Whether coming or not)\n비가 오든지 눈이 오든지 (Whether rain or snow)",
     "Shows that result doesn't depend on the condition.",
     [("오든지", "whether come"), ("안", "not"), ("오든지", "come")]),

    # ===== SELECTION & EMPHASIS =====
    ("-든지", "Noun + 이든지 / Noun + 든지",
     "Or / Either (any)",
     "물이든지 주스이든지 (Water or juice, either)\n사과든지 배든지 좋아요 (Like either apple or pear)",
     "Shows that any option is acceptable.",
     [("사과든지", "apple or"), ("배든지", "pear or"), ("좋아요", "like")]),

    ("-마다", "Noun + 마다",
     "Every / Each",
     "날마다 (Every day)\n사람마다 (Each person)\n주말마다 (Every weekend)",
     "Every single one without exception.",
     [("날마다", "every day")]),

    # ===== QUOTATION =====
    ("-다고(요)", "Statement + 다고(요)",
     "They said that / (I heard) that",
     "간다고 해요 (They say they're going)\n비 온다고 해요 (They say it's raining)",
     "Quoting someone's statement or hearsay.",
     [("간다고", "say going"), ("해요", "they say")]),

    ("-냐고(요)", "Question + 냐고(요)",
     "They asked if",
     "가냐고 물었어요 (Asked if going)\n맛있냐고 해요 (They asked if it's good)",
     "Quoting a question someone asked.",
     [("가냐고", "asked if go"), ("물었어요", "asked")]),

    ("-자고(요)", "Suggestion + 자고(요)",
     "They suggested to",
     "가자고 했어요 (They suggested to go)\n먹자고 해요 (They suggest eating)",
     "Quoting a suggestion someone made.",
     [("가자고", "let's go"), ("했어요", "suggested")]),

    # ===== CONTRAST & EMPHASIS =====
    ("-는 데", "Verb stem + 는 데",
     "But / However (contextual)",
     "가는 데 (Going, but...)\n먹는 데 (Eating, but...)",
     "Used when contrasting or giving context.",
     [("가는", "going"), ("데", "but/where")]),

    ("-기는 하다", "Verb stem + 기는 하다",
     "Do... but...",
     "가기는 해요 (Do go, but...)\n먹기는 해요 (Do eat, but...)",
     "Admit something while implying contrast.",
     [("가기는", "going"), ("해요", "do but...")]),

    # ===== PURPOSE =====
    ("-(으)러", "Verb stem + (으)러",
     "In order to / For the purpose of",
     "가려고요 (Going in order to...)\n먹으러 갔어요 (Went to eat)",
     "Expressing purpose or intention.",
     [("먹으러", "in order to eat"), ("갔어요", "went")]),

    ("-(으)러 가다/오다", "Verb stem + (으)러 가다/오다",
     "Go/Come in order to",
     "공부하러 가요 (Going to study)\n먹으러 왔어요 (Came to eat)",
     "Movement for purpose of doing something.",
     [("공부하러", "to study"), ("가요", "go")]),

    # ===== SIMILARITY =====
    ("-처럼", "Noun + 처럼",
     "Like / Similar to",
     "물처럼 (Like water)\n천사처럼 (Like an angel)\n아이처럼 (Like a child)",
     "Comparison - similar to something.",
     [("물처럼", "like water")]),

    ("-같이", "Noun + 같이",
     "Like / Together with",
     "친구같이 (Like a friend)\n함께 같이 (Together)",
     "Can mean 'like' or 'together'.",
     [("친구같이", "like a friend")]),

    # ===== TIME =====
    ("-(으)ㄹ 때", "Verb/Adj stem + (으)ㄹ 때",
     "When / At the time of",
     "갈 때 (When going)\n먹을 때 (When eating)\n작을 때 (When small)",
     "Point in time when something happens/exists.",
     [("갈", "go"), ("때", "when")]),

    ("-에", "Noun + 에",
     "At / On / In (time)",
     "7시에 (At 7 o'clock)\n월요일에 (On Monday)\n겨울에 (In winter)",
     "Time particle - when something happens.",
     [("7시에", "at 7 o'clock")]),

    # ===== SOURCE =====
    ("-에서부터", "Noun + 에서부터",
     "From (starting point emphasized)",
     "9시에서부터 (Starting from 9 o'clock)\n서울에서부터 (From Seoul)",
     "Emphasized starting point.",
     [("서울에서부터", "from Seoul")]),

    # ===== QUANTITIES =====
    ("-밖에", "Noun + 밖에 + Negative verb",
     "Only (with negative)",
     "하나밖에 없어요 (Have only one)\n조금밖에 안 먹었어요 (Ate only a little)",
     "Always used with negative verb.",
     [("하나밖에", "only one"), ("없어요", "don't have")]),

    ("-뿐이다", "Noun + 뿐이다",
     "Is only / Is nothing but",
     "하나뿐이에요 (Is only one)\n친구뿐이에요 (Is nothing but friend)",
     "Something is nothing but X.",
     [("하나뿐이에요", "is only one")]),

    # ===== DESIRE =====
    ("-고 싶다", "Verb stem + 고 싶다",
     "Want to",
     "가고 싶어요 (Want to go)\n보고 싶어요 (Want to see / miss)",
     "Desire to do something.",
     [("가고", "go"), ("싶어요", "want to")]),

    ("-고 싶어 하다", "Verb stem + 고 싶어 하다",
     "Someone wants to",
     "가고 싶어 해요 (He/She wants to go)",
     "Third person desire.",
     [("가고", "go"), ("싶어", "want"), ("해요", "he/she does")]),

    # ===== REQUEST =====
    ("-아/어 주다", "Verb stem + 아/어 주다",
     "Do for me / Please do",
     "가 주세요 (Please go)\n먹어 주세요 (Please eat)\n도와 주세요 (Please help)",
     "Requesting someone to do something.",
     [("가", "go"), ("주세요", "please do")]),

    ("-아/어 달라고 하다", "Verb stem + 아/어 달라고 하다",
     "Ask someone to do",
     "가 달라고 했어요 (Asked him/her to go)\n도와 달라고 해요 (Asking for help)",
     "Indirect request.",
     [("도와", "help"), ("달라고", "ask to do"), ("해요", "asking")]),

    # ===== PROHIBITION =====
    ("-지 마", "Verb stem + 지 마",
     "Don't",
     "가지 마세요 (Please don't go)\n먹지 마 (Don't eat)\n하지 마 (Don't do)",
     "Negative command or prohibition.",
     [("가지", "go"), ("마세요", "please don't")]),

    # ===== SUGGESTION =====
    ("-을까요?", "Verb stem + 을까요?",
     "Shall we? / Want to?",
     "갈까요? (Shall we go?)\n먹을까요? (Shall we eat?)\n할까요? (Shall we do?)",
     "Suggestion or question about doing something.",
     [("갈", "go"), ("까요", "shall we?")]),

    ("-을래요?", "Verb stem + 을래요?",
     "Want to? (casual suggestion)",
     "갈래요? (Want to go?)\n먹을래요? (Want to eat?)",
     "Casual suggestion or invitation.",
     [("갈", "go"), ("래요", "want to?")]),
]


def create_model():
    """Create card model for grammar patterns."""
    return genanki.Model(
        MODEL_ID,
        "Korean Intermediate Grammar Model",
        fields=[
            {"name": "PatternName"},
            {"name": "PatternFormation"},
            {"name": "Usage"},
            {"name": "Examples"},
            {"name": "Notes"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Grammar Card",
                "qfmt": """
<div style="padding: 12px; background: #f5f5f5; border-radius: 10px; margin: 12px; text-align: center;">
    <strong style="font-size: 16px; color: #666;">{{PatternName}}</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 30px;">
    {{PatternFormation}}
</div>
                """,
                "afmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">{{PatternName}}</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 25px;">
    {{PatternFormation}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
<hr style="margin: 12px 0;">
<div style="text-align: center; font-size: 16px; padding: 10px; margin: 10px auto; max-width: 550px; background: #e3f2fd; border-radius: 6px;">
    <strong>Usage:</strong> {{Usage}}
</div>
<div style="text-align: center; font-size: 15px; padding: 12px; margin: 12px auto; max-width: 600px; background: #f9f9f9; border-radius: 8px; white-space: pre-line;">
    <strong>Examples:</strong>
    {{Examples}}
</div>
{{#KoreanColored}}
<div style="text-align: center; padding: 15px; margin: 15px auto; max-width: 650px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 22px; padding: 12px; line-height: 1.8; color: #2c3e50; font-weight: 600;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 12px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{#Notes}}
<div style="text-align: center; font-size: 13px; color: #666; padding: 10px; margin: 10px auto; max-width: 550px; border-left: 4px solid #2196F3; background: #fffde7;">
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


def generate_deck(output_file="decks/12_korean_grammar_intermediate.apkg"):
    """Generate the intermediate grammar deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "12. Korean Intermediate Grammar - 중급 문법")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for pattern in GRAMMAR_PATTERNS:
            # Support both 5-tuple and 6-tuple formats
            # (pattern_name, pattern_formation, usage, examples, notes, word_pairs)
            if len(pattern) == 6:
                name, formation, usage, examples, notes, word_pairs = pattern
            else:
                name, formation, usage, examples, notes = pattern
                word_pairs = []

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            # Generate audio for pattern formation
            audio_text = formation.split('+')[0].strip() if '+' in formation else formation
            audio_filename = generate_audio(audio_text, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[name, formation, usage, examples, notes, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(GRAMMAR_PATTERNS)} grammar pattern cards")
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
