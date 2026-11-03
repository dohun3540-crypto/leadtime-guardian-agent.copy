# Python 통합·안전성 V6 개발 보고서 및 팀 인계

작성일: 2026-10-30 KST. 요청서의 V6는 이번 작업 묶음의 이름이며 Studio 설정 v6을 생성했다는 뜻이 아니다.

## 결과와 상태

| 항목 | 상태 | 실제 확인한 결과와 한계 |
|---|---|---|
| 개발 시작 기준 | PASS | PR #11 최신 HEAD `f196c694917f2d9e5f4ec228c752bd3f2a4eb882` 확인. 당시 CI run `41037193907` 성공 |
| 격리 브랜치 | PASS | `codex/teammate-python-safety-v6`. main·PR #11 브랜치 직접 수정, reset, force push, 자동 병합 없음 |
| 기존 환경 회귀 | PASS | Python 3.11.9, 기존 pytest 80개 통과(17.76초), Ruff 통과 |
| 수정 후 로컬 회귀 | PASS | pytest 189개 통과(19.06초), Ruff 통과. 신규 109개, 기존 80개 유지 |
| C001 실제 v4 예측 재분석 | PASS | 기존 부족 0 / 변경 후 60 / 추가 60 EA / 60,500.00 KRW, `OK`·`COMPLETED` |
| C013 실제 #5 예측 검증 | BLOCKED | 저장소 두 원격 브랜치 모두에 실제 Native JSON 없음. 사용자도 받은 파일이 설정 JSON뿐이라고 확인. 실제 PO 경고 2개·전체 경고 6개 유지 여부는 확인 불가 |
| C013 합성 PO 충돌 | PASS | DRAFT fixture의 PO999를 수정하지 않고 차단. 기준 R1 납기 불변, 계산값 null, 구매 초안 없음 |
| C008 부분 입고 | PASS | 합성 정규화 계약: PO의 R1=40/R2=60, 통보는 R2만. R1 유지/R2만 변경, 주문 부족 0/40, 견적 40,500 KRW |
| C008 실제 추출 | NOT_RUN | 원본 Studio 예측 없음. 합산 수량을 R1/R2로 추측해서 배분하지 않음 |
| C017 Python 경계 | PASS | 이미 ISO로 정규화된 합성 입력은 0/60/60. `2026년 11월 8일`이 경계에 남아 있으면 차단 |
| C017 한국어 PDF → ISO 추출 | NOT_RUN | 날짜 정규화는 Studio 담당. Python에서 원문을 자동 보정하지 않으며 실제 추출 성공을 주장하지 않음 |
| SDK HTTP 모의 | PASS | 기존 13개, 실제 SDK 2.54.0/httpx 0.28.1와 loopback 서버. 실제 Upstage 추론 아님 |
| FakeClient 수송 계약 | PASS | 기존 13개 + Job ID/이력 정합성·순서 보존 5개 = 18개 |
| 실제 Agents API 호출 | NOT_RUN | 사전 검사에서 API 키 없음. 이번 작업의 라이브 요청 0건 |
| Studio 설정 v5 가져오기·신규 실행 | NOT_RUN | 사용자가 제공한 실제 설정 export를 보존했으나 UI 가져오기·실행은 하지 않음 |
| PDF 근거·Gold 사람 검수 | NOT_RUN | `evidence_verified_against_pdf=false`. 정확도 수치를 산출하지 않음 |

최초 기준 CI 성공은 신규 브랜치의 CI 성공을 의미하지 않는다. 신규 PR의 현재 커밋 체크를 별도로 확인한다. CI가 PR #11의 기능 브랜치를 대상으로도 실행되도록 필터를 추가했다.

## 실제 변경 파일과 이유

| 파일 | 변경 이유 |
|---|---|
| `.gitattributes` | Windows `core.autocrlf=true` 환경에서도 Studio 원본과 재분석 보관 파일의 줄바꿈·SHA-256 보존 |
| `src/leadtime_guardian/strict_json.py` | 중복 객체 키, NaN/Infinity, 부동소수점 범위 초과, 잘못된 UTF-8·단독 surrogate 차단. BOM이 있는 UTF-8도 지원 |
| `src/leadtime_guardian/studio_integration.py` | 모든 내부 JSON 문자열도 엄격하게 파싱. 충돌 envelope·미완료/알 수 없는 상태·잘못된 metadata·Job ID 불일치 차단. 신뢰 입력 사전 검증, 중복 PO 입고행·PO 문서가 없는 통보·빈 ID·견적 충돌 검사 |
| `src/leadtime_guardian/engine.py` | 공통 `blocked_result` 생성. 실패 경로에서 기준 입력을 다시 계산하지 않음. 직접 엔진 입력의 비 KRW 견적도 차단. 기존 배분·견적 알고리즘 유지 |
| `src/leadtime_guardian/studio_adapter.py` | 저수준 연결에서도 경고·중복 통보·주어진 원래 날짜/수량 충돌 차단. 입력은 deepcopy 후에만 수정 |
| `src/leadtime_guardian/provenance.py` | 문서 스키마를 바꾸지 않는 별도 provenance 계약 구현 |
| `scripts/analyze_studio_export.py` | 원본을 한 번 읽어 같은 바이트를 보존·해시·분석. export/기준 JSON 파싱 오류도 완전한 BLOCKED 응답과 메타데이터로 저장. 실제 Job ID 대조, sidecar 저장 |
| `src/leadtime_guardian/agents_api.py` | 폴링 중 Job ID 변경 차단. include=all 이력의 ID/완료 상태/오류를 확인하고 원본 snapshot 보존 |
| `tests/test_python_safety_v6.py` | 실제 C001 재생과 합성/실패 회귀 104개. 파일 이름·주석으로 실제 예측과 합성 자료 구분 |
| `tests/test_studio_integration.py` | 공식 API envelope fixture에 Job ID 명시. 강화된 입력 계약 반영 |
| `tests/test_agents_api.py` | FakeClient 회귀 5개 추가. 원본 PDF 순서, Job ID, 이력 충돌 검증 |
| `.github/workflows/ci.yml` | PR #11 기능 브랜치 대상 PR에도 CI 실행 |
| `configs/studio_native/config_v5.user-supplied.export.json`, `config_v5.receipt.json` | 사용자 제공 설정 v5의 원본 바이트·SHA-256·관측된 설정 ID 보존. 예측으로 취급하지 않음 |
| `data/results/python_safety_v6/C001_v4_replay/` | 실제 v4 예측을 새 Python 코드로 재분석한 결과·원본·해시·정규화·provenance |
| `docs/python_safety_v6/validation.json`, 관련 인계 문서 | 검사 결과, 계약·호환성·미완료 구분 |

## Fail-closed 사용 계약

외부 Studio 자료의 정식 경로는 아래 순서다.

1. 원본 bytes를 보존하고 `loads_strict`로 파싱한다. 일반 `json.loads`로 먼저 읽으면 이미 사라진 중복 키를 나중에 검출할 수 없다.
2. `documents_from_export(raw, expected_job_id=실제_JOB_ID)`를 호출한다.
3. `analyze_studio_documents(trusted_base_case, documents, schema)`를 호출한다.
4. 소비자는 `status == "OK"`, `execution_status == "COMPLETED"`, `needs_review is False`를 모두 확인한 후에만 계산 결과를 표시한다. 견적은 검토용 초안이며 확정 발주가 아니다.

실패 시 `NEEDS_REVIEW` / `BLOCKED` / `needs_review=true`, 모든 부족량·견적금액·미충족량은 null, 지연·고객 주문 영향·공급 추천 배열은 비어 있다. `external_action_taken=false`다. 오류를 회피하기 위한 납기 보정, 경고 삭제, Gold 대입은 없다.

`apply_studio_extractions`는 저수준 매핑 함수다. 전체 문서 스키마·PO·견적 검증을 대체하지 않는다. `analyze_portfolio`와 데모는 신뢰된 정규화 입력용 기존 인터페이스다. 외부 예측을 저수준 함수 두 개에 직접 넘기는 이전 인계 예시는 위의 검증 경로로 교체해야 한다.

## JSON 계약과 호환성

기존 `configs/schemas/document_extraction.schema.json`, EA·KRW·ISO 날짜, 엔진 출력 버전 `1.1.0`과 정상 계산 필드는 유지했다. 새 Evidence 필드를 문서 스키마에 넣지 않았다. 기존 의존성만 사용하며 추가 패키지는 없다.

입력 허용 범위를 다음과 같이 의도적으로 좁혔다.

- 문서 배열, `{documents:[...]}`, Native `{content:JSON문자열,metadata:{job_execution_id,step_run_id,...}}`, 단독 `{output_text:JSON문자열}`, 완료된 공식 API `output` 형식을 지원한다.
- 한 객체에 documents/content/output_text/output을 두 개 이상 넣으면 같은 값이어도 차단한다. SDK의 계산된 output_text 속성과 output을 수동 결합한 호출자는 원본 API JSON 또는 단독 output_text wrapper 하나만 넘긴다.
- API `output` 및 id/status가 붙은 API wrapper는 `status=completed`와 nonempty `id`가 필수다. 단순 정규화 wrapper에는 실행 상태가 없으므로 실행 완료를 입증하지 못한다.
- Native metadata는 Job ID·step_run_id를 요구한다. 없는 Config ID·완료 상태를 만들어 넣지 않는다. Native 다운로드에 상태가 없으면 원본 실행 기록과 별도로 대조해야 한다.
- CLI `--run-id`는 관찰된 실제 Job ID와 같아야 한다. 정규화 배열만 있는 경우 CLI label은 자체 증거가 아니다. `--config-version`도 기존과 같이 감사 label이며 서버 설정 고정이나 실제 Config ID 검증을 의미하지 않는다.
- C008처럼 한 PO의 복수 입고는 receipt_id와 입고별 수량이 명시되어야 한다. 기존 날짜가 다르면 같은 전역 날짜를 공유하는 한 문서에 억지로 합치지 않는다. 합산 행을 임의 분할하는 계약은 지원하지 않는다.
- 견적 문서당 한 품목/한 quote 객체다. 여러 대안은 서로 다른 quote_id의 별도 문서로 표현하며 공급량을 공유하고 운송비는 사용한 견적당 한 번 계산한다. 비용은 greedy 초안이며 최소 비용 최적해가 아니다. 통화가 생략된 기존 엔진 견적은 KRW로 해석하는 호환성을 유지한다.

외부에서 비정상 입력을 허용하던 호출자는 위 계약으로 이전한다. 정상 C001 Native v4 원본은 변경 없이 통과한다.

## 경고 정책과 근거 구분

모든 비어 있지 않은 `warnings`는 계속 차단한다. C013 실제 원본을 확보하지 못했으므로 경고 분류를 임의로 완화하지 않았다.

| 유형 | 정책 |
|---|---|
| 견적의 original_delivery, 발주서의 supplier_id 등 계약상 선택 필드 null | 경고가 없고 필수 업무값이 맞으면 허용 |
| 통보의 PO/SKU/변경 날짜, 입고 수량·연결 등 필수값 누락/모호성 | 차단 |
| PO·SKU·Receipt·원래 날짜·수량·견적 가격/통화 불일치 | 차단 |
| Evidence 없음 | PDF 검증 성공으로 표시하지 않음. 현재 계약의 빈 배열 자체를 새 차단 조건으로 만들지는 않음 |
| 선택 필드의 근거 부족 warning | 현재는 차단 유지. Studio 담당과 필수/선택/불일치 경고 코드를 합의한 후 별도 PR로 정책 변경 |

스키마 유효성은 자료형 검사, 업무 검증은 신뢰 입력과의 일치 검사, PDF 검증은 원문 대조다. 서로 대체할 수 없다. 성공한 계산도 PDF 검증 성공을 의미하지 않는다.

sidecar 계약 `studio-provenance/1`은 `export_sha256`, `studio_metadata_supplied`, `agents_job_id_supplied`, `business_validation_status`, 문서별 `evidence_supplied/evidence_status`, `evidence_verified_against_pdf=false`로 구성된다. Native metadata의 실제 파일 ID/이름/페이지 범위와 Evidence의 실제 필드·원문·confidence·좌표가 있다면 그대로 보존한다. 문서와 파일의 대응, 병합 전후 페이지, 필드 경로·최종 값의 일치 여부는 자동으로 추정하거나 검증됐다고 표시하지 않는다. 원본 정규화 문서와 sidecar를 해시로 함께 보관한다. C001 Evidence는 전부 빈 배열이며 `ABSENT`다. 향후 필드별 원문 검증은 별도 계약 버전으로 추가한다.

## 실제 실행과 회귀 근거

환경 구성: `python -m venv .venv`, `.venv\Scripts\python -m pip install -r requirements-dev.txt -r requirements-agents.txt`. `requirements-integration.txt`는 기존 PDF 생성용 ReportLab만 추가하므로 이번에는 설치·재생성하지 않았다.

실행한 검사:

```powershell
.\.venv\Scripts\python -m pytest -q
.\.venv\Scripts\python -m ruff check .
git diff --check
git diff --exit-code f196c694917f2d9e5f4ec228c752bd3f2a4eb882 -- data/cases data/results/studio_runs configs/studio_native/config_v4.export.json
```

신규 109개는 엄격한 파싱/내부 JSON 14개, 응답 형태·상태·Job ID 24개, 업무 입력 변형·차단·매핑 38개, C002-C020 합성 계약 19개, 실제 C001 재분석 1개, provenance/CLI/엔진 견적 8개, API 모의 5개로 구성된다. 세부 식별자는 pytest 수집 결과와 `tests/test_python_safety_v6.py`, `tests/test_agents_api.py`를 기준으로 한다. 실제 Studio 추출 정확도는 측정하지 않았다.

C001 실제 재분석 명령(출력은 새 디렉터리를 사용):

```powershell
.\.venv\Scripts\python scripts/analyze_studio_export.py --export data/results/studio_runs/C001_20261030_v4/instruct_original.json --base data/cases/SYN-C001/trusted_base_case.json --output data/results/python_safety_v6/C001_v4_replay --run-id job_gPmEYKzuJdBA6BmKhVnujs --config-version cfg_SZi6qfyZ6XFoNszpXQK5xQ --prompt-version c001-studio-v4
```

원본 SHA-256 `88387f8d6aee1421c9f628304c6b91811396b32da297d41b40e3d53c3d98dfea`. 이번 실행은 저장된 실제 Studio 예측의 Python 재생이며 새 Studio 실행이 아니다. 기준 재고 40 + 지연 전 입고 100은 주문 100을 충족한다. 변경 입고일 11/08은 고객 납기 11/05보다 늦어 재고 40만 배정되고 60이 부족하다. 대체 견적 60 × 1,000 + 운임 500 = 60,500이다.

원본 해시 대조 중 Windows Git의 `core.autocrlf=true`가 checkout 시 LF를 CRLF로 바꾼 사실을 발견했다. 원본 자료 19개를 Git blob의 바이트로 복원하고 `.gitattributes`의 `-text`로 변환을 막았다. 원본 경로의 Git diff는 없으며 C001 테스트가 기록된 SHA-256도 검사한다. 최종 재분석은 복원된 실제 원본 바이트를 사용했다.

C002-C020의 19개는 DRAFT fixtures를 명시적으로 사용하는 합성 단위 테스트다. 13개 정규화 정상 계산과 6개 위험 입력 차단을 확인한다. wrapper 자체를 실제 export로 넣으면 거부되는 테스트도 유지한다. 원본 PDF 57개 압축 파일, C001 PDF 및 과거 실제 실행 자료는 수정하지 않았다.

## 보안·API·미완료 및 Studio 담당자 인계

- 사전 검사: PDF 3개 순서·해시 확인, `sdk_available=true`, `api_key_available=false`, 네트워크 요청 0. 키를 요청·저장·출력하지 않았다. API 오류 문자열을 그대로 저장하지 않는 기존 정책과 SDK 재시도 0을 유지한다.
- 제출 시간초과 후 자동 중복 제출 없음. 인증/429/서버 오류·미완료 job·폴링 시간초과·파일 덮어쓰기 방지는 기존 모의/SDK HTTP 회귀에서 통과한다. 새 Job ID/이력 충돌도 차단한다.
- 구매·결제·메일 전송 endpoint는 추가하지 않았다. 저장소 비밀 파일 제외 규칙을 유지하며 제공한 설정 JSON에는 자격증명 값이 없다.
- 제공 설정 v5: Config ID `cfg_o645qH9hDUgVnkrjw7Vets`, SHA-256 `890e3a9c5fa6dfa05d4df04a7c9b1ab82b1b984baf4a382c406b2ffce7d747e3`. 설정 파일은 C013 실행 원본이 아니다. 설정을 기존 Studio 에이전트에 덮어쓰지 않았다.
- Studio 담당자에게 필요한 자료: C013 `job_GvFUbjuLiPjNdBySNdH4kV`의 변경되지 않은 Native JSON, 실제 Config ID·완료 기록, 해당 PDF 3개/순서/해시, 단계별 다운로드와 파일·페이지 metadata. 받은 뒤 기존 CLI를 새 출력 디렉터리로 실행한다. PO999를 PO1로 바꾸거나 경고를 삭제하지 않는다.
- C001 #5 개선 후보의 실제 실행 자료는 미확보다. C008/C017도 같은 패키지로 전달받아 실제 추출과 정규화를 검증한다. PDF 근거·Gold 사람 검수는 별도 담당 확인이 필요하다.
- 다음 개발자는 정규화 문서 스키마를 유지하고 sidecar만 별도 취급한다. 임의 경고 완화 전에 정상 C001과 실제 충돌 C013을 모두 회귀해야 한다.
- 이 PR은 PR #11의 `feat/specs-data-engine-20261029`를 대상으로 한다. 프로젝트 담당자 검토 전 최종 병합하지 않는다.
