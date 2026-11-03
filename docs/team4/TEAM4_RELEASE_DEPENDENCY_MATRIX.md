# Team 4 G0–G9 Release/Submission Dependency Matrix

현재 시점 `2026-11-04`. 원본 Team4 문서의 과거 판정과 현재 GitHub 코드 CI를 **구분**. 실제 Studio Cloud, 공식 포털, 사람 Gold 증거가 확보되지 않았으므로 전체 Release **BLOCKED**.

| Gate | Owner(s) | 필요한 불변 증거/실행 조건 | 현 판정 |
| --- | --- | --- | --- |
| G0 공식 제출 규격·권한 | Team1 + Team4 | 실제 제출 포털 로그인 화면·필수 입력칸·확장자·크기·팀 등록·허용된 공개범위 | **NOT_VERIFIED / BLOCKED** |
| G1 Studio Native 단일 실행 | Team1 + Team2 | C001/C013 동일 케이스 PDF3, upload original SHA, 단일 Job/Step, 실제 Config version, raw Native 단계 | **BLOCKED** |
| G2 Python Safety V6 current-Native | Team2 | 동일 Native Job을 입력으로 한 계산/Sidecar, C001 수치, C013 PO 정책 차단 | **PASS_LOCAL / LIVE_BLOCKED** |
| G3 Independent QA | Team1 | 실제 IndependentQA Input, 원본 QA Report, Normalize→QA 요청·응답 | **NOT_VERIFIED / BLOCKED** |
| G4 Provenance/Cross-Agent | Team1 + Team2 | Case/Job/Step/Config/File ID, original PDF SHA256 Receipt, signed mapping, Gate trace | **BLOCKED** |
| G5 PDF 근거 & Human Gold | Team3 | PDF 페이지별 인간 검토/승인자·일시·Gold frozen SHA, 정식 지표 분모 | **NOT_APPROVED / NOT_MEASURED** |
| G6 회귀와 적대적 검증 | Team1 + Team2 + Team3 | C001 정상, C013 충돌, C008 부분납품, C017 한글 날짜, 로컬/Live 별도 | **PASS_LOCAL / LIVE_NOT_VERIFIED** |
| G7 코드·인계 무결성 | Team1 + Team2 + Team3 + Team4 | 통합 SHA·CI·Blob 및 source evidence 교차 확인 | **Team4 DOC6 EXACT; LOCAL CODE_CI_CONTEXT_ONLY; RELEASE_BLOCKED** |
| G8 시연·제출 구성 | Team4 (+ 팀 전체) | 시연 영상, 발표 자료, 실제 ZIP, README 재현, 검토된 Portal 규격, 소스 공개 허가 | **NOT_PRODUCED / BLOCKED** |
| G9 최종 승인·접수 | Team1 + Team4 | 최종 Release 서명, 승인 범위, 공식 제출 완료 영수증/접수 시각 | **NOT_AUTHORIZED / BLOCKED** |

## 구체적인 미확보 자료
- C001/C013 실제 Studio Native 단일 케이스 전 단계 실행 원본 및 최근 Job/Step/Config/File 연결.
- 실제 IndependentQA Input/Report, Normalize request, raw Merge, 원본 PDF upload SHA256.
- Team2 current-Native Python Sidecar, Team3 승인 Human Gold, 근거 분모, 공식 정확도/개선율.
- B0-C001, B0-C013, E1-C001, E1-C013 **공식 4개 비교 가능 실험 번들** (0/4 인증).
- 제출 포털의 실제 필수 필드·파일 규격·공개 권한, 최종 슬라이드/영상/제출 ZIP.
- 팀원 1의 명시적 공개/제출 승인 및 접수 영수증.

### 일정의 근거·구분
- 공식 최종 프로젝트 제출: **2026-11-11 13:00 KST** ([울산대학교 공식 공지](https://ie.ulsan.ac.kr/ie/893?action=view&no=282626)).
- **2026-11-10 17:00**은 팀 내부 패키지 동결 목표이지 공식 포털 마감이 아니다.
- 포털 실측 규격은 공식 공지와 별개이므로 **NOT_VERIFIED**.

`SUBMISSION_ZIP=NOT_CREATED`; `VIDEO=NOT_PRODUCED`; `PORTAL_RECEIPT=NOT_AVAILABLE`; `HUMAN_GOLD=NOT_APPROVED`; `OVERALL_RELEASE=BLOCKED`.
