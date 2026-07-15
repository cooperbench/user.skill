> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

I added two new sounds: action_wood_chop.mp3 > for use on a singular wood chop action, for use at the moment of chopping. and ambient_woodcutter.mp3 > for use positioned directly on the woodcutter job while the work is active and the observer is within earshot NOTE: singular chops may still be played by the woodcutter at the moment of various chops -- or -- we can use only the singular "action_wood_chop.mp3" so long as we varry the pitch and it takes more than one chop to fell a tree.

> AGENT

I’ll trace the existing audio asset registration and woodcutter/job chop flow first, then wire the new sounds into the closest existing content or event surface rather than adding one-off display logic.

> AGENT

I found both files already under `assets/audio`. The next step is to inspect the sound registry, positional ambient controller, and the townfolk woodcutter branch so the sound IDs and loop behavior fit the existing audio contracts.

> AGENT

The project already has two useful paths: one-shot `audio:play` events for positional sounds, and `WorldView.audioEmitters` for continuous local loops. I’m going to use those: woodcutter chops emit an `audio:play` at the worker, and active woodcutter work will project a `woodcutter` emitter into the local ambient loop controller.

> AGENT

I’m about to edit four focused areas: register the two sound IDs, make the local ambient controller understand `woodcutter`, emit the one-shot chop from townfolk work completion, and project a `woodcutter` emitter only while a woodcutter is actively working a chop site. Tests will cover each contract.