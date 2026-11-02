# LeadTime Guardian — all-team selective source integration

Date: 2026-11-02 (KST)

## Source anchors
- Original Team 2 PR #12 HEAD: `e9b9992b593a42d427ff1bbadeb9a9866ca593bd`.
- Original Team 3 PR #13 HEAD: `a925103077173b37d1cefcd6a9576ae644dc2040`.
- Copy PR #15 stable base: `ece3a7dcc254b5c7a14c72792750170346419eb8`.
- Protected original branches, existing PRs and both main branches are read-only for this effort.
- Team 3 code is imported selectively, not via PR #13 wholesale merge or cherry-pick.

## Team-based code integration
- Team 1 (구도훈): preserve `src/leadtime_guardian/qa/` independent QA, Cross-Agent handoff, Studio adapter and provenance.
- Team 2 (윤현준): preserve `src/leadtime_guardian/{engine,studio_adapter,studio_integration,strict_json,provenance,agents_api}.py` as-is; all six Git Blob SHAs match original Team 2 PR #12 at the parent SHA.
- Team 3 (김민주): import `qa/` inventory, review CSV validator, read-only XLSX snapshot, C001 evidence candidate, templates, handoff reports, `tests/qa/`, migration files, and an isolated CI workflow.
- `qa/` and `src/leadtime_guardian/qa/` have distinct Python import names. A targeted smoke test checks both packages and the non-promotion of unreviewed Gold.
- Original `data/cases/` files (including C001 PDFs and C002-C020 archive) are not changed by this integration.
- PR #16 is a parallel branch; identical strict JSON features are retained from copy PR #15 without merging PR #16.

## CI strategy
- Add Team 3 workflow for this isolated integration branch and its Draft PR.
- Add `qa/requirements.txt` dependencies (pypdf/openpyxl/defusedxml) to existing Independent QA workflow.
- Assess full pytest, Ruff, archive replay, local gate and Team 3 inventory on the final integrated HEAD; do not conflate with parent PR #15's previous 630/441 passes.

## External evidence and release limits
- No new Studio/Agents API live jobs, payment, PDF upload, or external purchase.
- C001 old Studio V4 offline replay is not a newly authenticated 3-PDF B0 job; prior three single-PDF jobs cannot pass single-case B0 gate.
- Actual E1 native raw input/output, authenticated three-document B0, Studio Step ID receipts, PDF SHA matching, human-approved Gold and quantitative improvement are not established here.
- `qa/gold_candidates/SYN-C001/candidate.v1.json` remains `AI_CANDIDATE`, `human_reviewed=false`, `team_approved=false`, `gold_frozen=false`.
- The latest human review XLSX is not in this GitHub branch; its original bytes must be checked separately.
- Code integration does not constitute Release approval or authorization to merge to main.

## Gate accounting
For a machine-readable, final-SHA code-vs-live assessment see `docs/FINAL_ALL_TEAM_INTEGRATION_GATE_20261102.json`. The final GitHub Actions result must be checked against the exact head commit before assigning LOCAL_INTEGRATION_VERIFIED.

## 2026-11-02 — GitHub Actions verification at source integration commit

The GitHub-reported checks below ran against **exact SHA `1054a2e2d9b0900c75ea28694ca5a1c6f93c91b7`**, not parent PR #15:

| Verification | Result | Run |
| --- | --- | --- |
| Full Python `pytest -q` | **690 passed** | [Independent QA #41456845894](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41456845894) |
| Team 1 independent QA tests | **441 passed** (included in full) | Same CI |
| Team 3 exclusive `tests/qa` | **57 passed** (included in full) | [member3 #41456815208](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41456815208) |
| New cross-team smoke tests | **3 passed** (included in full) | Full CI |
| Ruff (entire repository + Team 1 + Team 3) | **PASS** | Both runs |
| Team 3 original PDF hash/structure inventory | **60/60 PASS** | member3 #41456815208 |
| Stored C001 V4 archive, native envelope, offline replay | **PASS_LOCAL** | Independent QA CI |
| Local integration evidence gate | `local_checks_passed=true`; `overall_status=BLOCKED` | Independent QA CI |
| Actual three-PDF single B0 Job + native E1 | **NOT_VERIFIED** | No new Studio Job |
| Human-reviewed and team-approved Gold | **PENDING** | Actual source XLSX and review approval missing |

GitHub recursive-tree comparison confirmed **25/25 original Team 3 text data/code/test/docs Blob SHA matches**; the remaining original workflow YAML was intentionally adapted to the new branch. All six Team 2 core operational Blob SHAs match original PR #12, and no original operational, PDF/data cases, or Team 1 QA source file was modified. There are 29 changed files in the initial source integration commit.

### Scope distinction
**SOURCE_INTEGRATION_COMPLETE=PASS (selected source components).**
**LOCAL_INTEGRATION_VERIFIED=PASS (Python/QA/CI/local stored replay).**
**REAL_STUDIO_E2E_VERIFIED=NOT_VERIFIED.**
**HUMAN_GOLD_APPROVED=PENDING.**
**OVERALL_RELEASE_READY=BLOCKED.**

PR #16's strict-type protections are already supplied by PR #15's `_is_strict_json_tree` and canonical typed comparison. Its parallel replacement was not merged.

The local gate prints `python_ci_at_current_sha=NOT_RUN` and `independent_qa_ci_at_current_sha=NOT_RUN` because the local runner cannot query GitHub's run conclusion. Those are limitations of the local script, **not** claims that the external CI did not execute. The separate GitHub run records above establish successful CI at the source integration SHA.

The documentation checkpoint described below was independently checked against its exact commit SHA. Later documentation-only updates also require fresh CI on the new HEAD; do not recursively commit each new HEAD SHA into this file.

### Remaining owners and priorities
- **P0 · 구도훈:** Recover actual integrated 3-PDF C001 B0 single Job, original Normalize and independent QA raw reports with matching Agent/Config/Job/Step/PDF SHA provenance; previous 3 distinct Jobs are NOT valid.
- **P0 · 윤현준:** Supply native live Studio-to-Python V6 sidecar and evidence-bound execution matching the same C001 B0, then C013/C017/C008. Existing offline replay is not live proof.
- **P0 · 김민주:** Check latest actual source XLSX bytes, PDF field grounding and reviewer approvals before Gold promotion. Candidate status stays AI_CANDIDATE.
- **P1 · 구도훈 + 윤현준 + 김민주:** After all three evidence streams exist, execute a new authenticated B0→E1 comparison, verify release Gate, and request human authorization before any production merge.

## Verified subsequent documentation checkpoint (distinct from original source integration)

Checkpoint HEAD before this final stability pass: `eead3d7f55226dfdc059c28fcf94b2ad89650788` (the second commit, following source commit `1054a2e2d9b0900c75ea28694ca5a1c6f93c91b7`).
The source-integration commit is immutable and remains the value of `source_integration_sha`. This checkpoint added the report and Gate JSON; no production code changed.

| Exact checkpoint SHA evidence | Actual observation |
| --- | --- |
| [Independent QA run #41457242166](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41457242166) | Completed / SUCCESS at `eead3d7f55226dfdc059c28fcf94b2ad89650788`: full pytest **690 passed**, independent QA **441 passed**, full and QA Ruff **PASS**, archived C001 replay **PASS_LOCAL**, local gate `local_checks_passed=true`, `overall_status=BLOCKED` |
| [Team 3 data run #41457242202](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41457242202) | Completed / SUCCESS at `eead3d7f55226dfdc059c28fcf94b2ad89650788`: Team 3 pytest **57 passed**, Ruff **PASS**, source PDF inventory **60/60 PASS** |

The 441 independent QA, 57 Team 3, and 3 cross-team tests are **subsets of the 690 full tests**, not separate quantities to add.
PR #17 at checkpoint HEAD has **30 changed files** vs its PR #15 base. The initial source-only commit had **29 changed files**; do not conflate those counts.

### Reproducibility and evidence boundary

Code and data paths are verified in the same source tree: `src/leadtime_guardian/qa/` (Team 1), operational modules under `src/leadtime_guardian/` (Team 2), and `qa/` plus `tests/qa/` (Team 3). The existing QA CLI, strict JSON input guard, Safety V6 and other cross-agent boundaries are covered by the passing regression suite; the full provider-to-evaluation pipeline has **not** been proven by a single authenticated live execution.

For code-only reproduction on the isolated copy branch (Python 3.11+):
```bash
git clone --branch feat/all-team-final-integration-20261102 https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy.git
cd leadtime-guardian-agent.copy
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q
python -m ruff check .
mkdir -p qa-run
python -m qa.inventory --root . --out qa-run/inventory
```
The inventory output must be a new path; existing reports must not be overwritten. Windows requires equivalent PYTHONPATH environment setup.
Studio is **not** contacted by these commands; do not report historical C001 V4 replay as a new live B0/E1 run.

### Precise external Studio handoff (not yet verified)

Return **original native bytes**, not a reconstructed prompt summary, for an authorized C001 B0 three-PDF *single case*; include PDF source SHA-256, upload/file receipts, actual Agent/Workflow ID, Config/version ID, Job ID, Step IDs, Parse/Classify/Extract (all three documents), Merge, Normalize JSON, QA input and QA report. Independently preserve E1 native execution, Python Safety V6 result and provenance sidecar, and evidence-binding records. If the platform cannot create a single multi-document Job, record the real limitation, platform-supported alternative, and review requirement; never concatenate three Job IDs into a fabricated one. Do not run paid Studio tasks from this GitHub review.

- **구도훈 (Team 1):** Collect the authentic B0/E1 reports, verify document/case/job/config/step provenance, run Cross-Agent evidence gate, then measure comparable B0/E1 results only after approved labels.
- **윤현준 (Team 2):** On the exact same native inputs, run/verify Python Safety V6, confirm numerical allocations/costs and supply immutable run sidecar, recording live-vs-offline provenance separately.
- **김민주 (Team 3):** Obtain the latest original review XLSX bytes and hashes, check the C001 evidence matrix against original PDF pages, substantiate human reviewer identity/approval, and only then decide whether any candidate can be promoted to Gold. Extend evaluation to C013/C017/C008 using verified ground truth.

**Code freeze ≠ deployment approval.** No new authenticated Studio B0/E1 evidence, live Python sidecar, human-approved Gold or validated performance advantage is present in this checkpoint. `REAL_STUDIO_E2E_VERIFIED=NOT_VERIFIED`, `HUMAN_GOLD_APPROVED=PENDING`, `OVERALL_RELEASE_READY=BLOCKED`; do not merge Draft PR #17 to main.

### Later documentation-only commit rule

This report and Gate JSON intentionally **do not claim their own next commit SHA**. Review the next PR HEAD against its GitHub Actions SUCCESS separately, and update the PR description with the verified SHA/CI URLs without another code commit. This prevents an infinite CI-documentation SHA loop.
