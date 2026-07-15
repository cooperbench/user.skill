> DEVELOPER

perform a deep review of this project against https://github.com/github/spec-kit/tree/main which one is better?

> AGENT

I'll dig into both projects in parallel — explore this repo's structure and content, and research spec-kit.

> AGENT

Let me read this project's README and research spec-kit in parallel.

> AGENT

Let me ground the comparison by reading a representative Shaper skill and spec-kit's actual templates.

> AGENT

I've reviewed both in depth. Here's the comparison, grounded in what each actually ships. ## What each one is **spec-kit** (GitHub, official) — a packaged, agent-agnostic toolkit for **Spec-Driven Development**. A real CLI (`specify`, installed via `uv`), versioned releases, support for 30+ coding agents, and a tight 7-step pipeline centered on one idea: the *spec* is the executable source of truth, code is generated output. Its arc: `constitution → specify → clarify → plan → tasks → implement → analyze → converge`. It scaffolds `.specify/` (templates, bash scripts, constitution) and produces `specs/<feature>/{spec,plan,tasks,data-model,research,contracts}`. **Shaper** (this repo, personal project) — a Markdown-only skill pack encoding **engineering discipline as enforced gates**, biased toward Claude Code. Much wider arc: `idea triage → project → design/spikes → delivery → build/debug/simplify → verify/review → pr-prepare/finishing`. It ships skills, a SessionStart navigator hook, mechanical hooks (stop-the-line, ta[REDACTED_SK]), persistent rule files (PRODUCT_RULES, eng-principles), and is structured so an orchestrator (drain-cycle) can drive a delivery plan unattended. ## Where they actually differ | Dimension | spec-kit | Shaper | |---|---|---| | **Lifecycle covered** | "We've decided to build feature X" → working code | "Is this worth building?" → shipped, reviewed PRs | | **Front of funnel** | None […]