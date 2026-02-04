#!/usr/bin/env python3
"""
Korean Numbers Anki Deck Generator with Color-Coded Word Alignment

Covers:
1. Native Korean numbers (하나, 둘, 셋...) - used for counting, age, hours
2. Sino-Korean numbers (일, 이, 삼...) - used for dates, money, minutes, phone numbers
3. Counter words (개, 명, 잔, 장...) - used with numbers to count objects

Usage: python3 korean_numbers.py
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
DECK_ID = DECK_IDS["numbers"]
MODEL_ID = MODEL_IDS["word"]


# =============================================================================
# NATIVE KOREAN NUMBERS (1-99)
# Used for: counting objects, age, hours (when telling time)
# =============================================================================
NATIVE_NUMBERS = [
    # 1-10 (Basic numbers - learn these first!)
    ("하나", "One", "hana", "하나, 둘, 셋!", "One, two, three!",
     [("하나,", "One,"), ("둘,", "two,"), ("셋!", "three!")]),
    ("둘", "Two", "dul", "사과가 둘 있어요.", "There are two apples.",
     [("사과가", "Apples"), ("둘", "two"), ("있어요.", "are there.")]),
    ("셋", "Three", "set", "아이가 셋이에요.", "There are three children.",
     [("아이가", "Children"), ("셋이에요.", "are three.")]),
    ("넷", "Four", "net", "사람이 넷 명이에요.", "There are four people.",
     [("사람이", "People"), ("넷 명", "four"), ("이에요.", "are there.")]),
    ("다섯", "Five", "daseot", "연필이 다섯 개 있어요.", "There are five pencils.",
     [("연필이", "Pencils"), ("다섯 개", "five"), ("있어요.", "are there.")]),
    ("여섯", "Six", "yeoseot", "책이 여섯 권이에요.", "There are six books.",
     [("책이", "Books"), ("여섯 권", "six"), ("이에요.", "are there.")]),
    ("일곱", "Seven", "ilgop", "일곱 시에 만나요.", "Let's meet at 7 o'clock.",
     [("일곱 시에", "At 7 o'clock"), ("만나요.", "let's meet.")]),
    ("여덟", "Eight", "yeodeol", "여덟 명이 왔어요.", "Eight people came.",
     [("여덟 명", "Eight people"), ("왔어요.", "came.")]),
    ("아홉", "Nine", "ahop", "아홉 살이에요.", "I am nine years old.",
     [("아홉 살", "nine years old"), ("이에요.", "I am.")]),
    ("열", "Ten", "yeol", "열 개 주세요.", "Please give me ten.",
     [("열 개", "Ten items"), ("주세요.", "please give me.")]),

    # 11-19 (Ten + X)
    ("열하나", "Eleven", "yeolhana", "열하나 살이에요.", "I am eleven years old.",
     [("열하나", "Eleven"), ("살이에요.", "years old.")]),
    ("열둘", "Twelve", "yeoldul", "열둘 명이 와요.", "Twelve people are coming.",
     [("열둘 명", "Twelve people"), ("와요.", "are coming.")]),
    ("열셋", "Thirteen", "yeolset", "열셋 시예요.", "It is 13 o'clock.",
     [("열셋", "Thirteen"), ("시예요.", "o'clock.")]),
    ("열넷", "Fourteen", "yeolnet", "고기가 열넷 마리예요.", "There are fourteen animals.",
     [("고기가", "Animals"), ("열넷 마리", "fourteen"), ("예요.", "are there.")]),
    ("열다섯", "Fifteen", "yeoldaseot", "열다섯 장 주세요.", "Please give me fifteen sheets.",
     [("열다섯 장", "Fifteen sheets"), ("주세요.", "please.")]),
    ("열여섯", "Sixteen", "yeolyeoseot", "열여섯 살이에요.", "I am sixteen years old.",
     [("열여섯", "Sixteen"), ("살이에요.", "years old.")]),
    ("열일곱", "Seventeen", "yeolilgop", "열일곱 개예요.", "There are seventeen items.",
     [("열일곱", "Seventeen"), ("개예요.", "items.")]),
    ("열여덟", "Eighteen", "yeolyeodeol", "열여덟 명이에요.", "There are eighteen people.",
     [("열여덟", "Eighteen"), ("명이에요.", "people.")]),
    ("열아홉", "Nineteen", "yeolahop", "열아홉 시예요.", "It is 19 o'clock.",
     [("열아홉", "Nineteen"), ("시예요.", "o'clock.")]),

    # Multiples of 10 (20, 30, 40... 90)
    ("스물", "Twenty", "seumul", "스무 살이에요.", "I am twenty years old.",
     [("스무", "Twenty"), ("살이에요.", "years old.")]),
    ("서른", "Thirty", "seoreun", "서른 명이 왔어요.", "Thirty people came.",
     [("서른", "Thirty"), ("명이", "people"), ("왔어요.", "came.")]),
    ("마흔", "Forty", "maheun", "마흔 개 있어요.", "There are forty items.",
     [("마흔", "Forty"), ("개", "items"), ("있어요.", "there are.")]),
    ("쉰", "Fifty", "swin", "쉰 살이에요.", "I am fifty years old.",
     [("쉰", "Fifty"), ("살이에요.", "years old.")]),
    ("예순", "Sixty", "yesun", "예순 번 쳤어요.", "Hit sixty times.",
     [("예순", "Sixty"), ("번", "times"), ("쳤어요.", "hit.")]),
    ("일흔", "Seventy", "ilheun", "일흔 살이에요.", "I am seventy years old.",
     [("일흔", "Seventy"), ("살이에요.", "years old.")]),
    ("여든", "Eighty", "yeodeun", "여든 명이에요.", "There are eighty people.",
     [("여든", "Eighty"), ("명이에요.", "people.")]),
    ("아흔", "Ninety", "aheun", "아흔 아홉 살이에요.", "I am ninety-nine years old.",
     [("아흔 아홉", "ninety-nine"), ("살이에요.", "years old.")]),

    # Compound numbers (X-ten + Y)
    ("스물하나", "Twenty-one", "seumulhana", "스물하나 살이에요.", "I am twenty-one years old.",
     [("스물하나", "Twenty-one"), ("살이에요.", "years old.")]),
    ("서른다섯", "Thirty-five", "seoreundaseot", "서른다섯 명이에요.", "There are thirty-five people.",
     [("서른다섯", "Thirty-five"), ("명이에요.", "people.")]),
    ("마흔여덟", "Forty-eight", "maheunyeodeol", "마흔여덟 권이에요.", "There are forty-eight books.",
     [("마흔여덟", "Forty-eight"), ("권이에요.", "books.")]),
    ("쉰둘", "Fifty-two", "swindul", "쉰둘 살이에요.", "I am fifty-two years old.",
     [("쉰둘", "Fifty-two"), ("살이에요.", "years old.")]),
    ("예순셋", "Sixty-three", "yesunset", "예순셋 시예요.", "It is 63 o'clock.",
     [("예순셋", "Sixty-three"), ("시예요.", "o'clock.")]),
    ("일흔다섯", "Seventy-five", "ilheundaseot", "일흔다섯 마리예요.", "There are seventy-five animals.",
     [("일흔다섯", "Seventy-five"), ("마리예요.", "animals.")]),
    ("여덟아홉", "Eighty-nine", "yeodeunahop", "여든아홉 살이에요.", "I am eighty-nine years old.",
     [("여든아홉", "Eighty-nine"), ("살이에요.", "years old.")]),
    ("아흔여섯", "Ninety-six", "aheunyeoseot", "아흔여섯 장이에요.", "There are ninety-six sheets.",
     [("아흔여섯", "Ninety-six"), ("장이에요.", "sheets.")]),

    # Special note about counters
    ("한", "One (before counter)", "han", "한 개 주세요.", "Please give me one (item).",
     [("한 개", "One item"), ("주세요.", "please.")]),
    ("두", "Two (before counter)", "du", "두 명이에요.", "There are two people.",
     [("두 명", "Two people"), ("이에요.", "there are.")]),
    ("세", "Three (before counter)", "se", "세 잔 마셨어요.", "Drank three cups.",
     [("세 잔", "Three cups"), ("마셨어요.", "drank.")]),
    ("네", "Four (before counter)", "ne", "네 권 읽었어요.", "Read four books.",
     [("네 권", "Four books"), ("읽었어요.", "read.")]),
    ("스무", "Twenty (before counter)", "seumu", "스무 살이에요.", "I am twenty years old.",
     [("스무", "Twenty"), ("살이에요.", "years old.")]),
]


# =============================================================================
# SINO-KOREAN NUMBERS (1-1000+)
# Used for: dates, money, minutes, phone numbers, addresses, floors
# =============================================================================
SINO_NUMBERS = [
    # 1-10 (Basic - must memorize)
    ("일", "One (Sino-Korean)", "il", "일 월", "January",
     [("일", "First/1"), ("월", "month")]),
    ("이", "Two (Sino-Korean)", "i", "이 월", "February",
     [("이", "Second/2"), ("월", "month")]),
    ("삼", "Three (Sino-Korean)", "sam", "삼 월", "March",
     [("삼", "Third/3"), ("월", "month")]),
    ("사", "Four (Sino-Korean)", "sa", "사 월", "April",
     [("사", "Fourth/4"), ("월", "month")]),
    ("오", "Five (Sino-Korean)", "o", "오 월", "May",
     [("오", "Fifth/5"), ("월", "month")]),
    ("육", "Six (Sino-Korean)", "yuk", "육 월", "June",
     [("육", "Sixth/6"), ("월", "month")]),
    ("칠", "Seven (Sino-Korean)", "chil", "칠 월", "July",
     [("칠", "Seventh/7"), ("월", "month")]),
    ("팔", "Eight (Sino-Korean)", "pal", "팔 월", "August",
     [("팔", "Eighth/8"), ("월", "month")]),
    ("구", "Nine (Sino-Korean)", "gu", "구 월", "September",
     [("구", "Ninth/9"), ("월", "month")]),
    ("십", "Ten (Sino-Korean)", "sip", "십 월", "October",
     [("십", "Tenth/10"), ("월", "month")]),

    # 11-19
    ("십일", "Eleven (Sino-Korean)", "sibil", "11월 11일", "November 11th",
     [("11", "11"), ("월", "month"), ("11일", "11th day")]),
    ("십이", "Twelve (Sino-Korean)", "sibi", "12월", "December",
     [("십이", "Twelve"), ("월", "month")]),
    ("십삼", "Thirteen (Sino-Korean)", "sipsam", "13층", "13th floor",
     [("십삼", "Thirteen"), ("층", "floor")]),
    ("십사", "Fourteen (Sino-Korean)", "sipsa", "14번", "Number 14",
     [("십사", "Fourteen"), ("번", "number")]),
    ("십오", "Fifteen (Sino-Korean)", "sibo", "15분", "15 minutes",
     [("십오", "Fifteen"), ("분", "minutes")]),
    ("십육", "Sixteen (Sino-Korean)", "sipyuk", "16살", "16 years old (formal)",
     [("십육", "Sixteen"), ("살", "years old")]),
    ("십칠", "Seventeen (Sino-Korean)", "sipchil", "17일", "17th day",
     [("십칠", "Seventeen"), ("일", "day")]),
    ("십팔", "Eighteen (Sino-Korean)", "sippal", "18호", "Room 18",
     [("십팔", "Eighteen"), ("호", "room")]),
    ("십구", "Nineteen (Sino-Korean)", "sipgu", "19번지", "Address number 19",
     [("십구", "Nineteen"), ("번지", "address")]),

    # Multiples of 10 (20-90)
    ("이십", "Twenty (Sino-Korean)", "isip", "2000원", "2000 won",
     [("이천", "2000"), ("원", "won")]),
    ("삼십", "Thirty (Sino-Korean)", "samsip", "30분", "30 minutes",
     [("삼십", "Thirty"), ("분", "minutes")]),
    ("사십", "Forty (Sino-Korean)", "sasip", "40살", "40 years old (formal)",
     [("사십", "Forty"), ("살", "years old")]),
    ("오십", "Fifty (Sino-Korean)", "osip", "50번", "Number 50",
     [("오십", "Fifty"), ("번", "number")]),
    ("육십", "Sixty (Sino-Korean)", "yuksip", "60층", "60th floor",
     [("육십", "Sixty"), ("층", "floor")]),
    ("칠십", "Seventy (Sino-Korean)", "chilsip", "70%", "70 percent",
     [("칠십", "Seventy"), ("%", "percent")]),
    ("팔십", "Eighty (Sino-Korean)", "palsip", "80km", "80 kilometers",
     [("팔십", "Eighty"), ("km", "kilometers")]),
    ("구십", "Ninety (Sino-Korean)", "gusip", "90페이지", "Page 90",
     [("구십", "Ninety"), ("페이지", "page")]),

    # Hundreds
    ("백", "Hundred (Sino-Korean)", "baek", "100원", "100 won",
     [("백", "100"), ("원", "won")]),
    ("이백", "Two hundred", "ibaek", "200명", "200 people (formal)",
     [("이백", "200"), ("명", "people")]),
    ("삼백", "Three hundred", "sambaek", "300페이지", "Page 300",
     [("삼백", "300"), ("페이지", "page")]),
    ("사백", "Four hundred", "sabaek", "400일", "400 days",
     [("사백", "400"), ("일", "days")]),
    ("오백", "Five hundred", "obaek", "500원", "500 won",
     [("오백", "500"), ("원", "won")]),
    ("육백", "Six hundred", "yukbaek", "600번", "Number 600",
     [("육백", "600"), ("번", "number")]),
    ("칠백", "Seven hundred", "chilbaek", "700만원", "7 million won",
     [("칠백만", "7 million"), ("원", "won")]),
    ("팔백", "Eight hundred", "palbaek", "800년", "Year 800",
     [("팔백", "800"), ("년", "year")]),
    ("구백", "Nine hundred", "gubaek", "900미터", "900 meters",
     [("구백", "900"), ("미터", "meters")]),

    # Thousands
    ("천", "Thousand (Sino-Korean)", "cheon", "1000원", "1000 won",
     [("천", "1000"), ("원", "won")]),
    ("이천", "Two thousand", "icheon", "2024년", "Year 2024",
     [("이천", "2000"), ("이십사", "24"), ("년", "year")]),
    ("삼천", "Three thousand", "samcheon", "3000명", "3000 people (formal)",
     [("삼천", "3000"), ("명", "people")]),
    ("오천", "Five thousand", "ocheon", "5000원", "5000 won",
     [("오천", "5000"), ("원", "won")]),
    ("만", "Ten thousand", "man", "10000원", "10,000 won",
     [("만", "10,000"), ("원", "won")]),
    ("십만", "Hundred thousand", "sipman", "100000원", "100,000 won",
     [("십만", "100,000"), ("원", "won")]),
    ("백만", "One million", "baengman", "1000000원", "1,000,000 won",
     [("백만", "1 million"), ("원", "won")]),
    ("천만", "Ten million", "cheonman", "천만 원", "10 million won",
     [("천만", "10 million"), ("원", "won")]),
    ("억", "Hundred million", "eok", "1억", "100 million",
     [("일억", "100 million")]),
]


# =============================================================================
# COUNTER WORDS (Korean Counters)
# Used after numbers to count specific types of objects
# =============================================================================
COUNTER_WORDS = [
    # Common counters
    ("개", "General counter (things)", "gae", "사과 세 개", "Three apples",
     [("사과", "Apples"), ("세 개", "three (items)")]),
    ("명", "People (polite)", "myeong", "학생 다섯 명", "Five students",
     [("학생", "Students"), ("다섯 명", "five people")]),
    ("분", "People (honorific)", "bun", "선생님 두 분", "Two teachers (hon)",
     [("선생님", "Teachers"), ("두 분", "two (hon.)")]),
    ("마리", "Animals", "mari", "고기 네 마리", "Four animals",
     [("고기", "Animals"), ("네 마리", "four animals")]),
    ("잔", "Cups/glasses", "jan", "물 한 잔", "A glass of water",
     [("물", "Water"), ("한 잔", "one cup")]),
    ("병", "Bottles", "byeong", "맥주 두 병", "Two bottles of beer",
     [("맥주", "Beer"), ("두 병", "two bottles")]),
    ("장", "Flat objects (paper)", "jang", "종이 다섯 장", "Five sheets of paper",
     [("종이", "Paper"), ("다섯 장", "five sheets")]),
    ("권", "Books", "gwon", "책 두 권", "Two books",
     [("책", "Books"), ("두 권", "two books")]),
    ("층", "Floors", "cheung", "3층", "3rd floor",
     [("삼", "3"), ("층", "floor")]),
    ("번", "Times/occasions", "beon", "세 번", "Three times",
     [("세", "Three"), ("번", "times")]),
    ("살", "Age (Native)", "sal", "스무 살", "Twenty years old",
     [("스무", "Twenty"), ("살", "years old")]),
    ("세", "Age (Sino, formal)", "se", "구십세", "Ninety years old (formal)",
     [("구십", "Ninety"), ("세", "years old")]),

    # Time counters
    ("시", "O'clock (Native hours)", "si", "세 시", "3 o'clock",
     [("세", "Three"), ("시", "o'clock")]),
    ("분", "Minutes (Sino)", "bun", "십 분", "Ten minutes",
     [("십", "Ten"), ("분", "minutes")]),
    ("초", "Seconds", "cho", "오십 초", "Fifty seconds",
     [("오십", "Fifty"), ("초", "seconds")]),
    ("년", "Years (Sino)", "nyeon", "2024년", "Year 2024",
     [("이천이십사", "2024"), ("년", "year")]),
    ("월", "Months (Sino)", "wol", "삼 월", "March",
     [("삼", "3"), ("월", "month")]),
    ("일", "Days (Sino)", "il", "십오 일", "15th day",
     [("십오", "15"), ("일", "day")]),

    # Communication/Location counters
    ("번지", "Address/house number", "beonji", "123번지", "Address number 123",
     [("일이삼", "123"), ("번지", "address")]),
    ("호", "Room/hotel number", "ho", "304호", "Room 304",
     [("삼공사", "304"), ("호", "room")]),
    ("통", "Phone calls/emails", "tong", "전화 세 통", "Three phone calls",
     [("전화", "Phone calls"), ("세 통", "three")]),
    ("그릇", "Bowls of food", "geureut", "밥 한 그릇", "A bowl of rice",
     [("밥", "Rice/meal"), ("한 그릇", "one bowl")]),
    ("켤레", "Pairs (shoes, gloves)", "kyeolle", "양말 두 켤레", "Two pairs of socks",
     [("양말", "Socks"), ("두 켤레", "two pairs")]),
    ("대", "Vehicles/machines", "dae", "자동차 한 대", "One car",
     [("자동차", "Car"), ("한 대", "one")]),
    ("벌", "Suits/outfits", "beol", "옷 두 벌", "Two outfits",
     [("옷", "Clothes"), ("두 벌", "two outfits")]),
    ("송이", "Bunches (flowers)", "songi", "꽃 한 송이", "One flower",
     [("꽃", "Flower"), ("한 송이", "one")]),

    # Measurement counters
    ("원", "Won (currency)", "won", "오천 원", "5,000 won",
     [("오천", "5,000"), ("원", "won")]),
    ("미터", "Meters", "miteo", "100미터", "100 meters",
     [("백", "100"), ("미터", "meters")]),
    ("킬로미터", "Kilometers", "killomiteo", "3킬로미터", "3 kilometers",
     [("삼", "3"), ("킬로미터", "kilometers")]),
    ("킬로그램", "Kilograms", "killogeuraem", "5킬로그램", "5 kilograms",
     [("오", "5"), ("킬로그램", "kilograms")]),
    ("페이지", "Pages", "peiji", "50페이지", "Page 50",
     [("오십", "50"), ("페이지", "page")]),
    ("퍼센트", "Percent", "peoseonteu", "50퍼센트", "50 percent",
     [("오십", "50"), ("퍼센트", "percent")]),

    # Other useful counters
    ("잎", "Leaves", "ip", "나뭇잎 다섯 잎", "Five leaves",
     [("나뭇잎", "Leaves"), ("다섯 잎", "five")]),
    ("평", "Pyong (area unit)", "pyeong", "십평", "10 pyeong",
     [("십", "10"), ("평", "pyeong")]),
    ("학기", "Semesters", "hakgi", "이 학기", "Second semester",
     [("이", "Second"), ("학기", "semester")]),
    ("학년", "Grade in school", "haknyeon", "삼 학년", "Third grade",
     [("삼", "Third"), ("학년", "grade")]),
]


# =============================================================================
# COMBINED: NUMBER + COUNTER EXAMPLES
# Shows how numbers are used with counters in context
# =============================================================================
NUMBER_COUNTER_EXAMPLES = [
    # Native numbers with common counters
    ("한 개", "One item", "han gae", "연필 한 개 주세요.", "Please give me one pencil.",
     [("연필", "Pencil"), ("한 개", "one"), ("주세요.", "please.")]),
    ("두 명", "Two people", "du myeong", "학생이 두 명 왔어요.", "Two students came.",
     [("학생이", "Students"), ("두 명", "two"), ("왔어요.", "came.")]),
    ("세 잔", "Three cups", "se jan", "커피 세 잔 마셨어요.", "Drank three cups of coffee.",
     [("커피", "Coffee"), ("세 잔", "three cups"), ("마셨어요.", "drank.")]),
    ("네 권", "Four books", "ne gwon", "책을 네 권 샀어요.", "Bought four books.",
     [("책을", "Books"), ("네 권", "four"), ("샀어요.", "bought.")]),
    ("다섯 마리", "Five animals", "daseot mari", "고기를 다섯 마리 키워요.", "Raising five animals.",
     [("고기를", "Animals"), ("다섯 마리", "five"), ("키워요.", "raising.")]),

    # Time expressions (Native + Sino mix)
    ("세 시 십 분", "3:10 (time)", "se si sip bun", "지금 세 시 십 분이에요.", "It is 3:10 now.",
     [("세 시", "3 o'clock"), ("십 분", "10 minutes"), ("이에요.", "it is.")]),
    ("다섯 시 이십 분", "5:20", "daseot si isip bun", "다섯 시 이십 분에 만나요.", "Let's meet at 5:20.",
     [("다섯 시", "5 o'clock"), ("이십 분", "20 minutes"), ("에 만나요.", "meet at.")]),
    ("열두 시", "12 o'clock", "yeoldu si", "점심은 열두 시예요.", "Lunch is at 12 o'clock.",
     [("점심은", "Lunch"), ("열두 시", "12 o'clock"), ("예요.", "is.")]),
    ("한 시 삼십 분", "1:30", "han si samsip bun", "한 시 삼십 분에 일어나요.", "Wake up at 1:30.",
     [("한 시", "1 o'clock"), ("삼십 분", "30 minutes"), ("에 일어나요.", "wake at.")]),

    # Age expressions
    ("스무 살", "20 years old", "seumu sal", "저는 스무 살이에요.", "I am 20 years old.",
     [("저는", "I"), ("스무 살", "20 years old"), ("이에요.", "am.")]),
    ("서른다섯 살", "25 years old", "seoreundaseot sal", "언니는 서른다섯 살이에요.", "My sister is 25.",
     [("언니는", "My sister"), ("서른다섯 살", "25 years old"), ("이에요.", "is.")]),
    ("마흔 살", "40 years old", "maheun sal", "아빠가 마흔 살이에요.", "Dad is 40 years old.",
     [("아빠가", "Dad"), ("마흔 살", "40 years old"), ("이에요.", "is.")]),

    # Money (Sino-Korean)
    ("천 원", "1,000 won", "cheon won", "이거 천 원이에요.", "This is 1,000 won.",
     [("이거", "This"), ("천 원", "1,000 won"), ("이에요.", "is.")]),
    ("오천 원", "5,000 won", "ocheon won", "오천 원만 주세요.", "Please give just 5,000 won.",
     [("오천 원", "5,000 won"), ("만", "only"), ("주세요.", "please.")]),
    ("만 원", "10,000 won", "man won", "만 원 있어요?", "Do you have 10,000 won?",
     [("만 원", "10,000 won"), ("있어요?", "have?")]),
    ("일만 오천 원", "15,000 won", "ilmanocheon won", "가격이 일만 오천 원이에요.", "The price is 15,000 won.",
     [("가격이", "Price"), ("일만 오천 원", "15,000 won"), ("이에요.", "is.")]),

    # Dates (Sino-Korean)
    ("삼 월 십오 일", "March 15th", "sam wol sibo il", "생일이 삼 월 십오 일이에요.", "Birthday is March 15.",
     [("생일이", "Birthday"), ("삼 월", "March"), ("십오 일", "15th day"), ("이에요.", "is.")]),
    ("십이 월 이십오 일", "December 25th", "sibi wol isibo il", "12월 25일은 크리스마스예요.", "Dec 25 is Christmas.",
     [("십이 월", "December"), ("이십오 일", "25th day"), ("은", "is"), ("크리스마스예요.", "Christmas.")]),
    ("이천 이십사 년", "Year 2024", "icheon isipsa nyeon", "지금은 이천 이십사 년이에요.", "Now is the year 2024.",
     [("지금은", "Now"), ("이천 이십사 년", "2024"), ("이에요.", "is.")]),

    # Phone numbers and addresses (Sino-Korean)
    ("공일공", "010 (phone prefix)", "gongilgong", "제 번호는 010-1234-5678이에요.", "My number is 010-1234-5678.",
     [("제 번호는", "My number"), ("공일공", "010"), ("이에요.", "is.")]),
    ("일이삼 사", "1234", "ilisamsa", "1234번 버스", "Bus number 1234",
     [("일이삼사", "1234"), ("번", "number"), ("버스", "bus")]),
]


# =============================================================================
# NUMBER PRONUNCIATION RULES
# Special cases when numbers change form before counters
# =============================================================================
PRONUNCIATION_NOTES = [
    ("하나 → 한", "hana → han", "Before counters", "한 개", "One item",
     [("하나", "One"), ("→", "becomes"), ("한", "han (before counter)")]),
    ("둘 → 두", "dul → du", "Before counters", "두 명", "Two people",
     [("둘", "Two"), ("→", "becomes"), ("두", "du (before counter)")]),
    ("셋 → 세", "set → se", "Before counters", "세 잔", "Three cups",
     [("셋", "Three"), ("→", "becomes"), ("세", "se (before counter)")]),
    ("넷 → 네", "net → ne", "Before counters", "네 권", "Four books",
     [("넷", "Four"), ("→", "becomes"), ("네", "ne (before counter)")]),
    ("스물 → 스무", "seumul → seumu", "Before counters", "스무 살", "Twenty years old",
     [("스물", "Twenty"), ("→", "becomes"), ("스무", "seumu (before counter)")]),
    ("육 → 륙", "yuk → ryuk", "Before ㄹ sounds", "육 → 륙월", "Six → June (formal)",
     [("육", "Six"), ("→", "becomes"), ("륙", "ryuk (before ㄹ)")]),
]


def create_model():
    """Create card model for numbers with color alignment support."""
    return genanki.Model(
        MODEL_ID,
        "Korean Numbers Model",
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
                "name": "Korean Number Card",
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


def generate_deck(output_file="decks/03_korean_numbers.apkg"):
    """Generate the Korean numbers deck with color alignment."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "03. Korean Numbers - 한국어 숫자")

    # Combine all number data
    all_entries = NATIVE_NUMBERS + SINO_NUMBERS + COUNTER_WORDS + NUMBER_COUNTER_EXAMPLES + PRONUNCIATION_NOTES

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for entry in all_entries:
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

        print(f"Deck created: {output_file}")
        print(f"  - {len(NATIVE_NUMBERS)} Native Korean number cards (1-99+)")
        print(f"  - {len(SINO_NUMBERS)} Sino-Korean number cards (1-1억+)")
        print(f"  - {len(COUNTER_WORDS)} Counter word cards")
        print(f"  - {len(NUMBER_COUNTER_EXAMPLES)} Number + Counter example cards")
        print(f"  - {len(PRONUNCIATION_NOTES)} Pronunciation rule cards")
        print(f"  - {len(all_entries)} total cards")
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
