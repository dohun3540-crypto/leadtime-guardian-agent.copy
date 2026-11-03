# Team4 README / 제출 체크리스트 선택적 이식 차이

대상 원본: Team4 Source PR #1 (`c34e9b7d6d310ef26f38c430f6ad8134afe47633`). `.copy` README 및 `docs/SUBMISSION_CHECKLIST.md`는 **이번 작업에서 수정하지 않음**.

## Source PR #1에서 확인한 8개 파일 변화
- 6개 문서 신규 추가 (Git Blob 동일성 6/6 보존).
- `README.md`: (a) Team4 인계 문서 링크 추가, (b) 설치 안내 `requirements-validation.txt`, (c) Source용 clone URL, (d) PDF 재생성 권장 삭제 및 보관 tar.xz 57개 명시, (e) 없는 `data/gold/extraction_gold.json`을 `qa/gold_candidates/SYN-C001/candidate.v1.json`으로 변경, (f) C001 원본 재생성 지시 제거.
- `docs/SUBMISSION_CHECKLIST.md`: 기존 `2026-11-10 17:00`을 **내부 동결**로, **2026-11-11 13:00 KST**을 공식 최종 제출로 명시.

## 대상별 선택 적용
| 항목 | .copy PR29 현재 | 3rd 현재 | 이식 시 권장 |
| --- | --- | --- | --- |
| Clone | 과거 Team1 문구 | 이미 `3rd_task_dohun`로 갱신됨 | **3rd 링크 유지**, Team4 Source URL 붙여넣기 금지 |
| 의존성 | `requirements-validation.txt` 미존재 | 해당 파일 존재 | 3rd에서만 설치 명령을 검증 |
| PDF 보관 | `SYN-C002-C020_DRAFT_PDFs.tar.xz` 존재 | 동일 보관 아카이브 존재 | `tar -xJf`는 지정된 테스트/검수 환경에서만; 원본 C001 재생성 금지 |
| Gold 경로 | `qa/gold_candidates/SYN-C001/candidate.v1.json` 존재 | 존재, 미승인 후보 | 정식 Human Gold처럼 표현하지 않기 |
| 11/10 17:00 | 기존 문구에 제출처럼 보일 수 있음 | 체크리스트에 옛 문구 있음 | **팀 내부 동결 목표**로 표기 |
| 11/11 13:00 | 원본 공지에 명시 | 별도 최신 안내 일부 존재 | [울산대 공지](https://ie.ulsan.ac.kr/ie/893?action=view&no=282626) 기준 공식 마감으로 표시 |
| 팀원 4 문서 링크 | 없음 | 없음 | `docs/team4/FINAL_HANDOFF.md` 포함 이식 후 링크 추가 |
| Source의 739 pytest | Team1/3rd CI와 다름 | 현재 950 PASS와 다름 | 과거 **Source main SHA 범위**만 보존; 현재 CI로 재사용 금지 |

## 실제 안전 수정 예시 — 3rd에서만 후속 검토
1. `README.md`에 `[Team4 제출 인계](docs/team4/FINAL_HANDOFF.md)` 추가. 기존 3rd 단일 Clone 명령을 그대로 유지.
2. `docs/SUBMISSION_CHECKLIST.md`의 11/10 항목을 내부 동결로 명시하고 공식 11/11 13:00을 별도로 기록. 원본 상태 “20+ PDF not in GitHub”는 현재 3rd의 60-PDF 보관 구조에 맞춰 업데이트.
3. `docs/TEAM_WORKFLOW.md`에 Team4 담당(발표·데모·제출 ZIP/portal), 승인·비밀자료 처리 원칙 추가.
4. 공개용·심사용 범위를 확정한 뒤 README에 새 팀원4 브랜치/경로와 담당 링크. **이 작업 자체는 3rd에 일절 적용하지 않았음**.
