# LeadTime Guardian — Native E2E r5 이후 남은 증거 작업 재개

저장소 https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy
Branch feat/team1-native-e2e-closure-20261103-r5, Base PR28 @9225c06b33328b275fcf8c8a6f57b85ccf26ab8e. 최종 후속 PR/SHA/CI는 전달패키지 POST_PUSH_ATTESTATION.json과 PR본문에서 확인한다.

먼저 docs/team1_native_e2e_closure_20261103/REPORT.md, NATIVE_EVIDENCE_INDEX.json, VALIDATION.json, RELEASE_GATE.precommit.json과 패키지 최종 attestation을 읽는다. 현재 로컬787/538, 격리통합845/577, 새17회귀,7표적mutation kill, 원본143SHA·Team2src8·PDF60/60·신규C013provider3/3 일치가 완료됐다. 기존 원본감사나데모를 재작성하지 않는다.

현재 실제 보존Job은 C001 job_DkzsPqVpfBkXLSDvScbdgC, C013 job_aq9eWmd23vb4G6DySyF5sF, Agent agt_oMuHCjkGkVUkyyxjVDJda4, cfg_mokhkXae6d5U7CfgpL7ffw v1이다. 이번에 이 정확한 Config의 로컬 intake와 C001/SYN-C001·C013/SYN-C013의 명시적 같은케이스 매핑을 지원했다. 원본report는 수정하지 않는다. 다른Config·버전·Case는 거절한다.

Native pair+실제report content를V6와CrossAgent에연결했다. C001계산60/60500 PASS_LOCAL, 원래QA NOT_VERIFIED→Cross BLOCKED. C013계산안전차단·금액null, 원래QA NEEDS_REVIEW→Cross정책FAIL. 이FAIL을계약예외나새테스트실패로오인하지말고PASS로바꾸지않는다. Source 원본은private_evidence/C001,C013, 새C013ProviderPDF ZIP과현재Config export가있다. V6 sidecar는Team1이원래Team2엔진을실행한LOCAL_REPLAY이며Team2가생산한새Live실측이아니다.

남은순서:
1. 두기존Job의actual IndependentQA Input, raw Merge, complete ProviderStepTrace와업로드원본SHA receipt를회수한다. 저장된Parse/Classify/Extract는재사용하고StepRun바인딩을보충한다. QA Input의형태·Normalize출력과일치·Job/Step/Config출처를검증해야NORMALIZED_OUTPUT_NOT_PROVIDED의전달실패와형식인식문제를구분할수있다. 현재원인미확정.
2. private_evidence각케이스의stage_manifest.PARTIAL/release_manifest.PARTIAL에실제증거만연결해기존preflight·combined를실행한다. QA ReportNative의Job/Step과원래report content SHA를유지한다. C013은이제C001XLSX22칸통계를오염시키지않고동일단계검증이가능하다.
3. B0/E1×C001/C013의정확한savedConfig/정의/공식aliasregistry와동일PDF영수증을확보한다. 기존NCik는reportedB0부분자료이고RpJv2는UNASSIGNED다. 이름·null flag만으로E1을지정하지않는다. E3v3사본은조회상실행결과가없었고실행하지않았다.
4. 현재NativeSHA에맞는Team2검토산출물과실제사람승인Gold를연결한다. 과거gPmReplay둘은이미회수했다. 다시요청하지않는다.
5. 새결함이재현될때만실패회귀→최소수정→전체회귀→새branchcommit/push→정확HEAD CI. 이미통과한테스트숫자를늘리기위한반복작업금지.

Native전체0/2·공식번들0/4·HumanGold0·ReleaseBLOCKED를유지한다. 새로운실제증거가있을때만Gate를갱신한다. 원본repo/PR24–28/이번후속PR/원격동결통합을보호한다. 유료실행·공유설정적용·외부제출·merge·forcepush·Gold대리승인금지. 권한/자료가없어도독립적코드·증거검증을계속하고결과를저장한다.
