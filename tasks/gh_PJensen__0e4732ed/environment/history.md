> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

1. enchanter / enchantress needs glyph 2. enchanter / enchantress nees clear shop hours. 3. enchanting shop needs plenty of floor stock -- I think pre-made enchanting scrolls and/or enchanting ingredients are a good starting point.

> AGENT

I’ll use the repo’s content-authoring guidance here, starting with the local Entire/codebase instructions so I can change the existing shop and content paths instead of inventing new wiring.

> AGENT

I’m checking the current shop/content definitions and the existing “enchant” references now. That should tell me whether this is a catalog-only change, a shop stocking rule change, or both.

> AGENT

The current tests show an explicit old constraint that alchemy/general loot should not carry finished enchant scrolls. I’m going to keep that distinction and make the dedicated enchanting shop carry them, along with reagent floor stock and a clearer NPC schedule.

> AGENT

The enchanter shop building currently has only the bench, runestone, crate, pillar, and sign as authored spawns. There is already a generic shop stock generator pattern for apothecary, gem, and book shops, so I’m extending that same surface for enchanting stock.

> TOOL

<turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>

> DEVELOPER

stopping you -- this should be easy. 1. assign glyph to enchanter 2. ensure enchanter has a cottage complete those then we'll talk floor stock.

> AGENT

Understood. I’m narrowing this to two changes only: display glyph for the enchanter/enchantress identity and placement coverage so the role gets a cottage/home.

> AGENT

The home plumbing already has a shopkeeper-home pass, but the role allowlist looks like the likely gap. I’m going to add the enchantress palette entry and include the role in that cottage-home allocation, then verify with the focused structure/glyph tests.

> TOOL

<turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>