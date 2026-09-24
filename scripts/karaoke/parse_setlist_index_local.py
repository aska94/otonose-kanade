#!/usr/bin/env python3
"""Parse a local Setlist Index page into one JSON file per broadcast."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import date
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlparse


def clean(value):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", value))).strip()


def seconds(value):
    result = 0
    for part in value.split(":"):
        result = result * 60 + int(part)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("data/karaoke/normalized"))
    parser.add_argument("--metadata", type=Path, default=Path("data/karaoke/source-metadata/setlist-index.json"))
    args = parser.parse_args()

    raw = args.input.read_bytes()
    html = raw.decode("utf-8", "replace")
    source = "https://setlist.kibunya.org/channel/@OtonoseKanade/"
    output = args.output_dir / "broadcasts"
    output.mkdir(parents=True, exist_ok=True)
    index = []
    broadcast_count = 0
    performance_count = 0

    for chunk in html.split('<div class="video-card')[1:]:
        head = re.search(r'<h3[^>]*>\s*<a href="([^"]+)"[^>]*>(.*?)</a>', chunk, re.S)
        date_match = re.search(r"配信日:\s*(\d{4})/(\d{1,2})/(\d{1,2})", chunk)
        if not head or not date_match:
            continue
        year, month, day = date_match.groups()
        youtube_url = head.group(1)
        broadcast_id = parse_qs(urlparse(youtube_url).query).get("v", [""])[0]
        if not broadcast_id:
            continue
        broadcast = {
            "id": broadcast_id,
            "title": clean(head.group(2)),
            "date": f"{int(year):04d}-{int(month):02d}-{int(day):02d}",
            "youtubeUrl": youtube_url,
            "broadcastUrl": youtube_url,
            "sources": [source],
            "status": "source-confirmed",
        }
        performances = []
        for order, part in enumerate(chunk.split('<div class="song-row')[1:], 1):
            time_match = re.search(r"font-mono[^>]*>\s*([^<]+?)\s*</div>", part, re.S)
            title_match = re.search(r"font-bold text-gray-800[^>]*>\s*([^<]+?)\s*</div>", part, re.S)
            artist_match = re.search(r"text-xs text-gray-500[^>]*>\s*([^<]*?)\s*</div>", part, re.S)
            url_match = re.search(r'<a href="(https://youtube\.com/watch\?v=[^"]+&t=\d+s)"', part)
            if not time_match or not title_match:
                continue
            timestamp = clean(time_match.group(1))
            start = seconds(timestamp)
            performances.append({
                "id": f"{broadcast_id}-{order:02d}",
                "broadcastId": broadcast_id,
                "date": broadcast["date"],
                "order": order,
                "title": clean(title_match.group(1)),
                "normalizedTitle": clean(title_match.group(1)),
                "artist": clean(artist_match.group(1)) if artist_match else None,
                "timestamp": timestamp,
                "timestampSeconds": start,
                "sourceUrl": url_match.group(1) if url_match else f"{youtube_url}&t={start}s",
                "sources": [source],
                "evidence": [{"type": "setlist-index", "url": source}],
                "status": "source-confirmed",
            })
        (output / f"{broadcast_id}.json").write_text(
            json.dumps({"broadcast": broadcast, "performances": performances}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        index.append({"id": broadcast_id, "date": broadcast["date"], "title": broadcast["title"], "file": f"broadcasts/{broadcast_id}.json"})
        broadcast_count += 1
        performance_count += len(performances)

    (args.output_dir / "index.json").write_text(
        json.dumps({"schemaVersion": 1, "broadcastCount": broadcast_count, "performanceCount": performance_count, "broadcasts": index}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    metadata = {
        "schemaVersion": 1,
        "sourceUrl": source,
        "observedAt": date.today().isoformat(),
        "extractionMode": "local-html",
        "rawFileUploaded": False,
        "sourceSnapshotName": args.input.name,
        "sourceSnapshotSha256": hashlib.sha256(raw).hexdigest(),
        "broadcastCount": broadcast_count,
        "performanceCount": performance_count,
        "parserVersion": "per-broadcast-v1",
    }
    args.metadata.parent.mkdir(parents=True, exist_ok=True)
    args.metadata.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False))


if __name__ == "__main__":
    main()
