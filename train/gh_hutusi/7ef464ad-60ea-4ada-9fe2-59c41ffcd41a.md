> DEVELOPER

let's take a look at the home page, try to refine it. 1, I think the slogan fonts seems too big, may be small is better. 2. the number of "x skills, cureated for your team" is not right, I think it should show the totoal number of this site 3. do you think we need add some other extensions in the homepage, like MCP. what do you think of these?

> AGENT

I have a clear picture. Let me read the key files directly to confirm before drafting the plan.

> AGENT

Findings so far: **Slogan** — `app/components/home/HomeHero.vue:19-23`: the h1 uses `text-4xl sm:text-5xl md:text-[56px]`. Easy to scale down. **Counter bug** — `app/components/home/HomeDiscovery.vue:42-44, 62-68`: the heading reads `total` from the *current tab's query*, which is locked to `category: "skills"` and (on the "Recommended" tab) `filter: "official"`. So the number changes per tab and is never the true site total. It also hardcodes the word "skills" in the i18n string (`home.discoveryHeading` → `"{count} skills, curated for your team."`). **Other extension types** — home shows skills only. The product supports `skills | mcp | slash | plugins` (`shared/types.ts:5`). MCP, slash, and plugins have no presence on the home. Before drafting the plan, two things to settle so the plan is on-target.

> AGENT

I have all the info needed. Drafting the plan file now.

> AGENT

Creating a feature branch per CLAUDE.md, then applying the four edits.

> AGENT

All four edits applied. Let me verify by running typecheck/lint and starting the dev server.

> AGENT

Lint and typecheck both pass. Starting the dev server to verify in browser.

> AGENT

Dev server running on :3001. Let me verify the home renders and the new total fetch works.

> AGENT

138 = 56 (skills) + 68 (mcp) + 7 (slash) + 7 (plugins). The site-wide count is correct. Let me confirm the rendered heading shows 138.

> AGENT

Verified end-to-end: - `/en/`: renders **"138 extensions, curated for your team."** - `/zh/`: renders **"收录 138 个扩展，为你的团队精选。"** - Slogan classes are now `text-3xl sm:text-4xl md:text-5xl` (down one step). - 138 = 56 skills + 68 mcp + 7 slash + 7 plugins — the heading now reflects the true site-wide total. - The hydration payload confirms two independent fetches: `home-discovery-extensions` (per-tab) and `home-discovery-total` (site-wide), so flipping tabs won't move the heading number. Stopping the dev server and committing on the feature branch.

> AGENT

Done. Summary: **Changes (commit `2f7387c` on `refactor/home-refine`):** - `app/components/home/HomeHero.vue` — h1 dropped one Tailwind step: `text-3xl sm:text-4xl md:text-5xl` (was `text-4xl sm:text-5xl md:text-[56px]`). - `app/components/home/HomeDiscovery.vue` — added a second `useFetch` to `/api/internal/extensions` with no `category`, bound the heading `total` to that. Per-tab fetch still drives the grid, so flipping tabs no longer moves the count. - `i18n/locales/{en,zh}.json` — `discoveryHeading` / `discoveryHeadingEmpty` now say "extensions" / "扩展" since the count covers all types. **Verified:** Dev server rendered `>138 extensions, curated for your team.<` (en) and `收录 138 个扩展，为你的团队精选。` (zh). 138 = 56 skills + 68 mcp + 7 slash + 7 plugins. Lint + typecheck clean. **Out of scope (per your "leave home as Skills-only" decision):** no new MCP / slash / plugins sections on the home — those stay reachable via `/extensions?category=…`. Not pushed; let me know when you want me to push and open a PR.
