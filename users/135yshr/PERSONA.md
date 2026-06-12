---
name: 135yshr-persona
description: Background and expertise profile for 135yshr
metadata:
  type: user
---

## Role and seniority (inferred)

Mid-to-senior Go developer who writes technical articles as a side practice or personal brand effort. Evidence: manages a 95 %-weight Zenn article repo, runs textlint/markdownlint CI, orchestrates multi-agent writing teams, and self-generates expert-level critiques of DDD/security topics. Likely an individual contributor or tech lead in a Go backend shop (inferred from Go + DDD + Clean Architecture focus and references to "会社のコード" — company code — being off-limits for articles).

## Domain expertise

- **Go**: DDD, Clean Architecture, Repository/QueryService patterns, error handling, interface design, injection attacks
- **Security**: GitHub Actions injection, `fmt.Sprintf` injection, regex injection, CVE analysis
- **Technical writing**: Zenn platform conventions, textlint rules (`no-mix-dearu-desumasu`, `no-doubled-joshi`, `ja-no-weak-phrase`), mermaid diagrams, markdownlint
- **Dev tooling**: tmux/tmuxinator, Claude Code multi-agent (`TeamCreate`, `TaskUpdate`, `SendMessage`), gitmoji commit conventions

## Attitude toward the agent

**Skeptically trusting**: delegates large tasks freely but fact-checks outputs against authoritative sources and pastes corrections as structured refutations. Does not hedge corrections ("修正が間違えています" — not "I think this might be wrong"). Trusts the agent's ability to execute; doubts its accuracy on technical claims.

Persona tags (from annotations): Expert Nitpicker 68 %, Vague Requester 24 %, Mind Changer 2 %. The "Vague Requester" facet shows up in short openers like 「次に公開すると良い記事は何がいいと思いますか？」where context is expected to carry weight.

## Tone

- Japanese: polite but direct; no excessive keigo; says 「ごめんなさい」when self-correcting an earlier instruction
- No emojis in own messages (appears only inside pasted plan/review blocks from slash commands)
- Does not explain rationale for short redirects — just issues the new direction
- Uses「私」strictly (inferred preference: professional/formal over casual)
