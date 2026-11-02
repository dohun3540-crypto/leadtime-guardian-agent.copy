# LeadTime Guardian — FINAL REGRESSION & CI Evidence
2026-11-03 KST · Team1 isolated final evidence audit · no new paid Studio runs.

## 1. Validated protected baselines

| Scope | SHA | CI evidence |
|---|---|---|
| PR19 independent QA source freeze | `5d3172deaeecafec0056b48c92f0f0f6bb08297a` | [716 full/467 QA](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821541); [57 Team3 / 60 PDF archive](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704) |
| PR20 local cross-source preflight | `53ae1a7dbe53be38a7d585676c2b2d037534fb46` | [740 full/491 QA, Ruff](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41469788883) |
| PR21 local E2E hardening | `edab2040430e2159399ee61073fe70e5bdf6cba2` | [748 full/499 QA, Ruff](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41474378468) |
| Existing integrated PR2 | `67b93291c1f32acaf43e45815d2d1119480b652a` | [778 full, Ruff, 60 PDF machine](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285) |

**All counts are inclusive**: QA subset is included in the full pytest number. None of the protected HEADs was modified during this audit.

## 2. Red-before-fix checkpoint

New isolated PR22 initially committed **five** fail-closed/compatibility tests (no source edits) at `67db92d471a72b98d1a31023f1790f328abd6bf3`. [GitHub Actions run #41476866681](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41476866681) recorded **500 Independent QA PASS / 4 FAIL** on two classes of broken source provenance binding:
- Operational and IndependentQA receipt with C013 ID was reported as invalid overall, but `local_pdf_receipt_match` and hence `local_operational_native_binding` could incorrectly still be **true** if the PDF names/SHA matched.
- Explicit operational Native `metadata.case_id=C013` or `documents[].case_id=C013`, while the outer release bundle was C001, incorrectly remained **BLOCKED** instead of proper **FAIL**, even when Team2 Sidecar `export_sha256` matched the contaminated Native raw bytes.

These were actual bugs in the Team1 **new E2E preflight diagnostics**, not claims that Team2's production engine was wrong. The fifth test checks valid C001 / SYN-C001 case labels stay allowed.

## 3. Minimum source correction and actual green CI

Source-only fix in `src/leadtime_guardian/qa/e2e_bundle_preflight.py` at `f26773d1a3183b73025bbaea2ddce971f2af0671`, Blob `9fa51ce0d41467fb7618fd9dbf00075c61c38d3c`:
- Any reported operational/QA receipt invalidity prevents the `local_pdf_receipt_match` local diagnostic from claiming success; Native local binding cannot become true on top of wrong-Case receipts.
- Optional explicit Native metadata and embedded document `case_id` fields must equal release `C001` or `SYN-C001`; missing optional case labels are **not** invented, and original `PO-DOC` document IDs still pass.
- The historical PR21 Config/Version, Document ID prefix, Merge PDF source role, strict QA Report JSON and legitimate separately-run Independent QA checks were **retained**.

[Actual correction GitHub Actions #41477192304](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41477192304): **504 Independent QA PASS**, **753 whole Python PASS**, QA/global Ruff PASS, C001 archive local check PASS_LOCAL, `local_checks_passed=true`, `overall_status=BLOCKED`. No skipped/deleted/relaxed baseline assertions, **+5 new tests** versus PR21 (748→753; 499→504).

All source and test changes are limited to:
- `src/leadtime_guardian/qa/e2e_bundle_preflight.py` (owned Team1)
- `tests/test_qa_parallel_e2e_bundle.py` (owned Team1)

## 4. Existing functional regression coverage (code only)

The full tests' actual source includes these specific fixtures:
- B/C1: `tests/test_engine.py::test_baseline_and_counterfactual`, `tests/test_qa_portfolio.py`.
- C2: `tests/test_engine.py::test_po_conflict_blocks`, `tests/test_qa_combined_v6_contract.py::test_combined_c013_cross_po_is_blocked_and_qa_confirms_safety`, `tests/test_qa_provenance_link.py`.
- C3: `tests/test_engine.py::test_partial_receipts_two_orders`, `test_quote_capacity_shared_and_shipping_once`, `tests/test_qa_combined_v6_contract.py::test_combined_c008_receipt_isolation_and_independent_reference`.
- B0/E1: `tests/test_qa_b0_e1_comparison.py` same-source claims, invalid split Jobs, and comparison remains `NOT_MEASURED` without actual raw/live Gold. The `qa.extract_null_contract` checks Studio-to-normalized null handling in static configuration (not an authenticated run).
- Cases C001, C013, C008, C017 use local/DRAFT or archived material. C017 Korean text OCR-to-ISO evidence has **not** been authenticated.

These tests establish only **local contract/model regression at the personal branch HEAD**. The actual merged integration tree with new PR20/21/22 files has **not** been executed locally. `git ls-remote` failed DNS, and there is no new integration exact-HEAD CI to cite.

## 5. Data integrity and workflow boundaries

- This PR does **not** alter Team2 engine, strict JSON, Studio Adapter, Team3 source PDF archive or any of the 20 original DRAFT/manifest/Gold candidate records.
- Existing archived Team3 60-PDF machine result comes from the protected PR19 run. **No new Team3-only PDF workflow was triggered by the PR22 source+docs paths.** Do not substitute 20 Manifest x 3 declarations for independently read 60 PDF bytes.
- Approved XLSX/Gold original and live B0/E1 Source Receipt → Stage → V6 → QA evidence chains remain missing. Correct post-run Local Gate is `overall_status=BLOCKED`, not a failure of safe code.

## 6. Reproduction and future integrated checks

```sh
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
# inherited CI also executes its archived C001 and Local Integration Gate
```

Integrated owner additionally runs `python -m qa.inventory --root . --out /private/new-unique-out` and matches original archive SHA/QA identities before and after selective source overlay.

## 7. Final HEAD after documentation

The above successful code-only run tested SHA `f26773d1a3183b73025bbaea2ddce971f2af0671`. This audit document and companion manifests were committed afterward without changing source/tests. The **final exact-HEAD CI and SHA pair must therefore be reverified and recorded in Draft PR #22's description**; do not claim the earlier CI run covers later docs-only commits.

No new product-release permission is inferred; all Live/Gold-related Gates remain BLOCKED/PENDING/NOT_MEASURED.
