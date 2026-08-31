# Local Anki web app

A self-contained study server for the `.apkg` decks in this repo. No Anki
install, no account, no third-party Python packages — stdlib only.

```bash
python3 webapp/server.py          # http://127.0.0.1:8777, opens a browser
python3 webapp/server.py --port 9000 --no-browser
python3 webapp/server.py --deck-dir some/other/dir   # repeatable
```

By default it serves the **7 decks in `v2/build/`** (815 cards) and nothing
else. The 19 v1 decks in `decks/` cover the same ground with worse cards, and 26
decks in one list is unusable — `--deck-dir decks` brings them back if you want
them. First run takes ~10s (it extracts audio); later runs start instantly and
only re-import files whose size or mtime changed. Decks that leave the scanned
directories are dropped, along with their cards, media, and scheduling.

## What it does

- Deck list with new / learning / due counts, and lifetime review stats.
- Study view that renders each card with its own Anki note-type CSS, including
  cloze deletions, conditional `{{#Field}}` sections, and `{{FrontSide}}`.
- Audio: `[sound:...]` becomes a play button. The front's audio autoplays, so
  the v2 listening cards work as intended. `r` replays.
- Keyboard: `space` shows the answer then grades Good, `1`–`4` grade directly.
- SM-2 scheduling with 1m/10m learning steps, a 1-day graduating interval, and
  per-deck new-card limits (default 15/day, matching the v2 README).
- Dark mode follows the OS setting, for the page and for the cards.

## Where state lives

`webapp/data/study.db` (gitignored) holds imported cards, scheduling, and the
review log. `webapp/data/media/` holds audio extracted from each `.apkg`.

Scheduling is keyed on a hash of *card content* (deck name + template ordinal +
note fields), not on Anki card ids. Rebuilding a deck — `python3 v2/build_all.py`
— therefore keeps your progress on every card whose text didn't change; only
edited or new cards come back as new. Renaming a deck resets it.

Delete `webapp/data/` to start over. "Reset progress" on a finished deck clears
just that deck.

## Limits

- It reads the legacy `collection.anki2` layout that genanki writes. Newer
  Anki exports (`collection.anki21b`, zstd-compressed) are not handled.
- It does not sync with Anki or AnkiWeb, and does not write `.apkg` files back.
  Progress lives only in `study.db`.
- Scheduling is SM-2, not FSRS.
- One duplicate note in `decks/09_korean_sentences_1.apkg` (비가 와요) collapses
  to a single card, since identical content hashes to one uid.

## Reaching it from other devices (Tailscale)

The server binds `127.0.0.1` and Tailscale proxies to it, so nothing is exposed
on the LAN or the public internet:

```bash
tailscale serve --bg --https=8777 http://127.0.0.1:8777
```

→ **https://johndoe-thinkpad-t520.tail14d815.ts.net:8777**

Reachable from any device signed into the tailnet (phone, laptop), from
anywhere, with a real TLS certificate. Tailscale handles identity, so the app
needs no login of its own. To take it down: `tailscale serve --https=8777 off`.

This is `serve`, not `funnel` — the public internet cannot reach it. Funnel
would need a password gate first, since anyone with the URL could otherwise
grade cards and wreck the scheduling. Ports 443 and 8443 are already funneled to
other services on this machine; 10000 is the only funnel port left if you ever
want one.

Because it runs from a phone, audio uses a single reusable `<audio>` element:
iOS grants playback permission per element after a user gesture, so autoplay
keeps working after the first tap.

## Keeping it running

A user-level systemd unit at `~/.config/systemd/user/korean-anki.service` starts
it at boot (user lingering is on, so no login required):

```bash
systemctl --user status korean-anki      # is it up?
systemctl --user restart korean-anki     # after editing server code
journalctl --user -u korean-anki -f      # logs
systemctl --user disable --now korean-anki
```

## Phone layout

Laid out and verified at 430×932 CSS px — the iPhone 15 Pro Max viewport —
driven in a same-origin iframe, since headless Firefox clamps its own window to
about 500px wide and never reports a narrower viewport.

- Deck rows stack the counts and Study button under the deck name. At full width
  the row overflowed the screen by ~100px and pushed Study off the right edge.
- The answer buttons sit in a sticky footer, so a long card (the honorific and
  idiom decks are the worst) never pushes them below the fold.
- Every target clears 44px, and the number input is 16px so iOS doesn't zoom the
  page when you focus it.
- Tapping the card reveals the answer — the touch equivalent of `space`. The
  keyboard hint line and the `1`–`4` key chips hide on coarse-pointer devices.
- `viewport-fit=cover` plus `env(safe-area-inset-*)` padding keeps content clear
  of the Dynamic Island and the home indicator.
- "Add to Home Screen" gets an icon and opens without browser chrome
  (`apple-touch-icon.png`, `apple-mobile-web-app-capable`).

Two bugs the phone work exposed, both fixed and both present on desktop too:
`#controls` (flex) and `#grades` (grid) carry their own `display`, which beat the
UA's `[hidden]` rule — "Show answer" and the grade buttons rendered at the same
time. And a deck with nothing due had a disabled button, which made its own
new-cards/day and reset controls unreachable; a finished deck now still opens.

## Fixes from the review pass

Found by running the API against an isolated copy (`--deck-dir` on a scratch
directory) rather than by reading the code:

- **Concurrent requests corrupted the sqlite connection.** One connection is
  shared by every request thread, and sqlite3 objects are not thread-safe: eight
  simultaneous clients produced 169 `InterfaceError` tracebacks and dropped
  responses. All database access now runs under a single `store.lock`. This was
  reachable in normal use the moment a phone and a laptop were both open.
- **A raising handler answered nothing at all.** Malformed JSON, a missing
  `grade`, or a non-numeric grade killed the connection with no status line, so
  the client hung. `do_GET`/`do_POST` now wrap the routes and return 400 or 500.
- **Answers for cards that no longer exist wrote orphan scheduling rows.** A tab
  left open across a deck rebuild could schedule a deleted card; `/api/answer`
  now checks the card belongs to the deck and returns 404, and the page moves to
  the next card instead of alerting.
- **Media directories accumulated.** They are named for the deck file's hash, so
  every rebuild stranded the previous run's audio — about 35MB per v2 rebuild.
  `sync_library` now drops directories no live deck refers to.
- **"Nothing due" hid the fact that cards were coming back.** After the daily
  allowance the deck looked finished, with no hint that 15 cards return in ten
  minutes. Counts now carry `waiting` and `next_due_in`; the deck row reads
  "in 10m" and the finished screen says how many are still in learning.
- **Two .apkg files claiming one deck name** silently deleted the first one's
  cards. It now warns at import which file won. (Nothing in this repo collides.)
