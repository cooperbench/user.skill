> DEVELOPER

Looking at hermes in ~/code/hermes-agent I see it comes with tons of skills already, the loader shows: ██╗ ██╗███████╗██████╗ ███╗ ███╗███████╗███████╗ █████╗ ██████╗ ███████╗███╗ ██╗████████╗ ██║ ██║██╔════╝██╔══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗██╔════╝ ██╔════╝████╗ ██║╚══██╔══╝ ███████║█████╗ ██████╔╝██╔████╔██║█████╗ ███████╗█████╗███████║██║ ███╗█████╗ ██╔██╗ ██║ ██║ ██╔══██║██╔══╝ ██╔══██╗██║╚██╔╝██║██╔══╝ ╚════██║╚════╝██╔══██║██║ ██║██╔══╝ ██║╚██╗██║ ██║ ██║ ██║███████╗██║ ██║██║ ╚═╝ ██║███████╗███████║ ██║ ██║╚██████╔╝███████╗██║ ╚████║ ██║ ╚═╝ ╚═╝╚══════╝╚═╝ ╚═╝╚═╝ ╚═╝╚══════╝╚══════╝ ╚═╝ ╚═╝ ╚═════╝ ╚══════╝╚═╝ ╚═══╝ ╚═╝ ╭──────────────────────────── Hermes Agent v0.10.0 (2026.4.16) · upstream 9f22977f ─────────────────────────────╮ │ Available Tools │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⣀⣀⠀⢀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ browser: browser_back, browser_cdp, browser_click, ... │ │ ⠀⠀⠀⠀⠀⠀⢀⣠⣴⣾⣿⣿⣇⠸⣿⣿⠇⣸⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀ clarify: clarify │ │ ⠀⢀⣠⣴⣶⠿⠋⣩⡿⣿⡿⠻⣿⡇⢠⡄⢸⣿⠟⢿⣿⢿⣍⠙⠿⣶⣦⣄⡀⠀ code_execution: execute_code │ │ ⠀⠀⠉⠉⠁⠶⠟⠋⠀⠉⠀⢀⣈⣁⡈⢁⣈⣁⡀⠀⠉⠀⠙⠻⠶⠈⠉⠉⠀⠀ cronjob: cronjob │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⣿⡿⠛⢁⡈⠛⢿⣿⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ delegation: delegate_task │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠿⣿⣦⣤⣈⠁⢠⣴⣿⠿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ discord: discord_server │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠻⢿⣿⣦⡉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ file: patch, read_file, search_files, write_file │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢷⣦⣈⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ homeassistant: ha_call_service, ha_get_state, ... │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣴⠦⠈⠙⠿⣦⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ (and 12 more toolsets...) │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣤⡈⠁⢤⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠛⠷⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ Available Skills │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠑⢶⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ autonomous-ai-agents: claude-code, codex, hermes-agent, opencode │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⠁⢰⡆⠈⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ creative: architecture-diagram, ascii-art, ascii-video, b... │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⠈⣡⠞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ data-science: jupyter-live-kernel │ │ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ devops: webhook-subscriptions │ │ email: himalaya │ │ claude-opus-4.6 · Nous Research gaming: minecraft-modpack-server, pokemon-player │ │ /root general: dogfood │ │ Session: 20260420_113745_966d4d github: codebase-inspection, github-auth, github-code-r... │ │ mcp: native-mcp │ │ media: gif-search, heartmula, songsee, […]

> AGENT

Let me explore both codebases to understand how Hermes skills work and how Moltis currently handles tools/skills.

> AGENT

Now I have a clear picture of both systems. Here's the good news: **Moltis already has a skill system** (`crates/skills/`) that uses the same SKILL.md format as Hermes. The architecture is already there — what's missing is bundled default content. ## Recommended Approach **Embed default skills in the binary** (same pattern as web UI assets with `include_dir!`), and add a "bundled" discovery source to the existing skill system. ### Concretely, three changes: **1. New crate: `crates/default-skills/`** - Contains a `skills/` directory tree with ported SKILL.md files from Hermes - Uses `include_dir!` to embed them at compile time - Exposes a function like `fn bundled_skills() -> &'static IncludeDir` or an iterator over `(name, metadata, content)` - Binary size impact is small — these are just markdown files **2. Extend skill discovery** (`crates/skills/src/discover.rs`) - Add a 5th source after the existing four (project → personal → registry → plugin → **bundled**) - Bundled skills are lowest priority — anything the user creates overrides them - No filesystem extraction needed; serve directly from memory **3. Port the Hermes skills** - Map Hermes tool references to Moltis tool names (`terminal` → `exec`, `web_extract` → `web_fetch`, `files` → relevant Moltis tools) - Drop skills that […]

> DEVELOPER

I would rather have something like assets for the web-ui (html, etc), with an external directory where we just copy hermes skills (and other skills I'll find online and I "vouched" for security issues), each skill could have metadata for its original source/origin. And have all those skills enabled by default since they've been secured.

> AGENT

Makes sense — a committed assets directory with vetted skills, same pattern as the web UI. Let me look at the exact patterns to follow.

> AGENT

Now let me look at the web assets embedding pattern and the skill reading/prompt generation.

> AGENT

Let me check how the `read_skill` tool loads content and the skill crate's lib.rs.

> AGENT

Clear. A committed assets directory in the skills crate, embedded via `include_dir!`, with origin tracking. Here's the concrete plan: ### Directory layout ``` crates/skills/ src/ assets/ # ← committed skill files (like web/src/assets/) research/ arxiv/SKILL.md polymarket/SKILL.md creative/ ascii-art/SKILL.md productivity/ ... bundled.rs # ← include_dir!, BundledSkillStore ``` ### Origin metadata in each SKILL.md ```yaml --- name: arxiv description: Search arXiv papers and summarize findings origin: source: hermes-agent url: https://github.com/nous-research/hermes-agent commit: 9f22977f copied_at: "2026-04-20" --- ``` ### Key changes 1. **`SkillSource::Bundled`** — new variant, lowest priority (Project > Personal > Registry > Plugin > Bundled) 2. **`SkillOrigin`** — new struct in `types.rs`, deserialized from frontmatter 3. **`bundled.rs`** — `include_dir!` store with dev-mode filesystem fallback (same three-tier pattern as web assets) 4. **Discovery** — `BundledSkillDiscoverer` implements `SkillDiscoverer`, composed with existing `FsSkillDiscoverer` 5. **`ReadSkillTool`** — serves bundled skills from memory in release mode, filesystem in dev mode 6. **Feature flag** — `bundled-skills` in `crates/skills/Cargo.toml`, enabled by default in CLI crate User-created skills (Personal/Project) override bundled ones by name — same priority model as the web assets where filesystem beats embedded. ### What stays the same - Prompt generation (`generate_skills_prompt`) works unchanged — it just sees more `SkillMetadata` - Create/Update/Delete tools only operate on Personal […]

> DEVELOPER

please proceed

> AGENT

Good plan. Let me start implementing. First, let me check some key files for wiring context.

> AGENT

Let me check the gateway features and CLI Cargo.toml.

> AGENT

Good, I have all the context. Let me also look at a few Hermes skills to port as initial examples.

> AGENT

Now let me also check the gateway features for skill-related features and the `registry.rs` file.

> AGENT

Good. Now I have everything I need. Let me start implementing step by step. I'll work on multiple files in parallel where possible. **Step 1**: Types, Cargo.toml changes, and the first bundled skill asset.

> AGENT

Now let me implement all the foundational changes in parallel.

> AGENT

Now update `Cargo.toml` for the skills crate.

> AGENT

Now update `lib.rs` to expose the bundled module.

> AGENT

Now update `prompt_gen.rs` for the `Bundled` source label.

> AGENT

Now create the first bundled skill assets and the `bundled.rs` module. Let me create the asset directory structure first.

> AGENT

Now create the first bundled skill (arxiv) and the `bundled.rs` module in parallel.

> AGENT

Now create the `bundled.rs` module — the core of this feature.

> AGENT

Now add the `CompositeSkillDiscoverer` to `discover.rs`.

> AGENT

Now add the `CompositeSkillDiscoverer` after `FsSkillDiscoverer`:

> AGENT

Now let me update the tools crate and gateway wiring. First, `crates/tools/Cargo.toml`:

> AGENT

Now update the gateway Cargo.toml to forward the feature:

> AGENT

Now update the CLI Cargo.toml:

> AGENT

Now add the `bundled-skills` feature definition in CLI Cargo.toml:

> AGENT

Now the critical part — update `ReadSkillTool` in `skill_tools.rs` to handle bundled skills. Let me update it carefully.

> AGENT

Now update the `execute` method of `ReadSkillTool` to handle bundled skills. The key change: when `meta.source == Bundled`, read from the bundled store instead of the filesystem.

> AGENT

Now add the `source_label` arm for `Bundled` in `read_primary`:

> AGENT

Now add the `read_bundled` function. Let me find a good place for it — right before `read_primary`:

> AGENT

Now wire the gateway. Let me update `post_state.rs`:

> AGENT

Now update `services.rs` to also use the composite discoverer for skill listing in the web UI:

> AGENT

Now do the same for `install_dep`:

> AGENT

Now let me check if there are any other places that match on `SkillSource` exhaustively:

> AGENT

Good — none of these have exhaustive `match` on `SkillSource`, they just use specific variants. The `serde(rename_all = "lowercase")` on the enum handles the new variant for serialization. Let me also check the `services.rs` protected skill check to make sure bundled skills aren't accidentally deletable:

> AGENT

Good — bundled skills won't be marked as `protected` (that only applies to Personal/Project), and the delete tool only operates on the personal skills directory. Bundled skills are inherently read-only. Now let me try to compile to see if everything wires up:

> AGENT

Good — one exhaustive match in `discover.rs`. Let me fix it:

> AGENT

Skills crate compiles. Now check the tools crate:

> AGENT

Tools crate compiles clean. Now check the gateway:

> AGENT

There's another exhaustive match. The gateway builds skills without the `bundled-skills` feature first (some dependency doesn't forward it). Let me check — the gateway's default features include `bundled-skills`, but there might be a non-feature-gated match somewhere. Let me find it:

> AGENT

Clippy/warning issues. Let me see the full errors:

> AGENT

Lint errors on `std::sync::Arc` — the gateway already has `Arc` in scope. Let me fix:

> AGENT

Let me check if `Arc` is already imported in `services.rs`:

> AGENT

There's no `Arc` import at the top level — it must be used via `std::sync::Arc` elsewhere, or the lint is triggered by a different mechanism. Let me check what's imported:

> AGENT

`Arc` is imported at line 17. The lint error is about `std::sync::Arc::new` being fully qualified when `Arc` is already in scope. My fix with `replace_all` was correct. Let me rebuild:

> AGENT

Gateway compiles clean. Let me now run the tests for the skills crate:

> AGENT

All 116 tests pass. Let me also run the bundled-specific tests:

> AGENT

All 4 bundled tests pass. Now let me run the full check including the CLI to make sure the feature chain is correct:

> AGENT

Full build passes clean. Now let me also verify the gateway tests still pass:

> AGENT

Disk space issue on the worktree. That's not related to our changes — the test target needs the full project compilation which fills the disk. The important thing is the `cargo check` passed for all crates. Let me run just the skills crate tests (which don't need llama-cpp):

> AGENT

All 116 tests pass (includes the 4 new bundled tests). Let me also run the tools crate tests:

> AGENT

All 68 skill-related tests pass. Let me run the format check too:

> AGENT

Good, formatting is applied. Let me verify it's clean now:

> AGENT

Clean. Let me do a final full check + tests to make sure everything still works:

> AGENT

Everything passes. Let me summarize what was implemented: ## Summary ### Files created - **`crates/skills/src/bundled.rs`** — `BundledSkillStore` with `include_dir!` embedding, dev-mode filesystem fallback, discovery/read/sidecar methods - **`crates/skills/src/assets/research/arxiv/SKILL.md`** — First bundled skill (ported from Hermes, with `origin` metadata) ### Files modified - **`crates/skills/src/types.rs`** — Added `SkillSource::Bundled` variant, `SkillOrigin` struct, `origin` field on `SkillMetadata` - **`crates/skills/src/lib.rs`** — Exposed `pub mod bundled` (feature-gated) - **`crates/skills/src/discover.rs`** — Added `CompositeSkillDiscoverer` that merges FS + bundled with name deduplication - **`crates/skills/src/prompt_gen.rs`** — `source="bundled"` label for bundled skills in system prompt - **`crates/skills/src/watcher.rs`** — `Bundled` arm in exhaustive match (no-op, not watched) - **`crates/skills/Cargo.toml`** — `include_dir` dep, `bundled-skills` feature - **`crates/tools/Cargo.toml`** — `bundled-skills` feature forwarding - **`crates/tools/src/skill_tools.rs`** — `ReadSkillTool` gains `with_bundled()` constructor, `read_bundled()` function serves from memory - **`crates/gateway/Cargo.toml`** — `bundled-skills` feature (default-on) - **`crates/gateway/src/server/prepare_core/post_state.rs`** — Wires `CompositeSkillDiscoverer` + `BundledSkillStore` into `ReadSkillTool` - **`crates/gateway/src/services.rs`** — Web UI skill listing uses composite discoverer - **`crates/cli/Cargo.toml`** — `bundled-skills` feature (default-on) ### How it works 1. Skills go in `crates/skills/src/assets/<category>/<name>/SKILL.md` — committed, with `origin:` metadata 2. In dev mode: read directly from filesystem for instant iteration 3. In release: served from `include_dir!` (embedded in binary) 4. User skills (Personal/Project) override bundled by name 5. Bundled skills are always enabled (pre-vetted, […]

> DEVELOPER

commit push create a PR

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/797

> DEVELOPER

You can now add all hermes skills by default, just copy them over from the local hermes clone I gave you

> AGENT

67 skills total. Let me first check for sidecar files to copy too, and identify which skills to skip (Hermes-internal).

> AGENT

53 sidecar directories. The mlops category has nested sub-categories (3 levels deep). I need to update my discovery code to handle arbitrary depth, then do a bulk copy. Let me also check the dogfood skill to confirm it's Hermes-internal:

> AGENT

OK — dogfood is actually a QA testing skill (useful), hermes-agent is Hermes-specific, and native-mcp is Hermes-specific. I'll skip just `hermes-agent` and `native-mcp`. First, let me update the discovery code to handle nested directories (for mlops sub-categories), then do the bulk copy.

> AGENT

I need to make both the FS and embedded discovery recursive to handle `mlops/training/axolotl/SKILL.md` (3+ levels). Let me update `bundled.rs`:

> AGENT

Now update the embedded discovery to also be recursive:

> AGENT

Also update `find_skill_dir_fs` and `find_skill_dir_embedded` to search recursively:

> AGENT

Good. Now let me do the bulk copy from Hermes, skipping the two Hermes-internal skills. First, remove the arxiv I created manually (it'll be replaced by the Hermes copy):

> AGENT

Now copy all Hermes skills, preserving directory structure, excluding Hermes-internal ones:

> AGENT

69 skills copied. Now let me clean up any non-SKILL.md files at the category level (like DESCRIPTION.md):

> AGENT

Also remove the empty `mcp/` directory (we excluded `native-mcp` and the category is now empty):

> AGENT

Now inject `origin:` metadata into all SKILL.md frontmatters. Let me get the Hermes commit SHA first:

> AGENT

Let me verify the injection worked:

> AGENT

That sed didn't work correctly. Let me try a different approach — a Python script:

> AGENT

The earlier sed corrupted some files. Let me check and restore from Hermes:

> AGENT

The sed truncated it. Let me re-copy from Hermes and try again more carefully:

> AGENT

Now use a more robust Python script to inject origin:

> AGENT

Let me verify it worked:

> AGENT

Let me also verify a deeply nested one:

> AGENT

Now compile and test:

> AGENT

Let me also verify the total count of discovered skills:

> AGENT

Let me add a quick count assertion to make sure all 69 are discoverable:

> AGENT

Let me write a quick test to print the count:

> AGENT

The tests pass. Now let me check if there are any SKILL.md files that fail to parse (some Hermes skills might have names that fail Moltis validation):

> AGENT

All 69 skills have valid names. Now format and run the full test suite:

> AGENT

All clean. Now commit, push, and update the PR:

> AGENT

69 skills across 18 categories. Now commit and push:

> AGENT

Pushed. PR #797 is updated with both commits: 1. **feat(skills): add bundled skills embedded in the binary** — the infrastructure (BundledSkillStore, CompositeSkillDiscoverer, feature flags, gateway wiring) 2. **feat(skills): bundle all 69 Hermes Agent skills** — all skill content copied from hermes-agent@9f22977f with origin metadata and sidecar files 69 skills across 18 categories, all discoverable and readable from the embedded binary. User skills override bundled by name.

> DEVELOPER

This skill is specific to hermes: crates/skills/src/assets/devops/webhook-subscriptions/SKILL.md but since we have webhooks in moltis you should be able to update it for moltis

> AGENT

Now let me understand how Moltis webhooks work.

> AGENT

Good research. Now I have the full picture. Let me rewrite the skill for Moltis.

> AGENT

Done. The webhook-subscriptions skill now covers the Moltis webhook system instead of Hermes: - **RPC API** (`webhooks.*`) instead of `hermes webhook` CLI commands - **Built-in source profiles** (GitHub, GitLab, Stripe, Linear, PagerDuty, Sentry, generic) - **All auth modes** with constant-time verification - **Session modes** (per_delivery, per_entity, named_session) - **Event filtering**, tool policy, IP allowlists, rate limiting, deduplication - **Concrete examples** for GitHub issues, PR review, Stripe payments, GitLab CI, generic alerts - **Troubleshooting** section with Moltis-specific diagnostics

> DEVELOPER

Look at every skills and see which ones are actually depending on hermes or another tool, I think Moltis skills include frontmatter data to list required tools (cli, etc) for the skill to work, we could include that.

> AGENT

That audit was too shallow — it missed most skills. Let me do a proper one by reading every file.

> AGENT

Almost every skill has Hermes references (from the origin metadata at minimum, but many also in the body). Let me do a deeper scan — grep for Hermes references *outside* the origin block and the author field:

> AGENT

Now let me identify actual external tool dependencies from code blocks:

> AGENT

Now let me check how Moltis `requires:` frontmatter works exactly:

> AGENT

Good — the Moltis `requires:` format uses `bins` (required binaries), `any_bins` (at least one), and `install` (how to install). Now I have the full picture. Let me write a Python script to do the bulk update — adding `requires:` blocks and cleaning up Hermes references:

> AGENT

28 skills updated with `requires:`. Let me verify one:

> AGENT

Now let me make sure everything still parses:

> AGENT

All parse fine. Now let me also check which skills have `apple-notes` — the `a` binary name looks suspicious, let me check:

> AGENT

The binary is `memo`, not `a`. My earlier grep truncated. Let me fix the apple-notes requires:

> AGENT

Now let me verify everything still parses and commit:

> AGENT

Let me now provide a summary of what was found and done, then commit:

> AGENT

Done. Here's the full audit summary: ## Audit Results ### Skills with `requires:` added (28 skills) | Category | Skill | Required Bins | Install Methods | |----------|-------|---------------|-----------------| | apple | apple-notes | `memo` | brew (macOS) | | apple | apple-reminders | `remi` | brew (macOS) | | apple | findmy | `peekaboo` | brew (macOS) | | apple | imessage | `imsg` | brew (macOS) | | autonomous-ai-agents | claude-code | `claude` | npm | | autonomous-ai-agents | codex | `codex` | npm | | autonomous-ai-agents | opencode | `opencode` | brew | | creative | ascii-art | any of: pyfiglet, cowsay, boxes, toilet, ascii-image-converter, jp2a | uv, brew, go | | creative | manim-video | `manim` | uv | | email | himalaya | `himalaya` | brew, cargo | | github | * (5 skills) | `gh` | — | | media | songsee | `songsee` | go | | media | heartmula | `hf` | uv | | media | youtube-content | `python3` | uv | | mlops | huggingface-hub | `hf` | uv | | note-taking | obsidian | `obsidian` | — | | productivity | nano-pdf | `nano-pdf` | uv | | productivity | […]

> DEVELOPER

Please cleanup hermes sections, and use the moltis skill metadata fields to add binary expectations if any

> AGENT

Let me first get a precise picture of what needs cleaning across all files.

> AGENT

That was too broad. Let me be more targeted:

> AGENT

Now I have the complete picture. Let me write a comprehensive cleanup script:

> AGENT

66 files cleaned. Let me verify the cleanup worked and nothing is broken:

> AGENT

Good. Now let me check how many Hermes references remain in bodies:

> AGENT

Down from 100+ to 24 refs in 9 files. Most of the remaining ones are in code/context where a simple regex can't help. Let me fix them individually:

> AGENT

5 remaining — all in `godmode/SKILL.md`, and they're all legitimate references to "Nous Hermes" (the model family name, not the agent) or generic text. These are correct to keep. Let me also verify the frontmatter cleanup was thorough — check that `metadata:`, `dependencies:`, `version:`, `author:` are all gone:

> AGENT

Clean. Only Moltis-native fields remain: `name`, `description`, `origin`, `requires`, `platforms` (6 skills restrict to macOS/Linux), and 1 `license` that isn't MIT.

> AGENT

Done. Here's what changed: **Frontmatter cleaned** — removed from all 69 skills: - `metadata:` / `hermes:` blocks (tags, related_skills, requires_toolsets) - `dependencies:` (Hermes Python packages list) - `prerequisites:` (Hermes env/command checks) - `version:`, `author:`, `license: MIT`, `title:`, `triggers:` **Remaining frontmatter** (Moltis-native only): - `name` (69), `description` (69), `origin` (69), `requires` (28), `platforms` (6) **Body text cleaned** across 66 files: - `~/.hermes/` → `~/.moltis/` or "your environment" - `${HERMES_HOME}` → `${MOLTIS_HOME}` / `${SKILL_DIR}` - "Hermes Agent" → "Moltis" in prose, examples, JSON - "Hermes Integration" sections → "Agent Integration" - `~/.hermes/.env` token lookups in GitHub skills → standard env patterns - Kept "Nous Hermes" (model names) unchanged — only 5 references remain, all correct

> DEVELOPER

Merge main to this branch, commit and push

> AGENT

Clean merge, no conflicts.

> AGENT

Merged and pushed. Branch is up to date with main.

> DEVELOPER

I see +160k lines, where are they from?

> AGENT

162k lines across 411 files — all from the Hermes skills copy. The skills themselves plus their sidecar files (references/, templates/, scripts/).

> AGENT

The bulk is from sidecar reference files: - **unsloth/references/llms-full.md** — 16.8k lines (LLM config reference table) - **unsloth/references/llms-txt.md** — 12k lines - **axolotl/references/api.md** — 5.5k lines - **powerpoint/scripts/office/schemas/*.xsd** — XML Schema files (~39 XSD files) - **research-paper-writing/templates/** — LaTeX templates (.tex, .sty, .bst, .bib, .pdf) These are the heavy hitters. The 69 SKILL.md files themselves are only ~18k lines. The remaining ~144k is reference docs, LaTeX templates, XML schemas, and Python scripts. Want me to trim the large reference files or drop specific sidecar directories? The unsloth references alone are 29k lines, and the powerpoint XSD schemas are another ~15k.

> DEVELOPER

How can we know those are safe?

> AGENT

Good question. The SKILL.md files are passive LLM instructions, but the sidecar scripts (Python, shell, JS) could be executed by the agent via the exec tool. Let me audit them.

> AGENT

Here's the security picture: **Network access** (urllib/requests): `polymarket`, `arxiv`, `excalidraw`, `maps`, `google-workspace` — these make HTTP calls to known public APIs. Expected for their purpose. **exec()/eval()**: `red-teaming/godmode/*` — 4 scripts use `exec(open(...).read())` to load each other. This is inherently dangerous code designed for jailbreaking. **subprocess**: `pixel-art` (ffmpeg), `google-workspace` (gws CLI), `p5js` (render pipeline) — expected for their purpose. **rm -rf**: `p5js/render.sh` — cleans temp frame directory. The real question is: **these scripts never execute automatically**. The `ReadSkillTool` only returns their content as text to the LLM. The agent *could* then write them to disk and run them via exec tool, but that's the agent's choice, same as any code it generates. That said, bundling executable scripts in the binary bloats it and the scripts reference Hermes paths that don't exist in Moltis. The scripts are effectively dead code — useful as *reference* for the LLM but not directly executable. Two options: 1. **Remove all scripts/** directories — the SKILL.md bodies already contain the same instructions as inline code blocks. Saves ~144k lines and eliminates any security concern. 2. **Keep references/templates, remove scripts/** — reference markdown and LaTeX templates are passive content. Only scripts are potentially executable. I'd recommend option 2. […]

> DEVELOPER

but those are from the hermes repo, so I guess it's fine to fully copy them over

> AGENT

Fair point — you've already vetted the source. The scripts came from the Hermes repo you cloned locally, and you're vouching for them. The `origin:` metadata tracks provenance. Nothing more to do here.

> DEVELOPER

anything else to improve? Can you look at ~/code/openclaw and see if there are bundled skills?

> AGENT

72 skills. Three categories: `.agents/skills/` (openclaw-internal), `extensions/` (platform-specific like Feishu/QQBot), and `skills/` (general-purpose). Let me check which ones we already have and which are new:

> AGENT

Background tasks seem to hang. Let me run it directly:

> AGENT

72 skills in openclaw. Here's the breakdown: **Already bundled (10):** nano-pdf, himalaya, blogwatcher, openhue, xurl, notion, apple-reminders, obsidian, songsee, apple-notes **Skip (7 internal):** openclaw-specific project maintenance skills (.agents/skills/) **Skip (11 extensions):** Platform-specific (Feishu, QQBot, ACP, prose, diffs, tavily, lobster) **43 NEW general-purpose skills**, including interesting ones like: - **Useful utilities:** weather, tmux, video-frames, summarize, trello, 1password, slack, discord - **Audio/media:** openai-whisper, openai-whisper-api, sherpa-onnx-tts, sag, spotify-player, sonoscli, blucli - **Smart home:** eightctl (Eight Sleep), camsnap (RTSP cameras) - **Dev tools:** github (consolidated gh CLI), gh-issues, coding-agent, skill-creator, mcporter - **Messaging:** bluebubbles, wacli (WhatsApp), imsg - **Productivity:** things-mac, bear-notes, goplaces, gog (Google Workspace CLI), ordercli **OpenClaw-specific (skip for bundling):** clawflow, clawflow-inbox-triage, clawhub, node-connect, healthcheck, oracle, canvas, voice-call, session-logs, model-usage, peekaboo (some overlap with findmy) Want me to copy over the general-purpose ones that aren't openclaw-specific? I'd estimate ~25-30 of the 43 are genuinely portable.