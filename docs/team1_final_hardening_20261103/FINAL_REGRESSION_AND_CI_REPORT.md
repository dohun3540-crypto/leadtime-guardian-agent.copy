# Team1 Final E2E Hardening — Regression and CI

## Baselines

| Protected source | Exact SHA | Actual CI status |
|---|---|---|
| Personal Code Freeze PR #19 | `5d3172deaeecafec0056b48c92f0f0f6bb08297a` | [716 Python / 467 QA, Ruff pass](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821541); [Team3 57 tests + 60 PDF machine PASS](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704) |
| Parallel E2E PR #20 | `53ae1a7dbe53be38a7d585676c2b2d037534fb46` | [740 Python / 491 QA, Ruff pass](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41469788883) |
| Read-only integrated PR #2 | `67b93291c1f32acaf43e45815d2d1119480b652a` | [778 Python / 60 PDF inventory, Ruff pass](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285) |

## Red-first evidence and repairs

- Red QA-only regression [run #41473349263](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473349263) on test-only SHA `813a80d961c2c523d2d7289f885cd789bc0d1900`: **491 passed, five failed**; these five failures proved four previously unhandled local contract gaps (Native Config ID, Config Version, explicit cross-case document ID, malformed duplicate-key QA report, swapped Merge source PDF role). This is a **diagnostic red checkpoint**, not a successful code freeze.
- Minimal production correction applied **only** to `src/leadtime_guardian/qa/e2e_bundle_preflight.py`; eight new cases in `tests/test_qa_parallel_e2e_bundle.py`, including three positive compatibility checks (matching native Config/Merge, original `PO-DOC` naming, well-formed but unapproved QA report). All baseline tests retained.
- Corrected source and expanded tests at exact SHA `4e78d8ea9fa8358acc6f33f33d9ae8acf2803c5e` verified by [GitHub Actions #41473658472](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41473658472): **499 QA PASS**, **748 full Python pytest PASS**, QA Ruff and whole Ruff PASS, archived C001 and local gate checks true with `overall_status=BLOCKED`.
- Whole Python counts are inclusive: full 740→748 (+8), QA 491→499 (+8); do not add 499 to 748, do not imply 8 separate measured Studio jobs.
- **After docs-only final commits:** new branch exact HEAD and exact commit-associated CI must be rechecked. Final Draft PR #21 description records authoritative final HEAD/CI; do not present source-only #41473658472 as evidence of later docs-only commits.

## Inputs / scope checked

- Original C001 synthetic fixture for 3 PDF roles, operational + QA Upload Receipt identities and SHA, Native ID/Job/optional Config binding and document/merge role, Team2 Sidecar raw digest and Job, strict QA Report JSON parse (not full review schema), separate Independent QA Job, B0/E1 equal original PDF manifest claims, duplicate SHA/Job/File ID and raw JSON rejection.
- Existing regression suite includes C013 mismatched PO handling, C008 partial delivery/receipt allocation and C017 normalized fixture/date contracts. None are labeled new certified Studio Live execution.
- Original C001 source files, Gold Candidate, Team3 archived 20-case/60-PDF data and all Team2 operating code have identical Git Blobs between protected PR #20 and this hardening branch (the new diff changes only Team1 preflight/test and adds documents).
- The new PR's **Independent QA workflow runs full Python, Ruff, archived local replay + local gate**. The Team3-exclusive PDF inventory workflow **was not triggered by PR21's scoped source/docs paths**; the previous frozen PR19 60/60 result is historical machine integrity evidence, not falsely labeled as run anew for PR21.
- A genuinely merged-tree integration checkout was **NOT_RUN** because external GitHub DNS was unavailable in the isolated container; static exact-file/name/Blob dependencies were checked using GitHub connector.

## Reproduction commands

```sh
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
python scripts/qa_archive_check.py --root .
python scripts/qa_gate_check.py --root .
```

## Final gate logic

| Gate | Honest result |
|---|---|
| PERSONAL_CODE_FREEZE | PASS, protected PR19+PR20 unmodified |
| TEAM1_PARALLEL_CODE_READY | PASS on source regression CI, final docs-only SHA must be checked |
| INDEPENDENT_QA_GATE | PASS_LOCAL |
| CROSS_AGENT_CONTRACT_GATE | PASS_LOCAL |
| DATA_QUALITY_GATE | PASS_MACHINE_ONLY / PARTIAL_LOCAL_SEMANTIC |
| PDF_INTEGRITY_GATE | PASS_PROTECTED_60_60; NOT_RERUN_IN_NEW_BRANCH |
| PROVENANCE_LOCAL_GATE | PASS_LOCAL for synthetic source identity joins |
| E2E_PREFLIGHT_GATE | PASS_LOCAL |
| INTEGRATION_COMPATIBILITY_GATE | STATIC_COMPATIBILITY_ONLY |
| INTEGRATION_SIMULATION_GATE | NOT_RUN_NETWORK_RESTRICTED |
| FULL_REGRESSION_GATE | PASS source-code CI; latest final SHA pending confirmation |
| CI_GATE | PASS source-code CI; latest final SHA pending confirmation |
| STUDIO_LIVE_GATE | BLOCKED |
| PYTHON_V6_LIVE_GATE | BLOCKED |
| HUMAN_GOLD_GATE | PENDING |
| B0_E1_COMPARISON_GATE | NOT_MEASURED |
| FULL_PRODUCT_RELEASE_GATE | BLOCKED |

No additional Team1 runtime fixes were found after the four corrected defects and passing regression tests. Human Gold approval, authenticated Studio uploads and actual same-run Python/QA, B0/E1 metrics are **not** produced by this test suite.
