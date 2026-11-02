# LeadTime Guardian — Data Contract & 20-Case Quality Matrix
2026-11-03 KST · Team1 source/manifest audit · **not a Human Gold review**.

## A. Verified source scope and provenance

Read-only GitHub inspection at protected PR #21 SHA `edab2040430e2159399ee61073fe70e5bdf6cba2` found **20** individual `data/cases/SYN-C001...SYN-C020/manifest.json` objects and **20** `extraction_gold.DRAFT.json` fixtures. Each manifest lists **exactly 3** roles (`purchase_order`, `delivery_notice`, `quotation`) with document SHA declarations. All **20** contain `studio_executed=false` and `human_gold_reviewed=false`. Thus **60 SHA declarations exist**, but that is not by itself 60 provider-verified cloud uploads or independently signed Gold.

The original, unchanged Team3 20-case PDF archive passed its historical [machine Inventory workflow](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704) **60/60**, duplicate PDF SHA **zero**; archive SHA-256 `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`. Only C001's **3** actual source PDFs are standalone Git tree files; the other 57 reside in the original archive. This PR neither modifies source bytes nor runs a new Team3-specific 60-PDF workflow.

The `configs/schemas/document_extraction.schema.json` original Normalized Document schema explicitly requires `document_id`, `document_type`, `items`, `warnings`; its top level has `additionalProperties=false`. Other optional and nested types are described below. Stage raw field shape is separately audited by `qa.extract_null_contract` and cannot be assumed to equal final Normalize exactly.

## B. Field-by-field contract / responsibility

| Field / stage | Grounded type and null policy | Meaning / transition / current gate | Owner |
|---|---|---|---|
| `case_id` | Release Preflight string `C001`; PDF archive `SYN-C001` label, explicit allowed normalization | Must not combine cases. Optional Native metadata or document case label must agree when supplied; **new PR22 strict guard** | Team1 |
| `document_id` | Required normalized string, unique | `PO-DOC` and explicit `C001-* / SYN-C001_*` naming supported; explicit other-Case prefix rejected | Team1 + Studio owner |
| `document_type` | Required enum `purchase_order`, `delivery_notice`, `quotation`, `other` | `other` reviewed/blocked by Python operation; all 3 expected source roles bound to files | Studio + Team1 |
| `po_id` | normalized string/null | C013 notice `PO999` vs order `PO1` is intentional **blocking contradiction**; missing optional not to be guessed | Team2 validation |
| `supplier_id` | string/null | Document-type-dependent; quotation may supply S1; absent PO supplier is not automatically conflict | Team2/3 |
| `product_id` | `items[].product_id` required string | Map to trusted inbound/stock/order product; unknown product must not auto-map | Team2 |
| `receipt_id` | `items[].receipt_id` string/null | For C008 R2 specifically changed; an omitted ID only maps if exactly one trusted row matches | Team2 |
| `quantity` | `items[].quantity` integer/null; min 0 in normalized schema | Ordered vs notified vs alternative capacity **different meanings**; missing/null never manufactured as 0; positive input may need stricter business checks | Studio schema / Team2 |
| `unit` | `items[].unit` string/null | C001 EA; no silent conversion | Team2/3 |
| `original_delivery` | ISO date string/null in final Normalize | C017 pre-normalized DRAFT does not prove original Korean OCR-to-ISO; supplied date must match trusted receipt when applicable | Studio/Team2 |
| `revised_delivery` | ISO date string/null in final Normalize | C014 intentionally missing, needs review; Python delivery notice adapter requires valid ISO date | Studio/Team2 |
| `quote_id` | Nested quotation identifier in DRAFT and existing Python validation; nullable behavior depends on quote presence | Do not fabricate quote for non-quotation document | Team2 |
| `capacity` | DRAFT quote integer (20/60/0 examples); Studio extraction may use nullable types | C011 cap20, C019 cap0 legitimate distinct boundary cases; not same as order quantity | Team2 |
| `unit_price` | DRAFT decimal string, e.g. `"1000.00"`, `"1200.00"` | Decimal arithmetic, KRW per EA; no binary-float implicit rounding | Team2 |
| `shipping_cost` | DRAFT decimal string, e.g. `"500"` | Per quote/shipment charge **once**, not multiplied by receipt quantity or number of customers | Team2 |
| `currency` | DRAFT quote string `KRW` | Preserve currency; not implicit exchange rate | Team2 |
| `quote` | Final normalized `object|null`; Studio Extract draft may be array | Array-to-object/null Normalize boundary must be explicitly validated; `qa.extract_null_contract` reports unresolved static nullable conflicts, not Studio Live PASS | Studio + Team1 |
| `warnings` | required normalized array | Nonempty warnings/unknown types must trigger review; not to be silently discarded | Team2 + Team1 |
| `evidence` | optional array of `{source_page: integer>=1, source_field: string, source_value: string, confidence: number|null}` | Local references not equivalent to independent source PDF OCR/page visual grounding | Team3 + Team1 |
| `source_page` | positive integer when provided | Per-PDF page number vs combined 3-page workflow pages must not be conflated | Team3 |
| `file_id` | provider-supplied string in Upload Receipt/Native source_files | Different operational and QA upload IDs are legitimate; each must match its own Receipt and actual PDF SHA | Studio + Team1 |
| `job_execution_id` | Native `job_*` string, Sidecar `studio_metadata_supplied` | Separate QA Job allowed; V6 Sidecar Job must bind *operational* Native and exact bytes | Team2 + Team1 |
| `config_id` / `config_version` | Release string `cfg_*`, positive integer version | Optional Native fields checked when present; do not guess missing configuration provenance | Studio + Team1 |
| `step_run_id` | Native metadata nonempty string | Raw Extract 3, Merge, Normalize, Independent QA step identities must be unique in relevant run | Studio + Team1 |
| `source_sha256`, `export_sha256` | 64-hex SHA claims, compared with original local bytes | Same bytes claim is necessary but **not provider upload authentication** | Team1 + Team2 |
| `qa_status` / Gold | Explicit QA status string; Gold requires human reviewer decisions | Valid JSON QA Report is parseable only; no auto-approval. `AI_CANDIDATE` stays unapproved | Team1/3 |

**Caution**: `configs/schemas/document_extraction.schema.json` constrains normalized `quote` as `object|null` without full nested field typing in that schema; nested quote value representations above are grounded in the inspected DRAFT fixtures and Python validators, not invented as exact Studio Extract provider field types. `qa.extract_null_contract` already exists and raises static risks for nullability; do not rewrite Studio config or broaden parsing automatically.

## C. All 20 source DRAFT case identities

Each row below refers to the **20 original DRAFT fixtures and their manifest declarations**, not real Live Studio observations, independently inspected PDF visual semantics, or approved Gold. All have 3 declared source roles.

| Case | Distinguishing fixture facts | Local interpretation / warning |
|---|---|---|
| C001 | PO1, order/notice R1 100, quote capacity 60, price `1000.00`, shipping `500` KRW | **different business roles, not automatic quantity conflict** |
| C002 | revised date Nov 4 | Early vs C001 revised, date scenario |
| C003 | revised date Nov 12 | Longer delay scenario |
| C004 | same baseline amounts/dates | Scenario variation elsewhere in underlying test base, do not infer from these fields |
| C005 | revised Nov 5 | Date variation |
| C006 | revised Nov 2, prior original Nov 3 | Earlier revised delivery; not an automatic parse failure just because date is earlier |
| C007 | same visible baseline fields | Other scenario attributes require trusted base data |
| C008 | PO R1 40/R2 60; notice R2 60 only | Partial receipt ID isolation; no R1 date mutation |
| C009 | PO R1 100 + RB 30; notice both | Two receipts, do not double allocate |
| C010 | baseline visible fields | Do not infer hidden scenario label |
| C011 | quote capacity 20 | Limited alternate supply |
| C012 | quote unit price `1200.00` | Price/cost variation |
| C013 | PO1, delivery notice PO999 | **intentional PO conflict; safety review/block** |
| C014 | notice revised_delivery null | **Missing critical field**; do not auto-fill |
| C015 | notice R1 quantity null | **Missing critical quantity**; retain JSON null |
| C016 | baseline visible fields | Other scenario attributes require trusted base data |
| C017 | final DRAFT dates ISO Nov 3/Nov 8 and quote Nov 4 | Original Korean date OCR/normalization remains **NOT_VERIFIED_LIVE** |
| C018 | PO R1 50/R2 50, notice receipt_id null/quantity 50 | Ambiguous receipt mapping; review when >1 match |
| C019 | quote capacity 0 | Zero capacity must not become usable alternative |
| C020 | baseline visible fields | Other scenario attributes require trusted base data |

## D. Quality dimensions and Gold

| Dimension | Evidence | Gate |
|---|---|---|
| COMPLETENESS | 20 manifests x 3 declared PDFs; only subset of Live artifacts available | PASS_MACHINE_MANIFEST, LIVE_BLOCKED |
| VALIDITY | Existing strict JSON+date+money+schema and new adversarial case checks | PASS_LOCAL |
| CONSISTENCY | C001 roles, C013 PO conflict, C008 partial allocation, C014/C015/C018 null cases | PASS_LOCAL_CONTRACT; semantic source page NOT_VERIFIED |
| UNIQUENESS | Historical 60/60 original archive, no duplicate file SHA; PR22 receipt identifiers tested | PASS_MACHINE_ONLY |
| INTEGRITY | Historical archive SHA, Git C001 PDF hashes, original SHA/Sidecar local validation | PASS_LOCAL / CLOUD_NOT_AUTHENTICATED |
| TRACEABILITY | New original Release/Native explicit Case guards; preserved original File IDs, Stage API | PASS_LOCAL_PARTIAL, cloud Stage receipts missing |
| BUSINESS_SEMANTICS | Different PO order/notice/quote meaning, quote shipping once, C013 block | PASS_LOCAL_FIXTURE |
| GOLD_READINESS | C001 `AI_CANDIDATE`, 40-row Evidence Matrix CSV, `human_reviewed=false`, `team_approved=false`, `gold_sha256=null` | **PENDING** |

The latest corrected reviewer-owned `PDF_EVIDENCE_MATRIX.xlsx` bytes and signed approval state were **not found** in checked GitHub/Library sources. Only the actual reviewed source workbook and original PDF page evidence may justify official evaluation. Overall: **original PDF visual accuracy, Gold approval and measured B0/E1 improvements NOT_VERIFIED**.
