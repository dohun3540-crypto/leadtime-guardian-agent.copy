# LeadTime Guardian — FINAL TEAM1 E2E RELEASE AUDIT
**Reference date:** 2026-11-03 KST. **Owner:** Team1 구도훈. **Work:** Phase A–G concentrated contract, data and integration audit, not a claim of 480 clock minutes elapsed.

## A. Scope, decision and baselines

The three protected Team1 Draft PRs are **unchanged**:
- [PR #19](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/19) `5d3172deaeecafec0056b48c92f0f0f6bb08297a` — 716 full / 467 Independent QA, Ruff PASS, protected Team3 57 tests + **60 PDF machine PASS**.
- [PR #20](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/20) `53ae1a7dbe53be38a7d585676c2b2d037534fb46` — 740 full / 491 QA.
- [PR #21](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/21) `edab2040430e2159399ee61073fe70e5bdf6cba2` — 748 full / 499 QA, Ruff PASS, Archive/Local Gate PASS_LOCAL.
- Separate [integration PR #2](https://github.com/dohun3540-crypto/yuseok_integration/pull/2) `67b93291c1f32acaf43e45815d2d1119480b652a` remains **Open/Draft/Unmerged**, prior 778 full Python/Ruff/60 PDF machine CI SUCCESS. It was never written to from this task.
- Original Team2 PR #12 `e9b9992b593a42d427ff1bbadeb9a9866ca593bd` and Team3 PR #13 `a925103077173b37d1cefcd6a9576ae644dc2040`, both original CI SUCCESS, read only.

**New isolated branch:** `feat/team1-final-e2e-release-audit-20261104`, base the frozen PR21 branch. New Draft PR #22 contains ONLY Team1-owned preflight/test changes and five audit/handoff artifacts. No original Team2 V6, Team3 archive, Gold candidate, PDF, Studio Config or main branch modified.

### Reproduced, corrected source defects

The new test-first [red workflow #41476866681](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41476866681) found **4 failing tests / 500 passing QA tests** in two distinct new validation gaps:
1. **P1 diagnostic false-positive:** a syntactically valid operational or QA upload receipt with `case_id=C013` and *otherwise matching C001 PDF bytes* recorded a `RECEIPT_CASE_MISMATCH` overall FAIL but **incorrectly kept `local_pdf_receipt_match=true` and `local_operational_native_binding=true`**. These booleans could mislead a later intake operator into promoting untrusted cross-case evidence. The corrected preflight no longer marks such local bindings true.
2. **P1 explicit Native case contamination:** `Native.metadata.case_id=C013` or an embedded normalized `document.case_id=C013` passed the previous C001 local contract if doc IDs/files/digests otherwise matched. The code now compares each *explicitly supplied* case label against `C001` / `SYN-C001`, while still accepting historical `PO-DOC` IDs and correct case labels. A matching Sidecar digest does not redeem contaminated source identity.

New positive regression verifies correct optional metadata/document labels still remain BLOCKED (not FAIL or Live PASS). **Five new pytest cases** were added, none removed or skipped. Corrected source-only [workflow #41477192304](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41477192304) **SUCCESS: 753 full / 504 QA**, Ruff QA/global PASS, C001 archived gate PASS_LOCAL, `local_checks_passed=true`, `overall_status=BLOCKED`.

**Operational impact:** The two defects were in the Team1 *diagnostic preflight*, not confirmed new failures in Team2 V6 production calculations. Remaining unknown Live/Gold behavior must not be called defect-free without genuine data. Final exact documentation HEAD CI is recorded in the new PR body after all files land.

## B. E2E responsibility map and what was actually exercised

| Pipeline | Existing real implementation / reused validator | Evidence boundary |
|---|---|---|
| PDF → Parse → Classify → 3-way Extract | Studio Native V4 archived, `qa.extract_null_contract`, `qa.pipeline_config_audit` | Static schema/archive PASS_LOCAL, NOT newly executed Studio |
| Extract → Merge → Normalize | `qa.studio_contract`, `qa.stage_trace`, `qa.release_inventory`, `qa.e2e_bundle_preflight` | 3 PDF roles, Native IDs, Case, Config, Step/Receipt local checks |
| Normalize → Python Adapter | `studio_integration.documents_from_export`, `validate_documents`, `studio_adapter.apply_studio_extractions` | Strict JSON, exact receipt matching, ISO dates; offline tests only |
| Adapter → Safety V6 | Team2 `engine.analyze_portfolio` via `studio_integration.analyze_studio_documents` | C001/C013/C008/C017 full local synthetic/archived CI; no same-run new Live result |
| Independent QA | `qa.audit`, `qa.studio_qa_adapter`, `qa.input_delivery` | Normalized Input/Report local contract, separate QA Job allowed, malformed Report FAIL |
| Cross-Agent / Provenance | `qa.cross_agent`, `qa.provenance_link`, Team2 `studio-provenance/1` | Sidecar's `export_sha256` bound to original Native bytes locally; cloud upload not authenticated |
| B0/E1 | `qa.experiment_compare` and original-byte identity checks | Same Case/source SHA claims only; real multi-PDF pair, Gold accuracy NOT_MEASURED |
| Human Gold / Release | `qa.xlsx_snapshot`, `qa.review_records`, `qa.gate` | Source workbook/reviewer approval missing; Release BLOCKED |

**B solution and C1/C2/C3 distinctions**:
- **B** — Parse/Classify/Extract/Merge/Normalize; old archived C001 3-document Native and strict schema/duplicate/missing warnings have local regressions. Live B0/E1 not verified.
- **C1 Counterfactual** — Engine includes original vs changed shortage and ETA/quantity comparisons. `tests/test_engine.py::test_baseline_and_counterfactual` + `tests/test_qa_portfolio.py` cover local arithmetic/reference checks. No independently authenticated live counterfactual.
- **C2 Evidence-Grounded Safety Gate** — C013 `PO1/PO999` safety blocking, duplicate/unknown document, receipt/Job/Source SHA, local QA/Provenance fail-closed. `tests/test_qa_combined_v6_contract.py::test_combined_c013_cross_po_is_blocked_and_qa_confirms_safety`; independent PDF page visual verification and live business-block receipts absent.
- **C3 Partial Delivery** — C008 purchase R1 40 EA + R2 60 EA, notice R2 only, unique receipt mapping, shortage and alternate quote capacity/shipping-once. `tests/test_engine.py::test_partial_receipts_two_orders`, `test_quote_capacity_shared_and_shipping_once`, `tests/test_qa_combined_v6_contract.py::test_combined_c008_receipt_isolation_and_independent_reference`. This is validated local allocation logic, **not** an optimal allocation algorithm or live Studio result.

Case-specific C017 DRAFT ISO values must never be treated as tested Korean OCR date extraction. C014 missing revised date, C015 null quantity, C018 null receipt ID and C019 capacity 0 remain source fixture anomalies and are not silently corrected.

## C. Data evidence and missing originals

GitHub inspection found **20** original synthetic case Manifests and **20 DRAFT fixtures**, each Manifest declaring **3** document roles and all cases having `studio_executed=false`, `human_gold_reviewed=false`. The existing Team3 archive previously passed **60/60 machine PDF integrity** (old exact SHA), not fresh PDF semantic review. C001 AI Candidate has `human_reviewed=false`, `team_approved=false`, `gold_frozen=false`, `gold_sha256=null`. The C001 Evidence Matrix 40-row CSV is a candidate and not human-signed Gold. The latest corrected original reviewer XLSX was not found in the source inventory.

Exact field types and 20-case exceptions are in `DATA_CONTRACT_CONSISTENCY_MATRIX.md`. Actual cloud Upload Receipts, complete B0/E1 native stage outputs for C001/C013, exact original V6 output/Sidecar matched to same Native bytes and independent QA original Report/Input, plus approved Gold are still **external blockers**.

## D. Cross-team integration evidence and limitations

The integration PR2 original checkout tree is not locally available to run a true overlay: `git ls-remote https://github.com/dohun3540-crypto/yuseok_integration.git HEAD` failed `Could not resolve host: github.com`. Connector GitHub API read-only **did** inspect target exact tree, Git Blobs and API interfaces:
- New `qa/e2e_bundle_preflight.py`, CLI and synthetic tests **do not yet exist** in integrated PR2.
- Existing `qa.release_inventory`, `qa.studio_contract`, `qa.experiment_compare` blobs match the personal versions.
- Integration `audit.py`, `input_delivery.py`, `strict_json.py` differ intentionally, with hardened typed JSON, underflow and signed-zero protections. **Never overwrite.**
- No import/path conflict detected by static inspection; **actual integrated 778+N merged test run NOT_RUN**.

Next action for the integrated maintainer: apply ONLY new Team1 PR20 original module/CLI/tests with PR22's latest hardened module/tests, then run isolated integrated `pytest`, Ruff, PDF Inventory, Archive and Local Gate on its own new SHA. Use `CROSS_TEAM_INTEGRATION_HANDOFF.md` for the exact Blob SHA manifest.

## E. Readiness estimates, deliberately not measured performance

These are **planning milestones**, not extraction accuracy, business improvement or formal completion metrics. Weighted rule:
- **11/4 Team1 task 90/100** = code hardening 40/40 + standalone CI 25/25 + source/data/contract audit 15/15 + handoff docs 10/10 + actual integrated-tree overlay 0/10.
- **Team1 final submission preparedness 70/100** = code 35/35 + QA/regression 20/20 + handoff 15/15 + real integrated E2E run 0/15 + approved Gold-linked Live evidence 0/15.
- **Entire four-person team final submission preparedness 55/100** = prior core integrated code 30/30 + historical PDF machine inventory 10/10 + local QA 15/15 + selective latest QA overlay 0/10 + authenticated B0/E1/Studio 0/15 + human Gold approval 0/10 + four-person demo evidence 0/10. Other team members' uninspected status may materially change this estimate. This is **not** a measured percent of all project tasks or a claim of their work incomplete.

## F. Decision and 11/4 priority

**Team1 QA additional code work can stop after final exact-head CI success**, because both newly reproduced Team1-owned defects were corrected locally and no other confirmed P0/P1 remains in the covered tests. This is *not* proof that bugs cannot exist in untested Live or merged-tree paths. Switch effort to evidence intake instead of repetitive feature development.

**Priority for 2026-11-04**: (1) integrated maintainer performs selective checkout/overlay and records merged-tree test/CI SHA, (2) Studio owner provides current C001 and C013 single-case B0/E1 original PDF receipt→Config→Job→Stage→Native→QA files, (3) Team2 supplies reproducible exact-Native V6 outcome + `studio-provenance/1` sidecar, (4) Team3 supplies reviewed original `PDF_EVIDENCE_MATRIX.xlsx` and immutable approved Gold record, (5) Team1 executes offline Cross-Agent and source-grounded B0/E1 metrics only if all requirements are met.

**OVERALL_RELEASE_GATE = BLOCKED** until these external inputs and real integrated execution are authenticated. Do not merge to main or approve product release on the strength of synthetic local CI alone.
