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

The README/documentation-only follow-up may create a later PR HEAD; verify a fresh GitHub Actions run on that final HEAD before declaring the latest commit CI-verified.

### Remaining owners and priorities
- **P0 · 구도훈:** Recover actual integrated 3-PDF C001 B0 single Job, original Normalize and independent QA raw reports with matching Agent/Config/Job/Step/PDF SHA provenance; previous 3 distinct Jobs are NOT valid.
- **P0 · 윤현준:** Supply native live Studio-to-Python V6 sidecar and evidence-bound execution matching the same C001 B0, then C013/C017/C008. Existing offline replay is not live proof.
- **P0 · 김민주:** Check latest actual source XLSX bytes, PDF field grounding and reviewer approvals before Gold promotion. Candidate status stays AI_CANDIDATE.
- **P1 · 구도훈 + 윤현준 + 김민주:** After all three evidence streams exist, execute a new authenticated B0→E1 comparison, verify release Gate, and request human authorization before any production merge.
