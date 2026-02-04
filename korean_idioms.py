#!/usr/bin/env python3
"""
Korean Common Idioms & Expressions

Natural expressions for everyday conversations.
Usage: python3 korean_idioms.py
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
DECK_ID = DECK_IDS["idioms"]
MODEL_ID = MODEL_IDS["word"]


# Expressions: (korean, english, romanization, situation, usage_notes, word_pairs)
# word_pairs: List of (korean_word, english_word) tuples for color-coded alignment
EXPRESSIONS = [
    # ===== GREETINGS BEYOND BASICS =====
    ("안녕하신가요?", "Hello? (on phone)", "annyeonghasinkka?",
     "Answering phone",
     "Used when answering the phone",
     [("안녕하신가요", "Hello?")]),
    ("여보세요", "Hello? (phone)", "yeoboseyo",
     "Answering phone / Calling for attention",
     "Used when answering phone or getting someone's attention",
     [("여보세요", "Hello?")]),
    ("오래간만이에요", "Long time no see", "oraeganmanieyo",
     "Meeting someone after a long time",
     "Used when you haven't seen someone in a while",
     [("오래", "Long"), ("간만", "time"), ("이에요", "no see")]),
    ("그동안 잘 지내셨어요?", "Have you been well?", "geudongan jal jinaesyeosseoyo?",
     "Asking about well-being after time apart",
     "Asking how someone has been during your time apart",
     [("그동안", "during that time"), ("잘", "well"), ("지내셨어요", "have you been")]),
    ("별일 없으셨죠?", "Nothing happened, right?", "byeolireopseusyeotjyo?",
     "Small talk about time apart",
     "Hoping nothing bad happened while apart",
     [("별일", "nothing special"), ("없으셨죠", "didn't happen")]),

    # ===== THANKS & RESPONSES =====
    ("천만에요", "Not at all / You're welcome", "cheonmaneyo",
     "Responding to thanks (humble)",
     "Humble 'not at all' response to thanks",
     [("천만", "ten million"), ("에요", "not at all")]),
    ("별말씀을요", "You're flattering me", "byeolmalsseumeulyo",
     "Responding to compliment",
     "Used when someone praises you excessively",
     [("별말씀", "such words"), ("을요", "you're flattering")]),
    ("아니에요", "No / Not at all", "anieyo",
     "Humble denial",
     "Modest response to thanks or praise",
     [("아니", "no"), ("에요", "not at all")]),
    ("고맙습니다", "Thank you", "gomapseumnida",
     "Standard thanks",
     "Polite way to say thank you",
     [("고맙", "grateful"), ("습니다", "thank you")]),
    ("감사합니다", "Thank you (formal)", "gamsahamnida",
     "Formal thanks",
     "More formal thank you",
     [("감사", "gratitude"), ("합니다", "thank you")]),
    ("정말 감사드려요", "Thank you so much", "jeongmal gamsadeuryeo",
     "Very grateful",
     "Expressing deep gratitude",
     [("정말", "really"), ("감사", "thank"), ("드려요", "give")]),
    ("신경 써줘서 고마워요", "Thanks for caring", "singyeong sseojjwoseo gomawoyo",
     "Thanking someone for their concern",
     "Appreciating someone's thoughtfulness",
     [("신경", "concern"), ("써줘서", "for caring"), ("고마워요", "thank you")]),

    # ===== APOLOGIES & RESPONSES =====
    ("죄송합니다", "I'm sorry (formal)", "joesonghamnida",
     "Formal apology",
     "Used in formal situations or with strangers",
     [("죄송", "sorry"), ("합니다", "formal")]),
    ("미안합니다", "I'm sorry", "mianhamnida",
     "Standard apology",
     "Common way to say sorry",
     [("미안", "sorry"), ("합니다", "I am")]),
    ("미안해요", "Sorry (polite)", "mianhaeyo",
     "Polite apology",
     "Used with people you know",
     [("미안", "sorry"), ("해요", "am")]),
    ("정말 죄송해요", "Really sorry", "jeongmal joesonghaeyo",
     "Emphasized apology",
     "When you're truly sorry",
     [("정말", "really"), ("죄송", "sorry"), ("해요", "am")]),
    ("괜찮아요", "It's okay / No problem", "gwaenchanaeyo",
     "Accepting apology",
     "Forgiving someone",
     [("괜찮", "okay"), ("아요", "it is")]),
    ("별문제예요", "No problem at all", "byeolmunjeyeyo",
     "Strong reassurance",
     "It's really no problem",
     [("별", "no"), ("문제", "problem"), ("예요", "at all")]),
    ("신경 쓰지 마세요", "Don't worry about it", "singyeong sseuji maseyo",
     "Don't be concerned",
     "Telling someone not to feel bad",
     [("신경", "concern"), ("쓰지", "don't use"), ("마세요", "please")]),

    # ===== COMMON REACTIONS =====
    ("진짜?", "Really?", "jinjja?",
     "Expressing surprise/interest",
     "Asking if something is true",
     [("진짜", "really")]),
    ("정말?", "Really?", "jeongmal?",
     "Expressing surprise",
     "Can't believe something",
     [("정말", "really")]),
    ("설마?", "No way / You don't say", "seolma?",
     "Disbelief",
     "Hoping something isn't true",
     [("설마", "no way")]),
    ("대박", "Awesome / Crazy", "daebak",
     "Strong reaction",
     "Something amazing or shocking",
     [("대박", "awesome")]),
    ("헐", "Whoa / Oh my", "heol",
     "Surprise",
     "Expression of shock or disbelief",
     [("헐", "whoa")]),
    ("와", "Wow", "wa",
     "Amazement",
     "Impressed by something",
     [("와", "wow")]),
    ("우와", "Ooh/Wow", "uwa",
     "Amazement",
     "Impressed reaction",
     [("우와", "ooh")]),
    ("억소리가 없다", "Speechless", "eoksolliga eopda",
     "Can't believe it",
     "Too surprised to speak",
     [("억소리", "speechless"), ("가", "is"), ("없다", "no")]),
    ("뭐라고?", "What did you say?", "mworago?",
     "Didn't hear / Disbelief",
     "Asking for repetition or expressing disbelief",
     [("뭐", "what"), ("라고", "did you say")]),

    # ===== AGREEMENT & UNDERSTANDING =====
    ("그렇구나", "I see / That's right", "geureokuna",
     "Realization",
     "Understanding something new",
     [("그렇", "so"), ("구나", "I see")]),
    ("그렇군요", "I see", "geureokunnyo",
     "Understanding",
     "Polite realization",
     [("그렇", "so"), ("군요", "I see")]),
    ("알겠습니다", "I understand", "algesseumnida",
     "Acknowledgment",
     "Showing you understood instructions",
     [("알", "know"), ("겠", "will"), ("습니다", "I")]),
    ("알겠어요", "Got it / Understand", "algesseoyo",
     "Acknowledgment",
     "Polite understanding",
     [("알", "know"), ("겠", "will"), ("어요", "I")]),
    ("그렇지요", "That's right", "geureojiyo",
     "Agreement",
     "Agreeing with someone",
     [("그렇", "so"), ("지요", "right")]),
    ("맞아요", "That's right / Correct", "majayo",
     "Agreement",
     "Confirming something is correct",
     [("맞", "correct"), ("아요", "it is")]),
    ("투명", "Exactly", "yumyeong",
     "Strong agreement",
     "You're absolutely right (slang)",
     [("투명", "exactly")]),
    ("당연하지", "Of course", "dangyeonhaji",
     "Obviously",
     "Something should be clear",
     [("당연", "natural"), ("하지", "of course")]),
    ("물론이지요", "Of course", "mullonijiyo",
     "Naturally",
     "No doubt about it",
     [("물론", "of course"), ("이지요", "it is")]),

    # ===== THINKING & CONSIDERING =====
    ("글쎄요", "Well / Hmm", "geulsseyo",
     "Hesitation",
     "Thinking about answer",
     [("글쎄", "well"), ("요", "hmm")]),
    ("음", "Hmm", "eum",
     "Thinking sound",
     "Considering something",
     [("음", "hmm")]),
    ("잠깐만요", "Just a moment", "jamkkanmanyo",
     "Asking to wait",
     "Need a moment to think or do something",
     [("잠깐", "moment"), ("만", "just"), ("요", "please")]),
    ("잠시만요", "Wait a moment", "jamsimanyo",
     "Polite wait request",
     "Asking someone to wait briefly",
     [("잠시", "a moment"), ("만", "just"), ("요", "please")]),
    ("잠깐만 기다려주세요", "Please wait a moment", "jamkkan gidaryeojuseyo",
     "Polite wait",
     "Asking for patience",
     [("잠깐", "moment"), ("만", "just"), ("기다려", "wait"), ("주세요", "please")]),
    ("생각해 볼게요", "Let me think about it", "saenggakhaebolgeyo",
     "Need to consider",
     "Will think before deciding",
     [("생각", "think"), ("해", "do"), ("볼게요", "will")]),
    ("좀 생각해보게요", "Let me think for a bit", "jom saenggakhabokeyo",
     "Need time",
     "Need more time to consider",
     [("좀", "a bit"), ("생각", "think"), ("해보게요", "will try")]),

    # ===== LEAVING =====
    ("먼저 가요", "I'm going first / Leaving now", "meonjeo gayo",
     "Leaving before others",
     "Leaving when others are staying",
     [("먼저", "first"), ("가요", "go")]),
    ("먼저 일어날게요", "I'll get going", "meonjeo ireonageyo",
     "Leaving",
     "Time to leave",
     [("먼저", "first"), ("일어날게요", "will get up")]),
    ("가야 해요", "I have to go", "gayahaeyo",
     "Need to leave",
     "Must go now",
     [("가야", "must go"), ("해요", "have to")]),
    ("이만 갈게요", "I'll go now", "iman galgeyo",
     "Leaving",
     "Casual goodbye when leaving",
     [("이만", "now"), ("갈게요", "will go")]),
    ("안녕히 가세요", "Go peacefully (goodbye)", "annyeonghi gaseyo",
     "Goodbye to person leaving",
     "Said by person staying",
     [("안녕히", "peacefully"), ("가세요", "go")]),
    ("안녕히 계세요", "Stay peacefully (goodbye)", "annyeonghi gyeseyo",
     "Goodbye to person staying",
     "Said by person leaving",
     [("안녕히", "peacefully"), ("계세요", "stay")]),
    ("내일 봐요", "See you tomorrow", "naeil bwayo",
     "Future meeting",
     "Will meet tomorrow",
     [("내일", "tomorrow"), ("봐요", "see")]),
    ("또 만나요", "Meet again", "tto mannaeyo",
     "Future meeting",
     "Will meet again sometime",
     [("또", "again"), ("만나요", "meet")]),

    # ===== CONCERN =====
    ("괜찮으세요?", "Are you okay?", "gwaencheuseyo?",
     "Concern for someone",
     "Asking if someone is alright",
     [("괜찮", "okay"), ("으세요", "are you")]),
    ("무슨 일 있어요?", "What's wrong?", "museun ireoyo?",
     "Asking about problem",
     "Noticing something is wrong",
     [("무슨", "what"), ("일", "matter"), ("있어요", "is there")]),
    ("무슨 일이에요?", "What happened?", "museun irieyo?",
     "Asking what's wrong",
     "Asking about a problem",
     [("무슨", "what"), ("일", "matter"), ("이에요", "is it")]),
    ("왜 그래요?", "Why (are you like that)?", "wae geuraeyo?",
     "Asking why",
     "Why is something wrong",
     [("왜", "why"), ("그래요", "like that")]),
    ("괜찮아요?", "Are you okay?", "gwaenchanaeyo?",
     "Concern",
     "Checking someone is okay",
     [("괜찮", "okay"), ("아요", "is it")]),
    ("별일 아니에요", "Nothing serious", "byeolirieopda",
     "Reassurance",
     "It's nothing to worry about",
     [("별일", "nothing serious"), ("아니에요", "it's not")]),

    # ===== ENCOURAGEMENT =====
    ("힘내세요", "Cheer up / Be strong", "himnaeseyo",
     "Encouragement",
     "Encouraging someone going through hard time",
     [("힘", "strength"), ("내세요", "give")]),
    ("괜찮아요", "It's okay", "gwaenchanaeyo",
     "Reassurance",
     "Everything will be fine",
     [("괜찮", "okay"), ("아요", "it is")]),
    ("잘 될 거예요", "It will work out", "jal doel geoyeyo",
     "Optimism",
     "Things will get better",
     [("잘", "well"), ("될", "will become"), ("거예요", "it")]),
    ("포기하지 마세요", "Don't give up", "pogihajiseyo",
     "Encouragement",
     "Keep trying",
     [("포기", "give up"), ("하지", "don't"), ("마세요", "please")]),
    ("할 수 있어요", "You can do it", "hal suisueyo",
     "Encouragement",
     "Believing in someone",
     [("할", "do"), ("수", "able to"), ("있어요", "you are")]),
    ("너무 걱정하지 마세요", "Don't worry too much", "neomu geokjeonghaji maseyo",
     "Reassurance",
     "Stop worrying so much",
     [("너무", "too"), ("걱정", "worry"), ("하지", "don't"), ("마세요", "please")]),
    ("괜찮아질 거예요", "It will get better", "gwaenchanajil geoyeyo",
     "Hope",
     "Situation will improve",
     [("괜찮아", "okay"), ("질", "will become"), ("거예요", "it")]),

    # ===== CONGRATULATIONS =====
    ("축하해요", "Congratulations", "chukahaeyo",
     "Congratulating",
     "Standard congratulations",
     [("축하", "congratulations"), ("해요", "I")]),
    ("축하드려요", "Congratulations (formal)", "chukahadeuryeo",
     "Formal congratulations",
     "More formal congrats",
     [("축하", "congratulations"), ("드려요", "I give")]),
    ("잘하셨어요", "Well done", "jalhasyeosseoyo",
     "Praise",
     "You did well",
     [("잘", "well"), ("하셨어요", "you did")]),
    ("대단하네요", "Amazing", "daedanhaneyo",
     "Impressed",
     "That's impressive",
     [("대단", "amazing"), ("하네요", "it is")]),
    ("멋지네요", "Cool", "meojineyo",
     "Compliment",
     "That's cool",
     [("멋", "cool"), ("지네요", "it is")]),
    ("잘했어", "Good job", "jahasseo",
     "Praise",
     "You did good",
     [("잘", "well"), ("했어", "did")]),
    ("역시나요", "As expected of you", "yeoksinayo",
     "Compliment",
     "You're consistently good",
     [("역시", "as expected"), ("나요", "of you")]),

    # ===== FOOD & EATING =====
    ("잘 먹겠습니다", "Thank you for the food (before)", "jal meokgesseumnida",
     "Before eating",
     "Said before eating someone's food",
     [("잘", "well"), ("먹겠", "will eat"), ("습니다", "I")]),
    ("잘 먹었습니다", "Thank you for the food (after)", "jal meogeotseumnida",
     "After eating",
     "Said after eating someone's food",
     [("잘", "well"), ("먹었습니다", "I ate")]),
    ("맛있게 드세요", "Enjoy your meal", "masitge deuseyo",
     "Before eating",
     "Wishing someone enjoyment of food",
     [("맛있게", "deliciously"), ("드세요", "please eat")]),
    ("맛있어 보여요", "Looks delicious", "masitge boyeoyo",
     "Complimenting food",
     "Food looks good",
     [("맛있", "delicious"), ("어", "it"), ("보여요", "looks")]),
    ("배부르다", "I'm full", "baebureuda",
     "After eating",
     "Ate enough",
     [("배", "stomach"), ("부르다", "full")]),
    ("배고파", "I'm hungry", "baegopa",
     "Hungry",
     "Need to eat",
     [("배", "stomach"), ("고파", "hungry")]),
    ("식사하셨어요?", "Have you eaten?", "siksahasyeosseoyo?",
     "Greeting/care",
     "Common greeting in Korea",
     [("식사", "meal"), ("하셨어요", "did you have")]),
    ("밥 먹었어?", "Have you eaten? (casual)", "bap meogeosseo?",
     "Casual greeting",
     "Common greeting with friends",
     [("밥", "rice/meal"), ("먹었어", "did you eat")]),

    # ===== WORK & EFFORT =====
    ("수고하셨습니다", "Thank you for your hard work", "sugohasyeotseumnida",
     "After someone's work",
     "Acknowledging effort",
     [("수고", "effort"), ("하셨습니다", "you did")]),
    ("고생하셨어요", "You went through a lot", "gosaenghasyeosseoyo",
     "Acknowledging hardship",
     "Someone had a hard time",
     [("고생", "hardship"), ("하셨어요", "you went through")]),
    ("정말 수고가 많으셨어요", "You really worked hard", "jeongmal sugoga maneusyeosseoyo",
     "Acknowledging effort",
     "Appreciating hard work",
     [("정말", "really"), ("수고", "effort"), ("가", "was"), ("많으셨어요", "a lot")]),
    ("고생했어", "You had it hard", "gosaenghaesseo",
     "Acknowledging hardship",
     "Casual acknowledgment",
     [("고생", "hardship"), ("했어", "you had")]),
    ("늦게까지 고생했어요", "Thanks for staying late", "neutge kkaji gosaenghaeseoyo",
     "Thanking for late work",
     "Someone stayed late to work",
     [("늦게", "late"), ("까지", "until"), ("고생", "hardship"), ("했어요", "you did")]),

    # ===== EMPATHY =====
    ("속상해요", "I feel bad (for you)", "soksanghaeyo",
     "Empathy",
     "Feeling bad for someone's situation",
     [("속", "inside"), ("상", "heart"), ("해요", "feels")]),
    ("미안해요", "I feel bad (for you)", "mianhaeyo",
     "Empathy",
     "Sorry to hear something",
     [("미안", "sorry"), ("해요", "I feel")]),
    ("진심으로 응원할게요", "I sincerely support you", "jinsimeureung wonhalgeyo",
     "Support",
     "Genuinely supporting someone",
     [("진심", "sincerity"), ("으로", "with"), ("응원", "support"), ("할게요", "I will")]),
    ("마음이 아프네요", "My heart hurts", "maeumi apeuneyo",
     "Sadness for someone",
     "Feeling someone's pain",
     [("마음", "heart/mind"), ("이", "subject"), ("아프네요", "hurts")]),
    ("정말 안타까워요", "Really heartbreaking", "jeongmal antakkawoyo",
     "Pity",
     "Feeling bad for someone",
     [("정말", "really"), ("안타까워", "heartbreaking"), ("요", "it is")]),

    # ===== SUGGESTIONS =====
    ("어때요?", "How about / What do you think?", "eottaeyo?",
     "Asking opinion",
     "What do you think about this",
     [("어때", "how is"), ("요", "it?")]),
    ("하는 게 어때요?", "How about doing?", "haneun ge eottaeyo?",
     "Making suggestion",
     "Why don't you do this",
     [("하는", "doing"), ("게", "thing"), ("어때요", "how about")]),
    ("같이 가요", "Let's go together", "gachi gayo",
     "Invitation",
     "Come with me",
     [("같이", "together"), ("가요", "let's go")]),
    ("함께 가요", "Let's go together", "hamkke gayo",
     "Invitation",
     "Go together",
     [("함께", "together"), ("가요", "let's go")]),
    ("한번 해볼까요?", "Shall we try once?", "hanbeon haebolkkayo?",
     "Suggestion",
     "Let's give it a try",
     [("한번", "once"), ("해볼까", "shall we try"), ("요", "?")]),
    ("그럽시다", "Let's do that", "geureopsida",
     "Agreement",
     "Okay, let's do it",
     [("그렇", "so"), ("입시다", "let's do")]),

    # ===== UNCERTAINTY =====
    ("글쎄요 말이에요", "It's hard to say", "geulsseyo marieyo",
     "Uncertain",
     "Can't say for sure",
     [("글쎄", "well"), ("요", "hmm"), ("말", "words"), ("이에요", "it is")]),
    ("잘 모르겠어요", "I don't know well", "jal moreugessoyo",
     "Not sure",
     "Don't know much about it",
     [("잘", "well"), ("모르", "don't know"), ("겠어요", "I")]),
    ("확실하지 않아요", "Not certain", "hwaksilhaji anayo",
     "Uncertain",
     "Not sure about something",
     [("확실", "certain"), ("하지", "not"), ("않아요", "it is")]),
    ("모르겠네요", "I'm not sure", "moreugesseneyo",
     "Don't know",
     "Not sure about answer",
     [("모르", "don't know"), ("겠네요", "I seem")]),

    # ===== FRUSTRATION =====
    ("아 진짜!", "Oh really/come on!", "a jinjja!",
     "Frustration",
     "Expression of frustration",
     [("아", "oh"), ("진짜", "really")]),
    ("에휴", "Sigh", "ehyu",
     "Frustration",
     "Sighing in frustration",
     [("에휴", "sigh")]),
    ("헐 이건 진짜 아니야", "No way, this can't be", "heol igeon jinjja aniya",
     "Strong denial",
     "This can't be happening",
     [("헐", "whoa"), ("이건", "this"), ("진짜", "really"), ("아니야", "not")]),
    ("어떡해", "What to do", "eotteokae",
     "Helplessness",
     "Don't know what to do",
     [("어떡", "how"), ("해", "do")]),
    ("망했다", "It's ruined/screwed", "manghaetta",
     "Situation is bad",
     "Everything went wrong",
     [("망", "ruined"), ("했다", "became")]),

    # ===== WISHES =====
    ("좋은 꿈 꿨어요", "Sweet dreams", "joeun kkum kkweosseoyo",
     "Bedtime wish",
     "Have good dreams",
     [("좋은", "good"), ("꿈", "dream"), ("꿨어요", "dreamed")]),
    ("좋은 하루 보내세요", "Have a nice day", "joeun haru bonaeseyo",
     "Daily wish",
     "Have a good day",
     [("좋은", "good"), ("하루", "day"), ("보내세요", "spend")]),
    ("좋은 주말 보내세요", "Have a nice weekend", "joeun jumal bonaeseyo",
     "Weekend wish",
     "Enjoy your weekend",
     [("좋은", "good"), ("주말", "weekend"), ("보내세요", "spend")]),
    ("행운을 빕니다", "Good luck", "haenguneul bibnida",
     "Wishing luck",
     "Good luck to you",
     [("행운", "fortune"), ("을", "object"), ("빕니다", "I wish")]),
    ("부디 잘 되기를", "Hope it goes well", "budi jal doegireul",
     "Hope",
     "Hope everything goes well",
     [("부디", "please"), ("잘", "well"), ("되기를", "become")]),
]


def create_model():
    """Create card model for idioms."""
    return genanki.Model(
        MODEL_ID,
        "Korean Idiom Model",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Romanization"},
            {"name": "Situation"},
            {"name": "Usage"},
            {"name": "KoreanColored"},
            {"name": "EnglishColored"},
            {"name": "Audio"},
        ],
        templates=[
            {
                "name": "Korean Idiom Card",
                "qfmt": """
<div style="padding: 12px; background: #f5f5f5; border-radius: 10px; margin: 12px; text-align: center;">
    <strong style="font-size: 14px; color: #666;">{{Situation}}</strong>
</div>
<div style="text-align: center; font-size: 55px; padding: 35px;">
    {{Korean}}
</div>
                """,
                "afmt": """
<div style="padding: 10px; background: #f5f5f5; border-radius: 8px; margin: 8px; text-align: center;">
    <strong style="font-size: 13px; color: #666;">{{Situation}}</strong>
</div>
<div style="text-align: center; font-size: 50px; padding: 30px;">
    {{Korean}}
</div>
<div style="text-align: center; padding: 12px;">
    {{Audio}}
</div>
{{#Romanization}}
<div style="text-align: center; font-size: 22px; color: #666; padding: 8px;">
    <em>{{Romanization}}</em>
</div>
{{/Romanization}}
{{#KoreanColored}}
<div style="text-align: center; padding: 20px; margin: 15px auto; max-width: 600px; background: #fafafa; border-radius: 10px; border: 1px solid #eee;">
    <div style="font-size: 26px; padding: 10px; line-height: 1.8; color: #2c3e50; font-weight: 600;">
        {{KoreanColored}}
    </div>
    {{#EnglishColored}}
    <div style="font-size: 18px; color: #666; padding: 10px; line-height: 1.8;">
        {{EnglishColored}}
    </div>
    {{/EnglishColored}}
</div>
{{/KoreanColored}}
{{^KoreanColored}}
<hr style="margin: 12px 0;">
<div style="text-align: center; font-size: 28px; color: #2196F3; font-weight: bold; padding: 10px;">
    {{English}}
</div>
{{/KoreanColored}}
{{#Usage}}
<div style="text-align: center; font-size: 16px; padding: 12px; margin: 12px auto; max-width: 550px; background: #f9f9f9; border-radius: 8px;">
    {{Usage}}
</div>
{{/Usage}}
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


def generate_deck(output_file="decks/13_korean_idioms.apkg"):
    """Generate the idioms deck."""
    global created_audio_files
    created_audio_files.clear()

    model = create_model()
    deck = genanki.Deck(DECK_ID, "13. Korean Idioms & Expressions - 관용표현")

    # Create temporary directory for audio files
    audio_dir = tempfile.mkdtemp()

    try:
        for expression in EXPRESSIONS:
            # Handle both old format (5 elements) and new format (6 elements with word_pairs)
            if len(expression) == 6:
                korean, english, roman, situation, usage, word_pairs = expression
            else:
                korean, english, roman, situation, usage = expression
                word_pairs = []

            # Generate colored HTML if word_pairs available
            if word_pairs:
                korean_colored, english_colored = create_colored_html(word_pairs)
            else:
                korean_colored, english_colored = "", ""

            # Generate audio
            audio_filename = generate_audio(korean, audio_dir)
            audio_field = f"[sound:{audio_filename}]" if audio_filename else ""

            note = genanki.Note(
                model=model,
                fields=[korean, english, roman, situation, usage, korean_colored, english_colored, audio_field],
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
        print(f"  - {len(EXPRESSIONS)} idiom/expression cards")
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
