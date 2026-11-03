# Schema 40개 후보 정밀 분류

정확한 기존 목록 40개를 모두 검토했다. CONFIRMED_DEFECT는 0개이며, 이 결과는 Studio 런타임 인증이 아니다.
각 행의 필수 여부·선언 null 허용·숫자 옵션·프롬프트·Native 관찰·재현 범위·위험·담당자는 SCHEMA_40_REVIEW.json에 보존했다.

분류: {'POTENTIAL_CONFLICT': 13, 'INTENDED_TRANSFORMATION': 16, 'NOT_VERIFIED': 11}. 모든 부모에 required 목록이 없으며, 이를 provider 암묵적 동작으로 확대하지 않는다.
v4/v2의 addNullTypeToNumericTypes=true는 숫자 필드의 런타임 null 허용 가능성을 남긴다. B0에는 옵션이 내보내지지 않아 false라고 단정하지 않는다.

| # | 필드 | 타입 | Required(선언) | 관찰 | 분류 |
| --- | --- | --- | --- | --- | --- |
| 1 | Extract_purchase_order.po_id | string | false | C013-PO:["PO1"]; PO-DOC:["PO1"] | POTENTIAL_CONFLICT |
| 2 | Extract_purchase_order.supplier_id | string | false | C013-PO:[""]; PO-DOC:[""] | POTENTIAL_CONFLICT |
| 3 | Extract_purchase_order.quote[].quote_id | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 4 | Extract_purchase_order.quote[].supplier_id | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 5 | Extract_purchase_order.quote[].product_id | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 6 | Extract_purchase_order.quote[].capacity | integer | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 7 | Extract_purchase_order.quote[].arrival_date | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 8 | Extract_purchase_order.quote[].unit_price | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 9 | Extract_purchase_order.quote[].shipping_cost | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 10 | Extract_purchase_order.quote[].currency | string | false | C013-PO:[]; PO-DOC:[] | INTENDED_TRANSFORMATION |
| 11 | Extract_delivery_notice.po_id | string | false | C013-NOTICE:["PO999"]; NOTICE-DOC:["PO1"] | POTENTIAL_CONFLICT |
| 12 | Extract_delivery_notice.supplier_id | string | false | C013-NOTICE:[""]; NOTICE-DOC:[""] | POTENTIAL_CONFLICT |
| 13 | Extract_delivery_notice.quote[].quote_id | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 14 | Extract_delivery_notice.quote[].supplier_id | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 15 | Extract_delivery_notice.quote[].product_id | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 16 | Extract_delivery_notice.quote[].capacity | integer | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 17 | Extract_delivery_notice.quote[].arrival_date | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 18 | Extract_delivery_notice.quote[].unit_price | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 19 | Extract_delivery_notice.quote[].shipping_cost | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 20 | Extract_delivery_notice.quote[].currency | string | false | C013-NOTICE:[]; NOTICE-DOC:[] | INTENDED_TRANSFORMATION |
| 21 | Extract_quotation.po_id | string | false | C013-QUOTE:["PO1"]; QUOTE-DOC:["PO1"] | POTENTIAL_CONFLICT |
| 22 | Extract_quotation.supplier_id | string | false | C013-QUOTE:["S1"]; QUOTE-DOC:["S1"] | POTENTIAL_CONFLICT |
| 23 | Extract_quotation.quote[].quote_id | string | false | C013-QUOTE:["Q013"]; QUOTE-DOC:["Q1"] | POTENTIAL_CONFLICT |
| 24 | Extract_quotation.quote[].supplier_id | string | false | C013-QUOTE:["S1"]; QUOTE-DOC:["S1"] | POTENTIAL_CONFLICT |
| 25 | Extract_quotation.quote[].product_id | string | false | C013-QUOTE:["A"]; QUOTE-DOC:["A"] | POTENTIAL_CONFLICT |
| 26 | Extract_quotation.quote[].capacity | integer | false | C013-QUOTE:[60]; QUOTE-DOC:[60] | NOT_VERIFIED |
| 27 | Extract_quotation.quote[].arrival_date | string | false | C013-QUOTE:["2026-11-04"]; QUOTE-DOC:["2026-11-04"] | POTENTIAL_CONFLICT |
| 28 | Extract_quotation.quote[].unit_price | string | false | C013-QUOTE:["1000.00"]; QUOTE-DOC:["1000.00"] | POTENTIAL_CONFLICT |
| 29 | Extract_quotation.quote[].shipping_cost | string | false | C013-QUOTE:["500"]; QUOTE-DOC:["500"] | POTENTIAL_CONFLICT |
| 30 | Extract_quotation.quote[].currency | string | false | C013-QUOTE:["KRW"]; QUOTE-DOC:["KRW"] | POTENTIAL_CONFLICT |
| 31 | Extract_other.po_id | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 32 | Extract_other.supplier_id | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 33 | Extract_other.quote[].quote_id | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 34 | Extract_other.quote[].supplier_id | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 35 | Extract_other.quote[].product_id | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 36 | Extract_other.quote[].capacity | integer | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 37 | Extract_other.quote[].arrival_date | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 38 | Extract_other.quote[].unit_price | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 39 | Extract_other.quote[].shipping_cost | string | false | 해당 branch 미관찰 | NOT_VERIFIED |
| 40 | Extract_other.quote[].currency | string | false | 해당 branch 미관찰 | NOT_VERIFIED |

16개 INTENDED_TRANSFORMATION은 빈 quote[]에 자식 행이 없는 실제 관찰과 quote=null 변환에 한정된다. 해당 필드에서 미래 null 행이 생성될 때의 동작까지 승인한 것이 아니다.
string 13개는 잠재 계약 충돌이다. quotation.capacity 1개 및 other 10개는 옵션/미관찰로 NOT_VERIFIED다. 실제 null branch Native 실패는 0건 재현됐다.
40개 일괄 패치는 적용하지 않았다. CONFIRMED_DEFECT가 없으므로 실행 설정 변경 요청은 발행하지 않고, nullable 지원·실제 QA Input·해당 missing-value 경로 검증을 후속 증거 요청으로 남긴다.

기존 PR25 도구는 선언상 위험을 36 POTENTIAL_CONFLICT / 4 NOT_VERIFIED로 분류한다. 이 보완표는 같은 40개 JSON pointer를 C001/C013에서 실제로 사용된 경로 기준으로 재분류한 것이다. 빈 표 16개와 other 미관찰 10개를 declaration 위험 없음으로 선언하지 않으며, 두 관점의 라벨을 JSON 각 행에 함께 보존했다.
