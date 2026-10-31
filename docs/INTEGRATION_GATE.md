# Independent QA integration gate — isolated copy branch

## Scope
This module is deliberately read-only. It does not patch the engine, Studio adapter, original Studio configuration, source PDFs or draft gold. It is **not** a replacement for end-to-end Studio validation.

Run locally:
```sh
python scripts/qa_audit.py --case data/cases/SYN-C001/trusted_base_case.json
PYTHONPATH=src python -m pytest -q tests/test_qa_independent.py tests/test_qa_portfolio.py
python -m ruff check src/leadtime_guardian/qa scripts/qa_audit.py tests/test_qa_independent.py tests/test_qa_portfolio.py
```

Caution: the C001 trusted base is deliberately **pre-Studio** and has no predicted quotation or revised ETA. Do not pair it directly with the live C001 analysis.json to claim a real end-to-end PASS. Use the actual integrated case produced by the original adapter, when available. All test cases in this copy are synthetic contract examples.

## Merge gate
| Gate | Status until verified |
| --- | --- |
| Source branch and binary assets fully restored | BLOCKED |
| Existing pytest regressions | NOT_RUN |
| Existing Ruff checks | NOT_RUN |
| Independent QA regression | PASS: 54 tests in QA-only GitHub Actions run #41177193626 |
| Schema compatibility | NOT_RUN |
| Actual Studio C001 live provenance | NOT_RUN, archived evidence available in source PR |
| Human gold review | BLOCKED |
| Actual C013 and C017 runs | BLOCKED |

No claim of measured Studio extraction accuracy without human-reviewed ground truth. Never merge this work into source repository without explicit review. External actions are prohibited.

## Provenance
Source intended snapshot: source PR #11, `f196c694917f2d9e5f4ec228c752bd3f2a4eb882`. This copy's base was initially README-only, and a complete source tree migration is separately required.

## Safe restoration
Run `bash scripts/qa_restore_source.sh` in an authenticated clone of the copy repo after checking out `feat/independent-qa-integration`. This creates a new integration branch and merges fetched original PR files while protecting them. The script has **not** been executed; no full source copy has been verified.
