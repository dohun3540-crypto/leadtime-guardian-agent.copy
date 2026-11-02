# 기본 pytest 수집 경로 오류 수정

관찰 대상 SHA: 124b81e237bd33b3aea10183922ac8377955cff5.
전용 검사 https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41282902345/job/124778277639 는 success.
기본 검사 https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41282906137/job/124778289326 는 failure.
기본 로그에서 Ruff는 All checks passed. pytest -q는 tests/qa 두 파일을 수집할 때 ModuleNotFoundError: No module named 'qa'로 종료했다.

원인: 프로젝트 설치는 src 패키지를 대상으로 하며 별도 루트 qa 폴더는 설치하지 않는다. python -m pytest와 pytest 콘솔 명령의 경로 차이가 드러났다.
조치: tests/qa/conftest.py에서 해당 파일 위치로 저장소 루트를 결정해 시험 프로세스 검색 경로에 추가한다. 기존 운영 패키지와 CI 설정 변경 없음. 시험을 삭제하거나 오류를 skip 처리하지 않는다.

수정 커밋의 통과는 아직 확인 전이며 별도 새 CI 결과를 확인한다. 전용 검사 통과는 원본 기계 검사/도구 시험이며 사람 검수, Gold 승인, Studio 정확도 평가가 아니다.
