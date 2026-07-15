> DEVELOPER

can you take a look at https://github.com/entireio/git-sync/issues/70

> AGENT

I'll fetch the issue.

> AGENT

Let me explore the codebase to understand how pushes work.

> AGENT

Let me look at how the bootstrap strategy streams data and the push implementation.

> AGENT

Let me check whether 408 is handled anywhere in the retry/syncer layer and how `--target-max-pack-bytes` is wired.

> AGENT

I've dug through the issue and the relevant code. Here's my read. ## What's happening The user is doing a one-shot bootstrap relay from a GitLab source to a fresh GitHub target. git-sync streams the pack straight from the source's `upload-pack` into the target's `receive-pack` POST (`bootstrap.Execute` → `PushPack` → `sendReceivePack`, which builds an `io.MultiReader(header, packData)` and POSTs it at `internal/gitproto/push.go:301`). GitHub returns **HTTP 408 (Request Timeout)** on `git-receive-pack`. GitHub enforces a wall-clock deadline on the receive-pack POST. The repo is large (compiled kernels/modules = big blobs), and the relay is bottlenecked by a very slow source — the progress line shows `gitlab.baylibre.com → 4.59 KB @ 402 B/s` feeding `479 B @ 39 B/s → github.com`. Because it's a direct relay, the slow GitLab read rate-limits the GitHub write, the single giant POST runs past GitHub's deadline, and GitHub kills it with 408. So the user's instinct in the issue is right: repo size (combined with slow source throughput) is the cause. ## Why git-sync doesn't auto-recover here There's already good machinery for "pack too big for the target" — batched bootstrap with checkpointing and auto-subdivision. But none of it triggers for this case: 1. **GitHub preflight** (`githubBatchLimit`, `bootstrap.go:1304`) […]

> DEVELOPER

let's implement the fix in a new branch, do meaningful commits, run /simplify when done

> AGENT

Let me create the branch and look at existing tests for the classifier functions to mirror their style.

> AGENT

Now I understand the patterns. Let me implement. First, the classifier helpers and wiring (commit 1).

> AGENT

Now the mid-batch subdivision path:

> AGENT

Now let me add tests for the classifier and the auto-batch-on-timeout path before committing. Let me check the existing one-shot retry test exists:

> AGENT

Let me add classifier tests right after `TestIsTargetBodyLimitError`:

> AGENT

Commit 1:

> AGENT

Now commit 2: messaging. Let me update the one-shot retry notice and add an actionable error when batching is impossible.

> AGENT

Now add the `actionableTargetPushError` helper near the classifiers:

> AGENT

Now tests for the messaging behavior. Let me add a non-batching source fake and two tests:

> AGENT

The embedded source needs a `fetchPack`. Let me fix the test:

> AGENT

Full build/test and vet:

> AGENT

All passing. Commit 2:

> AGENT

Now run `/simplify` on the diff.

> AGENT

I'll gather the diff and launch the four review agents in parallel.

> AGENT

The reviews converge: the code is clean and consistent with the package's existing `isTargetBodyLimitError` pattern. The only in-scope, actionable item is **Finding 2 (simplification)**: `TestIsBatchableTargetPushError` largely re-tests edge cases already owned by the two per-predicate tests. I'll trim it to just confirm the OR wiring. Everything else I'm skipping deliberately: - **Reuse / efficiency**: clean — double `ToLower` is cold-path-only, not worth restructuring the predicates. - **Altitude** (typed gitproto HTTP error via `errors.As`): a real but separate cleanup that would require refactoring the pre-existing 413 path and threading status through `httpError`; scope creep for this fix. Worth a follow-up ticket, not this diff.

> AGENT

Done. Here's the summary. ## What I shipped Branch `fix/target-push-timeout-batched-retry`, three commits: 1. **`bootstrap: treat receive-pack timeouts (408/504) as batchable`** — the core fix. New `isTargetPushDeadlineError` (matches `http 408`/`http 504`) and `isBatchableTargetPushError` (body-limit OR deadline). Wired into both the one-shot auto-batch decision (`autoTargetMaxPackBytes`) and the mid-batch subdivision path, so a GitHub 408 now routes into the same batched-bootstrap fallback that 413 already used instead of hard-failing. 2. **`bootstrap: clearer messaging when a push times out`** — the auto-batch notice now distinguishes "target push timed out" from "target rejected pack", and a one-shot batchable failure that *can't* fall back (source lacks the protocol-v2 fetch filter checkpointing needs) gets wrapped with guidance instead of a bare `http 408`. Original error stays wrapped for `errors.Is`. 3. **`bootstrap: trim redundant batchable-error test cases`** — the `/simplify` cleanup. Tests: 2 classifier table tests + `TestAutoTargetMaxPackBytesTimeoutTriggersBatching` + `TestExecuteOneShotTimeoutWithoutBatchSupportIsActionable`. Full `go build`/`go vet`/`go test ./...` green. ## `/simplify` outcome Four parallel review agents (reuse, simplification, efficiency, altitude). Net: the diff was already clean and consistent with the package's existing `isTargetBodyLimitError` substring-matching convention. - **Applied**: trimmed `TestIsBatchableTargetPushError` from 6 cases to 3 (the per-status edge cases are owned by the two dedicated predicate tests; the combinator test only […]