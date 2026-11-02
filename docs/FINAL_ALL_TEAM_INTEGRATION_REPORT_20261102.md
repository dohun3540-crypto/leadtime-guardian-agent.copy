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
