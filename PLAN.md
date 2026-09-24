# Otonose Kanade Fan Activity Archive Plan

## 목적

오토노세 카나데의 가라오케 방송과 Setlist Index 셋리스트를 기록하고, GitHub Pages에서 사용 통계와 연도별 목록을 공개합니다.

## 현재 실행 구조

- `data/karaoke/raw/setlist-index/`: 로컬 전용 HTML 원본
- `data/karaoke/source-metadata/`: 원본 URL, 수집일, 해시, 파서 버전, 건수
- `data/karaoke/normalized/broadcasts.json`: 방송 데이터
- `data/karaoke/normalized/performances.json`: 공연·곡 데이터
- `data/karaoke/candidates/`: 구조적으로 처리되지 않은 후보 데이터가 필요할 때 사용
- `data/karaoke/review/`: 구조적 오류나 사람이 결정해야 하는 예외
- `data/karaoke/playlist/`: 향후 원곡 매칭 후 생성할 playlist manifest
- `site/index.html`: 저장소 안내 페이지
- `site/dashboard.html`: 정규화 공연 JSON을 읽는 대시보드

대시보드의 실행에 필요한 데이터는 `data/karaoke/normalized/`입니다. 원본 HTML은 GitHub에 업로드하지 않습니다.

## 로컬 갱신 절차

1. Setlist Index 채널 페이지를 로컬에 저장합니다.
2. `scripts/karaoke/parse_setlist_index_local.py`를 실행합니다.
3. 생성된 정규화 JSON과 source metadata를 GitHub에 업로드합니다.
4. `scripts/validate_karaoke.py`로 JSON과 참조를 검사합니다.
5. `main`에 반영되면 Pages workflow가 자동 배포됩니다.

Setlist Index에 표시된 방송·곡·순서·타임스탬프는 source-confirmed로 저장합니다.

## 대시보드 현재 기능

- 방송 수
- 공연 수
- 고유 곡 수
- 연도 수
- 연도별 곡 목록과 사용 횟수
- 사용 횟수 상위 50곡
- 검토된 태그가 없을 때 분위기·장르 미표시

## 향후 기능

- 원곡 YouTube URL 매칭
- 연도별 원곡 playlist manifest
- 사용 횟수 상위 50곡 playlist manifest
- 원곡별 장르·분위기 태그
- 원곡 매칭 후 YouTube Music playlist 생성

## 자동화 원칙

자동화는 변경안을 review 가능한 방식으로 만들며, 원본 HTML을 GitHub에 업로드하지 않습니다. GitHub Actions는 커밋된 JSON을 검증하고 Pages를 배포합니다.
