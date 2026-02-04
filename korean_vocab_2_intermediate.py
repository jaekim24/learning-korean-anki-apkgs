#!/usr/bin/env python3
"""
Korean Intermediate Vocabulary Deck (200 words)

Everyday vocabulary for intermediate learners.
Categories: Food, Locations, Transportation, Shopping, Weather, Emotions, Activities
Usage: python3 korean_vocab_2_intermediate.py
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
DECK_ID = DECK_IDS["vocab_2"]
MODEL_ID = MODEL_IDS["word"]


# Intermediate vocabulary: (korean, english, romanization, example, example_translation, word_pairs)
# word_pairs: list of (korean, english) tuples for color-coded alignment
INTERMEDIATE_VOCAB = [
    # ===== FOOD & DINING (30) =====
    ("음식", "Food", "eumsik", "한국 음식을 좋아해요", "I like Korean food",
     [("한국", "Korean"), ("음식을", "food"), ("좋아해요", "like")]),
    ("식당", "Restaurant", "sikdang", "식당에 가요", "Going to a restaurant",
     [("식당에", "to the restaurant"), ("가요", "go")]),
    ("카페", "Cafe", "kape", "카페에서 커피를 마셔요", "Drinking coffee at a cafe",
     [("카페에서", "at a cafe"), ("커피를", "coffee"), ("마셔요", "drink")]),
    ("빵집", "Bakery", "ppangjip", "빵집에서 빵을 사요", "Buying bread at a bakery",
     [("빵집에서", "at a bakery"), ("빵을", "bread"), ("사요", "buy")]),
    ("김밥", "Gimbap (seaweed rice roll)", "gimbap", "김밥을 먹어요", "Eating gimbap",
     [("김밥을", "gimbap"), ("먹어요", "eat")]),
    ("비빔밥", "Bibimbap (mixed rice)", "bibimbap", "비빔밥이 맛있어요", "Bibimbap is delicious",
     [("비빔밥이", "bibimbap"), ("맛있어요", "is delicious")]),
    ("불고기", "Bulgogi (marinated beef)", "bulgogi", "불고기를 좋아해요", "I like bulgogi",
     [("불고기를", "bulgogi"), ("좋아해요", "like")]),
    ("갈비", "Galbi (ribs)", "galbi", "갈비를 구워요", "Grilling galbi",
     [("갈비를", "galbi/ribs"), ("구워요", "grill")]),
    ("라면", "Ramyeon (instant noodles)", "ramyeon", "라면을 끓여요", "Cooking ramyeon",
     [("라면을", "ramyeon"), ("끓여요", "cook")]),
    ("김치", "Kimchi", "gimchi", "김치를 만들어요", "Making kimchi",
     [("김치를", "kimchi"), ("만들어요", "make")]),
    ("된장", "Doenjang (soybean paste)", "doenjang", "된장찌개를 끓여요", "Making doenjang stew",
     [("된장찌개를", "doenjang stew"), ("끓여요", "cook")]),
    ("간장", "Ganjang (soy sauce)", "ganjang", "간장을 넣어요", "Adding soy sauce",
     [("간장을", "soy sauce"), ("넣어요", "add")]),
    ("고추장", "Gochujang (chili paste)", "gochujang", "고추장이 매워요", "Gochujang is spicy",
     [("고추장이", "gochujang/chili paste"), ("매워요", "is spicy")]),
    ("쌀", "Rice (uncooked)", "ssal", "쌀을 씻어요", "Washing rice",
     [("쌀을", "rice (uncooked)"), ("씻어요", "wash")]),
    ("밥", "Rice (cooked) / Meal", "bap", "밥을 먹었어요", "Ate rice/a meal",
     [("밥을", "rice/meal"), ("먹었어요", "ate")]),
    ("국", "Soup", "guk", "국을 끓여요", "Making soup",
     [("국을", "soup"), ("끓여요", "make/boil")]),
    ("찌개", "Stew", "jjigae", "김치찌개를 먹어요", "Eating kimchi stew",
     [("김치찌개를", "kimchi stew"), ("먹어요", "eat")]),
    ("반찬", "Side dish", "banchan", "반찬을 많이 해요", "Making many side dishes",
     [("반찬을", "side dishes"), ("많이", "many"), ("해요", "make")]),
    ("후식", "Dessert", "husik", "후식을 먹어요", "Eating dessert",
     [("후식을", "dessert"), ("먹어요", "eat")]),
    ("과일", "Fruit", "gwail", "과일을 썰어요", "Cutting fruit",
     [("과일을", "fruit"), ("썰어요", "cut")]),
    ("사과", "Apple", "sagwa", "사과를 깎아요", "Peeling an apple",
     [("사과를", "apple"), ("깎아요", "peel")]),
    ("바나나", "Banana", "bana", "바나나를 먹어요", "Eating a banana",
     [("바나나를", "banana"), ("먹어요", "eat")]),
    ("오렌지", "Orange", "orenji", "오렌지 주스를 마셔요", "Drinking orange juice",
     [("오렌지", "orange"), ("주스를", "juice"), ("마셔요", "drink")]),
    ("포도", "Grape", "podo", "포도를 먹어요", "Eating grapes",
     [("포도를", "grapes"), ("먹어요", "eat")]),
    ("수박", "Watermelon", "subak", "수박을 깨요", "Cutting a watermelon",
     [("수박을", "watermelon"), ("깨요", "cut (into pieces)")]),
    ("딸기", "Strawberry", "ttalgi", "딸기를 씻어요", "Washing strawberries",
     [("딸기를", "strawberries"), ("씻어요", "wash")]),
    ("치즈", "Cheese", "chiji", "피자에 치즈를 넣어요", "Putting cheese on pizza",
     [("피자에", "on pizza"), ("치즈를", "cheese"), ("넣어요", "put/add")]),
    ("버터", "Butter", "beoteo", "빵에 버터를 발라요", "Spreading butter on bread",
     [("빵에", "on bread"), ("버터를", "butter"), ("발라요", "spread")]),
    ("우유", "Milk", "uyu", "아침에 우유를 마셔요", "Drinking milk in the morning",
     [("아침에", "in the morning"), ("우유를", "milk"), ("마셔요", "drink")]),
    ("쥬스", "Juice", "jyuseu", "오렌지 쥬스를 마셔요", "Drinking orange juice",
     [("오렌지", "orange"), ("쥬스를", "juice"), ("마셔요", "drink")]),
    ("콜라", "Cola", "kolla", "콜라를 마셔요", "Drinking cola",
     [("콜라를", "cola"), ("마셔요", "drink")]),
    ("물", "Water", "mul", "물을 마셔요", "Drinking water",
     [("물을", "water"), ("마셔요", "drink")]),

    # ===== LOCATIONS (25) =====
    ("편의점", "Convenience store", "pyeonijeom", "편의점에 가요", "Going to a convenience store",
     [("편의점에", "to the convenience store"), ("가요", "go")]),
    ("마트", "Mart/Supermarket", "mateu", "마트에서 장을 봐요", "Shopping at the mart",
     [("마트에서", "at the mart"), ("장을", "groceries/shopping"), ("봐요", "do/buy")]),
    ("시장", "Market", "sijang", "시장에 가요", "Going to the market",
     [("시장에", "to the market"), ("가요", "go")]),
    ("병원", "Hospital", "byeongwon", "병원에 가요", "Going to the hospital",
     [("병원에", "to the hospital"), ("가요", "go")]),
    ("약국", "Pharmacy", "yakkuk", "약국에서 약을 사요", "Buying medicine at the pharmacy",
     [("약국에서", "at the pharmacy"), ("약을", "medicine"), ("사요", "buy")]),
    ("은행", "Bank", "eunhaeng", "은행에 가요", "Going to the bank",
     [("은행에", "to the bank"), ("가요", "go")]),
    ("우체국", "Post office", "ucheoguk", "우체국에서 편지를 보내요", "Sending mail at the post office",
     [("우체국에서", "at the post office"), ("편지를", "letter/mail"), ("보내요", "send")]),
    ("경찰서", "Police station", "gyeongchalseo", "경찰서에 신고해요", "Reporting to the police",
     [("경찰서에", "to the police station"), ("신고해요", "report")]),
    ("소방서", "Fire station", "sobangseo", "소방서 옆이에요", "Next to the fire station",
     [("소방서", "fire station"), ("옆이에요", "is next to")]),
    ("영화관", "Movie theater", "yeonghwagwan", "영화관에서 영화를 봐요", "Watching a movie at the theater",
     [("영화관에서", "at the movie theater"), ("영화를", "movie"), ("봐요", "watch")]),
    ("노래방", "Karaoke room", "noraebang", "노래방에 가요", "Going to karaoke",
     [("노래방에", "to karaoke room"), ("가요", "go")]),
    ("PC방", "PC bang (internet cafe)", "pisibang", "PC방에서 게임을 해요", "Playing games at PC bang",
     [("PC방에서", "at PC bang"), ("게임을", "game"), ("해요", "play")]),
    ("찜질방", "Korean sauna/spa", "jjimjilbang", "찜질방에 가요", "Going to the Korean spa",
     [("찜질방에", "to jjimjilbang"), ("가요", "go")]),
    ("미용실", "Beauty salon", "miyongsil", "미용실에 가요", "Going to the beauty salon",
     [("미용실에", "to the beauty salon"), ("가요", "go")]),
    ("이발소", "Barber shop", "ibalso", "이발소에 머리를 자르러 가요", "Going to the barber to cut hair",
     [("이발소에", "to the barber shop"), ("머리를", "hair"), ("자르러", "cut"), ("가요", "go")]),
    ("세탁소", "Laundry", "setakso", "세탁소에 빨래를 맡겨요", "Dropping off laundry",
     [("세탁소에", "at the laundry"), ("빨래를", "laundry"), ("맡겨요", "drop off/entrust")]),
    ("세탁기", "Washing machine", "setakgi", "세탁기로 빨래해요", "Doing laundry in the washing machine",
     [("세탁기로", "with washing machine"), ("빨래해요", "do laundry")]),
    ("건조기", "Dryer", "geonjogi", "건조기로 말려요", "Drying with the dryer",
     [("건조기로", "with dryer"), ("말려요", "dry")]),
    ("주방", "Kitchen", "jubang", "주방에서 요리해요", "Cooking in the kitchen",
     [("주방에서", "in the kitchen"), ("요리해요", "cook")]),
    ("거실", "Living room", "geosil", "거실에서 TV를 봐요", "Watching TV in the living room",
     [("거실에서", "in the living room"), ("TV를", "TV"), ("봐요", "watch")]),
    ("침실", "Bedroom", "chimsil", "침실에서 자요", "Sleeping in the bedroom",
     [("침실에서", "in the bedroom"), ("자요", "sleep")]),
    ("화장실", "Bathroom/Restroom", "hwajangsil", "화장실이 어디예요?", "Where is the restroom?",
     [("화장실이", "restroom/bathroom"), ("어디예요?", "where is?")]),
    ("목욕탕", "Bathroom", "mogyoktang", "목욕탕에서 목욕해요", "Bathing in the bathroom",
     [("목욕탕에서", "in the bathroom"), ("목욕해요", "bathe")]),
    ("발코니", "Balcony", "balkoni", "발코니에서 나가요", "Going out to the balcony",
     [("발코니에서", "to the balcony"), ("나가요", "go out")]),
    ("지하", "Basement", "jiha", "지하 주차장에 있어요", "In the basement parking",
     [("지하", "basement"), ("주차장에", "in the parking lot"), ("있어요", "am at/is")]),

    # ===== TRANSPORTATION (20) =====
    ("자동차", "Car", "jadongcha", "자동차를 운전해요", "Driving a car",
     [("자동차를", "car"), ("운전해요", "drive")]),
    ("버스", "Bus", "beoseu", "버스를 타요", "Taking the bus",
     [("버스를", "bus"), ("타요", "take/ride")]),
    ("지하철", "Subway", "jihacheol", "지하철을 타요", "Taking the subway",
     [("지하철을", "subway"), ("타요", "take/ride")]),
    ("기차", "Train", "gicha", "기차역에 가요", "Going to the train station",
     [("기차역에", "to the train station"), ("가요", "go")]),
    ("KTX", "KTX (high-speed train)", "ketiex", "KTX를 타고 부산에 가요", "Taking KTX to Busan",
     [("KTX를", "KTX"), ("타고", "taking/riding"), ("부산에", "to Busan"), ("가요", "go")]),
    ("택시", "Taxi", "taeksi", "택시를 잡아요", "Catching a taxi",
     [("택시를", "taxi"), ("잡아요", "catch/hail")]),
    ("자전거", "Bicycle", "jajeongeo", "자전거를 타요", "Riding a bicycle",
     [("자전거를", "bicycle"), ("타요", "ride")]),
    ("오토바이", "Motorcycle", "otobai", "오토바이를 타요", "Riding a motorcycle",
     [("오토바이를", "motorcycle"), ("타요", "ride")]),
    ("비행기", "Airplane", "bihaenggi", "비행기를 타요", "Taking an airplane",
     [("비행기를", "airplane"), ("타요", "take/ride")]),
    ("배", "Boat/Ship", "bae", "배를 타요", "Taking a boat",
     [("배를", "boat/ship"), ("타요", "take/ride")]),
    ("페리", "Ferry", "peri", "페리를 타요", "Taking a ferry",
     [("페리를", "ferry"), ("타요", "take/ride")]),
    ("역", "Station", "yeok", "역에서 내려요", "Getting off at the station",
     [("역에서", "at the station"), ("내려요", "get off")]),
    ("정류장", "Bus stop", "jeongnyujang", "버스 정류장에서 기다려요", "Waiting at the bus stop",
     [("버스", "bus"), ("정류장에서", "at the stop/station"), ("기다려요", "wait")]),
    ("터미널", "Terminal", "teomineol", "터미널에 가요", "Going to the terminal",
     [("터미널에", "to the terminal"), ("가요", "go")]),
    ("주차장", "Parking lot", "jachajang", "주차장에 세워요", "Parking in the parking lot",
     [("주차장에", "in the parking lot"), ("세워요", "park")]),
    ("교통카드", "Transportation card", "gyotongkadeu", "교통카드를 찍어요", "Tapping the transportation card",
     [("교통카드를", "transportation card"), ("찍어요", "tap/beep")]),
    ("표", "Ticket", "pyo", "표를 사요", "Buying a ticket",
     [("표를", "ticket"), ("사요", "buy")]),
    ("승차권", "Boarding pass", "seungchagwon", "승차권을 보여줘요", "Showing the boarding pass",
     [("승차권을", "boarding pass/ticket"), ("보여줘요", "show")]),
    ("운전", "Driving", "unjeon", "운전을 해요", "Driving",
     [("운전을", "driving"), ("해요", "do")]),
    ("길", "Road/Street/Way", "gil", "길을 잃어버렸어요", "Lost the way",
     [("길을", "way/road"), ("잃어버렸어요", "lost")]),

    # ===== SHOPPING (25) =====
    ("가격", "Price", "gagyeok", "가격이 얼마예요?", "How much is the price?", []),
    ("비싸다", "Expensive", "bissada", "너무 비싸요", "It's too expensive", []),
    ("싸다", "Cheap", "ssada", "싸요", "It's cheap", []),
    ("할인", "Discount", "halin", "할인을 해주세요", "Please give a discount", []),
    ("세일", "Sale", "seil", "세일 중이에요", "It's on sale", []),
    ("영수증", "Receipt", "yeongsujeung", "영수증 주세요", "Please give me a receipt", []),
    ("계산하다", "To calculate/pay bill", "gyesanhada", "계산해주세요", "Please calculate (the bill)", []),
    ("카드", "Card", "kadeu", "카드로 계산해요", "Paying by card", []),
    ("현금", "Cash", "hyeongeum", "현금으로 낼게요", "I'll pay in cash", []),
    ("돈", "Money", "don", "돈이 없어요", "I don't have money", []),
    ("원", "Won (Korean currency)", "won", "1000원이에요", "It's 1000 won", []),
    ("달러", "Dollar", "dalleo", "달러로 환전해요", "Exchanging to dollars", []),
    ("옷", "Clothes", "ot", "옷을 사요", "Buying clothes", []),
    ("신발", "Shoes", "sinbal", "신발을 신어요", "Wearing shoes", []),
    ("모자", "Hat/Cap", "moja", "모자를 써요", "Wearing a hat", []),
    ("안경", "Glasses", "angyeong", "안경을 써요", "Wearing glasses", []),
    ("가방", "Bag", "gabang", "가방을 샀어요", "Bought a bag", []),
    ("지갑", "Wallet", "jigap", "지갑을 잃어버렸어요", "Lost my wallet", []),
    ("시계", "Watch/Clock", "sigye", "시계를 봐요", "Looking at the watch", []),
    ("반지", "Ring", "banji", "반지를 끼워요", "Wearing a ring", []),
    ("목걸이", "Necklace", "mokgeori", "목걸이를 했어요", "Wearing a necklace", []),
    ("귀걸이", "Earrings", "gwigeori", "귀걸이를 했어요", "Wearing earrings", []),
    ("화장품", "Cosmetics", "hwajangpum", "화장품을 샀어요", "Bought cosmetics", []),
    ("선물", "Present/Gift", "seonmul", "선물을 줬어요", "Gave a present", []),
    ("인터넷", "Internet", "inteonet", "인터넷으로 쇼핑해요", "Shopping on the internet", []),
    ("쇼핑하다", "To shop", "syopinghada", "쇼핑을 해요", "Shopping", []),

    # ===== WEATHER (20) =====
    ("날씨", "Weather", "nalssi", "날씨가 좋아요", "The weather is good", []),
    ("비", "Rain", "bi", "비가 와요", "It's raining", []),
    ("눈", "Snow", "nun", "눈이 와요", "It's snowing", []),
    ("바람", "Wind", "baram", "바람이 불어요", "The wind is blowing", []),
    ("구름", "Cloud", "gureum", "구름이 꼈어요", "It's cloudy", []),
    ("해", "Sun", "hae", "해가 떠요", "The sun is rising", []),
    ("달", "Moon", "dal", "달이 떠요", "The moon is rising", []),
    ("별", "Star", "byeol", "별이 보여요", "Stars are visible", []),
    ("천둥", "Thunder", "cheondung", "천둥이 치는데", "It's thundering", []),
    ("번개", "Lightning", "beongae", "번개가 치는데", "Lightning is striking", []),
    ("무지개", "Rainbow", "mujigae", "무지개가 생겼어요", "A rainbow appeared", []),
    ("안개", "Fog", "angae", "안개가 꼈어요", "It's foggy", []),
    ("더위", "Heat", "deowi", "더위를 먹었어요", "Got heat exhaustion", []),
    ("추위", "Cold", "chuwii", "추위를 타요", "Sensitive to cold", []),
    ("온도", "Temperature", "ondo", "온도를 체크해요", "Checking the temperature", []),
    ("습도", "Humidity", "seupdo", "습도가 높아요", "Humidity is high", []),
    ("맑다", "Clear (sky)", "matda", "하늘이 맑아요", "The sky is clear", []),
    ("흐리다", "Cloudy", "heurida", "날씨가 흐려요", "The weather is cloudy", []),
    ("건조하다", "Dry", "geonjohada", "날씨가 건조해요", "The weather is dry", []),
    ("습하다", "Humid", "seupada", "날씨가 습해요", "The weather is humid", []),

    # ===== EMOTIONS & FEELINGS (30) =====
    ("기분", "Feeling/Mood", "gibun", "기분이 좋아요", "I feel good",
     [("기분이", "feeling/mood"), ("좋아요", "good")]),
    ("감정", "Emotion", "gamjeong", "감정이 풍부해요", "Emotionally rich",
     [("감정이", "emotion"), ("풍부해요", "rich/abundant")]),
    ("기쁘다", "Glad/Happy", "gippeuda", "기뻐요", "I'm glad",
     [("기뻐요", "am glad/happy")]),
    ("슬프다", "Sad", "seulpeuda", "슬퍼요", "I'm sad",
     [("슬퍼요", "am sad")]),
    ("화나다", "Angry", "hwanada", "화가 났어요", "I got angry",
     [("화가", "anger"), ("났어요", "got/occurred")]),
    ("두렵다", "Afraid/Scared", "duryeopda", "두려워요", "I'm scared",
     [("두려워요", "am afraid/scared")]),
    ("걱정하다", "To worry", "geokjeonghada", "걱정돼요", "I'm worried",
     [("걱정돼요", "am worried")]),
    ("신나다", "Excited", "sinnada", "신나요", "I'm excited",
     [("신나요", "am excited")]),
    ("즐겁다", "Enjoyable/Fun", "jeulgeopda", "즈거워요", "It's enjoyable",
     [("즐거워요", "is enjoyable/fun")]),
    ("재미있다", "Fun/Interesting", "jaemiitda", "재미있어요", "It's fun",
     [("재미있어요", "is fun/interesting")]),
    ("지루하다", "Boring", "jiruhada", "지루해요", "It's boring",
     [("지루해요", "is boring")]),
    ("피곤하다", "Tired", "pigonhada", "피곤해요", "I'm tired",
     [("피곤해요", "am tired")]),
    ("힘들다", "Hard/Difficult/Tiring", "himdeulda", "힘들어요", "It's hard/tiring",
     [("힘들어요", "is hard/tiring")]),
    ("편안하다", "Comfortable", "pyeonanhada", "편안해요", "It's comfortable",
     [("편안해요", "is comfortable")]),
    ("불편하다", "Uncomfortable", "bulpyeonhada", "불편해요", "It's uncomfortable",
     [("불편해요", "is uncomfortable")]),
    ("아프다", "Sick/Painful", "apeuda", "아파요", "I'm sick/hurt",
     [("아파요", "hurt/sick")]),
    ("다치다", "To get hurt/injured", "dachida", "다쳤어요", "I got hurt",
     [("다쳤어요", "got hurt/injured")]),
    ("아프다", "To hurt", "apeuda", "머리가 아파요", "My head hurts",
     [("머리가", "head"), ("아파요", "hurts")]),
    ("배아프다", "Stomachache", "beapeuda", "배가 아파요", "I have a stomachache",
     [("배가", "stomach"), ("아파요", "hurts")]),
    ("두통", "Headache", "dutong", "머리가 아파요", "I have a headache",
     [("머리가", "head"), ("아파요", "hurts")]),
    ("열", "Fever", "yeol", "열이 나요", "I have a fever",
     [("열이", "fever"), ("나요", "have/coming out")]),
    ("감기", "Cold", "gamgi", "감기에 걸렸어요", "I caught a cold",
     [("감기에", "cold"), ("걸렸어요", "caught")]),
    ("알레르기", "Allergy", "allerugi", "알레르기가 있어요", "I have allergies",
     [("알레르기가", "allergies"), ("있어요", "have")]),
    ("스트레스", "Stress", "seuteureseu", "스트레스를 받아요", "Getting stressed",
     [("스트레스를", "stress"), ("받아요", "get/receive")]),
    ("긴장하다", "Nervous", "ginjanghada", "긴장돼요", "I'm nervous",
     [("긴장돼요", "am nervous")]),
    ("놀라다", "Surprised", "nollada", "놀랐어요", "I was surprised",
     [("놀랐어요", "was surprised")]),
    ("실망하다", "Disappointed", "silmanghada", "실망했어요", "I was disappointed",
     [("실망했어요", "was disappointed")]),
    ("놀라다", "Startled", "nollada", "놀랐어요", "I was startled",
     [("놀랐어요", "was startled")]),
    ("안심하다", "Relieved", "ansimhada", "마음이 놓였어요", "I'm relieved",
     [("마음이", "mind/heart"), ("놓였어요", "was relieved")]),

    # ===== ACTIVITIES & VERBS (30) =====
    ("운동", "Exercise", "undong", "운동을 해요", "Exercising",
     [("운동을", "exercise"), ("해요", "do")]),
    ("요가", "Yoga", "yoga", "요가를 해요", "Doing yoga",
     [("요가를", "yoga"), ("해요", "do")]),
    ("조깅", "Jogging", "joging", "조깅을 해요", "Jogging",
     [("조깅을", "jogging"), ("해요", "do")]),
    ("수영", "Swimming", "suyeong", "수영을 해요", "Swimming",
     [("수영을", "swimming"), ("해요", "do")]),
    ("등산", "Mountain climbing", "deungsan", "등산을 가요", "Going mountain climbing",
     [("등산을", "mountain climbing"), ("가요", "go")]),
    ("여행", "Travel", "yeohaeng", "여행을 가요", "Going traveling",
     [("여행을", "travel"), ("가요", "go")]),
    ("휴가", "Vacation", "hyuga", "휴가를 가요", "Going on vacation",
     [("휴가를", "vacation"), ("가요", "go")]),
    ("방학", "School break", "banghak", "방학 동안 쉴 거예요", "Resting during break",
     [("방학", "school break"), ("동안", "during"), ("쉴", "rest"), ("거예요", "will")]),
    ("취미", "Hobby", "chwimi", "취미가 뭐예요?", "What are your hobbies?",
     [("취미가", "hobby"), ("뭐예요?", "what is?")]),
    ("독서", "Reading", "dokseo", "독서를 좋아해요", "I like reading",
     [("독서를", "reading"), ("좋아해요", "like")]),
    ("그림", "Picture/Drawing", "geurim", "그림을 그려요", "Drawing a picture",
     [("그림을", "picture/drawing"), ("그려요", "draw")]),
    ("음악", "Music", "eumak", "음악을 들어요", "Listening to music",
     [("음악을", "music"), ("들어요", "listen")]),
    ("노래", "Song", "norae", "노래를 불러요", "Singing a song",
     [("노래를", "song"), ("불러요", "sing")]),
    ("춤", "Dance", "chum", "춤을 춰요", "Dancing",
     [("춤을", "dance"), ("춰요", "dance")]),
    ("영화", "Movie", "yeonghwa", "영화를 봐요", "Watching a movie",
     [("영화를", "movie"), ("봐요", "watch")]),
    ("드라마", "Drama", "deurama", "드라마를 봐요", "Watching a drama",
     [("드라마를", "drama"), ("봐요", "watch")]),
    ("애니메이션", "Animation", "aenimeisyeon", "애니메이션을 봐요", "Watching animation",
     [("애니메이션을", "animation"), ("봐요", "watch")]),
    ("게임", "Game", "geim", "게임을 해요", "Playing games",
     [("게임을", "game"), ("해요", "play")]),
    ("스포츠", "Sports", "seupochu", "스포츠를 해요", "Playing sports",
     [("스포츠를", "sports"), ("해요", "play")]),
    ("축구", "Soccer", "chukgu", "축구를 해요", "Playing soccer",
     [("축구를", "soccer"), ("해요", "play")]),
    ("야구", "Baseball", "yagu", "야구를 해요", "Playing baseball",
     [("야구를", "baseball"), ("해요", "play")]),
    ("농구", "Basketball", "nonggu", "농구를 해요", "Playing basketball",
     [("농구를", "basketball"), ("해요", "play")]),
    ("배구", "Volleyball", "baegu", "배구를 해요", "Playing volleyball",
     [("배구를", "volleyball"), ("해요", "play")]),
    ("테니스", "Tennis", "teniseu", "테니스를 쳐요", "Playing tennis",
     [("테니스를", "tennis"), ("쳐요", "play (racquet sports)")]),
    ("골프", "Golf", "golpeu", "골프를 쳐요", "Playing golf",
     [("골프를", "golf"), ("쳐요", "play")]),
    ("스키", "Skiing", "seuki", "스키를 타요", "Skiing",
     [("스키를", "ski"), ("타요", "ride")]),
    ("보드", "Snowboarding", "bodeu", "보드를 타요", "Snowboarding",
     [("보드를", "snowboard"), ("타요", "ride")]),
    ("쇼핑", "Shopping", "syoping", "쇼핑을 해요", "Shopping",
     [("쇼핑을", "shopping"), ("해요", "do")]),
    ("요리", "Cooking", "yori", "요리를 해요", "Cooking",
     [("요리를", "cooking"), ("해요", "do")]),
    ("청소", "Cleaning", "cheongso", "청소를 해요", "Cleaning",
     [("청소를", "cleaning"), ("해요", "do")]),
    ("빨래", "Laundry", "ppallae", "빨래를 해요", "Doing laundry",
     [("빨래를", "laundry"), ("해요", "do")]),
    ("설거지", "Dishwashing", "seolgeoji", "설거지를 해요", "Washing dishes",
     [("설거지를", "dishwashing"), ("해요", "do")]),

    # ===== SCHOOL & WORK (20) =====
    ("학교", "School", "hakgyo", "학교에 가요", "Going to school",
     [("학교에", "to school"), ("가요", "go")]),
    ("대학교", "University", "daehakgyo", "대학교에 다녀요", "Attending university",
     [("대학교에", "to university"), ("다녀요", "attend/go to")]),
    ("도서관", "Library", "doseogwan", "도서관에서 공부해요", "Studying at the library",
     [("도서관에서", "at the library"), ("공부해요", "study")]),
    ("강의실", "Lecture room", "gangnisil", "강의실에 가요", "Going to the lecture room",
     [("강의실에", "to the lecture room"), ("가요", "go")]),
    ("교실", "Classroom", "gyosil", "교실에 있어요", "In the classroom",
     [("교실에", "in the classroom"), ("있어요", "am at")]),
    ("시험", "Exam", "siheom", "시험을 봐요", "Taking an exam",
     [("시험을", "exam"), ("봐요", "take")]),
    ("숙제", "Homework", "sukje", "숙제를 해요", "Doing homework",
     [("숙제를", "homework"), ("해요", "do")]),
    ("과제", "Assignment", "gwaje", "과제를 제출해요", "Submitting an assignment",
     [("과제를", "assignment"), ("제출해요", "submit")]),
    ("성적", "Grades", "seongjeok", "성적이 좋아요", "Grades are good",
     [("성적이", "grades"), ("좋아요", "good")]),
    ("졸업", "Graduation", "joreop", "졸업을 했어요", "Graduated",
     [("졸업을", "graduation"), ("했어요", "did/completed")]),
    ("입학", "Entrance", "iphak", "입학을 했어요", "Entered school",
     [("입학을", "entrance/admission"), ("했어요", "did")]),
    ("선생님", "Teacher", "seonsaengnim", "선생님을 만나요", "Meeting the teacher",
     [("선생님을", "teacher"), ("만나요", "meet")]),
    ("교수님", "Professor", "gyosunim", "교수님 수업을 들어요", "Taking the professor's class",
     [("교수님", "professor"), ("수업을", "class"), ("들어요", "take/listen")]),
    ("학생", "Student", "haksaeng", "학생이에요", "I am a student",
     [("학생", "student"), ("이에요", "am")]),
    ("동료", "Colleague", "dongryo", "동료와 일해요", "Working with colleagues",
     [("동료와", "with colleagues"), ("일해요", "work")]),
    ("상사", "Boss", "sangsa", "상사를 만나요", "Meeting the boss",
     [("상사를", "boss"), ("만나요", "meet")]),
    ("회의", "Meeting", "hoeui", "회의를 해요", "Having a meeting",
     [("회의를", "meeting"), ("해요", "have/do")]),
    ("프로젝트", "Project", "peurojekteu", "프로젝트를 해요", "Working on a project",
     [("프로젝트를", "project"), ("해요", "work on/do")]),
    ("보고서", "Report", "bogoseo", "보고서를 써요", "Writing a report",
     [("보고서를", "report"), ("써요", "write")]),
    ("이력서", "Resume", "iryeokseo", "이력서를 썼어요", "Wrote a resume",
     [("이력서를", "resume"), ("썼어요", "wrote")]),
]


def create_model():
    """Create card model for vocabulary with color-coded word alignment."""
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
<div style="text-align: center; font-size: 60px; padding: 20px;">
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
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 600px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 24px; padding: 10px; line-height: 1.8;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 10px; line-height: 1.8;">
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


def generate_deck(output_file="decks/11_korean_vocab_2_intermediate.apkg"):
    """Generate the intermediate vocabulary deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "11. Korean Intermediate Vocab - 중급 어휘")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for entry in INTERMEDIATE_VOCAB:
            # Handle both old format (5 items) and new format (6 items with word_pairs)
            if len(entry) == 6:
                korean, english, roman, example, ex_trans, word_pairs = entry
            else:
                korean, english, roman, example, ex_trans = entry
                word_pairs = []

            # Skip malformed entries
            if not korean:
                continue

            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

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
        print(f"  - {len(INTERMEDIATE_VOCAB)} vocabulary cards")
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
