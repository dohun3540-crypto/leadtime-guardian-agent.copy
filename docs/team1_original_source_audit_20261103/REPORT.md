# 원본 데이터 통합·독립 자기회귀 감사 — 2026-11-03

**원본 자료를 재사용해 검증했고, 추가 결함2개를 수정했다. 전체 Native E2E/Release는 BLOCKED다.** 시작점은 보호 PR27 `b73dd0159d55a0c771115b83c19ebf1dc9ac330b`, 작업은 별도 `feat/team1-original-data-self-audit-20261103-r4`다.

## 원본 조사와 선택 통합

| 원본 브랜치 | 최신 확인 HEAD | 전체 동일/누락/상이 | 결정 |
| --- | --- | --- | --- |
| Team2 codex/teammate-python-safety-v6 | e9b9992b593a42d427ff1bbadeb9a9866ca593bd | 151 /45 /8 | 데이터·설정 범위는 기존 설명과 같은97동일/12누락. 12경로 private로 회수; raw 재게시 없음 |
| Team3 feat/qa-ground-truth-evaluation | a925103077173b37d1cefcd6a9576ae644dc2040 | 173 /1 /9 | 데이터88개 전부 동일. 누락 QA_HANDOFF만 exact import. source4개는 더 오래된 V6 안전 검사라 덮어쓰지 않음 |

원본 main `e36250074eed33db7951c4d58d8678e07b333a58`, specs `f196c694917f2d9e5f4ec228c752bd3f2a4eb882`, 원본5branch/고유4HEAD와 PR11/12/13, `.copy`29branch를 조사했다. `.copy`의 다른 현재 branch에는 기준보다 추가/다른 data/config blob이 없었다. PR12/13 리뷰·댓글도 각각0개다. 이전 비교 수치와 차이는 전체파일/관련자료 분모 차이다.

서로 다른63개 경로를 원본 SHA로 고정해 로컬 감사했고 모두 Git Blob SHA가 일치한다. 동일한 기존 경로는 재복사하지 않았다. 누락12경로 중6개는 다른 기존 경로의 같은 blob이며 중복 출처 별칭으로 표시했다. 신규 실측12건으로 세지 않는다. 12파일은 private 입력으로 보존하고 CLI의 명시적 export 경로로 사용했다. `.copy`에는 비민감한 `.gitattributes`, Team2 PYTHON_SAFETY_V6_HANDOFF, Team3 QA_HANDOFF 세 파일만 원본 그대로 반영했다. 자동 줄바꿈 변환을 켠 Git hash 검사도12/12 일치한다.

Team3와 다른 runtime4모듈·스크립트·테스트·CI는 diff했다. 현재 파일은 원본 Team2의8개 src 파일과 이미 동일하며 강화된 Job/strict JSON/차단 검사를 포함한다. Team3의 이전 소스로 덮어쓰면 해당 보호를 잃으므로 유지했다. 원본 코드·PDF·Gold·공유 설정은 변경하지 않았다. 파일별 branch/commit/path/blob/SHA256/판정/반영 이유는 SOURCE_INTEGRATION_MANIFEST.json에 있다.

## 추가 확보한 증거의 의미

Team2가 작성한 C001_v4_replay 및 C001_v4_replay_20261031 두 묶음을 찾았다. 둘 다 과거 Job `job_gPmEYKzuJdBA6BmKhVnujs`, 원본SHA `88387f8d6aee1421c9f628304c6b91811396b32da297d41b40e3d53c3d98dfea`에 연결된다. 현 엔진으로 새로 로컬 재생한 analysis와 provenance가 Team2 원본과 정확히 같았다. 따라서 이 과거 자료를 다시 요청하지 않는다. 두 디렉터리는 하나의 과거 Native를 재생한 것이며 신규 Native2건이 아니다. 11월3일 C001/C013 원본SHA와는 다르므로 현재 Target Sidecar로 혼합하지 않는다.

v5 receipt는 설정 Export SHA와 일치하지만 실행/upload receipt가 아니다. config_version 필드가 cfg_ ID 문자열인 옛 run metadata도 원형 그대로 보존하고 provider의 정수 version으로 변환하지 않는다. Team3의20개 Gold는 DRAFT이며 QA_HANDOFF와 빈 검수 양식, PR 리뷰/댓글에서 사람 승인을 확인하지 못했다. 공식 Gold0, 정확도 미측정이다.

## 독립 품질 감사와 수정

1. output/content 중첩 wrapper 안 Native의 다른 Job/Step/Config가 기존 Stage 검사를 우회할 수 있었다. CLI 최소 반례를 먼저1 FAIL로 확인하고, document reader가 허용한 동일한 bounded wrapper 경로의 정체성을 모두 검사하도록 수정했다. 충돌은 Python 전 FAIL/NOT_RUN이다.
2. Manifest의 File ID는 검사했지만 Receipt 안 nested list/object는 set(qa_ids)에서 TypeError를 냈다. API 최소 반례1 FAIL을 먼저 보존하고 Receipt ID에도 같은 타입·prefix·공백 검사를 적용했다.

원래3개 수정도 재검증했다. 실제 원본 Extract ZIP을 원형 그대로 읽는 테스트는 로컬 shape binding이라고 명시하며 provider Step ID를 만들어 인증하지 않는다. 별도 정상 QA Job 허용을 유지했다. Seed20261103으로 순서24회·정체성36경로·File ID21위치·비즈니스9경계와 결정성/불변성을 검사했다. 추가 회귀8개를 포함한 관련52개가 통과했다.

Mutation은 격리 복제본에서 ID검사 제거, config type 완화, live evidence 검사 우회, FAIL→PASS, Python 실행 차단 제거5종을 수행했다. **PR27 기존 테스트가5/5 검출**, 무변형 동일 snapshot 대조군47개 PASS다. 전역 mutation coverage100%라는 뜻은 아니다. 별도 두 반례는 이전 테스트의 빈틈이었고 이번에 보완했다.

## 기능과 근거를 나눈 E2E 결과

C001~C020 원본 DRAFT를 재생해 정상14·안전차단6을 확인했다. 이는 공식 정답 정확도가 아닌 합성 로컬 회귀다. 원본60PDF도 재생성 없이 기계 검사60/60 PASS다. C001의 독립 날짜/Decimal 계산은 부족60·비용60,500원으로 기존 검산과 일치하고, C013 PO1/PO999는 원형 보존 후 BLOCKED다.

PDF/Parse/Classify/Extract/Normalize 과거 원본과 Team2 재생 연결은 확인했지만 raw Merge, 실제 IndependentQA Input, provider trace/upload receipt가 없다. QA 결과를 입력으로 바꾸지 않았다. B0/E1 공식4묶음0/4다. Functional Correctness는 scoped PASS_REPLAY/PASS_LOCAL, Evidence Correctness는 현재 Target 미인증으로 구분한다.

| Task | 이전 | 현재 | 근거 |
| --- | --- | --- | --- |
| A | BLOCKED | BLOCKED | 현재 대상 QA 실제 Input·raw Merge·receipt 없음 |
| B | BLOCKED | BLOCKED | 공식 B0/E1 0/4 |
| C | PASS_LOCAL | PASS_LOCAL | schema·원본 타입 검토 유지 |
| D | PASS_LOCAL | PASS_LOCAL | 추가 경계2결함 수정, mutation5/5, adversarial52 |
| E | PASS_LOCAL | PASS_REPLAY | Team2 과거 원본2묶음 재현, C00160/60500, C013차단 |
| F | PASS_LOCAL | PASS_LOCAL | 개인770/521, 격리828/560, 기존ID보존 |

전체pytest **770 PASS**, QA **521 PASS**, 격리 통합 **828/560 PASS**, E2E8파일 **127 PASS**, 실패·스킵0. 신규8개를 기존762/820에 더한 수치이며 QA/E2E subset을 합산하지 않는다. Ruff·Archive/Replay·SourceIntegrity·Cross-Agent local·LocalGate 통과, 기존762/820/최초778ID 보존이다. 통합에만 있던 테스트는 덮어쓰지 않았다.

완료율은 합의 가능한 분모로 나눈다. 로컬 체크리스트10항목 중 커밋 전9/10(신규CI 대기), 현재대상 Native 완전인증0/2(0%), 공식 B0/E1 0/4(0%), Overall Release BLOCKED다. 최종CI가 끝나면 post-push attestation이 로컬10/10을 확정한다. 프로젝트 전체 완료율은 합의한 분모가 없어 임의 산정하지 않는다.

## 다음 행동과 저장 경계

기존 PR25/26/27, main, 원본 저장소와 원격 통합 동결은 보호한다. 신규유료/무료Studio실행·외부제출·구매·Gold승인·Merge·ForcePush는0이다. 최종SHA/신규CI는 PR본문과 POST_PUSH_ATTESTATION.json이 커밋 전 문서의 후속 권위 기록이다.

외부 요청은 아직 보내지 않았다. 모든 접근 가능한 원본/사본 branch·원본 PR·보존 패키지를 조사한 뒤 남긴 정확한 파일명/Job/필드는 REMAINING_EXTERNAL_EVIDENCE_REQUESTS.json에 있다. 다음 우선순위는 현재 C001/C013 QA Input·provider trace/receipt, 공식 네 묶음, 현재 Native에 맞는 Team2 Sidecar와 승인 Human Gold다. 이미 찾은 과거 Team2 Replay를 다시 요구하지 않는다.
