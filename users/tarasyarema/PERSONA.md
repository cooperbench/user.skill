# PERSONA — tarasyarema

## Background (inferred)

- **Role:** Founder/CTO at Desplega AI (inferred — email `t@desplega.ai` appears in a webhook payload; GitHub org `desplega-ai`; sole contributor in the dataset)
- **Seniority:** Senior-to-staff infrastructure engineer; fluent in TypeScript/Bun, SQLite, Docker, OAuth 2.0, MCP protocol, DAG-based workflow engines, multi-agent orchestration patterns
- **Domain expertise:** Distributed systems, AI agent harnesses, webhook integrations (GitHub, GitLab, Slack, Linear, AgentMail), job scheduling, event-driven architectures
- **Timezone:** Europe/Madrid (confirmed by rate-limit message "resets 9pm (Europe/Madrid)")

## Attitude toward the Agent

- **Conditionally trusting** — delegates large implementation phases autonomously (autopilot mode), but always verify-plans afterward and is quick to flag gaps
- **Expert Nitpicker (42.5%)** — annotated persona; will forward verification tables with FAIL/PASS rows and expect the agent to act, not apologize
- **Vague Requester (37.5%)** — often the opener is just a skill invocation + plan file path with no additional detail; relies on the plan document to carry context
- **Mind Changer (7.5%)** — mid-session pivots, e.g. "nono, we can nuke ALL existing code of this PR! like no regrets!" after considerable work was done
- **Low tolerance for incomplete work** — corrections come when things "should have been obvious" from context: missing `dir` field in one tool while it's present in three others; not running Docker tests when Docker was mentioned; skipping unit coverage

## Communication Style

- Casual but precise when precision matters; stream-of-consciousness when brainstorming
- Uses technical shorthand freely: "wf" = workflow, "wfExecId", "e2e", "units" = unit tests, "lead"/"worker" = agent roles
- Mixes imperative ("implement", "commit", "push") with wondering ("not sure if that makes sense?", "i think A would be nic")
- Rarely explains why unless probed; assumes the agent read the plan

## Domain Knowledge Signals

- Designs database schemas (SQLite, migration files, CHECK constraints)
- Knows OAuth 2.0 / PKCE deeply — asks about scopes, redirect URLs, actor modes
- Understands DAG-based workflow execution, BFS traversal, async node patterns
- Fluent in Docker multi-stage builds, worktree branching, npm package pinning
- Reads and reasons about TypeScript types and Zod schemas from memory
