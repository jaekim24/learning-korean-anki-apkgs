#!/usr/bin/env python3
"""
Korean Common Verbs Anki Deck Generator

Creates Anki decks for the most commonly used Korean verbs.
Usage: python3 korean_verbs_common.py
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
DECK_ID = 1837523964
MODEL_ID = MODEL_IDS["word"]


# Basic Verbs - To Be/Exist & Have (1-15)
VERBS_1_15 = [
    KoreanWordCard("이다", "to be (copula)", "ida", "저는 학생이에요 (I am a student)", "I am a student"),
    KoreanWordCard("있다", "to exist / to have / there is", "itda", "시간이 있어요 (I have time)", "I have time"),
    KoreanWordCard("없다", "to not exist / to not have / there isn't", "eopda", "돈이 없어요 (I don't have money)", "I don't have money"),
    KoreanWordCard("있다", "to be located (at)", "itda", "집에 있어요 (I'm at home)", "I'm at home"),
    KoreanWordCard("계시다", "to be (honorific)", "gyesida", "어머니가 집에 계세요 (Mother is at home)", "Mother is at home"),
    KoreanWordCard("되다", "to become", "doida", "의사가 되고 싶어요 (I want to become a doctor)", "I want to become a doctor"),
    KoreanWordCard("아니다", "to not be", "anida", "학생이 아니에요 (I'm not a student)", "I'm not a student"),
    KoreanWordCard("같다", "to be the same / to be like", "gatda", "꼭 같아요 (It's exactly the same)", "It's exactly the same"),
    KoreanWordCard("다르다", "to be different", "dareuda", "완전 달라요 (It's completely different)", "It's completely different"),
]

# Movement & Action Verbs (16-40)
VERBS_16_40 = [
    KoreanWordCard("가다", "to go", "gada", "학교에 가요 (I go to school)", "I go to school"),
    KoreanWordCard("오다", "to come", "oda", "친구가 와요 (A friend is coming)", "A friend is coming"),
    KoreanWordCard("나가다", "to go out", "nagada", "밖에 나가요 (I'm going outside)", "I'm going outside"),
    KoreanWordCard("들어오다", "to come in / to enter", "deureooda", "방에 들어와요 (Come into the room)", "Come into the room"),
    KoreanWordCard("나오다", "to come out", "naoda", "밖으로 나와요 (Come outside)", "Come outside"),
    KoreanWordCard("다니다", "to attend / to go back and forth", "danida", "학교에 다녀요 (I attend school)", "I attend school"),
    KoreanWordCard("오르다", "to go up / to climb", "oreuda", "산에 올라가요 (I'm climbing the mountain)", "I'm climbing the mountain"),
    KoreanWordCard("내려가다", "to go down", "naeryeogada", "엘리베이터를 내려가요 (I'm going down in the elevator)", "I'm going down in the elevator"),
    KoreanWordCard("내려오다", "to come down", "naeryeooda", "계단에서 내려와요 (Come down the stairs)", "Come down the stairs"),
    KoreanWordCard("돌아오다", "to come back / to return", "dorao da", "집에 돌아와요 (I'm coming back home)", "I'm coming back home"),
    KoreanWordCard("돌아가다", "to go back / to return", "doragada", "미국으로 돌아가요 (I'm going back to the US)", "I'm going back to the US"),
    KoreanWordCard("건너가다", "to cross", "geonneogada", "길을 건너가요 (I'm crossing the street)", "I'm crossing the street"),
    KoreanWordCard("지나가다", "to pass by", "jinagada", "버스가 지나가요 (The bus is passing)", "The bus is passing"),
    KoreanWordCard("서다", "to stand", "seoda", "거기에 서세요 (Please stand there)", "Please stand there"),
    KoreanWordCard("앉다", "to sit", "anda", "여기에 앉아요 (I'm sitting here)", "I'm sitting here"),
    KoreanWordCard("눕다", "to lie down", "nupda", "침대에 누워요 (I'm lying on the bed)", "I'm lying on the bed"),
    KoreanWordCard("일어나다", "to get up / to wake up", "ireonada", "7시에 일어나요 (I wake up at 7)", "I wake up at 7"),
    KoreanWordCard("움직이다", "to move", "umjigida", "움직이지 마세요 (Don't move)", "Don't move"),
    KoreanWordCard("멈추다", "to stop", "meomchuda", "멈춰 주세요 (Please stop)", "Please stop"),
    KoreanWordCard("쉬다", "to rest / to take a break", "swida", "잠시 쉴게요 (I'll rest for a moment)", "I'll rest for a moment"),
    KoreanWordCard("달리다", "to run", "dallida", "매일 달려요 (I run every day)", "I run every day"),
    KoreanWordCard("걷다", "to walk", "geotda", "걸어서 가요 (I'm walking)", "I'm walking"),
    KoreanWordCard("뛰다", "to run / to jump", "twida", "아이들이 뛰어요 (The kids are running)", "The kids are running"),
    KoreanWordCard("도망가다", "to run away / to escape", "domanggada", "도망가지 마세요 (Don't run away)", "Don't run away"),
    KoreanWordCard("따라가다", "to follow", "ttaragada", "저를 따라와요 (Follow me)", "Follow me"),
]

# Daily Routine Verbs (41-65)
VERBS_41_65 = [
    KoreanWordCard("하다", "to do", "hada", "숙제를 해요 (I'm doing homework)", "I'm doing homework"),
    KoreanWordCard("시작하다", "to start / to begin", "sijakada", "수업을 시작해요 (The class starts)", "The class starts"),
    KoreanWordCard("끝내다", "to finish / to end", "kkeunnaeda", "일을 끝냈어요 (I finished the work)", "I finished the work"),
    KoreanWordCard("마치다", "to finish / to complete", "machida", "일을 마쳤어요 (I completed the work)", "I completed the work"),
    KoreanWordCard("계속하다", "to continue", "gyesokada", "계속 해요 (Keep going)", "Keep going"),
    KoreanWordCard("준비하다", "to prepare", "junbihada", "저녁을 준비해요 (I'm preparing dinner)", "I'm preparing dinner"),
    KoreanWordCard("시간내다", "to make time", "sigannaeda", "시간을 내주세요 (Please make time)", "Please make time"),
    KoreanWordCard("일어나다", "to wake up", "ireonada", "아침에 일어나요 (I wake up in the morning)", "I wake up in the morning"),
    KoreanWordCard("자다", "to sleep", "jada", "9시에 자요 (I go to sleep at 9)", "I go to sleep at 9"),
    KoreanWordCard("씻다", "to wash", "ssitda", "손을 씻어요 (I'm washing my hands)", "I'm washing my hands"),
    KoreanWordCard("샤워하다", "to shower", "syawohada", "샤워해요 (I'm taking a shower)", "I'm taking a shower"),
    KoreanWordCard("목욕하다", "to take a bath", "mogyokada", "목욕해요 (I'm taking a bath)", "I'm taking a bath"),
    KoreanWordCard("입다", "to wear (clothes)", "ipda", "옷을 입어요 (I'm putting on clothes)", "I'm putting on clothes"),
    KoreanWordCard("벗다", "to take off (clothes)", "betda", "옷을 벗어요 (I'm taking off clothes)", "I'm taking off clothes"),
    KoreanWordCard("신다", "to wear (shoes/socks)", "sinda", "신발을 신어요 (I'm putting on shoes)", "I'm putting on shoes"),
    KoreanWordCard("입다", "to wear (accessories like glasses, hat)", "ipda", "안경을 써요 (I'm wearing glasses)", "I'm wearing glasses"),
    KoreanWordCard("씹다", "to chew", "ssibda", "음식을 씹어요 (I'm chewing food)", "I'm chewing food"),
    KoreanWordCard("삼키다", "to swallow", "samkida", "약을 삼켰어요 (I swallowed the pill)", "I swallowed the pill"),
    KoreanWordCard("먹다", "to eat", "meokda", "밥을 먹어요 (I'm eating rice/a meal)", "I'm eating a meal"),
    KoreanWordCard("마시다", "to drink", "masida", "물을 마셔요 (I'm drinking water)", "I'm drinking water"),
    KoreanWordCard("요리하다", "to cook", "yorihada", "매일 요리해요 (I cook every day)", "I cook every day"),
    KoreanWordCard("청소하다", "to clean", "cheongsohada", "방을 청소해요 (I'm cleaning the room)", "I'm cleaning the room"),
    KoreanWordCard("설거지하다", "to do the dishes", "seolgeojihada", "설거지를 해요 (I'm doing the dishes)", "I'm doing the dishes"),
    KoreanWordCard("빨래하다", "to do laundry", "ppallaeada", "빨래를 해요 (I'm doing laundry)", "I'm doing laundry"),
    KoreanWordCard("쇼핑하다", "to shop", "syopinghada", "옷을 쇼핑해요 (I'm shopping for clothes)", "I'm shopping for clothes"),
]

# Communication & Speaking Verbs (66-90)
VERBS_66_90 = [
    KoreanWordCard("말하다", "to say / to speak", "malhada", "진실을 말해요 (I'm telling the truth)", "I'm telling the truth"),
    KoreanWordCard("이야기하다", "to talk / to tell a story", "iyagihada", "친구와 이야기해요 (I'm talking with a friend)", "I'm talking with a friend"),
    KoreanWordCard("대화하다", "to converse / to have a conversation", "daehwahada", "대화해요 (Let's talk)", "Let's talk"),
    KoreanWordCard("통화하다", "to have a phone conversation", "tonghwahada", "전화로 통화해요 (I'm talking on the phone)", "I'm talking on the phone"),
    KoreanWordCard("전화하다", "to call / to phone", "jeonhwahada", "친구에게 전화해요 (I'm calling a friend)", "I'm calling a friend"),
    KoreanWordCard("문자하다", "to text", "munjahada", "문자해요 (Text me)", "Text me"),
    KoreanWordCard("듣다", "to hear / to listen", "deutda", "음악을 들어요 (I'm listening to music)", "I'm listening to music"),
    KoreanWordCard("보다", "to see / to look at / to watch", "boda", "영화를 봐요 (I'm watching a movie)", "I'm watching a movie"),
    KoreanWordCard("읽다", "to read", "ikda", "책을 읽어요 (I'm reading a book)", "I'm reading a book"),
    KoreanWordCard("쓰다", "to write", "sseuda", "편지를 써요 (I'm writing a letter)", "I'm writing a letter"),
    KoreanWordCard("부르다", "to call (someone's name) / to sing", "bureuda", "이름을 불러요 (I'm calling the name)", "I'm calling the name"),
    KoreanWordCard("대답하다", "to answer", "daedapada", "질문에 대답해요 (I'm answering the question)", "I'm answering the question"),
    KoreanWordCard("물어보다", "to ask", "mureoboda", "질문을 물어봐요 (I'm asking a question)", "I'm asking a question"),
    KoreanWordCard("묻다", "to ask", "mutda", "길을 물어요 (I'm asking for directions)", "I'm asking for directions"),
    KoreanWordCard("설명하다", "to explain", "seolmyeonghada", "설명해 주세요 (Please explain)", "Please explain"),
    KoreanWordCard("알다", "to know / to understand", "alda", "알아요 (I know)", "I know"),
    KoreanWordCard("모르다", "to not know", "moreuda", "몰라요 (I don't know)", "I don't know"),
    KoreanWordCard("이해하다", "to understand", "ihaehada", "이해해요 (I understand)", "I understand"),
    KoreanWordCard("생각하다", "to think", "saenggakada", "생각해 봐요 (Let me think)", "Let me think"),
    KoreanWordCard("느끼다", "to feel", "neukkida", "행복을 느껴요 (I feel happy)", "I feel happy"),
    KoreanWordCard("기억하다", "to remember", "gieokada", "기억해요 (I remember)", "I remember"),
    KoreanWordCard("잊다", "to forget", "itda", "잊어버렸어요 (I forgot)", "I forgot"),
    KoreanWordCard("배우다", "to learn", "baeuda", "한국어를 배워요 (I'm learning Korean)", "I'm learning Korean"),
    KoreanWordCard("가르치다", "to teach", "fareuchida", "학생들을 가르쳐요 (I teach students)", "I teach students"),
    KoreanWordCard("공부하다", "to study", "gongbuhada", "공부해요 (I'm studying)", "I'm studying"),
]

# Emotion & Feeling Verbs (91-115)
VERBS_91_115 = [
    KoreanWordCard("좋아하다", "to like", "joahada", "음악을 좋아해요 (I like music)", "I like music"),
    KoreanWordCard("사랑하다", "to love", "saranghada", "가족을 사랑해요 (I love my family)", "I love my family"),
    KoreanWordCard("싫어하다", "to hate / to dislike", "sireohada", "싫어해요 (I hate it)", "I hate it"),
    KoreanWordCard("행복하다", "to be happy", "haengbokada", "행복해요 (I'm happy)", "I'm happy"),
    KoreanWordCard("즐겁다", "to be enjoyable / pleasant", "jeulgeopda", "즐거워요 (It's enjoyable)", "It's enjoyable"),
    KoreanWordCard("기쁘다", "to be glad / pleased", "gippeuda", "기뻐요 (I'm glad)", "I'm glad"),
    KoreanWordCard("슬프다", "to be sad", "seulpeuda", "슬퍼요 (I'm sad)", "I'm sad"),
    KoreanWordCard("우울하다", "to be depressed / gloomy", "uulhada", "우울해요 (I'm depressed)", "I'm depressed"),
    KoreanWordCard("화나다", "to be angry / mad", "hwanada", "화났어요 (I'm angry)", "I'm angry"),
    KoreanWordCard("짜증나다", "to be annoyed", "jjajeungnada", "짜증 나요 (I'm annoyed)", "I'm annoyed"),
    KoreanWordCard("신나다", "to be excited", "sinnada", "신나요 (I'm excited)", "I'm excited"),
    KoreanWordCard("두렵다", "to be afraid / scared", "duryeopda", "무서워요 (I'm scared)", "I'm scared"),
    KoreanWordCard("무섭다", "to be scared / frightened", "museopda", "무서워요 (I'm frightened)", "I'm frightened"),
    KoreanWordCard("걱정하다", "to worry", "geokjeonghada", "걱정하지 마세요 (Don't worry)", "Don't worry"),
    KoreanWordCard("불안하다", "to be anxious / uneasy", "bulanhada", "불안해요 (I'm anxious)", "I'm anxious"),
    KoreanWordCard("편안하다", "to be comfortable / at ease", "pyeonanhada", "편안해요 (I'm comfortable)", "I'm comfortable"),
    KoreanWordCard("답답하다", "to feel frustrated / stifled", "dapdaphada", "답답해요 (I feel frustrated)", "I feel frustrated"),
    KoreanWordCard("스트레스받다", "to be stressed", "seuteureusibadta", "스트레스 받아요 (I'm stressed)", "I'm stressed"),
    KoreanWordCard("피곤하다", "to be tired", "pigonhada", "피곤해요 (I'm tired)", "I'm tired"),
    KoreanWordCard("힘들다", "to be difficult / tough / hard", "himdeulda", "힘들어요 (It's hard)", "It's hard"),
    KoreanWordCard("쉽다", "to be easy", "swipda", "쉬워요 (It's easy)", "It's easy"),
    KoreanWordCard("괜찮다", "to be okay / fine", "gwaenchanta", "괜찮아요 (I'm okay)", "I'm okay"),
    KoreanWordCard("아프다", "to be sick / in pain", "apda", "아파요 (I'm sick / it hurts)", "I'm sick / it hurts"),
    KoreanWordCard("편하다", "to be convenient / comfortable", "pyeonhada", "편해요 (It's convenient)", "It's convenient"),
    KoreanWordCard("불편하다", "to be inconvenient", "bulpyeonhada", "불편해요 (It's inconvenient)", "It's inconvenient"),
]

# Giving & Receiving Verbs (116-135)
VERBS_116_135 = [
    KoreanWordCard("주다", "to give", "juda", "선물을 줘요 (I give a gift)", "I give a gift"),
    KoreanWordCard("받다", "to receive", "batda", "선물을 받아요 (I receive a gift)", "I receive a gift"),
    KoreanWordCard("드리다", "to give (honorific)", "deurida", "어머니께 드려요 (I give to mother)", "I give to mother"),
    KoreanWordCard("가져다주다", "to bring (to someone)", "gajyeodajuda", "물을 가져다줘요 (Bring me water)", "Bring me water"),
    KoreanWordCard("가져오다", "to bring", "gajyeooda", "가져와요 (Bring it)", "Bring it"),
    KoreanWordCard("가져가다", "to take (away)", "gajyeogada", "가져가세요 (Please take it)", "Please take it"),
    KoreanWordCard("만들다", "to make / to create", "mandeulda", "음식을 만들어요 (I'm making food)", "I'm making food"),
    KoreanWordCard("만들어주다", "to make for someone", "mandeureojuda", "만들어 줄게요 (I'll make it for you)", "I'll make it for you"),
    KoreanWordCard("사다", "to buy", "sada", "옷을 사요 (I'm buying clothes)", "I'm buying clothes"),
    KoreanWordCard("팔다", "to sell", "palda", "옷을 팔아요 (I'm selling clothes)", "I'm selling clothes"),
    KoreanWordCard("빌리다", "to borrow", "billida", "책을 빌려요 (I'm borrowing a book)", "I'm borrowing a book"),
    KoreanWordCard("빌려주다", "to lend", "billyeojuda", "책을 빌려줘요 (I lend a book)", "I lend a book"),
    KoreanWordCard("갚다", "to pay back / to return", "gatda", "돈을 갚아요 (I'm paying back money)", "I'm paying back money"),
    KoreanWordCard("보내다", "to send", "bonaeda", "편지를 보내요 (I'm sending a letter)", "I'm sending a letter"),
    KoreanWordCard("받다", "to get / to receive", "batda", "편지를 받아요 (I got a letter)", "I got a letter"),
    KoreanWordCard("전하다", "to convey / to pass on", "jeonhada", "인사를 전해주세요 (Please convey my regards)", "Please convey my regards"),
    KoreanWordCard("건네다", "to hand over", "geonneda", "건네주세요 (Please hand it over)", "Please hand it over"),
    KoreanWordCard("내놓다", "to take out / to produce", "naenota", "내놓으세요 (Take it out)", "Take it out"),
    KoreanWordCard("넣다", "to put in / to insert", "neota", "가방에 넣어요 (I put it in the bag)", "I put it in the bag"),
    KoreanWordCard("꺼내다", "to take out / to pull out", "kkonaeda", "가방에서 꺼내요 (I take it out of the bag)", "I take it out of the bag"),
]

# Helping & Trying Verbs (136-160)
VERBS_136_160 = [
    KoreanWordCard("돕다", "to help / to assist", "dopda", "친구를 도와줘요 (I help my friend)", "I help my friend"),
    KoreanWordCard("도와주다", "to help (someone)", "dowaojuda", "도와줘요 (Help me)", "Help me"),
    KoreanWordCard("돕다", "to help (dictionary form)", "dopda", "도와주세요 (Please help)", "Please help"),
    KoreanWordCard("살리다", "to save (a life)", "sallida", "목숨을 살렸어요 (I saved a life)", "I saved a life"),
    KoreanWordCard("구하다", "to save / to rescue", "guhada", "사람을 구해요 (I rescue people)", "I rescue people"),
    KoreanWordCard("노력하다", "to make an effort / to try hard", "noryeokada", "노력해요 (I make an effort)", "I make an effort"),
    KoreanWordCard("시도하다", "to attempt / to try", "sidohada", "시도해요 (I attempt)", "I attempt"),
    KoreanWordCard("해보다", "to try doing something", "haeboda", "한번 해봐요 (Try it once)", "Try it once"),
    KoreanWordCard("해보다", "to try (action)", "haeboda", "먹어봐요 (Try eating)", "Try eating"),
    KoreanWordCard("시작하다", "to start", "sijakada", "시작해요 (Let's start)", "Let's start"),
    KoreanWordCard("완료하다", "to complete", "wallyohada", "완료했어요 (I completed it)", "I completed it"),
    KoreanWordCard("성공하다", "to succeed", "seonggonghada", "성공했어요 (I succeeded)", "I succeeded"),
    KoreanWordCard("실패하다", "to fail", "silpaehada", "실패했어요 (I failed)", "I failed"),
    KoreanWordCard("참가하다", "to participate", "chamgahada", "참가해요 (I participate)", "I participate"),
    KoreanWordCard("참석하다", "to attend", "chamseokada", "회의에 참석해요 (I attend the meeting)", "I attend the meeting"),
    KoreanWordCard("합격하다", "to pass (an exam)", "hapgyeokada", "시험에 합격했어요 (I passed the exam)", "I passed the exam"),
    KoreanWordCard("불합격하다", "to fail (an exam)", "bulhapgyeokada", "불합격했어요 (I failed the exam)", "I failed the exam"),
    KoreanWordCard("응원하다", "to cheer for / to support", "eungwonhada", "응원해요 (I cheer for you)", "I cheer for you"),
    KoreanWordCard("추천하다", "to recommend", "cheucheonada", "추천해요 (I recommend)", "I recommend"),
    KoreanWordCard("초대하다", "to invite", "chodaehada", "초대해요 (I invite you)", "I invite you"),
    KoreanWordCard("환영하다", "to welcome", "hwanyeonghada", "환영해요 (I welcome you)", "I welcome you"),
    KoreanWordCard("거절하다", "to refuse / to reject", "geojjeolada", "거절했어요 (I refused)", "I refused"),
    KoreanWordCard("수락하다", "to accept / to agree", "surakada", "수락했어요 (I accepted)", "I accepted"),
    KoreanWordCard("약속하다", "to promise", "yaksokada", "약속했어요 (I promised)", "I promised"),
    KoreanWordCard("결정하다", "to decide", "gyeoljeonghada", "결정했어요 (I decided)", "I decided"),
    KoreanWordCard("선택하다", "to choose / to select", "seontaekada", "선택했어요 (I chose)", "I chose"),
]

# Social & Interaction Verbs (161-185)
VERBS_161_185 = [
    KoreanWordCard("만나다", "to meet", "mannada", "친구를 만나요 (I meet a friend)", "I meet a friend"),
    KoreanWordCard("만나다", "to get to know / to date", "mannada", "남자친구를 만나요 (I have a boyfriend)", "I have a boyfriend"),
    KoreanWordCard("약속하다", "to make a promise / appointment", "yaksokada", "약속했어요 (I made a promise)", "I made a promise"),
    KoreanWordCard("초대하다", "to invite", "chodaehada", "파티에 초대해요 (I invite to a party)", "I invite to a party"),
    KoreanWordCard("방문하다", "to visit", "bangmunhada", "친구를 방문해요 (I visit a friend)", "I visit a friend"),
    KoreanWordCard("놀러가다", "to go visit / to go hang out", "nolleogada", "친구 집에 놀러 가요 (I go visit a friend's house)", "I go visit a friend's house"),
    KoreanWordCard("놀다", "to play / to hang out", "nolda", "친구들이랑 놀아요 (I hang out with friends)", "I hang out with friends"),
    KoreanWordCard("파티하다", "to party", "patihada", "파티해요 (We're partying)", "We're partying"),
    KoreanWordCard("소개하다", "to introduce", "sogaeada", "소개해요 (Let me introduce)", "Let me introduce"),
    KoreanWordCard("인사하다", "to greet / to say hello", "insahada", "인사해요 (Say hello)", "Say hello"),
    KoreanWordCard("작별하다", "to say goodbye", "jakbyeolhada", "작별해요 (Say goodbye)", "Say goodbye"),
    KoreanWordCard("안부하다", "to ask about someone's well-being", "anbuada", "안부 전해주세요 (Please give my regards)", "Please give my regards"),
    KoreanWordCard("축하하다", "to congratulate", "chukhada", "축하해요 (Congratulations)", "Congratulations"),
    KoreanWordCard("감사하다", "to thank / to be grateful", "gamsahada", "감사해요 (Thank you)", "Thank you"),
    KoreanWordCard("사과하다", "to apologize", "sagwahada", "사과했어요 (I apologized)", "I apologized"),
    KoreanWordCard("용서하다", "to forgive", "yongseohada", "용서해 주세요 (Please forgive)", "Please forgive"),
    KoreanWordCard("친하다", "to be close (friends)", "chinhada", "우리는 친해요 (We're close)", "We're close"),
    KoreanWordCard("싸우다", "to fight / to argue", "ssauda", "싸우지 마세요 (Don't fight)", "Don't fight"),
    KoreanWordCard("화해하다", "to make up / to reconcile", "hwahaehada", "화해했어요 (We made up)", "We made up"),
    KoreanWordCard("결혼하다", "to marry", "gyeolhonhada", "결혼했어요 (I got married)", "I got married"),
    KoreanWordCard("이혼하다", "to divorce", "ihonhada", "이혼했어요 (I got divorced)", "I got divorced"),
    KoreanWordCard("약혼하다", "to be engaged", "yakhonhada", "약혼했어요 (I got engaged)", "I got engaged"),
    KoreanWordCard("소개받다", "to be introduced (for dating)", "sogaebatda", "소개받았어요 (I was introduced to someone)", "I was introduced to someone"),
    KoreanWordCard("사귀다", "to date (someone)", "sagwida", "남자친구랑 사귀어요 (I'm dating a guy)", "I'm dating a guy"),
    KoreanWordCard("헤어지다", "to break up", "heeojida", "헤어졌어요 (We broke up)", "We broke up"),
    KoreanWordCard("절교하다", "to cut ties / to end friendship", "jeolgyohada", "절교했어요 (I ended the friendship)", "I ended the friendship"),
]

# Miscellaneous Common Verbs (186-210)
VERBS_186_210 = [
    KoreanWordCard("필요하다", "to need / to be necessary", "piryohada", "필요해요 (I need it)", "I need it"),
    KoreanWordCard("원하다", "to want", "wonhada", "원해요 (I want it)", "I want it"),
    KoreanWordCard("바라다", "to wish / to hope", "barada", "바라요 (I wish for it)", "I wish for it"),
    KoreanWordCard("찾다", "to find / to look for", "chatda", "열쇠를 찾아요 (I'm looking for keys)", "I'm looking for keys"),
    KoreanWordCard("잃다", "to lose", "ilta", "지갑을 잃어버렸어요 (I lost my wallet)", "I lost my wallet"),
    KoreanWordCard("놓다", "to put / to place", "nota", "책상 위에 놔요 (I put it on the desk)", "I put it on the desk"),
    KoreanWordCard("두다", "to place / to keep", "duda", "여기에 둬요 (Put it here)", "Put it here"),
    KoreanWordCard("옮기다", "to move / to transfer", "omgida", "짐을 옮겨요 (I'm moving luggage)", "I'm moving luggage"),
    KoreanWordCard("수리하다", "to repair / to fix", "suriada", "컴퓨터를 수리해요 (I'm fixing the computer)", "I'm fixing the computer"),
    KoreanWordCard("고치다", "to fix / to repair", "ochida", "고쳐주세요 (Please fix it)", "Please fix it"),
    KoreanWordCard("깨지다", "to break / to shatter", "kkaejida", "유리가 깨졌어요 (The glass broke)", "The glass broke"),
    KoreanWordCard("부러지다", "to snap / to break off", "bureojida", "부러졌어요 (It snapped)", "It snapped"),
    KoreanWordCard("작동하다", "to operate / to work", "jakdonghada", "작동해요 (It works)", "It works"),
    KoreanWordCard("열다", "to open", "yeolda", "문을 열어요 (I open the door)", "I open the door"),
    KoreanWordCard("닫다", "to close", "datda", "문을 닫아요 (I close the door)", "I close the door"),
    KoreanWordCard("잠그다", "to lock", "jamgeuda", "문을 잠가요 (I lock the door)", "I lock the door"),
    KoreanWordCard("잠기다", "to be locked", "jamgida", "문이 잠겼어요 (The door is locked)", "The door is locked"),
    KoreanWordCard("나오다", "to come out / to exit", "naoda", "밖으로 나와요 (Come out)", "Come out"),
    KoreanWordCard("들어가다", "to enter / to go in", "deureogada", "방에 들어가요 (Go into the room)", "Go into the room"),
    KoreanWordCard("기다리다", "to wait", "gidarida", "기다려 주세요 (Please wait)", "Please wait"),
    KoreanWordCard("지키다", "to keep / to protect / to observe", "jikida", "약속을 지켜요 (I keep the promise)", "I keep the promise"),
    KoreanWordCard("어기다", "to break (a promise/rule)", "eogida", "약속을 어겼어요 (I broke the promise)", "I broke the promise"),
    KoreanWordCard("지나다", "to pass / to elapse", "jinada", "시간이 지났어요 (Time has passed)", "Time has passed"),
    KoreanWordCard("늦다", "to be late", "neuta", "늦었어요 (I'm late)", "I'm late"),
    KoreanWordCard("빠르다", "to be fast / quick", "ppareuda", "빨라요 (It's fast)", "It's fast"),
    KoreanWordCard("늦어지다", "to become late", "neueojida", "늦어졌어요 (It became late)", "It became late"),
]


def generate_deck(output_file="decks/16_korean_verbs_common.apkg"):
    """Generate the Anki deck with common verbs."""
    model = create_word_model()
    deck = genanki.Deck(DECK_ID, "16. Korean Common Verbs - 자주 쓰는 동사")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        notes = []

        # Add all verb cards
        all_cards = (
            VERBS_1_15 + VERBS_16_40 + VERBS_41_65 + VERBS_66_90 +
            VERBS_91_115 + VERBS_116_135 + VERBS_136_160 +
            VERBS_161_185 + VERBS_186_210
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
        print(f"  - {len(notes)} verbs")
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
