# Persona — zchee

## Identity (inferred)
Japanese developer, Asia/Tokyo timezone. Public GitHub username is `zchee`. Non-native English speaker — communicates in broken English for corrections; his OMX config instructs agents to "keep internal reasoning in English, even if the user writes in Japanese," implying he does write Japanese elsewhere.

## Role (inferred)
Systems engineer / tool author, likely independent or small team. He is building `zmux` — a from-scratch Zig terminal multiplexer with Metal/Vulkan GPU rendering — as a personal project with production ambitions (tmux parity is the explicit goal). He also maintains `spanner-manager` (Go, Google Cloud Spanner tooling) and `agent` (his OMX orchestration framework itself).

## Seniority signals
- Built an entire multi-agent orchestration framework (OMX) from scratch, including leader/worker protocol, mailbox messaging, team panes, skill files, and tmux-driven pane injection
- Configures agents with a 30-year-senior-architect persona: "Go, Python, Lua, TypeScript, C, C++, Objective-C, Protocol Buffers, Terraform, Microservices architecture, Performance optimization at scale"
- Specifies Zig stdlib APIs precisely: `std.Io`, `std.c.read`, `zig build --summary all`
- References tmux source at github.com/tmux/tmux and Zig source at codeberg.org/ziglang/zig when directing agents
- Understands low-level systems: GCD (Grand Central Dispatch), io_uring, libxev, OSC probe sequences, startup relay state machines, PTY framing

## Attitude toward the agent
**Complete delegator, impatient monitor.** He trusts the agent to execute autonomously ("EXECUTE TASKS TO COMPLETION WITHOUT ASKING FOR PERMISSION") and watches pane output to see if workers are stalled or have messages pending. When something is wrong, he redirects to a different skill rather than debugging himself. He cancels (`$cancel`) when the approach is clearly wrong. He never explains the bug in depth — just names the symptom and expects investigation.

## Tone
- Detached and operational; sessions feel like monitoring dashboards, not conversations
- Corrections are redirects, not criticisms
- Occasional philosophical note: "I thought affected by GPU rendering, not?" — musing, not demanding
- No praise or pleasantries observed in the dataset
