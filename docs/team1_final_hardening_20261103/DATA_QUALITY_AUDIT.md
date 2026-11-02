# LeadTime Guardian — Data Quality / Semantic Consistency Audit

**2026-11-03 KST • Team1 read-only assessment.** This document intentionally separates *machine source integrity* from *PDF visual semantics*, actual Studio extraction, Live provenance and approved human Gold.

## Scope and evidence

- The prior exact frozen personal PR #19 [Team3 workflow 41465821704](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704) verified **20 synthetic cases / 60 PDFs** in the original asset archive by the `qa.inventory` checker: 60 machine PASS, 0 FAIL, 0 BLOCKED, no duplicate archive SHA. Original asset archive SHA-256 `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`. The *new PR21* modifies **no original PDF, manifest, Gold candidate, data asset, engine or Team3 `qa/` code**. Do not claim this was independently rerun as a new Team3-specific PDF workflow if that workflow did not trigger.
- C001 three standalone Git PDF source file entries and manifest SHA agree with existing C001 Candidate source records in the frozen baseline. `qa/gold_candidates/SYN-C001/PDF_EVIDENCE_MATRIX.csv` has **40 rows** in its existing approved-for-machine-check format, but approval fields remain PENDING.
- Existing Team3 tools `qa.xlsx_snapshot` and `qa.review_records` are the official ingestion steps for a future corrected XLSX and human reviewer metadata. **The latest corrected `PDF_EVIDENCE_MATRIX.xlsx` original is not present in the inspected GitHub source/earlier Library inventory**, and its actual cell types/formulas/reviewer approvals therefore cannot be verified. No cells/reviewers/timestamps/Gold hashes were generated.
- Case data below is from each `data/cases/SYN-C###/extraction_gold.DRAFT.json` (DRAFT fixture). The DRAFT label is **not** independent human Gold, blind truth or successful new Studio extraction. Assertions about their values are *fixture-level only*.

## Quality dimensions

| Dimension | Actual verified scope | Status / reason |
|---|---|---|
| COMPLETENESS | C001 manifest lists the original three PDF roles; archived portfolio inventory has 60 expected PDFs | PASS_MACHINE_ONLY; full Live Extract/QA/Gold absent |
| VALIDITY | Existing JSON strict type rules, date/quantity/amount local regression; new report duplicate-key rejection | PASS_LOCAL; no new field-wise source visual review |
| CONSISTENCY | C001 different business roles, C013 explicit PO conflict, C008 receipt allocation, C017 normalized fixture | PASS_LOCAL_FIXTURE; Live semantic extraction NOT_VERIFIED |
| UNIQUENESS | Archived PDF SHA duplicate report zero; extra File ID duplicate/mismatched Native tests | PASS_MACHINE_ONLY |
| INTEGRITY | Existing original Git asset SHA plus new local PDF/Receipt/Native/Sidecar SHA joins | PASS_LOCAL_SOURCE_BYTES_ONLY, provider uploads NOT_AUTHENTICATED |
| TRACEABILITY | Existing manifest/candidate PDF names/pages, new explicit Merge source-role and cross-case Native ID checks | PARTIAL_LOCAL; provider File/Job/Step and field evidence chains incomplete |
| GOLD_READINESS | Existing AI Candidate status and Team3 XLSX/review tooling | PENDING; human-approved original XLSX, final signatures and Gold version absent |

No extracted field accuracy, business recommendation improvement, missing-rate percentage, gold precision, evidence recall or B0/E1 uplift may be reported from these data alone.

## C001 — quantity roles and cost semantics

- Purchase: PO1, product A receipt R1, ordered **100 EA**, original delivery **2026-11-03**.
- Delivery notice: same PO1 and R1 **100 EA** affected; revised delivery **2026-11-08**.
- Alternative quotation: Q1, supply capacity **60 EA** and arrival **2026-11-04**. The 100 EA obligation and 60 EA *alternative available quantity* are **different roles**, not evidence of contradictory document quantities. A potential outstanding 40 EA must not be silently represented as delivered.
- Unit price is the decimal string `"1000.00"` with currency **KRW**; quote shipping cost is `"500"` **per shipping quotation**, not per each 60 EA unit or a repeated receipt cost. Actual routing/accounting uses Team2's unchanged calculation engine and base case, not this audit report.
- The manifest has original PDF hash entries and C001 candidate points to them. The Evidence Matrix has 40 candidate rows, not independently signed source field truth.

## C013 — intentional conflict

- PO and quotation refer to **PO1**; delivery notice refers to **PO999**.
- This discrepancy is **intentional** and must not be repaired as a data typo or bypassed to allow an unsound alternate purchase recommendation.
- Existing archived Normalize output contains a conflict *warning*, not authenticated V6 safety-block execution. New PR21 local preflight also rejects explicit `C013`-prefixed Native Document IDs under a C001 release, preventing a distinct class of case mixing.
- Actual Native→Python business blocking and external action inhibition remain `NOT_VERIFIED_LIVE`.

## C008 — partial receipt allocation

- Purchase PO1 lists receipt R1 **40 EA** and R2 **60 EA** (100 total ordered).
- Delivery notice changes **only R2 60 EA**, not R1.
- Alternative quote capacity 60 EA is not a second occurrence of the same receipt quantity. Shipping cost 500 KRW is a one-time quote line, not repeated per receipt.
- No local source manipulation or changes to Team2's allocation model. New live Studio allocation/receipt ID proof unavailable.

## C017 — Korean date normalization

- DRAFT fields retain ISO strings: original **2026-11-03**, revised **2026-11-08**, quoted arrival **2026-11-04**; the DRAFT ordering is internally consistent for their distinct roles.
- This does **not** prove the actual Korean source date (including localized spacing, Korean suffixes or OCR) was extracted or normalized correctly by Studio. That requires original PDF page-to-Native field evidence and explicit Python validation.
- No dates were silently rewritten.

## New defect-level evidence risks and corrections

New PR21 fail-first regression [41473349263](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473349263) proved that: (1) explicitly wrong Native Config IDs/versions were not independently diagnosed; (2) C013 document IDs could be accepted in a C001 binding; (3) duplicate-key raw QA reports were not strictly parsed; (4) the Merge document type could reference the wrong role-specific PDF while source File IDs still existed. The new Team1-only Preflight checks each of those local contradictions, without asserting cloud authenticity or human truth. Correction verified on 748/499 passing source CI [41473658472](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473658472).

## Required outstanding source verification

Original corrected, private `PDF_EVIDENCE_MATRIX.xlsx` with a retained SHA, sheet name, original PDF page/field locations, actual typed reviewer cells, timestamp, approval state and frozen Gold version; actual B0/E1 Native/Config/Step/Upload receipts; independent QA input/report; Team2 V6 same-run output/Sidecar. No Gold or Live Gate can be promoted without these original materials.
