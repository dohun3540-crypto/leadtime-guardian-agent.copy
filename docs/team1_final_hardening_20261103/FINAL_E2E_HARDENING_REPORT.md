# LeadTime Guardian — FINAL E2E HARDENING REPORT

Date basis: 2026-11-03 KST. Team1: 구도훈. This document records **local/offline contract validation only**, not certified Studio execution.

## 1. Protected code and dedicated PR

- Original personal PR #19: immutable `5d3172deaeecafec0056b48c92f0f0f6bb08297a`, [716 all / 467 QA PASS](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821541).
- Parallel PR #20: immutable `53ae1a7dbe53be38a7d585676c2b2d037534fb46`, [740 all / 491 QA, Ruff PASS](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41469788883).
- Final hardening: new `feat/team1-e2e-final-hardening-20261103` based exactly on PR #20 commit, new Draft PR #21 targeting PR #20's branch. No changes to PR19/PR20, original Team2 or Team3, integration PR #2, main or Studio.

## 2. Existing contracts reused, not duplicated

`qa.release_inventory.audit_release_folder` reads existing release Manifest, checks local bytes, SHA, paths and Stage Manifest; `qa.studio_contract.audit_native_envelope` checks one Native envelope's document types, IDs and Merge refs; `qa.experiment_compare.audit_b0_e1_readiness` blocks uncertified experiment improvements; `qa.provenance_link` and the combined E2E CLI perform deeper original-provenance and Independent QA validation; Team3 `qa.inventory`, `qa.xlsx_snapshot`, `qa.review_records` remain authoritative for data structures and human-review inputs.

The **new cross-file preflight**, introduced in PR20, is limited to `leadtime-release-evidence/v1` / C001. It joins three locally hash-checked PDF bytes to operational + separate QA Receipt file sets, Native File IDs, operational Job, and original-byte Team2 Sidecar digest. It detects contradictions before all full-E2E materials arrive. It deliberately returns no authenticated Live PASS, no official B0/E1 metric, no human Gold approval.

## 3. Four actual missing validations, red-before-fix

The **test-only red checkpoint** [GitHub Action 41473349263](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473349263) at `813a80d961c2c523d2d7289f885cd789bc0d1900` reported **491 QA passed / 5 QA failed**; the intentionally failing tests exposed four actual Team1 preflight omissions:

1. **Operational Config provenance** — explicit `metadata.config_id` and `metadata.config_version` differing from the saved Manifest were ignored by the new preflight. The revised code checks optional supplied values strictly by Python JSON type/value, without demanding absent fields or changing Team2's serializer. Two regressions reproduce both cases.
2. **Cross-case Native document contamination** — a Native containing `C013-*` document IDs under `case_id=C001` could satisfy document-count/File ID and Sidecar digest tests. The revised code rejects *explicit* `C###-` or `SYN-C###_` prefixes from another case while preserving the legacy `PO-DOC` / `NOTICE-DOC` / `QUOTE-DOC` IDs that do not encode a case. This only detects explicit contradictions; it is not a PDF semantic authentication.
3. **Provided QA Report format** — release inventory verified the supplied Report file's raw byte hash but the preflight never parsed it. A provided report containing duplicate JSON keys (e.g. inconsistent `qa_status`) was treated as present. Now any provided QA Report must be strictly parseable JSON object; full report semantics still belong to the existing Cross-Agent CLI. A parse-only check never means `QA_PASS`.
4. **Merge document source-role confusion** — `audit_native_envelope` checks Merge File IDs exist and document type counts agree, but without checking whether each branch references the original PDF assigned to that document type by the Release Manifest. The new local join checks this when Merge metadata and the declared source PDFs are provided. The original C001 Archive and legitimate matching Merge refs remain valid.

**Minimal changes:** only the Team1-owned `src/leadtime_guardian/qa/e2e_bundle_preflight.py` and existing Team1-only regression `tests/test_qa_parallel_e2e_bundle.py`. No schema rewrite, paid Studio call, other-team code modification or fake Gold. The new tests are five fail-closed cases (Config ID, Config Version, cross-case ID, malformed Report, wrong Merge role) and three positive compatibility cases (matching Config/Merge, archived document IDs, parseable unapproved QA report).

## 4. Verified corrected code checkpoint

[GitHub Actions 41473658472](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473658472) at corrected source+tests commit `4e78d8ea9fa8358acc6f33f33d9ae8acf2803c5e` **completed SUCCESS**:
- **748 whole Python pytest PASS** (baseline 740, **+8** added test cases, inclusive)
- **499 Independent QA pytest PASS** (baseline 491, **+8**, included in full)
- QA Ruff PASS and whole repository Ruff PASS
- C001 Archive replay/local Integration Gate PASS_LOCAL, `local_checks_passed=true`, `overall_status=BLOCKED`.

A final exact-HEAD CI must run again after this documentation is committed. The final **PR #21 body** records that HEAD + CI pair; do not assume an older run proves success of a newer docs-only commit.

## 5. Evidence-chain status and scenario readiness

- **C001:** existing synthetic original 3-PDF inventory and candidate record, proposed alternate quote 60 vs order/change 100, existing archived Native, all local identity/error contracts. Latest actual B0/E1 multi-PDF Native+stage proof, provider upload receipts and same-run V6 are still unavailable.
- **C013:** intentional `PO1`/notice `PO999` must block unsafe approval. The historical stored Native warning is not a new certified run. Explicit `C013` document ID injection into C001 now fails in local preflight.
- **C008:** R1 40 EA and R2 60 EA; only R2 changed, unit-cost vs one-time quote shipping distinct. Existing portfolio/Safety contracts cover this locally. Not a new Live test of this Preflight.
- **C017:** stored DRAFT ISO dates do not prove actual Korean date extraction. Raw-original date normalization remains an external Studio/Python validation.
- **B0/E1:** same case and PDF byte identities must match; each experiment's own Job/Config/Step may differ legitimately. Official improvement `NOT_MEASURED` and `official_metrics_eligible=false` without authenticated Raw Native, QA, V6 and human Gold.

## 6. Current command and limits

```sh
python scripts/team1_e2e_preflight.py --manifest /private/evidence/release_evidence.json --json-report /private/results/team1_hardening_new.json
python scripts/qa_stage_intake_check.py --manifest /private/evidence/stage_manifest.json
python scripts/qa_combined_e2e_check.py --help
python scripts/qa_b0_e1_compare_check.py --help
```

Real files must be supplied privately; the preflight never calls Studio or overwrites originals. Exit 1=invalid evidence, exit 2=blocked/unverified. QA JSON parse PASS is **not** a real IndependentQA verdict. File IDs and locally matched PDF hashes do **not** independently prove provider upload. Gold verification requires an original independently approved XLSX, PDF page evidence and signed review metadata.

### Final local recommendation

These fixes close the four newly reproduced local contract gaps without changing the team boundary. No additional independent Team1 feature is established as mandatory by the current audit. Real integrated-tree execution remains separately required by the integration owner, and **full product release must remain BLOCKED**.
