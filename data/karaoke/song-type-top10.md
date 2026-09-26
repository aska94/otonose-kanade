# 상위 10곡 장르 조회·표시

2026-09-25 기준 대시보드의 `normalizedTitle` 사용 횟수 상위 10곡을 대상으로 한다. 일본 iTunes Search API(`country=jp`, `media=music`, `entity=song`)에 곡명과 원곡 아티스트를 함께 검색하고 `trackName`, `artistName`, 수록 음반을 대조한다. 라이브·리믹스·반주·커버는 원곡 음원으로 간주하지 않는다. API의 `primaryGenreName`과 해당 `trackViewUrl`을 `data/karaoke/normalized/song-tags.json`에 기록한다.

9곡에서 원곡에 대응하는 음원을 찾았고 모두 `J-Pop`으로 분류됐다. `ワールドイズマイン`은 ryo (supercell)와 初音ミク의 라이브·리믹스 음원만 확인되어 원곡 장르를 비워 둔다. 따라서 대시보드 장르 확인 범위는 9/10곡이다. iTunes 분류는 음원 버전에 따라 달라질 수 있어 `candidate`로 표시한다.

대시보드는 빌드 시 검토된 JSON을 읽어 생성한다. 장르 차트의 분모는 공연 횟수가 아닌 상위 10개 고유 곡이다. 기존 스타일·제작 유형 태그는 근거 기록으로 보존하지만 장르 차트와 곡별 표시에 사용하지 않는다. 새로운 곡이 상위 10위에 들어오면 같은 기준으로 음원을 대조하고 출처 URL과 조회일을 갱신해야 한다.
