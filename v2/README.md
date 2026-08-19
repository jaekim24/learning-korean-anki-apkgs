# Korean v2

A rebuilt deck set. Fresh code — it does not share `lib/` or any generator with v1.

## Build

```bash
uv venv --python 3.12 .venv
uv pip install --python .venv/bin/python genanki gTTS
.venv/bin/python build_all.py
```

Output lands in `build/`. Audio is cached in `build/audio/`, so the first run
fetches ~480 TTS clips and later runs are near-instant unless deck text changed.

## What's in it

| Deck | Notes | Cards | Purpose |
|---|---|---|---|
| `00_hangul` | 40 | 40 | Letters by derivation. **Disposable — suspend after 3 days.** |
| `01_minimal_pairs` | 32 | 32 | Plain/tense/aspirated ear training. Audio-only front. |
| `02_batchim` | 36 | 36 | Spelling vs. sound. Audio front, spelling back. |
| `03_core_vocab` | 200 | 450 | Frequency-ordered, 4 tiers. Tier 1 also gets production cards. |
| `04_particles_cloze` | 43 | 46 | Particles as fill-in-the-blank, never as definitions. |
| `05_conjugation` | 69 | 69 | 3 rules + 7 irregular classes + the traps. |
| `06_sentence_patterns` | 59 | 142 | 8 patterns in teaching order, all 해요체. |
| **Total** | **479** | **815** | |

## What changed from v1

**Every note type generates a listening card.** v1 rendered `{{Audio}}` on the
answer side only, so the TTS was a confirmation after you'd already read the
answer — it never tested listening. Here audio is the front of its own card.

**Korean is the default front.** v1's sentence model put `{{English}}` on the
front, which made every sentence in the collection a production card — the
hardest possible drill applied to the longest items. Production is now opt-in
per note via the `Production` field: fill it and Anki generates the EN→KR card,
leave it blank and it doesn't. 74 of 479 notes opt in.

**Particles are cloze.** 은/는 vs 이/가 does not survive being written as a
definition. Every particle card blanks the slot and puts the reason on the back.

**Conjugation is rules, not stored forms.** v1's tense deck stored ~100 verbs ×
several tenses as individually memorized forms. Korean conjugation is three
rules plus seven irregular classes, so this deck drills the transformation and
names the rule — 69 cards instead of ~600. It also includes the traps: 입다,
좁다, 받다, 닫다, 웃다, 씻다, 좋다, 따르다 all look irregular and are not.

**Two new foundation decks** that v1 had no equivalent for: minimal-pair
discrimination and batchim sound change. These are the two things that strand
beginners right after hangul.

**IDs are derived, not curated.** v1 hand-maintained `DECK_IDS` / `MODEL_IDS`
dicts. Here `korean/ids.py` hashes a stable name string, so adding a deck can't
collide. Deck names are therefore load-bearing — renaming one orphans the old
deck in Anki.

**Dark mode.** All templates define `.nightMode` colors; v1's CSS was light-only.

## How to study it

**Settings first.** In each deck's options: turn on **FSRS**, set desired
retention to **0.90**, and cap new cards at **15/day**. That settles at roughly
100–150 reviews/day, about 20 minutes. Fifty new cards/day settles at 400+
reviews and people quit around day 12 under the backlog — surviving month one is
the single biggest predictor of getting anywhere.

**Days 1–3.** Deck 00 only. Learn the derivations, not the list. Start 01 and 02
on day 2 and run them alongside everything else for about two weeks.

**Week 1 onward.** Deck 06, one pattern per day, plus deck 03 Tier 1. You should
be able to say "I'm a student" in week one.

**Week 2 onward.** Add deck 04. Add deck 05 once you've met 아/어요 in deck 06.

**Month 2 onward.** Keep deck 03 running through the tiers, and start sentence
mining: take content slightly above your level (TTMIK Iyagi, Korean-subtitled
shows), find sentences where you know everything but one word, and make cards
from those. Ten a day. Mined cards from content you cared about stick far better
than anything on a prepared list, and this is where actual speed comes from.

**Every day, regardless.** Say every card out loud — never review silently.
Articulation builds motor memory that recognition alone never touches, and it
costs nothing extra. Write three sentences about your own day somewhere a native
will correct them.

**Leeches are broken cards, not personal failures.** If something fails 8 times,
delete it and rewrite it with more context. Never grind a leech.

## Notes on scope

Deck 03 stops at 200 words. The tier lists in `decks/d03_core_vocab.py` are plain
Python tuples — extend them and rebuild. Everything stays in 해요체; 반말 and
합쇼체 are deliberately absent, because mixing speech levels early triples the
conjugation load for no communicative gain.

Numbers, counters, and time are also absent. Korean's two number systems with
mismatched counters are genuinely hard, and v1 put them at position 03 where they
land on someone who can't yet form a sentence. They belong after deck 06.
