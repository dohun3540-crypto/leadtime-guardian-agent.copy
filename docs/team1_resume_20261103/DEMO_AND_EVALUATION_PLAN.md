# 재현 시연과 평가 매뉴얼

결과 수준은 LOCAL_REPLAY와 SYNTHETIC_DRAFT_LOCAL_ONLY다. Native 원본을 읽지만 신규 Studio 실행은 0이며 전체 Native E2E는 BLOCKED다. 원본은 수정하지 않는다. approved Gold가 없으므로 공식 정확도는 계산하지 않는다.

## 준비

개인 PR25 브랜치에서 requirements-agents.txt와 qa/requirements.txt를 설치한다. 기존 Resume Checkpoint ZIP의 PRIVATE_EVIDENCE_SNAPSHOT.zip을 별도 폴더에 풀고 ORIGINAL_SHA256_MANIFEST.json의 143개 경로 SHA256을 확인한다. 아래 evidence_root는 내부 ZIP을 푼 경로다. 개인/통합 소스 중 어떤 경로로 실행하는지 혼동하지 않는다.

```bash
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
python scripts/team1_replay_demo.py --evidence-root /ABS/evidence_root --out /ABS/demo_results --include-drafts
```

정상 종료0, DEMO_EVALUATION.json.status=PASS_LOCAL, release_gate=BLOCKED를 함께 확인한다. 기존 Combined E2E CLI의 exit2는 누락 증거로 인한 예상 안전 차단이다. Wrapper의 PASS_LOCAL은 기대한 계산/차단 시연을 재현했다는 의미다. QA Native는 별도 기존 adapter로 구조 검사하며 Combined CLI에는 인증된 QA input/receipt 묶음을 공급하지 않았다. 실제 QA 입력을 검증한 연결 시연으로 표현하지 않는다.

| 시나리오 | 입력·목적 | 예상/실제 확인 | 증거 수준 | 실패 시 대응·차별점 |
| --- | --- | --- | --- | --- |
| C001 정상 | 보관 v4 Normalize+QA, trusted 재고·고객주문 | 재고40, 발주100, shortage60, 구매60, 60500.00 KRW; baseline shortage0 → changed60 | LOCAL_REPLAY; QA 원문 NOT_VERIFIED; source SHA summary.json | 예상과 다르면 원본·base·schema SHA 확인. Counterfactual 납기 두 번 계산, quote당 운송비1회 |
| C013 차단 | 보관 v4 PO/notice 불일치 및 warning | QA NEEDS_REVIEW, V6 BLOCKED, 비용 null, supplier_options=[] | LOCAL_REPLAY; cloud C013 PDF bytes 미확보 | warning이 먼저 차단한다. 원본 warning을 지워 성공을 만들지 않는다. PO/SKU/receipt 결정론 검증은 기존 V6 회귀로 별도 확인 |
| C008 부분입고 | repository extraction_gold.DRAFT.json의 documents | 주문1 shortage0, 주문2 shortage40, 40500.00 KRW | SYNTHETIC_DRAFT_LOCAL_ONLY | 재고 중복 배분 방지·부분 입고. Greedy는 최적해 보장이 아님 |
| C017 날짜 | 이미 ISO로 정규화된 DRAFT documents | shortage60, 60500.00 KRW | SYNTHETIC_DRAFT_LOCAL_ONLY | 한국어 PDF→ISO 변환은 NOT_MEASURED; 변환 성공이라 발표하지 않음 |

입력 파일명·원본 SHA, historical Job ID, 실제 로컬 결과는 C001/summary.json, C013/summary.json, DEMO_EVALUATION.json 및 시연 출력 폴더에 기록된다. C008/C017의 DRAFT는 사람 승인 Gold가 아니다. 모든 결과에서 release_authorized=false를 유지한다. Native QA input·stage trace·receipts를 받을 때까지 Evidence-Grounded Gate는 BLOCKED를 정직하게 보여준다.

## 평가 기록

각 시연의 통과 조건은 C001 비용/부족량 일치, C013 잘못된 연결 계산 차단, C008 두 주문의 재고 중복 사용 방지, C017 ISO fixture 호환이다. 이번 네 시연은 모두 PASS_LOCAL이다. 공식 추출 정확도, B0/E1 개선율, 실제 Studio runtime grounding은 NOT_MEASURED다. 재현 실패 시 입력/버전/Job/SHA를 고정하고 오류를 보존한다. 원문·Gold·warning이나 기대값을 고쳐 PASS를 만들지 않는다.
