# Independent QA scorecard — 2026-10-31 KST

## Verified in GitHub Actions
- QA-only CI: **54 passed**, Ruff **PASS** at commit `859c5d8fcb68efb97a9c95d5ce712b7bdc5dde20`.
- Run: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/actions/runs/41177193626
- Scope: local deterministic unit/adversarial tests only. Newer branch commits require their own CI.
- Tested: incomplete input rejection, non-ISO dates, negative/NaN fields, duplicate keys and IDs, provenance label abuse, per-order and aggregate conservation, double-use of stock, excessive/late quote, repeated shipping, blocked-state no-purchase.
- Output examples in these tests are synthetic contracts shaped like C001, not re-execution of original Studio job.

## Not verified (do not imply otherwise)
- The COPY repository does not yet contain the complete original PR #11 code, PDFs, Native Studio exports or full evidence archive. This is a **blocking prerequisite** for full integration.
- Existing source PR has a recorded local checkpoint of 80 pytest passing; those 80 have **not** been rerun in the copy.
- No new live Studio job, API call or human-verified Gold was run.
- Real PDF-grounded extraction accuracy: **N/A**. Real end-to-end latency and cost: **N/A**.
- No source repository changes. No merge to main. No procurement or email.

## Next mandatory actions
1. On an authenticated Git clone of the COPY repository, check out the QA branch.
2. Run `bash scripts/qa_restore_source.sh` to fetch source PR HEAD into a **new** branch and merge without changing the source. The script checks for unexpected protected-file differences before Push.
3. Install dependencies, run all pytest/Ruff checks and resolve actual failures. Verify GitHub CI for the integrated branch.
4. Re-run archived C001 prediction through the real adapter using immutable original bytes. Report replay distinctly from live Studio inference.
5. Verify C013/C017 real Studio outputs with teammates. No human-Gold accuracy until verified PDF labels exist.
6. Update scorecard and PR with commit and factual evidence; merge only after review.
