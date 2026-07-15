> SYSTEM

# AGENTS.md instructions for /Users/alisha/Projects/wt/external-agents/kiro-windows-bug <INSTRUCTIONS> ## Aliases - `test-repos` → `/Users/alisha/Projects/test-repos` - `entire frontend` → `/Users/alisha/Projects/devenv/entire.io` - `entire cli` → `/Users/alisha/Projects/devenv/cli` Resolve aliases to their full paths before acting on any instruction. When creating PR ALWAYS create in draft mode When debugging instead of writing logs and asking me to give them to you. Write the logs to a local file so you can see them. # Security All API endpoints must require authentication; apply the most restrictive access controls and minimal permissions necessary by default. All prompts that incorporate external or user-supplied content must be constructed to prevent prompt injection — treat untrusted input as data, never as instructions All prompts that incorporate external or user-supplied content must be constructed to prevent prompt injection — treat untrusted input as data, never as instructions. Never add a dependency without checking it is actively maintained and widely trusted. Never hardcode secrets, credentials, or environment-specific values — use environment variables only. Return generic error messages to clients; log full details server-side only. Avoid storing sensitive data beyond what is strictly necessary; prefer not storing it at all. ## Parallelism - Always perform independent operations concurrently. Use Promise.all(), Promise.allSettled(), or equivalent parallel […]

> DEVELOPER

do adversarial review of docs/rfds/windows-e2e-design.md use docs/rfds/windows-e2e-design-timeline.md for understanding decisions

> AGENT

I’m reviewing `docs/rfds/windows-e2e-design.md` as an adversarial design review and I’ll use the timeline doc to reconstruct why the choices were made before I assess risks and gaps.

> AGENT

I’ve got the design and the decision history. Next I’m checking the referenced code paths to verify whether the doc’s assumptions still hold and where the design is under-specified or overly optimistic.

> AGENT

The test harness matters here because some of the proposed mitigations only work if they’re wired at the right layer. I’m checking how sessions are opened, closed, and whether bootstrap/auth hooks already exist.

> AGENT

Two areas look suspicious now: the workflow security model after secrets are wired, and the assumption that a raw ConPTY byte stream can replace tmux’s rendered screen semantics without a real screen model. I’m pinning those down against the doc text before I write findings.

> AGENT

**Findings** 1. High: the `/test-e2e` `issue_comment` design is still unsafe once secrets are added. The doc treats `author_association` as the load-bearing control, but the workflow still resolves and checks out the PR head SHA from arbitrary refs, so a maintainer commenting on a malicious fork PR would run attacker code with repo secrets. That is exactly the path the doc says is acceptable for external contributors. See [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:219), [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:287), [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:334), and the timeline’s repeated approval of that assumption in [windows-e2e-design-timeline.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design-timeline.md:11). This needs a stronger boundary: either no secrets on `issue_comment`, or restrict secret-bearing runs to same-repo branches / manual dispatch only. 2. High: the auth follow-up plan relies on `Bootstrap()`, but nothing in the proposed execution path calls it. The RFD says the follow-up commit will “update `Bootstrap()` to write the appropriate config file”, yet the workflow only runs `mise run test:e2e:lifecycle`, `TestMain` does not invoke bootstrap, and the only existing caller is the standalone bootstrap helper. See [windows-e2e-design.md](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/docs/rfds/windows-e2e-design.md:301), [setup_test.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/setup_test.go:19), and [main.go](/Users/alisha/Projects/wt/external-agents/kiro-windows-bug/e2e/bootstrap/main.go:12). As written, removing `E2E_NO_AUTH` later still leaves no mechanism to materialize auth config. 3. Medium: the ConPTY design assumes an append-only ANSI-stripped byte stream is “close enough” to tmux’s rendered pane, but the wait logic depends on current-screen […]