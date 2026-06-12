# PREFERENCES — basher83

## Pushback distribution

- Non-pushback: 74.6% — he follows the agent's lead most of the time
- Correction: 16.9% — redirects when agent has wrong mental model of infra/routing/architecture
- Failure report: 8.5% — typically UI or auth failures; reported visually with screenshots

## What he corrects

**Architecture and routing assumptions**: When the agent uses the wrong test path ("hold on, why are you trying to curl through the port fwd? the real test is over tailnet to the proxy"), assumes a permanent fix where a one-time patch suffices ("I likely don't need a permanent annotation at all"), or proposes a workaround when the proper structural fix is known ("isn't the proper fix: Migrate from configmap.yaml as a resource to configMapGenerator").

**Missed steps in a diagnosis**: Will point out what the agent omitted rather than just accepting the conclusion ("One thing missed on the diagnosis. After the sync succeeds verify the 401 clear up").

**Context the agent didn't have**: Redirects when the agent over-engineers a task it misunderstood ("Sry I wasn't clear, the plugin is already created. You just need to update the marketplace").

**Config/auth paths**: Knows where config files live and directs the agent there ("you can swap the kubectl auth to the on disk config for the mcp. i think its at ~/.config/kubectl mcp something like that. actually you can see it in ~/.claude/plugins/cache/omni-scale/").

## What satisfies him

- Clean diagnosis with clear severity, evidence, and remediation steps (spec for k8s diagnosis includes explicit formatting requirements)
- Agent takes action without being asked twice ("well lets do it", then "send it")
- Tests over the correct path (tailnet, not port-forward)
- Documentation updated before commit
- CI passing, confirmed in cluster

## Workflow habits

**Planning style**: In automation mode, planning is baked into the spec — the agent reads IMPLEMENTATION_PLAN.md or TASK.md and picks the most important item. In interactive mode, basher83 does not plan out loud; he starts with a high-level ask and redirects as needed.

**Test-driven?**: Not explicitly. Tests are run after implementation ("run the tests for that unit of code that was improved"), not before. CI verification is a checkpoint ("lets verify ci cleared"), not a gating ritual.

**Commit cadence**: Commit at the end of each logical unit of work (automation spec mandates this). In interactive mode, commits at natural stopping points after verifying docs. Uses `/git-workflow:git-commit` slash command rather than raw git commands.

**Explanations vs. results**: Prefers results. Asks for explanations only when something is genuinely novel ("cool, can you look at the oauth proxy and tell me how it works at a high level", "that is interesting, so the admin api ... how does one interact with that?"). Once he understands, switches immediately to action ("sounds pretty well thought out and implemented. can we see if theres any accounts in there").

**Interrupts freely**: Does not wait for the agent to finish if it's heading the wrong way. Uses `[Request interrupted by user]` without explanation, then follows up with a short redirect.

**Docs before commit**: Consistent pattern — asks to review/update documentation before committing ("lets review repo docs and make sure everything is updated properly before we commit it all").

## Tool and stack preferences

- Claude Code (100% of sessions)
- MCP plugins: omni-scale kubernetes (`k8s-diagnose`), git-workflow (`git-commit`)
- Kubernetes / ArgoCD / Talos / kustomize
- Tailscale for service networking
- GitHub CLI (`gh auth setup-git`) for auth in constrained environments
- mise for CI toolchain management
- Port cleanup discipline: "make sure to close out any port fwds that were opened"
