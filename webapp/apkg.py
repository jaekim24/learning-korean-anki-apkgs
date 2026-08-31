"""Read .apkg files: decks, note types, cards, media.

Only the legacy `collection.anki2` layout is handled -- that is what genanki
writes, and every deck in this repo comes from genanki.
"""

import hashlib
import json
import os
import re
import shutil
import sqlite3
import tempfile
import zipfile

FIELD_SEP = "\x1f"


def file_key(path):
    """Stable id for a deck file, changing when the file changes."""
    st = os.stat(path)
    raw = "%s|%d|%d" % (os.path.abspath(path), st.st_size, int(st.st_mtime))
    return hashlib.sha1(raw.encode()).hexdigest()[:12]


def read(path, media_dir):
    """Extract media into media_dir and return (decks, models, notes, cards)."""
    tmp = tempfile.mkdtemp()
    try:
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            if "collection.anki2" not in names:
                raise ValueError("no collection.anki2 in %s" % path)
            z.extract("collection.anki2", tmp)
            media_map = {}
            if "media" in names:
                media_map = json.loads(z.read("media").decode("utf-8") or "{}")
            if media_map and not os.path.isdir(media_dir):
                os.makedirs(media_dir)
                for num, real in media_map.items():
                    if num in names:
                        with z.open(num) as src:
                            with open(os.path.join(media_dir, real), "wb") as dst:
                                shutil.copyfileobj(src, dst)

        con = sqlite3.connect(os.path.join(tmp, "collection.anki2"))
        models_json, decks_json = con.execute("select models, decks from col").fetchone()
        models = json.loads(models_json)
        decks = json.loads(decks_json)
        notes = {
            nid: {"mid": str(mid), "fields": flds.split(FIELD_SEP), "tags": tags.strip()}
            for nid, mid, flds, tags in con.execute("select id, mid, flds, tags from notes")
        }
        cards = [
            {"id": cid, "nid": nid, "did": str(did), "ord": ordv}
            for cid, nid, did, ordv in con.execute("select id, nid, did, ord from cards")
        ]
        con.close()
        return decks, models, notes, cards
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# --- template rendering ---------------------------------------------------

CLOZE_RE = re.compile(r"\{\{c(\d+)::(.*?)(?:::(.*?))?\}\}", re.S)
SOUND_RE = re.compile(r"\[sound:(.*?)\]")
SECTION_RE = re.compile(r"\{\{([#^])([^}]+)\}\}(.*?)\{\{/\2\}\}", re.S)
REPL_RE = re.compile(r"\{\{([^}#^/][^}]*)\}\}")


def render_cloze(text, ord_num, answer_side):
    """Blank out the c{ord+1} deletions; reveal the rest."""
    target = ord_num + 1

    def sub(m):
        num, content, hint = int(m.group(1)), m.group(2), m.group(3)
        if num != target:
            return content
        if answer_side:
            return '<span class="cloze">%s</span>' % content
        return '<span class="cloze">[%s]</span>' % (hint or "...")

    return CLOZE_RE.sub(sub, text)


def render(template, fields, model, ord_num, front_side=None):
    """Render one side of a card. Supports {{Field}}, filters, sections."""

    def value(name):
        name = name.strip()
        if name == "FrontSide":
            return front_side or ""
        plain = False
        while ":" in name:
            filt, name = name.split(":", 1)
            filt, name = filt.strip(), name.strip()
            if filt == "cloze":
                return render_cloze(fields.get(name, ""), ord_num, front_side is not None)
            if filt in ("text", "type"):
                plain = True
        raw = fields.get(name, "")
        return re.sub(r"<[^>]+>", "", raw) if plain else raw

    def strip_media(s):
        return SOUND_RE.sub("", s).strip()

    def sections(text):
        while True:
            m = SECTION_RE.search(text)
            if not m:
                return text
            kind, name, body = m.group(1), m.group(2).strip(), m.group(3)
            filled = bool(strip_media(value(name)))
            keep = body if (filled if kind == "#" else not filled) else ""
            text = text[: m.start()] + keep + text[m.end() :]

    out = sections(template)
    out = REPL_RE.sub(lambda m: value(m.group(1)), out)
    return out


def is_empty(html):
    """A card side with no content -- Anki would not generate it.

    Audio counts as content: a listening card's front is often nothing but
    [sound:...].
    """
    if SOUND_RE.search(html):
        return False
    return not re.sub(r"<[^>]+>|&nbsp;|\s", "", html)


def sounds(html):
    return SOUND_RE.findall(html)


def strip_sounds(html):
    return SOUND_RE.sub("", html)
