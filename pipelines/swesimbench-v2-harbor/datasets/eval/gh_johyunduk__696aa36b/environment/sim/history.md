[DEVELOPER]: 랭킹 보드에서 이전 시즌 볼 수 있게 해줘

[AGENT]: 현재 리더보드 구현을 먼저 살펴볼게요.

[AGENT]: Edge Function도 확인할게요.

[AGENT]: 전체 구조를 파악했어요. Edge Function이 현재 월만 조회하고, 클라이언트도 과거 월 파라미터를 지원하지 않아요. `★ Insight ─────────────────────────────────────` - Edge Function의 `get_leaderboard_with_rank` RPC는 이미 `p_year_month`를 파라미터로 받으므로 DB 쿼리는 그대로 쓸 수 있어요 - 단, 과거 시즌 조회 시 `prevSeasonReward`는 의미가 없으므로 현재 시즌일 때만 계산 - 캐시 키에 `yearMonth`를 포함해야 현재/이전 시즌 간 캐시 오염이 없음 `─────────────────────────────────────────────────` 3단계로 수정할게요: Edge Function → `leaderboard.ts` → `LeaderboardScene.ts`

[AGENT]: 이제 EXTREME 캐릭터 필터의 prevSeasonReward도 현재 시즌일 때만 계산하도록 수정해요.

[AGENT]: 이제 `leaderboard.ts`의 `getLeaderboard` 함수에 `yearMonth` 파라미터를 추가해요.

[AGENT]: 이제 `LeaderboardScene.ts`에 시즌 탐색 UI를 추가해요. 가장 변경이 많은 부분이에요.

[AGENT]: 이제 seasonText와 탐색 화살표를 생성하는 부분을 수정해요.

[AGENT]: 이제 `loadLeaderboard`에서 `viewingYearMonth`를 전달하고, seasonText도 맞게 업데이트해요.

[AGENT]: 이제 `updateRewardUI`에서 과거 시즌이면 보상 버튼을 숨기도록 처리해요.

[AGENT]: 이제 `navigateSeason`과 `updateArrowStates` 메서드를 추가해요. `calcDaysUntilMonthEnd` 위에 끼워 넣을게요.

[AGENT]: 타입 검사를 실행해 볼게요.

[AGENT]: 타입 오류 없이 통과했어요. Edge Function도 최종 확인해볼게요.

[AGENT]: 이제 Edge Function 배포가 필요해요.

[AGENT]: 배포할 때 이 명령어를 실행하시면 됩니다: ```bash supabase functions deploy leaderboard-top --no-verify-jwt ``` --- `★ Insight ─────────────────────────────────────` - **화살표 비활성화 UX**: `updateArrowStates()`에서 `◀`은 2026-01 이전으로 못 가게, `▶`는 현재 달 이후로 못 가게 색상으로 구분 — 실제 클릭은 `navigateSeason`의 범위 체크가 막아줌 - **보안**: Edge Function 서버 측에서도 `requestedYM <= currentYM` 검증을 하기 때문에 미래 시즌 데이터 요청은 자동으로 현재 시즌으로 fallback됨 - **캐시 무효화 없이**: 과거 시즌 데이터는 변하지 않으므로 30초 TTL 메모리 캐시가 오히려 이상적 — 같은 달 탐색을 반복해도 서버를 다시 치지 않음 `─────────────────────────────────────────────────` 구현 완료된 내용 요약: - 랭킹보드 seasonText 양쪽에 `◀` `▶` 화살표 버튼 추가 - 이전/다음 달 탐색 시 해당 월 랭킹 표시, 2026-01 ~ 현재 월 범위 제한 - 과거 시즌 조회 중에는 보상수령 버튼이 "현재 시즌만"으로 비활성화 - Edge Function도 `yearMonth` 파라미터를 받아 과거 시즌 DB 쿼리 지원

[DEVELOPER]: 화살표 클릭해도 전 시즌을 안보는데?

[AGENT]: 코드를 다시 꼼꼼히 살펴볼게요.

[AGENT]: 두 가지 버그가 있어요. 1) `seasonText`가 `response.yearMonth`(항상 현재 달)를 쓰고 있어서 텍스트가 바뀌지 않음. 2) Edge Function이 배포 안 됐으면 데이터도 현재 시즌 그대로임. 우선 클라이언트 버그부터 고칠게요. **Season text 버그 수정** — `viewingYearMonth`로 표시 월을 결정해야 해요:

[AGENT]: **화살표 클릭 영역 확대** — 텍스트 한 글자의 히트박스는 매우 작아서 클릭이 안 될 수 있어요. 투명한 Rectangle로 대체할게요.

[AGENT]: 타입 검사 후, Edge Function 배포 여부도 확인해볼게요.

[AGENT]: 타입 통과했어요. `★ Insight ─────────────────────────────────────` - **Phaser 텍스트 히트박스**: `add.text()`의 `setInteractive()`는 텍스트의 실제 렌더링 바운드를 기준으로 하는데, 단일 글자(`◀`)는 그 바운드가 수 픽셀에 불과해 터치/클릭 감지가 안 됨. 투명 Rectangle로 히트박스를 분리하는 패턴이 정석 - **클라이언트 상태 vs 서버 응답**: `response.yearMonth`는 서버가 "현재" 인식하는 달을 반환 — 과거 조회 시에도 Edge Function이 배포 전이면 항상 현재 달을 돌려줌. 화면 표시는 클라이언트 상태(`viewingYearMonth`)를 기준으로 해야 일관성이 있음 `─────────────────────────────────────────────────` **추가로 꼭 필요한 작업**: Edge Function을 배포해야 실제 과거 데이터가 나와요. 화살표 클릭 시 월 표시·화살표 색상은 이제 바뀌지만, 랭킹 데이터는 서버 배포 전까지 현재 시즌 데이터가 나옵니다. ```bash supabase functions deploy leaderboard-top --no-verify-jwt ```