"""Korean TTS with an on-disk cache.

Audio is keyed by a hash of the text, so identical text across lessons is
fetched once and reused. The cache lives in build/audio/ and persists between
runs -- rebuilding costs no network calls unless the text actually changed.
"""

import hashlib
import os
from typing import Optional

from gtts import gTTS

CACHE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build", "audio"
)


def _filename(text: str) -> str:
    return "ko_%s.mp3" % hashlib.md5(text.encode("utf-8")).hexdigest()[:12]


def clip(text: str) -> Optional[str]:
    """Return the cached filename for `text`, fetching it if absent.

    Returns None if synthesis fails so a network blip degrades one card to
    silent rather than aborting the whole build.
    """
    if not text:
        return None

    os.makedirs(CACHE_DIR, exist_ok=True)
    name = _filename(text)
    path = os.path.join(CACHE_DIR, name)

    if not os.path.exists(path):
        try:
            gTTS(text=text, lang="ko").save(path)
        except Exception as exc:
            print("  ! TTS failed for %r: %s" % (text, exc))
            return None

    return name


def path_for(name: str) -> str:
    return os.path.join(CACHE_DIR, name)


def sound_tag(text: str) -> tuple:
    """Return (anki_sound_field, media_path_or_None) for `text`."""
    name = clip(text)
    if not name:
        return "", None
    return "[sound:%s]" % name, path_for(name)
