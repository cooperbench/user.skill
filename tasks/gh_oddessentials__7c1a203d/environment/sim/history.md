[DEVELOPER]: Howdy! familiarize yourself with this dev container, our patterns, and best practices. We have strict invariants and important local/ci parity rules that must be understood well before we begin.

[AGENT]: I'll dig into the key docs and patterns. Let me start with the files CLAUDE.md points me to, plus the file you have open.

[AGENT]: The spec paths in CLAUDE.md are stale (likely merged and cleaned up). Let me explore the actual current structure.

[AGENT]: The specs dir is gone — that work merged. Let me read the actual current docs: CLAUDE.md, the parity invariants doc, husky dispatchers, and devcontainer config.

[AGENT]: Let me read the governance invariants, the husky dispatcher pattern (the entire.io determinism fix), and the parity doc's structure.

[AGENT]: Excellent — this is a thoroughly documented setup. Let me read the full parity invariants doc (the heart of it) and the self-heal mechanism.

[AGENT]: Very thorough. Let me finish the parity doc (incidents, tradeoffs, platform-conditional collection) and look at the self-heal mechanism.

[AGENT]: Let me verify a couple of load-bearing claims rather than take the docs on faith — the hooks path wiring and the self-heal function.

[AGENT]: I've got a solid mental model now. Here's what I understand about this dev container, its patterns, and the invariants — plus two doc-drift items I want to flag. ## The architecture **Image delivery is decoupled from the repo.** The devcontainer pulls a prebuilt `ghcr.io/oddessentials/ado-git-repo-insights-dev:main` image. It's a *"Dev Containers-ready base,"* not a standalone runnable image — Node 22 arrives via the pinned-by-digest Dev Container Feature (`pnpmVersion: "none"`), and pnpm@9.15.0 via Corepack in `postCreateCommand`. **Dockerfile edits don't take effect until merge + image republish** — this previously caused a dead-hooks bug, which is why hook wiring deliberately avoids depending on image state. **Hook execution is `entire.io`-proof by construction.** Git runs `.husky/_/<hook>` (`core.hooksPath=.husky/_`, confirmed). `entire` re-injects its own wrappers there *every session*, backing up the prior dispatcher as `<hook>.pre-entire` and chaining to it *by path*. The fix (PR #426): `scripts/install-githooks.cjs` writes **self-contained** dispatchers that `exec` the tracked `.husky/<hook>` by hard-coded name (not husky's `$0`-basename `h` resolver, which breaks under the rename). Result: the gate runs in every state with no skip window. `entire` owns session capture; the tracked gate scripts no longer call `entire` (avoids duplicate `Entire-Checkpoint` trailers) — which is exactly why `prepare-commit-msg` and `post-commit` are intentional no-ops. ## The […]