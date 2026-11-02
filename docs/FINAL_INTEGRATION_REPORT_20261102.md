# LeadTime Guardian — 2026-11-02 Independent QA final integration candidate

**Owner:** Team 1 / 구도훈. **Mode:** source-preserving GitHub integration, not Studio deployment.
**Repository:** `dohun3540-crypto/leadtime-guardian-agent.copy`
**Branch:** `feat/final-qa-cross-agent-integration-20261102`
**Base immutable commit:** `ece3a7dcc254b5c7a14c72792750170346419eb8` (Draft PR #15)
**Final head:** obtain from current branch/PR; do not treat this self-referencing document as a final SHA.

## Baseline evidence (actual GitHub reads on 2026-11-02)

| Source | Repo | PR | Actual HEAD | Scope |
|---|---|---:|---|---|
| Python Safety V6 | original | #12 | `e9b9992b593a42d427ff1bbadeb9a9866ca593bd` | operations, adapter, provenance |
| Gold/evaluation candidate | original | #13 | `a925103077173b37d1cefcd6a9576ae644dc2040` | inventory, XLSX snapshot, human review templates |
| selective consolidated QA | .copy | #15 | `ece3a7dcc254b5c7a14c72792750170346419eb8` | QA + Cross-Agent + Stage + local gate |
| parallel strict JSON | .copy | #16 | `d244d6a791600b8f6ea23097fe88f6ca50834a2b` | JSON equality-only alternate branch |

At PR #15 exact HEAD, GitHub Actions run [41310379906](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41310379906) passed: **630 full Python tests, 441 independent QA tests, QA Ruff, repository Ruff**. The 441 are included within 630, not additional independent tests. Local conservative gate remained **BLOCKED**. PR #16 [41310353744](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41310353744) also succeeded on its own diverged head. Team2 [41265874061](https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41265874061) and Team3 [41374031831](https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41374031831) showed completed/success but this is branch-local CI, not combined production authentication.

### Collision and selective integration decision

PR #15 and PR #16 have **diverged** from merge base `585142e718b444cbbd3c2b5e42d68637450`. Git compare PR #15 -> PR #16: ahead 3, behind 11. PR #15 already rejects tuple/list promotion, integer JSON map keys, bool/int and int/float cross-type equality, invalid JSON primitives and duplicate document IDs using `_is_strict_json_tree` plus canonical serialization. **Do not wholesale merge/cherry-pick PR #16** or remove PR #15 protections. PR #15 additionally handles known lowercase Studio issue severities and explicit null workflow_version for triage only.

Existing `studio_batch.py` and tests already reject three separately completed PDFs/Jobs as one integrated B0 C001. Do not duplicate that module or relabel split B0 Jobs as an integrated C001 case.

## Newly implemented QA hardening in this branch

**Only Team1-owned code and synthetic tests:**
- `src/leadtime_guardian/qa/experiment_compare.py` rejects duplicate `file_id` across a run's three claimed source PDFs with `DUPLICATE_SOURCE_FILE_ID` (FAIL).
- Same module rejects duplicate operational `step_run_id` among Extract / MergeDocuments / NormalizeDocuments and conflicting optional `job_id`, `config_id`, `config_version` on those operational steps (FAIL). IndependentQA may execute in a separate QA job, so it is not incorrectly forced to share the operational job's IDs.
- The local-only B0/E1 normalized field diff is now case-bound to the **already-established identical manifest case_id**, permitting C013 local comparison without changing `NOT_MEASURED`, `studio_comparison_authenticated=false`, or release denial. A C001 result cannot be joined into C013.
- `tests/test_qa_experiment_identity_hardening.py` adds 9 synthetic regression cases for these boundaries, including preservation of distinct QA-job metadata.

These changes **do not** generate new Studio Jobs, invoke payable APIs, modify calculation/engine modules, manipulate PDF/Gold labels, or turn local equality into provider certification.

## Roles and contract status

- **Team2 / 윤현준:** `src/leadtime_guardian/engine.py`, `agents_api.py`, `studio_integration.py`, `studio_adapter.py`, `provenance.py`, `strict_json.py`. No source changes in this branch. Prior PR #15 already integrated a compatible Team2 source snapshot; new Live Sidecar and current real Studio result remain unverified.
- **Team3 / 김민주:** original repo PR #13 includes inventory, C001 Gold **candidate**, reviewer CSV validation and XLSX snapshot tools. Its 2026-11-02 `docs/member3_migration_20261102/STATE.json` explicitly reports `frozen_gold=false`, `team_approved=false`, `xlsx_sha256=null`, `official_accuracy=null`; do not promote candidates or claimed reviewed XLSX to confirmed Gold. No original source PDFs or labels modified.
- **Team1 / 구도훈:** Independent QA, Cross-Agent, Stage/Batch contracts, evidence inventory, comparison guardrails and release reporting. Existing gates retained; new scope is the manifest identity hardening above.

## Test, CI and provenance limitations

Run from exact integration branch HEAD with Python 3.11 and existing project dependencies:

```bash
python -m pip install -r requirements-agents.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_experiment_identity_hardening.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
```

The CI on the **new branch's final HEAD** must be checked independently and the exact test totals copied from its job logs. PR #15 baseline results must not be recast as new-branch results.

The existing read-only release sequence remains: evidence inventory -> stage-intake -> combined E2E/Safety V6/Independent QA/Cross-Agent -> Team2 PDF/provenance-link -> B0/E1 comparison (when truly paired) -> Team3 human Gold evaluation. See `docs/NINTH_RELEASE_VALIDATION_RUNBOOK_20261101.md` for exact tested command examples. All new measured claims require original Native and independent source receipt evidence.

## Current release blockers

1. New B0-C001 evidence was reported as separate per-PDF Jobs; not a single three-document operational result. Historical archived C001 V4 is not a new B0/E1 success.
2. Current B0/E1 C001/C013 original job/step/config/raw Native, QA inputs and reports, PDF SHA/operational+QA upload receipts, and Team2 actual Sidecar not authenticated as one coherent run.
3. Team3 latest reviewed XLSX original bytes and semantic validation/approved immutable Gold are not in the known repo proof. No measured extraction quality or B0/E1 improvement.
4. New branch CI and latest HEAD are reported separately after GitHub Actions completes. Never infer from previous branch logs.

**Decision:** code-only candidate, not approved deployment. No merge, force push, Studio reexecution, purchasing or email dispatch. See `docs/FINAL_RELEASE_GATE_20261102.md` for final status matrix.
