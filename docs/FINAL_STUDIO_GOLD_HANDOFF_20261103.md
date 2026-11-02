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
