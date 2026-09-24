# Local-only Setlist Index snapshots

Setlist Index HTML 원본은 로컬에서만 보관합니다. GitHub에는 업로드하지 않습니다.

로컬 절차:

1. 채널 페이지를 `latest.html` 같은 파일명으로 저장합니다.
2. `scripts/karaoke/parse_setlist_index_local.py`로 정규화 JSON을 생성합니다.
3. `data/karaoke/normalized/`와 `data/karaoke/source-metadata/`의 결과만 GitHub에 업로드합니다.

원본 파일은 `.gitignore`로 제외됩니다.
