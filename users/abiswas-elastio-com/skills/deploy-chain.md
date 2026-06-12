---
name: deploy-chain
description: >
  Trigger: agent has finished implementing a feature or fixing a bug. User expects
  the full commit → CI → staging → promote → prod chain to happen automatically,
  and will push back if the agent stops short.
---

# Deploy chain

After any substantive code change, this user expects the full deploy pipeline to run without being asked. Stopping after "code is done" without deploying triggers a correction.

The expected chain:
1. Commit changes with meaningful message
2. Push to `main` → triggers Travis CI + staging webhook deploy
3. Verify staging is healthy
4. `./script/server promote` (or `gh workflow run deploy-production.yml`) → production
5. Verify production health endpoint
6. Close any related tasks in TaskAI (comment + mark done)

**Correction examples when agent stops short:**
> "is it deployed to prod? do it and close all tasks"

> "it is healthy but did we cimmit, start ci cd pipeline and thewn promote to prod"

> "please deploy, i don;t see the changhes"

> "yes, actually, make another change, then push to staging, then promote and then push to prod"

> "finish the tasks then push yo staging then ptod"

**Shorthand steering after a deploy question:**
> "deploy to production via staging"

> "deploy to staging and then production"

Note: The user uses Travis CI (not GitHub Actions) for the deploy pipeline. Corrects the agent if GitHub Actions is used: "we should not be using github at all, this should be fully travis."
