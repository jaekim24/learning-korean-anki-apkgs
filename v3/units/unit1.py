# -*- coding: utf-8 -*-
"""Unit 1 -- Basic Korean Grammar (HTSK lessons 1-25).

Content here is written for this deck. The HTSK index supplies only the lesson
numbering, titles and source links (see korean/syllabus.py); the patterns,
explanations and example sentences below are our own, so the deck can be built
and shared without redistributing their lesson text.

Style rules for this unit, kept consistent so cards drill grammar and not
register variation:
  - Everything is 해요체 unless the lesson is specifically about another speech
    level (Lesson 6, honorifics).
  - Sentences stay short enough that the target pattern is the only new thing.
  - `produce=True` opts a note into an EN->KR production card. Used sparingly:
    the patterns and sentences worth being able to generate cold, not all of them.

Schema:
  points:    (pattern, meaning, form, note, produce)
  vocab:     (korean, english, note, produce)
  sentences: (korean, english, note, produce)
"""

LESSONS = {
    1: {
        'points': [
            ('N은/는', 'Topic particle -- marks what the sentence is about', '은 after a consonant, 는 after a vowel.<br>학생 → 학생은 &nbsp;·&nbsp; 저 → 저는', 'Introduces or contrasts a topic. Not the same as the subject particle in Lesson 2.', True),
            ('N이다', 'to be (equating one noun with another)', 'Polite 해요체: 이에요 after a consonant, 예요 after a vowel.<br>학생 → 학생이에요 &nbsp;·&nbsp; 의사 → 의사예요', "Attaches directly to the noun -- there is no separate word for 'is'.", True),
        ],
        'vocab': [
            ('저', 'I (humble)', 'Used with 는. Plain form is 나.', True),
            ('학생', 'student', '', True),
            ('책', 'book', '', True),
            ('사람', 'person', '', True),
            ('의사', 'doctor', '', False),
            ('선생님', 'teacher', '님 is an honorific suffix.', True),
            ('이것', 'this thing', 'Contracts to 이거 in speech.', False),
        ],
        'sentences': [
            ('저는 학생이에요.', 'I am a student.', '저 = I (humble). 는 because 저 ends in a vowel.', True),
            ('이것은 책이에요.', 'This is a book.', '책 ends in a consonant, so 이에요.', False),
            ('그 사람은 의사예요.', 'That person is a doctor.', '의사 ends in a vowel, so 예요.', False),
            ('저는 한국 사람이에요.', 'I am Korean.', '사람 = person; 한국 사람 = Korean person.', True),
            ('이 사람은 제 친구예요.', 'This person is my friend.', '제 = my (humble).', False),
        ],
    },
    2: {
        'points': [
            ('N이/가', 'Subject particle -- marks who or what does the action', '이 after a consonant, 가 after a vowel.<br>물 → 물이 &nbsp;·&nbsp; 친구 → 친구가', '은/는 frames the topic; 이/가 identifies the subject. New or specific information tends to take 이/가.', True),
        ],
        'vocab': [
            ('물', 'water', '', True),
            ('친구', 'friend', '', True),
            ('날씨', 'weather', '', True),
            ('고양이', 'cat', '', False),
            ('시간', 'time; hour', '', True),
            ('문', 'door', '', False),
        ],
        'sentences': [
            ('물이 차가워요.', 'The water is cold.', '물 takes 이 after its final consonant.', False),
            ('친구가 왔어요.', 'A friend came.', '친구 takes 가 after its final vowel.', True),
            ('날씨가 좋아요.', 'The weather is nice.', "Describing a subject's state uses 이/가, not 은/는.", False),
            ('고양이가 자요.', 'The cat is sleeping.', '자다 → 자요.', False),
            ('시간이 없어요.', "There's no time.", '없다 with the subject particle.', True),
        ],
    },
    3: {
        'points': [
            ('N을/를', 'Object particle -- marks what the verb acts on', '을 after a consonant, 를 after a vowel.<br>밥 → 밥을 &nbsp;·&nbsp; 커피 → 커피를', 'Korean word order is Subject–Object–Verb: the verb always comes last.', True),
        ],
        'vocab': [
            ('밥', 'rice; a meal', '밥을 먹다 = to eat a meal.', True),
            ('커피', 'coffee', '', False),
            ('먹다', 'to eat', '', True),
            ('마시다', 'to drink', '', True),
            ('보다', 'to see; to watch', '', True),
            ('하다', 'to do', 'The most common verb; forms compounds.', True),
        ],
        'sentences': [
            ('저는 밥을 먹어요.', 'I eat rice.', 'Subject–Object–Verb. 밥 takes 을.', True),
            ('저는 커피를 마셔요.', 'I drink coffee.', '커피 takes 를 after its final vowel.', False),
            ('동생이 물을 마셔요.', 'My younger sibling drinks water.', 'Subject 이, object 을, verb last.', False),
            ('친구가 영화를 봐요.', 'My friend watches a movie.', 'Subject 가, object 를.', False),
            ('저는 숙제를 해요.', 'I do homework.', '하다 → 해요.', True),
        ],
    },
    4: {
        'points': [
            ('Adj + ~ㄴ/은 + N', 'Turns an adjective into one that describes a noun', 'Stem + ㄴ after a vowel, + 은 after a consonant.<br>예쁘다 → 예쁜 &nbsp;·&nbsp; 작다 → 작은', 'Korean adjectives conjugate like verbs, so they need this form to sit in front of a noun.', True),
        ],
        'vocab': [
            ('예쁘다', 'to be pretty', 'ㅡ irregular.', True),
            ('작다', 'to be small', '', True),
            ('크다', 'to be big', 'ㅡ irregular.', True),
            ('좋다', 'to be good', '', True),
            ('꽃', 'flower', '', False),
            ('가방', 'bag', '', False),
        ],
        'sentences': [
            ('예쁜 꽃이 많아요.', 'There are many pretty flowers.', '예쁘다 → 예쁜 before the noun.', False),
            ('작은 가방을 샀어요.', 'I bought a small bag.', '작다 → 작은 after its final consonant.', True),
            ('좋은 사람이에요.', "It's a good person.", '좋다 → 좋은.', False),
            ('새 책을 읽어요.', 'I read a new book.', '새 is a determiner, so it needs no ~ㄴ/은.', False),
            ('큰 집에 살아요.', 'I live in a big house.', '크다 → 큰.', True),
        ],
    },
    5: {
        'points': [
            ('~아/어요', 'Present tense, polite', 'Stem vowel ㅏ or ㅗ → 아요, otherwise → 어요, and 하다 → 해요.<br>가다 → 가요 &nbsp;·&nbsp; 먹다 → 먹어요 &nbsp;·&nbsp; 공부하다 → 공부해요', 'The everyday polite ending. Same form serves as a statement or, with rising tone, a question.', True),
            ('~았/었어요', 'Past tense, polite', 'Same vowel rule, then 았/었 + 어요.<br>가다 → 갔어요 &nbsp;·&nbsp; 먹다 → 먹었어요 &nbsp;·&nbsp; 하다 → 했어요', '', True),
            ('~(으)ㄹ 거예요', 'Future tense -- will / is going to', 'Stem + ㄹ 거예요 after a vowel, + 을 거예요 after a consonant.<br>가다 → 갈 거예요 &nbsp;·&nbsp; 먹다 → 먹을 거예요', "Also carries a sense of probability: 'probably will'.", True),
        ],
        'vocab': [
            ('가다', 'to go', '', True),
            ('오다', 'to come', '', True),
            ('공부하다', 'to study', '', True),
            ('영화', 'movie', '', False),
            ('어제', 'yesterday', '', True),
            ('내일', 'tomorrow', '', True),
            ('지금', 'now', '', True),
        ],
        'sentences': [
            ('어제 영화를 봤어요.', 'I watched a movie yesterday.', '보다 → 봤어요.', True),
            ('내일 학교에 갈 거예요.', 'I will go to school tomorrow.', '가다 → 갈 거예요.', True),
            ('지금 공부해요.', "I'm studying now.", '하다 verbs → 해요.', False),
            ('저는 매일 공부해요.', 'I study every day.', '매일 = every day.', True),
            ('친구가 내일 올 거예요.', 'My friend will come tomorrow.', '오다 → 올 거예요.', False),
        ],
    },
    6: {
        'points': [
            ('~(으)시~', "Honorific infix -- raises the person you're speaking about", 'Stem + 시 after a vowel, + 으시 after a consonant; commonly surfaces as ~(으)세요.<br>가다 → 가세요 &nbsp;·&nbsp; 읽다 → 읽으세요', 'Used for elders and superiors. Never applied to yourself.', True),
            ('~ㅂ/습니다', 'Formal polite speech level', 'Stem + ㅂ니다 after a vowel, + 습니다 after a consonant.<br>가다 → 갑니다 &nbsp;·&nbsp; 먹다 → 먹습니다', 'More formal than 해요체 -- news broadcasts, presentations, the military.', False),
        ],
        'vocab': [
            ('할아버지', 'grandfather', '', False),
            ('할머니', 'grandmother', '', False),
            ('신문', 'newspaper', '', False),
            ('계시다', 'to be, to stay (honorific)', 'Honorific of 있다.', True),
            ('드시다', 'to eat (honorific)', 'Honorific of 먹다.', True),
            ('께서', 'subject particle (honorific)', 'Honorific of 이/가.', False),
        ],
        'sentences': [
            ('할아버지가 신문을 읽으세요.', 'Grandfather reads the newspaper.', '읽다 + 으시 → 읽으세요, honoring the grandfather.', False),
            ('안녕히 가세요.', 'Goodbye. (to someone leaving)', 'Said to the person who is departing.', True),
            ('어디에 가십니까?', 'Where are you going?', 'Honorific 시 plus the formal ending.', False),
            ('어머니께서 요리하세요.', 'Mother cooks.', '께서 is the honorific subject particle.', False),
            ('선생님께서 오셨어요.', 'The teacher came.', '오다 + 시 + 었어요 → 오셨어요.', True),
        ],
    },
    7: {
        'points': [
            ('ㅂ irregular', 'ㅂ becomes 우 before a vowel ending', '춥다 → 추워요 &nbsp;·&nbsp; 어렵다 → 어려워요 &nbsp;·&nbsp; 돕다 → 도와요', 'Applies to most ㅂ-final adjectives. 좁다 and 잡다 are regular.', True),
            ('ㅡ irregular', 'The final ㅡ drops before a vowel ending', '바쁘다 → 바빠요 &nbsp;·&nbsp; 쓰다 → 써요 &nbsp;·&nbsp; 예쁘다 → 예뻐요', 'The vowel of the preceding syllable decides 아 or 어.', True),
            ('르 irregular', '르 becomes ㄹㄹ before a vowel ending', '모르다 → 몰라요 &nbsp;·&nbsp; 부르다 → 불러요 &nbsp;·&nbsp; 다르다 → 달라요', '', True),
            ('ㄷ irregular', 'ㄷ becomes ㄹ before a vowel ending', '듣다 → 들어요 &nbsp;·&nbsp; 걷다 → 걸어요', '받다 and 닫다 are regular.', False),
        ],
        'vocab': [
            ('춥다', 'to be cold (weather)', 'ㅂ irregular.', True),
            ('덥다', 'to be hot (weather)', 'ㅂ irregular.', True),
            ('어렵다', 'to be difficult', 'ㅂ irregular.', True),
            ('바쁘다', 'to be busy', 'ㅡ irregular.', True),
            ('모르다', 'to not know', '르 irregular.', True),
            ('듣다', 'to listen', 'ㄷ irregular.', True),
            ('걷다', 'to walk', 'ㄷ irregular.', False),
        ],
        'sentences': [
            ('오늘은 정말 추워요.', 'Today is really cold.', '춥다 → 추워요 (ㅂ irregular).', True),
            ('저는 잘 몰라요.', "I don't really know.", '모르다 → 몰라요 (르 irregular).', True),
            ('요즘 너무 바빠요.', "I'm too busy these days.", '바쁘다 → 바빠요 (ㅡ irregular).', False),
            ('음악을 들어요.', 'I listen to music.', '듣다 → 들어요 (ㄷ irregular).', True),
            ('한국어는 어려워요.', 'Korean is difficult.', '어렵다 → 어려워요 (ㅂ irregular).', True),
        ],
    },
    8: {
        'points': [
            ('Adj + ~게', 'Turns an adjective into an adverb', 'Stem + 게.<br>조용하다 → 조용하게 &nbsp;·&nbsp; 쉽다 → 쉽게', "The general-purpose way to say '-ly'.", True),
            ('안 + V / ~지 않다', "Negation -- don't / doesn't", '안 goes in front of the verb; ~지 않다 attaches to the stem.<br>안 먹어요 = 먹지 않아요', 'Identical in meaning. 안 is more colloquial; ~지 않다 is slightly more formal.', True),
        ],
        'vocab': [
            ('고기', 'meat', '', False),
            ('재미있다', 'to be interesting, fun', '', True),
            ('조용하다', 'to be quiet', '', False),
            ('쉽다', 'to be easy', 'ㅂ irregular.', True),
            ('말하다', 'to speak', '', True),
            ('술', 'alcohol', '', False),
        ],
        'sentences': [
            ('저는 고기를 안 먹어요.', "I don't eat meat.", '안 placed directly before the verb.', True),
            ('그 영화는 재미있지 않아요.', "That movie isn't interesting.", '~지 않다 on the stem.', False),
            ('조용하게 말해 주세요.', 'Please speak quietly.', '조용하다 → 조용하게.', False),
            ('빠르게 걸었어요.', 'I walked quickly.', '빠르다 → 빠르게.', False),
            ('저는 술을 안 마셔요.', "I don't drink alcohol.", '안 before the verb.', True),
        ],
    },
    9: {
        'points': [
            ('N일 거예요', 'Future / supposition of 이다 -- will be, is probably', 'Noun + 일 거예요.<br>선생님 → 선생님일 거예요', 'The 이다 counterpart of the ~(으)ㄹ 거예요 in Lesson 5.', True),
            ('~(으)ㄹ 것이다', 'The written/formal form behind ~(으)ㄹ 거예요', '것이다 contracts to 거예요 in speech.', 'Useful to recognize in writing.', False),
        ],
        'vocab': [
            ('집', 'house; home', '', True),
            ('있다', 'to exist; to have', '', True),
            ('없다', 'to not exist; to lack', '', True),
            ('아마', 'probably', 'Pairs with ~ㄹ 거예요.', False),
            ('비싸다', 'to be expensive', '', True),
        ],
        'sentences': [
            ('그 사람은 선생님일 거예요.', 'That person is probably a teacher.', '이다 → 일 거예요.', True),
            ('저는 집에 있을 거예요.', 'I will be at home.', '있다 → 있을 거예요 after a consonant.', False),
            ('아마 비쌀 거예요.', "It's probably expensive.", '아마 pairs naturally with ~ㄹ 거예요.', True),
            ('내일은 바쁠 거예요.', "I'll be busy tomorrow.", '바쁘다 → 바쁠 거예요.', False),
        ],
    },
    10: {
        'points': [
            ('Sino-Korean numbers', '일 이 삼 사 오 육 칠 팔 구 십', 'Used for dates, money, phone numbers, minutes, and counting above ~100.', 'Borrowed from Chinese. 십일 = 11, 이십 = 20.', True),
            ('Native Korean numbers', '하나 둘 셋 넷 다섯 여섯 일곱 여덟 아홉 열', 'Used for counting objects and for the hour.<br>Before a counter: 하나→한, 둘→두, 셋→세, 넷→네', 'Only goes up to 99 in practical use.', True),
        ],
        'vocab': [
            ('개', 'counter for objects', 'Takes native numbers.', True),
            ('명', 'counter for people', '', True),
            ('살', 'counter for age', '스무 살 = 20 years old.', True),
            ('사과', 'apple', '', False),
            ('시', "o'clock", 'Takes native numbers.', True),
            ('전화번호', 'phone number', 'Takes Sino-Korean.', False),
        ],
        'sentences': [
            ('사과 세 개를 샀어요.', 'I bought three apples.', 'Native number + counter 개; 셋 → 세.', True),
            ('지금 두 시예요.', "It's two o'clock now.", 'Hours take native numbers; 둘 → 두.', True),
            ('전화번호가 삼사오예요.', 'The phone number is three-four-five.', 'Phone numbers take Sino-Korean.', False),
            ('학생이 열 명 있어요.', 'There are ten students.', 'Native number + counter 명.', True),
            ('저는 스무 살이에요.', 'I am twenty years old.', '스물 → 스무 before 살.', True),
        ],
    },
    11: {
        'points': [
            ('N 동안', 'for (a duration)', 'Time amount + 동안.<br>세 시간 동안 = for three hours', 'Measures how long something lasted.', True),
            ('Time units', '초 · 분 · 시간 · 일 · 주 · 달/개월 · 년', 'Second · minute · hour · day · week · month · year', '시간 = duration in hours, 시 = the hour on the clock.', False),
        ],
        'vocab': [
            ('초', 'second', '', False),
            ('분', 'minute', '', True),
            ('주', 'week', '', True),
            ('달', 'month', '개월 is the Sino-Korean counterpart.', False),
            ('년', 'year', '', True),
            ('여행하다', 'to travel', '', False),
        ],
        'sentences': [
            ('세 시간 동안 공부했어요.', 'I studied for three hours.', '시간 for elapsed hours, with 동안.', True),
            ('이 주 동안 여행했어요.', 'I traveled for two weeks.', '주 = week.', False),
            ('오 분 동안 기다렸어요.', 'I waited for five minutes.', '분 takes Sino-Korean numbers.', True),
            ('일 년 동안 한국어를 배웠어요.', 'I studied Korean for a year.', '년 takes Sino-Korean numbers.', False),
        ],
    },
    12: {
        'points': [
            ('N만', 'only, just', 'Attaches directly to the noun.<br>물만 = only water', 'Replaces 은/는 or 이/가 rather than stacking with them.', True),
            ('N에서', 'at / in / from (a place)', 'Marks where an action happens, or a starting point.', '에 marks a destination or location of existence; 에서 marks where an action occurs.', True),
            ('N부터 N까지', 'from ~ until ~', '부터 for the start, 까지 for the end.', '에서...까지 is preferred for physical places.', True),
            ('N(으)로', 'by means of / toward', '로 after a vowel or ㄹ, 으로 after other consonants.<br>버스 → 버스로 &nbsp;·&nbsp; 손 → 손으로', 'Covers tools, methods, and direction.', True),
        ],
        'vocab': [
            ('일하다', 'to work', '', True),
            ('학교', 'school', '', True),
            ('버스', 'bus', '', False),
            ('지하철', 'subway', '', False),
            ('손', 'hand', '', False),
            ('까지', 'until; as far as', '', True),
        ],
        'sentences': [
            ('저는 집에서 일해요.', 'I work at home.', '에서 because working is an action done there.', True),
            ('아홉 시부터 여섯 시까지 일해요.', 'I work from nine to six.', '부터...까지 spanning a time range.', True),
            ('버스로 학교에 갔어요.', 'I went to school by bus.', '(으)로 marking the means.', False),
            ('커피만 마셔요.', 'I only drink coffee.', '만 replaces the object particle.', True),
            ('지하철로 왔어요.', 'I came by subway.', '(으)로 for the means.', False),
        ],
    },
    13: {
        'points': [
            ('과/와, 하고, (이)랑', 'and / with (joining nouns)', '과 after a consonant, 와 after a vowel. 하고 and (이)랑 attach to either.', '과/와 is the most formal, 하고 neutral, (이)랑 casual.', True),
            ('에게/한테/께', 'to (a person)', '한테 is spoken, 에게 written, 께 honorific.', 'For things rather than people, use 에.', True),
            ('N에 대해', 'about, concerning', 'Noun + 에 대해(서).', '에 대한 is the form used before a noun.', True),
        ],
        'vocab': [
            ('어머니', 'mother', '엄마 is the casual form.', True),
            ('아버지', 'father', '아빠 is the casual form.', True),
            ('선물', 'present, gift', '', False),
            ('역사', 'history', '', False),
            ('같이', 'together', 'Pronounced 가치.', True),
            ('주다', 'to give', '', True),
        ],
        'sentences': [
            ('친구하고 같이 갔어요.', 'I went with a friend.', '하고 joining a person, with 같이.', True),
            ('어머니한테 선물을 줬어요.', 'I gave a present to my mother.', '한테 marking the recipient.', False),
            ('한국 역사에 대해 배웠어요.', 'I learned about Korean history.', '에 대해 = about.', False),
            ('동생과 같이 놀았어요.', 'I played with my younger sibling.', '과 after a consonant.', False),
            ('선생님께 편지를 썼어요.', 'I wrote a letter to the teacher.', '께 is the honorific of 에게.', True),
        ],
    },
    14: {
        'points': [
            ('Passive 이/히/리/기', 'Makes an active verb passive', '보다 → 보이다 &nbsp;·&nbsp; 먹다 → 먹히다 &nbsp;·&nbsp; 열다 → 열리다 &nbsp;·&nbsp; 끊다 → 끊기다', 'Which of the four attaches is lexical -- it has to be learned per verb.', True),
            ('하다 → 되다', 'The passive counterpart of 하다 verbs', '시작하다 → 시작되다 &nbsp;·&nbsp; 준비하다 → 준비되다', 'The passive subject takes 이/가, not 을/를.', True),
        ],
        'vocab': [
            ('열다', 'to open', '', True),
            ('닫다', 'to close', '', True),
            ('산', 'mountain', '', False),
            ('수업', 'class, lesson', '', False),
            ('시작하다', 'to start', '', True),
            ('창문', 'window', '', False),
        ],
        'sentences': [
            ('문이 열렸어요.', 'The door opened.', '열다 → 열리다, subject marked with 이.', True),
            ('산이 잘 보여요.', 'The mountain is clearly visible.', '보다 → 보이다.', False),
            ('수업이 시작됐어요.', 'The class started.', '시작하다 → 시작되다.', False),
            ('창문이 닫혔어요.', 'The window closed.', '닫다 → 닫히다.', True),
            ('제 이름이 불렸어요.', 'My name was called.', '부르다 → 불리다.', False),
        ],
    },
    15: {
        'points': [
            ('다르다 / 비슷하다 / 같다', 'different / similar / same', 'Compared-against noun takes 과/와 or 하고.<br>A는 B와 달라요', '같다 often appears as 같아요 with 와/과.', True),
            ('N이/가 아프다', 'to hurt, to be sick', 'The body part takes 이/가.<br>배가 아파요 = my stomach hurts', '아프다 is an adjective, so it takes adjective endings.', True),
        ],
        'vocab': [
            ('아프다', 'to hurt; to be sick', 'ㅡ irregular.', True),
            ('배', 'stomach; boat; pear', 'A common homonym.', True),
            ('머리', 'head; hair', '', True),
            ('다르다', 'to be different', '르 irregular.', True),
            ('비슷하다', 'to be similar', '', False),
            ('감기', 'a cold (illness)', '감기에 걸리다 = to catch a cold.', False),
        ],
        'sentences': [
            ('두 가방이 비슷해요.', 'The two bags are similar.', '비슷하다 describing a subject.', False),
            ('배가 아파요.', 'My stomach hurts.', '아프다 → 아파요 (ㅡ irregular).', True),
            ('이것은 저것과 달라요.', 'This is different from that.', '과 marking what it differs from.', False),
            ('머리가 아파요.', 'My head hurts.', 'The body part takes 이/가.', True),
            ('감기에 걸렸어요.', 'I caught a cold.', '걸리다 with 감기.', True),
        ],
    },
    16: {
        'points': [
            ('N + ~적', 'Turns a Sino-Korean noun into a descriptor', '~적인 before a noun, ~적으로 as an adverb, ~적이다 as a predicate.<br>개인 → 개인적인 / 개인적으로', 'Only attaches to Sino-Korean nouns.', True),
            ('~스럽다', '-like, having the quality of', 'Noun + 스럽다 → 스러운 (before a noun), 스러워요 (predicate).<br>사랑 → 사랑스러워요', 'Conjugates as a ㅂ irregular.', True),
        ],
        'vocab': [
            ('개인', 'individual', '', False),
            ('문제', 'problem; question', '', True),
            ('사랑', 'love', '', True),
            ('자연', 'nature', '', False),
            ('사회', 'society', '', False),
        ],
        'sentences': [
            ('그것은 개인적인 문제예요.', 'That is a personal matter.', '적인 before the noun 문제.', False),
            ('개인적으로 그 영화를 좋아해요.', 'Personally, I like that movie.', '적으로 as an adverb.', True),
            ('그 아이는 사랑스러워요.', 'That child is lovable.', '사랑 + 스럽다, ㅂ irregular.', False),
            ('자연스럽게 말해요.', 'Speak naturally.', '자연 + 스럽다 → 자연스럽게.', True),
            ('그것은 사회적인 문제예요.', 'That is a social problem.', '사회 + 적인 before a noun.', False),
        ],
    },
    17: {
        'points': [
            ('~고', 'and / and then (joining clauses)', 'Stem + 고.<br>먹다 → 먹고', 'Joins verbs or clauses in sequence. Tense is carried by the final verb only.', True),
            ('~고 싶다', 'want to', 'Stem + 고 싶다.<br>가다 → 가고 싶어요', "For a third person's desire, Korean uses ~고 싶어하다.", True),
        ],
        'vocab': [
            ('한국', 'Korea', '', True),
            ('배우다', 'to learn', '', True),
            ('만나다', 'to meet', '', True),
            ('쉬다', 'to rest', '', False),
            ('여행', 'travel, a trip', '', False),
        ],
        'sentences': [
            ('저는 한국에 가고 싶어요.', 'I want to go to Korea.', '가다 + 고 싶다.', True),
            ('밥을 먹고 학교에 갔어요.', 'I ate and then went to school.', 'Only the last verb carries past tense.', True),
            ('친구를 만나고 싶어요.', 'I want to meet a friend.', '만나다 + 고 싶다.', True),
            ('밥을 먹고 쉬었어요.', 'I ate and then rested.', '~고 joining two clauses.', False),
        ],
    },
    18: {
        'points': [
            ('~고 있다', 'Present progressive -- is ___ing', 'Stem + 고 있다.<br>공부하다 → 공부하고 있어요', 'Plain ~아/어요 often covers the progressive too; ~고 있다 makes it explicit.', True),
            ('Adj + ~아/어지다', 'to become, to get ___', 'Adjective stem + 아/어지다.<br>따뜻하다 → 따뜻해지다', 'Turns a state into a change of state.', True),
        ],
        'vocab': [
            ('기다리다', 'to wait', '', True),
            ('따뜻하다', 'to be warm', '', True),
            ('시원하다', 'to be cool, refreshing', '', False),
            ('살다', 'to live', 'ㄹ irregular.', True),
        ],
        'sentences': [
            ('지금 공부하고 있어요.', "I'm studying right now.", 'Explicitly ongoing.', True),
            ('날씨가 따뜻해졌어요.', 'The weather has gotten warm.', '따뜻하다 → 따뜻해지다, past tense.', True),
            ('친구를 기다리고 있어요.', "I'm waiting for a friend.", '기다리다 + 고 있다.', True),
            ('날씨가 시원해졌어요.', 'The weather has gotten cool.', '시원하다 → 시원해지다.', False),
        ],
    },
    19: {
        'points': [
            ('N보다 (더)', 'more than N', 'The compared-against noun takes 보다; 더 is optional but common.<br>어제보다 더 더워요', '보다 attaches to the thing being surpassed.', True),
            ('가장 / 제일', 'most, -est', 'Placed before the adjective.<br>가장 좋아요 = is the best', '제일 is more conversational.', True),
        ],
        'vocab': [
            ('더', 'more', '', True),
            ('가장', 'most, -est', '', True),
            ('제일', 'most, -est', 'More conversational than 가장.', False),
            ('싸다', 'to be cheap', '', True),
        ],
        'sentences': [
            ('오늘이 어제보다 더 더워요.', 'Today is hotter than yesterday.', '보다 on 어제, the thing surpassed.', True),
            ('이게 가장 좋아요.', 'This is the best.', '가장 before the adjective.', False),
            ('이 책이 더 비싸요.', 'This book is more expensive.', '더 before the adjective.', True),
            ('저는 커피를 제일 좋아해요.', 'I like coffee the most.', '제일 = 가장.', False),
        ],
    },
    20: {
        'points': [
            ('잘하다 / 못하다', 'to be good at / bad at', 'Often with the skill as object: 한국어를 잘해요.', '잘 = well, 못 = cannot, as separate adverbs too.', True),
            ('못 + V', 'cannot (inability)', '못 goes before the verb; 하다 verbs split as 공부 못 해요.', '안 is choosing not to; 못 is being unable to.', True),
            ('잘못', 'wrongly, mistakenly', "One word -- distinct from 잘 and 못.<br>잘못했어요 = I did wrong / I'm sorry", '', False),
        ],
        'vocab': [
            ('잘하다', 'to be good at', '', True),
            ('못하다', 'to be bad at', '', True),
            ('노래', 'song', '노래를 부르다 = to sing.', True),
            ('수영', 'swimming', '', False),
            ('운전', 'driving', '', False),
        ],
        'sentences': [
            ('저는 한국어를 잘해요.', "I'm good at Korean.", 'Skill as the object of 잘하다.', True),
            ('오늘은 못 가요.', "I can't go today.", '못 for inability, before the verb.', True),
            ('노래를 잘 불러요.', 'I sing well.', '부르다 → 불러요 (르 irregular).', True),
            ('저는 수영을 못해요.', "I can't swim.", '못하다 with the skill as object.', True),
        ],
    },
    21: {
        'points': [
            ('왜 · 언제 · 어디 · 누구', 'why · when · where · who', 'Placed where the answer would go -- word order does not change.<br>어디 takes 에/에서 for places.', '누구 + 가 contracts to 누가.', True),
        ],
        'vocab': [
            ('왜', 'why', '', True),
            ('언제', 'when', '', True),
            ('어디', 'where', '', True),
            ('누구', 'who', '누구 + 가 becomes 누가.', True),
            ('전화하다', 'to call (phone)', '', False),
        ],
        'sentences': [
            ('왜 안 왔어요?', "Why didn't you come?", '왜 before the negated verb.', True),
            ('어디에 가요?', 'Where are you going?', '어디 + 에 for a destination.', True),
            ('이 사람은 누구예요?', 'Who is this person?', '누구 + 예요.', False),
            ('언제 왔어요?', 'When did you come?', '언제 before the verb.', True),
            ('누가 전화했어요?', 'Who called?', '누구 + 가 → 누가.', True),
        ],
    },
    22: {
        'points': [
            ('어떻게 · 뭐/무엇 · 어느 · 몇', 'how · what · which · how many', '뭐 is the spoken form of 무엇. 어느 and 몇 come before a noun.<br>몇 시 = what time', '몇 pairs with a counter: 몇 개, 몇 명, 몇 시.', True),
        ],
        'vocab': [
            ('어떻게', 'how', '', True),
            ('뭐', 'what', 'Spoken form of 무엇.', True),
            ('어느', 'which', 'Comes before a noun.', True),
            ('몇', 'how many', 'Comes before a counter.', True),
            ('이름', 'name', '', True),
        ],
        'sentences': [
            ('이름이 뭐예요?', 'What is your name?', '뭐 + 예요.', True),
            ('학교에 어떻게 가요?', 'How do you get to school?', '어떻게 before the verb.', True),
            ('지금 몇 시예요?', 'What time is it now?', '몇 + counter 시.', False),
            ('어느 것이 좋아요?', 'Which one is good?', '어느 before a noun.', False),
            ('몇 명이 왔어요?', 'How many people came?', '몇 + counter 명.', True),
        ],
    },
    23: {
        'points': [
            ('ㅎ irregular', 'The ㅎ drops before an ending', '빨갛다 → 빨간 (before a noun), 빨개요 (predicate)<br>그렇다 → 그런 / 그래요', 'Covers the color adjectives and 이렇다/그렇다/저렇다. 좋다 and 넣다 are regular.', True),
            ('Colors', '빨갛다 · 파랗다 · 노랗다 · 하얗다 · 까맣다', 'red · blue · yellow · white · black', 'All follow the ㅎ irregular.', True),
        ],
        'vocab': [
            ('빨갛다', 'to be red', 'ㅎ irregular.', True),
            ('파랗다', 'to be blue', 'ㅎ irregular.', True),
            ('노랗다', 'to be yellow', 'ㅎ irregular.', True),
            ('하얗다', 'to be white', 'ㅎ irregular.', True),
            ('까맣다', 'to be black', 'ㅎ irregular.', True),
            ('하늘', 'sky', '', False),
        ],
        'sentences': [
            ('빨간 사과를 먹었어요.', 'I ate a red apple.', '빨갛다 → 빨간 before the noun.', True),
            ('하늘이 파래요.', 'The sky is blue.', '파랗다 → 파래요.', True),
            ('노란 꽃이 예뻐요.', 'The yellow flower is pretty.', '노랗다 → 노란.', True),
            ('그렇게 하세요.', 'Do it that way.', '그렇다 → 그렇게.', False),
        ],
    },
    24: {
        'points': [
            ('V~기 전에 / N 전에', 'before', 'Verb stem + 기 전에, or noun + 전에.<br>먹다 → 먹기 전에', 'Always 기 전에 for verbs -- never the plain stem.', True),
            ('V~(으)ㄴ 후에 / N 후에', 'after', 'Verb stem + ㄴ/은 후에, or noun + 후에.<br>먹다 → 먹은 후에', '~고 나서 is a common spoken alternative.', True),
            ('N 이내에', 'within (a time span)', 'Noun + 이내에.<br>일주일 이내에 = within a week', '', False),
        ],
        'vocab': [
            ('전', 'before', '', True),
            ('후', 'after', '', True),
            ('씻다', 'to wash', '', False),
            ('자다', 'to sleep', '', True),
            ('일주일', 'one week', '', False),
            ('끝내다', 'to finish', '', False),
        ],
        'sentences': [
            ('밥을 먹기 전에 손을 씻어요.', 'I wash my hands before eating.', '~기 전에 on the verb stem.', True),
            ('수업 후에 만나요.', "Let's meet after class.", 'Noun + 후에.', True),
            ('자기 전에 책을 읽어요.', 'I read a book before sleeping.', '자다 → 자기 전에.', True),
            ('일주일 이내에 끝낼 거예요.', "I'll finish within a week.", '이내에 = within.', False),
        ],
    },
    25: {
        'points': [
            ('아무도 + negative', 'nobody', 'Requires a negative verb.<br>아무도 안 왔어요', 'The negative is obligatory -- 아무도 왔어요 is ungrammatical.', True),
            ('누구나 / 아무나', 'anyone', '누구나 = anyone at all (inclusive); 아무나 = just anyone (indiscriminate).', '아무거나 = anything, 아무데나 = anywhere.', True),
            ('모두 / 다', 'everyone, everything, all', '모두 can be a noun or adverb; 다 is an adverb.', '', False),
        ],
        'vocab': [
            ('아무도', 'nobody', 'Requires a negative verb.', True),
            ('누구나', 'anyone', '', True),
            ('모두', 'everyone; everything; all', '', True),
            ('다', 'all, entirely', 'Adverb.', True),
            ('아무거나', 'anything', '', False),
        ],
        'sentences': [
            ('아무도 안 왔어요.', 'Nobody came.', '아무도 with an obligatory negative.', True),
            ('누구나 할 수 있어요.', 'Anyone can do it.', '누구나 as an inclusive subject.', True),
            ('다 먹었어요.', 'I ate it all.', '다 as an adverb before the verb.', False),
            ('아무나 올 수 있어요.', 'Just anyone can come.', "아무나 = indiscriminate 'anyone'.", False),
            ('모두 왔어요.', 'Everyone came.', '모두 as a subject.', True),
        ],
    },
}
