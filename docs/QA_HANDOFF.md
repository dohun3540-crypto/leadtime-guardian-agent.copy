# 팀원 3 QA 작업 인계 — 첫 구현

## 기준선과 보호 범위
원본 저장소 dohun3540-crypto/leadtime-guardian-agent.
작업 브랜치 feat/qa-ground-truth-evaluation.
작성 전 원격 HEAD: f196c694917f2d9e5f4ec228c752bd3f2a4eb882.
본 커밋 SHA는 이 문서 자체에 예측해 넣지 않고 Git 이력에서 확인한다.
기존 PDF, extraction_gold.DRAFT.json, engine, Adapter, API, Studio 설정, 기존 CI는 변경하지 않는다.
main/PR #11 직접 커밋·병합·force push·외부 제출 없음.

## 실제 확인
- QA 브랜치 HEAD 조회 성공.
- C001과 C002 manifest를 GitHub에서 조회해 documents 배열, document_id, document_type, filename, sha256 계약 확인.
- C001 manifest에는 pages가 있지만 C002에는 없다. 누락 페이지 수는 추정하지 않는다.
- manifest의 studio_executed는 오래된 선언과 실제 보관 Job 이력이 다를 수 있어 평가 증거로 자동 승격하지 않는다.

## 작성 산출물
qa/inventory.py, 합성 단위 테스트, 별도 의존성, 검수·coverage 빈 CSV 양식, 실행·상태 해석 문서.
실제 인벤토리 결과, 원문 Gold 후보, 사람 승인 기록, 성능 지표는 아직 생성하지 않았다.

## 상태
- 코드/양식 작성: 작성됨, 실행 검증 전.
- pytest: NOT_RUN.
- Ruff: NOT_RUN.
- 실제 PDF 바이트/페이지/텍스트 기계 검사: NOT_RUN.
- 원본 시각적 검수: NOT_RUN; 이번 작업 검수 PDF 0개.
- Gold 후보: 0개. 사람 승인 기록: 미확보.
- Studio 성능 평가: BLOCKED(동결된 검수 Gold와 해당 실제 예측 결합 필요).
- 최신 PR #12/QA 사본 PR #2 계약·CI 재확인: NOT_RUN. 이 도구는 운영/QA 코드를 import하지 않는다.

## 실행 제약
현재 대화에는 터미널 실행 도구가 없다. GitHub 파일 저장은 테스트 실행이 아니다.
기존 CI는 main push/main 대상 PR 조건이므로 이 브랜치 커밋만으로 자동 실행됐다고 주장하지 않는다.
팀원 2 결과가 없어도 검사 코드 실행과 원문 검수는 가능하다. 실행 가능한 개발 환경/CI 경로 확보는 별도 작업이다.

## 다음 검증
qa/README.md 명령으로 검사/테스트를 실행하고 로그·환경·Git SHA를 보존한다.
기계 텍스트를 눈으로 본 PDF 대신 사용하지 않는다. 검수자는 원본 페이지와 비교한다.
팀원 2에는 읽기 전용으로 Native/Parse/Extract/Job/Config/Step/입력 파일 해시를 요청한다.
팀원 1에는 향후 승인 Gold 해시, 검수 수준, coverage, 지표 분모와 중요 오류를 전달한다.
