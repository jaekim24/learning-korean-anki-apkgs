#!/usr/bin/env python3
"""
Korean Basic Sentence Patterns

Common sentence structures using learned vocabulary and grammar.
Usage: python3 korean_sentences_1.py
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
    create_colored_html, create_sentence_model
)

# Deck info
DECK_ID = DECK_IDS["sentences_1"]
MODEL_ID = MODEL_IDS["sentence"]


# Sentences: (korean, english, breakdown, word_pairs)
# word_pairs: list of (korean_word, english_word) tuples for color alignment
SENTENCES = [
    # ===== SUBJECT + IS + NOUN =====
    ("저는 학생이에요.", "I am a student.", "저(I) + 는(topic) + 학생(student) + 이에요(is)",
     [("저는", "I"), ("학생이에요", "am a student")]),
    ("저는 한국 사람이에요.", "I am Korean.", "저 + 는 + 한국(Korea) + 사람(person) + 이에요",
     [("저는", "I"), ("한국 사람이에요", "am Korean")]),
    ("친구는 의사예요.", "My friend is a doctor.", "친구(friend) + 는 + 의사(doctor) + 예요",
     [("친구는", "My friend"), ("의사예요", "is a doctor")]),
    ("이것은 책이에요.", "This is a book.", "이것(this) + 은 + 책(book) + 이에요",
     [("이것은", "This"), ("책이에요", "is a book")]),
    ("그것은 물이에요.", "That is water.", "그것(that) + 은 + 물(water) + 이에요",
     [("그것은", "That"), ("물이에요", "is water")]),
    ("저것은 컴퓨터예요.", "That over there is a computer.", "저것(over there) + 은 + 컴퓨터(computer) + 예요",
     [("저것은", "That over there"), ("컴퓨터예요", "is a computer")]),
    ("오늘은 금요일이에요.", "Today is Friday.", "오늘(today) + 은 + 금요일(Friday) + 이에요",
     [("오늘은", "Today"), ("금요일이에요", "is Friday")]),
    ("날씨가 좋아요.", "The weather is good.", "날씨(weather) + 가(subject) + 좋아요(good)",
     [("날씨가", "The weather"), ("좋아요", "is good")]),
    ("음식이 맛있어요.", "The food is delicious.", "음식(food) + 이(subject) + 맛있어요(delicious)",
     [("음식이", "The food"), ("맛있어요", "is delicious")]),

    # ===== SUBJECT + VERB =====
    ("저는 집에 가요.", "I am going home.", "저 + 는 + 집(home) + 에(to) + 가요(go)",
     [("저는", "I"), ("집에 가요", "am going home")]),
    ("친구가 학교에 가요.", "Friend is going to school.", "친구 + 가(subject) + 학교(school) + 에 + 가요",
     [("친구가", "Friend"), ("학교에 가요", "is going to school")]),
    ("아빠가 회사에 가셨어요.", "Dad went to work.", "아빠(dad) + 가 + 회사(company) + 에 + 가셨어요(went-honorific)",
     [("아빠가", "Dad"), ("회사에 가셨어요", "went to work")]),
    ("엄마가 시장에 가요.", "Mom is going to the market.", "엄마(mom) + 가 + 시장(market) + 에 + 가요",
     [("엄마가", "Mom"), ("시장에 가요", "is going to the market")]),
    ("버스가 와요.", "The bus is coming.", "버스(bus) + 가 + 와요(coming)",
     [("버스가", "The bus"), ("와요", "is coming")]),
    ("비가 와요.", "It is raining.", "비(rain) + 가 + 와요(coming)",
     [("비가", "It"), ("와요", "is raining")]),
    ("눈이 와요.", "It is snowing.", "눈(snow) + 이(subject) + 와요",
     [("눈이", "It"), ("와요", "is snowing")]),
    ("저는 한국어를 배워요.", "I am learning Korean.", "저 + 는 + 한국어(Korean) + 를(object) + 배워요(learning)",
     [("저는", "I"), ("한국어를", "Korean"), ("배워요", "am learning")]),
    ("친구를 만나요.", "Meeting a friend.", "친구 + 를 + 만나요(meeting)",
     [("친구를", "a friend"), ("만나요", "Meeting")]),
    ("밥을 먹어요.", "Eating rice/a meal.", "밥(rice/meal) + 을(object) + 먹어요(eating)",
     [("밥을", "rice/a meal"), ("먹어요", "Eating")]),

    # ===== SUBJECT + OBJECT + VERB =====
    ("저는 사과를 먹어요.", "I am eating an apple.", "저 + 는 + 사과(apple) + 를 + 먹어요(eating)",
     [("저는", "I"), ("사과를", "an apple"), ("먹어요", "am eating")]),
    ("친구가 책을 읽어요.", "Friend is reading a book.", "친구 + 가 + 책(book) + 을 + 읽어요(reading)",
     [("친구가", "Friend"), ("책을", "a book"), ("읽어요", "is reading")]),
    ("동생이 물을 마셨어요.", "Younger sibling drank water.", "동생(younger sibling) + 이 + 물(water) + 을 + 마셨어요(drank)",
     [("동생이", "Younger sibling"), ("물을", "water"), ("마셨어요", "drank")]),
    ("할머니께서 드셨어요.", "Grandmother ate (honorific).", "할머니(grandmother) + 께서(honorific) + 드셨어요(ate-honorific)",
     [("할머니께서", "Grandmother"), ("드셨어요", "ate (honorific)")]),
    ("저는 영화를 봤어요.", "I watched a movie.", "저 + 는 + 영화(movie) + 를 + 봤어요(watched)",
     [("저는", "I"), ("영화를", "a movie"), ("봤어요", "watched")]),
    ("우리는 축구를 해요.", "We play soccer.", "우리(we) + 는 + 축구(soccer) + 를 + 해요(playing/doing)",
     [("우리는", "We"), ("축구를", "soccer"), ("해요", "play")]),
    ("학생이 숙제를 해요.", "The student is doing homework.", "학생(student) + 이 + 숙제(homework) + 를 + 해요",
     [("학생이", "The student"), ("숙제를", "homework"), ("해요", "is doing")]),
    ("아기를 재워요.", "Putting the baby to sleep.", "아기(baby) + 를 + 재워요(putting to sleep)",
     [("아기를", "the baby"), ("재워요", "Putting to sleep")]),
    ("음악을 들어요.", "Listening to music.", "음악(music) + 을 + 들어요(listening)",
     [("음악을", "music"), ("들어요", "Listening to")]),

    # ===== LOCATION + EXISTENCE VERBS =====
    ("집에 있어요.", "(Someone) is at home.", "집(home) + 에(at) + 있어요(exist)",
     [("집에", "at home"), ("있어요", "(someone) is")]),
    ("학교에 가요.", "Going to school.", "학교 + 에(to) + 가요(go)",
     [("학교에", "to school"), ("가요", "Going")]),
    ("도서관에서 공부해요.", "Studying at the library.", "도서관(library) + 에서(at) + 공부해요(studying)",
     [("도서관에서", "at the library"), ("공부해요", "Studying")]),
    ("식당에서 밥을 먹어요.", "Eating at a restaurant.", "식당(restaurant) + 에서 + 밥 + 을 + 먹어요",
     [("식당에서", "at a restaurant"), ("밥을 먹어요", "Eating")]),
    ("친구가 집에 왔어요.", "Friend came to the house.", "친구 + 가 + 집(home) + 에(to) + 왔어요(came)",
     [("친구가", "Friend"), ("집에", "to the house"), ("왔어요", "came")]),
    ("한국에 살아요.", "Living in Korea.", "한국(Korea) + 에(in) + 살아요(living)",
     [("한국에", "in Korea"), ("살아요", "Living")]),
    ("책상 위에 책이 있어요.", "There is a book on the desk.", "책상(desk) + 위(on) + 에 + 책(book) + 이 + 있어요",
     [("책상 위에", "On the desk"), ("책이 있어요", "there is a book")]),
    ("냉장고에 물이 있어요.", "There is water in the refrigerator.", "냉장고(refrigerator) + 에 + 물 + 이 + 있어요",
     [("냉장고에", "in the refrigerator"), ("물이 있어요", "there is water")]),
    ("가방 안에 지갑이 없어요.", "There is no wallet in the bag.", "가방(bag) + 안(inside) + 에 + 지갑(wallet) + 이 + 없어요(no)",
     [("가방 안에", "in the bag"), ("지갑이 없어요", "there is no wallet")]),

    # ===== QUESTION SENTENCES =====
    ("이름이 뭐예요?", "What is your name?", "이름(name) + 이(subject) + 뭐(what) + 예요?",
     [("이름이", "Your name"), ("뭐예요?", "what is?")]),
    ("나이가 어떻게 되세요?", "How old are you? (polite)", "나이(age) + 가 + 어떻게(how) + 되세요?",
     [("나이가", "You"), ("어떻게 되세요?", "how old? (polite)")]),
    ("어디에 가요?", "Where are you going?", "어디(where) + 에 + 가요?",
     [("어디에", "Where"), ("가요?", "are you going?")]),
    ("무엇을 먹어요?", "What are you eating?", "무엇(what) + 을 + 먹어요?",
     [("무엇을", "What"), ("먹어요?", "are you eating?")]),
    ("누가 와요?", "Who is coming?", "누구(who) + 가(subject) + 와요?",
     [("누가", "Who"), ("와요?", "is coming?")]),
    ("언제 왔어요?", "When did you come?", "언제(when) + 왔어요?",
     [("언제", "When"), ("왔어요?", "did you come?")]),
    ("왜 가요?", "Why are you going?", "왜(why) + 가요?",
     [("왜", "Why"), ("가요?", "are you going?")]),
    ("어떻게 가요?", "How do you go?", "어떻게(how) + 가요?",
     [("어떻게", "How"), ("가요?", "do you go?")]),
    ("누구를 만나요?", "Who are you meeting?", "누구(who) + 를 + 만나요?",
     [("누구를", "Who"), ("만나요?", "are you meeting?")]),
    ("몇 시에 일어나요?", "What time do you wake up?", "몇 시(what time) + 에 + 일어나요?",
     [("몇 시에", "What time"), ("일어나요?", "do you wake up?")]),

    # ===== NEGATION =====
    ("안 가요.", "Not going.", "안(not) + 가요(go)",
     [("안", "Not"), ("가요", "going")]),
    ("안 먹어요.", "Not eating.", "안 + 먹어요(eat)",
     [("안", "Not"), ("먹어요", "eating")]),
    ("못 가요.", "Cannot go.", "못(cannot) + 가요(go)",
     [("못", "Cannot"), ("가요", "go")]),
    ("못 먹어요.", "Cannot eat.", "못 + 먹어요(eat)",
     [("못", "Cannot"), ("먹어요", "eat")]),
    ("하지 않아요.", "Not doing.", "하다(do) + 지 않아요(not)",
     [("하지", "not"), ("않아요", "doing")]),
    ("가지 않아요.", "Not going.", "가다(go) + 지 않아요",
     [("가지", "not"), ("않아요", "going")]),
    ("먹지 않아요.", "Not eating.", "먹다(eat) + 지 않아요",
     [("먹지", "not"), ("않아요", "eating")]),
    ("없어요.", "There is none / don't have.", "없다(no) + 어요",
     [("없어요", "There is none / don't have")]),
    ("안 좋아요.", "Not good.", "안(not) + 좋아요(good)",
     [("안", "Not"), ("좋아요", "good")]),
    ("싫어해요.", "Dislike / hate.", "싫어해요(dislike)",
     [("싫어해요", "Dislike / hate")]),

    # ===== WANT / CAN =====
    ("가고 싶어요.", "I want to go.", "가다(go) + 고 싶어요(want)",
     [("가고", "go"), ("싶어요", "I want to")]),
    ("먹고 싶어요.", "I want to eat.", "먹다(eat) + 고 싶어요",
     [("먹고", "eat"), ("싶어요", "I want to")]),
    ("보고 싶어요.", "I want to see / miss you.", "보다(see) + 고 싶어요",
     [("보고", "see"), ("싶어요", "I want to / miss you")]),
    ("만나고 싶어요.", "I want to meet.", "만나다(meet) + 고 싶어요",
     [("만나고", "meet"), ("싶어요", "I want to")]),
    ("갈 수 있어요?", "Can you go?", "가다 + 을 수(can) + 있어요?",
     [("갈 수", "can"), ("있어요?", "you go?")]),
    ("먹을 수 없어요.", "Cannot eat.", "먹다 + 을 수 + 없어요(not)",
     [("먹을 수", "can"), ("없어요", "not / cannot eat")]),
    ("할 수 있어요.", "Can do.", "하다(do) + 을 수 + 있어요",
     [("할 수", "can"), ("있어요", "do")]),
    ("올 수 있어요?", "Can you come?", "오다(come) + 을 수 + 있어요?",
     [("올 수", "can"), ("있어요?", "you come?")]),
    ("읽을 수 있어요.", "Can read.", "읽다(read) + 을 수 + 있어요",
     [("읽을 수", "can"), ("있어요", "read")]),
    ("쓸 수 없어요.", "Cannot write/use.", "쓰다(write/use) + 을 수 + 없어요",
     [("쓸 수", "can"), ("없어요", "not write/use")]),

    # ===== REQUESTS / SUGGESTIONS =====
    ("도와주세요.", "Please help me.", "돕다(help) + 아 주세요(please)",
     [("도와", "help"), ("주세요", "Please")]),
    ("기다려주세요.", "Please wait.", "기다리다(wait) + 어 주세요",
     [("기다려", "wait"), ("주세요", "Please")]),
    ("조용히 해주세요.", "Please be quiet.", "조용히(quietly) + 해주세요(do please)",
     [("조용히", "quietly"), ("해주세요", "Please be")]),
    ("천천히 말해주세요.", "Please speak slowly.", "천천히(slowly) + 말하다(speak) + 어 주세요",
     [("천천히", "slowly"), ("말해주세요", "Please speak")]),
    ("가요.", "Let's go.", "가다(go) + 아요(let's)",
     [("가요", "Let's go")]),
    ("먹어요.", "Let's eat.", "먹다(eat) + 어요(let's)",
     [("먹어요", "Let's eat")]),
    ("만나요.", "Let's meet.", "만나다(meet) + 아요(let's)",
     [("만나요", "Let's meet")]),
    ("봐요.", "Let's see.", "보다(see) + 아요(let's)",
     [("봐요", "Let's see")]),
    ("시작할까요?", "Shall we start?", "시작하다(start) + 을까요(shall we?)",
     [("시작할까요?", "Shall we start?")]),
    ("갈까요?", "Shall we go?", "가다 + 을까요?",
     [("갈까요?", "Shall we go?")]),
    ("먹을까요?", "Shall we eat?", "먹다 + 을까요?",
     [("먹을까요?", "Shall we eat?")]),
    ("영화 볼래요?", "Do you want to watch a movie?", "영화(movie) + 보다 + ㄹ래요(want to?)",
     [("영화", "a movie"), ("볼래요?", "Do you want to watch?")]),
    ("커피 마실래요?", "Do you want to drink coffee?", "커피(coffee) + 마시다(drink) + ㄹ래요?",
     [("커피", "coffee"), ("마실래요?", "Do you want to drink?")]),

    # ===== FEELINGS / STATES =====
    ("배가 고파요.", "I am hungry.", "배(stomach) + 가(subject) + 고파요(hungry)",
     [("배가", "I"), ("고파요", "am hungry")]),
    ("배가 불러요.", "I am full.", "배 + 가 + 불러요(full)",
     [("배가", "I"), ("불러요", "am full")]),
    ("피곤해요.", "I am tired.", "피곤(tired) + 해요",
     [("피곤해요", "I am tired")]),
    ("졸려워요.", "I am sleepy.", "졸리다(sleepy) + 어워요",
     [("졸려워요", "I am sleepy")]),
    ("아파요.", "It hurts / I am sick.", "아프다(sick/hurt) + 아요",
     [("아파요", "It hurts / I am sick")]),
    ("기분이 좋아요.", "I feel good.", "기분(feeling/mood) + 이(subject) + 좋아요(good)",
     [("기분이", "I"), ("좋아요", "feel good")]),
    ("기분이 안 좋아요.", "I feel bad.", "기분 + 이 + 안 좋아요(not good)",
     [("기분이", "I"), ("안 좋아요", "feel bad")]),
    ("즐거워요.", "It is enjoyable.", "즐겁다(enjoyable) + 어워요",
     [("즐거워요", "It is enjoyable")]),
    ("심심해요.", "I am bored.", "심심하다(bored) + 해요",
     [("심심해요", "I am bored")]),
    ("무서워요.", "I am scared.", "무섭다(scared) + 어워요",
     [("무서워요", "I am scared")]),
    ("행복해요.", "I am happy.", "행복하다(happy) + 해요",
     [("행복해요", "I am happy")]),
    ("슬퍼요.", "I am sad.", "슬프다(sad) + 어워요",
     [("슬퍼요", "I am sad")]),
    ("화가 났어요.", "I got angry.", "화(anger) + 가 + 났어요(rose)",
     [("화가", "I"), ("났어요", "got angry")]),
    ("괜찮아요?", "Are you okay?", "괜찮다(okay) + 아요?",
     [("괜찮아요?", "Are you okay?")]),

    # ===== DAILY ACTIVITIES =====
    ("아침에 일어났어요.", "Woke up in the morning.", "아침(morning) + 에 + 일어나다(wake up) + 았어요",
     [("아침에", "in the morning"), ("일어났어요", "Woke up")]),
    ("양치를 했어요.", "Brushed teeth.", "양치(tooth brushing) + 를 + 했어요(did)",
     [("양치를", "teeth"), ("했어요", "Brushed")]),
    ("샤워를 해요.", "Taking a shower.", "샤워(shower) + 를 + 해요(doing)",
     [("샤워를", "a shower"), ("해요", "Taking")]),
    ("옷을 입었어요.", "Put on clothes.", "옷(clothes) + 을 + 입다(wear) + 었어요",
     [("옷을", "clothes"), ("입었어요", "Put on")]),
    ("신발을 신어요.", "Putting on shoes.", "신발(shoes) + 을 + 신다(wear(feet)) + 어요",
     [("신발을", "shoes"), ("신어요", "Putting on")]),
    ("화장을 지워요.", "Removing makeup.", "화장(makeup) + 을 + 지우다(remove) + 어요",
     [("화장을", "makeup"), ("지워요", "Removing")]),
    ("출근했어요.", "Went to work.", "출근(going to work) + 했어요(did)",
     [("출근했어요", "Went to work")]),
    ("퇴근했어요.", "Left work.", "퇴근(leaving work) + 했어요",
     [("퇴근했어요", "Left work")]),
    ("집에 왔어요.", "Came home.", "집(home) + 에 + 오다(come) + 았어요",
     [("집에", "home"), ("왔어요", "Came")]),
    ("잤어요.", "Slept.", "자다(sleep) + 았어요",
     [("잤어요", "Slept")]),
    ("꿈을 꿨어요.", "Dreamed.", "꿈(dream) + 을 + 꾸다(dream) + 었어요",
     [("꿈을", "a dream"), ("꿨어요", "Dreamed")]),

    # ===== WEATHER =====
    ("날씨가 좋아요.", "The weather is good.", "날씨(weather) + 가 + 좋아요(good)",
     [("날씨가", "The weather"), ("좋아요", "is good")]),
    ("날씨가 안 좋아요.", "The weather is bad.", "날씨 + 가 + 안 좋아요(not good)",
     [("날씨가", "The weather"), ("안 좋아요", "is bad")]),
    ("비가 와요.", "It is raining.", "비(rain) + 가 + 와요(coming)",
     [("비가", "It"), ("와요", "is raining")]),
    ("눈이 와요.", "It is snowing.", "눈(snow) + 이 + 와요",
     [("눈이", "It"), ("와요", "is snowing")]),
    ("바람이 불어요.", "The wind is blowing.", "바람(wind) + 이(subject) + 불다(blow) + 어요",
     [("바람이", "The wind"), ("불어요", "is blowing")]),
    ("따뜻해요.", "It is warm.", "따뜻하다(warm) + 해요",
     [("따뜻해요", "It is warm")]),
    ("더워요.", "It is hot.", "덥다(hot) + 어워요",
     [("더워요", "It is hot")]),
    ("추워요.", "It is cold.", "춥다(cold) + 우워요",
     [("추워요", "It is cold")]),
    ("안개가 꼈어요.", "It is foggy.", "안개(fog) + 가 + 끼다(form) + 꼈어요",
     [("안개가", "It"), ("꼈어요", "is foggy")]),
    ("햇볕이 쨍쨍해요.", "The sun is shining brightly.", "햇볕(sunshine) + 이 + 쨍쨍해요(shining)",
     [("햇볕이", "The sun"), ("쨍쨍해요", "is shining brightly")]),

    # ===== TIME EXPRESSIONS =====
    ("지금 9시예요.", "It is 9 o'clock now.", "지금(now) + 9시(9 o'clock) + 예요",
     [("지금", "Now"), ("9시예요", "it is 9 o'clock")]),
    ("오전 7시에 일어나요.", "I wake up at 7 AM.", "오전(AM) + 7시 + 에 + 일어나요",
     [("오전 7시에", "At 7 AM"), ("일어나요", "I wake up")]),
    ("오후 6시에 저녁을 먹어요.", "Eating dinner at 6 PM.", "오후(PM) + 6시 + 에 + 저녁(dinner) + 을 + 먹어요",
     [("오후 6시에", "At 6 PM"), ("저녁을 먹어요", "eating dinner")]),
    ("오늘 뭐 해요?", "What are you doing today?", "오늘(today) + 뭐(what) + 해요?",
     [("오늘", "today"), ("뭐 해요?", "what are you doing?")]),
    ("내일 만날까요?", "Shall we meet tomorrow?", "내일(tomorrow) + 만나다(meet) + ㄹ까요?",
     [("내일", "tomorrow"), ("만날까요?", "shall we meet?")]),
    ("어제 친구를 만났어요.", "Met a friend yesterday.", "어제(yesterday) + 친구 + 를 + 만났어요(met)",
     [("어제", "Yesterday"), ("친구를", "a friend"), ("만났어요", "met")]),
    ("주말에 뭐 해요?", "What do you do on weekends?", "주말(weekend) + 에 + 뭐 + 해요?",
     [("주말에", "on weekends"), ("뭐 해요?", "what do you do?")]),
    ("다음 주에 시간 있어요?", "Do you have time next week?", "다음 주(next week) + 에 + 시간(time) + 있어요?",
     [("다음 주에", "next week"), ("시간 있어요?", "do you have time?")]),

    # ===== FAMILY / RELATIONSHIPS =====
    ("가족이 몇 명이에요?", "How many family members?", "가족(family) + 이(subject) + 몇(how many) + 명(people) + 이에요?",
     [("가족이", "family"), ("몇 명이에요?", "how many members?")]),
    ("가족이 4명이에요.", "There are 4 family members.", "가족 + 이 + 4명(4 people) + 이에요",
     [("가족이", "There are"), ("4명이에요", "4 family members")]),
    ("형이 한 명 있어요.", "I have one older brother.", "형(older brother-male) + 이(subject) + 한 명(one person) + 있어요(have)",
     [("형이", "I have"), ("한 명", "one"), ("있어요", "older brother")]),
    ("누나가 두 명 있어요.", "I have two older sisters.", "누나(older sister-male) + 가 + 두 명(two people) + 있어요",
     [("누나가", "I have"), ("두 명", "two"), ("있어요", "older sisters")]),
    ("동생이 없어요.", "I don't have siblings.", "동생(sibling) + 이 + 없어요(don't have)",
     [("동생이", "I don't have"), ("없어요", "siblings")]),
    ("결혼했어요?", "Are you married?", "결혼(marriage) + 했어요(did)?",
     [("결혼했어요?", "Are you married?")]),
    ("아이가 있어요.", "I have a child.", "아이(child) + 가(subject) + 있어요(have)",
     [("아이가", "I have"), ("있어요", "a child")]),
    ("부모님과 살아요.", "Living with parents.", "부모님(parents) + 과(with) + 살아요(living)",
     [("부모님과", "with parents"), ("살아요", "Living")]),

    # ===== LIKES / DISLIKES =====
    ("김치를 좋아해요.", "I like kimchi.", "김치(kimchi) + 를 + 좋아해요(like)",
     [("김치를", "kimchi"), ("좋아해요", "I like")]),
    ("피자를 싫어해요.", "I dislike pizza.", "피자(pizza) + 를 + 싫어해요(dislike)",
     [("피자를", "pizza"), ("싫어해요", "I dislike")]),
    ("한국 음식을 좋아해요?", "Do you like Korean food?", "한국(Korean) + 음식(food) + 을 + 좋아해요?",
     [("한국 음식을", "Korean food"), ("좋아해요?", "do you like?")]),
    ("커피를 마셔요.", "I drink coffee.", "커피(coffee) + 를 + 마셔요(drink)",
     [("커피를", "coffee"), ("마셔요", "I drink")]),
    ("술을 안 마셔요.", "I don't drink alcohol.", "술(alcohol) + 을 + 안 + 마셔요",
     [("술을", "alcohol"), ("안 마셔요", "I don't drink")]),
    ("고기를 안 먹어요.", "I don't eat meat.", "고기(meat) + 을 + 안 + 먹어요",
     [("고기를", "meat"), ("안 먹어요", "I don't eat")]),

    # ===== NUMBERS / QUANTITIES =====
    ("사과가 세 개 있어요.", "There are three apples.", "사과(apple) + 가 + 세 개(three items) + 있어요",
     [("사과가", "There are"), ("세 개", "three"), ("있어요", "apples")]),
    ("물 한 잔 주세요.", "Please give me a glass of water.", "물(water) + 한 잔(one glass) + 주세요(please)",
     [("물 한 잔", "a glass of water"), ("주세요", "Please give me")]),
    ("친구가 다섯 명 왔어요.", "Five friends came.", "친구(friend) + 가 + 다섯 명(five people) + 왔어요",
     [("친구가", "Five"), ("다섯 명", "friends"), ("왔어요", "came")]),
    ("책 두 권을 샀어요.", "Bought two books.", "책(book) + 두 권(two books) + 을 + 샀어요(bought)",
     [("책 두 권을", "two books"), ("샀어요", "Bought")]),
    ("1000원이에요.", "It is 1000 won.", "1000원(1000 won) + 이에요",
     [("1000원이에요", "It is 1000 won")]),
]


def create_model():
    """Create card model for sentences with color-coded word alignment."""
    return genanki.Model(
        MODEL_ID,
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


def generate_deck(output_file="decks/09_korean_sentences_1.apkg"):
    """Generate the basic sentences deck with color-coded word alignment."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "09. Korean Sentences - 기본 문장")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for entry in SENTENCES:
            # Support both old format (3-tuple) and new format (4-tuple with word_pairs)
            if len(entry) == 4:
                korean, english, breakdown, word_pairs = entry
            else:
                korean, english, breakdown = entry
                word_pairs = []

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs)

            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[korean, english, breakdown, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(SENTENCES)} sentence cards")
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
