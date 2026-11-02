# 첫 자동 검사 실패 원인과 확인된 부분 성공

검사 대상 SHA: af3e4649d5db0c372b879bf13de483c41ac0ed64.
전용 실행: https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41281371674/job/124773810405
기본 CI: https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41281374622/job/124773818795

## 읽은 실제 로그
전용 실행에서 Python 3.11.17, pypdf 6.21.4, pytest 9.2.0, Ruff 0.17.3 사용.
Ruff: FURB188, BLE001, TRY004, UP017 총 4개 오류 → FAIL.
전용 pytest: 26 passed in 0.21s → PASS. 합성 도구 시험이며 Studio 성능 시험 아님.
원본 인벤토리: documents=60, PASS=60, FAIL=0, BLOCKED=0, duplicate_hashes={}.
아카이브 SHA-256: a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc.
사람 검수, 시각적 검수, Studio 평가는 모두 NOT_RUN.
기본 CI는 같은 Ruff 4건에서 종료됐으며 그 실행의 전체 pytest 통과를 주장하지 않는다.
Node.js 경고와 Ubuntu 이미지 안내는 표시됐지만 확인된 실패 명령은 Ruff이다.

## 수정 범위
qa/inventory.py에서 문자열 접두사 처리, 구체적 PDF 예외 처리, manifest 타입 오류, UTC 표현을 수정한다.
기본 CI가 pypdf를 설치하지 않으므로 PDF 생성 시험 2개에만 선택 의존성 건너뛰기를 명시한다.
전용 CI는 pypdf를 설치하므로 해당 시험을 정상 실행해야 한다. 건너뜀을 통과로 보고하지 않는다.
기존 운영 CI, 운영 엔진, 원본 PDF와 DRAFT는 수정하지 않는다.

## 이후 확인
이 보고서의 PASS는 위 SHA의 관찰값이다. 수정 커밋의 결과는 별도로 확인해야 한다.
실제 인벤토리 CSV/기계 텍스트 파일의 개별 행은 아직 이 대화에서 읽지 않았다.
다음은 새 CI 결과 확인 및 원본 PDF 페이지와 기계 텍스트를 비교한 C001 검수 후보 작성이다.
