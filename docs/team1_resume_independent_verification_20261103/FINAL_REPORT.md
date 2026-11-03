# Team 1 체크포인트 재개 및 독립 보완 검증 — 2026-11-03

전체 Release는 **BLOCKED**다. 체크포인트 복원과 가능한 로컬 작업을 완료했으며, 신규 Studio 실행·공식 비교 성능을 주장하지 않는다.

## 복원 결과와 작업 관계

- 체크포인트 `checkpoint/team1-e2e-resume-20261103` / `8b671d4a67cd649b08c4e6603a457f607342c3d7`와 Draft PR #24를 확인했다. 당시 QUEUED였던 Independent QA run `41610223172`는 현재 completed/SUCCESS다.
- 원격 recursive Git tree와 로컬 bytes를 비교해 체크포인트 363파일, 고정 통합 기준 336파일을 복원했다. Git tree `a7d1e7449735fd7965db25f66a01118edf985832`와 실제 checkpoint commit object SHA까지 재구성해 로컬 HEAD를 검증했다. 기존 private snapshot 원본·로그 143개 SHA는 전부 일치했다.
- 일반 Git clone은 인증 정보가 없어 실패했다. 연결된 GitHub 접근으로 원격 SHA를 조회하고 보존된 로컬 bytes를 Git Blob SHA로 검증해 복원했다. 인증 토큰을 출력하지 않았다.
- 저장 시점에 동일 체크포인트에서 이어진 Draft PR #25를 발견했다. 해당 HEAD `6929ea1dc29e1ad6c1d1c604dd1180968ef7ec1a`는 도구 2개와 경계 테스트 4개를 포함한다. CI `41614855340` completed/SUCCESS를 확인했다. 이 도구를 그대로 받아 Git tree `ef6d9db5ef6f65c1b7f41970ad103514aba9cd23`와 일치시킨 후 실제 검증했다. 중복 CLI를 새로 제출하지 않았다.
- 이 브랜치는 PR #25의 코드를 수정하지 않고 독립 검증·시연 매뉴얼·증거 인덱스만 보완한다. PR #24/#25를 대체하거나 close하지 않는다. 신규 필수 운영 코드 결함은 발견하지 않았다.

## 실제 수행 결과

| Task | 판정 | 이번에 확인·완료한 범위 | 남은 부분 |
| --- | --- | --- | --- |
| A | BLOCKED | 이전 미확보 v2 Normalize를 실제로 다운로드·SHA 검증. C001 한 Native에 PDF3종/3 File ID가 묶임을 확인 | QA 실제 Input, raw Merge, provider 단계 trace/receipt 및 동일 바이트 연결 |
| B | BLOCKED | B0 보고 실행과 unassigned v2의 Config/Job/Native/QA를 대조하고 두 출력을 로컬 재생 | 인증된 4조합 0/4, E1 alias 미인증, 공식 정확도/개선율 NOT_MEASURED |
| C | PASS_LOCAL | 정확한 40행 전부 required/null/숫자 옵션/프롬프트/관찰/재현/위험/담당 분류. 추가 경계 probe16개 안전 차단 | Provider nullable 런타임, 미관찰 other/missing-value 분기 |
| D | PASS_LOCAL | 기존 C001 Preflight 재사용, invalid_inputs=[]/BLOCKED, release_authorized=false. C013은 Combined 사용 | Live E2E 승인 범위는 계속 BLOCKED |
| E | PASS_LOCAL | PR25 CLI로 C001/C013 및 C008/C017 실행, 팀원이 재현할 시연·평가 매뉴얼 작성 | 한국어 PDF→날짜 실제 추출 및 공식 Gold 평가 미측정 |
| F | PASS_LOCAL | 정확한 5경로 patch를 격리 통합 기준에 적용·검증, 812/544 및 기존778 ID 보존, 나머지334 base blob 보존 | 통합 담당자의 원격 반영 및 외부 E2E/Grounding/Gold |

## Native 증거의 의미

신규 회수한 원본은 과거 Job `job_RpJUGhdMWSH6iww476BjFJ`의 Config v2 Normalize다. SHA256 `6223e5ce21e39da70bd62c4c0a2a3d9641b30fa2bb9de04f5e276d8551156eca`. Agent/Config/Job/Step/File ID는 `NATIVE_RECOVERY_REPORT.json`에 있다. 이 원본은 신규 실행이 아니라 저장 결과 회수다.

Native 한 개에 purchase_order/delivery_notice/quotation과 서로 다른 File ID 3개가 존재한다. 같은 Job QA와 source rows도 일치한다. 그러나 QA는 `NORMALIZED_OUTPUT_NOT_PROVIDED`를 보고하고, 실제 QA 입력 bytes는 없다. 저장 config에는 Normalize→QA edge가 있으나 그것만으로 실제 평가 입력을 인증하지 않는다. 결과 패널은 출력 preview/JSON을 제공하며 실제 input/raw Merge export는 관찰하지 못했다. 접근 차단 오류나 provider 런타임 원인을 추측하지 않는다.

기존 v4 C001/C013, 보고된 B0 C001, unassigned v2 C001을 모두 별도 식별했다. 해당 Native의 로컬 계산은 C001 부족60/60,500원, C013 경고·PO1/PO999 보존 후 BLOCKED다. 로컬 생성 Sidecar는 원본 Native SHA와 일치하지만 Team2 본인 실행 인계가 아니다. 기존 Config 두 개의 차이는 workflow_name과 numeric-null 옵션 4개 추가이며, 이 차이만으로 E1을 지정하지 않는다.

## Schema 판정

기존 PR25 도구의 선언 기준은 36 POTENTIAL_CONFLICT / 4 NOT_VERIFIED다. 이 보완 검토는 같은40 pointer의 실제 관찰 경로를 13 POTENTIAL_CONFLICT / 16 INTENDED_TRANSFORMATION / 11 NOT_VERIFIED로 구분했다. 두 라벨을 각 JSON 행에 함께 기록했다.

16개는 non-quotation의 빈 quote[]에 child row가 없는 의도된 경로에 한정된다. 다른 실행의 미래 null 경로를 안전하다고 승인하지 않는다. other10개와 숫자옵션이 있는 quotation.capacity1개는 실제 동작 미확정이다. 실제 null branch Native 실패 확인은0건이다. 설정·스키마·Gold를 수정하지 않았으며 40개 일괄 nullable patch를 적용하지 않았다.

## 이번 세션 검증

| 검사 | 결과 | 기준 |
| --- | --- | --- |
| 체크포인트 전체/QA | 750 / 501 PASS | PR25 적용 전 원본 기준 |
| PR25 고정 도구 포함 전체/QA | 754 / 505 PASS | 원래750 + PR25 기존4, 이 보완에서 추가 테스트0 |
| Team1 E2E/contract/provenance | 86 PASS | 5개 파일 subset, 전체와 합산하지 않음 |
| 격리 통합 전체/QA | 812 / 544 PASS | 고정 통합 + 보존5경로; PR25 도구3파일은 미포함 |
| 기존 통합 test ID | 778/778 보존 | 누락0 |
| Ruff | PASS | 개인 PR25 소스와 격리 통합 각각 |
| C001 Archive/Replay | PASS_LOCAL | 보관자료 재생, 신규 Live 아님 |
| C001/C013 시연 | PASS_LOCAL | C001 COMPLETED; C013 SAFELY_BLOCKED_LOCAL |
| C008/C017 시연 | PASS_LOCAL | DRAFT fixtures, C017 PDF 파싱 미측정 |
| PDF 원본 기계 inventory | 60/60 PASS | 사람 검수·Gold 승인 아님 |
| Local Integration Gate | PASS_LOCAL | overall_status=BLOCKED |
| Native Studio QA·B0/E1 공식 비교 | BLOCKED | 실제 Input/trace/receipt/Gold 누락 |

원본 XML·로그·Native는 private 전달물에 보존한다. 위 수치는 이번에 실제 실행한 결과이며 과거 체크포인트 수치를 새 실행으로 재표기하지 않는다. 신규 커밋/CI는 이 문서의 커밋 이전 경계 이후에 생기므로 최종 PR 본문과 전달 ZIP의 `POST_PUSH_ATTESTATION.json`을 참조한다.

## 보호와 다음 단계

원본 저장소, 개인 main/PR19/20/21/23/24/25, 통합 main/PR2와 Team2/Team3 운영 source/data/Gold는 쓰지 않았다. 새로운 개인 보완 브랜치만 사용한다. 통합 실험은 로컬 격리 디렉터리에서 수행했고 원격 통합 push/merge/force push는0회다.

다음 우선순위는 실제 QA Input·provider trace/receipt 확보 → 별칭과 4조합 연결 → Team2 동일 Native 실행/Sidecar와 사람 승인 Gold → 기존 자동 검증기로 Release 재평가다. 세부 요구와 담당은 `NEXT_ACTIONS.md`, 재현은 `DEMO_MANUAL.md`, 파일 SHA와 누락항목은 `EVIDENCE_MANIFEST.json`에 있다.
