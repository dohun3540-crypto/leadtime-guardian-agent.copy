# 검수 기록 형식 검사 — 범위와 제한

사용자 수정 XLSX는 채팅에 수신했으나 직접 셀 읽기 도구 내부 오류로 아직 검증하지 못했다. 파싱 텍스트의 열 병합과 잘림은 사용자 원본 셀의 오류를 증명하지 않는다. 그 텍스트로 승인 기록을 복원하지 않는다.

이번 구현은 qa/review_records.py와 합성 단위 테스트다. CSV 원본의 헤더, 행 식별자, 누락/중복, 검수자, 시간대 있는 ISO 시각, 승인 상태, ACCEPT, 고정 후보값/원문/페이지 변경을 검사한다. 변경값은 자동 교정하지 않고 NEEDS_REVIEW로 구분한다. CORRECT/AMBIGUOUS 등은 별도 검토 대상이며 자동 승인하지 않는다.

## 실행
python -m qa.review_records --review 사용자검수.csv --baseline qa/gold_candidates/SYN-C001/PDF_EVIDENCE_MATRIX.csv --out 새보고서.json
python -m pytest tests/qa -q
python -m ruff check qa tests/qa

CSV만 지원한다. XLSX 실제 셀 읽기와 날짜/금액의 자료형 보존 변환은 미구현이다. 사용자 XLSX를 변환하거나 실행한 것처럼 주장하지 않는다. 사용자에게 다시 CSV로 저장하라는 요구도 아니다.

PASS는 형식/후보 일치일 뿐 사람 신원·검수 사실 인증 또는 원본 근거 검증이 아니다. human_identity_verified/source_visual_review_verified/gold_promoted/official_metrics_eligible는 false로 유지한다. 입력 CSV와 기준 CSV의 바이트 SHA를 보고서에 기록한다. 미래 시각·검수자 권한·PDF 해시 연결·Gold 동결은 이 모듈의 검사 범위에 포함되지 않는다.

## 현재 상태
사용자 최신 XLSX 셀 검증: BLOCKED(도구 내부 오류).
사람 검수 수행 보고: 수신; 승인 범위 자동 확정하지 않음.
사용자 수정본 변환 및 검사: NOT_RUN.
도구/합성 테스트: 새 커밋에서 추가. 실제 CI 결과 별도 확인 필요.
PDF/DRAFT/운영 코드/설정 변경 없음.

## 다음
CI 결과 확인; XLSX 원본 바이트 읽기 경로 확보; 셀별 타입과 값 보존 후 검사; 확인된 승인 범위만 Gold로 버전화. 최신 실제 예측 수신 전 성능 수치 생성 금지.
