# Team1 개발 재개 결과

담당 구도훈. 기록 2026-11-03T19:00:40.650314+09:00. **전체 Release BLOCKED**, 독립 로컬 잔여 작업 C/E/F는 PASS_LOCAL까지 진행했다. 이전 완료 구현을 다시 만들지 않았다.

## 복원

checkpoint branch `checkpoint/team1-e2e-resume-20261103`, HEAD `8b671d4a67cd649b08c4e6603a457f607342c3d7`, PR24 Draft/Open/Unmerged를 확인했다. 당시 queued CI41610223172는 지금 completed SUCCESS다. WORK_RESUME_HANDOFF.md, RESUME_WORK_PROMPT.md, CHECKPOINT_STATUS.json, SOURCE_STATE.json, EVIDENCE_INDEX.json 및 ZIP의 POST_PUSH_ATTESTATION.json을 대조했다. 증거143/143 SHA256, source363/363 Git Blob SHA가 일치했다.

직접 HTTPS clone은 credential 부재로 사용할 수 없었다. GitHub connector의 고정 tree/blob/commit metadata로 복원하고, 로컬 Git tree와 commit object SHA까지 `8b671d4a67cd649b08c4e6603a457f607342c3d7`와 일치시켰다. 복원 직후 git status는 clean이었다. 새 브랜치 `feat/team1-resume-schema-demo-20261103`를 개인 .copy 저장소에만 만들었다.

## Task 상태

| Task | 판정 | 신규 완료·기존 보존 | 남은 조건 |
| --- | --- | --- | --- |
| A | BLOCKED | Recovered previously missing candidate v2 Normalize original; same Job/source rows and 3-document contract verified locally | Actual QA input, raw Merge/complete step trace and upload receipts; same-input Team2 original handoff; approved Gold |
| B | BLOCKED | Preserved B0/candidate identities without assigning an unauthenticated E1 alias | 0/4 complete authenticated B0-C001/E1-C001/B0-C013/E1-C013 bundles |
| C | PASS_LOCAL | Exact 40 candidates classified: 36 POTENTIAL_CONFLICT, 4 NOT_VERIFIED; live defects 0 confirmed | Provider null runtime/import validation; no unverified schema patch applied |
| D | PASS_LOCAL | Existing missing-input diagnostic completion preserved; preflight BLOCKED, invalid_inputs=[], no exception | Full Native E2E acceptance remains BLOCKED |
| E | PASS_LOCAL | Runnable C001/C013 Native replay CLI, C008/C017 synthetic demos, evaluation and manual | Live demo and official accuracy NOT_MEASURED without approved Gold |
| F | PASS_LOCAL | Five-path patch applied in isolation to exact integration base; 812/544 tests, prior 778 and 812 nodeIDs preserved, Ruff/archive/local gate/PDF60 PASS_LOCAL | Maintainer-only remote integration and new integration CI; no integration push performed |

## 신규 개발과 문제 해결

- scripts/team1_schema_review.py: 정확한40개 재귀 후보, nested required, nullable flag, 실제 관찰·branch 미실행, local leaf 검증과 provider runtime의 구분을 재현 가능하게 만들었다.
- scripts/team1_replay_demo.py: 원본을 바꾸지 않는 C001/C013 replay, 다른 Job·source row 혼합 거부, 기존 Combined CLI의 BLOCKED 유지, 별도 QA 구조 검사, C008/C017 DRAFT 추가 시연을 제공한다.
- tests/test_qa_team1_resume_tools.py: 숫자 nullable flag 오판, 빈 quote row 미실행 오판, Job 혼합, same-Job 다른 source 혼합을 막는4개 경계 회귀다.
- 사용자에게 인계된 기존 작업의 미완료였던 schema40 분류·재현 매뉴얼·선택 통합 검증을 완성했다. 새 운영 엔진 결함은 확인되지 않아 Team2/3 운영 코드를 수정하지 않았다.

Native 새 회수 파일은 UNASSIGNED_v2_C001_NormalizeDocuments.native.json, SHA256 `6223e5ce21e39da70bd62c4c0a2a3d9641b30fa2bb9de04f5e276d8551156eca`. 과거11/1 Job의 보관 출력이며 신규 실행이 아니다. 같은 Job QA는 Normalize 미제공을 보고하므로 graph edge가 존재해도 실제 입력 전달 성공을 선언하지 않았다.

## 저장과 보호

[Draft PR25](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/25)는 PR24를 base로 한 후속 작업이며 PR24나 PR23을 대체·종료하지 않는다. source code commit `6929ea1dc29e1ad6c1d1c604dd1180968ef7ec1a` 원격 반영 및 CI SUCCESS를 확인했다. 최종 문서 SHA/CI는 PR25의 사후 attestation과 전달 ZIP에 기록한다. original/main/PR19·20·21·23·24/integration PR2를 변경하지 않았다. 결제·Studio 실행·Gold승인·merge·force-push는0이다.
