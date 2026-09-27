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

// Split the longer edge into balanced groups, preserving exact count ratios.
function treemapLayout(items, x, y, width, height) {
  if (!items.length) return [];
  if (items.length === 1) return [{ tag: items[0], x, y, width, height }];
  const total = items.reduce((sum, tag) => sum + tag.songCount, 0);
  let split = 1;
  let weight = items[0].songCount;
  while (split < items.length - 1 &&
    Math.abs(weight + items[split].songCount - total / 2) < Math.abs(weight - total / 2)) {
    weight += items[split++].songCount;
  }
  const ratio = weight / total;
  return width >= height
    ? [...treemapLayout(items.slice(0, split), x, y, width * ratio, height),
       ...treemapLayout(items.slice(split), x + width * ratio, y, width * (1 - ratio), height)]
    : [...treemapLayout(items.slice(0, split), x, y, width, height * ratio),
       ...treemapLayout(items.slice(split), x, y + height * ratio, width, height * (1 - ratio))];
}

function renderTreemap(selector, tags, axis) {
  const chart = document.querySelector(selector);
  const items = tags.filter((tag) => tag.axis === axis && Number.isFinite(tag.songCount) && tag.songCount > 0)
    .sort((a, b) => b.songCount - a.songCount);
  if (!items.length) {
    chart.innerHTML = '<p class="tag-empty">수집된 태그가 없습니다.</p>';
    return;
  }
  const tooltip = document.createElement('div');
  tooltip.className = 'treemap-tooltip';
  tooltip.id = `${chart.id}-tooltip`;
  tooltip.setAttribute('role', 'tooltip');
  tooltip.hidden = true;
  let activeTile;
  const hide = () => { tooltip.hidden = true; activeTile = null; };
  const tiles = items.map((tag) => {
    const tile = document.createElement('button');
    tile.type = 'button';
    tile.className = 'treemap-tile';
    const label = `${tag.name} · ${tag.songCount}곡 · ${tag.percent}%`;
    tile.setAttribute('aria-label', label);
    tile.setAttribute('aria-describedby', tooltip.id);
    tile.innerHTML = `<span class="treemap-label"><strong>${escapeHtml(tag.name)}</strong><span>${escapeHtml(tag.percent)}%</span></span>`;
    const intensity = Math.sqrt(tag.songCount / items[0].songCount);
    tile.style.backgroundColor = `hsl(${axis === 'genre' ? 346 : 247} 65% ${94 - 25 * intensity}%)`;
    const show = () => {
      activeTile = tile;
      tooltip.textContent = label;
      tooltip.hidden = false;
      const left = Math.max(0, Math.min(tile.offsetLeft, chart.clientWidth - tooltip.offsetWidth));
      const top = tile.offsetTop + tile.offsetHeight;
      tooltip.style.left = `${left}px`;
      tooltip.style.top = `${top + tooltip.offsetHeight <= chart.clientHeight ? top : Math.max(0, tile.offsetTop - tooltip.offsetHeight)}px`;
    };
    tile.addEventListener('pointerenter', show);
    tile.addEventListener('focus', show);
    tile.addEventListener('click', show);
    tile.addEventListener('blur', hide);
    tile.addEventListener('pointerleave', (event) => {
      if (event.relatedTarget !== tooltip && document.activeElement !== tile) hide();
    });
    return tile;
  });
  chart.replaceChildren(...tiles, tooltip);
  chart.addEventListener('keydown', (event) => { if (event.key === 'Escape') hide(); });
  // Allow moving the pointer onto the tooltip without dismissing it.
  chart.addEventListener('pointerleave', () => {
    if (!activeTile || document.activeElement !== activeTile) hide();
  });
  const layout = () => {
    hide();
    treemapLayout(items, 0, 0, chart.clientWidth, chart.clientHeight).forEach((rect, index) => {
      const tile = tiles[index];
      Object.assign(tile.style, { left: `${rect.x}px`, top: `${rect.y}px`, width: `${rect.width}px`, height: `${rect.height}px` });
      const label = tile.firstElementChild;
      label.hidden = false;
      label.hidden = rect.width < 38 || rect.height < 42 || label.scrollWidth > tile.clientWidth - 12 || label.scrollHeight > tile.clientHeight - 12;
    });
  };
  new ResizeObserver(layout).observe(chart);
  layout();
}

function renderTagProfile(profile) {
  const total = profile.denominator;
  document.querySelector("#tag-explanation").textContent =
    "agy의 Google 검색으로 수집한 장르와 분위기·특징입니다. AI 검색 후보를 한국어로 통일해 표시합니다.";
  renderTreemap("#tag-chart", profile.tags, "genre");
  renderTreemap("#mood-chart", profile.tags, "mood");
  document.querySelector("#tag-genre-note").textContent =
    `태그가 수집된 ${total}곡 기준 (AI 검색 후보) · 면적이 클수록 해당 특성을 가진 곡이 많음 · 한 곡에 여러 태그가 있어 비율 합계는 100%를 넘을 수 있으며, 표시 비율은 카드 전체에서 차지하는 면적 비율과 다릅니다. 타일에 마우스를 올리거나, 탭하거나, 키보드로 초점을 이동하면 곡 수와 비율을 볼 수 있습니다.`;

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
