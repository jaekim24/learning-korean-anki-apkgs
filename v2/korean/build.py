"""Deck assembly.

Each deck module builds one Build, adds notes to it, and calls write(). Media
is collected as notes are added, so a deck only ships the clips it uses.
"""

import os
from typing import Iterable, List

import genanki

from . import audio as audio_mod
from .ids import stable_id

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build")


class Build:
    def __init__(self, slug: str, title: str):
        self.slug = slug
        self.deck = genanki.Deck(stable_id("deck:%s" % slug), title)
        self.media: List[str] = []
        self._seen_media = set()

    def audio(self, text: str) -> str:
        """Synthesize `text`, register the media file, return the Anki tag."""
        tag, path = audio_mod.sound_tag(text)
        if path and path not in self._seen_media:
            self._seen_media.add(path)
            self.media.append(path)
        return tag

    def add(self, model: genanki.Model, fields: Iterable[str], tags: Iterable[str] = ()) -> None:
        self.deck.add_note(genanki.Note(model=model, fields=list(fields), tags=list(tags)))

    def write(self) -> str:
        os.makedirs(OUT_DIR, exist_ok=True)
        out = os.path.join(OUT_DIR, "%s.apkg" % self.slug)
        pkg = genanki.Package(self.deck)
        pkg.media_files = self.media
        pkg.write_to_file(out)
        print("  %-34s %4d notes  %4d clips" % (self.slug + ".apkg", len(self.deck.notes), len(self.media)))
        return out
