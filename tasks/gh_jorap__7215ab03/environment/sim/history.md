[DEVELOPER]: /ponytail-audit

[AGENT]: <think></think>

[AGENT]: Running a repo-wide ponytail audit: mapping structure and hunting over-engineering patterns.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Glob pattern "**/*" matches every file and is not allowed. Use a more specific glob or no glob.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: # Ponytail audit — jorap.com Repo-wide scan, ranked biggest cut first. **Lists only — nothing applied.** 1. `delete:` Eleven Jul-2026 shareable/key-concept migration scripts (~2,587 lines), hardcoded `NOTE_FIXES` / `KEY_PATCHES`, not in `package.json`. Replacement: git history. [`scripts/fix-shareable-p0-p3.py`, `fix-shareable-thought-review.py`, `fix-shareable-principles.py`, `add-kc-relationships.py`, `expand-short-shareables.py`, `migrate-description-verses.py`, `pad-thin-key-concepts.py`, `polish-note-card-blurbs.py`, `fold-key-concept-refs.py`, `tidy-key-concept-refs.py`, `reformat-note-frontmatter.py`] 2. `yagni:` Three randomizer YAML maintainer scripts (~2,322 lines) with overlapping `yaml.safe_load` / curation logic. Replacement: one `scripts/randomizer-maintain.py` with `build | curate | spectrum` subcommands. [`scripts/build-randomizer-decks.py`, `curate-randomizer-300.py`, `build-spectrum-500.py`] 3. `delete:` `.specify/` PowerShell + spec templates (~583 lines) — GitHub Spec Kit scaffolding, zero Hugo/deploy wiring. Replacement: nothing. [`.specify/`] 4. `delete:` One-shot garden audit scripts (~476 lines), not in `package.json`. Replacement: re-run from git if needed. [`scripts/audit-note-categories.py`, `audit-blog-related-notes.py`] 5. `stdlib:` Hand-rolled `split_frontmatter` / `parse_scalar` / `parse_bool` in six scripts (~150 lines) while `notes_content.split_frontmatter` + `yaml.safe_load` already exist. Replacement: `from notes_content import split_frontmatter`. [`export-anki-deck.py`, `export-okf-bundle.py`, `import-from-obsidian.py`, `lint-flashcard-frontmatter.py`, `audit-flashcard-north-star.py`, `lint-utility-wikilinks.py`] 6. `delete:` Stale non-Cloudflare hosting configs (~134 lines). Canonical deploy is `wrangler.toml` + `pnpm run deploy`. Replacement: nothing. [`amplify.yml.disabled`, `vercel.json.disabled`, `vercel-build.sh.disabled`, `netlify.toml`, `.gitlab-ci.yml`] 7. `yagni:` `search-core.mjs` mirrors `assets/js/search.js` match/rank helpers (~70 lines duplicated). Replacement: one `assets/js/search-core.js` imported by both `search.js` and `test-search.mjs`. [`scripts/search-core.mjs`, `assets/js/search.js`] 8. `delete:` `themes/jorap/assets/js/main.js` (~78 lines) — shadowed by project `assets/js/main.js` via Hugo asset […]

[DEVELOPER]: yes

[AGENT]: <think></think>

[AGENT]: Executing Phase 1 safe deletes, then the smaller shrink items from the audit.

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: <think></think>

[AGENT]: Phase 1 cuts are done. **~4,900 lines removed** across 44 files; Hugo build passes. ### Deleted - **11 one-shot migration scripts** (`fix-shareable-*`, `add-kc-relationships`, `expand-short-shareables`, etc.) - **2 audit scripts** (`audit-note-categories.py`, `audit-blog-related-notes.py`) - **`.specify/`** scaffolding - **Stale hosting configs** (`netlify.toml`, `.gitlab-ci.yml`, `amplify.yml.disabled`, `vercel.*.disabled`) - **Dead `themes/jorap/assets/js/main.js`** (project `assets/js/main.js` wins) - **`issues-total-count.html`** partial ### Shrunk - **`spawnUtil.mjs`** — dropped unused `runLocalBin` - **`themeGenerator.js`** — removed dead `exampleSite` branch - **`layouts/notes/list.html`** — removed duplicate `lint-note-issues` on every list render (`pnpm lint:notes` still covers it) - **`toolbar.html`** — inlined issue count - **`package.json`** — shared `hugo:prod-server` script for `preview` / `watch` ### Consolidated - **`notes_content.py`** — added `split_frontmatter_parts`, `parse_scalar`, `parse_bool` - **6 scripts** now import those instead of hand-rolling parsers ### Skipped (Phase 2 — say when) - **Randomizer script merge** (`build-randomizer-decks` + `curate-randomizer-300` + `build-spectrum-500`) — you have active randomizer edits in the tree - **`pixi.js` / `notes-graph.js`** — intentional Obsidian parity - **`search-core.mjs` dedup** — smaller win, separate pass ### Heads-up - `.github/prompts/speckit.*` and `docs/SPEC.md` still reference `.specify/` — those links are now dead. Want those cleaned up too? No commit created. Say if you want Phase 2 (randomizer merge) or a commit.