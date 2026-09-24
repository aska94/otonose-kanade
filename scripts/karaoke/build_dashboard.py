"""Build the small, reviewable data payload used by the karaoke dashboard."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "karaoke" / "normalized" / "performances.json"
TARGET = ROOT / "site" / "data.json"


def song_key(performance: dict) -> str:
    return performance["normalizedTitle"]


def label(song: str, artists: dict[str, str]) -> dict[str, str]:
    return {"title": song, "artist": artists.get(song, "")}


def main() -> None:
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    performances = source["performances"]
    index_path = ROOT / "data" / "karaoke" / "normalized" / "index.json"
    broadcast_count = (
        len(json.loads(index_path.read_text(encoding="utf-8")).get("broadcasts", []))
        if index_path.exists()
        else len({item["broadcastId"] for item in performances})
    )

    artists: dict[str, str] = {}
    for performance in performances:
        key = song_key(performance)
        artists.setdefault(key, performance.get("artist", ""))

    overall = Counter(song_key(item) for item in performances)
    by_year: dict[str, Counter] = defaultdict(Counter)
    for performance in performances:
        by_year[performance["date"][:4]][song_key(performance)] += 1

    payload = {
        "source": "data/karaoke/normalized/performances.json",
        "performanceCount": len(performances),
        "songCount": len(overall),
        "broadcastCount": broadcast_count,
        "topSongs": [
            {**label(song, artists), "count": count}
            for song, count in overall.most_common(20)
        ],
        "years": [
            {
                "year": year,
                "songs": [
                    {**label(song, artists), "count": count}
                    for song, count in songs.most_common(10)
                ],
            }
            for year, songs in sorted(by_year.items(), reverse=True)
        ],
    }

    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
