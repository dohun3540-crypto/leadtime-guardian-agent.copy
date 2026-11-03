# Team1 Full E2E 계약 수정·회귀 검증 — 2026-11-03

**실제 로컬 결함 3개를 수정했다. 전체 Native E2E와 Release는 BLOCKED다.** PR26 고정 HEAD `fdc00f963eec991033904a9675bcdc23a9f7142c`에서 별도 브랜치 `feat/team1-e2e-contract-hardening-20261103-r3`로 작업했다. 기존 PR25/26 및 동결 통합은 수정하지 않았다.

## 해결한 결함

1. Stage 검사기가 Native의 metadata/additional_values 안 Job·Step·Config 정체성을 놓쳤다. 같은 문서 값과 정상처럼 작성된 Manifest만 있으면 다른 Job 원본으로 Python Safety 검증을 진행할 수 있었다. 이제 관찰된 내부 정체성과 타입을 대조하고, 충돌을 FAIL로 판정해 Python을 실행하지 않는다. Config version true를1로 인정하지 않는다. 정상적인 별도 QA Job은 계속 허용한다.
2. 보존된 실제 Extract ZIP은 문서 객체를 바로 출력하지만 기존 검사기는 document/documents wrapper만 읽었다. 원본 bytes를 바꾸지 않고 명시된 Extract branch의 올바른 종류·문서 ID만 받아들인다. 누락된 provider Step ID나 QA 입력을 만들지는 않는다.
3. 출처 연결 API에 중첩 File ID 배열을 넣으면 TypeError가 발생했다. set 비교 전에 ID 타입·file_ suffix·중복을 검사해 구조화된 FAIL을 반환한다.

첫 재현은 **5 FAIL /36 PASS**, 수정·양성 경계 검증 후 관련 **44 PASS**다. 추가 회귀 테스트는 총8개이며 테스트 개수 자체를 목표로 늘리지 않았다. 원본 Evidence·Gold·계산 엔진·Adapter·shared strict_json·워크플로우는 변경하지 않았다.

## 이전 상태와 현재 상태

| 항목 | 이전 상태 | 현재 상태 | 실제 변경·검증 근거 |
| --- | --- | --- | --- |
| Task A | BLOCKED | BLOCKED | 현재 Studio v2 설정 unchanged. bare Extract 입력 호환 및 내부 실행 ID 검증 수정. 실제 QA Input/trace/receipt는 없음 |
| Task B | BLOCKED | BLOCKED | 공식4조합은 여전히0/4. v2를 E1으로 추정하지 않음 |
| Task C | PASS_LOCAL | PASS_LOCAL | 기존40행 정적 검토 유지, 실제 Normalize 문서6개 schema PASS. nullable provider 동작 미인증 |
| Task D | PASS_LOCAL | PASS_LOCAL | 잘못된 내부 Job/Step은 Python 전 FAIL. 실제 누락 증거 Preflight는 invalid_inputs=[]/BLOCKED |
| Task E | PASS_LOCAL | PASS_REPLAY | C001 독립 날짜·Decimal 계산60개/60,500원과 Engine 일치. C013 PO1/PO999 보존 후 차단 |
| Task F | PASS_LOCAL | PASS_LOCAL | 개인762/513, 격리 통합820/552, 기존754/812 및 최초778ID 보존 |
| Full E2E | BLOCKED | BLOCKED | 로컬 Stage→Combined→Python 경로는 검증. 실제 QA 입력과 provider 체인은 확보 못함 |
| Overall Release | BLOCKED | BLOCKED | 공식 B0/E1, Team2 본인 same-Native Sidecar, 사람 승인Gold 미확보 |

## 검증 수치와 범위

- 전체 **762 PASS**, QA **513 PASS**, 실패·스킵0.
- E2E 관련 **119 PASS**는 Stage/Combined/contract/provenance7파일 subset이다. 이전86은5파일 subset이므로33개 신규 테스트로 해석하면 안 된다.
- 고정 통합 기준+기존5경로 patch+이번5파일 선택 수정은 **820 PASS / QA552 PASS**. 원래812 전부와 최초778ID가 유지됐다. 통합에만 있던 테스트를 개인 테스트 파일로 덮어쓰지 않고 추가8개만 결합했다.
- Ruff, C001 Archive/Replay, C013 차단, Local Gate 통과. Local Gate의 전체 Release 상태는 BLOCKED다. PDF bytes는 변경하지 않았고 이전60/60 기계 검사를 이번 신규 검사로 재집계하지 않는다.
- 현재 저장 Studio Config를 읽기 전용으로 다시 export했다. cfg_bXh7dAFikuFp3rajaSWGgb/v2이며 workflowConfig는 기존과 동일하다. Normalize→QA edge와 QA 프롬프트는 존재하나 실제 입력 bytes를 증명하지 못한다. NORMALIZED_OUTPUT_NOT_PROVIDED의 provider 내부 원인은 여전히 미확정이다.
- Native 결과를 새 실행으로 표시하거나 QA 출력을 입력으로 바꾸지 않았다. 무료·유료를 포함한 신규 Studio 실행은0회다.

## 독립 계산과 출처

C001은 실제 보관 Native의 PO/납기 변경/견적과 trusted base의 고객 수요·재고를 사용했다. 기존 ETA가 고객 납기 이전이면 입고100+재고40으로 baseline 부족0이다. 변경 ETA는 납기 이후라 재고40만 사용해 수요100 대비 부족60이다. 유효 견적의 capacity60, 단가1000.00, 사용한 견적당 운송비500으로 Decimal 계산60×1000+500=60,500원이다. 기대 결과 문자열을 비교하는 것 외에 원본 값으로 독립 검산했다. PDF 의미 진실성이나 Gold 승인으로 확대하지 않는다.

기존 실제 Normalize 원본 한 단계만 제공한 Stage intake는 해당 원본을 읽되 QA Input과 나머지 단계가 없어 BLOCKED를 반환한다. 로컬 생성 Sidecar를 Team2 본인 원본 인계로 승인하지 않는다. Cross-Agent/비즈니스 보고서는 CROSS_AGENT_AND_BUSINESS_VALIDATION.json, 결함·재현·수정은 DEFECT_FIX_REGISTER.json, 명령·XML/SHA는 VALIDATION_REPORT.json과 private 로그를 참조한다.

## 저장·후속 작업

기존 PR25/26/main, 원본 저장소, Team2·3 운영 코드·Gold 및 원격 통합 브랜치는 보호했다. 이 문서는 커밋 전 경계 기록이며 최종 HEAD·Push·신규 CI 결과는 PR 본문과 전달물 POST_PUSH_ATTESTATION.json이 권위 있는 후속 기록이다.

다음 개발 우선순위3개: (1) 실제 QA Input·raw Merge·provider trace/receipt 확보 후 동일성 검증, (2) 공식 B0/E1×C001/C013 네 묶음 인증, (3) Team2 동일 Native 본인 실행 Sidecar와 사람 승인Gold를 연결해 기존 Release Gate 재평가. 이 외부 증거 없이 Release를 승인하지 않는다.
