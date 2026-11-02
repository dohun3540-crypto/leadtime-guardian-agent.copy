# LeadTime Guardian — 2026-11-03 Studio / Gold / V6 evidence handoff

**Owner (GitHub QA):** Team1 구도훈.
**Code tree:** `feat/all-team-qa-final-freeze-20261103`; final Draft PR number, SHA and CI are recorded in the PR itself after creation and verification.
**Never** alter original PR #17/#18, main, PDFs, Human Gold, Studio configs, or paid Job state as part of GitHub QA work.

## Priority 1 — Authentic operational single-case B0 (Studio owner)

For C001 and subsequently C013, collect original, byte-preserved:
- all three input PDF bytes, their hashes and actual operational file-upload receipt IDs;
- Agent/Workflow ID, saved Config ID/version, case ID and **one unified operational Job ID** linking three documents;
- step records and original Parse/Classify/Extract three branches, MergeDocuments, NormalizeDocuments Native JSON bytes with each Step ID and SHA;
- Independent QA original *input* and raw QA *report*, its own Job/Config/Step and QA PDF upload receipts.

A valid separately completed one-file Job is not a unified three-document case. Never join differing Job IDs by name or case prefix. QA and operational executions **may** have distinct Job IDs, requiring explicit PDF origin and input linkage instead of false equality.

## Priority 2 — Team2 윤현준 Safety V6

Supply original Native-to-Python Adapter input, Safety V6 result, calculation inputs, provenance `studio-provenance/1` sidecar, source-hash binding and current run identity; distinguish provider-authenticated Live from archived V4, local replay, FakeClient, and synthetic fixtures. Ensure arrival dates, original/revised shortage, partial allocation, 60 EA alternative capacity, shipping once per quote are audited without writing to the real purchase system.

## Priority 3 — Team3 김민주 PDF / Gold

Collect the *latest corrected* `PDF_EVIDENCE_MATRIX.xlsx` as original bytes (do not request the user to re-review before locating the original), calculate SHA, parse actual typed cells, validate field-to-page alignment and reviewer/reviewed_at/decision/approval_state, then explicitly version the approved subset. C001 candidate files currently remain `AI_CANDIDATE` and are not a Gold truth set. C013 PO999 needs actual PDF evidence before expected block is called human-approved.

## Priority 4 — Team1 read-only release verification

Use `docs/NINTH_RELEASE_VALIDATION_RUNBOOK_20261101.md`:
1. Evidence inventory `python scripts/qa_release_evidence_check.py --manifest /private/evidence/release_evidence.json`.
2. Stage `python scripts/qa_stage_intake_check.py --manifest /private/evidence/stage_manifest.json`.
3. Combined `python scripts/qa_combined_e2e_check.py` using documented full inputs, truthful `--execution-kind`, all identity receipts.
4. B0/E1 `python scripts/qa_b0_e1_compare_check.py` when original matched PDF digests, two job/config/steps and approved human Gold exist.
5. Independent QA / Cross-Agent / Provenance / real numerical calculation / source-page Gold adjudication, then human release authorization.

No nonexistent paths or model-generated Native files should be created as fake replacements. Existing local gates can remain `BLOCKED` when code CI is PASS.

## Submit / handoff package

- Draft PR and commit SHA
- exact-HEAD Actions run links and full/QA/Team3 pytest totals (subsets, do not add)
- repository-wide Ruff output, C001 archive local check and PDF machine-inventory 60/60
- `docs/FINAL_ALL_TEAM_QA_FREEZE_20261103.md`
- current native/Gold missing-evidence checklist and accurately scoped Release Gate

**Team1 code task completion != full product deployment readiness.** No paid Studio reexecution, merge or LMS submission without the relevant user's decision.


## 2026-11-02 latest observed cross-repository/E2E handoff

- **Personal source**: PR #19 at immutable QA code checkpoint `af66a2d9c1b093558c3e7dc534ecbe66621d2657`; independently successful [QA 41463679425](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41463679425) (716 full, 467 QA, Ruff) and [Team3 41463679568](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41463679568) (57 Team3, 60 PDFs). New documentation-only HEAD should be verified separately through PR #19's latest CI.
- **Read-only integrated source**: `dohun3540-crypto/yuseok_integration` PR #2 observed at `5a7d4df070a7607585b5c1adb4847a1b79f8c2e7`. [GitHub CI 41464994396](https://github.com/dohun3540-crypto/yuseok_integration/actions/runs/41464994396) SUCCESS: 778 whole pytest, Ruff PASS, 60/60 PDF inventory. Older 757/8 failure and missing-pytest-import Ruff failure are superseded at this verified checkpoint. Do not cherry-pick personal QA source into this integrated branch: the independent QA type guard is present, batch source is byte-identical and shared strict JSON has compatible overflow/underflow safeguards.
- **Historical C013 Native found in user Library**: `SYN-C013_quotation_NormalizeDocuments (1).json` (uploaded 2026-10-30) preserves 3 normalized documents and a PO1 versus PO999 warning, source File IDs and a historical Job/Step reference. It is **STORED_NATIVE_HISTORY**, not current B0/E1. No original upload-receipt/PDF-SHA link, current Config-version proof, raw QA input/report or same-run V6 Sidecar was authenticated. Do not use as current E1 or real official accuracy.
- **Latest corrected Gold XLSX**: Library's spreadsheet file inventory showed only Studio job-list XLSX exports for this project, not the requested `PDF_EVIDENCE_MATRIX.xlsx` original. Latest human reviewer cells, source SHA and Gold freeze are still PENDING.
- **Current evidence sequencing**: User/Studio owner supplies actual C001 (then C013) single-case multi-document B0 and E1 Native, raw stage outputs/receipts; Team2 supplies exactly bound V6 Python result and `studio-provenance/1` sidecar; Team3 supplies original corrected source XLSX and approved field/page Gold. Use integration-side `docs/integration_20261102/NATIVE_AND_GOLD_REQUEST.md` and `python -m qa.integration` for a read-only local comparison. Do not treat a replay or archived Native as new live run.
- **Gate separation**: PERSONAL_CODE_FREEZE=PASS; INTEGRATION_SYNC_CODE=PASS_LOCAL at observed SHA; STUDIO_LIVE=BLOCKED; PYTHON_V6_LIVE=BLOCKED; GOLD_APPROVAL=PENDING; B0/E1=NOT_MEASURED; OVERALL_RELEASE=BLOCKED.
