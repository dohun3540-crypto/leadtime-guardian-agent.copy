# Team 4 → 3rd 단일 저장소: 안전한 차기 이식 절차

**이번 단계에서는 3rd 및 `integration_finished_workforlast`에 쓰기 작업 0회.** 파일 6개를 `.copy`의 독립 인계 브랜치에 보존한 뒤 소스와 해시를 확인함.

## 준비물과 Source pins
1. 3rd 신규 작업 시작 시 **최신** `main` 및 개발 브랜치, PR #1·#2, CI HEAD를 재조회. 현재 조사한 참고 SHA `25690af367db7f298c5f2b6acd984d94e6d5b35a`는 이식 시 자동 재사용 금지.
2. Team4 원본 `061015ed-cys/Upstage-AI` PR #1 exact HEAD `c34e9b7d6d310ef26f38c430f6ad8134afe47633`와 6개 Git blob/SHA256 기록을 확인.
3. Team1 `.copy` handoff 브랜치 `feat/team4-submission-handoff-20261104`의 실제 PR/HEAD, `TEAM4_SOURCE_MANIFEST.json`을 확인. 이전 Team1 PR29 `bcd09794db7b5fe6c09ceffe84d33c5e98043479`는 보호된 기준선.
4. 3rd의 기존 `docs/team4/` 경로가 없는지 다시 검사. 충돌 시 **별도 복제 디렉터리**로 보존하고 리뷰를 받아야 하며 원본 덮어쓰기 금지.

## 3rd 이식 매핑
| .copy 보관 원본 | 3rd 목적지 |
| --- | --- |
| `docs/team4/DEMO_AND_PITCH.md` | `docs/team4/DEMO_AND_PITCH.md` |
| `docs/team4/FINAL_HANDOFF.md` | `docs/team4/FINAL_HANDOFF.md` |
| `docs/team4/OFFICIAL_SUBMISSION_REQUIREMENTS.md` | `docs/team4/OFFICIAL_SUBMISSION_REQUIREMENTS.md` |
| `docs/team4/PRE_FLIGHT_CHECKLIST.md` | `docs/team4/PRE_FLIGHT_CHECKLIST.md` |
| `docs/team4/SETUP_RUNBOOK.md` | `docs/team4/SETUP_RUNBOOK.md` |
| `docs/team4/SUBMISSION_PACKAGE_MANIFEST.DRAFT.json` | `docs/team4/SUBMISSION_PACKAGE_MANIFEST.DRAFT.json` |

원본 6개는 Git Blob ID가 계속 동일하도록 선택적으로 이식하고, Source 기반 README 또는 과거 `.copy` 소스코드로 3rd의 최신 코드를 덮지 않는다. Git Blob가 다른 문서가 있으면 원본 보존 + 변화 사유 검토.

## 실행 단계 (담당자가 차기 세션에 수행)
1. 3rd 최신 검증된 부모 커밋에서 **신규 별도 브랜치** 생성. 충돌 및 보호 Blob 확인 후 6개 문서만 가져오기.
2. Source 전용 `git clone https://github.com/061015ed-cys/Upstage-AI`는 원본 스냅샷에 그대로 남겨두고, 3rd README와 새 파생 Runbook에는 `git clone https://github.com/dohun3540-crypto/3rd_task_dohun` 및 최신 올바른 브랜치/설치 환경으로 안내.
3. `README.md`에는 Team4 `FINAL_HANDOFF.md` 링크만 최소 추가; `docs/SUBMISSION_CHECKLIST.md`에는 11/10 내부 동결, 11/11 13:00 공식 제출, 포털 실제 필수 규격 NOT_VERIFIED를 명시. 원본 README 체크리스트로 덮어쓰지 않음.
4. `SUBMISSION_PACKAGE_MANIFEST.DRAFT.json`의 `source_main_sha=575745...` 및 오래된 bytes/SHA는 3rd에 적용하지 않음. 실제 대상에 포함할 파일의 새 상대 경로/byte length/SHA256를 깨끗한 체크아웃에서 다시 계산해 **새 타깃 전용 Manifest** 파일을 생성. `status=DRAFT_NOT_SUBMISSION_READY`, `share_approved=false` 유지. 팀원1과4가 제출 자료/민감정보 범위를 승인하기 전 제출/ZIP 생성 금지.
5. `git diff`로 수정 파일이 문서 6개 + 승인된 최소 README/체크리스트 변경뿐인지 확인. Python 엔진, QA, Gold, PDF, Studio Config, CI 워크플로는 변경하지 않음.
6. 3rd에서 새 문서전용 Commit → Draft PR 작성. 3rd의 기존 PR #1·#2 및 GitHub Actions 상태를 훼손하지 않음. **Cherry-pick은 부모 히스토리 차이로 자동 성공 보장 불가:** 6개 문서를 바이트 그대로 path-selective copy하는 것이 기본.
7. 새 PR의 실제 HEAD SHA로 Markdown/link/JSON parse + Git Blob 6/6 재검증. README가 수정되면 깨끗한 Clone 설치 CLI 및 기본 코드 회귀·Ruff; 문서만 추가면 전체 테스트 반복 대신 기존 성공 CI와 자동 CI 결과를 범위 구분해 기록.
8. Release Gate는 필수 Native QA/Gold/B0E1 증거 확보 전 계속 **BLOCKED**. 등록 포털 권한·최종 대외 제출은 인간 승인 전 실행 금지.

## 다음 작업 담당자에게 전달할 재개 프롬프트
“3rd 최신 HEAD를 먼저 확인하고 `.copy`의 Team4 Draft PR에서 원본 6개 Git Blob과 Source manifest SHA256을 읽어라. docs/team4에 동일 Blob으로만 선택 복사하고 README/Submission Checklist는 최소 패치로 검토하라. 팀1/2/3 코드는 그대로 유지하고 정확한 SHA의 CI를 확인한 뒤 3rd Draft PR을 만든다. 실제 Studio Job/Gold/포털 증거 없으면 Release BLOCKED 유지. 기존 공용 통합 저장소는 사용자가 별도 승인하지 않는 한 수정하지 않는다.”
