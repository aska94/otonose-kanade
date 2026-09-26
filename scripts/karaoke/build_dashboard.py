"""Build the small, reviewable data payload used by the karaoke dashboard."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from build_song_features import build_features


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "data" / "karaoke" / "normalized" / "performances.json"
TAG_SOURCE = ROOT / "data" / "karaoke" / "normalized" / "song-tags.json"
TARGET = ROOT / "site" / "data.json"


def song_key(performance: dict) -> str:
    return performance["normalizedTitle"]


def label(song: str, artists: dict[str, str]) -> dict[str, str]:
    return {"title": song, "artist": artists.get(song, "")}


def build_tag_profile(top_songs: list[dict], tag_data: dict) -> dict:
    reviewed = {item["title"]: item for item in tag_data["songs"]}
    if len(reviewed) != len(tag_data["songs"]):
        raise ValueError("Duplicate reviewed song tag title")
    counts: Counter[tuple[str, str]] = Counter()
    songs = []
    for song in top_songs[:10]:
        record = reviewed.get(song["title"])
        tags = [tag for tag in record["tags"] if tag["axis"] == "genre"] if record else []
        if record and record["artist"] != song["artist"]:
            raise ValueError(f'Artist mismatch for {song["title"]}')
        for axis, name in {(tag["axis"], tag["name"]) for tag in tags}:
            counts[(axis, name)] += 1
        songs.append({
            **song,
            "tags": [
                {
                    "name": tag["name"],
                    "axis": tag["axis"],
                    "basis": tag["basis"],
                    "status": tag.get("status", "candidate"),
                    "sourceUrl": tag["sourceUrl"],
                    "note": tag["note"],
                }
                for tag in tags
            ],
        })
    denominator = len(songs)
    return {
        "scope": "performance-top-10",
        "denominator": denominator,
        "taggedSongCount": sum(bool(song["tags"]) for song in songs),
        "reviewedAt": tag_data["reviewedAt"],
        "tags": [
            {"axis": axis, "name": name, "songCount": count, "percent": round(count * 100 / denominator)}
            for (axis, name), count in sorted(counts.items(), key=lambda entry: (-entry[1], entry[0]))
        ] if denominator else [],
        "songs": songs,
    }


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

    top_songs = [
        {**label(song, artists), "count": count}
        for song, count in overall.most_common(20)
    ]
    feature_data = build_features()
    payload = {
        "source": "data/karaoke/normalized/performances.json",
        "performanceCount": len(performances),
        "songCount": len(overall),
        "broadcastCount": broadcast_count,
        "topSongs": top_songs,
        "tagProfile": build_feature_profile(feature_data),
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


def build_feature_profile(feature_data: dict) -> dict:
    songs = feature_data['songs']
    keys = [(s['title'], s['artist']) for s in songs]
    if len(keys) != len(set(keys)):
        raise ValueError('Duplicate feature title/artist pair')
    counts = Counter((axis, tag) for song in songs for axis, field in [('genre', 'genres'), ('mood', 'mood_tags')] for tag in set(song[field]))
    total = len(songs)
    return {
        'scope': 'collected-ai-candidates', 'language': 'ko',
        'denominator': total, 'inventoryCount': feature_data['inventoryCount'],
        'taggedSongCount': sum(bool(s['genres'] or s['mood_tags']) for s in songs),
        'retrievedAt': feature_data['retrievedAt'],
        'tags': [{'axis': axis, 'name': name, 'songCount': count, 'percent': round(count * 100 / total)} for (axis, name), count in sorted(counts.items(), key=lambda x: (-x[1], x[0]))] if total else [],
        'songs': [{k: song[k] for k in ('id', 'title', 'artist', 'genres', 'mood_tags', 'status', 'count', 'sourceUrl')} for song in songs],
    }


if __name__ == "__main__":
    main()
