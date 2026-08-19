#!/usr/bin/env python3
"""03 - Core vocabulary, frequency ordered.

Tiers are study order, not categories. The top ~200 words carry an enormous
share of ordinary speech, so learning them in frequency order buys comprehension
faster than learning them grouped by topic -- topic grouping is tidy but it
front-loads words like "eggplant" ahead of words like "thing".

Tier 1 additionally gets a production card (EN->KR). The rest are recognition
and listening only, because production costs several times more per item and is
only worth paying for the words you actually need to say.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import vocab_model

# (korean, english, romanization, example, example_english)
TIER1 = [
    ("저", "I, me (polite)", "jeo", "저는 학생이에요.", "I'm a student."),
    ("나", "I, me (casual)", "na", "나는 괜찮아.", "I'm fine."),
    ("우리", "we, our", "uri", "우리 집에 오세요.", "Come to our house."),
    ("사람", "person", "saram", "저 사람은 누구예요?", "Who is that person?"),
    ("것", "thing, one", "geot", "이건 제 거예요.", "This one is mine."),
    ("곳", "place", "got", "좋은 곳이에요.", "It's a nice place."),
    ("때", "time, moment", "ttae", "그때 만났어요.", "We met at that time."),
    ("일", "work; matter; day", "il", "일이 많아요.", "I have a lot of work."),
    ("말", "words, speech", "mal", "말이 빨라요.", "You speak fast."),
    ("집", "house, home", "jip", "집에 가요.", "I'm going home."),
    ("물", "water", "mul", "물 좀 주세요.", "Some water, please."),
    ("밥", "rice; a meal", "bap", "밥 먹었어요?", "Have you eaten?"),
    ("돈", "money", "don", "돈이 없어요.", "I don't have money."),
    ("시간", "time", "sigan", "시간이 없어요.", "I don't have time."),
    ("오늘", "today", "oneul", "오늘 뭐 해요?", "What are you doing today?"),
    ("내일", "tomorrow", "naeil", "내일 만나요.", "See you tomorrow."),
    ("어제", "yesterday", "eoje", "어제 비가 왔어요.", "It rained yesterday."),
    ("지금", "now", "jigeum", "지금 어디예요?", "Where are you now?"),
    ("여기", "here", "yeogi", "여기 앉으세요.", "Please sit here."),
    ("거기", "there", "geogi", "거기 뭐 있어요?", "What's there?"),
    ("어디", "where", "eodi", "화장실이 어디예요?", "Where is the bathroom?"),
    ("언제", "when", "eonje", "언제 와요?", "When are you coming?"),
    ("누구", "who", "nugu", "누구세요?", "Who is it?"),
    ("뭐", "what", "mwo", "뭐 먹을래요?", "What do you want to eat?"),
    ("왜", "why", "wae", "왜 그래요?", "Why? / What's wrong?"),
    ("어떻게", "how", "eotteoke", "어떻게 가요?", "How do I get there?"),
    ("네", "yes", "ne", "네, 맞아요.", "Yes, that's right."),
    ("아니요", "no", "aniyo", "아니요, 괜찮아요.", "No, I'm fine."),
    ("있다", "to exist; to have", "itda", "시간 있어요?", "Do you have time?"),
    ("없다", "to not exist; to lack", "eopda", "돈이 없어요.", "I have no money."),
    ("하다", "to do", "hada", "뭐 해요?", "What are you doing?"),
    ("가다", "to go", "gada", "학교에 가요.", "I go to school."),
    ("오다", "to come", "oda", "친구가 왔어요.", "My friend came."),
    ("보다", "to see, to watch", "boda", "영화를 봤어요.", "I watched a movie."),
    ("먹다", "to eat", "meokda", "점심 먹었어요.", "I ate lunch."),
    ("마시다", "to drink", "masida", "커피를 마셔요.", "I drink coffee."),
    ("자다", "to sleep", "jada", "일찍 잤어요.", "I slept early."),
    ("주다", "to give", "juda", "이거 주세요.", "Please give me this."),
    ("알다", "to know", "alda", "저도 알아요.", "I know too."),
    ("모르다", "to not know", "moreuda", "잘 몰라요.", "I don't really know."),
    ("좋다", "to be good", "jota", "날씨가 좋아요.", "The weather is nice."),
    ("많다", "to be many, a lot", "manta", "사람이 많아요.", "There are a lot of people."),
    ("크다", "to be big", "keuda", "집이 커요.", "The house is big."),
    ("작다", "to be small", "jakda", "방이 작아요.", "The room is small."),
    ("안", "not (before a verb)", "an", "안 가요.", "I'm not going."),
    ("못", "cannot (before a verb)", "mot", "못 갔어요.", "I couldn't go."),
    ("이거", "this thing", "igeo", "이거 뭐예요?", "What is this?"),
    ("그거", "that thing", "geugeo", "그거 주세요.", "Give me that."),
    ("좀", "a little; please (softener)", "jom", "좀 도와주세요.", "Please help me a bit."),
    ("들다", "to hold; to cost; to enter", "deulda", "가방을 들어 주세요.", "Please hold the bag."),
]

TIER2 = [
    ("말하다", "to speak, to say", "malhada", "천천히 말해 주세요.", "Please speak slowly."),
    ("듣다", "to listen, to hear", "deutda", "음악을 들어요.", "I listen to music."),
    ("읽다", "to read", "ikda", "책을 읽어요.", "I read a book."),
    ("쓰다", "to write; to use", "sseuda", "이름을 쓰세요.", "Write your name."),
    ("사다", "to buy", "sada", "뭐 샀어요?", "What did you buy?"),
    ("팔다", "to sell", "palda", "여기서 팔아요.", "They sell it here."),
    ("만나다", "to meet", "mannada", "친구를 만났어요.", "I met a friend."),
    ("살다", "to live", "salda", "서울에 살아요.", "I live in Seoul."),
    ("일하다", "to work", "ilhada", "어디서 일해요?", "Where do you work?"),
    ("공부하다", "to study", "gongbuhada", "한국어를 공부해요.", "I study Korean."),
    ("좋아하다", "to like", "joahada", "김치를 좋아해요.", "I like kimchi."),
    ("싫어하다", "to dislike", "sireohada", "저는 싫어해요.", "I don't like it."),
    ("생각하다", "to think", "saenggakhada", "저도 그렇게 생각해요.", "I think so too."),
    ("필요하다", "to be necessary, to need", "piryohada", "도움이 필요해요.", "I need help."),
    ("시작하다", "to start", "sijakhada", "지금 시작해요.", "Let's start now."),
    ("끝나다", "to end, to be over", "kkeutnada", "수업이 끝났어요.", "Class is over."),
    ("기다리다", "to wait", "gidarida", "조금만 기다려 주세요.", "Please wait just a moment."),
    ("찾다", "to look for, to find", "chatda", "뭘 찾아요?", "What are you looking for?"),
    ("돕다", "to help", "dopda", "도와주세요.", "Please help me."),
    ("배우다", "to learn", "baeuda", "한국어를 배워요.", "I'm learning Korean."),
    ("가르치다", "to teach", "gareuchida", "영어를 가르쳐요.", "I teach English."),
    ("앉다", "to sit", "anda", "여기 앉으세요.", "Please sit here."),
    ("걷다", "to walk", "geotda", "같이 걸어요.", "Let's walk together."),
    ("열다", "to open", "yeolda", "문을 열어 주세요.", "Please open the door."),
    ("닫다", "to close", "datda", "창문을 닫았어요.", "I closed the window."),
    ("나가다", "to go out", "nagada", "밖에 나가요.", "I'm going outside."),
    ("들어가다", "to go in, to enter", "deureogada", "안에 들어가세요.", "Please go inside."),
    ("친구", "friend", "chingu", "친구를 만나요.", "I'm meeting a friend."),
    ("가족", "family", "gajok", "가족이 보고 싶어요.", "I miss my family."),
    ("학생", "student", "haksaeng", "저는 학생이에요.", "I'm a student."),
    ("선생님", "teacher", "seonsaengnim", "선생님, 질문 있어요.", "Teacher, I have a question."),
    ("회사", "company", "hoesa", "회사에 다녀요.", "I work at a company."),
    ("학교", "school", "hakgyo", "학교에 가요.", "I go to school."),
    ("이름", "name", "ireum", "이름이 뭐예요?", "What's your name?"),
    ("나라", "country", "nara", "어느 나라에서 왔어요?", "What country are you from?"),
    ("음식", "food", "eumsik", "한국 음식 좋아해요.", "I like Korean food."),
    ("커피", "coffee", "keopi", "커피 한 잔 주세요.", "One coffee, please."),
    ("책", "book", "chaek", "책을 읽어요.", "I'm reading a book."),
    ("전화", "phone; phone call", "jeonhwa", "전화했어요.", "I called."),
    ("방", "room", "bang", "방이 깨끗해요.", "The room is clean."),
    ("길", "road, way", "gil", "길을 몰라요.", "I don't know the way."),
    ("문", "door", "mun", "문을 닫으세요.", "Please close the door."),
    ("손", "hand", "son", "손을 씻으세요.", "Wash your hands."),
    ("눈", "eye; snow", "nun", "눈이 와요.", "It's snowing."),
    ("몸", "body", "mom", "몸이 아파요.", "My body aches."),
    ("머리", "head; hair", "meori", "머리가 아파요.", "I have a headache."),
    ("차", "tea; car", "cha", "차 마실래요?", "Would you like some tea?"),
    ("옷", "clothes", "ot", "옷을 샀어요.", "I bought clothes."),
    ("날", "day", "nal", "그날 비가 왔어요.", "It rained that day."),
    ("월", "month (in dates)", "wol", "오월에 가요.", "I'm going in May."),
]

TIER3 = [
    ("나쁘다", "to be bad", "nappeuda", "날씨가 나빠요.", "The weather is bad."),
    ("예쁘다", "to be pretty", "yeppeuda", "정말 예뻐요.", "It's really pretty."),
    ("맛있다", "to be delicious", "masitda", "진짜 맛있어요.", "It's really delicious."),
    ("맛없다", "to taste bad", "maseopda", "좀 맛없어요.", "It doesn't taste good."),
    ("비싸다", "to be expensive", "bissada", "너무 비싸요.", "It's too expensive."),
    ("싸다", "to be cheap", "ssada", "여기가 싸요.", "It's cheap here."),
    ("많이", "a lot, much", "mani", "많이 드세요.", "Please eat a lot."),
    ("조금", "a little", "jogeum", "조금만 주세요.", "Just a little, please."),
    ("아주", "very", "aju", "아주 좋아요.", "It's very good."),
    ("너무", "too, excessively", "neomu", "너무 어려워요.", "It's too difficult."),
    ("정말", "really, truly", "jeongmal", "정말 고마워요.", "Thank you so much."),
    ("진짜", "really (casual)", "jinjja", "진짜요?", "Really?"),
    ("잘", "well", "jal", "잘 지냈어요?", "Have you been well?"),
    ("빨리", "quickly", "ppalli", "빨리 오세요.", "Come quickly."),
    ("천천히", "slowly", "cheoncheonhi", "천천히 하세요.", "Take your time."),
    ("다시", "again", "dasi", "다시 말해 주세요.", "Please say that again."),
    ("또", "again; also", "tto", "또 만나요.", "Let's meet again."),
    ("같이", "together", "gachi", "같이 가요.", "Let's go together."),
    ("혼자", "alone", "honja", "혼자 살아요.", "I live alone."),
    ("먼저", "first, ahead", "meonjeo", "먼저 가세요.", "You go ahead."),
    ("나중에", "later", "najunge", "나중에 얘기해요.", "Let's talk later."),
    ("벌써", "already", "beolsseo", "벌써 끝났어요.", "It's already over."),
    ("아직", "still, not yet", "ajik", "아직 안 왔어요.", "They haven't come yet."),
    ("항상", "always", "hangsang", "항상 늦어요.", "You're always late."),
    ("가끔", "sometimes", "gakkeum", "가끔 만나요.", "We meet sometimes."),
    ("어렵다", "to be difficult", "eoryeopda", "한국어가 어려워요.", "Korean is difficult."),
    ("쉽다", "to be easy", "swipda", "생각보다 쉬워요.", "It's easier than I thought."),
    ("재미있다", "to be fun, interesting", "jaemiitda", "정말 재미있어요.", "It's really fun."),
    ("재미없다", "to be boring", "jaemieopda", "좀 재미없어요.", "It's a bit boring."),
    ("바쁘다", "to be busy", "bappeuda", "요즘 바빠요.", "I'm busy these days."),
    ("아프다", "to hurt, to be sick", "apeuda", "배가 아파요.", "My stomach hurts."),
    ("피곤하다", "to be tired", "pigonhada", "너무 피곤해요.", "I'm so tired."),
    ("춥다", "to be cold (weather)", "chupda", "오늘 추워요.", "It's cold today."),
    ("덥다", "to be hot (weather)", "deopda", "여름은 더워요.", "Summer is hot."),
    ("배고프다", "to be hungry", "baegopeuda", "배고파요.", "I'm hungry."),
    ("목마르다", "to be thirsty", "mongmareuda", "목말라요.", "I'm thirsty."),
    ("빠르다", "to be fast", "ppareuda", "정말 빨라요.", "It's really fast."),
    ("느리다", "to be slow", "neurida", "인터넷이 느려요.", "The internet is slow."),
    ("멀다", "to be far", "meolda", "여기서 멀어요?", "Is it far from here?"),
    ("가깝다", "to be close, near", "gakkapda", "아주 가까워요.", "It's very close."),
    ("높다", "to be high, tall", "nopda", "산이 높아요.", "The mountain is high."),
    ("길다", "to be long", "gilda", "머리가 길어요.", "Your hair is long."),
    ("짧다", "to be short", "jjalda", "시간이 짧아요.", "Time is short."),
    ("무겁다", "to be heavy", "mugeopda", "가방이 무거워요.", "The bag is heavy."),
    ("가볍다", "to be light (weight)", "gabyeopda", "아주 가벼워요.", "It's very light."),
    ("깨끗하다", "to be clean", "kkaekkeutada", "방이 깨끗해요.", "The room is clean."),
    ("더럽다", "to be dirty", "deoreopda", "손이 더러워요.", "Your hands are dirty."),
    ("새", "new (before a noun)", "sae", "새 옷이에요.", "They're new clothes."),
    ("오래", "for a long time", "orae", "오래 기다렸어요.", "I waited a long time."),
    ("괜찮다", "to be okay, fine", "gwaenchanta", "괜찮아요.", "It's okay."),
]

TIER4 = [
    ("그리고", "and (joining sentences)", "geurigo", "커피 그리고 빵 주세요.", "Coffee and bread, please."),
    ("그런데", "but; by the way", "geureonde", "그런데 왜요?", "But why?"),
    ("하지만", "but, however", "hajiman", "하지만 어려워요.", "But it's difficult."),
    ("그래서", "so, therefore", "geuraeseo", "그래서 안 갔어요.", "So I didn't go."),
    ("그러면", "then, in that case", "geureomyeon", "그러면 내일 만나요.", "Then let's meet tomorrow."),
    ("아마", "probably", "ama", "아마 올 거예요.", "They'll probably come."),
    ("물론", "of course", "mullon", "물론이죠.", "Of course."),
    ("혹시", "by any chance", "hoksi", "혹시 시간 있어요?", "Do you happen to have time?"),
    ("갑자기", "suddenly", "gapjagi", "갑자기 비가 왔어요.", "It suddenly rained."),
    ("아침", "morning; breakfast", "achim", "아침 먹었어요?", "Did you eat breakfast?"),
    ("점심", "lunch; midday", "jeomsim", "점심 뭐 먹을까요?", "What should we eat for lunch?"),
    ("저녁", "evening; dinner", "jeonyeok", "저녁에 봐요.", "See you in the evening."),
    ("밤", "night", "bam", "밤에 잘 못 자요.", "I don't sleep well at night."),
    ("오전", "morning, a.m.", "ojeon", "오전에 회의 있어요.", "I have a meeting in the morning."),
    ("오후", "afternoon, p.m.", "ohu", "오후에 만나요.", "Let's meet in the afternoon."),
    ("주말", "weekend", "jumal", "주말에 뭐 해요?", "What are you doing this weekend?"),
    ("요일", "day of the week", "yoil", "무슨 요일이에요?", "What day is it?"),
    ("이번", "this (occasion)", "ibeon", "이번 주에 만나요.", "Let's meet this week."),
    ("다음", "next", "daeum", "다음에 봐요.", "See you next time."),
    ("지난", "last, past", "jinan", "지난주에 갔어요.", "I went last week."),
    ("년", "year (counter)", "nyeon", "삼 년 살았어요.", "I lived there three years."),
    ("달", "month; moon", "dal", "세 달 걸려요.", "It takes three months."),
    ("주", "week", "ju", "이번 주 바빠요.", "I'm busy this week."),
    ("시", "o'clock", "si", "몇 시예요?", "What time is it?"),
    ("분", "minute", "bun", "십 분만요.", "Just ten minutes."),
    ("날씨", "weather", "nalssi", "날씨가 좋아요.", "The weather is nice."),
    ("봄", "spring", "bom", "봄이 좋아요.", "I like spring."),
    ("여름", "summer", "yeoreum", "여름은 더워요.", "Summer is hot."),
    ("가을", "autumn, fall", "gaeul", "가을이 예뻐요.", "Autumn is beautiful."),
    ("겨울", "winter", "gyeoul", "겨울은 추워요.", "Winter is cold."),
    ("가게", "shop, store", "gage", "가게에 갔어요.", "I went to the store."),
    ("시장", "market", "sijang", "시장에서 샀어요.", "I bought it at the market."),
    ("역", "station", "yeok", "역이 어디예요?", "Where is the station?"),
    ("병원", "hospital", "byeongwon", "병원에 가야 해요.", "I have to go to the hospital."),
    ("은행", "bank", "eunhaeng", "은행이 닫았어요.", "The bank is closed."),
    ("화장실", "bathroom, restroom", "hwajangsil", "화장실이 어디예요?", "Where is the restroom?"),
    ("자리", "seat, spot", "jari", "자리 있어요?", "Is this seat taken?"),
    ("표", "ticket", "pyo", "표 두 장 주세요.", "Two tickets, please."),
    ("값", "price", "gap", "값이 비싸요.", "The price is high."),
    ("신발", "shoes", "sinbal", "신발이 예뻐요.", "Those shoes are nice."),
    ("가방", "bag", "gabang", "가방이 무거워요.", "The bag is heavy."),
    ("우산", "umbrella", "usan", "우산 있어요?", "Do you have an umbrella?"),
    ("열쇠", "key", "yeolsoe", "열쇠를 잃어버렸어요.", "I lost my key."),
    ("사진", "photo", "sajin", "사진 찍어도 돼요?", "May I take a photo?"),
    ("노래", "song", "norae", "노래를 불러요.", "I'm singing a song."),
    ("영화", "movie", "yeonghwa", "영화 봤어요?", "Did you see the movie?"),
    ("이야기", "story, talk", "iyagi", "이야기해요.", "Let's talk."),
    ("문제", "problem; question", "munje", "문제가 있어요.", "There's a problem."),
    ("생각", "thought, idea", "saenggak", "좋은 생각이에요.", "That's a good idea."),
    ("기분", "mood, feeling", "gibun", "기분이 좋아요.", "I'm in a good mood."),
]

TIERS = [
    ("tier1", TIER1, True),
    ("tier2", TIER2, False),
    ("tier3", TIER3, False),
    ("tier4", TIER4, False),
]


def main():
    b = Build("03_core_vocab", "Korean v2::03 Core vocab (frequency)")
    model = vocab_model()

    for tier_tag, entries, produce in TIERS:
        for korean, english, reading, example, example_en in entries:
            b.add(
                model,
                [
                    korean,
                    english,
                    reading,
                    example,
                    example_en,
                    b.audio(korean),
                    "y" if produce else "",
                ],
                tags=["vocab", tier_tag],
            )

    b.write()


if __name__ == "__main__":
    main()
