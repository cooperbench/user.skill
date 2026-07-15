[SYSTEM]: # AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

[DEVELOPER]: Hey! We need bigger feedback loops in the town economy. Yeah. The problem is not that it lacks *complexity*. It lacks **economic tension and circularity**. Right now the economy is basically: `resource node → worker → chest → processor → item/state counter` That is a production pipeline, not yet an economy. The biggest structural weakness is that almost every flow terminates. Wheat becomes flour, flour becomes stew, stew becomes a reserve counter or gets eaten. Ore becomes iron, iron becomes tools, tools mostly stop. Herbs become potions, potions become shop stock, then stop. There is very little feedback from the town back into production. I think the missing shape is: `production → consumption → capability → increased/changed production → scarcity → substitution` For example, a stronger farming loop would be: `farmer → wheat → flour → meals → fed workers → labor capacity` but then: `tools → farming speed` `weather → yield` `worker hunger → productivity` `seed reserve → next harvest` `town population → consumption pressure` Now food isn't merely a number. The town can enter recognizable states: abundance, shortage, famine, recovery. The other major weakness is that your current bottlenecks are mostly **routing failures**: > Goods only produce when […]

[AGENT]: I’ll use the repo’s Entire-backed guidance first, then I’ll trace the existing town economy code before changing anything. The goal is to deepen the current loops without widening content or adding a separate abstraction layer.

[AGENT]: There’s one existing modified file, `src/rules/environment/dungeon/underworldRegions.js`; I’ll leave it alone unless the town economy code depends on it. I’m checking the economy’s current shape and any recorded intent next.

[AGENT]: The current economy already has the right anchor points: `townSimulationSystem` derives broad stock scores from storage inventories, and `aiTownfolkSystem` handles job output, hauling, smithing, cooking, and role capability. I’m narrowing this to the smallest high-leverage change: make food/fuel/tools feed back into labor and production.

[AGENT]: I found this is not a blank slate. Some of your proposed shape is partially present already: food/material/medicine/morale are derived from physical inventories, tavern meals are physically consumed, and smith outputs already bias toward tools. The missing piece is that those derived states do not meaningfully slow or amplify the producer jobs yet, so I’m going to wire that feedback into worker output and pulse timing.

[AGENT]: The producer jobs already require tools for miners and woodcutters, and hauling already creates the lumber-vs-firewood conflict. I’m going to avoid inventing new recipes and instead add two concrete feedback mechanisms: food quality changes labor speed, and service tools increase/degrade output in their own loops.

[AGENT]: The implementation surface I’m targeting is intentionally local: `aiTownfolkSystem` and `TownState`/`townSimulationSystem` tests. I’m not adding a new economy manager; the feedback belongs where the physical inventories and NPC work already converge.

[AGENT]: One timing detail matters: townfolk AI runs in the `ai` phase, town simulation updates in `effects`, so AI reads the prior town assessment. That is fine for a feedback loop; shortages affect the next work decisions instead of same-tick self-correction.

[AGENT]: There is checkpoint coverage for the recent economy work. I’m reading the latest intent so the patch extends that direction instead of fighting it.

[AGENT]: I’m about to edit. The patch will add derived `fuelStores`, `foodQuality`, and `laborReadiness`, make the tavern/town consume fallback foods when prepared meals are unavailable, and use those assessments in townfolk work speed/output.

[AGENT]: The first edit exposed one ordering issue in `townSimulationSystem`: labor readiness should be derived after morale, not via a separate helper. I’m correcting that before moving to the NPC system.

[AGENT]: Now I’m wiring the derived state into townfolk behavior: shortages slow work, prepared food keeps work fast, and role tools turn into capital goods by improving output before eventually wearing out.

[AGENT]: I hit a patch-context mismatch because the import block layout is slightly different than the hunk I prepared. I’m applying the same change in smaller chunks.

[AGENT]: Tool degradation needs to work with both carried and equipped tools, so I’m adding helper functions around the existing inventory/equipment APIs rather than changing item definitions.

[AGENT]: Next is the labor gate. I’m keeping it deterministic and simple: town state creates extra work turns under raw-food or no-food conditions, while the correct capital tool offsets that delay for the role that uses it.

[AGENT]: I’m changing the labor gate to a stateless skip cadence instead of storing per-worker countdowns. That keeps the ECS component shape stable and avoids adding hidden world state.

[AGENT]: I’m adding the actual circularity now: workers who lack their role tool will pull one from smithy stock, and active economy tools will boost output once before becoming worn; worn tools break on a later use. Existing direct tests without a `TownState` keep their old one-shot behavior.

[AGENT]: One nuance: the kitchen knife lives in tavern storage, not on the barkeep. I’m adjusting the helper so storage-held tools can wear too.

[AGENT]: I’m replacing the barkeep’s actor-held knife check with the tavern chest’s knife check so the cooking loop reflects the real inventory location.

[AGENT]: I’m also letting the stored kitchen knife offset shortage delay for cooking, since that is the tool that actually improves the tavern loop.

[AGENT]: The town simulation test expectations need to move with the new behavior: after the tavern cooks, the town can consume fallback flour instead of treating it as a passive counter. I’m updating focused tests to assert the new loop explicitly.

[AGENT]: I’m adding focused AI tests for the feedback behavior without disturbing the legacy tests: no `TownState` means old output; with `TownState`, tools become productive capital and then wear.

[AGENT]: The test additions are intentionally small: one for woodcutter productivity/wear, one for kitchen-knife cooking efficiency/wear.

[AGENT]: I’m adding the cooking-side assertion beside the existing barkeep tests so the contrast between ordinary reuse and active economy feedback is clear.

[AGENT]: The code and tests are in place. I’m running the focused economy and townfolk suites now to catch behavioral or syntax issues before any broader guardrail.

[AGENT]: The first test run found two useful issues. The town feeding fallback was using a stale tavern stock snapshot after cooking, and the new AI tests were being throttled by the active town state before they reached the boosted work path. I’m fixing both directly.

[AGENT]: For town feeding, I’m refreshing stock snapshots after production before consumption. That makes the fallback consume the actual post-cook inventory instead of yesterday’s view of the chest.

[AGENT]: I’m checking the AI branch with a tiny one-off script now. The test result says the base work path runs, so this is specifically about the `TownState` feedback guard or tool-state lookup.

[AGENT]: The static checks say the guard should be active. I’m running a closer reproduction of the woodcutter case to inspect the actual inventory after the system call.

[AGENT]: The one-off reproduction confirms the woodcutter path now produces stacked lumber `count: 2` and marks the hatchet worn. I’m updating the food-substitution test to reflect that wheat is milled before it is eaten, then rerunning.

[AGENT]: I’m rerunning both focused suites after the stock-refresh and test expectation corrections.

[AGENT]: The behavior reproduces correctly in isolation but fails inside the suite, so I’m running just the new filtered cases. That will tell me whether another test is leaving shared state behind or the new tests need stricter setup.

[AGENT]: I need one direct diagnostic inside the filtered tests to see whether the tool is wearing without the bonus or whether the bonus item is landing somewhere unexpected. I’ll add it briefly and remove it after the check.

[AGENT]: The diagnostic shows the simulation is correct: the inventory contains `material_lumber` count `2` and `food_stew` count `2`. The local test helper undercounts stacks because it ignores `count > 1`; I’m fixing the helper expectation path and removing the diagnostic.

[AGENT]: The helper currently counts item entities, not stacked units. Since the economy APIs stack identical goods, I’m updating that helper to match the other town simulation tests and count physical units.

[AGENT]: I’m rerunning the AI suite now that its helper counts stacked units correctly.

[AGENT]: The core focused suites pass. I’m adding one more small regression test for the shortage throttle itself, because otherwise the productivity slowdown would only be covered indirectly by code review.

[AGENT]: The insertion point was a few lines lower than expected. I’m applying the labor-readiness test there.

[AGENT]: I’m rerunning the townfolk suite with the added labor-readiness regression.

[AGENT]: The focused AI suite is green. I’m running the economy suite again and the project’s standard architecture/event check, since this touched shared rules systems and `TownState`.

[AGENT]: Focused tests and `deno task check` are green. I’m doing a final diff/status pass now, with the existing unrelated `underworldRegions.js` change left untouched.

[AGENT]: The final diff is scoped to the town economy systems/tests and passes the focused suites plus `deno task check`. I’m grabbing a few line references for the handoff summary.

[AGENT]: Implemented the first deeper feedback pass for the town economy. Changed: - [TownState.js](/home/pjensen/Repos/JSHack/src/rules/components/TownState.js:5) now tracks derived `fuelStores`, `foodQuality`, `laborReadiness`, and `lowFuel`. - [townSimulationSystem.js](/home/pjensen/Repos/JSHack/src/rules/systems/townSimulationSystem.js:141) now feeds the town from actual inventories by preference: preserves the last prepared meal, then substitutes raw/fallback foods. - [townSimulationSystem.js](/home/pjensen/Repos/JSHack/src/rules/systems/townSimulationSystem.js:201) separates fuel from materials and derives labor readiness from food quality, morale, and fuel shortage. - [aiTownfolkSystem.js](/home/pjensen/Repos/JSHack/src/rules/systems/aiTownfolkSystem.js:176) adds physical tool wear for economy tools. - [aiTownfolkSystem.js](/home/pjensen/Repos/JSHack/src/rules/systems/aiTownfolkSystem.js:920) makes low labor readiness delay scheduled productive work. - Woodcutters/miners can pull missing tools from smithy stock, so smith output now feeds back into production. - Sharp hatchets/pickaxes/kitchen knives boost production once, then become worn; worn tools break on later use. Verification: - `deno test --allow-read tests/townSimulationSystem.test.mjs` - `deno test --allow-read tests/aiTownfolk.test.mjs` - `deno task check` All passed.