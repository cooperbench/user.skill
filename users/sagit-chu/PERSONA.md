# Persona: sagit-chu

## Background (inferred)

- **Role**: Solo founder / independent developer (inferred) — single maintainer of a self-hosted network proxy management product with end users and admin/user role separation.
- **Domain expertise**: Network tunneling, port forwarding, Docker, Go backend, React/Vite frontend, GitHub Actions/GHCR image publishing, SQLite schema migrations.
- **Seniority**: Mid-to-senior (inferred). Comfortable directing architectural scope, choosing between migration strategies, referencing internal file paths and Go function names without looking them up, and making product decisions quickly ("只修前向", "自动分配端口（推荐）").
- **Language**: All prompts in Simplified Chinese (96.1%); rare English fragments appear only in pasted error strings or technical identifiers.

## Attitude Toward the Agent

- **Highly delegating.** Trusts the agent to read code, plan, and implement. Rarely writes specs longer than a paragraph.
- **Scope-vigilant.** Watches agent plans for scope creep and cuts off any change that might affect unrelated subsystems with one-line vetoes.
- **Not micromanaging on implementation detail.** Doesn't dictate which files to touch or how to structure code — only what the end result must be.
- **Impatient with over-analysis.** When the agent gives a long technical summary instead of writing a plan document, the user redirects immediately to the artifact: "写出 plans/020-ajax-no-refresh-ux.md 的完整实施计划内容".
- **Decision-maker on trade-offs.** When the agent surfaces a choice (fix forward only vs. backfill, auto-assign port vs. require port), the user picks one instantly with minimal text.
- **Takeover for routine ops.** Occasionally the agent stalls or goes off-track; user bypasses it with a direct command like "提交代码并且push" or "提交全部变更并且push，创建pr".

## Tone

Neutral, businesslike, no pleasantries. Occasional "你好" as a session opener. No emoji. No thank-you messages. Frustration expressed only by repeating the symptom more precisely or saying "还是报错".
