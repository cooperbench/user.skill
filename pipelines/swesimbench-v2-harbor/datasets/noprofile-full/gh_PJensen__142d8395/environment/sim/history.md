[SYSTEM]: # AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

[DEVELOPER]: small handful of UX work items. 1. the "mail" ux is a bit awkward on mobile, currently left aligned with no easy way to close it. I was thinking we could design a centered window with an obvious close button on each tab. this is our primary focus. 2. bumping into an altar from the left or right on mobile forces an offering of whatever item happens to be under your finger because inventory opens right away and the player is still mid tap. 2.1. we should only allow one offering per day per altar 2.2. the offered item glyph should appear rendered atop the shrine. 2.3. we should consider adding "on_offered" handler -- I know we have special handling for offering a dead pet, but I was thinking about making it (offering handler) canon across the engine. this opens up a whole new design dimension, if you offer something under a specific set of circumstances, something special happens -- we can dream stuff up. do as much as you possibly can in one-shot.

[AGENT]: I’ll use the local project guidance and inspect the existing mail and altar interaction paths before editing. I’m going to keep the first pass focused on the mobile mail close affordance, then push as far into altar offering behavior as the current architecture supports cleanly.

[AGENT]: I found both surfaces: mailbox UI is under `src/cloud/wiring` plus display UI, and altar behavior already has a two-phase offering flow with tests. I’m also loading the repo’s historical-context skill because this repo explicitly asks agents to use it when exploring code intent.

[AGENT]: Entire is enabled; I’ll treat intent as mostly inferred unless a specific checkpoint shows up for the exact files. Next I’m reading the UI overlay and altar action code side by side so the mobile event timing issue doesn’t get patched in the wrong layer.

[AGENT]: The mailbox overlay has no close event of its own, so the close button should be presentation-only: dispatch `ui:closeMailbox` and let the common overlay manager hide it. For altars, bump interaction currently bypasses the queued intent path, which explains the mobile “mid tap” inventory issue.

[AGENT]: The altar implementation already separates “prompt” and “execute offer”; the missing pieces are stronger gating around repeat offers and a way to preserve the offered item’s visual after the item entity is consumed. I’m going to add that as explicit altar state on the altar entity, then project it through WorldView for display.

[AGENT]: I’m going to implement “one offering per day per altar” as a small component on the altar, not world-attached state. The day key will use the existing calendar turn math, which keeps the rule deterministic and saveable alongside the altar entity.

[AGENT]: I haven’t found a direct rendered-glyph override field in WorldView yet, so I’ll add the altar overlay as a regular projected entity view at the altar position. That keeps display code generic: the item glyph rides the existing glyph renderer instead of needing a new canvas pass.

[AGENT]: The common panel helper has a close button, but mailbox rendering replaces the panel contents, so the generic close control gets deleted. I’m going to make mailbox render its own centered inner window and add a `ui:closeMailbox` listener so this overlay behaves like the others.

[AGENT]: I’m adding the canonical hook as a script verb rather than a one-off altar callback. That gives authored altar/shrine entities a reusable `altar:offered` extension point later, while the current default altar behavior remains unchanged.

[AGENT]: I’m about to patch four areas: mailbox overlay rendering, altar offering state/component, WorldView projection of the shrine-top glyph, and focused tests around the new altar behavior.

[AGENT]: One wrinkle: normal item entities draw below room features, but the offered item needs to sit above the altar. I’m projecting it as a normal entity-layer glyph with its own scale/offset so it draws after the altar but before the player.

[AGENT]: The altar state and projection are in place. I’m now wiring the projection into the final entity list and adjusting the mailbox overlay without touching unrelated panel code.

[AGENT]: To make the shrine-top glyph read like a small offering instead of a full-sized actor, I’m applying the existing `itemScale` field to the specific projected offering tag in the main draw loop.

[AGENT]: The mailbox change is next: centered modal window, an always-visible Close button, and a secondary close control in the tab row so it stays obvious after scrolling or switching tabs.

[AGENT]: I caught an implementation detail from the shared overlay helper: `show()` sets inline `display: block`, so CSS grid centering would be overridden. I’m switching the mailbox window itself to absolute centering, which works with the existing overlay show/hide behavior.

[AGENT]: For the mobile altar bug, I’m marking bump-triggered interactions with a source flag and making altars treat bumps as prayer-only. Intentional altar use still opens the offering chooser.

[AGENT]: Because I touched a listener installer, I’m also bringing it up to the repo’s current extension pattern now. That keeps this change inside the architecture ratchet instead of adding new installer debt.

[AGENT]: I’m adding focused tests for the behavior that changed: bumping an altar no longer opens the offer prompt, offerings are capped per altar day, the projected glyph appears, and the new offered hook runs while the offered item is still inspectable.

[AGENT]: The import wiring is in the test file; I’ll keep the tests local to `interaction.test.mjs` so verification stays focused on the interaction pipeline and WorldView projection.

[AGENT]: I noticed the overlay projection should key off the current frame’s visible/projected altar, not the reused record cache. I’m tightening that now so stale altar records don’t create offering glyphs after the altar leaves view.

[AGENT]: The functional edits are in. I’m running the focused interaction tests first, then I’ll run the relevant architecture/event guardrails if the focused suite is clean enough to proceed.

[AGENT]: The first failure is a plain JavaScript defaulting bug: day `0` was being treated as “missing.” I’m fixing that and then I’ll re-check the projection failure, which may be downstream of the same state issue.

[AGENT]: The day gate is fixed. The projection test still fails, so I’m checking whether the altar itself is entering WorldView in that minimal setup or whether the test needs to initialize visibility/map state like other WorldView tests.

[AGENT]: The projection code is working with altar state, but the minimal test world has no player and no loaded tile context, so `buildWorldView()` returns no entities. I’m updating that test setup to match real projection conditions with a player near the altar.

[AGENT]: I’m using the same setup pattern as the mailbox projection test: player plus nearby position. That makes WorldView’s visible-entity branch exercise the altar overlay.

[AGENT]: The projection setup is corrected. I’m rerunning the altar-focused filter before the broader interaction file.

[AGENT]: The altar-focused tests are green now. I’m running the full interaction test file next to catch collateral interaction regressions.

[AGENT]: The full interaction file is green. I’m running the architecture/event guardrails that matter here because this touched interaction listeners, event-ish altar behavior, and a new component.

[AGENT]: The architecture and event guardrails passed, and `deno check` on the touched files was clean. I’m doing one more targeted ratchet for world-attached state because the altar day gate deliberately uses a component instead.

[AGENT]: All targeted guardrails are green. I’m reviewing the final diff now for accidental scope creep and any obvious cleanup before I hand it over.

[AGENT]: The final diff review shows the altar work, but the mailbox files are not showing as modified. I’m checking those files directly now because the mailbox UX was the primary item and I don’t want to hand back a partial change.

[AGENT]: The mailbox changes are present in the working tree, but Git reports no diff for those two files, which means this checkout’s HEAD already contains the same mailbox edits now. I’m going to leave them as-is and include them in the summary as verified present rather than as pending diff.

[AGENT]: I found one small cleanup in the tests: two imports from the same interaction system module. I’m consolidating that before the final status.

[AGENT]: The cleanup is tiny, but I’m rerunning the focused test file once more so the final report reflects the actual final tree.

[AGENT]: The final focused test and check are clean. I’m taking one last status snapshot so I can give you the exact files changed and verification commands.

[AGENT]: Implemented the altar pass and verified the mailbox UX is present in the current tree. Key changes: - Altar bumping now prays only and does not open the offering chooser, fixing the mobile mid-tap accidental offering path. - Added `AltarOfferingState` so each altar allows only one accepted offering per in-game day. - Offered item identity is preserved and projected as a small glyph rendered above the altar/shrine. - Added canonical `ScriptVerb.AltarOffered` hook support for future authored `on_offered`-style behavior. - Converted the touched bump listener installer to `defineExtension(...)` / `world.install(...)`. - Confirmed mailbox overlay has a centered modal window and obvious close buttons in the current files. Verification run: - `deno test --allow-read tests/interaction.test.mjs` - `deno check src/display/ui/mailboxOverlay.js src/display/ui/overlay.js src/rules/content/interaction/interactPayloads.js src/bridge/schema/worldView.js tests/interaction.test.mjs` - `deno task guard:architecture` - `deno task guard:events` - `deno task ratchet:world-state` All passed.

[DEVELOPER]: interacting with an altar now does nothing but pray apparently, that wasnt the point. the point was that when players bumped it, they automatically offered the item that was directly undrer their finger. my reccommendation is to tweak the UX to popup an "offer" verb first that way they can control what happens -- otherwise, seems directionally right-ish.

[AGENT]: Got it. I overcorrected bump by making it prayer-only; the better shape is to make altar interaction present an explicit verb choice first, so neither bump nor tap drops straight into inventory selection. I’ll wire `Pray` and `Offer` as altar verbs, with `Offer` opening the item chooser.

[AGENT]: The action chooser infrastructure already exists and is used for fountain-style multi-action interactions. I’m going to register altar in that same menu path and adjust the altar payload so `Pray` prays, `Offer` opens inventory, and only selecting an item executes the offering.

[AGENT]: I confirmed the generic chooser dispatches `ui:requestActionSelect`, which queues an `InteractIntent` with the selected mode. That means `Offer` can open the altar item chooser only after the player explicitly chooses it.

[AGENT]: The current altar payload already handles `mode: "offer"` with no item by opening the item chooser, so the main bug is that `mode: "pray"` was missing and no-mode interactions were still going straight to offer prompt. I’m changing no-mode to chooser and `Pray` to prayer-only.

[AGENT]: I removed the bump special case from the altar payload. Since no-mode interactions now hit the generic action menu first, bumping and tapping both require an explicit `Pray` or `Offer` choice.

[AGENT]: The tests now match the corrected UX: first interaction produces the verb chooser; only `Offer` opens inventory selection; `Pray` is prayer-only. I’m running the interaction tests now.

[AGENT]: The altar-specific flow is green. I’m running the full interaction file and a targeted check for the files touched by this correction.

[AGENT]: The full interaction suite is green after the correction. Because this touched the interaction menu registry, I’m rerunning the architecture guardrail too.

[AGENT]: Fixed the altar UX correction. Now altar interaction works like this: - First tap/bump opens the generic action chooser: `Pray` / `Offer`. - `Pray` only prays. - `Offer` opens the item offering chooser. - Selecting an item still performs the offering, with the one-per-day gate, shrine-top glyph, and `AltarOffered` hook intact. Verification: - `deno test --allow-read tests/interaction.test.mjs` - `deno check src/rules/content/interaction/actionMenus.js src/rules/content/interaction/interactPayloads.js tests/interaction.test.mjs` - `deno task guard:architecture` All passed.