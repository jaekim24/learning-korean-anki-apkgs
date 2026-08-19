#!/usr/bin/env python3
"""04 - Particles, as fill-in-the-blank.

Particles cannot be learned as vocabulary. 은/는 vs 이/가 is not a definition you
memorize, it is a contrast that only resolves after seeing the slot empty in
many sentences and feeling which one belongs. So every card here blanks the
particle and puts the reason on the back.

The audio always speaks the complete sentence, so the ear hears the particle in
place even while the eye is guessing it.
"""

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from korean.build import Build
from korean.models import cloze_model

CLOZE_RE = re.compile(r"\{\{c\d+::(.*?)(?:::.*?)?\}\}")


def plain(text: str) -> str:
    """Strip cloze markup so TTS speaks the finished sentence."""
    return CLOZE_RE.sub(r"\1", text)


# (cloze text, english, why)
ITEMS = [
    # --- 은/는 vs 이/가: the hard one. Many contrasting examples, no definition. ---
    ("저{{c1::는}} 한국어를 배워요.", "I'm learning Korean.",
     "는 sets the topic: 'as for me...'. This is the default when you introduce yourself or your own situation."),
    ("이름{{c1::이}} 뭐예요?", "What's your name?",
     "이/가 marks the thing you are asking new information about. A question word answer never takes 은/는."),
    ("누{{c1::가}} 왔어요?", "Who came?",
     "누구 + 가 contracts to 누가. Question words take 이/가 because they are asking for brand-new information."),
    ("날씨{{c1::가}} 좋아요.", "The weather is nice.",
     "A fresh observation about something in front of you takes 이/가."),
    ("김치{{c1::는}} 맵지만 불고기{{c1::는}} 안 매워요.", "Kimchi is spicy, but bulgogi isn't.",
     "는 marks contrast. When you set two things against each other, both get 는."),
    ("제{{c1::가}} 할게요.", "I'll do it.",
     "가 here picks you out as specifically the one who will do it. 저는 할게요 would just be 'as for me, I'll do it'."),
    ("친구{{c1::가}} 전화했어요.", "A friend called.",
     "이/가 introduces someone into the conversation for the first time."),
    ("그 친구{{c1::는}} 지금 서울에 살아요.", "That friend now lives in Seoul.",
     "Once someone is already in the conversation, they become the topic and switch to 은/는."),
    ("고양이{{c1::가}} 있어요.", "There's a cat.",
     "있다/없다 take 이/가 for the thing that exists."),
    ("한국 음식{{c1::은}} 정말 맛있어요.", "Korean food is really delicious.",
     "은 after a consonant, 는 after a vowel. Here it frames the general topic being commented on."),

    # --- 을/를 object ---
    ("밥{{c1::을}} 먹어요.", "I eat rice.", "을 after a consonant. Marks the object being acted on."),
    ("커피{{c1::를}} 마셔요.", "I drink coffee.", "를 after a vowel. Marks the object being acted on."),
    ("책{{c1::을}} 읽었어요.", "I read a book.", "을 after a consonant (책)."),
    ("한국어{{c1::를}} 공부해요.", "I study Korean.", "를 after a vowel (어)."),
    ("영화{{c1::를}} 볼까요?", "Shall we watch a movie?", "를 after a vowel (화)."),

    # --- 에 vs 에서: the second hard one ---
    ("학교{{c1::에}} 가요.", "I'm going to school.",
     "에 marks a destination with a movement verb (가다, 오다)."),
    ("학교{{c1::에서}} 공부해요.", "I study at school.",
     "에서 marks where an action takes place. Studying happens there, so 에서, not 에."),
    ("집{{c1::에}} 있어요.", "I'm at home.",
     "있다/없다 take 에, not 에서 -- existing somewhere is not an action."),
    ("집{{c1::에서}} 밥을 먹어요.", "I eat at home.",
     "Eating is an action performed at that place, so 에서."),
    ("한국{{c1::에서}} 왔어요.", "I came from Korea.",
     "에서 also means 'from' -- the starting point of movement."),
    ("세 시{{c1::에}} 만나요.", "Let's meet at three.",
     "에 marks a point in time. Note: 오늘, 어제, 내일, 지금 take no particle at all."),
    ("주말{{c1::에}} 뭐 해요?", "What are you doing on the weekend?",
     "에 with a time expression."),

    # --- 도 / 만 ---
    ("저{{c1::도}} 갈래요.", "I want to go too.",
     "도 means 'also'. It replaces 은/는/이/가/을/를 -- you never stack them (never 저는도)."),
    ("이것{{c1::도}} 주세요.", "Give me this one too.", "도 replaces the object particle 을 here."),
    ("물{{c1::만}} 주세요.", "Just water, please.",
     "만 means 'only'. Like 도, it replaces the subject/object particle."),
    ("조금{{c1::만}} 주세요.", "Just a little, please.", "만 attaches to quantity words too."),

    # --- and / with ---
    ("빵{{c1::하고}} 우유 주세요.", "Bread and milk, please.",
     "하고 joins nouns in everyday speech. Works after both vowels and consonants."),
    ("친구{{c1::와}} 같이 갔어요.", "I went with a friend.",
     "와 after a vowel, 과 after a consonant. More formal / written than 하고."),
    ("선생님{{c1::과}} 이야기했어요.", "I talked with the teacher.",
     "과 after a consonant (님)."),

    # --- possessive ---
    ("이건 친구{{c1::의}} 책이에요.", "This is my friend's book.",
     "의 marks possession, and is usually pronounced 에. In casual speech it is often dropped: 친구 책."),

    # --- 로/으로 ---
    ("버스{{c1::로}} 가요.", "I go by bus.",
     "로 after a vowel or ㄹ; 으로 after any other consonant. Marks the means or method."),
    ("젓가락{{c1::으로}} 먹어요.", "I eat with chopsticks.",
     "으로 after a consonant (락). Marks the instrument."),
    ("오른쪽{{c1::으로}} 가세요.", "Go to the right.",
     "로/으로 also marks direction -- 'toward', as opposed to 에 which marks the endpoint."),
    ("한국어{{c1::로}} 말해 주세요.", "Please speak in Korean.",
     "로 after a vowel. Marks the medium or language used."),

    # --- 부터 / 까지 ---
    ("아홉 시{{c1::부터}} 여섯 시{{c2::까지}} 일해요.", "I work from nine to six.",
     "부터...까지 for a span of time: from X until Y."),
    ("서울{{c1::에서}} 부산{{c2::까지}} 세 시간 걸려요.", "It takes three hours from Seoul to Busan.",
     "For places it is 에서...까지, not 부터...까지. 부터 is for time."),

    # --- to a person ---
    ("친구{{c1::한테}} 전화했어요.", "I called my friend.",
     "한테 marks the person receiving something. Everyday spoken form."),
    ("친구{{c1::에게}} 선물을 줬어요.", "I gave my friend a present.",
     "에게 is the written / slightly formal equivalent of 한테."),
    ("선생님{{c1::께}} 드렸어요.", "I gave it to the teacher.",
     "께 is the honorific form, used with 드리다 for someone you are respecting."),

    # --- comparison and likeness ---
    ("오늘이 어제{{c1::보다}} 더워요.", "Today is hotter than yesterday.",
     "보다 marks the thing being compared against -- it attaches to the *standard*, not the winner."),
    ("한국 사람{{c1::처럼}} 말해요.", "You speak like a Korean.",
     "처럼 means 'like, as'."),
    ("날{{c1::마다}} 운동해요.", "I exercise every day.",
     "마다 means 'every'. 날마다 = every day."),

    # --- topic vs subject, one last contrast pair ---
    ("코끼리{{c1::는}} 코{{c2::가}} 길어요.", "Elephants have long trunks.",
     "The classic double-marking sentence: 는 sets the overall topic (elephants), 가 marks what specifically is long (the trunk)."),
]


def main():
    b = Build("04_particles_cloze", "Korean v2::04 Particles (cloze)")
    model = cloze_model()

    for text, english, why in ITEMS:
        b.add(model, [text, english, why, b.audio(plain(text))], tags=["particle"])

    b.write()


if __name__ == "__main__":
    main()
