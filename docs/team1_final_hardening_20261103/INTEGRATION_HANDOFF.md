# Final Team1 E2E Hardening — Selective Integration Handoff

**Purpose**: transfer only verified Team1 improvements from new Draft PR #21, without overwriting the earlier PR #20 functionality or the integration repo's strengthened Team2/Team3 implementations.

## Exact protected refs / destination (as observed)

- Personal original freeze PR #19: `5d3172deaeecafec0056b48c92f0f0f6bb08297a` (UNCHANGED).
- Personal parallel intake PR #20: `53ae1a7dbe53be38a7d585676c2b2d037534fb46` (UNCHANGED).
- New hardening source PR #21: `feat/team1-e2e-final-hardening-20261103`, **base PR20 branch**, final SHA and CI recorded in the new PR body after final HEAD validation.
- Read-only destination `dohun3540-crypto/yuseok_integration` Draft PR #2 at last observed `67b93291c1f32acaf43e45815d2d1119480b652a` ([778 full pytest/Ruff and 60-PDF CI SUCCESS](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285)). Check its HEAD again before integration.

## Source changeset (exact file Git Blob SHAs)

| Apply order | Path | Source Blob SHA | Integration action |
|---:|---|---|---|
| 1 | `src/leadtime_guardian/qa/e2e_bundle_preflight.py` | `d6b66339f192f8edbc4d822b6070e13d41caeab5` | copy/overlay entire hardened version from PR21 |
| 2 | `scripts/team1_e2e_preflight.py` | `7968fffbe93be4e67175baa09786dccbe751cdde` | copy unmodified CLI from PR20 |
| 3 | `tests/test_qa_parallel_e2e_bundle.py` | `1cd238e9973622c6620c925b760731feef47dd07` | copy/overlay entire expanded tests from PR21 |
| 4 | `docs/team1_parallel_readiness_20261103/README.md` | `56dea32f35f9d9d6de06bc7bab921b376f24277b` | optional historical intake contract |
| 5 | `docs/team1_parallel_readiness_20261103/INTEGRATION_CHANGESET_MANIFEST.json` | from PR20 unchanged | optional historical source map |
| 6 | `docs/team1_parallel_readiness_20261103/FINAL_REGRESSION_REPORT.md` | from PR20 unchanged | optional historical regressions |
| 7 | `docs/team1_final_hardening_20261103/` | see PR21 latest changed files | new final audit, quality, compatibility, tests and handoff |

**Important:** PR21 diff over PR20 should contain only two changed Team1 files plus new docs. PR20's *initial code* is **not** present as new additions in PR21's isolated diff. If integrating directly into `yuseok_integration`, copy both PR20's original new files and PR21's hardened versions, not just PR21's diff.

**Prohibited overwrites:** `src/leadtime_guardian/strict_json.py`, `src/leadtime_guardian/qa/audit.py`, `src/leadtime_guardian/qa/input_delivery.py`, `qa/inventory.py`, Team2 Safety V6 calculation/Adapter/Provenance files, Team3 `qa/` and `data/` archive, original Native/Gold/Manifest and `.github/workflows`.

No dependency changes, new third-party imports, schema migrations or workflow edits; current module imports existing `qa.audit.load_json_strict`, `qa.experiment_compare.audit_b0_e1_readiness`, `qa.release_inventory`, and `qa.studio_contract.audit_native_envelope`.

## Repro / test commands for destination maintainer

Run in a **disposable local checkout** of the integrated PR #2 latest SHA (the private repo must be accessible with a valid GitHub authorization):

```sh
python -m pip install -r requirements-validation.txt
python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
python -m pytest -q
python -m ruff check .
python scripts/qa_archive_check.py --root .
python scripts/qa_gate_check.py --root .
python -m qa.inventory --root . --out /new/private/unique-inventory-dir
python scripts/team1_e2e_preflight.py --manifest /private/evidence/release_evidence.json --json-report /private/new/result.json
```

Use a **new report path** on each run; the CLI fails closed rather than overwriting existing evidence. When supplied data are absent, exit 2 means BLOCKED, not operational success. Compare the post-overlay test collection with existing **778 whole Python tests**, but do not presume it simply adds 32 or 8: compare collected tests and run the whole merged suite.

## Runtime boundary / explicit gaps

**Local merged-tree validation was not performed in this Task**. The available container's `git ls-remote` failed with `Could not resolve host: github.com`; only connector-based *source tree and Git Blob* static checks and actual source PR21 GitHub Actions are available. No remote push/branch/merge to the integrated repo was attempted. The integration maintainer must perform actual overlay, dependency and full test verification before `INTEGRATION_SIMULATION_GATE` can PASS.

The new Preflight guards explicit Native Config mismatches, C###-prefixed case mix, Strict JSON QA Report duplicates and Merge source PDF role mismatch while allowing valid separate QA Job IDs. It remains a local C001 intake contract, not a full Live case classifier or Human Gold verifier. The original correct XLSX/Gold review and original Studio Native/Stage/Receipt/V6 Sidecar/QA chains are still external requirements.

## Team responsibilities after handoff

- **구도훈 (Team1):** retain source code/CI checkpoint, apply original Native evidence to the existing cross-agent and Release Gate once received, B0/E1 same-case measured comparison only after approvals.
- **윤현준 (Team2):** supply original Python V6 result on the exact Native bytes, its Sidecar `export_sha256` + Job mapping and local reproduction command; ensure production strict JSON is not replaced.
- **김민주 (Team3):** supply the corrected original `PDF_EVIDENCE_MATRIX.xlsx` with true cell types, page links, actual reviewer approvals, signed Gold version and hash; do not auto-approve AI Candidate.
- **Integration maintainer:** isolated overlay, exact HEAD workflow CI, unchanged core and original archive SHA, post-merge local Gate and actual receipt/Gold tests before choosing final merge approval.

**Final product Release remains BLOCKED** pending authentic Live Studio, provenance and human Gold. GitHub local code PASS is not product release.
