# Preferences — zchee

## Pushback distribution
- **non_pushback**: 90.7% — he mostly lets the agent run
- **correction**: 6.1% — redirects to different skill or reframes the task
- **failure_report**: 2.8% — build/test failure, pastes the failing command
- **rejection**: 0.5% — `$cancel`, no explanation

## What triggers correction
1. **Wrong approach**: agent tackles GPU rendering when he wants input path tracing → `"Please forgot 'GPU rendering', and do work 'real-terminal trace command...'"` — tells agent to forget the wrong frame, supplies the right one in quotes
2. **Wrong behavior on the binary**: result doesn't match tmux behavior → `"No. In \`tmux\`, will open the new window. Current \`agentmux\` nothing work."` — states expected behavior, states actual behavior, expects agent to figure out why
3. **Build failures**: `"Fix \`zig build --summary all\` failed."` — names the exact failing command, no further detail
4. **Uncommitted or stale changes lingering**: `"Do we need the uncommitted files?"` — asks a question rather than instructing; expects agent to confirm or clean up
5. **Stale repo name**: `"$autopilot Replace to \`agentmux\` repository name to \`zmux\`"` — brief, combined skill + correction
6. **Wrong skill chosen**: relaunches with better skill: `"$deep-interview --deep \"statusline is not drawn correctly. /Users/zchee/Documents/Screenshots/Screenshot 2026-04-07 at 4.10.17.png\""` after a previous skill failed to diagnose

## What triggers failure reports
- Build failure: `"Fix \`zig build test\` fail"` — command, then "fail" or "failed", nothing more
- Feature still not working after a fix attempt: `"Stil \`./zig-out/bin/agentmux new -s test\`, the cursor doesn't show the bar style. Fix it."` — repeats the invocation, notes it still doesn't work
- Input not being accepted: `"$autopilot \"The zsh instance started with \`zmux new -s test\` was not accepting input. Fix it.\""` — wraps a description in a skill call
- Performance regression: `"$autopilot \"The zsh instance started with \`zmux new -s test\` now accepts input, but the delay before keys are registered is too long. I need to investigate the cause and fix it.\""`

## What satisfies him
- 90.7% of turns receive no pushback — he lets work proceed
- When team workers complete and report correctly, he simply reads the next status message
- He chains `$commit` after a working sequence without commenting on quality

## Workflow habits
- **Planning first**: uses `$plan`, `$ralplan`, or `$deep-interview` before `$team`/`$ultrawork` for complex features
- **Team orchestration over solo**: major features go through `omx team` (multi-worker) with leader/mailbox protocol
- **Commit cadence**: triggers `$commit` frequently at checkpoints; also uses commit range squash to clean history
- **Verification**: relies on `zig build test`, `zig fmt --check`, and `zig build --summary all` as the canonical verify loop
- **No explanation requests**: never asks agent to explain code; intent is 26% "understand" but those are OMX system-level summarize requests, not "explain this to me" queries
- **Screenshot-driven UI debug**: attaches screenshot paths when visual bugs are reported: `"/Users/zchee/Documents/Screenshots/Screenshot 2026-04-07 at 7.22.44.png"`
- **Reference to upstream**: expects agents to consult `https://github.com/tmux/tmux` for tmux parity and `https://codeberg.org/ziglang/zig` for Zig stdlib

## Stack preferences visible in prompts
- Zig (`std.Io`, `std.c`, `zig build`, `zig fmt`, `zls`)
- Go (spanner-manager, conventional capitalization of IDs)
- OMX / oh-my-codex skill ecosystem (`$ralph`, `$autopilot`, `$ultrawork`, `$ultraqa`, `$ralplan`, `$team`)
- tmux-compatible architecture as the reference target
- libxev over GCD/io_uring for event loops on macOS
- Protocol Buffers, Terraform mentioned in agent persona but not in direct prompts
