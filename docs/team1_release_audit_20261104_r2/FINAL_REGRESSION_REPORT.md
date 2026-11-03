# 최종 회귀 근거

## 실행 결과

| 실행 트리 | 전체 pytest | QA subset | fail/skip | 의미 |
| --- | --- | --- | --- | --- |
| 개인 PR21 정확한 원본 345 Blob | 748 | 499 (기존 CI 기록) | 0/0 | 이번 로컬 full 748 재확인 |
| 통합 PR2 정확한 원본 336 Blob | 778 | 별도 가산 안 함 | 0/0 | PYTHONPATH=src로 소스 경로를 고정한 재확인 |
| 통합 + PR20/21 파일 11개 | 810 | 별도 가산 안 함 | 0/0 | 원래 파일 overwrite 0, 신규 Preflight 32개 포함 |
| 신규 수정 개인 트리 | **750** | **501** | **0/0** | 재현 테스트 2개 추가; QA 수는 XML class명이 test_qa_로 시작하는 subset |
| 신규 수정 격리 통합 트리 | **812** | **544** | **0/0** | 778개 원래 node ID 전부 보존, 신규 34개 포함 |

개인750과 QA501은 중첩된다. 통합812와 QA544도 중첩된다. 서로 더하지 않는다. 실제 JUnit XML을 사용했으며 예상 덧셈만으로 집계하지 않았다. 모든 기존 778개 테스트의 class/name 식별자가 최종812개에 포함된다.

로컬 Python 3.12.14; pytest9.2.0; Ruff0.17.3. 전체 선언 의존성 requirements-validation.txt 설치. 원격 기준선은 Python3.11이며 새 원격 CI의 실제 결과는 새 Draft PR에 기록한다.

- 개인/통합 각각 repository Ruff: All checks passed.
- Archive: qa_status=PASS, ARCHIVED_RECORD_ONLY, 원본 PDF SHA 확인.
- Local Gate: local_checks_passed=true, overall_status=BLOCKED, release_or_merge_authorized=false.
- PDF Inventory: 이번 개인·통합 두 트리 각각 60 PASS / 0 FAIL / 0 BLOCKED, duplicate hash 0. 원본 archive SHA a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc.
- C001/C008/C017 DRAFT 입력 로컬 COMPLETED, C013 DRAFT/보관 Native 입력 안전 BLOCKED. 의도된 차단은 계산 테스트 실패가 아님.
- 추가 malformed header 25개 분석 probe: 24 FAIL, 정상적인 sources={} 1개 BLOCKED, 예외0, release 승인0. 별도 pytest 개수에 더하지 않음.
- 실제 Job-list XLSX Snapshot: NEEDS_REVIEW, merged ranges10. 병합된 Job 정보가 세 Extract 행에 걸쳐 있으므로 셀을 자동 수정하거나 승인 처리하지 않음.

## 재현 가능한 명령

```bash
python -m pip install -r requirements-validation.txt
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
python -m ruff check .
python scripts/qa_archive_check.py --root .
python scripts/qa_gate_check.py --root .
python -m qa.inventory --root . --out /tmp/new-inventory-output
```

개인 저장소에는 requirements-validation.txt가 없으므로 requirements-agents.txt와 qa/requirements.txt를 사용한다. 출력 경로는 기존 폴더를 덮어쓰지 않는 새 경로를 사용한다.

## 원격 CI와 범위 제한

PR19/20/21/통합PR2의 원격 exact-HEAD SUCCESS를 이번 조회로 확인했다. 새 코드의 원격 CI는 이 보고서 작성 시 시작 전이며, **새 Draft PR의 최종 검증 기록 및 배포 패키지 CI_ATTESTATION.json이 최종 근거**다. 새 branch의 PR base는 보호 PR21이다. 기존 member3 workflow의 base branch 필터와 맞지 않아 PDF 전용 CI가 실행되지 않을 수 있으며, 그 경우 로컬60/60과 원격QA workflow를 구분한다. Workflow를 바꾸어 실행 수를 늘리지 않는다.

로그·JUnit·PDF·출처 목록은 배포 패키지의 evidence/ 아래 보존한다. 원격 통합 저장소에는 commit/push를 하지 않았으므로 통합의 새로운 원격 HEAD/CI는 없다.
