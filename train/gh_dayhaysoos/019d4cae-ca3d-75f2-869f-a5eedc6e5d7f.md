> DEVELOPER

list

> AGENT

I’m listing the current workspace directory so you can see what’s available.

> TOOL

tool_use exec_command
id: call_JU22gSFzMhGfOT6eSOSNnmT3
```json
{
  "cmd": "ls -1"
}
```

> TOOL

tool_result
id: call_JU22gSFzMhGfOT6eSOSNnmT3
```
Command: /bin/zsh -lc 'ls -1'
Chunk ID: 4ccf01
Wall time: 0.5117 seconds
Process exited with code 0
Original token count: 38
Output:
README.md
docs
enforce-node-version.mjs
llm-docs
node_modules
package.json
packages
pnpm-lock.yaml
pnpm-workspace.yaml
scripts
specs
tsconfig.base.json

```

> AGENT

README.md
docs
enforce-node-version.mjs
llm-docs
node_modules
package.json
packages
pnpm-lock.yaml
pnpm-workspace.yaml
scripts
specs
tsconfig.base.json

> DEVELOPER

what's the command I use to continue an older codex session?

> AGENT

I’ll check this repo’s docs for the exact CLI command so I give you the right one.

> TOOL

tool_use exec_command
id: call_bgmXFMjwlkrm0HaeZLc1xD0Z
```json
{
  "cmd": "rg -n \"resume|session|continue\" README.md docs llm-docs -S"
}
```

> TOOL

tool_use exec_command
id: call_XKonnPaU3VOUBb3TbW4orWLp
```json
{
  "cmd": "rg -n \"codex\" README.md docs llm-docs -S"
}
```

> TOOL

tool_result
id: call_bgmXFMjwlkrm0HaeZLc1xD0Z
```
Command: /bin/zsh -lc 'rg -n "resume|session|continue" README.md docs llm-docs -S'
Chunk ID: adc318
Wall time: 0.6294 seconds
Process exited with code 0
Original token count: 4423
Output:
llm-docs/auth-roadmap-for-shared-hosted-nimbus.md:24:   - Use per-run or per-session tokens with strict TTL.
llm-docs/auth-roadmap-for-shared-hosted-nimbus.md:70:It is acceptable to continue iterating on review output in a controlled internal setup. Do not treat current auth posture as production-ready for broad external users.
llm-docs/admin-key-governance-and-recovery.md:106:## Notes from active debugging session
llm-docs/local-review-ui-policy-workflow.md:5:Nimbus review quality depends heavily on policy quality. Current CLI-first flow can produce noise when policy extraction is imperfect. This document defines a policy-first local UI workflow and a secure local authentication model so only the local runner can access the review UI session.
llm-docs/local-review-ui-policy-workflow.md:44:Only the user/process that launched the local review session should be able to access that session UI.
llm-docs/local-review-ui-policy-workflow.md:48:Session auth must be run-scoped by default. No historical review browsing unless explicitly implemented as a separate mode.
llm-docs/local-review-ui-policy-workflow.md:56:## Recommended local auth/session architecture
llm-docs/local-review-ui-policy-workflow.md:71:## 3) Session exchange
llm-docs/local-review-ui-policy-workflow.md:75:- Server issues HttpOnly session cookie:
llm-docs/local-review-ui-policy-workflow.md:78:- Browser JS never sees the session secret.
llm-docs/local-review-ui-policy-workflow.md:82:- Session scope must include only current run resources:
llm-docs/local-review-ui-policy-workflow.md:88:## 5) Session lifecycle
llm-docs/local-review-ui-policy-workflow.md:90:- Expire session on short inactivity window (e.g. 30-60 min) or when CLI exits.
llm-docs/local-review-ui-policy-workflow.md:91:- Local server should revoke all session state when run completes or process terminates.
llm-docs/local-review-ui-policy-workflow.md:155:- `POST /local/session/exchange`
llm-docs/local-review-ui-policy-workflow.md:157:  - output: `204`, sets session cookie
llm-docs/local-review-ui-policy-workflow.md:179:All endpoints must enforce run-scoped authorization from session claims.
llm-docs/local-review-ui-policy-workflow.md:191:## Explicit decision about previous sessions
llm-docs/local-review-ui-policy-workflow.md:193:Default mode: **no previous session access**.
llm-docs/local-review-ui-policy-workflow.md:204:- [ ] Session cookie is HttpOnly + SameSite.
llm-docs/local-review-ui-policy-workflow.md:207:- [ ] Session scope enforces run-only resources.
llm-docs/local-review-ui-policy-workflow.md:208:- [ ] Session revoked when CLI exits/run ends.
llm-docs/archive/review-tool-best-practices.md:23:   - Keep prompt/session lineage in Nimbus metadata; do not overload commit messages with full transcripts.
llm-docs/archive/review-tool-best-practices.md:35:## Prompt/Session Provenance Guidelines
docs/architecture/auth-flow.md:60:- Self-hosted mode must continue bypassing hosted credential requirements and provide an internal admin-like auth context.
docs/architecture/auth-flow.md:61:- Hosted mode must continue restricting non-public API routes to authenticated callers only.
docs/architecture/auth-flow.md:62:- GitHub OIDC exchange must continue requiring repository registration before minting a Nimbus JWT.
docs/modules/review-execution.md:35:- Review context assembly: the review gathers diff, changed files, conventions, Entire session context, and co-change evidence before analysis.
docs/modules/review-execution.md:54:- Context assembly fails because required source material, session context, or co-change inputs cannot be resolved.
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:19:1. Work with your agent in a focused session
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:43:The reason: Phase 2 was implemented in one giant agent session and committed all at once instead of as 6 separate vertical slices. If those had been 6 separate commits with 6 separate Entire checkpoints, each review would have been ~10-15k tokens and produced high quality findings on every one.
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:60:- **Entire** captures the agent session context at commit time
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:71:Start focused agent session
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:94:- Related files historically co-changed in prior Entire sessions (when GitHub token is configured)
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:96:- The actual agent session intent — what the developer asked their agent to do
llm-docs/archive/nimbus-teaching-better-agent-workflows.md:117:1. **Work in vertical slices** — one focused agent session per meaningful unit of work
docs/entire/recovery.md:5:This document explains how to recover Nimbus review preflight when Entire session metadata becomes unreadable, incomplete, or stops attaching usable checkpoint data to commits.
docs/entire/recovery.md:17:- after re-enabling Entire, an already-running OpenCode process did not re-establish an active Entire session, so the next commit still did not get a usable checkpoint trailer.
docs/entire/recovery.md:41:- `entire status` should show the current OpenCode session as active.
docs/entire/recovery.md:44:- `review preflight HEAD` should say `Entire session metadata is readable` and should not mention branch fallback.
docs/entire/recovery.md:64:### 2. Make sure this OpenCode session is actually registered
docs/entire/recovery.md:66:This matters. Re-enabling Entire is not enough if the currently running OpenCode process never re-established an active Entire session.
docs/entire/recovery.md:74:If the current session is not shown as active, start a fresh OpenCode session after fixing the Entire settings.
docs/entire/recovery.md:80:If you only need to test trailer/session attachment first, an empty commit is acceptable:
docs/entire/recovery.md:83:git commit --allow-empty -m "chore: test Entire session health"
docs/entire/recovery.md:113:- `Entire session metadata is readable`
docs/entire/recovery.md:135:- Does the session entry reference `prompt`, `context`, or `transcript`?
docs/entire/recovery.md:144:- preflight prints `Entire session metadata is readable`
docs/entire/recovery.md:149:- If Entire was disabled and later re-enabled, prefer starting a fresh OpenCode session before trusting new commits.
docs/entire/recovery.md:150:- Do not assume the absence of a trailer means commit hooks are broken; it may just mean the active OpenCode session was stale.
docs/entire/recovery.md:158:If a future corruption incident looks similar, verify whether Entire changed the checkpoint metadata shape again before assuming the session data itself is missing.
docs/architecture/review-studio-experience-build-plan.md:94:8. Active reviews can survive Studio/browser restart and resume from worker truth plus replay.
docs/architecture/review-studio-experience-build-plan.md:168:3. Secondary `Resume active review` CTA appears when applicable.
docs/architecture/review-studio-experience-build-plan.md:255:3. Agent remediation loop can continue in mutable environment without implicitly starting a fresh checkpoint review.
docs/architecture/review-studio-experience-build-plan.md:274:2. User can resume correct active review from Home.
docs/architecture/review-studio-experience-build-plan.md:286:7. Parallel path: start two runs and resume each from Home correctly.
docs/getting-started.md:41:2. Validate Entire session metadata
docs/getting-started.md:77:This helps catch checkpoint/session-context issues and token readiness problems before queueing a full review.
llm-docs/archive/intent-capture-policy.md:5:Define how Nimbus converts Entire session history into review intent context that is safe, compact, and useful for high-precision code review.
llm-docs/archive/intent-capture-policy.md:15:## Session Summarization Controls
llm-docs/archive/intent-capture-policy.md:19:- `--summarize-session <auto|always|never>`
llm-docs/archive/intent-capture-policy.md:38:You are assisting Nimbus in gathering intent from a coding prompt session for deployment-backed code review.
llm-docs/archive/intent-capture-policy.md:40:Your job is to convert session history into a compact, factual intent record.
llm-docs/archive/intent-capture-policy.md:51:5) Never invent requirements not present in session history.
llm-docs/archive/intent-capture-policy.md:127:- Session context file missing/unreadable.
llm-docs/archive/intent-capture-policy.md:128:- Budget exceeded with `summarize-session=never`.
llm-docs/archive/intent-capture-policy.md:131:Each failure should include an actionable recovery hint (increase budget, split session/commit scope, restore session metadata).
llm-docs/archive/review-tool-v1-contract.md:151:    "sessionIds": ["ses_..."],
llm-docs/archive/review-context-phase1-spec.md:19:- If no valid Entire checkpoint/session context is resolvable, `review create` hard-fails with a clear error.
llm-docs/archive/review-context-phase1-spec.md:39:    session: {
llm-docs/archive/review-context-phase1-spec.md:40:      sessionId: string;
llm-docs/archive/review-context-phase1-spec.md:42:      sessionIntent: string | null; // extracted from prompt.txt/context.md
llm-docs/archive/review-context-phase1-spec.md:53:      lookbackSessions: number; // default 5
llm-docs/archive/review-context-phase1-spec.md:54:      sessionsScanned: number;
llm-docs/archive/review-context-phase1-spec.md:86:  supportingSessionIds: string[];
llm-docs/archive/review-context-phase1-spec.md:107:5. existing review-analysis lifecycle continues
llm-docs/archive/review-context-phase1-spec.md:131:1. Resolve eligible checkpoint sessions from `entire/checkpoints/v1`.
llm-docs/archive/review-context-phase1-spec.md:132:   - Eligibility definition in Phase 1: the N most recent sessions ordered by `assembledAt` descending.
llm-docs/archive/review-context-phase1-spec.md:136:   - fallback: last 5 checkpoint sessions
llm-docs/archive/review-context-phase1-spec.md:137:3. Keep only sessions touching any changed file.
llm-docs/archive/review-context-phase1-spec.md:138:4. For matched sessions, collect all other touched files.
llm-docs/archive/review-context-phase1-spec.md:151:  cochange_json TEXT NOT NULL, -- [{path, frequency, sessionIds}]
llm-docs/archive/review-context-phase1-spec.md:152:  lookback_sessions INTEGER NOT NULL,
llm-docs/archive/review-context-phase1-spec.md:295:  sessionId: string;
llm-docs/archive/review-context-phase1-spec.md:296:  coChangeLookbackSessions: number;
llm-docs/archive/review-context-phase1-spec.md:322:- `coChangeLookbackSessions`: 5
llm-docs/archive/review-context-phase1-spec.md:338:- Review fails fast when Entire checkpoint/session context is missing.
llm-docs/archive/review-quality-roadmap.md:9:- Resolver logic is hardened for multi-ref and multi-session checkpoint metadata cases.
llm-docs/archive/review-quality-roadmap.md:79:  - checkpoint/session metadata lookup failures
llm-docs/archive/review-prompt-phase2-spec.md:13:- Analysis prompt must consume full Phase 1 `ReviewContext` (changed files, diff hunks, related files, convention files, checkpoint/session context, provenance references).
llm-docs/archive/review-prompt-phase2-spec.md:184:   - checkpoint/session intent context
llm-docs/archive/review-prompt-phase2-spec.md:199:- Explicitly frame co-change related files as historical context from Entire checkpoint session history, not files directly modified in the current commit.
docs/architecture/review-flow.md:85:- The worker must continue rejecting unsupported review target types and unsupported review modes.
docs/architecture/review-flow.md:86:- The policy-first path must preserve its current states and continue requiring explicit approval before enqueuing execution.
docs/architecture/report-ui-flow.md:67:- Review history pages must continue distinguishing active review states from terminal states and grouping history by repo/branch.
docs/architecture/report-ui-flow.md:68:- Policy approval must continue redirecting users from policy routes to report routes once the review advances past the policy stage.
docs/architecture/report-ui-flow.md:69:- Report pages must continue supporting live progress updates, terminal refresh, markdown download, and JSON export without mutating backend review state.
docs/refactor-audit-phase-5.md:5:This document is the handoff for the next refactor session.
docs/refactor-audit-phase-5.md:209:The next branch/session should be disciplined about **not reopening architecture unnecessarily**. The value now comes from making the already-improved structure easy to read, easy to debug, and easy to extend.
docs/architecture/workspace-flow.md:78:- Workspace creation must continue persisting the uploaded source bundle and hydrating the sandbox from that exact bundle.
docs/architecture/workspace-flow.md:79:- File and diff endpoints must continue enforcing path safety and byte limits.
docs/architecture/workspace-flow.md:80:- Reset must continue rebuilding the sandbox from the original stored source bundle rather than from the current mutated state.
docs/architecture/review-studio-experience.md:61:18. Secondary Home CTA should be `Resume active review` when applicable.
docs/architecture/review-studio-experience.md:84:- Secondary `Resume active review` CTA when active review exists
docs/architecture/review-studio-experience.md:99:- No active review: hide `Resume active review` and keep layout stable.
docs/architecture/review-studio-experience.md:454:    "sessionIds": ["ses_x"],
docs/architecture/review-studio-experience.md:456:    "intentSessionContext": ["string"],
docs/architecture/review-studio-experience.md:457:    "rawSessionPrompts": "string",
docs/architecture/review-studio-experience.md:466:      "lookbackSessions": 10,
docs/architecture/review-studio-experience.md:468:      "sessionsScanned": 8,
docs/architecture/review-studio-experience.md:474:    "studioSessionId": "st_abc123"
docs/architecture/review-studio-experience.md:589:1. environment is active/locked by running session
docs/architecture/review-studio-experience.md:597:2. `Promote to edit session`
docs/architecture/review-studio-experience.md:648:| `Resume active review` | no | yes | reuses existing active environment | reconnects UI to existing review/policy route and resumes live status |
docs/architecture/review-studio-experience.md:656:| `Promote to edit session` | no | yes | changes environment mode from `review` to `edit` when safe | updates retention and mutability semantics only |
docs/architecture/review-studio-experience.md:728:1. If Studio dies while a worker-run review continues, the worker remains the source of truth and the review continues.
docs/architecture/review-studio-experience.md:730:3. If browser refresh happens during an active run, the route should reload current review state, then resume live updates.
docs/architecture/review-studio-experience.md:740:Load and resume behavior:
docs/architecture/review-studio-experience.md:754:   - if replay cursor is unavailable or a gap is detected, fall back to full snapshot refresh and continue streaming from the refreshed cursor
docs/architecture/review-studio-experience.md:921:- Keep language consistent with this spec (`Home`, `New Review`, `Review Run`, `Agent Thinking`, `Resume active review`).
docs/architecture/deployment-flow.md:46:  - optional provenance fields such as repo, session IDs, task ID, and operation ID
docs/architecture/deployment-flow.md:70:  - retry recovery may temporarily keep a deployment in `queued` with `retry_scheduled` semantics before execution resumes
docs/architecture/deployment-flow.md:83:- Deployment creation must preserve idempotency semantics and continue persisting the deployment record before background execution begins.
docs/architecture/deployment-flow.md:84:- Cancellation must continue to be safe for both queued and running deployments, even when provider state is only partially known.
docs/architecture/overview.md:104:- Workspace access, review access, and hosted account scoping are enforced at the worker boundary before resource-specific handlers continue.
docs/architecture/review-studio-implementation-plan.md:100:Studio becomes a reusable local service with explicit runtime metadata, instead of a terminal-bound process that dies with the session.
docs/architecture/review-studio-implementation-plan.md:104:- `packages/cli/src/app/reviews/session.ts`
docs/architecture/review-studio-implementation-plan.md:137:- `packages/cli/test/app/reviews/session.test.ts`
docs/architecture/review-studio-implementation-plan.md:217:2. Teach the CLI-side SSE fanout to resume from the last known cursor when possible.
docs/architecture/review-studio-implementation-plan.md:224:   - resume/replay from last known `seq`
docs/architecture/review-studio-implementation-plan.md:340:- `packages/cli/src/app/reviews/session.ts`
docs/architecture/review-studio-implementation-plan.md:380:4. PR 4: event replay/resume plumbing
docs/architecture/review-studio-implementation-plan.md:428:3. Studio can launch, survive terminal exit, resume runs, and render all review states on one route.
docs/architecture/review-studio-implementation-plan.md:454:- replay/resume scaffolding
docs/architecture/review-studio-implementation-plan.md:481:- `Resume active review`
docs/architecture/review-studio-implementation-plan.md:490:4. `Resume active review` appears only when applicable and routes correctly.
docs/architecture/review-studio-implementation-plan.md:499:- resume-active-review scenario
docs/architecture/review-studio-implementation-plan.md:565:5. Browser refresh restores current state and continues live updates.

```

> TOOL

tool_result
id: call_XKonnPaU3VOUBb3TbW4orWLp
```
Command: /bin/zsh -lc 'rg -n "codex" README.md docs llm-docs -S'
Chunk ID: eb004d
Wall time: 0.6293 seconds
Process exited with code 1
Original token count: 0
Output:

```

> AGENT

I didn’t find a repo-specific note, so I’m checking the local `codex` CLI help to confirm the exact syntax.

> TOOL

tool_use exec_command
id: call_fNsGU5sv845sAftv91vgeL8u
```json
{
  "cmd": "codex --help"
}
```

> TOOL

tool_result
id: call_fNsGU5sv845sAftv91vgeL8u
```
Command: /bin/zsh -lc 'codex --help'
Chunk ID: 089fcc
Wall time: 0.5895 seconds
Process exited with code 0
Original token count: 1362
Output:
WARNING: proceeding, even though we could not update PATH: Operation not permitted (os error 1)
Codex CLI

If no subcommand is specified, options will be forwarded to the interactive CLI.

Usage: codex [OPTIONS] [PROMPT]
       codex [OPTIONS] <COMMAND> [ARGS]

Commands:
  exec        Run Codex non-interactively [aliases: e]
  review      Run a code review non-interactively
  login       Manage login
  logout      Remove stored authentication credentials
  mcp         Manage external MCP servers for Codex
  mcp-server  Start Codex as an MCP server (stdio)
  app-server  [experimental] Run the app server or related tooling
  app         Launch the Codex desktop app (downloads the macOS installer if missing)
  completion  Generate shell completion scripts
  sandbox     Run commands within a Codex-provided sandbox
  debug       Debugging tools
  apply       Apply the latest diff produced by Codex agent as a `git apply` to your local working
              tree [aliases: a]
  resume      Resume a previous interactive session (picker by default; use --last to continue the
              most recent)
  fork        Fork a previous interactive session (picker by default; use --last to fork the most
              recent)
  cloud       [EXPERIMENTAL] Browse tasks from Codex Cloud and apply changes locally
  features    Inspect feature flags
  help        Print this message or the help of the given subcommand(s)

Arguments:
  [PROMPT]
          Optional user prompt to start the session

Options:
  -c, --config <key=value>
          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.
          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed
          as TOML. If it fails to parse as TOML, the raw string is used as a literal.
          
          Examples: - `-c model="o3"` - `-c 'sandbox_permissions=["di[REDACTED_SK]"]'` - `-c
          shell_environment_policy.inherit=all`

      --enable <FEATURE>
          Enable a feature (repeatable). Equivalent to `-c features.<name>=true`

      --disable <FEATURE>
          Disable a feature (repeatable). Equivalent to `-c features.<name>=false`

      --remote <ADDR>
          Connect the TUI to a remote app server websocket endpoint.
          
          Accepted forms: `ws://host:port` or `wss://host:port`.

      --remote-auth-token-env <ENV_VAR>
          Name of the environment variable containing the bearer token to send to a remote app
          server websocket

  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt

  -m, --model <MODEL>
          Model the agent should use

      --oss
          Convenience flag to select the local open source model provider. Equivalent to -c
          model_provider=oss; verifies a local LM Studio or Ollama server is running

      --local-provider <OSS_PROVIDER>
          Specify which local provider to use (lmstudio or ollama). If not specified with --oss,
          will use config default or show selection

  -p, --profile <CONFIG_PROFILE>
          Configuration profile from config.toml to specify default options

  -s, --sandbox <SANDBOX_MODE>
          Select the sandbox policy to use when executing model-generated shell commands
          
          [possible values: read-only, workspace-write, danger-full-access]

  -a, --ask-for-approval <APPROVAL_POLICY>
          Configure when the model requires human approval before executing a command

          Possible values:
          - untrusted:  Only run "trusted" commands (e.g. ls, cat, sed) without asking for user
            approval. Will escalate to the user if the model proposes a command that is not in the
            "trusted" set
          - on-failure: DEPRECATED: Run all commands without asking for user approval. Only asks for
            approval if a command fails to execute, in which case it will escalate to the user to
            ask for un-sandboxed execution. Prefer `on-request` for interactive runs or `never` for
            non-interactive runs
          - on-request: The model decides when to ask the user for approval
          - never:      Never ask for user approval Execution failures are immediately returned to
            the model

      --full-auto
          Convenience alias for low-friction sandboxed automatic execution (-a on-request, --sandbox
          workspace-write)

      --dangerously-bypass-approvals-and-sandbox
          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY
          DANGEROUS. Intended solely for running in environments that are externally sandboxed

  -C, --cd <DIR>
          Tell the agent to use the specified directory as its working root

      --search
          Enable live web search. When enabled, the native Responses `web_search` tool is available
          to the model (no per‑call approval)

      --add-dir <DIR>
          Additional directories that should be writable alongside the primary workspace

      --no-alt-screen
          Disable alternate screen mode
          
          Runs the TUI in inline mode, preserving terminal scrollback history. This is useful in
          terminal multiplexers like Zellij that follow the xterm spec strictly and disable
          scrollback in alternate screen buffers.

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

```

> TOOL

tool_use exec_command
id: call_zLTkbSmITBzmRwlTf1BzQN8O
```json
{
  "cmd": "codex resume --help"
}
```

> TOOL

tool_result
id: call_zLTkbSmITBzmRwlTf1BzQN8O
```
Command: /bin/zsh -lc 'codex resume --help'
Chunk ID: 1f9280
Wall time: 0.5859 seconds
Process exited with code 0
Original token count: 1186
Output:
WARNING: proceeding, even though we could not update PATH: Operation not permitted (os error 1)
Resume a previous interactive session (picker by default; use --last to continue the most recent)

Usage: codex resume [OPTIONS] [SESSION_ID] [PROMPT]

Arguments:
  [SESSION_ID]
          Conversation/session id (UUID) or thread name. UUIDs take precedence if it parses. If
          omitted, use --last to pick the most recent recorded session

  [PROMPT]
          Optional user prompt to start the session

Options:
  -c, --config <key=value>
          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.
          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed
          as TOML. If it fails to parse as TOML, the raw string is used as a literal.
          
          Examples: - `-c model="o3"` - `-c 'sandbox_permissions=["di[REDACTED_SK]"]'` - `-c
          shell_environment_policy.inherit=all`

      --last
          Continue the most recent session without showing the picker

      --all
          Show all sessions (disables cwd filtering and shows CWD column)

      --enable <FEATURE>
          Enable a feature (repeatable). Equivalent to `-c features.<name>=true`

      --disable <FEATURE>
          Disable a feature (repeatable). Equivalent to `-c features.<name>=false`

      --include-non-interactive
          Include non-interactive sessions in the resume picker and --last selection

      --remote <ADDR>
          Connect the TUI to a remote app server websocket endpoint.
          
          Accepted forms: `ws://host:port` or `wss://host:port`.

      --remote-auth-token-env <ENV_VAR>
          Name of the environment variable containing the bearer token to send to a remote app
          server websocket

  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt

  -m, --model <MODEL>
          Model the agent should use

      --oss
          Convenience flag to select the local open source model provider. Equivalent to -c
          model_provider=oss; verifies a local LM Studio or Ollama server is running

      --local-provider <OSS_PROVIDER>
          Specify which local provider to use (lmstudio or ollama). If not specified with --oss,
          will use config default or show selection

  -p, --profile <CONFIG_PROFILE>
          Configuration profile from config.toml to specify default options

  -s, --sandbox <SANDBOX_MODE>
          Select the sandbox policy to use when executing model-generated shell commands
          
          [possible values: read-only, workspace-write, danger-full-access]

  -a, --ask-for-approval <APPROVAL_POLICY>
          Configure when the model requires human approval before executing a command

          Possible values:
          - untrusted:  Only run "trusted" commands (e.g. ls, cat, sed) without asking for user
            approval. Will escalate to the user if the model proposes a command that is not in the
            "trusted" set
          - on-failure: DEPRECATED: Run all commands without asking for user approval. Only asks for
            approval if a command fails to execute, in which case it will escalate to the user to
            ask for un-sandboxed execution. Prefer `on-request` for interactive runs or `never` for
            non-interactive runs
          - on-request: The model decides when to ask the user for approval
          - never:      Never ask for user approval Execution failures are immediately returned to
            the model

      --full-auto
          Convenience alias for low-friction sandboxed automatic execution (-a on-request, --sandbox
          workspace-write)

      --dangerously-bypass-approvals-and-sandbox
          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY
          DANGEROUS. Intended solely for running in environments that are externally sandboxed

  -C, --cd <DIR>
          Tell the agent to use the specified directory as its working root

      --search
          Enable live web search. When enabled, the native Responses `web_search` tool is available
          to the model (no per‑call approval)

      --add-dir <DIR>
          Additional directories that should be writable alongside the primary workspace

      --no-alt-screen
          Disable alternate screen mode
          
          Runs the TUI in inline mode, preserving terminal scrollback history. This is useful in
          terminal multiplexers like Zellij that follow the xterm spec strictly and disable
          scrollback in alternate screen buffers.

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version

```

> AGENT

Use:

- `codex resume` to open the session picker
- `codex resume --last` to continue the most recent session directly
- `codex resume <SESSION_ID>` if you already know the session ID/thread name
