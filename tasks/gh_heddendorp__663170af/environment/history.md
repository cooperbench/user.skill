> SYSTEM

# AGENTS.md instructions for /Users/hedde/code/evorto <INSTRUCTIONS> # Repository Guidelines ## Context Discipline - Keep repository knowledge in small, relevant files. - Use this file as the map, not the full manual. - Read the nearest applicable guidance before editing: - root product/system context - module-level `AGENTS.md` - local README files - Update context files when reality changes, assumptions are invalidated, or new constraints are discovered. - Prefer small, accurate updates over large stale manuals. ## Root Context Files - `PRODUCT.md` - product goals, personas, core workflows, domain concepts, and product invariants. - `ARCHITECTURE.md` - high-level system shape, architectural boundaries, and where to look first for common changes. - `QUALITY.md` - behavior-focused verification guidance, Browser/Playwright expectations, and done criteria. Keep these files concise. Put implementation-specific guidance in the nearest module-level `AGENTS.md` or README. ## Project Structure - App code: `src/app/**` - Server runtime and APIs: `src/server/**` - Data layer: `src/db/**` - Shared contracts/types/utilities: `src/shared/**` and `src/types/**` - Unit tests: `*.spec.ts` in `src/**` - Playwright tests: `tests/**` - Legacy e2e reference: `e2e/**` - Assets/public: `public/` - Theming: `src/styles.scss` and `_theme-colors.scss` Start with the nearest applicable module guidance: - `src/app/AGENTS.md` - `src/server/AGENTS.md` - `src/db/AGENTS.md` - `tests/AGENTS.md` More specific guidance may exist deeper in […]

> DEVELOPER

Update the branch from remote

> AGENT

I’ll refresh the local repo state and check the current branch/upstream before changing anything, then use the repo’s existing branch-management convention where it fits.

> AGENT

The checkout is on `main`, currently clean and reported as 2 commits behind `origin/main`. I’m checking whether there is any closer local guidance before fast-forwarding it.

> AGENT

There are no local modifications to protect, and this is `main`, so the right operation is a straight remote refresh plus fast-forward merge. I’m going to fetch first, then update only if it remains a clean fast-forward.

> AGENT

Fetch completed cleanly. I’m checking the exact ahead/behind relationship before applying the fast-forward.

> AGENT

`main` has no local-only commits and is exactly two commits behind `origin/main`, so this is safe to fast-forward.

> AGENT

The fast-forward succeeded to `origin/main`. I’m doing a final status check so I can report the exact new commit and whether the working tree stayed clean.

> AGENT

Updated `/Users/hedde/code/evorto` from remote. `main` fast-forwarded from `c1edf30384f` to `70215b09fb2`, bringing in 2 commits from `origin/main`. Final status is clean and aligned with remote: `HEAD...origin/main` is `0 0`. No tests were run since this was only a branch update. <oai-mem-citation> <citation_entries> MEMORY.md:116-116|note=[checked prior evorto branch sync context] MEMORY.md:139-147|note=[confirmed rebase guidance was for stacked PRs not main fast-forward] </citation_entries> <rollout_ids> </rollout_ids> </oai-mem-citation>

> DEVELOPER

Can you exclude the repos folder from dependabot analysis?

> AGENT

I’ll update the Dependabot configuration so vendored `repos/` content is ignored, then run the repo-required formatting/lint checks if the edit is not Markdown-only. First I’m locating the current Dependabot setup.

> AGENT

There isn’t an existing `.github/dependabot.yml`, so I’m checking whether the repo is using GitHub dependency submission/review configuration elsewhere before adding the minimal supported config.

> AGENT

GitHub’s current `dependabot.yml` supports `exclude-paths`, relative to the configured `directory`, specifically for skipping vendored code during Dependabot update scans. Since there’s no config yet, I’m checking the root package setup so the new config doesn’t accidentally target the wrong ecosystem.

> AGENT

I’m adding a root Dependabot config for the repo’s Bun dependency manifest and explicitly excluding `repos/**`, which is the vendored upstream reference area called out in the repo guidance. This keeps Dependabot’s root scan from walking those vendored package manifests.

> AGENT

The config is in place. I’m running the required formatter and lint now; since this is a YAML-only change, there is no WebStorm file-problems pass needed.

> AGENT

Formatting completed successfully, with existing Prettier config warnings about ignored options. I’m running lint next and then I’ll check the final diff.

> AGENT

Lint passed. I’m checking whether the formatter touched anything besides the new Dependabot file before I wrap up.

> AGENT

`bun run format:write` reformatted several unrelated source files. Since those changes are outside this request and were produced by my verification step, I’m reverting only those formatter side effects and keeping the new Dependabot config.

> AGENT

The unrelated formatter changes are reverted. I’m doing a final targeted validation of the YAML plus one more lint/status check so the final state is clean and scoped.

> AGENT

The new YAML parses and is formatted; only `.github/dependabot.yml` is changed now. I’m running lint once more after reverting the incidental formatter output.

> AGENT

Lint passed again. I’m capturing the final diff for the new config.

> AGENT

Added [`.github/dependabot.yml`](/Users/hedde/code/evorto/.github/dependabot.yml) with a Bun Dependabot update config and `exclude-paths: ["repos/**"]`, so Dependabot skips vendored manifests under `repos/` during update scans. This uses GitHub’s current `exclude-paths` option and Bun ecosystem support docs: [exclude-paths](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference#exclude-paths), [Bun support](https://docs.github.com/en/code-security/reference/supply-chain-security/supported-ecosystems-and-repositories#bun). Verified: - `bun run format:write` completed, with existing Prettier config warnings - `bunx prettier --check .github/dependabot.yml` - YAML parse check - `bun run lint` Final working tree change is only the new `.github/dependabot.yml`.