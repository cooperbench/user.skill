> DEVELOPER

can you take a look at: 

Here's the git-sync issue, structured to mirror the entiredb one.

---

## git-sync: batched bootstrap sends pack-less ref creates that some servers reject

### Symptom
During a batched bootstrap, git-sync finalizes a "subsumed" branch by sending a **ref-create command with no packfile**. Against a receive-pack implementation that expects a pack for any non-delete command, this fails:
```
bootstrap execute: create subsumed branch ref for refs/heads/<branch>:
report-status: unpack error: quarantine fanout: read packfile header: EOF
```
The bootstrap dies mid-run, leaving the target half-populated. First observed mirroring `github.com/JUMPTOON/app` → entiredb prod `aws-us-east-2`, 2026-06-15 07:36 (trace `433bad8f4ef654ac651f868ab3c2fa3e`): ~15 batch pushes succeeded, then the subsumed-ref create EOF'd.

### Root cause
In the batched bootstrap, the subsumed-branch path issues a ref-only push:
```go
// internal/strategy/bootstrap/bootstrap.go (subsumed branch finalize)
cmds := []gitproto.PushCommand{{Name: ..., Old: ZeroHash, New: batch.Plan.SourceHash}}
p.TargetPusher.PushCommands(ctx, cmds)   // no pack
```
`PushCommands` → `sendReceivePack(ctx, conn, req, nil, …)` with `packData=nil`, so the request body is the command pkt-lines + flush and **nothing else** (`internal/gitproto/push.go:585`, body assembly at `push.go:293-296`).

That's valid git when the objects already exist, but it relies on the server tolerating a pack-less create. entiredb (and likely others) treats every non-delete as "a pack will […]

> AGENT

I'll verify these claims against the actual git-sync codebase. Let me investigate the key files referenced.

> TOOL

tool_use Bash
id: toolu_01DRuKSyz4iN81NASYkVvfPL
```json
{
  "command": "pwd && ls && echo \"---REMOTE---\" && git remote -v 2>/dev/null | head",
  "description": "Show repo root and remotes"
}
```

> TOOL

tool_result
id: toolu_01DRuKSyz4iN81NASYkVvfPL
```
/home/<USER>/Work/entire/devenv/git-sync
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
---REMOTE---
<REDACTED_EMAIL>:entirehq/git-sync.git	
origin	<REDACTED_EMAIL>:entireio/git-sync.git (fetch) [blob:none]
origin	<REDACTED_EMAIL>:entireio/git-sync.git (push)
```

> AGENT

I'll dispatch parallel exploration to verify each claim in the report against the real source.

> TOOL

tool_use Agent
id: toolu_018f8mGPnhJJkqhSeymfadb9
```json
{
  "description": "Verify pack-less create bug",
  "subagent_type": "Explore",
  "prompt": "I'm verifying a bug report against the git-sync repo at /home/<USER>/Work/entire/devenv/git-sync.\n\nInvestigate the \"subsumed branch\" / pack-less ref-create path in the BATCHED BOOTSTRAP strategy. I need to confirm or correct these specific claims:\n\n1. In `internal/strategy/bootstrap/bootstrap.go`, there is a \"subsumed branch finalize\" path that issues a ref-only push: builds `[]gitproto.PushCommand{{Name: ..., Old: ZeroHash, New: batch.Plan.SourceHash}}` and calls `p.TargetPusher.PushCommands(ctx, cmds)` with NO packfile. Find the actual code, quote it, and give exact file:line locations. Search for \"subsumed\" in the codebase.\n\n2. In `internal/gitproto/push.go`: confirm that `PushCommands` eventually calls `sendReceivePack(ctx, conn, req, nil, …)` with `packData=nil`. The report cites `push.go:585` and body assembly at `push.go:293-296`. Verify these line numbers and quote the relevant code — specifically how the request body is assembled when packData is nil (is it just command pkt-lines + flush and nothing else?).\n\n3. Is there any existing notion of sending an \"empty packfile\" (12-byte header + trailer, 0 objects) anywhere in the codebase? Search for pack header construction (e.g. \"PACK\" literal, version, object count). Does git-sync ever construct empty packs?\n\nReport exact file:line for every claim, quote the code, and flag any claim in the report that is inaccurate […]

> TOOL

tool_use Agent
id: toolu_01Fx1PcCGvq3P29qbjNYEYtW
```json
{
  "description": "Verify replicate batching gaps",
  "subagent_type": "Explore",
  "prompt": "I'm verifying a bug report against the git-sync repo at /home/<USER>/Work/entire/devenv/git-sync.\n\nI need to confirm or correct these claims about the REPLICATE strategy vs the BOOTSTRAP strategy, and about config plumbing:\n\n1. `internal/strategy/replicate/replicate.go`: The report claims around lines 62-73 the replicate strategy does \"fetch one pack, push once, no retry\" — one pack for all updates with no subdivision, and on failure just returns `push target refs: %w`. Find and quote the actual code. Confirm there is NO body-limit fallback / no batching / no checkpoint relay in replicate. Give exact file:line.\n\n2. `internal/strategy/bootstrap/bootstrap.go`: The report claims the body-limit handling lives ONLY in bootstrap: a `body exceeded size limit` detection + checkpoint-batched relay, referencing `autoTargetMaxPackBytes` and `bodyLimitPattern` at lines 33 and 1380, and an `executeBatched` function. Find and quote these. Give exact file:line for: the `bodyLimitPattern` definition, `autoTargetMaxPackBytes`, `executeBatched`, and any \"body exceeded size limit\" string matching. Confirm replicate has none of this.\n\n3. `TargetMaxPackBytes` plumbing: The report claims `Options`/`SyncRequest`/`SyncPolicy` don't expose `TargetMaxPackBytes`, and that `internalbridge/config.go:75` hardcodes it to 0. \n   - Find where `TargetMaxPackBytes` is defined (which struct/config).\n   - Check the public API surface: look at types.go, client.go, and […]

> TOOL

tool_result
id: toolu_018f8mGPnhJJkqhSeymfadb9
```
Excellent! Now I have all the information I need. Let me create a comprehensive report.

## Investigation Complete: Bug Report Verification

Based on my thorough investigation of the git-sync codebase, here are my findings on each claim:

### **CLAIM 1: "Subsumed branch finalize" path in bootstrap.go**

**STATUS: ACCURATE** ✓

**Code Location:** `/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go:323-337`

**Exact Quote:**
```go
if batch.subsumed {
    cmds := []gitproto.PushCommand{{
        Name: batch.Plan.TargetRef,
        Old:  plumbing.ZeroHash,
        New:  batch.Plan.SourceHash,
    }}
    if err := p.TargetPusher.PushCommands(ctx, cmds); err != nil {
        return result, fmt.Errorf("create subsumed branch ref for %s: %w", batch.Plan.TargetRef, err)
    }
    completedRefs[batch.Plan.TargetRef] = batch.Plan.SourceHash
    result.BatchCount++
    p.log("bootstrap batch subsumed branch finalized",
        "branch", batch.Plan.TargetRef.String(),
        "source_hash", planner.ShortHash(batch.Plan.SourceHash))
    continue
}
```

**Verification:**
- Line 323: Check for `batch.subsumed` boolean
- Line 324-328: Build `[]gitproto.PushCommand{{Name: ..., Old: ZeroHash, New: batch.Plan.SourceHash}}` 
- Line 329: Calls `p.TargetPusher.PushCommands(ctx, cmds)` with NO packfile
- Line 334: Logs "bootstrap batch subsumed branch finalized"

The `subsumed` field is defined in the `plannedBatch` struct at lines 121-126, with documentation explaining it "skips the commit-graph fetch, the pack fetch, the temp ref, and the pack push — emitting only a single ref create command."

The subsumed batch is constructed in `planBatches()` at lines 747-760 when a branch's tip is already reachable […]

> TOOL

tool_result
id: toolu_01Fx1PcCGvq3P29qbjNYEYtW
```
Perfect! Now let me prepare my final report.

## Bug Report Verification Summary

I've systematically verified all claims in the bug report against the actual code. Here are my findings:

---

### Claim 1: Replicate strategy "fetch one pack, push once, no retry"

**VERIFIED - Lines 62-75 in `/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/replicate/replicate.go`**

Quote from lines 62-74:
```go
if len(updatePlans) > 0 {
	desired := convert.DesiredRefsForPlans(p.DesiredRefs, updatePlans)
	packReader, err := p.SourceService.FetchPack(ctx, p.SourceConn, desired, p.TargetRefs)
	if err != nil {
		return Result{}, fmt.Errorf("fetch source pack: %w", err)
	}
	packReader = gitproto.LimitPackReader(packReader, p.MaxPackBytes)
	packReader = closeOnce(packReader)
	if err := p.TargetPusher.PushPack(ctx, convert.PlansToPushCommands(updatePlans, false), packReader); err != nil {
		_ = packReader.Close()
		return Result{}, fmt.Errorf("push target refs: %w", err)
	}
	_ = packReader.Close()
}
```

**Confirmed:** One FetchPack call for all desired refs, one PushPack call, and on failure returns `fmt.Errorf("push target refs: %w", err)` with no fallback, retry, batching, or checkpoint relay. Replicate is 114 lines total and has no body-limit detection, no batching, no checkpoint management.

---

### Claim 2: Body-limit handling ONLY in bootstrap

**VERIFIED - Multiple locations in `/home/<USER>/Work/entire/devenv/git-sync/internal/strategy/bootstrap/bootstrap.go`**

1. **`bodyLimitPattern` definition - Line 33:**
   ```go
   var bodyLimitPattern = regexp.MustCompile(`body exceeded size limit ([0-9]+)`)
   ```

2. **`autoTargetMaxPackBytes` function - Line […]

> AGENT

I dug into the actual git-sync source. Your report holds up well — line numbers are accurate and the mechanism is correctly described. Here's the verification, with the one correction worth fixing before you file.

## Primary bug: pack-less subsumed-ref create — ✅ confirmed

**`internal/strategy/bootstrap/bootstrap.go:323-337`** (the report didn't pin a line; here it is):

```go
if batch.subsumed {
    cmds := []gitproto.PushCommand{{
        Name: batch.Plan.TargetRef,
        Old:  plumbing.ZeroHash,
        New:  batch.Plan.SourceHash,
    }}
    if err := p.TargetPusher.PushCommands(ctx, cmds); err != nil {
        return result, fmt.Errorf("create subsumed branch ref for %s: %w", batch.Plan.TargetRef, err)
    }
```

The `subsumed` field (struct doc at lines 121-126) explicitly says it "skips the commit-graph fetch, the pack fetch, the temp ref, and the pack push — emitting only a single ref create command." That matches your error string exactly.

**`internal/gitproto/push.go`** — your line cites verified:
- `push.go:585` — `PushCommands` calls `sendReceivePack(ctx, conn, req, nil, …)` with `packData=nil`. ✅
- `push.go:293-296` — body assembly is `bytes.NewReader(header.Bytes())`, and the pack is appended *only* `if packData != nil`. So with nil it's command pkt-lines + flush, nothing else. ✅

**Empty-pack suggestion:** confirmed there is **no** empty-pack construction anywhere in git-sync today (only `packfile.NewEncoder` for non-empty packs in `PushObjects`). So your suggested fix is […]