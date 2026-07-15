---
session_id: "nathanbooth-konecta/claude-code-backup|e19ffde0-8d2f-4dcb-aa46-e8448902d717"
developer: "gh:nathanbooth-konecta"
split: train
source: crawl
repo: nathanbooth-konecta/claude-code-backup
start_time: "2026-02-12T22:13:47.534Z"
n_turns: 4
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

does replicated have an optional field for instance id

> AGENT

Let me check both the codebase and Replicated documentation for this.

> AGENT

Let me check the Replicated subchart's values and how the `replicatedID` is used in templates.

> AGENT

Yes, `replicatedID` is an optional field. In the Replicated SDK Helm chart ([values.yaml:273](charts/replicated/values.yaml#L273)), it defaults to an empty string:

```yaml
replicatedID: ""
```

In the secret template ([replicated-secret.yaml:45](charts/replicated/templates/replicated-secret.yaml#L45)), it's rendered with a fallback to empty string:

```yaml
replicatedID: {{ .Values.replicatedID | default "" | quote }}
```

So it's never required — if you don't set it, it just gets passed as `""` in the SDK config. The Replicated SDK will generate or resolve its own instance identity when `replicatedID` is not provided. The same applies to `appID` on line 274/46.

In your parent chart's [values.yaml](values.yaml), there's no `replicatedID` being set under `global.replicated`, which means it's using the default empty value from the subchart. The SDK handles instance identification automatically in that case.

Sources:
- [Config | Replicated Docs](https://docs.replicated.com/reference/custom-resource-config)
- [Set Helm Values with KOTS | Replicated Docs](https://docs.replicated.com/vendor/helm-optional-value-keys)
