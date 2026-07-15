> DEVELOPER

랭킹 보드에 플레이했던 캐릭터를 저장은 하고 있었는데 점수 제출시 근데 랭킹에 표시는 아직 안해주고 있었거든. 이거 표시해 줄 수 있니? 어떤 캐릭터를 플레이 했는지?

> AGENT

현재 구현 상태를 먼저 파악해 볼게요.

> TOOL

tool_use Bash
id: toolu_01Ur3mchsAeUBfeaAfYgsS1f
```json
{
  "command": "find /Users/johyunduk/Projects/ddong-avoid-game/src -name \"*.ts\" | xargs grep -l \"character\\|initials\\|leaderboard\" -i | grep -v node_modules",
  "description": "Find leaderboard and character related files"
}
```

> TOOL

tool_result
id: toolu_01Ur3mchsAeUBfeaAfYgsS1f
```
/Users/johyunduk/Projects/ddong-avoid-game/src/main.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/GameScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/BattleLeaderboardScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/BattleMatchScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/GachaScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/CharacterSelectScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/ModeSelectScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/BattleResultScene.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/types/toss-sdk.d.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/types/BattleTypes.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/config/synergyMap.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/character.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/battleChannel.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/tossSDK.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/leaderboard.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/battleTier.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/wallpaper.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/gacha.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/utils/battleLeaderboard.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/abilities/BaseAbility.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/abilities/types.ts
/Users/johyunduk/Projects/ddong-avoid-game/src/abilities/index.ts
```

> TOOL

tool_use Bash
id: toolu_01Gfvdq9TtqUo5cg64m9tJWu
```json
{
  "command": "find /Users/johyunduk/Projects/ddong-avoid-game/supabase -name \"*.ts\" | head -20",
  "description": "List supabase function files"
}
```

> TOOL

tool_result
id: toolu_01Gfvdq9TtqUo5cg64m9tJWu
```
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/gacha-pull/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/game-start/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/skor-submit/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-submit/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/claim-season-reward/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-top/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/battle-leaderboard-top/index.ts
/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/battle-result-submit/index.ts
```

> TOOL

tool_use Read
id: toolu_018ArW8ApmWr47rDUBAezLkz
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/utils/leaderboard.ts"
}
```

> TOOL

tool_result
id: toolu_018ArW8ApmWr47rDUBAezLkz
```
1	import { type Difficulty } from '../types/GameMode';
2	import { getCurrentUserId } from './auth';
3	import { supabase } from './supabase';
4	import { getCurrentYearMonth } from './localStorage';
5	
6	export interface LeaderboardEntry {
7	  userId: string;
8	  userName: string;
9	  score: number;
10	  rank: number;
11	  characterType?: string;
12	}
13	
14	export interface SubmitScoreResponse {
15	  success: boolean;
16	  isNewRecord: boolean;
17	  previousScore: number | null;
18	  newScore: number;
19	  rank: number | null;
20	  message?: string;
21	}
22	
23	export interface PrevSeasonReward {
24	  yearMonth: string;       // 'YYYY-MM' (직전 달)
25	  rank: number | null;     // null이면 해당 달 기록 없음
26	  skorAwarded: number;     // 0이면 100위 밖
27	  alreadyClaimed: boolean;
28	}
29	
30	export interface LeaderboardResponse {
31	  success: boolean;
32	  difficulty: string;
33	  yearMonth: string;       // 현재 시즌 'YYYY-MM'
34	  season: number;          // 시즌 번호
35	  leaderboard: LeaderboardEntry[];
36	  currentUserRank: {
37	    rank: number;
38	    score: number;
39	  } | null;
40	  totalEntries: number;
41	  prevSeasonReward: PrevSeasonReward | null;
42	}
43	
44	export interface ClaimRewardResponse {
45	  success: boolean;
46	  alreadyClaimed: boolean;
47	  rank: number | null;
48	  skorAwarded: number;
49	  newBalance?: number;
50	}
51	
52	/**
53	 * 사용자 ID 조회 (Supabase Auth 기반)
54	 */
55	export async function getUserId(): Promise<string> {
56	  return getCurrentUserId();
57	}
58	
59	/**
60	 * 사용자 이니셜 조회
61	 */
62	export function getUserInitials(): string | null {
63	  return localStorage.getItem('userInitials');
64	}
65	
66	/**
67	 * 사용자 이니셜 저장
68	 * @param initials 3자리 영어 대문자 (예: "ABC")
69	 */
70	export function setUserInitials(initials: string): boolean {
71	  const validation = /^[A-Z]{3}$/;
72	  if (!validation.test(initials)) {
73	    return false;
74	  }
75	
76	  localStorage.setItem('userInitials', initials);
77	  return true;
78	}
79	
80	/**
81	 * 이니셜이 설정되어 있는지 확인
82	 */
83	export function hasUserInitials(): boolean {
84	  const initials = getUserInitials();
85	  return initials !== null && /^[A-Z]{3}$/.test(initials);
86	}
87	
88	export interface ScoreVerificationData {
89	  gameStartTime: number;
90	  gameEndTime: number;
91	  goldCollected: number;
92	  diamondCollected: number;
93	  topazCollected: number;
94	  rainbowCollected: number;
95	  collectBonusTotal?: number; // ability.onCollectSpecial + synergy.collectBonus 누계
96	  abilityBonusTotal?: number; // addAbilityBonus() + getTickScore 배율 초과분 누계 (레거시 불태우기, 아카이브 배율 등)
97	}
98	
99	/**
100	 * 게임 세션 시작 — 서버가 start_time을 기록하여 점수 조작 방지
101	 */
102	export async function startGameSession(difficulty: Difficulty): Promise<string | null> {
103	  try {
104	    const { data, error } = await supabase.functions.invoke('game-start', {
105	      body: { difficulty },
106	    });
107	    if (error || !data?.sessionId) return null;
108	    return data.sessionId as string;
109	  } catch {
110	    return null;
111	  }
112	}
113	
114	/**
115	 * 점수 제출
116	 */
117	export async function submitScore(
118	  score: number,
119	  difficulty: Difficulty,
120	  initials: string,
121	  verificationData: ScoreVerificationData,
122	  characterType: string = 'chibi',
123	  sessionId: string | null = null
124	): Promise<SubmitScoreResponse> {
125	  if (!/^[A-Z]{3}$/.test(initials)) {
126	    throw new Error('Invalid initials: must be 3 uppercase letters');
127	  }
128	
129	  const { data, error } = await supabase.functions.invoke('leaderboard-submit', {
130	    body: {
131	      score,
132	      difficulty,
133	      userName: initials,
134	      sessionId,
135	      verification: verificationData,
136	      characterType,
137	    },
138	  });
139	
140	  if (error) {
141	    throw new Error(error.message || 'Failed to submit score');
142	  }
143	
144	  return data as SubmitScoreResponse;
145	}
146	
147	/**
148	 * 리더보드 조회
149	 */
150	export async function getLeaderboard(
151	  difficulty: Difficulty,
152	  limit: number = 100
153	): Promise<LeaderboardResponse> {
154	  const { data, error } = await supabase.functions.invoke('leaderboard-top', {
155	    body: { difficulty, limit },
156	  });
157	
158	  if (error) {
159	    throw new Error(error.message || 'Failed to fetch leaderboard');
160	  }
161	
162	  return data as LeaderboardResponse;
163	}
164	
165	// ── 시즌 보상 수령 캐시 (localStorage) ──────────────────────────────────
166	// 수령 완료된 시즌/난이도는 localStorage에 캐시해 불필요한 서버 조회 방지
167	// 보안: djb2 서명으로 변조 방지 (실제 이중 수령은 서버 UNIQUE 제약이 방어)
168	
169	const _CLAIMS_KEY = 'seasonRewardClaims';
170	const _CLAIMS_SIG_KEY = 'seasonRewardClaimsSig';
171	const _CLAIMS_SALT = 'ddong-reward-\u0076\u0031';
172	
173	function _djb2(str: string): string {
174	  let h = 5381;
175	  for (let i = 0; i < str.length; i++) {
176	    h = ((h << 5) + h) ^ str.charCodeAt(i);
177	    h = h >>> 0;
178	  }
179	  return h.toString(36);
180	}
181	
182	function _signClaims(claims: Record<string, number>): string {
183	  const str = Object.entries(claims)
184	    .sort(([a], [b]) => a.localeCompare(b))
185	    .map(([k, v]) => `${k}:${v}`)
186	    .join(',') + _CLAIMS_SALT;
187	  return _djb2(str);
188	}
189	
190	/** 현재 달 + 직전 달 외의 오래된 캐시 항목 제거 */
191	function _pruneOldClaims(claims: Record<string, number>): Record<string, number> {
192	  const now = new Date();
193	  const cur = getCurrentYearMonth();
194	  const prevDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - 1, 1));
195	  const prev = `${prevDate.getUTCFullYear()}-${String(prevDate.getUTCMonth() + 1).padStart(2, '0')}`;
196	  const keep = new Set([cur, prev]);
197	  return Object.fromEntries(
198	    Object.entries(claims).filter(([k]) => keep.has(k.slice(0, 7)))
199	  );
200	}
201	
202	function _loadClaimedCache(): Record<string, number> {
203	  try {
204	    const raw = localStorage.getItem(_CLAIMS_KEY);
205	    const sig = localStorage.getItem(_CLAIMS_SIG_KEY);
206	    if (!raw) return {};
207	    const parsed = JSON.parse(raw) as Record<string, number>;
208	    if (sig && sig !== _signClaims(parsed)) {
209	      // 서명 불일치 → 변조로 판단, 초기화
210	      localStorage.removeItem(_CLAIMS_KEY);
211	      localStorage.removeItem(_CLAIMS_SIG_KEY);
212	      return {};
213	    }
214	    return parsed;
215	  } catch {
216	    return {};
217	  }
218	}
219	
220	function _saveClaimedCache(claims: Record<string, number>): void {
221	  const pruned = _pruneOldClaims(claims);
222	  localStorage.setItem(_CLAIMS_KEY, JSON.stringify(pruned));
223	  localStorage.setItem(_CLAIMS_SIG_KEY, _signClaims(pruned));
224	}
225	
226	/**
227	 * 해당 달/난이도의 보상을 이미 수령했는지 localStorage에서 확인
228	 * @returns 수령한 SKOR 양 (없으면 null)
229	 */
230	export function getCachedClaimAmount(yearMonth: string, difficulty: string): number | null {
231	  const cache = _loadClaimedCache();
232	  const key = `${yearMonth}_${difficulty}`;
233	  return key in cache ? cache[key] : null;
234	}
235	
236	/**
237	 * 직전 달 시즌 보상 수령
238	 */
239	export async function claimSeasonReward(difficulty: Difficulty): Promise<ClaimRewardResponse> {
240	  const { data, error } = await supabase.functions.invoke('claim-season-reward', {
241	    body: { difficulty },
242	  });
243	
244	  if (error) {
245	    throw new Error(error.message || 'Failed to claim reward');
246	  }
247	
248	  const result = data as ClaimRewardResponse;
249	
250	  // 수령 성공(또는 이미 수령) 시 localStorage 캐시 갱신
251	  if (result.success && result.skorAwarded && result.skorAwarded > 0) {
252	    const now = new Date();
253	    const prevDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth() - 1, 1));
254	    const prevYearMonth = `${prevDate.getUTCFullYear()}-${String(prevDate.getUTCMonth() + 1).padStart(2, '0')}`;
255	    const cache = _loadClaimedCache();
256	    cache[`${prevYearMonth}_${difficulty}`] = result.skorAwarded;
257	    _saveClaimedCache(cache);
258	  }
259	
260	  return result;
261	}
262	
```

> TOOL

tool_use Read
id: toolu_01MVuzgzyVg1Tioi2dya67sT
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-submit/index.ts"
}
```

> TOOL

tool_result
id: toolu_01MVuzgzyVg1Tioi2dya67sT
```
1	import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
2	
3	/** 현재 달 'YYYY-MM' 반환 (UTC 기준) */
4	function getCurrentYearMonth(): string {
5	  const now = new Date();
6	  const y = now.getUTCFullYear();
7	  const m = String(now.getUTCMonth() + 1).padStart(2, '0');
8	  return `${y}-${m}`;
9	}
10	
11	/** 시즌 번호: 2026-01 = 1, 2026-02 = 2, ... */
12	function calcSeason(yearMonth: string): number {
13	  const [y, m] = yearMonth.split('-').map(Number) as [number, number];
14	  return (y - 2026) * 12 + m;
15	}
16	
17	const corsHeaders = {
18	  'Access-Control-Allow-Origin': '*',
19	  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
20	};
21	
22	// 난이도별 물리적 최대 점수 (2시간 연속 플레이 기준)
23	const SCORE_CAPS: Record<string, number> = {
24	  easy: 10000,
25	  normal: 15000,
26	  hard: 20000,
27	  extreme: 99999,
28	  physical: 99999,
29	};
30	
31	// 어빌리티 보너스 상한: 점수의 이 비율까지 허용 (나머지는 최소한 시간 기반이어야 함)
32	const ABILITY_BONUS_CAP_RATIO = 0.95;
33	
34	Deno.serve(async (req: Request) => {
35	  if (req.method === 'OPTIONS') {
36	    return new Response('ok', { headers: corsHeaders });
37	  }
38	
39	  try {
40	    const { score, difficulty, userName, sessionId, verification, characterType } = await req.json();
41	
42	    // 기본 입력 검증
43	    if (typeof score !== 'number' || score < 0) {
44	      return new Response(
45	        JSON.stringify({ error: 'Invalid score' }),
46	        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
47	      );
48	    }
49	
50	    const validDifficulties = ['easy', 'normal', 'hard', 'extreme', 'physical'];
51	    if (!validDifficulties.includes(difficulty)) {
52	      return new Response(
53	        JSON.stringify({ error: 'Invalid difficulty' }),
54	        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
55	      );
56	    }
57	
58	    if (!userName || !/^[A-Z]{3}$/.test(userName)) {
59	      return new Response(
60	        JSON.stringify({ error: 'Invalid userName: must be 3 uppercase letters' }),
61	        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
62	      );
63	    }
64	
65	    // 하드 캡: 물리적으로 불가능한 점수 차단
66	    if (score > (SCORE_CAPS[difficulty] ?? 10000)) {
67	      console.warn('Score exceeds hard cap', { score, difficulty });
68	      return new Response(
69	        JSON.stringify({ error: 'Score exceeds maximum possible value' }),
70	        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
71	      );
72	    }
73	
74	    // JWT 인증
75	    const authHeader = req.headers.get('Authorization');
76	    if (!authHeader) {
77	      return new Response(
78	        JSON.stringify({ error: 'Missing authorization header' }),
79	        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
80	      );
81	    }
82	
83	    const supabaseUser = createClient(
84	      Deno.env.get('SUPABASE_URL') ?? '',
85	      Deno.env.get('SUPABASE_ANON_KEY') ?? '',
86	      { global: { headers: { Authorization: authHeader } } }
87	    );
88	
89	    const { data: { user }, error: authError } = await supabaseUser.auth.getUser();
90	    if (authError || !user) {
91	      return new Response(
92	        JSON.stringify({ error: 'Unauthorized' }),
93	        { status: 401, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
94	      );
95	    }
96	
97	    const supabaseAdmin = createClient(
98	      Deno.env.get('SUPABASE_URL') ?? '',
99	      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
100	    );
101	
102	    // ── 세션 검증: 서버가 기록한 start_time 기준으로 경과 시간 확인 ──────────
103	    // UPDATE WHERE used=false RETURNING ... 패턴으로 원자적 검증 + 소비 처리
104	    // SELECT 후 UPDATE 방식은 동시 요청 시 race condition 가능 → 이 방식으로 방지
105	    if (sessionId) {
106	      const { data: session } = await supabaseAdmin
107	        .from('game_sessions')
108	        .update({ used: true })
109	        .eq('id', sessionId)
110	        .eq('used', false)
111	        .eq('user_id', user.id)
112	        .eq('difficulty', difficulty)
113	        .select('start_time')
114	        .single();
115	
116	      // null → 세션 없음 / 이미 사용됨 / 소유자 불일치 / 난이도 불일치 중 하나
117	      if (!session) {
118	        return new Response(
119	          JSON.stringify({ error: 'Invalid or already used session' }),
120	          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
121	        );
122	      }
123	
124	      // 서버 시각 기준 경과 시간으로 점수 타당성 검증
125	      const nowMs = Date.now();
126	      const serverStartMs = new Date(session.start_time).getTime();
127	      const elapsedMs = nowMs - serverStartMs;
128	      const elapsedSec = elapsedMs / 1000;
129	
130	      // 세션 만료 체크 (2시간 초과)
131	      if (elapsedMs > 2 * 60 * 60 * 1000) {
132	        return new Response(
133	          JSON.stringify({ error: 'Session expired' }),
134	          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
135	        );
136	      }
137	
138	      // 핵심 검증: 이 점수가 나오려면 최소 N초는 걸렸어야 함
139	      // 보너스 아이템(금똥/다이아/토파즈/무지개) + ability/synergy collectBonus는 시간 없이도 점수를 올리므로 제외
140	      // 1점 = 100ms → timeBasedScore점 = timeBasedScore * 0.1초, 50% 여유 적용
141	      const totalItemsCollected =
142	        (verification?.goldCollected ?? 0) +
143	        (verification?.diamondCollected ?? 0) +
144	        (verification?.topazCollected ?? 0) +
145	        (verification?.rainbowCollected ?? 0);
146	      // collectBonusTotal은 클라이언트 신고값이므로 수집 아이템당 최대 10점으로 상한 적용 (tampering 방지)
147	      const collectBonusTotal = Math.min(verification?.collectBonusTotal ?? 0, totalItemsCollected * 10);
148	      const rawAbilityBonus = verification?.abilityBonusTotal ?? 0;
149	      const abilityBonusTotal = Math.min(rawAbilityBonus, score * ABILITY_BONUS_CAP_RATIO);
150	      if (rawAbilityBonus > abilityBonusTotal) {
151	        console.warn('abilityBonusTotal clamped', { rawAbilityBonus, cap: score * ABILITY_BONUS_CAP_RATIO, score });
152	      }
153	      const bonusScore =
154	        (verification?.goldCollected ?? 0) * 20 +
155	        (verification?.diamondCollected ?? 0) * 40 +
156	        (verification?.topazCollected ?? 0) * 80 +
157	        (verification?.rainbowCollected ?? 0) * 90 +
158	        collectBonusTotal +
159	        abilityBonusTotal;
160	      const timeBasedScore = Math.max(0, score - bonusScore);
161	      const minRequiredSec = timeBasedScore * 0.1 * 0.5;
162	
163	      // Edge Function cold start 보정: 클라이언트 신고 시각 기준 경과를 추가 허용
164	      // session.start_time이 실제 게임 시작보다 늦을 수 있음 (cold start)
165	      // 클라이언트 신고 시각을 최대 20초 범위 내에서 신뢰 (tampering 방지용 상한)
166	      const clientStartMs = verification?.gameStartTime ?? null;
167	      const COLD_START_TOLERANCE_MS = 20_000;
168	      let adjustedElapsedSec = elapsedSec;
169	      if (clientStartMs && clientStartMs < serverStartMs) {
170	        const effectiveStartMs = Math.max(clientStartMs, serverStartMs - COLD_START_TOLERANCE_MS);
171	        adjustedElapsedSec = (nowMs - effectiveStartMs) / 1000;
172	      }
173	
174	      if (adjustedElapsedSec < minRequiredSec) {
175	        console.warn('Session time gate failed', { score, adjustedElapsedSec, minRequiredSec, elapsedSec });
176	        return new Response(
177	          JSON.stringify({ error: 'Score not achievable in elapsed time' }),
178	          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
179	        );
180	      }
181	    } else if (verification) {
182	      // 세션 없이 구 방식 verification만 있는 경우 (하위 호환)
183	      const {
184	        gameStartTime,
185	        gameEndTime,
186	        goldCollected = 0,
187	        diamondCollected = 0,
188	        topazCollected = 0,
189	        rainbowCollected = 0,
190	      } = verification;
191	
192	      const playDuration = gameEndTime - gameStartTime;
193	      const timeScore = Math.floor(playDuration / 100);
194	      const bonusScore =
195	        goldCollected * 20 +
196	        diamondCollected * 40 +
197	        topazCollected * 80 +
198	        rainbowCollected * 90;
199	      const expectedScore = timeScore + bonusScore;
200	      const tolerance = Math.max(expectedScore * 0.2, 10);
201	
202	      if (score > expectedScore + tolerance) {
203	        console.warn('Score verification failed', { score, expectedScore, playDuration });
204	        return new Response(
205	          JSON.stringify({ error: 'Score verification failed' }),
206	          { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
207	        );
208	      }
209	    }
210	
211	    // profiles 테이블에 이니셜 업데이트
212	    await supabaseAdmin
213	      .from('profiles')
214	      .update({ initials: userName })
215	      .eq('id', user.id);
216	
217	    const yearMonth = getCurrentYearMonth();
218	    const season = calcSeason(yearMonth);
219	
220	    // 현재 시즌 기존 점수 조회
221	    const { data: existing } = await supabaseAdmin
222	      .from('leaderboard')
223	      .select('score')
224	      .eq('user_id', user.id)
225	      .eq('difficulty', difficulty)
226	      .eq('year_month', yearMonth)
227	      .single();
228	
229	    const previousScore = existing?.score ?? null;
230	    const isNewRecord = previousScore === null || score > previousScore;
231	
232	    // 최고 점수만 저장 (upsert)
233	    if (isNewRecord) {
234	      const validCharacterTypes = [
235	        'chibi',
236	        'log', 'swap', 'sum', 'fork', 'seed', 'session', 'branch', 'hook', 'socket', 'index',
237	        'hacker', 'miner', 'maehwa', 'archieve', 'glitch', 'noise',
238	        'sentinel', 'legacy',
239	      ];
240	      const safeCharacterType = validCharacterTypes.includes(characterType) ? characterType : 'chibi';
241	
242	      const { error: upsertError } = await supabaseAdmin
243	        .from('leaderboard')
244	        .upsert(
245	          {
246	            user_id: user.id,
247	            difficulty,
248	            score,
249	            character_type: safeCharacterType,
250	            year_month: yearMonth,
251	            season,
252	            updated_at: new Date().toISOString(),
253	          },
254	          { onConflict: 'user_id,difficulty,year_month' }
255	        );
256	
257	      if (upsertError) {
258	        console.error('Upsert error:', upsertError);
259	        return new Response(
260	          JSON.stringify({ error: 'Failed to save score' }),
261	          { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
262	        );
263	      }
264	    }
265	
266	    // 현재 시즌 순위 계산
267	    const { count: rank } = await supabaseAdmin
268	      .from('leaderboard')
269	      .select('*', { count: 'exact', head: true })
270	      .eq('difficulty', difficulty)
271	      .eq('year_month', yearMonth)
272	      .gt('score', isNewRecord ? score : (previousScore ?? 0));
273	
274	    return new Response(
275	      JSON.stringify({
276	        success: true,
277	        isNewRecord,
278	        previousScore,
279	        newScore: isNewRecord ? score : (previousScore ?? score),
280	        rank: rank !== null ? rank + 1 : null,
281	      }),
282	      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
283	    );
284	  } catch (error) {
285	    console.error('Unexpected error:', error);
286	    return new Response(
287	      JSON.stringify({ error: 'Internal server error' }),
288	      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
289	    );
290	  }
291	});
292	
```

> TOOL

tool_use Read
id: toolu_01ANpPLkpBTygvf9cNajQTN7
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-top/index.ts"
}
```

> TOOL

tool_result
id: toolu_01ANpPLkpBTygvf9cNajQTN7
```
1	import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
2	
3	/** 현재 달 'YYYY-MM' 반환 (UTC 기준) */
4	function getCurrentYearMonth(): string {
5	  const now = new Date();
6	  const y = now.getUTCFullYear();
7	  const m = String(now.getUTCMonth() + 1).padStart(2, '0');
8	  return `${y}-${m}`;
9	}
10	
11	/** 직전 달 'YYYY-MM' 반환 */
12	function getPrevYearMonth(current: string): string {
13	  const [y, m] = current.split('-').map(Number) as [number, number];
14	  const prev = new Date(Date.UTC(y, m - 2, 1));
15	  return `${prev.getUTCFullYear()}-${String(prev.getUTCMonth() + 1).padStart(2, '0')}`;
16	}
17	
18	/** 시즌 번호: 2026-01 = 1, 2026-02 = 2, ... */
19	function calcSeason(yearMonth: string): number {
20	  const [y, m] = yearMonth.split('-').map(Number) as [number, number];
21	  return (y - 2026) * 12 + m;
22	}
23	
24	/** 난이도별 시즌 보상 티어 (퍼센타일 기반) */
25	const REWARD_TIERS = {
26	  normal:   { r1: 6000,  r2: 4000,  r3: 2000,  top10: 1000, top50: 600,  rest: 200 },
27	  hard:     { r1: 12000, r2: 8000,  r3: 4000,  top10: 2000, top50: 1200, rest: 400 },
28	  extreme:  { r1: 30000, r2: 20000, r3: 10000, top10: 5000, top50: 3000, rest: 1000 },
29	  physical: { r1: 30000, r2: 20000, r3: 10000, top10: 5000, top50: 3000, rest: 1000 },
30	} as const;
31	
32	type RewardDifficulty = keyof typeof REWARD_TIERS;
33	
34	function getReward(difficulty: string, rank: number, totalPlayers: number): number {
35	  const tier = REWARD_TIERS[difficulty as RewardDifficulty];
36	  if (!tier) return 0;
37	  if (rank === 1) return tier.r1;
38	  if (rank === 2) return tier.r2;
39	  if (rank === 3) return tier.r3;
40	  const percentile = rank / totalPlayers;
41	  if (percentile <= 0.10) return tier.top10;
42	  if (percentile <= 0.50) return tier.top50;
43	  return tier.rest;
44	}
45	
46	const corsHeaders = {
47	  'Access-Control-Allow-Origin': '*',
48	  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
49	};
50	
51	Deno.serve(async (req: Request) => {
52	  // CORS preflight
53	  if (req.method === 'OPTIONS') {
54	    return new Response('ok', { headers: corsHeaders });
55	  }
56	
57	  try {
58	    const { difficulty, limit: limitParam } = await req.json().catch(() => ({}));
59	    const limit = parseInt(limitParam ?? '100', 10);
60	
61	    // 입력 검증
62	    const validDifficulties = ['easy', 'normal', 'hard', 'extreme', 'physical'];
63	    if (!difficulty || !validDifficulties.includes(difficulty)) {
64	      return new Response(
65	        JSON.stringify({ error: 'Invalid difficulty' }),
66	        { status: 400, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
67	      );
68	    }
69	
70	    const safeLimit = Math.min(Math.max(1, limit), 100);
71	
72	    // JWT에서 사용자 인증 (선택적 — 비로그인 시에도 랭킹 조회 가능)
73	    const authHeader = req.headers.get('Authorization');
74	    let currentUserId: string | null = null;
75	
76	    if (authHeader) {
77	      const supabaseUser = createClient(
78	        Deno.env.get('SUPABASE_URL') ?? '',
79	        Deno.env.get('SUPABASE_ANON_KEY') ?? '',
80	        { global: { headers: { Authorization: authHeader } } }
81	      );
82	      const { data: { user } } = await supabaseUser.auth.getUser();
83	      currentUserId = user?.id ?? null;
84	    }
85	
86	    // Service Role 클라이언트 (profiles JOIN을 위해)
87	    const supabaseAdmin = createClient(
88	      Deno.env.get('SUPABASE_URL') ?? '',
89	      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? ''
90	    );
91	
92	    const yearMonth = getCurrentYearMonth();
93	    const prevYearMonth = getPrevYearMonth(yearMonth);
94	
95	    // 현재 시즌 리더보드 조회 (profiles와 JOIN하여 이니셜 포함)
96	    const { data: leaderboard, error: leaderboardError } = await supabaseAdmin
97	      .from('leaderboard')
98	      .select(`
99	        user_id,
100	        score,
101	        character_type,
102	        profiles!inner(initials)
103	      `)
104	      .eq('difficulty', difficulty)
105	      .eq('year_month', yearMonth)
106	      .order('score', { ascending: false })
107	      .limit(safeLimit);
108	
109	    if (leaderboardError) {
110	      console.error('Leaderboard query error:', leaderboardError);
111	      return new Response(
112	        JSON.stringify({ error: 'Failed to fetch leaderboard' }),
113	        { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
114	      );
115	    }
116	
117	    // 응답 형식 변환
118	    const entries = (leaderboard ?? []).map((entry, index) => ({
119	      userId: entry.user_id,
120	      userName: (entry.profiles as { initials: string | null }).initials ?? '???',
121	      score: entry.score,
122	      rank: index + 1,
123	      characterType: (entry as Record<string, unknown>).character_type ?? 'chibi',
124	    }));
125	
126	    const totalEntries = entries.length;
127	
128	    // 현재 유저의 이번 시즌 순위 조회
129	    let currentUserRank: { rank: number; score: number } | null = null;
130	    // 직전 시즌 보상 상태 (로그인 유저에게만 제공)
131	    let prevSeasonReward: {
132	      yearMonth: string;
133	      rank: number | null;
134	      skorAwarded: number;
135	      alreadyClaimed: boolean;
136	    } | null = null;
137	
138	    if (currentUserId) {
139	      // currentUserRank 조회와 prevSeason 보상 조회는 독립적이므로 병렬 실행
140	      const [userEntryResult, claimedResult, userPrevEntryResult] = await Promise.all([
141	        // 이번 시즌 점수
142	        supabaseAdmin.from('leaderboard').select('score')
143	          .eq('user_id', currentUserId).eq('difficulty', difficulty).eq('year_month', yearMonth).single(),
144	        // 직전 시즌 수령 이력 (easy 제외)
145	        difficulty !== 'easy'
146	          ? supabaseAdmin.from('season_reward_history').select('skor_awarded, rank')
147	              .eq('year_month', prevYearMonth).eq('user_id', currentUserId).eq('difficulty', difficulty).single()
148	          : Promise.resolve({ data: null, error: null }),
149	        // 직전 시즌 유저 점수 (easy 제외, 미수령 시 순위 계산용)
150	        difficulty !== 'easy'
151	          ? supabaseAdmin.from('leaderboard').select('score')
152	              .eq('user_id', currentUserId).eq('difficulty', difficulty).eq('year_month', prevYearMonth).single()
153	          : Promise.resolve({ data: null, error: null }),
154	      ]);
155	
156	      // 이번 시즌 순위
157	      const userEntry = userEntryResult.data;
158	      if (userEntry) {
159	        const { count: higherCount } = await supabaseAdmin
160	          .from('leaderboard')
161	          .select('*', { count: 'exact', head: true })
162	          .eq('difficulty', difficulty)
163	          .eq('year_month', yearMonth)
164	          .gt('score', userEntry.score);
165	
166	        currentUserRank = { rank: (higherCount ?? 0) + 1, score: userEntry.score };
167	      }
168	
169	      // 직전 시즌 보상 상태
170	      if (difficulty !== 'easy') {
171	        const claimed = claimedResult.data;
172	        if (claimed) {
173	          prevSeasonReward = {
174	            yearMonth: prevYearMonth,
175	            rank: claimed.rank,
176	            skorAwarded: claimed.skor_awarded,
177	            alreadyClaimed: true,
178	          };
179	        } else {
180	          const userPrevEntry = userPrevEntryResult.data;
181	          if (userPrevEntry) {
182	            // DB COUNT로 직전 시즌 순위 계산
183	            const [{ count: prevHigherCount }, { count: prevTotal }] = await Promise.all([
184	              supabaseAdmin.from('leaderboard').select('*', { count: 'exact', head: true })
185	                .eq('difficulty', difficulty).eq('year_month', prevYearMonth).gt('score', userPrevEntry.score),
186	              supabaseAdmin.from('leaderboard').select('*', { count: 'exact', head: true })
187	                .eq('difficulty', difficulty).eq('year_month', prevYearMonth),
188	            ]);
189	            const rank = (prevHigherCount ?? 0) + 1;
190	            prevSeasonReward = {
191	              yearMonth: prevYearMonth,
192	              rank,
193	              skorAwarded: getReward(difficulty, rank, prevTotal ?? 0),
194	              alreadyClaimed: false,
195	            };
196	          }
197	        }
198	      }
199	    }
200	
201	    return new Response(
202	      JSON.stringify({
203	        success: true,
204	        difficulty,
205	        yearMonth,
206	        season: calcSeason(yearMonth),
207	        leaderboard: entries,
208	        currentUserRank,
209	        totalEntries,
210	        prevSeasonReward,
211	      }),
212	      { headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
213	    );
214	  } catch (error) {
215	    console.error('Unexpected error:', error);
216	    return new Response(
217	      JSON.stringify({ error: 'Internal server error' }),
218	      { status: 500, headers: { ...corsHeaders, 'Content-Type': 'application/json' } }
219	    );
220	  }
221	});
222	
```

> TOOL

tool_use Read
id: toolu_0169XnCmUepjVfup7MmUce1S
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts"
}
```

> TOOL

tool_result
id: toolu_0169XnCmUepjVfup7MmUce1S
```
1	import type Phaser from 'phaser';
2	import { Difficulty, Difficulty as DifficultyEnum } from '../types/GameMode';
3	import {
4	  getLeaderboard,
5	  claimSeasonReward,
6	  getCachedClaimAmount,
7	  type LeaderboardEntry,
8	  type PrevSeasonReward,
9	} from '../utils/leaderboard';
10	import BaseScene from './BaseScene';
11	
12	export default class LeaderboardScene extends BaseScene {
13	  private selectedDifficulty: Difficulty = DifficultyEnum.NORMAL;
14	  private leaderboardData: LeaderboardEntry[] = [];
15	  private leaderboardTexts: Phaser.GameObjects.Text[] = [];
16	  private loadingText?: Phaser.GameObjects.Text;
17	  private errorText?: Phaser.GameObjects.Text;
18	  private currentRequestId: number = 0;
19	  private difficultyButtons = new Map<Difficulty, Phaser.GameObjects.Rectangle>();
20	
21	  // 시즌 UI 요소
22	  private seasonText?: Phaser.GameObjects.Text;
23	  private prevSeasonReward: PrevSeasonReward | null = null;
24	
25	  // 보상수령 버튼 (create에서 1회 생성, updateRewardUI에서 상태 변경)
26	  private rewardBtnBg?: Phaser.GameObjects.Rectangle;
27	  private rewardBtnLabel?: Phaser.GameObjects.Text;
28	
29	  constructor() {
30	    super('LeaderboardScene');
31	  }
32	
33	  init() {
34	    const last = localStorage.getItem('lastPlayedDifficulty') as Difficulty | null;
35	    if (last) {
36	      this.selectedDifficulty = last;
37	    }
38	  }
39	
40	  preload() {
41	    // 배경 이미지 로드 (캐시 확인으로 중복 로딩 방지)
42	    if (!this.textures.exists('background2')) {
43	      this.load.image('background2', 'assets/backgrounds/background2.webp');
44	    }
45	  }
46	
47	  create() {
48	    super.create();
49	
50	    const W = this.scale.width;
51	    const H = this.scale.height;
52	    const cx = W / 2;
53	    const yOff = (H - 600) / 2;
54	
55	    // 배경 이미지 추가
56	    const background = this.add.image(cx, H / 2, 'background2');
57	    background.setDisplaySize(W, H);
58	
59	    // 타이틀
60	    this.add.text(cx, 40 + yOff, '🏆 랭킹보드 🏆', {
61	      fontSize: '28px',
62	      color: '#fff',
63	      fontStyle: 'bold',
64	      stroke: '#000',
65	      strokeThickness: 5,
66	      padding: { top: 6 },
67	    }).setOrigin(0.5);
68	
69	    // 시즌 월 표시 (데이터 로드 후 갱신)
70	    this.seasonText = this.add.text(cx, 70 + yOff, '', {
71	      fontSize: '13px',
72	      color: '#aaddff',
73	      stroke: '#000',
74	      strokeThickness: 3,
75	    }).setOrigin(0.5);
76	
77	    // 난이도 선택 버튼들
78	    this.createDifficultyButtons(cx, yOff);
79	
80	    // 랭킹 표시 영역 (초기 로딩)
81	    this.loadingText = this.add.text(cx, H / 2, '로딩 중...', {
82	      fontSize: '20px',
83	      color: '#fff',
84	      stroke: '#000',
85	      strokeThickness: 3
86	    }).setOrigin(0.5);
87	
88	    // 보상수령 버튼 (하단 왼쪽, 뒤로가기와 나란히)
89	    const rbY = H - 40;
90	    this.rewardBtnBg = this.add.rectangle(cx - 80, rbY, 150, 40, 0x555555, 1);
91	    this.rewardBtnBg.setStrokeStyle(3, 0x333333);
92	    this.rewardBtnLabel = this.add.text(cx - 80, rbY, '보상수령', {
93	      fontSize: '18px',
94	      color: '#999999',
95	      fontStyle: 'bold',
96	      stroke: '#000',
97	      strokeThickness: 4,
98	    }).setOrigin(0.5);
99	
100	    // 뒤로가기 버튼 (하단 오른쪽)
101	    this.createBackButton(cx + 80, H - 40);
102	
103	    // 초기 데이터 로드
104	    this.loadLeaderboard();
105	  }
106	
107	  private createDifficultyButtons(cx: number, yOff: number) {
108	    this.difficultyButtons.forEach(btn => btn.destroy());
109	    this.difficultyButtons.clear();
110	
111	    const difficulties: Difficulty[] = [
112	      DifficultyEnum.NORMAL,
113	      DifficultyEnum.HARD,
114	      DifficultyEnum.EXTREME,
115	      DifficultyEnum.PHYSICAL
116	    ];
117	
118	    const buttonWidth = 70;
119	    const spacing = 85;
120	    const startX = cx - (spacing * 1.5);
121	    const y = 108 + yOff;
122	
123	    difficulties.forEach((difficulty, index) => {
124	      const x = startX + (index * spacing);
125	      const isSelected = difficulty === this.selectedDifficulty;
126	
127	      const button = this.add.rectangle(
128	        x,
129	        y,
130	        buttonWidth,
131	        35,
132	        isSelected ? 0xffff99 : 0xffffff,
133	        1
134	      );
135	      button.setStrokeStyle(3, isSelected ? 0xff0000 : 0x000000);
136	
137	      this.add.text(x, y, difficulty, {
138	        fontSize: '12px',
139	        color: '#000',
140	        fontStyle: 'bold'
141	      }).setOrigin(0.5);
142	
143	      this.difficultyButtons.set(difficulty, button);
144	      button.setInteractive({ useHandCursor: true });
145	
146	      button.on('pointerover', () => {
147	        if (difficulty !== this.selectedDifficulty) {
148	          button.setFillStyle(0xffffcc);
149	        }
150	      });
151	
152	      button.on('pointerout', () => {
153	        if (difficulty !== this.selectedDifficulty) {
154	          button.setFillStyle(0xffffff);
155	        }
156	      });
157	
158	      button.on('pointerdown', () => {
159	        this.selectDifficulty(difficulty);
160	      });
161	    });
162	  }
163	
164	  private selectDifficulty(difficulty: Difficulty) {
165	    // 같은 난이도면 무시
166	    if (this.selectedDifficulty === difficulty) {
167	      return;
168	    }
169	
170	    this.selectedDifficulty = difficulty;
171	
172	    // 모든 버튼 스타일 재설정
173	    this.difficultyButtons.forEach((btn, diff) => {
174	      const isSelected = diff === difficulty;
175	      btn.setFillStyle(isSelected ? 0xffff99 : 0xffffff);
176	      btn.setStrokeStyle(3, isSelected ? 0xff0000 : 0x000000);
177	    });
178	
179	    // 새로운 난이도 데이터 로드
180	    this.loadLeaderboard();
181	  }
182	
183	  private async loadLeaderboard() {
184	    // 요청 ID 증가 (새로운 요청 시작)
185	    this.currentRequestId++;
186	    const requestId = this.currentRequestId;
187	
188	    // 기존 랭킹 텍스트 제거
189	    this.leaderboardTexts.forEach(text => text.destroy());
190	    this.leaderboardTexts = [];
191	    this.prevSeasonReward = null;
192	
193	    if (this.errorText) {
194	      this.errorText.destroy();
195	      this.errorText = undefined;
196	    }
197	
198	    // 로딩 표시
199	    if (!this.loadingText) {
200	      this.loadingText = this.add.text(this.scale.width / 2, this.scale.height / 2, '로딩 중...', {
201	        fontSize: '20px',
202	        color: '#fff',
203	        stroke: '#000',
204	        strokeThickness: 3
205	      }).setOrigin(0.5);
206	    } else {
207	      this.loadingText.setVisible(true);
208	    }
209	
210	    try {
211	      const response = await getLeaderboard(this.selectedDifficulty, 10);
212	
213	      // 응답이 도착했을 때 최신 요청인지 확인
214	      if (requestId !== this.currentRequestId) {
215	        // 이미 새로운 요청이 시작됨 - 이 응답은 무시
216	        return;
217	      }
218	
219	      this.leaderboardData = response.leaderboard;
220	
221	      // 시즌 텍스트 갱신
222	      if (this.seasonText && response.yearMonth) {
223	        const [y, m] = response.yearMonth.split('-');
224	        const daysLeft = this.calcDaysUntilMonthEnd();
225	        this.seasonText.setText(`${y}년 ${parseInt(m)}월 시즌  |  시즌 종료까지 D-${daysLeft}`);
226	      }
227	
228	      // 직전 달 보상 상태 결정 (localStorage 캐시 우선)
229	      if (response.yearMonth) {
230	        const [y, m] = response.yearMonth.split('-').map(Number) as [number, number];
231	        const prevDate = new Date(Date.UTC(y, m - 2, 1));
232	        const prevYM = `${prevDate.getUTCFullYear()}-${String(prevDate.getUTCMonth() + 1).padStart(2, '0')}`;
233	        const cached = getCachedClaimAmount(prevYM, this.selectedDifficulty);
234	        if (cached !== null) {
235	          // localStorage 캐시 히트 → 서버 응답의 prevSeasonReward 무시하고 캐시 사용
236	          this.prevSeasonReward = {
237	            yearMonth: prevYM,
238	            rank: response.prevSeasonReward?.rank ?? null,
239	            skorAwarded: cached,
240	            alreadyClaimed: true,
241	          };
242	        } else {
243	          this.prevSeasonReward = response.prevSeasonReward;
244	        }
245	      } else {
246	        this.prevSeasonReward = null;
247	      }
248	
249	      if (this.loadingText) {
250	        this.loadingText.setVisible(false);
251	      }
252	
253	      this.displayLeaderboard();
254	      this.updateRewardUI();
255	    } catch (error) {
256	      // 에러가 발생했을 때도 최신 요청인지 확인
257	      if (requestId !== this.currentRequestId) {
258	        // 이미 새로운 요청이 시작됨 - 이 에러는 무시
259	        return;
260	      }
261	
262	      console.error('Failed to load leaderboard:', error);
263	
264	      if (this.loadingText) {
265	        this.loadingText.setVisible(false);
266	      }
267	
268	      this.errorText = this.add.text(this.scale.width / 2, this.scale.height / 2, '랭킹을 불러올 수 없습니다\n\n나중에 다시 시도해주세요', {
269	        fontSize: '16px',
270	        color: '#ff6666',
271	        stroke: '#000',
272	        strokeThickness: 3,
273	        align: 'center'
274	      }).setOrigin(0.5);
275	    }
276	  }
277	
278	  private displayLeaderboard() {
279	    const yOff = (this.scale.height - 600) / 2;
280	    const cx = this.scale.width / 2;
281	    const startY = 163 + yOff;
282	    const lineHeight = 35;
283	
284	    // 헤더
285	    const headerText = this.add.text(cx, startY, '순위    이름      점수', {
286	      fontSize: '16px',
287	      color: '#ffff00',
288	      fontStyle: 'bold',
289	      stroke: '#000',
290	      strokeThickness: 4
291	    }).setOrigin(0.5);
292	    this.leaderboardTexts.push(headerText);
293	
294	    // 랭킹 데이터 표시
295	    if (this.leaderboardData.length === 0) {
296	      const noDataText = this.add.text(cx, startY + 50, '아직 랭킹이 없습니다\n\n첫 번째 플레이어가 되어보세요!', {
297	        fontSize: '18px',
298	        color: '#ccc',
299	        stroke: '#000',
300	        strokeThickness: 3,
301	        align: 'center'
302	      }).setOrigin(0.5);
303	      this.leaderboardTexts.push(noDataText);
304	      return;
305	    }
306	
307	    this.leaderboardData.forEach((entry, index) => {
308	      const y = startY + 30 + (index * lineHeight);
309	
310	      // 순위별 색상
311	      let color = '#ffffff';
312	      if (entry.rank === 1) color = '#FFD700'; // 금색
313	      else if (entry.rank === 2) color = '#C0C0C0'; // 은색
314	      else if (entry.rank === 3) color = '#CD7F32'; // 동색
315	
316	
317	      const rankText = `${entry.rank}`.padEnd(8, ' ');
318	      const nameText = entry.userName.padEnd(8, ' ');
319	      const scoreText = entry.score.toString().padStart(6, ' ');
320	
321	      const text = this.add.text(
322	        cx,
323	        y,
324	        `${rankText}${nameText}${scoreText}`,
325	        {
326	          fontSize: '16px',
327	          color: color,
328	          fontFamily: 'monospace',
329	          stroke: '#000',
330	          strokeThickness: 3
331	        }
332	      ).setOrigin(0.5);
333	
334	      this.leaderboardTexts.push(text);
335	    });
336	  }
337	
338	  /** 이번 달 말일까지 남은 일수 */
339	  private calcDaysUntilMonthEnd(): number {
340	    const now = new Date();
341	    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
342	    const diff = lastDay.getTime() - now.getTime();
343	    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
344	  }
345	
346	  /** 보상수령 버튼 상태 갱신 */
347	  private updateRewardUI() {
348	    if (!this.rewardBtnBg || !this.rewardBtnLabel) return;
349	
350	    const btn = this.rewardBtnBg;
351	    const label = this.rewardBtnLabel;
352	    const reward = this.prevSeasonReward;
353	
354	    btn.removeAllListeners();
355	    btn.disableInteractive();
356	
357	    if (!reward || reward.rank === null || reward.skorAwarded === 0) {
358	      // 비활성: 기록 없음 또는 100위 밖
359	      btn.setFillStyle(0x555555).setStrokeStyle(3, 0x333333);
360	      label.setText('보상수령').setColor('#999999');
361	
362	    } else if (reward.alreadyClaimed) {
363	      // 비활성: 수령 완료 (초록)
364	      btn.setFillStyle(0x336633).setStrokeStyle(3, 0x224422);
365	      label.setText('수령완료').setColor('#88ff88');
366	
367	    } else {
368	      // 활성: 수령 가능 (노란색)
369	      btn.setFillStyle(0xffcc00).setStrokeStyle(3, 0xaa8800);
370	      label.setText('보상수령').setColor('#000000');
371	      btn.setInteractive({ useHandCursor: true });
372	      btn.on('pointerover', () => btn.setFillStyle(0xffe566));
373	      btn.on('pointerout', () => btn.setFillStyle(0xffcc00));
374	      btn.on('pointerdown', () => this.handleClaimReward());
375	    }
376	  }
377	
378	  /** 보상받기 버튼 클릭 처리 */
379	  private async handleClaimReward() {
380	    if (!this.rewardBtnBg || !this.rewardBtnLabel) return;
381	
382	    // 처리 중 표시 (중복 클릭 방지)
383	    this.rewardBtnBg.disableInteractive();
384	    this.rewardBtnLabel.setText('처리중...').setColor('#aaaaaa');
385	
386	    try {
387	      const result = await claimSeasonReward(this.selectedDifficulty);
388	
389	      if (result.success && (result.skorAwarded ?? 0) > 0) {
390	        if (this.prevSeasonReward) {
391	          this.prevSeasonReward = { ...this.prevSeasonReward, alreadyClaimed: true };
392	        }
393	        this.updateRewardUI();
394	
395	        // 획득 플래시 연출
396	        const flashText = this.add.text(
397	          this.scale.width / 2, this.scale.height / 2 - 60,
398	          `+${result.skorAwarded} SKOR 획득!`, {
399	            fontSize: '24px',
400	            color: '#ffcc00',
401	            fontStyle: 'bold',
402	            stroke: '#000',
403	            strokeThickness: 5,
404	          }
405	        ).setOrigin(0.5);
406	
407	        this.tweens.add({
408	          targets: flashText,
409	          alpha: { from: 1, to: 0 },
410	          y: flashText.y - 40,
411	          duration: 1500,
412	          ease: 'Cubic.easeOut',
413	          onComplete: () => flashText.destroy(),
414	        });
415	      } else {
416	        if (this.prevSeasonReward && result.alreadyClaimed) {
417	          this.prevSeasonReward = { ...this.prevSeasonReward, alreadyClaimed: true };
418	        }
419	        this.updateRewardUI();
420	      }
421	    } catch {
422	      // 실패 시 원래 상태로 복구
423	      this.updateRewardUI();
424	    }
425	  }
426	
427	  private createBackButton(cx: number, y: number) {
428	    const button = this.add.rectangle(cx, y, 150, 40, 0xffffff, 1);
429	    button.setStrokeStyle(3, 0x000000);
430	
431	    const text = this.add.text(cx, y, '← 뒤로가기', {
432	      fontSize: '18px',
433	      color: '#000',
434	      fontStyle: 'bold'
435	    }).setOrigin(0.5);
436	
437	    button.setInteractive({ useHandCursor: true });
438	
439	    const elements = [button, text];
440	    elements.forEach(element => {
441	      element.on('pointerover', () => {
442	        button.setFillStyle(0xffff99);
443	      });
444	
445	      element.on('pointerout', () => {
446	        button.setFillStyle(0xffffff);
447	      });
448	
449	      element.on('pointerdown', () => {
450	        this.scene.start('ModeSelectScene');
451	      });
452	    });
453	  }
454	}
455	
```

> AGENT

현황 파악 완료. 서버에서 `characterType`이 이미 반환되고 있는데, `LeaderboardScene.displayLeaderboard()`에서 표시만 안 하고 있네요. 캐릭터 목록도 확인할게요.

> TOOL

tool_use Bash
id: toolu_014Z1NdAPmp2PuFH8uk2tPuu
```json
{
  "command": "grep -n \"id:\\|imageKey\\|imagePath\\|illustKey\\|name:\" /Users/johyunduk/Projects/ddong-avoid-game/src/utils/character.ts | head -80",
  "description": "Check character IDs and image keys"
}
```

> TOOL

tool_result
id: toolu_014Z1NdAPmp2PuFH8uk2tPuu
```
9:  id: string;
10:  name: string;
13:  imageKey: string;     // Phaser 텍스처 키 (카드용 스프라이트)
14:  imagePath: string;    // public/ 기준 경로
15:  illustKey: string;    // Phaser 텍스처 키 (일러스트 배경용)
35:    id: 'chibi',
36:    name: '치비',
39:    imageKey: 'chibi_front',
40:    imagePath: 'assets/players/chibi_front.webp',
41:    illustKey: 'illust_chibi',
50:    id: 'mugi',
51:    name: '무기',
54:    imageKey: 'mugi_front',
55:    imagePath: 'assets/players/mugi_front.webp',
56:    illustKey: 'illust_mugi',
65:    id: 'gumi',
66:    name: '구미',
69:    imageKey: 'gumi_front',
70:    imagePath: 'assets/players/gumi_front.webp',
71:    illustKey: 'illust_gumi',
81:    id: 'sentinel',
82:    name: '센티넬',
85:    imageKey: 'sentinel_front',
86:    imagePath: 'assets/players/sentinel_front.webp',
87:    illustKey: 'illust_sentinel',
95:    id: 'legacy',
96:    name: '레거시',
99:    imageKey: 'legacy_front',
100:    imagePath: 'assets/players/legacy_front.webp',
101:    illustKey: 'illust_legacy',
110:    id: 'knight',
111:    name: '나이트',
114:    imageKey: 'knight_front',
115:    imagePath: 'assets/players/knight_front.webp',
116:    illustKey: 'illust_knight',
124:    id: 'hacker',
125:    name: '루트',
128:    imageKey: 'hacker_front',
129:    imagePath: 'assets/players/hacker_front.webp',
130:    illustKey: 'illust_hacker',
138:    id: 'miner',
139:    name: '광부',
142:    imageKey: 'miner_front',
143:    imagePath: 'assets/players/miner_front.webp',
144:    illustKey: 'illust_miner',
152:    id: 'maehwa',
153:    name: '매화',
156:    imageKey: 'maehwa_front',
157:    imagePath: 'assets/players/maehwa_front.webp',
158:    illustKey: 'illust_maehwa',
166:    id: 'archieve',
167:    name: '아카이브',
170:    imageKey: 'archieve_front',
171:    imagePath: 'assets/players/archieve_front.webp',
172:    illustKey: 'illust_archieve',
180:    id: 'glitch',
181:    name: '글리치',
184:    imageKey: 'glitch_front',
185:    imagePath: 'assets/players/glitch_front.webp',
186:    illustKey: 'illust_glitch',
194:    id: 'noise',
195:    name: '노이즈',
198:    imageKey: 'noise_front',
199:    imagePath: 'assets/players/noise_front.webp',
200:    illustKey: 'illust_noise',
209:    id: 'log',
210:    name: '로그',
213:    imageKey: 'log_front',
214:    imagePath: 'assets/players/log_front.webp',
215:    illustKey: 'illust_log',
221:    id: 'swap',
222:    name: '스왑',
225:    imageKey: 'swap_front',
226:    imagePath: 'assets/players/swap_front.webp',
227:    illustKey: 'illust_swap',
233:    id: 'sum',
234:    name: '섬',
237:    imageKey: 'sum_front',
238:    imagePath: 'assets/players/sum_front.webp',
239:    illustKey: 'illust_sum',
```

> TOOL

tool_use Bash
id: toolu_015jU38TTvEbfxLrGSY1Z3iC
```json
{
  "command": "grep -n \"id:\\|name:\" /Users/johyunduk/Projects/ddong-avoid-game/src/utils/character.ts | tail -40",
  "description": "Check remaining character IDs and names"
}
```

> TOOL

tool_result
id: toolu_015jU38TTvEbfxLrGSY1Z3iC
```
96:    name: '레거시',
110:    id: 'knight',
111:    name: '나이트',
124:    id: 'hacker',
125:    name: '루트',
138:    id: 'miner',
139:    name: '광부',
152:    id: 'maehwa',
153:    name: '매화',
166:    id: 'archieve',
167:    name: '아카이브',
180:    id: 'glitch',
181:    name: '글리치',
194:    id: 'noise',
195:    name: '노이즈',
209:    id: 'log',
210:    name: '로그',
221:    id: 'swap',
222:    name: '스왑',
233:    id: 'sum',
234:    name: '섬',
245:    id: 'fork',
246:    name: '포크',
257:    id: 'seed',
258:    name: '시드',
269:    id: 'session',
270:    name: '세션',
281:    id: 'branch',
282:    name: '브랜치',
293:    id: 'hook',
294:    name: '훅',
305:    id: 'socket',
306:    name: '소켓',
317:    id: 'index',
318:    name: '인덱스',
375:export function getDuplicateCount(id: string): number {
400:export function setDuplicateCount(id: string, count: number): void {
469:export function addOwnedCharacter(id: string): void {
483:export function setSelectedCharacter(id: string): void {
498:export function getCharacterDef(id: string): CharacterDef {
```

> AGENT

구조 파악 완료!

- `leaderboard-submit`: `character_type` DB 저장 ✅  
- `leaderboard-top`: `characterType` 응답에 포함 ✅  
- `LeaderboardEntry` 타입: `characterType?: string` 필드 존재 ✅  
- `LeaderboardScene.displayLeaderboard()`: 표시 코드 없음 ❌  

`★ Insight ─────────────────────────────────────`

1. `leaderboardTexts`가 `Phaser.GameObjects.Text[]`로 타입 선언되어 있어, Image 오브젝트를 함께 관리하려면 `Phaser.GameObjects.GameObject[]`로 확장해야 함 — Phaser의 GameObject 계층에서 Text와 Image 모두 GameObject를 상속함
2. 리더보드 `preload()`에서 전체 21종 이미지를 미리 로드하되, `this.textures.exists()` 가드로 다른 씬에서 이미 캐시된 경우 중복 로딩을 방지하는 패턴이 중요함

`─────────────────────────────────────────────────`

이제 `LeaderboardScene.ts`를 수정할게요. 각 행 왼쪽에 캐릭터 아이콘(26×26)을 표시하도록 구현합니다.

> TOOL

tool_use Read
id: toolu_011724EgAzdhQGDSDm7u5JMp
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/utils/character.ts",
  "offset": 1,
  "limit": 35
}
```

> TOOL

tool_result
id: toolu_011724EgAzdhQGDSDm7u5JMp
```
1	import {
2	  HACKER_DESC, MINER_DESC, MAEHWA_DESC,
3	  ARCHIEVE_DESC, GLITCH_DESC, NOISE_DESC,
4	  SENTINEL_DESC, LEGACY_DESC, KNIGHT_DESC,
5	  GUMI_DESC, MUGI_DESC,
6	} from '../config/abilityParams';
7	
8	export interface CharacterDef {
9	  id: string;
10	  name: string;
11	  grade: '등급외' | 'R' | 'SR' | 'UR';
12	  gradeColor: string;   // hex 문자열 (UI용)
13	  imageKey: string;     // Phaser 텍스처 키 (카드용 스프라이트)
14	  imagePath: string;    // public/ 기준 경로
15	  illustKey: string;    // Phaser 텍스처 키 (일러스트 배경용)
16	  illustPath: string;   // public/ 기준 경로
17	  videoKey?: string;    // Phaser 비디오 키 (선택, 있으면 일러스트 클릭 시 재생)
18	  videoPath?: string;   // public/ 기준 경로 (선택)
19	  basicEffect: string;  // 기본 효과 설명 (상세 팝업용)
20	  specialAbility: string; // 특수 능력 설명 (없으면 '없음')
21	  /** 인게임 플레이어 표시 크기 [w, h]. 생략 시 [50, 80] */
22	  playerDisplaySize?: [number, number];
23	  /** 캐릭터 선택 카드 표시 크기 [w, h]. 생략 시 [58, 85] */
24	  cardDisplaySize?: [number, number];
25	}
26	
27	/** 등급 이미지 텍스처 키 반환. 등급외 → null */
28	export function getGradeImgKey(grade: string): string | null {
29	  if (grade === '등급외') return null;
30	  return `grade_${grade.toLowerCase()}`; // grade_r, grade_sr, grade_ur
31	}
32	
33	export const CHARACTERS: CharacterDef[] = [
34	  {
35	    id: 'chibi',
```

> TOOL

tool_use Edit
id: toolu_014jj1EJaRPpPw2Vc1qc3fyy
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "import type Phaser from 'phaser';\nimport { Difficulty, Difficulty as DifficultyEnum } from '../types/GameMode';\nimport {\n  getLeaderboard,\n  claimSeasonReward,\n  getCachedClaimAmount,\n  type LeaderboardEntry,\n  type PrevSeasonReward,\n} from '../utils/leaderboard';\nimport BaseScene from './BaseScene';",
  "new_string": "import type Phaser from 'phaser';\nimport { Difficulty, Difficulty as DifficultyEnum } from '../types/GameMode';\nimport {\n  getLeaderboard,\n  claimSeasonReward,\n  getCachedClaimAmount,\n  type LeaderboardEntry,\n  type PrevSeasonReward,\n} from '../utils/leaderboard';\nimport { CHARACTERS } from '../utils/character';\nimport BaseScene from './BaseScene';"
}
```

> TOOL

tool_result
id: toolu_014jj1EJaRPpPw2Vc1qc3fyy
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01SwPisVxjpZKvZGiwPib2uj
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  private leaderboardTexts: Phaser.GameObjects.Text[] = [];",
  "new_string": "  private leaderboardTexts: Phaser.GameObjects.GameObject[] = [];"
}
```

> TOOL

tool_result
id: toolu_01SwPisVxjpZKvZGiwPib2uj
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이제 `preload()`에 캐릭터 이미지 로드를 추가합니다.

> TOOL

tool_use Edit
id: toolu_01JzV8EvF6C5iYWjPJgsQULA
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  preload() {\n    // 배경 이미지 로드 (캐시 확인으로 중복 로딩 방지)\n    if (!this.textures.exists('background2')) {\n      this.load.image('background2', 'assets/backgrounds/background2.webp');\n    }\n  }",
  "new_string": "  preload() {\n    if (!this.textures.exists('background2')) {\n      this.load.image('background2', 'assets/backgrounds/background2.webp');\n    }\n    // 캐릭터 아이콘 (랭킹 표시용)\n    CHARACTERS.forEach(char => {\n      if (!this.textures.exists(char.imageKey)) {\n        this.load.image(char.imageKey, char.imagePath);\n      }\n    });\n  }"
}
```

> TOOL

tool_result
id: toolu_01JzV8EvF6C5iYWjPJgsQULA
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이제 `displayLeaderboard()`에서 캐릭터 아이콘 표시를 추가합니다.

> TOOL

tool_use Edit
id: toolu_01R5WHxJtvRuH8Baeo9NhQmh
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const cx = this.scale.width / 2;\n    const startY = 163 + yOff;\n    const lineHeight = 35;\n\n    // 헤더\n    const headerText = this.add.text(cx, startY, '순위    이름      점수', {\n      fontSize: '16px',\n      color: '#ffff00',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 4\n    }).setOrigin(0.5);\n    this.leaderboardTexts.push(headerText);\n\n    // 랭킹 데이터 표시\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(cx, startY + 50, '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!', {\n        fontSize: '18px',\n        color: '#ccc',\n        stroke: '#000',\n        strokeThickness: 3,\n        align: 'center'\n      }).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    this.leaderboardData.forEach((entry, index) => {\n      const y = startY + 30 + (index * lineHeight);\n\n      // 순위별 색상\n      let color = '#ffffff';\n      if (entry.rank === 1) color = '#FFD700'; // 금색\n      else if (entry.rank === 2) color = '#C0C0C0'; // 은색\n      else if (entry.rank === 3) color = '#CD7F32'; // 동색\n\n\n      const rankText = `${entry.rank}`.padEnd(8, ' ');\n      const nameText = entry.userName.padEnd(8, ' ');\n      const scoreText = entry.score.toString().padStart(6, ' ');\n\n      const text = this.add.text(\n        cx,\n        y,\n        `${rankText}${nameText}${scoreText}`,\n        {\n          fontSize: '16px',\n          color: color,\n          fontFamily: 'monospace',\n          stroke: '#000',\n          strokeThickness: 3\n        }\n      ).setOrigin(0.5);\n\n      this.leaderboardTexts.push(text);\n    });\n  }",
  "new_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const cx = this.scale.width / 2;\n    const startY = 163 + yOff;\n    const lineHeight = 35;\n    const ICON_SIZE = 26;\n    const ICON_X = 20;\n\n    // 헤더\n    const headerText = this.add.text(cx + 14, startY, '순위   이름     점수', {\n      fontSize: '16px',\n      color: '#ffff00',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 4\n    }).setOrigin(0.5);\n    this.leaderboardTexts.push(headerText);\n\n    // 랭킹 데이터 표시\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(cx, startY + 50, '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!', {\n        fontSize: '18px',\n        color: '#ccc',\n        stroke: '#000',\n        strokeThickness: 3,\n        align: 'center'\n      }).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    this.leaderboardData.forEach((entry, index) => {\n      const y = startY + 30 + (index * lineHeight);\n\n      // 순위별 색상\n      let color = '#ffffff';\n      if (entry.rank === 1) color = '#FFD700';\n      else if (entry.rank === 2) color = '#C0C0C0';\n      else if (entry.rank === 3) color = '#CD7F32';\n\n      // 캐릭터 아이콘\n      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];\n      const icon = this.add.image(ICON_X, y, charDef.imageKey)\n        .setDisplaySize(ICON_SIZE, ICON_SIZE)\n        .setOrigin(0.5);\n      this.leaderboardTexts.push(icon);\n\n      const rankText = `${entry.rank}`.padEnd(7, ' ');\n      const nameText = entry.userName.padEnd(8, ' ');\n      const scoreText = entry.score.toString().padStart(6, ' ');\n\n      const text = this.add.text(\n        cx + 14,\n        y,\n        `${rankText}${nameText}${scoreText}`,\n        {\n          fontSize: '16px',\n          color: color,\n          fontFamily: 'monospace',\n          stroke: '#000',\n          strokeThickness: 3\n        }\n      ).setOrigin(0.5);\n\n      this.leaderboardTexts.push(text);\n    });\n  }"
}
```

> TOOL

tool_result
id: toolu_01R5WHxJtvRuH8Baeo9NhQmh
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이제 `leaderboardTexts.forEach(text => text.destroy())` 부분이 `Phaser.GameObjects.GameObject[]` 타입을 잘 처리하는지 확인할게요.

> TOOL

tool_use Bash
id: toolu_01YKSUhecvmtCAiCnNRLHifA
```json
{
  "command": "grep -n \"leaderboardTexts\" /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "description": "Check all leaderboardTexts usages"
}
```

> TOOL

tool_result
id: toolu_01YKSUhecvmtCAiCnNRLHifA
```
16:  private leaderboardTexts: Phaser.GameObjects.GameObject[] = [];
195:    this.leaderboardTexts.forEach(text => text.destroy());
196:    this.leaderboardTexts = [];
300:    this.leaderboardTexts.push(headerText);
311:      this.leaderboardTexts.push(noDataText);
329:      this.leaderboardTexts.push(icon);
348:      this.leaderboardTexts.push(text);
```

> AGENT

`destroy()`는 `Phaser.GameObjects.GameObject`에 정의되어 있으므로 문제없습니다. 이제 타입 검사를 돌려볼게요.

> TOOL

tool_use Bash
id: toolu_01E7DHiGERbPh4nKBk4K1ZCF
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_01E7DHiGERbPh4nKBk4K1ZCF
```
(Bash completed with no output)
```

> AGENT

타입 에러 없음. 마지막으로 `leaderboard-submit`의 유효 캐릭터 목록에서 `mugi`, `gumi`, `knight`가 빠져 있던 것도 함께 수정할게요. 이들이 빠지면 제출 시 'chibi'로 강제 교체됩니다.

> TOOL

tool_use Edit
id: toolu_01NYCnzSYwWSVNtcu7zsa9pD
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-submit/index.ts",
  "old_string": "      const validCharacterTypes = [\n        'chibi',\n        'log', 'swap', 'sum', 'fork', 'seed', 'session', 'branch', 'hook', 'socket', 'index',\n        'hacker', 'miner', 'maehwa', 'archieve', 'glitch', 'noise',\n        'sentinel', 'legacy',\n      ];",
  "new_string": "      const validCharacterTypes = [\n        'chibi', 'mugi', 'gumi', 'knight',\n        'log', 'swap', 'sum', 'fork', 'seed', 'session', 'branch', 'hook', 'socket', 'index',\n        'hacker', 'miner', 'maehwa', 'archieve', 'glitch', 'noise',\n        'sentinel', 'legacy',\n      ];"
}
```

> TOOL

tool_result
id: toolu_01NYCnzSYwWSVNtcu7zsa9pD
```
The file /Users/johyunduk/Projects/ddong-avoid-game/supabase/functions/leaderboard-submit/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

완료입니다.

**변경 사항 요약:**

**`src/scenes/LeaderboardScene.ts`**
- `leaderboardTexts` 타입을 `Text[]` → `GameObject[]`로 변경 (Image도 함께 관리)
- `preload()`에서 전체 21종 캐릭터 이미지를 미리 로드 (캐시 체크로 중복 방지)
- `displayLeaderboard()` 각 행 왼쪽 x=20 위치에 26×26 캐릭터 아이콘 추가
- `characterType`이 없거나 알 수 없는 값이면 치비(기본 캐릭터)로 폴백

**`supabase/functions/leaderboard-submit/index.ts`**
- `mugi`, `gumi`, `knight` 를 유효 캐릭터 목록에 추가 (기존엔 빠져 있어서 'chibi'로 저장되고 있었음)

Edge Function 재배포가 필요합니다:
```bash
supabase functions deploy leaderboard-submit --no-verify-jwt
```

> DEVELOPER

뭔가 너무 동떨어져 있는데? 좀 뭔가 괜찮은 UI로 해줘.

> AGENT

현재 레이아웃 전체를 확인하고 제대로 리디자인할게요.

> TOOL

tool_use Read
id: toolu_01Q61HWMs29fA6oNVrUWe9Ae
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "offset": 278,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01Q61HWMs29fA6oNVrUWe9Ae
```
278	        strokeThickness: 3,
279	        align: 'center'
280	      }).setOrigin(0.5);
281	    }
282	  }
283	
284	  private displayLeaderboard() {
285	    const yOff = (this.scale.height - 600) / 2;
286	    const cx = this.scale.width / 2;
287	    const startY = 163 + yOff;
288	    const lineHeight = 35;
289	    const ICON_SIZE = 26;
290	    const ICON_X = 20;
291	
292	    // 헤더
293	    const headerText = this.add.text(cx + 14, startY, '순위   이름     점수', {
294	      fontSize: '16px',
295	      color: '#ffff00',
296	      fontStyle: 'bold',
297	      stroke: '#000',
298	      strokeThickness: 4
299	    }).setOrigin(0.5);
300	    this.leaderboardTexts.push(headerText);
301	
302	    // 랭킹 데이터 표시
303	    if (this.leaderboardData.length === 0) {
304	      const noDataText = this.add.text(cx, startY + 50, '아직 랭킹이 없습니다\n\n첫 번째 플레이어가 되어보세요!', {
305	        fontSize: '18px',
306	        color: '#ccc',
307	        stroke: '#000',
308	        strokeThickness: 3,
309	        align: 'center'
310	      }).setOrigin(0.5);
311	      this.leaderboardTexts.push(noDataText);
312	      return;
313	    }
314	
315	    this.leaderboardData.forEach((entry, index) => {
316	      const y = startY + 30 + (index * lineHeight);
317	
318	      // 순위별 색상
319	      let color = '#ffffff';
320	      if (entry.rank === 1) color = '#FFD700';
321	      else if (entry.rank === 2) color = '#C0C0C0';
322	      else if (entry.rank === 3) color = '#CD7F32';
323	
324	      // 캐릭터 아이콘
325	      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];
326	      const icon = this.add.image(ICON_X, y, charDef.imageKey)
327	        .setDisplaySize(ICON_SIZE, ICON_SIZE)
328	        .setOrigin(0.5);
329	      this.leaderboardTexts.push(icon);
330	
331	      const rankText = `${entry.rank}`.padEnd(7, ' ');
332	      const nameText = entry.userName.padEnd(8, ' ');
333	      const scoreText = entry.score.toString().padStart(6, ' ');
334	
335	      const text = this.add.text(
336	        cx + 14,
337	        y,
338	        `${rankText}${nameText}${scoreText}`,
339	        {
340	          fontSize: '16px',
341	          color: color,
342	          fontFamily: 'monospace',
343	          stroke: '#000',
344	          strokeThickness: 3
345	        }
346	      ).setOrigin(0.5);
347	
348	      this.leaderboardTexts.push(text);
349	    });
350	  }
351	
352	  /** 이번 달 말일까지 남은 일수 */
353	  private calcDaysUntilMonthEnd(): number {
354	    const now = new Date();
355	    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
356	    const diff = lastDay.getTime() - now.getTime();
357	    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
```

> AGENT

`★ Insight ─────────────────────────────────────`

1. 현재 구조의 문제: 아이콘(x=20)과 텍스트(x=214)가 400px 캔버스에서 190px나 떨어져 있어 시각적으로 완전히 분리됨. 각 컬럼을 별도의 `add.text()` / `add.image()` 오브젝트로 고정 x좌표에 배치하면 이 문제가 해결됨
2. Phaser에서 행마다 반투명 배경 rect를 깔면 readability가 크게 향상되는데, `add.rectangle()`의 `setAlpha()`로 간단히 구현 가능

`─────────────────────────────────────────────────`

`displayLeaderboard()`를 컬럼 기반 구조로 완전히 재작성합니다.

> TOOL

tool_use Edit
id: toolu_01NJKAt5x4Xowib7KvzxSC1K
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const cx = this.scale.width / 2;\n    const startY = 163 + yOff;\n    const lineHeight = 35;\n    const ICON_SIZE = 26;\n    const ICON_X = 20;\n\n    // 헤더\n    const headerText = this.add.text(cx + 14, startY, '순위   이름     점수', {\n      fontSize: '16px',\n      color: '#ffff00',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 4\n    }).setOrigin(0.5);\n    this.leaderboardTexts.push(headerText);\n\n    // 랭킹 데이터 표시\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(cx, startY + 50, '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!', {\n        fontSize: '18px',\n        color: '#ccc',\n        stroke: '#000',\n        strokeThickness: 3,\n        align: 'center'\n      }).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    this.leaderboardData.forEach((entry, index) => {\n      const y = startY + 30 + (index * lineHeight);\n\n      // 순위별 색상\n      let color = '#ffffff';\n      if (entry.rank === 1) color = '#FFD700';\n      else if (entry.rank === 2) color = '#C0C0C0';\n      else if (entry.rank === 3) color = '#CD7F32';\n\n      // 캐릭터 아이콘\n      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];\n      const icon = this.add.image(ICON_X, y, charDef.imageKey)\n        .setDisplaySize(ICON_SIZE, ICON_SIZE)\n        .setOrigin(0.5);\n      this.leaderboardTexts.push(icon);\n\n      const rankText = `${entry.rank}`.padEnd(7, ' ');\n      const nameText = entry.userName.padEnd(8, ' ');\n      const scoreText = entry.score.toString().padStart(6, ' ');\n\n      const text = this.add.text(\n        cx + 14,\n        y,\n        `${rankText}${nameText}${scoreText}`,\n        {\n          fontSize: '16px',\n          color: color,\n          fontFamily: 'monospace',\n          stroke: '#000',\n          strokeThickness: 3\n        }\n      ).setOrigin(0.5);\n\n      this.leaderboardTexts.push(text);\n    });\n  }",
  "new_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const startY = 130 + yOff;\n    const ROW_H = 38;\n    const ROW_W = 370;\n    const LEFT = 15;\n    // 컬럼 x 좌표\n    const COL_RANK  = LEFT + 28;   // 순위 (우측 정렬)\n    const COL_ICON  = LEFT + 58;   // 캐릭터 아이콘 (중앙)\n    const COL_NAME  = LEFT + 84;   // 이름 (좌측 정렬)\n    const COL_SCORE = LEFT + ROW_W - 8; // 점수 (우측 정렬)\n\n    // ── 헤더 구분선 ──────────────────────────────────────\n    const headerY = startY + 16;\n    const headerStyle = {\n      fontSize: '13px',\n      color: '#aaddff',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 3,\n    };\n    this.leaderboardTexts.push(\n      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),\n      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0, 0.5),\n      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),\n    );\n    const divider = this.add.rectangle(LEFT + ROW_W / 2, headerY + 11, ROW_W, 1, 0xaaddff, 0.5);\n    this.leaderboardTexts.push(divider);\n\n    // ── 데이터 없음 ──────────────────────────────────────\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(\n        LEFT + ROW_W / 2, startY + 80,\n        '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!',\n        { fontSize: '18px', color: '#ccc', stroke: '#000', strokeThickness: 3, align: 'center' }\n      ).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    // ── 각 행 ────────────────────────────────────────────\n    this.leaderboardData.forEach((entry, index) => {\n      const rowY = startY + 38 + index * ROW_H;\n      const cy = rowY + ROW_H / 2;\n\n      // 행 배경\n      const bgColor =\n        entry.rank === 1 ? 0x4a3a00 :\n        entry.rank === 2 ? 0x2a2a35 :\n        entry.rank === 3 ? 0x3a2010 :\n        index % 2 === 0  ? 0x0a0a18 : 0x121220;\n      const bgAlpha = entry.rank <= 3 ? 0.85 : 0.55;\n      const bg = this.add.rectangle(LEFT + ROW_W / 2, cy, ROW_W, ROW_H - 2, bgColor, bgAlpha);\n      this.leaderboardTexts.push(bg);\n\n      // 상위 3위 왼쪽 테두리 강조\n      if (entry.rank <= 3) {\n        const accentColor = entry.rank === 1 ? 0xFFD700 : entry.rank === 2 ? 0xC0C0C0 : 0xCD7F32;\n        const accent = this.add.rectangle(LEFT + 1, cy, 3, ROW_H - 2, accentColor, 1);\n        this.leaderboardTexts.push(accent);\n      }\n\n      // 순위 색상\n      const rankColor =\n        entry.rank === 1 ? '#FFD700' :\n        entry.rank === 2 ? '#C0C0C0' :\n        entry.rank === 3 ? '#CD7F32' : '#aaaaaa';\n\n      // 순위\n      const rankLabel = entry.rank <= 3\n        ? ['🥇', '🥈', '🥉'][entry.rank - 1]\n        : `${entry.rank}`;\n      this.leaderboardTexts.push(\n        this.add.text(COL_RANK, cy, rankLabel, {\n          fontSize: entry.rank <= 3 ? '18px' : '15px',\n          color: rankColor,\n          fontStyle: 'bold',\n          stroke: '#000',\n          strokeThickness: 3,\n        }).setOrigin(1, 0.5)\n      );\n\n      // 캐릭터 아이콘\n      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];\n      this.leaderboardTexts.push(\n        this.add.image(COL_ICON, cy, charDef.imageKey).setDisplaySize(28, 28).setOrigin(0.5)\n      );\n\n      // 이름\n      this.leaderboardTexts.push(\n        this.add.text(COL_NAME, cy, entry.userName, {\n          fontSize: '15px',\n          color: entry.rank <= 3 ? '#ffffff' : '#dddddd',\n          fontFamily: 'monospace',\n          fontStyle: 'bold',\n          stroke: '#000',\n          strokeThickness: 3,\n        }).setOrigin(0, 0.5)\n      );\n\n      // 점수\n      this.leaderboardTexts.push(\n        this.add.text(COL_SCORE, cy, entry.score.toLocaleString(), {\n          fontSize: '15px',\n          color: entry.rank <= 3 ? rankColor : '#ffffff',\n          fontFamily: 'monospace',\n          fontStyle: 'bold',\n          stroke: '#000',\n          strokeThickness: 3,\n        }).setOrigin(1, 0.5)\n      );\n    });\n  }"
}
```

> TOOL

tool_result
id: toolu_01NJKAt5x4Xowib7KvzxSC1K
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01NPvbc6nb6wRW16VsUcwTJk
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_01NPvbc6nb6wRW16VsUcwTJk
```
(Bash completed with no output)
```

> AGENT

타입 에러 없음. 변경된 레이아웃 구조를 정리하면:

```
┌─────────────────────────────────────┐
│  순위         이름              점수  │  ← 헤더 (하늘색)
├─────────────────────────────────────┤  ← 구분선
│🥇 [아이콘] ABE            1,234     │  ← 금색 배경 + 좌측 금 강조선
│🥈 [아이콘] CDF              987     │  ← 은색 배경 + 좌측 은 강조선
│🥉 [아이콘] GHI              756     │  ← 동색 배경 + 좌측 동 강조선
│ 4  [아이콘] JKL              600     │  ← 교번 어두운 배경
│ 5  [아이콘] MNO              543     │
└─────────────────────────────────────┘
```

**주요 변경:**
- 아이콘이 순위 바로 옆 (rank → icon → name → score) 컬럼 구조로 정렬
- 각 행에 반투명 배경 rect (상위 3위는 금/은/동 배경 색조)
- 상위 3위 왼쪽에 컬러 강조 세로선
- 1~3위 메달 이모지 (🥇🥈🥉), 4위 이하는 숫자
- 점수에 `.toLocaleString()` 적용 (1,234 형식)

> DEVELOPER

1,2,3 도 그냥 숫자로 해줘 메달 이모티콘 말고 그리고 왼쪽으로 치우쳐져있는데 랭킹 항목들 자체가. 가운데 정렬을 하던가 아니면 꽉차게 하던가 좀 보기 편하게 해달라고

> TOOL

tool_use Read
id: toolu_0129j1EAKm5H8tSWXPCTnCbw
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "offset": 284,
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_0129j1EAKm5H8tSWXPCTnCbw
```
284	  private displayLeaderboard() {
285	    const yOff = (this.scale.height - 600) / 2;
286	    const startY = 130 + yOff;
287	    const ROW_H = 38;
288	    const ROW_W = 370;
289	    const LEFT = 15;
290	    // 컬럼 x 좌표
291	    const COL_RANK  = LEFT + 28;   // 순위 (우측 정렬)
292	    const COL_ICON  = LEFT + 58;   // 캐릭터 아이콘 (중앙)
293	    const COL_NAME  = LEFT + 84;   // 이름 (좌측 정렬)
294	    const COL_SCORE = LEFT + ROW_W - 8; // 점수 (우측 정렬)
295	
296	    // ── 헤더 구분선 ──────────────────────────────────────
297	    const headerY = startY + 16;
298	    const headerStyle = {
299	      fontSize: '13px',
300	      color: '#aaddff',
301	      fontStyle: 'bold',
302	      stroke: '#000',
303	      strokeThickness: 3,
304	    };
305	    this.leaderboardTexts.push(
306	      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),
307	      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0, 0.5),
308	      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),
309	    );
310	    const divider = this.add.rectangle(LEFT + ROW_W / 2, headerY + 11, ROW_W, 1, 0xaaddff, 0.5);
311	    this.leaderboardTexts.push(divider);
312	
313	    // ── 데이터 없음 ──────────────────────────────────────
314	    if (this.leaderboardData.length === 0) {
315	      const noDataText = this.add.text(
316	        LEFT + ROW_W / 2, startY + 80,
317	        '아직 랭킹이 없습니다\n\n첫 번째 플레이어가 되어보세요!',
318	        { fontSize: '18px', color: '#ccc', stroke: '#000', strokeThickness: 3, align: 'center' }
319	      ).setOrigin(0.5);
320	      this.leaderboardTexts.push(noDataText);
321	      return;
322	    }
323	
324	    // ── 각 행 ────────────────────────────────────────────
325	    this.leaderboardData.forEach((entry, index) => {
326	      const rowY = startY + 38 + index * ROW_H;
327	      const cy = rowY + ROW_H / 2;
328	
329	      // 행 배경
330	      const bgColor =
331	        entry.rank === 1 ? 0x4a3a00 :
332	        entry.rank === 2 ? 0x2a2a35 :
333	        entry.rank === 3 ? 0x3a2010 :
334	        index % 2 === 0  ? 0x0a0a18 : 0x121220;
335	      const bgAlpha = entry.rank <= 3 ? 0.85 : 0.55;
336	      const bg = this.add.rectangle(LEFT + ROW_W / 2, cy, ROW_W, ROW_H - 2, bgColor, bgAlpha);
337	      this.leaderboardTexts.push(bg);
338	
339	      // 상위 3위 왼쪽 테두리 강조
340	      if (entry.rank <= 3) {
341	        const accentColor = entry.rank === 1 ? 0xFFD700 : entry.rank === 2 ? 0xC0C0C0 : 0xCD7F32;
342	        const accent = this.add.rectangle(LEFT + 1, cy, 3, ROW_H - 2, accentColor, 1);
343	        this.leaderboardTexts.push(accent);
344	      }
345	
346	      // 순위 색상
347	      const rankColor =
348	        entry.rank === 1 ? '#FFD700' :
349	        entry.rank === 2 ? '#C0C0C0' :
350	        entry.rank === 3 ? '#CD7F32' : '#aaaaaa';
351	
352	      // 순위
353	      const rankLabel = entry.rank <= 3
354	        ? ['🥇', '🥈', '🥉'][entry.rank - 1]
355	        : `${entry.rank}`;
356	      this.leaderboardTexts.push(
357	        this.add.text(COL_RANK, cy, rankLabel, {
358	          fontSize: entry.rank <= 3 ? '18px' : '15px',
359	          color: rankColor,
360	          fontStyle: 'bold',
361	          stroke: '#000',
362	          strokeThickness: 3,
363	        }).setOrigin(1, 0.5)
364	      );
365	
366	      // 캐릭터 아이콘
367	      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];
368	      this.leaderboardTexts.push(
369	        this.add.image(COL_ICON, cy, charDef.imageKey).setDisplaySize(28, 28).setOrigin(0.5)
370	      );
371	
372	      // 이름
373	      this.leaderboardTexts.push(
```

> AGENT

문제 파악 완료. 전체 레이아웃을 재설계할게요.

`★ Insight ─────────────────────────────────────`

현재 ROW_W=370에 LEFT=15를 더하면 전체 블록이 x=15~385로 캔버스 좌측에 더 가까움. 400px 캔버스에서 좌우 여백을 동일하게 주려면 LEFT=8, ROW_W=384가 적합. 또한 이름 컬럼이 x=99에서 좌측 정렬이라 3자 이름 "ABC"는 x=99~126 정도만 차지하고 나머지 공간이 비어 보임 — 이름과 점수 사이 공간을 채우도록 컬럼 비율을 재배분하는 게 핵심.

`─────────────────────────────────────────────────`

> TOOL

tool_use Edit
id: toolu_015h5vWmmrBP8xkhsgQuCvG8
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const startY = 130 + yOff;\n    const ROW_H = 38;\n    const ROW_W = 370;\n    const LEFT = 15;\n    // 컬럼 x 좌표\n    const COL_RANK  = LEFT + 28;   // 순위 (우측 정렬)\n    const COL_ICON  = LEFT + 58;   // 캐릭터 아이콘 (중앙)\n    const COL_NAME  = LEFT + 84;   // 이름 (좌측 정렬)\n    const COL_SCORE = LEFT + ROW_W - 8; // 점수 (우측 정렬)\n\n    // ── 헤더 구분선 ──────────────────────────────────────\n    const headerY = startY + 16;\n    const headerStyle = {\n      fontSize: '13px',\n      color: '#aaddff',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 3,\n    };\n    this.leaderboardTexts.push(\n      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),\n      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0, 0.5),\n      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),\n    );\n    const divider = this.add.rectangle(LEFT + ROW_W / 2, headerY + 11, ROW_W, 1, 0xaaddff, 0.5);\n    this.leaderboardTexts.push(divider);\n\n    // ── 데이터 없음 ──────────────────────────────────────\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(\n        LEFT + ROW_W / 2, startY + 80,\n        '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!',\n        { fontSize: '18px', color: '#ccc', stroke: '#000', strokeThickness: 3, align: 'center' }\n      ).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    // ── 각 행 ────────────────────────────────────────────\n    this.leaderboardData.forEach((entry, index) => {\n      const rowY = startY + 38 + index * ROW_H;\n      const cy = rowY + ROW_H / 2;\n\n      // 행 배경\n      const bgColor =\n        entry.rank === 1 ? 0x4a3a00 :\n        entry.rank === 2 ? 0x2a2a35 :\n        entry.rank === 3 ? 0x3a2010 :\n        index % 2 === 0  ? 0x0a0a18 : 0x121220;\n      const bgAlpha = entry.rank <= 3 ? 0.85 : 0.55;\n      const bg = this.add.rectangle(LEFT + ROW_W / 2, cy, ROW_W, ROW_H - 2, bgColor, bgAlpha);\n      this.leaderboardTexts.push(bg);\n\n      // 상위 3위 왼쪽 테두리 강조\n      if (entry.rank <= 3) {\n        const accentColor = entry.rank === 1 ? 0xFFD700 : entry.rank === 2 ? 0xC0C0C0 : 0xCD7F32;\n        const accent = this.add.rectangle(LEFT + 1, cy, 3, ROW_H - 2, accentColor, 1);\n        this.leaderboardTexts.push(accent);\n      }\n\n      // 순위 색상\n      const rankColor =\n        entry.rank === 1 ? '#FFD700' :\n        entry.rank === 2 ? '#C0C0C0' :\n        entry.rank === 3 ? '#CD7F32' : '#aaaaaa';\n\n      // 순위\n      const rankLabel = entry.rank <= 3\n        ? ['🥇', '🥈', '🥉'][entry.rank - 1]\n        : `${entry.rank}`;\n      this.leaderboardTexts.push(\n        this.add.text(COL_RANK, cy, rankLabel, {\n          fontSize: entry.rank <= 3 ? '18px' : '15px',\n          color: rankColor,\n          fontStyle: 'bold',\n          stroke: '#000',\n          strokeThickness: 3,\n        }).setOrigin(1, 0.5)\n      );\n\n      // 캐릭터 아이콘\n      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];\n      this.leaderboardTexts.push(\n        this.add.image(COL_ICON, cy, charDef.imageKey).setDisplaySize(28, 28).setOrigin(0.5)\n      );\n\n      // 이름\n      this.leaderboardTexts.push(",
  "new_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const startY = 130 + yOff;\n    const ROW_H = 38;\n    // 좌우 여백 8px씩 — 전체 행이 x=8~392로 캔버스를 꽉 채움\n    const LEFT = 8;\n    const ROW_W = 384;\n    const CX = LEFT + ROW_W / 2; // 200\n\n    // 컬럼 x 좌표 (4구역으로 균등 분배)\n    // [순위 50px][아이콘 40px][이름 180px][점수 114px]\n    const COL_RANK  = LEFT + 38;        // 순위: 우측 정렬, 0~50 구역\n    const COL_ICON  = LEFT + 69;        // 아이콘: 중앙, 50~90 구역\n    const COL_NAME  = LEFT + 95;        // 이름: 좌측 정렬, 90~270 구역\n    const COL_SCORE = LEFT + ROW_W - 6; // 점수: 우측 정렬\n\n    // ── 헤더 ────────────────────────────────────────────\n    const headerY = startY + 16;\n    const headerStyle = {\n      fontSize: '13px',\n      color: '#aaddff',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 3,\n    };\n    this.leaderboardTexts.push(\n      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),\n      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0, 0.5),\n      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),\n    );\n    const divider = this.add.rectangle(CX, headerY + 11, ROW_W, 1, 0xaaddff, 0.5);\n    this.leaderboardTexts.push(divider);\n\n    // ── 데이터 없음 ──────────────────────────────────────\n    if (this.leaderboardData.length === 0) {\n      const noDataText = this.add.text(\n        CX, startY + 80,\n        '아직 랭킹이 없습니다\\n\\n첫 번째 플레이어가 되어보세요!',\n        { fontSize: '18px', color: '#ccc', stroke: '#000', strokeThickness: 3, align: 'center' }\n      ).setOrigin(0.5);\n      this.leaderboardTexts.push(noDataText);\n      return;\n    }\n\n    // ── 각 행 ────────────────────────────────────────────\n    this.leaderboardData.forEach((entry, index) => {\n      const rowY = startY + 38 + index * ROW_H;\n      const cy = rowY + ROW_H / 2;\n\n      // 행 배경\n      const bgColor =\n        entry.rank === 1 ? 0x4a3a00 :\n        entry.rank === 2 ? 0x2a2a35 :\n        entry.rank === 3 ? 0x3a2010 :\n        index % 2 === 0  ? 0x0a0a18 : 0x121220;\n      const bgAlpha = entry.rank <= 3 ? 0.85 : 0.55;\n      const bg = this.add.rectangle(CX, cy, ROW_W, ROW_H - 2, bgColor, bgAlpha);\n      this.leaderboardTexts.push(bg);\n\n      // 상위 3위 왼쪽 테두리 강조\n      if (entry.rank <= 3) {\n        const accentColor = entry.rank === 1 ? 0xFFD700 : entry.rank === 2 ? 0xC0C0C0 : 0xCD7F32;\n        const accent = this.add.rectangle(LEFT + 1, cy, 3, ROW_H - 2, accentColor, 1);\n        this.leaderboardTexts.push(accent);\n      }\n\n      // 순위 색상\n      const rankColor =\n        entry.rank === 1 ? '#FFD700' :\n        entry.rank === 2 ? '#C0C0C0' :\n        entry.rank === 3 ? '#CD7F32' : '#aaaaaa';\n\n      // 순위 (숫자만)\n      this.leaderboardTexts.push(\n        this.add.text(COL_RANK, cy, `${entry.rank}`, {\n          fontSize: '15px',\n          color: rankColor,\n          fontStyle: 'bold',\n          stroke: '#000',\n          strokeThickness: 3,\n        }).setOrigin(1, 0.5)\n      );\n\n      // 캐릭터 아이콘\n      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];\n      this.leaderboardTexts.push(\n        this.add.image(COL_ICON, cy, charDef.imageKey).setDisplaySize(30, 30).setOrigin(0.5)\n      );\n\n      // 이름\n      this.leaderboardTexts.push("
}
```

> TOOL

tool_result
id: toolu_015h5vWmmrBP8xkhsgQuCvG8
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이제 이름/점수 텍스트 부분도 COL_SCORE 변수가 바뀐 것에 맞게 확인할게요.

> TOOL

tool_use Read
id: toolu_014f7f5VzDLBGGeCtVoU5uzh
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "offset": 378,
  "limit": 35
}
```

> TOOL

tool_result
id: toolu_014f7f5VzDLBGGeCtVoU5uzh
```
378	          fontFamily: 'monospace',
379	          fontStyle: 'bold',
380	          stroke: '#000',
381	          strokeThickness: 3,
382	        }).setOrigin(0, 0.5)
383	      );
384	
385	      // 점수
386	      this.leaderboardTexts.push(
387	        this.add.text(COL_SCORE, cy, entry.score.toLocaleString(), {
388	          fontSize: '15px',
389	          color: entry.rank <= 3 ? rankColor : '#ffffff',
390	          fontFamily: 'monospace',
391	          fontStyle: 'bold',
392	          stroke: '#000',
393	          strokeThickness: 3,
394	        }).setOrigin(1, 0.5)
395	      );
396	    });
397	  }
398	
399	  /** 이번 달 말일까지 남은 일수 */
400	  private calcDaysUntilMonthEnd(): number {
401	    const now = new Date();
402	    const lastDay = new Date(now.getFullYear(), now.getMonth() + 1, 0);
403	    const diff = lastDay.getTime() - now.getTime();
404	    return Math.max(0, Math.ceil(diff / (1000 * 60 * 60 * 24)));
405	  }
406	
407	  /** 보상수령 버튼 상태 갱신 */
408	  private updateRewardUI() {
409	    if (!this.rewardBtnBg || !this.rewardBtnLabel) return;
410	
411	    const btn = this.rewardBtnBg;
412	    const label = this.rewardBtnLabel;
```

> TOOL

tool_use Bash
id: toolu_013N1vvQL1Wbf3VzQpW5RYRm
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_013N1vvQL1Wbf3VzQpW5RYRm
```
(Bash completed with no output)
```

> AGENT

완료입니다. 변경 내용:

**메달 이모지 제거** — 1, 2, 3위 모두 금/은/동 색상 숫자로 표시

**레이아웃 재설계** — 좌우 8px 여백으로 캔버스를 거의 꽉 채우고, 4구역으로 균등 분배:

```
[순위 50px] [아이콘 40px] [이름 180px] [점수 114px]
    x=38         x=69         x=95         x=386
```

이전에는 아이콘이 x=20, 텍스트가 x=214로 떨어져 있었는데, 이제 `순위 → 아이콘 → 이름 → 점수`가 모두 연속된 흐름으로 배치됩니다. 이름 컬럼에 180px를 배정해서 점수와의 사이 공백도 자연스럽게 채워집니다.

> DEVELOPER

스크린샷 2026-05-15 오후 3.35.18 이거 봐바

> TOOL

tool_use Read
id: toolu_01UwTeGbQowLkw32cZtmSDYq
```json
{
  "file_path": "/Users/johyunduk/Downloads/스크린샷 2026-05-15 오후 3.35.18.png"
}
```

> TOOL

tool_result ERROR
id: toolu_01UwTeGbQowLkw32cZtmSDYq
```
File does not exist. Note: your current working directory is /Users/johyunduk/Projects/ddong-avoid-game.
```

> TOOL

tool_use Bash
id: toolu_01Y66m3eBdJ1XzMFrWVBk8MC
```json
{
  "command": "find /Users/johyunduk -name \"스크린샷 2026-05-15 오후 3.35.18*\" 2>/dev/null",
  "description": "Find screenshot file"
}
```

> TOOL

tool_result ERROR
id: toolu_01Y66m3eBdJ1XzMFrWVBk8MC
```
The user doesn't want to proceed with this tool use. The tool use was rejected (eg. if it was a file edit, the new_string was NOT written to the file). STOP what you are doing and wait for the user to tell you how to proceed.

Note: The user's next message may contain a correction or preference. Pay close attention — if they explain what went wrong or how they'd prefer you to work, consider saving that to memory for future sessions.
```

> DEVELOPER

데스크탑에 있을거야

> TOOL

tool_use Read
id: toolu_01RXHCYDCmi8DL4nemjBqny3
```json
{
  "file_path": "/Users/johyunduk/Desktop/스크린샷 2026-05-15 오후 3.35.18.png"
}
```

> TOOL

tool_result
id: toolu_01RXHCYDCmi8DL4nemjBqny3
```
{
  "type": "image",
  "source": {
    "type": "base64",
    "data": "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",
    "media_type": "image/png"
  }
}
```

> AGENT

꽤 괜찮아 보이네요! 캐릭터 아이콘도 잘 나오고, 1~3위 배경 색조 + 왼쪽 강조선도 자연스럽습니다.

눈에 띄는 부분이 있다면:
- **순위 컬럼 헤더** "순위" 텍스트가 카드 왼쪽 가장자리에 약간 붙어 있어 보임
- **행 간격**이 적당한지 — 6명 항목이 화면 아래 버튼과 너무 가깝진 않은지

추가로 개선하고 싶은 부분이 있으신가요? 아니면 이 정도면 괜찮으신가요?

> DEVELOPER

뭐가 괜찮아 왼쪽으로 치우쳐져있잖아

> AGENT

다시 보니 카드 안에서 순위+아이콘+이름이 전부 왼쪽 절반에 몰려 있고 오른쪽에 점수 하나만 있어서 시각적 무게가 왼쪽으로 쏠리는 거네요. 이름 컬럼을 가운데 구역에 center-align으로 바꿀게요.

> TOOL

tool_use Edit
id: toolu_01QJNX8UaJUjwjc6FDLQudCQ
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "    // 컬럼 x 좌표 (4구역으로 균등 분배)\n    // [순위 50px][아이콘 40px][이름 180px][점수 114px]\n    const COL_RANK  = LEFT + 38;        // 순위: 우측 정렬, 0~50 구역\n    const COL_ICON  = LEFT + 69;        // 아이콘: 중앙, 50~90 구역\n    const COL_NAME  = LEFT + 95;        // 이름: 좌측 정렬, 90~270 구역\n    const COL_SCORE = LEFT + ROW_W - 6; // 점수: 우측 정렬\n\n    // ── 헤더 ────────────────────────────────────────────\n    const headerY = startY + 16;\n    const headerStyle = {\n      fontSize: '13px',\n      color: '#aaddff',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 3,\n    };\n    this.leaderboardTexts.push(\n      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),\n      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0, 0.5),\n      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),\n    );",
  "new_string": "    // 컬럼 x 좌표\n    // [순위 50px] [아이콘 44px] [← 이름 중앙 정렬 →] [점수 110px]\n    const COL_RANK       = LEFT + 40;          // 순위: 우측 정렬\n    const COL_ICON       = LEFT + 72;          // 아이콘: 중앙\n    const ICON_R         = LEFT + 89;          // 아이콘 오른쪽 끝\n    const SCORE_L        = LEFT + ROW_W - 110; // 점수 구역 왼쪽 끝\n    const COL_NAME       = (ICON_R + SCORE_L) / 2; // 이름: 중앙 정렬\n    const COL_SCORE      = LEFT + ROW_W - 6;   // 점수: 우측 정렬\n\n    // ── 헤더 ────────────────────────────────────────────\n    const headerY = startY + 16;\n    const headerStyle = {\n      fontSize: '13px',\n      color: '#aaddff',\n      fontStyle: 'bold',\n      stroke: '#000',\n      strokeThickness: 3,\n    };\n    this.leaderboardTexts.push(\n      this.add.text(COL_RANK, headerY, '순위', headerStyle).setOrigin(1, 0.5),\n      this.add.text(COL_NAME, headerY, '이름', headerStyle).setOrigin(0.5, 0.5),\n      this.add.text(COL_SCORE, headerY, '점수', headerStyle).setOrigin(1, 0.5),\n    );"
}
```

> TOOL

tool_result
id: toolu_01QJNX8UaJUjwjc6FDLQudCQ
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이름 텍스트의 origin도 center로 바꿉니다.

> TOOL

tool_use Read
id: toolu_01PL9K6Ln1WbPPotQMLV359f
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "offset": 370,
  "limit": 25
}
```

> TOOL

tool_result
id: toolu_01PL9K6Ln1WbPPotQMLV359f
```
370	      const charDef = CHARACTERS.find(c => c.id === (entry.characterType ?? 'chibi')) ?? CHARACTERS[0];
371	      this.leaderboardTexts.push(
372	        this.add.image(COL_ICON, cy, charDef.imageKey).setDisplaySize(30, 30).setOrigin(0.5)
373	      );
374	
375	      // 이름
376	      this.leaderboardTexts.push(
377	        this.add.text(COL_NAME, cy, entry.userName, {
378	          fontSize: '15px',
379	          color: entry.rank <= 3 ? '#ffffff' : '#dddddd',
380	          fontFamily: 'monospace',
381	          fontStyle: 'bold',
382	          stroke: '#000',
383	          strokeThickness: 3,
384	        }).setOrigin(0, 0.5)
385	      );
386	
387	      // 점수
388	      this.leaderboardTexts.push(
389	        this.add.text(COL_SCORE, cy, entry.score.toLocaleString(), {
390	          fontSize: '15px',
391	          color: entry.rank <= 3 ? rankColor : '#ffffff',
392	          fontFamily: 'monospace',
393	          fontStyle: 'bold',
394	          stroke: '#000',
```

> TOOL

tool_use Edit
id: toolu_01PSFYqw3MpRuevxR2bMQ6yB
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "        }).setOrigin(0, 0.5)\n      );\n\n      // 점수",
  "new_string": "        }).setOrigin(0.5, 0.5)\n      );\n\n      // 점수"
}
```

> TOOL

tool_result
id: toolu_01PSFYqw3MpRuevxR2bMQ6yB
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01DUywBzwfqjZZhEpXQkknMn
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_01DUywBzwfqjZZhEpXQkknMn
```
(Bash completed with no output)
```

> AGENT

타입 에러 없음. 변경 내용:

**핵심 변경**: 이름 컬럼을 좌측 정렬 → **중앙 정렬**로 변경

```
이전: [순위][아이콘][이름...]........[점수]
                    ← 왼쪽 절반에 몰림

이후: [순위][아이콘]......[이름]......[점수]
                          ↑ 아이콘과 점수 구역 사이 정중앙
```

`ICON_R`(아이콘 오른쪽 끝)과 `SCORE_L`(점수 구역 왼쪽 끝)의 중간 지점을 계산해서 이름을 그 정중앙에 배치했습니다. 확인해보세요!

> DEVELOPER

그게 아니라 순위 테이블 자체가 가운데이 있지가 않다고

> TOOL

tool_result
id: toolu_01X4HYmWfUFgArRottP7YdXR
```
284	  private displayLeaderboard() {
285	    const yOff = (this.scale.height - 600) / 2;
286	    const startY = 130 + yOff;
287	    const ROW_H = 38;
288	    // 좌우 여백 8px씩 — 전체 행이 x=8~392로 캔버스를 꽉 채움
289	    const LEFT = 8;
290	    const ROW_W = 384;
291	    const CX = LEFT + ROW_W / 2; // 200
292	
293	    // 컬럼 x 좌표
294	    // [순위 50px] [아이콘 44px] [← 이름 중앙 정렬 →] [점수 110px]
295	    const COL_RANK       = LEFT + 40;          // 순위: 우측 정렬
296	    const COL_ICON       = LEFT + 72;          // 아이콘: 중앙
297	    const ICON_R         = LEFT + 89;          // 아이콘 오른쪽 끝
298	    const SCORE_L        = LEFT + ROW_W - 110; // 점수 구역 왼쪽 끝
```

> AGENT

`create()`에서는 `this.scale.width`를 써서 동적으로 중앙을 계산하는데, `displayLeaderboard()`에서는 `LEFT=8, ROW_W=384`를 하드코딩해서 `CX=200`으로 고정해버린 게 문제네요. 실제 캔버스 너비가 다르면 어긋납니다.

> TOOL

tool_use Read
id: toolu_01X4HYmWfUFgArRottP7YdXR
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "offset": 284,
  "limit": 15
}
```

> TOOL

tool_use Edit
id: toolu_01CrnwqZLXfsxfhhrLKsirzU
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "  private displayLeaderboard() {\n    const yOff = (this.scale.height - 600) / 2;\n    const startY = 130 + yOff;\n    const ROW_H = 38;\n    // 좌우 여백 8px씩 — 전체 행이 x=8~392로 캔버스를 꽉 채움\n    const LEFT = 8;\n    const ROW_W = 384;\n    const CX = LEFT + ROW_W / 2; // 200\n\n    // 컬럼 x 좌표\n    // [순위 50px] [아이콘 44px] [← 이름 중앙 정렬 →] [점수 110px]\n    const COL_RANK       = LEFT + 40;          // 순위: 우측 정렬\n    const COL_ICON       = LEFT + 72;          // 아이콘: 중앙\n    const ICON_R         = LEFT + 89;          // 아이콘 오른쪽 끝\n    const SCORE_L        = LEFT + ROW_W - 110; // 점수 구역 왼쪽 끝\n    const COL_NAME       = (ICON_R + SCORE_L) / 2; // 이름: 중앙 정렬\n    const COL_SCORE      = LEFT + ROW_W - 6;   // 점수: 우측 정렬",
  "new_string": "  private displayLeaderboard() {\n    const W = this.scale.width;\n    const yOff = (this.scale.height - 600) / 2;\n    const startY = 130 + yOff;\n    const ROW_H = 38;\n    const PAD = 8;\n    const ROW_W = W - PAD * 2;\n    const LEFT = PAD;\n    const CX = W / 2;\n\n    // 컬럼 x 좌표 (모두 W 기준 비율 계산)\n    // [순위 50px] [아이콘 44px] [← 이름 중앙 정렬 →] [점수 110px]\n    const COL_RANK       = LEFT + 40;\n    const COL_ICON       = LEFT + 72;\n    const ICON_R         = LEFT + 89;\n    const SCORE_L        = LEFT + ROW_W - 110;\n    const COL_NAME       = (ICON_R + SCORE_L) / 2;\n    const COL_SCORE      = LEFT + ROW_W - 6;"
}
```

> TOOL

tool_result
id: toolu_01CrnwqZLXfsxfhhrLKsirzU
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

이제 헤더와 각 행의 배경 rect도 CX 기준으로 되어있는지 확인할게요.

> TOOL

tool_use Bash
id: toolu_01VtPfnHJmWgDFTXGk3p2zp5
```json
{
  "command": "grep -n \"add.rectangle\\|LEFT + ROW_W / 2\\|LEFT + ROW\" /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts | head -20",
  "description": "Check rectangle positioning in displayLeaderboard"
}
```

> TOOL

tool_result
id: toolu_01VtPfnHJmWgDFTXGk3p2zp5
```
96:    this.rewardBtnBg = this.add.rectangle(cx - 80, rbY, 150, 40, 0x555555, 1);
133:      const button = this.add.rectangle(
299:    const SCORE_L        = LEFT + ROW_W - 110;
301:    const COL_SCORE      = LEFT + ROW_W - 6;
317:    const divider = this.add.rectangle(CX, headerY + 11, ROW_W, 1, 0xaaddff, 0.5);
343:      const bg = this.add.rectangle(CX, cy, ROW_W, ROW_H - 2, bgColor, bgAlpha);
349:        const accent = this.add.rectangle(LEFT + 1, cy, 3, ROW_H - 2, accentColor, 1);
492:    const button = this.add.rectangle(cx, y, 150, 40, 0xffffff, 1);
```

> AGENT

모든 rect가 이미 `CX` 기준. 이제 `noDataText`도 확인합니다.

> TOOL

tool_use Bash
id: toolu_01NCfueofkpK8RCfFZcAZpmW
```json
{
  "command": "grep -n \"LEFT + ROW_W / 2\" /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "description": "Check for remaining hardcoded center references"
}
```

> TOOL

tool_result
id: toolu_01NCfueofkpK8RCfFZcAZpmW
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01BovEQ95bdgxajWxsvv7ddZ
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_01BovEQ95bdgxajWxsvv7ddZ
```
(Bash completed with no output)
```

> AGENT

수정 완료입니다. 핵심 변경:

```typescript
// 이전 — 하드코딩
const LEFT = 8;
const ROW_W = 384;
const CX = 200;  // W=400 가정

// 이후 — 실제 캔버스 너비 기준
const W = this.scale.width;
const ROW_W = W - PAD * 2;
const CX = W / 2;  // 항상 진짜 중앙
```

`create()`의 다른 요소들(타이틀, 난이도 버튼 등)은 이미 `this.scale.width`를 쓰고 있었는데, `displayLeaderboard()`만 혼자 400px 고정값을 쓰고 있었던 게 원인이었습니다.

> DEVELOPER

너무 가로로 꽉차있으니까 별로다

> TOOL

tool_use Edit
id: toolu_012M1XraieitHprjsLiP3pt5
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "    const PAD = 8;\n    const ROW_W = W - PAD * 2;",
  "new_string": "    const PAD = 24;\n    const ROW_W = W - PAD * 2;"
}
```

> TOOL

tool_result
id: toolu_012M1XraieitHprjsLiP3pt5
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01GK3BaLczEqfnGcSKRxhMVw
```json
{
  "command": "npx tsc --noEmit 2>&1",
  "description": "TypeScript type check"
}
```

> TOOL

tool_result
id: toolu_01GK3BaLczEqfnGcSKRxhMVw
```
(Bash completed with no output)
```

> AGENT

좌우 여백을 8px → 24px로 늘렸습니다. 이제 양쪽에 24px씩 여백이 생겨서 ROW_W = W - 48px이 됩니다. 확인해보시고 더 여유롭게 하고 싶으면 말씀해 주세요.

> DEVELOPER

좀만 더 줄여줘. 48px 씩으로

> TOOL

tool_use Edit
id: toolu_01Hg9e3aN9KqSfm6t5ogYkcM
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts",
  "old_string": "    const PAD = 24;",
  "new_string": "    const PAD = 48;"
}
```

> TOOL

tool_result
id: toolu_01Hg9e3aN9KqSfm6t5ogYkcM
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/scenes/LeaderboardScene.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

완료. 좌우 48px씩 여백이 생겨서 ROW_W = W - 96px이 됩니다.

> DEVELOPER

아까 점수 제출 명령어 뭐 해야 한다고?

> AGENT

```bash
supabase functions deploy leaderboard-submit --no-verify-jwt
```

`mugi`, `gumi`, `knight` 유효 캐릭터 목록 추가한 거 반영하려면 이거 한 번 실행해주시면 됩니다.

> DEVELOPER

레거시 지금 능력이 1.2배 시키는게 상시 1.2배인가?

> TOOL

tool_use Read
id: toolu_01PFh82DxbkkMYC7Nmyy5sfk
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/abilities"
}
```

> TOOL

tool_result ERROR
id: toolu_01PFh82DxbkkMYC7Nmyy5sfk
```
EISDIR: illegal operation on a directory, read '/Users/johyunduk/Projects/ddong-avoid-game/src/abilities'
```

> TOOL

tool_use Bash
id: toolu_01XeAGvf3T6qBa7er9E2ajEt
```json
{
  "command": "find /Users/johyunduk/Projects/ddong-avoid-game/src/abilities -name \"*egacy*\" -o -name \"*Legacy*\"",
  "description": "Find Legacy ability file"
}
```

> TOOL

tool_result
id: toolu_01XeAGvf3T6qBa7er9E2ajEt
```
/Users/johyunduk/Projects/ddong-avoid-game/src/abilities/LegacyAbility.ts
```

> TOOL

tool_use Read
id: toolu_014dq5YdKA6xzmtw3HyNWbjw
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/abilities/LegacyAbility.ts"
}
```

> TOOL

tool_result
id: toolu_014dq5YdKA6xzmtw3HyNWbjw
```
1	import { BaseAbility } from './BaseAbility';
2	import type { GameSceneAPI } from './types';
3	import type PoolablePoopBase from '../objects/PoolablePoopBase';
4	import { LEGACY_PARAMS } from '../config/abilityParams';
5	import { ensureGlowDot } from '../utils/glowDot';
6	
7	/**
8	 * 레거시 (UR) — 피버 + 레거시 모드
9	 * ★0: 6초 피버 / 불태우기 30%/2개(일반) 60%/4개(레거시) / 500점마다 / 10초 / 1.2배
10	 * ★1: 8초 / 35%/2개 65%/4개 / 450점마다 / 10초 / 1.25배
11	 * ★2: 10초 / 40%/3개 70%/4개 / 400점마다 / 12초 / 1.30배
12	 * ★3: 12초 / 45%/3개 75%/4개 / 350점마다 / 15초 / 1.35배 + 모드 종료 직후 3초 미니 피버
13	 */
14	
15	interface RainStarData {
16	  startX: number; startY: number;
17	  travelX: number; travelY: number;
18	  startRot: number; rotDelta: number;
19	  alpha: number; whiteAlpha: number;
20	  s: number; col: number;
21	  startTime: number; endTime: number; duration: number;
22	}
23	
24	export class LegacyAbility extends BaseAbility {
25	  private startFeverActive = false;
26	  private legacyModeActive = false;
27	  private accum           = 0;
28	  private lastLegacyScore = 0;
29	
30	  private legacyTopGlow?:       Phaser.GameObjects.Graphics;
31	  private legacyPulseTween?:    Phaser.Tweens.Tween;
32	  private legacyRainTimer?:     Phaser.Time.TimerEvent;
33	  private legacyEndTimer?:      Phaser.Time.TimerEvent;
34	  private startFeverTimer?:     Phaser.Time.TimerEvent;
35	  private startFeverEndTimer?:  Phaser.Time.TimerEvent;
36	
37	  // A: 상시 불꽃 오라
38	  private oraTimer = 0;
39	  private static readonly ORA_INTERVAL_NORMAL = 180;
40	  private static readonly ORA_INTERVAL_LEGACY =  80;
41	  private static readonly ORA_COLS_NORMAL = [0xff3300, 0xff6600, 0xffaa00];
42	  private static readonly ORA_COLS_LEGACY = [0xffaa00, 0xffcc00, 0xffee44, 0xffffff];
43	
44	  // D: 빗줄기 색상
45	  private static readonly RAIN_COLS_FEVER  = [0xff8800, 0xffaa00, 0xffcc00, 0xffee00];
46	  private static readonly RAIN_COLS_LEGACY = [0xff5500, 0xff8800, 0xffaa00, 0xffcc00];
47	
48	  // D: 빗줄기 별 배치 — 단일 Graphics + 데이터 배열로 N개 draw call → 1개로 축소
49	  private rainStarGfx: Phaser.GameObjects.Graphics | null = null;
50	  private rainStars: RainStarData[] = [];
51	
52	  // 8각 별 정규화 좌표 (크기=1) — 프레임당 재사용하는 회전 버퍼와 함께 GC 압력 제거
53	  private static readonly _STAR_NORM: { x: number; y: number }[] = [
54	    { x:  0,    y: -1    }, { x:  0.4, y: -0.4 },
55	    { x:  1,    y:  0    }, { x:  0.4, y:  0.4 },
56	    { x:  0,    y:  1    }, { x: -0.4, y:  0.4 },
57	    { x: -1,    y:  0    }, { x: -0.4, y: -0.4 },
58	  ];
59	  private static readonly _STAR_BUF: { x: number; y: number }[] =
60	    Array.from({ length: 8 }, () => ({ x: 0, y: 0 }));
61	
62	  // ── 불꽃 물방울 다각형 좌표 ─────────────────────────────────────────
63	  private static flamePts(w: number, h: number) {
64	    return [
65	      { x:  0,         y: -h        },
66	      { x:  w * 0.55,  y: -h * 0.1  },
67	      { x:  w * 0.75,  y:  h * 0.35 },
68	      { x:  w * 0.3,   y:  h        },
69	      { x: -w * 0.3,   y:  h        },
70	      { x: -w * 0.75,  y:  h * 0.35 },
71	      { x: -w * 0.55,  y: -h * 0.1  },
72	    ];
73	  }
74	
75	  // ─────────────────────────────────────────────────────────────────
76	  // 생명주기
77	  // ─────────────────────────────────────────────────────────────────
78	
79	  override onCreate(api: GameSceneAPI): void {
80	    ensureGlowDot(api.scene);
81	    this.rainStarGfx = api.scene.add.graphics().setDepth(85);
82	    this.rainStars   = [];
83	
84	    this.startFeverActive = true;
85	    this.startFeverRain(api);
86	    this.startFeverEndTimer = api.scene.time.delayedCall(LEGACY_PARAMS.feverDuration, () => {
87	      this.startFeverActive = false;
88	    });
89	  }
90	
91	  override onUpdate(api: GameSceneAPI): void {
92	    const delta = api.scene.game.loop.delta;
93	    this.oraTimer += delta;
94	    const interval = this.legacyModeActive
95	      ? LegacyAbility.ORA_INTERVAL_LEGACY
96	      : LegacyAbility.ORA_INTERVAL_NORMAL;
97	    if (this.oraTimer >= interval) {
98	      this.oraTimer -= interval;
99	      this.spawnOraFlame(api);
100	    }
101	
102	    if (this.rainStars.length > 0) {
103	      this._updateRainStars(api.scene);
104	    }
105	  }
106	
107	  override getTickScore(base: number): number {
108	    if (!this.legacyModeActive) return base;
109	    this.accum += base * LEGACY_PARAMS.scoreExtra;
110	    const bonus = Math.floor(this.accum);
111	    this.accum -= bonus;
112	    return base + bonus;
113	  }
114	
115	  override overrideSpawnPoop(api: GameSceneAPI): boolean {
116	    if (this.startFeverActive) {
117	      api.spawnGoldPoop();
118	      api.spawnGoldPoop();
119	      return true;
120	    }
121	    return false;
122	  }
123	
124	  override onAfterSpawnPoop(api: GameSceneAPI): void {
125	    const chance = this.legacyModeActive ? LEGACY_PARAMS.burnChanceLegacy : LEGACY_PARAMS.burnChanceNormal;
126	    const count  = this.legacyModeActive ? LEGACY_PARAMS.burnCountLegacy  : LEGACY_PARAMS.burnCountNormal;
127	    if (Math.random() < chance) {
128	      this.burnRandomPoops(api, count);
129	    }
130	  }
131	
132	  override onScoreMilestone(score: number, api: GameSceneAPI): void {
133	    if (score % LEGACY_PARAMS.legacyInterval === 0 && score > this.lastLegacyScore) {
134	      this.lastLegacyScore = score;
135	      this.activateLegacyMode(api);
136	    }
137	  }
138	
139	  // ─────────────────────────────────────────────────────────────────
140	  // A: 상시 불꽃 오라 — glow_dot Image (Graphics → Image, 드로우콜 제거)
141	  // ─────────────────────────────────────────────────────────────────
142	
143	  private spawnOraFlame(api: GameSceneAPI): void {
144	    const scene = api.scene;
145	    const px    = api.player.x;
146	    const py    = api.player.y;
147	    const leg   = this.legacyModeActive;
148	    const cols  = leg ? LegacyAbility.ORA_COLS_LEGACY : LegacyAbility.ORA_COLS_NORMAL;
149	    const count = leg ? Phaser.Math.Between(5, 7) : Phaser.Math.Between(2, 3);
150	    const rMax  = leg ? 2.2  : 1.6;
151	    const aMax  = leg ? 0.90 : 0.70;
152	    const riseMin = leg ? 20  : 14;
153	    const riseMax = leg ? 42  : 28;
154	    const lifeMin = leg ? 280 : 180;
155	    const lifeMax = leg ? 520 : 380;
156	
157	    for (let i = 0; i < count; i++) {
158	      const r   = Phaser.Math.FloatBetween(0.8, rMax);
159	      const col = Phaser.Utils.Array.GetRandom(cols) as number;
160	      const a   = Phaser.Math.FloatBetween(0.50, aMax);
161	      const x   = px + Phaser.Math.Between(-10, 10);
162	      const y   = py + Phaser.Math.Between(10, 24);
163	
164	      const img = scene.add.image(x, y, 'glow_dot')
165	        .setBlendMode(Phaser.BlendModes.ADD)
166	        .setTint(col)
167	        .setScale(r / 10)
168	        .setAlpha(a)
169	        .setDepth(88);
170	
171	      scene.tweens.add({
172	        targets:  img,
173	        y:        y - Phaser.Math.Between(riseMin, riseMax),
174	        x:        x + Phaser.Math.Between(-4, 4),
175	        alpha:    0,
176	        scale:    0,
177	        duration: Phaser.Math.Between(lifeMin, lifeMax),
178	        ease:     'Quad.easeOut',
179	        onComplete: () => { if (img.active) img.destroy(); },
180	      });
181	    }
182	  }
183	
184	  // ─────────────────────────────────────────────────────────────────
185	  // B: 화염 추적선
186	  // ─────────────────────────────────────────────────────────────────
187	
188	  private drawFireTrail(
189	    scene: Phaser.Scene,
190	    fromX: number, fromY: number,
191	    toList: { x: number; y: number }[],
192	  ): void {
193	    if (toList.length === 0) return;
194	
195	    const gfx = scene.add.graphics();
196	    gfx.setDepth(195);
197	
198	    for (const { x, y } of toList) {
199	      gfx.lineStyle(3.5, 0xff6600, 0.50);
200	      gfx.beginPath(); gfx.moveTo(fromX, fromY); gfx.lineTo(x, y); gfx.strokePath();
201	      gfx.lineStyle(1.5, 0xffee00, 0.75);
202	      gfx.beginPath(); gfx.moveTo(fromX, fromY); gfx.lineTo(x, y); gfx.strokePath();
203	    }
204	
205	    scene.tweens.add({
206	      targets: gfx, alpha: 0, duration: 200, ease: 'Quad.easeOut',
207	      onComplete: () => { gfx.destroy(); },
208	    });
209	  }
210	
211	  // ─────────────────────────────────────────────────────────────────
212	  // C: 레거시 모드 활성화
213	  // ─────────────────────────────────────────────────────────────────
214	
215	  private activateLegacyMode(api: GameSceneAPI): void {
216	    if (this.legacyModeActive) return;
217	    this.legacyModeActive = true;
218	    this.accum = 0;
219	
220	    const scene = api.scene;
221	    const cx    = api.player.x;
222	    const cy    = api.player.y;
223	
224	    // ─ 반투명 플래시 ──────────────────────────────────────────────
225	    const flashOverlay = scene.add.graphics().setDepth(200).setScrollFactor(0);
226	    flashOverlay.fillStyle(0xffee00, 1);
227	    flashOverlay.fillRect(0, 0, scene.scale.width, scene.scale.height);
228	    flashOverlay.setAlpha(0.38);
229	    scene.tweens.add({
230	      targets: flashOverlay, alpha: 0, duration: 220, ease: 'Quad.easeOut',
231	      onComplete: () => { flashOverlay.destroy(); },
232	    });
233	
234	    // ─ 팽창 링 2개 ───────────────────────────────────────────────
235	    [{ delay: 0, maxScale: 4.3 }, { delay: 80, maxScale: 3.4 }].forEach(({ delay, maxScale }) => {
236	      const ring = scene.add.graphics().setDepth(155);
237	      ring.lineStyle(2.5, 0xffee00, 0.9);
238	      ring.strokeEllipse(0, 0, 74, 98);
239	      ring.setPosition(cx, cy);
240	      scene.tweens.add({
241	        targets: ring, scaleX: maxScale, scaleY: maxScale, alpha: 0,
242	        duration: 500, delay, ease: 'Quad.easeOut',
243	        onComplete: () => { ring.destroy(); },
244	      });
245	    });
246	
247	    // ─ 채움 타원 ─────────────────────────────────────────────────
248	    const fill = scene.add.graphics().setDepth(154);
249	    fill.fillStyle(0xffaa00, 0.28);
250	    fill.fillEllipse(0, 0, 74, 98);
251	    fill.setPosition(cx, cy);
252	    scene.tweens.add({
253	      targets: fill, alpha: 0, duration: 180, ease: 'Quad.easeOut',
254	      onComplete: () => { fill.destroy(); },
255	    });
256	
257	    // ─ 파편 8개 ──────────────────────────────────────────────────
258	    for (let i = 0; i < 8; i++) {
259	      const angle = (i / 8) * Math.PI * 2 + Phaser.Math.FloatBetween(-0.25, 0.25);
260	      const speed = Phaser.Math.FloatBetween(40, 95);
261	      const sw    = Phaser.Math.Between(5, 12);
262	      const sh    = Phaser.Math.Between(2, 5);
263	      const shard = scene.add.graphics().setDepth(156);
264	      shard.fillStyle(0xffee00, 1);
265	      shard.fillRect(-sw / 2, -sh / 2, sw, sh);
266	      shard.setPosition(cx, cy).setRotation(angle);
267	      scene.tweens.add({
268	        targets: shard,
269	        x: cx + Math.cos(angle) * speed, y: cy + Math.sin(angle) * speed,
270	        alpha: 0, rotation: angle + Phaser.Math.FloatBetween(-1, 1),
271	        duration: Phaser.Math.Between(270, 440), ease: 'Quad.easeOut',
272	        onComplete: () => { shard.destroy(); },
273	      });
274	    }
275	
276	    // ─ 화면 전체 불꽃 폭발 ────────────────────────────────
277	    const BURST_COLS = [0xff2200, 0xff6600, 0xffaa00, 0xffdd00, 0xffff88];
278	    for (let i = 0; i < 12; i++) {
279	      const gfx = scene.add.graphics();
280	      const w   = Phaser.Math.Between(4, 10);
281	      const h   = Phaser.Math.Between(10, 22);
282	      const col = Phaser.Utils.Array.GetRandom(BURST_COLS) as number;
283	
284	      gfx.fillStyle(col, Phaser.Math.FloatBetween(0.22, 0.50));
285	      gfx.fillPoints(LegacyAbility.flamePts(w, h), true);
286	      gfx.fillStyle(0xffee88, Phaser.Math.FloatBetween(0.28, 0.55));
287	      gfx.fillPoints(LegacyAbility.flamePts(w * 0.4, h * 0.5), true);
288	
289	      gfx.setPosition(Phaser.Math.Between(20, scene.scale.width - 20), Phaser.Math.Between(40, scene.scale.height - 40));
290	      gfx.setRotation(Phaser.Math.DegToRad(Phaser.Math.Between(-180, 180)));
291	      gfx.setDepth(158).setAlpha(0);
292	
293	      scene.tweens.add({
294	        targets: gfx, alpha: 1,
295	        scaleX: Phaser.Math.FloatBetween(1.2, 1.9),
296	        scaleY: Phaser.Math.FloatBetween(1.2, 1.9),
297	        duration: 140, delay: Phaser.Math.Between(0, 280), ease: 'Quad.easeOut',
298	        onComplete: () => {
299	          scene.tweens.add({
300	            targets: gfx, alpha: 0, y: gfx.y - Phaser.Math.Between(20, 50),
301	            duration: Phaser.Math.Between(380, 650), ease: 'Quad.easeIn',
302	            onComplete: () => { gfx.destroy(); },
303	          });
304	        },
305	      });
306	    }
307	
308	    // ─ 상단 노란빛 그라데이션 ────────────────────────────────────
309	    this.legacyTopGlow = scene.add.graphics();
310	    this.legacyTopGlow.fillGradientStyle(0xffee00, 0xffee00, 0xffee00, 0xffee00, 0.28, 0.28, 0, 0);
311	    this.legacyTopGlow.fillRect(0, 0, scene.scale.width, Math.round(scene.scale.height * 0.37));
312	    this.legacyTopGlow.setDepth(148).setScrollFactor(0);
313	
314	    this.legacyPulseTween = scene.tweens.add({
315	      targets: [this.legacyTopGlow], alpha: 0.55,
316	      duration: 600, yoyo: true, repeat: -1, ease: 'Sine.easeInOut',
317	    });
318	
319	    // ─ 레거시 모드 황금 빗줄기 (repeat: -1, 10초 후 remove로 정리) ─
320	    this.legacyRainTimer = scene.time.addEvent({
321	      delay: 120,
322	      repeat: -1,
323	      callback: () => { this.spawnRainStar(scene, LegacyAbility.RAIN_COLS_LEGACY, 0.75, 1.00, 3); },
324	    });
325	
326	    // 레거시 모드 종료
327	    this.legacyEndTimer = scene.time.delayedCall(LEGACY_PARAMS.legacyDuration, () => {
328	      this.legacyModeActive = false;
329	      this.legacyRainTimer?.remove();
330	      this.legacyRainTimer = undefined;
331	      this.legacyPulseTween?.stop();
332	      this.legacyPulseTween = undefined;
333	      scene.tweens.add({
334	        targets: [this.legacyTopGlow], alpha: 0, duration: 400, ease: 'Quad.easeOut',
335	        onComplete: () => {
336	          this.legacyTopGlow?.destroy();
337	          this.legacyTopGlow = undefined;
338	        },
339	      });
340	
341	    });
342	  }
343	
344	  // ─────────────────────────────────────────────────────────────────
345	  // D: 황금 빗줄기 — 단일 Graphics 배치 방식
346	  // ─────────────────────────────────────────────────────────────────
347	
348	  private startFeverRain(api: GameSceneAPI): void {
349	    const scene  = api.scene;
350	    const REPEAT = Math.floor(LEGACY_PARAMS.feverDuration / 140) - 1;
351	
352	    this.startFeverTimer = scene.time.addEvent({
353	      delay: 140,
354	      repeat: REPEAT,
355	      callback: () => { this.spawnRainStar(scene, LegacyAbility.RAIN_COLS_FEVER, 0.60, 0.90, 2); },
356	    });
357	  }
358	
359	  /** 빗줄기 별 데이터를 배열에 추가 — 실제 렌더링은 _updateRainStars에서 단일 Graphics로 일괄 처리 */
360	  private spawnRainStar(
361	    scene: Phaser.Scene,
362	    cols: readonly number[],
363	    aMin: number,
364	    aMax: number,
365	    count: number,
366	  ): void {
367	    if (!this.rainStarGfx) return;
368	    const now = scene.time.now;
369	    for (let i = 0; i < count; i++) {
370	      const s        = Phaser.Math.FloatBetween(2.5, 5.5);
371	      const col      = Phaser.Utils.Array.GetRandom(cols as number[]) as number;
372	      const alpha    = Phaser.Math.FloatBetween(aMin, aMax);
373	      const duration = Phaser.Math.Between(2200, 3600);
374	      this.rainStars.push({
375	        startX:     Phaser.Math.Between(10, scene.scale.width - 10),
376	        startY:     -15,
377	        travelX:    Phaser.Math.Between(-25, 25),
378	        travelY:    Phaser.Math.Between(450, 600),
379	        startRot:   Phaser.Math.DegToRad(Phaser.Math.Between(0, 360)),
380	        rotDelta:   Phaser.Math.FloatBetween(1.5, 3.0),
381	        alpha,
382	        whiteAlpha: aMax > 0.85 ? 0.65 : 0.50,
383	        s, col,
384	        startTime: now,
385	        endTime:   now + duration,
386	        duration,
387	      });
388	    }
389	  }
390	
391	  /** 단일 Graphics를 clear → 전체 별 재드로우 (N draw call → 1) */
392	  private _updateRainStars(scene: Phaser.Scene): void {
393	    const gfx = this.rainStarGfx;
394	    if (!gfx) return;
395	    const now = scene.time.now;
396	    gfx.clear();
397	    const remaining: RainStarData[] = [];
398	    for (const star of this.rainStars) {
399	      if (now >= star.endTime) continue;
400	      const t   = (now - star.startTime) / star.duration;
401	      const cx  = star.startX + t * star.travelX;
402	      const cy  = star.startY + t * star.travelY;
403	      const rot = star.startRot + t * star.rotDelta;
404	      const a   = star.alpha * (1 - t);
405	      const wA  = star.whiteAlpha * (1 - t);
406	
407	      gfx.fillStyle(star.col, a);
408	      gfx.fillPoints(this._rotatedStarPts(cx, cy, star.s, rot), true);
409	      gfx.fillStyle(0xffffff, wA);
410	      gfx.fillCircle(cx, cy, star.s * 0.32);
411	
412	      remaining.push(star);
413	    }
414	    this.rainStars = remaining;
415	  }
416	
417	  /** 8각 별 좌표를 회전·스케일·이동 적용해 정적 버퍼에 in-place 기록 (GC 제로) */
418	  private _rotatedStarPts(cx: number, cy: number, s: number, rot: number): { x: number; y: number }[] {
419	    const buf  = LegacyAbility._STAR_BUF;
420	    const norm = LegacyAbility._STAR_NORM;
421	    const cos  = Math.cos(rot);
422	    const sin  = Math.sin(rot);
423	    for (let i = 0; i < 8; i++) {
424	      const p  = norm[i]!;
425	      buf[i]!.x = cx + (p.x * cos - p.y * sin) * s;
426	      buf[i]!.y = cy + (p.x * sin + p.y * cos) * s;
427	    }
428	    return buf;
429	  }
430	
431	  // ─────────────────────────────────────────────────────────────────
432	  // 불태우기 로직
433	  // ─────────────────────────────────────────────────────────────────
434	
435	  private burnRandomPoops(api: GameSceneAPI, count: number): void {
436	    const visible = api.poops.getChildren().filter(
437	      c => c.active && (c as Phaser.Physics.Arcade.Sprite).y > -10,
438	    ) as Phaser.Physics.Arcade.Sprite[];
439	
440	    if (visible.length === 0) return;
441	
442	    // Partial Fisher-Yates: count개만 앞으로 뽑아내고 나머지 순회 생략
443	    const pool = visible.slice();
444	    const take = Math.min(count, pool.length);
445	    for (let i = 0; i < take; i++) {
446	      const j = i + Math.floor(Math.random() * (pool.length - i));
447	      [pool[i], pool[j]] = [pool[j], pool[i]];
448	    }
449	    const targets = pool.slice(0, take);
450	
451	    this.drawFireTrail(
452	      api.scene,
453	      api.player.x, api.player.y,
454	      targets.map(p => ({ x: p.x, y: p.y })),
455	    );
456	
457	    for (const poop of targets) {
458	      if (!poop.active) continue;
459	      this.playBurnEffect(api.scene, poop.x, poop.y);
460	      (poop as PoolablePoopBase).recycle();
461	      api.addAbilityBonus(10);
462	    }
463	  }
464	
465	  // ─────────────────────────────────────────────────────────────────
466	  // 리소스 정리 (게임 오버 시 GameScene에서 호출)
467	  // ─────────────────────────────────────────────────────────────────
468	
469	  override onDestroy(_api: GameSceneAPI): void {
470	    this.startFeverEndTimer?.remove();
471	    this.startFeverTimer?.remove();
472	    this.legacyEndTimer?.remove();
473	    this.legacyRainTimer?.remove();
474	    this.legacyPulseTween?.stop();
475	    this.legacyTopGlow?.destroy();
476	    this.rainStarGfx?.destroy();
477	    this.rainStarGfx = null;
478	    this.rainStars = [];
479	  }
480	
481	  // ─────────────────────────────────────────────────────────────────
482	  // 불꽃 소멸 이펙트
483	  // ─────────────────────────────────────────────────────────────────
484	
485	  private playBurnEffect(scene: Phaser.Scene, cx: number, cy: number): void {
486	    const flash = scene.add.graphics();
487	    flash.fillStyle(0xff7700, 0.60); flash.fillCircle(0, 0, 17);
488	    flash.fillStyle(0xffee88, 0.45); flash.fillCircle(0, 0, 9);
489	    flash.setPosition(cx, cy).setDepth(202);
490	    scene.tweens.add({
491	      targets: flash, scaleX: 2.8, scaleY: 2.8, alpha: 0,
492	      duration: 190, ease: 'Quad.easeOut',
493	      onComplete: () => { flash.destroy(); },
494	    });
495	
496	    for (let i = 0; i < 6; i++) {
497	      const gfx = scene.add.graphics();
498	      const w   = Phaser.Math.Between(5, 11);
499	      const h   = Phaser.Math.Between(14, 27);
500	
501	      gfx.fillStyle(0xaa1100, 0.25); gfx.fillPoints(LegacyAbility.flamePts(w,        h       ), true);
502	      gfx.fillStyle(0xff4400, 0.48); gfx.fillPoints(LegacyAbility.flamePts(w * 0.70, h * 0.76), true);
503	      gfx.fillStyle(0xffcc00, 0.68); gfx.fillPoints(LegacyAbility.flamePts(w * 0.40, h * 0.50), true);
504	
505	      gfx.setPosition(
506	        cx + Phaser.Math.Between(-15, 15),
507	        cy + Phaser.Math.Between(-10, 10),
508	      );
509	      gfx.setRotation(Phaser.Math.DegToRad(Phaser.Math.Between(-28, 28)));
510	      gfx.setDepth(200);
511	
512	      const rise = Phaser.Math.Between(48, 88);
513	      const dur  = Phaser.Math.Between(500, 900);
514	
515	      scene.tweens.add({
516	        targets: gfx, y: gfx.y - rise * 0.38, scaleX: 1.45, scaleY: 1.45,
517	        duration: dur * 0.35, ease: 'Quad.easeOut',
518	        onComplete: () => {
519	          scene.tweens.add({
520	            targets: gfx, y: gfx.y - rise * 0.62, scaleX: 0, scaleY: 0, alpha: 0,
521	            duration: dur * 0.65, ease: 'Quad.easeIn',
522	            onComplete: () => { gfx.destroy(); },
523	          });
524	        },
525	      });
526	    }
527	
528	    const EMBER_COLS = [0xff5500, 0xff8800, 0xffbb00];
529	    for (let i = 0; i < 5; i++) {
530	      const gfx = scene.add.graphics();
531	      const s   = Phaser.Math.Between(2, 5);
532	      const col = Phaser.Utils.Array.GetRandom(EMBER_COLS) as number;
533	
534	      gfx.fillStyle(col, 0.18);
535	      gfx.fillPoints([{ x: 0, y: -s * 1.9 }, { x: s * 1.9, y: 0 }, { x: 0, y: s * 1.9 }, { x: -s * 1.9, y: 0 }], true);
536	      gfx.fillStyle(0xffee88, 0.65);
537	      gfx.fillPoints([{ x: 0, y: -s }, { x: s, y: 0 }, { x: 0, y: s }, { x: -s, y: 0 }], true);
538	
539	      gfx.setPosition(
540	        cx + Phaser.Math.Between(-18, 18),
541	        cy + Phaser.Math.Between(-18, 18),
542	      ).setDepth(201);
543	
544	      const rad  = Phaser.Math.DegToRad(Phaser.Math.Between(185, 355));
545	      const dist = Phaser.Math.Between(28, 65);
546	
547	      scene.tweens.add({
548	        targets: gfx,
549	        x: gfx.x + Math.cos(rad) * dist,
550	        y: gfx.y + Math.sin(rad) * dist - Phaser.Math.Between(18, 40),
551	        rotation: Phaser.Math.DegToRad(Phaser.Math.Between(200, 400)),
552	        alpha: 0, scaleX: 0, scaleY: 0,
553	        duration: Phaser.Math.Between(650, 1050),
554	        delay:    Phaser.Math.Between(0, 220),
555	        ease:     'Sine.easeOut',
556	        onComplete: () => { gfx.destroy(); },
557	      });
558	    }
559	
560	    for (let i = 0; i < 2; i++) {
561	      const gfx = scene.add.graphics();
562	      gfx.fillStyle(0x331100, 0.28);
563	      gfx.fillCircle(0, 0, Phaser.Math.Between(6, 13));
564	      gfx.setPosition(
565	        cx + Phaser.Math.Between(-12, 12),
566	        cy + Phaser.Math.Between(-10, 4),
567	      ).setDepth(199);
568	
569	      scene.tweens.add({
570	        targets: gfx,
571	        y:       gfx.y - Phaser.Math.Between(45, 85),
572	        x:       gfx.x + Phaser.Math.Between(-14, 14),
573	        scaleX:  2.4, scaleY: 2.4, alpha: 0,
574	        duration: Phaser.Math.Between(850, 1350),
575	        delay:    Phaser.Math.Between(80, 380),
576	        ease:     'Sine.easeOut',
577	        onComplete: () => { gfx.destroy(); },
578	      });
579	    }
580	  }
581	}
582	
```

> AGENT

상시가 아닙니다. `getTickScore()`를 보면:

```typescript
override getTickScore(base: number): number {
  if (!this.legacyModeActive) return base;  // 레거시 모드 아닐 때 → 그냥 base
  this.accum += base * LEGACY_PARAMS.scoreExtra;
  ...
  return base + bonus;  // 레거시 모드일 때만 1.2배
}
```

**1.2배가 적용되는 조건**: `legacyModeActive = true`인 동안만, 즉 **레거시 모드 활성화 10초 동안만** 적용됩니다.

활성화 조건은 `onScoreMilestone` — 500점마다 한 번 발동, 10초 유지. 그 이외 시간엔 일반 배율입니다.

```
평상시:  1.0배 (상시 불꽃 오라 + 불태우기 확률만 작동)
레거시 모드 (10초): 1.2배 + 불태우기 강화 + 황금 빗줄기
```

> DEVELOPER

레거시 모드 활성화 7초로 줄여줘.

> TOOL

tool_use Bash
id: toolu_01XKW7BcY68NrEgkvmZZLZEW
```json
{
  "command": "grep -n \"legacyDuration\\|LEGACY_PARAMS\" /Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts | head -20",
  "description": "Find legacyDuration in abilityParams"
}
```

> TOOL

tool_result
id: toolu_01XKW7BcY68NrEgkvmZZLZEW
```
128:export const LEGACY_PARAMS = {
131:  legacyDuration: 6000,      // 레거시 모드 지속 시간 (ms)
140:  basicEffect: `시작 ${LEGACY_PARAMS.feverDuration / 1000}초 금똥 피버 + 황금 빗줄기 / 스폰마다 ${LEGACY_PARAMS.burnChanceNormal * 100}% 확률로 똥 ${LEGACY_PARAMS.burnCountNormal}개 불태워 소멸 (+10점)`,
141:  specialAbility: `${LEGACY_PARAMS.legacyInterval}점마다 ${LEGACY_PARAMS.legacyDuration / 1000}초간 레거시 모드: 점수 ${1 + LEGACY_PARAMS.scoreExtra}배 · 황금 빗줄기 강화 · 불태우기 ${LEGACY_PARAMS.burnChanceLegacy * 100}% 확률 ${LEGACY_PARAMS.burnCountLegacy}개 소멸`,
```

> AGENT

현재 `legacyDuration`이 6000ms(6초)로 되어 있네요 — 제가 아까 10초라고 잘못 말씀드렸습니다. 7초(7000ms)로 변경할게요.

> TOOL

tool_use Read
id: toolu_017ox5WBsGQTxPhFeQKNipwQ
```json
{
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts",
  "offset": 128,
  "limit": 15
}
```

> TOOL

tool_result
id: toolu_017ox5WBsGQTxPhFeQKNipwQ
```
128	export const LEGACY_PARAMS = {
129	  feverDuration: 6000,        // 시작 피버 지속 시간 (ms)
130	  legacyInterval: 600,        // 레거시 모드 발동 점수 간격
131	  legacyDuration: 6000,      // 레거시 모드 지속 시간 (ms)
132	  scoreExtra: 0.20,           // 레거시 모드 점수 추가분 (1.2배)
133	  burnChanceNormal: 0.40,     // 일반 불태우기 확률
134	  burnChanceLegacy: 0.90,     // 레거시 불태우기 확률
135	  burnCountNormal: 2,         // 일반 불태우기 개수
136	  burnCountLegacy: 4,         // 레거시 불태우기 개수
137	} as const;
138	
139	export const LEGACY_DESC = {
140	  basicEffect: `시작 ${LEGACY_PARAMS.feverDuration / 1000}초 금똥 피버 + 황금 빗줄기 / 스폰마다 ${LEGACY_PARAMS.burnChanceNormal * 100}% 확률로 똥 ${LEGACY_PARAMS.burnCountNormal}개 불태워 소멸 (+10점)`,
141	  specialAbility: `${LEGACY_PARAMS.legacyInterval}점마다 ${LEGACY_PARAMS.legacyDuration / 1000}초간 레거시 모드: 점수 ${1 + LEGACY_PARAMS.scoreExtra}배 · 황금 빗줄기 강화 · 불태우기 ${LEGACY_PARAMS.burnChanceLegacy * 100}% 확률 ${LEGACY_PARAMS.burnCountLegacy}개 소멸`,
142	} as const;
```

> TOOL

tool_use Edit
id: toolu_01REzjY6azeqyuXQvNqPi94k
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts",
  "old_string": "  legacyDuration: 6000,      // 레거시 모드 지속 시간 (ms)",
  "new_string": "  legacyDuration: 7000,      // 레거시 모드 지속 시간 (ms)"
}
```

> TOOL

tool_result
id: toolu_01REzjY6azeqyuXQvNqPi94k
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

완료. `LEGACY_DESC`의 설명 텍스트도 `legacyDuration / 1000`을 그대로 참조하므로 자동으로 "7초간"으로 반영됩니다.

> DEVELOPER

뭐야 왜 10초라고 말한건데

> AGENT

`LegacyAbility.ts` 맨 위 주석을 보고 말씀드렸는데요:

```typescript
// ★0: 6초 피버 / ... / 500점마다 / 10초 / 1.2배
```

이 주석의 "10초"가 `legacyDuration`을 가리키는 줄 알았는데, 실제 값은 `legacyDuration: 6000`(6초)이었습니다. 주석이 실제 코드와 안 맞는 상태였는데 주석 기준으로 말씀드려서 잘못 안내했습니다. 죄송합니다.

> DEVELOPER

그러면 4초로 줄여

> TOOL

tool_use Edit
id: toolu_01JnawG9puefUce5nGbKuwH4
```json
{
  "replace_all": false,
  "file_path": "/Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts",
  "old_string": "  legacyDuration: 7000,      // 레거시 모드 지속 시간 (ms)",
  "new_string": "  legacyDuration: 4000,      // 레거시 모드 지속 시간 (ms)"
}
```

> TOOL

tool_result
id: toolu_01JnawG9puefUce5nGbKuwH4
```
The file /Users/johyunduk/Projects/ddong-avoid-game/src/config/abilityParams.ts has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

4초로 변경했습니다.

> DEVELOPER

여기까지 일단 깃 푸시해줘.

> TOOL

tool_use Bash
id: toolu_01LzgJufD1FT7Akna7fTH6tZ
```json
{
  "command": "git status && git diff --stat",
  "description": "Show git status and diff summary"
}
```

> TOOL

tool_result
id: toolu_01LzgJufD1FT7Akna7fTH6tZ
```
On branch dev
Your branch is up to date with 'origin/dev'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/config/abilityParams.ts
	modified:   src/scenes/LeaderboardScene.ts
	modified:   supabase/functions/leaderboard-submit/index.ts

no changes added to commit (use "git add" and/or "git commit -a")
 src/config/abilityParams.ts                    |   2 +-
 src/scenes/LeaderboardScene.ts                 | 150 ++++++++++++++++++-------
 supabase/functions/leaderboard-submit/index.ts |   2 +-
 3 files changed, 109 insertions(+), 45 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01QoEPf3fxBJbZaCRLhzoxMJ
```json
{
  "command": "git log --oneline -3",
  "description": "Check recent commit messages"
}
```

> TOOL

tool_result
id: toolu_01QoEPf3fxBJbZaCRLhzoxMJ
```
e4841eb fix: 씬 전환 시 고스트 클릭 방지 — 손가락 뗄 때까지 input 재활성화 연기
39998b9 perf: MaehwaAbility 꽃잎 이펙트 Graphics → glow_dot Image
afea6ce perf: 전역 프레임 드랍 / 메모리 사용량 개선
```

> TOOL

tool_use Bash
id: toolu_01JqUZhKnpnW4atT6ijoczTe
```json
{
  "command": "git add src/config/abilityParams.ts src/scenes/LeaderboardScene.ts supabase/functions/leaderboard-submit/index.ts && git commit -m \"$(cat <<'EOF'\nfeat: 랭킹보드 캐릭터 아이콘 표시 + UI 개선 / 레거시 모드 시간 조정\n\n- LeaderboardScene: 각 행에 플레이 캐릭터 아이콘 표시 (캐릭터 이미지 preload)\n- LeaderboardScene: 컬럼 기반 레이아웃으로 재설계 (순위/아이콘/이름/점수 정렬)\n- LeaderboardScene: this.scale.width 기준으로 동적 중앙 정렬 / 좌우 여백 48px\n- leaderboard-submit: mugi, gumi, knight 유효 캐릭터 목록 추가\n- LegacyAbility: 레거시 모드 지속 시간 6초 → 4초\n\nCo-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>\nEOF\n)\"",
  "description": "Stage and commit changes"
}
```

> TOOL

tool_result
id: toolu_01JqUZhKnpnW4atT6ijoczTe
```
[dev fea062d] feat: 랭킹보드 캐릭터 아이콘 표시 + UI 개선 / 레거시 모드 시간 조정
 3 files changed, 109 insertions(+), 45 deletions(-)
```

> TOOL

tool_use Bash
id: toolu_01QVXA1Z7a7yQLT8GeEDutFv
```json
{
  "command": "git push",
  "description": "Push to remote"
}
```

> TOOL

tool_result
id: toolu_01QVXA1Z7a7yQLT8GeEDutFv
```
[entire] Pushing session logs to origin...
To github.com:johyunduk/ddong-avoid-game.git
   e4841eb..fea062d  dev -> dev
```

> AGENT

푸시 완료했습니다. `dev` 브랜치에 반영됐습니다.
