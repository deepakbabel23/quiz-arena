// Quiz Arena front end: plain JavaScript, no build step.
const $ = (id) => document.getElementById(id);
let gameId = null;
let shownAt = 0;
let timerHandle = null;

async function api(path, options = {}) {
  const res = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error((await res.json()).detail || res.statusText);
  return res.json();
}

async function loadPacks() {
  const packs = await api("/api/packs");
  $("pack").replaceChildren(
    ...packs.map((p) => new Option(`${p.title} (${p.questions})`, p.id)),
  );
  await loadLeaderboard();
}

async function loadLeaderboard() {
  const rows = await api(`/api/leaderboard/${$("pack").value}`);
  $("leaders").replaceChildren(
    ...rows.map((r) => {
      const li = document.createElement("li");
      li.textContent = `${r.player}: ${r.score}`;
      return li;
    }),
  );
}

function startTimer() {
  clearInterval(timerHandle);
  shownAt = performance.now();
  timerHandle = setInterval(() => {
    const left = Math.max(0, 20 - Math.floor((performance.now() - shownAt) / 1000));
    $("timer").textContent = left;
  }, 250);
}

async function showQuestion() {
  const q = await api(`/api/games/${gameId}/question`);
  if (q.finished) return finish(q.score);
  $("progress").textContent = `Question ${q.number}/${q.total}`;
  $("score").textContent = q.score;
  $("question").textContent = q.text;
  $("feedback").textContent = "";
  $("choices").replaceChildren(
    ...q.choices.map((text, i) => {
      const b = document.createElement("button");
      b.textContent = text;
      b.onclick = () => answer(i);
      return b;
    }),
  );
  startTimer();
}

async function answer(choice) {
  const seconds = (performance.now() - shownAt) / 1000;
  const r = await api(`/api/games/${gameId}/answer`, {
    method: "POST",
    body: JSON.stringify({ choice, seconds_taken: seconds }),
  });
  $("feedback").textContent = r.correct ? `Correct! +${r.points}` : "Wrong answer";
  $("feedback").className = r.correct ? "correct" : "wrong";
  setTimeout(showQuestion, 700);
}

function finish(score) {
  clearInterval(timerHandle);
  $("play").hidden = true;
  $("done").hidden = false;
  $("final").textContent = score;
  loadLeaderboard();
}

$("start").onclick = async () => {
  try {
    const g = await api("/api/games", {
      method: "POST",
      body: JSON.stringify({ player: $("player").value.trim(), pack: $("pack").value }),
    });
    gameId = g.game_id;
    $("setup").hidden = true;
    $("done").hidden = true;
    $("play").hidden = false;
    showQuestion();
  } catch (err) {
    alert(err.message);
  }
};

$("again").onclick = () => {
  $("done").hidden = true;
  $("setup").hidden = false;
};

$("pack").onchange = loadLeaderboard;
loadPacks();
