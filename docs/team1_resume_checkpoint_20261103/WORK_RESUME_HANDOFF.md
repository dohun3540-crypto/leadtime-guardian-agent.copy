# LeadTime Guardian Team1 — 안전 중단·재개 인계

담당 구도훈. 중단 기록 2026-11-03T18:19:34+09:00. 사용자 이동 요청으로 신규 개발·분석·실측을 즉시 중단했다. **Release BLOCKED**, 코드 동결 유지. 이번 문서는 완료 보고서가 아니라 WIP 체크포인트다.

## 저장소·Git 상태

- 개인: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy
- 코드 기준 HEAD: `fc974f9589dfc1d56d407e2482c6294b6603e2a9` / 기준 PR23 Draft, unchanged.
- 새 체크포인트 브랜치: `checkpoint/team1-e2e-resume-20261103` (기준 HEAD에서 생성, 다른 브랜치를 덮어쓰지 않음).
- 로컬 작업 폴더: `/workspace/scratch/28d256eab1b7`. personal/358와 integration/336은 API Git Blob으로 복원한 소스트리이며 `.git`이 없다. 따라서 로컬 git branch/HEAD는 NOT_VERIFIED이고 `git status`, `git diff`, `git diff --cached` 대상이 아니다. 대신 원격 고정 tree의 모든 Blob SHA를 대조해 수정/삭제0을 확인했다.
- 신규 프로덕션·테스트 수정0, 미저장 편집 버퍼 없음. checkpoint_public/ 문서5개만 새 원격 커밋 대상. 실행 중인 테스트/명령 없음. 원래8개 overlay 인계문서+5개 코드/테스트 선택분, editable-install egg-info는 기존 로컬 상태이며 새 수정으로 세지 않는다. egg-info는 재생성 가능하며 통합 패치에서 제외했다.
- 이 파일은 커밋 전 내용이다. 실제 checkpoint Commit/Draft PR/최신 CI는 최종 전달 ZIP의 CHECKPOINT_STATUS.json·POST_PUSH_ATTESTATION.json와 새 PR 본문에서 확인한다. 저장 이전 기준 HEAD를 새 커밋으로 오인하지 않는다.

## Task A–F

| Task | 상태 | 실제 완료 | 다음 재개 작업 |
| --- | --- | --- | --- |
| A | BLOCKED | v4 C001/C013 Normalize/QA/Parse/Classify originals recovered previously; source rows and Job equality checked; C001 provider PDF3 SHA match | Obtain actual IndependentQA input bytes and provider step input/output trace, Merge raw and original upload receipts; compare input with Normalize bytes without using QA verdict as input |
| B | BLOCKED | NEW: B0 recorded NCik Job verified in UI; Config cfg_X2/v1 and Normalize/QA/Parse/Classify/Extract zip downloaded. NEW: candidate cfg_bX/v2 QA downloaded; structural config diff preserved | Authenticate alias registry and PDF-byte equality; retrieve candidate v2 Normalize failed sync; complete four bundles. No paid run |
| C | IN_PROGRESS | Prior recursive audit lists40 static null/type candidates and raw declarations, no reproduced live failure; candidate patch is unvalidated and NOT applied | Finish40-row classification with required/nullable/prompt/observed-native/reproduction/risk/owner fields. Account for actual addNullTypeToNumericTypes flag; do not equate declaration mismatch with runtime failure |
| D | COMPLETED | Prior C001 actual source Preflight returned BLOCKED with invalid_inputs=[] and no exception. C013 actual Native local Combined/V6 safely blocked; manifests preserved | Revalidate only after new authentic evidence; do not force C001-only preflight on C013 |
| E | NOT_STARTED | Prior C001/C013 local replay outputs available; no new runnable demo/manual created in interrupted third task | Create reproducible C00160500KRW and C013 conflict-block demo/manual using existing CLI. Label LOCAL_REPLAY, no formal accuracy without Gold |
| F | IN_PROGRESS | Prior full overlay812 and original778 nodeIDs preserved. Existing five selected paths conserved as patch for this checkpoint, not newly applied/tested | Validate selective patch on exact integration base in isolation, preserve strict_json/engine/adapter/QA guards; only maintainer may push integration. No repeat full tests merely to save checkpoint |

D의 COMPLETED는 확보 자료의 로컬 누락 진단 범위만 의미한다. 완전한 실제 E2E·Release 승인은 미완료다. 이번 세 번째 실측 요청에서 A~F 전체 acceptance를 새로 완료한 Task는 없다. 중단 전에 추가한 성과는 B0 원본 회수·비교 원본 회수이며, C/F/E 잔여 작업을 완료로 올리지 않았다.

## 이번에 새로 확보한 것과 미완료

기존 B0 기록의 NCik Job을 Studio에서 직접 확인하고 Normalize·QA·Classify·Parse·Extract ZIP·Config를 회수했다. cfg_X2/v1을 확인했고, 비교 후보 cfg_bX/v2 QA도 회수했다. 총 새 원본7개와 Config diff1개가 verification_v3/에 있다. 이름만으로 E1을 지정하지 않는다. B0 QA도 Normalize 미제공을 보고한다. 최종 v2 Normalize 다운로드는 브라우저 경로 반환 후 실제 공유 파일 동기화에 실패해 **미확보**로 남겼다. 다시 받을 필요가 있으면 다음 세션에서 UI 보관 결과를 조회한다.

기존 v4 C001/C013 Parse·Classify·Extract·Normalize·QA와 Config, C001 원본 PDF3개, 동일 Native 로컬 V6 결과·Sidecar는 보존했다. 실제 QA Input, raw Merge, provider Upload Receipt, 모든 Step Run ID 결합, Team2 본인 원본 실행 인계, 승인된 Human Gold는 확보하지 못했다. 같은 Job/파일명, config edge, exported gold/ 폴더를 입력 인증/Gold 승인으로 쓰지 않는다.

## 결함·미해결 문제

- 알려진 새 필수 Team1 코드 결함0. 기존 중첩 JSON RecursionError 수정은 PR23에 이미 포함되어 있으므로 새 결함으로 집계하지 않는다.
- Schema40은 정적 후보이며 실제 실패40건이 아니다. 정밀40행 분류는 미완료. 이전 제안 patch는 NOT_APPLIED/NOT_IMPORT_VALIDATED. Extract quote[]→Normalize object/null, 빈문자열→null은 의도된 변환이다.
- 보존 Config 비교에는 addNullTypeToNumericTypes:true 추가가 있으므로 선언 타입만 보고 실제 null 동작을 확정하지 않는다.
- 이전 병렬 회귀811/1 timeout 실패는 원본 로그를 보존했고 독립 테스트 PASS+직렬812 PASS. 코드/기대값/timeout을 바꾸지 않았다. 새 필수 엔진 결함으로 확정하지 않았다.

## 회귀·CI

이전 실제 검증: 개인750/QA501, 격리 통합812/QA544, 기존778 nodeID 전부 보존, PDF60/60 machine PASS, Ruff PASS. 중단 요청 이후 로컬 전체/QA/Ruff는 **NOT_RUN_AFTER_CHECKPOINT**. 코드 변화가 없어 저장을 지연하는 반복 검증은 하지 않았다.

기준 개인 CI: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41599142645 — stop 시 completed SUCCESS 재확인. head_sha=fc974f9589dfc1d56d407e2482c6294b6603e2a9; checkout synthetic merge와 candidate는 같은 Git Tree다. 통합 기존 CI: https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285 —778 기준;812 overlay의 원격 통합 CI가 아니다. 새 체크포인트 CI는 PR 생성 후 상태를 별도 기록하며 완료 전 SUCCESS라 쓰지 않는다.

## Gate·준비도

OVERALL_RELEASE_GATE=BLOCKED. 공식 B0/E1 네 묶음0/4. 코드 구현100%, 기존 감사96.15%, 비공식 준비도74.375% 유지, 코드/로컬 component9/16. 이번 원본 추가만으로 임의 점수 상승하지 않는다. 프로젝트 전체 준비율은 분모가 없어 산정하지 않는다. 미승인 Gold는 승인하지 않았다.

## 영구 보존·원본 위치

[체크포인트 패키지](https://chatgpt.com/library?file_id=libfile_a5a7ed79e6c0819198e51e4e5bf5c607&account_id=personal) 안 PRIVATE_EVIDENCE_SNAPSHOT.zip에 원본·로그·분석143파일과 자체 SHA manifest를 넣었다. 공개 GitHub에는 원본을 넣지 않는다. 바깥 ZIP에는 최종 인계3파일, 이 인덱스, source state, 보존용 five-path patch와 post-push attestation이 들어간다. 이전 두 ZIP 없이도 이 원본 스냅샷과 원격 소스로 현재 상태를 복원할 수 있다.

주요 경로(내부 ZIP):
- verification_v3/studio_originals/: 새 B0/candidate 원본7개
- verification_v3/evidence/config_comparison.diff 및 STOP_SOURCE_STATE.json
- verification_v2/studio_originals/: v4 C001/C013 및 Config/PDF 원본
- verification_v2/local_v6/C001, C013/: **TEAM1_GENERATED_LOCAL_REPLAY**, Team2 본인 원본 인계 아님
- verification_v2/evidence/: raw pytest XML/log, 실제CLI current_c001_preflight.json, nodeID, 실패 및 직렬 재검증
- verification_v2/SCHEMA_CANDIDATE_AUDIT.json 및 PROPOSED_NULLABILITY_PATCH_NOT_IMPORT_VALIDATED.json
- audit_evidence/, studio_evidence/: 이전 근거
- final_remote_tree.json / integration_source_manifest.json:358/336 source Blob inventory

## 다음 실행 순서·복원 명령

A → B → D → C → F → E. A/B 외부 원본이 없으면 C/F/E 독립 작업을 계속한다. 이 중단 세션에서는 신규 실행하지 않는다.

```bash
git clone https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy.git leadtime-team1
cd leadtime-team1
git fetch origin checkpoint/team1-e2e-resume-20261103
git switch --detach FETCH_HEAD
git rev-parse HEAD
git status --short
```

실제 SHA를 전달 ZIP/PR의 post-push attestation과 대조한다. clone 인증 불가 시 GitHub plugin의 정확한 commit tree/blob API 복원으로 대체하고 각 Blob SHA를 검증한다. 토큰을 출력하지 않는다. 통합 source는 `67b93291c1f32acaf43e45815d2d1119480b652a` 고정 read-only 별도 폴더에서 복원한다. private ZIP을 별도 폴더에 풀고 원본 manifest를 다음처럼 검증한다.

```python
import json, hashlib
from pathlib import Path
root=Path('evidence')  # PRIVATE_EVIDENCE_SNAPSHOT.zip을 푼 위치
m=json.loads((root/'ORIGINAL_SHA256_MANIFEST.json').read_text())
for e in m['entries']:
    p=root/e['path']
    assert p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'], e['path']
```

실제 검증이 필요한 새 변경/증거가 생긴 뒤만 필요한 명령을 실행한다. 개인 requirements-validation.txt가 없으므로 requirements-agents.txt와 qa/requirements.txt를 사용한다. C001 preflight는 기존 LOCAL_ONLY_C001_EVIDENCE_INPUT.json의 절대경로를 **복사본에서** 새 복원 위치로 바인딩하고 원본 바이트/SHA는 바꾸지 않는다.

```bash
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python scripts/team1_e2e_preflight.py --manifest /ABS/EVIDENCE/LOCAL_ONLY_C001_EVIDENCE_INPUT.rebound.json --json-report /ABS/NEW_OUTPUT/c001_preflight.json
# Expected until missing receipts/stages/input/Gold arrive: exit2, BLOCKED, release_authorized=false
# Only after source changes or a justified regression check:
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
python -m ruff check .
python scripts/qa_archive_check.py --root .
python scripts/qa_gate_check.py --root .
python -m qa.inventory --root . --out /ABS/NEW_OUTPUT/pdf-inventory
```

再開後완료조건: 실제 QA Input 동일성 및 출처 사슬 확인, B0/E1 alias/config/PDF동일성+4조합,40행 schema 근거분류, 기존 Preflight 누락안전차단,5경로 선택통합 검증, 재현가능 시연·평가 인계. 코드가 필요 없으면 수정하지 않는다. 필수 재현 결함만 Red→Green→전체회귀→별도브랜치CI. 기존 PR19/20/21/23/main 및 통합 전체 보호; 유료 Studio 실행/merge/force push/Gold승인 금지.
