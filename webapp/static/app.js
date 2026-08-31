const $ = (id) => document.getElementById(id);
const state = { deck: null, card: null, shown: false, sounds: [] };

async function api(path, body) {
  const opts = body ? { method: "POST", body: JSON.stringify(body) } : {};
  try {
    const r = await fetch(path, opts);
    const data = await r.json();
    if (!r.ok) throw new Error(data.error || r.status);
    return data;
  } catch (e) {
    // Phones drop connections when they sleep or switch networks -- say so
    // rather than leaving a half-rendered card on screen.
    throw new Error(e.message || "network error");
  }
}

// --- deck list ---
// Decks arrive flat, named "HTSK Korean::Unit 1 - ...::Lesson 01 - ...". Any
// deck with a parent path is folded into a collapsible group, so a 25-lesson
// unit reads as one row until you open it. A flat-named deck renders on its own.
const OPEN_KEY = "openGroups";

function openGroups() {
  try {
    return new Set(JSON.parse(localStorage.getItem(OPEN_KEY) || "[]"));
  } catch (e) {
    return new Set();
  }
}

function setGroupOpen(path, open) {
  const s = openGroups();
  open ? s.add(path) : s.delete(path);
  try {
    localStorage.setItem(OPEN_KEY, JSON.stringify([...s]));
  } catch (e) {}
}

function groupDecks(decks) {
  const groups = new Map();
  const loose = [];
  for (const d of decks) {
    const parts = d.name.split("::");
    if (parts.length < 2) {
      loose.push(d);
      continue;
    }
    const path = parts.slice(0, -1).join("::");
    if (!groups.has(path))
      groups.set(path, { path, label: parts[parts.length - 2], decks: [] });
    groups.get(path).decks.push(Object.assign({}, d, { leaf: parts[parts.length - 1] }));
  }
  return { groups: [...groups.values()], loose };
}

const PILL_LABEL = { new: "new", learn: "learning", due: "due" };
const pill = (n, cls) =>
  `<span class="pill ${cls} ${n ? "" : "zero"}" title="${PILL_LABEL[cls]}">${n}</span>`;

function deckRow(d, label, withSource) {
  const ready = d.new + d.learn + d.due;
  const btnText = ready ? "Study" : d.waiting ? "in " + d.next_due_in : "Done";
  const sub = withSource ? esc(d.source) + " · " + d.total + " cards" : d.total + " cards";
  return `<div class="deck">
    <div class="name">${esc(label)}<span class="src">${sub}</span></div>
    ${pill(d.new, "new")}${pill(d.learn, "learn")}${pill(d.due, "due")}
    <button class="study ${ready ? "" : "empty"}" data-key="${d.key}" data-name="${esc(d.name)}"
      title="${d.waiting ? d.waiting + " card(s) still in learning" : ""}">${btnText}</button>
  </div>`;
}

function groupBlock(g, open) {
  const sum = (k) => g.decks.reduce((a, d) => a + d[k], 0);
  // One box for the whole unit unless its lessons disagree, in which case it
  // shows empty rather than pretending they share a value.
  const vals = [...new Set(g.decks.map((d) => d.new_per_day))];
  const npd = vals.length === 1 ? vals[0] : "";
  return `<div class="group" data-path="${esc(g.path)}">
    <div class="group-head" role="button" tabindex="0" aria-expanded="${open}">
      <span class="chev">${open ? "▾" : "▸"}</span>
      <div class="name">${esc(g.label)}
        <span class="src">${g.decks.length} lessons · ${sum("total")} cards</span></div>
      ${pill(sum("new"), "new")}${pill(sum("learn"), "learn")}${pill(sum("due"), "due")}
      <div class="npd">
        <label>new/day</label>
        <input type="number" min="0" max="9999" value="${npd}" placeholder="mixed">
        <button class="ghost save">Save</button>
      </div>
    </div>
    <div class="group-body"${open ? "" : " hidden"}>
      ${g.decks.map((d) => deckRow(d, d.leaf, false)).join("")}
    </div>
  </div>`;
}

async function showDecks() {
  state.deck = null;
  $("study-view").hidden = true;
  $("deck-view").hidden = false;
  const data = await api("/api/decks");
  $("stats").innerHTML =
    `<div><b>${data.stats.reviews_today}</b><div class="muted">reviews today</div></div>` +
    `<div><b>${data.stats.in_review}</b><div class="muted">cards in review</div></div>` +
    `<div><b>${data.stats.reviews_total}</b><div class="muted">reviews all time</div></div>`;
  $("header-info").innerHTML =
    `${data.decks.length} decks &nbsp;·&nbsp; ` +
    `<span class="pill new">new</span> <span class="pill learn">learning</span> <span class="pill due">due</span>`;
  const { groups, loose } = groupDecks(data.decks);
  const open = openGroups();
  $("decks").innerHTML =
    groups.map((g) => groupBlock(g, open.has(g.path))).join("") +
    loose.map((d) => deckRow(d, d.name, true)).join("");
  bindDeckList();
}

function bindDeckList() {
  document.querySelectorAll("button.study").forEach((b) =>
    b.addEventListener("click", () => startDeck(b.dataset.key, b.dataset.name))
  );
  document.querySelectorAll(".group").forEach((el) => {
    const head = el.querySelector(".group-head");
    const body = el.querySelector(".group-body");
    const toggle = () => {
      const open = body.hidden;
      body.hidden = !open;
      el.querySelector(".chev").textContent = open ? "▾" : "▸";
      head.setAttribute("aria-expanded", String(open));
      setGroupOpen(el.dataset.path, open);
    };
    head.addEventListener("click", (e) => {
      if (e.target.closest(".npd")) return; // the settings box is not a toggle
      toggle();
    });
    head.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggle();
      }
    });
    el.querySelector(".npd .save").addEventListener("click", async () => {
      const v = el.querySelector(".npd input").value;
      if (v === "") return;
      const keys = [...el.querySelectorAll("button.study")].map((b) => b.dataset.key);
      await api("/api/settings", { decks: keys, new_per_day: +v });
      showDecks();
    });
  });
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// --- study ---
async function startDeck(key, name) {
  state.deck = key;
  $("deck-view").hidden = true;
  $("study-view").hidden = false;
  $("study-title").textContent = name;
  location.hash = "#deck=" + key;
  await nextCard();
}

async function nextCard() {
  let data;
  try {
    data = await api("/api/next?deck=" + encodeURIComponent(state.deck));
  } catch (e) {
    $("card").innerHTML = `<p class="muted">Couldn't reach the server (${esc(e.message)}).</p>`;
    $("controls").hidden = true;
    return;
  }
  renderCounts(data.counts);
  state.card = data.card;
  state.shown = false;
  if (!data.card) {
    $("card-area").hidden = true;
    $("controls").hidden = true;
    $("audio-row").innerHTML = "";
    $("done").hidden = false;
    const waiting = data.counts.waiting
      ? `<p>${data.counts.waiting} card${data.counts.waiting > 1 ? "s" : ""} still in learning — ` +
        `the next one is back in ${data.counts.next_due_in}.</p>`
      : data.counts.next_due_in
      ? `<p>Next review in ${data.counts.next_due_in}.</p>`
      : "";
    $("done").innerHTML =
      `<p>Nothing due in this deck right now.</p>` + waiting +
      `<div class="settings">New cards/day
         <input id="npd" type="number" min="0" max="9999" value="${data.counts.new_per_day}">
         <button class="ghost" id="save-npd">Save</button>
         <button class="ghost" id="reset-deck">Reset progress</button></div>`;
    $("save-npd").onclick = async () => {
      await api("/api/settings", { deck: state.deck, new_per_day: +$("npd").value });
      nextCard();
    };
    $("reset-deck").onclick = async () => {
      if (!confirm("Erase all scheduling for this deck?")) return;
      await api("/api/reset", { deck: state.deck });
      nextCard();
    };
    return;
  }
  $("card-area").hidden = false;
  $("controls").hidden = false;
  $("done").hidden = true;
  $("card-css").textContent = data.card.css || "";
  $("card").className = "card" + (matchMedia("(prefers-color-scheme: dark)").matches ? " nightMode night_mode" : "");
  $("card").innerHTML = data.card.front;
  $("show").hidden = false;
  $("grades").hidden = true;
  const b = data.card.buttons;
  document.querySelectorAll("button.grade").forEach((btn) => {
    btn.querySelector("span").textContent = b[btn.dataset.grade];
  });
  setSounds(data.card.front_sounds, true);
}

function renderCounts(c) {
  $("queue-counts").innerHTML =
    `<b class="n" title="new">${c.new}</b>·<b class="l" title="learning">${c.learn}</b>` +
    `·<b class="d" title="due">${c.due}</b>`;
}

function setSounds(list, autoplay) {
  state.sounds = list || [];
  $("audio-row").innerHTML = state.sounds
    .map((s, i) => `<button data-i="${i}">▶ audio${state.sounds.length > 1 ? " " + (i + 1) : ""}</button>`)
    .join("");
  document.querySelectorAll("#audio-row button").forEach((b) =>
    b.addEventListener("click", () => play(+b.dataset.i))
  );
  if (autoplay && state.sounds.length) play(0);
}

// One reusable element: iOS only lets audio play after a user gesture, and the
// permission sticks to the element -- so a fresh Audio() per card stays silent
// on a phone while this one keeps working after the first tap.
const player = new Audio();
function play(i) {
  if (!state.sounds[i]) return;
  player.pause();
  player.src = "/media/" + state.sounds[i].split("/").map(encodeURIComponent).join("/");
  player.play().catch(() => {});
}
function unlockAudio() {
  player.play().catch(() => {});
  player.pause();
}
document.addEventListener("pointerdown", unlockAudio, { once: true });
document.addEventListener("keydown", unlockAudio, { once: true });

function showAnswer() {
  if (!state.card || state.shown) return;
  state.shown = true;
  $("card").innerHTML = state.card.back;
  $("show").hidden = true;
  $("grades").hidden = false;
  const back = state.card.back_sounds || [];
  const fresh = back.filter((s) => !(state.card.front_sounds || []).includes(s));
  setSounds(back.length ? back : state.card.front_sounds, fresh.length > 0);
}

async function grade(g) {
  if (!state.card || !state.shown) return;
  const card = state.card;
  state.card = null;
  try {
    await api("/api/answer", { uid: card.uid, deck: state.deck, grade: g });
  } catch (e) {
    if (!/unknown card/.test(e.message)) {
      state.card = card; // keep the card up so the answer isn't silently lost
      alert("Couldn't save that answer: " + e.message);
      return;
    }
    // the deck was rebuilt under us -- just move on
  }
  await nextCard();
}

document.addEventListener("keydown", (e) => {
  if ($("study-view").hidden) return;
  if (e.key === " " || e.key === "Enter") {
    e.preventDefault();
    state.shown ? grade(3) : showAnswer();
  } else if ("1234".includes(e.key)) {
    state.shown ? grade(+e.key) : showAnswer();
  } else if (e.key === "r") {
    play(0);
  }
});

$("show").addEventListener("click", showAnswer);
// Tapping the card reveals it -- the phone equivalent of pressing space.
$("card-area").addEventListener("click", (e) => {
  if (e.target.closest("a, button, audio")) return;
  if (!state.shown) showAnswer();
});
document.querySelectorAll("button.grade").forEach((b) =>
  b.addEventListener("click", () => grade(+b.dataset.grade))
);
$("back").addEventListener("click", showDecks);
$("home-link").addEventListener("click", (e) => { e.preventDefault(); location.hash = ""; showDecks(); });

showDecks();
