# LeadTime Guardian — Final Release Gate / 2026-11-02

**Owner:** Team1 구도훈. **Branch:** `feat/final-qa-cross-agent-integration-20261102`.
**Decision:** **NOT RELEASED / OVERALL_RELEASE_GATE=BLOCKED**.
This report separates GitHub-tested code quality from any authenticated current Studio run.

## Separate gates

| Gate | Status before final new-branch CI | Evidence and remaining blocker |
|---|---|---|
| CODE_GATE | PENDING_NEW_HEAD_CI | PR #15 baseline GitHub Actions 41310379906 PASS: full 630 / QA 441 / Ruff. New branch includes identity hardening and 9 new synthetic tests; check its own final HEAD logs. |
| CONTRACT_GATE | PASS_LOCAL_CANDIDATE | Existing Native wrapper, Safety V6, QA and Cross-Agent contracts retained; new B0/E1 File ID + operational stage-binding guards. New Studio provider originals not authenticated. |
| PROVENANCE_GATE | BLOCKED | No verified matching operational Native original, current PDF upload receipts, QA original and Team2 current Live Sidecar. |
| GOLD_GATE | BLOCKED | Team3 original PR #13 latest handoff records human Gold not frozen, unverified original reviewed XLSX bytes, missing versioned approval and official accuracy. |
| STUDIO_E2E_GATE | BLOCKED | Historical C001 V4 archive ≠ current B0/E1. 2026-11-01 reported B0-C001 three one-file Jobs ≠ one integrated 3-PDF Job; C013 current comparable job still absent. |
| OVERALL_RELEASE_GATE | BLOCKED | Requires all evidence-backed gates and authorized human decision; code CI alone insufficient. |

**Do not promote** any code-only PASS_LOCAL, synthetic replay, user-reported Studio AI summary, GitHub Actions success, or source ZIP to a Live Studio PASS or measured extraction accuracy.

## Official comparison matrix (evidence-driven)

| Run | Status | Claim boundary |
|---|---|---|
| B0-C001 | BLOCKED | Reported split PDF Jobs cannot supply single-case Normalize/QA; prior NCik is historical/unverified native chain |
| B0-C013 | NOT_VERIFIED | No authenticated same-case B0 Native, source PDFs and expected PO1/PO999 evidence chain |
| E1-C001 | NOT_VERIFIED | Raw E1 provider Job+Config+PDF digest+QA input/report not authenticated |
| E1-C013 | NOT_VERIFIED | No authenticated E1 C013 counterpart |
| B0↔E1 quality | NOT_MEASURED | Same original PDF SHA and approved human Gold are unverified |

The NEW C001 B0 split observation, if received as three different Job IDs, should be processed by existing `python scripts/qa_studio_batch_check.py --report ... --case-id C001`. A mere list of completed jobs is not evidence of integrated processing. Do **not** re-run paid Studio jobs, alter configs or fabricate receipts.

## Cross-agent evidence requirements

**Operational run:** original PDF bytes + SHA, 3 source File IDs/Upload Receipt, saved Workflow/Config ID & version, one Job ID covering all documents, original 3 Extract steps, Merge/Normalize steps with Step IDs and raw bytes, original output envelope, Team2 Safety V6 result and studio-provenance/1 sidecar.

**Independent QA:** original Normalize→QA raw input bytes, QA Job/Config/Step ID, raw QA report, original source PDF receipt for QA workspace, checked_document_ids, qa_status, evidence_status, workflow_version, review flag. QA Job may legitimately differ from operational Job; match through explicit source hashes/receipts rather than fabricated matching IDs.

**Gold:** source PDF SHA + document/page/field evidence + actual reviewer verdict and timestamp + exact approved Gold artifact checksum + version/adjudication. DRAFT/candidate or unverified XLSX is never approved Gold.

## Reproduce code verification

```bash
python -m pip install -r requirements-agents.txt
PYTHONPATH=src python -m pytest -q tests/test_qa_experiment_identity_hardening.py
PYTHONPATH=src python -m pytest -q tests/test_qa_*.py
PYTHONPATH=src python -m pytest -q
python -m ruff check .
```

Further read-only E2E commands (run only with genuine files) are documented in `docs/NINTH_RELEASE_VALIDATION_RUNBOOK_20261101.md`. 
On missing current Native or reviewed Gold, report **BLOCKED** with exact missing artifact, not a guessed success.

## Human release guard

Do not merge PRs #12/#13/#15/#16, change main, force push, change other members' branches, overwrite PDF/Gold originals, run paid Studio, send purchases/emails or submit an LMS entry. A new Team1 Draft PR is only a proposed code candidate. A real release requires explicit evidence review and approval.
