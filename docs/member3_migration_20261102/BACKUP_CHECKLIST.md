# 계정 만료 전 백업 체크리스트

이 문서를 만들었다고 파일 원본까지 전송된 것은 아니다. 아래 체크는 실제로 다운로드한 뒤 표시한다. 인계 패키지 전체 백업 상태는 현재 미완료다.

## A. GitHub 저장소 — 별도 계정 접근과 함께 보존
- [ ] feat/qa-ground-truth-evaluation 브랜치의 Code → Download ZIP으로 소스 사본 다운로드. main ZIP만 받으면 QA 변경/데이터가 빠질 수 있다.
- [ ] ZIP을 풀어 qa/, tests/qa/, docs/member3_migration_20261102/, data/cases/가 있는지 확인.
- [ ] Git 이력까지 필요하면 별도 로컬 clone 후 git bundle create ../leadtime-member3.bundle --all 로 보존. 이 명령은 아직 실행하지 않았다. bundle/clone에는 이력상 민감정보가 없는지 점검하고 팀 허용 저장소에만 보관.
- [ ] 원본 PR #12 및 QA 사본 저장소의 최신 작업도 해당 담당자에게 별도 백업 요청. QA 브랜치 ZIP이 다른 브랜치/저장소 전체를 포함하지는 않는다.
- [ ] 새 AI 계정에서 저장소 권한이 있는 GitHub 계정을 재연결. GitHub 계정 자체를 새로 만들 필요는 없다.

## B. 채팅/사용자 PC에만 있는 원본 — 중요
아래 원본들은 이번 Git 커밋에 포함하지 않았다. 첨부를 하나씩 로컬로 다운로드하거나 이미 보관된 원본을 복사한다. 텍스트 추출본/스크린샷으로 대체하지 않는다.
- [ ] PDF_EVIDENCE_MATRIX.xlsx 최신 수정본. 반드시 최우선 보존. 동일 이름 구판과 다른 폴더에 저장한다. 권장 폴더: review/latest/ 및 review/older/. 파일 확장자만 바꾸지 않는다.
- [ ] 261101_기록.json
- [ ] LeadTime Guardian - B+C3 V1.json
- [ ] Studio_QA_Sandbox_Config_v5.export.json
- [ ] Studio_QA_설정5_확인메모.txt
- [ ] 10-31_작업_현황_및_현재_작업구조.docx
- [ ] 팀원123_협업_및_최종통합_실행계획.docx
- [ ] 팀원3_상세_TASK_최종제출품질.docx
- [ ] 팀원3_Work_개인AI_실행프롬프트.txt
- [ ] 팀원123_전체공지_복사용.txt
- [ ] 필요하면 C001 검수 화면 PNG 3개 및 서비스가 제공하는 방식으로 이전 대화 내보내기. 대화 백업은 원본 파일 백업을 대신하지 않는다.
C001 PDF3개는 GitHub data/cases/SYN-C001에도 있으므로 Git 사본에서 복구 가능하다.
구판 수정본 식별을 위한 이전 대화 파일 ID는 STATE.json에 기록했지만 새 계정에서는 사용할 수 없다. 최신 실제 로컬 파일을 직접 확인해야 한다.

## C. Studio 계정/워크스페이스
- [ ] 본인이 접근 가능한 운영/QA/복사본 설정 각각 원본 Export 다운로드.
- [ ] 해당 설정의 이름/Workflow ID/Config ID/버전/내보낸 시각을 별도 기록.
- [ ] 실제 실행이 있다면 최종 Native JSON, 노드별 결과, Job/Step/입력 File ID/입력 PDF 목록과 SHA를 다운로드.
- [ ] 입력 PDF도 별도 보존. 설정 Export는 입력 파일이나 실행 이력 전체 백업이 아니다.
- [ ] 새 계정에서 접근 가능한지 확인하거나 팀 관리자에게 워크스페이스 초대/공식 이전 절차 문의. 이전 기능/가져오기 지원 범위는 현재 UI와 정책으로 확인.
- [ ] 새로 가져온 설정은 ID가 달라질 수 있으므로 이전→신규 매핑 기록. 예전 Job을 새 실행으로 표시 금지.
이 작업에서 Studio 삭제/복사/새 실행/계정 이전을 실제 수행한 것은 아니다.

## D. CI 원본 산출물 — 만료 주의
- [ ] 최신 전용 실행 https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41295813181 에서 로그와 artifact 다운로드.
- [ ] 기본 실행 https://github.com/dohun3540-crypto/leadtime-guardian-agent/actions/runs/41295817959 로그 다운로드.
- [ ] artifact의 DATA_INVENTORY.csv, SOURCE_TEXT_MACHINE.jsonl, INVENTORY_REPORT.json, pytest/ruff 로그 및 의존성 목록 확인.
전용 workflow retention-days=14다. 로그 링크만 보관하지 말고 필요한 원본을 다운로드한다. 파일이 만료됐다면 원본 체크아웃에서 재검사하고 새 실행으로 구분한다.

## E. 새 AI에 처음 전달할 최소 묶음
1. NEXT_AI_PROMPT.txt 내용 붙여넣기.
2. START_HERE.md, STATE.json 첨부 또는 GitHub 경로 제공.
3. 최신 PDF_EVIDENCE_MATRIX.xlsx 원본 첨부.
4. 공용 현황/통합 계획/팀원3 지침과 설정 JSON 3종 첨부.
5. GitHub 연결 또는 해당 브랜치 소스 ZIP 제공.
6. 실제 Native JSON이 있으면 별도로 첨부하며 설정과 구분.

## F. 완료 판단
- [ ] 새 계정에서 인계 문서/소스/최신 XLSX/설정 원본을 열 수 있음.
- [ ] 새 환경에서 pytest/Ruff와 원본 검사 재현 또는 정확한 BLOCKED 기록.
- [ ] 원본 바이트 SHA를 새 환경에서 계산해 인계 manifest 추가.
- [ ] 백업 사본을 최소 한 곳 더 보관.
위 조건 전에는 기존 계정을 먼저 삭제하지 않는다. 계정 만료/요금/보존 정책은 해당 서비스에서 확인한다. 비밀번호, OAuth 토큰, 쿠키, API 키, 만료되는 서명 URL은 백업 문서에 넣지 않는다.
