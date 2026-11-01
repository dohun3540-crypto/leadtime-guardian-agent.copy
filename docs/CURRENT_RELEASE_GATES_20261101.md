# Team2 V6 + QA Combined Candidate — Release Gates (2026-11-01)

**All statuses attached to exact staged code HEAD `bdcdac48a39a73ee72f19936818648eae1813c90`**; GitHub Actions run #41291094905 (SUCCESS). Later documentation commits do not change that test claim until independently checked.

| Gate | Status | Verified evidence | Remaining blocker / owner |
| --- | --- | --- | --- |
| QA_CODE_GATE | PASS | QA 315 pytest + QA Ruff | code evidence only / Team1 |
| TEAM2_ENGINE_GATE | PASS_LOCAL | exact six source blobs from PR#12, 504 whole Python pytest | actual operating V5 live Job / Team2 |
| COMBINED_SOURCE_COMPATIBILITY_GATE | PASS | six core source Blob SHAs identical to PR#12; old QA preserved; exact combined HEAD | official original-repo integration not executed / Team1+Team2 |
| COMBINED_CODE_CI_GATE | PASS | GitHub Actions 41291094905 at combined HEAD | original-repo release branch CI still NOT_RUN |
| OFFLINE_E2E_GATE | PASS_LOCAL | C001 archived, C013/C017/C008 DRAFT, combined CLI + QA reference | no new Studio measured accuracy |
| STUDIO_DOCUMENT_GATE | NOT_VERIFIED | QA copy reported NOT_VERIFIED/PARTIAL on prior historical C001 | actual raw QA native+report+Step/Config / Studio AI |
| STUDIO_PROVENANCE_GATE | BLOCKED | local SHA/ID binding logic implemented | original PDF byte SHA + job-specific upload receipts / Studio+Team2 |
| PYTHON_SAFETY_GATE | PASS_LOCAL | independent local numeric audit and blocked path, V6 tests | actual current Python Job + source evidence / Team2 |
| CROSS_AGENT_GATE | BLOCKED | raw mapping and strict manifest tests | actual QA raw pair, same source PDF provenance, Python independent evidence / Team1 |
| HUMAN_GOLD_GATE | BLOCKED | only DRAFT case labels | human reviewed source-page field Gold / Team3 |
| OVERALL_RELEASE_GATE | BLOCKED | local Gate outputs BLOCKED, no approval | all above + G9 human sign-off |

`PASS_LOCAL` is a scope qualifier, **never Actual Studio PASS**.
No automatic merge, release, email, purchase or Studio paid run is authorized.
