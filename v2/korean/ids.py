"""Deterministic Anki IDs.

v1 kept hand-maintained DECK_IDS / MODEL_IDS dicts, which drift and collide as
decks are added. Here an ID is a pure function of a stable name string, so a
deck keeps its identity across rebuilds without anyone curating a registry.
Changing the name string orphans the old deck in Anki, so treat names as fixed.
"""

import hashlib

# genanki's recommended range for user-generated IDs.
_LO = 1 << 30
_HI = 1 << 31


def stable_id(name: str) -> int:
    digest = hashlib.md5(name.encode("utf-8")).hexdigest()
    return _LO + (int(digest[:12], 16) % (_HI - _LO))
