# Otonose Kanade Fan Activity Archive

오토노세 카나데 관련 팬활동 작업물을 기록하고 공개하기 위한 저장소입니다.

첫 번째 활동은 Setlist Index를 기본 데이터 소스로 삼아 가라오케 방송, set list, 원곡 정보, 방송 내 타임스탬프를 정리하는 것입니다. Setlist Index에 표시된 항목을 별도 검증 없이 source-confirmed로 취급합니다.

이 저장소는 AI agent가 자료를 수집하고 변경안을 준비할 수 있도록 설계되어 있습니다. 확정되지 않은 정보는 검토 대기 상태로 남기며, 출처 없는 사실을 등록하지 않습니다.

자세한 운영 규칙은 [AGENTS.md](AGENTS.md), 전체 실행 계획은 [PLAN.md](PLAN.md)를 참고하세요.

## 데이터 업데이트 방식

Setlist Index 원본은 로컬에서 다운로드하고 가공합니다. GitHub에는 원본 HTML을 올리지 않고, 생성된 후보·정규화 JSON, 통계·playlist manifest, source metadata만 업로드합니다.

자세한 절차는 [scripts/karaoke/README.md](scripts/karaoke/README.md)를 참고하세요.
