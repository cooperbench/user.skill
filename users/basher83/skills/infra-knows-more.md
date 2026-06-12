---
name: infra-knows-more
description: basher83 delivers precise infrastructure corrections when the agent's diagnosis or fix is technically incomplete or wrong — citing specific Kubernetes/ArgoCD/kustomize concepts by name and proposing the correct solution. Trigger: agent misdiagnoses a k8s failure, proposes a workaround when a structural fix exists, or omits a post-fix verification step.
---

When the agent gets infrastructure wrong, basher83 does not ask a question — he states the correct answer. He knows the system well enough to identify the exact edge case (e.g., ArgoCD SSA field ownership after strategy type change) and explain why the agent's diagnosis was incomplete or its fix was insufficient.

Characteristics:
- Confident, declarative corrections — "The root issue is...", "isn't the proper fix..."
- Cites named concepts: "known Argo CD slash SSA edge case", "configMapGenerator", "hash suffix", "rollout"
- Points out what the agent missed rather than just disagreeing ("One thing missed on the diagnosis")
- May propose the correct architectural pattern as a leading question: "isn't the proper fix: [description]?"
- Writes in complete sentences with proper capitalization when the topic warrants it — a departure from his usual lowercase
- Does not require the agent to validate his understanding; he already knows he's right

**Examples:**

> "The root issue is that I switched from rolling update to recreate and SSA couldn't remove the orphaned rolling update spec. This is a known Argo CD slash SSA edge case that only triggers on strategy type changes. It won't reoccur on normal deploys so the one-time patch is probably sufficient. I likely don't need a permanent annotation at all. One thing missed on the diagnosis. After the sync succeeds verify the 401 clear up. The diagnosis attributes them to stale config but confirm the new config map content is actually correct. The hashed config map was generated from the same source data so it should be fine but worth a quick sanity check on the running pods mounted config after recovery"

> "isn't the proper fix:  Migrate from configmap.yaml as a resource to configMapGenerator in kustomization.yaml — then any config change automatically gets a new hash suffix, which changes the pod spec, which triggers a rollout"

> "i thought we just fixed that via kustomization.yaml"  *(terse follow-up when the longer explanation was ignored)*
