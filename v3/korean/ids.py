"""Deterministic Anki IDs.

Same approach as v2: an ID is a pure function of a stable name string, so a
deck keeps its identity across rebuilds without a hand-curated registry. Lesson
decks are named from their HTSK lesson number, which never changes, so a
rebuild lands on top of the existing deck instead of duplicating it.

Changing a name string orphans the old deck in Anki, so treat names as fixed.
"""

import hashlib

# genanki's recommended range for user-generated IDs.
_LO = 1 << 30
_HI = 1 << 31


def stable_id(name: str) -> int:
    digest = hashlib.md5(name.encode("utf-8")).hexdigest()
    return _LO + (int(digest[:12], 16) % (_HI - _LO))
