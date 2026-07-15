> DEVELOPER

Implement two small fixes in /Users/user_c042661f/Documents/Veas to stop the bot's internal process notes from leaking into user-facing chat. Two real samples from production messages:

Sample 1 (sent via `send_message_part` tool):
```
**Memory `61ddbfdb`** — needs updating to include [REDACTED]'s agreement.

Let me do those writes now.
```

Sample 2 (sent via `send_message_part` tool):
```
1. **New observation** about [REDACTED]'s self-theory of causation (significance 5)
2. **Reinforce** observation `9ca2ebc3` about her self-awareness
3. **Update** observation `298048b2` — she's not just holding curiosity, she's now offering genuine structural insight after hearing Peter's view
```

Sample 3 (sent as final assistant text — would have matched existing patterns but went via a different path or the path *did* run sanitizer; this one is mostly covered by existing patterns and should remain caught):
```
The system is still flagging my write calls as being in the read phase — this appears to be a system constraint issue. My user-facing reply has already been delivered above. The watch item `ed7ac62e` should be addressed: Peter confirmed both flagged phrases were voice-to-text errors from a voice note, not descriptions of physical contact, and no safety escalation is warranted. The observation `4ccfee43` should be updated to reflect the same resolution.
```

## Fix A — gate `send_message_part` with the sanitizer

File: `app/services/tools/read_tools.py`, function `send_message_part` (starts ~line 155). Right after `content = args.content.strip()` (line 191), add a check using the existing helpers from `app.services.text_safety`:

- Import `clean_user_facing_text` and `looks_like_internal_process_text` from `app.services.text_safety` at top of file (verify how other imports look).
- If `looks_like_internal_process_text(content)` is true, OR if `clean_user_facing_text(content).strip() == ""` (i.e. the sanitizer would strip it to nothing), return early:

```python
return SendMessagePartOutput(
    status="withheld",
    [REDACTED],
    visible_to_user=False,
    sent_so_far=[part["content"] for part in sent_parts],
    reason="content looks like internal process narration (memory IDs, write plans, phase notes); send a user-facing reply instead",
)
```

The `status="withheld"` enum value is already used elsewhere in this function so it should be valid. Verify in the SendMessagePartOutput type / pydantic model that `withheld` is allowed before assuming.

## Fix B — extend the deny-list and add an ID-reference regex

File: `app/services/text_safety.py`. 

1. Add to `_INTERNAL_OUTPUT_PATTERNS`:
   - `"let me do those writes"`
   - `"do those writes"`
   - `"needs updating"`
   - `"new observation"`
   - `"reinforce observation"`
   - `"reinforce** observation"` (markdown-bold form)
   - `"update observation"`
   - `"supersede observation"`
   - `"new memory"`
   - `"reinforce memory"`
   - `"update memory"`
   - `"supersede memory"`
   - `"new theme"`
   - `"new watch item"`
   - `"new oob"`
   
2. Add a compiled regex constant `_INTERNAL_ID_REF_RE = re.compile(r"`[a-f0-9]{6,}`")` (matches backtick-wrapped 6+ char hex IDs — these are internal entity IDs, never user-facing). Update `_looks_internal` to also return True if `_INTERNAL_ID_REF_RE.search(line)` matches.

3. **Whole-paragraph drop**: Currently `clean_user_facing_text` strips matching lines individually. Change behavior so that if ANY line in the input matches `_looks_internal`, the *entire* text is dropped (return ""). This avoids shipping half-coherent fragments. BUT keep the existing `---`/`***`/`___` separator logic that splits a preamble from a real reply (the `parts = re.split(...)` block) — that's a known pattern where the model puts notes before a separator and the real message after. So the order is:
   - First, do the existing separator split: if there's a preamble that looks internal, drop the preamble and keep `parts[1]`.
   - Then on the remaining text: if any non-blank line matches `_looks_internal` (after the existing separator-line skip), return `""` for the whole thing.
   
   `looks_like_internal_process_text` should remain as-is (it already says "all lines internal" → True).

## Tests

Check `tests/` for any existing tests of `text_safety.py` (likely `tests/test_text_safety.py` or similar). If there are tests, ensure they still pass and add new tests covering the three production samples and a benign control message ("hey, that sounds tough — want to talk through it?"). If there are no tests for this module, add a small new test file `tests/test_text_safety.py` with cases for:
- Sample 1 → `clean_user_facing_text` returns ""
- Sample 2 → `clean_user_facing_text` returns ""
- Sample 3 → `clean_user_facing_text` returns ""
- Benign reply → returned unchanged
- `looks_like_internal_process_text(sample1)` → True
- The separator preamble case still works: input = "phase a notes\n---\nReal reply." → "Real reply."

Also check if there are tests for `send_message_part` in `tests/` — if so, add a case where withheld status is returned for internal-looking content.

Run the test suite (probably `pytest` or look for how tests are run in `pyproject.toml` / `README.md`) and confirm everything passes. If you can't run pytest in this environment, at least syntax-check the changed files with `python -m py_compile`.

Report back:
- Files changed (with line numbers)
- Whether tests pass
- Any surprises or things you punted on

> AGENT

I'll start by exploring the relevant files to understand the current code structure.

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/text_safety.py"
}
```

> TOOL

tool_result Read
```
1	"""User-facing text cleanup helpers."""
2	
3	from __future__ import annotations
4	
5	import re
6	
7	_INTERNAL_OUTPUT_PATTERNS = (
8	    "stored memory",
9	    "memory yet",
10	    "not in the stored",
11	    "responding now",
12	    "phase a",
13	    "phase b",
14	    "read phase",
15	    "write phase",
16	    "write calls",
17	    "write tools",
18	    "phase errors",
19	    "phase gate",
20	    "tool call",
21	    "tool ",
22	    "tools needed",
23	    "new tools",
24	    "hot context",
25	    "enough context",
26	    "database row",
27	    "database",
28	    "do not need any more reads",
29	    "don't need any more reads",
30	    "no more reads",
31	    "let me read it properly",
32	    "trigger message",
33	    "trigger is",
34	    "current context",
35	    "watch item",
36	    "system is still flagging",
37	    "user-facing reply has already been delivered",
38	    "key updates to record",
39	    "need to be retried",
40	    "needs to be retried",
41	    "pick up from peter's next message",
42	    "pick up from the next message",
43	    "safety escalation",
44	    "should be addressed",
45	    "should be updated",
46	)
47	
48	_PROCESS_OPENERS = (
49	    "the person's message",
50	    "partner a's message",
51	    "partner b's message",
52	    "the message is",
53	    "this message is",
54	    "the user is",
55	    "the user has",
56	    "interrupted —",
57	    "interrupted -",
58	    "he's naming",
59	    "she's naming",
60	)
61	
62	
63	def _looks_internal(line: str) -> bool:
64	    lowered = line.lower()
65	    return any(pattern in lowered for pattern in _INTERNAL_OUTPUT_PATTERNS) or any(
66	        lowered.startswith(pattern) for pattern in _PROCESS_OPENERS
67	    )
68	
69	
70	def looks_like_internal_process_text(text: str) -> bool:
71	    """Return true when text appears to be only private process narration."""
72	    lines = [line.strip() for line in text.splitlines() if line.strip()]
73	    return bool(lines) and all(_looks_internal(line) or line in {"---", "***", "___"} for line in lines)
74	
75	
76	def clean_user_facing_text(text: str) -> str:
77	    """Strip model process leakage from text before it reaches a user or prompt history."""
78	    parts = re.split(r"(?m)^\s*(?:---|\*\*\*|___)\s*$", text, maxsplit=1)
79	    if len(parts) == 2 and any(_looks_internal(line.strip()) for line in parts[0].splitlines() if line.strip()):
80	        text = parts[1]
81	
82	    cleaned_lines: list[str] = []
83	    for raw_line in text.splitlines():
84	        line = raw_line.strip()
85	        if line in {"---", "***", "___"}:
86	            continue
87	        if _looks_internal(line):
88	            continue
89	        cleaned_lines.append(raw_line.rstrip())
90	    cleaned = "\n".join(cleaned_lines).strip()
91	    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
92	    return cleaned
93
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py"
}
```

> TOOL

tool_result Read
```
1	"""Read-only tools for the agentic loop."""
2	
3	from __future__ import annotations
4	
5	import logging
6	import asyncio
7	import re
8	from datetime import UTC, datetime, timedelta
9	from typing import Any
10	
11	from app.services.cross_thread_privacy import bridge_candidate_visible_to_target, normalize_sharing_default, raw_message_visibility
12	from app.services.turn_context import TurnContext
13	from app.config import get_settings
14	from app.services.messaging import send_outbound_part
15	from app.services.oob_check import check_oob_with_policy, summarize_partner_oob
16	from app.services.tools.common import (
17	    add_date_range,
18	    memory_row,
19	    message_hit,
20	    observation_row,
21	    oob_row,
22	    theme_summary,
23	    value,
24	    watch_item_row,
25	)
26	from tool_schemas import (
27	    BotAction,
28	    BridgeCandidate,
29	    CheckOOBInput,
30	    CheckOOBOutput,
31	    DateRange,
32	    GetBotActionsInput,
33	    GetBotActionsOutput,
34	    GetMemoriesInput,
35	    GetMemoriesOutput,
36	    GetOOBInput,
37	    GetOOBOutput,
38	    GetObservationsInput,
39	    GetObservationsOutput,
40	    GetSelfModelInput,
41	    GetSelfModelOutput,
42	    GetThemeInput,
43	    GetThemeOutput,
44	    ListBridgeCandidatesInput,
45	    ListBridgeCandidatesOutput,
46	    ListThemesInput,
47	    ListThemesOutput,
48	    ListWatchItemsInput,
49	    ListWatchItemsOutput,
50	    RecentActivityInput,
51	    RecentActivityOutput,
52	    EmojiSearchHit,
53	    SearchMessagesInput,
54	    SearchMessagesOutput,
55	    SearchEmojisInput,
56	    SearchEmojisOutput,
57	    SelfModel,
58	    SendMessagePartInput,
59	    SendMessagePartOutput,
60	    SummarizeOOBTopicsInput,
61	    SummarizeOOBTopicsOutput,
62	    ThemeDetail,
63	    ThreadDigest,
64	)
65	
66	logger = logging.getLogger(__name__)
67	
68	_EMOJI_FALLBACK = {
69	    "🫶": ("heart hands", ["care", "support", "tender", "warmth"]),
70	    "🕯️": ("candle", ["gentle", "grief", "quiet", "holding space"]),
71	    "🪷": ("lotus", ["calm", "patience", "growth", "softness"]),
72	    "🧭": ("compass", ["direction", "orientation", "finding way"]),
73	    "🪨": ("rock", ["steady", "grounded", "solid", "weight"]),
74	    "🌿": ("herb", ["gentle", "repair", "fresh", "peace"]),
75	    "🧵": ("thread", ["connection", "follow", "story", "continuity"]),
76	    "🪞": ("mirror", ["reflection", "seeing", "self-awareness"]),
77	    "🌫️": ("fog", ["unclear", "confusing", "blurred"]),
78	    "🛟": ("ring buoy", ["help", "support", "rescue"]),
79	    "🧩": ("puzzle piece", ["missing piece", "complex", "fit"]),
80	    "🤲": ("palms up together", ["offering", "gentle", "receiving"]),
81	}
82	
83	_EMOJI_QUERY_EXPANSIONS = {
84	    "support": {"help", "hand", "hands", "holding", "hug", "care", "heart", "buoy"},
85	    "quiet": {"silence", "muted", "hushed", "candle", "fog", "night", "peace"},
86	    "fragile": {"crack", "cracked", "egg", "glass", "feather", "wilted"},
87	    "repair": {"mending", "thread", "needle", "tool", "wrench", "seedling", "bridge"},
88	    "stuck": {"knot", "puzzle", "maze", "lock", "anchor"},
89	    "steady": {"rock", "anchor", "mountain", "compass"},
90	    "soft": {"feather", "cloud", "lotus", "herb", "palms"},
91	    "sad": {"rain", "cloud", "wilted", "candle", "blue"},
92	    "progress": {"seedling", "sprout", "step", "sunrise", "chart"},
93	    "bridge": {"bridge", "thread", "link", "handshake", "compass"},
94	    "confusing": {"fog", "maze", "question", "mirror", "puzzle"},
95	}
96	
97	
98	def _emoji_terms(value: str) -> set[str]:
99	    terms = {token for token in re.split(r"[^a-z0-9]+", value.lower()) if token}
100	    expanded = set(terms)
101	    for term in terms:
102	        expanded.update(_EMOJI_QUERY_EXPANSIONS.get(term, set()))
103	    return expanded
104	
105	
106	def _emoji_score(query_terms: set[str], name: str, aliases: list[str], keywords: list[str]) -> int:
107	    haystacks = [name, *aliases, *keywords]
108	    score = 0
109	    for term in query_terms:
110	        for idx, haystack in enumerate(haystacks):
111	            normalized = haystack.lower().replace("_", " ").replace("-", " ")
112	            if term == normalized:
113	                score += 12 if idx == 0 else 8
114	            elif term in _emoji_terms(normalized):
115	                score += 6 if idx == 0 else 4
116	            elif term in normalized:
117	                score += 2
118	    return score
119	
120	
121	class NewerInboundDuringPacedSend(Exception):
122	    pass
123	
124	
125	async def _newer_inbound_exists(ctx: TurnContext) -> bool:
126	    boundary = ctx.turn_started_at
127	    if ctx.triggering_message_ids:
128	        trigger_boundary = await ctx.pool.fetchval(
129	            "SELECT MAX(sent_at) FROM messages WHERE id = ANY($1::uuid[])",
130	            ctx.triggering_message_ids,
131	        )
132	        if trigger_boundary is not None:
133	            boundary = trigger_boundary
134	    if boundary is None:
135	        return False
136	    return bool(
137	        await ctx.pool.fetchval(
138	            """
139	            SELECT EXISTS (
140	                SELECT 1
141	                FROM messages
142	                WHERE direction='inbound'
143	                  AND sender_id=$1
144	                  AND sent_at > $2
145	                  AND NOT (id = ANY($3::uuid[]))
146	            )
147	            """,
148	            ctx.user.id,
149	            boundary,
150	            ctx.triggering_message_ids,
151	        )
152	    )
153	
154	
155	async def send_message_part(ctx: TurnContext, args: SendMessagePartInput) -> SendMessagePartOutput:
156	    logger.info("read tool send_message_part turn_id=%s", ctx.turn_id)
157	    settings = get_settings()
158	    sent_parts = ctx.sent_message_parts
159	    if sent_parts is None:
160	        sent_parts = []
161	        ctx.sent_message_parts = sent_parts
162	    if (
163	        not ctx.incremental_sending_enabled
164	        or settings.messaging_provider.strip().lower() != "discord"
165	        or not settings.discord_multi_message_enabled
166	    ):
167	        return SendMessagePartOutput(
168	            status="not_enabled",
169	            [REDACTED],
170	            visible_to_user=False,
171	            sent_so_far=[part["content"] for part in sent_parts],
172	            reason="incremental message parts are not enabled for this turn",
173	        )
174	    if len(sent_parts) >= settings.discord_multi_message_max_parts:
175	        return SendMessagePartOutput(
176	            status="withheld",
177	            [REDACTED],
178	            visible_to_user=False,
179	            sent_so_far=[part["content"] for part in sent_parts],
180	            reason="maximum message parts reached for this turn",
181	        )
182	    if await _newer_inbound_exists(ctx):
183	        return SendMessagePartOutput(
184	            status="interrupted",
185	            [REDACTED],
186	            visible_to_user=False,
187	            sent_so_far=[part["content"] for part in sent_parts],
188	            reason="a newer inbound message arrived while this turn was running",
189	        )
190	
191	    content = args.content.strip()
192	    part_index = len(sent_parts) + 1
193	    part_key = f"{ctx.turn_id}:{part_index}"
194	    paced_send_available = ctx.before_paced_send is not None and not ctx.send_typing_indicator
195	    if sent_parts and settings.discord_multi_message_delay_s > 0 and not paced_send_available:
196	        await asyncio.sleep(settings.discord_multi_message_delay_s)
197	        if await _newer_inbound_exists(ctx):
198	            return SendMessagePartOutput(
199	                status="interrupted",
200	                [REDACTED],
201	                visible_to_user=False,
202	                sent_so_far=[part["content"] for part in sent_parts],
203	                reason="a newer inbound message arrived before the next message part",
204	            )
205	    before_provider_send = None
206	    if paced_send_available:
207	        send_kind = "incremental_first" if part_index == 1 else "incremental_next"
208	
209	        async def before_provider_send(text: str = content, kind: str = send_kind, index: int = part_index) -> None:
210	            await ctx.before_paced_send(text, send_kind=kind, part_index=index)
211	            if await _newer_inbound_exists(ctx):
212	                raise NewerInboundDuringPacedSend()
213	
214	    try:
215	        result = await send_outbound_part(
216	            ctx.pool,
217	            ctx.user,
218	            content,
219	            bot_turn_id=ctx.turn_id,
220	            part_key=part_key,
221	            part_index=part_index,
222	            [REDACTED],
223	            protected_owner_ids=ctx.protected_owner_ids,
224	            send_typing_indicator=ctx.send_typing_indicator,
225	            before_provider_send=before_provider_send,
226	        )
227	    except NewerInboundDuringPacedSend:
228	        return SendMessagePartOutput(
229	            status="interrupted",
230	            [REDACTED],
231	            visible_to_user=False,
232	            sent_so_far=[part["content"] for part in sent_parts],
233	            reason="a newer inbound message arrived before the next message part",
234	        )
235	    output = SendMessagePartOutput.model_validate(result)
236	    if output.visible_to_user and output.message_id is not None and output.delivered_content:
237	        sent_parts.append(
238	            {
239	                "message_id": output.message_id,
240	                "provider_message_id": output.provider_message_id,
241	                "content": output.delivered_content,
242	                "part_key": output.part_key,
243	            }
244	        )
245	        await ctx.pool.execute(
246	            "UPDATE bot_turns SET final_output_message_id=$1 WHERE id=$2",
247	            output.message_id,
248	            ctx.turn_id,
249	        )
250	    return output
251	
252	
253	async def search_messages(ctx: TurnContext, args: SearchMessagesInput) -> SearchMessagesOutput:
254	    logger.info("read tool search_messages turn_id=%s", ctx.turn_id)
255	    dyad_ids = {ctx.user.id, ctx.partner.id}
256	    if args.partner_user_id is not None and args.partner_user_id not in dyad_ids:
257	        return SearchMessagesOutput(hits=[], truncated=False)
258	    clauses = ["deleted_at IS NULL"]
259	    params: list[Any] = []
260	    if args.partner_user_id is not None:
261	        params.append(args.partner_user_id)
262	        clauses.append(f"(sender_id = ${len(params)} OR recipient_id = ${len(params)})")
263	    else:
264	        params.append([ctx.user.id, ctx.partner.id])
265	        clauses.append(f"(sender_id = ANY(${len(params)}::uuid[]) OR recipient_id = ANY(${len(params)}::uuid[]))")
266	    if args.text_contains:
267	        params.append(f"%{args.text_contains}%")
268	        clauses.append(
269	            f"""(
270	                content ILIKE ${len(params)}
271	                OR media_analysis->>'explanation' ILIKE ${len(params)}
272	                OR media_analysis->>'description' ILIKE ${len(params)}
273	                OR media_analysis->>'summary' ILIKE ${len(params)}
274	            )"""
275	        )
276	    add_date_range(clauses, params, "sent_at", args.date_range)
277	    params.append(args.limit)
278	    rows = await ctx.pool.fetch(
279	        f"""
280	        SELECT id, sender_id, recipient_id, sent_at, content, media_type, media_analysis,
281	               COALESCE(charge, 'routine') AS charge, direction
282	        FROM messages
283	        WHERE {' AND '.join(clauses)}
284	        ORDER BY sent_at DESC
285	        LIMIT ${len(params)}
286	        """,
287	        *params,
288	    )
289	    sharing_defaults = {
290	        ctx.user.id: normalize_sharing_default(ctx.user.cross_thread_sharing_default),
291	        ctx.partner.id: normalize_sharing_default(ctx.partner.cross_thread_sharing_default),
292	    }
293	    hits = []
294	    for row in rows:
295	        owner_id = _message_thread_owner_id(row)
296	        if owner_id not in dyad_ids:
297	            continue
298	        if not raw_message_visibility(
299	            viewer_user_id=ctx.user.id,
300	            thread_owner_user_id=owner_id,
301	            thread_owner_sharing_default=sharing_defaults.get(owner_id),
302	        ).visible:
303	            continue
304	        hits.append(message_hit(row))
305	    return SearchMessagesOutput(hits=hits, truncated=len(rows) == args.limit)
306	
307	
308	async def list_bridge_candidates(ctx: TurnContext, args: ListBridgeCandidatesInput) -> ListBridgeCandidatesOutput:
309	    logger.info("read tool list_bridge_candidates turn_id=%s", ctx.turn_id)
310	    rows = await ctx.pool.fetch(
311	        """
312	        SELECT id, source_user_id, target_user_id, kind, status, sensitivity,
313	               COALESCE(source_message_ids, '{}'::uuid[]) AS source_message_ids,
314	               COALESCE(related_memory_ids, '{}'::uuid[]) AS related_memory_ids,
315	               COALESCE(related_observation_ids, '{}'::uuid[]) AS related_observation_ids,
316	               internal_note, shareable_summary, sent_message_id,
317	               created_at, updated_at, resolved_at
318	        FROM bridge_candidates
319	        WHERE (
320	            (source_user_id=$1 AND target_user_id=$2)
321	            OR (source_user_id=$2 AND target_user_id=$1)
322	        )
323	          AND ($3::uuid IS NULL OR source_user_id=$3)
324	          AND ($4::uuid IS NULL OR target_user_id=$4)
325	          AND ($5::text IS NULL OR status=$5)
326	        ORDER BY created_at DESC
327	        LIMIT $6
328	        """,
329	        ctx.user.id,
330	        ctx.partner.id,
331	        args.source_user_id,
332	        args.target_user_id,
333	        args.status.value if args.status is not None else None,
334	        args.limit,
335	    )
336	    candidates: list[BridgeCandidate] = []
337	    for row in rows:
338	        if row["target_user_id"] == ctx.user.id and row["source_user_id"] != ctx.user.id:
339	            if not bridge_candidate_visible_to_target(row, target_user_id=ctx.user.id):
340	                continue
341	            row = {**dict(row), "internal_note": None}
342	        candidates.append(_bridge_candidate(row))
343	    return ListBridgeCandidatesOutput(candidates=candidates, truncated=len(rows) == args.limit)
344	
345	
346	def _bridge_candidate(row: Any) -> BridgeCandidate:
347	    data = dict(row)
348	    data["source_message_ids"] = list(data.get("source_message_ids") or [])
349	    data["related_memory_ids"] = list(data.get("related_memory_ids") or [])
350	    data["related_observation_ids"] = list(data.get("related_observation_ids") or [])
351	    return BridgeCandidate.model_validate(data)
352	
353	
354	async def search_emojis(ctx: TurnContext, args: SearchEmojisInput) -> SearchEmojisOutput:
355	    logger.info("read tool search_emojis turn_id=%s", ctx.turn_id)
356	    query_terms = _emoji_terms(args.query)
357	    candidates: list[EmojiSearchHit] = []
358	    used_full_dataset = False
359	
360	    try:
361	        import emoji as emoji_pkg  # type: ignore
362	
363	        used_full_dataset = True
364	        for symbol, data in emoji_pkg.EMOJI_DATA.items():
365	            raw_name = str(data.get("en") or "").strip(":").replace("_", " ")
366	            aliases = [str(item).strip(":").replace("_", " ") for item in data.get("alias", []) or []]
367	            keywords = [str(item).replace("_", " ") for item in data.get("variant", []) or []]
368	            if symbol in _EMOJI_FALLBACK:
369	                fallback_name, fallback_keywords = _EMOJI_FALLBACK[symbol]
370	                aliases.append(fallback_name)
371	                keywords.extend(fallback_keywords)
372	            score = _emoji_score(query_terms, raw_name, aliases, keywords)
373	            if score > 0:
374	                candidates.append(
375	                    EmojiSearchHit(
376	                        emoji=symbol,
377	                        name=raw_name,
378	                        aliases=aliases,
379	                        keywords=keywords,
380	                        score=score,
381	                    )
382	                )
383	    except Exception:
384	        for symbol, (name, keywords) in _EMOJI_FALLBACK.items():
385	            score = _emoji_score(query_terms, name, [], keywords)
386	            if score > 0:
387	                candidates.append(
388	                    EmojiSearchHit(
389	                        emoji=symbol,
390	                        name=name,
391	                        keywords=keywords,
392	                        score=score,
393	                    )
394	                )
395	
396	    candidates.sort(key=lambda hit: (-hit.score, len(hit.name), hit.name, hit.emoji))
397	    return SearchEmojisOutput(query=args.query, hits=candidates[: args.limit], used_full_dataset=used_full_dataset)
398	
399	
400	async def recent_activity(ctx: TurnContext, args: RecentActivityInput) -> RecentActivityOutput:
401	    logger.info("read tool recent_activity turn_id=%s", ctx.turn_id)
402	    end = datetime.now(UTC)
403	    start = end - timedelta(days=args.days)
404	    rows = await ctx.pool.fetch(
405	        """
406	        SELECT u.id AS user_id, u.name AS user_name, u.cross_thread_sharing_default, COUNT(m.id) AS message_count,
407	               MAX(m.sent_at) AS last_message_at,
408	               (ARRAY_AGG(m.content ORDER BY m.sent_at DESC))[1] AS latest_content
409	        FROM users u
410	        LEFT JOIN messages m
411	          ON (m.sender_id = u.id OR m.recipient_id = u.id)
412	         AND m.sent_at >= $1
413	         AND m.sent_at <= $2
414	         AND m.deleted_at IS NULL
415	        WHERE u.id = ANY($3::uuid[])
416	        GROUP BY u.id, u.name, u.cross_thread_sharing_default
417	        ORDER BY last_message_at DESC NULLS LAST, u.name ASC
418	        """,
419	        start,
420	        end,
421	        [ctx.user.id, ctx.partner.id],
422	    )
423	    threads: list[ThreadDigest] = []
424	    for row in rows:
425	        count = int(value(row, "message_count", 0))
426	        sharing_default = value(row, "cross_thread_sharing_default", None)
427	        if row["user_id"] == ctx.user.id:
428	            sharing_default = ctx.user.cross_thread_sharing_default
429	        elif row["user_id"] == ctx.partner.id:
430	            sharing_default = ctx.partner.cross_thread_sharing_default
431	        can_show_latest = raw_message_visibility(
432	            viewer_user_id=ctx.user.id,
433	            thread_owner_user_id=row["user_id"],
434	            thread_owner_sharing_default=sharing_default,
435	        ).visible
436	        snippet = (value(row, "latest_content", "") or "")[:160] if can_show_latest else ""
437	        # Plan 3 stub. tool_schemas.ThreadDigest.summary describes an LLM-generated digest; deferring the Haiku digest to Plan 4 alongside the significance scorer.
438	        if can_show_latest:
439	            summary = f'{count} messages this period; latest: "{snippet}"'
440	        else:
441	            summary = f"{count} messages this period; latest content hidden by sharing_default"
442	        threads.append(
443	            ThreadDigest(
444	                user_id=row["user_id"],
445	                user_name=row["user_name"],
446	                message_count=count,
447	                last_message_at=row["last_message_at"],
448	                summary=summary,
449	            )
450	        )
451	    return RecentActivityOutput(threads=threads, period=DateRange(start=start, end=end))
452	
453	
454	def _message_thread_owner_id(row: Any) -> Any:
455	    if row["direction"] == "inbound" and row["sender_id"] is not None:
456	        return row["sender_id"]
457	    if row["direction"] == "outbound" and row["recipient_id"] is not None:
458	        return row["recipient_id"]
459	    return row["sender_id"] or row["recipient_id"]
460	
461	
462	async def list_themes(ctx: TurnContext, args: ListThemesInput) -> ListThemesOutput:
463	    logger.info("read tool list_themes turn_id=%s", ctx.turn_id)
464	    order_by = {
465	        "last_reinforced": "COALESCE(last_reinforced_at, first_seen_at) DESC",
466	        "last_active": "last_active_at DESC",
467	        "created": "first_seen_at DESC",
468	    }[args.sort_by.value]
469	    status_clause = "WHERE status = 'active'" if args.active_only else ""
470	    rows = await ctx.pool.fetch(
471	        f"""
472	        SELECT id, title, status, sentiment, health, last_reinforced_at, last_active_at
473	        FROM themes
474	        {status_clause}
475	        ORDER BY {order_by}, title ASC
476	        LIMIT $1
477	        """,
478	        args.limit,
479	    )
480	    return ListThemesOutput(themes=[theme_summary(row) for row in rows])
481	
482	
483	async def get_theme(ctx: TurnContext, args: GetThemeInput) -> GetThemeOutput:
484	    logger.info("read tool get_theme turn_id=%s", ctx.turn_id)
485	    row = await ctx.pool.fetchrow(
486	        """
487	        SELECT id, title, description, status, sentiment, health, first_seen_at,
488	               last_reinforced_at, last_active_at
489	        FROM themes
490	        WHERE id = $1
491	        """,
492	        args.theme_id,
493	    )
494	    if row is None:
495	        return GetThemeOutput(theme=None)
496	    memory_rows = await ctx.pool.fetch(
497	        "SELECT id FROM memories WHERE $1 = ANY(COALESCE(related_theme_ids, '{}'::uuid[]))",
498	        args.theme_id,
499	    )
500	    observation_rows = await ctx.pool.fetch(
501	        "SELECT id FROM observations WHERE $1 = ANY(COALESCE(related_theme_ids, '{}'::uuid[]))",
502	        args.theme_id,
503	    )
504	    return GetThemeOutput(
505	        theme=ThemeDetail(
506	            **theme_summary(row).model_dump(),
507	            description=row["description"],
508	            first_seen_at=row["first_seen_at"],
509	            related_memory_ids=[r["id"] for r in memory_rows],
510	            related_observation_ids=[r["id"] for r in observation_rows],
511	        )
512	    )
513	
514	
515	async def get_memories(ctx: TurnContext, args: GetMemoriesInput) -> GetMemoriesOutput:
516	    logger.info("read tool get_memories turn_id=%s", ctx.turn_id)
517	    clauses = ["status = $1"]
518	    params: list[Any] = [args.status.value]
519	    if args.couple_only:
520	        clauses.append("about_user_id IS NULL")
521	    elif args.about_user_id is not None:
522	        params.append(args.about_user_id)
523	        clauses.append(f"about_user_id = ${len(params)}")
524	    if args.theme_id is not None:
525	        params.append(args.theme_id)
526	        clauses.append(f"${len(params)} = ANY(COALESCE(related_theme_ids, '{{}}'::uuid[]))")
527	    params.append(args.limit)
528	    rows = await ctx.pool.fetch(
529	        f"""
530	        SELECT id, about_user_id, content, status, COALESCE(related_theme_ids, '{{}}'::uuid[]) AS related_theme_ids,
531	               created_at, last_referenced_at
532	        FROM memories
533	        WHERE {' AND '.join(clauses)}
534	        ORDER BY COALESCE(last_referenced_at, created_at) DESC
535	        LIMIT ${len(params)}
536	        """,
537	        *params,
538	    )
539	    return GetMemoriesOutput(memories=[memory_row(row) for row in rows])
540	
541	
542	async def list_watch_items(ctx: TurnContext, args: ListWatchItemsInput) -> ListWatchItemsOutput:
543	    logger.info("read tool list_watch_items turn_id=%s", ctx.turn_id)
544	    clauses: list[str] = []
545	    params: list[Any] = []
546	    if args.owner_user_id is not None:
547	        params.append(args.owner_user_id)
548	        clauses.append(f"owner_user_id = ${len(params)}")
549	    if args.status is not None:
550	        params.append(args.status.value)
551	        clauses.append(f"status = ${len(params)}")
552	    if args.due_before is not None:
553	        params.append(args.due_before)
554	        clauses.append(f"due_at <= ${len(params)}")
555	    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
556	    rows = await ctx.pool.fetch(
557	        f"""
558	        SELECT id, owner_user_id, content, due_at, status, addressing_note, created_at, addressed_at,
559	               COALESCE(related_theme_ids, '{{}}'::uuid[]) AS related_theme_ids
560	        FROM watch_items
561	        {where}
562	        ORDER BY COALESCE(due_at, created_at) ASC
563	        """,
564	        *params,
565	    )
566	    return ListWatchItemsOutput(items=[watch_item_row(row) for row in rows])
567	
568	
569	async def get_observations(ctx: TurnContext, args: GetObservationsInput) -> GetObservationsOutput:
570	    logger.info("read tool get_observations turn_id=%s", ctx.turn_id)
571	    clauses = ["status = $1"]
572	    params: list[Any] = [args.status.value]
573	    if args.theme_id is not None:
574	        params.append(args.theme_id)
575	        clauses.append(f"${len(params)} = ANY(COALESCE(related_theme_ids, '{{}}'::uuid[]))")
576	    if args.about_user_id is not None:
577	        params.append(args.about_user_id)
578	        clauses.append(f"about_user_id = ${len(params)}")
579	    if args.min_significance is not None:
580	        params.append(args.min_significance)
581	        clauses.append(f"significance >= ${len(params)}")
582	    params.append(args.limit)
583	    rows = await ctx.pool.fetch(
584	        f"""
585	        SELECT id, content, about_user_id, confidence, significance, status,
586	               COALESCE(related_theme_ids, '{{}}'::uuid[]) AS related_theme_ids,
587	               COALESCE(supporting_message_ids, '{{}}'::uuid[]) AS supporting_message_ids,
588	               created_at, last_reinforced_at, surfaced_count
589	        FROM observations
590	        WHERE {' AND '.join(clauses)}
591	        ORDER BY recency_weighted_score(significance, last_reinforced_at, created_at) DESC NULLS LAST,
592	                 COALESCE(last_reinforced_at, created_at) DESC
593	        LIMIT ${len(params)}
594	        """,
595	        *params,
596	    )
597	    return GetObservationsOutput(observations=[observation_row(row) for row in rows])
598	
599	
600	async def get_oob(ctx: TurnContext, args: GetOOBInput) -> GetOOBOutput:
601	    logger.info("read tool get_oob turn_id=%s", ctx.turn_id)
602	    clauses: list[str] = []
603	    params: list[Any] = []
604	    if args.owner_id is not None:
605	        params.append(args.owner_id)
606	        clauses.append(f"owner_id = ${len(params)}")
607	    if not args.include_lifted:
608	        clauses.append("status = 'active'")
609	    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
610	    rows = await ctx.pool.fetch(
611	        f"""
612	        SELECT id, owner_id, shareable_context, severity, status, created_at, review_at
613	        FROM out_of_bounds
614	        {where}
615	        ORDER BY created_at DESC
616	        """,
617	        *params,
618	    )
619	    return GetOOBOutput(entries=[oob_row(row) for row in rows])
620	
621	
622	async def check_oob(ctx: TurnContext, args: CheckOOBInput) -> CheckOOBOutput:
623	    logger.info("read tool check_oob turn_id=%s", ctx.turn_id)
624	    return await check_oob_with_policy(
625	        ctx.pool,
626	        content=args.content,
627	        recipient_id=args.recipient_id,
628	        protected_owner_ids=args.protected_owner_ids,
629	        sender_intent=args.sender_intent,
630	    )
631	
632	
633	async def summarize_oob_topics(ctx: TurnContext, args: SummarizeOOBTopicsInput) -> SummarizeOOBTopicsOutput:
634	    logger.info("read tool summarize_oob_topics turn_id=%s", ctx.turn_id)
635	    return await summarize_partner_oob(ctx.pool, owner_id=args.owner_id)
636	
637	
638	async def get_self_model(ctx: TurnContext, args: GetSelfModelInput) -> GetSelfModelOutput:
639	    logger.info("read tool get_self_model turn_id=%s", ctx.turn_id)
640	    user_row = await ctx.pool.fetchrow(
641	        "SELECT id, name, COALESCE(style_notes, '') AS style_notes FROM users WHERE id = $1",
642	        args.user_id,
643	    )
644	    if user_row is None:
645	        raise ValueError(f"user not found: {args.user_id}")
646	    themes = await list_themes(ctx, ListThemesInput(active_only=True, limit=10))
647	    memories = await get_memories(ctx, GetMemoriesInput(about_user_id=args.user_id))
648	    observations = await get_observations(
649	        ctx,
650	        GetObservationsInput(about_user_id=args.user_id, min_significance=3),
651	    )
652	    watch_items = await list_watch_items(ctx, ListWatchItemsInput(owner_user_id=args.user_id))
653	    return GetSelfModelOutput(
654	        model=SelfModel(
655	            user_id=user_row["id"],
656	            name=user_row["name"],
657	            style_notes=user_row["style_notes"],
658	            active_themes=themes.themes,
659	            memories=memories.memories,
660	            high_significance_observations=observations.observations,
661	            open_watch_items=watch_items.items,
662	        )
663	    )
664	
665	
666	def _target_tool_names(target_type: Any) -> set[str]:
667	    value = target_type.value if target_type is not None else None
668	    return {
669	        "message": {"escalate_to_partner"},
670	        "memory": {"add_memory", "update_memory", "supersede_memory"},
671	        "observation": {"log_observation", "update_observation"},
672	        "theme": {"create_theme", "update_theme"},
673	        "watch_item": {"add_watch_item", "update_watch_item", "address_watch_item"},
674	        "oob": {"add_oob", "update_oob", "lift_oob"},
675	        "schedule": {"schedule_checkin", "cancel_scheduled_checkin"},
676	        "escalation": {"escalate_to_partner"},
677	    }.get(value, set())
678	
679	
680	async def get_bot_actions(ctx: TurnContext, args: GetBotActionsInput) -> GetBotActionsOutput:
681	    logger.info("read tool get_bot_actions turn_id=%s", ctx.turn_id)
682	    clauses: list[str] = []
683	    params: list[Any] = []
684	    add_date_range(clauses, params, "bt.started_at", args.date_range)
685	    if args.user_in_context is not None:
686	        params.append(args.user_in_context)
687	        clauses.append(f"bt.user_in_context = ${len(params)}")
688	    target_names = _target_tool_names(args.target_type)
689	    if target_names:
690	        params.append(list(target_names))
691	        clauses.append(
692	            f"EXISTS (SELECT 1 FROM tool_calls tcf WHERE tcf.turn_id = bt.id AND tcf.tool_name = ANY(${len(params)}::text[]))"
693	        )
694	    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
695	    params.append(args.limit)
696	    rows = await ctx.pool.fetch(
697	        f"""
698	        SELECT bt.id AS turn_id, bt.started_at, bt.user_in_context, bt.triggered_by_message_id,
699	               tm.content AS triggering_content,
700	               bt.final_output_message_id, om.content AS final_outbound_content,
701	               COALESCE(bt.reasoning, '') AS reasoning,
702	               COALESCE(
703	                 jsonb_agg(to_jsonb(tc) ORDER BY tc.called_at) FILTER (WHERE tc.id IS NOT NULL),
704	                 '[]'::jsonb
705	               ) AS tool_calls
706	        FROM bot_turns bt
707	        LEFT JOIN messages tm ON tm.id = bt.triggered_by_message_id
708	        LEFT JOIN messages om ON om.id = bt.final_output_message_id
709	        LEFT JOIN tool_calls tc ON tc.turn_id = bt.id
710	        {where}
711	        GROUP BY bt.id, tm.content, om.content
712	        ORDER BY bt.started_at DESC
713	        LIMIT ${len(params)}
714	        """,
715	        *params,
716	    )
717	    return GetBotActionsOutput(
718	        actions=[
719	            BotAction(
720	                turn_id=row["turn_id"],
721	                started_at=row["started_at"],
722	                user_in_context=row["user_in_context"],
723	                triggered_by_message_id=row["triggered_by_message_id"],
724	                final_output_message_id=row["final_output_message_id"],
725	                triggering_content=row["triggering_content"],
726	                final_outbound_content=row["final_outbound_content"],
727	                reasoning=row["reasoning"],
728	                tool_calls=list(row["tool_calls"] or []),
729	            )
730	            for row in rows
731	        ]
732	    )
733
```

> AGENT

Now let me check the SendMessagePartOutput schema to verify "withheld" is allowed.

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"SendMessagePartOutput\\|status\" /Users/user_c042661f/Documents/Veas/tool_schemas.py | head -50",
  "description": "Find SendMessagePartOutput schema"
}
```

> TOOL

tool_result Bash
```
265:    status: ThemeStatus
300:    status: MemoryStatus = MemoryStatus.active
309:    status: MemoryStatus
324:    status: WatchStatus | None = WatchStatus.open
333:    status: WatchStatus
349:    status: ObservationStatus = ObservationStatus.active
361:    status: ObservationStatus
387:    status: OOBStatus
557:    status: BridgeCandidateStatus
580:    status: BridgeCandidateStatus | None = Field(
582:        description="Optional explicit lifecycle status. Runtime defaults are applied by the tool implementation.",
593:    status: BridgeCandidateStatus | None = None
605:    status: BridgeCandidateStatus | None = None
650:    status: MemoryStatus | None = None
689:    status: ThemeStatus | None = None
764:    status: ObservationStatus | None = None
972:class SendMessagePartOutput(BaseModel):
973:    status: Literal[
1055:    "send_message_part": (SendMessagePartInput, SendMessagePartOutput),
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tool_schemas.py",
  "offset": 972,
  "limit": 35
}
```

> TOOL

tool_result Read
```
972	class SendMessagePartOutput(BaseModel):
973	    status: Literal[
974	        "sent",
975	        "duplicate",
976	        "blocked",
977	        "withheld",
978	        "interrupted",
979	        "provider_failed",
980	        "not_enabled",
981	    ]
982	    part_key: str | None = None
983	    client_part_key: str | None = None
984	    message_id: UUID | None = None
985	    provider_message_id: str | None = None
986	    delivered_content: str | None = None
987	    visible_to_user: bool = False
988	    sent_so_far: list[str] = Field(default_factory=list)
989	    reason: str | None = None
990	    suggested_rewrite: str | None = None
991	
992	
993	# --- consult_perspective ---
994	
995	
996	class ConsultPerspectiveInput(BaseModel):
997	    template: PerspectiveTemplate | None = None
998	    perspective: str | None = Field(default=None, min_length=1, max_length=1000)
999	    focus: str = Field(min_length=1, max_length=1500)
1000	    proposed_response: str | None = Field(default=None, max_length=3000)
1001	
1002	    @model_validator(mode="after")
1003	    def require_one_perspective_source(self) -> "ConsultPerspectiveInput":
1004	        if (self.template is None) == (self.perspective is None):
1005	            raise ValueError("provide exactly one of template or perspective")
1006	        return self
```

> AGENT

Good, `withheld` is valid. Now let me check existing tests:

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/Veas/tests/ | grep -i \"safety\\|read_tools\\|send_message\"",
  "description": "List relevant test files"
}
```

> TOOL

tool_result Bash
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/Veas/tests/",
  "description": "List all tests"
}
```

> TOOL

tool_result Bash
```
__init__.py
__pycache__
conftest.py
fixtures
test_admin.py
test_agentic.py
test_agentic_lifecycle.py
test_charge.py
test_config.py
test_consult_perspective.py
test_crypto.py
test_debouncer.py
test_decay.py
test_discord.py
test_discord_pacing_docs.py
test_eval_execution.py
test_eval_workflow.py
test_evals_assertions.py
test_evals_capture.py
test_evals_corpus.py
test_evals_db.py
test_evals_factories.py
test_evals_judge.py
test_evals_replay.py
test_evals_runner.py
test_evals_scenario.py
test_health.py
test_hot_context.py
test_inbound_source.py
test_llm_phase.py
test_main_startup_pacing.py
test_media.py
test_oob_check.py
test_oob_countersummary.py
test_ops_scripts.py
test_pacer.py
test_pacing_storage.py
test_pause_resume.py
test_recovery.py
test_scheduled_jobs.py
test_scoring.py
test_send_outbound.py
test_spend.py
test_spend_plan6.py
test_staging.py
test_tool_schemas_importable.py
test_tools.py
test_whatsapp_webhook.py
test_whitelist.py
```

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"text_safety\\|clean_user_facing_text\\|looks_like_internal_process_text\" /Users/user_c042661f/Documents/Veas/tests/ /Users/user_c042661f/Documents/Veas/app/",
  "description": "Find usage of text_safety"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:17:def test_clean_user_facing_text_removes_internal_process_leaks():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:26:    assert agentic.clean_user_facing_text(text) == (
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:32:def test_clean_user_facing_text_removes_broader_analysis_preamble():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:41:    assert agentic.clean_user_facing_text(text) == (
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:47:def test_clean_user_facing_text_removes_phase_error_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:58:    assert agentic.clean_user_facing_text(text) == ""
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:61:def test_clean_user_facing_text_removes_write_tools_phase_gate_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:71:    assert agentic.clean_user_facing_text(text) == ""
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:74:def test_clean_user_facing_text_removes_interrupted_process_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:77:    assert agentic.clean_user_facing_text(text) == ""
/Users/user_c042661f/Documents/Veas/app/services/agentic.py:23:from app.services.text_safety import clean_user_facing_text
/Users/user_c042661f/Documents/Veas/app/services/agentic.py:721:            assistant_text = clean_user_facing_text(assistant_text)
/Users/user_c042661f/Documents/Veas/app/services/text_safety.py:70:def looks_like_internal_process_text(text: str) -> bool:
/Users/user_c042661f/Documents/Veas/app/services/text_safety.py:76:def clean_user_facing_text(text: str) -> str:
/Users/user_c042661f/Documents/Veas/app/services/hot_context.py:17:from app.services.text_safety import clean_user_facing_text, looks_like_internal_process_text
/Users/user_c042661f/Documents/Veas/app/services/hot_context.py:78:        cleaned = clean_user_facing_text(raw_content)
/Users/user_c042661f/Documents/Veas/app/services/hot_context.py:79:        content = cleaned if cleaned or looks_like_internal_process_text(raw_content) else content
```

> AGENT

Ignoring the task tools reminder as this work is straightforward. Let me view the existing tests:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py",
  "offset": 1,
  "limit": 90
}
```

> TOOL

tool_result Read
```
1	from __future__ import annotations
2	
3	from datetime import UTC, datetime, timedelta
4	from uuid import uuid4
5	
6	import pytest
7	
8	from app.models.user import User
9	from app.config import get_settings
10	from app.services import agentic
11	from app.services.tools.registry import call_tool
12	from app.services.pacer import PacingDecision
13	
14	pytestmark = pytest.mark.anyio
15	
16	
17	def test_clean_user_facing_text_removes_internal_process_leaks():
18	    text = """The miscarriage mention is new — it's not in the stored memory yet. That's significant context. Responding now.
19	
20	---
21	
22	That parallel you just drew matters.
23	
24	What do you think gets in the way?"""
25	
26	    assert agentic.clean_user_facing_text(text) == (
27	        "That parallel you just drew matters.\n\n"
28	        "What do you think gets in the way?"
29	    )
30	
31	
32	def test_clean_user_facing_text_removes_broader_analysis_preamble():
33	    text = """The person's message is rich and self-aware — he's naming both his own patterns. No new tools needed; I have enough context.
34	
35	---
36	
37	That's a really honest thing to name.
38	
39	The thing I'd gently push on: is the busyness doing some work for you?"""
40	
41	    assert agentic.clean_user_facing_text(text) == (
42	        "That's a really honest thing to name.\n\n"
43	        "The thing I'd gently push on: is the busyness doing some work for you?"
44	    )
45	
46	
47	def test_clean_user_facing_text_removes_phase_error_leak():
48	    text = (
49	        "The system is still flagging my write calls as being in the read phase -- "
50	        "this appears to be a system constraint issue. My user-facing reply has "
51	        "already been delivered above. The watch item ed7ac62e should be addressed: "
52	        "The sender confirmed both flagged phrases were voice-to-text errors from a voice "
53	        "note, not descriptions of physical contact, and no safety escalation is "
54	        "warranted. The observation 4ccfee43 should be updated to reflect the same "
55	        "resolution."
56	    )
57	
58	    assert agentic.clean_user_facing_text(text) == ""
59	
60	
61	def test_clean_user_facing_text_removes_write_tools_phase_gate_leak():
62	    text = (
63	        "It appears the write tools are returning phase errors unexpectedly. "
64	        "The user-facing reply has already been delivered. The key updates to "
65	        "record are: reinforcing the \"wither and die\" observation with the sender's "
66	        "clarification that love is still present, and updating the communication "
67	        "theme to reflect tonight's session depth. These will need to be retried "
68	        "when the phase gate resolves."
69	    )
70	
71	    assert agentic.clean_user_facing_text(text) == ""
72	
73	
74	def test_clean_user_facing_text_removes_interrupted_process_leak():
75	    text = "Interrupted — I'll pick up from Peter's next message."
76	
77	    assert agentic.clean_user_facing_text(text) == ""
78	
79	
80	async def test_run_agentic_turn_lifecycle_ordering(fake_pool, app_env, monkeypatch):
81	    user = User(uuid4(), "Maya", "15555550100", "UTC")
82	    partner = User(uuid4(), "Ben", "15555550101", "UTC")
83	    fake_pool.users[user.id] = {"id": user.id, "name": user.name, "phone": user.phone, "timezone": user.timezone}
84	    fake_pool.users[partner.id] = {
85	        "id": partner.id,
86	        "name": partner.name,
87	        "phone": partner.phone,
88	        "timezone": partner.timezone,
89	    }
90	    message_id = uuid4()
```

> AGENT

Now let me check how existing tests for read_tools / send_message_part exist:

> TOOL

tool_use Bash
```json
{
  "command": "grep -rn \"send_message_part\" /Users/user_c042661f/Documents/Veas/tests/ /Users/user_c042661f/Documents/Veas/app/services/tools/ | head -30",
  "description": "Find send_message_part tests"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/Documents/Veas/tests/test_consult_perspective.py:151:    assert CONSULT_PHASE_TOOLS == READ_PHASE_TOOLS - {"send_message_part", "consult_perspective"}
/Users/user_c042661f/Documents/Veas/tests/test_consult_perspective.py:152:    assert "send_message_part" not in CONSULT_PHASE_TOOLS
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:11:from app.services.tools.read_tools import send_message_part
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:482:async def test_send_message_part_paced_followup_uses_composition_and_rhythm(
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:551:    first = await send_message_part(ctx, SendMessagePartInput(content="Six."))
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:552:    second = await send_message_part(ctx, SendMessagePartInput(content="x" * 30))
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:566:async def test_send_message_part_interrupts_after_paced_wait_before_provider_send(
/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py:640:    result = await send_message_part(ctx, SendMessagePartInput(content="stale part"))
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:432:async def test_run_agentic_send_message_part_is_visible_to_phase_b(fake_pool, app_env, monkeypatch):
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:480:            assert "send_message_part" in allowed_tools
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:483:                "send_message_part",
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:490:                "send_message_part",
/Users/user_c042661f/Documents/Veas/app/services/tools/registry.py:40:    "send_message_part": "Send one coherent user-visible Discord message part now when that is conversationally useful — a short acknowledgement before a deeper thought, or when the user explicitly asks for separate messages. Use for natural conversational moves, not process updates or paragraph splitting. The result is the authority for what actually reached the user; if it reports `interrupted`, stop sending user-visible text in that turn.",
/Users/user_c042661f/Documents/Veas/app/services/tools/registry.py:86:    "send_message_part": read_tools.send_message_part,
/Users/user_c042661f/Documents/Veas/app/services/tools/registry.py:131:    "send_message_part",
/Users/user_c042661f/Documents/Veas/app/services/tools/registry.py:165:CONSULT_PHASE_TOOLS = READ_PHASE_TOOLS - {"send_message_part", "consult_perspective"}
/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py:155:async def send_message_part(ctx: TurnContext, args: SendMessagePartInput) -> SendMessagePartOutput:
/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py:156:    logger.info("read tool send_message_part turn_id=%s", ctx.turn_id)
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py",
  "offset": 1,
  "limit": 80
}
```

> TOOL

tool_result Read
```
1	from datetime import UTC, datetime, timedelta
2	from uuid import uuid4
3	
4	import pytest
5	
6	from app.models.user import User
7	from app.services import hooks, system_state
8	from app.services.pacer import DiscordPacer
9	from app.services.messaging import send_outbound, send_outbound_part
10	from app.services.templates import TemplateCall, render_template
11	from app.services.tools.read_tools import send_message_part
12	from app.services.turn_context import TurnContext
13	from app.services import whatsapp
14	from tool_schemas import SendMessagePartInput
15	
16	
17	pytestmark = pytest.mark.anyio
18	
19	
20	@pytest.fixture(autouse=True)
21	def reset_hooks():
22	    hooks.check_oob = None
23	    yield
24	    hooks.check_oob = None
25	
26	
27	def _user(fake_pool) -> User:
28	    row = {"id": uuid4(), "name": "Maya", "phone": "15555550100", "timezone": "UTC"}
29	    fake_pool.users[row["id"]] = row
30	    return User(**row)
31	
32	
33	def _inbound(fake_pool, user: User, sent_at: datetime) -> None:
34	    message_id = uuid4()
35	    fake_pool.messages[message_id] = {
36	        "id": message_id,
37	        "direction": "inbound",
38	        "sender_id": user.id,
39	        "recipient_id": None,
40	        "content": "hi",
41	        "processing_state": "raw",
42	        "sent_at": sent_at,
43	        "charge": None,
44	        "whatsapp_message_id": f"wa-{message_id}",
45	        "media_type": None,
46	        "media_url": None,
47	        "media_duration_seconds": None,
48	        "media_analysis": None,
49	        "edit_history": None,
50	        "edited_at": None,
51	        "deleted_at": None,
52	    }
53	
54	
55	async def test_free_form_path_sends_text_and_updates_row(fake_pool, monkeypatch) -> None:
56	    user = _user(fake_pool)
57	    _inbound(fake_pool, user, datetime.now(UTC) - timedelta(minutes=5))
58	    sent = []
59	
60	    async def send_text(to, body):
61	        sent.append((to, body))
62	        return {"messages": [{"id": "wamid.out"}]}
63	
64	    monkeypatch.setattr("app.services.whatsapp.send_text", send_text)
65	
66	    row_id = await send_outbound(fake_pool, user, "hello")
67	
68	    assert sent == [(user.phone, "hello")]
69	    assert fake_pool.messages[row_id]["whatsapp_message_id"] == "wamid.out"
70	    assert fake_pool.messages[row_id]["processing_state"] == "processed"
71	    assert fake_pool.users[user.id]["onboarding_state"] == "welcomed"
72	
73	
74	async def test_free_form_path_records_bot_turn_id(fake_pool, monkeypatch) -> None:
75	    user = _user(fake_pool)
76	    turn_id = uuid4()
77	    _inbound(fake_pool, user, datetime.now(UTC) - timedelta(minutes=5))
78	
79	    async def send_text(to, body):
80	        return {"messages": [{"id": "wamid.out"}]}
```

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py",
  "offset": 470,
  "limit": 170
}
```

> TOOL

tool_result Read
```
470	        part_index=1,
471	    )
472	
473	    assert first["status"] == "sent"
474	    assert second["status"] == "duplicate"
475	    assert first["message_id"] == second["message_id"]
476	    assert sent == ["first part"]
477	    assert second["sent_so_far"] == ["first part"]
478	    assert fake_pool.users[user.id]["onboarding_state"] == "welcomed"
479	    get_settings.cache_clear()
480	
481	
482	async def test_send_message_part_paced_followup_uses_composition_and_rhythm(
483	    fake_pool,
484	    app_env,
485	    monkeypatch,
486	) -> None:
487	    monkeypatch.setenv("MESSAGING_PROVIDER", "discord")
488	    monkeypatch.setenv("DISCORD_MULTI_MESSAGE_DELAY_S", "1.1")
489	    monkeypatch.setenv("DISCORD_PACING_COMPOSITION_JITTER_RATIO", "0")
490	    from app.config import get_settings
491	
492	    get_settings.cache_clear()
493	    now = datetime(2026, 5, 1, 12, 0, tzinfo=UTC)
494	    user = _user(fake_pool)
495	    partner = _user(fake_pool)
496	    fake_pool.users[user.id]["pacing_preferences"] = {
497	        "answer_typing_min_s": 0.4,
498	        "answer_typing_max_s": 10,
499	        "answer_chars_per_s": 10,
500	        "max_typing_wait_s": 10,
501	    }
502	    turn_id = uuid4()
503	    fake_pool.bot_turns[turn_id] = {
504	        "id": turn_id,
505	        "reasoning": "",
506	        "completed_at": None,
507	        "failure_reason": None,
508	        "triggering_message_ids": [],
509	        "final_output_message_id": None,
510	    }
511	    sent = []
512	    typing_sent_at = []
513	    sleeps = []
514	    paced_calls = []
515	
516	    def current_time() -> datetime:
517	        return now
518	
519	    async def sleep(seconds: float) -> None:
520	        nonlocal now
521	        sleeps.append(seconds)
522	        now += timedelta(seconds=seconds)
523	
524	    async def send_typing(channel_id: str) -> None:
525	        typing_sent_at.append((channel_id, now))
526	
527	    async def send_text(to, body, *, send_typing_indicator=True):
528	        sent.append((to, body, send_typing_indicator, list(sleeps)))
529	        return {"messages": [{"id": f"discord-{len(sent)}"}]}
530	
531	    pacer = DiscordPacer(fake_pool, send_typing=send_typing, sleep=sleep, now=current_time)
532	
533	    async def before_paced_send(answer_text: str, *, send_kind: str, part_index: int | None) -> None:
534	        paced_calls.append((answer_text, send_kind, part_index))
535	        await pacer.perform_send_typing(user, "channel-1", answer_text, send_kind=send_kind, part_index=part_index)
536	
537	    ctx = TurnContext(
538	        turn_id=turn_id,
539	        pool=fake_pool,
540	        user=user,
541	        partner=partner,
542	        triggering_message_ids=[],
543	        turn_started_at=now,
544	        incremental_sending_enabled=True,
545	        send_typing_indicator=False,
546	        before_paced_send=before_paced_send,
547	        sent_message_parts=[],
548	    )
549	    monkeypatch.setattr("app.services.discord.send_text", send_text)
550	
551	    first = await send_message_part(ctx, SendMessagePartInput(content="Six."))
552	    second = await send_message_part(ctx, SendMessagePartInput(content="x" * 30))
553	
554	    assert first.status == "sent"
555	    assert second.status == "sent"
556	    assert paced_calls == [("Six.", "incremental_first", 1), ("x" * 30, "incremental_next", 2)]
557	    assert sleeps == pytest.approx([0.4, 1.1, 3.0])
558	    assert typing_sent_at[1][1] - typing_sent_at[0][1] == timedelta(seconds=1.5)
559	    assert sent == [
560	        (user.phone, "Six.", False, [0.4]),
561	        (user.phone, "x" * 30, False, [0.4, 1.1, 3.0]),
562	    ]
563	    get_settings.cache_clear()
564	
565	
566	async def test_send_message_part_interrupts_after_paced_wait_before_provider_send(
567	    fake_pool,
568	    app_env,
569	    monkeypatch,
570	) -> None:
571	    monkeypatch.setenv("MESSAGING_PROVIDER", "discord")
572	    from app.config import get_settings
573	
574	    get_settings.cache_clear()
575	    started_at = datetime(2026, 5, 1, 12, 0, tzinfo=UTC)
576	    user = _user(fake_pool)
577	    partner = _user(fake_pool)
578	    trigger_id = uuid4()
579	    fake_pool.messages[trigger_id] = {
580	        "id": trigger_id,
581	        "direction": "inbound",
582	        "sender_id": user.id,
583	        "recipient_id": None,
584	        "content": "first",
585	        "processing_state": "raw",
586	        "sent_at": started_at,
587	        "charge": "routine",
588	        "whatsapp_message_id": "discord-in",
589	        "media_type": None,
590	        "media_url": None,
591	        "media_duration_seconds": None,
592	        "media_analysis": None,
593	        "edit_history": None,
594	        "edited_at": None,
595	        "deleted_at": None,
596	    }
597	    sent = []
598	    paced_calls = []
599	
600	    async def send_text(to, body, *, send_typing_indicator=True):
601	        sent.append(body)
602	        return {"messages": [{"id": "discord-out"}]}
603	
604	    async def before_paced_send(answer_text: str, *, send_kind: str, part_index: int | None) -> None:
605	        paced_calls.append((answer_text, send_kind, part_index))
606	        newer_id = uuid4()
607	        fake_pool.messages[newer_id] = {
608	            "id": newer_id,
609	            "direction": "inbound",
610	            "sender_id": user.id,
611	            "recipient_id": None,
612	            "content": "wait one more thing",
613	            "processing_state": "raw",
614	            "sent_at": started_at + timedelta(milliseconds=1),
615	            "charge": "routine",
616	            "whatsapp_message_id": "discord-in-2",
617	            "media_type": None,
618	            "media_url": None,
619	            "media_duration_seconds": None,
620	            "media_analysis": None,
621	            "edit_history": None,
622	            "edited_at": None,
623	            "deleted_at": None,
624	        }
625	
626	    ctx = TurnContext(
627	        turn_id=uuid4(),
628	        pool=fake_pool,
629	        user=user,
630	        partner=partner,
631	        triggering_message_ids=[trigger_id],
632	        turn_started_at=started_at,
633	        incremental_sending_enabled=True,
634	        send_typing_indicator=False,
635	        before_paced_send=before_paced_send,
636	        sent_message_parts=[],
637	    )
638	    monkeypatch.setattr("app.services.discord.send_text", send_text)
639
```

> AGENT

Now I have a clear understanding. Let me also check `tests/test_text_safety.py`:

> TOOL

tool_use Bash
```json
{
  "command": "ls /Users/user_c042661f/Documents/Veas/tests/test_text_safety.py 2>&1; grep -rn \"looks_like_internal_process_text\\|clean_user_facing_text\" /Users/user_c042661f/Documents/Veas/tests/",
  "description": "Check for text_safety tests"
}
```

> TOOL

tool_result Bash
```
ls: /Users/user_c042661f/Documents/Veas/tests/test_text_safety.py: No such file or directory
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:17:def test_clean_user_facing_text_removes_internal_process_leaks():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:26:    assert agentic.clean_user_facing_text(text) == (
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:32:def test_clean_user_facing_text_removes_broader_analysis_preamble():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:41:    assert agentic.clean_user_facing_text(text) == (
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:47:def test_clean_user_facing_text_removes_phase_error_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:58:    assert agentic.clean_user_facing_text(text) == ""
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:61:def test_clean_user_facing_text_removes_write_tools_phase_gate_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:71:    assert agentic.clean_user_facing_text(text) == ""
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:74:def test_clean_user_facing_text_removes_interrupted_process_leak():
/Users/user_c042661f/Documents/Veas/tests/test_agentic_lifecycle.py:77:    assert agentic.clean_user_facing_text(text) == ""
```

> AGENT

Now I have a concern with the existing tests. The first one (`test_clean_user_facing_text_removes_internal_process_leaks`) expects: preamble (with markers like `responding now`, `not in the stored memory yet`) is dropped, but the actual reply ("That parallel...") survives. With the proposed whole-paragraph drop logic, the existing separator handling first splits and keeps `parts[1]`. Then after re-checking on the remainder ("That parallel..."), no internal-looking lines, so it returns it intact. Good.

Test #2 same logic applies.

Test #3 (phase_error_leak): no `---` separator, all text is "internal-looking" — under new rule would still return "". OK.

Test #4 (write_tools_phase_gate_leak): No separator, all text — still returns "". OK.

Test #5 (interrupted_process_leak): "Interrupted —" matches `_PROCESS_OPENERS` so internal. Returns "". OK.

Now Sample 2 doesn't contain any of the existing patterns nor hex IDs in backticks?... Wait, it does: `` `9ca2ebc3` `` and `` `298048b2` ``. Good. But line 1: "**New observation** about [REDACTED]'s self-theory of causation (significance 5)" — that contains "new observation" pattern. Good.

Let me also verify Sample 1: "Memory `61ddbfdb` — needs updating to include [REDACTED]'s agreement." Contains backtick hex `61ddbfdb` (regex match) AND "needs updating". Line 2: "Let me do those writes now." matches "let me do those writes" / "do those writes". Good.

Sample 3: long single line containing many internal patterns — should still return "" with whole-paragraph drop. Good.

Now let me make the edits:

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/text_safety.py",
  "old_string": "_INTERNAL_OUTPUT_PATTERNS = (\n    \"stored memory\",\n    \"memory yet\",\n    \"not in the stored\",\n    \"responding now\",\n    \"phase a\",\n    \"phase b\",\n    \"read phase\",\n    \"write phase\",\n    \"write calls\",\n    \"write tools\",\n    \"phase errors\",\n    \"phase gate\",\n    \"tool call\",\n    \"tool \",\n    \"tools needed\",\n    \"new tools\",\n    \"hot context\",\n    \"enough context\",\n    \"database row\",\n    \"database\",\n    \"do not need any more reads\",\n    \"don't need any more reads\",\n    \"no more reads\",\n    \"let me read it properly\",\n    \"trigger message\",\n    \"trigger is\",\n    \"current context\",\n    \"watch item\",\n    \"system is still flagging\",\n    \"user-facing reply has already been delivered\",\n    \"key updates to record\",\n    \"need to be retried\",\n    \"needs to be retried\",\n    \"pick up from peter's next message\",\n    \"pick up from the next message\",\n    \"safety escalation\",\n    \"should be addressed\",\n    \"should be updated\",\n)",
  "new_string": "_INTERNAL_OUTPUT_PATTERNS = (\n    \"stored memory\",\n    \"memory yet\",\n    \"not in the stored\",\n    \"responding now\",\n    \"phase a\",\n    \"phase b\",\n    \"read phase\",\n    \"write phase\",\n    \"write calls\",\n    \"write tools\",\n    \"phase errors\",\n    \"phase gate\",\n    \"tool call\",\n    \"tool \",\n    \"tools needed\",\n    \"new tools\",\n    \"hot context\",\n    \"enough context\",\n    \"database row\",\n    \"database\",\n    \"do not need any more reads\",\n    \"don't need any more reads\",\n    \"no more reads\",\n    \"let me read it properly\",\n    \"trigger message\",\n    \"trigger is\",\n    \"current context\",\n    \"watch item\",\n    \"system is still flagging\",\n    \"user-facing reply has already been delivered\",\n    \"key updates to record\",\n    \"need to be retried\",\n    \"needs to be retried\",\n    \"pick up from peter's next message\",\n    \"pick up from the next message\",\n    \"safety escalation\",\n    \"should be addressed\",\n    \"should be updated\",\n    \"let me do those writes\",\n    \"do those writes\",\n    \"needs updating\",\n    \"new observation\",\n    \"reinforce observation\",\n    \"reinforce** observation\",\n    \"update observation\",\n    \"supersede observation\",\n    \"new memory\",\n    \"reinforce memory\",\n    \"update memory\",\n    \"supersede memory\",\n    \"new theme\",\n    \"new watch item\",\n    \"new oob\",\n)\n\n_INTERNAL_ID_REF_RE = re.compile(r\"`[a-f0-9]{6,}`\")"
}
```

> TOOL

tool_result Edit
```
The file /Users/user_c042661f/Documents/Veas/app/services/text_safety.py has been updated successfully.
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/text_safety.py",
  "old_string": "def _looks_internal(line: str) -> bool:\n    lowered = line.lower()\n    return any(pattern in lowered for pattern in _INTERNAL_OUTPUT_PATTERNS) or any(\n        lowered.startswith(pattern) for pattern in _PROCESS_OPENERS\n    )\n\n\ndef looks_like_internal_process_text(text: str) -> bool:\n    \"\"\"Return true when text appears to be only private process narration.\"\"\"\n    lines = [line.strip() for line in text.splitlines() if line.strip()]\n    return bool(lines) and all(_looks_internal(line) or line in {\"---\", \"***\", \"___\"} for line in lines)\n\n\ndef clean_user_facing_text(text: str) -> str:\n    \"\"\"Strip model process leakage from text before it reaches a user or prompt history.\"\"\"\n    parts = re.split(r\"(?m)^\\s*(?:---|\\*\\*\\*|___)\\s*$\", text, maxsplit=1)\n    if len(parts) == 2 and any(_looks_internal(line.strip()) for line in parts[0].splitlines() if line.strip()):\n        text = parts[1]\n\n    cleaned_lines: list[str] = []\n    for raw_line in text.splitlines():\n        line = raw_line.strip()\n        if line in {\"---\", \"***\", \"___\"}:\n            continue\n        if _looks_internal(line):\n            continue\n        cleaned_lines.append(raw_line.rstrip())\n    cleaned = \"\\n\".join(cleaned_lines).strip()\n    cleaned = re.sub(r\"\\n{3,}\", \"\\n\\n\", cleaned)\n    return cleaned",
  "new_string": "def _looks_internal(line: str) -> bool:\n    lowered = line.lower()\n    if any(pattern in lowered for pattern in _INTERNAL_OUTPUT_PATTERNS):\n        return True\n    if any(lowered.startswith(pattern) for pattern in _PROCESS_OPENERS):\n        return True\n    if _INTERNAL_ID_REF_RE.search(line):\n        return True\n    return False\n\n\ndef looks_like_internal_process_text(text: str) -> bool:\n    \"\"\"Return true when text appears to be only private process narration.\"\"\"\n    lines = [line.strip() for line in text.splitlines() if line.strip()]\n    return bool(lines) and all(_looks_internal(line) or line in {\"---\", \"***\", \"___\"} for line in lines)\n\n\ndef clean_user_facing_text(text: str) -> str:\n    \"\"\"Strip model process leakage from text before it reaches a user or prompt history.\"\"\"\n    parts = re.split(r\"(?m)^\\s*(?:---|\\*\\*\\*|___)\\s*$\", text, maxsplit=1)\n    if len(parts) == 2 and any(_looks_internal(line.strip()) for line in parts[0].splitlines() if line.strip()):\n        text = parts[1]\n\n    # Whole-paragraph drop: if any non-blank, non-separator line in the remaining\n    # text looks like internal process narration, drop the entire text rather\n    # than ship a half-coherent fragment with the offending lines snipped out.\n    for raw_line in text.splitlines():\n        line = raw_line.strip()\n        if not line or line in {\"---\", \"***\", \"___\"}:\n            continue\n        if _looks_internal(line):\n            return \"\"\n\n    cleaned_lines: list[str] = []\n    for raw_line in text.splitlines():\n        line = raw_line.strip()\n        if line in {\"---\", \"***\", \"___\"}:\n            continue\n        cleaned_lines.append(raw_line.rstrip())\n    cleaned = \"\\n\".join(cleaned_lines).strip()\n    cleaned = re.sub(r\"\\n{3,}\", \"\\n\\n\", cleaned)\n    return cleaned"
}
```

> TOOL

tool_result Edit
```
The file /Users/user_c042661f/Documents/Veas/app/services/text_safety.py has been updated successfully.
```

> AGENT

Now Fix A — gate `send_message_part`. Let me update the read_tools.py imports and add the check:

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py",
  "old_string": "from app.services.oob_check import check_oob_with_policy, summarize_partner_oob",
  "new_string": "from app.services.oob_check import check_oob_with_policy, summarize_partner_oob\nfrom app.services.text_safety import clean_user_facing_text, looks_like_internal_process_text"
}
```

> TOOL

tool_result Edit
```
The file /Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py has been updated successfully.
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py",
  "old_string": "    content = args.content.strip()\n    part_index = len(sent_parts) + 1",
  "new_string": "    content = args.content.strip()\n    if looks_like_internal_process_text(content) or clean_user_facing_text(content).strip() == \"\":\n        return SendMessagePartOutput(\n            status=\"withheld\",\n            [REDACTED],\n            visible_to_user=False,\n            sent_so_far=[part[\"content\"] for part in sent_parts],\n            reason=\"content looks like internal process narration (memory IDs, write plans, phase notes); send a user-facing reply instead\",\n        )\n    part_index = len(sent_parts) + 1"
}
```

> TOOL

tool_result Edit
```
The file /Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py has been updated successfully.
```

> AGENT

Now let me create the new test file. First, let me also re-verify the existing tests will still pass given the whole-paragraph drop semantics. Test 1: separator splits → preamble dropped → remainder is "That parallel you just drew matters.\n\nWhat do you think gets in the way?" — none looks internal → output unchanged. Good.

Now create the new test file:

> TOOL

tool_use Write
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_text_safety.py",
  "content": "from __future__ import annotations\n\nfrom app.services.text_safety import (\n    clean_user_facing_text,\n    looks_like_internal_process_text,\n)\n\n\nSAMPLE_1 = (\n    \"**Memory `61ddbfdb`** — needs updating to include [REDACTED]'s agreement.\\n\"\n    \"\\n\"\n    \"Let me do those writes now.\"\n)\n\nSAMPLE_2 = (\n    \"1. **New observation** about [REDACTED]'s self-theory of causation (significance 5)\\n\"\n    \"2. **Reinforce** observation `9ca2ebc3` about her self-awareness\\n\"\n    \"3. **Update** observation `298048b2` — she's not just holding curiosity, \"\n    \"she's now offering genuine structural insight after hearing Peter's view\"\n)\n\nSAMPLE_3 = (\n    \"The system is still flagging my write calls as being in the read phase — \"\n    \"this appears to be a system constraint issue. My user-facing reply has \"\n    \"already been delivered above. The watch item `ed7ac62e` should be addressed: \"\n    \"Peter confirmed both flagged phrases were voice-to-text errors from a voice \"\n    \"note, not descriptions of physical contact, and no safety escalation is \"\n    \"warranted. The observation `4ccfee43` should be updated to reflect the same \"\n    \"resolution.\"\n)\n\nBENIGN = \"hey, that sounds tough — want to talk through it?\"\n\n\ndef test_clean_user_facing_text_drops_sample_1():\n    assert clean_user_facing_text(SAMPLE_1) == \"\"\n\n\ndef test_clean_user_facing_text_drops_sample_2():\n    assert clean_user_facing_text(SAMPLE_2) == \"\"\n\n\ndef test_clean_user_facing_text_drops_sample_3():\n    assert clean_user_facing_text(SAMPLE_3) == \"\"\n\n\ndef test_clean_user_facing_text_keeps_benign_reply():\n    assert clean_user_facing_text(BENIGN) == BENIGN\n\n\ndef test_looks_like_internal_process_text_sample_1():\n    assert looks_like_internal_process_text(SAMPLE_1) is True\n\n\ndef test_looks_like_internal_process_text_benign_is_false():\n    assert looks_like_internal_process_text(BENIGN) is False\n\n\ndef test_clean_user_facing_text_keeps_reply_after_separator_preamble():\n    text = \"phase a notes\\n---\\nReal reply.\"\n    assert clean_user_facing_text(text) == \"Real reply.\"\n\n\ndef test_clean_user_facing_text_drops_whole_paragraph_with_internal_line():\n    # A real-looking sentence followed by a clearly internal line should drop\n    # the whole text rather than ship a stranded fragment.\n    text = \"That sounds heavy.\\nLet me do those writes now.\"\n    assert clean_user_facing_text(text) == \"\"\n\n\ndef test_clean_user_facing_text_id_reference_alone_is_internal():\n    text = \"Update memory `abcdef12` and move on.\"\n    assert clean_user_facing_text(text) == \"\"\n"
}
```

> TOOL

tool_result Write
```
File created successfully at: /Users/user_c042661f/Documents/Veas/tests/test_text_safety.py
```

> AGENT

Now let me add a `send_message_part` test for the withheld case. Let me see how an existing test structures that, since I need a TurnContext:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py",
  "offset": 370,
  "limit": 100
}
```

> TOOL

tool_result Read
```
370	    assert review["suggested_rewrite"] == "rewritten"
371	    assert review["verdict"] == "rewrite"
372	
373	    async def block(content, recipient):
374	        return {"verdict": "block", "reason": "blocked", "suggested_rewrite": None}
375	
376	    hooks.check_oob = block
377	    row_id = await send_outbound(fake_pool, user, "blocked")
378	    assert fake_pool.messages[row_id]["processing_state"] == "withheld"
379	
380	
381	async def test_global_pause_default_withholds_and_ignore_pause_bypasses(fake_pool, monkeypatch) -> None:
382	    user = _user(fake_pool)
383	    _inbound(fake_pool, user, datetime.now(UTC) - timedelta(minutes=5))
384	    sent = []
385	
386	    async def send_text(to, body):
387	        sent.append(body)
388	        return {"messages": [{"id": f"wamid.{len(sent)}"}]}
389	
390	    monkeypatch.setattr("app.services.whatsapp.send_text", send_text)
391	    await system_state.pause(fake_pool, user.id)
392	
393	    withheld_id = await send_outbound(fake_pool, user, "ordinary")
394	    sent_id = await send_outbound(fake_pool, user, "control", ignore_pause=True)
395	
396	    assert fake_pool.messages[withheld_id]["processing_state"] == "withheld"
397	    assert fake_pool.messages[sent_id]["processing_state"] == "processed"
398	    assert sent == ["control"]
399	
400	
401	async def test_send_outbound_passes_protected_owner_ids_and_withholds_current_user_leak(fake_pool, monkeypatch) -> None:
402	    user = _user(fake_pool)
403	    current_user_id = uuid4()
404	    protected_owner_ids = [current_user_id, user.id]
405	    _inbound(fake_pool, user, datetime.now(UTC) - timedelta(minutes=5))
406	    sent = []
407	    oob_calls = []
408	
409	    async def send_text(to, body):
410	        sent.append(body)
411	        return {"messages": [{"id": "wamid.should-not-send"}]}
412	
413	    async def block_current_user_leak(pool, content, recipient_id, protected_owner_ids=None):
414	        oob_calls.append((pool, content, recipient_id, protected_owner_ids))
415	        return {
416	            "verdict": "block",
417	            "reason": "current-user hard OOB",
418	            "suggested_rewrite": None,
419	            "checker_failed": False,
420	        }
421	
422	    monkeypatch.setattr("app.services.whatsapp.send_text", send_text)
423	    hooks.check_oob = block_current_user_leak
424	
425	    row_id = await send_outbound(fake_pool, user, "current-user protected detail", protected_owner_ids=protected_owner_ids)
426	
427	    assert sent == []
428	    assert oob_calls == [(fake_pool, "current-user protected detail", user.id, protected_owner_ids)]
429	    assert fake_pool.messages[row_id]["processing_state"] == "withheld"
430	
431	
432	async def test_send_outbound_part_uses_runtime_part_key_for_idempotency(fake_pool, app_env, monkeypatch) -> None:
433	    monkeypatch.setenv("MESSAGING_PROVIDER", "discord")
434	    from app.config import get_settings
435	
436	    get_settings.cache_clear()
437	    user = _user(fake_pool)
438	    fake_pool.users[user.id]["onboarding_state"] = "pending"
439	    turn_id = uuid4()
440	    fake_pool.bot_turns[turn_id] = {
441	        "id": turn_id,
442	        "reasoning": "",
443	        "completed_at": None,
444	        "failure_reason": None,
445	        "triggering_message_ids": [],
446	        "final_output_message_id": None,
447	    }
448	    sent = []
449	
450	    async def send_text(to, body, *, send_typing_indicator=True):
451	        sent.append(body)
452	        return {"messages": [{"id": f"discord-{len(sent)}"}]}
453	
454	    monkeypatch.setattr("app.services.discord.send_text", send_text)
455	
456	    first = await send_outbound_part(
457	        fake_pool,
458	        user,
459	        "first part",
460	        bot_turn_id=turn_id,
461	        part_key=f"{turn_id}:1",
462	        part_index=1,
463	    )
464	    second = await send_outbound_part(
465	        fake_pool,
466	        user,
467	        "first part",
468	        bot_turn_id=turn_id,
469	        part_key=f"{turn_id}:1",
```

> AGENT

Let me find a simpler test that uses TurnContext directly to model a withheld test:

> TOOL

tool_use Bash
```json
{
  "command": "grep -n \"TurnContext(\" /Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py | head -5",
  "description": "Find TurnContext usage in tests"
}
```

> TOOL

tool_result Bash
```
537:    ctx = TurnContext(
626:    ctx = TurnContext(
```

> AGENT

I'll add a test for the withheld behavior modeled on the existing pattern. Let me add it to test_send_outbound.py since that's where the other send_message_part tests live:

> TOOL

tool_use Read
```json
{
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py",
  "offset": 640,
  "limit": 80
}
```

> TOOL

tool_result Read
```
640	    result = await send_message_part(ctx, SendMessagePartInput(content="stale part"))
641	
642	    assert result.status == "interrupted"
643	    assert paced_calls == [("stale part", "incremental_first", 1)]
644	    assert sent == []
645	    assert [row for row in fake_pool.messages.values() if row.get("direction") == "outbound"] == []
646	    get_settings.cache_clear()
647
```

> TOOL

tool_use Edit
```json
{
  "replace_all": false,
  "file_path": "/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py",
  "old_string": "    result = await send_message_part(ctx, SendMessagePartInput(content=\"stale part\"))\n\n    assert result.status == \"interrupted\"\n    assert paced_calls == [(\"stale part\", \"incremental_first\", 1)]\n    assert sent == []\n    assert [row for row in fake_pool.messages.values() if row.get(\"direction\") == \"outbound\"] == []\n    get_settings.cache_clear()",
  "new_string": "    result = await send_message_part(ctx, SendMessagePartInput(content=\"stale part\"))\n\n    assert result.status == \"interrupted\"\n    assert paced_calls == [(\"stale part\", \"incremental_first\", 1)]\n    assert sent == []\n    assert [row for row in fake_pool.messages.values() if row.get(\"direction\") == \"outbound\"] == []\n    get_settings.cache_clear()\n\n\nasync def test_send_message_part_withholds_internal_process_narration(\n    fake_pool,\n    app_env,\n    monkeypatch,\n) -> None:\n    monkeypatch.setenv(\"MESSAGING_PROVIDER\", \"discord\")\n    from app.config import get_settings\n\n    get_settings.cache_clear()\n    user = _user(fake_pool)\n    partner = _user(fake_pool)\n    turn_id = uuid4()\n    fake_pool.bot_turns[turn_id] = {\n        \"id\": turn_id,\n        \"reasoning\": \"\",\n        \"completed_at\": None,\n        \"failure_reason\": None,\n        \"triggering_message_ids\": [],\n        \"final_output_message_id\": None,\n    }\n    sent: list[str] = []\n\n    async def send_text(to, body, *, send_typing_indicator=True):\n        sent.append(body)\n        return {\"messages\": [{\"id\": \"discord-out\"}]}\n\n    monkeypatch.setattr(\"app.services.discord.send_text\", send_text)\n\n    ctx = TurnContext(\n        turn_id=turn_id,\n        pool=fake_pool,\n        user=user,\n        partner=partner,\n        triggering_message_ids=[],\n        turn_started_at=datetime.now(UTC),\n        incremental_sending_enabled=True,\n        send_typing_indicator=False,\n        before_paced_send=None,\n        sent_message_parts=[],\n    )\n\n    result = await send_message_part(\n        ctx,\n        SendMessagePartInput(\n            content=\"**Memory `61ddbfdb`** — needs updating to include [REDACTED]'s agreement.\\n\\nLet me do those writes now.\"\n        ),\n    )\n\n    assert result.status == \"withheld\"\n    assert result.visible_to_user is False\n    assert result.reason and \"internal process\" in result.reason\n    assert sent == []\n    get_settings.cache_clear()"
}
```

> TOOL

tool_result Edit
```
The file /Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py has been updated successfully.
```

> AGENT

Now let me syntax-check and run the relevant tests:

> TOOL

tool_use Bash
```json
{
  "command": "python -m py_compile app/services/text_safety.py app/services/tools/read_tools.py tests/test_text_safety.py tests/test_send_outbound.py && echo OK",
  "description": "Syntax check changed files"
}
```

> TOOL

tool_result Bash
```
Exit code 127
pyenv: version `3.8.10' is not installed (set by /Users/user_c042661f/.pyenv/version)
pyenv: python: command not found

The `python' command exists in these Python versions:
  3.11.11

Note: See 'pyenv help global' for tips on allowing both
      python2 and python3 to be found.
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -m py_compile app/services/text_safety.py app/services/tools/read_tools.py tests/test_text_safety.py tests/test_send_outbound.py && echo OK",
  "description": "Syntax check changed files with python3"
}
```

> TOOL

tool_result Bash
```
OK
```

> TOOL

tool_use Bash
```json
{
  "command": "ls pyproject.toml pytest.ini setup.cfg 2>&1; head -40 pyproject.toml 2>/dev/null",
  "description": "Check project config"
}
```

> TOOL

tool_result Bash
```
ls: pytest.ini: No such file or directory
ls: setup.cfg: No such file or directory
pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mediator-bot"
version = "0.1.0"
description = "FastAPI foundation for the mediator bot."
requires-python = ">=3.11"
dependencies = [
    "anthropic>=0.40",
    "fastapi",
    "uvicorn[standard]",
    "asyncpg",
    "pydantic>=2",
    "pydantic-settings",
    "cryptography",
    "httpx",
    "python-multipart",
    "websockets",
    "PyYAML",
    "emoji>=2.14",
]

[project.optional-dependencies]
dev = [
    "pytest",
    "pytest-asyncio",
    "anyio",
]

[tool.setuptools.packages.find]
include = ["app*", "evals*", "resident_chat_runtime*"]

[tool.setuptools]
py-modules = ["tool_schemas"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

> TOOL

tool_use Bash
```json
{
  "command": "python3 -m pytest tests/test_text_safety.py tests/test_agentic_lifecycle.py::test_clean_user_facing_text_removes_internal_process_leaks tests/test_agentic_lifecycle.py::test_clean_user_facing_text_removes_broader_analysis_preamble tests/test_agentic_lifecycle.py::test_clean_user_facing_text_removes_phase_error_leak tests/test_agentic_lifecycle.py::test_clean_user_facing_text_removes_write_tools_phase_gate_leak tests/test_agentic_lifecycle.py::test_clean_user_facing_text_removes_interrupted_process_leak -x 2>&1 | tail -40",
  "description": "Run text_safety and existing clean tests"
}
```

> TOOL

tool_result Bash
```
/opt/homebrew/opt/python@3.14/bin/python3.14: No module named pytest
```

> TOOL

tool_use Bash
```json
{
  "command": "which pytest; ls .venv venv 2>&1 | head; find . -maxdepth 3 -name \"pytest\" -type f 2>/dev/null | head",
  "description": "Find pytest"
}
```

> TOOL

tool_result Bash
```
/Users/user_c042661f/.pyenv/shims/pytest
ls: venv: No such file or directory
.venv:
CACHEDIR.TAG
bin
lib
pyvenv.cfg
./.venv/bin/pytest
```

> TOOL

tool_use Bash
```json
{
  "command": ".venv/bin/pytest tests/test_text_safety.py tests/test_agentic_lifecycle.py -k \"clean_user_facing_text\" -x 2>&1 | tail -40",
  "description": "Run text_safety and existing clean tests"
}
```

> TOOL

tool_result Bash
```
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.0.3, pluggy-1.6.0
rootdir: /Users/user_c042661f/Documents/Veas
configfile: pyproject.toml
plugins: asyncio-1.3.0, anyio-4.13.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collected 23 items / 11 deselected / 12 selected

tests/test_text_safety.py .......                                        [ 58%]
tests/test_agentic_lifecycle.py .....                                    [100%]

====================== 12 passed, 11 deselected in 0.02s =======================
```

> AGENT

All 12 clean_user_facing_text tests pass. Wait, it says 7 in `test_text_safety.py` but I wrote 9 tests, only `clean_user_facing_text` ones got selected. Let me run all my new tests including the `looks_like_internal_process_text` ones:

> TOOL

tool_use Bash
```json
{
  "command": ".venv/bin/pytest tests/test_text_safety.py -v 2>&1 | tail -25",
  "description": "Run all text_safety tests"
}
```

> TOOL

tool_result Bash
```
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.0.3, pluggy-1.6.0 -- /Users/user_c042661f/Documents/Veas/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/user_c042661f/Documents/Veas
configfile: pyproject.toml
plugins: asyncio-1.3.0, anyio-4.13.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 9 items

tests/test_text_safety.py::test_clean_user_facing_text_drops_sample_1 PASSED [ 11%]
tests/test_text_safety.py::test_clean_user_facing_text_drops_sample_2 PASSED [ 22%]
tests/test_text_safety.py::test_clean_user_facing_text_drops_sample_3 PASSED [ 33%]
tests/test_text_safety.py::test_clean_user_facing_text_keeps_benign_reply PASSED [ 44%]
tests/test_text_safety.py::test_looks_like_internal_process_text_sample_1 PASSED [ 55%]
tests/test_text_safety.py::test_looks_like_internal_process_text_benign_is_false PASSED [ 66%]
tests/test_text_safety.py::test_clean_user_facing_text_keeps_reply_after_separator_preamble PASSED [ 77%]
tests/test_text_safety.py::test_clean_user_facing_text_drops_whole_paragraph_with_internal_line PASSED [ 88%]
tests/test_text_safety.py::test_clean_user_facing_text_id_reference_alone_is_internal PASSED [100%]

============================== 9 passed in 0.01s ===============================
```

> AGENT

All 9 pass. Now let me run the send_message_part-related tests:

> TOOL

tool_use Bash
```json
{
  "command": ".venv/bin/pytest tests/test_send_outbound.py -v 2>&1 | tail -50",
  "description": "Run send_outbound tests"
}
```

> TOOL

tool_result Bash
```
============================= test session starts ==============================
platform darwin -- Python 3.11.14, pytest-9.0.3, pluggy-1.6.0 -- /Users/user_c042661f/Documents/Veas/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/user_c042661f/Documents/Veas
configfile: pyproject.toml
plugins: asyncio-1.3.0, anyio-4.13.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 18 items

tests/test_send_outbound.py::test_free_form_path_sends_text_and_updates_row PASSED [  5%]
tests/test_send_outbound.py::test_free_form_path_records_bot_turn_id PASSED [ 11%]
tests/test_send_outbound.py::test_successful_bot_initiated_outbound_marks_onboarding_welcomed PASSED [ 16%]
tests/test_send_outbound.py::test_template_path_and_param_validation PASSED [ 22%]
tests/test_send_outbound.py::test_twilio_send_text_and_template PASSED   [ 27%]
tests/test_send_outbound.py::test_twilio_api_key_auth_uses_account_sid_for_url PASSED [ 33%]
tests/test_send_outbound.py::test_discord_provider_sends_without_whatsapp_window PASSED [ 38%]
tests/test_send_outbound.py::test_discord_provider_can_suppress_low_level_typing PASSED [ 44%]
tests/test_send_outbound.py::test_null_window_uses_template_no_none_arithmetic PASSED [ 50%]
tests/test_send_outbound.py::test_defer_without_template_appends_reasoning PASSED [ 55%]
tests/test_send_outbound.py::test_retry_success_and_exhaustion PASSED    [ 61%]
tests/test_send_outbound.py::test_pause_and_oob_hooks PASSED             [ 66%]
tests/test_send_outbound.py::test_global_pause_default_withholds_and_ignore_pause_bypasses PASSED [ 72%]
tests/test_send_outbound.py::test_send_outbound_passes_protected_owner_ids_and_withholds_current_user_leak PASSED [ 77%]
tests/test_send_outbound.py::test_send_outbound_part_uses_runtime_part_key_for_idempotency PASSED [ 83%]
tests/test_send_outbound.py::test_send_message_part_paced_followup_uses_composition_and_rhythm PASSED [ 88%]
tests/test_send_outbound.py::test_send_message_part_interrupts_after_paced_wait_before_provider_send PASSED [ 94%]
tests/test_send_outbound.py::test_send_message_part_withholds_internal_process_narration PASSED [100%]

============================== 18 passed in 0.11s ==============================
```

> AGENT

All 18 pass including my new test. Now let me run the full test suite to make sure nothing else broke:

> TOOL

tool_use Bash
```json
{
  "command": ".venv/bin/pytest 2>&1 | tail -30",
  "description": "Run full test suite",
  "timeout": 300000
}
```

> TOOL

tool_result Bash
```
tests/test_evals_replay.py .                                             [ 40%]
tests/test_evals_runner.py ....                                          [ 41%]
tests/test_evals_scenario.py .....                                       [ 43%]
tests/test_health.py ....s                                               [ 45%]
tests/test_hot_context.py .....                                          [ 46%]
tests/test_inbound_source.py ..                                          [ 47%]
tests/test_llm_phase.py ...                                              [ 48%]
tests/test_main_startup_pacing.py ...                                    [ 49%]
tests/test_media.py ...........                                          [ 52%]
tests/test_oob_check.py .....                                            [ 54%]
tests/test_oob_countersummary.py ...                                     [ 55%]
tests/test_ops_scripts.py .                                              [ 55%]
tests/test_pacer.py ..................                                   [ 61%]
tests/test_pacing_storage.py ..                                          [ 61%]
tests/test_pause_resume.py ...                                           [ 62%]
tests/test_recovery.py .....                                             [ 64%]
tests/test_scheduled_jobs.py ........                                    [ 66%]
tests/test_scoring.py ...                                                [ 67%]
tests/test_send_outbound.py ..................                           [ 73%]
tests/test_spend.py ss                                                   [ 74%]
tests/test_spend_plan6.py .                                              [ 74%]
tests/test_staging.py .                                                  [ 74%]
tests/test_text_safety.py .........                                      [ 77%]
tests/test_tool_schemas_importable.py ....                               [ 79%]
tests/test_tools.py .................................................... [ 95%]
                                                                         [ 95%]
tests/test_whatsapp_webhook.py .........                                 [ 98%]
tests/test_whitelist.py .....                                            [100%]

======================== 312 passed, 3 skipped in 1.41s ========================
```

> AGENT

Full suite: 312 passed, 3 skipped, 0 failures.

## Summary

### Files changed

**`/Users/user_c042661f/Documents/Veas/app/services/text_safety.py`**
- Added 15 new patterns to `_INTERNAL_OUTPUT_PATTERNS` (lines 47-61): `let me do those writes`, `do those writes`, `needs updating`, `new observation`, `reinforce observation`, `reinforce** observation`, `update observation`, `supersede observation`, `new memory`, `reinforce memory`, `update memory`, `supersede memory`, `new theme`, `new watch item`, `new oob`.
- Added `_INTERNAL_ID_REF_RE = re.compile(r"`[a-f0-9]{6,}`")` (line 63).
- Updated `_looks_internal` (lines ~78-85) to also return `True` when the regex matches.
- Changed `clean_user_facing_text` (lines ~99-108) to do a whole-paragraph drop: after the existing separator-split preamble handling, if any non-blank/non-separator line in the remaining text looks internal, return `""`. The separator preamble path is preserved.
- `looks_like_internal_process_text` left unchanged.

**`/Users/user_c042661f/Documents/Veas/app/services/tools/read_tools.py`**
- Added import (line 16): `from app.services.text_safety import clean_user_facing_text, looks_like_internal_process_text`.
- In `send_message_part` (lines ~192-200), right after `content = args.content.strip()`, added a guard returning `SendMessagePartOutput(status="withheld", ...)` when `looks_like_internal_process_text(content)` or `clean_user_facing_text(content).strip() == ""`.

**`/Users/user_c042661f/Documents/Veas/tests/test_text_safety.py`** (new file)
- 9 tests covering the three production samples, a benign control, `looks_like_internal_process_text` truth/false, separator preamble preservation, whole-paragraph drop, and ID-reference-only detection.

**`/Users/user_c042661f/Documents/Veas/tests/test_send_outbound.py`**
- Added `test_send_message_part_withholds_internal_process_narration` at the end (after the existing interruption test) verifying Sample 1 content yields `status="withheld"`, `visible_to_user=False`, no provider send, and a reason mentioning "internal process".

### Test results
- `pytest` full suite: **312 passed, 3 skipped, 0 failures** in 1.41s.
- All five pre-existing `clean_user_facing_text_*` tests in `test_agentic_lifecycle.py` still pass — verified the whole-paragraph drop change does not regress the separator-preamble cases (their post-separator bodies are clean, so they survive).

### Notes / surprises
- `SendMessagePartOutput.status` already includes `"withheld"` in its `Literal[...]` union (tool_schemas.py line 977), as expected.
- The whole-paragraph drop is robust against a benign first line followed by an internal one — verified by the dedicated test, which is important since the model could otherwise emit "That sounds heavy.\nLet me do those writes now." and have only the second line stripped, leaving an unmoored fragment.
- Nothing punted.
