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