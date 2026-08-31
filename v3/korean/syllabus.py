"""The HTSK lesson index.

htsk_lessons.json is scraped metadata only -- lesson numbers, grammar-point
titles and URLs. It supplies deck names and the source link on each card; the
study content itself is authored in units/.
"""

import json
import os

_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "htsk_lessons.json"
)

with open(_PATH, encoding="utf-8") as fh:
    _DATA = json.load(fh)

UNITS = {u["unit"]: u for u in _DATA["units"]}
LESSONS = {l["lesson"]: l for l in _DATA["lessons"]}


def unit_name(unit: int) -> str:
    return UNITS[unit]["name"]


def lesson(number: int) -> dict:
    """Metadata for one lesson: title, url, unit, status."""
    return LESSONS[number]


def lessons_in(unit: int) -> list:
    return [l for l in _DATA["lessons"] if l["unit"] == unit and l["status"] == "published"]
