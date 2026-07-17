> SYSTEM

# AGENTS.md instructions for /home/<USER>/Projects/yyork

<INSTRUCTIONS>
General instructions: follow these all the time.
- whenever you are unaware of what a particular cli option does, refer to the man page or use the --help option to learn its behaviour but never assume based on typical examples of its use.

--- project-doc ---

# Agent workflow

- User will assign one PRD at a time to an agent to implement. All the PRDs are available in the `./prds` dir.
- At any time if you think you could do a better job if a CLI tool was available to you and it would take you lesser tokens to do the task in presence of that tool, explicitly ask user to install it. Do not install it directly on your own as there are security related issues regarding this way of installation.

</INSTRUCTIONS>
<environment_context>
  <cwd>/home/<USER>/Projects/yyork</cwd>
  <shell>zsh</shell>
  <current_date>2026-06-09</current_date>
  <timezone>Asia/Kolkata</timezone>
  <filesystem><workspace_roots><root>/home/<USER>/Projects/yyork</root></workspace_roots><permission_profile type="disabled"><file_system type="unrestricted" /></permission_profile></filesystem>
</environment_context>

> DEVELOPER

# Context from my IDE setup:

## Active file: package.json

## Open tabs:
- package.json: package.json
- portless.json: portless.json
- dashboard.go: dashboard.go
- .gitkeep: cmd/yyork/dashboard/.gitkeep
- .gitignore: .gitignore

## My request for Codex:
https://https-yyork-localhost-preview.yyork.localhost/terminal/5pcyw3

why does yyork's preview url has this: `https-` prefix?

I was also thinking about what if there are 2 agents working on diff worktrees, made some changes and user would like to see the preview of the code changes. What it would do?

so for that something like `https://{sessionId}-{projectName}-preview.yyork.localhost` would be awesome and distinguishing enough.

> AGENT

I’ll trace where that preview host is constructed and how portless is interpreting it, then I’ll separate confirmed behavior from the naming/design implication for multiple worktrees.

> TOOL

tool_use exec_command
id: call_uuqLO9GkhymjdC5Lz7ZCXikD
```json
{
  "cmd": "rg -n \"https-|preview|portless|yyork\\.localhost|localhost-preview|sessionId|projectName\" .",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_mIu6T4U3tOKjSTQf6EdphIE4
```json
{
  "cmd": "rg -n \"preview|portless|yyork\\.localhost|localhost-preview\" /home/<USER>/.codex/memories/MEMORY.md",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_FxinznBYTDsayN7nTJDGqqC2
```json
{
  "cmd": "sed -n '1,220p' portless.json",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_C3kr87pzS6kj6g02TId0wGxg
```json
{
  "cmd": "sed -n '1,220p' package.json",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_uuqLO9GkhymjdC5Lz7ZCXikD
```
Chunk ID: c93742
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 13116
Output:
Total output lines: 503

./package.json:44:    "dev": "portless run",
./package.json:76:    "portless": "0.14.0"
./package.json:81:  "portless": {
./prds/canvas/BROWSER_PLAN.md:4:Canvas Browser tab into a VS Code Simple Browser-style local preview surface.
./prds/canvas/BROWSER_PLAN.md:8:yyork Browser supports local development previews only:
./prds/canvas/BROWSER_PLAN.md:10:- `https://yyork.localhost` and other `*.localhost` portless previews.
./prds/canvas/BROWSER_PLAN.md:20:Browser tab should be a live iframe surface with local-preview instrumentation.
./prds/canvas/BROWSER_PLAN.md:24:- Annotation and preview instrumentation must be vendored with yyork. User
./prds/canvas/BROWSER_PLAN.md:25:  preview apps must not install yyork, Agentation, or any annotation dependency.
./prds/canvas/BROWSER_PLAN.md:46:- `microsoft/vscode/extensions/simple-browser/preview-src/index.ts`
./prds/canvas/BROWSER_PLAN.md:53:  - `web/src/features/home/<USER>/molecules/canvas-web-preview.tsx`
./prds/canvas/BROWSER_PLAN.md:54:  - `web/src/features/home/<USER>/browser-preview.ts`
./prds/canvas/BROWSER_PLAN.md:55:  - `web/src/features/home/<USER>/browser-preview.unit.spec.ts`
./prds/canvas/BROWSER_PLAN.md:63:- Live iframe preview exists.
./prds/canvas/BROWSER_PLAN.md:67:  `https://yyork.localhost`.
./prds/canvas/BROWSER_PLAN.md:74:- History is React-local and does not know about SPA navigation inside previews.
./prds/canvas/BROWSER_PLAN.md:91:- Copy: the Browser surface is an iframe-based preview, not a screenshot stream.
./prds/canvas/BROWSER_PLAN.md:94:- Copy: use one active preview model instead of creating duplicate Browser
./prds/canvas/BROWSER_PLAN.md:97:  local preview usability.
./prds/canvas/BROWSER_PLAN.md:100:- Adapt: yyork also supports `*.localhost` for portless previews.
./prds/canvas/BROWSER_PLAN.md:104:  remains local/portless-preview-only.
./prds/canvas/BROWSER_PLAN.md:105:- Reject: VS Code's reload behavior that mutates the preview URL with request-id
./prds/canvas/BROWSER_PLAN.md:110:  capture/history state so agents can reason about preview interactions.
./prds/canvas/BROWSER_PLAN.md:140:- [x] Browser tab still dogfoods `https://yyork.localhost`.
./prds/canvas/BROWSER_PLAN.md:146:- [x] Normalize […]

> TOOL

tool_result
id: call_mIu6T4U3tOKjSTQf6EdphIE4
```
Chunk ID: f4723e
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2069
Output:
1:# Task Group: `Projects/yyork` in-app browser readiness, Agentation delivery, portless routing, and bundled Browser plugin internals [chronicle memory]
2:scope: Use for recent `yyork` work around the Browser tab/IAB path, Agentation annotation delivery, portless-backed local routing, and local inspection of Codex’s bundled Browser plugin files when the user is tracing the real control path or debugging why preview behavior differs from the expected proxied app.
3:applies_to: cwd=/home/<USER>/Projects/yyork plus local Browser-plugin cache paths under /home/<USER>/.codex/plugins/cache/openai-bundled/browser/*; reuse_rule=safe for similar yyork browser-preview and local Browser-plugin forensics on this machine, but re-open the current `yyork` dev scripts, preview host wiring, and installed plugin version before claiming exact runtime behavior
26:- Agentation, annotations.go, canvas-web-preview.tsx, annotations.ts, internal/durabilityprovider/send.go, internal/durabilityprovider/zellij.go, staged annotations, batch delivery, markdown user message, Send to agent, severity, intent, selectedText, elementPath [chronicle memory]
28:## Task 3: Assess IAB end-to-end readiness and debug missing Agentation in the Browser preview [chronicle memory]
32:- extensions/chronicle/resources/2026-06-09T03-26-00-AQhM-10min-memory-summary.md (cwd=/home/<USER>/Projects/yyork, rollout_path=/home/<USER>/.codex/memories/extensions/chronicle/resources/2026-06-09T03-26-00-AQhM-10min-memory-summary.md, updated_at=2026-06-09T03:26:00+00:00, thread_id=None, portless-backed route shape, stale raw listener cleanup, missing preview asset, and dev-mode patch direction) [chronicle memory]
33:- extensions/chronicle/resources/2026-06-09T03-16-00-bOOV-10min-memory-summary.md (cwd=/home/<USER>/Projects/yyork, rollout_path=/home/<USER>/.codex/memories/extensions/chronicle/resources/2026-06-09T03-16-00-bOOV-10min-memory-summary.md, updated_at=2026-06-09T03:16:00+00:00, thread_id=None, stale server/proxy diagnosis, `508 LOOP DETECTED`, and […]

> TOOL

tool_result
id: call_FxinznBYTDsayN7nTJDGqqC2
```
Chunk ID: cdf4d6
Wall time: 0.0000 seconds
Process exited with code 1
Original token count: 12
Output:
sed: portless.json: No such file or directory

```

> TOOL

tool_result
id: call_C3kr87pzS6kj6g02TId0wGxg
```
Chunk ID: 1274e7
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 852
Output:
{
  "name": "@yyopc/yyork",
  "version": "0.0.1",
  "private": false,
  "description": "Agent routing platform with an interface to the agent router.",
  "homepage": "https://github.com/yyopc/yyork#readme",
  "bugs": {
    "url": "https://github.com/yyopc/yyork/issues"
  },
  "license": "MIT",
  "author": {
    "name": "yyopc",
    "email": "<REDACTED_EMAIL>",
    "url": "https://github.com/yyopc"
  },
  "repository": {
    "type": "git",
    "url": "git+https://github.com/yyopc/yyork.git"
  },
  "bin": {
    "yyork": "./bin/yyork.mjs"
  },
  "files": [
    "dashboard.go",
    "main.go",
    "go.mod",
    "go.sum",
    "cmd/yyork/dashboard/**",
    "internal/**/*.go",
    "internal/store/migrations/*.sql",
    "bin/yyork.mjs",
    "bin/install-yyork.mjs"
  ],
  "publishConfig": {
    "access": "public"
  },
  "type": "module",
  "scripts": {
    "prepare": "pnpm --filter @yyork/web exec lefthook install --force || true",
    "prepack": "pnpm web:build",
    "postinstall": "node ./bin/install-yyork.mjs",
    "api:generate": "go run ./api/generate-workspace-contract.go",
    "yyork": "go run .",
    "dev": "portless run",
    "dev:app": "go run . dev",
    "web:dev": "pnpm --filter @yyork/web dev",
    "web:build": "pnpm --filter @yyork/web build",
    "web:lint": "pnpm --filter @yyork/web lint",
    "web:test": "pnpm --filter @yyork/web test:ci",
    "backend:build": "pnpm web:build && go build -o ./yyork .",
    "backend:test": "go test ./...",
    "build": "pnpm web:build && pnpm backend:build",
    "lint": "pnpm backend:test && pnpm web:lint",
    "lint:ts": "pnpm --filter @yyork/web lint:ts",
    "test": "pnpm backend:test && pnpm web:test",
    "test:ci": "pnpm --filter @yyork/web test:ci",
    "e2e": "pnpm --filter @yyork/web e2e",
    "e2e:live-terminal": "pnpm --dir web e2e:live-terminal",
    "e2e:live-terminal:reconnect": "pnpm --dir web e2e:live-terminal:reconnect",
    "e2e:live-terminal:soak": "pnpm […]

> AGENT

I found the relevant server path: `POST /api/browser-preview/targets` registers a synthetic `*-preview.yyork.localhost` host, and the current suspicious name looks generated from the target origin rather than a session-specific identity. I’m reading that host builder now.

> TOOL

tool_use exec_command
id: call_bgXzPTotQabrA50uKD2YaM4L
```json
{
  "cmd": "sed -n '1,380p' internal/server/browser_preview.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 24000
}
```

> TOOL

tool_use exec_command
id: call_qSm5O6PPPzOrsuNP1TGa72RI
```json
{
  "cmd": "sed -n '380,620p' internal/server/browser_preview.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_KlUQI1sqRylztgOdKZO8j45g
```json
{
  "cmd": "sed -n '1,240p' internal/server/browser_preview_test.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_NbYzOKEPvBKKROcVgfXn3UAp
```json
{
  "cmd": "sed -n '180,230p' web/src/features/home/<USER>/organisms/canvas-panel.tsx && sed -n '520,650p' web/src/features/home/<USER>/molecules/canvas-web-preview.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_bgXzPTotQabrA50uKD2YaM4L
```
Chunk ID: 2a561e
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2776
Output:
package server

import (
	"bytes"
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"mime"
	"net"
	"net/http"
	"net/url"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

const (
	browserPreviewAgentationPath = "/__yyork_browser/agentation.js"
	browserPreviewBridgePath     = "/__yyork_browser/preview-bridge.js"
	browserPreviewHostSuffix     = "-preview.yyork.localhost"
)

var browserPreviewSlugChars = regexp.MustCompile(`[^a-z0-9]+`)

type browserPreviewTargetRequest struct {
	PreviewName string `json:"previewName"`
	URL         string `json:"url"`
}

type browserPreviewTargetResponse struct {
	PreviewURL string `json:"previewUrl"`
	TargetURL  string `json:"targetUrl"`
}

func (s *Server) handleBrowserPreviewTarget(w http.ResponseWriter, r *http.Request) {
	var payload browserPreviewTargetRequest
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "invalid preview target payload", http.StatusBadRequest)
		return
	}

	targetURL, err := parseBrowserPreviewTargetURL(payload.URL)
	if err != nil {
		http.Error(w, err.Error(), http.StatusUnprocessableEntity)
		return
	}

	targetOrigin := browserPreviewOrigin(targetURL)
	previewHost := browserPreviewHostForTarget(r, payload.PreviewName, targetOrigin)
	s.setBrowserPreviewTarget(previewHost, targetOrigin)

	writeJSON(w, http.StatusOK, browserPreviewTargetResponse{
		PreviewURL: browserPreviewURLForTarget(r, previewHost, targetURL),
		TargetURL:  targetURL.String(),
	})
}

func (s *Server) handleBrowserPreview(w http.ResponseWriter, r *http.Request) {
	if r.URL.Path == browserPreviewBridgePath {
		serveBrowserPreviewBridge(w)
		return
	}
	if r.URL.Path == browserPreviewAgentationPath {
		s.serveBrowserPreviewDashboardAsset(w, r, strings.TrimPrefix(browserPreviewAgentationPath, "/"))
		return
	}

	previewHost := normalizedRequestHostname(externalRequestHost(r))
	targetOrigin, ok := s.browserPreviewTarget(previewHost)
	if !ok {
		http.Error(w, "preview target not registered", http.StatusNotFound)
		return
	}

	upstreamURL := *targetOrigin
	upstreamURL.Path = r.URL.Path
	upstreamURL.RawPath = r.URL.RawPath
	upstreamURL.RawQuery = r.URL.RawQuery […]

> TOOL

tool_result
id: call_qSm5O6PPPzOrsuNP1TGa72RI
```
Chunk ID: 0a6e24
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1657
Output:
		proto, _, _ := strings.Cut(forwardedProto, ",")
		proto = strings.ToLower(strings.TrimSpace(proto))
		if proto == "http" || proto == "https" {
			return proto
		}
	}
	if r.TLS != nil {
		return "https"
	}
	if r.URL.Scheme == "http" || r.URL.Scheme == "https" {
		return r.URL.Scheme
	}
	return "http"
}

func browserPreviewHTTPClient() *http.Client {
	transport := http.DefaultTransport.(*http.Transport).Clone()
	transport.Proxy = nil
	return &http.Client{
		Transport: transport,
		CheckRedirect: func(_ *http.Request, _ []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}
}

func copyBrowserPreviewRequestHeaders(dst http.Header, src http.Header) {
	for key, values := range src {
		if skipBrowserPreviewRequestHeader(key) {
			continue
		}
		for _, value := range values {
			dst.Add(key, value)
		}
	}
}

func skipBrowserPreviewRequestHeader(key string) bool {
	switch strings.ToLower(key) {
	case "accept-encoding", "host", "x-forwarded-host", "x-forwarded-proto":
		return true
	default:
		return false
	}
}

func copyBrowserPreviewResponseHeaders(dst http.Header, src http.Header) {
	for key, values := range src {
		if skipBrowserPreviewResponseHeader(key) {
			continue
		}
		for _, value := range values {
			dst.Add(key, value)
		}
	}
}

func skipBrowserPreviewResponseHeader(key string) bool {
	switch strings.ToLower(key) {
	case "content-length", "content-encoding":
		return true
	default:
		return false
	}
}

func removeBrowserPreviewInjectionHeaders(headers http.Header) {
	headers.Del("Content-Security-Policy")
	headers.Del("Content-Security-Policy-Report-Only")
	headers.Del("Integrity-Policy")
	headers.Del("Integrity-Policy-Report-Only")
}

func […]

> TOOL

tool_result
id: call_KlUQI1sqRylztgOdKZO8j45g
```
Chunk ID: 1a78dd
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 2155
Output:
package server

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"testing/fstest"
)

func TestBrowserPreviewTargetRegistrationRejectsExternalHosts(t *testing.T) {
	server := New(Config{})
	request := httptest.NewRequest(
		http.MethodPost,
		"/api/browser-preview/targets",
		strings.NewReader(`{"url":"https://google.com"}`),
	)
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusUnprocessableEntity {
		t.Fatalf("expected external preview target to be rejected, got %d", response.Code)
	}
}

func TestBrowserPreviewTargetRegistrationRejectsPreviewHosts(t *testing.T) {
	server := New(Config{})
	request := httptest.NewRequest(
		http.MethodPost,
		"/api/browser-preview/targets",
		strings.NewReader(`{"url":"https://yyork-preview.yyork.localhost/"}`),
	)
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusUnprocessableEntity {
		t.Fatalf("expected preview target host to be rejected, got %d", response.Code)
	}
}

func TestBrowserPreviewTargetRegistrationUsesPreviewName(t *testing.T) {
	server := New(Config{})
	request := httptest.NewRequest(
		http.MethodPost,
		"http://127.0.0.1:4217/api/browser-preview/targets",
		strings.NewReader(`{"url":"http://localhost:3000/app","previewName":"yyork"}`),
	)
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("register preview target failed with %d: %s", response.Code, response.Body.String())
	}

	var payload browserPreviewTargetResponse
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		t.Fatalf("decode preview target response: %v", err)
	}
	if payload.PreviewURL != "http://yyork-preview.yyork.localhost:4217/app" {
		t.Fatalf("expected named preview URL, got %q", payload.PreviewURL)
	}
}

func TestBrowserPreviewTargetRegistrationUsesYyorkSelfPreviewName(t *testing.T) {
	server := New(Config{})
	request := httptest.NewRequest(
		http.MethodPost,
		"https://yyork.localhost/api/browser-preview/targets",
		strings.NewReader(`{"url":"https://yyork.localhost/board/demo"}`),
	)
	request.Header.Set("X-Forwarded-Proto", "https")
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("register preview target failed […]

> TOOL

tool_result
id: call_NbYzOKEPvBKKROcVgfXn3UAp
```
Chunk ID: 3498e1
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1386
Output:
      className="flex h-full min-h-0 w-full min-w-0 flex-col bg-background"
    >
      <Tabs
        value={props.activeTab}
        onValueChange={(value) => {
          if (isCanvasTab(value)) {
            props.onTabChange(value);
          }
        }}
        className="min-h-0 w-full flex-1 flex-col gap-0"
      >
        <TabsContent value="files" className="min-h-0 w-full overflow-hidden">
          <CanvasFilesPanel
            active={props.activeTab === 'files'}
            target={props.target}
          />
        </TabsContent>
        <TabsContent value="review" className="min-h-0 w-full overflow-hidden">
          <CanvasDiffView
            active={props.activeTab === 'review'}
            reviewPreferences={props.reviewPreferences}
            onReviewPreferencesChange={props.onReviewPreferencesChange}
            target={props.target}
          />
        </TabsContent>
        <TabsContent value="browser" className="min-h-0 w-full overflow-hidden">
          <CanvasWebPreview
            defaultUrl={props.previewUrl}
            onUrlChange={props.onPreviewUrlChange}
            projectId={props.target.projectId}
            previewName={props.target.projectName}
            sessionId={props.target.sessionId}
          />
        </TabsContent>
      </Tabs>
    </aside>
  );
}

function CanvasFilesPanel(props: {
  active: boolean;
  target: CanvasTargetSummary;
}) {
  const [fileTreeOpen, setFileTreeOpen] = useState(true);
  const {
    data: filesData,
    error: filesError,
    isError: filesIsError,
    isPending: filesIsPending,
  } = useQuery(
    sessionFilesQueryOptions({
  return (
    <Tooltip>
      <TooltipTrigger
        render={
          <Toggle
            size={domEventsOpen ? 'sm' : 'icon-sm'}
            className={cn(
              'ms-auto rounded-sm font-normal shadow-none',
              domEventsOpen &&
                'border-positive-500/60 bg-positive-500/10 text-positive-500 hover:border-positive-500/70 hover:bg-positive-500/15 hover:text-positive-500 data-pressed:border-positive-500/60 data-pressed:bg-positive-500/10 data-pressed:text-positive-500'
            )}
            pressed={domEventsOpen}
            aria-label={tooltip}
            onPressedChange={setDomEventsOpen}
          />
        }
      >
        <SquareMousePointerIcon aria-hidden="true" data-icon="inline-start" />
        {domEventsOpen ? <span>{domEvents.length}</span> : null}
      </TooltipTrigger>
      <TooltipContent>
        <p>{tooltip}</p>
      </TooltipContent>
    </Tooltip>
  );
}

function BrowserViewport(props: {
  onAgentationMessage: (message: BrowserPreviewAgentationMessage) => void;
  onDOMEvent: (event: BrowserDomEvent) => void;
}) {
  const [frameState, setFrameState] = useState<{
    frameUrl: string;
    sourceUrl: string;
  }>({ frameUrl: '', sourceUrl: '' });
  const {
    currentUrl, […]

> AGENT

The `https-` itself is not Portless adding a protocol marker to the public host. In yyork’s code it is the fallback slug produced by `browserPreviewHostForOrigin`: scheme plus normalized host, so `https://yyork.localhost` becomes `https-yyork-localhost-preview.yyork.localhost` when no usable preview name/self-preview shortcut wins.

> TOOL

tool_use exec_command
id: call_IaBkTs7ObAoJbUYaMct9ma98
```json
{
  "cmd": "sed -n '1,180p' web/src/features/home/<USER>/molecules/canvas-web-preview.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_use exec_command
id: call_YbDcHEzeU6JAF9lQx7r1lNSw
```json
{
  "cmd": "sed -n '140,190p' web/src/features/home/<USER>/browser-preview.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_2MooGLXjp0cw9ZjuMamimZY1
```json
{
  "cmd": "sed -n '1,130p' web/src/features/home/<USER>/workspace-preferences.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_use exec_command
id: call_2CCzFr3akOlJivsrNv200dVl
```json
{
  "cmd": "sed -n '1,130p' internal/server/server.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_IaBkTs7ObAoJbUYaMct9ma98
```
Chunk ID: c1e534
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1199
Output:
import { useMutation } from '@tanstack/react-query';
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  CookieIcon,
  ExternalLinkIcon,
  HardDriveIcon,
  MoreVerticalIcon,
  RefreshCcwIcon,
  RotateCcwIcon,
  SendHorizontalIcon,
  SquareMousePointerIcon,
  Trash2Icon,
  XIcon,
} from 'lucide-react';
import {
  type ComponentProps,
  createContext,
  use,
  useEffect,
  useEffectEvent,
  useRef,
  useState,
} from 'react';
import { toast } from 'sonner';

import { cn } from '@/lib/tailwind/utils';

import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import { Toggle } from '@/components/ui/toggle';
import {
  Tooltip,
  TooltipContent,
  TooltipTrigger,
} from '@/components/ui/tooltip';

import {
  type AnnotationPayload,
  sendAnnotationsMutationOptions,
} from '@/features/home/<USER>/annotations';
import {
  type BrowserDomEvent,
  type BrowserPreviewAgentationMessage,
  type BrowserPreviewAnnotation,
  type BrowserPreviewMessage,
  type BrowserPreviewUrlResult,
  isBrowserPreviewMessage,
  registerBrowserPreviewTarget,
  validatePreviewUrlInput,
} from '@/features/home/<USER>/browser-preview';

interface WebPreviewContextValue {
  canGoBack: boolean;
  canGoForward: boolean;
  currentUrl: string;
  domEvents: BrowserDomEvent[];
  domEventsOpen: boolean;
  error: string | null;
  iframeKey: number;
  iframeRef: React.RefObject<HTMLIFrameElement | null>;
  loading: boolean;
  navigateTo: (url: string) => void;
  previewName?: string;
  recordFrameNavigation: (url: string) => void;
  reloadPreview: (
    hard?: boolean,
    storageScope?: 'cache' | 'cookies' | 'all'
  ) => void;
  runHistory: (direction: 'back' | 'forward') => void;
  setDomEventsOpen: (open: boolean) => void;
  setError: (error: string | null) => void; […]

> TOOL

tool_result
id: call_YbDcHEzeU6JAF9lQx7r1lNSw
```
Chunk ID: 86e114
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 357
Output:
  const normalized = hostname.toLowerCase().replace(/^\[|\]$/g, '');
  return (
    normalized === 'localhost' ||
    normalized.endsWith('.localhost') ||
    normalized === '::1' ||
    normalized === '::' ||
    normalized === '0.0.0.0' ||
    normalized.startsWith('127.')
  );
}

export async function registerBrowserPreviewTarget(
  url: string,
  options?: { previewName?: string; signal?: AbortSignal }
): Promise<BrowserPreviewTarget> {
  const response = await fetch('/api/browser-preview/targets', {
    body: JSON.stringify({ previewName: options?.previewName, url }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
    signal: options?.signal,
  });

  if (!response.ok) {
    throw new Error(
      (await response.text()) || 'Preview target registration failed.'
    );
  }

  return (await response.json()) as BrowserPreviewTarget;
}

export function isBrowserPreviewBridgeMessage(
  value: unknown
): value is BrowserPreviewBridgeMessage {
  if (!value || typeof value !== 'object') {
    return false;
  }

  const message = value as Record<string, unknown>;
  return (
    message.source === 'yyork-preview-bridge' &&
    typeof message.type === 'string' &&
    message.type.startsWith('yyork:')
  );
}

export function isBrowserPreviewAgentationMessage(
  value: unknown
): value is BrowserPreviewAgentationMessage {
  if (!value || typeof value !== 'object') {
    return false;

```

> TOOL

tool_result
id: call_2MooGLXjp0cw9ZjuMamimZY1
```
Chunk ID: bf2865
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 884
Output:
import { validatePreviewUrlInput } from '@/features/home/<USER>/browser-preview';
import { type CanvasTab, isCanvasTab } from '@/features/home/<USER>/canvas-tabs';
import {
  type WorkerSessionState,
  workerSessionStates,
} from '@/features/home/<USER>/session-workspace';

const homeWorkspacePreferencesStorageKey =
  'yyork.home.workspace-preferences';
const homeWorkspacePreferencesVersion = 1;

export interface HomeWorkspacePreferences {
  canvasLayout?: HomeWorkspaceCanvasLayout;
  canvasOpen: boolean;
  canvasPreviewUrls?: Record<string, string>;
  canvasPreviewUrl?: string;
  canvasReview?: HomeWorkspaceCanvasReviewPreferences;
  canvasTab?: CanvasTab;
  hiddenProjectIds?: string[];
  hiddenTerminalSessionKeys?: string[];
  openProjectIds?: string[];
  openWorkerSessionGroupIds?: WorkerSessionState[];
  pinnedProjectIds?: string[];
  pinnedTerminalSessionKeys?: string[];
  projectNameOverrides?: Record<string, string>;
  sidebarOpen: boolean;
  sidebarWidth?: number;
  skipStopSessionConfirmation?: boolean;
}

export interface HomeWorkspaceCanvasLayout {
  canvas: number;
  main: number;
}

export type HomeWorkspaceCanvasReviewDiffLayout = 'split' | 'stacked';

export interface HomeWorkspaceCanvasReviewPreferences {
  diffLayout?: HomeWorkspaceCanvasReviewDiffLayout;
  wrapLines?: boolean;
}

export type CanvasPreviewTargetSummary = {
  cwd?: string;
  projectId?: string;
  sessionId?: string;
};

interface StoredHomeWorkspacePreferences extends Partial<HomeWorkspacePreferences> {
  version?: number;
}

export const defaultHomeWorkspacePreferences: HomeWorkspacePreferences = {
  canvasOpen: false,
  sidebarOpen: false,
};

export function readHomeWorkspacePreferences(): HomeWorkspacePreferences {
  const storedValue = readStoredValue();

  if (!storedValue) {
    return defaultHomeWorkspacePreferences;
  }

  try {
    return normalizeHomeWorkspacePreferences(JSON.parse(storedValue));
  } catch {
    return defaultHomeWorkspacePreferences;
  }
}

export function writeHomeWorkspacePreferences(
  preferences: HomeWorkspacePreferences
) {
  if (typeof window === 'undefined') {
    return;
  }

  try {
    window.localStorage.setItem(
      homeWorkspacePreferencesStorageKey,
      JSON.stringify({
        ...normalizeHomeWorkspacePreferences(preferences),
        version: homeWorkspacePreferencesVersion,
      })
    );
  } catch { […]

> TOOL

tool_result
id: call_2CCzFr3akOlJivsrNv200dVl
```
Chunk ID: c5dcb6
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 931
Output:
package server

import (
	"context"
	"encoding/json"
	"errors"
	"fmt"
	"io/fs"
	"net"
	"net/http"
	"net/url"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strconv"
	"strings"
	"sync"

	"github.com/yyopc/yyork/internal/durabilityprovider"
	"github.com/yyopc/yyork/internal/events"
	"github.com/yyopc/yyork/internal/plugin"
	"github.com/yyopc/yyork/internal/session"
	"github.com/yyopc/yyork/internal/store"
	"github.com/yyopc/yyork/internal/terminal"
)

// SessionStopper terminates a running session. The session.Engine satisfies
// this interface; the server depends on the narrow surface to keep the
// dependency one-directional.
type SessionStopper interface {
	Stop(ctx context.Context, id string) error
}

type Config struct {
	IDEOpener       IDEOpener
	Registry        *plugin.Registry
	TerminalManager *terminal.Manager

	// WebDir is a filesystem path to serve the dashboard from (dev mode).
	// Takes priority over WebFS when both are set.
	WebDir string

	// WebFS is an embedded dashboard filesystem (single-binary mode).
	// Used when WebDir is empty.
	WebFS fs.FS

	Workspace           session.Workspace
	WorkspaceSource     WorkspaceSource
	DurabilityProviders *durabilityprovider.Registry

	// Sessions is the SQLite-backed session repository the new
	// /api/sessions endpoint reads from. Optional — if nil, the endpoint
	// returns an empty list.
	Sessions store.SessionRepo

	// Stopper terminates a session by id. When set, the dashboard can stop
	// sessions via DELETE /api/sessions/{sessionID}. Optional — if nil, the
	// endpoint returns 501.
	Stopper SessionStopper

	// EventBus is the in-process […]

> AGENT

There’s also a front-end detail: the Browser panel only sends `previewName={projectName}` today. It does not send the selected `sessionId`, even though preview URL preferences are already scoped by `projectId + sessionId`.

> TOOL

tool_use exec_command
id: call_6hlAXVi0UfbjvMXh4FUS9E1H
```json
{
  "cmd": "sed -n '130,190p' internal/server/server.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_2MWvlUTSxrRq1kYjuHxWtyRu
```json
{
  "cmd": "sed -n '420,470p' internal/server/server.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_RQZntDMFaVKJJpPLrdVjIexL
```json
{
  "cmd": "sed -n '130,175p' prds/canvas/BROWSER_PLAN.md",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 10000
}
```

> TOOL

tool_use exec_command
id: call_PinAYnK5cCgWvWBLTf7cXfN9
```json
{
  "cmd": "sed -n '245,260p' prds/canvas/BROWSER_PLAN.md",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 10000
}
```

> TOOL

tool_result
id: call_6hlAXVi0UfbjvMXh4FUS9E1H
```
Chunk ID: 2fcbf1
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 571
Output:
		stopper:             cfg.Stopper,
		eventBus:            cfg.EventBus,
		controlToken:        cfg.ControlToken,
		previewTargets:      map[string]*url.URL{},
	}
}

func (s *Server) Handler() http.Handler {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/health", s.handleHealth)
	mux.HandleFunc("GET /api/plugins", s.handlePlugins)
	mux.HandleFunc("GET /api/workspace", s.handleWorkspace)
	mux.HandleFunc("POST /api/projects/{projectID}/ide", s.handleProjectIDE)
	mux.HandleFunc("POST /api/sessions/{sessionID}/ide", s.handleSessionIDE)
	mux.HandleFunc("GET /api/sessions/{sessionID}/files", s.handleSessionFiles)
	mux.HandleFunc("GET /api/sessions/{sessionID}/files/content", s.handleSessionFileContent)
	mux.HandleFunc("GET /api/sessions/{sessionID}/canvas/diff", s.handleSessionCanvasDiff)
	mux.HandleFunc("GET /api/sessions/{sessionID}/terminal", s.handleSessionTerminal)
	mux.HandleFunc("POST /api/annotations/{sessionID}", s.handleAnnotations)
	mux.HandleFunc("POST /api/browser-preview/targets", s.handleBrowserPreviewTarget)
	mux.HandleFunc("GET /api/sessions", s.handleListSessions)
	mux.HandleFunc("PATCH /api/sessions/{sessionID}", s.handleRenameSession)
	mux.HandleFunc("DELETE /api/sessions/{sessionID}", s.handleStopSession)
	mux.HandleFunc("GET /api/events", s.handleEventsStream)
	mux.HandleFunc("POST /api/events", s.handlePublishEvent)
	mux.HandleFunc("/", s.handleDashboard)
	return mux
}

func (s *Server) Close() error {
	return s.terminalManager.Close()
}

func (s *Server) handleHealth(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, map[string]string{
		"status": "ok",
	})
}

func (s *Server) handlePlugins(w http.ResponseWriter, _ *http.Request) {
	writeJSON(w, http.StatusOK, s.registry.Manifests())
}

func (s *Server) handleWorkspace(w http.ResponseWriter, r *http.Request) {
	workspace, err := s.workspaceForRequest(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	writeJSON(w, http.StatusOK, workspace)
}

func (s *Server) handleProjectIDE(w http.ResponseWriter, r *http.Request) {
	projectID := r.PathValue("projectID")
	workspace, err := s.workspaceForRequest(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}


```

> TOOL

tool_result
id: call_2MWvlUTSxrRq1kYjuHxWtyRu
```
Chunk ID: 2c3621
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 373
Output:
			return host
		}
	}

	return r.Host
}

func isAPIHost(host string) bool {
	hostname := host
	if parsedHost, _, err := net.SplitHostPort(host); err == nil {
		hostname = parsedHost
	}
	hostname = strings.ToLower(strings.TrimSuffix(hostname, "."))
	return hostname == "api.yyork.localhost"
}

// serveSPA serves static assets from fsys with SPA-style fallback: any
// request whose path doesn't resolve to a real file returns index.html, so
// client-side routes like /board/<id> work on direct navigation and reload.
//
// We use http.ServeFileFS rather than http.FileServer because the latter
// has automatic directory-redirect behavior that rewrites `/index.html`
// to `./` (a 301), which is exactly the wrong thing for a SPA root.
func (s *Server) serveSPA(w http.ResponseWriter, r *http.Request, fsys fs.FS) {
	name := strings.TrimPrefix(r.URL.Path, "/")
	if name == "" {
		name = "index.html"
	}
	if _, err := fs.Stat(fsys, name); err != nil {
		// Unknown path → let the SPA router handle it client-side.
		name = "index.html"
	}
	http.ServeFileFS(w, r, fsys, name)
}

func writeJSON(w http.ResponseWriter, status int, value any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(value)
}

func parsePositiveInt(value string, fallback […]

> TOOL

tool_result
id: call_RQZntDMFaVKJJpPLrdVjIexL
```
Chunk ID: 81262b
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 541
Output:
  are no longer registered.
- The untracked CDP/headless files `internal/server/browser.go` and
  `internal/browser/manager.go` were removed from this checkout.
- No screenshot-specific Browser frontend tests existed in the current tree;
  the current Browser frontend tests cover local URL validation instead.

Acceptance:

- [x] `rg "browser snapshot|Browser viewport|screenshot|snapshot"` has no Browser
  UI path implying screenshots.
- [x] Browser tab still dogfoods `https://yyork.localhost`.
- [x] TypeScript and focused Browser tests pass.

### B2. Local Preview URL Model

- [x] Keep validation local-only.
- [x] Normalize local preview URLs without surprising protocol rewrites.
- [x] Preserve explicit `https://` input, especially `https://yyork.localhost`.
- [x] Reject arbitrary external hosts with a clear unsupported state.
- [x] Persist last Browser URL per Canvas target.
- [x] Add history seed from the persisted URL.

Implementation note:

- `workspace-preferences.ts` now stores Browser preview URLs in
  `canvasPreviewUrls`, keyed by Canvas target:
  `session:<projectId>:<sessionId>`, `project:<projectId>`, or `cwd:<cwd>`.
- The active Canvas tab is stored in `canvasTab`, so selecting Browser survives
  Canvas close/reopen and yyork page refresh.
- The old `canvasPreviewUrl` field remains a read-only legacy fallback and is
  cleared by new Browser […]

> TOOL

tool_result
id: call_PinAYnK5cCgWvWBLTf7cXfN9
```
Chunk ID: 740cba
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 223
Output:
- [x] Block redirects to unsupported hosts.
- [x] Add clear error states for unsupported content or blocked redirects.

Implementation note:

- `POST /api/browser-preview/targets` registers a local-only target and returns
  a synthetic `*-preview.yyork.localhost` URL for the iframe.
- Preview registration accepts a yyork-owned `previewName`; project Browser
  tabs send the selected project name so URLs use the intended
  `appname-preview.yyork.localhost` shape instead of port-derived hostnames.
- yyork self-preview is special-cased to `yyork-preview.yyork.localhost`, both
  when yyork is reached through `yyork.localhost` and when the current dev
  process is reached through `127.0.0.1:<port>`.
- Preview-host requests are reverse-proxied server-side by yyork; HTML responses
  receive yyork-vendored bridge and Agentation scripts, and non-HTML responses
  pass through unchanged.

```

> AGENT

The PRD note matches the code’s intended behavior: named project previews should use `appname-preview.yyork.localhost`; yyork self-preview should use `yyork-preview.yyork.localhost`. So the exact URL you pasted suggests the request path skipped both of those named cases and fell back to origin-based slugging.

> TOOL

tool_use exec_command
id: call_K9mmKMCrvAl6KkNzFt6DWZVj
```json
{
  "cmd": "rg -n \"handleDashboard|isBrowserPreviewHost|externalRequestHost|X-Forwarded-Host|previewHost\" internal/server internal/cli web/src/features/home -g '!**/*.map'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 20000
}
```

> TOOL

tool_use exec_command
id: call_T9VMjEYgJFIg4uelrHLOAZah
```json
{
  "cmd": "sed -n '360,430p' internal/server/server.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_UnyJDeqbcFQgl3Bd4pw7TuwE
```json
{
  "cmd": "sed -n '1,220p' internal/cli/dev.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_7Tl7cMzAwsYjHDigXrYYltEF
```json
{
  "cmd": "find . -maxdepth 3 -name 'portless.json' -o -name '*.portless*'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 4000
}
```

> TOOL

tool_result
id: call_K9mmKMCrvAl6KkNzFt6DWZVj
```
Chunk ID: 9145ba
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 875
Output:
internal/server/server_test.go:67:	request.Header.Set("X-Forwarded-Host", "api.yyork.localhost")
internal/server/server.go:155:	mux.HandleFunc("/", s.handleDashboard)
internal/server/server.go:363:func (s *Server) handleDashboard(w http.ResponseWriter, r *http.Request) {
internal/server/server.go:364:	if isBrowserPreviewHost(externalRequestHost(r)) {
internal/server/server.go:369:	if isAPIHost(externalRequestHost(r)) {
internal/server/server.go:416:func externalRequestHost(r *http.Request) string {
internal/server/server.go:417:	if forwardedHost := r.Header.Get("X-Forwarded-Host"); forwardedHost != "" {
internal/server/browser_preview.go:55:	previewHost := browserPreviewHostForTarget(r, payload.PreviewName, targetOrigin)
internal/server/browser_preview.go:56:	s.setBrowserPreviewTarget(previewHost, targetOrigin)
internal/server/browser_preview.go:59:		PreviewURL: browserPreviewURLForTarget(r, previewHost, targetURL),
internal/server/browser_preview.go:74:	previewHost := normalizedRequestHostname(externalRequestHost(r))
internal/server/browser_preview.go:75:	targetOrigin, ok := s.browserPreviewTarget(previewHost)
internal/server/browser_preview.go:103:	upstreamRequest.Header.Set("X-Forwarded-Host", externalRequestHost(r))
internal/server/browser_preview.go:171:	internalRequest.Header.Del("X-Forwarded-Host")
internal/server/browser_preview.go:175:	s.handleDashboard(response, internalRequest)
internal/server/browser_preview.go:186:func (s *Server) setBrowserPreviewTarget(previewHost string, targetOrigin *url.URL) {
internal/server/browser_preview.go:189:	s.previewTargets[previewHost] = targetOrigin
internal/server/browser_preview.go:192:func (s *Server) browserPreviewTarget(previewHost string) (*url.URL, bool) {
internal/server/browser_preview.go:195:	targetOrigin, ok := s.previewTargets[previewHost]
internal/server/browser_preview.go:215:	if isBrowserPreviewHost(targetURL.Hostname()) {
internal/server/browser_preview.go:228:func browserPreviewURLForTarget(r *http.Request, previewHost string, targetURL *url.URL) string {
internal/server/browser_preview.go:231:		Host:     browserPreviewPublicHost(r, previewHost),
internal/server/browser_preview.go:243:func browserPreviewPublicHost(r *http.Request, previewHost string) string {
internal/server/browser_preview.go:244:	_, port, err := net.SplitHostPort(externalRequestHost(r))
internal/server/browser_preview.go:246:		return previewHost
internal/server/browser_preview.go:248:	return net.JoinHostPort(previewHost, port)
internal/server/browser_preview.go:309:		normalizedRequestHostname(externalRequestHost(r)) == normalizedRequestHostname(targetOrigin.Host) &&
internal/server/browser_preview.go:310:		requestPortForScheme(externalRequestScheme(r), externalRequestHost(r)) ==
internal/server/browser_preview.go:317:func isBrowserPreviewHost(host string) bool {
internal/server/browser_preview.go:323:	requestHost := normalizedRequestHostname(externalRequestHost(r))
internal/server/browser_preview.go:324:	requestPort := requestPortForScheme(externalRequestScheme(r), externalRequestHost(r))
internal/server/browser_preview.go:550:	previewHost := browserPreviewHostForOrigin(redirectOrigin)
internal/server/browser_preview.go:552:		previewHost = normalizedRequestHostname(externalRequestHost(r))
internal/server/browser_preview.go:554:	s.setBrowserPreviewTarget(previewHost, redirectOrigin)
internal/server/browser_preview.go:557:	w.Header().Set("Location", browserPreviewURLForTarget(r, previewHost, redirectURL))

```

> TOOL

tool_result
id: call_T9VMjEYgJFIg4uelrHLOAZah
```
Chunk ID: a532f6
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 417
Output:
	return absolutePath, http.StatusOK, nil
}

func (s *Server) handleDashboard(w http.ResponseWriter, r *http.Request) {
	if isBrowserPreviewHost(externalRequestHost(r)) {
		s.handleBrowserPreview(w, r)
		return
	}

	if isAPIHost(externalRequestHost(r)) {
		if r.URL.Path == "/" {
			writeJSON(w, http.StatusOK, map[string]string{
				"service": "yyork api",
				"status":  "ok",
			})
			return
		}

		writeJSON(w, http.StatusNotFound, map[string]string{
			"error": "not found",
		})
		return
	}

	// Prefer the on-disk dashboard when WebDir is set (dev workflow).
	if s.webDir != "" {
		if _, err := os.Stat(filepath.Join(s.webDir, "index.html")); err == nil {
			s.serveSPA(w, r, os.DirFS(s.webDir))
			return
		}
	}

	// Fall back to the embedded dashboard when present (single-binary).
	if s.webFS != nil {
		if _, err := fs.Stat(s.webFS, "index.html"); err == nil {
			s.serveSPA(w, r, s.webFS)
			return
		}
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	_, _ = fmt.Fprint(w, `<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>yyork</title>
  </head>
  <body>
    <main>
      <h1>yyork</h1>
      <p>Build the web dashboard first with <code>pnpm web:build</code>.</p>
    </main>
  </body>
</html>`)
}

func externalRequestHost(r *http.Request) string {
	if forwardedHost := r.Header.Get("X-Forwarded-Host"); forwardedHost != "" {
		host, _, _ := strings.Cut(forwardedHost, ",")
		if host = strings.TrimSpace(host); host != "" {
			return host
		}
	}

	return r.Host
}

func isAPIHost(host string) […]

> TOOL

tool_result
id: call_UnyJDeqbcFQgl3Bd4pw7TuwE
```
Chunk ID: 33e3b9
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1746
Output:
package cli

import (
	"context"
	"errors"
	"fmt"
	"io"
	"io/fs"
	"net"
	"os"
	"os/exec"
	"strconv"
	"syscall"
	"time"

	"github.com/spf13/cobra"

	"github.com/yyopc/yyork/internal/app"
)

const devBrowserPreviewAliasName = "yyork-preview.yyork"

// newDevCmd builds the dev-stack launcher. It is hidden because it is a
// development-loop entrypoint (driven by `pnpm dev` -> portless -> `go run .
// dev`), not a product verb. It runs the API server in-process and Vite as a
// child, wiring Vite's /api proxy at the server's bound address.
func newDevCmd(runApp appRunner, webFS fs.FS) *cobra.Command {
	return &cobra.Command{
		Use:    "dev",
		Hidden: true,
		Short:  "Run the dev stack: Vite + the API server (used by `pnpm dev`).",
		Long: "Run the local development stack: the API server in-process plus the " +
			"Vite dev server as a child, with Vite proxying /api to the server.\n\n" +
			"Ports come from the environment, not from scanning: portless assigns the " +
			"web PORT/HOST; the API binds an OS-chosen ephemeral port unless " +
			"YYORK_BACKEND_PORT pins it. Intended to be launched by `pnpm dev`.",
		Args: cobra.NoArgs,
		RunE: func(cmd *cobra.Command, _ []string) error {
			return runDev(cmd, runApp, webFS)
		}, […]

> TOOL

tool_result
id: call_7Tl7cMzAwsYjHDigXrYYltEF
```
Chunk ID: 21ef47
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 0
Output:

```

> AGENT

The dev stack currently registers only one Portless alias for preview traffic: `yyork-preview.yyork -> backend port`. That means every `*-preview.yyork.localhost` host depends on Portless wildcard/subdomain routing reaching yyork’s backend, while yyork keeps the per-host target mapping in memory.

> TOOL

tool_use exec_command
id: call_ci4WJYcj5HWQ2pW5IAh6eSzz
```json
{
  "cmd": "sed -n '240,360p' internal/server/browser_preview_test.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_use exec_command
id: call_HK04AyeBYvgbdmhe7jt8aXbz
```json
{
  "cmd": "sed -n '1,130p' internal/cli/dev_test.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_gFUF6lHvXz5w3SIDYt2PvWcK
```json
{
  "cmd": "sed -n '130,210p' internal/cli/dev_test.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_3KtdS8WqOALXGJzuGsOTu2RJ
```json
{
  "cmd": "rg -n \"projectName|CanvasTargetSummary|previewUrl|getCanvasPreviewTargetKey|target=|CanvasPanel\" web/src/features/home/<USER>/organisms web/src/features/home/<USER>/workspace.ts web/src/features/home/<USER> -g '*.tsx' -g '*.ts'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_ci4WJYcj5HWQ2pW5IAh6eSzz
```
Chunk ID: 787c9b
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 689
Output:
		t.Fatalf("expected vendored bridge script, got %s", response.Body.String())
	}
}

func TestBrowserPreviewProxyServesAgentationBundle(t *testing.T) {
	upstream := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, _ *http.Request) {
		_, _ = w.Write([]byte("ok"))
	}))
	t.Cleanup(upstream.Close)

	server := New(Config{
		WebFS: fstest.MapFS{
			"index.html": {
				Data: []byte("dashboard fixture"),
			},
			strings.TrimPrefix(browserPreviewAgentationPath, "/"): {
				Data: []byte("window.__yyorkAgentationLoaded = true;"),
			},
		},
	})
	previewURL := registerBrowserPreviewTarget(t, server, upstream.URL)
	request := httptest.NewRequest(http.MethodGet, previewURL, nil)
	request.URL.Path = browserPreviewAgentationPath
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("expected Agentation asset to be served, got %d", response.Code)
	}
	if !strings.Contains(response.Body.String(), "__yyorkAgentationLoaded") {
		t.Fatalf("expected Agentation bundle asset, got %s", response.Body.String())
	}
}

func TestBrowserPreviewTargetRegistrationPreservesDashboardPort(t *testing.T) {
	server := New(Config{})
	request := httptest.NewRequest(
		http.MethodPost,
		"http://127.0.0.1:4217/api/browser-preview/targets",
		strings.NewReader(`{"url":"http://localhost:3000/app"}`),
	)
	response := httptest.NewRecorder()

	server.Handler().ServeHTTP(response, request)

	if response.Code != http.StatusOK {
		t.Fatalf("register preview target failed with %d: %s", response.Code, response.Body.String())
	}

	var payload browserPreviewTargetResponse
	if err := json.NewDecoder(response.Body).Decode(&payload); err != nil {
		t.Fatalf("decode preview target response: %v", err)
	}
	if !strings.Contains(payload.PreviewURL, ".yyork.localhost:4217/app") {
		t.Fatalf("expected preview URL to preserve dashboard port, got %q", payload.PreviewURL)
	}
}

func registerBrowserPreviewTarget(t *testing.T, server *Server, targetURL string) string {
	t.Helper()

	request := httptest.NewRequest(
		http.MethodPost,
		"https://yyork.localhost/api/browser-preview/targets",
		strings.NewReader(`{"url":"`+targetURL+`"}`),
	)
	request.Header.Set("X-Forwarded-Proto", […]

> TOOL

tool_result
id: call_HK04AyeBYvgbdmhe7jt8aXbz
```
Chunk ID: d50c8c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 921
Output:
package cli

import (
	"net"
	"testing"
	"testing/fstest"
)

// envFunc builds a getenv-style lookup from a map for resolveDevConfig.
func envFunc(env map[string]string) func(string) string {
	return func(key string) string { return env[key] }
}

func TestResolveDevConfigDefaults(t *testing.T) {
	cfg, err := resolveDevConfig(envFunc(nil))
	if err != nil {
		t.Fatalf("resolveDevConfig: %v", err)
	}

	if cfg.webHost != "127.0.0.1" {
		t.Errorf("webHost = %q, want 127.0.0.1", cfg.webHost)
	}
	if cfg.webPort != 3000 {
		t.Errorf("webPort = %d, want 3000", cfg.webPort)
	}
	// No YYORK_BACKEND_PORT => ephemeral (port 0) on localhost.
	if cfg.backendAddr != "127.0.0.1:0" {
		t.Errorf("backendAddr = %q, want 127.0.0.1:0", cfg.backendAddr)
	}
	if got := cfg.webOrigin(); got != "http://127.0.0.1:3000" {
		t.Errorf("webOrigin = %q, want http://127.0.0.1:3000", got)
	}
}

func TestResolveDevConfigPortlessEnv(t *testing.T) {
	cfg, err := resolveDevConfig(envFunc(map[string]string{
		"PORT":         "4123",
		"HOST":         "0.0.0.0",
		"PORTLESS_URL": "https://yyork.localhost",
	}))
	if err != nil {
		t.Fatalf("resolveDevConfig: %v", err)
	}

	if cfg.webPort != 4123 {
		t.Errorf("webPort = %d, want 4123 (PORT from portless)", cfg.webPort)
	}
	if cfg.webHost != "0.0.0.0" {
		t.Errorf("webHost = %q, want 0.0.0.0 (HOST from portless)", cfg.webHost)
	}
	if got := cfg.webOrigin(); got != "https://yyork.localhost" {
		t.Errorf("webOrigin = %q, want the […]

> TOOL

tool_result
id: call_gFUF6lHvXz5w3SIDYt2PvWcK
```
Chunk ID: a53e24
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 205
Output:
	addr, err := net.ResolveTCPAddr("tcp", "127.0.0.1:7331")
	if err != nil {
		t.Fatalf("resolve addr: %v", err)
	}

	port, ok, err := devPreviewAliasPort(devConfig{}, addr)
	if err != nil {
		t.Fatalf("devPreviewAliasPort: %v", err)
	}
	if ok {
		t.Fatalf("ok = true, want false")
	}
	if port != "" {
		t.Fatalf("port = %q, want empty", port)
	}
}

func TestDevPreviewAliasPortUsesBackendPortUnderPortless(t *testing.T) {
	addr, err := net.ResolveTCPAddr("tcp", "127.0.0.1:7331")
	if err != nil {
		t.Fatalf("resolve addr: %v", err)
	}

	port, ok, err := devPreviewAliasPort(
		devConfig{portlessURL: "https://yyork.localhost"},
		addr,
	)
	if err != nil {
		t.Fatalf("devPreviewAliasPort: %v", err)
	}
	if !ok {
		t.Fatal("ok = false, want true")
	}
	if port != "7331" {
		t.Fatalf("port = %q, want 7331", port)
	}
}

```

> TOOL

tool_result
id: call_3KtdS8WqOALXGJzuGsOTu2RJ
```
Chunk ID: fbce81
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1375
Output:
web/src/features/home/<USER>/workspace.ts:26:  projectName: z.string().optional().default(''),
web/src/features/home/<USER>/workspace.ts:154:      name: row.projectName || basename(row.projectPath),
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:706:            projectName={props.project.name}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1086:  projectName: string;
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1092:        label={`Open ${props.projectName} actions`}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1097:                aria-label={`${props.projectName} actions`}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1390:  const projectNames = new Map(
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1399:      label: projectNames.get(orchestrator.project) ?? 'Orchestrator',
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:248:        <TopbarOrchestratorPanel projectName={activeProject.name} />
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:468:          projectName={props.project.name}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:576:function TopbarOrchestratorPanel(props: { projectName: string }) {
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:582:            {props.projectName}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:619:        eyebrow={props.projectName}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:637:  previewUrl: string;
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:681:        <SelectedTargetWorkspacePanel target={target} />
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:713:                projectName={project.name}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:762:  projectName: string;
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:770:          aria-label={`Open ${props.projectName} Kanban`}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:772:          title={`Open ${props.projectName} Kanban`}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:917:            target={props.target}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:959:        <span className="truncate">{props.target.previewUrl}</span>
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1042:  const projectNames = new Map(
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1066:      previewUrl: 'http://localhost:3000',
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1071:  const projectName = projectNames.get(session.project) ?? session.project;
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1081:    eyebrow: `${projectName} / ${targetKind}`,
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1091:    previewUrl: 'http://localhost:3000',
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1188:          projectName={activeProject.name}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1212:  projectName: string;
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1221:            {props.projectName}
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1472:  const projectNames = new Map(
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.stories.tsx:1479:      label: projectNames.get(orchestrator.project) ?? 'Orchestrator',
web/src/features/home/<USER>/organisms/canvas-panel.tsx:54:export interface CanvasTargetSummary {
web/src/features/home/<USER>/organisms/canvas-panel.tsx:57:  projectName?: string;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:152:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:166:export function CanvasPanel(props: {
web/src/features/home/<USER>/organisms/canvas-panel.tsx:168:  previewUrl?: string;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:175:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:194:            target={props.target}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:202:            target={props.target}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:207:            defaultUrl={props.previewUrl}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:210:            previewName={props.target.projectName}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:221:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:289:        target={props.target}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:300:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:333:      target={props.target}
web/src/features/home/<USER>/organisms/canvas-panel.tsx:397:  target: CanvasTargetSummary;

```

> AGENT

For two agents on different worktrees, the current storage model is already per session, but the proxy host name is not. If both sessions send the same project name and the same upstream origin, yyork can end up reusing the same preview host label and just overwrite the in-memory target for that host.

> TOOL

tool_use exec_command
id: call_xGRABkh6tHmzfx5EU3OlLbHI
```json
{
  "cmd": "sed -n '45,75p' web/src/features/home/<USER>/organisms/canvas-panel.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 10000
}
```

> TOOL

tool_use exec_command
id: call_jmbs3nU3HEOvRYmqhyb9FCno
```json
{
  "cmd": "rg -n \"<CanvasPanel|CanvasPanel\\(\" web/src/features/home/<USER> -g '*.tsx'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_use exec_command
id: call_hLvXP1x89KVScDU3DEOaF8Gs
```json
{
  "cmd": "rg -n \"canvasPreview|targetKey|selectedTarget|CanvasTargetSummary|projectName:\" web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx web/src/features/home/<USER>/organisms/terminal-panel.tsx web/src/features/home/<USER>/workspace.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_6oVaBPMLWwL0kUufobpN3BOS
```json
{
  "cmd": "sed -n '130,175p' web/src/features/home/<USER>/workspace.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_xGRABkh6tHmzfx5EU3OlLbHI
```
Chunk ID: f1666d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 190
Output:
} from '@/features/home/<USER>/session-files';
import type { HomeWorkspaceCanvasReviewPreferences } from '@/features/home/<USER>/workspace-preferences';
import {
  type CanvasTab,
  isCanvasTab,
} from '@/features/home/<USER>/canvas-tabs';

export type { CanvasTab } from '@/features/home/<USER>/canvas-tabs';

export interface CanvasTargetSummary {
  cwd?: string;
  projectId?: string;
  projectName?: string;
  sessionId?: string;
}

type FileCodeViewOptions = NonNullable<CodeViewProps<undefined>['options']>;

const fileCodeViewOptions: FileCodeViewOptions = {
  disableFileHeader: true,
  itemMetrics: {
    lineHeight: 17.4,
  },
  layout: {
    gap: 0,
    paddingBottom: 0,
    paddingTop: 0,
  },
  overflow: 'scroll',
  stickyHeaders: true,
  theme: {

```

> TOOL

tool_result
id: call_jmbs3nU3HEOvRYmqhyb9FCno
```
Chunk ID: 76fe40
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 26
Output:
web/src/features/home/<USER>/organisms/canvas-panel.tsx:166:export function CanvasPanel(props: {

```

> TOOL

tool_result
id: call_hLvXP1x89KVScDU3DEOaF8Gs
```
Chunk ID: fca62c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 50
Output:
web/src/features/home/<USER>/workspace.ts:26:  projectName: z.string().optional().default(''),
web/src/features/home/<USER>/organisms/project-orchestrator-sidebar.tsx:1086:  projectName: string;

```

> TOOL

tool_result
id: call_6oVaBPMLWwL0kUufobpN3BOS
```
Chunk ID: c7d620
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 292
Output:
    issue: '',
    kind: 'worker',
    metadata: row.metadata ? JSON.stringify(row.metadata) : '',
    project: row.projectPath,
    recap,
    state: 'working',
    terminalSupported: true,
    title,
    updatedAt: row.updatedAt,
    workerId: row.id,
    zellijSession: row.zellijSession,
  };
}

function uniqueProjects(
  rows: ApiSession[]
): { id: string; name: string; cwd?: string }[] {
  const seen = new Map<string, { id: string; name: string; cwd?: string }>();
  for (const row of rows) {
    if (seen.has(row.projectPath)) {
      continue;
    }
    seen.set(row.projectPath, {
      id: row.projectPath,
      name: row.projectName || basename(row.projectPath),
      cwd: row.projectPath,
    });
  }
  return Array.from(seen.values());
}

function basename(path: string): string {
  const idx = Math.max(path.lastIndexOf('/'), path.lastIndexOf('\\'));
  return idx === -1 ? path : path.slice(idx + 1);
}

export const fallbackHomeWorkspace: SessionWorkspace = {
  activeProjectId: '',
  orchestrators: [],
  projects: [],
  sessions: [],
};

export function stopSessionMutationOptions() {
  return {
    mutationFn: async (sessionId: string) => {

```

> AGENT

I’m checking how the selected Canvas target is assembled. That determines whether the project name or session id is actually available at the point where the Browser tab registers the proxy host.

> TOOL

tool_use exec_command
id: call_zklDmVjnpJElBvl05F0jPMlW
```json
{
  "cmd": "rg -n \"CanvasPanel|canvasPreview|canvasTab|targetKey|activeCanvas|selected.*target|CanvasTarget\" web/src -g '*.tsx' -g '*.ts'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 26000
}
```

> TOOL

tool_use exec_command
id: call_26W04wr2H8tQ4HXCSG4v9XYJ
```json
{
  "cmd": "sed -n '1,130p' web/src/features/home/<USER>/session-workspace.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 16000
}
```

> TOOL

tool_use exec_command
id: call_CcrX965Hx7yvuuSpnnpylKBQ
```json
{
  "cmd": "sed -n '1,90p' web/src/features/home/<USER>/workspace.ts",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_use exec_command
id: call_KIg89r8sUqYYOA1FN9PBUrl0
```json
{
  "cmd": "rg -n \"sessionId|projectName|projectPath\" internal/server/sessions.go internal/store/sessions.go internal/session -g '*.go'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_result
id: call_zklDmVjnpJElBvl05F0jPMlW
```
Chunk ID: 8dbd0a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1615
Output:
web/src/features/home/<USER>/workspace-layout.tsx:36:  CanvasTargetSummary,
web/src/features/home/<USER>/workspace-layout.tsx:89:  canvasTab: CanvasTab;
web/src/features/home/<USER>/workspace-layout.tsx:103:  | { canvasTab: CanvasTab; type: 'canvas-tab' };
web/src/features/home/<USER>/workspace-layout.tsx:110:    canvasTab: homeWorkspacePreferences.canvasTab ?? 'files',
web/src/features/home/<USER>/workspace-layout.tsx:148:        canvasTab: action.canvasTab,
web/src/features/home/<USER>/workspace-layout.tsx:179:    canvasTab,
web/src/features/home/<USER>/workspace-layout.tsx:287:  const canvasTarget: CanvasTargetSummary = selectedTerminalSession
web/src/features/home/<USER>/workspace-layout.tsx:299:  const canvasPreviewTargetKey = getCanvasPreviewTargetKey(canvasTarget);
web/src/features/home/<USER>/workspace-layout.tsx:300:  const canvasPreviewUrl = getCanvasPreviewUrlForTarget(
web/src/features/home/<USER>/workspace-layout.tsx:302:    canvasPreviewTargetKey
web/src/features/home/<USER>/workspace-layout.tsx:399:    dispatchLayout({ canvasTab: tab, type: 'canvas-tab' });
web/src/features/home/<USER>/workspace-layout.tsx:400:    updateHomeWorkspacePreferences({ canvasTab: tab });
web/src/features/home/<USER>/workspace-layout.tsx:407:        canvasPreviewTargetKey,
web/src/features/home/<USER>/workspace-layout.tsx:701:    canvasPreviewUrl,
web/src/features/home/<USER>/workspace-layout.tsx:704:    canvasTab,
web/src/features/home/<USER>/terminal-layout.tsx:5:import { CanvasPanel } from '@/features/home/<USER>/organisms/canvas-panel';
web/src/features/home/<USER>/terminal-layout.tsx:102:          <CanvasPanel
web/src/features/home/<USER>/terminal-layout.tsx:103:            activeTab={context.canvasTab}
web/src/features/home/<USER>/terminal-layout.tsx:104:            previewUrl={context.canvasPreviewUrl}
web/src/features/home/<USER>/workspace-context.ts:5:  CanvasTargetSummary,
web/src/features/home/<USER>/workspace-context.ts:21:  canvasPreviewUrl?: string;
web/src/features/home/<USER>/workspace-context.ts:24:  canvasTab: CanvasTab;
web/src/features/home/<USER>/workspace-context.ts:25:  canvasTarget: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:54:export interface CanvasTargetSummary {
web/src/features/home/<USER>/organisms/canvas-panel.tsx:152:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:166:export function CanvasPanel(props: {
web/src/features/home/<USER>/organisms/canvas-panel.tsx:175:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:221:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:300:  target: CanvasTargetSummary;
web/src/features/home/<USER>/organisms/canvas-panel.tsx:397:  target: CanvasTargetSummary;
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:43:      canvasPreviewUrl: 'https://yyork.localhost/',
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:44:      canvasPreviewUrls: {
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:61:        canvasPreviewUrl: 'https://yyork.localhost/',
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:62:        canvasPreviewUrls: {
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:71:      canvasPreviewUrl: undefined,
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:72:      canvasPreviewUrls: {
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:91:      canvasPreviewUrl: 'https://google.com',
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:92:      canvasPreviewUrls: {
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:101:      canvasPreviewUrls: {
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:120:      canvasTab: 'browser',
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:126:      canvasTab: 'browser',
web/src/features/home/<USER>/workspace-preferences.unit.spec.ts:134:        canvasTab: 'terminal',
web/src/features/home/<USER>/organisms/main-topbar.tsx:28:    canvasTab,
web/src/features/home/<USER>/organisms/main-topbar.tsx:102:                  value={canvasTab}
web/src/features/home/<USER>/workspace-preferences.ts:15:  canvasPreviewUrls?: Record<string, string>;
web/src/features/home/<USER>/workspace-preferences.ts:16:  canvasPreviewUrl?: string;
web/src/features/home/<USER>/workspace-preferences.ts:18:  canvasTab?: CanvasTab;
web/src/features/home/<USER>/workspace-preferences.ts:113:    'canvasPreviewUrl' | 'canvasPreviewUrls'
web/src/features/home/<USER>/workspace-preferences.ts:115:  targetKey: string
web/src/features/home/<USER>/workspace-preferences.ts:117:  return preferences.canvasPreviewUrls?.[targetKey] ?? preferences.canvasPreviewUrl;
web/src/features/home/<USER>/workspace-preferences.ts:123:    'canvasPreviewUrl' | 'canvasPreviewUrls'
web/src/features/home/<USER>/workspace-preferences.ts:125:  targetKey: string,
web/src/features/home/<USER>/workspace-preferences.ts:127:): Pick<HomeWorkspacePreferences, 'canvasPreviewUrl' | 'canvasPreviewUrls'> […]

> TOOL

tool_result
id: call_26W04wr2H8tQ4HXCSG4v9XYJ
```
Chunk ID: 1721aa
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 854
Output:
import {
  getElapsedLabel,
  type SessionActivity,
  toKanbanCardView,
  type WorkerSessionRecord,
} from '@/features/home/<USER>/kanban-card-model';
import {
  type SessionWorkspace,
  type TerminalSessionKind,
  type WorkerAgent,
  type WorkerSession,
  type WorkerSessionState,
  workerSessionStates,
} from '@/features/home/<USER>/session-workspace-contract.generated';

export {
  type SessionActivity,
  sessionActivityStates,
  type WorkerSessionRecord,
} from '@/features/home/<USER>/kanban-card-model';
export {
  type ProjectOrchestrator,
  type SessionWorkspace,
  type TerminalSessionKind,
  type WorkerAgent,
  type WorkerSession,
  type WorkerSessionState,
  workerSessionStates,
} from '@/features/home/<USER>/session-workspace-contract.generated';

export interface KanbanCardData {
  activity: SessionActivity;
  activityLabel: string;
  agent: WorkerAgent;
  agentLabel: string;
  /** @deprecated Prefer `recap`. */
  currentLine: string;
  /** @deprecated Prefer `recap`. */
  description: string;
  id: string;
  issue: string;
  /** Raw metadata blob — not for direct display. */
  metadata: string;
  project: string;
  selected?: boolean;
  selectionKey: string;
  recap: string;
  shortId: string;
  task: string;
  /** @deprecated Prefer `task` — kept for transitional callers. */
  title: string;
  workerId: string;
}

export interface KanbanColumnData {
  cards: KanbanCardData[];
  id: WorkerSessionState;
  title: string;
}

export interface WorkerSessionNavItem {
  agent: WorkerAgent;
  elapsedLabel: string;
  id: string;
  kind?: TerminalSessionKind;
  /**
   * Resolved display label for the session. The backend is the single source
   * of truth: a user-set displayName wins, then the hook-derived title, then
   * the raw prompt, then "new […]

> TOOL

tool_result
id: call_CcrX965Hx7yvuuSpnnpylKBQ
```
Chunk ID: 017d6c
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 873
Output:
import { type QueryClient, queryOptions } from '@tanstack/react-query';
import { z } from 'zod';

import {
  type SessionWorkspace,
  type WorkerSession,
  type WorkerSessionRecord,
} from '@/features/home/<USER>/session-workspace';

// ---------------------------------------------------------------------------
// /api/sessions — the new SQLite-backed source of truth.
//
// The server returns a flat list of currently-running sessions (a row
// exists in the database exactly when the session is alive). The dashboard
// expects the legacy SessionWorkspace shape, so we adapt one to the other
// here. Until activity capture lands, every session lands in the kanban's
// "working" column by default — the prompt/triage/done columns are real
// (the contract still includes them) but unreachable in v1.
// ---------------------------------------------------------------------------

export const homeWorkspaceQueryKey = ['home-workspace'] as const;

const apiSessionSchema = z.object({
  id: z.string(),
  projectPath: z.string(),
  projectName: z.string().optional().default(''),
  agentPlugin: z.string(),
  workspacePath: z.string(),
  zellijSession: z.string(),
  pid: z.number().optional(),
  metadata: z.record(z.string(), z.unknown()).optional(),
  title: z.string().optional().default(''),
  recap: z.string().optional().default(''),
  createdAt: z.string(),
  updatedAt: z.string(),
});
type ApiSession = z.infer<typeof apiSessionSchema>;

const apiSessionsResponseSchema = z.array(apiSessionSchema);

export function homeWorkspaceQueryOptions() {
  return queryOptions({
    enabled: typeof window !== 'undefined',
    queryFn: fetchHomeWorkspace,
    queryKey: homeWorkspaceQueryKey,
    // SSE drives live updates — no polling. […]

> TOOL

tool_result
id: call_KIg89r8sUqYYOA1FN9PBUrl0
```
Chunk ID: 2a2880
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 512
Output:
internal/server/sessions.go:22:	ProjectPath   string         `json:"projectPath"`
internal/server/sessions.go:23:	ProjectName   string         `json:"projectName"`
internal/store/sessions.go:54:	ListByProject(ctx context.Context, projectPath string) ([]Session, error)
internal/store/sessions.go:153:func (r *sessionRepo) ListByProject(ctx context.Context, projectPath string) ([]Session, error) {
internal/store/sessions.go:159:	return r.queryList(ctx, q, projectPath)
internal/store/sessions.go:258:		projectName   sql.NullString
internal/store/sessions.go:267:		&projectName,
internal/store/sessions.go:280:	if projectName.Valid {
internal/store/sessions.go:281:		s.ProjectName = projectName.String
internal/session/engine.go:441:func (e *Engine) rollbackWorktree(ctx context.Context, projectPath, worktreePath, branchName string) {
internal/session/engine.go:444:	_ = e.worktree.Remove(ctx, projectPath, worktreePath, branchName)
internal/session/engine_test.go:31:	projectPath, worktreePath, branchName, baseRef string
internal/session/engine_test.go:35:	projectPath, worktreePath, branchName string
internal/session/engine_test.go:38:func (f *fakeWorktree) IsGitRepo(_ context.Context, projectPath string) bool {
internal/session/engine_test.go:40:		return f.isGitRepo(projectPath)
internal/session/engine_test.go:45:func (f *fakeWorktree) BaseRef(_ context.Context, projectPath string) (string, error) {
internal/session/engine_test.go:47:		return f.baseRef(projectPath)
internal/session/engine_test.go:52:func (f *fakeWorktree) Create(_ context.Context, projectPath, worktreePath, branchName, baseRef string) error {
internal/session/engine_test.go:55:	f.createCalls = append(f.createCalls, fakeWorktreeCreateCall{projectPath, worktreePath, branchName, baseRef})
internal/session/engine_test.go:59:func (f *fakeWorktree) Remove(_ context.Context, projectPath, worktreePath, branchName string) error {
internal/session/engine_test.go:62:	f.removeCalls = append(f.removeCalls, fakeWorktreeRemoveCall{projectPath, worktreePath, branchName})

```

> AGENT

At this point the root cause is clear enough for an answer, but I’m doing one more pass over the layout assembly so I can say exactly what field would need to change for your proposed `{sessionId}-{projectName}-preview` shape.

> TOOL

tool_use exec_command
id: call_cWn5GuhOrVf9JBgsl2lQCz90
```json
{
  "cmd": "sed -n '260,315p' web/src/features/home/<USER>/workspace-layout.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_x8usxtwlHoS2pwnk7M07MYbo
```json
{
  "cmd": "sed -n '390,415p' web/src/features/home/<USER>/workspace-layout.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_b6uaFo3k67cG2FVvR2arftfB
```json
{
  "cmd": "sed -n '680,710p' web/src/features/home/<USER>/workspace-layout.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_use exec_command
id: call_Y3VHDRb6IeiLioYZXO2SszRc
```json
{
  "cmd": "sed -n '90,115p' web/src/features/home/<USER>/terminal-layout.tsx",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_cWn5GuhOrVf9JBgsl2lQCz90
```
Chunk ID: 202398
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 546
Output:
    : undefined;
  const selectedTerminalSessionKey = selectedTerminalSession
    ? getWorkerSessionSelectionKey(selectedTerminalSession)
    : routeSelectedWorkerSessionKey;
  const terminalRouteTargetLegacy =
    terminalRouteTarget?.legacySelectionKey ?? false;
  const terminalRouteTargetProject = terminalRouteTarget?.project;
  const terminalRouteTargetSessionId = terminalRouteTarget?.sessionId;
  const selectedTerminalSessionId = selectedTerminalSession?.id;
  const selectedTerminalSessionProject = selectedTerminalSession?.project;
  const selectedTerminalSessionRouteProject =
    selectedTerminalSession &&
    terminalSessionIdRequiresProject(
      terminalSessions,
      selectedTerminalSession.id
    )
      ? selectedTerminalSession.project
      : undefined;
  const selectedProjectId =
    selectedTerminalSession?.project ??
    boardProjectIdParam ??
    projects[0]?.id ??
    workspace.activeProjectId;
  const activeBoardProjectId = isTerminalRoute ? undefined : selectedProjectId;
  const selectedProject = projects.find(
    (project) => project.id === selectedProjectId
  );
  const canvasTarget: CanvasTargetSummary = selectedTerminalSession
    ? {
        cwd: selectedTerminalSession.cwd,
        projectId: selectedTerminalSession.project,
        projectName: selectedProject?.name,
        sessionId: selectedTerminalSession.id,
      }
    : {
        cwd: selectedProject?.cwd,
        projectId: selectedProject?.id,
        projectName: selectedProject?.name,
      };
  const canvasPreviewTargetKey = getCanvasPreviewTargetKey(canvasTarget);
  const canvasPreviewUrl = getCanvasPreviewUrlForTarget(
    homeWorkspacePreferences,
    canvasPreviewTargetKey
  );
  const defaultOpenProjectIds: string[] =
    selectedProjectId &&
    projects.some((project) => project.id === selectedProjectId)
      ? [selectedProjectId]
      : [];
  const boardSessions = sessions.filter(
    (session) => session.project === selectedProjectId
  );
  const kanbanColumns = getKanbanColumns(boardSessions);
  const workerSessionGroups = getWorkerSessionGroups(sessions);
  const workspaceState: WorkspacePanelState = workspaceQueryIsPending
    ? 'loading'

```

> TOOL

tool_result
id: call_x8usxtwlHoS2pwnk7M07MYbo
```
Chunk ID: 214dfb
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 197
Output:
  const handleCanvasOpenChange = (open: boolean) => {
    updateHomeWorkspacePreferences({ canvasOpen: open });
  };

  const handleCanvasLayoutChange = (layout: HomeWorkspaceCanvasLayout) => {
    updateHomeWorkspacePreferences({ canvasLayout: layout });
  };

  const handleCanvasTabChange = (tab: CanvasTab) => {
    dispatchLayout({ canvasTab: tab, type: 'canvas-tab' });
    updateHomeWorkspacePreferences({ canvasTab: tab });
  };

  const handleCanvasPreviewUrlChange = (url: string) => {
    updateHomeWorkspacePreferences(
      getCanvasPreviewUrlPreferenceUpdate(
        homeWorkspacePreferences,
        canvasPreviewTargetKey,
        url
      )
    );
  };

  const handleCanvasReviewPreferencesChange = (
    preferences: HomeWorkspaceCanvasReviewPreferences
  ) => {

```

> TOOL

tool_result
id: call_b6uaFo3k67cG2FVvR2arftfB
```
Chunk ID: 90487a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 214
Output:
          true,
          defaultOpenProjectIds
        ),
      });
    }

    void navigate({
      to: '/terminal/$sessionId',
      params: { sessionId: targetSessionId },
      search: targetSession
        ? getTerminalRouteSearch(terminalSessions, targetSession)
        : targetProjectId
          ? { project: targetProjectId }
          : {},
    });
  };

  const workspaceContextValue: WorkspaceContextValue = {
    canvasAvailable: isTerminalRoute,
    canvasLayout,
    canvasOpen,
    canvasPreviewUrl,
    canvasReviewPreferences,
    canvasResizing,
    canvasTab,
    canvasTarget,
    kanbanColumns,
    onCanvasLayoutChange: handleCanvasLayoutChange,
    onCanvasOpenChange: handleCanvasOpenChange,
    onCanvasPreviewUrlChange: handleCanvasPreviewUrlChange,
    onCanvasReviewPreferencesChange: handleCanvasReviewPreferencesChange,

```

> TOOL

tool_result
id: call_Y3VHDRb6IeiLioYZXO2SszRc
```
Chunk ID: aaf829
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 243
Output:
        }}
        aria-hidden={!context.canvasOpen}
        inert={!context.canvasOpen}
      >
        <div
          data-state={context.canvasOpen ? 'expanded' : 'collapsed'}
          className={cn(
            'flex h-full w-full min-w-70 transition-[transform,opacity] duration-200 ease-linear',
            'data-[state=collapsed]:translate-x-full data-[state=collapsed]:opacity-0',
            'group-data-[canvas-resizing=true]/canvas-layout:transition-none'
          )}
        >
          <CanvasPanel
            activeTab={context.canvasTab}
            previewUrl={context.canvasPreviewUrl}
            reviewPreferences={context.canvasReviewPreferences}
            onPreviewUrlChange={context.onCanvasPreviewUrlChange}
            onReviewPreferencesChange={context.onCanvasReviewPreferencesChange}
            onTabChange={context.onCanvasTabChange}
            target={context.canvasTarget}
          />
        </div>
      </div>
    </div>
  );
}

```

> AGENT

One subtlety: with the current Go code, `https://yyork.localhost/...` with no `previewName` should still become `yyork-preview.yyork.localhost`. So your pasted `https-yyork-localhost-preview...` most likely means the browser registration sent `previewName: "https://yyork.localhost"` or equivalent, because explicit preview names take precedence over the self-preview shortcut.

> TOOL

tool_use exec_command
id: call_Q6cRVJmiJgcEXensXzmvPL4M
```json
{
  "cmd": "sed -n '1,70p' internal/server/sessions.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 10000
}
```

> TOOL

tool_use exec_command
id: call_xDVVZ1uVHfugrm3Hahkr1cAH
```json
{
  "cmd": "rg -n \"ProjectName|projectName|project_name|NewSession|Create\\(\" internal/session internal/store internal/server -g '*.go'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 22000
}
```

> TOOL

tool_use exec_command
id: call_EpsP2tH7X4NYiZ9CJCgPT6rN
```json
{
  "cmd": "rg -n \"project_name|projectName\" internal/store/migrations internal -g '*.sql' -g '*.go'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 18000
}
```

> TOOL

tool_use exec_command
id: call_7svZeGruuxRLDm9dqXFAs8PA
```json
{
  "cmd": "sed -n '200,300p' internal/store/sessions.go",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 12000
}
```

> TOOL

tool_result
id: call_Q6cRVJmiJgcEXensXzmvPL4M
```
Chunk ID: cac3e2
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 535
Output:
package server

import (
	"crypto/subtle"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/yyopc/yyork/internal/control"
	"github.com/yyopc/yyork/internal/events"
	"github.com/yyopc/yyork/internal/store"
)

// sessionDTO is the JSON shape /api/sessions returns. It mirrors
// store.Session but with explicit JSON tags and ISO-8601 timestamps so the
// dashboard doesn't need to format Unix epochs.
type sessionDTO struct {
	ID            string         `json:"id"`
	ProjectPath   string         `json:"projectPath"`
	ProjectName   string         `json:"projectName"`
	AgentPlugin   string         `json:"agentPlugin"`
	WorkspacePath string         `json:"workspacePath"`
	ZellijSession string         `json:"zellijSession"`
	PID           int64          `json:"pid,omitempty"`
	Metadata      map[string]any `json:"metadata,omitempty"`
	Title         string         `json:"title"`
	Recap         string         `json:"recap"`
	CreatedAt     time.Time      `json:"createdAt"`
	UpdatedAt     time.Time      `json:"updatedAt"`
}

func toSessionDTO(s store.Session) sessionDTO {
	return sessionDTO{
		ID:            s.ID,
		ProjectPath:   s.ProjectPath,
		ProjectName:   s.ProjectName,
		AgentPlugin:   s.AgentPlugin,
		WorkspacePath: s.WorkspacePath,
		ZellijSession: s.ZellijSession,
		PID:           s.PID,
		Metadata:      s.Metadata,
		Title:         resolvedSessionTitle(s),
		Recap:         resolvedSessionRecap(s),
		CreatedAt:     s.CreatedAt,
		UpdatedAt:     s.UpdatedAt,
	}
}

func resolvedSessionTitle(s store.Session) string {
	for _, key := range []string{"displayName", "title", "prompt"} {
		if value := metadataString(s.Metadata, key); value != "" {
			return value
		}
	}
	return "new agent: " + s.ID
}

func resolvedSessionRecap(s store.Session) string {
	if recap := metadataString(s.Metadata, "recap"); recap != "" {
		return recap
	}
	// Legacy compatibility for stores created before metadata.summary was […]

> TOOL

tool_result
id: call_xDVVZ1uVHfugrm3Hahkr1cAH
```
Chunk ID: 287799
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 762
Output:
internal/store/store_test.go:76:		ProjectName:   "proj",
internal/store/store_test.go:254:	if got.ProjectName != want.ProjectName {
internal/store/store_test.go:255:		t.Errorf("ProjectName = %q, want %q", got.ProjectName, want.ProjectName)
internal/store/sessions.go:20:	ProjectName   string
internal/store/sessions.go:105:    id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:112:		nullableString(s.ProjectName),
internal/store/sessions.go:129:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:146:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:155:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:258:		projectName   sql.NullString
internal/store/sessions.go:267:		&projectName,
internal/store/sessions.go:280:	if projectName.Valid {
internal/store/sessions.go:281:		s.ProjectName = projectName.String
internal/session/workspace_source.go:49:			Name: row.ProjectName,
internal/server/sessions_test.go:64:		{ID: "01HRSERVER000000000000000A", ProjectPath: "/tmp/a", ProjectName: "a", AgentPlugin: "codex", WorkspacePath: "/tmp/a/.w", ZellijSession: "01HRSERVER000000000000000A", Metadata: map[string]any{"recap": "Reviewed the workspace setup."}},
internal/server/sessions_test.go:65:		{ID: "01HRSERVER000000000000000B", ProjectPath: "/tmp/b", ProjectName: "b", AgentPlugin: "codex", WorkspacePath: "/tmp/b/.w", ZellijSession: "01HRSERVER000000000000000B", Metadata: map[string]any{"displayName": "Project overview", "prompt": "tell me about this project"}},
internal/server/sessions_test.go:155:	bus.Publish(events.NewSessionCreated("test-session-id"))
internal/server/sessions_test.go:252:		ID: "01HRRENAME0000000000000001", ProjectPath: "/tmp/a", ProjectName: "a",
internal/server/sessions_test.go:292:		ID: "01HRRENAME0000000000000002", ProjectPath: "/tmp/a", ProjectName: "a",
internal/server/sessions.go:23:	ProjectName   string         `json:"projectName"`
internal/server/sessions.go:39:		ProjectName:   s.ProjectName,
internal/server/sessions.go:155:		s.eventBus.Publish(events.NewSessionUpdated(sessionID))
internal/session/engine.go:251:	if err := e.worktree.Create(ctx, req.ProjectPath, workspacePath, branchName, baseRef); err != nil {
internal/session/engine.go:304:		ProjectName:   filepath.Base(req.ProjectPath),
internal/session/engine.go:329:	e.bus.Publish(events.NewSessionCreated(id))
internal/session/engine.go:361:	e.bus.Publish(events.NewSessionTerminated(id))
internal/session/engine.go:391:	e.bus.Publish(events.NewSessionTerminated(id))
internal/session/engine.go:424:		e.bus.Publish(events.NewSessionTerminated(row.ID))
internal/session/engine_test.go:52:func (f *fakeWorktree) Create(_ context.Context, projectPath, worktreePath, branchName, baseRef string) error {
internal/session/engine_test.go:267:	if sess.ProjectName != "proj" {
internal/session/engine_test.go:268:		t.Errorf("ProjectName = %q, want %q", sess.ProjectName, "proj") […]

> TOOL

tool_result
id: call_EpsP2tH7X4NYiZ9CJCgPT6rN
```
Chunk ID: 24de9d
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 261
Output:
internal/store/migrations/0001_create_sessions.sql:5:    project_name    TEXT,
internal/store/sessions.go:105:    id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:129:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:146:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:155:SELECT id, project_path, project_name, agent_plugin, workspace_path,
internal/store/sessions.go:258:		projectName   sql.NullString
internal/store/sessions.go:267:		&projectName,
internal/store/sessions.go:280:	if projectName.Valid {
internal/store/sessions.go:281:		s.ProjectName = projectName.String
internal/store/migrations/0001_create_sessions.sql:5:    project_name    TEXT,
internal/server/sessions.go:23:	ProjectName   string         `json:"projectName"`
internal/ao/workspace.go:115:			Name: projectName(projectID, running.ConfigPath),
internal/ao/workspace.go:520:func projectName(projectID string, configPath string) string {

```

> TOOL

tool_result
id: call_7svZeGruuxRLDm9dqXFAs8PA
```
Chunk ID: eec610
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 572
Output:

	merged := map[string]any{}
	if current.Valid && current.String != "" {
		if err := json.Unmarshal([]byte(current.String), &merged); err != nil {
			return fmt.Errorf("decode current metadata: %w", err)
		}
	}
	for k, v := range fields {
		merged[k] = v
	}

	encoded, err := encodeMetadata(merged)
	if err != nil {
		return err
	}

	now := time.Now().UTC().Unix()
	res, err := tx.ExecContext(ctx,
		`UPDATE sessions SET metadata = ?, updated_at = ? WHERE id = ?`,
		nullableString(encoded), now, id)
	if err != nil {
		return fmt.Errorf("update metadata: %w", err)
	}
	if err := ensureRowAffected(res, id); err != nil {
		return err
	}
	return tx.Commit()
}

func (r *sessionRepo) queryList(ctx context.Context, q string, args ...any) ([]Session, error) {
	rows, err := r.db.QueryContext(ctx, q, args...)
	if err != nil {
		return nil, fmt.Errorf("query sessions: %w", err)
	}
	defer func() { _ = rows.Close() }()

	var out []Session
	for rows.Next() {
		s, err := scanSession(rows)
		if err != nil {
			return nil, fmt.Errorf("scan session: %w", err)
		}
		out = append(out, s)
	}
	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate sessions: %w", err)
	}
	return […]

> AGENT

I’m not going to patch it unless you want that next; this turn reads like a design/root-cause question. I’ll give you the exact current behavior and the smallest code direction for the session-scoped hostname.

> TOOL

tool_use exec_command
id: call_2Jcb2OtpcZ7VMUJUZD1NYwR2
```json
{
  "cmd": "nl -ba internal/server/browser_preview.go | sed -n '20,65p;225,315p'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 14000
}
```

> TOOL

tool_use exec_command
id: call_06KkKO2kFdzrfagsnCVLyzIG
```json
{
  "cmd": "nl -ba web/src/features/home/<USER>/organisms/canvas-panel.tsx | sed -n '204,214p'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_use exec_command
id: call_vEW2xEm7ODB04xlwcLchMvc2
```json
{
  "cmd": "nl -ba web/src/features/home/<USER>/molecules/canvas-web-preview.tsx | sed -n '620,642p'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 9000
}
```

> TOOL

tool_use exec_command
id: call_BrfmUJcyhGeN4gcRRRM7YgIY
```json
{
  "cmd": "nl -ba internal/cli/dev.go | sed -n '18,24p;123,151p'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 10000
}
```

> TOOL

tool_use exec_command
id: call_yBLQVT22O3MYx6451iEQbcj1
```json
{
  "cmd": "nl -ba /home/<USER>/.codex/memories/MEMORY.md | sed -n '1,3p;51,52p'",
  "workdir": "/home/<USER>/Projects/yyork",
  "yield_time_ms": 10000,
  "max_output_tokens": 8000
}
```

> TOOL

tool_result
id: call_2Jcb2OtpcZ7VMUJUZD1NYwR2
```
Chunk ID: 3b6a18
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 1267
Output:
    20		"strings"
    21	)
    22	
    23	const (
    24		browserPreviewAgentationPath = "/__yyork_browser/agentation.js"
    25		browserPreviewBridgePath     = "/__yyork_browser/preview-bridge.js"
    26		browserPreviewHostSuffix     = "-preview.yyork.localhost"
    27	)
    28	
    29	var browserPreviewSlugChars = regexp.MustCompile(`[^a-z0-9]+`)
    30	
    31	type browserPreviewTargetRequest struct {
    32		PreviewName string `json:"previewName"`
    33		URL         string `json:"url"`
    34	}
    35	
    36	type browserPreviewTargetResponse struct {
    37		PreviewURL string `json:"previewUrl"`
    38		TargetURL  string `json:"targetUrl"`
    39	}
    40	
    41	func (s *Server) handleBrowserPreviewTarget(w http.ResponseWriter, r *http.Request) {
    42		var payload browserPreviewTargetRequest
    43		if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
    44			http.Error(w, "invalid preview target payload", http.StatusBadRequest)
    45			return
    46		}
    47	
    48		targetURL, err := parseBrowserPreviewTargetURL(payload.URL)
    49		if err != nil {
    50			http.Error(w, err.Error(), http.StatusUnprocessableEntity)
    51			return
    52		}
    53	
    54		targetOrigin := browserPreviewOrigin(targetURL)
    55		previewHost := browserPreviewHostForTarget(r, payload.PreviewName, targetOrigin)
    56		s.setBrowserPreviewTarget(previewHost, targetOrigin)
    57	
    58		writeJSON(w, http.StatusOK, browserPreviewTargetResponse{
    59			PreviewURL: browserPreviewURLForTarget(r, previewHost, targetURL),
    60			TargetURL:  targetURL.String(),
    61		})
    62	}
    63	
    64	func (s *Server) handleBrowserPreview(w http.ResponseWriter, r *http.Request) {
    65		if r.URL.Path == browserPreviewBridgePath {
   225		}
   226	}
   227	
   228	func browserPreviewURLForTarget(r *http.Request, previewHost string, targetURL *url.URL) string {
   229		previewURL := […]

> TOOL

tool_result
id: call_06KkKO2kFdzrfagsnCVLyzIG
```
Chunk ID: 6368f7
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 125
Output:
   204	        </TabsContent>
   205	        <TabsContent value="browser" className="min-h-0 w-full overflow-hidden">
   206	          <CanvasWebPreview
   207	            defaultUrl={props.previewUrl}
   208	            onUrlChange={props.onPreviewUrlChange}
   209	            projectId={props.target.projectId}
   210	            previewName={props.target.projectName}
   211	            sessionId={props.target.sessionId}
   212	          />
   213	        </TabsContent>
   214	      </Tabs>

```

> TOOL

tool_result
id: call_vEW2xEm7ODB04xlwcLchMvc2
```
Chunk ID: c18f8f
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 178
Output:
   620	    }
   621	
   622	    const controller = new AbortController();
   623	
   624	    void registerBrowserPreviewTarget(currentUrl, {
   625	      previewName,
   626	      signal: controller.signal,
   627	    })
   628	      .then((target) => {
   629	        setFrameState({
   630	          frameUrl: target.previewUrl,
   631	          sourceUrl: currentUrl,
   632	        });
   633	      })
   634	      .catch((errorValue: unknown) => {
   635	        if (controller.signal.aborted) {
   636	          return;
   637	        }
   638	        handlePreviewRegistrationError(errorValue);
   639	      });
   640	
   641	    return () => controller.abort();
   642	  }, [currentUrl, previewName]);

```

> TOOL

tool_result
id: call_BrfmUJcyhGeN4gcRRRM7YgIY
```
Chunk ID: 79503a
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 301
Output:
    18		"github.com/yyopc/yyork/internal/app"
    19	)
    20	
    21	const devBrowserPreviewAliasName = "yyork-preview.yyork"
    22	
    23	// newDevCmd builds the dev-stack launcher. It is hidden because it is a
    24	// development-loop entrypoint (driven by `pnpm dev` -> portless -> `go run .
   123		if cfg.portlessURL == "" {
   124			return "", false, nil
   125		}
   126		_, port, err := net.SplitHostPort(apiAddr.String())
   127		if err != nil || port == "" {
   128			return "", false, fmt.Errorf("backend address %q has no port", apiAddr.String())
   129		}
   130		return port, true, nil
   131	}
   132	
   133	func registerDevPreviewAlias(ctx context.Context, cmd *cobra.Command, cfg devConfig, apiAddr net.Addr) error {
   134		port, ok, err := devPreviewAliasPort(cfg, apiAddr)
   135		if err != nil || !ok {
   136			return err
   137		}
   138	
   139		alias := exec.CommandContext(
   140			ctx,
   141			"pnpm",
   142			"exec",
   143			"portless",
   144			"alias",
   145			devBrowserPreviewAliasName,
   146			port,
   147			"--force",
   148		)
   149		alias.Stdout = cmd.OutOrStdout()
   150		alias.Stderr = cmd.ErrOrStderr()
   151		if err := alias.Run(); err != nil {

```

> TOOL

tool_result
id: call_yBLQVT22O3MYx6451iEQbcj1
```
Chunk ID: 7bb7c9
Wall time: 0.0000 seconds
Process exited with code 0
Original token count: 421
Output:
     1	# Task Group: `Projects/yyork` in-app browser readiness, Agentation delivery, portless routing, and bundled Browser plugin internals [chronicle memory]
     2	scope: Use for recent `yyork` work around the Browser tab/IAB path, Agentation annotation delivery, portless-backed local routing, and local inspection of Codex’s bundled Browser plugin files when the user is tracing the real control path or debugging why preview behavior differs from the expected proxied app.
     3	applies_to: cwd=/home/<USER>/Projects/yyork plus local Browser-plugin cache paths under /home/<USER>/.codex/plugins/cache/openai-bundled/browser/*; reuse_rule=safe for similar yyork browser-preview and local Browser-plugin forensics on this machine, but re-open the current `yyork` dev scripts, preview host wiring, and installed plugin version before claiming exact runtime behavior
    51	- The Browser-preview path in `yyork` depends on the proxied/preview route, not a raw loopback iframe: the missing bottom-right Agentation component was described as injected through the preview proxy script, with the expected bundle at `cmd/yyork/dashboard/app/yyork_browser/agentation.js` produced by `web/vite.preview.config.ts` [Task 2][Task 3] [chronicle memory]
    52	- The stable local route shape for this dev flow was `pnpm dev`/`portless run` plus `direnv`-mediated Go tooling, where `yyork.localhost` is the desired app URL and […]

> AGENT

The `https-` prefix comes from yyork’s fallback preview-host slugger, not from Portless. In [internal/server/browser_preview.go](/home/<USER>/Projects/yyork/internal/server/browser_preview.go:265), `browserPreviewHostForOrigin()` builds:

```text
{scheme}-{normalized-host}-preview.yyork.localhost
```

So `https://yyork.localhost/...` can become:

```text
https-yyork-localhost-preview.yyork.localhost
```

But the intended yyork self-preview path is `yyork-preview.yyork.localhost`: [internal/server/browser_preview.go](/home/<USER>/Projects/yyork/internal/server/browser_preview.go:304) special-cases `yyork.localhost`. Also, an explicit `previewName` wins first: [internal/server/browser_preview.go](/home/<USER>/Projects/yyork/internal/server/browser_preview.go:251). So the URL you pasted suggests the registration got a name like `https://yyork.localhost`, or missed the self-preview path somehow.

For two agents: today the Browser panel sends only `previewName={projectName}`: [canvas-panel.tsx](/home/<USER>/Projects/yyork/web/src/features/home/<USER>/organisms/canvas-panel.tsx:206). The server stores preview targets in a map keyed by preview host. If two sessions in the same project both register `yyork-preview.yyork.localhost`, the later registration can overwrite the target for that host. Existing frames may keep what they already loaded, but reloads, navigations, and later proxied requests can route to the most recent target.

Your proposed shape is the right direction. I’d make the frontend send a session-scoped preview name, probably:

```text
{sessionId}-{projectName}
```

which the existing server would turn into:

```text
https://{sessionId}-{projectName}-preview.yyork.localhost
```

That keeps the proxy map distinct per agent/worktree without needing a backend protocol change.

<oai-mem-citation>
<citation_entries>
MEMORY.md:51-52|note=[confirmed yyork preview route and portless shape]
MEMORY.md:1-3|note=[matched yyork browser preview context]
</citation_entries>
<rollout_ids>
</rollout_ids>
</oai-mem-citation>