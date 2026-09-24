#!/usr/bin/env python3
"""Build dashboard statistics and playlist manifests from normalized performances."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="data/karaoke/normalized/performances.json")
    parser.add_argument("--output", default="data/karaoke/playlist")
    args = parser.parse_args()

    payload = read_json(Path(args.input))
    performances = payload.get("performances", [])
    counts = Counter()
    display = {}
    yearly = defaultdict(Counter)

    for item in performances:
        if item.get("status") not in {"source-confirmed", "confirmed"}:
            continue
        key = item.get("normalizedTitle") or item.get("title")
        if not key:
            continue
        counts[key] += 1
        display[key] = {
            "title": item.get("title", key),
            "artist": item.get("artist"),
            "originalUrl": item.get("originalUrl"),
        }
        year = str(item.get("date") or item.get("broadcastDate") or "")[:4] or "unknown"
        yearly[year][key] += 1

    top50 = []
    for key, count in counts.most_common(50):
        item = dict(display[key])
        item.update({"key": key, "count": count})
        top50.append(item)

    write_json(Path(args.output) / "top-50.json", {
        "generatedFrom": args.input,
        "songs": top50,
    })

    for year, year_counts in sorted(yearly.items()):
        songs = []
        for key, count in year_counts.most_common():
            item = dict(display[key])
            item.update({"key": key, "count": count})
            songs.append(item)
        write_json(Path(args.output) / f"{year}.json", {
            "generatedFrom": args.input,
            "year": year,
            "songs": songs,
        })

    write_json(Path(args.output) / "stats.json", {
        "generatedFrom": args.input,
        "performanceCount": sum(counts.values()),
        "uniqueSongCount": len(counts),
        "yearCount": len(yearly),
        "songCounts": [{"key": key, "count": count, **display[key]} for key, count in counts.most_common()],
    })


if __name__ == "__main__":
    main()
