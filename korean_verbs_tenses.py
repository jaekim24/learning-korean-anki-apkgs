#!/usr/bin/env python3
"""
Korean Verb Conjugation - Past & Future Tense

Learn past and future tense conjugations for common Korean verbs.
Usage: python3 korean_verbs_tenses.py
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
DECK_ID = DECK_IDS["verbs_tenses"]
MODEL_ID = MODEL_IDS["grammar"]


# Past Tense Verbs: (dictionary_form, past_polite, past_casual, meaning, word_pairs)
PAST_VERBS = [
    # Regular past tense (았/었)
    ("가다", "갔어요", "갔어", "Went", [("가다", "to go"), ("갔어요", "went")]),
    ("오다", "왔어요", "왔어", "Came", [("오다", "to come"), ("왔어요", "came")]),
    ("보다", "봤어요", "봤어", "Saw / Watched", [("보다", "to see"), ("봤어요", "saw/watched")]),
    ("먹다", "먹었어요", "먹었어", "Ate", [("먹다", "to eat"), ("먹었어요", "ate")]),
    ("마시다", "마셨어요", "마셨어", "Drank", [("마시다", "to drink"), ("마셨어요", "drank")]),
    ("자다", "잤어요", "잤어", "Slept", [("자다", "to sleep"), ("잤어요", "slept")]),
    ("일어나다", "일어났어요", "일어났어", "Woke up", [("일어나다", "to wake up"), ("일어났어요", "woke up")]),
    ("앉다", "앉았어요", "앉았어", "Sat", [("앉다", "to sit"), ("앉았어요", "sat")]),
    ("서다", "섰어요", "섰어", "Stood", [("서다", "to stand"), ("섰어요", "stood")]),
    ("만나다", "만났어요", "만났어", "Met", [("만나다", "to meet"), ("만났어요", "met")]),
    ("사다", "샀어요", "샀어", "Bought", [("사다", "to buy"), ("샀어요", "bought")]),
    ("팔다", "팔았어요", "팔았어", "Sold", [("팔다", "to sell"), ("팔았어요", "sold")]),
    ("주다", "줬어요", "줬어", "Gave", [("주다", "to give"), ("줬어요", "gave")]),
    ("받다", "받았어요", "받았어", "Received", [("받다", "to receive"), ("받았어요", "received")]),
    ("찾다", "찾았어요", "찾았어", "Found", [("찾다", "to find"), ("찾았어요", "found")]),
    ("잃다", "잃었어요", "잃었어", "Lost", [("잃다", "to lose"), ("잃었어요", "lost")]),
    ("배우다", "배웠어요", "배웠어", "Learned", [("배우다", "to learn"), ("배웠어요", "learned")]),
    ("가르치다", "가르쳤어요", "가르쳤어", "Taught", [("가르치다", "to teach"), ("가르쳤어요", "taught")]),
    ("읽다", "읽었어요", "읽었어", "Read", [("읽다", "to read"), ("읽었어요", "read")]),
    ("쓰다", "썼어요", "썼어", "Wrote / Used", [("쓰다", "to write/use"), ("썼어요", "wrote/used")]),
    ("듣다", "들었어요", "들었어", "Heard / Listened", [("듣다", "to hear"), ("들었어요", "heard/listened")]),
    ("말하다", "말했어요", "말했어", "Spoke / Said", [("말하다", "to speak"), ("말했어요", "spoke/said")]),
    ("운동하다", "운동했어요", "운동했어", "Exercised", [("운동하다", "to exercise"), ("운동했어요", "exercised")]),
    ("공부하다", "공부했어요", "공부했어", "Studied", [("공부하다", "to study"), ("공부했어요", "studied")]),
    ("일하다", "일했어요", "일했어", "Worked", [("일하다", "to work"), ("일했어요", "worked")]),
    ("요리하다", "요리했어요", "요리했어", "Cooked", [("요리하다", "to cook"), ("요리했어요", "cooked")]),
    ("청소하다", "청소했어요", "청소했어", "Cleaned", [("청소하다", "to clean"), ("청소했어요", "cleaned")]),
    ("전화하다", "전화했어요", "전화했어", "Called", [("전화하다", "to call"), ("전화했어요", "called")]),
    ("사랑하다", "사랑했어요", "사랑했어", "Loved", [("사랑하다", "to love"), ("사랑했어요", "loved")]),
    ("좋아하다", "좋아했어요", "좋아했어", "Liked", [("좋아하다", "to like"), ("좋아했어요", "liked")]),
    ("싫어하다", "싫어했어요", "싫어했어", "Disliked", [("싫어하다", "to dislike"), ("싫어했어요", "disliked")]),
    ("행복하다", "행복했어요", "행복했어", "Was happy", [("행복하다", "to be happy"), ("행복했어요", "was happy")]),
    ("슬프다", "슬펐어요", "슬펐어", "Was sad", [("슬프다", "to be sad"), ("슬펐어요", "was sad")]),
    ("기쁘다", "기뻤어요", "기뻤어", "Was glad", [("기쁘다", "to be glad"), ("기뻤어요", "was glad")]),
    ("무섭다", "무서웠어요", "무서웠어", "Was scary", [("무섭다", "to be scary"), ("무서웠어요", "was scary")]),
    ("재미있다", "재미있었어요", "재미있었어", "Was fun", [("재미있다", "to be fun"), ("재미있었어요", "was fun")]),
    ("맛있다", "맛있었어요", "맛있었어", "Was delicious", [("맛있다", "to be delicious"), ("맛있었어요", "was delicious")]),
    ("컸다", "컸어요", "컸어", "Was big (크다)", [("크다", "to be big"), ("컸어요", "was big")]),
    ("작았다", "작았어요", "작았어", "Was small (작다)", [("작다", "to be small"), ("작았어요", "was small")]),
    ("좋았다", "좋았어요", "좋았어", "Was good (좋다)", [("좋다", "to be good"), ("좋았어요", "was good")]),
    ("나빴다", "나빴어요", "나빴어", "Was bad (나쁘다)", [("나쁘다", "to be bad"), ("나빴어요", "was bad")]),
    ("많았다", "많았어요", "많았어", "Was many (많다)", [("많다", "to be many"), ("많았어요", "was many")]),
    ("적었다", "적었어요", "적었어", "Was few (적다)", [("적다", "to be few"), ("적었어요", "was few")]),
    ("덥다", "더웠어요", "더웠어", "Was hot (덥다)", [("덥다", "to be hot"), ("더웠어요", "was hot")]),
    ("춥다", "추웠어요", "추웠어", "Was cold (춥다)", [("춥다", "to be cold"), ("추웠어요", "was cold")]),
    ("즐거웠다", "즈거웠어요", "즐거웠어", "Was enjoyable (즐겁다)", [("즐겁다", "to be enjoyable"), ("즐거웠어요", "was enjoyable")]),
    ("아팠다", "아팠어요", "아팠어", "Was sick/hurt (아프다)", [("아프다", "to hurt/be sick"), ("아팠어요", "hurt/was sick")]),
    ("바빴다", "바빴어요", "바빴어", "Was busy (바쁘다)", [("바쁘다", "to be busy"), ("바빴어요", "was busy")]),
    ("괜찮았다", "괜찮았어요", "괜찮았어", "Was okay (괜찮다)", [("괜찮다", "to be okay"), ("괜찮았어요", "was okay")]),
    ("쉬웠다", "쉬웠어요", "쉬웠어", "Was easy (쉽다)", [("쉽다", "to be easy"), ("쉬웠어요", "was easy")]),
    ("어려웠다", "어려웠어요", "어려웠어", "Was difficult (어렵다)", [("어렵다", "to be difficult"), ("어려웠어요", "was difficult")]),
    ("예뻤다", "예뻤어요", "예뻤어", "Was pretty (예쁘다)", [("예쁘다", "to be pretty"), ("예뻤어요", "was pretty")]),
    ("까다", "까웠어요", "까웠어", "Was spicy (맵다 - 까 appears)", [("맵다", "to be spicy"), ("까웠어요", "was spicy")]),
    ("달콤했다", "달콤했어요", "달콤했어", "Was sweet (달콤하다)", [("달콤하다", "to be sweet"), ("달콤했어요", "was sweet")]),
    ("따뜻했다", "따뜻했어요", "따뜻했어", "Was warm (따뜻하다)", [("따뜻하다", "to be warm"), ("따뜻했어요", "was warm")]),
    ("시원했다", "시원했어요", "시원했어", "Was cool/refreshing (시원하다)", [("시원하다", "to be cool"), ("시원했어요", "was cool")]),
    ("늦었다", "늦었어요", "늦었어", "Was late (늦다)", [("늦다", "to be late"), ("늦었어요", "was late")]),
    ("일찍 일어났다", "일찍 일어났어요", "일찍 일어났어", "Woke up early", [("일찍", "early"), ("일어났어요", "woke up")]),
    ("늦게 잤다", "늦게 잤어요", "늦게 잤어", "Slept late", [("늦게", "late"), ("잤어요", "slept")]),
    ("쉬었다", "쉬었어요", "쉬었어", "Rested (쉬다)", [("쉬다", "to rest"), ("쉬었어요", "rested")]),
    ("쉬웠다", "쉬웠어요", "쉬웠어", "Was easy (쉽다)", [("쉽다", "to be easy"), ("쉬웠어요", "was easy")]),
    ("했다", "했어요", "했어", "Did (하다)", [("하다", "to do"), ("했어요", "did")]),
    ("됐다", "됐어요", "됐어", "Became (되다)", [("되다", "to become"), ("됐어요", "became")]),
]

# Future / Intention Verbs: (dictionary_form, future_form, future_casual, meaning, word_pairs)
FUTURE_VERBS = [
    # Using 겠다 (intention/probability)
    ("가다", "가겠어요", "가겠어", "Will go / Intend to go", [("가다", "to go"), ("가겠어요", "will go")]),
    ("오다", "오겠어요", "오겠어", "Will come", [("오다", "to come"), ("오겠어요", "will come")]),
    ("보다", "보겠어요", "보겠어", "Will see / watch", [("보다", "to see"), ("보겠어요", "will see")]),
    ("먹다", "먹겠어요", "먹겠어", "Will eat", [("먹다", "to eat"), ("먹겠어요", "will eat")]),
    ("마시다", "마시겠어요", "마시겠어", "Will drink", [("마시다", "to drink"), ("마시겠어요", "will drink")]),
    ("자다", "자겠어요", "자겠어", "Will sleep", [("자다", "to sleep"), ("자겠어요", "will sleep")]),
    ("만나다", "만나겠어요", "만나겠어", "Will meet", [("만나다", "to meet"), ("만나겠어요", "will meet")]),
    ("사다", "사겠어요", "사겠어", "Will buy", [("사다", "to buy"), ("사겠어요", "will buy")]),
    ("하다", "하겠어요", "하겠어", "Will do", [("하다", "to do"), ("하겠어요", "will do")]),
    ("공부하다", "공부하겠어요", "공부하겠어", "Will study", [("공부하다", "to study"), ("공부하겠어요", "will study")]),
    ("일하다", "일하겠어요", "일하겠어", "Will work", [("일하다", "to work"), ("일하겠어요", "will work")]),
    ("전화하다", "전화하겠어요", "전화하겠어", "Will call", [("전화하다", "to call"), ("전화하겠어요", "will call")]),

    # Using 을 거예요 (future/probable)
    ("가다", "갈 거예요", "갈 거야", "Going to go / Will go", [("가다", "to go"), ("갈 거예요", "going to go")]),
    ("오다", "올 거예요", "올 거야", "Will come", [("오다", "to come"), ("올 거예요", "will come")]),
    ("보다", "볼 거예요", "볼 거야", "Will see", [("보다", "to see"), ("볼 거예요", "will see")]),
    ("먹다", "먹을 거예요", "먹을 거야", "Will eat", [("먹다", "to eat"), ("먹을 거예요", "will eat")]),
    ("마시다", "마실 거예요", "마실 거야", "Will drink", [("마시다", "to drink"), ("마실 거예요", "will drink")]),
    ("자다", "잘 거예요", "잘 거야", "Will sleep", [("자다", "to sleep"), ("잘 거예요", "will sleep")]),
    ("읽다", "읽을 거예요", "읽을 거야", "Will read", [("읽다", "to read"), ("읽을 거예요", "will read")]),
    ("쓰다", "쓸 거예요", "쓸 거야", "Will write / use", [("쓰다", "to write"), ("쓸 거예요", "will write")]),
    ("듣다", "들을 거예요", "들을 거야", "Will hear", [("듣다", "to hear"), ("들을 거예요", "will hear")]),
    ("만나다", "만날 거예요", "만날 거야", "Will meet", [("만나다", "to meet"), ("만날 거예요", "will meet")]),
    ("사다", "살 거예요", "살 거야", "Will buy", [("사다", "to buy"), ("살 거예요", "will buy")]),
    ("팔다", "팔 거예요", "팔 거야", "Will sell", [("팔다", "to sell"), ("팔 거예요", "will sell")]),
    ("찾다", "찾을 거예요", "찾을 거야", "Will find", [("찾다", "to find"), ("찾을 거예요", "will find")]),
    ("잃다", "잃을 거예요", "잃을 거야", "Will lose", [("잃다", "to lose"), ("잃을 거예요", "will lose")]),
    ("배우다", "배울 거예요", "배울 거야", "Will learn", [("배우다", "to learn"), ("배울 거예요", "will learn")]),
    ("가르치다", "가르칠 거예요", "가르칠 거야", "Will teach", [("가르치다", "to teach"), ("가르칠 거예요", "will teach")]),
    ("하다", "할 거예요", "할 거야", "Will do", [("하다", "to do"), ("할 거예요", "will do")]),
    ("공부하다", "공부할 거예요", "공부할 거야", "Will study", [("공부하다", "to study"), ("공부할 거예요", "will study")]),
    ("일하다", "일할 거예요", "일할 거야", "Will work", [("일하다", "to work"), ("일할 거예요", "will work")]),
    ("요리하다", "요리할 거예요", "요리할 거야", "Will cook", [("요리하다", "to cook"), ("요리할 거예요", "will cook")]),
    ("청소하다", "청소할 거예요", "청소할 거야", "Will clean", [("청소하다", "to clean"), ("청소할 거예요", "will clean")]),
    ("전화하다", "전화할 거예요", "전화할 거야", "Will call", [("전화하다", "to call"), ("전화할 거예요", "will call")]),
    ("사랑하다", "사랑할 거예요", "사랑할 거야", "Will love", [("사랑하다", "to love"), ("사랑할 거예요", "will love")]),
    ("좋아하다", "좋아할 거예요", "좋아할 거야", "Will like", [("좋아하다", "to like"), ("좋아할 거예요", "will like")]),
    ("싫어하다", "싫어할 거예요", "싫어할 거야", "Will dislike", [("싫어하다", "to dislike"), ("싫어할 거예요", "will dislike")]),
    ("살다", "살 거예요", "살 거야", "Will live", [("살다", "to live"), ("살 거예요", "will live")]),
    ("죽다", "죽을 거예요", "죽을 거야", "Will die", [("죽다", "to die"), ("죽을 거예요", "will die")]),
    ("열다", "열 거예요", "열 거야", "Will open", [("열다", "to open"), ("열 거예요", "will open")]),
    ("닫다", "닫을 거예요", "닫을 거야", "Will close", [("닫다", "to close"), ("닫을 거예요", "will close")]),
    ("입다", "입을 거예요", "입을 거야", "Will wear (clothes)", [("입다", "to wear"), ("입을 거예요", "will wear")]),
    ("벗다", "벗을 거예요", "벗을 거야", "Will take off", [("벗다", "to take off"), ("벗을 거예요", "will take off")]),
    ("씻다", "씻을 거예요", "씻을 거야", "Will wash", [("씻다", "to wash"), ("씻을 거예요", "will wash")]),
    ("앉다", "앉을 거예요", "앉을 거야", "Will sit", [("앉다", "to sit"), ("앉을 거예요", "will sit")]),
    ("서다", "설 거예요", "설 거야", "Will stand", [("서다", "to stand"), ("설 거예요", "will stand")]),
    ("기다리다", "기다릴 거예요", "기다릴 거야", "Will wait", [("기다리다", "to wait"), ("기다릴 거예요", "will wait")]),
    ("웃다", "웃을 거예요", "웃을 거야", "Will laugh", [("웃다", "to laugh"), ("웃을 거예요", "will laugh")]),
    ("울다", "울 거예요", "울 거야", "Will cry", [("울다", "to cry"), ("울 거예요", "will cry")]),
]

# Using 려고 하다 (intend to / plan to): (form, meaning, example, word_pairs)
INTENTION_VERBS = [
    ("가려고 하다", "Planned/Intending to go", "가려고 해요", [("가려고", "planning to"), ("해요", "doing")]),
    ("오려고 하다", "Planned/Intending to come", "오려고 해요", [("오려고", "planning to"), ("해요", "doing")]),
    ("보려고 하다", "Planned/Intending to see", "보려고 해요", [("보려고", "planning to"), ("해요", "doing")]),
    ("먹으려고 하다", "Planned/Intending to eat", "먹으려고 해요", [("먹으려고", "planning to"), ("해요", "doing")]),
    ("마시려고 하다", "Planned/Intending to drink", "마시려고 해요", [("마시려고", "planning to"), ("해요", "doing")]),
    ("자려고 하다", "Planned/Intending to sleep", "자려고 해요", [("자려고", "planning to"), ("해요", "doing")]),
    ("만나려고 하다", "Planned/Intending to meet", "만나려고 해요", [("만나려고", "planning to"), ("해요", "doing")]),
    ("사려고 하다", "Planned/Intending to buy", "사려고 해요", [("사려고", "planning to"), ("해요", "doing")]),
    ("하려고 하다", "Planned/Intending to do", "하려고 해요", [("하려고", "planning to"), ("해요", "doing")]),
    ("공부하려고 하다", "Planned/Intending to study", "공부하려고 해요", [("공부하려고", "planning to"), ("해요", "doing")]),
    ("일하려고 하다", "Planned/Intending to work", "일하려고 해요", [("일하려고", "planning to"), ("해요", "doing")]),
    ("배우려고 하다", "Planned/Intending to learn", "배우려고 해요", [("배우려고", "planning to"), ("해요", "doing")]),
    ("가르치려고 하다", "Planned/Intending to teach", "가르치려고 해요", [("가르치려고", "planning to"), ("해요", "doing")]),
    ("읽으려고 하다", "Planned/Intending to read", "읽으려고 해요", [("읽으려고", "planning to"), ("해요", "doing")]),
    ("쓰려고 하다", "Planned/Intending to write", "쓰려고 해요", [("쓰려고", "planning to"), ("해요", "doing")]),
]

# Using 것 같다 (seems like / probably): (form, meaning, example, word_pairs)
PROBABILITY_VERBS = [
    ("갈 것 같다", "Probably going / Seems like going", "갈 것 같아요", [("갈 것", "going"), ("같아요", "seems like")]),
    ("올 것 같다", "Probably coming / Seems like coming", "올 것 같아요", [("올 것", "coming"), ("같아요", "seems like")]),
    ("올 것 같다", "Probably coming", "올 것 같아요", [("올 것", "coming"), ("같아요", "seems like")]),
    ("왔을 것 같다", "Probably came", "왔을 것 같아요", [("왔을 것", "came"), ("같아요", "seems like")]),
    ("먹을 것 같다", "Probably eating / Seems like eating", "먹을 것 같아요", [("먹을 것", "eating"), ("같아요", "seems like")]),
    ("좋을 것 같다", "Probably good / Seems good", "좋을 것 같아요", [("좋을 것", "good"), ("같아요", "seems like")]),
    ("재미있을 것 같다", "Probably fun / Seems fun", "재미있을 것 같아요", [("재미있을 것", "fun"), ("같아요", "seems like")]),
    ("어려울 것 같다", "Probably difficult / Seems difficult", "어려울 것 같아요", [("어려울 것", "difficult"), ("같아요", "seems like")]),
    ("쉬울 것 같다", "Probably easy / Seems easy", "쉬울 것 같아요", [("쉬울 것", "easy"), ("같아요", "seems like")]),
    ("비올 것 같다", "Probably raining / Looks like rain", "비올 것 같아요", [("비올 것", "raining"), ("같아요", "seems like")]),
]


def create_model():
    """Create card model for tense conjugations."""
    return genanki.Model(
        MODEL_ID,
        "Korean Verb Tense Model",
        fields=[
            {"name": "Tense"},
            {"name": "DictionaryForm"},
            {"name": "ConjugatedForm"},
            {"name": "CasualForm"},
            {"name": "Meaning"},
            {"name": "Notes"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Verb Tense Card",
                "qfmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">{{Tense}}</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 25px;">
    {{DictionaryForm}}
</div>
{{#Notes}}
<div style="text-align: center; font-size: 14px; color: #888; font-style: italic;">
    {{Notes}}
</div>
{{/Notes}}
                """,
                "afmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">{{Tense}}</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 25px;">
    {{DictionaryForm}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
{{#Notes}}
<div style="text-align: center; font-size: 13px; color: #888; font-style: italic;">
    {{Notes}}
</div>
{{/Notes}}
<hr style="margin: 12px 0;">
<div style="text-align: center; font-size: 40px; color: #2196F3; font-weight: bold; padding: 15px;">
    {{ConjugatedForm}}
</div>
<div style="text-align: center; font-size: 20px; color: #666; padding: 8px;">
    {{CasualForm}}
</div>
<div style="text-align: center; font-size: 22px; padding: 10px;">
    {{Meaning}}
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


def generate_deck(output_file="decks/08_korean_verbs_tenses.apkg"):
    """Generate the past & future tense verbs deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "08. Korean Verbs Tenses - 시제")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        # Add past tense verbs
        for entry in PAST_VERBS:
            if len(entry) == 5:
                dict_form, polite, casual, meaning, word_pairs = entry
            else:
                dict_form, polite, casual, meaning = entry
                word_pairs = []

            audio_filename = generate_audio(polite, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            note = genanki.Note(
                model=model,
                fields=["Past Tense", dict_form, polite, casual, meaning, "", korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Add future/probability verbs
        for entry in FUTURE_VERBS:
            if len(entry) == 5:
                dict_form, polite, casual, meaning, word_pairs = entry
            else:
                dict_form, polite, casual, meaning = entry
                word_pairs = []

            audio_filename = generate_audio(polite, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            note = genanki.Note(
                model=model,
                fields=["Future Tense (을 거예요)", dict_form, polite, casual, meaning, "", korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Add intention verbs
        for entry in INTENTION_VERBS:
            if len(entry) == 4:
                form, meaning, example, word_pairs = entry
            else:
                form, meaning, example = entry
                word_pairs = []

            audio_filename = generate_audio(example, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            note = genanki.Note(
                model=model,
                fields=["Intention (려고 하다)", form, example, example.split()[0] + "해", meaning,
                        "Intend to / Planning to", korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Add probability verbs
        for entry in PROBABILITY_VERBS:
            if len(entry) == 4:
                form, meaning, example, word_pairs = entry
            else:
                form, meaning, example = entry
                word_pairs = []

            audio_filename = generate_audio(example, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            # Generate colored HTML from word_pairs
            korean_colored, english_colored = create_colored_html(word_pairs) if word_pairs else ("", "")

            note = genanki.Note(
                model=model,
                fields=["Probability (것 같다)", form, example, example.replace("요", ""), meaning,
                        "Seems like / Probably", korean_colored, english_colored, audio_field],
            )
            deck.add_note(note)

        # Generate the package with media files
        package = genanki.Package(deck)

        if created_audio_files:
            package.media_files = created_audio_files

        # Write the package
        output_path = os.path.join(os.getcwd(), output_file)
        package.write_to_file(output_path)

        total = len(PAST_VERBS) + len(FUTURE_VERBS) + len(INTENTION_VERBS) + len(PROBABILITY_VERBS)
        print(f"✓ Deck created: {output_file}")
        print(f"  - {len(PAST_VERBS)} past tense cards")
        print(f"  - {len(FUTURE_VERBS)} future tense cards")
        print(f"  - {len(INTENTION_VERBS)} intention cards")
        print(f"  - {len(PROBABILITY_VERBS)} probability cards")
        print(f"  - Total: {total} cards")
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
