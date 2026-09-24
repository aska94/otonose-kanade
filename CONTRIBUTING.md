# Contributing

자료를 추가하거나 수정할 때는 다음 원칙을 지킵니다.

1. Setlist Index HTML은 로컬에서만 보관합니다.
2. 로컬 파서로 정규화 방송·공연 JSON과 source metadata를 생성합니다.
3. 원본 URL과 수집 정보를 기록합니다.
4. 방송과 공연 곡을 별도 레코드로 관리합니다.
5. Setlist Index에 표시된 값은 source-confirmed로 저장합니다.
6. 구조적으로 누락되거나 파싱할 수 없는 행만 review 대상으로 분리합니다.
7. 정규화 데이터와 metadata를 GitHub에 업로드하면 Pages가 자동 배포됩니다.
8. credentials, cookies, access tokens는 저장하지 않습니다.

자동화 변경은 가능한 한 Pull Request로 검토합니다.
