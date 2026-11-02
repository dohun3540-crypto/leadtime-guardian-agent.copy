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


---

## 7. Team1 private QA deep audit addendum (2026-11-02, PR #19)

### Exact working scope
This addendum supersedes the **pre-CI decision** and baseline information in section 6 only for the private Team1 QA audit. The only writable repository was `dohun3540-crypto/leadtime-guardian-agent.copy`; `dohun3540-crypto/yuseok_integration`, original `leadtime-guardian-agent`, both mains, and PR #15/#17/#18 stayed read-only. Continue PR #19, do not start a new PR.

Starting exact HEAD `955a3c5e247aa2771498a3c48b8f21350c9bdcd6` was independently verified Draft/Open, unmerged, mergeable with two successful GitHub Actions:
- [QA 41461412396](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41461412396): whole 704, QA 455, Ruff pass, local gate BLOCKED.
- [Team3 41461412385](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41461412385): Team3 57, original PDF 60/60, hash duplicates 0.

### Reproduced, scoped code defects

First wrote regression tests to pre-existing Team1 files `tests/test_qa_independent.py` and `tests/test_qa_studio_batch.py`. The **failing test-only checkpoint** [GitHub Actions 41463094361](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41463094361) on `bdca9eac21bbb8f7d73fbcecaad94e0da20c7dbc` reported **10 failed / 456 passed** in QA-only pytest: the failures demonstrated actual unhandled exceptions and silent data conversion, not a regression caused by production-code changes.

1. `audit_provenance({"provenance": []})` and dictionary/list variants raised `TypeError: unhashable type` while testing frozenset membership instead of returning `UNKNOWN_PROVENANCE` with `qa_status=FAIL`.
2. `audit_studio_case_batch` with user-reported `provenance_level` supplied as list/dict raised the same exception instead of rejecting an invalid source.
3. `audit.load_json_strict` used the default Python float parser, accepting `1e999` or `-1e999` as infinities, and converting nonzero `1e-9999` or `-1e-9999` to 0.0; a nested JSON number was likewise accepted.

**Minimal scoped fixes**, no Team2 source/Team3 data rewrite:
- `src/leadtime_guardian/qa/audit.py`: type-check the provenance vocabulary before frozenset membership; reject JSON floating-point overflow/nonzero underflow by testing its decimal original before accepting the parsed finite Python float. Oversized exponent strings producing `decimal.InvalidOperation` are converted to deterministic `ValueError` rather than leaking parser internals.
- `src/leadtime_guardian/qa/studio_batch.py`: type-check `provenance_level` before allow-list membership and emit existing `UNVERIFIED_BATCH_OBSERVATION_SOURCE` as a fail-closed error.
- Existing `tests/test_qa_independent.py`: parametrized invalid provenance, exponent overflow, nonzero underflow, excessively long exponent, and valid finite/explicit zero compatibility.
- Existing `tests/test_qa_studio_batch.py`: test list/dict observation provenance rejection.
- No test removed, skipped, downgraded, no required metadata newly made mandatory, no Studio Live claim invented.

### Data and execution-contract audit

Using repository source text and previously verified PDF inventory:
- C001: candidate source SHA entries matched its manifest and 40-row evidence matrix under the existing 5 source-consistency tests; purchase/notice 100 EA vs quote 60 EA, price decimal-string `1000.00`, shipping `500` KRW retained. All approval fields in the candidate remain unreviewed.
- C013: DRAFT PO `PO1`, delivery notice `PO999`, quote `PO1`, deliberately inconsistent; do NOT autofix or claim current live Studio error detection from DRAFT.
- C008: DRAFT purchase receipt R1 40 EA + R2 60 EA, and notice changes only R2 60 EA; distinct allocation and transport roles, no duplicate receipt counting.
- C017: DRAFT fields stored normalized ISO date strings; any localized Korean date extraction is an input contract concern and cannot be reported as independently validated live.
- Original 60/60 PDF machine checks verify SHA/structure, not PDF field accuracy, independent reviewer approval or authenticated Upload receipts.
- User-reported B0 C001 one-file Job triplet remains `INVALID_SPLIT_JOBS`; separately running IndependentQA is normal and should not be rejected just because its Job differs.

### Known external / other-team boundary

`src/leadtime_guardian/strict_json.py` belongs to Team2 and was deliberately not changed. Its current default float parsing combined with `validate_json_value` rejects **infinite overflow** but may still treat a nonzero extremely small exponent as zero. This is a **proposed Team2 contract follow-up**, not a claim of a changed or failed Team2 engine. Team1's own `audit.load_json_strict` now explicitly prevents both nonfinite overflow and nonzero underflow. Existing JSON integer and finite float behavior remains intact.

There is **no claim of actual provider live Step/Job authentication, B0/E1 numerical measurement, original latest reviewed XLSX approval or human Gold**. Preserve original source and log all external evidence requests in `docs/FINAL_STUDIO_GOLD_HANDOFF_20261103.md`.

### Final checks and freeze criteria

Because source changes followed the baseline 704-pass CI, a new exact-HEAD GitHub Actions success is mandatory before `CODE_FREEZE_CONFIRMED=PASS`. The final commit SHA, counts, CI URLs and evidence-based final decisions are recorded in **PR #19 body**, not embedded recursively into this file. Keep a Draft PR; `OVERALL_RELEASE_GATE=BLOCKED` even if local code tests pass.


---

## 8. Phase A–G final read-only E2E and separate integration sync audit (2026-11-02)

### Governance and actual execution

**Only this .copy Draft PR #19 is writable.** `dohun3540-crypto/yuseok_integration` PR #2 and original operational repo remained entirely read-only. This audit did not access or change Studio settings, make paid requests, alter source PDFs or Human Gold, submit to LMS or merge existing PRs. QA source and tests were not changed because no *new* defect in the frozen personal QA branch was reproduced. Historical CI failures from the other repo are not evidence of a current failure in the personal branch.

### Verified personal baseline and exact evidence

Personal HEAD before this documentation-only update: `af66a2d9c1b093558c3e7dc534ecbe66621d2657` (PR #19, Open/Draft/Unmerged, mergeable).
- Personal [whole Python + Independent QA run 41463679425](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41463679425) **SUCCESS**, 716 full / 467 Independent QA (subset), QA/global Ruff PASS, archived C001 PASS_LOCAL, local gate checks true and overall BLOCKED.
- Personal [Team3 data run 41463679568](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41463679568) **SUCCESS**, 57 Team3 tests (subset of 716), 60/60 original PDF machine inventory PASS, duplicate hashes 0, archive SHA `a3f4ed1cefee4ebea3a4b94f9408f8a039bf042bd651a3a9222a5162c22149dc`.
- Historical PR19 704→716 improvement was already verified, no additional tests or source edits were needed in this audit.

### Separate integration PR #2: failure, repair and latest observed passing checkpoint

This audit found the integration repository had progressed since the previous handoff:
1. Red test-only [run 41464204131](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41464204131) at `d6a43083b61bb89b798b80951e3bc5a25b23842a`: **757 passed / 8 failed** on unhashable QA provenance and nonzero JSON underflow.
2. Newer [run 41464886852](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41464886852) at `4874f7b680d84e4916da0cde9cac57bf2dee04cb`: failed **Ruff F821** in `tests/test_qa_studio_batch.py:172` (pytest referenced without import); it stopped before full pytest.
3. **LATEST CHECKPOINT OBSERVED IN THIS AUDIT:** PR #2 exact HEAD `5a7d4df070a7607585b5c1adb4847a1b79f8c2e7`; [integrated run 41464994396](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41464994396) **completed SUCCESS**, full pytest **778 passed**, repository Ruff PASS, PDF inventory 60/60 PASS with the same source archive hash. The earlier red states are historical and not the latest observed result. PR #2 remained Open/Draft/Unmerged and mergeable at this checkpoint.

The integration repository **already incorporated the essential personal QA fixes**, by code functionality rather than copying every Git Blob:
- `src/leadtime_guardian/qa/studio_batch.py`: blob **identical**, `ca9e1cda63fa5413379d8c4f2bae6e2d6241f7b1`.
- `src/leadtime_guardian/qa/audit.py`: intentionally different, integration blob `8de0aaaf7b1911d361bd85c9b970d978a126daac`, personal `cdce35bfe3256d964695eae7164b2f034c3ead17`. Both reject unhashable provenance. Integration delegates JSON to fixed shared `src/leadtime_guardian/strict_json.py`, blob `afa56a5f201af250eeb28a20580bd0188fe5cb51`, which rejects overflow and nonzero underflow. Personal QA keeps its own strict parser, and Team2's original parser remains untouched in .copy.
- `src/leadtime_guardian/qa/input_delivery.py`: intentionally different (`f838759de7f188b1330a3c93a466f8cfab344e2a` integration vs `f56825a1a6202cc468e1f86c059b0d8dffa6e8de` personal). Integration's recursive typed JSON comparison preserves strict key/type validation including signed zero, instead of .copy's canonical JSON comparison; new integration tests passed. Do not blindly overwrite this integration-specific hardening with the personal blob.
- `tests/test_qa_independent.py`, `tests/test_qa_studio_batch.py` differ because the integration repository contains additional invalid-type checks; all current integrated tests pass.
- Comparison of the two Git trees: unchanged exact Git Blob SHAs for **5/6** core Team2 files; only integrated `strict_json.py` intentionally differs. C001/C013 original manifest, C001 archived V4 native and original C001 AI Candidate/Evidence Matrix blobs match exactly. No `data/cases/SYN-C0*` path diff observed. Personal QA and integration differ in just **2 QA source paths**, both intentionally and safely covered by passing integration CI. No new copy-to-integration cherry-pick is authorized or needed.

**INTEGRATION_SYNC_GATE = PASS_CODE_LOCAL at observed integrated exact HEAD**, not automatic permission to merge both PRs or infer live interoperability; repeated checks should use the current integration PR HEAD if it later moves.

### Source data and historical Stored Native available

- C001: unchanged machine-verified three synthetic source PDFs; purchase/notice 100 EA vs quotation availability 60 EA are different roles; unit price `1000.00` KRW/EA and shipping `500` KRW once per quotation preserved; 40-row Evidence Matrix remains **PENDING human review**.
- C013: DRAFT has PO1 versus delivery notice PO999; archived user-owned `SYN-C013_quotation_NormalizeDocuments (1).json` was located in ChatGPT Library, originally uploaded 2026-10-30. Its stored Native object lists **three documents** (purchase, notice, quotation) and three `metadata.source_files` with file IDs, a single historical operational Job ID and a Normalize Step ID. Its `content` includes the PO conflict warning but has empty `evidence` arrays. **This is not an authenticated current B0/E1 chain**: full saved Config/version, original cloud upload receipts, source-PDF-bytes-to-file-ID hashes, QA raw input/report, V6 sidecar, independent Gold and new E1 comparator are absent. Stored Native is read-only historical evidence; no automatic business block or new live success is claimed.
- C008: stored DRAFT receipt R1=40 EA and R2=60 EA, notice affects only R2; independent Python allocation and shipping are tested locally, not from a new Studio run.
- C017: stored DRAFT ISO-normalized dates; Korean-language date-to-ISO source extraction requires authentic Studio source evidence before declaring live success.
- 60/60 original source PDF machine checks show structural integrity and hashed bytes, **not** field-by-field original PDF human truth.
- Library inventory contained job-list XLSX exports but **no `PDF_EVIDENCE_MATRIX.xlsx` original**; the latest corrected human-reviewed spreadsheet and approval records remain unavailable in the checked connected Library/GitHub sources. Never substitute a job-list XLSX or `AI_CANDIDATE` for an approved Gold source.

### Studio / Python V6 / Cross-Agent / release readiness

The archived C001 V4 Native and C013 Stored Native, local Safety V6/QA offline regression and the operational Job summaries are distinct evidence origins. No verified current B0/E1 pair of three-PDF originals with upload SHA, config version, stage IDs, matching V6 sidecar, QA raw report and approved Gold was found. The prior B0-C001 file-specific three Job observation remains **INVALID_SPLIT_JOBS**; a historical stored three-document Native does not retroactively authenticate a new B0/E1 run. Independent QA can legitimately have its own separate Job, but must explicitly bind to operational source bytes.

Evidence gating:
- `TEAM1_CODE_TASK_COMPLETE` **PASS**; `TEAM1_INDEPENDENT_QA_GATE` **PASS_LOCAL**; `CODE_FREEZE_CONFIRMED` **PASS** with exact-head CI.
- `INTEGRATION_SYNC_VERIFIED` **PASS_CODE_LOCAL** for observed integration PR #2 `5a7d4df` / CI #41464994396.
- `DATA_INTEGRITY_GATE` **PASS_MACHINE_ONLY**; `PROVENANCE_GATE` **BLOCKED_LIVE**; `STUDIO_E2E_GATE` **BLOCKED**; `PYTHON_V6_LIVE_GATE` **BLOCKED**; `GOLD_APPROVAL_GATE` **PENDING**; `B0_E1_COMPARISON_GATE` **NOT_MEASURED**; `OVERALL_RELEASE_GATE` **BLOCKED**.
- `TEAM1_E2E_VERIFIED` **NOT_VERIFIED** and `FULL_PRODUCT_RELEASE_READY` **BLOCKED** despite two successful code lines.
- On arrival of authentic evidence, follow existing `docs/FINAL_STUDIO_GOLD_HANDOFF_20261103.md` and the integration-side `docs/integration_20261102/NATIVE_AND_GOLD_REQUEST.md` and `python -m qa.integration` contract. Do not create synthetic Live/Gold files to satisfy tests.

No additional Team1 QA source fix was reproduced; this is a **documentation and read-only evidence audit**, not new feature development. The latest .copy PR #19 HEAD after this documentation update must be checked against its own two GitHub Actions before reaffirming code freeze.
