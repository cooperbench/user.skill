[DEVELOPER]: what's next features do you recommend?

[AGENT]: I'll survey the current state of the game — what's already implemented, what's deferred, and what's on the roadmap — so I can recommend next features grounded in the actual codebase.

[AGENT]: Both exploration agents are running — one inventorying existing gameplay systems from the docs and changelog, the other checking open issues, PRs, and recent work themes. I'll synthesize recommendations once they report back.

[TOOL]: <task-notification> <task-id>ac9079bf7d834303a</task-id> <tool-use-id>toolu_01N2ATDY6TtX9Fdkqo7XJMs2</tool-use-id> <output-file>/private/tmp/claude-501/-Users-hutusi-workspace-ai-david-monecraft/0bbf36a0-b366-42d5-b782-1e8fcd71b3a9/tasks/ac9079bf7d834303a.output</output-file> <status>completed</status> <summary>Agent "Inventory current game features" finished</summary> <note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note> <result>I have a comprehensive picture. No dedicated ROADMAP/TODO/ideas file exists (the roadmap-keyword grep only hit incidental mentions in CHANGELOG/architecture/save-format; `docs/adding-content.md` is a contributor how-to-extend guide, not a roadmap). Here is the inventory. # Monecraft — Existing Feature Inventory ## 1. Version &amp; save format - **Latest released version: 0.11.0** (2026-06-28). The `[Unreleased]` section on top is substantial and effectively the current state of the code. - **Save schema version: v16** (bumped v15→v16 in Unreleased for the `vehicles` field). Migration chain runs v1→…→v16. - **Worldgen version: `WORLDGEN_VERSION` 9** (bumped 8→9 in Unreleased for generated villages). - Client-only, localStorage; two-level save hierarchy (profiles → worlds, each world its own save blob). Zero binary assets except one bundled Monocraft font (documented exception). ## 2. Major gameplay systems present (each one line) - **Crafting**: 74 recipes, always-available grid, recipe book grouped by category (Tools/Vehicles/Weapons/Armor/Building/Food/Materials) with have/need + "how to obtain" hints. - **Smelting**: Furnace station; coal/charcoal fuel economy; […]

[AGENT]: The feature inventory is in — the game is remarkably complete for a browser voxel game (v0.11.0, save v16 pending release): full survival loop, enchanting, potions, villages/raids, a boss endgame, and water vehicles just landed. Notable gaps: no alternate dimensions, no redstone/automation, no buckets/fluid placement, no partial blocks (slabs/stairs/fences), no maps/waypoints, thin ocean content, and no minecarts. Still waiting on the second agent checking open issues and PRs — I'll pull together recommendations when it reports.

[TOOL]: <task-notification> <task-id>ae21795b4ae54b254</task-id> <tool-use-id>REDACTED</tool-use-id> <output-file>/private/tmp/claude-501/-Users-hutusi-workspace-ai-david-monecraft/0bbf36a0-b366-42d5-b782-1e8fcd71b3a9/tasks/ae21795b4ae54b254.output</output-file> <status>completed</status> <summary>Agent "Check issues, PRs, recent history" finished</summary> <note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note> <result>I have a complete picture. Here's my report. ## Feature work: planned, requested, and in-flight ### How this project tracks work There is **no active issue tracker**. The fork `hutusi/monecraft` has GitHub Issues **disabled**, and upstream `davidhu0527/monecraft` has **zero** open/closed issues and **zero** open/closed PRs (only the default GitHub label set exists there, unused). All work flows through **feature branches → PRs on the fork → `CHANGELOG.md`**. So "what's planned/in flight" lives in the CHANGELOG `[Unreleased]` section and git history, not a backlog. ### Open PRs / Open Issues - Fork `hutusi/monecraft`: **0 open PRs**, issues disabled. - Upstream `davidhu0527/monecraft`: **0 open issues, 0 open PRs.** Nothing is currently in flight as an open PR — the last one (`#41`) merged 2026-07-02. ### Recent work themes (from `git log` and merged PRs) The last ~6 weeks show a steady march of Minecraft-style systems, each shipped as its own `feat/*` branch with a matching […]

[AGENT]: Both scouts are back. Here's the picture: there's no backlog anywhere — issues are disabled on the fork, upstream is empty, and every "future" hint in the docs has already been built except grass spread. The unreleased section already holds a big 0.12.0 (advancements, companions, villages/raids, water vehicles). So "what's next" is genuinely an open design decision, and here's what I'd recommend, ranked: **1. Aquatic/exploration update (my pick).** Water vehicles just landed, but the ocean they sail on is empty — no fish mobs, no underwater flora, nothing to sail *to*. An update with fish, kelp/coral, shipwreck and ocean-ruin structures with loot chests, and buried treasure with a treasure-map item would give ships a purpose and directly reuse what just shipped: the dungeon loot-chest system, the fishing treasure table, and the structure-generation seam from villages. Mostly content over existing seams, so low architectural risk for high visible payoff. **2. Deferred-mechanics batch (quick win).** From earlier releases there's a known deferred list: Fire Aspect and Thorns enchantments, Night Vision and Invisibility potions, splash potions — plus shields, golden apples, and grass spread (the one extension point in the code that's scaffolded but unbuilt). Small, low-risk, rounds out combat and brewing. **3. […]

[AGENT]: The Plan agent is designing the aquatic-update implementation — reading the extension seams, mob/worldgen code, and save-format rules before proposing commit slices. I'll review its output, then write up the final plan.

[TOOL]: <task-notification> <task-id>aa9dee203351e08e7</task-id> <tool-use-id>toolu_01BFgQXLpwNmxMoGXLfC3xtC</tool-use-id> <output-file>/private/tmp/claude-501/-Users-hutusi-workspace-ai-david-monecraft/0bbf36a0-b366-42d5-b782-1e8fcd71b3a9/tasks/aa9dee203351e08e7.output</output-file> <status>completed</status> <summary>Agent "Design aquatic update plan" finished</summary> <note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note> <result>I have a complete picture now. Here is the implementation plan, grounded in the actual code. # Aquatic Update — Implementation Plan ## Scope decision **In:** (1) two fish mobs (cod + salmon — the second variant is pure data rows), (2) kelp with random-tick growth + dried-kelp food, plus 2 decorative coral blocks (cheap to ride the same worldgen bump), (3) sunken shipwrecks with lazily-filled loot chests, (4) buried beach treasure + a `treasure_map` item rendered as a compass-style HUD pointer (reusing the boss-tracking pattern) with an X on the minimap. **Explicitly deferred:** the drowned-like hostile. It is *not* cheap after fish AI: fish AI is wander/flee only, while a hostile needs 3D water pursuit, a water-aware hostile spawn director, LOS/attack under water, and daylight-burn exceptions. Defer to a follow-up. Also deferred: full cartographic map rendering (compass + minimap X is the right scope), fish breeding/buckets. ## Verified facts the plan relies on […]

[AGENT]: The plan came back thorough and grounded — but I spotted one discrepancy between the two agents (where `WORLDGEN_VERSION` lives), so let me spot-check a few load-bearing claims before writing the final plan.

[AGENT]: All claims verified — `lib/game/bossTracking.ts` exists with tests and is wired into GameEngine. Writing the final plan.

[AGENT]: Plan approved. Starting implementation — first the branch, then Slice 1 (kelp + coral). Let me set up task tracking and create the feature branch.

[AGENT]: Now the lighting, audio materials, random ticks, and mining files:

[AGENT]: Now the contributor checklist so I don't miss a seam:

[AGENT]: The checklist is clear. Let me look at the sprite grid pattern for the `dried_kelp` icon:

[AGENT]: All patterns are clear. Now let me check the worldgen test and re-baseline policy before writing code:

[AGENT]: All context gathered. One quick check on how `WORLDGEN_VERSION` interacts with saves, then I'll write the code:

[AGENT]: Everything's verified. Now writing Slice 1 — starting with the block definitions:

[AGENT]: Now the atlas paint branches, lighting class, and sound rows:

[AGENT]: Now the config bump and the kelp growth tunable:

[AGENT]: Now the item plumbing — hardness, item defs, drops:

[AGENT]: The recipe is in. Now the dried-kelp sprite — a folded dried-kelp sheet:

[AGENT]: Now the kelp-stalk cascade on break in mining.ts:

[AGENT]: Only two hash failures so far — let me see the complete failure list including world types and meshing:

[AGENT]: Now the growth and cascade tests — let me check the existing test harness patterns:

[AGENT]: All 964 tests pass. Now lint, format, and build to complete the slice gate:

[AGENT]: Gate is green. Committing Slice 1:

[AGENT]: Now the mob model builder to see how to add a fish variant:

[AGENT]: The gait guard handles zero legs. Writing the fish implementation — types, model, templates first:

[AGENT]: One check — how mobVisuals positions the model group relative to `mob.position`, so the fish body renders at its swim height:

[AGENT]: `mob.position` is the body center, and the fish model is centered on the group origin — that works. Now the templates:

[AGENT]: Now the config tunables and the aquatic AI branch:

[AGENT]: Now the four remaining exhaustive tables — loot, XP, call intervals, and sounds:

[AGENT]: All seven tables are filled. Typecheck to catch anything missed:

[AGENT]: Typecheck green. Now the tests — let me check the spawnDirector test harness first:

[AGENT]: Now the fish tests — AI behavior in mobAI.test.ts, spawning in spawnDirector.test.ts:

[AGENT]: Adding the missing imports to spawnDirector.test.ts:

[AGENT]: Prettier reformatted those files — fine. The boot test still fails; let me see the actual count:

[AGENT]: The snapshot's `passiveCount` also includes the 10 fish now:

[AGENT]: Now the shipwreck build/derive pair, mirroring the dungeon pattern:

[AGENT]: Check the barrel export, then wire the engine:

[AGENT]: Now the loot side — generalize the tiered roll and add the shipwreck table:

[AGENT]: Now the treasure map item + sprite, and the generalized chest fill:

[AGENT]: Renames applied. Now wire shipwreck sites into the engine state:

[AGENT]: Tests next. Let me look at the dungeonLoot test to mirror, and the exploit-guard test:

[AGENT]: Wrecks now generate and the probe passes. Re-baselining the one changed digest:

[AGENT]: Adding a shipwreck-family test to the same describe:

[AGENT]: Now let me see the snapshot type, minimap, and how BossHealthBar is mounted:

[AGENT]: The minimap reads full GameState — easy to add an X overlay. Now the advancements registry and the shell component:

[AGENT]: All pieces identified. Writing the buried-treasure worldgen (appending after shipwrecks):

[AGENT]: Now the buried-treasure loot table and the third fill family with the unearthed event:

[AGENT]: Now thread `emit` through the two call sites:

[AGENT]: Now the state fields, snapshot field, and event:

[AGENT]: Now the advancement, stat, and fishing-table entries:

[AGENT]: No weight-pinned fishing tests. Now the compass HUD component — checking the boss-bar CSS to reuse the pointer styling:

[AGENT]: Now the tests — loot table, hint, worldgen probe, and the compass flow:

[AGENT]: Now the worldgen probe for buried treasure:

[AGENT]: The all-chests probe needs buried sites in its union too:

[AGENT]: Buried treasure lands in most worlds (beach bands exist even without ocean biome). Collecting all new digests:

[AGENT]: Six digests to re-baseline. Updating the count first, then extracting the new meshing hash:

[AGENT]: Gate green. Committing Slice 4:

[AGENT]: Slice 5 — docs. Let me survey the relevant sections:

[AGENT]: Now let me read the remaining reference tables I need to extend:

[AGENT]: Now applying all the reference.md updates in one pass:

[AGENT]: Docs are in. Running the full gate including e2e (renderer was touched):

[AGENT]: All five slices are committed. Let me update the roadmap memory to reflect this work:

[AGENT]: Done — the aquatic update is fully built. Here's the summary: ## What I recommended and built You asked for next-feature recommendations. My top pick was an **aquatic update** (the ocean your new rafts and ships sail was empty — nothing to see, nothing to sail to), with runner-ups being a deferred-mechanics batch, a Nether-style dimension, and redstone-lite. The plan question timed out, so I proceeded with the recommended option after you approved the plan. It's complete on the local branch `feat/aquatic-update` — **5 commits, not pushed** (per your review-first workflow): 1. **Kelp & coral** — swaying kelp stalks and pink/blue reef coral on the sandy ocean floor. Kelp keeps a 3-block clear-water band so boats never snag, regrows via random ticks, harvests as a full stalk (refilling with water, never air pockets), and smelts 3-at-a-time into dried kelp. 2. **Cod & salmon** — the first water-dwelling mobs, with a dedicated 3D swim/flee AI branch that can never leave water, a legless fish model variant, and an aquatic spawn director so oceans you sail to are stocked (zero fish on Superflat — the sampler fails closed). 3. **Shipwrecks** — flooded plank hulls sunk on the deep ocean floor with 1–2 […]

[DEVELOPER]: push and open pr

[AGENT]: Pushed and opened — updating the memory to reflect it:

[AGENT]: Done. The branch is pushed and the PR is open: **https://github.com/hutusi/monecraft/pull/42** — `feat/aquatic-update` → `main`, 5 commits. The PR description covers the four feature slices plus docs, flags the **`WORLDGEN_VERSION` 9→10** bump (existing worlds reboot from their seed) and that the **save schema stays v16** with no migration, lists the deferred follow-ups (drowned-like hostile, map rendering, fish buckets), and notes the test coverage (984 unit + 18 e2e, green at every commit). No attribution lines, per your convention. CI and CodeRabbit will run on it now. One reminder before merging: the **manual gameplay pass on an ocean seed** hasn't been done yet — worth a quick `bun run dev` to eyeball the kelp/coral/fish visuals, dive a wreck, and follow a treasure map end-to-end, since none of that is headless-verifiable.