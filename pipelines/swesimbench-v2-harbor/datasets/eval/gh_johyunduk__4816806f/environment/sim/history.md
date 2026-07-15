[DEVELOPER]: 지금보면 난이도 별로 랭킹이 있는데 이것과 별개로 난이도 & 캐릭터별 랭킹이 따로 있으면 좋을거 같은데 어떻게 생각해?

[AGENT]: 좋은 아이디어입니다. 캐릭터별로 차별화된 전략이 있으니 "같은 캐릭터 유저끼리의 경쟁"이 의미 있는 맥락이 됩니다. 다만 핵심 트레이드오프는 **랭킹 희소성**입니다. 현재 21개 캐릭터 × 3 난이도 = 63개 리더보드가 생기는데, 유저가 분산되면 각 보드에 사람이 너무 적어져서 경쟁이 없어질 수 있습니다. 대안으로 **단일 리더보드에 캐릭터 정보를 같이 기록**하고, 화면에서 "내 캐릭터로 필터" 기능을 제공하는 방식이 더 실용적일 수 있습니다 — 데이터는 통합, 보기만 분리하는 구조요. 어떤 방향이 더 마음에 드세요?

[DEVELOPER]: 음 이거는 그러면 익스트림 모드만 캐릭터별 랭킹을 두는건 어떤가?

[AGENT]: EXTREME 전용 캐릭터 랭킹은 꽤 좋은 접근입니다. EXTREME은 고난이도 + 시즌 한정이라 유저 풀이 자연스럽게 좁혀지고, 캐릭터 능력이 생존에 직접 영향을 주니 "어떤 캐릭터로 얼마나 버텼나"가 의미 있는 지표가 됩니다. 코드베이스를 먼저 살펴보고 구체적인 구현 계획을 잡겠습니다.

[AGENT]: 좋습니다, 탐색 결과가 매우 명확합니다. 이미 DB에 `character_type` 컬럼이 있고 제출 시에도 캐릭터 ID가 전달되고 있어서, **데이터 인프라는 이미 준비된 상태**입니다. UI와 Edge Function 쿼리 필터만 추가하면 됩니다. 세부 코드 구조를 확인하고 계획을 작성하겠습니다.

[AGENT]: Edge Function 쿼리 구조도 확인하겠습니다.

[AGENT]: 이제 전체 구조가 파악됐습니다. 계획을 작성하겠습니다.

[DEVELOPER]: 근데 궁금한게 있어. 현재 랭킹 제출은 기존 기록을 넘은 경우에만 제출을 하는데 레거시로 2만점이고 무기로 처음하여 5천점을 달성했을 때 무기의 점수가 등록은 되어야 하는데 이땐 등록이 안되는 그런 상태 아닌가? 이거 고려해줘봐

[AGENT]: 정확히 짚었습니다. 현재 `leaderboard` 테이블의 PK가 `(user_id, difficulty, year_month)`이라서 사용자당 월 1개 기록만 존재합니다. 레거시로 2만점 → 무기로 5천점 시도 시, 5천 < 2만이라 UPDATE가 일어나지 않고 무기 점수는 사라집니다. 이 문제는 캐릭터 필터 기능과 함께 **필수로** 해결해야 합니다. 계획을 수정하겠습니다. **해결 방향**: PK를 `(user_id, difficulty, year_month, character_type)`으로 확장 - 캐릭터마다 독립적인 베스트 스코어 저장 - 전체 랭킹(필터 없음): DB 뷰(VIEW)로 "유저별 최고 점수"만 노출 - 캐릭터 필터 랭킹: 기본 테이블을 character_type으로 필터

[AGENT]: `★ Insight ─────────────────────────────────────` - **PK 확장 vs 별도 테이블**: PK를 `character_type`까지 확장하면 "캐릭터별 베스트 스코어" 의미가 테이블 구조에 직접 반영된다. 별도 테이블은 데이터 중복과 동기화 문제를 낳는다. - **VIEW 패턴**: 전체 랭킹 쿼리에 `DISTINCT ON` VIEW를 사용하면 Edge Function 코드 변경을 최소화하면서 "유저당 최고 1개" 보장이 가능하다. DB 계층이 비즈니스 로직을 흡수하는 좋은 예시. - **Migration의 안전성**: PK 확장은 기존 행을 삭제하지 않는다. 기존 데이터 `(user_id, difficulty, year_month, chibi)` 형태로 자연스럽게 마이그레이션됨. `─────────────────────────────────────────────────` 계획을 업데이트했습니다. 기존 계획에서 **DB 스키마 변경(Migration)** 이 핵심으로 추가됐고, `leaderboard-submit`의 conflict target 변경, `leaderboard-top`의 VIEW 분기가 추가됐습니다.

[DEVELOPER]: 테이블을 따로 구분하는건 어떻게 생각해?

[AGENT]: 좋은 포인트입니다. 두 접근의 핵심 트레이드오프를 정리하면: **기존 테이블 PK 확장** - 장점: 단일 진실 공급원, 데이터 정합성 - 단점: 프로덕션 테이블 마이그레이션 위험 + 전체 랭킹 쿼리가 `DISTINCT ON` / VIEW로 복잡해짐 + EXTREME 외 난이도까지 구조 변경이 파급됨 **별도 테이블 분리** - 장점: 기존 시스템 완전 무변경, EXTREME에만 한정, 쿼리 단순, 롤백 쉬움 - 단점: EXTREME 플레이 시 두 테이블에 각각 write 필요 (경미한 중복) 저는 **별도 테이블 쪽을 추천**합니다. 이 기능이 EXTREME 전용이고, 기존 `leaderboard`는 월별 보상 시스템과 얽혀 있어 PK를 건드리면 파급 범위가 넓습니다. 별도 테이블이면 기존 코드에 영향 없이 독립적으로 배포/롤백할 수 있습니다. 계획을 그 방향으로 수정할까요?

[DEVELOPER]: 그래 별도 테이블로 하자.

[AGENT]: 계획을 별도 테이블 방식으로 수정합니다.

[AGENT]: `★ Insight ─────────────────────────────────────` - **조건부 upsert 패턴**: Supabase JS 클라이언트는 `WHERE old.score < new.score` 같은 조건부 upsert를 직접 지원하지 않는다. SELECT → 비교 → upsert의 2-step 방식을 쓰거나, Postgres의 `INSERT ... ON CONFLICT DO UPDATE SET score = GREATEST(excluded.score, leaderboard_extreme_char.score)`를 raw SQL RPC로 호출하는 방법이 있다. 동시성이 중요하지 않은 게임 서버에선 2-step이 충분하다. - **별도 테이블의 롤백 용이성**: 기존 테이블 구조를 건드리지 않으므로 이 기능에 문제가 생겨도 `DROP TABLE leaderboard_extreme_char` 한 줄로 완전 롤백 가능하다. `─────────────────────────────────────────────────` 계획이 별도 테이블 방식으로 업데이트됐습니다. 기존 `leaderboard` 테이블은 완전 무변경이고, EXTREME 플레이 시에만 `leaderboard_extreme_char`에 추가 write하는 구조입니다.

[AGENT]: 구현을 시작하겠습니다. 순서대로 진행합니다. 먼저 `leaderboard-submit` 전체 코드와 migration 폴더 구조를 확인하겠습니다.

[AGENT]: 코드 구조 파악이 완료됐습니다. 5개 파일을 순서대로 구현합니다. `★ Insight ─────────────────────────────────────` - `safeCharacterType` 계산이 현재 `if (isNewRecord)` 블록 안에 있어서 EXTREME 별도 upsert에서 재사용하려면 블록 밖으로 이동해야 합니다. - `profiles!inner(initials)` JOIN은 PostgREST가 FK 관계를 통해 자동으로 처리하므로, `leaderboard_extreme_char` 테이블도 `profiles(id)`를 FK로 참조해야 동일한 쿼리 패턴이 동작합니다. `─────────────────────────────────────────────────`

[AGENT]: 다음으로 `leaderboard-submit` Edge Function을 수정합니다.

[AGENT]: `leaderboard-top` Edge Function에 `characterType` 파라미터 분기를 추가합니다.

[AGENT]: 이제 캐릭터 필터 분기 로직을 추가합니다. 기존 리더보드 조회 이전에 삽입합니다.

[AGENT]: 클라이언트 유틸리티를 수정합니다.

[AGENT]: 마지막으로 `LeaderboardScene.ts`를 수정합니다. 새 프로퍼티, `selectDifficulty` 리셋, `loadLeaderboard` 수정, `updateCharFilterRow` 신규 메서드, `displayLeaderboard` startY 조정, `updateRewardUI` 필터 처리를 순서대로 적용합니다.

[AGENT]: `displayLeaderboard()`의 `startY`를 조정합니다.

[AGENT]: `updateRewardUI()`에 필터 활성 시 숨김 처리를 추가합니다.

[AGENT]: 이제 `updateCharFilterRow()` 메서드를 추가합니다. `calcDaysUntilMonthEnd()` 바로 앞에 삽입합니다.

[AGENT]: `loadLeaderboard`에서 `// 이미 새로운 요청이 시작됨 - 이 응답은 무시` 주석이 있던 줄도 제거됐는지 확인하고, TypeScript 타입 검사를 실행합니다.

[AGENT]: 타입 에러 없음을 확인했습니다. 전체 구현 결과를 검토합니다.

[AGENT]: 코드가 의도대로 적용됐습니다. 구현 완료 내용을 정리합니다. --- **변경된 파일 5개:** 1. **`supabase/migrations/20260515_leaderboard_extreme_char.sql`** (신규) — `leaderboard_extreme_char` 테이블 생성. PK `(user_id, year_month, character_type)`, RLS 포함 2. **`supabase/functions/leaderboard-submit/index.ts`** — `safeCharacterType` 계산을 블록 밖으로 이동. EXTREME 플레이 시 캐릭터별 테이블에 추가 upsert (캐릭터당 베스트 스코어 갱신) 3. **`supabase/functions/leaderboard-top/index.ts`** — `characterType` 파라미터 파싱 추가. EXTREME + 캐릭터 필터 요청 시 `leaderboard_extreme_char` 조회 후 조기 반환 4. **`src/utils/leaderboard.ts`** — `getLeaderboard(difficulty, limit, characterType?)` 파라미터 추가 5. **`src/scenes/LeaderboardScene.ts`** — EXTREME 탭 선택 시 캐릭터 필터 칩 행 표시. 난이도 전환 시 필터 초기화. 캐릭터 필터 활성 시 보상 버튼 비활성화 **배포 순서**: migration 먼저 실행 → `leaderboard-submit` 배포 → `leaderboard-top` 배포

[DEVELOPER]: 배포 순서 그거 쿼리랑 명령어 순서대로 뭐 날려야 하는지 알려줘

[AGENT]: 순서대로 실행하면 됩니다: **1단계 — DB Migration (Supabase 대시보드 SQL Editor에서 직접 실행)** `supabase/migrations/20260515_leaderboard_extreme_char.sql` 파일 내용을 그대로 붙여넣기: ```sql CREATE TABLE IF NOT EXISTS leaderboard_extreme_char ( user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE, year_month TEXT NOT NULL, character_type TEXT NOT NULL DEFAULT 'chibi', score INTEGER NOT NULL DEFAULT 0, season INTEGER NOT NULL DEFAULT 1, updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), PRIMARY KEY (user_id, year_month, character_type) ); CREATE INDEX IF NOT EXISTS idx_extreme_char_score ON leaderboard_extreme_char (year_month, character_type, score DESC); ALTER TABLE leaderboard_extreme_char ENABLE ROW LEVEL SECURITY; CREATE POLICY "extreme_char_read_all" ON leaderboard_extreme_char FOR SELECT USING (true); CREATE POLICY "extreme_char_insert_own" ON leaderboard_extreme_char FOR INSERT WITH CHECK (auth.uid() = user_id); CREATE POLICY "extreme_char_update_own" ON leaderboard_extreme_char FOR UPDATE USING (auth.uid() = user_id); ``` **2단계 — Edge Function 배포 (터미널에서 순서대로)** ```bash supabase functions deploy leaderboard-submit --no-verify-jwt ``` ```bash supabase functions deploy leaderboard-top --no-verify-jwt ``` --- migration을 CLI(`supabase db push`)로 날리지 않고 대시보드 SQL Editor를 쓰는 이유는, 기존 migration 파일들이 이미 원격에 적용된 상태라서 `db push`를 날리면 이전 migration도 재실행 시도할 수 있기 때문입니다. SQL Editor에서 직접 실행하는 게 안전합니다.

[DEVELOPER]: 마크다운 파일로 만들어줘

[AGENT]: `docs/deploy-extreme-char-leaderboard.md` 에 저장했습니다.

[DEVELOPER]: supabase functions deploy leaderboard-submit --no-verify-jwt 얘는 왜 하는거지?

[AGENT]: `leaderboard-submit`은 EXTREME 플레이 시 `leaderboard_extreme_char` 테이블에 추가 write하는 코드를 이번에 넣었기 때문입니다. 코드가 바뀌었으니 배포해야 변경사항이 반영됩니다. 배포 안 하면 서버에는 이전 코드가 그대로 남아서, EXTREME 플레이해도 `leaderboard_extreme_char`에 아무것도 쌓이지 않습니다.

[DEVELOPER]: supabase functions deploy leaderboard-top --no-verify-jwt 이건 그러면 뭔데?

[AGENT]: `leaderboard-top`도 이번에 코드를 바꿨기 때문입니다. `characterType` 파라미터를 받아서 `leaderboard_extreme_char` 테이블을 조회하는 분기를 추가했는데, 배포 안 하면 서버에는 이전 코드가 남아서 캐릭터 필터 칩을 눌러도 항상 전체 랭킹만 반환합니다.

[DEVELOPER]: 3개 다 했어. 로컬에서 테스트만 해보면 되나?

[AGENT]: 네, 로컬에서 `npm run dev`로 켜고 아래 순서로 확인하면 됩니다. **게임플레이 검증** 1. EXTREME 난이도로 플레이 후 점수 제출 2. Supabase 대시보드 → Table Editor → `leaderboard_extreme_char` 에 행 생성 확인 3. 다른 캐릭터로 다시 플레이 → 캐릭터별 독립 행 2개 존재 확인 **UI 검증** 1. 랭킹보드 → EXTREME 탭 → 캐릭터 필터 칩 행 표시 확인 2. 캐릭터 칩 클릭 → 해당 캐릭터 점수만 필터링 확인 3. EXTREME → HARD 탭 전환 → 필터 행 사라짐 확인 **회귀 확인** - NORMAL/HARD 랭킹 정상 작동 확인 (기존 테이블 무변경이라 문제없어야 함)

[DEVELOPER]: 센티넬로 플레이 했는데 아무런 네트워크 통신도 없는ㄷ[ㅔ?

[AGENT]: 좀 더 구체적으로 알아야 할 것 같습니다. 어느 시점에서 네트워크 통신이 없나요?