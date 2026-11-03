# 데이터 계약 통일성 Matrix

기준: 현재 config export(2026-11-03 14:07 KST), C013 원본 Normalize/QA, PR21 및 통합PR2의 schema/Adapter/V6/QA, C001 AI candidate. Extract의 선언과 관찰값을 구분한다. `|`는 표 안에서 `/`로 표시했다. 원문/Native/Gold/XLSX를 수정하지 않았다.

**전체 Schema 완전 통일 PASS가 아니다.** 선언상 null 모순과 미제공 출처가 남는다. 단계마다 업무 필수성과 외부 metadata가 달라 동일한 이름/타입을 전부 강제하지 않는다.

| 필드 | Source | Studio Extract 선언 | Normalize 관찰/계약 | Python Adapter | V6 입력 | Independent QA 기대 | Gold Candidate | null 정책 | 필수성 | 불일치/판정 | 해결책임 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| case_id | PDF/manifest | 별도 context | documents에는 없음 | trusted base | string | C001 context / report SYN-C013 명시 | string | 불가 | manifest/base 필수 | 접두사 canonicalization을 도구별로 명시; raw 수정 금지 | 팀원1/2/3 |
| document_id | PDF | string | string | 보존 | nonempty / enum | string / 허용4종 | string | 불가 | 필수 | 새 기능 충돌 없음 | 팀원1/2 |
| document_type | PDF | string | string | 보존 | nonempty / enum | string / 허용4종 | string | 불가 | 필수 | 새 기능 충돌 없음 | 팀원1/2 |
| po_id | PDF | string; null 지시 | string / null | receipt PO에 결합 | PO/notice/quote 필수 string | 문서간 PO 대조 | string / null | 형식상 허용, 업무상 필요 | 업무 필수 | 정적 null 선언 후보; C013 PO999 의도적 | 구도훈/윤현준 |
| receipt_id | PDF item | string | string / null | receipt_id로 대상 선택 | 입고 식별 string | receipt 중복/대상검사 | string / null | quote 허용 | 입고 연결필수 | 견적 receipt null은 정상; 빈문자→null 변환 | 팀원2/3 |
| product_id | PDF item/quote | string | string | 보존 | 기존 SKU에 결합 | SKU 일관성 | string | 불가 | 필수 | 빈 문자열 schema 통과만으로 업무통과 아님 | 팀원2 |
| quantity | PDF item | integer | integer / null | 원본 보존 | bool 제외 nonnegative int | nonnegative int | integer | schema허용, 업무불가 | 업무필수 | 발주/변경량과 quote capacity 구분 | 팀원2/3 |
| unit | PDF item | string | string / null | 보존 | EA 필수 | 단위검증 | string | schema허용, 업무불가 | 업무필수 | EA 외 단위는 자동 계산 차단 | 팀원2 |
| original_delivery | PDF ISO/한글 | string | ISO string / null | original_eta / eta에 반영 | strict YYYY-MM-DD | 실제 달력 날짜 | ISO string / null | 문서종별 허용 | PO original,notice revised필수 | C017 DRAFT ISO만 확인; Studio Korean→ISO 미실측 | 구도훈/윤현준 |
| revised_delivery | PDF ISO/한글 | string | ISO string / null | original_eta / eta에 반영 | strict YYYY-MM-DD | 실제 달력 날짜 | ISO string / null | 문서종별 허용 | PO original,notice revised필수 | C017 DRAFT ISO만 확인; Studio Korean→ISO 미실측 | 구도훈/윤현준 |
| quote_id | PDF quote[] | string | string | quote[]→single object; 값 보존 | nonempty unique string | 중복/수치/통화 검산 | string | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| supplier_id | PDF doc/quote[] | string | string / null | quote[]→single object; 값 보존 | quote nonempty string | 중복/수치/통화 검산 | string | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| capacity | PDF quote[] | integer | integer | quote[]→single object; 값 보존 | bool 제외 nonnegative int | 중복/수치/통화 검산 | integer | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| unit_price | PDF quote[] | string | string | quote[]→single object; 값 보존 | finite nonnegative decimal string/int | 중복/수치/통화 검산 | string | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| shipping_cost | PDF quote[] | string | string | quote[]→single object; 값 보존 | finite nonnegative decimal string/int | 중복/수치/통화 검산 | string | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| arrival_date | PDF quote | string | ISO string | quote object에 보존 | strict date | 고객기한과 비교 | ISO string | quote내 불가 | quote필수 | 원래/변경 납기와 다른 역할 | 팀원2/3 |
| currency | PDF quote[] | string | string | quote[]→single object; 값 보존 | KRW | 중복/수치/통화 검산 | string | 비견적 N/A; supplier docnull 허용 | quote 내부필수 | quote[] 내부32개 null 선언 후보 포함; 복수 quote rows는 임의 한개 선택 금지 | 구도훈/윤현준/김민주 |
| warnings | Normalize | 미정의 | array[string] | 보존 | nonempty면 차단 | 경고와 false-positive 구분 | 기대규칙 별도 | 불가 | 필수 | optional null 부재만으로 false warning 금지 | 구도훈 |
| evidence | PDF 위치 | array[object] | array[object] | 자동보충 안함 | JSON검증≠PDF grounding | field_checks evidence 별도 | CSV 40행 | 빈배열 허용 | 원문 검증에는 필수 | C013 Native evidence 모두빈배열. QA 문장만으로 upload 검증 불가 | 구도훈/김민주 |
| source_page | PDF 1-based | evidence[].integer | evidence[].integer>=1 | 보존 | 계산에 미사용 | 페이지/field 연결 | source_page integer | 미제공 가능 | evidence있으면 위치필요 | 로컬PDF page와 merged global page 구분 | 김민주/구도훈 |
| file_id | provider metadata/receipt/local bytes | 추출field 아님 | metadata.source_files string | 추출 사실과 분리 | sidecar metadata | Upload Receipt exact join | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | 동일파일명은 동일바이트 증거 아님 | 구도훈/윤현준;PDF SHA 김민주 |
| job_execution_id | provider metadata/receipt/local bytes | 추출field 아님 | metadata string | 추출 사실과 분리 | expected Job string | 운영/QA distinct 허용 | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | QA 본문 job_id=null; QA Input 운영연결 없음 | 구도훈/윤현준;PDF SHA 김민주 |
| config_id | provider metadata/receipt/local bytes | 추출field 아님 | 해당 Native 미제공 | 추출 사실과 분리 | 실행메타 optional | 공급되면 expected 일치 | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | export draft cfg_mokhkXae6d5U7CfgpL7ffw를 각 Job에 추정 결합 금지 | 구도훈/윤현준;PDF SHA 김민주 |
| config_version | provider metadata/receipt/local bytes | 추출field 아님 | 해당 Native 미제공 | 추출 사실과 분리 | 실행메타 optional | bool제외 positive int | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | XLSX Ver1만으로 Config ID/승인 증명 불가 | 구도훈/윤현준;PDF SHA 김민주 |
| step_run_id | provider metadata/receipt/local bytes | 추출field 아님 | metadata nonempty string | 추출 사실과 분리 | sidecar metadata | stage Step 중복 검사 | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | 운영/QA 다른 Step 정상 | 구도훈/윤현준;PDF SHA 김민주 |
| source_sha256 | provider metadata/receipt/local bytes | 추출field 아님 | Native 자체 필드 아님 | 추출 사실과 분리 | sidecar export_sha256 | 원본 byte hash exact join | source manifest/approval link | 누락은 미검증 | 인증E2E필수 | 파일SHA≠Git Blob SHA; receipt 없는 cloud link는 BLOCKED | 구도훈/윤현준;PDF SHA 김민주 |

## 컨테이너와 의미 변환

- Extract quote는 array<object>, Normalize quote는 object/null. 관찰한 export는 quotation 1행·다른문서 empty list이며 C013 Normalize는 object/null로 변환됐다. 이 차이 자체는 계약 오류가 아니다. 여러 행 견적의 일반적 정상 처리까지 입증하지 않는다.
- Extract의 supplier/date/receipt blank string과 Normalize null은 해당 PDF에 값이 없을 때 의도된 변환. 수량0·false·null은 서로 바꾸지 않는다.
- Normalize 경고는 빈배열도 유효하다. C013은 PO999 불일치를 보존했고 V6가 차단했다. C001 100/60 차이는 공급 가능량과 발주량의 역할 차이다.
- 기존 정적 도구는 top-level null 모순8개만 찾았다. 중첩 own-description `Null if/Null when` 검사로 quote[]32개를 추가 식별해 총40개(중복 가산 아님). 정확한 path는 배포 패키지 recursive_null_directives.json. 실행 실패40건/정확도 저하40건이라는 뜻이 아니다.
- case_id는 release manifest에서 C001로 제한된다. C013은 report SYN-C013 및 기존 CLI expected C013를 도구별 계약에 맞게 명시한다. 원본 값을 임의 수정하지 않는다.
- QA report의 `field_checks[].field_name/extracted_value/verification_status`와 Python Adapter의 내부 검증 표현은 다르다. 기존 Studio QA adapter가 구조를 허용하며, observed adapter PASS와 업무 NEEDS_REVIEW를 구분한다.
- 재고/고객주문은 PDF에서 추정하지 않고 trusted_base_case에서 공급한다. supplier_risk=UNKNOWN은 정책 metadata이며 공급업체 원문 사실이 아니다.

현재상태: **SCHEMA_CONSISTENCY_GATE=PENDING**(로컬 Python 호환성 PASS_LOCAL, 현재 Studio 선언·실측 provenance까지 완전일치 미확인).
