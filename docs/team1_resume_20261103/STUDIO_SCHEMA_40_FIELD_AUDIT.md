# Studio Schema 40-field audit

정확한 체크포인트 40개 경로를 대조했다. 기존 top-level 8개와 nested quote[] 32개를 중복 집계하지 않았다. **정밀 분류 완료 PASS_LOCAL / Studio runtime Gate BLOCKED.**

36 string: POTENTIAL_CONFLICT. 4 integer(capacity): NOT_VERIFIED. 네 Extract entry의 addNullTypeToNumericTypes=true를 확인했으므로 numeric null 지원 여부는 선언만 보고 단정하지 않는다. 로컬 JSON Schema leaf는 null을 거부하지만 provider의 변환 후 Schema를 재현한 것은 아니다.

보관 Extract 두 ZIP에서 관찰한 실제 scalar의 leaf-type 위반은 0이다. 26개 후보 경로는 해당 branch 또는 quote row가 실행되지 않았다. 빈 quote table은 quote row의 null 지원을 시험하지 않는다. ZIP의 gold/ 이름은 사람 승인 증거가 아니다. 실제 Native null-type 오류 확정 0, 실측으로 필요한 설정 수정 확정 0이다. 전체 관찰값·원본 SHA·필수성·위험·담당자는 비공개 results/schema40.json에 보존했다.

| Field path | Type | 직접 컨테이너 필수 | Numeric-null flag | 관찰 branch/값 존재 | 분류 |
| --- | --- | --- | --- | --- | --- |
| Extract_purchase_order.po_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_purchase_order.supplier_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].quote_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].supplier_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].product_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].capacity | integer | False | True | False | NOT_VERIFIED |
| Extract_purchase_order.quote[].arrival_date | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].unit_price | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].shipping_cost | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_purchase_order.quote[].currency | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.po_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_delivery_notice.supplier_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].quote_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].supplier_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].product_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].capacity | integer | False | True | False | NOT_VERIFIED |
| Extract_delivery_notice.quote[].arrival_date | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].unit_price | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].shipping_cost | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_delivery_notice.quote[].currency | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_quotation.po_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.supplier_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].quote_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].supplier_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].product_id | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].capacity | integer | False | True | True | NOT_VERIFIED |
| Extract_quotation.quote[].arrival_date | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].unit_price | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].shipping_cost | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_quotation.quote[].currency | string | False | True | True | POTENTIAL_CONFLICT |
| Extract_other.po_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.supplier_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].quote_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].supplier_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].product_id | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].capacity | integer | False | True | False | NOT_VERIFIED |
| Extract_other.quote[].arrival_date | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].unit_price | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].shipping_cost | string | False | True | False | POTENTIAL_CONFLICT |
| Extract_other.quote[].currency | string | False | True | False | POTENTIAL_CONFLICT |

quote[]의 자식 required는 해당 row가 존재할 때의 필수성이며 빈 부모 배열에 row를 생성하라는 뜻이 아니다. 40개 모두 현재 선언은 null 불허이고 설명에는 명시적 Null if/when 지시가 있다. 전체 행에서 실제 failure 재현은 NOT_REPRODUCED, provider effective nullability는 NOT_VERIFIED다.

## 핵심 계약 확인

| 필드 | Normalize/V6 또는 QA 경계 | 관찰·검증 범위 |
| --- | --- | --- |
| po_id | string/null 선언; PO·notice·quote 업무 연결은 nonempty 일치 필수 | C013 불일치 보존, local V6 safely BLOCKED |
| receipt_id | string/null; notice는 trusted receipt에 유일 연결 | quotation receipt null은 의도된 변환 |
| product_id | 문자열; trusted SKU와 일치 | 식별자 대소문자/문자 보존, 기존 회귀 PASS_LOCAL |
| quantity | integer/null 선언; 업무 계산은 bool 제외 유효 정수 | C001 PO/notice100과 offered capacity60은 다른 역할 |
| unit | string/null 선언; 업무 적용은 EA | 미지원·누락 단위 기존 V6 차단 회귀 |
| original_delivery | ISO date string/null; notice original과 trusted original 연결 | 정상 납기 변경과 모순 구분 |
| revised_delivery | ISO date string/null; notice 적용에는 필수 | PO·quote null 정상; C017 fixture는 이미 ISO |
| quote_id | quote 내부 nonempty unique string | Extract quote[] -> single object/null 의도적 변환 |
| supplier_id | document optional; quote 내부 nonempty | PO·notice 선택 부재만으로 오류 아님 |
| capacity | quote 내부 bool 제외 유효 정수 | numeric-null flag runtime NOT_VERIFIED |
| unit_price | finite nonnegative decimal string/int | C001 1000.00; strict numeric guards 보존 |
| shipping_cost | finite nonnegative; quote당 운송비 | C001 500 한 번, 총60500 local replay |
| arrival_date | quote 내부 strict ISO date | original/revised와 다른 역할 |
| currency | KRW 업무 지원 | 다른 통화 차단은 기존 V6 회귀 |
| warnings | array[string]; nonempty이면 업무 계산 차단 | C013 warning이 먼저 차단; PDF 정확성 인증 아님 |
| evidence | array[object]; 실제 원문 대조 별도 필요 | retained Normalize empty arrays; grounding BLOCKED |
| source_page | evidence item integer>=1; local/global mapping 별도 | empty evidence라 live page mapping NOT_MEASURED |

Case ID는 trusted base/명시적 expected Case와 QA에서, Document ID는 documents/QA 집합에서 확인한다. 같은 Job ID와 File ID 목록은 local 연결 증거이며 업로드 바이트·실제 QA input을 인증하지 않는다. 기존 상세 계약 Matrix는 ../team1_release_audit_20261104_r2/DATA_CONTRACT_CONSISTENCY_MATRIX.md를 보존했다.

## 최소 변경 요청

확정 실측 결함이 없으므로 운영 설정 변경 요청은 승인 대기 수정안이 아니라 **재현 증거 요청**이다. 기존 PROPOSED_NULLABILITY_PATCH_NOT_IMPORT_VALIDATED.json을 일괄 import하지 않는다. string 필드의 명시적 부재, integer capacity 부재, quote empty table을 구별한 disposable probe가 필요하다. provider가 지원하는 nullable 문법과 numeric flag를 먼저 확인하고, 실제 실패가 재현된 필드만 수정한다. 담당 구도훈, Adapter 의미 검토 윤현준. 부작용은 필수 업무 사실 누락을 정상 처리하거나 quote[]를 손실 변환하는 것이다. 수정 후에는 원본 보존, import 성공, null·0·false·빈문자 구별, 업무 누락 차단, 정상 C001 및 C013 차단을 모두 확인한다. 이번 세션의 유료 실행·config import·운영 설정 수정은 0이다.
