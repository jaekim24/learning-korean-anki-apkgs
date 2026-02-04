#!/usr/bin/env python3
"""
Korean Common Phrases Anki Deck Generator

Creates Anki decks for the 300 most commonly used Korean phrases.
Usage: python3 korean_phrases_common.py
"""

import genanki
import os
import tempfile
import shutil
from lib.korean_deck_base import (
    KoreanSentenceCard, add_sentence_note, create_sentence_model,
    DECK_IDS, MODEL_IDS, generate_deck, generate_audio
)

# Deck ID
DECK_ID = 1837523963
MODEL_ID = MODEL_IDS["sentence"]


# Greetings & Basic Phrases (1-30)
PHRASES_1_30 = [
    # Greetings
    KoreanSentenceCard("안녕하세요?", "Hello? / How are you?", "annyeonghaseyo - standard polite greeting"),
    KoreanSentenceCard("안녕하세요!", "Hello!", "annyeonghaseyo - standard greeting"),
    KoreanSentenceCard("안녕?", "Hi? (casual)", "annyeong - casual greeting to friends"),
    KoreanSentenceCard("안녕!", "Hi! (casual)", "annyeong - casual greeting"),
    KoreanSentenceCard("주무세요?", "Did you sleep well? (very formal)", "jumuseyo - honorific greeting"),
    KoreanSentenceCard("잘 주무셨어요?", "Did you sleep well? (formal)", "jal jumusyeosseoyo"),
    KoreanSentenceCard("잘 잤어?", "Did you sleep well? (casual)", "jal jasseo"),
    KoreanSentenceCard("반갑습니다", "Nice to meet you (formal)", "bangapseumnida"),
    KoreanSentenceCard("반가워요", "Nice to meet you (polite)", "bangawoyo"),
    KoreanSentenceCard("만나서 반가워요", "Nice to meet you", "annaseo bangawoyo"),

    # Goodbyes
    KoreanSentenceCard("안녕히 가세요", "Goodbye (to person leaving)", "annyeonghi gaseyo - stay in peace"),
    KoreanSentenceCard("안녕히 계세요", "Goodbye (to person staying)", "annyeonghi gyeseyo"),
    KoreanSentenceCard("안녕!", "Bye! (casual)", "annyeong"),
    KoreanSentenceCard("또 봐요!", "See you again!", "tto bwayo"),
    KoreanSentenceCard("내일 봐요", "See you tomorrow", "naeil bwayo"),
    KoreanSentenceCard("나중에 봐요", "See you later", "najung-e bwayo"),
    KoreanSentenceCard("다음에 봐요", "See you next time", "da-eum-e bwayo"),
    KoreanSentenceCard("잘 가요", "Go well (goodbye to person leaving)", "jal gayo"),
    KoreanSentenceCard("잘 있어", "Be well (goodbye)", "jal isseo"),

    # Thank You & Sorry
    KoreanSentenceCard("감사합니다", "Thank you (formal)", "gamsahamnida"),
    KoreanSentenceCard("감사해요", "Thank you (polite)", "gamsahaeyo"),
    KoreanSentenceCard("고마워요", "Thank you (polite, common)", "gomawoyo"),
    KoreanSentenceCard("고마워", "Thanks (casual)", "gomawo"),
    KoreanSentenceCard("정말 고마워요", "Thank you very much", "jeongmal gomawoyo"),
    KoreanSentenceCard("대단히 감사합니다", "Thank you very much (formal)", "daedanhi gamsahamnida"),
    KoreanSentenceCard("천만에요", "You're welcome", "cheonman-eyo"),
    KoreanSentenceCard("별말씀을요", "Don't mention it", "byeolmalsseum-eyo"),
    KoreanSentenceCard("아니에요", "No problem / Not at all", "anieyo"),
    KoreanSentenceCard("아니야", "No (casual)", "aniya"),
    KoreanSentenceCard("죄송합니다", "I'm sorry (formal)", "joesonghamnida"),
    KoreanSentenceCard("죄송해요", "I'm sorry (polite)", "joesonghaeyo"),
    KoreanSentenceCard("미안해요", "I'm sorry (polite)", "mianhaeyo"),
    KoreanSentenceCard("미안해", "Sorry (casual)", "mianhae"),
    KoreanSentenceCard("괜찮아요", "It's okay / No problem", "gwaenchanaeyo"),
    KoreanSentenceCard("괜찮아", "It's okay (casual)", "gwaenchana"),
    KoreanSentenceCard("상관없어요", "It doesn't matter", "sanggwan-eopseoyo"),
    KoreanSentenceCard("신경 쓰지 마세요", "Don't worry about it", "singyeong sseuji maseyo"),
    KoreanSentenceCard("걱정하지 마세요", "Don't worry", "geokjeonghaji maseyo"),
]

# Yes, No & Basic Responses (31-60)
PHRASES_31_60 = [
    KoreanSentenceCard("네", "Yes (formal/polite)", "ne"),
    KoreanSentenceCard("예", "Yes (formal)", "ye"),
    KoreanSentenceCard("아니요", "No (polite)", "aniyo"),
    KoreanSentenceCard("아니", "No (casual)", "ani"),
    KoreanSentenceCard("그래요", "That's right / I see", "geuraeyo"),
    KoreanSentenceCard("맞아요", "That's right / Correct", "majayo"),
    KoreanSentenceCard("그렇습니까?", "Is that so? (formal)", "geureoseumnikka"),
    KoreanSentenceCard("그래?", "Really? / Is that right? (casual)", "geurae"),
    KoreanSentenceCard("진짜요?", "Really?", "jinjjayo"),
    KoreanSentenceCard("진짜?", "Really? (casual)", "jinjja"),
    KoreanSentenceCard("정말?", "Really? (casual)", "jeongmal"),
    KoreanSentenceCard("알겠습니다", "I understand (formal)", "algetseumnida"),
    KoreanSentenceCard("알겠어요", "I understand (polite)", "algesseoyo"),
    KoreanSentenceCard("알았어", "Got it (casual)", "arasseo"),
    KoreanSentenceCard("모르겠습니다", "I don't know (formal)", "moreugesseumnida"),
    KoreanSentenceCard("몰라요", "I don't know (polite)", "mollayo"),
    KoreanSentenceCard("몰라", "I don't know (casual)", "molla"),
    KoreanSentenceCard("잘 모르겠어요", "I'm not sure", "jal moreugesseoyo"),
    KoreanSentenceCard("글쎄요", "Well... / I'm not sure", "geulsseyo"),
    KoreanSentenceCard("아마", "Maybe / Probably", "ama"),
    KoreanSentenceCard("아마도", "Perhaps", "amado"),
    KoreanSentenceCard("아닌가 봐요", "I guess not", "anin-ga bwayo"),
    KoreanSentenceCard("그런 것 같아요", "I think so", "geureon geot gatayo"),
    KoreanSentenceCard("생각해요", "I think so", "saenggakhaeyo"),
    KoreanSentenceCard("되돌려죠", "I suppose so", "doedollyejwo"),
    KoreanSentenceCard("물론이지요", "Of course", "mullon-ijiyo"),
    KoreanSentenceCard("당연하지요", "Naturally / Of course", "dangyeonhajiyo"),
    KoreanSentenceCard("물론이고요", "Of course", "mullon-igoyo"),
    KoreanSentenceCard("안 돼요", "It's not okay / Can't do that", "an dwaeyo"),
    KoreanSentenceCard("안 돼", "No / Can't (casual)", "an dwae"),
]

# Introductions & Personal Info (61-90)
PHRASES_61_90 = [
    KoreanSentenceCard("제 이름은 [name]입니다", "My name is [name]", "je ireumeun [name]imnida"),
    KoreanSentenceCard("제 이름은 [name]이에요", "My name is [name] (polite)", "je ireumeun [name]ieyo"),
    KoreanSentenceCard("저는 [name]라고 해요", "I'm called [name]", "jeoneun [name]rago haeyo"),
    KoreanSentenceCard("이름이 뭐예요?", "What's your name?", "ireumi mwoyeyo"),
    KoreanSentenceCard("성함이 어떻게 되세요?", "What's your name? (formal)", "seongham-e eotteoke doeseyo"),
    KoreanSentenceCard("한국 사람이에요", "I'm Korean", "hanguk saram-ieyo"),
    KoreanSentenceCard("미국 사람이에요", "I'm American", "miguk saram-ieyo"),
    KoreanSentenceCard("일본 사람이에요", "I'm Japanese", "ilbon saram-ieyo"),
    KoreanSentenceCard("중국 사람이에요", "I'm Chinese", "jungguk saram-ieyo"),
    KoreanSentenceCard("어느 나라 사람이에요?", "What country are you from?", "eoneu nara saram-ieyo"),
    KoreanSentenceCard("어디에서 왔어요?", "Where are you from?", "eodieseo wasseoyo"),
    KoreanSentenceCard("어디 사세요?", "Where do you live?", "eodi saseyo"),
    KoreanSentenceCard("서울에 살아요", "I live in Seoul", "seoeu-e sarayo"),
    KoreanSentenceCard("저는 서울에서 왔어요", "I'm from Seoul", "jeoneun seoeu-eseo wasseoyo"),
    KoreanSentenceCard("직업이 뭐예요?", "What's your job?", "jigeobi mwoyeyo"),
    KoreanSentenceCard("무엇을 하세요?", "What do you do?", "mueoseul haseyo"),
    KoreanSentenceCard("학생이에요", "I'm a student", "haksaeng-ieyo"),
    KoreanSentenceCard("선생님이에요", "I'm a teacher", "seonsaengnim-ieyo"),
    KoreanSentenceCard("회사원이에요", "I'm an office worker", "hoesawon-ieyo"),
    KoreanSentenceCard("의사예요", "I'm a doctor", "uisayeyo"),
    KoreanSentenceCard("변호사예요", "I'm a lawyer", "byeonhosayeyo"),
    KoreanSentenceCard("엔지니어예요", "I'm an engineer", "enjinieoyeyo"),
    KoreanSentenceCard("무직이에요", "I'm unemployed", "mujig-ieyo"),
    KoreanSentenceCard("은퇴했어요", "I'm retired", "euntoehaessyeoyo"),
    KoreanSentenceCard("나이가 어떻게 되세요?", "How old are you? (formal)", "naiga eotteoke doeseyo"),
    KoreanSentenceCard("몇 살이에요?", "How old are you?", "myeot sal-ieyo"),
    KoreanSentenceCard("스물다섯 살이에요", "I'm 25 years old", "seumuldaseot sal-ieyo"),
    KoreanSentenceCard("나이는 비밀이에요", "My age is a secret", "naigineun bimil-ieyo"),
    KoreanSentenceCard("결혼했어요?", "Are you married?", "gyeolhonhaesseoyo"),
    KoreanSentenceCard("아니요, 돌싱이에요", "No, I'm single (divorced)", "aniyo, dolsing-ieyo"),
    KoreanSentenceCard("아니요, 총각이에요", "No, I'm single (male)", "aniyo, chonggag-ieyo"),
    KoreanSentenceCard("아니요, 미혼이에요", "No, I'm unmarried", "aniyo, mihon-ieyo"),
]

# Getting to Know People (91-120)
PHRASES_91_120 = [
    KoreanSentenceCard("취미가 뭐예요?", "What are your hobbies?", "chwemiga mwoyeyo"),
    KoreanSentenceCard("무엇을 좋아하세요?", "What do you like?", "mueoseul joahaseyo"),
    KoreanSentenceCard("무엇을 좋아해요?", "What do you like? (polite)", "mueoseul joahaeyo"),
    KoreanSentenceCard("음악을 좋아해요", "I like music", "eumageul joahaeyo"),
    KoreanSentenceCard("영화를 좋아해요", "I like movies", "yeonghwareul joahaeyo"),
    KoreanSentenceCard("독서를 좋아해요", "I like reading", "dokseoreul joahaeyo"),
    KoreanSentenceCard("운동을 좋아해요", "I like exercising", "undongeul joahaeyo"),
    KoreanSentenceCard("요리를 좋아해요", "I like cooking", "yorireul joahaeyo"),
    KoreanSentenceCard("여행을 좋아해요", "I like traveling", "yeohaengeul joahaeyo"),
    KoreanSentenceCard("게임을 좋아해요", "I like games", "geimeul joahaeyo"),
    KoreanSentenceCard("특별한 취미가 없어요", "I don't have any special hobbies", "teukbyeolhan chumi-ga eopsseoyo"),
    KoreanSentenceCard("가족이 몇 명이에요?", "How many family members?", "gajogi myeot myeong-ieyo"),
    KoreanSentenceCard("우리 가족은 4명이에요", "There are 4 in my family", "uri gajogeun 4myeong-ieyo"),
    KoreanSentenceCard("형제가 있어요?", "Do you have siblings?", "hyeongje-ga isseoyo"),
    KoreanSentenceCard("오빠가 있어요", "I have an older brother", "oppa-ga isseoyo"),
    KoreanSentenceCard("언니가 있어요", "I have an older sister", "eonni-ga isseoyo"),
    KoreanSentenceCard("남동생이 있어요", "I have a younger brother", "namdongsaeng-i isseoyo"),
    KoreanSentenceCard("여동생이 있어요", "I have a younger sister", "yeodongsaeng-i isseoyo"),
    KoreanSentenceCard("외동아이에요", "I'm an only child", "oedong-a-ieyo"),
    KoreanSentenceCard("키가 크다", "(You are) tall", "kiga keuda"),
    KoreanSentenceCard("키가 작아요", "(I'm) short", "kiga jagayo"),
    KoreanSentenceCard("전화번호 알려주세요", "Please tell me your phone number", "jeonhwabeonho allyeojuseyo"),
    KoreanSentenceCard("이메일 주소 알려주세요", "Please tell me your email address", "imeil juso allyeojuseyo"),
    KoreanSentenceCard("카카오톡 있어요?", "Do you have KakaoTalk?", "kakaotok isseoyo"),
    KoreanSentenceCard("인스타그램 해요?", "Do you use Instagram?", "inseutageuraem haeyo"),
    KoreanSentenceCard("친구 추가해요", "Add me as a friend", "chingu chogahaeyo"),
    KoreanSentenceCard("연락 드릴게요", "I'll contact you", "yeollak deurilgeyo"),
    KoreanSentenceCard("나중에 연락할게요", "I'll contact you later", "najung-e yeollakhalgeyo"),
    KoreanSentenceCard("시간 될 때 전화하세요", "Call me when you have time", "sigandoel ttae jeonhwahaseyo"),
]

# Asking for Help & Communication (121-150)
PHRASES_121_150 = [
    KoreanSentenceCard("도와주세요", "Please help me", "dowajuseyo"),
    KoreanSentenceCard("도와줄 수 있어요?", "Can you help me?", "dowajul su isseoyo"),
    KoreanSentenceCard("도와주실 수 있나요?", "Could you help me?", "dowajusil su innayo"),
    KoreanSentenceCard("제가 도와드릴까요?", "Can I help you?", "jega dowadeurilkkayo"),
    KoreanSentenceCard("뭐 도와드릴까요?", "What can I help you with?", "mwo dowadeurilkkayo"),
    KoreanSentenceCard("괜찮으시다면 도와드릴게요", "If you don't mind, I'll help you", "gwaencheusimyeon dowadeurilgeyo"),
    KoreanSentenceCard("영어를 하실 수 있나요?", "Can you speak English?", "yeong-eoreul hasil su innayo"),
    KoreanSentenceCard("한국어를 할 수 있어요?", "Can you speak Korean?", "hangugeoreul hal su isseoyo"),
    KoreanSentenceCard("영어를 해요", "I speak English", "yeong-eoreul haeyo"),
    KoreanSentenceCard("한국어를 조금해요", "I speak a little Korean", "hangugeoreul jogeumhaeyo"),
    KoreanSentenceCard("한국어를 잘 못해요", "I'm not good at Korean", "hangugeoreul jal mothaeyo"),
    KoreanSentenceCard("아직 한국어를 배우고 있어요", "I'm still learning Korean", "ajik hangugeoreul baeugo isseoyo"),
    KoreanSentenceCard("천천히 말씀해 주세요", "Please speak slowly", "cheoncheonhi malsseumhae juseyo"),
    KoreanSentenceCard("다시 한번 말씀해 주세요", "Please say that again", "dasi hanbeon malsseumhae juseyo"),
    KoreanSentenceCard("이해가 안 돼요", "I don't understand", "ihaega-an dwaeyo"),
    KoreanSentenceCard("이해가 잘 안 돼요", "I don't understand well", "ihaega jal an dwaeyo"),
    KoreanSentenceCard("무슨 뜻이에요?", "What does it mean?", "mseun tteusieyo"),
    KoreanSentenceCard("무슨 말이에요?", "What are you saying?", "mseu mar-ieyo"),
    KoreanSentenceCard("그게 무슨 뜻이에요?", "What does that mean?", "geuge mseun tteusieyo"),
    KoreanSentenceCard("글쎄요, 이해가 안 가네요", "Well, I don't get it", "geulsseyo, ihaega-an ganeyo"),
    KoreanSentenceCard("한국어로 어떻게 말해요?", "How do you say it in Korean?", "hangukeoro eotteoke malhaeyo"),
    KoreanSentenceCard("이것 한국어로 뭐예요?", "What's this in Korean?", "igeot hangukeoro mwoyeyo"),
    KoreanSentenceCard("그것 한국어로 뭐예요?", "What's that in Korean?", "geugeot hangukeoro mwoyeyo"),
    KoreanSentenceCard("번역해 주실 수 있나요?", "Could you translate for me?", "beonyeokhaejusil su innayo"),
    KoreanSentenceCard("번역기 있어요?", "Do you have a translator?", "beonyeokgi isseoyo"),
    KoreanSentenceCard("적어 주세요", "Please write it down", "jeogeo juseyo"),
    KoreanSentenceCard("철자가 어떻게 돼요?", "How do you spell it?", "cheoljaga eotteoke dwaeyo"),
    KoreanSentenceCard("발음이 어려워요", "The pronunciation is difficult", "bareum-i eoryeowoyo"),
    KoreanSentenceCard("한번 더 말해 주세요", "Please say it one more time", "hanbeon deo malhae juseyo"),
    KoreanSentenceCard("들리지 않아요", "I can't hear (you)", "deulliji anayo"),
]

# At a Restaurant (151-180)
PHRASES_151_180 = [
    KoreanSentenceCard("여기요!", "Excuse me! / Here! (calling staff)", "yeogiyo"),
    KoreanSentenceCard("저기요!", "Excuse me! (calling attention)", "jeogiyo"),
    KoreanSentenceCard("메뉴 주세요", "Can I have the menu?", "menyu juseyo"),
    KoreanSentenceCard("주문하겠습니다", "I'd like to order", "jumunhagessseumnida"),
    KoreanSentenceCard("주문할게요", "I'll order (now)", "jumunhalgeyo"),
    KoreanSentenceCard("뭐 드시겠어요?", "What would you like to order?", "mwo deusigesseoyo"),
    KoreanSentenceCard("뭐 먹을래요?", "What would you like to eat?", "mwo meogeullaeyo"),
    KoreanSentenceCard("이거 주세요", "I'll have this, please", "igeo juseyo"),
    KoreanSentenceCard("이것으로 주세요", "I'll have this one", "igeoseuro juseyo"),
    KoreanSentenceCard("김치찌개 주세요", "Kimchi stew, please", "gimchijjigae juseyo"),
    KoreanSentenceCard("비빔밥 주세요", "Bibimbap, please", "bibimbap juseyo"),
    KoreanSentenceCard("불고기 주세요", "Bulgogi, please", "bulgogi juseyo"),
    KoreanSentenceCard("삼겹살 주세요", "Pork belly, please", "samgyeopsal juseyo"),
    KoreanSentenceCard("라면 주세요", "Ramyun, please", "ramyeon juseyo"),
    KoreanSentenceCard("짜장면 주세요", "Jjajangmyeon, please", "jjajangmyeon juseyo"),
    KoreanSentenceCard("볶음밥 주세요", "Fried rice, please", "bokkeumbap juseyo"),
    KoreanSentenceCard("냉면 주세요", "Cold noodles, please", "naengmyeon juseyo"),
    KoreanSentenceCard("된장찌개 주세요", "Doenjang stew, please", "doenjangjjigae juseyo"),
    KoreanSentenceCard("같이 먹을까요?", "Shall we eat together?", "gachi meogeulkkayo"),
    KoreanSentenceCard("맛있게 드세요", "Enjoy your meal", "masitge deuseyo"),
    KoreanSentenceCard("잘 먹겠습니다", "Thank you for the food (before eating)", "jal meokgetseumnida"),
    KoreanSentenceCard("잘 먹을게요", "I'll eat well (informal)", "jal meogeulgeyo"),
    KoreanSentenceCard("맛있어 보여요", "It looks delicious", "masitbo boyeyo"),
    KoreanSentenceCard("맛있어요", "It's delicious", "masisseoyo"),
    KoreanSentenceCard("정말 맛있어요", "It's really delicious", "jeongmal masisseoyo"),
    KoreanSentenceCard("너무 맛있어요", "It's so delicious", "neomu masisseoyo"),
    KoreanSentenceCard("맛없어요", "It doesn't taste good", "madeopseoyo"),
    KoreanSentenceCard("맛이 괜찮아요", "The taste is okay", "masi gwaenchanaeyo"),
    KoreanSentenceCard("너무 매워요", "It's too spicy", "neomu maewoyo"),
    KoreanSentenceCard("안 매워요", "It's not spicy", "an maewoyo"),
    KoreanSentenceCard("좀 더 주세요", "Please give me a little more", "jom deo juseyo"),
    KoreanSentenceCard("국물 있어요?", "Is there soup?", "gukmul isseoyo"),
]

# Shopping & Numbers (181-210)
PHRASES_181_210 = [
    KoreanSentenceCard("이게 얼마예요?", "How much is this?", "ige eolmayeyo"),
    KoreanSentenceCard("저것 얼마예요?", "How much is that?", "jeogeot eolmayeyo"),
    KoreanSentenceCard("가격이 어떻게 돼요?", "What's the price?", "gagyeogi eotteoke dwaeyo"),
    KoreanSentenceCard("너무 비싸요", "It's too expensive", "neomu bissayo"),
    KoreanSentenceCard("좀 싼 거 있어요?", "Do you have anything cheaper?", "jom ssan geo isseoyo"),
    KoreanSentenceCard("할인해 주세요", "Please give me a discount", "halinhae juseyo"),
    KoreanSentenceCard("깎아 주세요", "Please lower the price", "kkakka juseyo"),
    KoreanSentenceCard("얼면에 팔아요?", "Will you sell for [amount]?", "eolmyeone parayo"),
    KoreanSentenceCard("계산해 주세요", "Please calculate (the bill)", "gyesanhae juseyo"),
    KoreanSentenceCard("여기 계산할게요", "I'll pay here", "yeogi gyesanhalgeyo"),
    KoreanSentenceCard("카드로 결제해 주세요", "Please pay by card", "kadeuro gyeoljaehae juseyo"),
    KoreanSentenceCard("현금으로 할게요", "I'll pay in cash", "hyeongeumeuro halgeyo"),
    KoreanSentenceCard("영수증 주세요", "Please give me a receipt", "yeongsujeung juseyo"),
    KoreanSentenceCard("봉투 필요 없어요", "I don't need a bag", "bongtu piryoeopseoyo"),
    KoreanSentenceCard("사이즈가 어때요?", "How's the size?", "saijuga eottaeyo"),
    KoreanSentenceCard("입어 볼 수 있어요?", "Can I try it on?", "ibeo bol su isseoyo"),
    KoreanSentenceCard("신어 볼 수 있나요?", "Can I try them on (shoes)?", "sineo bol su innayo"),
    KoreanSentenceCard("너무 커요", "It's too big", "neomu keoyo"),
    KoreanSentenceCard("너무 작아요", "It's too small", "neomu jagayo"),
    KoreanSentenceCard("딱 맞아요", "It fits perfectly", "ttak majayo"),
    KoreanSentenceCard("좀 큰 거 있어요?", "Do you have a bigger size?", "jom keun geo isseoyo"),
    KoreanSentenceCard("좀 작은 거 있어요?", "Do you have a smaller size?", "jom jageun geo isseoyo"),
    KoreanSentenceCard("색상이 어때요?", "How's the color?", "saeksang-i eottaeyo"),
    KoreanSentenceCard("다른 색 있어요?", "Do you have other colors?", "dareun saek isseoyo"),
    KoreanSentenceCard("이거 살게요", "I'll buy this", "igeo salgeyo"),
    KoreanSentenceCard("안 살게요", "I won't buy this", "an salgeyo"),
    KoreanSentenceCard("그냥 볼게요", "Just looking", "geunyang bolgeyo"),
    KoreanSentenceCard("구경만 할게요", "Just browsing", "gugyeongman halgeyo"),
    KoreanSentenceCard("다음에 올게요", "I'll come next time", "da-eume olgeyo"),
]

# Directions & Locations (211-240)
PHRASES_211_240 = [
    KoreanSentenceCard("화장실이 어디예요?", "Where is the restroom?", "hwajangsil-i eodiyeyo"),
    KoreanSentenceCard("화장실 어디 있어요?", "Where is the bathroom?", "hwajangsil eodi isseoyo"),
    KoreanSentenceCard("지하에 있어요", "It's in the basement", "jiha-e isseoyo"),
    KoreanSentenceCard("2층에 있어요", "It's on the 2nd floor", "2cheung-e isseoyo"),
    KoreanSentenceCard("역이 어디예요?", "Where is the station?", "yeog-i eodiyeyo"),
    KoreanSentenceCard("지하철역 어디예요?", "Where is the subway station?", "jihacheolyeog eodiyeyo"),
    KoreanSentenceCard("버스정류장 어디예요?", "Where is the bus stop?", "beoseojeongnyujang eodiyeyo"),
    KoreanSentenceCard("택시 승강장 어디예요?", "Where is the taxi stand?", "taeksi seunggangjang eodiyeyo"),
    KoreanSentenceCard("공항 어떻게 가요?", "How do I get to the airport?", "gonghang eotteoke gayo"),
    KoreanSentenceCard("서울역 어떻게 가요?", "How do I get to Seoul Station?", "seouryeog eotteoke gayo"),
    KoreanSentenceCard("지금 가장 가까운 역이 어디예요?", "Where's the nearest station?", "jigeum gajang gakkaun yeogi eodiyeyo"),
    KoreanSentenceCard("이 근처에 은행 있어요?", "Is there a bank nearby?", "i geuncheoe eunhaeng isseoyo"),
    KoreanSentenceCard("병원 어디 있어요?", "Where is the hospital?", "byeongwon eodi isseoyo"),
    KoreanSentenceCard("약국 어디예요?", "Where is the pharmacy?", "yakguk eodiyeyo"),
    KoreanSentenceCard("편의점 어디예요?", "Where is the convenience store?", "pyeonijeom eodiyeyo"),
    KoreanSentenceCard("슈퍼 어디예요?", "Where is the supermarket?", "syupeo eodiyeyo"),
    KoreanSentenceCard("시장 어디예요?", "Where is the market?", "sijang eodiyeyo"),
    KoreanSentenceCard("카페 어디예요?", "Where is a cafe?", "kapi eodiyeyo"),
    KoreanSentenceCard("은행 어디 있어요?", "Where is the bank?", "eunhaeng eodi isseoyo"),
    KoreanSentenceCard("우체국 어디예요?", "Where is the post office?", "ucheguk eodiyeyo"),
    KoreanSentenceCard("경찰서 어디예요?", "Where is the police station?", "gyeongchalseo eodiyeyo"),
    KoreanSentenceCard("오른쪽으로 가세요", "Go to the right", "oreunjjogeuro gaseyo"),
    KoreanSentenceCard("왼쪽으로 가세요", "Go to the left", "wenjjogeuro gaseyo"),
    KoreanSentenceCard("곧장 가세요", "Go straight", "gojjang gaseyo"),
    KoreanSentenceCard("똑바로 가세요", "Go straight ahead", "ttokbaro gaseyo"),
    KoreanSentenceCard("여기서 가까워요", "It's close from here", "yeogiseo gakkawoyo"),
    KoreanSentenceCard("멀어요", "It's far", "meoleoyyo"),
    KoreanSentenceCard("걸어서 갈 수 있어요?", "Can I walk there?", "georeoseo gal su isseoyo"),
    KoreanSentenceCard("택시 타세요", "Take a taxi", "taeksi taseyo"),
    KoreanSentenceCard("버스 타세요", "Take a bus", "beoseu taseyo"),
    KoreanSentenceCard("지하철 타세요", "Take the subway", "jihacheol taseyo"),
]

# Time & Schedule (241-270)
PHRASES_241_270 = [
    KoreanSentenceCard("지금 몇 시예요?", "What time is it now?", "jigeum myeot siyeyo"),
    KoreanSentenceCard("지금 몇 시입니까?", "What time is it? (formal)", "jigeum myeot siimnikka"),
    KoreanSentenceCard("9시 10분이에요", "It's 9:10", "9si 10bun-ieyo"),
    KoreanSentenceCard("몇 시에 만날까요?", "What time shall we meet?", "myeot si-e mannalkkayo"),
    KoreanSentenceCard("몇 시에 돼요?", "What time works for you?", "myeot si-e dwaeyo"),
    KoreanSentenceCard("몇 시에 좋아하세요?", "What time is good for you?", "myeot si-e joahaseyo"),
    KoreanSentenceCard("아침에 좋아요", "Morning is good", "achim-e joayoyo"),
    KoreanSentenceCard("오후에 좋아요", "Afternoon is good", "ohue joayoyo"),
    KoreanSentenceCard("저녁에 좋아요", "Evening is good", "jeonyeog-e joayoyo"),
    KoreanSentenceCard("오전에 만나요", "Let's meet in the morning", "ojeone mannayo"),
    KoreanSentenceCard("오후에 만나요", "Let's meet in the afternoon", "ohue mannayo"),
    KoreanSentenceCard("저녁에 만나요", "Let's meet in the evening", "jeonyeog-e mannayo"),
    KoreanSentenceCard("내일 만날까요?", "Shall we meet tomorrow?", "naeil mannalkkayo"),
    KoreanSentenceCard("모레 만날까요?", "Shall we meet the day after tomorrow?", "more mannalkkayo"),
    KoreanSentenceCard("주말에 만날까요?", "Shall we meet on the weekend?", "jumale mannalkkayo"),
    KoreanSentenceCard("언제 시간이 돼요?", "When are you available?", "eonje sigani dwaeyo"),
    KoreanSentenceCard("언제 좋으세요?", "When is good for you?", "eonje joeuseyo"),
    KoreanSentenceCard("오늘 안 돼요", "Today doesn't work", "oneul an dwaeyo"),
    KoreanSentenceCard("내일은 안 돼요", "Tomorrow doesn't work", "naeil-eun an dwaeyo"),
    KoreanSentenceCard("다음 주는 어때요?", "How about next week?", "daeum uneun eottaeyo"),
    KoreanSentenceCard("월요일은 어때요?", "How about Monday?", "woryoil-eun eottaeyo"),
    KoreanSentenceCard("화요일은 어때요?", "How about Tuesday?", "hwayoil-eun eottaeyo"),
    KoreanSentenceCard("수요일은 어때요?", "How about Wednesday?", "suyoil-eun eottaeyo"),
    KoreanSentenceCard("목요일은 어때요?", "How about Thursday?", "mogyoil-eun eottaeyo"),
    KoreanSentenceCard("금요일은 어때요?", "How about Friday?", "geumyoil-eun eottaeyo"),
    KoreanSentenceCard("토요일은 어때요?", "How about Saturday?", "toyoil-eun eottaeyo"),
    KoreanSentenceCard("일요일은 어때요?", "How about Sunday?", "iryoil-eun eottaeyo"),
    KoreanSentenceCard("시간이 얼마나 걸려요?", "How long does it take?", "sigani eolmana geollyeoyo"),
    KoreanSentenceCard("30분 걸려요", "It takes 30 minutes", "30bun geollyeoyo"),
    KoreanSentenceCard("1시간 걸려요", "It takes 1 hour", "1sigan geollyeoyo"),
    KoreanSentenceCard("늦었어요", "It's late", "neujisseoyo"),
    KoreanSentenceCard("빨리 와주세요", "Please come quickly", "ppalli wajuseyo"),
]

# Emotions & Opinions (271-300)
PHRASES_271_300 = [
    KoreanSentenceCard("좋아요", "I like it / It's good", "joayoyo"),
    KoreanSentenceCard("좋아", "I like it (casual)", "joa"),
    KoreanSentenceCard("안 좋아요", "I don't like it", "an joayoyo"),
    KoreanSentenceCard("안 좋아", "I don't like it (casual)", "an joa"),
    KoreanSentenceCard("좋아해요", "I like (someone/doing something)", "joahaeyo"),
    KoreanSentenceCard("사랑해요", "I love you", "saranghaeyo"),
    KoreanSentenceCard("사랑해", "I love you (casual)", "saranghae"),
    KoreanSentenceCard("행복해요", "I'm happy", "haengbokhaeyo"),
    KoreanSentenceCard("기분이 좋아요", "I feel good", "gibun-i joayoyo"),
    KoreanSentenceCard("기분이 안 좋아요", "I feel bad", "gibun-i an joayoyo"),
    KoreanSentenceCard("기쁘다", "(I'm) glad", "gippeuda"),
    KoreanSentenceCard("슬퍼요", "I'm sad", "seulpeoyo"),
    KoreanSentenceCard("슬프다", "(I'm) sad", "seupeuda"),
    KoreanSentenceCard("화나요", "I'm angry", "hwanayo"),
    KoreanSentenceCard("화나", "I'm angry (casual)", "hwana"),
    KoreanSentenceCard("화났어요", "I got angry", "hwanasseoyo"),
    KoreanSentenceCard("피곤해요", "I'm tired", "pigonhaeyo"),
    KoreanSentenceCard("피곤해", "I'm tired (casual)", "pigonhae"),
    KoreanSentenceCard("배고파요", "I'm hungry", "baegopayo"),
    KoreanSentenceCard("배고파", "I'm hungry (casual)", "baegopa"),
    KoreanSentenceCard("목말라요", "I'm thirsty", "okmallayo"),
    KoreanSentenceCard("추워요", "It's cold / I'm cold", "chuwoyo"),
    KoreanSentenceCard("더워요", "It's hot / I'm hot", "deowoyo"),
    KoreanSentenceCard("덥다", "(It's) hot", "deopda"),
    KoreanSentenceCard("춥다", "(It's) cold", "chupda"),
    KoreanSentenceCard("아파요", "It hurts / I'm sick", "apayo"),
    KoreanSentenceCard("아파", "It hurts (casual)", "apa"),
    KoreanSentenceCard("머리가 아파요", "I have a headache", "meoriga apayo"),
    KoreanSentenceCard("배가 아파요", "I have a stomachache", "baega apayo"),
    KoreanSentenceCard("목이 아파요", "My throat hurts", "mogi apayo"),
    KoreanSentenceCard("다리가 아파요", "My leg hurts", "dariga apayo"),
    KoreanSentenceCard("재미있어요", "It's fun / interesting", "jaemiisseoyo"),
    KoreanSentenceCard("재미없어요", "It's boring / not fun", "jaemieopseoyo"),
    KoreanSentenceCard("심심해요", "I'm bored", "simsimhaeyo"),
    KoreanSentenceCard("괜찮아요", "It's okay / I'm fine", "gwaenchanaeyo"),
]


def generate_deck(output_file="decks/15_korean_phrases_common.apkg"):
    """Generate the Anki deck with common phrases."""
    model = create_sentence_model()
    deck = genanki.Deck(DECK_ID, "15. Korean Common Phrases - 자주 쓰는 표현")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        notes = []

        # Add all phrase cards
        all_cards = (
            PHRASES_1_30 + PHRASES_31_60 + PHRASES_61_90 + PHRASES_91_120 +
            PHRASES_121_150 + PHRASES_151_180 + PHRASES_181_210 +
            PHRASES_211_240 + PHRASES_241_270 + PHRASES_271_300
        )

        for card in all_cards:
            note = add_sentence_note(deck, model, card, audio_dir)
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
        print(f"  - {len(notes)} phrases")
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
