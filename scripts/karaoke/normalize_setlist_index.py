#!/usr/bin/env python3
"""Normalize imported Setlist Index candidates without inventing song metadata."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-root", default="data/karaoke")
    parser.add_argument("--output", default="data/karaoke/normalized/performances.json")
    args = parser.parse_args()

    root = Path(args.input_root)
    broadcasts = read_json(root / "candidates/setlist-index-broadcasts.json").get("broadcasts", [])
    performance_payload = read_json(root / "candidates/setlist-index-performances.json")
    performances = performance_payload.get("performances", [])
    source_page = performance_payload.get("source")
    dates = {item["id"]: item.get("date") for item in broadcasts}

    normalized_broadcasts = []
    for item in broadcasts:
        normalized_broadcasts.append({
            **item,
            "sources": item.get("sources", [source_page]),
            "evidence": [{"type": "setlist-index", "url": source_page}] if source_page else [],
        })

    normalized = []
    for item in performances:
        normalized.append({
            "id": item["id"],
            "broadcastId": item["broadcastId"],
            "date": dates.get(item["broadcastId"]),
            "order": item["order"],
            "title": item["displayText"],
            "normalizedTitle": item["displayText"],
            "artist": None,
            "timestampCandidate": item["timestampCandidate"],
            "sourceUrl": item["sourceUrl"],
            "sources": [item["sourceUrl"]],
            "evidence": [{"type": "setlist-index", "url": source_page}] if source_page else [],
            "status": "source-confirmed",
            "notes": [
                "Title is preserved as displayed by Setlist Index.",
                "Artist and original-song mapping require normalization or review."
            ]
        })

    output_path = Path(args.output)
    write_json(output_path.parent / "broadcasts.json", {
        "schemaVersion": 1,
        "source": "data/karaoke/candidates/setlist-index-broadcasts.json",
        "broadcasts": normalized_broadcasts
    })
    write_json(output_path, {
        "schemaVersion": 1,
        "source": "data/karaoke/candidates/setlist-index-performances.json",
        "performances": normalized
    })
    print(json.dumps({"performances": len(normalized)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
