# Korean v3 — HTSK-aligned

Decks that follow the [HowToStudyKorean](https://www.howtostudykorean.com/)
syllabus: one `.apkg` per unit, one subdeck per lesson.

## Build

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python genanki gTTS
.venv/bin/python build_all.py
```

Output lands in `build/`. Audio is cached in `build/audio/`, so the first run
fetches the TTS clips and later runs are near-instant unless sentence text changed.

## Status

| Unit | Lessons | Notes | Cards | State |
|---|---|---|---|---|
| 1 — Basic Korean Grammar | 25 | 121 | 272 | Written |
| 2–9 | 176 | — | — | Not yet written |

## Deck tree

```
HTSK Korean
  Unit 1 - Basic Korean Grammar
    Lesson 01 - Basic Korean Sentences
    Lesson 02 - Korean Particles 이/가
    ...
    Lesson 25 - Anybody, Everybody, Somebody, Nobody, etc.
```

Study one lesson by clicking it, or the whole unit from the parent. Each card
links back to its source lesson. Notes are tagged `unit1` / `lesson007` /
`grammar` / `sentence`.

## Where the content comes from

`htsk_lessons.json` is scraped **index metadata only** — lesson numbers, titles
and URLs for all 208 lessons (201 published; 202–208 aren't written yet on the
site). It supplies deck names and the source link on each card.

The study content — patterns, explanations, example sentences — is written for
this deck. HTSK sells PDF/workbook editions of their lesson material, so their
vocabulary lists and example sentences are deliberately **not** reproduced here.
That keeps these decks distributable. It also means the cards teach the same
grammar point as the corresponding lesson but won't match its examples
word-for-word — use them alongside the lesson, not as a replacement for reading it.

## Note types

**Grammar Point** — pattern on the front, meaning + formation rule on the back.
No listening card: a bare pattern like `~ㄴ/은` read aloud out of context tests nothing.

**Sentence** — Korean front, English back, with audio. Always generates a
separate listening card (audio front, text back).

Both carry an opt-in production card (EN→KR) via the `Production` field, following
v2's convention that Anki only generates a card when its front renders non-empty.

Opt-in rates here are higher than v2's: 47 of 54 grammar points and 37 of 67
sentences. For grammar, recalling the pattern *from* the meaning is the skill
worth having, so most points opt in. To dial it back, flip the trailing `produce`
flag in `units/unit1.py` — no template changes needed.

## Adding a unit

Unit modules are pure data. Write `units/unit2.py` with a `LESSONS` dict in the
schema documented at the top of `units/unit1.py`, add `2` to `UNITS` in
`build_all.py`, and rebuild — `korean/compose.py` handles the rest.

## Layout

```
build_all.py            entry point
htsk_lessons.json       scraped lesson index (all 208)
korean/
  ids.py                deterministic deck/model IDs from stable name strings
  syllabus.py           reads htsk_lessons.json
  models.py             the two note types
  build.py              UnitBuild — one package, a subdeck per lesson
  compose.py            LESSONS data -> notes
  audio.py              gTTS with an on-disk cache
units/
  unit1.py              authored content, lessons 1-25
```
