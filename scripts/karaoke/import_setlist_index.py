#!/usr/bin/env python3
"""Parse a locally downloaded Setlist Index snapshot."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

SOURCE_URL = "https://setlist.kibunya.org/channel/@OtonoseKanade/"
TIMESTAMP_RE = re.compile(r"^(?P<time>(?:\d+:)?\d{1,2}:\d{2})\s+(?P<label>.+)$")
DATE_RE = re.compile(r"(\d{4})/(\d{1,2})/(\d{1,2})")


class SetlistParser(HTMLParser):
    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.entries = []
        self.current = None
        self.in_h3 = False
        self.h3_parts = []
        self.current_anchor = None

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "h3":
            self._flush()
            self.in_h3 = True
            self.h3_parts = []
        if tag == "a":
            self.current_anchor = {
                "href": urljoin(self.base_url, attrs_dict.get("href", "")),
                "parts": [],
            }

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_h3 = False
        if tag == "a" and self.current_anchor is not None:
            text = " ".join("".join(self.current_anchor["parts"]).split())
            self._add_anchor(text, self.current_anchor["href"])
            self.current_anchor = None

    def handle_data(self, data):
        if self.in_h3:
            self.h3_parts.append(data)
        if self.current_anchor is not None:
            self.current_anchor["parts"].append(data)
        elif self.current is not None:
            text = " ".join(data.split())
            if text:
                match = DATE_RE.search(text)
                if match:
                    self.current["date"] = f"{int(match.group(1)):04d}-{int(match.group(2)):02d}-{int(match.group(3)):02d}"

    def _add_anchor(self, text: str, href: str):
        if self.current is None or not text:
            return
        match = TIMESTAMP_RE.match(text)
        if match and "youtube.com" in href:
            self.current["performances"].append({
                "timestampCandidate": match.group("time"),
                "displayText": match.group("label"),
                "sourceUrl": href,
            })
        elif "youtube.com/watch" in href and self.current.get("videoUrl") is None:
            self.current["videoUrl"] = href

    def _flush(self):
        if self.current is not None and self.current.get("title"):
            self.entries.append(self.current)
        title = " ".join("".join(self.h3_parts).split())
        self.current = {
            "title": title,
            "date": None,
            "videoUrl": None,
            "performances": [],
        }

    def close(self):
        super().close()
        self._flush()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Local HTML snapshot downloaded from Setlist Index")
    parser.add_argument("--source-url", default=SOURCE_URL)
    parser.add_argument("--retrieved-at", default=None)
    parser.add_argument("--output-root", default="data/karaoke")
    parser.add_argument("--metadata-output", default="data/karaoke/source-metadata/setlist-index.json")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.is_file():
        raise FileNotFoundError(f"Local snapshot not found: {input_path}")

    retrieved_at = args.retrieved_at or datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    snapshot_sha256 = hashlib.sha256(input_path.read_bytes()).hexdigest()
    html = input_path.read_text(encoding="utf-8", errors="replace")
    parser_instance = SetlistParser(args.source_url)
    parser_instance.feed(html)
    entries = [entry for entry in parser_instance.entries if entry.get("title")]

    if not entries:
        raise RuntimeError("No broadcast headings were parsed; inspect the local snapshot or parser assumptions.")

    root = Path(args.output_root)
    broadcasts = []
    performances = []
    for index, entry in enumerate(entries, start=1):
        video_id = (entry.get("videoUrl") or "").split("v=")[-1].split("&")[0]
        broadcast_id = video_id or f"setlist-index-entry-{index:03d}"
        broadcasts.append({
            "id": broadcast_id,
            "title": entry["title"],
            "date": entry.get("date"),
            "videoUrl": entry.get("videoUrl"),
            "sources": [args.source_url],
            "sourceSnapshotName": input_path.name,
            "status": "source-confirmed",
            "retrievedAt": retrieved_at,
        })
        for order, item in enumerate(entry["performances"], start=1):
            performances.append({
                "id": f"{broadcast_id}-{order:02d}",
                "broadcastId": broadcast_id,
                "order": order,
                "displayText": item["displayText"],
                "timestampCandidate": item["timestampCandidate"],
                "sourceUrl": item["sourceUrl"],
                "sourceSnapshotName": input_path.name,
                "status": "source-confirmed",
            })

    write_json(Path(args.metadata_output), {
        "schemaVersion": 1,
        "sourceUrl": args.source_url,
        "retrievedAt": retrieved_at,
        "localFilename": input_path.name,
        "sha256": snapshot_sha256,
        "parser": "scripts/karaoke/import_setlist_index.py",
        "rawFileUploaded": False,
        "broadcastCount": len(broadcasts),
        "performanceCount": len(performances)
    })

    write_json(root / "candidates" / "setlist-index-broadcasts.json", {
        "schemaVersion": 1,
        "source": args.source_url,
        "sourceSnapshot": str(input_path),
        "retrievedAt": retrieved_at,
        "broadcasts": broadcasts,
    })
    write_json(root / "candidates" / "setlist-index-performances.json", {
        "schemaVersion": 1,
        "source": args.source_url,
        "sourceSnapshot": str(input_path),
        "retrievedAt": retrieved_at,
        "performances": performances,
    })
    print(json.dumps({
        "broadcasts": len(broadcasts),
        "performances": len(performances),
        "sourceSnapshot": str(input_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Import failed: {exc}", file=sys.stderr)
        sys.exit(1)
