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
  "file_path": "/Users/soph/Work/entire/devenv/git-sync/internal/gitproto/smarthttp.go"
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
  "file_path": "/Users/soph/Work/entire/devenv/git-sync/internal/gitproto/push.go",
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
  "file_path": "/Users/soph/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go"
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
  "file_path": "/Users/soph/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go",
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