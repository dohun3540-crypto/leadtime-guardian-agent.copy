# 新 session regression and selective integration

기준 개인 checkpoint 8b671d4a67cd649b08c4e6603a457f607342c3d7, remote code commit 6929ea1dc29e1ad6c1d1c604dd1180968ef7ec1a, 격리 통합 기준 67b93291c1f32acaf43e45815d2d1119480b652a. 기존 수치와 이번 실측은 아래처럼 구분한다.

| 검증 | 중단 전 기록 | 이번 새 실행 | 판정 |
| --- | --- | --- | --- |
| 개인 full pytest | 750 | 754 / 0 fail / 0 skip | PASS_LOCAL; 기존750 + 도구 경계4 |
| 개인 Independent QA | 501 | 505 | PASS_LOCAL; 전체754의 subset |
| Team1 E2E selected | 별도 합산 안 함 | 106 | PASS_LOCAL; 전체754의 subset |
| 격리 통합 full | 812 | 812 / 0 fail / 0 skip | PASS_LOCAL; 기존778 nodeID 전부 보존 |
| 격리 통합 QA | 544 | 544 | PASS_LOCAL; 전체812의 subset |
| 전체 Ruff | PASS | 개인·격리 통합 PASS | PASS_LOCAL |
| C001 archive/replay | PASS | 양쪽 archive/local Gate, 새 demo 정상 | PASS_LOCAL |
| PDF 원본 기계 검사 | 60/60 | 양쪽60/60, 오류0 | PASS_LOCAL; 사람 semantic 검수 아님 |
| C001 Preflight | BLOCKED | BLOCKED, invalid_inputs=[], exception 없음 | 예상 안전 진단 PASS_LOCAL |
| source commit CI | checkpoint queued | checkpoint SUCCESS; PR25 code CI SUCCESS | PASS |
| 실제 Studio QA input chain | BLOCKED | 후보 v2 Normalize만 추가 회수 | BLOCKED |
| B0/E1 | formal0/4 | formal0/4 | BLOCKED / metrics NOT_MEASURED |

개인 full과 격리 통합 full을 직렬로 실행했다. 기존 병렬 SDK fixture timeout 실패/독립 PASS/직렬812 PASS 로그는 원본143파일에 그대로 보존했고 이번 실패로 재집계하지 않는다. 테스트 삭제, skip 추가, 기대값·timeout 변경은 0이다.

검증 명령: `PYTHONPATH=src python -m pytest -q`, `PYTHONPATH=src python -m pytest -q tests/test_qa_*.py`, `python -m ruff check .`, `python scripts/qa_archive_check.py --root .`, `python scripts/qa_gate_check.py --root .`, `python -m qa.inventory --root . --out /ABS/out`. Team1 subset은 parallel_e2e_bundle, studio_contract, combined_e2e_cli, stage_trace, b0_e1_comparison, experiment_identity_hardening 테스트106개다. 실제 stdout/JUnit은 private results/에 있다.

PR25 code CI [41614855340](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41614855340) completed SUCCESS, 실제 로그505 QA /754 full /Ruff PASS. GitHub checkout synthetic merge `89b04154431cf52126068d57131789a0ad75cdb1`의 tree `ef6d9db5ef6f65c1b7f41970ad103514aba9cd23`가 code HEAD tree와 정확히 일치함을 API로 확인했다. 최종 문서 커밋의 exact-head CI는 후속 PR attestation과 전달 ZIP에서 별도로 확인하며 이 source CI를 최종 SHA CI로 바꾸어 부르지 않는다.

선택 패치의 세 경로는 ADD, 기존 두 경로는 최소 패치다. 336개 기준 source blob을 확인했고 strict_json/engine/studio_adapter/QA 운영 안전/qa.inventory는 SHA가 동일하다. 모든 dependency가 기존 base에 있어 추가 운영 모듈 복사가 필요하지 않다. 원본 data/Gold/workflow를 바꾸지 않았다. integration 원격 적용·원격 신규812 CI는 NOT_MEASURED이며 maintainer가 담당한다.
