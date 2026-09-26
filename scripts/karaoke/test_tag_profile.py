"""Checks for the dashboard's genre summary."""

import unittest

from build_dashboard import build_tag_profile, build_feature_profile
from build_song_features import build_features, translate_tags


class TagProfileTests(unittest.TestCase):
    def test_korean_features_preserve_collected_records(self):
        data = build_features()
        self.assertEqual(data['collectedCount'], len(data['songs']))
        self.assertEqual(len({s['id'] for s in data['songs']}), len(data['songs']))
        for song in data['songs']:
            self.assertEqual(song['status'], 'candidate')
            self.assertLessEqual(len(song['genres']), 2)
            self.assertLessEqual(len(song['mood_tags']), 4)
            for tag in song['genres'] + song['mood_tags']:
                self.assertNotRegex(tag, r'[A-Za-z\u3040-\u30ff\u3400-\u9fff0-9]')

    def test_translation_collapses_synonyms_and_rejects_untranslated(self):
        self.assertEqual(translate_tags(['ロック', '록'], {'ロック': '록'}), ['록'])
        with self.assertRaisesRegex(ValueError, 'Korean translation required'):
            translate_tags(['unmapped'], {})

    def test_features_count_pairs_once_and_keep_mood_separate(self):
        songs = [
            {'id': 'a', 'title': 'Same', 'artist': 'One', 'genres': ['록', '록'], 'mood_tags': ['밝음'], 'count': 100, 'status': 'candidate', 'sourceUrl': 'https://example.org/a'},
            {'id': 'b', 'title': 'Same', 'artist': 'Two', 'genres': [], 'mood_tags': ['밝음'], 'count': 1, 'status': 'candidate', 'sourceUrl': 'https://example.org/b'},
        ]
        data = {'songs': songs, 'inventoryCount': 5, 'retrievedAt': '2026-09-27'}
        profile = build_feature_profile(data)
        self.assertEqual(profile['denominator'], 2)
        self.assertEqual({(t['axis'], t['name'], t['songCount'], t['percent']) for t in profile['tags']}, {('genre', '록', 1, 50), ('mood', '밝음', 2, 100)})
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            build_feature_profile({**data, 'songs': songs + songs[:1]})

    def test_counts_distinct_songs_and_keeps_scope(self):
        top = [
            {"title": "A", "artist": "One", "count": 110},
            {"title": "B", "artist": "Two", "count": 1},
        ]
        reviewed = {
            "reviewedAt": "2026-09-24",
            "songs": [
                {"title": "A", "artist": "One", "tags": [
                     {"axis": "style", "name": "dance", "basis": "manual-mapping", "sourceUrl": "https://example.org/a", "note": "reviewed"},
                     {"axis": "style", "name": "dance", "basis": "manual-mapping", "sourceUrl": "https://example.org/a", "note": "reviewed"},
                     {"axis": "genre", "name": "pop", "basis": "catalog-category", "sourceUrl": "https://example.org/a", "note": "reviewed"},
                 ]},
            ],
        }
        profile = build_tag_profile(top, reviewed)
        self.assertEqual(profile["denominator"], 2)
        self.assertEqual(profile["taggedSongCount"], 1)
        self.assertEqual(
            {(tag["name"], tag["songCount"], tag["percent"]) for tag in profile["tags"]},
            {("pop", 1, 50)},
        )
        self.assertEqual([tag["name"] for tag in profile["songs"][0]["tags"]], ["pop"])
        self.assertEqual(profile["songs"][1]["tags"], [])

    def test_rejects_artist_mismatch(self):
        with self.assertRaisesRegex(ValueError, "Artist mismatch"):
            build_tag_profile(
                [{"title": "A", "artist": "One", "count": 1}],
                {"reviewedAt": "2026-09-24", "songs": [
                    {"title": "A", "artist": "Other", "tags": []},
                ]},
            )

    def test_empty_tags_have_no_chart_rows(self):
        profile = build_tag_profile(
            [{"title": "A", "artist": "One", "count": 1}],
            {"reviewedAt": "2026-09-24", "songs": []},
        )
        self.assertEqual(profile["taggedSongCount"], 0)
        self.assertEqual(profile["tags"], [])


if __name__ == "__main__":
    unittest.main()
