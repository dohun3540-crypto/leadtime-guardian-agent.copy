# B0/E1 experiment readiness

정식 비교는 **BLOCKED, 완전한 증거 묶음 0/4, 개선율 NOT_MEASURED**다. 과거 Job을 신규 측정으로 다시 세지 않는다.

| 조합 | 보관 관찰 | 정식 비교 상태 | 부족한 증거 |
| --- | --- | --- | --- |
| B0-C001 | B0 candidate job_NCik8shwrgM93PDnNNYukT, cfg_X2xXakDtmDTHh2RoqVysvL/v1; Normalize/QA/Parse/Classify/Extract retained | BLOCKED | alias registry, 원래 Agent/복사 이력·실행 config 결합, receipts, QA input/trace, 동일-input Team2 원본, approved Gold |
| E1-C001 | UNASSIGNED v2 job_RpJUGhdMWSH6iww476BjFJ; UI 설정2, 보관 cfg_bXh7dAFikuFp3rajaSWGgb; Normalize 이번 회수 | BLOCKED | E1 alias 미인증; 위와 같은 complete bundle 누락 |
| B0-C013 | v4 C013 보관 출력은 있으나 B0로 재지정하지 않음 | BLOCKED | B0-C013 고유 실행 묶음 |
| E1-C013 | 인증된 E1-C013 없음 | BLOCKED | E1-C013 고유 실행 묶음 |

B0 export의 exportedFrom.workflowId는 agt_HdtUJPQPXir9rGKgPWSyZG, v2 export는 agt_NMzLzoiRQz8DZJ4Ymsf8PL이다. 이름이 비슷하다는 이유로 Agent/alias/현재 운영 실행을 동일시하지 않는다. 보관 config 차이는 workflow_name과 네 numeric-null flag가 중심이며, export 시점의 draft가 과거 Job 당시 프롬프트였다는 인증은 없다.

새로 회수한 v2 Normalize와 보관 QA는 같은 Job·세 source row를 가진다. Native envelope 로컬 계약 PASS, Python local replay60500.00 KRW. QA verdict NOT_VERIFIED와 NORMALIZED_OUTPUT_NOT_PROVIDED는 그대로다. 이것은 구성별 정확도나 개선의 실측 증거가 아니다.

각 조합에서 PDF 3종 SHA/File receipt → Parse/Classify/Extract/Merge/Normalize/실제 QA Input/QA Report의 Job·Config·Step 결합 → 동일 Native SHA의 Team2 결과·Sidecar → 사람 승인 Gold 순으로 확인한다. 입력 PDF 바이트·runtime config·alias가 검증되기 전에는 버전 간 값을 합치거나 성공률을 계산하지 않는다. 비용 발생 실행은 하지 않았다.
