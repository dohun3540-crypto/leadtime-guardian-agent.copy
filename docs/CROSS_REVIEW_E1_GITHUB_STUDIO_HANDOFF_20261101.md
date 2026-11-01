# LeadTime Guardian — GitHub × Studio E1 cross-review and handoff (2026-11-01)

## Scope and evidence grades

- Isolated QA cross-review Draft PR: https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy/pull/14
- Baseline QA code freeze: PR #11, branch `feat/qa-tenth-final-code-freeze-20261101`.
- Parallel old-base QA PR #12 has a different `input_delivery.py` implementation and MUST NOT be merged/cherry-picked wholesale over PR #11.
- Observed E1 properties (`issues[*].severity="info"`, `workflow_version=null`, `qa_status=NOT_VERIFIED`, `evidence_status=PARTIAL`) are **user-reported**, not authenticated Upstage raw bytes in this GitHub session.
- Full original B0/E1 stage JSON, actual IndependentQA input, PDF uploads/receipts, Team2 live sidecar and Human-reviewed Gold remain NOT_PROVIDED in this task. No paid Studio job was launched.

## Confirmed code defects and bounded corrections

1. **Invalid Python input could masquerade as identical valid JSON.** Previous `_typed_json_equal` called `json.dumps` directly. `{"items":(1,2)}` and `{"items":[1,2]}` serialized identically; `{1:"x"}` and `{"1":"x"}` serialized identically. This was reproduced using Python serialization and blocked by a recursive strict JSON input-type validator before existing canonical comparison. Rejects tuples, non-string object keys, non-finite floats and unsupported objects. Preserves normal JSON and source objects. This is a **local payload comparison fix**, not provider authentication.
2. **Studio report severity and workflow version contract mismatch.** On the supplied *user-reported* E1 shape, the previous adapter rejected lowercase `info` and explicitly present `workflow_version:null`. Adapter now recognizes only lowercase `info`, `warning`, `error` with explicit `STUDIO_ISSUE_SEVERITY_CASE_NORMALIZED` warning and human review; arbitrary spellings remain invalid. Explicit null workflow version is structurally accepted with `STUDIO_WORKFLOW_VERSION_NOT_VERIFIED`, preserves the original null, and triggers human review; omitted required key remains structural FAIL. An optimistic PASS with null version is not promoted to verified PASS.
3. Original Studio report is never mutated; `actual_cloud_input_authenticated`, `python_run_verified`, `pdf_grounding_verified`, and release authorization remain false where applicable.

## Files

- `src/leadtime_guardian/qa/input_delivery.py`
- `src/leadtime_guardian/qa/studio_qa_adapter.py`
- `tests/test_qa_cross_review_e1_contract.py` (synthetic contract tests, not live E1 evidence)

## CI / regression

- Pre-change PR #11: 600 full Python PASS, 411 Independent QA PASS.
- Updated isolated PR code commit: check PR #14 HEAD; workflow run `41308883904` passed **627 full Python**, **438 QA**, both Ruff checks, Archived C001 replay and local integration. QA tests are included in full Python tests.
- One initial Ruff import-formatting failure was corrected; never cite an earlier failed CI as final evidence.
- After this documentation commit, verify **the final PR HEAD** has its own SUCCESS run and report the actual SHA/run; this document intentionally does not self-reference its final SHA.
- No new live provider run was performed. `OVERALL_RELEASE_GATE=BLOCKED`.

## Studio-side independent verification request (NOT sent automatically)

1. Preserve existing B0 C001 `job_NCik8shwrgM93PDnNNYukT`, saved `cfg_X2xXakDtmDTHh2RoqVysvL` v1.
2. Obtain the actual E1 IndependentQA raw report bytes, source Job/Step ID, Config ID/Version and SHA. Confirm exact casing, null `workflow_version`, required nine top-level keys, field checks, checked document IDs and original provenance. Do not claim the reported shape is authenticated until source bytes are obtained.
3. Verify that a lowercase severity maps to uppercase only in the local **adapter output**; raw Studio JSON remains immutable. Null workflow version must remain unverified; no invented version/Job ID. Never turn `NOT_VERIFIED` into PASS.
4. Check saved Studio schema and workflows; change a Studio node only if a real source-level incompatibility is confirmed. Preserve before/after Config diff; no unapproved paid execution.
5. Gather original B0 Extract3/Merge/Normalize, QA actual Step INPUT/Report, three PDF bytes/SHA and both upload receipts, Team2 sidecar, Team3 reviewed Gold. Without these, live cross-agent/accuracy/release remain BLOCKED.
6. Re-run the local GitHub adapter and QA strict-JSON tests with authenticated input when provided; differences must be reproduced and passed to GitHub as a minimal `GITHUB_FIX_REQUEST`.

## Gate status

| Gate | Status | Evidence |
| --- | --- | --- |
| QA code / Python regression | PASS_LOCAL_CI | 627/438 PASS on workflow 41308883904 (code SHA), two Ruff PASS |
| E1 adapter structural contract | SYNTHETIC_CONTRACT_PASS | New synthetic tests; Studio native report not provided |
| Normalize → QA actual cloud input | NOT_VERIFIED | No actual Step input+raw evidence |
| Cross-agent actual provider provenance | BLOCKED | No authenticated Job/Step/source uploads |
| B0/E1 quality change | NOT_MEASURED | Need identical PDF SHA + Human-reviewed Gold |
| Final Studio E2E / Overall release | BLOCKED | Source evidence and signoff still missing |

## Suggested next autonomous task

Receive genuine E1 QA raw and B0/E1 Stage sources, recompute original byte SHA, run `qa_release_evidence_check.py`, `qa_stage_intake_check.py`, `qa_combined_e2e_check.py`, and when both runs exist `qa_b0_e1_compare_check.py`. Do not silently merge old-base PR #12. Preserve GitHub PR #11 code freeze until review/approval.
