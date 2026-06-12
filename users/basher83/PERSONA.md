# PERSONA — basher83

## Role and seniority (inferred)

Senior infrastructure or platform engineer, likely at a company running Kubernetes in production on Talos. Has operational ownership of at least two distinct systems: a Tailscale-based microservices cluster (`tailnet-microservices`) and a Claude Code plugin marketplace (`lunar-claude`). Comfortable enough with ArgoCD internals, SSA (Server-Side Apply) semantics, and kustomize generator patterns to correct an agent's diagnosis rather than just accept it.

The "founder or staff-level IC" profile fits (inferred): he writes orchestration specs that look like system design documents, manages CI/CD pipelines, and handles Git auth constraints, yet also does casual "hey, can you help me add a plugin" tasks. Breadth suggests either a small team or a lead who touches everything.

## Domain expertise

- **Kubernetes / ArgoCD**: knows rollout strategies, SSA field ownership, sync failure modes, kustomize configMapGenerator hash-suffix trick for config-triggered rollouts. Cites specific edge cases by name ("known Argo CD slash SSA edge case that only triggers on strategy type changes").
- **Tailscale / tailnet networking**: understands the difference between `port-forward` localhost tests and a proper tailnet routing test; corrects agent when it uses the wrong path.
- **OAuth2 / PKCE**: familiar with the flow well enough to know when a PKCE verifier expires or a redirect is failing at the server vs. client side.
- **Claude Code plugin system**: knows the plugin marketplace structure, `plugin.json` manifests, and can register repos to the marketplace. Uses MCP tools (omni-scale kubernetes, git-workflow).
- **SSH / 1Password key management**: operates remotely over SSH, understands that 1Password SSH keys have no on-disk fallback, and asks for workarounds rather than assuming they exist.

## Attitude toward the agent

- **Trusting by default, but a quick trigger for corrections**: 74.6% of prompts are non-pushback; when the agent is on track he approves with one-liners. But when it makes an architecture assumption or misses a root cause, he corrects immediately and precisely.
- **Delegates implementation, keeps architecture**: will let the agent write code, update docs, and run tests. Retains decisions about routing, deployment topology, and when to commit.
- **Impatient with process theater**: interrupts agents that ask clarifying questions when the answer is already obvious ("well lets do it", "send it", "pls do"). Does not want to be walked through options.
- **Comfortable with AI autonomy at scale**: fires specs calling for "up to 500 parallel Sonnet subagents" without apparent concern — this is a user who understands multi-agent orchestration and uses it as a tool.
- **Brings his own second opinions**: consulted another Claude+Chrome session during a debugging impasse and pasted the result back ("I used Claude and Chrome directly, and here's what he said").

## Tone

Casual to the point of terse in interactive mode. Professional and precise in correction mode — no hostility, just crisp technical rebuttals. "Sry" instead of "Sorry". Uses "cool", "great", "awesome", "interesting" as approval signals. Does not say "please" or "thank you" but not rude — just efficient.
