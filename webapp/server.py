#!/usr/bin/env python3
"""Local Anki-style study server for the .apkg decks in this repo.

    python3 webapp/server.py            # http://127.0.0.1:8777
    python3 webapp/server.py --port 9000 --deck-dir some/other/dir

No third-party packages. Study progress lives in webapp/data/study.db.
"""

import argparse
import json
import mimetypes
import os
import posixpath
import re
import sys
import traceback
import urllib.parse
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import store  # noqa: E402

REPO = os.path.dirname(HERE)
DATA = os.path.join(HERE, "data")
MEDIA = os.path.join(DATA, "media")
STATIC = os.path.join(HERE, "static")


class BadRequest(Exception):
    pass


def find_decks(dirs):
    """(sort_hint, path) for every .apkg found, ordered by dir then filename."""
    out = []
    for prefix, d in enumerate(dirs):
        if not os.path.isdir(d):
            continue
        for name in sorted(os.listdir(d)):
            if name.endswith(".apkg"):
                out.append(("%d:%s" % (prefix, name), os.path.join(d, name)))
    return out


class Handler(BaseHTTPRequestHandler):
    con = None
    deck_dirs = ()

    def log_message(self, fmt, *args):
        pass

    # --- helpers ---
    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, cache=False):
        if not os.path.isfile(path):
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        with open(path, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        if cache:
            self.send_header("Cache-Control", "max-age=86400")
        self.end_headers()
        self.wfile.write(body)

    # --- routing ---
    def do_GET(self):
        """Wrapper: a handler that raises must still answer, or the client just
        sees the connection drop with no status at all."""
        try:
            self.route_get()
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            self.send_json({"error": "server error"}, 500)

    def do_POST(self):
        try:
            self.route_post()
        except (BadRequest, json.JSONDecodeError, KeyError, TypeError, ValueError) as e:
            self.send_json({"error": "bad request: %s" % e}, 400)
        except BrokenPipeError:
            pass
        except Exception:
            traceback.print_exc()
            self.send_json({"error": "server error"}, 500)

    def route_get(self):
        url = urllib.parse.urlparse(self.path)
        q = urllib.parse.parse_qs(url.query)
        path = url.path

        if path == "/":
            return self.send_file(os.path.join(STATIC, "index.html"))
        if path in ("/app.js", "/app.css", "/apple-touch-icon.png"):
            return self.send_file(os.path.join(STATIC, path[1:]), cache=path.endswith(".png"))
        if path.startswith("/media/"):
            rel = urllib.parse.unquote(path[len("/media/") :])
            safe = posixpath.normpath(rel).lstrip("/")
            if safe.startswith(".."):
                return self.send_error(403)
            return self.send_file(os.path.join(MEDIA, *safe.split("/")), cache=True)

        if path == "/api/decks":
            decks = []
            with store.lock:
                rows = self.con.execute("select * from decks order by sort").fetchall()
                for row in rows:
                    c = store.counts(self.con, row["key"])
                    c.update(
                        key=row["key"],
                        name=row["name"],
                        source=os.path.relpath(row["source"], REPO),
                    )
                    decks.append(c)
                stats = store.stats(self.con)
            return self.send_json({"decks": decks, "stats": stats})

        if path == "/api/next":
            deck_key = q.get("deck", [""])[0]
            with store.lock:
                row = store.next_card(self.con, deck_key)
                if row is None:
                    return self.send_json(
                        {"card": None, "counts": store.counts(self.con, deck_key)}
                    )
                buttons = store.intervals_preview(self.con, row["uid"])
                counts = store.counts(self.con, deck_key)
            card = {
                "uid": row["uid"],
                "front": row["front"],
                "back": row["back"],
                "css": row["css"],
                "front_sounds": json.loads(row["front_sounds"]),
                "back_sounds": json.loads(row["back_sounds"]),
                "state": row["state"] or "new",
                "buttons": buttons,
            }
            return self.send_json({"card": card, "counts": counts})

        self.send_error(404)

    def route_post(self):
        url = urllib.parse.urlparse(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        if length > 1 << 20:
            raise BadRequest("body too large")
        payload = json.loads(self.rfile.read(length) or "{}")
        if not isinstance(payload, dict):
            raise BadRequest("expected a JSON object")

        if url.path == "/api/answer":
            grade = int(payload["grade"])
            if grade not in (1, 2, 3, 4):
                raise BadRequest("grade must be 1-4")
            deck, uid = str(payload["deck"]), str(payload["uid"])
            with store.lock:
                # A tab left open across a deck rebuild can answer a card that
                # no longer exists; refuse rather than write orphan state.
                known = self.con.execute(
                    "select 1 from cards where uid=? and deck_key=?", (uid, deck)
                ).fetchone()
                if not known:
                    return self.send_json({"error": "unknown card"}, 404)
                store.answer(self.con, uid, deck, grade)
                return self.send_json({"counts": store.counts(self.con, deck)})

        if url.path == "/api/settings":
            # "decks" sets a whole unit in one call; "deck" is the single-deck
            # form the study screen still uses.
            keys = payload.get("decks")
            keys = [str(k) for k in keys] if keys else [str(payload["deck"])]
            if not keys:
                raise BadRequest("no deck given")
            n = int(payload["new_per_day"])
            with store.lock:
                for k in keys:
                    store.set_new_per_day(self.con, k, n)
                return self.send_json({"counts": store.counts(self.con, keys[0])})

        if url.path == "/api/reset":
            deck = str(payload["deck"])
            with store.lock:
                self.con.execute(
                    "delete from sched where uid in (select uid from cards where deck_key=?)",
                    (deck,),
                )
                self.con.execute("delete from revlog where deck_key=?", (deck,))
                self.con.commit()
                return self.send_json({"counts": store.counts(self.con, deck)})

        self.send_error(404)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8777)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument(
        "--deck-dir",
        action="append",
        default=None,
        help="directory of .apkg files (repeatable); defaults to v2/build/",
    )
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args()

    # v2/build only. The v1 decks in decks/ cover the same ground with worse
    # cards, and 26 decks in one list is unusable; --deck-dir brings them back.
    dirs = args.deck_dir or [os.path.join(REPO, "v2", "build")]
    os.makedirs(MEDIA, exist_ok=True)
    con = store.connect(os.path.join(DATA, "study.db"))

    files = find_decks(dirs)
    print("Scanning %s" % ", ".join(os.path.relpath(d, REPO) for d in dirs))
    added = store.sync_library(con, files, MEDIA)
    for path in added:
        print("  imported %s" % os.path.relpath(path, REPO))
    total = con.execute("select count(*) from cards").fetchone()[0]
    ndecks = con.execute("select count(*) from decks").fetchone()[0]
    print("%d decks, %d cards ready" % (ndecks, total))

    Handler.con = con
    Handler.deck_dirs = dirs
    url = "http://%s:%d/" % (args.host, args.port)
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    print("Serving %s   (ctrl-c to stop)" % url)
    if not args.no_browser:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")


if __name__ == "__main__":
    main()
