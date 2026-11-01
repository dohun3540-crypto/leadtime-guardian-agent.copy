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
