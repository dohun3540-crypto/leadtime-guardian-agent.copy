# 다음 재개 우선순위

1. **A BLOCKED** — C001/C013의 실제 IndependentQA 입력 원본, raw Merge 출력, provider 단계별 input/output·Step Run 연결 및 업로드 receipt를 확보한다. Normalize 출력과 QA 입력의 바이트/내용 동일성을 검사한다. QA 출력, 같은 Job, config edge는 실제 QA 입력 증거를 대신하지 않는다.
2. **B BLOCKED, 공식 0/4** — 승인된 B0/E1 별칭→Agent/Config/Job 매핑을 확보하고 B0-C001/E1-C001/B0-C013/E1-C013의 PDF 동일성·단계·QA Input/Output·동일 Native V6/Sidecar·Gold를 연결한다. `job_RpJUGhdMWSH6iww476BjFJ` v2는 아직 E1으로 확정하지 않는다. 이번 회수는 과거 실행 조회이며 신규 실측이 아니다.
3. **윤현준** — 위와 동일한 운영 Native 원본 바이트를 받은 본인 실행의 V6 결과와 원본 provenance sidecar를 인계한다. Team 1이 만든 로컬 replay sidecar를 Team 2 원본으로 승격하지 않는다. 공개 공유·메시지 전송은 하지 않았다.
4. **김민주** — 사람 검수 XLSX, 원문 PDF 근거, 검수자 승인과 Gold freeze를 인계한다. 기존 DRAFT 또는 export의 gold 폴더는 승인 Gold가 아니다. 공식 정확도는 그 후 계산한다.
5. **C PASS_LOCAL** — 정확한 40개 정적 검토는 완료했다. 실제 nullable 동작은 미인증이다. 숫자 자동 null 옵션, 빈 quote[] 경로, other branch 미관찰을 고려한다. 실행 실패가 증명되기 전 일괄 nullable patch는 적용하지 않는다.
6. **D PASS_LOCAL** — 이번 C001 Preflight는 예외 없이 invalid_inputs=[]/BLOCKED/release_authorized=false를 반환했다. 실제 receipt·stage 원본이 들어오면 재검증한다. C013은 기존 Combined 도구를 사용한다.
7. **E PASS_LOCAL** — 기존 PR #25 CLI와 이 보완 매뉴얼로 C001/C013 및 선택적 C008/C017 시연을 재현한다. C017의 한국어 원문 추출·날짜 변환은 여전히 NOT_MEASURED다.
8. **F PASS_LOCAL / 원격 통합 BLOCKED** — 보존 5경로 patch의 정확한 기준 통합, 812/544 및 원래 778 ID 보존을 검증했다. 통합 저장소 push/merge는 하지 않는다. PR #25의 도구 3파일은 이 5경로 patch와 별도 범위이며, 통합 담당자가 필요 시 추가 검토한다.

새 유료 Studio 실행, 외부 제출, 구매, 기존 PR 병합, force push, Gold 승인은 수행하지 않는다. 누락 증거를 현존하는 것처럼 만들거나 과거 Job을 신규 실행으로 표시하지 않는다.

## PR 관계

- PR #24: 체크포인트, 보호 유지.
- PR #25: 체크포인트 이후 Schema/Replay 도구 3파일, 이 검증 중 발견한 기존 작업. 덮어쓰거나 close하지 않는다.
- 이 보완 브랜치 `feat/team1-resume-schema-demo-20261103-r2`: PR #25 고정 코드 커밋 `6929ea1dc29e1ad6c1d1c604dd1180968ef7ec1a` 위의 독립 검증 문서/인덱스만 추가한다. PR #24/#25를 대체하지 않는다.
- 원본 저장소·개인 main·PR #19/#20/#21/#23·통합 PR #2/원격 코드 동결은 유지한다.
