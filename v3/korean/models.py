"""Anki note types for v3.

Two note types, matching how the HTSK syllabus is actually shaped: a lesson
teaches a *pattern*, and the pattern is drilled through *sentences*.

Conventions carried over from v2:
  - Korean is the default front; recognition is the cheap direction.
  - Production (EN->KR) is opt-in per note via the Production field: Anki only
    generates the card when its front renders non-empty.

There are no listening cards. Audio still renders on the answer side of both
note types as a pronunciation reference, but nothing drills audio-first.
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
.ko-sm   { font-size: 28px; font-weight: 600; }
.pattern { font-size: 40px; font-weight: 600; letter-spacing: .02em; }
.en      { font-size: 26px; color: #1976D2; font-weight: 600; }
.nightMode .en, .night_mode .en { color: #64B5F6; }
.note    { font-size: 16px; color: #666; }
.nightMode .note, .night_mode .note { color: #aaa; }

.panel {
  max-width: 620px; margin: 16px auto; padding: 14px 18px;
  background: #f6f6f6; border: 1px solid #e4e4e4; border-radius: 10px;
  text-align: left;
}
.nightMode .panel, .night_mode .panel { background: #2a2a2a; border-color: #3d3d3d; }
.panel-label {
  font-size: 12px; letter-spacing: .12em; text-transform: uppercase;
  color: #999; margin-bottom: 6px;
}
.form { font-size: 19px; line-height: 1.8; }

.prompt-label {
  font-size: 13px; letter-spacing: .12em; text-transform: uppercase;
  color: #999; margin-bottom: 14px;
}
.src { font-size: 13px; color: #aaa; margin-top: 18px; }
.src a { color: #aaa; text-decoration: none; }
hr { border: none; border-top: 1px solid #ddd; margin: 18px auto; max-width: 620px; }
.nightMode hr, .night_mode hr { border-top-color: #3d3d3d; }
"""

_SOURCE = """
{{#Link}}<div class="src"><a href="{{Link}}">HTSK Lesson {{Lesson}}</a></div>{{/Link}}
"""


def grammar_model() -> genanki.Model:
    """One note per grammar point: the pattern, what it means, how to build it."""
    return genanki.Model(
        stable_id("model:grammar:v3"),
        "Korean v3 - Grammar Point",
        fields=[
            {"name": "Pattern"},
            {"name": "Meaning"},
            {"name": "Form"},
            {"name": "Note"},
            {"name": "Lesson"},
            {"name": "Link"},
            {"name": "Production"},
        ],
        css=CSS,
        templates=[
            {
                "name": "1 Recognition",
                "qfmt": """
<div class="prompt-label">What does this do?</div>
<div class="pattern">{{Pattern}}</div>
""",
                "afmt": """
<div class="pattern">{{Pattern}}</div>
<hr>
<div class="en">{{Meaning}}</div>
{{#Form}}
<div class="panel">
  <div class="panel-label">How to build it</div>
  <div class="form">{{Form}}</div>
</div>
{{/Form}}
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
"""
                + _SOURCE,
            },
            {
                "name": "2 Production",
                "qfmt": """
{{#Production}}
<div class="prompt-label">Which pattern?</div>
<div class="en">{{Meaning}}</div>
{{/Production}}
""",
                "afmt": """
<div class="en">{{Meaning}}</div>
<hr>
<div class="pattern">{{Pattern}}</div>
{{#Form}}
<div class="panel">
  <div class="panel-label">How to build it</div>
  <div class="form">{{Form}}</div>
</div>
{{/Form}}
"""
                + _SOURCE,
            },
        ],
    )


def sentence_model() -> genanki.Model:
    """One note per example sentence -- where the pattern actually gets drilled."""
    return genanki.Model(
        stable_id("model:sentence:v3"),
        "Korean v3 - Sentence",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Note"},
            {"name": "Audio"},
            {"name": "Lesson"},
            {"name": "Link"},
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
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
"""
                + _SOURCE,
            },
            {
                "name": "2 Production",
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
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
"""
                + _SOURCE,
            },
        ],
    )

def vocab_model() -> genanki.Model:
    """One note per word. Vocabulary is chosen to fit the lesson's grammar."""
    return genanki.Model(
        stable_id("model:vocab:v3"),
        "Korean v3 - Vocab",
        fields=[
            {"name": "Korean"},
            {"name": "English"},
            {"name": "Note"},
            {"name": "Audio"},
            {"name": "Lesson"},
            {"name": "Link"},
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
<hr>
<div class="en">{{English}}</div>
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
"""
                + _SOURCE,
            },
            {
                "name": "2 Production",
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
{{#Note}}<div class="note">{{Note}}</div>{{/Note}}
"""
                + _SOURCE,
            },
        ],
    )
