> DEVELOPER

analyse the auxilio-extension, and check for any performance issues, memory leak or any other issue that can cause the system resource excess consumption, slow down or crash of browser or webpage or the extension itself, give me a detailed report.

> AGENT

I'll analyze the auxilio-extension for performance issues, memory leaks, and resource consumption problems. Let me start by exploring its structure.

> TOOL

tool_use Bash
id: toolu_0184vVRi54DSkjzwxMmdZ3NS
```json
{
  "command": "cd /home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension && find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/build/*' | head -100",
  "description": "List extension files"
}
```

> TOOL

tool_result
id: toolu_0184vVRi54DSkjzwxMmdZ3NS
```
./wxt.config.ts
./PRIVACY_POLICY.md
./.DS_Store
./auxilio-visitor-share.zip
./key.pem
./env.d.ts
./AUTHENTICATION_FLOW.md
./README.md
./CHROMEWEBSTORE.md
./.gitignore
./package-lock.json
./package.json
./.env
./tsconfig.json
./.env.example
./CLAUDE.md
./design/global.css
./design/tokens.ts
./auxilio-visitor/background.js
./auxilio-visitor/manifest.json
./auxilio-visitor/options.html
./auxilio-visitor/sidepanel.html
./.wxt/wxt.d.ts
./.wxt/tsconfig.json
./output/auxilio-extension-0.11.6-chrome.zip
./output/auxilio-extension-0.11.34-chrome.zip
./output/auxilio-extension-0.14.1-chrome.zip
./.claude/settings.json
./.codex/hooks.json
./.codex/config.toml
./lib/messaging.ts
./lib/engine.ts
./lib/people.ts
./lib/calendar.ts
./lib/types.ts
./lib/calendar-sync.ts
./lib/config.ts
./lib/auth.ts
./entrypoints/calendar.content.ts
./entrypoints/background.ts
./.entire/settings.json
./.entire/.gitignore
./design/components/Card.tsx
./design/components/Chip.tsx
./design/components/Switch.tsx
./design/components/TextField.tsx
./design/components/Logo.tsx
./design/components/IconButton.tsx
./design/components/index.ts
./design/components/Button.tsx
./design/components/Spinner.tsx
./design/components/Skeleton.tsx
./auxilio-visitor/chunks/global-CfWv9_A7.js
./auxilio-visitor/chunks/options-CZkJ7oGK.js
./auxilio-visitor/chunks/sidepanel-v2O5bqD3.js
./auxilio-visitor/content-scripts/calendar.js
./auxilio-visitor/icon/48.png
./auxilio-visitor/icon/Auxilio-vector-logo.svg
./auxilio-visitor/icon/128.png
./auxilio-visitor/icon/16.png
./auxilio-visitor/icon/32.png
./auxilio-visitor/icon/96.png
./auxilio-visitor/assets/global-Bg4Tzvqc.css
./.wxt/types/globals.d.ts
./.wxt/types/imports-module.d.ts
./.wxt/types/i18n.d.ts
./.wxt/types/paths.d.ts
./.wxt/types/imports.d.ts
./features/visit/RosterRow.tsx
./features/visit/VisitPanel.tsx
./features/visit/SignInGate.tsx
./features/visit/PreviewSheet.tsx
./features/visit/AccountMenu.tsx
./features/visit/hooks.ts
./features/visit/EmptyState.tsx
./output/chrome-mv3/background.js
./output/chrome-mv3/manifest.json
./output/chrome-mv3/options.html
./output/chrome-mv3/sidepanel.html
./.claude/agents/entire-search.md
./.codex/agents/entire-search.toml
./public/icon/48.png
./public/icon/Auxilio-vector-logo.svg
./public/icon/128.png
./public/icon/16.png
./public/icon/32.png
./public/icon/96.png
./entrypoints/options/main.tsx
./entrypoints/options/index.html
./entrypoints/options/Options.tsx
./entrypoints/sidepanel/App.tsx
./entrypoints/sidepanel/main.tsx
./entrypoints/sidepanel/index.html
./.entire/logs/entire.log
./.entire/tmp/pre-prompt-1bc3fdd9-a559-469a-be5c-35a507269eee.json
./.entire/tmp/pre-prompt-aead60d8-891f-4b2b-9fdb-a0c8e99da520.json
./.entire/tmp/pre-prompt-6384626f-39e6-4116-8c48-4ea4b6c5c2a5.json
./.entire/tmp/pre-prompt-eaabde84-3181-4717-a7e3-54bacb3d588d.json
./.entire/tmp/pre-prompt-1ee62b17-aaf6-40ca-8d8f-460067cf81e8.json
./output/chrome-mv3/chunks/sidepanel-CW0cRA_k.js
```

> TOOL

tool_use Read
id: toolu_01WttnHuVmMy35HDKdrf8xV3
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/CLAUDE.md"
}
```

> TOOL

tool_result
id: toolu_01WttnHuVmMy35HDKdrf8xV3
```
1	# auxilio-extension
2	
3	Google **Chrome extension (MV3)** for Auxilio (Office Ops) — the **desktop** surface for registering office visitors directly inside Google Calendar. It is the richer counterpart to the `auxilio-workspace` Calendar add-on: where the add-on is mobile-capable but lives under the CardService "card ceiling," the extension gives a full React UI (realtime guest updates, per-guest invite toggle, template preview, inline edits, intentional auto-nudge).
4	
5	> Read the umbrella `../CLAUDE.md` for the four constraints and UX rules — they apply here.
6	> Strategy + approval analysis: `../Planning-docs/2026-06-18_calendar_visitor_chrome_extension_decision.md`.
7	> Build plan: the approved plan that scaffolded this repo.
8	
9	## What this is (and isn't)
10	
11	- **Is:** an MV3 extension (WXT + React 19 + TS) that injects a trigger into Google Calendar (web) and renders the registration flow in the **side panel**. A **channel surface / dumb adapter** — it forwards intent to `office-ops-engine`.
12	- **Isn't:** a place for business logic. Dedup, draft curation, invite/pass issuance, and lifecycle all live in `office-ops-engine`'s visitor plugin. This repo renders UI and calls the engine.
13	- **Isn't:** mobile. Extensions are desktop-Chrome only. The `auxilio-workspace` add-on remains the mobile surface. […]

> AGENT

Let me read the core files — the content script (most performance-sensitive since it runs on Google Calendar), the background worker, and the sync logic.

> TOOL

tool_use Read
id: toolu_01SYFAZnDGckPWBfEyFk1xk2
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/entrypoints/calendar.content.ts"
}
```

> TOOL

tool_result
id: toolu_01SYFAZnDGckPWBfEyFk1xk2
```
<system-reminder>[Truncated: PARTIAL view — showing lines 1-1153 of 1843 total (33958 tokens, cap 25000). Call Read with offset=1154 limit=1153 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>

1	/**
2	 * Content script on Google Calendar — the DOM layer of the hybrid model.
3	 *
4	 * It reads the open event surface (detail popover / expanded edit) to:
5	 *  - GATE the "Manage Visitors" button on the magic address being a guest,
6	 *  - capture the `data-eventid` (base64url "<eventId> <calendarId>"), and
7	 *  - take a best-effort SNAPSHOT (guest emails) so the panel can paint instantly
8	 *    and cover the unsaved (no-API) case.
9	 * The API layer (background) remains the authoritative source. We read only the
10	 * semantic `data-eventid`, the `[role="dialog"]` ARIA signal, and the surface's
11	 * visible text — no layout/CSS-class coupling, no injection into Google's markup.
12	 */
13	import { MAGIC_ADDRESS } from '@/lib/config';
14	import {
15	  ACTIVE_EID_KEY,
16	  ACTIVE_SNAPSHOT_KEY,
17	  AUTH_LAPSED,
18	  NUDGE_TARGETS,
19	  PANEL_STATE,
20	} from '@/lib/messaging';
21	import type { DomEventSnapshot, […]

> AGENT

Let me read the rest of the content script and the other performance-critical files in parallel.

> TOOL

tool_use Read
id: toolu_01JRCn1gS6tKZymdmXrwrR7h
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/entrypoints/calendar.content.ts",
  "offset": 1154,
  "limit": 700
}
```

> TOOL

tool_use Read
id: toolu_01SK5RYjqDxbwqjPSrh2612i
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/entrypoints/background.ts"
}
```

> TOOL

tool_result
id: toolu_01SK5RYjqDxbwqjPSrh2612i
```
1	import {
2	  ACTIVE_EID_KEY,
3	  ACTIVE_SNAPSHOT_KEY,
4	  AUTH_LAPSED,
5	  NUDGE_TARGETS,
6	  PANEL_STATE,
7	  SIDEPANEL_PORT,
8	  broadcastRefreshActive,
9	  type RpcRequest,
10	  type RpcResponse,
11	} from '@/lib/messaging';
12	import { authStatus, getValidTokens, signIn, signOut, wasConnected } from '@/lib/auth';
13	import { decodeEid, encodeEid, fetchActiveEvent } from '@/lib/calendar';
14	import {
15	  clearSyncToken,
16	  eventState,
17	  isEventHandled,
18	  isEventMarked,
19	  listForPanel,
20	  listMarked,
21	  listPendingICalUids,
22	  listSuggested,
23	  markHandled,
24	  markUnhandled,
25	  readEngineHandled,
26	  runSync,
27	  setEngineHandled,
28	  syncConfigChanged,
29	} from '@/lib/calendar-sync';
30	import { EngineError, engine } from '@/lib/engine';
31	import { resolveGuests } from '@/lib/people';
32	import type { VisitorEventSummary } from '@/lib/types';
33	
34	const SYNC_ALARM = 'auxilio-sync';
35	const BADGE_COLOR = '#92288E';
36	// Cross-channel status poll throttle: don't ask the engine "which are handled"
37	// every alarm tick. Poll when the pending iCalUid set changes, else at most this
38	// often. Stored in storage.local so the throttle survives SW restarts.
39	const STATUS_POLL_KEY = 'auxilio.statusPoll';
40	const STATUS_POLL_INTERVAL_MS = 5 * 60_000;
41	// Muted/error badge for a recoverable auth lapse — visually distinct from the
42	// brand-tinted visitor-count badge so "nudging is offline" never reads as a […]

> TOOL

tool_result
id: toolu_01JRCn1gS6tKZymdmXrwrR7h
```
1154	function buildContentRowInner(row: HTMLElement, copy: RowCopy = DEFAULT_COPY): HTMLElement {
1155	  row.textContent = '';
1156	  const icon = document.createElement('span');
1157	  icon.className = 'auxilio-mv-row-icon';
1158	  icon.setAttribute('aria-hidden', 'true');
1159	  icon.innerHTML = AUXILIO_SVG;
1160	  const text = document.createElement('span');
1161	  text.className = 'auxilio-mv-row-text';
1162	  const title = document.createElement('span');
1163	  title.className = 'auxilio-mv-row-title';
1164	  title.textContent = copy.title;
1165	  title.setAttribute('role', 'button');
1166	  title.tabIndex = 0;
1167	  const sub = document.createElement('span');
1168	  sub.className = 'auxilio-mv-row-sub';
1169	  sub.textContent = copy.sub;
1170	  text.append(title, sub);
1171	  row.append(icon, text);
1172	  return title;
1173	}
1174	
1175	/** Match our row to a native sibling row: the same padding (the real left gutter),
1176	 *  the same icon size and icon→text gap so our icon lines up with Google's, the same
1177	 *  icon vertical offset, and the host theme's text color (so it reads identically in
1178	 *  light and dark). Computed-style/geometry only — measured ONCE at placement, never
1179	 *  per mutation. Falls back to sane defaults when no reference row is available. */
1180	function styleContentRowLikeNative(row: HTMLElement, list: HTMLElement): void {
1181	  const clamp = (n: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, n));
1182	  const icon = row.querySelector<HTMLElement>('.auxilio-mv-row-icon');
1183	  const text = row.querySelector<HTMLElement>('.auxilio-mv-row-text'); […]

> AGENT

Now the sync logic and the side panel app, plus the supporting libs.

> TOOL

tool_use Read
id: toolu_011Vdch1vcdk1nJGaFaiAzST
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/lib/calendar-sync.ts"
}
```

> TOOL

tool_use Read
id: toolu_01VFDFdkfAEyqJbgYBQswvvE
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/lib/calendar.ts"
}
```

> TOOL

tool_result
id: toolu_01VFDFdkfAEyqJbgYBQswvvE
```
1	/**
2	 * Calendar read (background only). Two jobs:
3	 *  1) resolve the canonical event for a given eid (events.get) — authoritative
4	 *     iCalUID + attendees for the side panel.
5	 *  2) list changes via a sync token (events.list) — the durable "what changed"
6	 *     API that drives post-save refresh + the visitor-event nudge/badge.
7	 * Calendar.events.readonly only.
8	 */
9	import { MAGIC_ADDRESS } from './config';
10	import type { ActiveEvent } from './types';
11	
12	/** Forward window for the change-feed scan. `singleEvents=true` expands EVERY
13	 *  recurring series into per-occurrence instances; with no bound a daily event
14	 *  alone yields ~700 rows and a busy calendar returns 6000+ — a ~14s, 25-page
15	 *  scan that the MV3 worker can be killed in the middle of (leaving the marked
16	 *  set stale). Visitor nudges are near-term, so we cap the window: ~90 days cuts
17	 *  that to a few hundred rows / ~2s. The periodic full re-scan slides it forward. */
18	const FORWARD_WINDOW_MS = 90 * 24 * 60 * 60_000;
19	
20	/** `eid` is URL-safe base64 of "<eventId> <calendarId>" (calendarId optional). */ […]

> TOOL

tool_result
id: toolu_011Vdch1vcdk1nJGaFaiAzST
```
1	/**
2	 * Calendar sync (background only). The durable, official "what changed" engine:
3	 * runs on a chrome.alarm, lists changes via a sync token, and maintains the set
4	 * of upcoming visitor (magic-address) events in storage.local. Drives:
5	 *  - post-save refresh of the open event (changedIds),
6	 *  - the visitor-event notification + toolbar badge (newMarked / count),
7	 *  - the side panel's "open from list" picker (listMarked).
8	 * No DOM. Reflects SAVED state only (pre-save edits are add-on-only — see
9	 * Planning-docs/2026-06-19_calendar_addon_vs_extension_capabilities.md).
10	 */
11	import { MAGIC_ADDRESS } from './config';
12	import { encodeEid, isMarked, isSuggested, listEvents } from './calendar';
13	import type { EventState, PanelVisitorEvent, VisitorEventSummary } from './types';
14	
15	const SYNC_TOKEN_KEY = 'auxilio.syncToken';
16	const MARKED_KEY = 'auxilio.markedEvents';
17	/** Events the user has already issued passes for from this extension — keyed by
18	 *  eventId, value = when handled. A durable overlay over the marked set so a
19	 *  finished event stops badging/notifying/nudging instead of nagging until it
20	 *  ages out. Local-only signal: passes sent via the add-on or another device
21	 *  won't appear here (full cross-channel truth needs […]

> AGENT

Now the side panel React app, hooks, and the auth/people/engine libs.

> TOOL

tool_use Read
id: toolu_01F94xY4zEfU5eYfMxWwA12w
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/entrypoints/sidepanel/App.tsx"
}
```

> TOOL

tool_result
id: toolu_01F94xY4zEfU5eYfMxWwA12w
```
1	import { VisitPanel } from '@/features/visit/VisitPanel';
2	
3	export default function App() {
4	  return <VisitPanel />;
5	}
6	
```

> TOOL

tool_use Read
id: toolu_01XJ2naLMTqYm9z2MPBvatz2
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/features/visit/hooks.ts"
}
```

> TOOL

tool_result
id: toolu_01XJ2naLMTqYm9z2MPBvatz2
```
1	import { useEffect, useState } from 'react';
2	import {
3	  useMutation,
4	  useQuery,
5	  useQueryClient,
6	} from '@tanstack/react-query';
7	import { ACTIVE_EID_KEY, ACTIVE_SNAPSHOT_KEY, RpcError, rpc } from '@/lib/messaging';
8	import type {
9	  ActiveEvent,
10	  AuthStatus,
11	  DomEventSnapshot,
12	  DraftPatch,
13	  DraftResponse,
14	  VisitDraft,
15	} from '@/lib/types';
16	
17	const isAuthError = (e: unknown) => e instanceof RpcError && !!e.needsAuth;
18	
19	/** The pending event id, read reactively from storage.session. */
20	export function useActiveEid(): string | null {
21	  const [eid, setEid] = useState<string | null>(null);
22	  useEffect(() => {
23	    chrome.storage.session
24	      .get(ACTIVE_EID_KEY)
25	      .then((r) => setEid((r[ACTIVE_EID_KEY] as string) ?? null));
26	    const listener = (
27	      changes: { [k: string]: chrome.storage.StorageChange },
28	      area: string,
29	    ) => {
30	      if (area === 'session' && changes[ACTIVE_EID_KEY]) {
31	        setEid((changes[ACTIVE_EID_KEY].newValue as string) ?? null);
32	      }
33	    };
34	    chrome.storage.onChanged.addListener(listener);
35	    return () => chrome.storage.onChanged.removeListener(listener);
36	  }, []);
37	  return eid;
38	}
39	
40	/** The DOM snapshot for the active event (instant + unsaved fallback). */
41	export function useActiveSnapshot(): DomEventSnapshot | null {
42	  const [snap, setSnap] = useState<DomEventSnapshot | null>(null);
43	  useEffect(() => {
44 […]

> TOOL

tool_use Read
id: toolu_01FtLLWVNwDHWbCECGLZb2yr
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/lib/auth.ts"
}
```

> TOOL

tool_result
id: toolu_01FtLLWVNwDHWbCECGLZb2yr
```
1	/**
2	 * Auth (background only). Mints a Google id_token (engine auth) + access_token
3	 * (Calendar read) via chrome.identity.launchWebAuthFlow against a Web OAuth
4	 * client, caches them in storage.session, and silently re-mints on expiry.
5	 *
6	 * The id_token's audience must be on the engine's AUXILIO_WORKSPACE_OAUTH_CLIENT_ID
7	 * allow-list. Calendar-only scopes (no Gmail/Drive — CASA line).
8	 */
9	import { OAUTH_CLIENT_ID } from './config';
10	import { engine } from './engine';
11	import type { AuthStatus } from './types';
12	
13	const SCOPES = [
14	  'openid',
15	  'email',
16	  'profile',
17	  'https://www.googleapis.com/auth/calendar.events.readonly',
18	  // Resolve guest names + photos the Calendar event API omits for external guests
19	  // (People API, client-side — mirrors the add-on). Both are *sensitive* scopes,
20	  // NOT restricted → no CASA, and still no Gmail/Drive. Adding these requires each
21	  // user to re-consent once (a silent renew won't widen scope).
22	  'https://www.googleapis.com/auth/contacts.readonly',
23	  'https://www.googleapis.com/auth/contacts.other.readonly',
24	].join(' ');
25	
26	const KEY = 'auxilio.tokens';
27	
28	/** Durable (storage.local) marker that the user has connected and intends to stay
29	 *  connected. Token bundles live in storage.session and are WIPED on every browser
30 […]

> AGENT

Now the main React panel component and the remaining libs.

> TOOL

tool_use Read
id: toolu_01T8TUJ37rqB3GkZzioojoWt
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/features/visit/VisitPanel.tsx"
}
```

> TOOL

tool_result
id: toolu_01T8TUJ37rqB3GkZzioojoWt
```
1	import { useEffect, useRef, useState } from 'react';
2	import { useQueryClient } from '@tanstack/react-query';
3	import {
4	  AlertCircle,
5	  ArrowLeft,
6	  Ban,
7	  CheckCircle2,
8	  Clock,
9	  DoorOpen,
10	  ExternalLink,
11	  Eye,
12	  Link2,
13	  LogIn,
14	  RefreshCw,
15	} from 'lucide-react';
16	import {
17	  Button,
18	  Card,
19	  IconButton,
20	  Logo,
21	  SelectField,
22	  Skeleton,
23	} from '@/design/components';
24	import {
25	  ACTIVE_EID_KEY,
26	  ACTIVE_SNAPSHOT_KEY,
27	  REFRESH_ACTIVE,
28	  RpcError,
29	  rpc,
30	} from '@/lib/messaging';
31	import { MAGIC_ADDRESS } from '@/lib/config';
32	import type { PreviewResponse } from '@/lib/types';
33	import {
34	  useActiveEid,
35	  useActiveSnapshot,
36	  useAuthStatus,
37	  useCancelEvent,
38	  useDraft,
39	  usePatchDraft,
40	  usePreview,
41	  useResolveEvent,
42	  useResolveGuestNames,
43	  useSend,
44	  useSignIn,
45	  useVisitorEvents,
46	} from './hooks';
47	import { AccountMenu } from './AccountMenu';
48	import { EmptyState } from './EmptyState';
49	import { RosterRow } from './RosterRow';
50	import { PreviewSheet } from './PreviewSheet';
51	import { SignInGate } from './SignInGate';
52	
53	const isAuthError = (err: unknown) => err instanceof RpcError && !!err.needsAuth;
54	
55	export function VisitPanel() {
56	  // `storedEid` is what the content script is pointing us at (auto-follow). We
57 […]

> TOOL

tool_use Read
id: toolu_01MGKgxxyZxdzJN55GgS57iK
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/lib/people.ts"
}
```

> TOOL

tool_result
id: toolu_01MGKgxxyZxdzJN55GgS57iK
```
1	/**
2	 * People API name + photo resolution (background only).
3	 *
4	 * Why: Google omits `attendee.displayName` for external non-contact guests — the
5	 * name Calendar's web UI shows is resolved client-side from the host's Google
6	 * Contacts and never reaches the event API. We replicate that with the host's own
7	 * `access_token` (the same client-side pattern the Calendar add-on uses), so the
8	 * side panel can upgrade a guest's email-derived fallback name (and show a profile
9	 * photo) with no backend round-trip.
10	 *
11	 * Needs contacts.readonly + contacts.other.readonly on the OAuth consent (see
12	 * lib/auth SCOPES). Resolves only emails the host has saved or interacted with —
13	 * fails gracefully (returns nothing) for everyone else. Never throws.
14	 */
15	import type { ResolvedPerson } from './types';
16	
17	const PEOPLE_BASE = 'https://people.googleapis.com/v1';
18	const CACHE_KEY = 'auxilio.peopleCache';
19	const CACHE_VERSION_KEY = 'auxilio.peopleCacheV';
20	/** Bump to drop the persisted cache on next load. v2 = discard caches written by the
21	 *  pre-fix code that stored lookup ERRORS as a 7-day "not found" (poisoning
22	 *  resolution for a week after a […]

> TOOL

tool_use Read
id: toolu_01FNfUZJtB71k1Ycq5RGY1Zd
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/lib/messaging.ts"
}
```

> TOOL

tool_result
id: toolu_01FNfUZJtB71k1Ycq5RGY1Zd
```
1	/**
2	 * Typed RPC over chrome.runtime messaging. The side panel (and content script)
3	 * never touch tokens or the network directly — they send these messages and the
4	 * background worker does the work. This keeps the thin-adapter boundary: one
5	 * place holds secrets + network.
6	 */
7	import type {
8	  ActiveEvent,
9	  AuthStatus,
10	  DomEventSnapshot,
11	  DraftPatch,
12	  DraftResponse,
13	  EventState,
14	  PanelVisitorEvent,
15	  PreviewResponse,
16	  ResolvedPerson,
17	  SendResponse,
18	  VisitDraft,
19	  VisitorEventSummary,
20	} from './types';
21	
22	export type RpcRequest =
23	  | { type: 'AUTH_STATUS' }
24	  | { type: 'AUTH_SIGN_IN' }
25	  | { type: 'AUTH_SIGN_OUT' }
26	  | { type: 'OPEN_PANEL' }
27	  | { type: 'OPEN_FOR_EVENT'; eid: string; snapshot?: DomEventSnapshot }
28	  | { type: 'FOLLOW_EVENT'; eid: string; snapshot?: DomEventSnapshot }
29	  | { type: 'RESOLVE_EVENT'; eid: string }
30	  | { type: 'DRAFT_LOAD'; event: ActiveEvent }
31	  | { type: 'RESOLVE_GUESTS'; emails: string[] }
32	  | { type: 'DRAFT_PATCH'; iCalUid: string; patch: DraftPatch }
33	  | { type: 'PREVIEW'; iCalUid: string; visitorEmail: string }
34	  | { type: 'SEND'; iCalUid: string; start?: string; end?: string }
35	  | { type: 'CANCEL_GUEST'; […]

> AGENT

Let me verify a few specifics: dead code, the QueryClient config, manifest, and `innerText` usage in hot paths.

> TOOL

tool_use Bash
id: toolu_019r4kevka4gSATsPNu9MiiP
```json
{
  "command": "echo \"=== usage of suspect helpers ===\" && grep -rn \"scrollContainer\\|mainVerticalList\\|shieldPadding\\|firstIconLedRow\" entrypoints/ lib/ | grep -v \"function \" && echo \"=== innerText calls ===\" && grep -rn \"innerText\" entrypoints/ && echo \"=== console.* count in content+bg+sync ===\" && grep -c \"console\\.\" entrypoints/calendar.content.ts entrypoints/background.ts lib/calendar-sync.ts lib/calendar.ts"
}
```

> TOOL

tool_result
id: toolu_019r4kevka4gSATsPNu9MiiP
```
=== usage of suspect helpers ===
entrypoints/calendar.content.ts:1190:  const ref = firstIconLedRow(list);
entrypoints/calendar.content.ts:1299: * (findContentList / firstIconLedRow / firstTextLeft) — no CSS-class coupling.
=== innerText calls ===
entrypoints/calendar.content.ts:292:      const text = el.innerText || '';
entrypoints/calendar.content.ts:312:        heading?.innerText?.trim() ||
entrypoints/calendar.content.ts:800:  const text = (dialog.innerText || '').toLowerCase();
=== console.* count in content+bg+sync ===
lib/calendar-sync.ts:2
entrypoints/background.ts:12
lib/calendar.ts:4
entrypoints/calendar.content.ts:2
```

> TOOL

tool_use Read
id: toolu_012VhGBKCSFEQimtwCDtRwNA
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/entrypoints/sidepanel/main.tsx"
}
```

> TOOL

tool_use Read
id: toolu_01NMPnETyLf7mpFJFhTduptp
```json
{
  "file_path": "/home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension/wxt.config.ts"
}
```

> TOOL

tool_result
id: toolu_012VhGBKCSFEQimtwCDtRwNA
```
1	import React from 'react';
2	import ReactDOM from 'react-dom/client';
3	import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
4	import App from './App';
5	import { SIDEPANEL_PORT } from '@/lib/messaging';
6	import '@/design/global.css';
7	
8	// Tell the background this panel is open (it broadcasts to calendar tabs so the
9	// in-page button hides). The port auto-disconnects when the panel closes.
10	chrome.runtime.connect({ name: SIDEPANEL_PORT });
11	
12	// Server state lives in TanStack Query: optimistic toggles + background refetch.
13	const queryClient = new QueryClient({
14	  defaultOptions: {
15	    queries: { retry: 1, staleTime: 30_000, refetchOnWindowFocus: false },
16	  },
17	});
18	
19	ReactDOM.createRoot(document.getElementById('root')!).render(
20	  <React.StrictMode>
21	    <QueryClientProvider client={queryClient}>
22	      <App />
23	    </QueryClientProvider>
24	  </React.StrictMode>,
25	);
26	
```

> TOOL

tool_result
id: toolu_01NMPnETyLf7mpFJFhTduptp
```
1	import { readFileSync } from 'node:fs';
2	import { defineConfig } from 'wxt';
3	
4	// WXT inlines import.meta.env (the baked engine URL in lib/config.ts) from .env,
5	// but does NOT populate process.env — which this config reads to build the engine
6	// host_permission. Load WXT_ENGINE_URL from .env here so host_permission always
7	// matches the URL baked into the bundle. An inline `env WXT_ENGINE_URL=… ` still
8	// wins (we only fill when it's unset).
9	if (!process.env.WXT_ENGINE_URL) {
10	  try {
11	    const m = readFileSync(new URL('.env', import.meta.url), 'utf8')
12	      .match(/^\s*WXT_ENGINE_URL\s*=\s*(.+?)\s*$/m);
13	    if (m) process.env.WXT_ENGINE_URL = m[1].trim();
14	  } catch { /* no .env — fall back to the default below */ }
15	}
16	
17	// Engine host_permission is derived from the build-time engine URL so the
18	// published manifest only ever carries the engine it actually targets (no stale
19	// tunnel hosts). Prod: pass WXT_ENGINE_URL=<bifrost url>. Local dev against the
20	// reserved tunnel: WXT_ENGINE_URL=<ngrok url> npm run dev. Falls back to the
21	// deployed bifrost dev engine when unset.
22	const ENGINE_URL = (
23	  process.env.WXT_ENGINE_URL ?? 'https://ops-engine-dev-330299.bifrost.saastack.site'
24	).replace(/\/$/, '');
25	const ENGINE_HOST […]

> AGENT

Let me confirm the unused helpers are truly dead and check the people-cache write pattern and `runSync` concurrency once more.

> TOOL

tool_use Bash
id: toolu_01GYiEKidaV56j2H6NLnAPYd
```json
{
  "command": "cd /home/<USER>/work/OfficeOperationsUmbrella/auxilio-extension\necho \"=== callers of possibly-dead helpers (excluding their own definitions/comments) ===\"\nfor fn in scrollContainer mainVerticalList shieldPadding stacksVertically; do\n  n=$(grep -rn \"\\b$fn\\b\" entrypoints/ lib/ | grep -v \"function $fn\" | grep -v \"^\\s*\\*\" | wc -l | tr -d ' ')\n  echo \"$fn: $n reference(s) outside its definition\"\ndone\necho \"=== getComputedStyle / getBoundingClientRect / getClientRects counts (content script) ===\"\ngrep -c \"getComputedStyle\" entrypoints/calendar.content.ts\ngrep -c \"getBoundingClientRect\\|getClientRects\" entrypoints/calendar.content.ts\necho \"=== version ===\"\ngrep '\"version\"' package.json"
}
```

> TOOL

tool_result
id: toolu_01GYiEKidaV56j2H6NLnAPYd
```
=== callers of possibly-dead helpers (excluding their own definitions/comments) ===
scrollContainer: 0 reference(s) outside its definition
mainVerticalList: 0 reference(s) outside its definition
shieldPadding: 0 reference(s) outside its definition
stacksVertically: 1 reference(s) outside its definition
=== getComputedStyle / getBoundingClientRect / getClientRects counts (content script) ===
7
18
=== version ===
  "version": "0.14.1",
```

> AGENT

I've now read the full extension — content script (1843 lines), background worker, sync engine, calendar/auth/people libs, and the side-panel React app. Here is the detailed report.

---

# Performance & Resource Audit — `auxilio-extension` (v0.14.1)

## Scope and method
I read every runtime file: the content script that runs on `calendar.google.com` (`entrypoints/calendar.content.ts`), the MV3 service worker (`entrypoints/background.ts`), the sync engine (`lib/calendar-sync.ts`, `lib/calendar.ts`), auth/people libs, and the side-panel React app (`features/visit/*`, `lib/*`). The content script is by far the highest-risk surface because it lives inside Google Calendar — a heavy, constantly-mutating SPA — so most findings concentrate there.

**Overall:** the code is defensively written (sync coalescing, burst caps, throttles, bounded 90-day window, TTL'd caches, orphan-context guards). There is **no catastrophic leak or runaway loop**. But there are a handful of real, fixable hot paths — one of which (full-page `innerText` on a timer) will cause noticeable jank on the low-end Android-class hardware your constraints target, and a lot of avoidable steady-state work.

---

## HIGH severity

### H1 — Full-page `document.body.innerText` on a recurring timer while editing an event
`entrypoints/calendar.content.ts`

- `readSurface()` returns `{ el: document.body, eid }` for the URL-eid case and the full-screen editor case (`calendar.content.ts:282` and `:287`). […]