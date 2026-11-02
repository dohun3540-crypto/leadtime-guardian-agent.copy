# Team1 Parallel E2E Readiness — final regression evidence

## Immutable baselines

- Frozen original personal PR #19 commit:
  `5d3172deaeecafec0056b48c92f0f0f6bb08297a`,
  [QA 467 / all 716 / Ruff / local gate](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821541)
  **SUCCESS**,
  [Team3 57 / 60 PDF Inventory](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41465821704)
  **SUCCESS**.
- Separate integrated PR #2 read-only checkpoint
  `67b93291c1f32acaf43e45815d2d1119480b652a`,
  [778 whole regression, Ruff, 60 PDF](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41465445285)
  **SUCCESS**. Never merge/push it from the personal task.

## New parallel code/QA checkpoints

- Initial regression with new preflight tests:
  [run 41468463613](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41468463613),
  **481 passed / 1 failed** in QA subset. Reproduced that a Team2 Sidecar
  falsely claiming independent PDF evidence could still set the local
  sidecar-binding boolean true. Fixed the boolean before continuing.
- Expanded 24 parametrized/additional regression cases for three synthetic
  PDF receipts, raw Native File IDs, independent QA Job, Team2 original Native
  digest/Job, B0/E1 same-hash vs changed-hash claims, strict JSON input,
  no-overwrite output behavior. Every test is offline SYNTHETIC only.
- Initial expanded run
  [41469115951](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41469115951):
  **491 QA pytest passed**, Ruff reported two `TRY004` style errors about
  exception types; no assertion was relaxed. Corrected only to TypeError.
- **Verified fixed source head** `4d3311dc7b895cbdac94b9901b6690e6d7126fe9`:
  [Independent QA run 41469262893](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41469262893)
  **completed SUCCESS**, **491 Independent QA tests passed**,
  **740 full Python tests passed**, no failed tests, QA Ruff PASS,
  repository-wide Ruff PASS; C001 archived replay/local gate PASS_LOCAL,
  `local_checks_passed=true`, `overall_status=BLOCKED`.
- Differences from protected HEAD: **+24 regression cases** (716→740
  full, 467→491 QA). QA is included in full, not added to it.
  The entire original source tree is preserved. No Team2, Team3, source PDF,
  approved Gold or previous QA files were altered.
- There is no separately triggered Team3-exclusive PDF workflow on this new
  Draft PR under the unchanged workflow filters. The 57 Team3 tests run as
  part of the full `pytest` suite; the separate 60/60 machine PDF inventory
  evidence is the exact protected PR #19 baseline and the source asset archive
  remains byte-identical to that baseline. Do not misstate this as a new
  Team3-only workflow run.

## Last documentation commit and exact-HEAD verification

This file and the machine-readable changeset manifest were added **after**
the fixed-source test checkpoint, without modifying any source or tests.
The final Draft PR description records its current HEAD and successful
HEAD-associated workflow run. A prior run number alone is not proof of the
final docs-only commit; reviewers should check the final PR's Actions page.

## CI commands

```bash
python -m pip install -r requirements-agents.txt -r qa/requirements.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
python scripts/qa_archive_check.py --root .
python scripts/qa_gate_check.py --root .
```

PDF original asset hash check remains part of Team3 protected snapshot;
human PDF semantic review, human Gold approval, independent provider cloud
upload proof and paid/real Studio B0/E1 execution were **not** performed.
No synthetic fixture was reported as Live execution or officially measured
extraction accuracy.

## Release decision

`PERSONAL_CODE_FREEZE=PASS`;
`TEAM1_PARALLEL_LOCAL_CODE_GATE=PASS` on verified source checkpoint;
`E2E_INTAKE_READY=PASS_LOCAL`;
`B0_E1_EVALUATION_READY=PASS_CONTRACT_ONLY`;
`GOLD_INTAKE_READY=PASS_EXISTING_TOOLS_ONLY`;
`CROSS_TEAM_COMPATIBILITY_GATE=STATIC_COMPATIBILITY_ONLY` until isolated
integration-branch regression is run by its owner;
`STUDIO_LIVE_VERIFIED=BLOCKED`;
`PYTHON_V6_LIVE_VERIFIED=BLOCKED`;
`HUMAN_GOLD_APPROVED=PENDING`;
`B0_E1_IMPROVEMENT=NOT_MEASURED`;
`FULL_PRODUCT_RELEASE_READY=BLOCKED`.

**Only a new exact-final-HEAD passing CI justifies final code freeze for
this new Draft PR**, as recorded in the PR description. Personal PR #19
is already independently frozen and unchanged.
