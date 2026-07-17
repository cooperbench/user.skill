> DEVELOPER

can you take a look at https://github.com/entireio/git-sync/issues/70

> AGENT

I'll fetch the issue.

> TOOL

tool_use Bash
id: toolu_01TzbyBEB6SRxrob37iUgVLv
```json
{
  "command": "gh issue view 70 --repo entireio/git-sync --comments",
  "description": "View GitHub issue 70"
}
```

> TOOL

tool_result
id: toolu_01TzbyBEB6SRxrob37iUgVLv
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01Gp9V5FcgARHgi41Mmm46xy
```json
{
  "command": "gh issue view 70 --repo entireio/git-sync 2>&1; echo \"---EXIT: $?---\"",
  "description": "View GitHub issue 70 with error"
}
```

> TOOL

tool_result
id: toolu_01Gp9V5FcgARHgi41Mmm46xy
```
title:	post RPC stream body: http 408 error
state:	OPEN
author:	itviewer (Jack Ma)
labels:	
comments:	0
assignees:	
projects:	
milestone:	
number:	70
--
```
git-sync sync --progress -v \
  --branch yukawa-android-16 \
  --target-token "ghp_mytoken" \
  https://gitlab.baylibre.com/baylibre/amlogic/atv/aosp/device/amlogic/yukawa-kernel.git \
  https://github.com/aosp-latest/test.git

time=2026-06-11T16:14:01.649+08:00 level=INFO msg="bootstrap fetching refs from source" ref_count=1
time=2026-06-11T16:14:07.026+08:00 level=INFO msg="bootstrap pushing refs to target" ref_count=1
source: Enumerating objects: 17387, done.
source: Counting objects:  99% (664/670)
gitlab.baylibre.com → 4.59 KB @ 402 B/s ✓  │  479 B @ 39 B/s ✓ → github.com
error: sync: sync: bootstrap execute: push target refs: target receive-pack: post RPC stream body: http 408: https://github.com/aosp-latest/test.git/git-receive-pack [X-Github-Request-Id=BC38:3323DF:7AC1EE:7BBAEA:6A2A6E4F, Server=GitHub-Babel/3.0, Content-Type=text/plain; charset=UTF-8]
```
This repository
https://gitlab.baylibre.com/baylibre/amlogic/atv/aosp/device/amlogic/yukawa-kernel.git
might be somewhat unusual; it stores compiled kernels and kernel modules, and is frequently updated via CI, resulting in a large repository size. I wonder if that is the reason.
---EXIT: 0---
```

> AGENT

Let me explore the codebase to understand how pushes work.

> TOOL

tool_use Bash
id: toolu_016AJupvFwqRNN65qpzPSAyS
```json
{
  "command": "ls && echo \"---\" && git log --oneline -5",
  "description": "List repo and recent log"
}
```

> TOOL

tool_result
id: toolu_016AJupvFwqRNN65qpzPSAyS
```
CHANGELOG.md
client_test.go
client.go
cmd
CODE_OF_CONDUCT.md
CONTRIBUTING.md
doc.go
docs
errors_test.go
errors.go
example_test.go
go.mod
go.sum
internal
internalbridge
LICENSE
mise-tasks
mise.toml
README.md
SECURITY.md
tmp
types.go
unstable
---
2ace4367 Merge pull request #74 from entireio/fix/pack-less-ref-create-empty-pack
462a28b2 gitproto: send empty pack on pack-less ref creates
12e0ac60 Merge pull request #73 from entireio/fix/ref-rejected-value-target
06be8477 gitproto: classify target-ref moves by extracting CommandStatusErr robustly
92066eeb Merge pull request #71 from entireio/errors/target-ref-moved
```

> TOOL

tool_use Bash
id: toolu_012g2MU3pQ9Ejxp5mYYBgyHN
```json
{
  "command": "find internal -type d | head -50 && echo \"---FILES with receive-pack / RPC stream---\" && grep -rl \"RPC stream\\|receive-pack\\|git-receive-pack\" --include=\"*.go\" . | head",
  "description": "Find push-related code"
}
```

> TOOL

tool_result
id: toolu_012g2MU3pQ9Ejxp5mYYBgyHN
```
internal
internal/useragent
internal/gitproto
internal/auth
internal/planner
internal/syncer
internal/syncertest
internal/validation
internal/convert
internal/strategy
internal/strategy/bootstrap
internal/strategy/incremental
internal/strategy/replicate
internal/strategy/materialized
---FILES with receive-pack / RPC stream---
types.go
client_test.go
cmd/git-sync-bench/main.go
errors.go
cmd/git-sync/bootstrap.go
cmd/git-sync/syncplan.go
cmd/git-sync/main_test.go
internal/gitproto/push_test.go
internal/gitproto/refs_test.go
internal/gitproto/refs.go
```

> TOOL

tool_use Bash
id: toolu_015ZEN6MgAkoedaFMK2Ty3AB
```json
{
  "command": "grep -rn \"post RPC stream body\\|RPC stream body\\|http %d\\|408\\|StatusRequestTimeout\" --include=\"*.go\" internal/gitproto/ | head -30",
  "description": "Find the error message origin"
}
```

> TOOL

tool_result
id: toolu_015ZEN6MgAkoedaFMK2Ty3AB
```
internal/gitproto/smarthttp.go:61:		return fmt.Errorf("http %d: %s [%s] %s", res.StatusCode, res.Request.URL.Redacted(), strings.Join(diag, ", "), reason)
internal/gitproto/smarthttp.go:63:	return fmt.Errorf("http %d: %s %s", res.StatusCode, res.Request.URL.Redacted(), reason)
internal/gitproto/smarthttp.go:468:		return nil, fmt.Errorf("post RPC stream body: %w", err)
```

> TOOL

tool_use Read
id: toolu_019dvgHxXgcSkBHzHE37ccDd
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/gitproto/smarthttp.go"
}
```

> TOOL

tool_result
id: toolu_019dvgHxXgcSkBHzHE37ccDd
```
1	package gitproto
2	
3	import (
4		"bytes"
5		"context"
6		"crypto/tls"
7		"fmt"
8		"io"
9		"mime"
10		"net/http"
11		"net/http/httptrace"
12		"net/http/httputil"
13		"net/url"
14		"os"
15		"strings"
16	
17		"entire.io/entire/git-sync/internal/useragent"
18		transporthttp "github.com/go-git/go-git/v6/plumbing/transport/http"
19	)
20	
21	const maxHTTPErrorBody = 64 * 1024
22	
23	// diagnosticHeaders carry trace/correlation IDs that operators of upstream
24	// services use to look up the failing request server-side. Surfaced in
25	// httpError so a 500 with an opaque body (e.g. "Internal Server Error") still
26	// gives the user something actionable to share when reporting the failure.
27	var diagnosticHeaders = []string{
28		"Cf-Ray",
29		"X-Request-Id",
30		"Request-Id",
31		"X-Trace-Id",
32		"X-Amz-Request-Id",
33		"X-Github-Request-Id",
34		"Server",
35		"Content-Type",
36	}
37	
38	// httpError checks an HTTP response status and returns an error for non-2xx responses.
39	func httpError(res *http.Response) error {
40		if res.StatusCode >= http.StatusOK && res.StatusCode < http.StatusMultipleChoices {
41			return nil
42		}
43		var reason string
44		if res.Body != nil {
45			limited := io.LimitReader(res.Body, maxHTTPErrorBody+1)
46			data, err := io.ReadAll(limited)
47			if err == nil && len(data) > 0 {
48				if len(data) > maxHTTPErrorBody {
49 […]

> AGENT

Let me look at how the bootstrap strategy streams data and the push implementation.

> TOOL

tool_use Bash
id: toolu_01QEVwwAYeb7HSGEcW7717nS
```json
{
  "command": "ls internal/gitproto/ && echo \"---\" && ls internal/strategy/bootstrap/ && echo \"---PUSH---\" && grep -n \"MultiReader\\|io.Pipe\\|PostRPCStreamBody\\|receive-pack\\|func .*[Pp]ush\" internal/gitproto/push.go | head -40",
  "description": "Inspect push and bootstrap"
}
```

> TOOL

tool_result
id: toolu_01QEVwwAYeb7HSGEcW7717nS
```
benchmark_test.go
capability_test.go
capability.go
commitparents_test.go
commitparents.go
conn.go
convert_test.go
convert.go
fetch_helpers_test.go
fetch_test.go
fetch.go
pktline_test.go
pktline.go
push_test.go
push.go
refs_test.go
refs.go
smarthttp_test.go
smarthttp.go
ssh_test.go
ssh.go
target_features_test.go
target_features.go
---
bootstrap_test.go
bootstrap.go
pack_observer_test.go
pack_observer.go
---PUSH---
34:// Pusher wraps target-side receive-pack state behind a smaller execution API.
49:func NewPusher(conn Conn, adv *packp.AdvRefs, verbose bool) *Pusher {
54:func (p *Pusher) PushPack(ctx context.Context, commands []PushCommand, pack io.ReadCloser) error {
60:func (p *Pusher) PushCommands(ctx context.Context, commands []PushCommand) error {
65:func (p *Pusher) PushObjects(ctx context.Context, commands []PushCommand, store storer.Storer, hashes []plumbing.Hash) error {
69:// buildUpdateRequest builds the receive-pack update request.
108:// leaseFailureMarkers are receive-pack ng reason substrings that indicate the
119:// IsLeaseFailure reports whether a receive-pack ng reason indicates the
134:// override hint. Other receive-pack errors pass through unchanged.
155:// receive-pack report-status. Ref is the rejected ref; Reason is the raw,
171:	Reason string // raw receive-pack ng reason, e.g. "remote ref has changed"
187:// Unwrap exposes the underlying receive-pack error so existing
199:// concurrentMoveMarkers are receive-pack ng reasons that UNAMBIGUOUSLY mean the
224:// isConcurrentMove reports whether a receive-pack ng reason is an unambiguous
258:// asRefRejectedError wraps a target receive-pack report-status "ng" error in
277:// sendReceivePack encodes and POSTs a receive-pack request, then decodes the report.
290: […]

> TOOL

tool_use Read
id: toolu_012m4Kf8GxWacDadNfhtryWv
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/gitproto/push.go",
  "offset": 277,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_012m4Kf8GxWacDadNfhtryWv
```
277	// sendReceivePack encodes and POSTs a receive-pack request, then decodes the report.
278	func sendReceivePack(
279		ctx context.Context,
280		conn Conn,
281		req *packp.UpdateRequests,
282		packData io.Reader,
283		verbose bool,
284		onRejection func(plumbing.ReferenceName, string),
285	) error {
286		var header bytes.Buffer
287		if err := req.Encode(&header); err != nil {
288			return fmt.Errorf("encode update-request: %w", err)
289		}
290		// The push body is io.MultiReader(header, packData); packData comes
291		// from a live upload-pack pipe and isn't rewindable, so a mid-stream
292		// 401 can't trigger PostRPCStreamBody's normal helper retry. Probe
293		// for auth requirements with a same-shape POST first.
294		if hc, ok := conn.(*HTTPConn); ok {
295			hc.EnsureAuthForService(ctx, transport.ReceivePackService)
296		}
297		body := io.Reader(bytes.NewReader(header.Bytes()))
298		if packData != nil {
299			body = io.MultiReader(body, packData)
300		}
301		reader, err := PostRPCStreamBody(ctx, conn, transport.ReceivePackService, body, false, "receive-pack push")
302		if err != nil {
303			return fmt.Errorf("target receive-pack: %w", err)
304		}
305		defer reader.Close()
306	
307		// Unwrap sideband if negotiated; stream server-side progress to stderr
308		// when verbose so long-running pushes show "Resolving deltas ..." etc.
309		var respReader io.Reader = reader
310		switch {
311		case […]

> TOOL

tool_use Read
id: toolu_012qyLBV8pLE85E3os4CWjwz
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go"
}
```

> TOOL

tool_result
id: toolu_012qyLBV8pLE85E3os4CWjwz
```
<system-reminder>[Truncated: PARTIAL view — showing lines 1-1267 of 1497 total (25105 tokens, cap 25000). Call Read with offset=1268 limit=1267 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>

1	// Package bootstrap implements the bootstrap relay strategy for git-sync.
2	// This handles initial seeding of an empty target, both one-shot and batched.
3	package bootstrap
4	
5	import (
6		"bytes"
7		"context"
8		"encoding/json"
9		"errors"
10		"fmt"
11		"io"
12		"log/slog"
13		"net/http"
14		"regexp"
15		"strconv"
16		"strings"
17		"sync"
18	
19		git "github.com/go-git/go-git/v6"
20		"github.com/go-git/go-git/v6/plumbing"
21	
22		"entire.io/entire/git-sync/internal/convert"
23		"entire.io/entire/git-sync/internal/gitproto"
24		"entire.io/entire/git-sync/internal/planner"
25		"entire.io/entire/git-sync/internal/useragent"
26	)
27	
28	const (
29		defaultTargetMaxPackBytes  = 512 * 1024 * 1024
30		githubLargeRepoThresholdKB = 1536 * 1024
31	)
32	
33	var bodyLimitPattern = regexp.MustCompile(`body exceeded size limit ([0-9]+)`)
34	
35	// GitHubRepoAPIBaseURL is the base for GitHub API calls (replaceable in tests).
36	var GitHubRepoAPIBaseURL = "https://api.github.com"
37	
38	// Params holds the inputs for a bootstrap execution.
39	type Params struct {
40		SourceConn    gitproto.Conn
41		SourceService interface {
42			FetchPack(ctx context.Context, conn gitproto.Conn, […]

> TOOL

tool_use Bash
id: toolu_01A93oyxReBcw4jCmL3twBDi
```json
{
  "command": "grep -n \"408\\|RequestTimeout\\|githubBatchLimit\\|githubLargeRepo\\|isTargetBodyLimitError\\|autoTargetMaxPackBytes\\|StatusRequestTimeout\\|timeout\" internal/strategy/bootstrap/bootstrap.go",
  "description": "Search 408 and github preflight handling"
}
```

> TOOL

tool_result
id: toolu_01A93oyxReBcw4jCmL3twBDi
```
30:	githubLargeRepoThresholdKB = 1536 * 1024
136:	if batchLimit, ok := githubBatchLimit(ctx, p); ok {
180:		autoBatch, ok := autoTargetMaxPackBytes(p, pushErr)
504:				sizeIssue := abortedEarly || isTargetBodyLimitError(pushErr)
1304:func githubBatchLimit(ctx context.Context, p Params) (int64, bool) {
1312:	if !ok || repoSizeKB < githubLargeRepoThresholdKB {
1380:func autoTargetMaxPackBytes(p Params, err error) (int64, bool) {
1381:	if p.TargetMaxPack > 0 || !isTargetBodyLimitError(err) {
1430:func isTargetBodyLimitError(err error) bool {
```

> TOOL

tool_use Read
id: toolu_016HvXDwGgHr3g9MjM7wChct
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "offset": 1290,
  "limit": 207
}
```

> TOOL

tool_result
id: toolu_016HvXDwGgHr3g9MjM7wChct
```
1290		completedRefs map[plumbing.ReferenceName]plumbing.Hash,
1291		batchLimit int64,
1292	) (io.ReadCloser, error) {
1293		desired := singleGP(batch.Plan.SourceRef, batch.TempRef, checkpoint)
1294		haves := buildCheckpointHaves(batch.TempRef, pushedCheckpoints, completedRefs)
1295		packReader, err := p.SourceService.FetchPack(ctx, p.SourceConn, desired, haves)
1296		if err != nil {
1297			return nil, fmt.Errorf("fetch checkpoint pack: %w", err)
1298		}
1299		return gitproto.LimitPackReader(packReader, batchLimit), nil
1300	}
1301	
1302	// --- GitHub preflight ---
1303	
1304	func githubBatchLimit(ctx context.Context, p Params) (int64, bool) {
1305		if p.TargetMaxPack > 0 || p.SourceConn == nil || p.SourceConn.Endpoint() == nil {
1306			return 0, false
1307		}
1308		if p.SourceService == nil || !p.SourceService.SupportsBootstrapBatch() {
1309			return 0, false
1310		}
1311		repoSizeKB, ok := lookupGitHubRepoSizeKB(ctx, p.SourceConn)
1312		if !ok || repoSizeKB < githubLargeRepoThresholdKB {
1313			return 0, false
1314		}
1315		limit := int64(defaultTargetMaxPackBytes)
1316		if p.MaxPackBytes > 0 && p.MaxPackBytes < limit {
1317			limit = p.MaxPackBytes
1318		}
1319		if limit <= 0 {
1320			return 0, false
1321		}
1322		return limit, true
1323	}
1324	
1325	func lookupGitHubRepoSizeKB(ctx context.Context, conn gitproto.Conn) (int64, bool) {
1326		httpConn, ok := conn.(*gitproto.HTTPConn)
1327		if !ok {
1328			return 0, false
1329		}
1330		owner, repo, ok := GitHubOwnerRepo(conn)
1331		if […]

> AGENT

Let me check whether 408 is handled anywhere in the retry/syncer layer and how `--target-max-pack-bytes` is wired.

> TOOL

tool_use Bash
id: toolu_01Rt7S7pDwZBQ1c659B3yiBg
```json
{
  "command": "grep -rn \"408\\|RequestTimeout\\|target-max-pack\\|TargetMaxPack\\|retry\\|Retry\" --include=\"*.go\" cmd/ internal/syncer/ | grep -iv \"_test.go\" | head -40",
  "description": "Search 408 and retry handling in syncer/cmd"
}
```

> TOOL

tool_result
id: toolu_01Rt7S7pDwZBQ1c659B3yiBg
```
cmd/git-sync-bench/main.go:117:	fs.Int64Var(&cfg.Options.TargetMaxPackBytes, "target-max-pack-bytes", 0, "target receive-pack body size limit; batches are planned and auto-subdivided to fit")
cmd/git-sync-bench/main.go:462:	usage := fmt.Sprintf("usage:\n  %s --source-url <repo> [flags]\n\nflags:\n  --scenario bootstrap|sync\n  --repeat 3\n  --work-dir /tmp/git-sync-bench\n  --keep-targets\n  --json\n  --branch main,release\n  --map main:stable\n  --tags\n  --force-with-lease\n  --force-blind\n  --prune\n  --stats\n  --measure-memory\n  --max-pack-bytes 104857600\n  --target-max-pack-bytes 104857600\n  --protocol auto|v1|v2\n  -v\n", os.Args[0])
cmd/git-sync/bootstrap.go:84:	cmd.Flags().Int64Var(&req.Options.TargetMaxPackBytes, "target-max-pack-bytes", 0, "target receive-pack body size limit; batches are planned and auto-subdivided to fit")
cmd/git-sync/syncplan.go:143:	cmd.Flags().Int64Var(&req.Options.TargetMaxPackBytes, "target-max-pack-bytes", 0, "target receive-pack body size limit; batches are planned and auto-subdivided to fit")
cmd/git-sync/internal/sha256convert/sha256convert.go:264:	// config/objects/refs/HEAD behind, and the next retry hits
cmd/git-sync/internal/sha256convert/sha256convert.go:388:	// retry on ensureEmptyTarget; arm the deferred cleanup now.
internal/syncer/syncer.go:87:	TargetMaxPackBytes     int64
internal/syncer/syncer.go:1132:		MaxPackBytes:     s.cfg.MaxPackBytes, TargetMaxPack: s.cfg.TargetMaxPackBytes,
```

> AGENT

I've dug through the issue and the relevant code. Here's my read.

## What's happening

The user is doing a one-shot bootstrap relay from a GitLab source to a fresh GitHub target. git-sync streams the pack straight from the source's `upload-pack` into the target's `receive-pack` POST (`bootstrap.Execute` → `PushPack` → `sendReceivePack`, which builds an `io.MultiReader(header, packData)` and POSTs it at `internal/gitproto/push.go:301`).

GitHub returns **HTTP 408 (Request Timeout)** on `git-receive-pack`. GitHub enforces a wall-clock deadline on the receive-pack POST. The repo is large (compiled kernels/modules = big blobs), and the relay is bottlenecked by a very slow source — the progress line shows `gitlab.baylibre.com → 4.59 KB @ 402 B/s` feeding `479 B @ 39 B/s → github.com`. Because it's a direct relay, the slow GitLab read rate-limits the GitHub write, the single giant POST runs past GitHub's deadline, and GitHub kills it with 408. So the user's instinct in the issue is right: repo size (combined with slow source throughput) is the cause.

## Why git-sync doesn't auto-recover here

There's already good machinery for "pack too big for the target" — batched bootstrap with checkpointing and auto-subdivision. But none of it triggers for this case:

1. **GitHub preflight** (`githubBatchLimit`, `bootstrap.go:1304`) […]

> DEVELOPER

let's implement the fix in a new branch, do meaningful commits, run /simplify when done

> AGENT

Let me create the branch and look at existing tests for the classifier functions to mirror their style.

> TOOL

tool_use Bash
id: toolu_01VMiZWXeRrqZTGeowDkkakj
```json
{
  "command": "git checkout -b fix/target-push-timeout-batched-retry 2>&1 | tail -2 && echo \"---TESTS---\" && grep -n \"isTargetBodyLimitError\\|autoTargetMaxPackBytes\\|TestAuto\\|TestIsTarget\\|switching to batched\\|http 413\" internal/strategy/bootstrap/bootstrap_test.go",
  "description": "Create branch and find existing tests"
}
```

> TOOL

tool_result
id: toolu_01VMiZWXeRrqZTGeowDkkakj
```
Switched to a new branch 'fix/target-push-timeout-batched-retry'
---TESTS---
87:func TestIsTargetBodyLimitError(t *testing.T) {
137:			got := isTargetBodyLimitError(tt.err)
139:				t.Errorf("isTargetBodyLimitError(%v) = %v, want %v", tt.err, got, tt.want)
```

> TOOL

tool_use Read
id: toolu_01PnncwbPd2UcrerhtBktikZ
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "offset": 87,
  "limit": 160
}
```

> TOOL

tool_result
id: toolu_01PnncwbPd2UcrerhtBktikZ
```
87	func TestIsTargetBodyLimitError(t *testing.T) {
88		tests := []struct {
89			name string
90			err  error
91			want bool
92		}{
93			{
94				name: "nil error",
95				err:  nil,
96				want: false,
97			},
98			{
99				name: "body exceeded size limit",
100				err:  errors.New("body exceeded size limit 1048576"),
101				want: true,
102			},
103			{
104				name: "case insensitive body exceeded",
105				err:  errors.New("Body Exceeded Size Limit 999"),
106				want: true,
107			},
108			{
109				name: "request body too large",
110				err:  errors.New("request body is too large"),
111				want: true,
112			},
113			{
114				name: "payload too large",
115				err:  errors.New("payload is too large for this endpoint"),
116				want: true,
117			},
118			{
119				name: "HTTP 413",
120				err:  errors.New("server returned HTTP 413"),
121				want: true,
122			},
123			{
124				name: "unrelated error",
125				err:  errors.New("connection refused"),
126				want: false,
127			},
128			{
129				name: "partial match body without too large",
130				err:  errors.New("request body is fine"),
131				want: false,
132			},
133		}
134	
135		for _, tt := range tests {
136			t.Run(tt.name, func(t *testing.T) {
137				got := isTargetBodyLimitError(tt.err)
138				if got != tt.want {
139 […]

> TOOL

tool_use Bash
id: toolu_01RoWW3qbDuBd1cDCejxAvNv
```json
{
  "command": "grep -n \"autoTargetMaxPackBytes\\|func TestExecute\\|SupportsBootstrapBatch\\|switching to batched\\|fakeSource\\|stubSource\\|TargetPusher\" internal/strategy/bootstrap/bootstrap_test.go | head -40",
  "description": "Find executor tests and fakes"
}
```

> TOOL

tool_result
id: toolu_01RoWW3qbDuBd1cDCejxAvNv
```
1132:func TestExecuteBatchedSubsumedBranchSkipsPack(t *testing.T) {
1169:		TargetPusher: fakeBootstrapPusher{
1241:func (fakeBootstrapSource) SupportsBootstrapBatch() bool { return true }
1318:func TestExecuteOneShotUsesTargetPusher(t *testing.T) {
1335:		TargetPusher: fakeBootstrapPusher{
1366:func TestExecuteOneShotClosesPackOnPushError(t *testing.T) {
1377:		TargetPusher: fakeBootstrapPusher{
1400:func TestExecuteOneShotClosesPackWhenPusherDoesNot(t *testing.T) {
1411:		TargetPusher: fakeBootstrapPusher{
1433:func TestExecuteBatchedClosesCheckpointPackOnPushError(t *testing.T) {
1449:		TargetPusher: fakeBootstrapPusher{
1474:func TestExecuteBatchedClosesCheckpointPackOnReadInterruption(t *testing.T) {
1490:		TargetPusher: fakeBootstrapPusher{
1516:func TestExecuteRequiresTargetPusherBeforeFetch(t *testing.T) {
1549:			if err == nil || err.Error() != "bootstrap strategy requires TargetPusher" {
1550:				t.Fatalf("Execute() error = %v, want missing TargetPusher", err)
1559:func TestExecuteRequiresTargetPusherBeforeGitHubPreflight(t *testing.T) {
1597:	if err == nil || err.Error() != "bootstrap strategy requires TargetPusher" {
1598:		t.Fatalf("Execute() error = %v, want missing TargetPusher", err)
```

> TOOL

tool_use Read
id: toolu_01R669YHWvCfZVqNJoVQ9iLU
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "offset": 1190,
  "limit": 130
}
```

> TOOL

tool_result
id: toolu_01R669YHWvCfZVqNJoVQ9iLU
```
1190		}
1191	
1192		if graphFetches != 1 {
1193			t.Errorf("fetchCommitGraph called %d times, want 1 (trunk only)", graphFetches)
1194		}
1195		if packFetches != 1 {
1196			t.Errorf("fetchPack called %d times, want 1 (trunk only)", packFetches)
1197		}
1198		if pushPackCalls != 1 {
1199			t.Errorf("PushPack called %d times, want 1 (trunk only)", pushPackCalls)
1200		}
1201	
1202		var foundFeatureCreate bool
1203		for _, cmds := range pushCommandsBatches {
1204			for _, cmd := range cmds {
1205				if cmd.Name == featureRef && cmd.New == featureHash && cmd.Old == plumbing.ZeroHash && !cmd.Delete {
1206					foundFeatureCreate = true
1207				}
1208			}
1209		}
1210		if !foundFeatureCreate {
1211			t.Fatalf("expected ref-create command for feature at %s; got %v", featureHash, pushCommandsBatches)
1212		}
1213	}
1214	
1215	type fakeBootstrapSource struct {
1216		fetchPack          func(context.Context, gitproto.Conn, map[plumbing.ReferenceName]gitproto.DesiredRef, map[plumbing.ReferenceName]plumbing.Hash) (io.ReadCloser, error)
1217		fetchCommitParents func(context.Context, gitproto.Conn, gitproto.DesiredRef, []plumbing.Hash) (map[plumbing.Hash][]plumbing.Hash, error)
1218	}
1219	
1220	func (f fakeBootstrapSource) FetchPack(
1221		ctx context.Context,
1222		conn gitproto.Conn,
1223		desired map[plumbing.ReferenceName]gitproto.DesiredRef,
1224		targetRefs map[plumbing.ReferenceName]plumbing.Hash,
1225	) (io.ReadCloser, error) {
1226		return f.fetchPack(ctx, conn, desired, targetRefs)
1227	}
1228	
1229	func (f fakeBootstrapSource) FetchCommitParents(
1230		ctx context.Context,
1231		conn gitproto.Conn,
1232		ref gitproto.DesiredRef,
1233		haves […]

> TOOL

tool_use Read
id: toolu_01DFMNfV5QCP9iVUtg8Su691
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "offset": 1318,
  "limit": 120
}
```

> TOOL

tool_result
id: toolu_01DFMNfV5QCP9iVUtg8Su691
```
1318	func TestExecuteOneShotUsesTargetPusher(t *testing.T) {
1319		mainRef := plumbing.NewBranchReferenceName("main")
1320		mainHash := plumbing.NewHash("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
1321	
1322		var gotDesired map[plumbing.ReferenceName]gitproto.DesiredRef
1323		var gotCommands []gitproto.PushCommand
1324	
1325		result, err := Execute(context.Background(), Params{
1326			SourceService: fakeBootstrapSource{
1327				fetchPack: func(_ context.Context, _ gitproto.Conn, desired map[plumbing.ReferenceName]gitproto.DesiredRef, targetRefs map[plumbing.ReferenceName]plumbing.Hash) (io.ReadCloser, error) {
1328					gotDesired = desired
1329					if targetRefs != nil {
1330						t.Fatalf("expected nil target refs during one-shot bootstrap fetch, got %v", targetRefs)
1331					}
1332					return io.NopCloser(bytes.NewReader([]byte("PACK"))), nil
1333				},
1334			},
1335			TargetPusher: fakeBootstrapPusher{
1336				pushPack: func(_ context.Context, cmds []gitproto.PushCommand, pack io.ReadCloser) error {
1337					defer pack.Close()
1338					gotCommands = append([]gitproto.PushCommand(nil), cmds...)
1339					return nil
1340				},
1341			},
1342			DesiredRefs: map[plumbing.ReferenceName]planner.DesiredRef{
1343				mainRef: {
1344					SourceRef:  mainRef,
1345					TargetRef:  mainRef,
1346					SourceHash: mainHash,
1347					Kind:       planner.RefKindBranch,
1348				},
1349			},
1350			TargetRefs: map[plumbing.ReferenceName]plumbing.Hash{},
1351		}, "empty target")
1352		if err != nil {
1353			t.Fatalf("Execute() error = %v", err)
1354		}
1355		if result.Pushed != 1 || !result.Relay || result.RelayMode != "bootstrap" || result.RelayReason != "empty target" {
1356			t.Fatalf("unexpected result: %+v", result)
1357		}
1358		if gotDesired[mainRef].SourceHash != mainHash {
1359			t.Fatalf("desired source hash = %s, want %s", gotDesired[mainRef].SourceHash, mainHash)
1360		}
1361		if len(gotCommands) != 1 || […]

> AGENT

Now I understand the patterns. Let me implement. First, the classifier helpers and wiring (commit 1).

> TOOL

tool_use Edit
id: toolu_016rMDdMkyYojQNS7ay1aSXg
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "func isTargetBodyLimitError(err error) bool {\n\tif err == nil {\n\t\treturn false\n\t}\n\tmsg := strings.ToLower(err.Error())\n\treturn strings.Contains(msg, \"body exceeded size limit\") ||\n\t\t(strings.Contains(msg, \"request body\") && strings.Contains(msg, \"too large\")) ||\n\t\t(strings.Contains(msg, \"payload\") && strings.Contains(msg, \"too large\")) ||\n\t\tstrings.Contains(msg, \"http 413\")\n}",
  "new_string": "func isTargetBodyLimitError(err error) bool {\n\tif err == nil {\n\t\treturn false\n\t}\n\tmsg := strings.ToLower(err.Error())\n\treturn strings.Contains(msg, \"body exceeded size limit\") ||\n\t\t(strings.Contains(msg, \"request body\") && strings.Contains(msg, \"too large\")) ||\n\t\t(strings.Contains(msg, \"payload\") && strings.Contains(msg, \"too large\")) ||\n\t\tstrings.Contains(msg, \"http 413\")\n}\n\n// isTargetPushDeadlineError reports whether err indicates the target cut the\n// receive-pack POST short because it ran past a server-side deadline rather\n// than because the pack exceeded an announced size limit. GitHub returns 408\n// (Request Timeout) when a slow or oversized push outlasts its receive-pack\n// wall-clock window — common when relaying a large repo over a slow source\n// link, where the upstream read rate throttles the downstream write. Gateways\n// fronting other hosts surface the same condition as 504 (Gateway Timeout).\n//\n// Both are remedied the way a body-limit rejection is: smaller packs each\n// finish inside the window, so callers route them into the same batched\n// bootstrap retry. Kept distinct from isTargetBodyLimitError because the\n// trigger is a timeout, not a size rejection, and there's no body […]

> TOOL

tool_result
id: toolu_016rMDdMkyYojQNS7ay1aSXg
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_016gvj2E4rz7VuJy7dqt9WMe
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "func autoTargetMaxPackBytes(p Params, err error) (int64, bool) {\n\tif p.TargetMaxPack > 0 || !isTargetBodyLimitError(err) {\n\t\treturn 0, false\n\t}",
  "new_string": "func autoTargetMaxPackBytes(p Params, err error) (int64, bool) {\n\tif p.TargetMaxPack > 0 || !isBatchableTargetPushError(err) {\n\t\treturn 0, false\n\t}"
}
```

> TOOL

tool_result
id: toolu_016gvj2E4rz7VuJy7dqt9WMe
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now the mid-batch subdivision path:

> TOOL

tool_use Edit
id: toolu_01D1oBtywh9rjQN3khtjBwt5
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "\t\t\t\t// Treat abortedEarly the same as a body-limit error:\n\t\t\t\t// both indicate \"this pack is too big for the target\",\n\t\t\t\t// just one is detected by the server and one by us.\n\t\t\t\tsizeIssue := abortedEarly || isTargetBodyLimitError(pushErr)",
  "new_string": "\t\t\t\t// Treat abortedEarly the same as a body-limit error:\n\t\t\t\t// both indicate \"this pack is too big for the target\",\n\t\t\t\t// just one is detected by the server and one by us. A\n\t\t\t\t// receive-pack deadline (408/504) lands here too — a\n\t\t\t\t// checkpoint that times out is also too big for this\n\t\t\t\t// target/link, and subdividing makes each push finish sooner.\n\t\t\t\tsizeIssue := abortedEarly || isBatchableTargetPushError(pushErr)"
}
```

> TOOL

tool_result
id: toolu_01D1oBtywh9rjQN3khtjBwt5
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_0135M9S9zvLhgcKn4nLNLBjg
```json
{
  "command": "go build ./... && go test ./internal/strategy/bootstrap/ 2>&1 | tail -20",
  "description": "Build and test bootstrap package"
}
```

> TOOL

tool_result
id: toolu_0135M9S9zvLhgcKn4nLNLBjg
```
ok  	entire.io/entire/git-sync/internal/strategy/bootstrap	0.348s
```

> AGENT

Now let me add tests for the classifier and the auto-batch-on-timeout path before committing. Let me check the existing one-shot retry test exists:

> TOOL

tool_use Bash
id: toolu_01CRaZcosNDf57XJws337RNL
```json
{
  "command": "grep -n \"TestExecute.*Batch\\|autoBatch\\|switching to batched\\|retrying with batched\\|PlansToPushCommands\\|TestExecuteOneShotRetr\\|TestExecuteAutoBatch\" internal/strategy/bootstrap/bootstrap_test.go",
  "description": "Look for existing auto-batch retry tests"
}
```

> TOOL

tool_result
id: toolu_01CRaZcosNDf57XJws337RNL
```
1132:func TestExecuteBatchedSubsumedBranchSkipsPack(t *testing.T) {
1433:func TestExecuteBatchedClosesCheckpointPackOnPushError(t *testing.T) {
1474:func TestExecuteBatchedClosesCheckpointPackOnReadInterruption(t *testing.T) {
```

> AGENT

Let me add classifier tests right after `TestIsTargetBodyLimitError`:

> TOOL

tool_use Edit
id: toolu_01MQUTKkjSJ44ESessAvdiYx
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "old_string": "func TestTargetBodyLimit(t *testing.T) {",
  "new_string": "func TestIsTargetPushDeadlineError(t *testing.T) {\n\ttests := []struct {\n\t\tname string\n\t\terr  error\n\t\twant bool\n\t}{\n\t\t{name: \"nil error\", err: nil, want: false},\n\t\t{\n\t\t\tname: \"github receive-pack 408\",\n\t\t\terr:  errors.New(\"push target refs: target receive-pack: post RPC stream body: http 408: https://github.com/o/r.git/git-receive-pack\"),\n\t\t\twant: true,\n\t\t},\n\t\t{\n\t\t\tname: \"gateway 504\",\n\t\t\terr:  errors.New(\"target receive-pack: http 504: gateway timeout\"),\n\t\t\twant: true,\n\t\t},\n\t\t{\n\t\t\tname: \"body limit is not a deadline\",\n\t\t\terr:  errors.New(\"body exceeded size limit 1048576\"),\n\t\t\twant: false,\n\t\t},\n\t\t{\n\t\t\tname: \"413 is not a deadline\",\n\t\t\terr:  errors.New(\"http 413: payload too large\"),\n\t\t\twant: false,\n\t\t},\n\t\t{\n\t\t\tname: \"unrelated error\",\n\t\t\terr:  errors.New(\"connection refused\"),\n\t\t\twant: false,\n\t\t},\n\t}\n\n\tfor _, tt := range tests {\n\t\tt.Run(tt.name, func(t *testing.T) {\n\t\t\tif got := isTargetPushDeadlineError(tt.err); got != tt.want {\n\t\t\t\tt.Errorf(\"isTargetPushDeadlineError(%v) = %v, want %v\", tt.err, got, tt.want)\n\t\t\t}\n\t\t})\n\t}\n}\n\nfunc TestIsBatchableTargetPushError(t *testing.T) {\n\ttests := []struct {\n\t\tname string\n\t\terr  error\n\t\twant bool\n\t}{\n\t\t{name: \"nil error\", err: nil, want: false},\n\t\t{name: \"body limit\", err: errors.New(\"body exceeded size limit 1048576\"), want: true},\n\t\t{name: \"http 413\", err: errors.New(\"http 413\"), want: true},\n\t\t{name: \"http 408 deadline\", err: errors.New(\"http 408: request timeout\"), want: true},\n\t\t{name: \"http 504 deadline\", err: errors.New(\"http 504: gateway timeout\"), want: true},\n\t\t{name: \"unrelated\", err: errors.New(\"connection refused\"), want: false},\n\t}\n\n\tfor _, tt := range tests {\n\t\tt.Run(tt.name, func(t *testing.T) {\n\t\t\tif got := isBatchableTargetPushError(tt.err); got != tt.want {\n\t\t\t\tt.Errorf(\"isBatchableTargetPushError(%v) = %v, want %v\", tt.err, got, tt.want)\n\t\t\t}\n\t\t})\n\t}\n}\n\nfunc TestTargetBodyLimit(t *testing.T) {"
}
```

> TOOL

tool_result
id: toolu_01MQUTKkjSJ44ESessAvdiYx
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01FSUpMJavcDCTTB8tesFvQL
```json
{
  "command": "go test ./internal/strategy/bootstrap/ -run 'TestIsTarget|TestIsBatchable' -v 2>&1 | tail -30",
  "description": "Run classifier tests"
}
```

> TOOL

tool_result
id: toolu_01FSUpMJavcDCTTB8tesFvQL
```
=== RUN   TestIsTargetPushDeadlineError
=== RUN   TestIsTargetPushDeadlineError/nil_error
=== RUN   TestIsTargetPushDeadlineError/github_receive-pack_408
=== RUN   TestIsTargetPushDeadlineError/gateway_504
=== RUN   TestIsTargetPushDeadlineError/body_limit_is_not_a_deadline
=== RUN   TestIsTargetPushDeadlineError/413_is_not_a_deadline
=== RUN   TestIsTargetPushDeadlineError/unrelated_error
--- PASS: TestIsTargetPushDeadlineError (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/nil_error (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/github_receive-pack_408 (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/gateway_504 (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/body_limit_is_not_a_deadline (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/413_is_not_a_deadline (0.00s)
    --- PASS: TestIsTargetPushDeadlineError/unrelated_error (0.00s)
=== RUN   TestIsBatchableTargetPushError
=== RUN   TestIsBatchableTargetPushError/nil_error
=== RUN   TestIsBatchableTargetPushError/body_limit
=== RUN   TestIsBatchableTargetPushError/http_413
=== RUN   TestIsBatchableTargetPushError/http_408_deadline
=== RUN   TestIsBatchableTargetPushError/http_504_deadline
=== RUN   TestIsBatchableTargetPushError/unrelated
--- PASS: TestIsBatchableTargetPushError (0.00s)
    --- PASS: TestIsBatchableTargetPushError/nil_error (0.00s)
    --- PASS: TestIsBatchableTargetPushError/body_limit (0.00s)
    --- PASS: TestIsBatchableTargetPushError/http_413 (0.00s)
    --- PASS: TestIsBatchableTargetPushError/http_408_deadline (0.00s)
    --- PASS: TestIsBatchableTargetPushError/http_504_deadline (0.00s)
    --- PASS: TestIsBatchableTargetPushError/unrelated (0.00s)
PASS
ok  	entire.io/entire/git-sync/internal/strategy/bootstrap	0.318s
```

> AGENT

Commit 1:

> TOOL

tool_use Bash
id: toolu_01FpoXajNxGCxbncquuxddYP
```json
{
  "command": "git add internal/strategy/bootstrap/bootstrap.go internal/strategy/bootstrap/bootstrap_test.go && git commit -q -F - <<'EOF'\nbootstrap: treat receive-pack timeouts (408/504) as batchable\n\nGitHub kills a receive-pack POST with HTTP 408 when a slow or oversized\npush outlasts its server-side deadline — the failure mode in #70, where\na large GitLab repo relayed over a slow link timed out before the single\none-shot pack finished. Only body-limit rejections (413) previously\ntriggered the batched-bootstrap fallback, so a 408 hard-failed with no\nremediation despite --target-max-pack-bytes being the exact fix.\n\nClassify 408 (and gateway 504) as a receive-pack deadline and route it\nthrough the same batched retry as a size rejection: smaller packs each\nfinish inside the target's window. Applied both to the one-shot\nauto-batch decision and the mid-batch subdivision path.\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <<REDACTED_EMAIL>>\nEOF\ngit log --oneline -1",
  "description": "Commit classifier + wiring"
}
```

> TOOL

tool_result
id: toolu_01FpoXajNxGCxbncquuxddYP
```
81390b1b bootstrap: treat receive-pack timeouts (408/504) as batchable
```

> AGENT

Now commit 2: messaging. Let me update the one-shot retry notice and add an actionable error when batching is impossible.

> TOOL

tool_use Read
id: toolu_017fW7t7tccf8eni6uCge55W
```json
{
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "offset": 177,
  "limit": 18
}
```

> TOOL

tool_result
id: toolu_017fW7t7tccf8eni6uCge55W
```
177		pushErr := p.TargetPusher.PushPack(ctx, cmds, packReader)
178		_ = packReader.Close()
179		if pushErr != nil {
180			autoBatch, ok := autoTargetMaxPackBytes(p, pushErr)
181			if !ok {
182				return result, fmt.Errorf("push target refs: %w", pushErr)
183			}
184			p.log("bootstrap retrying with batched mode after target rejection",
185				"target_max_pack_bytes", autoBatch)
186			p.notice(fmt.Sprintf("target rejected pack — switching to batched mode (limit %s)",
187				humanBytes(autoBatch)))
188			p.TargetMaxPack = autoBatch
189			return executeBatched(ctx, p, plans, result)
190		}
191	
192		result.Pushed = len(plans)
193		return result, nil
194	}
```

> TOOL

tool_use Edit
id: toolu_01PqgY1x38txC7ECesiLDPK7
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "\t\tautoBatch, ok := autoTargetMaxPackBytes(p, pushErr)\n\t\tif !ok {\n\t\t\treturn result, fmt.Errorf(\"push target refs: %w\", pushErr)\n\t\t}\n\t\tp.log(\"bootstrap retrying with batched mode after target rejection\",\n\t\t\t\"target_max_pack_bytes\", autoBatch)\n\t\tp.notice(fmt.Sprintf(\"target rejected pack — switching to batched mode (limit %s)\",\n\t\t\thumanBytes(autoBatch)))\n\t\tp.TargetMaxPack = autoBatch\n\t\treturn executeBatched(ctx, p, plans, result)",
  "new_string": "\t\tautoBatch, ok := autoTargetMaxPackBytes(p, pushErr)\n\t\tif !ok {\n\t\t\treturn result, fmt.Errorf(\"push target refs: %w\", actionableTargetPushError(p, pushErr))\n\t\t}\n\t\treason := \"target rejected pack\"\n\t\tif isTargetPushDeadlineError(pushErr) {\n\t\t\treason = \"target push timed out\"\n\t\t}\n\t\tp.log(\"bootstrap retrying with batched mode after target rejection\",\n\t\t\t\"target_max_pack_bytes\", autoBatch, \"reason\", reason)\n\t\tp.notice(fmt.Sprintf(\"%s — switching to batched mode (limit %s)\",\n\t\t\treason, humanBytes(autoBatch)))\n\t\tp.TargetMaxPack = autoBatch\n\t\treturn executeBatched(ctx, p, plans, result)"
}
```

> TOOL

tool_result
id: toolu_01PqgY1x38txC7ECesiLDPK7
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now add the `actionableTargetPushError` helper near the classifiers:

> TOOL

tool_use Edit
id: toolu_01Ex4oZjEDmxVtA8w711jCb5
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "// isBatchableTargetPushError reports whether err is a target-side push failure\n// that batched bootstrap can work around by sending smaller packs: an explicit\n// body-size rejection (413 / \"body exceeded size limit\") or a receive-pack\n// deadline (408 / 504).\nfunc isBatchableTargetPushError(err error) bool {\n\treturn isTargetBodyLimitError(err) || isTargetPushDeadlineError(err)\n}",
  "new_string": "// isBatchableTargetPushError reports whether err is a target-side push failure\n// that batched bootstrap can work around by sending smaller packs: an explicit\n// body-size rejection (413 / \"body exceeded size limit\") or a receive-pack\n// deadline (408 / 504).\nfunc isBatchableTargetPushError(err error) bool {\n\treturn isTargetBodyLimitError(err) || isTargetPushDeadlineError(err)\n}\n\n// actionableTargetPushError augments a one-shot push failure with guidance\n// when the target rejected the pack for being too large or slow but batched\n// bootstrap couldn't take over — which, on the one-shot path, means the source\n// can't serve the protocol-v2 fetch filter that checkpointing requires. The\n// extra context tells the user why the obvious knob (--target-max-pack-bytes)\n// won't help here, instead of leaving a bare \"http 408\". Returns err unchanged\n// for non-batchable failures or when batching is in fact available.\nfunc actionableTargetPushError(p Params, err error) error {\n\tif !isBatchableTargetPushError(err) {\n\t\treturn err\n\t}\n\tif p.SourceService != nil && p.SourceService.SupportsBootstrapBatch() {\n\t\treturn err\n\t}\n\treturn fmt.Errorf(\"%w (target rejected the pack as […]

> TOOL

tool_result
id: toolu_01Ex4oZjEDmxVtA8w711jCb5
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Edit
id: toolu_01UQgoG6wKaMWC3u5gYzsgQF
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
  "old_string": "\treturn fmt.Errorf(\"%w (target rejected the pack as too large or too slow to receive; \"+\n\t\t\"batched bootstrap could split it into smaller pushes, but the source does not \"+\n\t\t\"support the protocol-v2 fetch filter that requires)\", err)",
  "new_string": "\treturn fmt.Errorf(\"%w (target rejected the pack as too large or too slow to receive; \"+\n\t\t\"batched bootstrap could split it into smaller pushes, but the source does not \"+\n\t\t\"support the protocol-v2 fetch filter batched bootstrap requires)\", err)"
}
```

> TOOL

tool_result
id: toolu_01UQgoG6wKaMWC3u5gYzsgQF
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> AGENT

Now tests for the messaging behavior. Let me add a non-batching source fake and two tests:

> TOOL

tool_use Edit
id: toolu_01GTMUqKU4RNmmiJJEBfQuso
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "old_string": "func TestExecuteBatchedClosesCheckpointPackOnPushError(t *testing.T) {",
  "new_string": "// noBatchSource is a source that can't serve the protocol-v2 fetch filter\n// batched bootstrap needs, so a one-shot push failure has no batched fallback.\ntype noBatchSource struct{ fakeBootstrapSource }\n\nfunc (noBatchSource) SupportsBootstrapBatch() bool { return false }\n\nfunc TestAutoTargetMaxPackBytesTimeoutTriggersBatching(t *testing.T) {\n\tlimit, ok := autoTargetMaxPackBytes(\n\t\tParams{SourceService: fakeBootstrapSource{}},\n\t\terrors.New(\"target receive-pack: http 408: request timeout\"),\n\t)\n\tif !ok {\n\t\tt.Fatal(\"autoTargetMaxPackBytes(408) = not ok, want batched fallback\")\n\t}\n\tif limit != defaultTargetMaxPackBytes {\n\t\tt.Fatalf(\"limit = %d, want default %d\", limit, int64(defaultTargetMaxPackBytes))\n\t}\n}\n\nfunc TestExecuteOneShotTimeoutWithoutBatchSupportIsActionable(t *testing.T) {\n\tmainRef := plumbing.NewBranchReferenceName(\"main\")\n\tmainHash := plumbing.NewHash(\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\")\n\tpushErr := errors.New(\"target receive-pack: post RPC stream body: http 408: request timeout\")\n\n\t_, err := Execute(context.Background(), Params{\n\t\tSourceService: noBatchSource{},\n\t\tTargetPusher: fakeBootstrapPusher{\n\t\t\tpushPack: func(_ context.Context, _ []gitproto.PushCommand, pack io.ReadCloser) error {\n\t\t\t\t_ = pack.Close()\n\t\t\t\treturn pushErr\n\t\t\t},\n\t\t},\n\t\tDesiredRefs: map[plumbing.ReferenceName]planner.DesiredRef{\n\t\t\tmainRef: {SourceRef: mainRef, TargetRef: mainRef, SourceHash: mainHash, Kind: planner.RefKindBranch},\n\t\t},\n\t}, \"empty target\")\n\tif err == nil {\n\t\tt.Fatal(\"Execute() error = nil, want actionable timeout error\")\n\t}\n\tif !errors.Is(err, pushErr) {\n\t\tt.Fatalf(\"Execute() error does not wrap original push error: %v\", err)\n\t}\n\tif !strings.Contains(err.Error(), \"protocol-v2 fetch filter\") {\n\t\tt.Fatalf(\"Execute() error missing batched-bootstrap guidance: %v\", err)\n\t}\n}\n\nfunc TestExecuteBatchedClosesCheckpointPackOnPushError(t *testing.T) {"
}
```

> TOOL

tool_result
id: toolu_01GTMUqKU4RNmmiJJEBfQuso
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01Fw4HRxKFo2CzYG9c1Xo2KQ
```json
{
  "command": "head -30 internal/strategy/bootstrap/bootstrap_test.go | grep -n '\"strings\"\\|import' ",
  "description": "Check strings import present"
}
```

> TOOL

tool_result
id: toolu_01Fw4HRxKFo2CzYG9c1Xo2KQ
```
3:import (
11:	"strings"
```

> TOOL

tool_use Bash
id: toolu_01QC7kwTDGU7GvxSWBeNyA3y
```json
{
  "command": "go test ./internal/strategy/bootstrap/ -run 'TestAutoTargetMaxPackBytesTimeout|TestExecuteOneShotTimeout' -v 2>&1 | tail -15",
  "description": "Run new messaging tests"
}
```

> TOOL

tool_result
id: toolu_01QC7kwTDGU7GvxSWBeNyA3y
```
	/home/<USER>/.local/share/mise/installs/go/1.26.2/src/testing/testing.go:1977 +0x318
panic({0x1012cdb20?, 0x1013c6b70?})
	/home/<USER>/.local/share/mise/installs/go/1.26.2/src/runtime/panic.go:860 +0x12c
entire.io/entire/git-sync/internal/strategy/bootstrap.fakeBootstrapSource.FetchPack(...)
	/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go:1292
entire.io/entire/git-sync/internal/strategy/bootstrap.Execute({0x10135e828, 0x1014050a0}, {{0x0, 0x0}, {0x10135dfb8, 0x101407360}, {0x10135c550, 0x387141f21540}, 0x387141fcd350, 0x0, ...}, ...)
	/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go:162 +0x71c
entire.io/entire/git-sync/internal/strategy/bootstrap.TestExecuteOneShotTimeoutWithoutBatchSupportIsActionable(0x387141f7b208)
	/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go:1523 +0x284
testing.tRunner(0x387141f7b208, 0x101355a58)
	/home/<USER>/.local/share/mise/installs/go/1.26.2/src/testing/testing.go:2036 +0xc4
created by testing.(*T).Run in goroutine 1
	/home/<USER>/.local/share/mise/installs/go/1.26.2/src/testing/testing.go:2101 +0x3a8
FAIL	entire.io/entire/git-sync/internal/strategy/bootstrap	0.334s
FAIL
```

> AGENT

The embedded source needs a `fetchPack`. Let me fix the test:

> TOOL

tool_use Edit
id: toolu_01DRyVKqu4TijpvAag8J6a9a
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "old_string": "\t_, err := Execute(context.Background(), Params{\n\t\tSourceService: noBatchSource{},\n\t\tTargetPusher: fakeBootstrapPusher{",
  "new_string": "\t_, err := Execute(context.Background(), Params{\n\t\tSourceService: noBatchSource{fakeBootstrapSource{\n\t\t\tfetchPack: func(_ context.Context, _ gitproto.Conn, _ map[plumbing.ReferenceName]gitproto.DesiredRef, _ map[plumbing.ReferenceName]plumbing.Hash) (io.ReadCloser, error) {\n\t\t\t\treturn io.NopCloser(bytes.NewReader([]byte(\"PACK\"))), nil\n\t\t\t},\n\t\t}},\n\t\tTargetPusher: fakeBootstrapPusher{"
}
```

> TOOL

tool_result
id: toolu_01DRyVKqu4TijpvAag8J6a9a
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_018D4wZtQhiMegDuXigjVAxr
```json
{
  "command": "go test ./internal/strategy/bootstrap/ 2>&1 | tail -15",
  "description": "Run full bootstrap test suite"
}
```

> TOOL

tool_result
id: toolu_018D4wZtQhiMegDuXigjVAxr
```
ok  	entire.io/entire/git-sync/internal/strategy/bootstrap	0.320s
```

> AGENT

Full build/test and vet:

> TOOL

tool_use Bash
id: toolu_01PiQYNGMU7V2pDRdus6YaYd
```json
{
  "command": "go build ./... && go vet ./internal/strategy/bootstrap/ && go test ./... 2>&1 | grep -v \"^ok\\|no test files\" | tail -20; echo \"exit: ${PIPESTATUS}\"",
  "description": "Build, vet, full test suite"
}
```

> TOOL

tool_result
id: toolu_01PiQYNGMU7V2pDRdus6YaYd
```
exit:
```

> AGENT

All passing. Commit 2:

> TOOL

tool_use Bash
id: toolu_013LcNSf1s6e4HSCfsF9Kdjh
```json
{
  "command": "git add internal/strategy/bootstrap/bootstrap.go internal/strategy/bootstrap/bootstrap_test.go && git commit -q -F - <<'EOF'\nbootstrap: clearer messaging when a push times out\n\nDistinguish a timeout from a size rejection in the auto-batch notice\n(\"target push timed out\" vs \"target rejected pack\") so the user sees why\nthe retry kicked in.\n\nWhen a one-shot push hits a batchable failure (408/504/413) but no\nbatched fallback is possible — the source can't serve the protocol-v2\nfetch filter checkpointing needs — wrap the error with guidance instead\nof surfacing a bare \"http 408\", while still wrapping the original error\nfor callers that inspect it.\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <<REDACTED_EMAIL>>\nEOF\ngit log --oneline -3",
  "description": "Commit messaging changes"
}
```

> TOOL

tool_result
id: toolu_013LcNSf1s6e4HSCfsF9Kdjh
```
bfc5a85c bootstrap: clearer messaging when a push times out
81390b1b bootstrap: treat receive-pack timeouts (408/504) as batchable
2ace4367 Merge pull request #74 from entireio/fix/pack-less-ref-create-empty-pack
```

> AGENT

Now run `/simplify` on the diff.

> TOOL

tool_use Skill
id: toolu_01NfMwCZDGduUMUFE9Z1BLd6
```json
{
  "skill": "simplify"
}
```

> TOOL

tool_result
id: toolu_01NfMwCZDGduUMUFE9Z1BLd6
```
Launching skill: simplify
```

> AGENT

I'll gather the diff and launch the four review agents in parallel.

> TOOL

tool_use Bash
id: toolu_01AZCsk2CVahTS8tMpLvb8FG
```json
{
  "command": "git diff main...HEAD",
  "description": "Get the diff under review"
}
```

> TOOL

tool_result
id: toolu_01AZCsk2CVahTS8tMpLvb8FG
```
diff --git a/internal/strategy/bootstrap/bootstrap.go b/internal/strategy/bootstrap/bootstrap.go
index 870f25ea..1daea80c 100644
--- a/internal/strategy/bootstrap/bootstrap.go
+++ b/internal/strategy/bootstrap/bootstrap.go
@@ -179,12 +179,16 @@ func Execute(ctx context.Context, p Params, relayReason string) (Result, error)
 	if pushErr != nil {
 		autoBatch, ok := autoTargetMaxPackBytes(p, pushErr)
 		if !ok {
-			return result, fmt.Errorf("push target refs: %w", pushErr)
+			return result, fmt.Errorf("push target refs: %w", actionableTargetPushError(p, pushErr))
+		}
+		reason := "target rejected pack"
+		if isTargetPushDeadlineError(pushErr) {
+			reason = "target push timed out"
 		}
 		p.log("bootstrap retrying with batched mode after target rejection",
-			"target_max_pack_bytes", autoBatch)
-		p.notice(fmt.Sprintf("target rejected pack — switching to batched mode (limit %s)",
-			humanBytes(autoBatch)))
+			"target_max_pack_bytes", autoBatch, "reason", reason)
+		p.notice(fmt.Sprintf("%s — switching to batched mode (limit %s)",
+			reason, humanBytes(autoBatch)))
 		p.TargetMaxPack = autoBatch
 		return executeBatched(ctx, p, plans, result)
 	}
@@ -500,8 +504,11 @@ func executeBatched( //nolint:maintidx // complex batch logic is inherently bran
 				_ = packReader.Close()
 				// Treat abortedEarly the same as a body-limit error:
 				// both indicate "this pack is too big for the target",
-				// just one is detected by the server and one by us.
-				sizeIssue := abortedEarly || isTargetBodyLimitError(pushErr)
+				// just one is detected by the server and one by us. A
+				// […]

> TOOL

tool_use Agent
id: toolu_01HfuPFdC8virqFMfwWarwYU
```json
{
  "description": "Reuse review",
  "subagent_type": "general-purpose",
  "prompt": "You are reviewing a git diff for REUSE issues only — new code that re-implements something the codebase already has. Do NOT hunt for correctness bugs.\n\nThe diff is in the Go file `internal/strategy/bootstrap/bootstrap.go` (and its test). Working dir: /home/<USER>/Work/entire/devenv/git-sync\n\nHere is the diff under review:\n\n```\n[bootstrap.go changes]\n- Execute(): when one-shot push fails, calls actionableTargetPushError(p, pushErr); varies notice reason \"target rejected pack\" vs \"target push timed out\" based on isTargetPushDeadlineError(pushErr).\n- executeBatched(): sizeIssue := abortedEarly || isBatchableTargetPushError(pushErr)  (was isTargetBodyLimitError)\n- autoTargetMaxPackBytes(): gate changed to !isBatchableTargetPushError(err)\n- NEW func isTargetPushDeadlineError(err) bool: lowercases err.Error(), returns strings.Contains(msg,\"http 408\") || strings.Contains(msg,\"http 504\")\n- NEW func isBatchableTargetPushError(err) bool: isTargetBodyLimitError(err) || isTargetPushDeadlineError(err)\n- NEW func actionableTargetPushError(p Params, err error) error: if not batchable return err; if p.SourceService != nil && p.SourceService.SupportsBootstrapBatch() return err; else wrap err with guidance about protocol-v2 fetch filter.\n```\n\nExisting related code: isTargetBodyLimitError(err) already exists (matches \"body exceeded size limit\", \"http 413\", etc.); targetBodyLimit(err) parses a numeric limit.\n\nTasks:\n1. Read bootstrap.go to see existing error-classification helpers and patterns.\n2. Check whether there is an existing shared HTTP-status classification helper anywhere (grep internal/ for \"http 4\", \"StatusCode\", error classifiers in internal/gitproto, errors.go) that the new 408/504 check should reuse instead of substring-matching err.Error().\n3. […]

> TOOL

tool_use Agent
id: toolu_01CdskpMjuxzAMFhywFrqQ2C
```json
{
  "description": "Simplification review",
  "subagent_type": "general-purpose",
  "prompt": "You are reviewing a git diff for SIMPLIFICATION issues only — unnecessary complexity the diff adds (redundant/derivable state, copy-paste with slight variation, deep nesting, dead code). Do NOT hunt for correctness bugs.\n\nWorking dir: /home/<USER>/Work/entire/devenv/git-sync. File: internal/strategy/bootstrap/bootstrap.go and bootstrap_test.go.\n\nDiff summary:\n- NEW isTargetPushDeadlineError(err): lowercases err.Error(); returns strings.Contains(msg,\"http 408\") || strings.Contains(msg,\"http 504\").\n- NEW isBatchableTargetPushError(err): isTargetBodyLimitError(err) || isTargetPushDeadlineError(err).\n- NEW actionableTargetPushError(p Params, err error) error: guard returns err if !batchable; returns err if SourceService supports batch; else wraps err with a multi-line guidance string.\n- Execute(): adds `reason := \"target rejected pack\"; if isTargetPushDeadlineError(pushErr){reason=\"target push timed out\"}` used in both p.log and p.notice.\n- executeBatched(): sizeIssue now uses isBatchableTargetPushError.\n- Tests added: TestIsTargetPushDeadlineError, TestIsBatchableTargetPushError (table tests), TestAutoTargetMaxPackBytesTimeoutTriggersBatching, TestExecuteOneShotTimeoutWithoutBatchSupportIsActionable, plus a noBatchSource test type embedding fakeBootstrapSource.\n\nRead the actual file to verify. Look for:\n- Whether the three new helpers are over-factored or could be inlined/merged without losing clarity.\n- Whether the new TestIsBatchableTargetPushError meaningfully differs from TestIsTargetPushDeadlineError + TestIsTargetBodyLimitError or is redundant coverage.\n- Any awkward duplication in the reason-string handling.\n\nReport findings with file:line, one-line summary, concrete cost, and the simpler form. Be concise. Do NOT edit files."
}
```

> TOOL

tool_use Agent
id: toolu_01H9MmUrfd6rpTL9wArAHuA3
```json
{
  "description": "Efficiency review",
  "subagent_type": "general-purpose",
  "prompt": "You are reviewing a git diff for EFFICIENCY issues only — wasted work the diff introduces (redundant computation, repeated I/O, blocking work on hot paths, closures keeping large scopes alive). Do NOT hunt for correctness bugs.\n\nWorking dir: /home/<USER>/Work/entire/devenv/git-sync. File: internal/strategy/bootstrap/bootstrap.go.\n\nDiff summary:\n- isTargetPushDeadlineError(err): calls strings.ToLower(err.Error()) then two strings.Contains.\n- isBatchableTargetPushError(err): calls isTargetBodyLimitError(err) || isTargetPushDeadlineError(err) — note isTargetBodyLimitError ALSO calls strings.ToLower(err.Error()) internally, so on a batchable check err.Error() may be lowercased twice.\n- These run only on a push-error path (not a hot loop), once per failed push attempt.\n- Execute() computes `reason` once; fine.\n\nRead the file. Assess:\n- Is the double strings.ToLower(err.Error()) in the batchable path worth avoiding given it only runs on push failure (cold path)? Be pragmatic — note it but weigh whether it's worth fixing.\n- Any other wasted work introduced.\n\nReport findings with file:line, one-line summary, concrete cost, and cheaper alternative. Be concise and pragmatic about cold-path vs hot-path. Do NOT edit files."
}
```

> TOOL

tool_use Agent
id: toolu_01AtsBxh8G7tRVirfk8AjupJ
```json
{
  "description": "Altitude review",
  "subagent_type": "general-purpose",
  "prompt": "You are reviewing a git diff for ALTITUDE issues only — is each change implemented at the right depth, or is it a fragile bandaid / special-case layered on shared infra when generalizing would be cleaner? Do NOT hunt for correctness bugs.\n\nWorking dir: /home/<USER>/Work/entire/devenv/git-sync. Files: internal/strategy/bootstrap/bootstrap.go, and the HTTP layer internal/gitproto/smarthttp.go which produces errors like `http 408: <url> [headers] <body>` from httpError().\n\nContext: The fix makes git-sync treat GitHub's HTTP 408 (and 504) receive-pack timeout as a \"batchable\" push failure, routing it into the same batched-bootstrap fallback used for 413 body-limit rejections. It does this by substring-matching \"http 408\"/\"http 504\" on err.Error() in a new isTargetPushDeadlineError() in the bootstrap package.\n\nKey questions:\n1. Is substring-matching the formatted error string (\"http 408\") the right altitude, or should HTTP status classification live in the gitproto layer (smarthttp.go httpError) as a typed/sentinel error that bootstrap inspects via errors.As/errors.Is? Look at how errors.go and gitproto currently expose classified errors (e.g. RefRejectedError, ErrTargetRefMoved were recently added per git log). Is there an established pattern the new code should follow?\n2. Is conflating 408 (timeout) and 504 with 413 (size) under \"isBatchableTargetPushError\" the right generalization, or a leaky […]

> TOOL

tool_result
id: toolu_01HfuPFdC8virqFMfwWarwYU
```
I have everything needed. The substring matching is the established pattern in this file and there is no shared status classifier to reuse.

## Findings

**No reuse issue. The new code follows the existing pattern appropriately.**

1. **`isTargetPushDeadlineError` does not duplicate any existing helper.** The only sibling classifier is `isTargetBodyLimitError` (`internal/strategy/bootstrap/bootstrap.go:1437`), which matches 413 / "body exceeded size limit" — a disjoint set of statuses (408/504 vs 413). The new function is its deliberate, documented counterpart, and `isBatchableTargetPushError` (`bootstrap.go:1473`) is a thin OR over the two. No overlap.

2. **There is no shared HTTP-status classification helper anywhere in `internal/` for the 408/504 check to reuse.** I checked:
   - `errors.go` — only re-exports `ErrTargetRefMoved` / `RefRejectedError`; no status classifiers.
   - `internal/gitproto/push.go` — has `IsLeaseFailure(status string)` and `commandStatusErr(...)`, both for git protocol "ng"/lease statuses, not HTTP codes.
   - `internal/gitproto/smarthttp.go` — uses `http.StatusXxx` constants inline against `res.StatusCode` but exposes no reusable `isTimeout`/`isStatus` predicate.
   - No `StatusRequestTimeout` / `StatusGatewayTimeout` / `StatusRequestEntityTooLarge` predicate exists anywhere.

3. **Substring-matching `err.Error()` is the correct (and only available) approach here, not a missed reuse.** The error these helpers inspect is produced as a flat string by `httpError` at `internal/gitproto/smarthttp.go:61` and `:63` via `fmt.Errorf("http %d: ...", […]

> TOOL

tool_result
id: toolu_01CdskpMjuxzAMFhywFrqQ2C
```
I have everything I need to report.

## Simplification review: bootstrap.go / bootstrap_test.go

Overall the diff is restrained. The three new helpers are not over-factored — each has a distinct, justified role. Two minor findings, both low-cost.

**Finding 1 — `isBatchableTargetPushError` is a justified wrapper, not redundant (no change needed)**
`bootstrap.go:1473` — The one-line OR helper is referenced at three call sites (`executeBatched:511`, `autoTargetMaxPackBytes:1388`, `actionableTargetPushError:1485`). Inlining `isTargetBodyLimitError(err) || isTargetPushDeadlineError(err)` at all three would duplicate the policy "these two conditions are both batchable" and lose the doc comment explaining why. Keep as is. Likewise `isTargetPushDeadlineError` is genuinely separate from `isTargetBodyLimitError` (different trigger, no limit to parse) — correctly kept distinct.

**Finding 2 — `TestIsBatchableTargetPushError` is largely redundant coverage (minor)**
`bootstrap_test.go:188-209` — The function under test is a pure 1-line OR with no logic of its own. Its 6 cases are all already covered by `TestIsTargetBodyLimitError` (body-limit/413) + `TestIsTargetPushDeadlineError` (408/504/nil/unrelated). The only thing this test adds beyond the two component tests is confirming the OR is wired correctly (an extra ~22 lines for one bit of information).
Cost: minor maintenance surface; not harmful. Defensible as a cheap guard that the combinator stays an OR. Simpler form if trimmed: […]

> TOOL

tool_result
id: toolu_01H9MmUrfd6rpTL9wArAHuA3
```
I have everything needed. Here are my findings.

## Efficiency review: `internal/strategy/bootstrap/bootstrap.go`

All the flagged work sits on the **push-failure path** — it runs at most once per failed push attempt, never in a hot loop. Each finding below is real but small; I weigh each one's worth accordingly.

### 1. Double `strings.ToLower(err.Error())` in the batchable check — not worth fixing
`bootstrap.go:1473-1474` — `isBatchableTargetPushError` calls `isTargetBodyLimitError` (lowercases at :1441) then, on the OR's right side, `isTargetPushDeadlineError` (lowercases again at :1465).
- Cost: one extra `err.Error()` formatting + one extra full-string `ToLower` allocation, only when the body-limit check fails and we fall through to the deadline check. Cold path, runs once per failed push.
- Cheaper alternative exists (lowercase once, pass `msg string` to internal helpers), but it would force restructuring the three small public-ish predicates and lose their standalone `err`-taking signatures. Given this only fires on a push failure, the readability cost outweighs the saved microseconds. **Recommend leaving as-is.**

### 2. The same error gets lowercased ~3-4 times across the one push-failure handler — same verdict
Worth noting as the fuller picture, since the prompt asked for "any other wasted work." On a single failed one-shot […]

> TOOL

tool_result
id: toolu_01AtsBxh8G7tRVirfk8AjupJ
```
This confirms the picture. The gitproto layer (`httpError`) does not classify any status codes itself — it just formats `http %d: ...`. All HTTP-status classification (413, and now 408/504) lives in the bootstrap package as substring matches on the formatted string. Meanwhile, the *report-status* "ng" rejection path got the full typed-error treatment (`RefRejectedError` / `ErrTargetRefMoved`) recently.

I have everything needed to give the recommendation.

## Altitude review: 408/504 "batchable push" classification

### Finding 1 — Substring-matching `"http 408"` on the formatted error string is at the wrong altitude, but it matches the package's *existing* HTTP-classification pattern

`internal/strategy/bootstrap/bootstrap.go:1448` (`isTargetPushDeadlineError`) classifies an HTTP status by `strings.Contains(strings.ToLower(err.Error()), "http 408")`. The status code is *known structurally* at `internal/gitproto/smarthttp.go:39` (`httpError` has `res.StatusCode`), then thrown away into a `fmt.Errorf("http %d: ...")` string at smarthttp.go:61/63, and re-parsed downstream.

- One-line summary: HTTP status re-derived by substring-scanning a formatted string instead of inspecting a typed error from the layer that has the status code.
- Concrete cost: brittle coupling to the exact format string `"http %d"`. Anyone reformatting httpError (e.g. "HTTP 408", "status 408", localizing, or adding the numeric code elsewhere in the URL/body — a body containing "...http 408..." would false-positive) silently breaks […]

> AGENT

The reviews converge: the code is clean and consistent with the package's existing `isTargetBodyLimitError` pattern. The only in-scope, actionable item is **Finding 2 (simplification)**: `TestIsBatchableTargetPushError` largely re-tests edge cases already owned by the two per-predicate tests. I'll trim it to just confirm the OR wiring.

Everything else I'm skipping deliberately:
- **Reuse / efficiency**: clean — double `ToLower` is cold-path-only, not worth restructuring the predicates.
- **Altitude** (typed gitproto HTTP error via `errors.As`): a real but separate cleanup that would require refactoring the pre-existing 413 path and threading status through `httpError`; scope creep for this fix. Worth a follow-up ticket, not this diff.

> TOOL

tool_use Edit
id: toolu_01YADnDLgSaC3GNeUbxSsWT3
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go",
  "old_string": "func TestIsBatchableTargetPushError(t *testing.T) {\n\ttests := []struct {\n\t\tname string\n\t\terr  error\n\t\twant bool\n\t}{\n\t\t{name: \"nil error\", err: nil, want: false},\n\t\t{name: \"body limit\", err: errors.New(\"body exceeded size limit 1048576\"), want: true},\n\t\t{name: \"http 413\", err: errors.New(\"http 413\"), want: true},\n\t\t{name: \"http 408 deadline\", err: errors.New(\"http 408: request timeout\"), want: true},\n\t\t{name: \"http 504 deadline\", err: errors.New(\"http 504: gateway timeout\"), want: true},\n\t\t{name: \"unrelated\", err: errors.New(\"connection refused\"), want: false},\n\t}",
  "new_string": "func TestIsBatchableTargetPushError(t *testing.T) {\n\t// Per-status edge cases are covered by TestIsTargetBodyLimitError and\n\t// TestIsTargetPushDeadlineError; this only confirms the OR wires both in.\n\ttests := []struct {\n\t\tname string\n\t\terr  error\n\t\twant bool\n\t}{\n\t\t{name: \"body limit\", err: errors.New(\"body exceeded size limit 1048576\"), want: true},\n\t\t{name: \"deadline\", err: errors.New(\"http 408: request timeout\"), want: true},\n\t\t{name: \"unrelated\", err: errors.New(\"connection refused\"), want: false},\n\t}"
}
```

> TOOL

tool_result
id: toolu_01YADnDLgSaC3GNeUbxSsWT3
```
The file /home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap_test.go has been updated successfully. (file state is current in your context — no need to Read it back)
```

> TOOL

tool_use Bash
id: toolu_01QM8h7pnU1NkvPhSYM7zUKv
```json
{
  "command": "go test ./internal/strategy/bootstrap/ 2>&1 | tail -5",
  "description": "Re-run bootstrap tests after trim"
}
```

> TOOL

tool_result
id: toolu_01QM8h7pnU1NkvPhSYM7zUKv
```
ok  	entire.io/entire/git-sync/internal/strategy/bootstrap	0.347s
```

> TOOL

tool_use Bash
id: toolu_01F47d9brzsQ4cvM1ipGJsVD
```json
{
  "command": "git add -A && git commit -q -m \"$(cat <<'EOF'\nbootstrap: trim redundant batchable-error test cases\n\nPer-status edge cases are already owned by TestIsTargetBodyLimitError and\nTestIsTargetPushDeadlineError; the combinator test only needs to confirm\nthe OR wires both predicates in.\n\nCo-Authored-By: Claude Opus 4.8 (1M context) <<REDACTED_EMAIL>>\nEOF\n)\" && git log --oneline -3",
  "description": "Commit test trim"
}
```

> TOOL

tool_result
id: toolu_01F47d9brzsQ4cvM1ipGJsVD
```
d8d64e61 bootstrap: trim redundant batchable-error test cases
bfc5a85c bootstrap: clearer messaging when a push times out
81390b1b bootstrap: treat receive-pack timeouts (408/504) as batchable
```

> AGENT

Done. Here's the summary.

## What I shipped

Branch `fix/target-push-timeout-batched-retry`, three commits:

1. **`bootstrap: treat receive-pack timeouts (408/504) as batchable`** — the core fix. New `isTargetPushDeadlineError` (matches `http 408`/`http 504`) and `isBatchableTargetPushError` (body-limit OR deadline). Wired into both the one-shot auto-batch decision (`autoTargetMaxPackBytes`) and the mid-batch subdivision path, so a GitHub 408 now routes into the same batched-bootstrap fallback that 413 already used instead of hard-failing.

2. **`bootstrap: clearer messaging when a push times out`** — the auto-batch notice now distinguishes "target push timed out" from "target rejected pack", and a one-shot batchable failure that *can't* fall back (source lacks the protocol-v2 fetch filter checkpointing needs) gets wrapped with guidance instead of a bare `http 408`. Original error stays wrapped for `errors.Is`.

3. **`bootstrap: trim redundant batchable-error test cases`** — the `/simplify` cleanup.

Tests: 2 classifier table tests + `TestAutoTargetMaxPackBytesTimeoutTriggersBatching` + `TestExecuteOneShotTimeoutWithoutBatchSupportIsActionable`. Full `go build`/`go vet`/`go test ./...` green.

## `/simplify` outcome

Four parallel review agents (reuse, simplification, efficiency, altitude). Net: the diff was already clean and consistent with the package's existing `isTargetBodyLimitError` substring-matching convention.

- **Applied**: trimmed `TestIsBatchableTargetPushError` from 6 cases to 3 (the per-status edge cases are owned by the two dedicated predicate tests; the combinator test only […]