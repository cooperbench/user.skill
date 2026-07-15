> DEVELOPER

랭킹 보드에서 이전 시즌 볼 수 있게 해줘

> AGENT

현재 리더보드 구현을 먼저 살펴볼게요.

> AGENT

Edge Function도 확인할게요.

> AGENT

전체 구조를 파악했어요. Edge Function이 현재 월만 조회하고, 클라이언트도 과거 월 파라미터를 지원하지 않아요. `★ Insight ─────────────────────────────────────` - Edge Function의 `get_leaderboard_with_rank` RPC는 이미 `p_year_month`를 파라미터로 받으므로 DB 쿼리는 그대로 쓸 수 있어요 - 단, 과거 시즌 조회 시 `prevSeasonReward`는 의미가 없으므로 현재 시즌일 때만 계산 - 캐시 키에 `yearMonth`를 포함해야 현재/이전 시즌 간 캐시 오염이 없음 `─────────────────────────────────────────────────` 3단계로 수정할게요: Edge Function → `leaderboard.ts` → `LeaderboardScene.ts`

> AGENT

이제 EXTREME 캐릭터 필터의 prevSeasonReward도 현재 시즌일 때만 계산하도록 수정해요.

> AGENT

이제 `leaderboard.ts`의 `getLeaderboard` 함수에 `yearMonth` 파라미터를 추가해요.

> AGENT

이제 `LeaderboardScene.ts`에 시즌 탐색 UI를 추가해요. 가장 변경이 많은 부분이에요.

> AGENT

이제 seasonText와 탐색 화살표를 생성하는 부분을 수정해요.

> AGENT

이제 `loadLeaderboard`에서 `viewingYearMonth`를 전달하고, seasonText도 맞게 업데이트해요.

> AGENT

이제 `updateRewardUI`에서 과거 시즌이면 보상 버튼을 숨기도록 처리해요.

> AGENT

이제 `navigateSeason`과 `updateArrowStates` 메서드를 추가해요. `calcDaysUntilMonthEnd` 위에 끼워 넣을게요.

> AGENT

타입 검사를 실행해 볼게요.

> AGENT

타입 오류 없이 통과했어요. Edge Function도 최종 확인해볼게요.

> AGENT

이제 Edge Function 배포가 필요해요.

> AGENT

배포할 때 이 명령어를 실행하시면 됩니다: ```bash supabase functions deploy leaderboard-top --no-verify-jwt ``` --- `★ Insight ─────────────────────────────────────` - **화살표 비활성화 UX**: `updateArrowStates()`에서 `◀`은 2026-01 이전으로 못 가게, `▶`는 현재 달 이후로 못 가게 색상으로 구분 — 실제 클릭은 `navigateSeason`의 범위 체크가 막아줌 - **보안**: Edge Function 서버 측에서도 `requestedYM <= currentYM` 검증을 하기 때문에 미래 시즌 데이터 요청은 자동으로 현재 시즌으로 fallback됨 - **캐시 무효화 없이**: 과거 시즌 데이터는 변하지 않으므로 30초 TTL 메모리 캐시가 오히려 이상적 — 같은 달 탐색을 반복해도 서버를 다시 치지 않음 `─────────────────────────────────────────────────` 구현 완료된 내용 요약: - 랭킹보드 seasonText 양쪽에 `◀` `▶` 화살표 버튼 추가 - 이전/다음 달 탐색 시 해당 월 랭킹 표시, 2026-01 ~ 현재 월 범위 제한 - 과거 시즌 조회 중에는 보상수령 버튼이 "현재 시즌만"으로 비활성화 - Edge Function도 `yearMonth` 파라미터를 받아 과거 시즌 DB 쿼리 지원