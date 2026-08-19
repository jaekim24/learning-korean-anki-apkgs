"""Chunk-aligned glossing.

A gloss is a list of (korean_chunk, english_chunk) pairs. Rendering both sides
in matching colors makes Korean word order visible at a glance -- the learner
sees that the verb landed at the end and the particle rode along with its noun.
"""

from typing import List, Tuple

# Chosen to stay legible on both light and dark card backgrounds.
COLORS = ["#D32F2F", "#1976D2", "#388E3C", "#F57C00", "#7B1FA2", "#0097A7"]


def render(pairs: List[Tuple[str, str]]) -> Tuple[str, str]:
    """Return (korean_html, english_html) with per-chunk matching colors."""
    if not pairs:
        return "", ""

    ko, en = [], []
    for i, (k, e) in enumerate(pairs):
        color = COLORS[i % len(COLORS)]
        ko.append('<span style="color:%s">%s</span>' % (color, k))
        en.append('<span style="color:%s">%s</span>' % (color, e))

    return " ".join(ko), " ".join(en)
