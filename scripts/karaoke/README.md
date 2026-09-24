# Karaoke scripts

현재 사용하는 로컬 파서는 `parse_setlist_index_local.py`입니다.

    python scripts/karaoke/parse_setlist_index_local.py data/karaoke/raw/setlist-index/latest.html

이 명령은 다음 파일을 생성합니다.

- `data/karaoke/normalized/broadcasts.json`
- `data/karaoke/normalized/performances.json`
- `data/karaoke/source-metadata/setlist-index.json`

검증:

    python scripts/validate_karaoke.py

원본 HTML은 로컬 전용이며 GitHub에 업로드하지 않습니다. 정규화 데이터가 `main`에 업로드되면 GitHub Pages가 자동 배포됩니다.
