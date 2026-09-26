const format = (value) => new Intl.NumberFormat("ko-KR").format(value);

function escapeHtml(value) {
  return String(value ?? "").replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function songMarkup(song) {
  const artist = song.artist || "아티스트 정보 없음";
  return `<div><p class="song-title">${escapeHtml(song.title)}</p><p class="song-artist">${escapeHtml(artist)}</p></div><strong class="song-count">${format(song.count)}</strong>`;
}

function renderTagProfile(profile) {
  const total = profile.denominator;
  document.querySelector("#tag-coverage").textContent = `${total}/${profile.inventoryCount}`;
  document.querySelector("#tag-explanation").textContent =
    "agy의 Google 검색으로 수집한 장르와 분위기·특징입니다. AI 검색 후보를 한국어로 통일해 표시합니다.";
  const renderChart = (selector, axis) => {
    const tags = profile.tags.filter((tag) => tag.axis === axis).slice(0, 8);
    document.querySelector(selector).innerHTML = tags.length
    ? tags.map((tag) => `
      <div class="tag-row">
        <div class="tag-row-head"><span>${escapeHtml(tag.name)}</span><strong>${tag.songCount}/${total} · ${tag.percent}%</strong></div>
        <div class="tag-track" role="img" aria-label="${escapeHtml(tag.name)}: ${tag.songCount}곡, ${tag.percent}%">
          <span class="tag-fill" style="width: ${tag.percent}%"></span>
        </div>
      </div>`).join("")
    : '<p class="tag-empty">수집된 태그가 없습니다.</p>';
  };
  renderChart("#tag-chart", "genre");
  renderChart("#mood-chart", "mood");
  document.querySelector("#tag-genre-note").textContent =
    `조회한 ${total}개 악곡 중 태그가 있는 곡 수 기준 · 각 상위 8개 태그 · 한 곡에 여러 태그가 있어 비율 합계는 100%를 넘을 수 있습니다.`;
  const renderSongs = (query = "") => {
    const term = query.trim().toLocaleLowerCase();
    const songs = profile.songs.filter((song) => [song.title, song.artist, ...song.genres, ...song.mood_tags].join(" ").toLocaleLowerCase().includes(term));
    document.querySelector("#feature-result-count").textContent = `${songs.length} / ${total}`;
    document.querySelector("#feature-empty").hidden = songs.length > 0;
    document.querySelector("#tag-songs").innerHTML = songs.map((song) => {
      const chips = (tags, kind) => tags.map((tag) => `<span class="tag-chip ${kind}">${escapeHtml(tag)}</span>`).join("");
      const genres = chips(song.genres, "genre-chip") || '<span class="tag-unavailable">장르 정보 없음</span>';
      const moods = chips(song.mood_tags, "mood-chip") || '<span class="tag-unavailable">특징 정보 없음</span>';
      return `<li><div class="feature-song-heading"><strong>${escapeHtml(song.title)}</strong><span class="tag-song-artist">${escapeHtml(song.artist || "아티스트 정보 없음")}</span></div><div class="tag-song-detail"><div class="tag-chips" aria-label="장르">${genres}</div><div class="tag-chips" aria-label="분위기와 특징">${moods}</div><a href="${escapeHtml(song.sourceUrl)}" target="_blank" rel="noopener noreferrer">Google 검색 · AI 후보</a></div></li>`;
    }).join("");
  };
  renderSongs();
  document.querySelector("#feature-search").addEventListener("input", (event) => renderSongs(event.target.value));
}

function renderTopSongs(songs) {
  document.querySelector("#top-songs").innerHTML = songs
    .map((song) => `<li class="ranking-item">${songMarkup(song)}</li>`)
    .join("");
}

function renderYears(years) {
  document.querySelector("#year-lists").innerHTML = years
    .map(({ year, songs }) => `<section class="year-block"><h3>${year}</h3><ol>${songs.map((song) => `<li>${songMarkup(song)}</li>`).join("")}</ol></section>`)
    .join("");
}

async function init() {
  const response = await fetch("data.json");
  if (!response.ok) throw new Error("Unable to load dashboard data");
  const data = await response.json();
  document.querySelector("#broadcast-count").textContent = format(data.broadcastCount);
  document.querySelector("#performance-count").textContent = format(data.performanceCount);
  document.querySelector("#song-count").textContent = format(data.songCount);
  renderTopSongs(data.topSongs);
  renderTagProfile(data.tagProfile);
  renderYears(data.years);
}

init().catch((error) => {
  document.querySelector("main").insertAdjacentHTML("beforeend", `<p class="footer-note">데이터를 불러오지 못했습니다: ${escapeHtml(error.message)}</p>`);
});
