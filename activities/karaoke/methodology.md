# Collection Methodology

1. Setlist Index 채널 페이지를 로컬 HTML로 저장합니다.
2. 방송 제목, 날짜, YouTube URL, 곡명, 가수, 순서, 타임스탬프를 파싱합니다.
3. 원본 표시값과 Setlist Index URL을 정규화 JSON에 보존합니다.
4. 방송 ID와 공연 ID를 생성하고 중복을 검사합니다.
5. 구조적으로 누락되거나 파싱할 수 없는 행만 review 대상으로 기록합니다.
6. 정규화 JSON과 source metadata를 GitHub에 업로드합니다.
7. Pages가 정규화 데이터를 사용해 대시보드를 자동 배포합니다.

Setlist Index의 곡·순서·타임스탬프는 별도 영상 검증 없이 source-confirmed로 취급합니다.
