# Cross-Team Compatibility and Isolated Merge Feasibility

**2026-11-03 KST.** No remote change to `yuseok_integration`, original Team2 repository, Team3 original data, PR #19 or PR #20. All changes are isolated in personal Draft PR #21.

## Actual repository state

| Repository/PR | Verified commit | Evidence | Modification |
|---|---|---|---|
| `leadtime-guardian-agent.copy` PR #19 | `5d3172deaeecafec0056b48c92f0f0f6bb08297a` | CI 716 total / 467 QA / 57 Team3 and protected 60 PDFs | None |
| `leadtime-guardian-agent.copy` PR #20 | `53ae1a7dbe53be38a7d585676c2b2d037534fb46` | CI 740 total / 491 QA, full Ruff | None |
| `yuseok_integration` PR #2 | `67b93291c1f32acaf43e45815d2d1119480b652a` | [778 total, Ruff and 60/60 PDF CI](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285) | Read-only |
| Original Team2 PR #12 | `e9b9992b593a42d427ff1bbadeb9a9866ca593bd` | source read-only / original Python CI successful | None |
| Original Team3 PR #13 | `a925103077173b37d1cefcd6a9576ae644dc2040` | source read-only / original Python CI successful | None |

## Direct GitHub tree & import inspection

- The **four new PR #20 paths** (`qa/e2e_bundle_preflight.py`, `scripts/team1_e2e_preflight.py`, `tests/test_qa_parallel_e2e_bundle.py`, its parallel handoff README) **do not exist** at the observed integration PR #2 HEAD. The new PR #21 changes only the Team1 preflight and its synthetic tests; no identically named integrated path will be overwritten at that checkpoint.
- Three dependencies' **Git Blob SHAs are identical** between the PR #20 protected source and integration:
  - `src/leadtime_guardian/qa/release_inventory.py`: `fb8982edb23078cb98a333ac4f9c581ad219ef47`
  - `src/leadtime_guardian/qa/studio_contract.py`: `08b23233ce12575c1c18f654e3ae296b8efa3e7c`
  - `src/leadtime_guardian/qa/experiment_compare.py`: `0c0bbf2c38456019d891625e7486e379e1f96ecf`
- **Different by design**: integrated `src/leadtime_guardian/qa/audit.py` blob `8de0aaaf7b1911d361bd85c9b970d978a126daac` delegates strict input parsing to integrated `src/leadtime_guardian/strict_json.py` blob `afa56a5f201af250eeb28a20580bd0188fe5cb51`. Personal `audit.py` blob `cdce35bfe3256d964695eae7164b2f034c3ead17` uses its own strict implementation. Both preserve duplicate-key/nonzero-underflow guards, but code has not been run as a joined tree. **Do not overwrite integrated shared strict parser or comparison rules**.
- Other protected integration differences include `src/leadtime_guardian/qa/input_delivery.py` with strict recursive typed comparison and Team3 `qa/inventory.py` guards. Neither is imported directly by the new E2E cross-file preflight or modified in PR21.
- New module's existing import signature and all existing source paths have been checked; no extra package dependency, CLI namespace collision or schema version bump was introduced.

## Why real merged-tree tests are NOT claimed

A remote Git Checkout from the execution container failed with `Could not resolve host: github.com`. The connected GitHub reader can independently inspect original files/trees and verify PR-associated GitHub Actions, but the local execution container cannot clone the private `yuseok_integration` repository. It would be misleading to claim an actual isolated overlay, import-only integration or 778+N test run without the full checked-out private integrated tree.

**MERGE_SIMULATION = NOT_RUN_NETWORK_RESTRICTED**; **INTEGRATION_COMPATIBILITY = STATIC_COMPATIBILITY_ONLY**. The tested personal branch is real GitHub Actions execution, but not an integrated-tree run.

## Safest integration workflow (for the integration maintainer)

1. Obtain current integration PR #2 exact HEAD and protect its source; use a disposable checkout, **not** main.
2. Copy only the PR #20 newly introduced module/CLI/test and handoff docs, then overlay the **PR #21 two patched Team1 files**. Do **not** use `git merge` of the entire divergent private QA branch or copy old `audit.py`.
3. Verify the resulting imported module resolves the *integrated* `qa.audit.load_json_strict` and unchanged three dependency modules.
4. Run `python -m pytest -q tests/test_qa_parallel_e2e_bundle.py`; then `python -m pytest -q`, `python -m ruff check .`, existing archived C001 gate, `python -m qa.inventory --root . --out /new/private/inventory` and provider/Gold readiness checks only with real originals.
5. Compare all original Team2 V6, Team3 archive/Git source SHAs before and after. Verify that no existing tests disappeared; do **not** assume an additive 778 + 8 total without actually collecting the merged suite.
6. Preserve Team1 PR #21 Draft and isolated until the integration maintainer reports exact resulting SHA + CI.

## Provenance and independent QA invariants

- Operational Native's explicitly supplied Config ID/Version must match its own saved Manifest; Team2 Sidecar must refer to the **actual operational Native bytes**. Config ID/Version may be absent from provider Native; the preflight does not fabricate them.
- Independent QA Job may be different from the operational Job, but its own File IDs, original QA Input/Report and provenance must be linked to the same source PDFs. No forced cross-Job equality.
- Local Receipt hash matches and GitHub passing tests do **not** authenticate Upstage cloud uploads; original Upload Receipts and team approval are external gates.
- A supplied QA verdict is not interpreted as a human-approved Gold or autonomous business action authorization.
- New `C###` Document ID clash and Merge type-to-source PDF role checks are additional *local* traceability guards; they cannot replace human PDF field-level review.

## Case scope

New preflight is **C001-only**, by existing `leadtime-release-evidence/v1` design. C013 deliberate PO1/PO999, C008 R1/R2 allocation, and C017 Korean-to-ISO extraction are covered by existing local fixtures and should not be claimed as new Live E2E tests. B0/E1 official comparison and Gold approval remain BLOCKED/NOT_MEASURED.

**Cross-team code collision detected at the observed integration HEAD: none among new Team1 paths. Runtime compatibility after overlay: NOT_RUN; integration owner action required.**
