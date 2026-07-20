> DEVELOPER

I have many posthog errors, here is one such stacktrace:

{
  "uuid": "019df379-8c96-7171-9599-0845e7504847",
  "event": "$exception",
  "properties": {
    "$cymbal_errors": [
      "Invalid properties on event 019df379-8c96-7171-9599-0845e7504847, serde error: missing field `type`"
    ],
    "$exception_list": [
      {
        "mechanism": {
          "handled": true,
          "type": "generic"
        },
        "stacktrace": {
          "frames": [
            {
              "colno": 30,
              "filename": "/C:/home/<USER>/AppData/Roaming/npm/node_modules/@code-insights/cli/server-dist/routes/route-helpers.js",
              "function": "<anonymous>",
              "in_app": false,
              "lineno": 127
            },
            {
              "colno": 5,
              "filename": "/C:/home/<USER>/AppData/Roaming/npm/node_modules/@code-insights/cli/node_modules/hono/dist/helper/streaming/sse.js",
              "function": "async run",
              "in_app": false,
              "lineno": 30
            }
          ]
        },
        "type": "Error",
        "value": "Cannot connect to Ollama at  http://10.10.10.67:11434 — is it running? Start it with: ollama serve"
      }
    ],
    "$exception_message": "Cannot connect to Ollama at  http://10.10.10.67:11434 — is it running? Start it with: ollama serve",
    "$exception_stack_trace_raw": "Error: Cannot connect to Ollama at  http://10.10.10.67:11434 — is it running? Start it with: ollama serve\n    at file:///C:/home/<USER>/AppData/Roaming/npm/node_modules/@code-insights/cli/server-dist/routes/route-helpers.js:127:30\n    at async run (file:///C:/home/<USER>/AppData/Roaming/npm/node_modules/@code-insights/cli/node_modules/hono/dist/helper/streaming/sse.js:30:5)",
    "$exception_type": "Error",
    "$geoip_disable": true,
    "$ip": "186.4.171.244",
    "$lib": "posthog-node",
    "$lib_version": "4.18.0",
    "$sent_at": "2026-05-04T14:52:02.582Z",
    "duration_ms": 306107,
    "error_message": "Cannot connect to Ollama at  http://10.10.10.67:11434 — is it running? Start it with: ollama serve",
    "error_type": "api_error",
    "llm_model": "gemma4:26b",
    "llm_provider": "ollama",
    "success": false,
    "type": "session",
    "$transformations_succeeded": [
      "GeoIP (019cad81-b34f-0000-8cca-78e5873bf67d)"
    ]
  },
  "timestamp": "2026-05-04T20:22:03.340000+05:30",
  "team_id": 328708,
  "distinct_id": "42faedf2f0e5318c",
  "elements_chain": "",
  "created_at": "2026-05-04T20:22:09.710000+05:30",
  "person_mode": "full"
}

Investigate this and tell me what is wrong..

> AGENT

Let me look at the relevant source files before diving deeper.

> TOOL

tool_use Bash
id: toolu_01Wqct2aVecoNLAxS5wHgS8K
```json
{
  "command": "find /home/<USER>/Workspace/codeInsights/code-insights/server/src/routes -name \"route-helpers*\" | head -5",
  "description": "Find route-helpers source file"
}
```

> TOOL

tool_use Bash
id: toolu_017TkirexnbVCNF2it32bQoZ
```json
{
  "command": "grep -rn \"Cannot connect to Ollama\" /home/<USER>/Workspace/codeInsights/code-insights --include=\"*.ts\" -l",
  "description": "Find where Ollama connection error is thrown"
}
```

> TOOL

tool_result
id: toolu_01Wqct2aVecoNLAxS5wHgS8K
```
/home/<USER>/Workspace/codeInsights/code-insights/server/src/routes/route-helpers.ts
```

> TOOL

tool_result
id: toolu_017TkirexnbVCNF2it32bQoZ
```
/home/<USER>/Workspace/codeInsights/code-insights/server/src/llm/providers/ollama.ts
```

> TOOL

tool_use Read
id: toolu_014hfSGMX2SUb7qa9aEAD9AJ
```json
{
  "file_path": "/home/<USER>/Workspace/codeInsights/code-insights/server/src/routes/route-helpers.ts"
}
```

> TOOL

tool_use Read
id: toolu_01E8RpN2YP2v1xFu1Txstsyy
```json
{
  "file_path": "/home/<USER>/Workspace/codeInsights/code-insights/server/src/llm/providers/ollama.ts"
}
```

> TOOL

tool_result
id: toolu_014hfSGMX2SUb7qa9aEAD9AJ
```
1	// Shared helpers for route files — eliminates duplicated SQL queries and LLM guard blocks.
2	// Centralising these here ensures the session/messages query columns stay in sync across
3	// analysis.ts, facets.ts, export.ts, and reflect.ts. If a new column is added to the
4	// sessions or messages tables it only needs updating in one place.
5	
6	import type { Context, MiddlewareHandler } from 'hono';
7	import { streamSSE } from 'hono/streaming';
8	import { getDb } from '@code-insights/cli/db/client';
9	import { trackEvent, captureError } from '@code-insights/cli/utils/telemetry';
10	import { isLLMConfigured, loadLLMConfig } from '../llm/client.js';
11	import { calculateAnalysisCost } from '../llm/analysis-pricing.js';
12	import type { AnalysisResult, AnalysisOptions } from '../llm/analysis.js';
13	import type { SessionData } from '../llm/analysis-db.js';
14	import type { SQLiteMessageRow } from '../llm/prompt-types.js';
15	
16	/**
17	 * Load a session row for LLM analysis. Returns undefined if the session doesn't exist
18	 * or has been soft-deleted. The selected columns match exactly what the analysis engine
19	 * expects via the SessionData interface.
20	 */
21	export function loadSessionForAnalysis(db: ReturnType<typeof getDb>, sessionId: string): SessionData | undefined {
22	  return db.prepare(`
23	    SELECT id, project_id, project_name, project_path, summary, ended_at, […]

> TOOL

tool_result
id: toolu_01E8RpN2YP2v1xFu1Txstsyy
```
1	// Ollama provider implementation (local models, no API key required)
2	
3	import type { LLMClient, LLMMessage, LLMResponse, ChatOptions } from '../types.js';
4	import { flattenContent } from '../types.js';
5	
6	const DEFAULT_OLLAMA_URL = 'http://localhost:11434';
7	
8	export function createOllamaClient(model: string, baseUrl?: string): LLMClient {
9	  const url = baseUrl || DEFAULT_OLLAMA_URL;
10	
11	  return {
12	    provider: 'ollama',
13	    model,
14	
15	    async chat(messages: LLMMessage[], options?: ChatOptions): Promise<LLMResponse> {
16	      let response: Response;
17	      try {
18	        response = await fetch(`${url}/api/chat`, {
19	          method: 'POST',
20	          headers: { 'Content-Type': 'application/json' },
21	          signal: options?.signal,
22	          body: JSON.stringify({
23	            model,
24	            // flattenContent converts ContentBlock[] to string; strings pass through unchanged.
25	            messages: messages.map(m => ({ role: m.role, content: flattenContent(m.content) })),
26	            stream: false,
27	            options: { temperature: 0.7 },
28	          }),
29	        });
30	      } catch (err) {
31	        // Network-level failure — Ollama is likely not running
32	        const cause = (err as { cause?: { code?: string } })?.cause;
33	        if (cause?.code === 'ECONNREFUSED' || (err instanceof TypeError && err.message.includes('fetch'))) {
34	          throw new Error(`Cannot connect to Ollama at ${url} — is it running? Start it with: ollama serve`);
35	        }
36 […]

> AGENT

Now let me look at the telemetry implementation, specifically `captureError`.

> TOOL

tool_use Bash
id: toolu_01NkZqg2A4w6hz1EJctX3GDM
```json
{
  "command": "grep -n \"captureError\\|trackEvent\" /home/<USER>/Workspace/codeInsights/code-insights/cli/src/utils/telemetry.ts | head -40",
  "description": "Find captureError and trackEvent definitions in telemetry"
}
```

> TOOL

tool_result
id: toolu_01NkZqg2A4w6hz1EJctX3GDM
```
38:// PostHog client — lazily initialized on first trackEvent call.
138: * Used to enrich trackEvent calls and captureError calls with consistent error metadata.
191: * Respects the same opt-out as trackEvent.
196:export function captureError(error: unknown, properties?: Record<string, unknown>): void {
235:export function trackEvent(event: TelemetryEventName, properties?: Record<string, unknown>): void {
```

> TOOL

tool_use Bash
id: toolu_01J9GDsMczN3L84kaWGZiCnD
```json
{
  "command": "grep -n \"ECONNREFUSED\\|fetch\\|TypeError\" /home/<USER>/Workspace/codeInsights/code-insights/server/src/llm/providers/ollama.ts",
  "description": "Check how Ollama handles connection errors"
}
```

> TOOL

tool_result
id: toolu_01J9GDsMczN3L84kaWGZiCnD
```
18:        response = await fetch(`${url}/api/chat`, {
33:        if (cause?.code === 'ECONNREFUSED' || (err instanceof TypeError && err.message.includes('fetch'))) {
85:    const response = await fetch(`${url}/api/tags`, {
```

> TOOL

tool_use Read
id: toolu_01CxzxZarja3h7dAwzmCQ4Lq
```json
{
  "file_path": "/home/<USER>/Workspace/codeInsights/code-insights/cli/src/utils/telemetry.ts",
  "offset": 185,
  "limit": 80
}
```

> TOOL

tool_result
id: toolu_01CxzxZarja3h7dAwzmCQ4Lq
```
185	
186	  return frames;
187	}
188	
189	/**
190	 * Capture an exception in PostHog. Never throws — telemetry must never break the CLI.
191	 * Respects the same opt-out as trackEvent.
192	 *
193	 * @param error - The caught error (or unknown value)
194	 * @param properties - Additional context properties (provider, model, etc.)
195	 */
196	export function captureError(error: unknown, properties?: Record<string, unknown>): void {
197	  const ph = getPostHogClient();
198	  if (!ph) return;
199	
200	  try {
201	    const { error_type, error_message } = classifyError(error);
202	    const exceptionType = error instanceof Error ? error.constructor.name : error_type;
203	    const stack = error instanceof Error && error.stack ? error.stack : '';
204	    const frames = stack ? parseStackFrames(stack) : [];
205	
206	    ph.capture({
207	      distinctId: getStableMachineId(),
208	      event: '$exception',
209	      properties: {
210	        $exception_message: error_message,
211	        $exception_type: exceptionType,
212	        $exception_stack_trace_raw: stack,
213	        $exception_list: [
214	          {
215	            type: exceptionType,
216	            value: error_message,
217	            mechanism: { type: 'generic', handled: true },
218	            ...(frames.length > 0 ? { stacktrace: { frames } } : {}),
219	          },
220	        ],
221	        ...(properties ?? {}),
222	      },
223	    });
224	  } catch {
225	    // Swallow all […]

> AGENT

Let me read the full telemetry file to understand the stack frame parsing and see the `classifyError` function.

> TOOL

tool_use Read
id: toolu_01KisSGXWEFeedWyWJG7FyvP
```json
{
  "file_path": "/home/<USER>/Workspace/codeInsights/code-insights/cli/src/utils/telemetry.ts",
  "offset": 100,
  "limit": 90
}
```

> TOOL

tool_result
id: toolu_01KisSGXWEFeedWyWJG7FyvP
```
100	 *
101	 * Returns true if the notice was shown.
102	 */
103	export function showTelemetryNoticeIfNeeded(): boolean {
104	  if (!isTelemetryEnabled()) return false;
105	
106	  const currentVersion = getCliVersion();
107	  let shownVersion: string | null = null;
108	
109	  if (fs.existsSync(NOTICE_FILE)) {
110	    try {
111	      shownVersion = fs.readFileSync(NOTICE_FILE, 'utf-8').trim();
112	    } catch {
113	      // Can't read — treat as not shown
114	    }
115	  }
116	
117	  if (shownVersion === currentVersion) return false;
118	
119	  // Show a condensed single-line disclosure
120	  console.log(chalk.dim('  Telemetry enabled · Disable: code-insights telemetry disable'));
121	
122	  // Write the current version as content — best-effort, non-fatal
123	  try {
124	    const configDir = getConfigDir();
125	    if (!fs.existsSync(configDir)) {
126	      fs.mkdirSync(configDir, { recursive: true, mode: 0o700 });
127	    }
128	    fs.writeFileSync(NOTICE_FILE, currentVersion, { encoding: 'utf-8', mode: 0o600 });
129	  } catch {
130	    // Non-fatal — if we can't write, we'll show the notice again next time
131	  }
132	
133	  return true;
134	}
135	
136	/**
137	 * Classify an error into a structured error_type + error_message pair.
138	 * Used to enrich trackEvent calls and captureError calls with consistent error metadata.
139	 */
140	export […]

> AGENT

Now I have a clear picture. There are **two distinct bugs** here.

`★ Insight ─────────────────────────────────────`
This PostHog event reveals a classic signal/noise problem in error telemetry: the same `captureError` path is firing for both **bugs** (unexpected exceptions) and **expected user-facing failures** (Ollama not configured/running). Good telemetry design separates these: `$exception` events should only fire for unexpected programming errors, not for gracefully-handled user errors.
`─────────────────────────────────────────────────`

---

## Two Issues Found

### Bug 1 — `captureError` fires for expected LLM failures (the main problem)

In `route-helpers.ts`, both `trackAnalysisResult` (line 100) and the `!result.success` branch of `streamSessionAnalysis` (line 202) call `captureError` whenever analysis fails:

```typescript
// trackAnalysisResult — lines 96-100
trackEvent('analysis_run', errorProperties);
captureError(new Error(result.error ?? `${analysisType} analysis failed`), errorProperties);  // ← WRONG
```

`captureError` emits a PostHog `$exception` event. But `result.success = false` is the **normal result** for user-facing errors like "Ollama not running", "invalid API key", "model not found" — these are handled gracefully and shown to the user. They are **not bugs**. `captureError` should only be called from `catch (err)` blocks (truly unexpected crashes), not from every `!result.success` path.

### Bug 2 — `type` property conflicts with PostHog's exception schema (causes the cymbal error)

When `captureError` is called with `{ type: […]