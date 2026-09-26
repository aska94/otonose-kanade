import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
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
    try:
        aggregate_broadcasts = normalized_dir / "broadcasts.json"
        aggregate_performances = normalized_dir / "performances.json"
        if aggregate_broadcasts.exists() and aggregate_performances.exists():
            broadcasts = load_json(aggregate_broadcasts)
            songs = load_json(aggregate_performances)
        else:
            files = sorted((normalized_dir / "broadcasts").glob("*.json"))
            records = [load_json(path) for path in files]
            broadcasts = {"broadcasts": [record["broadcast"] for record in records]}
            songs = {"performances": [item for record in records for item in record.get("performances", [])]}
    except (OSError, json.JSONDecodeError, KeyError) as exc:
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
        if status in {"source-confirmed", "confirmed"} and not (item.get("evidence") or item.get("sources")):
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

    tag_path = normalized_dir / "song-tags.json"
    if tag_path.exists():
        tag_data = load_json(tag_path)
        seen_titles = set()
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", tag_data.get("reviewedAt", "")):
            errors.append("song tags: invalid review date")
        if tag_data.get("method") not in {"web-search-and-source-review", "itunes-search-and-track-match"}:
            errors.append("song tags: missing collection method")
        for item in tag_data.get("songs", []):
            title = item.get("title")
            if not title or title in seen_titles:
                errors.append(f"song tags: missing or duplicate title {title}")
            seen_titles.add(title)
            if not item.get("artist"):
                errors.append(f"song tags {title}: missing artist")
            if not item.get("tags"):
                errors.append(f"song tags {title}: no tags")
            tag_names = set()
            for tag in item.get("tags", []):
                name = tag.get("name")
                tag_key = (tag.get("axis"), name)
                if not name or tag_key in tag_names or tag.get("axis") not in {"genre", "style", "origin"}:
                    errors.append(f"song tags {title}: invalid or duplicate tag {name}")
                tag_names.add(tag_key)
                if tag.get("basis") not in {"release-category", "catalog-category", "source-description", "label-discography", "manual-mapping"}:
                    errors.append(f"song tags {title}: invalid basis for {name}")
                if tag.get("axis") == "genre" and tag.get("status") not in STATUSES:
                    errors.append(f"song tags {title}: invalid genre status for {name}")
                if not tag.get("note"):
                    errors.append(f"song tags {title}: missing evidence note for {name}")
                require_https_url(tag.get("sourceUrl"), f"song tags {title} {name} source", errors)

    feature_path = normalized_dir / "song-features.ko.json"
    if feature_path.exists():
        features = load_json(feature_path)
        if features.get("language") != "ko":
            errors.append("song features: expected Korean display language")
        for field in ("retrievedAt", "extractionMode", "comparisonSummary", "sourceRecord"):
            if not features.get(field):
                errors.append(f"song features: missing {field}")
        seen_features = set()
        seen_feature_ids = set()
        for song in features.get("songs", []):
            key = (song.get("title"), song.get("artist"))
            if not key[0] or key in seen_features or not song.get("id") or song["id"] in seen_feature_ids:
                errors.append("song features: missing or duplicate identity")
            seen_features.add(key)
            seen_feature_ids.add(song.get("id"))
            if song.get("status") != "candidate":
                errors.append(f"song features {key}: AI tags must remain candidates")
            require_https_url(song.get("sourceUrl"), f"song features {key} source", errors)
            for field, limit in (("genres", 2), ("mood_tags", 4)):
                tags = song.get(field, [])
                if len(tags) > limit or len(tags) != len(set(tags)):
                    errors.append(f"song features {key}: invalid tag count")
                for tag in tags:
                    if not re.search(r"[\uac00-\ud7af]", tag) or re.search(r"[A-Za-z\u3040-\u30ff\u3400-\u9fff0-9]", tag):
                        errors.append(f"song features {key}: untranslated or numeric tag")

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    print("Karaoke data validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
