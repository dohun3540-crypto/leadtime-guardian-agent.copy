# Team1 다음 단계·통합 인계

개인 저장소 .copy의 `feat/team1-resume-schema-demo-20261103`, Draft PR25를 재개한다. PR24 체크포인트와 PR23 감사 결과는 보호하며 PR25는 후속 증분이다. 최종 원격 HEAD와 CI는 PR25 최신 본문 및 전달 ZIP POST_PUSH_ATTESTATION.json을 먼저 읽는다. 원래 source `8b671d4a67cd649b08c4e6603a457f607342c3d7`에서 운영 모듈을 변경하지 않았고 새 CLI2·경계 테스트4·문서만 추가했다.

| 담당 | 넘기는 완료물 | 다음 필요한 원본·수락 조건 |
| --- | --- | --- |
| 구도훈 | 회수 v2 Normalize, 40행 분류, 실제143 SHA 검증, 새 시연CLI/매뉴얼, Preflight 진단 | 실제 QA input와 Normalize 바이트/semantic join, raw Merge와 full stage trace, provider upload receipts, alias/config/run 인증 |
| 윤현준 | Native SHA별 local replay와 선택 patch Manifest | 본인이 동일 Native 원본을 실행한 Safety V6 결과+provenance sidecar; Team1 local replay를 본인 원본 인계로 바꾸지 않음 |
| 김민주 | 원본 PDF 기계검사60/60 및 핵심 계약 감사 | 최신 원본 검수 XLSX, PDF별 근거, 명시적 reviewer 승인 및 Gold freeze; 후보 Gold를 자동 승인하지 않음 |
| 통합 maintainer | INTEGRATION_CHANGESET_MANIFEST.json, 보존5경로patch, 격리812/544·기존778/812ID 보존 | `67b93291c1f32acaf43e45815d2d1119480b652a` 기준에 최소 patch 적용 후 본인 branch CI. strict_json/engine/Adapter/data/Gold 보호; 이번 세션 통합 원격 push0 |
| 발표 담당 | DEMO_AND_EVALUATION_PLAN.md, DEMO_EVALUATION.json | LOCAL_REPLAY / DRAFT / Live 차이와 Gate BLOCKED를 표시. 공식 정확도·최적해·한국어 변환 실측 주장 금지 |

재개 우선순위: A 실제QA Input/trace/receipts 확보 → B 4조합 alias·원본 동일성 인증 → Team2 동일 SHA·Team3 승인 Gold → full case E2E/공식 비교 → maintainer 선택통합 CI. C 정밀분류·E local시연·F 격리패치는 다시 구현할 필요가 없다. 변경된 원본이나 코드가 있을 때만 관련 검증을 다시 수행한다.

현 Studio output UI에서 실제 IndependentQA input 원본과 raw Merge/전체 step-run trace를 회수하지 못했다. UI의 결과 JSON은 input 증거가 아니다. 제공자가 해당 원본을 export할 수 있어야 A를 해제할 수 있다. 입력을 QA verdict에서 역생성하지 않는다. 새 실행이 필요하면 비용·권한을 별도로 확인한다.

원본보존143개와 새 v2 Normalize, 모든 raw stdout/JUnit, demo/schema report는 최종 비공개 전달 ZIP의 evidence/new_evidence/results에 있다. 공개 GitHub에는 source·문서·이름/SHA 인덱스만 있다. 항상 final Gate release_authorized=false, formal bundle0/4를 유지하고 누락 항목을 추측으로 완료 처리하지 않는다.
