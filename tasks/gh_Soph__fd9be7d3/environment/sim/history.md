> AGENT

I'll generate a changelog. Let me start by gathering data about recent changes.

> AGENT

Let me confirm the version number — there's a new `convert-sha256` subcommand (new feature) plus fixes, which suggests a minor bump.

> AGENT

Added the **0.6.0** entry (dated 2026-06-03) to the top of `CHANGELOG.md`: - **Added** — `git-sync convert-sha256` subcommand ([#66](https://github.com/entireio/git-sync/pull/66)) - **Changed** — deferred credential helper / git-style auth flow ([#65](https://github.com/entireio/git-sync/pull/65)); streaming bootstrap commit-graph fetch with memory wins ([#61](https://github.com/entireio/git-sync/pull/61)) - **Fixed** — materialized push against CDN-fronted HTTP targets ([#64](https://github.com/entireio/git-sync/pull/64)) - **Housekeeping** — go-git bump to alpha.4 ([#60](https://github.com/entireio/git-sync/pull/60)) Notes: - **No Thanks section** — all contributors (Andrea Nodari `@entire.io`, Soph, and `computermode`) are internal. - **Omitted PR #62** ("Remove checkpoints version 2 setting") — it only edits this repo's `.entire/settings.json` dogfooding config, not git-sync behavior, so it's not user-facing. Let me know if you'd rather list it under Housekeeping.