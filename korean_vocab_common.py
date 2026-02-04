#!/usr/bin/env python3
"""
Korean Common Vocabulary Anki Deck Generator

Creates Anki decks for the most commonly used Korean vocabulary.
Usage: python3 korean_vocab_common.py
"""

import genanki
import os
import tempfile
import shutil
from lib.korean_deck_base import (
    KoreanWordCard, add_word_note, create_word_model,
    MODEL_IDS, generate_audio
)

# Deck ID
DECK_ID = 1837523965
MODEL_ID = MODEL_IDS["word"]


# Personal Pronouns (1-15)
PRONOUNS = [
    KoreanWordCard("저", "I / me (humble)", "jeo", "저는 학생이에요 (I am a student)", "I am a student"),
    KoreanWordCard("나", "I / me (casual)", "na", "나는 갈 거야 (I will go)", "I will go"),
    KoreanWordCard("너", "you (casual)", "neo", "너는 어때? (How are you?)", "How are you?"),
    KoreanWordCard("당신", "you (formal / or spouse)", "dangsin", "당신은요? (And you?)", "And you?"),
    KoreanWordCard("우리", "we / us", "uri", "우리는 친구예요 (We are friends)", "We are friends"),
    KoreanWordCard("저희", "we / us (humble)", "jeohui", "저희 집 (Our house)", "Our house"),
    KoreanWordCard("이것", "this", "igeot", "이것 주세요 (Please give me this)", "Please give me this"),
    KoreanWordCard("그것", "that", "geugeot", "그것 알아요 (I know that)", "I know that"),
    KoreanWordCard("저것", "that over there", "jeogeot", "저것 봐요 (Look at that over there)", "Look at that over there"),
    KoreanWordCard("이분", "this person (polite)", "ibun", "이분은 제 선생님이에요 (This is my teacher)", "This is my teacher"),
    KoreanWordCard("그분", "that person (polite)", "geubun", "그분이 누구예요? (Who is that?)", "Who is that?"),
    KoreanWordCard("저분", "that person over there (polite)", "jeobun", "저분은 누구세요? (Who is that over there?)", "Who is that over there?"),
    KoreanWordCard("것", "thing / matter", "geot", "중요한 것 (important thing)", "important thing"),
    KoreanWordCard("무엇", "what", "mueos", "무엇을 원하세요? (What do you want?)", "What do you want?"),
    KoreanWordCard("뭐", "what (casual)", "mwo", "뭐예요? (What is it?)", "What is it?"),
]

# Family & People (16-35)
FAMILY = [
    KoreanWordCard("가족", "family", "gajog", "가족이 몇 명이에요? (How many family members?)", "How many family members?"),
    KoreanWordCard("아버지", "father (formal)", "abeoji", "아버지가 집에 계세요 (Father is at home)", "Father is at home"),
    KoreanWordCard("아빠", "dad (casual)", "appa", "아빠 사랑해요 (I love dad)", "I love dad"),
    KoreanWordCard("어머니", "mother (formal)", "eomeoni", "어머니께 드려요 (Give to mother)", "Give to mother"),
    KoreanWordCard("엄마", "mom (casual)", "eomma", "엄마가 요리해요 (Mom cooks)", "Mom cooks"),
    KoreanWordCard("부모님", "parents", "bumonim", "부모님과 함께 살아요 (I live with my parents)", "I live with my parents"),
    KoreanWordCard("형", "older brother (male speaker)", "hyeong", "형이 있어요 (I have an older brother)", "I have an older brother"),
    KoreanWordCard("오빠", "older brother (female speaker)", "oppa", "오빠가 도와줘요 (Oppa helps me)", "Oppa helps me"),
    KoreanWordCard("누나", "older sister (male speaker)", "nuna", "누나가 결혼했어요 (My older sister got married)", "My older sister got married"),
    KoreanWordCard("언니", "older sister (female speaker)", "eonni", "언니가 예뻐요 (My older sister is pretty)", "My older sister is pretty"),
    KoreanWordCard("남동생", "younger brother", "namdongsaeng", "남동생이 한 명 있어요 (I have one younger brother)", "I have one younger brother"),
    KoreanWordCard("여동생", "younger sister", "yeodongsaeng", "여동생이 귀여워요 (My younger sister is cute)", "My younger sister is cute"),
    KoreanWordCard("형제", "siblings / brothers", "hyeongje", "형제가 있어요 (I have siblings)", "I have siblings"),
    KoreanWordCard("자매", "sisters", "jamae", "자매가 두 명이에요 (There are two sisters)", "There are two sisters"),
    KoreanWordCard("아들", "son", "adeul", "아들이 하나 있어요 (I have one son)", "I have one son"),
    KoreanWordCard("딸", "daughter", "ttal", "딸이 셋이에요 (I have three daughters)", "I have three daughters"),
    KoreanWordCard("할아버지", "grandfather (paternal)", "harabeoji", "할아버지가 보고 싶어요 (I miss grandpa)", "I miss grandpa"),
    KoreanWordCard("할머니", "grandmother (paternal)", "halmeoni", "할머니랑 놀아요 (I play with grandma)", "I play with grandma"),
    KoreanWordCard("친척", "relatives", "chinchek", "친척을 만나요 (I meet relatives)", "I meet relatives"),
    KoreanWordCard("사람", "person", "saram", "좋은 사람 (good person)", "good person"),
]

# Numbers & Counting (36-55)
NUMBERS = [
    KoreanWordCard("하나", "one (native Korean)", "hana", "하나만 주세요 (Please give me one)", "Please give me one"),
    KoreanWordCard("둘", "two (native Korean)", "dul", "둘이 가요 (Two people go)", "Two people go"),
    KoreanWordCard("셋", "three (native Korean)", "set", "셋이에요 (It's three)", "It's three"),
    KoreanWordCard("넷", "four (native Korean)", "net", "넷이에요 (It's four)", "It's four"),
    KoreanWordCard("다섯", "five (native Korean)", "daseot", "다섯 명 (five people)", "five people"),
    KoreanWordCard("여섯", "six (native Korean)", "yeoseot", "여섯 시 (6 o'clock)", "6 o'clock"),
    KoreanWordCard("일곱", "seven (native Korean)", "ilgop", "일곱 번 (number seven)", "number seven"),
    KoreanWordCard("여덟", "eight (native Korean)", "yeodeol", "여덟 살 (8 years old)", "8 years old"),
    KoreanWordCard("아홉", "nine (native Korean)", "ahop", "아홉 시 (9 o'clock)", "9 o'clock"),
    KoreanWordCard("열", "ten (native Korean)", "yeol", "열 명 (ten people)", "ten people"),
    KoreanWordCard("일", "one (Sino-Korean)", "il", "1월 (January)", "January"),
    KoreanWordCard("이", "two (Sino-Korean)", "i", "이월 (February)", "February"),
    KoreanWordCard("삼", "three (Sino-Korean)", "sam", "삼월 (March)", "March"),
    KoreanWordCard("사", "four (Sino-Korean)", "sa", "사월 (April)", "April"),
    KoreanWordCard("오", "five (Sino-Korean)", "o", "오월 (May)", "May"),
    KoreanWordCard("육", "six (Sino-Korean)", "yuk", "유월 (June - pronounced yukwol)", "June"),
    KoreanWordCard("칠", "seven (Sino-Korean)", "chil", "칠월 (July)", "July"),
    KoreanWordCard("팔", "eight (Sino-Korean)", "pal", "팔월 (August)", "August"),
    KoreanWordCard("구", "nine (Sino-Korean)", "gu", "구월 (September)", "September"),
    KoreanWordCard("십", "ten (Sino-Korean)", "sip", "십월 (October)", "October"),
    KoreanWordCard("백", "hundred", "baek", "백 원 (100 won)", "100 won"),
]

# Time & Days (56-80)
TIME_DAYS = [
    KoreanWordCard("시간", "time / hour", "sigan", "시간이 없어요 (I don't have time)", "I don't have time"),
    KoreanWordCard("분", "minute", "bun", "5분 기다려주세요 (Please wait 5 minutes)", "Please wait 5 minutes"),
    KoreanWordCard("초", "second", "cho", "잠시만 (just a moment)", "just a moment"),
    KoreanWordCard("오늘", "today", "oneul", "오늘 만나요 (Let's meet today)", "Let's meet today"),
    KoreanWordCard("내일", "tomorrow", "naeil", "내일 뭐 해요? (What are you doing tomorrow?)", "What are you doing tomorrow?"),
    KoreanWordCard("모레", "day after tomorrow", "more", "모레 갈 거예요 (I'll go the day after tomorrow)", "I'll go the day after tomorrow"),
    KoreanWordCard("어제", "yesterday", "eoje", "어제 뭐 했어요? (What did you do yesterday?)", "What did you do yesterday?"),
    KoreanWordCard("그제", "day before yesterday", "geuje", "그제 만났어요 (I met him the day before yesterday)", "I met him the day before yesterday"),
    KoreanWordCard("아침", "morning", "achim", "아침을 먹어요 (I eat breakfast)", "I eat breakfast"),
    KoreanWordCard("점심", "lunch / noon", "jeomsim", "점심을 먹어요 (I eat lunch)", "I eat lunch"),
    KoreanWordCard("저녁", "evening / dinner", "jeonyeok", "저녁을 먹어요 (I eat dinner)", "I eat dinner"),
    KoreanWordCard("밤", "night", "bam", "밤에 자요 (I sleep at night)", "I sleep at night"),
    KoreanWordCard("새벽", "dawn / early morning", "saebyeok", "새벽에 일어나요 (I wake up at dawn)", "I wake up at dawn"),
    KoreanWordCard("주말", "weekend", "jumal", "주말에 뭐 해요? (What do you do on weekends?)", "What do you do on weekends?"),
    KoreanWordCard("평일", "weekday", "pyeongil", "평일에 바빠요 (I'm busy on weekdays)", "I'm busy on weekdays"),
    KoreanWordCard("월요일", "Monday", "woryoil", "월요일에 만나요 (Let's meet on Monday)", "Let's meet on Monday"),
    KoreanWordCard("화요일", "Tuesday", "hwayoil", "화요일이 싫어요 (I hate Tuesdays)", "I hate Tuesdays"),
    KoreanWordCard("수요일", "Wednesday", "suyoil", "수요일에 수업이 있어요 (I have class on Wednesday)", "I have class on Wednesday"),
    KoreanWordCard("목요일", "Thursday", "mogyoil", "목요일에 가요 (I'm going on Thursday)", "I'm going on Thursday"),
    KoreanWordCard("금요일", "Friday", "geumyoil", "금요일밤 (Friday night)", "Friday night"),
    KoreanWordCard("토요일", "Saturday", "toyoil", "토요일에 쉬어요 (I rest on Saturday)", "I rest on Saturday"),
    KoreanWordCard("일요일", "Sunday", "iryoil", "일요일에 교회에 가요 (I go to church on Sunday)", "I go to church on Sunday"),
    KoreanWordCard("지금", "now", "jigeum", "지금 가요 (I'm going now)", "I'm going now"),
    KoreanWordCard("방금", "just now / a moment ago", "banggeum", "방금 왔어요 (I just arrived)", "I just arrived"),
    KoreanWordCard("이제", "now / by now", "ije", "이제 갈 거예요 (I'll go now)", "I'll go now"),
    KoreanWordCard("곧", "soon", "got", "곧 올 거예요 (He'll come soon)", "He'll come soon"),
    KoreanWordCard("나중에", "later", "najung-e", "나중에 봐요 (See you later)", "See you later"),
]

# Places & Locations (81-105)
PLACES = [
    KoreanWordCard("집", "home / house", "jip", "집에 가요 (I'm going home)", "I'm going home"),
    KoreanWordCard("학교", "school", "hakgyo", "학교에 다녀요 (I attend school)", "I attend school"),
    KoreanWordCard("회사", "company / office", "hoesa", "회사에 가요 (I go to work)", "I go to work"),
    KoreanWordCard("식당", "restaurant", "sikdang", "식당에서 밥을 먹어요 (I eat at a restaurant)", "I eat at a restaurant"),
    KoreanWordCard("커피숍", "coffee shop", "keopisyop", "커피숍에서 커피를 마셔요 (I drink coffee at a cafe)", "I drink coffee at a cafe"),
    KoreanWordCard("카페", "cafe", "kapi", "카페에 가요 (I'm going to a cafe)", "I'm going to a cafe"),
    KoreanWordCard("병원", "hospital", "byeongwon", "병원에 가요 (I'm going to the hospital)", "I'm going to the hospital"),
    KoreanWordCard("약국", "pharmacy", "yakguk", "약국에서 약을 사요 (I buy medicine at the pharmacy)", "I buy medicine at the pharmacy"),
    KoreanWordCard("은행", "bank", "eunhaeng", "은행에 가요 (I'm going to the bank)", "I'm going to the bank"),
    KoreanWordCard("우체국", "post office", "ucheoguk", "우체국에서 편지를 보내요 (I send mail at the post office)", "I send mail at the post office"),
    KoreanWordCard("편의점", "convenience store", "pyeonijeom", "편의점에서 물을 사요 (I buy water at the convenience store)", "I buy water at the convenience store"),
    KoreanWordCard("마트", "mart / supermarket", "mateu", "마트에서 장을 봐요 (I grocery shop at the mart)", "I grocery shop at the mart"),
    KoreanWordCard("시장", "market", "sijang", "시장에 가요 (I'm going to the market)", "I'm going to the market"),
    KoreanWordCard("공항", "airport", "gonghang", "공항에 가요 (I'm going to the airport)", "I'm going to the airport"),
    KoreanWordCard("역", "station", "yeok", "역에서 만나요 (Let's meet at the station)", "Let's meet at the station"),
    KoreanWordCard("지하철역", "subway station", "jihacheolyeok", "지하철역이 어디예요? (Where is the subway station?)", "Where is the subway station?"),
    KoreanWordCard("버스정류장", "bus stop", "beoseojeongnyujang", "버스정류장에서 기다려요 (I wait at the bus stop)", "I wait at the bus stop"),
    KoreanWordCard("화장실", "restroom / bathroom", "hwajangsil", "화장실이 어디예요? (Where is the restroom?)", "Where is the restroom?"),
    KoreanWordCard("화장실", "toilet", "hwajangsil", "화장실에 가요 (I'm going to the restroom)", "I'm going to the restroom"),
    KoreanWordCard("도서관", "library", "doseogwan", "도서관에서 공부해요 (I study at the library)", "I study at the library"),
    KoreanWordCard("공원", "park", "gongwon", "공원에 산책하러 가요 (I go to the park for a walk)", "I go to the park for a walk"),
    KoreanWordCard("영화관", "movie theater", "yeonghwagwan", "영화관에서 영화를 봐요 (I watch a movie at the theater)", "I watch a movie at the theater"),
    KoreanWordCard("교회", "church", "gyohoe", "교회에 가요 (I go to church)", "I go to church"),
    KoreanWordCard("성당", "cathedral", "seongdang", "성당에 기도하러 가요 (I go to the cathedral to pray)", "I go to the cathedral to pray"),
    KoreanWordCard("절", "Buddhist temple", "jeol", "절에 가요 (I go to the temple)", "I go to the temple"),
]

# Food & Drink (106-135)
FOOD = [
    KoreanWordCard("음식", "food", "eumsig", "한국 음식을 좋아해요 (I like Korean food)", "I like Korean food"),
    KoreanWordCard("밥", "rice / meal", "bap", "밥을 먹었어요? (Did you eat?)", "Did you eat?"),
    KoreanWordCard("김치", "kimchi", "gimchi", "김치를 매일 먹어요 (I eat kimchi every day)", "I eat kimchi every day"),
    KoreanWordCard("비빔밥", "bibimbap", "bibimbap", "비빔밥을 좋아해요 (I like bibimbap)", "I like bibimbap"),
    KoreanWordCard("불고기", "bulgogi", "bulgogi", "불고기를 먹어요 (I eat bulgogi)", "I eat bulgogi"),
    KoreanWordCard("갈비", "ribs", "galbi", "갈비를 구워요 (I grill ribs)", "I grill ribs"),
    KoreanWordCard("삼겹살", "pork belly", "samgyeopsal", "삼겹살을 구워 먹어요 (I grill and eat pork belly)", "I grill and eat pork belly"),
    KoreanWordCard("라면", "ramyun / ramen", "ramyeon", "라면을 끓여요 (I cook ramyun)", "I cook ramyun"),
    KoreanWordCard("짜장면", "jjajangmyeon (black bean noodles)", "jjajangmyeon", "짜장면을 시켜요 (I order jjajangmyeon)", "I order jjajangmyeon"),
    KoreanWordCard("짬뽕", "jjamppong (spicy seafood noodles)", "jjamppong", "짬뽕을 좋아해요 (I like jjamppong)", "I like jjamppong"),
    KoreanWordCard("볶음밥", "fried rice", "bokkeumbap", "볶음밥을 먹어요 (I eat fried rice)", "I eat fried rice"),
    KoreanWordCard("김밥", "gimbap (seaweed rice rolls)", "gimbap", "김밥을 싸요 (I make gimbap)", "I make gimbap"),
    KoreanWordCard("떡볶이", "tteokbokki (spicy rice cakes)", "tteokbokki", "떡볶이를 매워요 (Tteokbokki is spicy)", "Tteokbokki is spicy"),
    KoreanWordCard("순대", "sundae (Korean blood sausage)", "sundae", "순대를 좋아해요 (I like sundae)", "I like sundae"),
    KoreanWordCard("국", "soup", "guk", "국을 끓여요 (I make soup)", "I make soup"),
    KoreanWordCard("찌개", "stew", "jjigae", "김치찌개를 끓여요 (I make kimchi stew)", "I make kimchi stew"),
    KoreanWordCard("된장찌개", "doenjang stew", "doenjangjjigae", "된장찌개를 좋아해요 (I like doenjang stew)", "I like doenjang stew"),
    KoreanWordCard("칼국수", "knife-cut noodles", "kalguksu", "칼국수를 먹어요 (I eat knife-cut noodles)", "I eat knife-cut noodles"),
    KoreanWordCard("잡채", "japchae (glass noodles)", "japchae", "잡채를 만들어요 (I make japchae)", "I make japchae"),
    KoreanWordCard("만두", "dumpling", "mandu", "만두를 찌어요 (I steam dumplings)", "I steam dumplings"),
    KoreanWordCard("빵", "bread", "ppang", "빵을 사요 (I buy bread)", "I buy bread"),
    KoreanWordCard("케이크", "cake", "keikeu", "케이크를 먹어요 (I eat cake)", "I eat cake"),
    KoreanWordCard("과자", "snacks", "gwaja", "과자를 좋아해요 (I like snacks)", "I like snacks"),
    KoreanWordCard("아이스크림", "ice cream", "aiseukeurim", "아이스크림을 먹어요 (I eat ice cream)", "I eat ice cream"),
    KoreanWordCard("물", "water", "mul", "물을 마셔요 (I drink water)", "I drink water"),
    KoreanWordCard("커피", "coffee", "keopi", "커피를 마셔요 (I drink coffee)", "I drink coffee"),
    KoreanWordCard("녹차", "green tea", "nokcha", "녹차를 마셔요 (I drink green tea)", "I drink green tea"),
    KoreanWordCard("우유", "milk", "uyu", "우유를 마셔요 (I drink milk)", "I drink milk"),
    KoreanWordCard("주스", "juice", "juseu", "주스를 마셔요 (I drink juice)", "I drink juice"),
    KoreanWordCard("콜라", "cola", "kolla", "콜라를 마셔요 (I drink cola)", "I drink cola"),
    KoreanWordCard("맥주", "beer", "maekju", "맥주를 마셔요 (I drink beer)", "I drink beer"),
    KoreanWordCard("소주", "soju", "soju", "소주를 마셔요 (I drink soju)", "I drink soju"),
]

# Adjectives & Descriptions (136-165)
ADJECTIVES = [
    KoreanWordCard("좋다", "good / to be good", "jota", "좋아요 (It's good)", "It's good"),
    KoreanWordCard("나쁘다", "bad / to be bad", "nappeuda", "나빠요 (It's bad)", "It's bad"),
    KoreanWordCard("크다", "big / large", "keuda", "커요 (It's big)", "It's big"),
    KoreanWordCard("작다", "small / little", "jakda", "작아요 (It's small)", "It's small"),
    KoreanWordCard("많다", "many / much", "manta", "많아요 (There are many)", "There are many"),
    KoreanWordCard("적다", "few", "jeokda", "적어요 (There are few)", "There are few"),
    KoreanWordCard("길다", "long", "gilda", "길어요 (It's long)", "It's long"),
    KoreanWordCard("짧다", "short", "jjalda", "짧아요 (It's short)", "It's short"),
    KoreanWordCard("넓다", "wide / spacious", "neolbda", "넓어요 (It's spacious)", "It's spacious"),
    KoreanWordCard("좁다", "narrow", "jobda", "좁아요 (It's narrow)", "It's narrow"),
    KoreanWordCard("높다", "high / tall", "nopda", "높아요 (It's high)", "It's high"),
    KoreanWordCard("낮다", "low", "najda", "낮아요 (It's low)", "It's low"),
    KoreanWordCard("무겁다", "heavy", "mugeopda", "무거워요 (It's heavy)", "It's heavy"),
    KoreanWordCard("가볍다", "light", "gabyeopda", "가버워요 (It's light)", "It's light"),
    KoreanWordCard("예쁘다", "pretty", "yeppeuda", "예뻐요 (She's pretty)", "She's pretty"),
    KoreanWordCard("못생기다", "ugly", "motsaenggida", "못생겼어요 (He's ugly)", "He's ugly"),
    KoreanWordCard("깨끗하다", "clean", "kkaekkeutada", "깨끗해요 (It's clean)", "It's clean"),
    KoreanWordCard("더럽다", "dirty", "dereopda", "더러워요 (It's dirty)", "It's dirty"),
    KoreanWordCard("맛있다", "delicious", "maditda", "맛있어요 (It's delicious)", "It's delicious"),
    KoreanWordCard("맛없다", "not tasty", "madeopda", "맛없어요 (It's not tasty)", "It's not tasty"),
    KoreanWordCard("덥다", "hot (weather)", "deopda", "더워요 (It's hot)", "It's hot"),
    KoreanWordCard("춥다", "cold (weather)", "chupda", "추워요 (It's cold)", "It's cold"),
    KoreanWordCard("따뜻하다", "warm", "ttatteutada", "따뜻해요 (It's warm)", "It's warm"),
    KoreanWordCard("시원하다", "cool / refreshing", "siwonhada", "시원해요 (It's cool)", "It's cool"),
    KoreanWordCard("재미있다", "fun / interesting", "jaemiitda", "재미있어요 (It's fun)", "It's fun"),
    KoreanWordCard("재미없다", "boring / not fun", "jaemieopda", "재미없어요 (It's boring)", "It's boring"),
    KoreanWordCard("어렵다", "difficult / hard", "eoryeopda", "어려워요 (It's difficult)", "It's difficult"),
    KoreanWordCard("쉽다", "easy", "swipda", "쉬워요 (It's easy)", "It's easy"),
    KoreanWordCard("busy", "busy", "bappeuda", "바빠요 (I'm busy)", "I'm busy"),
    KoreanWordCard("편하다", "comfortable", "pyeonhada", "편해요 (It's comfortable)", "It's comfortable"),
    KoreanWordCard("불편하다", "uncomfortable", "bulpyeonhada", "불편해요 (It's uncomfortable)", "It's uncomfortable"),
]

# Common Verbs (166-195)
COMMON_VERBS = [
    KoreanWordCard("가다", "to go", "gada", "학교에 가요 (I go to school)", "I go to school"),
    KoreanWordCard("오다", "to come", "oda", "친구가 와요 (A friend comes)", "A friend comes"),
    KoreanWordCard("먹다", "to eat", "meokda", "밥을 먹어요 (I eat rice/meal)", "I eat a meal"),
    KoreanWordCard("마시다", "to drink", "masida", "물을 마셔요 (I drink water)", "I drink water"),
    KoreanWordCard("자다", "to sleep", "jada", "9시에 자요 (I sleep at 9)", "I sleep at 9"),
    KoreanWordCard("일어나다", "to wake up / get up", "ireonada", "7시에 일어나요 (I wake up at 7)", "I wake up at 7"),
    KoreanWordCard("보다", "to see / watch", "boda", "영화를 봐요 (I watch a movie)", "I watch a movie"),
    KoreanWordCard("듣다", "to hear / listen", "deutda", "음악을 들어요 (I listen to music)", "I listen to music"),
    KoreanWordCard("읽다", "to read", "ikda", "책을 읽어요 (I read a book)", "I read a book"),
    KoreanWordCard("쓰다", "to write", "sseuda", "편지를 써요 (I write a letter)", "I write a letter"),
    KoreanWordCard("하다", "to do", "hada", "숙제를 해요 (I do homework)", "I do homework"),
    KoreanWordCard("말하다", "to speak / say", "malhada", "한국어를 말해요 (I speak Korean)", "I speak Korean"),
    KoreanWordCard("공부하다", "to study", "gongbuhada", "공부해요 (I study)", "I study"),
    KoreanWordCard("일하다", "to work", "ilhada", "일해요 (I work)", "I work"),
    KoreanWordCard("살다", "to live", "salda", "서울에 살아요 (I live in Seoul)", "I live in Seoul"),
    KoreanWordCard("만나다", "to meet", "mannada", "친구를 만나요 (I meet a friend)", "I meet a friend"),
    KoreanWordCard("사다", "to buy", "sada", "옷을 사요 (I buy clothes)", "I buy clothes"),
    KoreanWordCard("팔다", "to sell", "palda", "옷을 팔아요 (I sell clothes)", "I sell clothes"),
    KoreanWordCard("배우다", "to learn", "baeuda", "한국어를 배워요 (I learn Korean)", "I learn Korean"),
    KoreanWordCard("가르치다", "to teach", "fareuchida", "학생들을 가르쳐요 (I teach students)", "I teach students"),
    KoreanWordCard("알다", "to know", "alda", "알아요 (I know)", "I know"),
    KoreanWordCard("모르다", "to not know", "moreuda", "몰라요 (I don't know)", "I don't know"),
    KoreanWordCard("이해하다", "to understand", "ihaehada", "이해해요 (I understand)", "I understand"),
    KoreanWordCard("좋아하다", "to like", "joahada", "음악을 좋아해요 (I like music)", "I like music"),
    KoreanWordCard("싫어하다", "to hate / dislike", "sireohada", "싫어해요 (I hate it)", "I hate it"),
    KoreanWordCard("사랑하다", "to love", "saranghada", "너를 사랑해 (I love you)", "I love you"),
    KoreanWordCard("원하다", "to want", "wonhada", "원해요 (I want it)", "I want it"),
    KoreanWordCard("필요하다", "to need", "piryohada", "필요해요 (I need it)", "I need it"),
    KoreanWordCard("찾다", "to find / look for", "chatda", "찾아요 (I'm looking for it)", "I'm looking for it"),
    KoreanWordCard("기다리다", "to wait", "gidarida", "기다려요 (I'm waiting)", "I'm waiting"),
]

# Question Words & Connectors (196-220)
QUESTION_WORDS = [
    KoreanWordCard("누구", "who", "nugu", "누구예요? (Who is it?)", "Who is it?"),
    KoreanWordCard("무엇", "what", "mueos", "무엇을 해요? (What are you doing?)", "What are you doing?"),
    KoreanWordCard("뭐", "what (casual)", "mwo", "뭐예요? (What is it?)", "What is it?"),
    KoreanWordCard("어디", "where", "eodi", "어디에 가요? (Where are you going?)", "Where are you going?"),
    KoreanWordCard("언제", "when", "eonje", "언제 와요? (When are you coming?)", "When are you coming?"),
    KoreanWordCard("어떻게", "how", "eotteoke", "어떻게 가요? (How do you go?)", "How do you go?"),
    KoreanWordCard("왜", "why", "wae", "왜 그래요? (Why is that?)", "Why is that?"),
    KoreanWordCard("몇", "how many / what number", "myeot", "몇 명이에요? (How many people?)", "How many people?"),
    KoreanWordCard("어느", "which", "eoneu", "어느 거예요? (Which one is it?)", "Which one is it?"),
    KoreanWordCard("어떤", "what kind of / which", "eotteon", "어떤 음식을 좋아해요? (What kind of food do you like?)", "What kind of food do you like?"),
    KoreanWordCard("그리고", "and", "geurigo", "사과 그리고 배 (apple and pear)", "apple and pear"),
    KoreanWordCard("그렇지만", "but / however", "geureochiman", "예쁘다. 그렇지만 비싸다 (It's pretty. But it's expensive)", "It's pretty. But it's expensive"),
    KoreanWordCard("그런데", "however / but", "geureonde", "배고픈데 그런데 음식이 없어 (I'm hungry but there's no food)", "I'm hungry but there's no food"),
    KoreanWordCard("또", "again / also", "tto", "또 오세요 (Come again)", "Come again"),
    KoreanWordCard("아주", "very", "aju", "아주 좋아요 (It's very good)", "It's very good"),
    KoreanWordCard("정말", "really / truly", "jeongmal", "정말 좋아요 (It's really good)", "It's really good"),
    KoreanWordCard("너무", "too / very", "neomu", "너무 비싸요 (It's too expensive)", "It's too expensive"),
    KoreanWordCard("아직", "still / yet", "ajik", "아직 안 왔어요 (He hasn't come yet)", "He hasn't come yet"),
    KoreanWordCard("이미", "already", "imi", "이미 왔어요 (He already came)", "He already came"),
    KoreanWordCard("벌써", "already", "beolsseo", "벌써 12시예요 (It's already 12 o'clock)", "It's already 12 o'clock"),
    KoreanWordCard("조금", "a little", "jogeum", "조금 기다려주세요 (Please wait a little)", "Please wait a little"),
    KoreanWordCard("약간", "a few / some", "yakgan", "약간 있어요 (I have some)", "I have some"),
    KoreanWordCard("약속", "promise / appointment", "yaksok", "약속을 지켜요 (I keep the promise)", "I keep the promise"),
    KoreanWordCard("문제", "problem", "munje", "문제가 없어요 (There's no problem)", "There's no problem"),
    KoreanWordCard("해결", "solution", "haegyeol", "해결했어요 (I solved it)", "I solved it"),
    KoreanWordCard("생각", "thought / thinking", "saenggak", "생각해 봐요 (Let me think)", "Let me think"),
]


def generate_deck(output_file="decks/17_korean_vocab_common.apkg"):
    """Generate the Anki deck with common vocabulary."""
    model = create_word_model()
    deck = genanki.Deck(DECK_ID, "17. Korean Common Vocab - 기본 어휘")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        notes = []

        # Add all vocabulary cards
        all_cards = (
            PRONOUNS + FAMILY + NUMBERS + TIME_DAYS + PLACES + FOOD +
            ADJECTIVES + COMMON_VERBS + QUESTION_WORDS
        )

        for card in all_cards:
            note = add_word_note(deck, model, card, audio_dir)
            deck.add_note(note)
            notes.append(note)

        # Generate the package
        package = genanki.Package(deck)

        # Add media files
        media_files = [f for f in os.listdir(audio_dir) if f.endswith('.mp3')]
        if media_files:
            package.media_files = [os.path.join(audio_dir, f) for f in media_files]

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(notes)} vocabulary words")
        print(f"  - {len(media_files)} audio files")
        print("\nImport this file into Anki: File → Import...")

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(audio_dir)
        except:
            pass


if __name__ == "__main__":
    generate_deck()
