# Team 4 PR #1 — 원본 바이트 추출·보존 검증

## 검증된 출처
- Source: [`061015ed-cys/Upstage-AI`](https://github.com/061015ed-cys/Upstage-AI), **Public**, branch `codex/team4-final-review`, exact PR #1 HEAD `c34e9b7d6d310ef26f38c430f6ad8134afe47633`, OPEN/unmerged.
- Stage: [`dohun3540-crypto/leadtime-guardian-agent.copy`](https://github.com/dohun3540-crypto/leadtime-guardian-agent.copy), **Public**, isolated branch `feat/team4-submission-handoff-20261104`, pinned Team1 PR29 `bcd09794db7b5fe6c09ceffe84d33c5e98043479`에서 분기.
- Future read-only comparison: `dohun3540-crypto/3rd_task_dohun` at `25690af367db7f298c5f2b6acd984d94e6d5b35a`; `integration_finished_workforlast` PR4 at `f2b395c2122babab19a79df53ac633784f44924c`. **어느 쪽에도 쓰지 않았음.**

## 원본 6개 (경로: `docs/team4/`)
| File | Bytes | Original Git Blob SHA | Independent SHA-256 |
| --- | ---: | --- | --- |
| `DEMO_AND_PITCH.md` | 4002 | `76e5fb629d3cfbd7fe8127b899e2f5f3824d9551` | `19f760bc764b88ff597fd3a76ffe4bc72ce8df8bc0634c199824d1e8c6ffdb3a` |
| `FINAL_HANDOFF.md` | 6023 | `c0922983770b4dac846df7b9a6e51f683f78c4a4` | `ad36f62468930e61055e5236475f07b370cbe8a972b7fca47bb5e766952dacd3` |
| `OFFICIAL_SUBMISSION_REQUIREMENTS.md` | 2022 | `cbb29af39c0b5479e4bfb0bddb87192ef58a4b51` | `ca8a240b37d60253bd08dbff3df8b02dd2c51a11684009280465d60f6db3d013` |
| `PRE_FLIGHT_CHECKLIST.md` | 1410 | `d2341ffa51398ed142f3fb5b31fe2f65172843c6` | `61c9ed4b11207cd07d5e78493185857fad7ac107721fe81e773dcc55fcec1696` |
| `SETUP_RUNBOOK.md` | 3465 | `c94967cf8442e8419b21a8ea33507d2adb25fa82` | `2b0df949fb9c382cc55ff597c35d08b94256f57787aae1bf25d1c694234c031f` |
| `SUBMISSION_PACKAGE_MANIFEST.DRAFT.json` | 1967 | `49cfd4f592f03a05c591816b9173297f1ad4552d` | `0c09c0873acef138e58855e3d4698948e4a963da320b73ccdccae4b5a44d0b3d` |

**6/6** source Git Blob SHA == stage Git Blob SHA, source tree byte size == independently measured UTF-8 length. **5/5** source document hash values also match the source DRAFT manifest; manifest itself is not listed as an entry in itself and is separately SHA-256-attested above. Source DRAFT JSON syntax and seven listed `share_approved=false` entries are valid; `zip_created=false`, `upload_authorized=false`.

### Extraction and static document checks
- Source changed paths (PR #1): 8 = 6 new team4 documents plus `README.md` and `docs/SUBMISSION_CHECKLIST.md` (the latter two **not overwritten**).
- All six sources are original UTF-8 text; no content normalization, newline changes or replacements. Each stage-created Git Blob SHA matches the pinned source Blob.
- Markdown relative-link resolution: **0 broken relative Markdown links** in these six documents; external links 3 total. Markdown/JSON parse audit is structural; no actual media/portal/Studio submission validation implied.
- Narrow text scan: no detectable inline GitHub PAT, sk- token, AWS AKIA credential or PEM private-key block in six documents. No complete secret scanning, PDF/binary scan, third-party sharing/license approval or Git history leak attestation.
- **Public visibility caution:** Source and `.copy` are currently Public (source `FINAL_HANDOFF.md` says `private` — historically incorrect). Only text already Public at Source was copied. Do not add private Studio Native bytes, personal data or keys to this branch.

## Integrity and no-code-diff guarantee
The first isolated commit `450ea0ff2079469025083b34c6402372a94a5203` adds exactly 6 source `docs/team4/` files. The follow-up commit should add only six `TEAM4_*` report/manifest documents. No engine, QA, source PDFs, Studio Config, Gold candidate, CI workflow, README or original source branch was modified.

Historical Team4 source main CI claimed 739 tests at SHA `575745bd8c6a8f00627197de6e6bb8530bcec6bb`; this is **not** an attestation of `.copy` or 3rd current CI. No fresh Studio run or submit ZIP produced here.

**Result:** `SOURCE_EXTRACTED=6/6`, `BYTE_IDENTITY=PASS`, `JSON_SYNTAX=PASS`, `RELEASE=BLOCKED`.
