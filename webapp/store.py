"""Study database: imported cards plus an SM-2 scheduler.

Scheduling state is keyed on a content hash (deck name + template ordinal +
note fields), not on the Anki card id, so rebuilding a deck's .apkg keeps the
progress of every card whose text did not change.
"""

import hashlib
import json
import os
import shutil
import sqlite3
import threading
import time

import apkg

DAY = 86400.0
LEARN_STEPS = (60.0, 600.0)  # again -> 1 min, good -> 10 min, then graduate
GRADUATING_IVL = 1.0
EASY_IVL = 4.0

SCHEMA = """
create table if not exists decks (
  key text primary key, name text, source text, file_key text, sort text
);
create table if not exists cards (
  uid text primary key, deck_key text, ord integer, sort integer,
  front text, back text, css text, front_sounds text, back_sounds text
);
create table if not exists sched (
  uid text primary key, state text, due real, ivl real, ease real,
  reps integer, lapses integer, step integer, last real
);
create table if not exists revlog (
  id integer primary key autoincrement, uid text, deck_key text,
  ts real, grade integer, ivl real, state text
);
create table if not exists settings (deck_key text primary key, new_per_day integer);
create index if not exists cards_deck on cards(deck_key);
create index if not exists revlog_ts on revlog(ts);
"""


# One connection is shared by every request thread, and sqlite3 objects are not
# thread-safe: concurrent use raises InterfaceError and drops the response. The
# work here is microseconds of local I/O, so a single lock costs nothing.
lock = threading.RLock()


def connect(path):
    con = sqlite3.connect(path, check_same_thread=False)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def day_start(now=None):
    """Study days roll over at 4am local time, like Anki's default."""
    now = now or time.time()
    lt = time.localtime(now - 4 * 3600)
    midnight = time.mktime((lt.tm_year, lt.tm_mon, lt.tm_mday, 0, 0, 0, 0, 0, -1))
    return midnight + 4 * 3600


# --- import ---------------------------------------------------------------


def _uid(deck_name, ordv, fields):
    raw = "%s|%d|%s" % (deck_name, ordv, "\x1f".join(fields))
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def import_file(con, path, media_root, sort_hint):
    """Import one .apkg. Returns list of deck keys touched."""
    key = apkg.file_key(path)
    name_guess = os.path.splitext(os.path.basename(path))[0]
    media_dir = os.path.join(media_root, key)
    decks, models, notes, cards = apkg.read(path, media_dir)

    by_deck = {}
    for card in cards:
        note = notes.get(card["nid"])
        if not note:
            continue
        model = models.get(note["mid"])
        if not model:
            continue
        tmpls = model["tmpls"]
        ordv = card["ord"]
        tmpl = tmpls[ordv] if ordv < len(tmpls) else tmpls[0]
        if model.get("type") == 1:  # cloze: one template, many card ordinals
            tmpl = tmpls[0]
        fields = dict(zip([f["name"] for f in model["flds"]], note["fields"]))

        front = apkg.render(tmpl["qfmt"], fields, model, ordv)
        if apkg.is_empty(front):
            continue
        back = apkg.render(tmpl["afmt"], fields, model, ordv, front_side=front)
        deck_name = decks.get(card["did"], {}).get("name") or name_guess
        by_deck.setdefault(deck_name, []).append(
            {
                "uid": _uid(deck_name, ordv, note["fields"]),
                "ord": ordv,
                "front": apkg.strip_sounds(front),
                "back": apkg.strip_sounds(back),
                "css": model.get("css", ""),
                "front_sounds": [key + "/" + s for s in apkg.sounds(front)],
                "back_sounds": [key + "/" + s for s in apkg.sounds(back)],
            }
        )

    touched = []
    for deck_name, rows in by_deck.items():
        if not rows:
            continue
        deck_key = hashlib.sha1(deck_name.encode()).hexdigest()[:12]
        prior = con.execute("select source from decks where key=?", (deck_key,)).fetchone()
        if prior and prior["source"] != os.path.abspath(path):
            print("  warning: %r is also the deck name in %s -- the newer file wins"
                  % (deck_name, os.path.relpath(prior["source"], os.path.dirname(media_root))))
        con.execute(
            "insert or replace into decks (key, name, source, file_key, sort) values (?,?,?,?,?)",
            (deck_key, deck_name, os.path.abspath(path), key, sort_hint),
        )
        con.execute("delete from cards where deck_key=?", (deck_key,))
        con.executemany(
            "insert or replace into cards"
            " (uid, deck_key, ord, sort, front, back, css, front_sounds, back_sounds)"
            " values (?,?,?,?,?,?,?,?,?)",
            [
                (
                    r["uid"], deck_key, r["ord"], i, r["front"], r["back"], r["css"],
                    json.dumps(r["front_sounds"]), json.dumps(r["back_sounds"]),
                )
                for i, r in enumerate(rows)
            ],
        )
        touched.append(deck_key)
    con.commit()
    return touched


def sync_library(con, files, media_root):
    """Import any .apkg that is new or changed since the last run."""
    known = {r["source"]: r["file_key"] for r in con.execute("select source, file_key from decks")}
    added = []
    for sort_hint, path in files:
        path = os.path.abspath(path)
        if known.get(path) == apkg.file_key(path):
            continue
        import_file(con, path, media_root, sort_hint)
        added.append(path)
    # forget decks whose file disappeared
    live = {os.path.abspath(p) for _, p in files}
    for row in con.execute("select key, source from decks").fetchall():
        if row["source"] not in live:
            con.execute("delete from cards where deck_key=?", (row["key"],))
            con.execute("delete from decks where key=?", (row["key"],))
    con.commit()

    # Media lives under a directory named for the deck file's hash, so every
    # rebuild of a deck strands the previous run's audio. Drop what no live
    # deck refers to -- otherwise v2/build/ rebuilds pile up ~35MB a time.
    # scheduling for cards that no longer exist anywhere
    con.execute("delete from sched where uid not in (select uid from cards)")
    con.execute("delete from revlog where deck_key not in (select key from decks)")
    con.commit()

    keep = {r["file_key"] for r in con.execute("select file_key from decks")}
    for name in os.listdir(media_root) if os.path.isdir(media_root) else []:
        if name not in keep:
            shutil.rmtree(os.path.join(media_root, name), ignore_errors=True)
    return added


# --- scheduling -----------------------------------------------------------


# Effectively "no daily gate": high enough that the allowance never binds for a
# deck of any realistic size. A per-deck limit can still be set from the UI.
DEFAULT_NEW_PER_DAY = 9999


def new_per_day(con, deck_key):
    row = con.execute("select new_per_day from settings where deck_key=?", (deck_key,)).fetchone()
    return row["new_per_day"] if row else DEFAULT_NEW_PER_DAY


def set_new_per_day(con, deck_key, n):
    con.execute(
        "insert or replace into settings (deck_key, new_per_day) values (?,?)", (deck_key, max(0, n))
    )
    con.commit()


def introduced_today(con, deck_key):
    return con.execute(
        "select count(distinct uid) from revlog where deck_key=? and ts>=? and state='new'",
        (deck_key, day_start()),
    ).fetchone()[0]


def counts(con, deck_key):
    now = time.time()
    row = con.execute(
        """
        select
          sum(case when s.uid is null then 1 else 0 end) as new,
          sum(case when s.state='learn' and s.due<=? then 1 else 0 end) as learn,
          sum(case when s.state='review' and s.due<=? then 1 else 0 end) as due,
          count(*) as total
        from cards c left join sched s on s.uid=c.uid where c.deck_key=?
        """,
        (now, now, deck_key),
    ).fetchone()
    allowance = max(0, new_per_day(con, deck_key) - introduced_today(con, deck_key))
    nxt = con.execute(
        "select min(s.due) from cards c join sched s on s.uid=c.uid"
        " where c.deck_key=? and s.due>? and s.state in ('learn','review')",
        (deck_key, now),
    ).fetchone()[0]
    return {
        "new": min(row["new"] or 0, allowance),
        "new_total": row["new"] or 0,
        "learn": row["learn"] or 0,
        "due": row["due"] or 0,
        "total": row["total"] or 0,
        "new_per_day": new_per_day(con, deck_key),
        "waiting": (row["total"] or 0) and con.execute(
            "select count(*) from cards c join sched s on s.uid=c.uid"
            " where c.deck_key=? and s.state='learn' and s.due>?",
            (deck_key, now),
        ).fetchone()[0],
        "next_due_in": humanize(nxt - now) if nxt else None,
    }


def next_card(con, deck_key):
    now = time.time()
    q = (
        "select c.*, s.state, s.due, s.ivl, s.ease, s.reps, s.step from cards c"
        " left join sched s on s.uid=c.uid where c.deck_key=? "
    )
    for where, order in (
        ("and s.state='learn' and s.due<=?", "order by s.due limit 1"),
        ("and s.state='review' and s.due<=?", "order by s.due limit 1"),
    ):
        row = con.execute(q + where + " " + order, (deck_key, now)).fetchone()
        if row:
            return row
    if max(0, new_per_day(con, deck_key) - introduced_today(con, deck_key)) > 0:
        row = con.execute(q + "and s.uid is null order by c.sort limit 1", (deck_key,)).fetchone()
        if row:
            return row
    return None


def answer(con, uid, deck_key, grade):
    """grade: 1 again, 2 hard, 3 good, 4 easy. Returns the new sched row."""
    now = time.time()
    row = con.execute("select * from sched where uid=?", (uid,)).fetchone()
    state = row["state"] if row else "new"
    before = state
    ivl = row["ivl"] if row else 0.0
    ease = row["ease"] if row else 2.5
    reps = row["reps"] if row else 0
    lapses = row["lapses"] if row else 0
    step = row["step"] if row else 0

    if state in ("new", "learn"):
        if grade == 1:
            step, state, due = 0, "learn", now + LEARN_STEPS[0]
        elif grade == 4:
            state, ivl, due = "review", EASY_IVL, now + EASY_IVL * DAY
        elif grade == 2:
            state, due = "learn", now + LEARN_STEPS[min(step, len(LEARN_STEPS) - 1)]
        else:
            step += 1
            if step >= len(LEARN_STEPS):
                state, ivl, due = "review", GRADUATING_IVL, now + GRADUATING_IVL * DAY
            else:
                state, due = "learn", now + LEARN_STEPS[step]
    else:
        if grade == 1:
            lapses += 1
            ease = max(1.3, ease - 0.2)
            state, step, ivl, due = "learn", 0, max(1.0, ivl * 0.5), now + LEARN_STEPS[0]
        else:
            if grade == 2:
                ease = max(1.3, ease - 0.15)
                ivl = max(ivl + 1, ivl * 1.2)
            elif grade == 3:
                ivl = max(ivl + 1, ivl * ease)
            else:
                ease = min(3.0, ease + 0.15)
                ivl = max(ivl + 1, ivl * ease * 1.3)
            ivl = min(ivl, 365.0)
            due = now + ivl * DAY

    reps += 1
    con.execute(
        "insert or replace into sched (uid, state, due, ivl, ease, reps, lapses, step, last)"
        " values (?,?,?,?,?,?,?,?,?)",
        (uid, state, due, ivl, ease, reps, lapses, step, now),
    )
    con.execute(
        "insert into revlog (uid, deck_key, ts, grade, ivl, state) values (?,?,?,?,?,?)",
        (uid, deck_key, now, grade, ivl, before),
    )
    con.commit()
    return {"state": state, "ivl": ivl, "due": due}


def intervals_preview(con, uid):
    """What each button would schedule, as a short human string."""
    row = con.execute("select * from sched where uid=?", (uid,)).fetchone()
    out = {}
    for grade in (1, 2, 3, 4):
        state = row["state"] if row else "new"
        ivl = row["ivl"] if row else 0.0
        ease = row["ease"] if row else 2.5
        step = row["step"] if row else 0
        if state in ("new", "learn"):
            if grade == 1:
                secs = LEARN_STEPS[0]
            elif grade == 4:
                secs = EASY_IVL * DAY
            elif grade == 2:
                secs = LEARN_STEPS[min(step, len(LEARN_STEPS) - 1)]
            else:
                nxt = step + 1
                secs = GRADUATING_IVL * DAY if nxt >= len(LEARN_STEPS) else LEARN_STEPS[nxt]
        else:
            if grade == 1:
                secs = LEARN_STEPS[0]
            elif grade == 2:
                secs = max(ivl + 1, ivl * 1.2) * DAY
            elif grade == 3:
                secs = max(ivl + 1, ivl * ease) * DAY
            else:
                secs = min(max(ivl + 1, ivl * ease * 1.3), 365.0) * DAY
        out[grade] = humanize(secs)
    return out


def humanize(secs):
    if secs < 3600:
        return "%dm" % max(1, round(secs / 60))
    if secs < DAY:
        return "%dh" % round(secs / 3600)
    days = secs / DAY
    if days < 30:
        return "%dd" % round(days)
    if days < 365:
        return "%.1fmo" % (days / 30.0)
    return "%.1fy" % (days / 365.0)


def stats(con):
    start = day_start()
    today = con.execute("select count(*) from revlog where ts>=?", (start,)).fetchone()[0]
    total = con.execute("select count(*) from revlog").fetchone()[0]
    learned = con.execute("select count(*) from sched where state='review'").fetchone()[0]
    return {"reviews_today": today, "reviews_total": total, "in_review": learned}
