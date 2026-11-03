# 팀원 1 최종 E2E·데이터·통합 감사

감사일: 2026-11-03 KST. 11월 4일 인계용. 담당: 구도훈.

**판정: 로컬 코드 수정·통합 회귀 완료. 정식 제품 Release는 BLOCKED.**

## A. 달성률과 판정 범위

| 지표 | 현재 평가 | 산정 기준 |
| --- | --- | --- |
| 11/4 팀원 1 담당 검증 업무 | 약 96% | 요청한 종료 조건 13개 중 12개 완료, 데이터·출처 계약 1개는 로컬 완료/실측 부분 미완료: 12.5/13. 신규 원격 CI는 PR의 최종 검증 기록을 추가 확인 |
| 팀원 1 최종 제출 준비도 | 약 78% | 코드 40/40, 격리 통합 20/20, 계약 10/10, 출처 자료 7.5/15, 인증된 Live 0/10, 승인 Gold 0/5. 엔지니어링 체크리스트 점수이며 성능·정확도 아님 |
| 팀 전체 최종 제출 준비도 | 산정 불가 | 네 번째 팀원의 발표·시연·제출 문서와 최종 공통 트리 확인 자료 부족. 팀원 1 점수를 팀 전체 점수로 확대하지 않음 |

작업 시간을 8시간으로 채우지 않았다. 코드·자료를 실제 복원하여 검사했으며, 변경 없는 검사 반복으로 시간을 소비하지 않았다. 로컬 환경은 Python 3.12.14, 원격 기존/신규 CI는 Python 3.11이므로 결과를 분리한다.

## B. GitHub 기준선

| PR | 최신 확인 HEAD | 상태 | 확인한 해당 HEAD CI |
| --- | --- | --- | --- |
| 개인 #19 | 5d3172deaeecafec0056b48c92f0f0f6bb08297a | Open/Draft/Unmerged/mergeable | SUCCESS #41465821541, #41465821704 |
| 개인 #20 | 53ae1a7dbe53be38a7d585676c2b2d037534fb46 | Open/Draft/Unmerged/mergeable | SUCCESS #41469788883 |
| 개인 #21 | edab2040430e2159399ee61073fe70e5bdf6cba2 | Open/Draft/Unmerged/mergeable | SUCCESS #41474378468 |
| 통합 #2 | 67b93291c1f32acaf43e45815d2d1119480b652a | Open/Draft/Unmerged/mergeable | SUCCESS #41465445285 |

네 PR 모두 미해결 inline review thread 0개. 기존 브랜치/PR은 수정하지 않았다. 권장 새 브랜치는 이미 존재하여 해당 HEAD 81569b0ddcc384388ee0e2575ba3cc38cb1bf895를 변경하지 않고 **feat/team1-final-e2e-release-audit-20261104-r2**를 PR21 HEAD에서 새로 만들었다.

새 commit SHA 및 최종 CI는 이 문서를 포함하는 commit 자체에 선기록할 수 없으므로, **새 Draft PR 본문의 최종 exact-HEAD 검증 기록**과 배포용 `CI_ATTESTATION.json`을 사용한다. 이 문서의 상위 PR CI를 새 commit CI로 간주하지 않는다.

## C. 신규 코드 결함

**P1 1건 발견·수정: 중첩 Native JSON의 RecursionError가 Native QA와 E2E Preflight 밖으로 전파됨.**

- 재현: 유효한 Native envelope의 `content`에 깊은 JSON 배열 문자열을 넣는다. 통합 환경은 1,500단계에서도 재현됐고, 재현 테스트는 Python 버전에 관계없이 충분한 100,000단계(약 200KB)를 사용한다.
- 원인: `qa/studio_contract.py`의 JSON parsing 예외 처리에 RecursionError가 빠졌다. 공급자 원본의 content는 문자열이므로 외부 envelope 검사에서는 이 깊이가 검출되지 않는다.
- 최소 수정: 기존 parsing 예외 tuple에 RecursionError 하나 추가. 실패 코드 `INVALID_OR_DUPLICATE_NATIVE_JSON`과 기존 `OPERATIONAL_NATIVE_CONTRACT_FAILED`를 그대로 사용한다.
- Red: 직접 API와 CLI 재현 테스트 **2 failed**. Green: 동일 2개 **PASS**. 전체 개인 **750 PASS**, 격리 통합 **812 PASS**. 테스트 삭제·skip·기대값 완화 없음.
- 영향: 비정상 입력에서 구조화된 FAIL 대신 예외로 끝나는 문제. 잘못된 Release 승인 사례는 발견하지 않았다.
- 현재 알려진 미수정 필수 팀원 1 코드 결함: **0건**. 무결함의 수학적 보증을 뜻하지 않는다.

## D. E2E 증거

| 단계 | 이번 관찰 | 한계 |
| --- | --- | --- |
| C001 보관 V4 | 원본 Archive Replay PASS_LOCAL | 현재 B0/E1가 아님 |
| C001 최신 XLSX | job_DkzsPqVpfBkXLSDvScbdgC, 세 문서 한 Job 표시, Config Ver 1 | Normalize/QA 원본·업로드 SHA/Config ID 연결 없음. XLSX의 병합 셀은 Job 상위 정보이므로 행별 독립 Job으로 세지 않음 |
| C013 Normalize | job_aq9eWmd23vb4G6DySyF5sF, 3개 문서, PO999/PO1 경고 | 현재 B0/E1 별칭과 Config/version, 원본 Upload Receipt 없음 |
| C013 QA | job_jLmpnZczhWEnG8PbWxKhrE, NEEDS_REVIEW/PARTIAL, 원본 Adapter PASS | 별도 QA Job 허용. 본문 execution_provenance 4항목 null, workflow_version null, 실제 QA Input과 운영 Job 연결 미제공 |
| V6 | 위 C013 원본 바이트를 로컬 실행: BLOCKED, 독립 Safety SAFELY_BLOCKED_LOCAL | 팀원 2가 생성한 실제 Sidecar 원본과 Live 실행 결과는 없음. 이번 재생 결과를 그 원본으로 대체하지 않음 |
| Cross-Agent/Provenance | 로컬 회귀 PASS_LOCAL | QA Input 원본·운영 Job 결합·실제 receipt가 없어 현재 자료의 완전한 Cross-Agent 인계는 BLOCKED |
| B0/E1 | 네 조합의 계약·실패 차단 회귀 통과 | 네 조합의 인증된 실행 묶음 없음. 정확도·개선률 계산 안 함 |
| Gold | 후보 human_reviewed=false, Matrix 40행 모두 PENDING | `gold/` 이름의 내보내기 자체는 사람 승인 증거가 아님 |

실측 파일의 해시와 세부 증거는 비공개 배포 패키지에 보존했다. Native 원본을 수정하거나 공개 GitHub에 올리지 않았다.

## E. 데이터 품질

20 Case × 3 PDF **60/60**을 이번 실제 바이트로 검사했다. 3개는 개별 파일, 57개는 보호된 tar.xz 원본의 멤버다. 모두 파일 크기·PDF 포맷·manifest SHA·Document ID 유일성·Case/Document ID 파싱 텍스트 연결 통과. 중복 SHA 0. 데이터 원본 **68/68 Git Blob 보존**.

전체 60개 파싱 텍스트를 읽었고 C001/C008/C013/C017의 12개 PDF는 별도 이미지 렌더링과 AI 시각 점검도 수행했다. 이는 사람의 정답 승인이나 60개 전부의 시각 검수 완료가 아니다.

| 품질 영역 | 판정 | 근거/남은 일 |
| --- | --- | --- |
| Completeness | PASS_LOCAL | 20 Case/60 PDF·manifest 존재. Live 단계 원본은 부분 누락 |
| Validity | PASS_LOCAL/부분 | PDF 포맷·DRAFT Schema 조사. 정상/의도적 오류 시나리오는 구분 |
| Consistency | PASS_LOCAL/부분 | 주요 4 Case 업무 역할 대조. 추출→Normalize는 빈 문자열·배열 변환이 의도된 구간 |
| Uniqueness | PASS_LOCAL | SHA·Document ID 중복 0, 기존 Receipt/File/Step 오류 주입 회귀 |
| Integrity | PASS_LOCAL | 336개 통합 소스 Blob 검증, 68개 data Blob 보존, 60 PDF SHA 일치 |
| Traceability | BLOCKED Live | 로컬 파일 연결은 검증, cloud Upload Receipt·QA Input·Sidecar 없음 |
| Business semantics | PASS_LOCAL/부분 | C001 100발주/100변경/60견적 역할, C008 R2만 변경, C013 의도 PO충돌, C017 한글 원문→DRAFT ISO 대조 |
| Gold readiness | PENDING | 후보 미승인, 최신 사람 검수 XLSX 없음 |

현재 Studio export의 기존 top-level 정적 검사에서 null 지시/타입 충돌 후보 **8개**. 별도 중첩 필드 기술 감사에서 명시적 `Null if/Null when`이 있으나 null 불허인 선언은 **40개(위 8개 포함, quote[] 32개 추가)**. 모두 실제 실행 실패 수가 아닌 정적 계약 지적이다. 기존 과거 68개 수치와 혼합하지 않는다. 담당자: Studio 설정 총괄 구도훈, Adapter 경계 검토 윤현준. 원본 설정은 변경하지 않았다.

## F. B안과 C안

| 기능 | 구현/로컬 | 실제 Studio 범위 | 시연 판단 |
| --- | --- | --- | --- |
| B 기본 처리 | 기존 분류/추출/병합/Normalize 계약 회귀 PASS_LOCAL | 보관 C001·C013 일부 출력 있음 | 보관 자료 기반 시연 가능, 현재 전체 Live 완료 주장 불가 |
| C1 Counterfactual | 원래/변경 ETA 계산·차이 회귀 PASS_LOCAL | 인증된 비교 Live 없음 | 로컬 재현 시연 가능 |
| C2 Evidence Safety | PO충돌·출처/SHA/Config/Case 차단 PASS_LOCAL | C013 원본 경고+QA NEEDS_REVIEW 관찰, PDF 업로드 provenance 미완료 | 안전 차단 사례는 제시 가능. PDF 원문 검증 완료 제품으로 표현 불가 |
| C3 Partial delivery | R1/R2, 재고 1회 사용, capacity·운송비 회귀 PASS_LOCAL | C008 Native 없음 | 로컬 합성 시연 가능. Greedy를 최적화 알고리즘이라 부르지 않음 |

C001 기준 재고는 trusted JSON **40**, 고객 주문 **100**이므로 부족량 **60**, 견적 배정 **60**, 비용 **60,500원**. PDF 발주량 100과 견적 capacity 60이 다르다고 충돌 처리하지 않는다. C008은 재고20+R1 40으로 고객100 중60 배정, 부족40, 대체40·40,500원. C017 DRAFT ISO 계산은 통과했으나 한국어 날짜를 Studio가 실제 정규화했다는 증거는 없다.

## I. 최종 질문 답변

1. **개인 코드 개발을 종료해도 되는가?** 이번 수정의 새 exact-HEAD CI 성공 확인 후 동결 가능. 새 재현 결함 없이 코드 확장을 계속할 이유는 없다.
2. **알려진 필수 QA 코드 결함 수?** 1건 발견·수정, 미수정 0건. 별도 정적 Studio 계약 후보는 남아 있다.
3. **PR21 기능 통합 가능?** 가능. PR20 신규 모듈/CLI/테스트 + PR21 최종본을 함께 적용했고, 이번 예외 패치도 포함한 812개 로컬 통합 회귀가 통과했다.
4. **실제 통합 트리 전체 회귀?** 수행했다. 정확한 API Blob으로 복원한 실행 가능한 트리이며 Clone/원격 통합 CI는 아니다. 778개 원래 node ID 전부 보존.
5. **데이터/Schema 수준?** 기계 무결성 완료, 주요4 Case AI 의미 대조 완료, 전체 사람 정답/클라우드 실행 계약은 미완료.
6. **C1/C2/C3 실측 완료?** 완전한 인증 E2E 기준 0개. C2 C013 안전 경고만 실제 보관 출력에서 부분 관찰.
7. **Native 도착 즉시 검증 가능?** 포맷·Job·Config·PDF receipt·Sidecar·QA Input이 함께 오면 기존 CLI로 가능. Native 하나만으로 모든 Live Gate를 해제할 수는 없다. 새 Preflight는 C001 release manifest 전용이며 C013은 기존 Combined/B0-E1 도구를 사용한다.
8. **최대 제출 차단 원인?** 네 B0/E1 조합의 완전한 동일 원본 인계와 사람 승인 Gold 부재.
9. **실측·평가로 전환 가능?** 가능. 신규 QA 기능 추가보다 원본 수신·정적 Studio 계약 확인·사람 검수·실측 연결 우선.
10. **11/4 최우선?** 구도훈: 네 조합의 stage Native/QA Input·Receipt·Config/Job/Step 수신 → 윤현준: 같은 Native SHA의 V6 결과·Sidecar → 김민주: 원본 검수 XLSX·승인 Gold 동결 → 합동 E2E와 공식 비교. 네 번째 팀원은 이 검증 범위를 명시한 시연·발표 준비.

회귀 상세는 FINAL_REGRESSION_REPORT.md, 필드 계약은 DATA_CONTRACT_CONSISTENCY_MATRIX.md, 적용 경계는 CROSS_TEAM_INTEGRATION_HANDOFF.md, 기계 판정은 FINAL_RELEASE_GATE.json에만 상세화했다.
