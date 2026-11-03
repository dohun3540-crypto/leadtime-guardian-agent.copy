# LeadTime Guardian — Team 1 Native E2E 후속 개발·검증 (2026-11-03)

이 문서는 PR28 이후 새 변경의 커밋 전 검증 경계를 기록한다. 최종 SHA·PR·CI는 새 PR 본문과 비공개 전달 패키지 POST_PUSH_ATTESTATION.json이 권위 자료다. 이전 문서의 시점별 숫자를 현재 성과로 합산하지 않는다.

## A. EXECUTION_SUMMARY

- PR28 HEAD `9225c06b33328b275fcf8c8a6f57b85ccf26ab8e`와 Git Tree `5cbfea319563568840225858a1f8518c189a744d`, Actions41625172252 SUCCESS를 원격 확인하고 실제 로그의770 full/521 QA를 확인했다. 로컬 복제 시작점도 동일·CLEAN이었다.
- 새 branch `feat/team1-native-e2e-closure-20261103-r5`만 생성했다. PR24→25(두 커밋), PR26(25의 코드 부모에서 분기한 문서 보강), PR27→28 상속 관계를 확인했다. PR26은 PR25 최종 문서 커밋 전체를 상속한 것으로 오인하지 않는다.
- 원본 Team2 `e9b9992b593a42d427ff1bbadeb9a9866ca593bd`, Team3 `a925103077173b37d1cefcd6a9576ae644dc2040`는 이전 감사와 동일하다. 기존 원본 조사·63blob 감사는 재사용하고, 현재 Team2 src8파일의 Git blob 일치와 원본143 SHA를 다시 검증했다.
- 신규: C013 Studio 그룹의 원본 PDF3개를 실제 다운로드하여 저장소60PDF 아카이브의 대응 파일과 바이트3/3 일치 확인. 현재 v4 Config v1 export도 회수해 workflowConfig가 보존본과 같음을 확인했다.
- 신규: 실제 보존 Native의 C001/C013 Normalize+QA 출력 쌍을 현재 Team2 V6와 Team1 Cross-Agent에 연결했다. 기존 데모가 QA를 별도 구조 검사로만 다뤘던 범위에서 실제 원본 report content를 Cross-Agent로 넣는 범위로 확대했다. 과거 Job의 로컬 재생이며 신규 Studio 실행·전체 Live E2E가 아니다.
- 기존 완료: PDF60개, 원본업로드 감사, 과거 Team2 replay2폴더는 재생성·재요청하지 않았다. Human Gold0, 공식B0/E1 0/4, 전체 Native0/2와 Release BLOCKED를 유지한다.

## B. DEVELOPMENT_DELTA

1. B0/E1 필드 비교가 바깥 metadata만 검사해 안쪽 output/content의 다른 Job을 놓치고, metadata가 있으면 루트 Job도 놓쳤다. 실제7FAIL 중 관련 재현 후 문서 reader와 동일한8단계 경로의 루트·metadata·additional_values를 모두 비교하도록 수정했다. Case/Job/Step/Config 충돌을 차단하고 숫자1과 boolean true를 구별한다. Manifest의 단계 config_version 비교도 같은 타입 규칙을 적용했다.
2. C013은 Stage 및 Release manifest의 C001 전용 조건 때문에 유효한 자료도 FAIL이었다. C001/C013 두 고정 케이스를 지원하고 SHA·Job·Config·문서3개·QA입력 일치 검사를 그대로 적용한다. C013에 C001 XLSX22칸 통계와 참조SHA를 잘못 붙이지 않는다. C001의 기존 통계는 보존했다.
3. Combined 경로의3문서 사전차단이 C001에만 적용돼 불완전 C013도 Python에 도달했다. 실패 spy로 재현하고 C013에도 적용했다. 운영·QA 양쪽 그룹 검사를 유지한다.
4. 현재 실제 QA agent `agt_oMuHCjkGkVUkyyxjVDJda4`와 cfg `cfg_mokhkXae6d5U7CfgpL7ffw` v1을 고정된 로컬 수신 대상으로 등록했다. 다른 Config/버전/bool 버전은 거절한다. 이 등록은 클라우드 인증·실행 승인·Live PASS가 아니다. 기존 두 Agent와 원래 제약은 유지했다.
5. 실제 report의 `SYN-C001`/`SYN-C013`과 제어용 `C001`/`C013`을 명시된 같은 케이스 쌍으로 연결했다. 원본 report 바이트는 수정하지 않고 원래Case ID와 canonical ID를 파생 결과에 모두 남긴다. C001↔C013 교차 혼합은 FAIL이다.
6. Stage의 QA Report는 임의 `{}`도 완료 자료로 셌고, 실제 content+metadata QA 출력은 verdict를 읽지 못했다. 두 실패를 재현하고 제한된 wrapper 해석과 허용 verdict를 요구했다. SYN-case 별칭 관찰을 기록하며 QA Native의 원본SHA·Job·Step을 보존한다.

수정 범위는 Team1 QA6개 소스/CLI와 새 회귀파일1개다. Team2 engine/Studio Adapter/strict_json, Team3 PDF/Gold, 공유 Studio 설정은 변경하지 않았다. 로컬 테스트를 Live PASS로 승격하는 코드도 추가하지 않았다.

## C. TEST_RESULTS

| 범위 | 실제 결과 | 범위와 한계 |
|---|---|---|
| Team1 전체 pytest |787 PASS|Python3.11 환경, 이전770 ID 전부 보존|
| Independent QA |538 PASS|전체의 부분집합|
| 격리 통합 전체 |845 PASS|기존 통합후보828 ID 전부 보존; 원격 통합 저장소 변경 없음|
| 격리 통합 QA |577 PASS|845의 부분집합|
| 새 회귀 |17 PASS|15개 초기 경계·현재ID검사 +2개 QA report경계|
| Ruff |PASS|개인·격리통합 전체|
| Archive/Replay |PASS_REPLAY|불변 C001 과거 원본 검사|
| Integration Gate |PASS_LOCAL / Overall BLOCKED|릴리스·병합 권한 없음|
| 원본 PDF |60/60 PASS|기계무결성; Human Gold 평가 아님|
| C013 provider PDF |3/3 byte match|실제 다운로드와 저장소 원본비교; 업로드 receipt 대체 아님|
| 표적 mutation |7/7 KILLED|새 guard의 선택한7연산자만 검증; 전역 coverage 아님|
| 최종 원격CI |커밋 전 PENDING|완료 후 PR 본문/POST_PUSH_ATTESTATION 기준|

실패 로그→최소수정→통과 로그와 XML을 비공개 패키지에 보존한다. 모든 기존770/828 테스트ID를 보존했으며 합성 회귀와 실제 Native 재생을 분리한다. 로컬 실행은 Python 3.12.14, GitHub CI는 Python3.11이다. 실행 환경 차이를 구분한다.

## D. STUDIO_E2E_RESULTS

| 항목 | C001 | C013 |
|---|---|---|
| 기존 실제 Job |job_DkzsPqVpfBkXLSDvScbdgC|job_aq9eWmd23vb4G6DySyF5sF|
| Agent/Config |agt_oMuH… / cfg_mokhk… v1|동일|
| Normalize StepRun |4e66c576-79b8-55b4-82bc-4c73bd20976a|549446cb-fc93-5425-8399-88d678c9da25|
| QA StepRun |210e5946-631f-5d5c-9eeb-ff946e2fa7b0|376b80b3-95f0-553f-96b4-8d4b70815e78|
| 동일 Job·Source3개 |PASS_LOCAL + 현재 UI 조회|PASS_LOCAL + 현재 UI 조회|
| Python V6 재생 |COMPLETED / PASS_LOCAL|BLOCKED / SAFELY_BLOCKED_LOCAL|
| 계산 |부족60, 비용60,500 KRW|비용null, 구매옵션 없음|
| 실제 report 원래 판정 |NOT_VERIFIED|NEEDS_REVIEW / PO충돌|
| Cross-Agent 지역정책 |BLOCKED|FAIL: NEEDS_REVIEW 차단 정책에 따른 판정|
| QA구조·원본출처 매핑 |PASS_LOCAL|PASS_LOCAL|
| 실제 QA입력·완전Trace |없음|없음|
| 전체 Live E2E |BLOCKED|BLOCKED|

C013 Cross-Agent의 FAIL은 스키마 예외나 새 회귀 실패가 아니라 기존 NEEDS_REVIEW 거절 정책의 결과다. Release를 통과시키려고 이를 PASS로 바꾸지 않았다. 현재 Agent/Config 상수는 로컬 검증 범위이며 runtime Config 증명이 아니다.

Normalize 출력이 실제로 존재하고 정적 Normalize→QA edge도 있다. QA report에는 NORMALIZED_OUTPUT_NOT_PROVIDED가 남아 있다. 현재 UI Job 상세는 완료·파일ID·단계명과 시간만 보여 주며 실제 QA request body를 제공하지 않았다. 따라서 전달 누락과 입력 포맷 인식 실패 중 어느 원인인지 확정하지 않았다. E3 v3 사본은 실행 준비 상태·결과 없음으로 조회됐으며 실행하거나 E1으로 지정하지 않았다.

C013 그룹에서 회수한 PDF는 모두 저장소 원본과 동일하다. 원본Hash와FileID 매핑은 NATIVE_EVIDENCE_INDEX/비공개 원본 패키지에 있다. UI 관찰에서 파생한 매핑은 원래 provider upload receipt가 아니다.

## E. B0_E1_COMPARISON

| 공식 조합 | 보유 자료 | 판정 |
|---|---|---|
|B0-C001|기존 NCik Job의 일부 원본과 Config v1|BLOCKED: 전체 단계/실제QA입력/receipt/공식alias 인증 없음|
|B0-C013|완전한 공식 번들 없음|BLOCKED|
|E1-C001|RpJ v2 과거자료는 UNASSIGNED|BLOCKED: E1으로 임의 지정하지 않음|
|E1-C013|완전한 공식 번들 없음|BLOCKED|

보존 Config 간 확인된 차이는 numeric-null flag와 workflow 이름 등이다. 이것만으로 B0/E1의 실험 의미나 승인된 alias를 새로 정의하지 않았다. 실제 설정 정의·네 조합 registry·동일PDF receipt를 확인하기 전 새 실행을 시작하지 않는다. 공식 정확도·개선율·오승인율·지연시간 비교는 NOT_MEASURED다. 신규 유료실행0, 승인대행0이다.

C001/C013별 실제 원본이 채워진 PARTIAL stage/release manifest와 누락 목록을 전달 패키지에 만들었다. Team1이 이번에 실행한 V6 analysis/provenance/run_metadata도 별도로 보존했다. 이 로컬 Sidecar를 Team2가 작성한 신규 실측 산출물로 위장하지 않고 공식 Team2 evidence source에는 넣지 않았다.

## F. RELEASE_GATE

각 Gate의 판정·증거는 RELEASE_GATE.precommit.json에 있다. CODE는 현재 PASS_LOCAL(최종CI확인후 PASS 가능), DATA는 PASS(무결성 범위), STUDIO_NATIVE/CROSS_AGENT/PROVENANCE/B0_E1/GOLD/RELEASE는 BLOCKED다. C013의 로컬 Cross-Agent 정책 FAIL도 별도 보존한다. 모든 Mandatory Gate가 충족되기 전 release_authorized=false다.

## G. GITHUB_CHECKPOINT

Repository: dohun3540-crypto/leadtime-guardian-agent.copy. 새 Branch: feat/team1-native-e2e-closure-20261103-r5. Base는 보호 PR28의9225c06…다. 이 문서는 커밋 전 작성됐으며 최종 Commit/PR/CI/작업트리 상태는 완료 후 PR본문과 POST_PUSH_ATTESTATION.json에 기록한다. 기존 PR24–28, 원본5branch, 원격 동결통합 PR2를 변경하지 않는다. Force push·merge·외부메시지·외부제출·Gold승인·설정import는 수행하지 않았다.

## H. REMAINING_BLOCKERS

| 담당 | 원인 | 해결 방법과 필요한 자료 |
|---|---|---|
|Team1|actual QA input와 raw Merge 및 완전Trace 미회수|두 기존Job별 IndependentQA_Input.original.json, MergeDocuments.original.json과 provider step request/response trace 확보. 보존 Parse/Classify/Extract는 먼저 재사용하고 StepRun 바인딩만 보충|
|Team1|현재 same-Native V6 재생은 Team1 실행|보존된 실제원본SHA와 생성된 replay를 활용해 Team2 검토·연결; 로컬재생/원래 산출물 분류 유지|
|Team2|현재Job에 연결된 Team2 원본분석·Sidecar 없음|현재 두 Normalize SHA와 연결된 analysis/provenance/run_metadata 또는 검토된 계약 산출물 제공. 과거 gPm replay2폴더 재요청 불필요|
|Team3|승인된 Human Gold0|원본PDFSHA·reviewer·reviewed_at·decision·gold version/SHA가 있는 실제 승인 기록과 검수파일. AI_CANDIDATE 자동승격 금지|
|Studio플랫폼|UI의 단계시간과 모델주장만으로 입력전달 인증 불가|원래QA request body, 단계 output/input lineage, upload SHA receipt와 runtimeConfig 바인딩 제공|
|사용자/실험담당|공식 B0/E1 alias·정의 불명, 신규실행 과금 미확정|먼저 정확한 savedConfig와 네 조합 registry를 확정; 실행이 필요하면 비용/공유설정 영향 확인 후 해당 실행만 승인|

독립적인 Team1 구현·기존원본검증·증거저장은 완료했다. 아직 제공되지 않은 input/Gold/승인 기록은 추정으로 채우지 않는다. 필요한 자료 목록은 작성했지만 외부 팀원에게 보내지 않았다.

## I. NEXT_WORK_PROMPT

NEXT_WORK_PROMPT.md를 사용한다. 완료된 원본감사·회귀·데모를 처음부터 반복하지 말고 실제QA입력과Trace, 공식별칭, HumanGold 등 남은 외부 증거부터 확인한다.
