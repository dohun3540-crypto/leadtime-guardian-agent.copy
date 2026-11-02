# LeadTime Guardian — Team1 isolated parallel E2E readiness (2026-11-03)

**Owner:** Team1 구도훈. **Write scope:** `dohun3540-crypto/leadtime-guardian-agent.copy` only.  
**Protected frozen source:** PR #19, `feat/all-team-qa-final-freeze-20261103`,
exact SHA `5d3172deaeecafec0056b48c92f0f0f6bb08297a`.  
**New source branch:** `feat/team1-parallel-e2e-readiness-20261103`;
the new Draft PR targets the protected PR #19 *branch* as base.
**Read-only reference:** `dohun3540-crypto/yuseok_integration` Draft PR #2, observed
successful SHA `67b93291c1f32acaf43e45815d2d1119480b652a`:
[778 pytest, Ruff, 60 PDFs, exact-HEAD CI](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285).

No original Team2 operational source, Team3 PDF, Human Gold, Studio job/config,
or integration remote branch was written. Do not present archived replay or
synthetic local assertions as current Live/approved Gold.

## A. TEAM1_PARALLEL_DEVELOPMENT_REPORT — implementation inventory

| Existing feature (reused) | Location | Coverage / disposition |
|---|---|---|
| Strict JSON / numeric overflow | `qa.audit.load_json_strict`, `strict_json.loads_strict` | IMPLEMENTED; existing QA boundary retained |
| Native payload envelope | `qa.studio_contract.audit_native_envelope` | IMPLEMENTED; original Normalize 3-document contract retained |
| Release source inventory / SHA / path escape | `qa.release_inventory.audit_release_folder` | IMPLEMENTED; prerequisite, not reimplemented |
| Stage per-step original SHA / duplicate IDs | `qa.stage_trace.audit_stage_evidence` | IMPLEMENTED; release inventory already invokes stage intake |
| Studio-to-Python/QA complete offline flow | `scripts/qa_combined_e2e_check.py` | IMPLEMENTED, live authenticity EXTERNAL_EVIDENCE_BLOCKED |
| Cross-Agent+Provenance | `qa.cross_agent`, `qa.provenance_link` | IMPLEMENTED; no automatic Live authentication |
| B0/E1 manifest eligibility / field diff | `qa.experiment_compare` | IMPLEMENTED; improvement NOT_MEASURED without authentic Gold |
| PDF Inventory | `qa.inventory` | IMPLEMENTED (60/60 machine-only) |
| Candidate/XLSX review | `qa.review_records`, `qa.xlsx_snapshot` | IMPLEMENTED; Human approval EXTERNAL_EVIDENCE_BLOCKED |
| Multi-artifact receipt→PDF→Native+V6 join *before* full E2E | **new `qa.e2e_bundle_preflight`** | NEW, local-only, no provider or human authentication |

### New code vs existing capabilities

This Task adds a **single local cross-file join**, deliberately narrower than a
new E2E engine. The existing release inventory validates whether supplied byte
paths and SHA declarations can be read, while independent combined E2E requires
many valid inputs. The new checker can flag *contradictions in partially supplied
originals* without inventing unavailable intermediate records:

1. Reuse release inventory's verified local paths, SHA and Stage intake status.
2. Bind **three** source PDF filenames/SHA to operational and Independent QA
   Upload Receipt file sets, allowing legitimately different QA File IDs.
3. Bind original Normalize Native `metadata.job_execution_id` to the
   operational Job, and its `metadata.source_files` File IDs to operational
   receipt IDs (no false equality for QA separate Job).
4. Compare original Team2 `studio-provenance/1.export_sha256` against **actual
   Native raw bytes**, Job ID against Native release Job, reject self-asserted
   PDF verification. This is local source consistency only.
5. Accept an IndependentQA Native with a **verdict** content shape (not
   necessarily `{"documents":[]}`) if valid identity/JSON contract is present;
   optionally join its source File IDs to the QA receipt.
6. Reuse existing B0/E1 manifest readiness. Compare B0/E1 claimed PDF
   SHA sets against locally read original source PDFs; status remains
   `NOT_MEASURED` until independent authentic/human evidence exists.
7. Return machine-readable `missing_inputs`, `invalid_inputs`,
   `source_identity_conflicts`, `missing_stage_records`,
   `missing_qa_records`, `missing_team2_sidecar`,
   `missing_human_gold`, `next_required_action` and explicit false
   Live/Gold/Release gates. Output does **not** rewrite originals.

New owned files only:
- `src/leadtime_guardian/qa/e2e_bundle_preflight.py`
- `scripts/team1_e2e_preflight.py`
- `tests/test_qa_parallel_e2e_bundle.py`
- this isolated handoff doc

No additional package dependency. No changes to `src/leadtime_guardian/strict_json.py`,
`engine.py`, `studio_adapter.py`, `qa/`, `data/` or original PR #19.

## B. E2E_EVIDENCE_INTAKE_CONTRACT — receive and preflight

All actual raw files belong in a **private, non-versioned local folder**. Never
commit personal/reviewer data, access credentials, original undisclosed Native
or approved private Gold to a public integration repository.

Manifest contract: existing `leadtime-release-evidence/v1`, documented in
`docs/NINTH_RELEASE_VALIDATION_RUNBOOK_20261101.md`. Mandatory metadata:
`case_id=C001`, `operational_job_id`, `config_id`,
`config_version`, and `sources` with trusted relative paths.
Existing `qa.release_inventory` supports path or `{path,sha256}` values;
new preflight *only opens files that the inventory has hash-checked*.
The source roles are `purchase_order`, `delivery_notice`, `quotation`.

The receipt files use this *existing* interface:

```json
{"case_id":"C001","files":[
  {"filename":"SYN-C001_purchase_order.pdf",
   "file_id":"file_ACTUAL_ID","sha256":"ACTUAL_64_HEX"},
  {"filename":"SYN-C001_delivery_notice.pdf",
   "file_id":"file_ACTUAL_ID","sha256":"ACTUAL_64_HEX"},
  {"filename":"SYN-C001_quotation.pdf",
   "file_id":"file_ACTUAL_ID","sha256":"ACTUAL_64_HEX"}
]}
```

Placeholders above **are not valid Live evidence**. Upload Receipts must be
provider-grounded originals and PDF hashes checked against original local bytes;
equal filename/hash declarations alone never authenticate cloud upload.

Team2 Sidecar: `contract_version=studio-provenance/1`,
`export_sha256` of **original operational Native JSON bytes**,
`studio_metadata_supplied.job_execution_id`, business validation status,
and `evidence_verified_against_pdf=false`. Supply separately the true
Python Safety V6 output/result, code HEAD and reproducible run details.

IndependentQA Native: original content JSON and `metadata.job_execution_id`,
`metadata.step_run_id`; the QA Job may differ from the operational Job.
A real QA report + QA Input must be passed to the existing Cross-Agent/Stage
validator; the new preflight **does not claim to validate provider identity
or automatically parse the full IndependentQA report contract**.

Stage: existing `leadtime-stage-intake/v1` manifest plus original
Extract (3), MergeDocuments, NormalizeDocuments, IndependentQA Input and
Report with original Step IDs and SHA. Duplicate operational Step IDs or
conflicting supplied Job/Config metadata are rejected by existing functions.

Human Gold: original corrected `PDF_EVIDENCE_MATRIX.xlsx` bytes/SHA,
sheet name, typed cells, PDF page and field path, reviewer/approval time,
decision/state, immutable version, explicit team signoff. Candidate CSV/DRAFT
is never gold. Existing `qa.xlsx_snapshot` and `qa.review_records` must
run independently before official metrics can be computed.

### Run commands

```bash
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
python scripts/team1_e2e_preflight.py --manifest /private/evidence/release_evidence.json --json-report /private/results/team1_preflight_new.json
python scripts/qa_release_evidence_check.py --manifest /private/evidence/release_evidence.json
python scripts/qa_stage_intake_check.py --manifest /private/evidence/stage_manifest.json
python scripts/qa_combined_e2e_check.py --help
python scripts/qa_b0_e1_compare_check.py --help
python -m pytest -q
python -m ruff check .
```

Only execute Stage/Combined/B0-E1 on **actually existing** original evidence.
The `--help` entries above are safe reminders of their exact CLI contracts.
For the integrated tree the owner may use `python -m qa.integration --help`
then the production command in integration's
`docs/integration_20261102/NATIVE_AND_GOLD_REQUEST.md`.
For preflight, exit code **1 = malformed/conflicting**,
**2 = missing or only locally verified**; **there is deliberately no
exit-zero Live/Release mode**. Optional `--json-report` creates a new file
exclusively; reruns require a new filename. It will not overwrite source
manifests, Native, PDF or previous outputs.

### Provenance classifications

Use display labels `SYNTHETIC`, `OFFLINE_REPLAY`,
`STORED_NATIVE_HISTORY`, `AUTHENTICATED_LIVE`, `HUMAN_REVIEWED`,
`UNVERIFIED` only at the presentation/reporting layer.
Do **not** inject these into the existing operational provenance enum.
This preflight's sole verification scope is `LOCAL_SOURCE_BYTES_ONLY`.
`AUTHENTICATED_LIVE` and `HUMAN_REVIEWED` require independently verified
external evidence; this command can never grant either.

## C. CROSS_TEAM_COMPATIBILITY_MATRIX

| Subsystem | Required contract | Current proof | Conflict/decision |
|---|---|---|---|
| Team1 QA | `audit_release_folder(Path)`, native `audit_native_envelope`, `audit_b0_e1_readiness` | Baseline `af66a2d9` QA 467/whole 716 CI | New module imports stable functions, does not edit existing |
| Team2 V6 | `documents_from_export`, `analyze_studio_documents`, Sidecar `studio-provenance/1` | Source modules present, archived/local regression only | Actual same-run Sidecar and calculation remain EXTERNAL_EVIDENCE_BLOCKED |
| Team3 PDFs/Gold | `qa.inventory`, `qa.xlsx_snapshot`, `qa.review_records`, draft candidate | 60/60 machine PDF / 57 data tests | Latest corrected XLSX plus reviewer approval not supplied; no invented Gold |
| Integration PR #2 | strict `load_json_strict`, `release_inventory`, `studio_contract`, `experiment_compare` | Reference `67b93291` with 778 pytest/Ruff/60 PDF CI | New import surface compatible *by source signature*, runtime merged-tree test NOT_RUN |
| Studio live | original PDF upload/job/config/stage native chain | Historical V4 C001/C013 only | Stage receipt/provider auth and E1 pairing blocked |

**Exact Git Blob comparison** at protected personal / integrated HEADs:
- `release_inventory.py` **same** `fb8982edb23078cb98a333ac4f9c581ad219ef47`;
- `experiment_compare.py` **same** `0c0bbf2c38456019d891625e7486e379e1f96ecf`;
- `studio_contract.py` **same** `08b23233ce12575c1c18f654e3ae296b8efa3e7c`;
- `audit.py` **different intentionally**: personal `cdce35bfe3256d964695eae7164b2f034c3ead17`, integrated `8de0aaaf7b1911d361bd85c9b970d978a126daac` delegates to integrated hardened `strict_json.py` (`afa56a5f201af250eeb28a20580bd0188fe5cb51`). Do not overwrite either.

The new module only imports those existing APIs. No new imports from top-level
`qa/`, and no collisions with existing executable script/module names.
**Merge simulation status: STATIC_COMPATIBILITY_ONLY** until the integrated
owner runs the new tests in a disposable checkout of current PR #2.

## D. INTEGRATION_CHANGESET_MANIFEST

Target: integrated Draft PR #2 **through its maintainer only**,
do not push or merge remotely on this Team1 task.
The new Draft PR's **base is PR #19**, so the diff should consist *only*
of this isolated parallel readiness work; exclude old QA freeze files.
The exact source commit SHA, final files' Git Blobs and CI are recorded
in the new Draft PR body after source CI passes (avoids source self-hash
recursion).

Suggested selective transfer order:
1. Cherry-pick or file-copy only `src/leadtime_guardian/qa/e2e_bundle_preflight.py`.
2. Add `scripts/team1_e2e_preflight.py`.
3. Add `tests/test_qa_parallel_e2e_bundle.py`.
4. Copy this documentation only if relevant for integration handoff.
5. Run `python -m pytest -q tests/test_qa_parallel_e2e_bundle.py`,
   `python -m pytest -q`, `python -m ruff check .`, archive/local gate,
   Team3 PDF inventory and integrated Actions at its own new HEAD.

**NEVER cherry-pick or replace** personal `audit.py`,
`input_delivery.py`, `strict_json.py`, Team2 V6/Adapter/Engine,
Team3 `qa/` and original PDF/Gold/Natives or any other team's CI rules.

Classification: `READY_TO_CHERRY_PICK` only after personal exact-HEAD CI
success; `STATIC_COMPATIBILITY_ONLY` for integrated runtime before its
own isolated checkout; `EXTERNAL_EVIDENCE_BLOCKED` for current
Studio/Gold/official B0-E1.

## E. FINAL_REGRESSION_REPORT / release gates

**Historical protected baseline:** individual PR #19
[716 full/467 QA](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821541)
and [57 Team3/60 PDFs](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704)
at `5d3172deaeecafec0056b48c92f0f0f6bb08297a`, both SUCCESS.

**New feature branch:** only exact final HEAD and its independent workflow logs
establish the new regression PASS; see the Draft PR body after CI. Test
counts are not additive; new local synthetic tests are included in the full
suite. No skipped or removed baseline tests should be accepted.

Gate decisions:
- `PERSONAL_CODE_FREEZE=PASS` (PR19 source unchanged)
- `TEAM1_PARALLEL_TASK_COMPLETE=PENDING_FINAL_EXACT_HEAD_CI`
- `INDEPENDENT_QA_GATE=PASS_BASELINE` (new branch subject to CI)
- `CROSS_AGENT_CONTRACT_GATE=PASS_LOCAL_ONLY`
- `E2E_INTAKE_READY=PASS_LOCAL_CANDIDATE` (receipt/Native/sidecar join)
- `B0_E1_EVALUATION_READY=PASS_CONTRACT_ONLY`, improvement NOT_MEASURED
- `GOLD_INTAKE_READY=PASS_EXISTING_TOOLS_ONLY`, approval PENDING
- `CROSS_TEAM_COMPATIBILITY_GATE=STATIC_COMPATIBILITY_ONLY`
- `REGRESSION_GATE=PENDING_EXACT_HEAD_CI`
- `INTEGRATION_CHANGESET_READY=PENDING_FINAL_EXACT_HEAD_CI`
- `STUDIO_LIVE_VERIFIED=BLOCKED`
- `HUMAN_GOLD_APPROVED=PENDING`
- `FULL_PRODUCT_RELEASE_READY=BLOCKED`

**Final next action:** wait for real outputs only as needed for actual live
validation, not for this independent local code readiness. Keep all original
bytes, upload receipts and approved Gold private; explicitly preserve PASS_LOCAL
versus Live and human-reviewed verdicts.
