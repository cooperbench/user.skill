---
name: docker-build-push
description: After frontend or backend changes are complete, issues the standard docker build+push command verbatim. Trigger whenever a development cycle on vite-frontend or flux-panel-backend concludes.
---

Sagit-chu ends many work sessions (or mid-session checkpoints) by building and pushing Docker images to GHCR. The command is nearly identical every time, issued as a flat imperative with no preamble.

The canonical form:
```
编译docker 镜像 ghcr.io/sagit-chu/vite-frontend:beta linux/amd64架构 推送
```

Variants (multi-image builds):
```
编译docker镜像 vite-frontend flux-panel-backend，beta版本，推送到ghcr.io/sagit-chu linux/amd64架构
```

Key invariants:
- Architecture is always `linux/amd64架构` (explicit every time)
- Registry is always `ghcr.io/sagit-chu/`
- Tag is `beta` for development builds; `alpha` for pre-release tags
- No explanation of why; it's a routine punctuation mark on completed work

This command appears 4+ times in the digest across different sessions — it is the most repeated single prompt in the corpus.
