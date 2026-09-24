import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "karaoke"
STATUSES = {"candidate", "source-confirmed", "confirmed", "needs-review"}
YOUTUBE_HOSTS = {"youtube.com", "www.youtube.com", "youtu.be", "m.youtube.com"}
TIMESTAMP_RE = re.compile(r"^(?:(\d+):)?([0-5]?\d):([0-5]\d)$")


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def require_https_url(value, field, errors):
    if not isinstance(value, str) or not value:
        errors.append(f"{field}: missing URL")
        return
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{field}: invalid HTTPS URL")


def main():
    errors = []
    normalized_dir = DATA_DIR / "normalized"
    broadcasts_path = normalized_dir / "broadcasts.json" if (normalized_dir / "broadcasts.json").exists() else DATA_DIR / "broadcasts.json"
    songs_path = normalized_dir / "performances.json" if (normalized_dir / "performances.json").exists() else DATA_DIR / "songs.json"

    try:
        broadcasts = load_json(broadcasts_path)
        songs = load_json(songs_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    if not isinstance(broadcasts.get("broadcasts"), list):
        errors.append("broadcasts.json: broadcasts must be an array")
    if not isinstance(songs.get("performances"), list):
        errors.append("songs.json: performances must be an array")

    broadcast_ids = set()
    for item in broadcasts.get("broadcasts", []):
        item_id = item.get("id")
        if not item_id:
            errors.append("broadcast: missing id")
        elif item_id in broadcast_ids:
            errors.append(f"broadcast: duplicate id {item_id}")
        else:
            broadcast_ids.add(item_id)

        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"broadcast {item_id}: invalid status")
        if status in {"source-confirmed", "confirmed"} and not item.get("evidence"):
            errors.append(f"broadcast {item_id}: confirmed status requires evidence")
        for source in item.get("sources", []):
            require_https_url(source, f"broadcast {item_id} source", errors)
        for evidence in item.get("evidence", []):
            require_https_url(evidence.get("url"), f"broadcast {item_id} evidence", errors)

    performance_ids = set()
    for item in songs.get("performances", []):
        item_id = item.get("id")
        if not item_id:
            errors.append("performance: missing id")
        elif item_id in performance_ids:
            errors.append(f"performance: duplicate id {item_id}")
        else:
            performance_ids.add(item_id)

        if item.get("broadcastId") not in broadcast_ids:
            errors.append(f"performance {item_id}: unknown broadcastId")

        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"performance {item_id}: invalid status")
        if status in {"source-confirmed", "confirmed"} and not item.get("evidence"):
            errors.append(f"performance {item_id}: confirmed status requires evidence")

        timestamp = item.get("timestamp") or item.get("timestampCandidate")
        if timestamp and not TIMESTAMP_RE.match(timestamp):
            errors.append(f"performance {item_id}: invalid timestamp {timestamp}")

        for source in item.get("sources", []):
            require_https_url(source, f"performance {item_id} source", errors)
        for evidence in item.get("evidence", []):
            require_https_url(evidence.get("url"), f"performance {item_id} evidence", errors)

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Karaoke data validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
