[SYSTEM]: # AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

[DEVELOPER]: some play testing notes: 1. far too many creatures are doing battle before I ever arrive. creature infighing across species needs to be cut down, maybe behind a flag 2. traversing up and down between overworld and dungeon subsequently lets me walk of of the door of any shop with an armful of goods. 3. shopkeepers should all have little cottages instead of sleeping in their shops. that way they have more interesting behavior as well as opening up stealing from shops at night. do you're very best!

[AGENT]: I’ll trace the shop transition/shop ownership path first, then look at faction aggression and shopkeeper placement. The notes touch simulation behavior and content generation, so I’m going to keep changes focused and verify with targeted Deno tests/guardrails.

[AGENT]: The broad search confirms there is already a shopkeeper enforcement system and tests for blocking witnessed theft, plus faction hostility utilities. I’m narrowing to those implementation files and the world transition/materialization code so the fix lands where the current architecture expects it.

[AGENT]: I found a likely source for the first note: `enemy` is explicitly hostile to `enemy`, which makes all enemy factions fight each other by default. I’ll change that to an opt-in conflict path rather than global hostility, then update the Ring of Conflict expectation that currently documents the old default.

[AGENT]: The theft issue appears tied to restored overworld shop IDs: transition remaps `RoomMetadata.shopkeeperId`, but unpaid goods and shop keys may still point at the old shopkeeper after a cached floor restore. I’m checking the remap path and the tests that already cover shop restoration before editing.

[AGENT]: There is already a regression test asserting restored unpaid ownership links, and the transition code now remaps `Unpaid.shopkeeperId`. I’m going to add a stronger route-change test for the “walk out after round trip” case and check whether the system is missing the room boundary when the player stands on a door tile.

[AGENT]: The existing restored-shop test is close to the bug but stops at `shopkeeperSystem` directly; it does not simulate the scheduled movement after returning from the dungeon. I’m going to reproduce that path under the scheduler and fix the boundary/enforcement logic if it fails.

[AGENT]: For the cottage note, town placement already gives ordinary villagers cottages but shop definitions embed a `home_bed` inside each shop. I’m going to move vendor home coordinates to nearby cottage bedrooms without changing the shop stock layout wholesale, and remove the shop-bed spawns so their nightly schedule no longer sleeps in the store.

[AGENT]: The Ring of Conflict AI path already has its own opt-in targeting, so removing enemy self-hostility should not break that feature. I’m editing the hostility table/tests, the shop exit fallback, and vendor home placement together, then I’ll run the focused suites.

[AGENT]: The theft root cause is clearer now: an unpaid item already in the player’s inventory is treated as permanent during transition, so it is not part of the restored entity set and its `shopkeeperId` misses the old-to-new vendor remap. That exactly matches “go down/up, then walk out with goods,” so I’m fixing remap scope for `Unpaid` references.

[AGENT]: For shopkeepers, I’m adding separate generated cottage homes near their shop buildings and routing their `TownfolkJob` home/bed targets there while keeping their work target at the shop. This uses the existing cottage stamp and schedule system instead of adding a bespoke AI path.

[AGENT]: I found the apothecary also still had an embedded bed, so I’m removing that one too. After that the shopkeeper homes should come only from the new cottages.

[AGENT]: I’m adding regression coverage for the exact stolen-inventory transition case now: pick up stock, leave overworld, restore overworld, then try to move out through the shop door under a scheduled tick. That should fail before the remap-scope fix.

[AGENT]: Edits are in place. I’m running the narrow suites for faction conflict, shop restoration/doors, shopkeeper enforcement, and transition inventory now; if those pass I’ll run the architecture/event guard task in proportion to the touched areas.

[AGENT]: The focused tests pass, including the new held-stock round-trip regression and the cottage-home assertion. I’m running the project guard task now to catch architecture/event doctrine regressions from the touched rules files.

[AGENT]: Guardrails passed. I’m doing a final diff/status pass to make sure the changes are limited to the intended systems, data, and tests.

[AGENT]: The diff is scoped as intended. I noticed one metadata assignment in the cottage helper is not used anywhere, so I’m removing it to avoid inert code.

[AGENT]: I made that small cleanup. I’m rerunning the affected generated-town/shop test file once more after the cleanup.

[AGENT]: Implemented the playtest fixes. Changed: - Cut down ambient creature infighting by making `enemy` no longer hostile to `enemy` by default. Ring of Conflict still redirects enemies into rival targeting through its explicit AI path. - Fixed the shop theft transition bug: unpaid items already carried by the player now remap their `shopkeeperId` when the overworld shopkeeper is restored after dungeon travel. - Moved overworld shopkeepers out of shop beds: generated shop buildings no longer include `home_bed`, and shopkeeper roles now get nearby cottage homes while still working in their shops. - Added regression coverage for the stolen-stock dungeon round trip and shopkeeper cottage homes. Verified: - `deno test --allow-read tests/ringOfConflict.test.mjs` - `deno test --allow-read tests/shopDoorKeys.test.mjs` - `deno test --allow-read tests/shopkeeperSystem.test.mjs tests/transitionInventory.test.mjs` - `deno task check`

[DEVELOPER]: 1. farmer is sleeping in the open in his field 2. miner was spotted wide awake in the middle of the night, does he have a home? 3. anyone else effectively homeless? we should house them.

[AGENT]: I’ll trace how non-shop townfolk get home/bed targets and which building plans lack actual residential interiors. This sounds like the same town placement surface as the shopkeeper cottage work, so I’m checking that path before editing.

[AGENT]: Using `using-entire` for the town placement exploration; I’ll check whether there’s recorded history for this area, then use the current code to make the housing fix.

[AGENT]: The current placement rules explain the sightings: farmer’s `farm` building has no bed/home waypoint, so the fallback uses the field work waypoint as home. Miner uses a cottage-shaped mine camp, so he should have a bed, but I’ll add a generated-town audit to catch all roles whose home/bed is not in a roofed residential tile.

[AGENT]: Recorded checkpoint context for the previous change just confirms the touched files/session; the rest here is inferred from current code. The audit points to farmer and enchantress as definitely homeless after removing apothecary beds; miner/fisher/woodcutter use cottage-shaped work camps, but I’ll put a test around every generated town role so this does not regress quietly.

[AGENT]: I’m going to generalize the previous shopkeeper-cottage helper into “dedicated cottage homes” for roles whose workplace is not a residence. That covers farmer and enchantress, keeps shopkeepers housed, and leaves miner/fisher/woodcutter on their existing cottage camp homes.

[AGENT]: The code now gives farmer and enchantress dedicated cottages, and I expanded the generated-town test to audit every scheduled role’s bed as a roofed interior floor tile. I’m running that test to see if any other role fails the housing standard.

[AGENT]: The full town housing audit passes, including miner, farmer, and the roles that were previously easy to miss. I’m also rerunning the shop-door suite because this touched the same home-cottage placement used by shopkeepers.

[AGENT]: Focused behavior tests pass. I’ll run the standard architecture/event guard task now, since the change is in generation and scheduling data.

[AGENT]: Guardrails pass. I’m doing a final status/diff check so I can summarize exactly what changed.

[AGENT]: Implemented. The farmer was genuinely homeless: farm only had a work waypoint, so sleep fell back into the field. I generalized the cottage-home placement so `farmer` now gets a real nearby cottage. I also added `enchantress`, since after moving shop beds out of shops she otherwise fell through to non-residential apothecary coordinates. Shopkeepers keep their cottages through the same path. I added a generated-town housing audit covering every scheduled role: alchemist, barkeep, book vendor, enchantress, farmer, fisher, gem vendor, general vendor, herbalist, miner, priest, smith, villager, woodcutter. It verifies their bed is finite, not their work counter, on an interior floor tile, and under a roof. Miner passes that audit, so he has a cottage bed; if he was awake at night, that is likely scheduling/pathing/interruption rather than homelessness. Verified: - `deno test --allow-read tests/overworldStructures.test.mjs` - `deno test --allow-read tests/shopDoorKeys.test.mjs` - `deno test --allow-read tests/aiTownfolk.test.mjs` - `deno task check`