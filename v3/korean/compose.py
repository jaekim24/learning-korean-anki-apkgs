"""Turns a unit's LESSONS data into an .apkg.

Every unit module is pure data in the schema documented in units/unit1.py, so
adding Unit 2 means writing content, not build code.
"""

from . import syllabus
from .build import UnitBuild
from .models import grammar_model, sentence_model, vocab_model

# Instantiated once: two notes sharing a model must share its ID.
GRAMMAR = grammar_model()
SENTENCE = sentence_model()
VOCAB = vocab_model()


def build_unit(unit: int, lessons: dict) -> str:
    pkg = UnitBuild(unit)

    for number in sorted(lessons):
        meta = syllabus.lesson(number)
        link = meta["url"] or ""

        for pattern, meaning, form, note, produce in lessons[number]["points"]:
            pkg.add(number, GRAMMAR,
                    [pattern, meaning, form, note, str(number), link,
                     "y" if produce else ""],
                    tags=["grammar"])

        for korean, english, note, produce in lessons[number].get("vocab", ()):
            pkg.add(number, VOCAB,
                    [korean, english, note, pkg.audio(korean), str(number), link,
                     "y" if produce else ""],
                    tags=["vocab"])

        for korean, english, note, produce in lessons[number]["sentences"]:
            pkg.add(number, SENTENCE,
                    [korean, english, note, pkg.audio(korean), str(number), link,
                     "y" if produce else ""],
                    tags=["sentence"])

    return pkg.write()
