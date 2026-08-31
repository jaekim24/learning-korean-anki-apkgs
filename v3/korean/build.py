"""Deck assembly.

One .apkg per unit. Inside it, each lesson is its own subdeck, so Anki's tree
ends up as:

    HTSK Korean
      Unit 1 - Basic Korean Grammar
        Lesson 01 - Basic Korean Sentences
        Lesson 02 - Korean Particles 이/가
        ...

That gives a deck per unit *and* per lesson while staying at 9 imports rather
than 201. Study a single lesson by clicking it, or the whole unit by clicking
the parent.

Media is collected as notes are added, so a unit only ships the clips it uses.
"""

import os
import re
from typing import Iterable, List

import genanki

from . import audio as audio_mod
from . import syllabus
from .ids import stable_id

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build")

ROOT = "HTSK Korean"


def _clean(text: str) -> str:
    """Anki treats '::' as a deck separator, so it can't survive in a deck name."""
    return text.replace("::", " -").strip()


class UnitBuild:
    def __init__(self, unit: int):
        self.unit = unit
        self.name = syllabus.unit_name(unit)
        self.slug = "unit%02d_%s" % (unit, re.sub(r"[^a-z0-9]+", "_", self.name.lower()).strip("_"))
        self.unit_deck_name = "%s::Unit %d - %s" % (ROOT, unit, _clean(self.name))

        # The parent deck is emitted empty; it exists so Anki nests the lessons
        # under it and you can study the whole unit from one click.
        self.decks = {None: genanki.Deck(stable_id("deck:unit:%d" % unit), self.unit_deck_name)}
        self.media: List[str] = []
        self._seen_media = set()

    def _deck_for(self, lesson: int) -> genanki.Deck:
        if lesson not in self.decks:
            meta = syllabus.lesson(lesson)
            name = "%s::Lesson %02d - %s" % (self.unit_deck_name, lesson, _clean(meta["title"]))
            self.decks[lesson] = genanki.Deck(stable_id("deck:lesson:%d" % lesson), name)
        return self.decks[lesson]

    def audio(self, text: str) -> str:
        """Synthesize `text`, register the media file, return the Anki tag."""
        tag, path = audio_mod.sound_tag(text)
        if path and path not in self._seen_media:
            self._seen_media.add(path)
            self.media.append(path)
        return tag

    def add(self, lesson: int, model: genanki.Model, fields: Iterable[str],
            tags: Iterable[str] = ()) -> None:
        tags = list(tags) + ["unit%d" % self.unit, "lesson%03d" % lesson]
        self._deck_for(lesson).add_note(
            genanki.Note(model=model, fields=list(fields), tags=tags)
        )

    def write(self) -> str:
        os.makedirs(OUT_DIR, exist_ok=True)
        out = os.path.join(OUT_DIR, "%s.apkg" % self.slug)
        pkg = genanki.Package(list(self.decks.values()))
        pkg.media_files = self.media
        pkg.write_to_file(out)

        notes = sum(len(d.notes) for d in self.decks.values())
        lessons = len([k for k in self.decks if k is not None])
        print("  %-44s %3d lessons  %4d notes  %4d clips"
              % (self.slug + ".apkg", lessons, notes, len(self.media)))
        return out
