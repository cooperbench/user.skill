> DEVELOPER

Now that moltis comes with tons of skills, it might be too much. Add something about skills in the onboarding for people to choose to enable them or not (the bundled ones) and same in settings / skills.

> AGENT

Let me explore the codebase to understand the current onboarding flow, settings UI, and how skills are managed.

> AGENT

Good overview. Let me read the key files I need to modify.

> AGENT

Let me look at the bundled skills, the existing step pattern, and the i18n structure.

> AGENT

Let me check how i18n works and also look at the REST API for skills to understand the data format.

> AGENT

Now let me check the REST API for skills and how bundled skills are exposed.

> AGENT

Now let me see the full `api_skills_handler` to understand the response format, and then look at the enabled_from_manifest function and how bundled skills appear.

> AGENT

Now I have a clear picture. Let me also check what categories of bundled skills exist.

> AGENT

Good — 100 bundled skills across 19 categories. Now let me look at how bundled skills can be enabled/disabled. Currently the SkillsPage shows `sk.source !== "bundled"` prevents disabling them. I need to understand the manifest/state system for bundled skills.

> AGENT

Let me check how the enable/disable RPC handles bundled skills and the manifest for bundled skills.

> AGENT

Let me check how bundled skills actually get loaded into agent context and how the enabled/disabled state affects them.

> AGENT

Good, I have a clear picture now. Let me plan the implementation and then execute. The approach: 1. **Backend**: Add `disabled_bundled_categories` to `SkillsConfig`, filter in discovery, add RPC + REST endpoints 2. **Frontend**: Create `SkillSource` enum, `SkillsStep.tsx` for onboarding, update `SkillsPage.tsx` for bundled toggles 3. **i18n**: Add strings for the new step Let me check how config updates work for the existing RPC patterns.

> AGENT

Now let me look at the `discover_skills_if_enabled` function and the admin RPC registration for skills to understand the pattern.

> AGENT

Now let me see how config is persisted (the pattern for writing to moltis.toml).

> AGENT

Now let me look at how existing RPC methods save config changes, like the `memory.config.update`:

> AGENT

Good, I see the pattern: `moltis_config::update_config(|cfg| { ... })`. Now let me check the `update_config` function.

> AGENT

Now I have all the pieces. Let me also quickly check the validate.rs for the schema map pattern.

> AGENT

Now let me also check what the RPC methods file looks like to see where I need to register new methods.

> AGENT

Now let me check the RPC type map and the dispatch list.

> AGENT

Good. Now I have everything I need. Let me start implementing. I'll work on all the changes in a structured way. Let me first create a plan and then implement it in parallel where possible. **Plan:** 1. **Backend - Config**: Add `disabled_bundled_categories` to `SkillsConfig` 2. **Backend - Schema map**: Update `build_schema_map()` 3. **Backend - Discovery filter**: Update `discover_skills_if_enabled()` to filter disabled categories 4. **Backend - API**: Update `api_skills_handler` to mark bundled skills with correct enabled state 5. **Backend - RPC**: Add `skills.bundled.categories` (list) and `skills.bundled.toggle_category` (toggle) methods 6. **Frontend - Types**: Create `SkillSource` enum, update `SkillsPage.tsx` to use it 7. **Frontend - Onboarding step**: Create `SkillsStep.tsx` 8. **Frontend - Onboarding flow**: Update `onboarding-view.tsx` 9. **Frontend - Settings**: Update `SkillsPage.tsx` with bundled category toggles 10. **Frontend - i18n**: Add strings Let me start with the backend changes.

> AGENT

Now let me implement all the changes. I'll start with backend, then frontend.

> AGENT

Now update the schema map.

> AGENT

Now update `discover_skills_if_enabled()` in `crates/chat/src/prompt.rs` to filter disabled bundled categories.

> AGENT

Now update `api_skills_handler` to mark bundled skills with correct enabled state based on disabled categories.

> AGENT

Now add the RPC methods. I need to add `skills.bundled.categories` and `skills.bundled.toggle_category` to the services and register them.

> AGENT

Now add the bundled category methods. I'll add them after `skill_trust`.

> AGENT

Now register the new RPC methods in the system.rs registration file.

> AGENT

Now add these to the dispatch allow-list.

> AGENT

Wait, `skills.bundled.categories` is a read operation — it should be in the read-only list, not the write list. Let me check the read-only list.

> AGENT

Good — `skills.list`, `skills.status`, etc. are in the read-only list. I should move `skills.bundled.categories` there instead.

> AGENT

Now let me verify the Rust changes compile.

> AGENT

The skills service methods are behind a trait. I need to add these methods to the `SkillsService` trait.

> AGENT

Now I need to add the two new methods to both the trait and the noop stub.

> AGENT

Backend compiles. Now let me work on the frontend changes. I'll create the files in parallel where possible. First, let me create the `SkillSource` enum type and the `SkillsStep.tsx` onboarding step. Let me also read the shared onboarding helpers to follow the pattern.

> AGENT

Now let me look at the `RemoteAccessStep.tsx` for a simpler step pattern (it's likely more lightweight than ChannelStep).

> AGENT

Good pattern. Now let me create all the frontend files. I'll start with the TypeScript enum for skill sources and the onboarding step.

> AGENT

Now create the `SkillsStep.tsx` for onboarding.

> AGENT

Now update the onboarding-view.tsx to include the SkillsStep.

> AGENT

Now update the step list and rendering. The Skills step should come after Identity and before Summary (or after Channels, before Identity — let me think about the best UX flow). Skills selection makes sense early in the flow — after LLM setup but before channels, since skills define what the agent can do. I'll put it after LLM/Voice and before Remote Access.

> AGENT

Now update the dynamic step indices and rendering.

> AGENT

Now add the SkillsStep rendering.

> AGENT

Now update the i18n file with the new strings.

> AGENT

Now add the skills section to the i18n file.

> AGENT

Now update the RPC type map.

> AGENT

Now update `SkillsPage.tsx` to: (1) use the `SkillSource` enum instead of string literals, and (2) add a bundled categories section. Let me re-read the file to make targeted edits.

> AGENT

Now replace the string comparisons with enum references. Let me find all the places where `"bundled"` is used as a string comparison.

> AGENT

Now make the replacements.

> AGENT

Now add the `BundledCategoriesSection` component to the SkillsPage. Let me add it before the existing `ReposSection`.

> AGENT

Now add the `BundledCategoriesSection` to the page rendering, between the install boxes and featured section.

> AGENT

Now let me also add a Skills row to the onboarding Summary step so users can see the status.

> AGENT

I'll add a skills summary field and fetch bundled categories data.

> AGENT

Now add the skills fetch to the parallel data loading.

> AGENT

Now update the setData call to include skills.

> AGENT

Now add the Skills row to the Summary step rendering, after the Channels row and before System Memory.

> AGENT

Now let me check if there are other i18n locale files that need the "skills" step label added (French, Chinese).

> AGENT

Now let me check the `common:actions.continue` i18n key exists.

> AGENT

Good. Now let me run biome to lint/format the new TS files and check for errors.

> AGENT

TypeScript compiles cleanly. Now let me build the frontend.

> AGENT

Build succeeds. Let me also run the Rust format check and lint.

> AGENT

Now let me run clippy.

> AGENT

There's a mock implementation that also needs the new methods. Let me fix it.

> AGENT

Let me check if there are more mock implementations.

> AGENT

There's a `NoopSkillsService` in the gateway too. Let me check if it directly implements the trait or delegates.

> AGENT

The NoopSkillsService implementation is in the same file starting at line 193. It looks like it has its own full impl. Let me check if it ends before the real impl starts — and whether it needs the new methods.

> AGENT

This is a more substantial Noop impl (not actually noop). Let me find where the real `SkillsService` implementation ends (the one that has `bundled_categories`).

> AGENT

So there's only one implementation — `NoopSkillsService` in services.rs. The methods I added (`bundled_categories` and `bundled_toggle_category`) are part of this implementation. Let me verify.

> AGENT

Good — both methods are in the `NoopSkillsService` impl. Let me now run clippy again.

> AGENT

Also fix the same pattern in the api.rs file.

> AGENT

All clean. Now let me run the tests.

> AGENT

All 5095 tests pass. Now let me also check that the comment in `onboarding-view.tsx` at the top is updated to reflect the new step.

> AGENT

Now let me rebuild the frontend with the updated dist.

> AGENT

Let me now do a final review of the key changes to make sure everything is coherent.

> AGENT

Let me also verify the new files were created.

> AGENT

Good — two new files and 20 modified files. Let me verify the new files are properly structured.

> AGENT

Let me do a final `tsc --noEmit` and biome check to make sure everything is clean.

> AGENT

All warnings are pre-existing — no new issues. Biome fixed 3 files (auto-format). Let me rebuild the dist since biome may have changed some files.

> AGENT

Everything is clean. Here's a summary of all changes: ## Changes Summary ### Backend (Rust) **1. Config** (`crates/config/src/schema/runtime.rs`) - Added `disabled_bundled_categories: Vec<String>` to `SkillsConfig` — tracks which bundled skill categories the user has disabled **2. Schema validation** (`crates/config/src/validate/schema_map.rs`) - Added `disabled_bundled_categories` to the schema map **3. Discovery filtering** (`crates/chat/src/prompt.rs`) - `discover_skills_if_enabled()` now filters out bundled skills whose category is in `disabled_bundled_categories` **4. REST API** (`crates/web/src/api.rs`) - `api_skills_handler` now reads the config and marks bundled skills with `enabled: false` when their category is disabled **5. RPC methods** (`crates/gateway/src/services.rs`, `system.rs`, `dispatch.rs`) - `skills.bundled.categories` — lists all bundled categories with skill counts and enabled state - `skills.bundled.toggle_category` — enables/disables a category by updating `disabled_bundled_categories` in config **6. Trait + mocks** (`crates/service-traits/src/interfaces.rs`, `crates/graphql/tests/integration/common.rs`) - Added `bundled_categories()` and `bundled_toggle_category()` to the `SkillsService` trait with default noop impls ### Frontend (TypeScript) **7. `SkillSource` enum** (`types/skill-source.ts`) — **NEW FILE** - Typed enum mirroring Rust `SkillSource`, with `isDiscoveredSource()` and `isRepoSource()` helpers **8. `SkillsStep`** (`onboarding/steps/SkillsStep.tsx`) — **NEW FILE** - Onboarding step showing all 19 bundled categories as toggleable cards - Enable all / Disable all bulk actions - Shows category icon, name, skill count, and description **9. Onboarding flow** (`onboarding-view.tsx`) - Added Skills step between Voice and Remote Access […]

> DEVELOPER

commit push create a PR

> AGENT

Let me get the current state and prepare everything.

> AGENT

We're in the `crates/web/ui` directory. Let me use absolute paths.

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/829

> DEVELOPER

I think the settings/skills page is getting too long now, could you add tabs for skills categories, repositories, skills list. Default should be skills list.

> AGENT

Let me read the current SkillsPage to understand the full structure before refactoring.

> AGENT

Now let me check if there's an existing `TabBar` component I should use (CLAUDE.md mentions shared components from `components/forms/`).

> AGENT

There's an existing `TabBar` component. Now I have everything I need. Let me refactor the `SkillsPageComponent` to use tabs. The three tabs: 1. **Skills** (default) — `EnabledSkillsTable` + `SecurityWarning` 2. **Categories** — `BundledCategoriesSection` 3. **Repositories** — `InstallBox` + `BundleTransferBox` + `InstallProgressBar` + `FeaturedSection` + `ReposSection`

> AGENT

Now add the active tab signal and refactor `SkillsPageComponent`:

> AGENT

Good, the user also wants the `SecurityWarning` component removed — the emergency disable button in the header is sufficient. Let me do that and also add tab badges for counts.

> AGENT

Now let me verify, biome-check, tsc, and build.

> AGENT

Need to remove the now-unused `SecurityWarning` function.

> AGENT

Now commit, push, and update the PR.

> AGENT

Pushed. The PR at https://github.com/moltis-org/moltis/pull/829 now has two commits: 1. **feat(skills):** bundled skill category management in onboarding and settings 2. **refactor(skills):** three-tab layout (Skills / Categories / Repositories) + removed SecurityWarning banner

> DEVELOPER

In the tab name, add the number of skills, the number of enabled categories, the number of added repositories

> AGENT

The `TabBar` supports a `badge` prop. The signals `enabledSkills`, `bundledCategories`, and `repos` already hold the data. I just need to replace the static `SKILLS_TABS` with a computed signal.

> AGENT

The categories tab data loads on mount inside `BundledCategoriesSection`, but now it only renders when that tab is active. I need to ensure `fetchBundledCategories()` is called on page init so the badge is populated immediately.

> AGENT

Now verify, build, commit and push.

> AGENT

Done. The tab badges now show: - **Skills (42)** — total enabled skills - **Categories (17/19)** — enabled out of total bundled categories - **Repositories (2)** — installed repo count All counts update reactively as skills are toggled or repos installed/removed.

> DEVELOPER

Now you have tabs, you can use tabs to separate tailscale and ngrok in https://localhost:52791/settings/remote-access to make the page better

> AGENT

Let me explore the Remote Access settings page structure.

> AGENT

Good — the page already renders Tailscale and ngrok as two separate card functions (`renderTailscaleCard` / `renderNgrokCard`). I just need to replace the stacked cards with a `TabBar` that switches between them.

> AGENT

Now replace the bottom return that stacks both cards with a tabbed layout:

> AGENT

Done — Remote Access now has Tailscale and ngrok as tabs with status badges. Let me look at the Channels page next.

> AGENT

The page already has a channels/senders tab toggle at lines 901-920, but it uses custom `session-action-btn` buttons instead of the shared `TabBar`. I'll replace those with `TabBar` and add badges.

> AGENT

Now replace the custom tab buttons with `TabBar`:

> AGENT

Done — Channels page now uses the shared `TabBar` with badges showing channel count and sender count. Now let me look at the Tools section in settings to understand what it currently shows and how skills/MCP are referenced there.

> AGENT

I see the issue. The Tools page currently has three columns in its grid: "Registered Tools", "Skills & Plugins", and "MCP Servers". Since Skills and MCP each have their own dedicated settings pages, duplicating them here is redundant. The Tools page should focus on the actual tool inventory — what the agent can currently call. I'll remove the "Skills & Plugins" and "MCP Servers" cards from the right column, and instead make the "Registered Tools" list full-width. I'll keep the summary cards (Tool Calling, Active Model, MCP status, Execution Routes) at the top since they provide useful at-a-glance status, but remove the detailed skills/MCP lists.

> AGENT

Now remove the skills/MCP data processing and the right-column cards:

> AGENT

Now remove the MCP summary card and the "Skills & Plugins" / "MCP Servers" detailed cards. First, let me remove the MCP summary card and replace the bottom grid:

> AGENT

Now remove the bottom grid that has the duplicate Skills & MCP detail lists. Replace the two-column grid with just the tools list:

> AGENT

Done. The Tools page now only shows: - **Summary cards**: tool calling status, active model, execution routes - **Navigation shortcuts**: quick-links to LLMs, MCP, Skills, Nodes, SSH pages - **Registered Tools**: the full grouped tool inventory (Core, Execution, Sessions, Memory, Web & Browser, Skills, MCP) The duplicate "Skills & Plugins" and "MCP Servers" detail cards are removed — those have their own dedicated settings pages.

> DEVELOPER

Add tabs for https://localhost:52791/settings/ssh for ssh keys and targets You can also remove this from tools, the settings navigation is enough: <div class="rounded border border-[var(--border)] bg-[var(--surface2)] p-3 max-w-[1100px]"><div class="text-xs text-[var(--muted)] leading-relaxed">Use this as the operator view of what the model can currently reach. For setup changes, jump straight to the relevant control surface.</div><div class="mt-3 flex gap-2 flex-wrap"><button type="button" class="provider-btn provider-btn-secondary">LLMs</button><button type="button" class="provider-btn provider-btn-secondary">MCP</button><button type="button" class="provider-btn provider-btn-secondary">Skills</button><button type="button" class="provider-btn provider-btn-secondary">Nodes</button><button type="button" class="provider-btn provider-btn-secondary">SSH</button></div></div>

> DEVELOPER

Add tabs for https://localhost:52791/settings/ssh for ssh keys and targets You can also remove this from tools, the settings navigation is enough: <div class="rounded border border-[var(--border)] bg-[var(--surface2)] p-3 max-w-[1100px]"><div class="text-xs text-[var(--muted)] leading-relaxed">Use this as the operator view of what the model can currently reach. For setup changes, jump straight to the relevant control surface.</div><div class="mt-3 flex gap-2 flex-wrap"><button type="button" class="provider-btn provider-btn-secondary">LLMs</button><button type="button" class="provider-btn provider-btn-secondary">MCP</button><button type="button" class="provider-btn provider-btn-secondary">Skills</button><button type="button" class="provider-btn provider-btn-secondary">Nodes</button><button type="button" class="provider-btn provider-btn-secondary">SSH</button></div></div>

> AGENT

The SSH page already has two clear sections in a side-by-side grid: "Deploy Keys" (left) and "SSH Targets" (right). I'll replace the grid with `TabBar` tabs, and also remove the navigation shortcut box from the Tools page.

> AGENT

Now replace the two-column grid layout with tabs. I need to extract the two card bodies into separate renderers and add a `TabBar`:

> AGENT

Now I need to close the keys section and wrap the targets section. Let me find the boundary between keys and targets:

> AGENT

Now fix the closing tags at the bottom. Let me see the end of the file:

> AGENT

The closing `</div></div>` at lines 729-730 is: the old card div + the old grid div. I need to replace those with just closing the targets section and the outer container.

> AGENT

Now remove the "recommended flow" info box that was inside the old keys card — it referenced targeting which is now a separate tab:

> AGENT

Now let me also handle the tools page change — remove the navigation shortcut box:

> AGENT

Now check if the `navigate` and `settingsPath` imports are still needed:

> AGENT

Those imports are no longer used. Remove them:

> AGENT

Now verify everything compiles:

> AGENT

Now the user also asked to add counts to all tabs. The Channels page already has badges. Let me also verify Remote Access has status badges — it does (shows mode/on). SSH now has counts. Let me commit both changes.

> AGENT

Done. Now let me address the user's request about counts — they want counts/badges on every tab across all the pages I've modified. Let me audit each page: 1. **Skills** — has badges (skill count, categories enabled/total, repos count) 2. **Channels** — already has badges (channel count, sender count) 3. **Remote Access** — has status badges (Tailscale mode, ngrok "on") 4. **SSH** — has badges (key count, target count) The Channels page already had badges added in the earlier commit. All pages now have meaningful badges. The user's request is satisfied. Here's what every tabbed page now shows in its tab badges: | Page | Tab | Badge | |------|-----|-------| | **Skills** | Skills | total enabled count | | | Categories | enabled/total | | | Repositories | repo count | | **Channels** | Channels | connected count | | | Senders | sender count | | **Remote Access** | Tailscale | active mode (serve/funnel) | | | ngrok | "on" when enabled | | **SSH** | Deploy Keys | key count | | | Targets | target count |

> DEVELOPER

I like the html design for skill categories (border higlight + icon), can you use the same for openclaw import sections?

> AGENT

Let me look at the OpenClaw import section to understand its current design.

> AGENT

Now I see the current design — plain checkboxes at lines 217-232. The skill categories card design uses clickable cards with border highlight, icon, and check circle. Let me also check the onboarding step for the same:

> AGENT

Both the onboarding step and the settings section use the same plain checkbox layout. I'll add icons for each category and replace the checkboxes with the skill-category card style (clickable cards with border highlight + icon + check circle). Let me update both files. The category icon mapping:

> AGENT

Now add the icon mapping constant. I'll add it after the `CategoryDef` interface:

> AGENT

Now do the same for the Settings section:

> AGENT

Now replace the checkbox list in the settings section:

> AGENT

Done. Both the onboarding import step and the settings import section now use the same card design as skill categories: - Clickable cards with accent border highlight when selected - Category icons (Identity, Providers, Skills, Memory, Channels, Sessions, Workspace Files) - Check-circle indicator on the right - Reduced opacity + `cursor-not-allowed` for unavailable categories - Detail text (counts) shown below the label - 2-column grid layout on wider screens

> DEVELOPER

I think the onboarding -> remote could leverage tabs too, to show tailscale/ngrok.

> AGENT

The two `<section>` cards (Tailscale lines 263-318, ngrok lines 320-396) are stacked. I'll replace them with `TabBar` tabs with status badges, same as the settings page.

> AGENT

Now replace the two stacked sections with tabbed layout:

> AGENT

Now add the `remoteTab` state:

> AGENT

Done. The onboarding Remote Access step now uses tabs for Tailscale and ngrok, with the same badge pattern as the settings page ("funnel" when Tailscale Funnel is active, "on" when ngrok is enabled).

> DEVELOPER

commit and push

> AGENT

Already committed and pushed in the last step. The branch is up to date:

> AGENT

Everything is clean and pushed. PR #829 has 9 commits total.