#!/usr/bin/env python3
"""
Korean Time, Days & Months Deck

Expressions for time, dates, days of week, months.
Usage: python3 korean_time.py
"""

import sys
import os
import tempfile
import shutil

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import genanki
from lib.korean_deck_base import generate_audio, created_audio_files, DECK_IDS, create_colored_html

# Deck info
DECK_ID = DECK_IDS["time"]
MODEL_ID = 1482931031


# Time vocabulary: (korean, english, romanization, usage, example, word_pairs)
# word_pairs is a list of (korean_word, english_word) tuples for color alignment
TIME_VOCAB = [
    # ===== DAYS OF WEEK =====
    ("월요일", "Monday", "woryoil", "Day 1 of the week", "월요일에 회의가 있어요.", [("월요일에", "On Monday"), ("회의가", "meeting"), ("있어요", "there is")]),
    ("화요일", "Tuesday", "hwayoil", "Day 2 of the week", "화요일에 운동해요.", [("화요일에", "On Tuesday"), ("운동해요", "exercise (I do)")]),
    ("수요일", "Wednesday", "suyoil", "Day 3 of the week", "수요일에 친구를 만나요.", [("수요일에", "On Wednesday"), ("친구를", "friend"), ("만나요", "meet")]),
    ("목요일", "Thursday", "mogyoil", "Day 4 of the week", "목요일은 바빠요.", [("목요일은", "Thursday"), ("바빠요", "busy (I am)")]),
    ("금요일", "Friday", "geumyoil", "Day 5 of the week", "금요일에 영화를 봐요.", [("금요일에", "On Friday"), ("영화를", "movie"), ("봐요", "watch (I do)")]),
    ("토요일", "Saturday", "toyoil", "Day 6 of the week", "토요일에 쉬어요.", [("토요일에", "On Saturday"), ("쉬어요", "rest (I do)")]),
    ("일요일", "Sunday", "iryoil", "Day 7 of the week", "일요일에 교회에 가요.", [("일요일에", "On Sunday"), ("교회에", "church"), ("가요", "go (I do)")]),
    ("주말", "Weekend", "jumal", "토요일 + 일요일", "주말에 뭐 해요?", [("주말에", "On the weekend"), ("뭐", "what"), ("해요?", "do (you)?")]),

    # ===== MONTHS =====
    ("1월", "January", "ilwol", "1st month", "1월은 추워요.", [("1월은", "January"), ("추워요", "cold (it is)")]),
    ("2월", "February", "iwol", "2nd month", "2월에 생일이에요.", [("2월에", "In February"), ("생일이에요", "birthday (it is my)")]),
    ("3월", "March", "samwol", "3rd month", "3월이 따뜻해요.", [("3월이", "March"), ("따뜻해요", "warm (it is)")]),
    ("4월", "April", "sawol", "4th month", "4월에 벚꽃이 피어요.", [("4월에", "In April"), ("벚꽃이", "cherry blossoms"), ("피어요", "bloom")]),
    ("5월", "May", "owol", "5th month", "5월에 가족 여행을 가요.", [("5월에", "In May"), ("가족", "family"), ("여행을", "trip"), ("가요", "go (we do)")]),
    ("6월", "June", "yuwol", "6th month", "6월에 비가 많이 와요.", [("6월에", "In June"), ("비가", "rain"), ("많이", "a lot"), ("와요", "comes")]),
    ("7월", "July", "chilwol", "7th month", "7월은 더워요.", [("7월은", "July"), ("더워요", "hot (it is)")]),
    ("8월", "August", "palwol", "8th month", "8월에 바다에 가요.", [("8월에", "In August"), ("바다에", "to the sea/beach"), ("가요", "go (we do)")]),
    ("9월", "September", "guwol", "9th month", "9월이 시원해요.", [("9월이", "September"), ("시원해요", "cool/refreshing (it is)")]),
    ("10월", "October", "siwol", "10th month", "10월에 단풍이 예뻐요.", [("10월에", "In October"), ("단풍이", "autumn foliage"), ("예뻐요", "beautiful/pretty (it is)")]),
    ("11월", "November", "sibilwol", "11th month", "11월이 추워지기 시작해요.", [("11월이", "November"), ("추워지기", "getting cold"), ("시작해요", "starts")]),
    ("12월", "December", "sibilwol", "12th month", "12월에 눈이 와요.", [("12월에", "In December"), ("눈이", "snow"), ("와요", "falls/comes")]),

    # ===== TIMES OF DAY =====
    ("아침", "Morning", "achim", "Breakfast time", "아침에 일어나요.", [("아침에", "In the morning"), ("일어나요", "wake up (I do)")]),
    ("점심", "Lunch / Noon", "jeomsim", "Lunch time", "점심을 먹었어요?", [("점심을", "lunch"), ("먹었어요?", "ate (did you)?")]),
    ("저녁", "Evening / Dinner", "jeonyeok", "Dinner time", "저녁에 집에 가요.", [("저녁에", "In the evening"), ("집에", "home"), ("가요", "go (I do)")]),
    ("밤", "Night", "bam", "Nighttime", "밤에 잠을 자요.", [("밤에", "At night"), ("잠을", "sleep"), ("자요", "sleep (I do)")]),
    ("새벽", "Dawn / Early morning", "saebyeok", "Before sunrise", "새벽 4시에 일어났어요.", [("새벽", "Dawn"), ("4시에", "at 4 o'clock"), ("일어났어요", "woke up")]),
    ("정오", "Noon", "jeongno", "12:00 PM", "정오에 점심을 먹어요.", [("정오에", "At noon"), ("점심을", "lunch"), ("먹어요", "eat (I do)")]),
    ("자정", "Midnight", "jajeong", "12:00 AM", "자정에 잠들었어요.", [("자정에", "At midnight"), ("잠들었어요", "fell asleep")]),

    # ===== TODAY, TOMORROW, YESTERDAY =====
    ("오늘", "Today", "oneul", "Current day", "오늘 날씨가 좋아요.", [("오늘", "Today"), ("날씨가", "weather"), ("좋아요", "good (it is)")]),
    ("내일", "Tomorrow", "naeil", "Next day", "내일 만나요.", [("내일", "Tomorrow"), ("만나요", "meet (let's/we do)")]),
    ("모레", "Day after tomorrow", "more", "2 days from now", "모레 시간 있어요?", [("모레", "Day after tomorrow"), ("시간", "time"), ("있어요?", "have (do you)?")]),
    ("그저께", "Day before yesterday", "geujeokke", "2 days ago", "그저께 왔어요.", [("그저께", "Day before yesterday"), ("왔어요", "came")]),
    ("어제", "Yesterday", "eoje", "Previous day", "어제 뭐 했어요?", [("어제", "Yesterday"), ("뭐", "what"), ("했어요?", "did (you)?")]),
    ("그제", "Day before yesterday", "geuje", "2 days ago", "그제 만났어요.", [("그제", "Day before yesterday"), ("만났어요", "met")]),

    # ===== THIS WEEK, NEXT WEEK =====
    ("이번 주", "This week", "ibeon ju", "Current week", "이번 주에 바빠요.", [("이번 주에", "This week"), ("바빠요", "busy (I am)")]),
    ("다음 주", "Next week", "daeum ju", "Following week", "다음 주에 시간 있어요?", [("다음 주에", "Next week"), ("시간", "time"), ("있어요?", "have (do you)?")]),
    ("지난 주", "Last week", "jinan ju", "Previous week", "지난 주에 여행 갔어요.", [("지난 주에", "Last week"), ("여행", "trip"), ("갔어요", "went")]),

    # ===== THIS YEAR, NEXT YEAR =====
    ("올해", "This year", "olhae", "Current year", "올해 2024년이에요.", [("올해", "This year"), ("2024년이에요", "is 2024")]),
    ("내년", "Next year", "naenyeon", "Following year", "내년에 졸업해요.", [("내년에", "Next year"), ("졸업해요", "graduate (I will)")]),
    ("작년", "Last year", "jaknyeon", "Previous year", "작년에 만났어요.", [("작년에", "Last year"), ("만났어요", "met")]),

    # ===== NOW, LATER, BEFORE =====
    ("지금", "Now", "jigeum", "At this moment", "지금 집에 가요.", [("지금", "Now"), ("집에", "home"), ("가요", "go (I do)")]),
    ("방금", "Just now / A moment ago", "banggeum", "Very recently", "방금 왔어요.", [("방금", "Just now"), ("왔어요", "came")]),
    ("나중에", "Later", "najung-e", "In the future", "나중에 전화할게요.", [("나중에", "Later"), ("전화할게요", "will call")]),
    ("곧", "Soon", "got", "In short time", "곧 도착해요.", [("곧", "Soon"), ("도착해요", "arrive (I will)")]),
    ("이따가", "Later today", "ittaga", "After current activity", "이따가 만나요.", [("이따가", "Later today"), ("만나요", "meet (let's)")]),
    ("이미", "Already", "imi", "Before now", "이미 끝났어요.", [("이미", "Already"), ("끝났어요", "finished/ended")]),
    ("아직", "Still / Yet", "ajik", "Until now", "아직 안 했어요.", [("아직", "Still/Yet"), ("안", "not"), ("했어요", "did")]),
    ("이제", "Now / From now on", "ije", "At this point", "이제 갈게요.", [("이제", "Now"), ("갈게요", "will go")]),
    ("전에", "Before", "jeone", "Earlier time", "전에 만난 적 있어요.", [("전에", "Before"), ("만난 적", "experience of meeting"), ("있어요", "have")]),
    ("후에", "After", "hue", "Later time", "식사 후에 커피를 마셔요.", [("식사 후에", "After meal"), ("커피를", "coffee"), ("마셔요", "drink (I do)")]),

    # ===== TIME WORDS =====
    ("시간", "Time / Hour", "sigan", "Time or hour", "시간이 없어요.", [("시간이", "time"), ("없어요", "there is no")]),
    ("분", "Minute", "bun", "60 minutes = 1 hour", "5분만 기다려주세요.", [("5분만", "5 minutes only"), ("기다려주세요", "please wait")]),
    ("초", "Second", "cho", "60 seconds = 1 minute", "잠깐만요, 1초만요.", [("잠깐만요", "Wait a moment"), ("1초만요", "just 1 second")]),
    ("아침식사", "Breakfast", "achimsiksa", "Morning meal", "아침식사를 먹었어요?", [("아침식사를", "breakfast"), ("먹었어요?", "ate (did you)?")]),
    ("점심식사", "Lunch", "jeomsimsiksa", "Noon meal", "점심식사를 같이 해요.", [("점심식사를", "lunch"), ("같이", "together"), ("해요", "let's do")]),
    ("저녁식사", "Dinner", "jeonyeoksiksa", "Evening meal", "저녁식사에 만나요.", [("저녁식사에", "For dinner"), ("만나요", "meet (let's)")]),
    ("야식", "Late night snack", "yasik", "Midnight food", "야식 먹지 마세요.", [("야식", "late night snack"), ("먹지 마세요", "don't eat")]),
    ("간식", "Snack", "gansik", "Between meals", "간식을 좋아해요.", [("간식을", "snacks"), ("좋아해요", "like (I do)")]),

    # ===== TIME EXPRESSIONS =====
    ("언제", "When", "eonje", "Question word for time", "언제 왔어요?", [("언제", "When"), ("왔어요?", "did you come?")]),
    ("몇 시", "What time", "myeot si", "Asking for time", "지금 몇 시예요?", [("지금", "Now"), ("몇 시", "what time"), ("예요?", "is it?")]),
    ("오전", "AM / Morning", "ojeon", "Before noon", "오전 9시에 회의가 있어요.", [("오전 9시에", "At 9 AM"), ("회의가", "meeting"), ("있어요", "there is")]),
    ("오후", "PM / Afternoon", "ohu", "After noon", "오후 3시에 만나요.", [("오후 3시에", "At 3 PM"), ("만나요", "meet (let's)")]),
    ("새벽", "Dawn / Early morning", "saebyeok", "2-5 AM", "새벽 5시에 기상해요.", [("새벽 5시에", "At 5 AM"), ("기상해요", "wake up (I do)")]),
    ("밤새", "All night", "bamsae", "Through the night", "밤새 공부했어요.", [("밤새", "All night"), ("공부했어요", "studied")]),
    ("낮", "Daytime", "nat", "During the day", "낮에 일하고 밤에 자요.", [("낮에", "During the day"), ("일하고", "work and"), ("밤에", "at night"), ("자요", "sleep")]),
    ("해", "Year", "hae", "Used in counting years", "올해는 2024년이에요.", [("올해는", "This year"), ("2024년이에요", "is 2024")]),
    ("달", "Month", "dal", "Alternative to 월", "이번 달에 갈 거예요.", [("이번 달에", "This month"), ("갈", "will go"), ("거예요", "thing/planned")]),
    ("주", "Week", "ju", "7 days", "한 주에 3번 운동해요.", [("한 주에", "In a week"), ("3번", "3 times"), ("운동해요", "exercise")]),
    ("날", "Day", "nal", "Date or day", "오늘 며칠이에요?", [("오늘", "Today"), ("며칠", "what date"), ("이에요?", "is it?")]),
    ("날짜", "Date", "naljja", "Calendar date", "날짜를 정했어요.", [("날짜를", "the date"), ("정했어요", "decided/fixed")]),

    # ===== TIME DURATION =====
    ("동안", "For / During", "dong-an", "Duration of time", "3시간 동안 공부했어요.", [("3시간", "3 hours"), ("동안", "for/during"), ("공부했어요", "studied")]),
    ("부터", "From (starting time)", "buteo", "Starting point", "9시부터 수업이에요.", [("9시부터", "From 9 o'clock"), ("수업이에요", "it is class")]),
    ("까지", "Until / By (time)", "kkaji", "Ending point", "6시까지 일해요.", [("6시까지", "Until 6 o'clock"), ("일해요", "work (I do)")]),
    ("마다", "Every", "mada", "Repeated time", "매일 운동해요.", [("매일", "every day"), ("운동해요", "exercise (I do)")]),

    # ===== FREQUENCY =====
    ("매일", "Every day", "maeil", "Each day", "매일 학교에 가요.", [("매일", "Every day"), ("학교에", "to school"), ("가요", "go (I do)")]),
    ("항상", "Always", "hangsang", "All the time", "항상 도와줘서 고마워요.", [("항상", "Always"), ("도와줘서", "for helping"), ("고마워요", "thank you")]),
    ("자주", "Often", "jaju", "Frequently", "자주 만나요.", [("자주", "Often"), ("만나요", "meet (we do)")]),
    ("가끔", "Sometimes", "gakkkeum", "Occasionally", "가끔 한국 음식을 먹어요.", [("가끔", "Sometimes"), ("한국 음식을", "Korean food"), ("먹어요", "eat (I do)")]),
    ("안", "Not / Never", "an", "Negative frequency", "안 가요.", [("안", "not"), ("가요", "go")]),
    ("별로", "Not really / Not much", "byeollo", "Not very often", "별로 안 좋아해요.", [("별로", "not really"), ("안", "not"), ("좋아해요", "like")]),
    ("전혀", "Not at all", "jeonhyeo", "Absolutely not", "전혀 몰라요.", [("전혀", "not at all"), ("몰라요", "don't know")]),
    ("이미", "Already", "imi", "Completed before now", "이미 갔어요.", [("이미", "Already"), ("갔어요", "went/left")]),
    ("여전히", "Still", "yeojeonhi", "Continuing state", "여전히 좋아해요.", [("여전히", "Still"), ("좋아해요", "like (I do)")]),

    # ===== EARLY / LATE =====
    ("일찍", "Early", "iljjik", "Before expected time", "오늘 일찍 왔어요.", [("오늘", "today"), ("일찍", "early"), ("왔어요", "came")]),
    ("늦게", "Late", "neutge", "After expected time", "오늘 늦게 왔어요.", [("오늘", "today"), ("늦게", "late"), ("왔어요", "came")]),
    ("늦잠", "Sleeping in", "neutjam", "Waking up late", "늦잠을 잤어요.", [("늦잠을", "oversleeping"), ("잤어요", "slept")]),
]


def create_model():
    """Create card model for time expressions with color alignment support."""
    return genanki.Model(
        MODEL_ID,
        "Korean Time Model",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Romanization"},
            {"name": "Usage"},
            {"name": "Example"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Time Card",
                "qfmt": """
<div style="text-align: center; font-size: 50px; padding: 40px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="text-align: center; font-size: 50px; padding: 30px;">
    {{Korean}}
</div>
<div style="text-align: center; padding: 15px;">
    {{Audio}}
</div>
{{#Romanization}}
<div style="text-align: center; font-size: 22px; color: #666; padding: 10px;">
    <em>{{Romanization}}</em>
</div>
{{/Romanization}}
<hr style="margin: 15px 0;">
<div style="text-align: center; font-size: 30px; color: #2196F3; font-weight: bold; padding: 10px;">
    {{English}}
</div>
{{#Usage}}
<div style="text-align: center; font-size: 16px; color: #666; padding: 8px; margin: 8px auto; max-width: 500px; background: #e3f2fd; border-radius: 6px;">
    <strong>Usage:</strong> {{Usage}}
</div>
{{/Usage}}
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 600px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 22px; padding: 10px; line-height: 1.8;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 16px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{^KoreanColored}}
{{#Example}}
<div style="text-align: center; font-size: 18px; padding: 12px; margin: 10px auto; max-width: 550px; background: #f9f9f9; border-radius: 8px;">
    <strong>Example:</strong> {{Example}}
</div>
{{/Example}}
{{/KoreanColored}}
                """,
            },
        ],
        css="""
.card {
    font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Nanum Gothic', sans-serif;
}
        """,
    )


def generate_deck(output_file="decks/05_korean_time.apkg"):
    """Generate the time deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "05. Korean Time & Dates - 시간과 날짜")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for item in TIME_VOCAB:
            # Handle both old format (5-tuple) and new format (6-tuple with word_pairs)
            if len(item) == 6:
                korean, english, roman, usage, example, word_pairs = item
            else:
                korean, english, roman, usage, example = item
                word_pairs = []

            # Generate colored HTML from word pairs
            korean_colored, english_colored = create_colored_html(word_pairs)

            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[korean, english, roman, usage, example, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(TIME_VOCAB)} time & date cards")
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
