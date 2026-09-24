#!/usr/bin/env python3
"""Build dashboard aggregate JSON from one JSON file per broadcast."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="data/karaoke/normalized/broadcasts")
    parser.add_argument("--output-dir", default="data/karaoke/build")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    broadcasts = []
    performances = []

    for path in sorted(input_dir.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        broadcast = payload["broadcast"]
        rows = payload.get("performances", [])
        broadcasts.append(broadcast)
        performances.extend(rows)

    broadcasts.sort(key=lambda item: (item.get("date", ""), item.get("id", "")))
    performances.sort(key=lambda item: (item.get("date", ""), item.get("broadcastId", ""), item.get("order", 0)))

    (output_dir / "broadcasts.json").write_text(
        json.dumps({"schemaVersion": 1, "broadcasts": broadcasts}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (output_dir / "performances.json").write_text(
        json.dumps({"schemaVersion": 1, "performances": performances}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"broadcasts={len(broadcasts)} performances={len(performances)}")


if __name__ == "__main__":
    main()
