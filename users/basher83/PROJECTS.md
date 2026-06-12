# PROJECTS — basher83

## basher83/tailnet-microservices ★ dominant (62.5% of sessions)

**What basher83 does here**: Runs an autonomous agent loop to implement microservices according to specifications. Operates a production Kubernetes cluster (Talos, ArgoCD, kustomize). Debugs Kubernetes deployment failures, configures OAuth proxy services, and manages GitOps-driven rollouts.

**Tech stack**: Kubernetes (Talos), ArgoCD (Server-Side Apply / GitOps), kustomize with configMapGenerator, Tailscale/tailnet for service-to-service routing, Anthropic OAuth proxy (custom service enabling Claude API access through a tailnet), GitHub Actions CI.

**Recurring themes**:
- Autonomous agent loop: basher83 fires a standardized numbered spec prompt that tells the agent to read specs, pick from IMPLEMENTATION_PLAN.md or TASK.md, implement with up to 500 parallel subagents, run tests, commit/push, and EXIT. Each iteration handles exactly one phase.
- Kubernetes debugging: ArgoCD sync failures, rollout strategy conflicts, configMapGenerator vs plain resource patterns, pod restart triggers on config changes.
- OAuth proxy configuration and account management: enabling/disabling OAuth pool mode vs passthrough mode, registering accounts via admin API, credential management.
- Tailnet routing: ensuring tests go over the tailnet rather than localhost port-forwards.
- Documentation hygiene: reviewing RUNBOOK.md and specs before committing.

**Notable**: basher83 diagnosed an ArgoCD/SSA edge case (rolling update → recreate strategy change leaves orphaned fields in SSA field ownership) before the agent did, and proposed the correct one-time patch. Later identified that configMapGenerator was the proper structural fix for config-triggered pod rollouts rather than a manual restart workaround.

---

## basher83/lunar-claude (37.5% of sessions)

**What basher83 does here**: Develops and manages a Claude Code plugin marketplace. Registers new plugins, updates marketplace metadata, runs OAuth flows to enroll accounts, and validates plugin CI.

**Tech stack**: Claude Code plugin system (SKILL.md, plugin.json manifests, marketplace.json), mise for CI, GitHub for plugin source repos.

**Recurring themes**:
- Plugin registration: adding new plugins to the marketplace (e.g., `basher83/domain-chassis`). Often starts with a vague ask ("I need to add a new plugin to my marketplace") and corrects when the agent misunderstands the scope ("the plugin is already created. You just need to update the marketplace").
- OAuth account enrollment: registering new accounts through the proxy's registration flow. Ran into OAuth redirect failures (PKCE verifier, "Invalid request format" error) and debugged them by consulting a separate Claude+Chrome session.
- CI validation: verifying that mise CI configurations work as designed.
- Plugin workflow automation: pastes multi-phase plugin creation workflow specs (Phase 1–8: Discovery → Component Planning → Clarifying Questions → Structure → Implementation → Validation → Testing → Documentation).

**Notable**: In this repo basher83 is more "Vague Requester" — starts with a high-level ask, interrupts when the agent goes too deep into a wrong path, and clarifies in a short redirect. The Expert Nitpicker persona is more prominent in `tailnet-microservices`.
