# Team 1 재현 시연 및 평가표

증거 수준은 LOCAL_REPLAY다. 기존 Studio 실행의 저장된 출력과 현재 Python 코드를 사용한다. 신규 Studio 실행, 구매, 제출, Gold 승인은 수행하지 않는다. 실제 QA가 본 입력 원본은 없으므로 QA 결과를 입력으로 대신 쓰지 않는다.

## 준비와 실행

1. 개인 저장소의 PR #25 고정 커밋 `6929ea1dc29e1ad6c1d1c604dd1180968ef7ec1a` 이후 소스를 사용한다. 이 보완 PR은 해당 도구를 수정하지 않는다.
2. 체크포인트 ZIP 안 `PRIVATE_EVIDENCE_SNAPSHOT.zip`을 별도 `evidence/` 폴더에 푼다. 파일 구조를 유지한다. `ORIGINAL_SHA256_MANIFEST.json`의 143개 SHA를 먼저 대조한다. 아래 명령은 저장소 루트에서 실행한다.

```bash
python3 -m pip install -r requirements-agents.txt -r qa/requirements.txt
python3 - <<'PY'
import hashlib, json
from pathlib import Path
root = Path('../evidence')
manifest = json.loads((root / 'ORIGINAL_SHA256_MANIFEST.json').read_text())
for item in manifest['entries']:
    path = root / item['path']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == item['sha256'], item['path']
print('143 originals/logs verified')
PY
python3 scripts/team1_replay_demo.py \
  --evidence-root ../evidence --out ../demo_result --include-drafts
```

입력별 Native/QA/base/schema/PDF SHA는 `PINNED_REPLAY_INPUT_INDEX.json`에도 있다. C013 PDF는 보존된 원본 샘플과 저장소 archive manifest가 일치한다. Provider 업로드 바이트 인증은 아니다. 도구의 C013 provider PDF 목록이 비어 있는 것은 그 한계를 정직하게 표시한다.

## 실행해서 확인한 결과

| 시연 | 입력 수준 | 핵심 확인 | 실제 결과 | 평가 범위 |
| --- | --- | --- | --- | --- |
| C001 정상 | 보관 Native Normalize + 별도 QA 출력 구조 검사 | 발주 100, 재고 40, 부족 60, 견적 60 | COMPLETED, 비용 60,500 KRW, Python safety PASS_LOCAL | 원본 출력의 로컬 계산 재현 |
| C013 오류 | 보관 Native, PO1/PO999와 경고 보존 | 다른 발주 연결 차단, 비용 계산·구매 제안 금지 | BLOCKED, 비용 null, 제안 [], safety SAFELY_BLOCKED_LOCAL | 보존된 오류 입력의 안전 차단 |
| C008 분할 입고 | SYNTHETIC_DRAFT_LOCAL_ONLY | 입고별 배분과 주문별 부족량 | 부족 40, 비용 40,500 KRW | 예제 로컬 계산; 최적해 보장 아님 |
| C017 날짜 이후 계산 | SYNTHETIC_DRAFT_LOCAL_ONLY, 이미 ISO 날짜 | 날짜가 정규화된 입력의 이후 계산 | 부족 60, 비용 60,500 KRW | 한국어 PDF→ISO 변환 성능 미측정 |

`DEMO_EVALUATION.json`에서 전체 PASS_LOCAL, release_gate=BLOCKED를 확인한다. C001/C013 각각 `analysis.json`, `combined_e2e.json`, `qa_adapter.json`, `summary.json`을 보존한다. QA adapter PASS는 JSON 계약 검사이며 문서 QA PASS나 실제 입력 연결 인증이 아니다.

## 발표 순서

1. C001 원본 PDF 세 종류와 저장된 Normalize 결과를 보여 준다. 이번 시연에서 Parse/Extract를 새로 실행하지 않았음을 먼저 알린다.
2. 운영 Native에서 확인한 발주·변경일·견적 필드와 trusted base의 재고/고객주문을 구분한다. 부족 60개는 원문 필드가 아니라 계산 결과다.
3. 원래 ETA/변경 ETA에 대한 counterfactual 부족량 0→60 및 대체 조달비 60,500원을 설명한다.
4. C013의 PO999를 PO1로 고치지 않고, 원래 충돌값과 경고를 그대로 보존한 채 안전 차단을 보여 준다.
5. C008을 선택적으로 시연한다. 순차 배분은 greedy 정책이며 전역 최적화 보장을 주장하지 않는다.
6. 증거와 실행 출처가 없으면 release를 승인하지 않는 마지막 Gate를 보여 준다. 승인 Gold가 없어 정확도·오탐률·개선율은 제시하지 않는다.

## 오류 대응

- SHA 불일치: 입력을 수정해 맞추지 말고, 보존 ZIP에서 원본을 다시 복원한다. 다른 Job 결과를 섞지 않는다.
- Job/source row 불일치: 현재 도구는 Python 실행 전에 거부한다. 같은 실행의 QA 출력만 확보한다.
- CLI FAIL 또는 예외: 해당 JSON/로그를 보존하고 재현 입력을 고정한다. 계산값·기대값·안전 조건을 약화하지 않는다.
- C013 BLOCKED: 정상적인 오류 차단 시연이다. 비용 null과 제안 []가 유지되어야 한다.
- 실제 QA 입력 부재: Native E2E 성공으로 발표하지 않는다. 원본 QA 입력·provider step trace가 도착하면 기존 Stage/Combined 검증기로 연결한다.

기술 차별점은 납기 변경 전후의 반사실적 비교, 분할 입고 단위 배분, 문서 ID/원본 SHA·Job/Step 연결 및 근거 부족 차단이다. 실제 근거 인증이 끝난 부분과 로컬 계약만 확인한 부분을 나누어 설명한다.
