---
name: terse-course-correct
description: basher83 redirects an agent that is heading the wrong way with a very short, lowercase, sometimes incomplete sentence — often interrupting before the agent finishes. Trigger: agent makes a wrong assumption about routing, scope, or context.
---

When the agent proceeds on a wrong assumption, basher83 does not wait for it to finish and does not write a paragraph explaining the error. He fires a short interrupt — sometimes just one clause — that states what's wrong and what the right path is.

Characteristics:
- Starts with "hold on", "wait", or jumps straight to the correction
- Lowercase, no terminal period
- States the correct path or the missing context without explaining why the agent was wrong
- May follow up with a second one-liner if the agent still misses it
- Sometimes uses `[Request interrupted by user]` first, then the correction

**Examples:**

> "hold on, why are you trying to curl through the port fwd? the real test is over tailnet to the proxy"

> "i thought we just fixed that via kustomization.yaml"

> "isn't the proper fix:  Migrate from configmap.yaml as a resource to configMapGenerator in kustomization.yaml — then any config change automatically gets a new hash suffix, which changes the pod spec, which triggers a rollout"

> "Sry I wasn't clear, the plugin is already created. You just need to update the marketplace. The one I need to register is https://github.com/basher83/domain-chassis."

> "you can swap the kubectl auth to the on disk config for the mcp. i think its at ~/.config/kubectl mcp something like that. actually you can see it in ~/.claude/plugins/cache/omni-scale/"

> "well lets do it"  *(when agent asks permission to proceed instead of proceeding)*

> "lets review repo docs and make sure everything is updated properly before we commit it all"  *(when agent moves to commit too soon)*
