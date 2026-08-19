#!/usr/bin/env python3
"""06 - Sentence patterns, in teaching order.

One pattern per day, in this sequence. The learner should be producing whole
sentences in week one, not week nine -- v1 put its sentence deck at position 09,
which leaves a beginner unable to say "I'm a student" for two months.

Everything here stays in 해요체 (polite informal). Speech levels are deliberately
not mixed in: teaching 반말 and 합쇼체 alongside it triples the conjugation load
for no communicative gain.

Korean is on the front. Recognition is the cheap direction and it is what you
want by default; the first few sentences of each pattern additionally get a
production card, because those are the ones worth being able to say cold.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.gloss import render
from korean.models import sentence_model

# (korean, english, gloss pairs)
P1 = ("p1-ideyo", "N이에요/예요 -- X is Y",
      "이에요 after a consonant, 예요 after a vowel. This is the copula; it attaches "
      "directly to the noun with no space.", [
    ("저는 학생이에요.", "I'm a student.", [("저는", "I"), ("학생이에요", "am a student")]),
    ("이건 물이에요.", "This is water.", [("이건", "this"), ("물이에요", "is water")]),
    ("제 이름은 민수예요.", "My name is Minsu.", [("제 이름은", "my name"), ("민수예요", "is Minsu")]),
    ("저는 미국 사람이에요.", "I'm American.", [("저는", "I"), ("미국 사람이에요", "am an American")]),
    ("이거 뭐예요?", "What is this?", [("이거", "this"), ("뭐예요", "is what")]),
    ("여기가 우리 집이에요.", "This is our house.", [("여기가", "here"), ("우리 집이에요", "is our house")]),
    ("그건 제 가방이에요.", "That's my bag.", [("그건", "that"), ("제 가방이에요", "is my bag")]),
    ("오늘은 월요일이에요.", "Today is Monday.", [("오늘은", "today"), ("월요일이에요", "is Monday")]),
])

P2 = ("p2-itda", "있어요 / 없어요 -- there is / I have",
      "One verb covers both existence and possession. The thing that exists takes 이/가.", [
    ("시간 있어요?", "Do you have time?", [("시간", "time"), ("있어요", "do you have")]),
    ("저는 동생이 있어요.", "I have a younger sibling.", [("저는", "I"), ("동생이", "a younger sibling"), ("있어요", "have")]),
    ("돈이 없어요.", "I don't have money.", [("돈이", "money"), ("없어요", "don't have")]),
    ("여기 화장실 있어요?", "Is there a bathroom here?", [("여기", "here"), ("화장실", "bathroom"), ("있어요", "is there")]),
    ("집에 아무도 없어요.", "Nobody is home.", [("집에", "at home"), ("아무도", "nobody"), ("없어요", "there isn't")]),
    ("질문 있어요.", "I have a question.", [("질문", "question"), ("있어요", "I have")]),
    ("자리 있어요?", "Is this seat free?", [("자리", "seat"), ("있어요", "is there")]),
    ("우유가 없어요.", "There's no milk.", [("우유가", "milk"), ("없어요", "there isn't")]),
])

P3 = ("p3-hada", "Noun + 하다 -- the easiest verbs in Korean",
      "Hundreds of verbs are just a noun plus 하다, and they all conjugate identically: 해요.", [
    ("뭐 해요?", "What are you doing?", [("뭐", "what"), ("해요", "are you doing")]),
    ("한국어를 공부해요.", "I study Korean.", [("한국어를", "Korean"), ("공부해요", "study")]),
    ("매일 운동해요.", "I exercise every day.", [("매일", "every day"), ("운동해요", "exercise")]),
    ("지금 일해요.", "I'm working now.", [("지금", "now"), ("일해요", "am working")]),
    ("친구랑 이야기해요.", "I'm talking with a friend.", [("친구랑", "with a friend"), ("이야기해요", "am talking")]),
    ("주말에 요리해요.", "I cook on weekends.", [("주말에", "on weekends"), ("요리해요", "cook")]),
    ("어제 청소했어요.", "I cleaned yesterday.", [("어제", "yesterday"), ("청소했어요", "cleaned")]),
    ("사랑해요.", "I love you.", [("사랑해요", "I love you")]),
])

P4 = ("p4-present", "아요 / 어요 -- the present tense",
      "Stem + 아요 if the last stem vowel is ㅏ or ㅗ, otherwise 어요. This one ending "
      "also covers the near future and habitual actions.", [
    ("밥을 먹어요.", "I eat.", [("밥을", "rice"), ("먹어요", "eat")]),
    ("학교에 가요.", "I go to school.", [("학교에", "to school"), ("가요", "go")]),
    ("커피를 마셔요.", "I drink coffee.", [("커피를", "coffee"), ("마셔요", "drink")]),
    ("책을 읽어요.", "I read a book.", [("책을", "a book"), ("읽어요", "read")]),
    ("음악을 들어요.", "I listen to music.", [("음악을", "music"), ("들어요", "listen to")]),
    ("서울에 살아요.", "I live in Seoul.", [("서울에", "in Seoul"), ("살아요", "live")]),
    ("영화를 봐요.", "I watch a movie.", [("영화를", "a movie"), ("봐요", "watch")]),
    ("한국어를 배워요.", "I'm learning Korean.", [("한국어를", "Korean"), ("배워요", "am learning")]),
])

P5 = ("p5-past", "았어요 / 었어요 -- the past tense",
      "Take the 해요 form, drop 요, add ㅆ어요. There is no second rule to learn.", [
    ("밥 먹었어요.", "I ate.", [("밥", "rice"), ("먹었어요", "ate")]),
    ("어제 학교에 갔어요.", "I went to school yesterday.", [("어제", "yesterday"), ("학교에", "to school"), ("갔어요", "went")]),
    ("친구를 만났어요.", "I met a friend.", [("친구를", "a friend"), ("만났어요", "met")]),
    ("영화를 봤어요.", "I watched a movie.", [("영화를", "a movie"), ("봤어요", "watched")]),
    ("뭐 했어요?", "What did you do?", [("뭐", "what"), ("했어요", "did you do")]),
    ("잘 잤어요?", "Did you sleep well?", [("잘", "well"), ("잤어요", "did you sleep")]),
    ("늦게 일어났어요.", "I woke up late.", [("늦게", "late"), ("일어났어요", "woke up")]),
    ("정말 재미있었어요.", "It was really fun.", [("정말", "really"), ("재미있었어요", "was fun")]),
])

P6 = ("p6-gosipeo", "-고 싶어요 -- I want to",
      "Attach 고 싶어요 straight to the verb stem. It only works for your own wants; "
      "for someone else you need -고 싶어해요.", [
    ("집에 가고 싶어요.", "I want to go home.", [("집에", "home"), ("가고 싶어요", "want to go")]),
    ("뭐 먹고 싶어요?", "What do you want to eat?", [("뭐", "what"), ("먹고 싶어요", "do you want to eat")]),
    ("한국에 가고 싶어요.", "I want to go to Korea.", [("한국에", "to Korea"), ("가고 싶어요", "want to go")]),
    ("좀 쉬고 싶어요.", "I want to rest a bit.", [("좀", "a bit"), ("쉬고 싶어요", "want to rest")]),
    ("한국어를 잘하고 싶어요.", "I want to be good at Korean.", [("한국어를", "Korean"), ("잘하고 싶어요", "want to be good at")]),
    ("물 마시고 싶어요.", "I want to drink water.", [("물", "water"), ("마시고 싶어요", "want to drink")]),
    ("아무것도 하고 싶지 않아요.", "I don't want to do anything.", [("아무것도", "anything"), ("하고 싶지 않아요", "don't want to do")]),
])

P7 = ("p7-future", "-(으)ㄹ 거예요 -- will, going to",
      "ㄹ 거예요 after a vowel, 을 거예요 after a consonant. Also used for a confident guess.", [
    ("내일 갈 거예요.", "I'll go tomorrow.", [("내일", "tomorrow"), ("갈 거예요", "will go")]),
    ("뭐 할 거예요?", "What are you going to do?", [("뭐", "what"), ("할 거예요", "are you going to do")]),
    ("집에 있을 거예요.", "I'll be at home.", [("집에", "at home"), ("있을 거예요", "will be")]),
    ("친구를 만날 거예요.", "I'm going to meet a friend.", [("친구를", "a friend"), ("만날 거예요", "am going to meet")]),
    ("아마 비가 올 거예요.", "It'll probably rain.", [("아마", "probably"), ("비가", "rain"), ("올 거예요", "will come")]),
    ("저녁을 먹을 거예요.", "I'm going to eat dinner.", [("저녁을", "dinner"), ("먹을 거예요", "am going to eat")]),
])

P8 = ("p8-sueisseo", "-(으)ㄹ 수 있어요 -- can, to be able to",
      "Literally 'there exists a way to ___'. Swap 있어요 for 없어요 to say you can't.", [
    ("한국어를 할 수 있어요.", "I can speak Korean.", [("한국어를", "Korean"), ("할 수 있어요", "can speak")]),
    ("지금은 갈 수 없어요.", "I can't go right now.", [("지금은", "right now"), ("갈 수 없어요", "can't go")]),
    ("운전할 수 있어요?", "Can you drive?", [("운전할 수 있어요", "can you drive")]),
    ("매운 거 먹을 수 있어요.", "I can eat spicy food.", [("매운 거", "spicy things"), ("먹을 수 있어요", "can eat")]),
    ("좀 도와줄 수 있어요?", "Could you help me a bit?", [("좀", "a bit"), ("도와줄 수 있어요", "can you help")]),
    ("여기서 사진 찍을 수 있어요?", "Can I take photos here?", [("여기서", "here"), ("사진", "photos"), ("찍을 수 있어요", "can I take")]),
])

PATTERNS = [P1, P2, P3, P4, P5, P6, P7, P8]

# The first N sentences of each pattern also get a production (EN->KR) card.
PRODUCE_FIRST = 3


def main():
    b = Build("06_sentence_patterns", "Korean v2::06 Sentence patterns")
    model = sentence_model()

    for tag, title, explanation, sentences in PATTERNS:
        for i, (korean, english, pairs) in enumerate(sentences):
            gloss_ko, gloss_en = render(pairs)
            note = explanation if i == 0 else ""
            b.add(
                model,
                [
                    korean,
                    english,
                    gloss_ko,
                    gloss_en,
                    ("<b>%s</b><br>%s" % (title, note)) if note else "",
                    b.audio(korean),
                    "y" if i < PRODUCE_FIRST else "",
                ],
                tags=["pattern", tag],
            )

    b.write()


if __name__ == "__main__":
    main()
