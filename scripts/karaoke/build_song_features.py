"""Translate saved AI candidates to Korean without additional searches."""
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / 'data/karaoke/review/agy-song-features-2026-09-26'
TRANSLATIONS = ROOT / 'data/karaoke/normalization/feature-tags-ko.json'
TARGET = ROOT / 'data/karaoke/normalized/song-features.ko.json'


def translate_tags(tags, aliases):
    result = []
    for original in tags:
        translated = aliases.get(original, original)
        if re.search(r'[A-Za-z\u3040-\u30ff\u3400-\u9fff0-9]', translated) or not re.search(r'[\uac00-\ud7af]', translated):
            raise ValueError(f'Korean translation required: {original}')
        if translated not in result:
            result.append(translated)
    return result


def build_features():
    read = lambda path: json.loads(path.read_text(encoding='utf-8'))
    rows = read(RUN / 'results.json')
    inventory = read(RUN / 'inventory.json')['songs']
    metadata = read(RUN / 'evidence.json')
    translations = read(TRANSLATIONS)
    lookup = {(r['title'], r['artist']): r for r in inventory}
    if len({(r['title'], r['artist']) for r in rows}) != len(rows):
        raise ValueError('Duplicate title/artist pair in saved features')
    songs = []
    for row in rows:
        source = lookup[(row['title'], row['artist'])]
        if row['status'] != 'candidate' or len(row['genres']) > 2 or len(row['mood_tags']) > 4:
            raise ValueError('Invalid AI candidate schema')
        songs.append({
            'id': source['id'], 'title': row['title'], 'artist': row['artist'],
            'genres': translate_tags(row['genres'], translations['aliases']),
            'mood_tags': translate_tags(row['mood_tags'], translations['aliases']),
            'status': 'candidate', 'count': source['count'],
            'originalGenres': row['genres'], 'originalMoodTags': row['mood_tags'],
            'sourceUrl': 'https://www.google.com/search?q=' + quote(row['title'] + ' ' + row['artist']),
            'sourceNote': 'agy의 Google 검색 결과를 수용한 AI 후보입니다. 링크는 해당 곡의 검색이며 개별 태그의 검증 출처를 의미하지 않습니다.',
        })
    return {
        'language': 'ko', 'retrievedAt': metadata['retrievedAt'],
        'languageReviewedAt': translations['reviewedAt'],
        'extractionMode': 'Saved agy Google search candidates; local Korean translation only',
        'comparisonSummary': 'Translate and merge equivalent tag labels; preserve original names, raw tags and candidate status',
        'sourceRecord': str((RUN / 'results.json').relative_to(ROOT)).replace('\\', '/'),
        'sourceUrlField': 'songs[].sourceUrl',
        'inventoryCount': len(inventory), 'collectedCount': len(songs), 'songs': songs,
    }


def main():
    data = build_features()
    TARGET.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Korean feature records: {len(data["songs"])}')


if __name__ == '__main__':
    main()
