> DEVELOPER

do we need /docs for any closed issues since the last release?

> AGENT

Let me check which closed issues already had /docs run (via existing files in docs/) and identify candidates that may need it.

> AGENT

Last release was **v2.2.0** (2026-04-18). Of the ~28 issues closed since then, most are internal skill-prompt tweaks or bug fixes that don't need /docs. Two stand out as user-facing changes lacking a dedicated doc page: | Issue | Title | Why it may need /docs | |---|---|---| | **#540** | Live multi-issue dashboard for `sequant run` | New `sequant dashboard` command — README mentions it, but no `docs/features/*.md` page | | **#574** | `-q` mode liveness heartbeat + one-shot stall warning | Changes the user-visible behavior of `-q`; no doc entry | Already covered or not applicable: - **#533** (spec-by-default), **#554** (assess minimal flags), **#559** (`--security-review` flag) — have `docs/features/*.md` pages. - **#532** — docs-only PR, self-documenting. - **#587, #582, #580, #573, #569, #551, #530, #529** — internal `/qa` and `/spec` prompt changes (no user-facing surface). - **#587, #555, #556** — internal `/assess` heuristics. - **#583, #581, #575, #570, #568, #564, #562, #537, #534, #528** — bug fixes. - **#539** — small warning string; debatable but probably not worth a doc page. - **#531** — internal `/docs` classification logic. Recommendation: run `/docs 540` and `/docs 574`. Want me to kick those off?