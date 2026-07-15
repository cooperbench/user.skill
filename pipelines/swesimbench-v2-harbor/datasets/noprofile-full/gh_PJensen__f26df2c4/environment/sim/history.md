[SYSTEM]: # AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

[DEVELOPER]: 1. milling grain sound does not work 2. milling corn -> food_cornmeal does not work -- it should just happen when interacting with the mill 3. valkarie glyph is still not set -- this is obnoxious that I have to do this this late in the game!

[AGENT]: I’ll trace the mill interaction, audio event path, and the Valkyrie content definition before editing. Then I’ll make the smallest fixes and run focused checks around the touched behavior.

[AGENT]: The existing tests already describe the intended mill behavior, including corn to cornmeal and the grind sound. I’m narrowing this to the implementation path now, because the likely break is either catalog identity mismatch, interactable wiring, or audio payload shape.

[AGENT]: The mill recipe data exists and the registry has `action:millstone_grind`, so this looks like runtime glue rather than missing content. I’m checking the actual interaction implementation and class data next.

[AGENT]: The implementation consumes the first millable item directly from the actor inventory and emits `audio:play` with the registered key. Since that path looks correct in isolation, I’m going to run the focused tests before changing it so we can see whether the break is untested UI/catalog behavior or a regression the current test already catches.

[AGENT]: The existing focused tests pass, so they aren’t exercising the failing live path. I’m checking the item creation helper and the authored millstone definition now; if the live interaction is different from the synthetic test, that’s where the gap will be.

[AGENT]: One real gap is showing up: the mill recipe can output `food_cornmeal`, but the low-level simple item factory only special-cases raw foods and relies on catalog fallback for flour/cornmeal. I’m checking whether the catalog loader produces the exact components the interaction and inventory expect.

[AGENT]: I’m also loading the repo’s Entire guidance because this is a codebase investigation and the local instructions require provenance-backed exploration for that class of task.

[AGENT]: Recorded history points at the recent “cornmeal, general store sign, valk glyph” checkpoint, which matches all three complaints. I’m reading that checkpoint’s intent before patching so I don’t undo the intended direction.

[AGENT]: The recorded intent confirms the last patch was meant to add cornmeal, the millstone grind sound, and a Valkyrie glyph. The code inference says the current tests are too narrow: they bypass the real content item factory for corn input and only verify class display data, not where the glyph is actually missing.

[AGENT]: For the Valkyrie issue, the data object has `glyph`, but the character creation UI still renders `icon`, so the glyph was added to data without being consumed. I’m patching that and tightening tests so this doesn’t pass while still broken in the UI/data boundary.

[AGENT]: I found a second live-path mismatch: the audio registry test proved the sound table points at the file, but not that content-authored aliases and the real `audio:play` routing resolve through the display adapter. I’m adding coverage at those boundaries rather than only checking an isolated emitted object.

[AGENT]: The most concrete fixes are now scoped: use class `glyph` in the character creation slide, add a plain `millstone_grind` alias alongside the namespaced action ID, and strengthen the mill test to use real catalog-created corn/cornmeal instead of a hand-built corn entity. I’m making those edits now.

[AGENT]: I’m applying the patch now: no formatter, just targeted lines in UI, audio registry, and tests.

[AGENT]: The edits are in. I’m running the focused tests that cover mill behavior, sound registry resolution, class display data, and audio wiring resolution.

[AGENT]: The focused checks are green. I’m doing a final diff pass to make sure the changes stayed narrow and didn’t touch unrelated work.

[AGENT]: Fixed all three. Changed: - [src/display/ui/charCreation.js](/home/pjensen/Repos/JSHack/src/display/ui/charCreation.js): character creation now renders `cls.glyph` before the decorative `icon`, so Valkyrie shows `@` instead of the wing icon. - [src/display/audio/sounds.js](/home/pjensen/Repos/JSHack/src/display/audio/sounds.js): added `millstone_grind` alias to the existing `action:millstone_grind` sound. - [tests/interaction.test.mjs](/home/pjensen/Repos/JSHack/tests/interaction.test.mjs): corn milling test now uses real catalog-created corn and asserts cornmeal is materialized. - Added tests covering the sound alias and glyph-vs-icon boundary. Verified: - `deno test --allow-read tests/interaction.test.mjs --filter millstone` - `deno test --allow-read tests/audioSoundsRegistry.test.mjs` - `deno test --allow-read tests/classDisplayData.test.mjs` - `deno test --allow-read tests/audioWiring.test.mjs --filter "generic audio payload keys"`