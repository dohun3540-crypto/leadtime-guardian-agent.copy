# LeadTime Guardian — Cross-Team Selective Integration Handoff
**Team1 구도훈 · 2026-11-03 KST**. Destination is **READ-ONLY during this task**.

## 1. Destination and protected baselines

Source repository: `dohun3540-crypto/leadtime-guardian-agent.copy`.
Source final branch: `feat/team1-final-e2e-release-audit-20261104`; new **Draft PR #22** base `feat/team1-e2e-final-hardening-20261103` (protected PR21 SHA `edab2040430e2159399ee61073fe70e5bdf6cba2`). Protected PR19 SHA `5d3172deaeecafec0056b48c92f0f0f6bb08297a`, PR20 SHA `53ae1a7dbe53be38a7d585676c2b2d037534fb46` must remain unchanged.

Destination repo: `dohun3540-crypto/yuseok_integration`, Draft PR #2, last observed SHA `67b93291c1f32acaf43e45815d2d1119480b652a`; [existing 778 tests + Ruff + PDF 60 machine CI](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285). **Recheck destination HEAD immediately before importing.** Existing PR #2 does not contain the new Team1 preflight module, CLI, or tests.

## 2. Minimal file-copy manifest (do not blindly merge full branch)

Transfer in this order into a **disposable clone of the integrated PR2 code tree**; original PR20's new paths must come along because PR22's diff alone contains only revisions.

| Order | Final destination path | Definitive Git Blob SHA | Source |
|---:|---|---|---|
| 1 | `src/leadtime_guardian/qa/e2e_bundle_preflight.py` | `9fa51ce0d41467fb7618fd9dbf00075c61c38d3c` | latest PR22 hardened source |
| 2 | `scripts/team1_e2e_preflight.py` | `7968fffbe93be4e67175baa09786dccbe751cdde` | PR20 unchanged CLI |
| 3 | `tests/test_qa_parallel_e2e_bundle.py` | `429bc6f45bdfc63dbaee11d7aed9c30c0df9d94a` | latest PR22 expanded synthetic tests |
| 4 | `docs/team1_parallel_readiness_20261103/README.md` | `56dea32f35f9d9d6de06bc7bab921b376f24277b` | optional PR20 original protocol |
| 5 | `docs/team1_final_hardening_20261103/` | use immutable PR21 files | optional previous hardening evidence |
| 6 | `docs/team1_final_release_audit_20261104/` | use PR22 files | final audit, data/contract matrix, Gate |

Import from the actual GitHub file bytes associated with the specified source Blob/branch; do not reconstruct from chat fragments or rename source files. Original all-Team PR19 QA files must **not** be recopied to integration.

### Protected integrated core — compare hashes before and after

- `src/leadtime_guardian/qa/release_inventory.py` `fb8982edb23078cb98a333ac4f9c581ad219ef47`
- `src/leadtime_guardian/qa/studio_contract.py` `08b23233ce12575c1c18f654e3ae296b8efa3e7c`
- `src/leadtime_guardian/qa/experiment_compare.py` `0c0bbf2c38456019d891625e7486e379e1f96ecf`
- `src/leadtime_guardian/qa/audit.py` **integrated** `8de0aaaf7b1911d361bd85c9b970d978a126daac` — intentionally **not** personal copy.
- `src/leadtime_guardian/strict_json.py` **integrated** `afa56a5f201af250eeb28a20580bd0188fe5cb51`; preserves nonzero underflow/overflow strictness.
- `src/leadtime_guardian/qa/input_delivery.py` **integrated** `f838759de7f188b1330a3c93a466f8cfab344e2a`; preserves signed-zero/type comparison.
- `qa/inventory.py` **integrated** `6bdb6f6d710066e491451bdc21c6233a5965a19d`; team3 original safe inventory.

**NEVER replace** the above hardened files, Team2 calculation engine, Studio Adapter, Team3 PDF archive/Data/Gold, private Native/Upload Receipt, `.github/workflows`, main or old PRs. No dependencies or schema migrations are needed for the Team1 added files: `e2e_bundle_preflight` imports `qa.audit.load_json_strict`, `qa.release_inventory.audit_release_folder`, `qa.studio_contract.audit_native_envelope`, `qa.experiment_compare.audit_b0_e1_readiness`, which exist at destination. A true runtime merged-tree smoke test is **still required**.

## 3. Isolated integration validation — required, NOT performed here

The private integrated source could not be downloaded into this task's container (`Could not resolve host: github.com`). Static inspection found no matching destination filenames/path collisions, and the three validator blob dependencies matched. This does **not** prove imports/pytest/ruff of the merged tree. The integration maintainer should run:

```sh
# in a disposable, permissioned checkout of the latest integrated PR2
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_parallel_e2e_bundle.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
python -m qa.inventory --root . --out /private/new-unique-inventory-output
# Use the existing Archive/Local Gate commands already configured in PR2 CI
python scripts/team1_e2e_preflight.py --manifest /private/evidence/release_evidence.json --json-report /private/results/unused-new-name.json
```

Do not assume total `778 + 37` or similar without **actual merged test collection**. Record destination new HEAD, tests collected/failed/skipped, exact GitHub Actions run IDs, file/blob SHA invariants, PDF archive SHA and the Stage/C001/Local Gate result. A valid preflight without authenticated Live evidence intentionally exits **2** (BLOCKED), and malformed/conflicting input exits **1**; neither is a release PASS.

## 4. Distinct Team2/3/4 obligations

- **윤현준 (Team2)** — provide original exact input Native bytes, Job+Step/Config identity, Safety V6 calculation output, engine source SHA, reproducible command, `studio-provenance/1.export_sha256` bound to those original bytes. Preserve calculation, Adapter, strict parser and quote shipping semantics.
- **김민주 (Team3)** — provide latest corrected `PDF_EVIDENCE_MATRIX.xlsx` **original bytes** and SHA, real human-reviewed field/page references, reviewer timestamps/decisions/approval, Gold freeze state/version. Candidate/DRAFT fields are not human Gold.
- **구도훈 (Team1)** — use current Preflight for local missing/mismatch reports, Stage/Native original SHA, Independent QA original Input/Report, Cross-Agent+Release gate, only then B0/E1 measured comparison. Preserve separate operational and QA Jobs.
- **Fourth teammate** — presentation and demo evidence alignment; do not claim a real case demonstration using archived synthetic replay alone.

## 5. Required original Live evidence

For **B0/E1 × C001/C013** receive complete original PDF uploads and provider receipts, SHA, Agent/Config/Version, each distinct Job ID and Extract three branches / Merge / Normalize Step IDs & original outputs, actual QA Input+Report, same-Native V6 Sidecar and approved Gold. Original C001 V4 Archive or older C013 stored three-document Native is useful as historical local evidence, **not** substitute for a new exact-run authenticated chain. Three individual one-PDF Jobs are **not** a valid single operational three-PDF Job. Same PDF hashes across B0/E1 are required for fair comparisons; distinct experiment Config/Job are allowed. Do not invent improvements or approval.

## 6. Concrete integration exit gates

`PATH_COLLISION=NONE_STATIC`; `IMPORT_CONTRACT=STATIC_ONLY`; `DEPENDENCIES=NO_NEW_PACKAGES`; `MERGE_SIMULATION=NOT_RUN_NETWORK_RESTRICTED`; `INTEGRATED_FULL_REGRESSION=NOT_RUN_AFTER_OVERLAY`; `DESTINATION_EXISTING_CI=PASS_HISTORICAL_778`; `PERSONAL_CODE_FREEZE=PASS`; `GOLD_APPROVAL=PENDING`; `LIVE_STUDIO_VERIFICATION=BLOCKED`; `OFFICIAL_B0_E1_METRICS=NOT_MEASURED`; `OVERALL_RELEASE=BLOCKED`.

**Request from maintainer:** deliver back the exact integrated overlay SHA, merged-tree regression logs and first authentic operational/QA/V6/Gold original evidence package. PR22 remains Draft; no remote commit to integration is authorized by this Task.
