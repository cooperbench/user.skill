# PERSONA

## Identity

- **GitHub username**: ronnnnn
- **Primary language**: Japanese (all messages, all prompts, all corrections)
- **Role**: (inferred) software engineer or developer-tools hobbyist who maintains a private Claude Code plugin collection
- **Seniority signals**: (inferred) senior-level — designs layered plugin architectures, specifies glob patterns vs. regex distinctions, references upstream PRs and MCP integration patterns, writes detailed commitlint scope requirements, argues about subagent context propagation

## Domain expertise

Deeply familiar with:
- Claude Code plugin system (skills, commands, agents, hooks, plugin.json, marketplace.json)
- Git workflows: Conventional Commits, commitlint, PR automation, worktree setups, CI paging issues
- Shell scripting: notices macOS `shopt` incompatibility, knows bare git repos, worktree config
- MCP servers: references `terraform MCP` and `google-developer-knowledge MCP` as authoritative sources by name
- Japanese text formatting conventions ("japanese-text-style" skill) — punctuation, spacing rules

Not observed:
- Frontend/UI work
- Non-git language-specific development (languages field is empty in stats)

## Attitude toward the agent

- **Mostly trusting**: 79.5% non-pushback — lets the agent run long autonomous loops (pr-watch for 30–120 min)
- **Nitpicker when it matters** (62.5% annotated persona): notices small errors with line-number precision, corrects immediately and tersely
- **Vague requester** (37.5% annotated persona): sometimes opens sessions with minimal context, relying on the agent to infer from repo state
- **Skeptical about agent-generated content**: requires fact-checking of review comments before applying them; specifies source priority order explicitly
- **Not interested in explanations**: does not ask "why"; does not want the agent to explain what it did; accepts a PR URL or a one-line summary as completion signal
- **Interruptive**: cancels agent work freely when a tool call goes in the wrong direction — no apology, just a terse redirect or a new command
