> AGENT

Thanks for the release notes. Let me read the current files first.

> AGENT

Current version is `0.3.13`. I see the release notes for the 0.4.x line - this is a significant jump covering replicated SDK bump, image cleanup, and oauth image update. Let me proceed with the bump to `0.4.2` for the dev environment.

> AGENT

Now let me check the diff and recent commits before committing.

> AGENT

Changes look clean - just the version bump in `config.json` and `application.yaml`. No generated files changed (the helm values were already consistent). Let me commit and push.

> AGENT

Done. PR created: https://github.com/konecta-ix-services/kix-services-crewai/pull/262

**Summary of changes:**
- **Branch:** `feat/bump-crewai-chart-0.4.2` → `develop`
- [config.json:80](environments/dev/config.json#L80): version `0.3.13` → `0.4.2`
- [application.yaml:25](environments/dev/argocd/application.yaml#L25): targetRevision `0.3.13` → `0.4.2`
- Helm values verified with `--check` (no generated file changes needed)

> AGENT

There's no `replicatedID` field in this repo. However, `replicated` is used extensively. Let me check what's in the upstream values file you have open.

> AGENT

There is no `replicatedID` field anywhere in this repo. The upstream chart does use a `replicated` section (visible at [values-upstream.yaml:13-16](environments/dev/helm/values-upstream.yaml#L13-L16)) with two fields:

- `replicated.isAirgap` — controls whether the Replicated SDK operates in air-gapped mode
- `replicated.image.repository` — overrides the Replicated SDK image location (pointed at your Artifact Registry mirror)

If you're asking about a specific `replicatedID` field you've seen in the upstream chart's default values, it's not something this repo overrides or sets. It would be a value internal to the CrewAI chart that likely gets auto-populated by the Replicated SDK at runtime (the license ID / install ID). Since you're not in air-gap mode (`isAirgap: false`), the SDK handles that automatically — no need to set it explicitly.