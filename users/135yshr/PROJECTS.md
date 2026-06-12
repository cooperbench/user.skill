---
name: 135yshr-projects
description: Repo-level context for 135yshr's active projects
metadata:
  type: project
---

## 135yshr/documents ★ dominant (95.1 % of sessions)

**What the user does here**: Writes, reviews, and publishes technical articles on the Zenn platform. Articles are Markdown files under `articles/` with YAML frontmatter (`published`, `emoji`, `topics`). Images live in `images/`. A `CLAUDE.md` defines article style rules (ですます調, 一人称「私」, original code only).

**Tech stack**: Node.js toolchain (`prettier`, `markdownlint-cli2`, `textlint` with `no-mix-dearu-desumasu`/`no-doubled-joshi`/`ja-no-weak-phrase` rules), `zenn-cli`, GitHub Actions CI, `gh` CLI.

**Recurring themes**:
- Go + DDD / Clean Architecture article series (17+ articles, multi-agent writer pipeline via `TeamCreate`)
- Security vulnerability series (GitHub Actions injection, `fmt.Sprintf` injection, regex injection, Trojan Source CVE)
- AI coding tools / Entire.io meta-articles (AI attribution, "コードを読むのをやめた")
- Textlint fixes across batches of articles before PRs
- CodeRabbit PR review integration; user pastes nitpicks and expects fixes

**Branch naming**: `feature/ddd-ca-series`, `add-security-vulnerability-articles`, `publish/<article-name>`, `replace-todo-with-experiments`

**Publish workflow**: draft at `published: false` → content review + lint → `published: true` → commit → push → PR

---

## 135yshr/savanna-vet-go (4.9 % of sessions)

**What the user does here**: Appears to be a Go service project (inferred from name and low session count). Minimal evidence in digest; sessions likely involve code generation or debugging.

**Tech stack**: Go (inferred)

**Note**: Referenced alongside `meow` and `code-tempo` as the user's other Go repos, but `savanna-vet-go` is the only one in `stats.repos`. The others (`meow` — a Go programming language/transpiler; `code-tempo`) are mentioned in article context as source material for screenshots and code examples.
