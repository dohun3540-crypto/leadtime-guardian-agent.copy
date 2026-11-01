# TEAM3_GOLD_REQUEST — PDF source and independently reviewed Gold

To: Team 3 (PDF/Human Gold owner). Existing `data/cases/SYN-C001..SYN-C020/extraction_gold.DRAFT.json` records are generator-origin DRAFT, **not source-verified Gold**.

Please provide per case:

- Original source PDFs (3 per case when applicable), unchanged bytes, filename, SHA-256, source/storage path and checksum method; PDF generation versions when relevant. Compare embedded case manifests to original file bytes.
- Stable `case_id`, `document_id`, `document_type`, PO, supplier, SKU, receipt, quantity/unit, original/revised ETA, quotation quantity/arrival/cost/currency and all applicable multiple-row/partial-receipt details.
- Evidence trace for each gold field: source PDF SHA, document ID, page number, exact source text/span or visual location when available, reviewer decision and ambiguity/nil/exclusion status. Do not invent unsupported values.
- Human reviewer identity/role, review date, reviewed Gold version, exact file SHA, double-review/adjudication of ambiguous fields if performed.
- Proper distinction of literal null, missing field, empty string, string "null", empty list and numerical zero.
- C001 full positive example; C013 PO1 vs PO999 expected reject; C017 original Korean-date expression plus justified or unresolvable ISO normalization; C008 R1=40/R2=60 and R2-only notice.
- Complete 20-case table of labels: document class, field support/ambiguity, expected safe block, human review status and excluded comparison items.

Return three categories distinctly: `DRAFT`, `HUMAN_VERIFIED_GOLD`, `NOT_VERIFIED`. No accuracy metric should include non-human-verified fields. The QA code and Studio generated outputs must not be edited to match Gold.

## 3차 통합 후보와 Gold 검수 상태

QA PR #4는 C001 보관 Native, C013·C017·C008 DRAFT fixture를 팀원 2 엔진과 QA 참조 계산기로 실제 회귀 검증했습니다. 결과 315 QA/504 전체 Python PASS는 **PDF 추출 정확도 검증이 아닙니다**. C013 PO999 차단, C017 한글 날짜 근거 여부, C008 R1/R2 분리 배분을 독립적으로 정확도 측정할 수 있도록 원본 3 PDF SHA, field-level page/evidence, human review/version/date/adjudication status를 사례별로 전달해 주세요. 현재 Human Gold Gate는 BLOCKED입니다.
