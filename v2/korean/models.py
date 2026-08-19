"""Anki note types for v2.

Three deliberate departures from v1:

1. Every note type generates a *listening* card: audio on the front, text only
   on the back. v1 rendered {{Audio}} on the answer side only, which trains
   reading and then plays a confirmation -- it never tests listening.

2. Korean is the default front. Recognition (KR->EN) is the cheap direction and
   is what you want by default. v1's sentence model put English on the front,
   making every sentence in the collection a hard production card.

3. Production (EN->KR) is opt-in per note. The template is wrapped in
   {{#Production}}, and Anki only generates a card when its front renders
   non-empty -- so filling that field on a note adds the production card, and
   leaving it blank does not.
"""

import genanki

from .ids import stable_id

CSS = """
.card {
  font-family: 'Apple SD Gothic Neo', 'Malgun Gothic', 'Noto Sans KR', sans-serif;
  font-size: 20px;
  line-height: 1.7;
  text-align: center;
  background: #ffffff;
  color: #1a1a1a;
  padding: 24px 16px;
}
.card.nightMode, .card.night_mode { background: #1e1e1e; color: #e8e8e8; }

.ko      { font-size: 44px; font-weight: 600; }
.ko-sm   { font-size: 30px; font-weight: 600; }
.en      { font-size: 26px; color: #1976D2; font-weight: 600; }
.nightMode .en, .night_mode .en { color: #64B5F6; }
.reading { font-size: 18px; color: #777; font-style: italic; }
.nightMode .reading, .night_mode .reading { color: #aaa; }
.note    { font-size: 16px; color: #666; }
.nightMode .note, .night_mode .note { color: #aaa; }

.panel {
  max-width: 620px; margin: 16px auto; padding: 14px 18px;
  background: #f6f6f6; border: 1px solid #e4e4e4; border-radius: 10px;
}
.nightMode .panel, .night_mode .panel { background: #2a2a2a; border-color: #3d3d3d; }

.gloss-ko { font-size: 24px; line-height: 1.9; }
.gloss-en { font-size: 17px; line-height: 1.9; opacity: 0.85; }

.prompt-label {
  font-size: 13px; letter-spacing: .12em; text-transform: uppercase;
  color: #999; margin-bottom: 14px;
}
hr { border: none; border-top: 1px solid #ddd; margin: 18px auto; max-width: 620px; }
.nightMode hr, .night_mode hr { border-top-color: #3d3d3d; }
"""

_LISTEN_FRONT = """
<div class="prompt-label">Listen</div>
<div style="font-size:34px">{{Audio}}</div>
"""


def vocab_model() -> genanki.Model:
    return genanki.Model(
        stable_id("model:vocab:v2"),
        "Korean v2 - Vocab",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Reading"},
            {"name": "Example"},
            {"name": "ExampleEN"},
            {"name": "Audio"},
            {"name": "Production"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Recognition",
                "qfmt": '<div class="ko">{{Korean}}</div>',
                "afmt": """
<div class="ko">{{Korean}}</div>
<div>{{Audio}}</div>
{{#Reading}}<div class="reading">{{Reading}}</div>{{/Reading}}
<hr>
<div class="en">{{English}}</div>
{{#Example}}
<div class="panel">
  <div class="ko-sm" style="font-size:22px">{{Example}}</div>
  {{#ExampleEN}}<div class="note">{{ExampleEN}}</div>{{/ExampleEN}}
</div>
{{/Example}}
""",
            },
            {
                "name": "2 Listening",
                "qfmt": _LISTEN_FRONT,
                "afmt": """
<div class="ko">{{Korean}}</div>
<div>{{Audio}}</div>
<hr>
<div class="en">{{English}}</div>
""",
            },
            {
                "name": "3 Production",
                "qfmt": """
{{#Production}}
<div class="prompt-label">Say it in Korean</div>
<div class="en">{{English}}</div>
{{/Production}}
""",
                "afmt": """
<div class="en">{{English}}</div>
<hr>
<div class="ko">{{Korean}}</div>
<div>{{Audio}}</div>
""",
            },
        ],
    )


def sentence_model() -> genanki.Model:
    return genanki.Model(
        stable_id("model:sentence:v2"),
        "Korean v2 - Sentence",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "GlossKO"},
            {"name": "GlossEN"},
            {"name": "Note"},
            {"name": "Audio"},
            {"name": "Production"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Recognition",
                "qfmt": '<div class="ko-sm">{{Korean}}</div>',
                "afmt": """
<div class="ko-sm">{{Korean}}</div>
<div>{{Audio}}</div>
<hr>
<div class="en">{{English}}</div>
{{#GlossKO}}
<div class="panel">
  <div class="gloss-ko">{{GlossKO}}</div>
  <div class="gloss-en">{{GlossEN}}</div>
</div>
{{/GlossKO}}
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
""",
            },
            {
                "name": "2 Listening",
                "qfmt": _LISTEN_FRONT,
                "afmt": """
<div class="ko-sm">{{Korean}}</div>
<div>{{Audio}}</div>
<hr>
<div class="en">{{English}}</div>
""",
            },
            {
                "name": "3 Production",
                "qfmt": """
{{#Production}}
<div class="prompt-label">Say it in Korean</div>
<div class="en">{{English}}</div>
{{/Production}}
""",
                "afmt": """
<div class="en">{{English}}</div>
<hr>
<div class="ko-sm">{{Korean}}</div>
<div>{{Audio}}</div>
{{#GlossKO}}
<div class="panel">
  <div class="gloss-ko">{{GlossKO}}</div>
  <div class="gloss-en">{{GlossEN}}</div>
</div>
{{/GlossKO}}
""",
            },
        ],
    )


def cloze_model() -> genanki.Model:
    """Fill-in-the-blank, for particles and grammar endings.

    A particle contrast like 은/는 vs 이/가 is not learnable from a definition;
    it only resolves through many contrasting examples with the slot empty.
    """
    return genanki.Model(
        stable_id("model:cloze:v2"),
        "Korean v2 - Cloze",
        model_type=genanki.Model.CLOZE,
        fields=[
            {"name": "Text"},
            {"name": "English"},
            {"name": "Why"},
            {"name": "Audio"},
        ],
        css=CSS,
        templates=[
            {
                "name": "Cloze",
                "qfmt": '<div class="ko-sm">{{cloze:Text}}</div>',
                "afmt": """
<div class="ko-sm">{{cloze:Text}}</div>
<div>{{Audio}}</div>
<hr>
<div class="en">{{English}}</div>
{{#Why}}<div class="panel"><div class="note">{{Why}}</div></div>{{/Why}}
""",
            },
        ],
    )


def transform_model() -> genanki.Model:
    """Apply-the-rule drill, for conjugation.

    Korean conjugation is a small set of rules plus seven irregular classes.
    Drilling the transformation (and naming the rule on the back) teaches the
    generator; storing every inflected form as its own card does not.
    """
    return genanki.Model(
        stable_id("model:transform:v2"),
        "Korean v2 - Transform",
        fields=[
            {"name": "Prompt"},
            {"name": "Task"},
            {"name": "Answer"},
            {"name": "Rule"},
            {"name": "Audio"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Apply rule",
                "qfmt": """
<div class="prompt-label">{{Task}}</div>
<div class="ko">{{Prompt}}</div>
""",
                "afmt": """
<div class="prompt-label">{{Task}}</div>
<div class="ko-sm" style="opacity:.6">{{Prompt}}</div>
<hr>
<div class="ko">{{Answer}}</div>
<div>{{Audio}}</div>
{{#Rule}}<div class="panel"><div class="note">{{Rule}}</div></div>{{/Rule}}
""",
            },
        ],
    )


def audio_only_model() -> genanki.Model:
    """Pure listening discrimination, for minimal pairs and batchim.

    No text on the front at all -- the whole point is that the learner cannot
    yet map these sounds to spellings, and reading the answer first defeats it.
    """
    return genanki.Model(
        stable_id("model:audio:v2"),
        "Korean v2 - Audio",
        fields=[
            {"name": "Audio"},
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Contrast"},
            {"name": "Note"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Hear it",
                "qfmt": """
<div class="prompt-label">Listen</div>
<div style="font-size:34px">{{Audio}}</div>
{{#Contrast}}<div class="panel"><div class="ko-sm">{{Contrast}}</div></div>{{/Contrast}}
""",
                "afmt": """
<div style="font-size:34px">{{Audio}}</div>
<hr>
<div class="ko">{{Korean}}</div>
<div class="en">{{English}}</div>
{{#Note}}<div class="panel"><div class="note">{{Note}}</div></div>{{/Note}}
""",
            },
        ],
    )


def letter_model() -> genanki.Model:
    """Hangul letters, taught by derivation. Intentionally disposable."""
    return genanki.Model(
        stable_id("model:letter:v2"),
        "Korean v2 - Letter",
        fields=[
            {"name": "Letter"},
            {"name": "Sound"},
            {"name": "Name"},
            {"name": "Derivation"},
            {"name": "Example"},
            {"name": "Audio"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Letter",
                "qfmt": '<div style="font-size:110px;font-weight:600">{{Letter}}</div>',
                "afmt": """
<div style="font-size:110px;font-weight:600">{{Letter}}</div>
<hr>
<div class="en">{{Sound}}</div>
<div class="reading">{{Name}}</div>
{{#Derivation}}
<div class="panel"><div class="note">{{Derivation}}</div></div>
{{/Derivation}}
{{#Example}}<div class="ko-sm">{{Example}}</div>{{/Example}}
<div>{{Audio}}</div>
""",
            },
        ],
    )
