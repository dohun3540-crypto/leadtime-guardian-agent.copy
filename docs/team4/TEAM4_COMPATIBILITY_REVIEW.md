# Team 4 원본 문서 — Team1 .copy / 3rd 호환성 감사

## Git tree 비교
- Team4 Source PR1 `c34e9b7d6d310ef26f38c430f6ad8134afe47633`: **339** tracked blobs.
- 3rd latest inspected `25690af367db7f298c5f2b6acd984d94e6d5b35a`: source와 동일 Git Blob **308**, 같은 경로이지만 내용 차이 **25**, Source에만 있는 경로 **6** (본 인계 문서), 나머지는 3rd에만 존재.
- Team1 PR29 `bcd09794db7b5fe6c09ceffe84d33c5e98043479`: **397** tracked blobs, 신규 6개 모두 `docs/team4/`에 없음. 따라서 원래 문서 내용과 경로 충돌이 없음.
- 주요 차이 경로는 `README.md`, `docs/SUBMISSION_CHECKLIST.md`, `src/leadtime_guardian/engine.py`, `src/leadtime_guardian/strict_json.py`, QA/Cross-Agent 모듈 및 CI 등. 다른 Blob = 반드시 버그 아님; **Team4 코드로 무조건 덮어쓰기 금지**.

## 원본 그대로 보존한 충돌 및 주의
1. `FINAL_HANDOFF.md`의 Source repo 표시 `private`는 **현재 GitHub 메타데이터상 PUBLIC**와 불일치. 그 문서의 739 pytest 수치, `575745...` 소스 main, 원본 V4 Archive는 모두 과거 범위.
2. `SETUP_RUNBOOK.md`의 `git clone 061015ed-cys/Upstage-AI` 명령은 Source만을 위한 것. 3rd로 이식할 때 새 README 및 별도 runbook 지침에서 `3rd_task_dohun`으로 바꿔야 함. 원본 6개를 수정하지 않음.
3. Source의 `requirements-validation.txt`는 3rd에 존재하지만 **Team1 PR29에는 없음**. 따라서 `.copy` 브랜치 자체의 문서 원본 실행 명령을 현 상태에서 바로 정상 동작한다고 주장하지 않음.
4. 이전 README의 `scripts/generate_synthetic_dataset.py` 및 `data/gold/extraction_gold.json`은 조사한 Source/.copy/3rd Git Tree에 **없음**. Team4의 선택적 README 교정은 올바른 방향. `scripts/generate_c001.py`는 존재하지만 원본 C001 PDF의 무단 재생성을 권장하지 않음.
5. Source의 2026-10-30 V4 보존 데이터는 실측 V6 새 실행이 아니고, 실제 Independent QA Input/Report/StepRun/원본 receipt가 없으므로 Native E2E와 Release는 BLOCKED.
6. `SUBMISSION_PACKAGE_MANIFEST.DRAFT.json`은 Source main SHA 및 Source 문서 해시를 담은 **DRAFT_NOT_SUBMISSION_READY**. `.copy` 또는 3rd 제출용 Manifest로 자동 변경·승격·재사용 금지. 실제 대상 번들 SHA, 포함 자료, 공개 승인 여부를 새로 확정해야 함.
7. `OFFICIAL_SUBMISSION_REQUIREMENTS.md`의 **2026-11-11 13:00 KST** 마감은 [울산대 공지](https://ie.ulsan.ac.kr/ie/893?action=view&no=282626)와 일치. **2026-11-10 17:00**은 내부 동결 목표다. 포털 UI의 실제 필수 입력 규격·영상 길이·확장자/크기는 여전히 NOT_VERIFIED.
8. `.copy`와 Team4 Source가 현재 PUBLIC이므로 팀원 4 자료의 공개 범위를 재확인해야 함. `share_approved=false`는 심사 제출·재배포 승인 아님.

## 3rd 이식 원칙
기존 `README`와 제출 체크리스트는 무조건 덮어쓰지 않고, 6개 문서 파일만 `docs/team4/`에 추가. 출처와 상충하는 안내는 `TEAM4_README_CHECKLIST_DELTA.md`를 참조해 최소 변경. Python/QA/Gold/PDF/Config/CI는 변경하지 않음.
