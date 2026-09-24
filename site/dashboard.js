const format = (value) => new Intl.NumberFormat("ko-KR").format(value);

function songMarkup(song) {
  const artist = song.artist || "아티스트 정보 없음";
  return `<div><p class="song-title">${song.title}</p><p class="song-artist">${artist}</p></div><strong class="song-count">${format(song.count)}</strong>`;
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
  renderYears(data.years);
}

init().catch((error) => {
  document.querySelector("main").insertAdjacentHTML("beforeend", `<p class="footer-note">데이터를 불러오지 못했습니다: ${error.message}</p>`);
});
