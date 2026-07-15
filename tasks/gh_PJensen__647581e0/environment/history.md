> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

I was researching norse stuff this morning over breakfast, this is what I came away with. Let's work on these, broadly. VALKARIE — a new class. The only one that belongs at the same ontological level as fighter, mage, etc. Death-aware, fate-oriented, perhaps gains power from nearby deaths, interacts differently with corpses and Draugr. Ratatoskr — one diminutive squirrel, unique outdoor squirrel. Not hostile. Rare encounter. Moves between distant outdoor regions, perhaps carrying rumors, insults, quest state, or items between otherwise disconnected NPCs. 🐿️ ^^ kind of like chicken, but way way way cooler. Use that unicode character too, Landvættir — invisible or dormant spirits attached to particular places. A grove, standing stone, pond, old tree, ruined foundation. The player discovers that the place itself has state and disposition. ^^ We've already made a spirit guide, as well as spirit essence -- I feel like we could make this happen especially around landmarks. Draugr — not generic undead. A specific dead NPC who refuses to leave something: house, chest, grave, weapon, family property. Territorial rather than wandering. 💀 ^ I think it gets angry when the thing it's gaurding is touched. Hamingja — not a creature at all. An inheritable […]

> AGENT

I’ll treat this as a content/design implementation pass, starting by inspecting the existing class, monster, landmark, corpse, and chicken patterns so the new Norse pieces fit the current data surfaces instead of adding one-off code.

> AGENT

The class registry is plain data, while monsters are registered through content modules at runtime. I found existing tests for chickens, spirit guide, luck, and overworld creatures, so I’m narrowing to those patterns and then I’ll make the content plus focused coverage.

> AGENT

The least invasive shape is: add Valkyrie as a first-class starter class with authored metadata for future death/fate mechanics, add Ratatoskr and Draugr as catalog monsters, and add Landvaettir/Hamingja as explicit content metadata now rather than inventing new runtime state prematurely. I’m going to keep the behavioral hooks declarative where the engine already supports that, then test the contracts.

> AGENT

I’m making scoped data/content edits now: class registry, monster catalog, and a small Norse concept data module for Landvaettir and Hamingja. No scheduler or runtime world state is needed for this first pass, which keeps the future mechanics inspectable without breaking architecture rules.

> AGENT

Valkyrie is now in the class registry with starter gear, holy/death-facing starter spells, and explicit fate metadata. I’m checking that the spear id exists before I leave that equipment choice in place.

> AGENT

There isn’t a plain spear item, so I’m switching Valkyrie to an existing canonical weapon rather than adding a new weapon just to satisfy the class loadout.

> AGENT

Next I’m adding Ratatoskr near the chicken content so it inherits the same neutral/passive catalog expectations, but with unique, rare, messenger-oriented metadata and the requested squirrel glyph. Draugr belongs in undead with territorial guard metadata.

> AGENT

Ratatoskr and Draugr are authored as content definitions now. I’m adding one small data module for Landvaettir and Hamingja so they are first-class concepts without pretending there is already a save-history/lineage runtime.

> AGENT

I’m updating focused tests next: existing class coverage has an exact class count, and I’m adding a Norse content test that locks down the important authored properties rather than brittle full snapshots.

> AGENT

The tests now cover the class and content contracts. I’m running the focused class/content tests first, then I’ll run the relevant content catalog guard if these pass.

> AGENT

Focused tests pass. I’m doing a quick diff review and then a broader content catalog test to catch registration/palette issues from the new monster definitions.

> AGENT

Content catalog and glyph coverage pass too. I’m checking worktree status and scanning the new names so I can catch any misspellings or missing imports before wrapping.

> AGENT

The architecture/event guard passed. One detail I noticed: I normalized the class name to “Valkyrie” instead of the note’s “Valkarie” spelling, while keeping the requested squirrel Unicode glyph exactly in content.

> AGENT

Implemented the Norse content pass. Changed: - Added `valkyrie` class in [classes.js](/home/pjensen/Repos/JSHack/src/rules/data/classes.js) with fate/death-aware metadata. - Added `ratatoskr` in [animals.js](/home/pjensen/Repos/JSHack/src/content/monsters/animals.js) as a unique rare passive outdoor squirrel messenger using `🐿️`. - Added `draugr` in [undead.js](/home/pjensen/Repos/JSHack/src/content/monsters/undead.js) as a rare territorial undead guardian with bound-property anger metadata and `💀`. - Added [norseFate.js](/home/pjensen/Repos/JSHack/src/rules/data/norseFate.js) for Landvaettir site definitions and early Hamingja lineage-luck definition. - Added/updated focused tests in [classes.test.mjs](/home/pjensen/Repos/JSHack/tests/classes.test.mjs) and [norseContent.test.mjs](/home/pjensen/Repos/JSHack/tests/norseContent.test.mjs). Verification run: - `deno test --allow-read tests/classes.test.mjs tests/norseContent.test.mjs tests/chickenCatalog.test.mjs tests/overworldCreatureContent.test.mjs` - `deno test --allow-read tests/contentCatalogCanonical.test.mjs tests/displayGlyphCoverage.test.mjs` - `deno task check` All passed. Note: I normalized “VALKARIE” to the conventional `Valkyrie` for the class name/id.

> DEVELOPER

hey -- this is a decent starting point - but there is quite a bit more that can be fleshed out. drauger is peaceful until it gaurded treasure is messed with. come up with a way for a monster to gaurd treasure, to start assign dragon and drager to that role. why is inheritable luck not a component? why is landvaettir not a component attached to a tile with a radius? right? anyhow -- I have to step away for outdoor time I'd really love it if you could run with the ideas I pitched. overall: make sure we're using the engine for all aspects for what we're doing instead of just slamming frozen objects around.

> AGENT

Agreed. I’ll move this from “catalog notes” into engine-owned state: guarded treasure as ECS state, Draugr/dragon using it, Landvaettir as place/radius component state, and Hamingja as a real lineage-luck component instead of a frozen concept blob.

> AGENT

I found the right integration points: monster spawn params can attach components, pickup emits canonical `item:pickup`, and chest/container pickup has a source container id. I’m going to add components plus a small rules system that wakes/aggros guardians when guarded treasure is taken, then register that in the effects phase.

> AGENT

I’m going to make guarded treasure work as reusable ECS state, not Draugr-specific code: `TreasureGuardian` on the monster, `GuardedTreasure` on the protected chest/item, and a listener/system pair that binds nearby treasure and flips the guardian into hunting only when the protected entity is looted.

> AGENT

I’m also replacing the Norse concept module with component-centered definitions: authored defaults are fine, but the gameplay state needs to live on entities. That means Hamingja can be attached to the player/run lineage entity, and Landvaettir can be attached to a landmark/place entity with an origin radius and disposition.

> AGENT

I didn’t find the exact helper by name on the first pass, so I’m using the already-resolved monster definition path in `spawnMonsterEntity`; that is the canonical point shared by dungeon/debug/runtime spawns.

> AGENT

The spawn parameter conversion currently drops custom monster metadata, so I’ll carry only a small explicit `guardianRole` field through it instead of exposing arbitrary content metadata to spawn code. That keeps the engine surface deliberate.

> AGENT

The core state components are in place. Next I’m exporting them, replacing the old frozen Norse-state shape with component helpers, and adding the guardian binding/aggro system.

> AGENT

I’m adding the guarded treasure system now. It will auto-bind unassigned guardians to nearby treasure/chests, then react to pickup events from either a protected item or a protected container.

> AGENT

Now I’m wiring the system into spawn and scheduling, and marking dragon/Draugr as authored treasure guardians. Draugr will be neutral/passive until its guarded treasure is disturbed.

> AGENT

I noticed a stray no-op variable in the spawn patch while reviewing; I’m cleaning that up before testing.

> AGENT

The content DSL now preserves `guardianRole`, so dragon and Draugr can actually spawn with `TreasureGuardian`. I’m updating the tests to exercise runtime ECS behavior: binding, pickup disturbance, aggro transition, and the new Landvaettir/Hamingja components.

> AGENT

One architecture rule applies here: `treasure:disturbed` is a new event, so I’m changing that to a concrete `EcsEvent` class instead of a new string event.

> AGENT

With the typed event in place, I’m running the focused Norse/guardian tests and class tests now. If anything shakes loose, I’ll fix it against the engine path rather than weakening the tests.

> AGENT

Focused tests pass. I’m checking the stat pipeline next because a Hamingja component should feed luck somewhere meaningful, not just exist. If there’s an established passive bonus path, I’ll hook it there.

> AGENT

Hamingja can feed the existing passive bonus pipeline cleanly as `luckDerived`. I’m making that connection so combat/traps/disarm logic sees inherited luck through the same canonical stat path as equipment luck.

> AGENT

Hamingja now contributes through `getPassiveBonuses`, so inherited luck participates in the existing luck consumers. I’m rerunning focused tests plus the luck/passive coverage that could be affected.

> AGENT

The focused stat and guardian tests pass. I’m running the project guard now, including event doctrine, since this added a system, components, and a typed event.

> AGENT

The architecture and event guards pass. I’m doing one more focused content registration pass and a final diff/status review so the summary is accurate.

> AGENT

The final content tests pass. I’m reading the actual changed hunks now for accidental oddities, especially around the generic passive bonus change and the new guardian system.

> AGENT

The review found one over-defensive `try/catch` around component attachment. I’m removing it so invalid guardian component data fails loudly during spawn, consistent with the architecture rules.

> AGENT

That cleanup is done. I’m rerunning the narrow guardian test and then checking the final full file list.

> AGENT

Implemented the deeper engine pass. What changed: - Added ECS components: `TreasureGuardian`, `GuardedTreasure`, `Landvaettir`, `Hamingja`. - Added `treasureGuardianSystem` plus listener extension: - Guardians auto-bind to nearby treasure/chests. - Looting guarded treasure marks it disturbed. - Guardian wakes, becomes enemy, and hunts the looter. - Added typed `TreasureDisturbed` event. - Draugr is now neutral/passive and only turns hostile when its guarded property is disturbed. - Dragon and Draugr are authored with `guardianRole`. - Landvaettir now attaches to place entities with origin/radius/disposition. - Hamingja now attaches as lineage luck state and feeds `luckDerived` through the existing passive bonus/stat path. - Kept Ratatoskr as unique/passive outdoor messenger content with `🐿️`. Verification passed: - `deno test --allow-read tests/norseContent.test.mjs tests/classes.test.mjs` - `deno test --allow-read tests/norseContent.test.mjs tests/luck.test.mjs tests/statPipeline.test.mjs tests/passiveBonusesArchitectureGuards.test.mjs` - `deno test --allow-read tests/contentCatalogCanonical.test.mjs tests/chickenCatalog.test.mjs tests/overworldCreatureContent.test.mjs tests/displayGlyphCoverage.test.mjs` - `deno task check` This is now using engine surfaces instead of just frozen concept objects.

> DEVELOPER

why does the new class not show up in character creation screen?! NOTE: in the future adding a new class should be completely transparent.

> AGENT

I’ll trace character creation’s class list path now. Since the class exists in `CLASS_DEFS`, the missing screen entry is likely a separate display/order filter, and I’ll wire it so future classes flow from the registry automatically.

> AGENT

The main boot path already uses `listClassIds()`, but the character creation UI chooses a random starting class and likely only shows one card at a time. I’ll still add a regression around the boot mapping/order so future classes are transparent and not hand-maintained in `main.js`.

> AGENT

The UI has a hard-coded `CLASS_ICONS` map in the display layer, and the boot mapping is inline in `main.js`. That is exactly the kind of separate presentation list that makes new classes feel non-transparent, so I’m moving class display construction into one helper and letting class data carry its own optional icon.

> AGENT

The class picker now gets icon/presentation from class data instead of a UI hard-code, and there’s a regression test that character creation display data equals the registered class list. I’m cleaning up any now-unused imports and running the focused tests.

> AGENT

Focused tests pass, and `main.js` now has stale imports from the old inline display mapper. I’m removing those and then I’ll run the architecture guard.

> AGENT

I’m running `deno task check` again because moving a helper into `main/` changes cross-layer imports and the guard should validate it.

> AGENT

The guard passes. I’m taking a final status/diff snapshot so I can give you the exact fix and the “future class” guarantee.

> AGENT

Fixed. The character creation screen had separate presentation wiring: class icons were hard-coded in `src/display/ui/charCreation.js`, and display data was built inline in `src/main.js`. Now: - `src/main/classDisplayData.js` builds character creation data directly from `listClassIds()`. - `tests/classDisplayData.test.mjs` asserts every registered class appears in character creation data. - Class icons live on `CLASS_DEFS`, including Valkyrie `🪽`. - `charCreation.js` no longer has a hard-coded class icon list. Verification: - `deno test --allow-read tests/classDisplayData.test.mjs tests/classes.test.mjs tests/norseContent.test.mjs` - `deno task check` Both passed. Future class additions now flow into character creation automatically as long as they are added to `CLASS_DEFS`.

> DEVELOPER

1. valkarie is missing glyph 2. new milling feat: mill + corn -> cornmeal 3. general store sign (glyph) is missing -- attempted add 4. move smithy sign right 1, up 2 -- in building JS

> AGENT

I’ll handle these as four scoped content/map fixes: class glyph/presentation, milling recipe, general store sign spawn/glyph, and smithy building spawn coordinate adjustment. I’m reading the relevant building and milling/content files first.

> AGENT

I found existing mill tests and a general store sign spawn already present, but likely palette/materialization lacks the sign kind. I’m reading the interactable payload and spawn-kind/palette tables now so the fixes go through canonical surfaces.

> AGENT

The general store sign exists as an archetype and spawn kind, but its palette glyph is an empty string, so it materializes but renders blank. The mill path is currently hard-coded wheat-to-flour in interaction and townfolk systems; I’m making that a small reusable milling recipe table so corn-to-cornmeal is data-driven.

> AGENT

The mill interaction and townfolk mill both duplicate wheat logic. I’m adding `millingRecipes.js` under rules data, then using it in both paths so adding another milling conversion is one data entry.

> AGENT

I’m making the four edits now: `valkyrie.glyph`, `food_cornmeal`, data-driven milling recipes used by player/town/townfolk milling, visible general store sign palette, and smithy sign coordinates from `(-5, 1)` to `(-4, -1)`.

> AGENT

The data and map edits are in. I’m wiring the new milling recipe table into interaction, town simulation, and townfolk work so player milling and NPC milling both understand corn.

> AGENT

The multi-file patch hit a context mismatch in the message wiring, so I’m applying the milling changes in smaller patches after checking which files were already updated.

> AGENT

No milling code was changed by the failed patch, so I’m applying the recipe-table wiring cleanly now.

> AGENT

The milling paths now share recipe data. I’m adding regression tests for Valkyrie glyph, cornmeal milling, general store sign glyph, and smithy sign placement.

> AGENT

The tests are in. I’m running the focused suites now; if the new cornmeal item isn’t being installed into the catalog/palette, this should catch it.

> AGENT

Focused tests passed. I’m running content/catalog and architecture guardrails now because this touched content DSL item registration, display palette, rules data, and map stamps.

> AGENT

A test caught that the current working class glyph is `@`, not `V`; I’m aligning the assertion to the intended player-class glyph and checking the class data.

> AGENT

I’m picking up from the current diff and closing the glyph mismatch first, then I’ll rerun the focused coverage around classes, milling, palette entries, and building placement.

> AGENT

The remaining failure is specific: the class display path now exposes glyphs, but Valkyrie’s authored class glyph is `V` while the test and player-class convention expect `@`. I’m changing the authored data so future class screens can derive this transparently from `CLASS_DEFS`.

> AGENT

The file is already at `@` now, so I’m treating that as resolved and moving to verification across the touched behaviors.

> AGENT

Focused behavior tests are green now. I’m running the project’s architecture/event check next because this touched content paths, interaction payloads, and display projection.

> AGENT

The architecture/event guardrails pass. I’m doing one final diff pass to catch accidental scope creep before I summarize exactly what changed.

> AGENT

One caveat in status: there is an untracked `assets/audio/action_millstone_grind.mp3` already present. I didn’t create or modify it, and I’m leaving it alone.

> AGENT

Implemented the four fixes. Changed: - Valkyrie now has an authored `glyph: '@'`, and character creation display data derives glyphs from class definitions. - Added generic milling recipes in [millingRecipes.js](/home/pjensen/Repos/JSHack/src/rules/data/millingRecipes.js), with `corn -> cornmeal` alongside `wheat -> flour`. - Added `food_cornmeal` content and palette entry, plus cornmeal player messaging. - Added the missing `general_store_sign` glyph. - Moved the smithy sign from `dx: -4, dy: 1` to `dx: -4, dy: -1` in [smithy.js](/home/pjensen/Repos/JSHack/src/rules/data/buildings/smithy.js). Verification: - `deno test --allow-read tests/classDisplayData.test.mjs tests/interaction.test.mjs tests/displayGlyphCoverage.test.mjs tests/overworldStructures.test.mjs tests/aiTownfolk.test.mjs tests/townSimulationSystem.test.mjs tests/contentCatalogCanonical.test.mjs tests/dataIntegrity.test.mjs tests/paletteMonsterEntries.test.mjs` - `deno task check` Both passed. Note: `assets/audio/action_millstone_grind.mp3` is untracked and was already present; I left it untouched.