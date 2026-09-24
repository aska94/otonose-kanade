# Normalized karaoke data

정규화 원본은 방송별 파일로 저장합니다.

- `broadcasts/<youtube-video-id>.json`: 방송 1개와 해당 방송의 공연 목록
- `index.json`: 방송 파일 목록과 전체 건수

GitHub Pages 배포 시 `scripts/karaoke/build_site_data.py`가 방송별 파일을 취합해 대시보드용 임시 aggregate JSON을 생성합니다. aggregate 파일은 저장소의 원본 데이터로 관리하지 않습니다.
