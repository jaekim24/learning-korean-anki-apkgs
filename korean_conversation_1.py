#!/usr/bin/env python3
"""
Korean Conversation Practice Deck

Common dialogues for everyday situations.
Usage: python3 korean_conversation_1.py
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
DECK_ID = DECK_IDS["conversation_1"]
MODEL_ID = MODEL_IDS["conversation"]


# Conversations: (context, prompt, response, word_pairs, audio_response)
# word_pairs is a list of (korean_word, english_word) tuples for color alignment
CONVERSATIONS = [
    # ===== SELF INTRODUCTIONS =====
    ("First meeting", "안녕하세요? 만나서 반갑습니다.",
     "안녕하세요! 저도 만나서 반갑습니다. 이름이 뭐예요?",
     [("안녕하세요", "Hello"), ("저도", "I too"), ("만나서", "meeting"), ("반갑습니다", "am pleased"), ("이름이", "name"), ("뭐예요", "what is")],
     "Hello! Nice to meet you too. What's your name?"),

    ("First meeting", "이름은 김민수라고 해요. 한국 사람이에요.",
     "반갑습니다, 민수 씨. 저는 일본에서 왔어요.",
     [("반갑습니다", "Nice to meet you"), ("민수 씨", "Minsu"), ("저는", "I"), ("일본에서", "from Japan"), ("왔어요", "came")],
     "Nice to meet you, Minsu. I came from Japan."),

    ("First meeting", "직업은 무엇을 하세요?",
     "저는 회사원이에요. 씨는 무엇을 하시죠?",
     [("저는", "I"), ("회사원이에요", "am an office worker"), ("씨는", "you"), ("무엇을", "what"), ("하시죠", "do (polite)")],
     "I'm an office worker. What do you do?"),

    ("First meeting", "저는 학생이에요. 서울대학교에서 한국어를 공부해요.",
     "아, 한국어를 정말 잘하시네요! 얼마나 공부하셨어요?",
     [("아", "Ah"), ("한국어를", "Korean"), ("정말", "really"), ("잘하시네요", "speak well"), ("얼마나", "how much/long"), ("공부하셨어요", "have studied")],
     "Oh, you speak Korean really well! How long have you studied?"),

    ("First meeting", "6개월 정도 공부했어요. 아직 멀었어요.",
     "아니에요, 정말 잘하시는 것 같아요. 열심히 하시면 곧 더 좋아지실 거예요.",
     [("아니에요", "No"), ("정말", "really"), ("잘하시는", "doing well"), ("것 같아요", "seem"), ("열심히", "hard"), ("하시면", "if you do"), ("곧", "soon"), ("더", "more"), ("좋아지실", "will improve"), ("거예요", "will")],
     "No, you seem very good. If you work hard, you'll get even better soon."),

    ("First meeting", "연락처 좀 알려줄 수 있어요?",
     "네, 제 전화번호는 010-1234-5678이에요. 카카오톡도 해요.",
     [("네", "Yes"), ("제", "my"), ("전화번호는", "phone number"), ("카카오톡도", "KakaoTalk too"), ("해요", "use/do")],
     "Sure, my phone number is 010-1234-5678. I use KakaoTalk too."),

    ("First meeting", "시간 되면 같이 밥 먹어요!",
     "네, 좋아요! 저도 연락드릴게요. 안녕히 가세요!",
     [("네", "Yes"), ("좋아요", "good/sounds good"), ("저도", "I too"), ("연락드릴게요", "will contact"), ("안녕히 가세요", "goodbye")],
     "Yes, sounds good! I'll contact you too. Goodbye!"),

    # ===== ORDERING FOOD =====
    ("Restaurant greeting", "어서 오세요! 몇 분이세요?",
     "세 명이요. 자리 있어요?",
     [("세", "three"), ("명이요", "people"), ("자리", "seat"), ("있어요", "have/exist")],
     "Three people. Do you have a seat?"),

    ("Restaurant seating", "네, 이쪽으로 오세요. 메뉴는 여기 있어요.",
     "네, 감사합니다.",
     [("네", "Yes"), ("감사합니다", "thank you")],
     "Yes, come this way. Here's the menu. Thank you."),

    ("Ordering", "주문하시겠어요?",
     "비빔밥하고 김치찌개 주세요. 물은요?",
     [("비빔밥하고", "bibimbap and"), ("김치찌개", "kimchi stew"), ("주세요", "please give"), ("물은요", "and water")],
     "I'll have bibimbap and kimchi stew. And water?"),

    ("Ordering", "물은 바로 갖다 드릴게요. 다른 거 필요하세요?",
     "아니요, 그게 다요.",
     [("아니요", "No"), ("그게", "that is"), ("다요", "all")],
     "I'll bring water right away. Anything else? No, that's all."),

    ("Asking about food", "이거 매운 거예요?",
     "네, 좀 매워요. 안 매운 것도 있어요.",
     [("네", "Yes"), ("좀", "a little"), ("매워요", "spicy"), ("안", "not"), ("매운", "spicy"), ("것도", "thing too"), ("있어요", "have")],
     "Yes, it's a little spicy. We have non-spicy too."),

    ("Payment", "계산해주세요!",
     "네, 카드로 하시겠어요, 현금이요?",
     [("네", "Yes"), ("카드로", "by card"), ("하시겠어요", "will you do"), ("현금이요", "or cash")],
     "Check please! Card or cash?"),

    ("Payment", "카드로 할게요.",
     "여기 카드 리더기 있습니다. 결제 부탁드립니다.",
     [("여기", "here"), ("카드 리더기", "card reader"), ("있습니다", "is"), ("결제", "payment"), ("부탁드립니다", "please")],
     "Card, please. Here's the reader. Please pay."),

    ("Restaurant goodbye", "맛있게 먹었습니다. 안녕히 가세요!",
     "감사합니다. 또 오세요!",
     [("감사합니다", "Thank you"), ("또", "again"), ("오세요", "come")],
     "It was delicious. Goodbye! Thank you. Come again!"),

    # ===== SHOPPING =====
    ("Greeting", "어서 오세요! 무엇을 도와드릴까요?",
     "이 신발 사고 싶은데요.",
     [("이", "these"), ("신발", "shoes"), ("사고", "buy"), ("싶은데요", "want to")],
     "Welcome! How can I help you? I want to buy these shoes."),

    ("Shopping", "이거 얼마예요?",
     "이거는 50,000원이에요. 사이즈는 어떻게 되세요?",
     [("이거는", "this"), ("50,000원이에요", "is 50,000 won"), ("사이즈는", "size"), ("어떻게 되세요", "what is it")],
     "How much is this? It's 50,000 won. What's your size?"),

    ("Trying on", "신어볼 수 있어요?",
     "물론이죠! 피팅룸은 저기 있어요.",
     [("물론이죠", "Of course"), ("피팅룸은", "fitting room"), ("저기", "over there"), ("있어요", "is")],
     "Can I try them on? Of course! Fitting room is over there."),

    ("Feedback", "어때요? 잘 맞아요?",
     "네, 편안해요. 이거 살게요.",
     [("네", "Yes"), ("편안해요", "comfortable"), ("이거", "this"), ("살게요", "will buy/take")],
     "How is it? Does it fit well? Yes, it's comfortable. I'll take these."),

    ("Payment", "할인되는 거 없어요?",
     "지금 10% 세일 중이에요. 카드로 결제하시면 5% 더 추가 할인돼요.",
     [("지금", "now"), ("10% 세일", "10% sale"), ("중이에요", "in progress"), ("카드로", "by card"), ("결제하시면", "if you pay"), ("5% 더", "5% more"), ("추가", "additional"), ("할인돼요", "discounted")],
     "Any discounts? It's 10% off now. Plus 5% more if you pay with card."),

    ("Bag", "포장해 주실 수 있어요?",
     "네, 선물용 포장해 드릴게요.",
     [("네", "Yes"), ("선물용", "gift"), ("포장해", "wrap"), ("드릴게요", "will do for you")],
     "Can you wrap it? Yes, I'll gift wrap it for you."),

    ("Shopping goodbye", "또 올게요. 안녕히 계세요!",
     "네, 감사합니다. 좋은 하루 보내세요!",
     [("네", "Yes"), ("감사합니다", "thank you"), ("좋은", "good"), ("하루", "day"), ("보내세요", "spend/have")],
     "I'll come again. Stay well! Yes, thank you. Have a nice day!"),

    # ===== ASKING DIRECTIONS =====
    ("Asking for help", "실례합니다만, 길을 좀 물어봐도 될까요?",
     "네, 어디를 가세요?",
     [("네", "Yes"), ("어디를", "where"), ("가세요", "are you going")],
     "Excuse me, may I ask for directions? Yes, where are you going?"),

    ("Directions", "지하철역이 어디예요?",
     "이 길로 곧장 가시다가 사거리에서 오른쪽으로 가세요. 그러면 역이 보여요.",
     [("이", "this"), ("길로", "road"), ("곧장", "straight"), ("가시다가", "go and then"), ("사거리에서", "at intersection"), ("오른쪽으로", "to the right"), ("가세요", "turn"), ("그러면", "then"), ("역이", "station"), ("보여요", "is visible")],
     "Where's the subway station? Go straight this way, turn right at the intersection. You'll see the station."),

    ("Clarifying", "거기까지 멀어요?",
     "걸어서 10분 정도 걸려요. 택시 타면 더 빨라요.",
     [("걸어서", "on foot"), ("10분 정도", "about 10 minutes"), ("걸려요", "takes"), ("택시", "taxi"), ("타면", "if you take"), ("더", "more"), ("빨라요", "faster")],
     "Is it far? About 10 minutes on foot. Faster by taxi."),

    ("Landmark", "근처에 표지판 있어요?",
     "네, 큰 건물이 보여요. 그 근처에 있어요.",
     [("네", "Yes"), ("큰", "big"), ("건물이", "building"), ("보여요", "see"), ("그", "that"), ("근처에", "nearby"), ("있어요", "is")],
     "Any signs nearby? Yes, you'll see a big building. It's near there."),

    ("Thanking", "가르쳐 주셔서 감사합니다!",
     "별말씀을요. 잘 가세요!",
     [("별말씀을요", "Don't mention it"), ("잘", "well"), ("가세요", "go")],
     "Thank you for showing me! Don't mention it. Have a safe trip!"),

    # ===== MAKING PLANS =====
    ("Inviting", "이번 주말에 시간 있어요?",
     "이번 주말요? 네, 별일 없어요. 왜요?",
     [("이번", "this"), ("주말요", "weekend"), ("네", "Yes"), ("별일", "nothing special"), ("없어요", "no"), ("왜요", "why")],
     "Do you have time this weekend? This weekend? Yes, I'm free. Why?"),

    ("Suggesting", "영화 볼래요? 새로운 영화가 개봉했어요.",
     "좋아요! 어떤 영화예요?",
     [("좋아요", "Good/Sounds good"), ("어떤", "what kind of"), ("영화예요", "movie is it")],
     "Want to watch a movie? A new one came out. Sounds good! What movie?"),

    ("Planning", "액션 영화인데, 같이 볼까요?",
     "네, 같이 봐요! 몇 시에 만날까요?",
     [("네", "Yes"), ("같이", "together"), ("봐요", "watch"), ("몇 시에", "what time"), ("만날까요", "shall we meet")],
     "It's an action movie, shall we watch together? Yes! What time should we meet?"),

    ("Time", "3시에 어때요?",
     "3시는 좀 이른데 4시는 어때요?",
     [("3시는", "3 o'clock"), ("좀", "a little"), ("이른데", "early but"), ("4시는", "4 o'clock"), ("어때요", "how about")],
     "How about 3? 3 is a bit early, how about 4?"),

    ("Location", "어디서 만날까요?",
     "역 앞에서 만나요. 거기가 편해요.",
     [("역", "station"), ("앞에서", "in front of"), ("만나요", "meet"), ("거기가", "that place"), ("편해요", "convenient")],
     "Where shall we meet? Let's meet in front of the station. That's convenient."),

    ("Confirming", "그럽시다. 토요일 4시에 역 앞에서!",
     "네, 그때 보요!",
     [("네", "Yes"), ("그때", "then"), ("보요", "see you")],
     "Okay then. Saturday at 4, in front of the station! Yes, see you then!"),

    # ===== AT THE CAFE =====
    ("Cafe greeting", "어서 오세요! 주문하시겠어요?",
     "아메리카노 한 잔 주세요.",
     [("아메리카노", "Americano"), ("한 잔", "one cup"), ("주세요", "please")],
     "Welcome! Ready to order? One Americano, please."),

    ("Customizing", "얼음 넣을까요?",
     "네, 얼음 주세요. 그리고 시럽도 주세요.",
     [("네", "Yes"), ("얼음", "ice"), ("주세요", "please"), ("그리고", "and"), ("시럽도", "syrup too")],
     "Want ice? Yes, ice please. And syrup too, please."),

    ("Food", "제빵 있어요?",
     "네, 이쪽에 있어요. 치즈 케이크랑 크로와상이 있어요.",
     [("네", "Yes"), ("이쪽에", "over here"), ("있어요", "there is"), ("치즈", "cheese"), ("케이크랑", "cake and"), ("크로와상이", "croissants"), ("있어요", "there are")],
     "Any desserts? Yes, over here. We have cheesecake and croissants."),

    ("Ordering more", "치즈 케이크 한 조각 주세요.",
     "네, 여기 계시는 테이블 번호는?",
     [("네", "Yes"), ("여기", "here"), ("계시는", "sitting at"), ("테이블", "table"), ("번호는", "number")],
     "One slice of cheesecake, please. Yes, what's your table number?"),

    ("Payment", "여기서 계산해요?",
     "아니요, 주문하신 음료는 카운터에서 받으시고 거기서 계산하시면 돼요.",
     [("아니요", "No"), ("주문하신", "ordered"), ("음료는", "drink"), ("카운터에서", "at counter"), ("받으시고", "receive and"), ("거기서", "there"), ("계산하시면", "pay"), ("돼요", "it's okay")],
     "Pay here? No, get your drink at the counter and pay there."),

    # ===== AT THE HOSPITAL =====
    ("Reception", "안녕하세요, 어디가 아프신가요?",
     "배가 너무 아파요. 의사 선생님 볼 수 있을까요?",
     [("배가", "stomach"), ("너무", "very"), ("아파요", "hurts"), ("의사", "doctor"), ("선생님", "teacher/doctor"), ("볼", "see"), ("수", "ability to"), ("있을까요", "can I")],
     "Hello, where does it hurt? My stomach really hurts. Can I see a doctor?"),

    ("Process", "환자등록증 여기 있어요. 작성해 주세요.",
     "네, 다 작성했어요.",
     [("네", "Yes"), ("다", "all"), ("작성했어요", "filled out")],
     "Fill out this registration form. Yes, I filled it out."),

    ("Waiting", "기다리시면 호명할게요.",
     "얼마나 기다려야 하나요?",
     [("얼마나", "how much"), ("기다려야", "must wait"), ("하나요", "do I")],
     "Wait here and I'll call your name. How long will I wait?"),

    ("Consultation", "환자분 이름은?", "김민수예요.", [("김민수", "Kim Minsu"), ("예요", "is")], "Name? Kim Minsu."),

    ("Diagnosis", "언제부터 아프셨어요?",
     "어제 저녁부터 아팠어요. 밥도 못 먹었어요.",
     [("어제", "yesterday"), ("저녁부터", "since evening"), ("아팠어요", "hurt"), ("밥도", "meal/rice even"), ("못", "cannot"), ("먹었어요", "ate")],
     "Since when have you been in pain? Since last night. Couldn't eat."),

    ("Treatment", "소화가 잘 안되신 것 같아요. 약 처방해 드릴게요.",
     "약국은 어디에 있어요?",
     [("약국은", "pharmacy"), ("어디에", "where"), ("있어요", "is")],
     "Seems like indigestion. I'll prescribe medicine. Where's the pharmacy?"),

    ("Instructions", "1층에 있어요. 하루 3번 식후에 드세요.",
     "네, 감사합니다.",
     [("네", "Yes"), ("감사합니다", "thank you")],
     "On the first floor. Take it 3 times a day after meals. Yes, thank you."),

    # ===== RENTING ACCOMMODATION =====
    ("Inquiry", "안녕하세요, 방을 보고 싶은데요.",
     "어떤 방을 원하세요? 원룸이면 투룸이면?",
     [("어떤", "what kind of"), ("방을", "room"), ("원하세요", "do you want"), ("원룸", "one-room"), ("이면", "or"), ("투룸", "two-room")],
     "Hello, I want to see a room. What kind? One-room or two-room?"),

    ("Availability", "원룸 있어요? 얼마예요?",
     "네, 있습니다. 월세 50만원이고 보증금 500만원이에요.",
     [("네", "Yes"), ("있습니다", "there is"), ("월세", "monthly rent"), ("50만원이고", "50,000 won and"), ("보증금", "deposit"), ("500만원이에요", "is 5 million won")],
     "Do you have a one-room? How much? Yes. Monthly 500,000 won, deposit 5 million."),

    ("Viewing", "지금 볼 수 있어요?",
     "네, 지금 가능해요. 따라오세요.",
     [("네", "Yes"), ("지금", "now"), ("가능해요", "possible"), ("따라오세요", "follow me")],
     "Can I see it now? Yes, right now. Follow me."),

    ("Facilities", "주방이랑 주방이랑 화장실이 있어요.",
     "침대는 있어요?",
     [("침대는", "bed"), ("있어요", "is there")],
     "There's a kitchen and bathroom. Is there a bed?"),

    ("Beds", "네, 침대랑 옷장 다 있어요.",
     "냉장고는요?",
     [("네", "Yes"), ("침대랑", "bed and"), ("옷장", "closet"), ("다", "all"), ("있어요", "there is"), ("냉장고는요", "refrigerator")],
     "Yes, bed and closet all included. Refrigerator?"),

    ("More", "냉장고도 있어요. 에어컨도 있어요.",
     "인터넷은?",
     [("냉장고도", "refrigerator too"), ("있어요", "there is"), ("에어컨도", "air conditioner too"), ("인터넷은", "internet")],
     "There's a fridge too. And AC. Internet?"),

    ("Final details", "와이파이 되요. 계약은 최소 1년이에요.",
     "네, 알겠어요. 계속할게요.",
     [("네", "Yes"), ("알겠어요", "understand"), ("계속할게요", "will continue/take it")],
     "Has wifi. Contract minimum 1 year. Okay, I'll take it."),

    # ===== JOB INTERVIEW =====
    ("Greeting", "안녕하세요, 이력서를 냈던 김민수입니다.",
     "네, 기다리고 있었습니다. 앉으세요.",
     [("네", "Yes"), ("기다리고", "waiting"), ("있었습니다", "was"), ("앉으세요", "sit down")],
     "Hello, I'm Kim Minsu who submitted the resume. Yes, we've been expecting you. Sit down."),

    ("Self intro", "자기소개 한 번 해주세요.",
     "네, 대학교에서 경영학을 전공했고, 졸업 후 2년 동안 일한 경험이 있어요.",
     [("네", "Yes"), ("대학교에서", "at university"), ("경영학을", "business administration"), ("전공했고", "majored and"), ("졸업 후", "after graduation"), ("2년 동안", "for 2 years"), ("일한", "worked"), ("경험이", "experience"), ("있어요", "have")],
     "Please introduce yourself. I majored in business administration and have 2 years of work experience after graduation."),

    ("Motivation", "우리 회사에 지원한 이유는요?",
     "귀사의 성장 가능성과 회사 방향이 제 목표와 일치한다고 생각해서 지원했어요.",
     [("귀사의", "your company's"), ("성장", "growth"), ("가능성과", "potential and"), ("회사", "company"), ("방향이", "direction"), ("제", "my"), ("목표와", "goals with"), ("일치한다고", "align"), ("생각해서", "think so"), ("지원했어요", "applied")],
     "Why did you apply to our company? I applied because your company's growth potential and direction align with my goals."),

    ("Strengths", "장점은 무엇입니까?",
     "제 장점은 새로운 것을 빨리 배우는 것입니다. 그리고 팀원들과 잘 협력할 수 있어요.",
     [("제", "My"), ("장점은", "strength is"), ("새로운", "new"), ("것을", "things"), ("빨리", "quickly"), ("배우는", "learning"), ("것입니다", "is"), ("그리고", "and"), ("팀원들과", "with team members"), ("잘", "well"), ("협력할", "cooperate"), ("수", "ability to"), ("있어요", "have")],
     "What are your strengths? My strength is learning new things quickly. Also, I can work well with team members."),

    ("Weakness", "단점도 말씀해 주세요.",
     "가끔 너무 완벽을 기해서 일을 천천히 할 때가 있습니다. 지금은 이것을 고치려고 노력 중이에요.",
     [("가끔", "sometimes"), ("너무", "too"), ("완벽을", "perfection"), ("기해서", "seeking"), ("일을", "work"), ("천천히", "slowly"), ("할 때가", "times when I do"), ("있습니다", "there are"), ("지금은", "now"), ("이것을", "this"), ("고치려고", "fixing"), ("노력", "effort"), ("중이에요", "am in")],
     "What are your weaknesses? Sometimes I'm too much of a perfectionist and work slowly. I'm trying to fix this now."),

    ("Questions", "질문 있으신 거 있나요?",
     "네, 입사 후 교육은 어떻게 되나요?",
     [("네", "Yes"), ("입사 후", "after joining"), ("교육은", "training"), ("어떻게", "how"), ("되나요", "is it")],
     "Do you have any questions? Yes, what's the training after joining?"),

    ("Closing", "면접 감사합니다. 결과는 이메일로 알려드리겠습니다.",
     "네, 감사합니다. 안녕히 계세요!",
     [("네", "Yes"), ("감사합니다", "thank you"), ("안녕히 계세요", "goodbye")],
     "Thank you for the interview. We'll email results. Yes, thank you. Goodbye!"),

    # ===== MAKING AN APPOINTMENT =====
    ("Calling", "여보세요, 의사인데요. 예약하고 싶은데요.",
     "네, 예약 도와드릴게요. 언제 원하세요?",
     [("네", "Yes"), ("예약", "reservation"), ("도와드릴게요", "will help"), ("언제", "when"), ("원하세요", "do you want")],
     "Hello, this is Dr. Kim's office. I'd like to make an appointment. Sure, when do you want?"),

    ("Time", "내일 오후 2시 가능해요?",
     "내일 오후는 다 찼어요. 3시는 어떠세요?",
     [("내일", "tomorrow"), ("오후는", "afternoon"), ("다", "all"), ("찼어요", "full"), ("3시는", "3 o'clock"), ("어떠세요", "how about")],
     "Is tomorrow 2 PM possible? Tomorrow afternoon is fully booked. How about 3 PM?"),

    ("Confirming", "네, 3시로 예약해 주세요. 김민수인데요.",
     "네, 김민수 님, 내일 3시로 예약됐습니다. 오시면 꼭 신분증 가져오세요.",
     [("네", "Yes"), ("김민수 님", "Mr./Ms. Kim Minsu"), ("내일", "tomorrow"), ("3시로", "at 3 o'clock"), ("예약됐습니다", "reserved"), ("오시면", "when you come"), ("꼭", "must"), ("신분증", "ID"), ("가져오세요", "bring")],
     "Yes, book 3 PM for Kim Minsu. Yes, Kim Minsu, booked for tomorrow 3 PM. Bring your ID when you come."),

    ("Canceling", "죄송한데, 예약 취소할 수 있어요?",
     "네, 가능합니다. 다시 예약하고 싶으시면 연락 주세요.",
     [("네", "Yes"), ("가능합니다", "possible"), ("다시", "again"), ("예약하고", "reserve"), ("싶으시면", "if you want"), ("연락", "contact"), ("주세요", "please")],
     "Sorry, can I cancel the appointment? Yes, you can. Contact us when you want to re-book."),
]


def create_model():
    """Create card model for conversations with colored word alignment."""
    return genanki.Model(
        MODEL_ID,
        "Korean Conversation Model",
        fields=[
            {"name": "Context"},
            {"name": "Prompt"},
            {"name": "Response"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Conversation Card",
                "qfmt": """
<div style="padding: 12px; background: #f5f5f5; border-radius: 10px; margin: 12px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">{{Context}}</strong>
</div>
<div style="text-align: center; font-size: 32px; padding: 30px;">
    {{Prompt}}
</div>
                """,
                "afmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 13px; color: #666;">{{Context}}</strong>
</div>
<div style="text-align: center; font-size: 28px; padding: 20px; color: #666;">
    {{Prompt}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
<hr style="margin: 12px 0;">
<div style="text-align: center; font-size: 32px; color: #2196F3; font-weight: bold; padding: 20px;">
    {{Response}}
</div>
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 700px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 22px; padding: 10px; line-height: 1.8; color: #2c3e50; font-weight: 500;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 16px; color: #666; padding: 10px; line-height: 1.8;">
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


def generate_deck(output_file="decks/14_korean_conversation_1.apkg"):
    """Generate the conversation deck with colored word alignment."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "14. Korean Conversations - 회화 연습")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for context, prompt, response, word_pairs, _ in CONVERSATIONS:
            # Generate audio for response
            audio_filename = generate_audio(response, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            note = genanki.Note(
                model=model,
                fields=[context, prompt, response, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(CONVERSATIONS)} conversation cards")
        print(f"  - {len(created_audio_files)} audio files")
        print("\nImport this file into Anki: File -> Import...")

    finally:
        # Clean up temp directory
        try:
            shutil.rmtree(audio_dir)
        except:
            pass


if __name__ == "__main__":
    generate_deck()
