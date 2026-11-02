# LeadTime Guardian — Three-member final integration and code-freeze review

**Date:** 2026-11-02 KST. **Task target:** 2026-11-03. **Owner:** Team 1 (구도훈).
**Work repository:** `dohun3540-crypto/leadtime-guardian-agent.copy`
**Branch:** `feat/all-team-qa-final-freeze-20261103`
**PR base:** `feat/qa-pr13-pr14-final-selective-freeze-20261101` at `ece3a7dcc254b5c7a14c72792750170346419eb8`.
**Code base commit:** PR #17 exact source HEAD `fcc2afb2be315e261fa35b9ab17ee1a1134f578c`.
**QA hardening donor:** PR #18 exact HEAD `34f023f594e6bfeea60cb7ee88fce9b7f3140121`.

## 1. Verified prior evidence and exact source distinction

Both original PRs were Draft/Open, unmerged and mergeable when inspected. Comparison PR #17 -> PR #18 was **diverged**, ahead 4 / behind 3; merge base `ece3a7d...`. PR #17 changed 31 files (Team3 package/CI/test/docs); PR #18 changed four different paths (experiment_compare, regression test, two historical reports). There were **no identical modified paths** across the two PR diffs. No full PR merge or cherry-pick was necessary.

- [PR #17](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/17): exact-HEAD Independent QA [run 41458294002](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41458294002) completed SUCCESS, 690 whole Python / 441 Independent QA, QA and repo Ruff PASS, C001 archived local gate with `overall_status=BLOCKED`. Team3 [run 41458294030](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41458294030) SUCCESS, 57 Team3 pytest, Ruff PASS, 60 PDF original machine inventory PASS / 0 FAIL / 0 BLOCKED, no duplicate hashes. Counts are subsets of the 690.
- [PR #18](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/18): exact-HEAD [run 41458386262](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41458386262) SUCCESS, 639 full / 450 QA / Ruff PASS / local overall BLOCKED. This branch did not contain Team3's 57 tests.
- Historic PR #15 baseline: 630 full / 441 QA / Ruff PASS; not a substitute for new-branch testing.

**Only the new-branch final HEAD and its successful workflow job logs may justify a new CODE_FREEZE=PASS.** CI numbers from sibling branches must not be added together or represented as the new result.

## 2. Changes staged in this branch

1. Preserve PR #17's combined Team1+Team2+Team3 source, data, existing tests, isolated Team3 workflow and integration gates without modifying Team2 code or Team3 source PDFs.
2. Copy PR #18 `src/leadtime_guardian/qa/experiment_compare.py` exactly (original Git Blob `0c0bbf2c38456019d891625e7486e379e1f96ecf`) into the PR #17 branch. Existing file received minimal donor patch:
   - reject duplicate source `file_id` within each run;
   - reject duplicate operational `step_run_id`;
   - reject conflicting supplied operational Step Job/Config/version metadata, while keeping optional metadata optional and IndependentQA separate-Job identity legitimate;
   - allow C013 or another same-case local normalized field diff, but block C001/C013 cross-case mixing and preserve `NOT_MEASURED` improvement.
3. Copy PR #18 `tests/test_qa_experiment_identity_hardening.py` exactly (Blob `220f0a43f3e6638b90cf6721b1abb7f1e4d31ccb`): nine local synthetic fail-closed tests.
4. Copy PR #18 prior reports (historical source branch status, **not** the latest combined release verdict).
5. Add Team1-owned `tests/test_qa_c001_data_candidate_consistency.py` with five read-only source-consistency tests: same manifest/C001 PDF hashes, no Gold promotion, strict draft field/type equality, 40 evidence matrix source and candidate mappings, and distinct PO/notice/quote business roles including decimal string/currency preservation. This is **not human source review**, and does not change any original Team3 files.

The source integration adds no new workflow execution, model results, invoice, purchase action, emails, paid Studio requests, Gold approval or original PDF changes.

## 3. Immutable source and data scope

Team1 retained `src/leadtime_guardian/qa/` (Independent QA, Stage/Batch Intake, Cross-Agent, provenance and strict Studio JSON). Team2 retained `src/leadtime_guardian/{engine,studio_adapter,studio_integration,agents_api,provenance,strict_json}.py` (six Blob SHA matches previously verified by PR #17 to Team2 original PR #12 at `e9b9992b593a42d427ff1bbadeb9a9866ca593bd`). Team3 retained `qa/`, `tests/qa/`, C001 Candidate/CSV and isolated `member3-data-check` workflow (PR #17 recorded 25/25 exact matching imported blobs from Team3 original PR #13; one workflow adapted). Since this branch is a descendant of PR #17 with changes limited to the explicitly listed QA/test/report paths, the original Team2 core and Team3 imported sources are not rewritten here.

The source C001 manifest contains three synthetic PDFs and identical SHA-256 values to the AI Candidate `sources`; the machine PDF inventory is separate evidence. Candidate `candidate.v1.json` declares `AI_CANDIDATE`, `human_reviewed=false`, `team_approved=false`, `gold_frozen=false`, `eligible_for_official_metrics=false`; Evidence Matrix is 40 rows with approval still PENDING. C001's PO/notice 100 EA and quote capacity 60 EA are different business roles, not an automatic quantity conflict; quote unit price `1000.00` and shipping `500` are decimal *strings* with KRW, not an evaluated purchase.

The Team3 migration state explicitly records the latest corrected review XLSX was user-supplied in a **different conversation**, but original bytes, checksum, cell-level check, and official Gold freeze were not transferred to GitHub. Do not state that the user never reviewed anything; do state that approved original evidence **is not available in this code baseline**.

## 4. Run exact source validation (no Studio calls)

```bash
git checkout feat/all-team-qa-final-freeze-20261103
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_experiment_identity_hardening.py tests/test_qa_c001_data_candidate_consistency.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q tests/qa
PYTHONPATH=src python -m pytest -q
python -m ruff check .
python -m qa.inventory --root . --out ../ltg-final-inventory-unique
```

Use a new inventory output directory; source files are read-only. The actual CI workflow installs dependencies and supplies Python 3.11. Do **not** claim a local shell run unless one was actually executed; connector-based GitHub Actions are valid remote CI evidence, not local execution.

Existing project read-only E2E and provenance CLIs: `scripts/qa_release_evidence_check.py`, `qa_stage_intake_check.py`, `qa_combined_e2e_check.py`, `qa_b0_e1_compare_check.py` (exact prerequisites and commands: `docs/NINTH_RELEASE_VALIDATION_RUNBOOK_20261101.md`). Execute live evidence contracts only with preserved authentic originals; do not invent inputs. `qa_studio_batch_check.py` already correctly reports split three PDF Jobs as invalid grouping.

## 5. Pipeline reality and missing release evidence

Configured/intended architecture:
PDF → Studio Parse/Classify/Extract/Merge/Normalize → Native JSON → Python Adapter → Safety V6 → Independent QA → Cross-Agent → Gold Evaluation → Release Gate.

The same-tree **code interfaces and synthetic/offline cases** are tested via GitHub CI; this does not certify each operational Studio node or a single live provider-to-approval execution. Local Safety V6 numbers, archive replay, single-file Job reports, API mocks, QA summaries and unreviewed draft Gold must never be mixed into one authenticated result.

Case experiment readiness:
- B0-C001 **BLOCKED**: previous file-specific Job triplet is not a unified case; earlier reported single-Job B0 lacks complete original Step/Normalize/QA source chain.
- B0-C013 **NOT_VERIFIED**: no authenticated three-PDF C013 current Native plus PO1/PO999 raw proof.
- E1-C001 **NOT_VERIFIED**, E1-C013 **NOT_VERIFIED**: same-source raw runs, saved configs, Job/Step/Upload receipts not authenticated.
- B0 vs E1 numerical accuracy/evidence improvement: **NOT_MEASURED**.

Needed: original B0/E1 PDFs and SHA; operational/QA file upload receipts; workflow/config/version and Job/Step IDs; exact native Extract 3/Merge/Normalize bytes; actual QA input and raw report; Team2 true Python Safety V6 output and provenance sidecar; Team3 original reviewed XLSX and approved field-level page Gold with reviewer/version/time; then independent approval.

## 6. Final gates (code tests conditional on new HEAD)

| Gate | Pre-CI decision | Evidence required for upgrading |
|---|---|---|
| SOURCE_INTEGRATION_COMPLETE | PASS_SOURCE_TREE | PR17 files present + PR18 exact Blob SHAs + no source deletion |
| CODE_GATE / CODE_FREEZE | PENDING_FINAL_HEAD_CI | Latest branch CI: full pytest, QA, Team3 57+, Ruff, archive, machine inventory |
| CONTRACT_GATE | PASS_LOCAL_CANDIDATE | New regressions and existing fail-closed suites pass |
| DATA_INTEGRITY_GATE | PASS_MACHINE_ONLY conditional | 60 PDF hashes/pages + draft candidate / evidence matrix consistency; not semantic human review |
| PROVENANCE_GATE | BLOCKED | native source receipts and signed identity chain |
| GOLD_GATE | BLOCKED | verified original XLSX and immutable human-approved Gold |
| STUDIO_E2E_GATE | BLOCKED | authenticated complete C001/C013, B0/E1 E2E |
| B0_E1_COMPARISON_GATE | BLOCKED / NOT_MEASURED | same source PDF+config conditions+approved Gold |
| OVERALL_RELEASE_GATE | BLOCKED | all required live evidences and human approval |

**TEAM1_CODE_TASK_COMPLETE** may be PASS only on exact final-HEAD CI and evidence-preserving docs. **FULL_PRODUCT_RELEASE_READY=BLOCKED** until externally verified; do not approve merge or deployment.
