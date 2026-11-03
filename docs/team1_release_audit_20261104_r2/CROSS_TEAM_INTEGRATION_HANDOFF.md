# 통합 담당자 인계

읽기 전용 기준: yuseok_integration PR2 **67b93291c1f32acaf43e45815d2d1119480b652a**. 개인 원본: PR21 **edab2040430e2159399ee61073fe70e5bdf6cba2**. 신규 후보: **feat/team1-final-e2e-release-audit-20261104-r2**, 보호 PR21을 base로 하는 별도 Draft PR.

## 실제 호환성 판정

Git Clone 인증 실패 후 GitHub API로 통합336개 Blob 전체를 복원하여 크기와 `SHA1('blob '+byte_length+'\0'+bytes)`를 각 원본 SHA와 대조했다. 전부 일치했다. 이 **실행 가능한 전체 트리**에 PR20 신규 코드/CLI와 PR21 최종 코드·테스트·관련 문서11개를 추가했고 810개 실제 회귀가 통과했다. 이번 중첩 JSON 수정 적용 후 **812개 PASS**. 따라서 과거 STATIC_COMPATIBILITY_ONLY보다 강한 **PASS_LOCAL 실제 통합 시뮬레이션** 근거가 확보됐다. 원격 통합 PR은 변경하지 않았다.

최종 overlay에서 기존336개 중 바뀐 것은 팀원1 QA 소유 **studio_contract.py 및 test_qa_studio_contract.py 두 경로뿐**이다. strict_json/audit/input_delivery/engine/studio_adapter/qa.inventory 및 모든 data Blob은 통합 원본 그대로다. 기존 underflow·signed zero 보호를 개인 버전으로 덮어쓰지 않았다.

## 적용 순서와 원본 SHA

정확한 모든 path·parent Blob·최종 Blob은 `INTEGRATION_CHANGESET_MANIFEST.json`에 있다. PR21 diff만 복사하면 PR20에서 추가된 CLI/모듈을 놓칠 수 있다.

1. PR21 최종 e2e_bundle_preflight.py를 신규 추가한다.
2. PR20에서 도입된 team1_e2e_preflight.py CLI를 신규 추가한다(PR21 최종 트리에도 포함).
3. 새 감사 branch의 test_qa_parallel_e2e_bundle.py를 신규 추가한다(32개+이번CLI1개).
4. 기존 통합 studio_contract.py와 원본 Blob **08b23233ce12575c1c18f654e3ae296b8efa3e7c**를 대조한 뒤 parsing except에 RecursionError만 추가한다.
5. 새 branch의 test_qa_studio_contract.py diff에서 신규 API 재현 테스트1개만 기존 통합 테스트에 적용한다.
6. 필요한 새 감사 문서만 복사한다. 기존 PR20/21의 과거 STATIC_ONLY 문서를 현재 검증 결과로 오인하지 않는다.

새 package dependency 없음. 세 직접 dependency release_inventory/studio_contract(수정전)/experiment_compare의 두 repo 원본 Blob은 같으며 import/signature 충돌 없음. studio_contract의 새 변경은 exception handling만으로 API signature 변화가 없다.

| 충돌 분류 | 판정/조치 |
| --- | --- |
| FILE_PATH_CONFLICT | 신규3개 경로 없음. 기존2개는 위 명시한 최소 패치 |
| IMPORT_CONFLICT | 미발견, 실제 전체 import/회귀 통과 |
| SCHEMA_CONFLICT | Python 모듈 결합 충돌 없음. Studio null 선언 후보40개는 별도 운영 계약 |
| TYPE_CONTRACT_CONFLICT | Extract quote[]→Normalize quote object/null, blank→null 변환이 의도적. 전역타입을 동일화하지 않음 |
| PROVENANCE_CONFLICT | 현재 원본의 운영/QA Job이 다름은 허용. QA Input 결합·Receipt·Config 없어서 BLOCKED |
| TEST_FIXTURE_CONFLICT | 미발견. 기존778개 node ID 보존 |
| DEPENDENCY_CONFLICT | 미발견. 통합 선언 의존성으로 실행 |
| CI_WORKFLOW_CONFLICT | workflow 변경 없음. 개인/통합의 workflow/base필터 차이는 보존 |
| DATA_CONTRACT_CONFLICT | Gold 미승인·Stage metadata 미제공·null 선언 후보를 담당자에게 인계 |

통합 후 FINAL_REGRESSION_REPORT.md의 전체 pytest/Ruff/Archive/Gate/PDF 명령을 실행하고, **자체 새 HEAD에서 GitHub Actions SUCCESS**를 받아야 한다. 이번 로컬812개를 통합 원격 CI SUCCESS라고 표시하면 안 된다.

## 팀별 즉시 인계

| 담당 | 받을/확인할 자료 |
| --- | --- |
| 구도훈 | B0/E1 × C001/C013 각각의 원본 stage JSON, 운영 Normalize, QA Input/Report, Config ID/version, Job/Step/File, PDF upload receipt; 정적 null 계약 후보 확인 |
| 윤현준 | 동일 Native 원본 SHA로 실행한 Safety V6 output·원본 sidecar, 사용 commit/실행 명령. 생성 결과와 Studio 원문 grounding을 구분 |
| 김민주 | 최신 PDF_EVIDENCE_MATRIX.xlsx 원본·시트·typed cell·reviewer/time/decision·승인 Gold version/SHA. 40 PENDING 해소 |
| 발표 담당 | 로컬/보관 시연과 인증 Live 결과를 구분한 발표 자료. Greedy를 최적해로 표현하지 않음 |

Preflight는 C001 evidence manifest를 대상으로 한다. C013은 기존 combined E2E/B0-E1 validator로 실행한다. 별도 QA Job을 운영 Job과 같게 수정하거나, 의도된 PO999를 고치거나, 승인 필드를 자동으로 만들지 않는다.
