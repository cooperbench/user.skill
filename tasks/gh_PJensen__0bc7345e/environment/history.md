> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

we've been working on re-building interactable things. I want to make sarc and urn more RNG based outomes, an urn can spawn a spectral .. something a sarc can spwan a skeleton other outcomes? booby trapped? other creatures? NOTE: use new interaction strategy outlined in fountain.

> AGENT

I’ll ground this in the existing interactable and fountain work first, then turn it into a concrete implementation plan instead of guessing at the new strategy.

> AGENT

I found the search was too broad and noisy, so I’m narrowing to the actual interaction runtime and the fountain/urn/sarcophagus definitions. I’m also checking Entire metadata because this looks like a continuation of recent architectural work.

> AGENT

The repo confirms the new content-side interactables live under `src/content/interactables`, with fountain already separated there. I’m reading that path and the interaction runtime now, plus the checkpoint trail for the recent fountain strategy.

> AGENT

Fountain is using a chance-table rule inside a content-authored interactable, with outcome state recorded through components/events after a transactional interaction commits. I’m checking how objects like urns/sarcophagi are currently authored or spawned so the plan can attach to the right surface.

> AGENT

Urn and sarcophagus already have loot tables and population tests, but my scoped search still pulled a lot of unrelated lines. I’m going straight to the generator/population spots and existing loot tests now.

> AGENT

Current generation places `urn` and `sarcophagus` as spawn kinds and materializes sarcophagi through an archetype. The plan likely needs both content interactable definitions and a small materialization update if urns/sarcophagi do not already carry the right `Interactable.action`.

> AGENT

Both objects already have legacy actions: `breakUrn` and `openSarcophagus`. To follow the fountain strategy, the plan should move those outcomes out of the old payload registry into content-authored `defineInteractable` rules, keeping the archetype action names stable unless there is a reason to rename.

> AGENT

The legacy sarcophagus path already does two phases: spawn an undead guardian, then remove interactivity and stock burial loot in an inventory. I’m reading the exact tail so the plan preserves that one-time behavior while making the outcome table RNG-driven.

> AGENT

Fountain tests exercise exported rules directly with forced outcomes, which is the right pattern to copy. I’m checking those tests enough to make the acceptance criteria precise.

> AGENT

For “spectral something,” I’m checking what monster IDs already exist so the plan can reuse content rather than inventing a parallel creature unless needed.

> AGENT

There are enough existing pieces to plan this, but one product decision materially changes the implementation: whether these interactions should stay mostly loot objects with occasional danger, or become true risk/reward event tables.

> AGENT

I’ll use the risk/reward profile. One remaining feasibility detail is whether the transaction layer can already do “materialize drops into a container” or whether the plan needs a small mutation extension for sarcophagus loot.

> AGENT

<proposed_plan> # Crypt Interactable Outcome Tables **Summary** - Rebuild `breakUrn` and `openSarcophagus` using the same content-authored interaction strategy as fountain: `defineInteractable(...)`, `defineVerbRule(...)`, `chanceTable(...)`, transactional mutations, forced outcomes for tests, and typed result events. - Use a risk/reward profile: loot remains common, but traps and creature spawns become real outcomes. **Key Changes** - Add `src/content/interactables/crypt/index.js` and import it from `src/content/interactables/index.js`. - Keep archetype action names stable: - `Urn` keeps `Interactable.action = "breakUrn"`. - `Sarcophagus` keeps `Interactable.action = "openSarcophagus"`. - Remove the old `breakUrn` and `openSarcophagus` implementations from `src/rules/content/interaction/interactPayloads.js` once the authored content definitions replace them. **Outcome Behavior** - Urn `break` outcomes: - `ashes-loot`: destroy urn, spawn ashes, roll `urn:contents`. - `empty-ashes`: destroy urn, spawn ashes only. - `spectral-snake`: destroy urn, spawn ashes, spawn `spectral_snake` on nearest valid adjacent tile. - `poison-dust`: destroy urn, spawn ashes, apply poison or poison damage to actor. - `shard-trap`: destroy urn, spawn ashes, deal small physical/piercing damage to actor. - Sarcophagus `open` outcomes: - `burial-loot`: open sarcophagus, make it non-solid, remove interactivity, stock `sarcophagus:contents` inside its inventory. - `skeleton`: spawn depth-appropriate skeleton-family monster adjacent to the sarcophagus. - `restless-dead`: rarer depth-gated hostile outcome using existing undead such as `wight` or `carrion_shade`. - `booby-trap`: deal physical damage […]

> DEVELOPER

do it, make it clean too.

> AGENT

I’m still in Plan Mode, so I can’t edit the repo yet. The implementation spec is ready and decision-complete; switch me out of Plan Mode and I’ll make the changes cleanly, with focused tests and the event guardrail.

> DEVELOPER

go for it -- my benchmark, is I could trigger fungal spores at 5% chance, with relative ease vs hunting through some giant switch block.

> AGENT

I’m going to implement this as a small content module, not another branch in the legacy payload switch. The extensibility target is a reusable outcome table where adding something like a 5% fungal-spore outcome is one authored entry.

> AGENT

The existing transaction layer can destroy, spawn monsters, materialize drops, patch components, and damage, but it can’t yet “remove Interactable” or put materialized loot into an existing container atomically. I’m adding those as small generic mutation operations so crypt content stays declarative.

> AGENT

I’m going to preserve the existing action names and one-time semantics. The new part is the table shape: `crypt.urn.break` and `crypt.sarcophagus.open` will be exported authored rules with forced-outcome test hooks, mirroring fountain.

> AGENT

The component definitions are named exports but don’t include searchable string names the way I expected, so I’m reading the few components directly before patching the transaction types.

> AGENT

I’m patching the transaction layer first: small generic operations only, then the crypt content module can stay free of direct `world.remove`, `createFrom`, and inventory plumbing.

> AGENT

The first patch missed because this file didn’t already import `Inventory`; I’m applying the same idea in smaller patches against the exact current shape.

> AGENT

The transaction operations are in. I’m updating the public mutation facet now so authored interactables can call them without using low-level queue objects everywhere.

> AGENT

Next I’m making ashes usable through the existing loot materializer. That keeps urn outcomes as ordinary drop descriptors instead of a bespoke object-spawn path.

> AGENT

I’m adding typed events for the new interaction contracts now, then wiring display/audio to those typed events instead of relying on new string-only rules events.

> AGENT

I found the authored verb runner wasn’t passing static `Interactable.params` into the new rule context. I’m adding that as `interactableParams` so sarcophagus depth remains authored data, while keeping the existing fountain API intact.

> AGENT

Now I’m adding `src/content/interactables/crypt/index.js`. The table entries are the main extension point: adding fungal spores later should be a single weighted entry plus its apply function.

> AGENT

The crypt content module is in place. I’m registering it and then removing the old legacy urn/sarcophagus payload blocks so there’s one canonical interaction path.

> AGENT

I’m deleting only the two migrated payload entries from the legacy registry. Other legacy interactions stay untouched.

> AGENT

The old payload blocks are gone. I’m updating message and audio wiring to consume the new typed urn event while preserving the same user-facing shatter message and sound.

> AGENT

This message wiring file gets most dependencies through its install context, so I’m adding a normal event import at the top and leaving the rest of the context shape alone.

> AGENT

Audio already imports typed fountain events in the same file, so the urn event fits the existing pattern.

> AGENT

I’m cleaning up the imports now. Since the old block carried direct monster and loot helpers, any leftovers need to come out to keep the migration clean.

> AGENT

I’m tightening the crypt helper so loot counts are straightforward and not pretending to use a receipt it doesn’t need.

> AGENT

I’m adding focused tests next. They use forced outcomes like fountain tests, so the RNG table stays testable without hunting seeds.

> AGENT

The older interaction tests still expected the legacy string event and unforced skeleton behavior. I’m updating just those sarcophagus tests to use the authored rule and typed event deterministically.

> AGENT

The targeted tests are in place. I’m running a static check now before the runtime tests so syntax/import issues surface quickly.

> AGENT

Static check passed. I’m running the new crypt tests and the existing adjacent interaction/loot tests next.

> AGENT

The first runtime failure shows my new `removeComponent` op did not remove `Interactable` under this ECS API. I’m checking the removal semantics and fixing the generic op, then I’ll rerun.

> AGENT

ECS defers `world.remove` during ticks, which makes transactional “opened now” assertions stale. The library has an immediate removal API for exactly this kind of helper-local invariant, so I’m using that when available.

> AGENT

Actually the failed test is running outside the scheduler, so deferral isn’t the issue there. I’m going to instrument by checking the transaction result and op order in the failing path rather than guessing.

> AGENT

The actual failure is cleaner: `resolveLootTable` expects the RNG object to have `choice()`. Fountain didn’t hit that because its table paths mostly used `int/next`; crypt loot does. I’m extending the interaction RNG facade with `choice`, matching the project RNG API.

> AGENT

I’ve added the missing RNG method. I’m rerunning the failed crypt suite first.

> AGENT

The new crypt tests pass now. I’m running the full focused set again, plus the event guardrail because this added new event contracts.

> AGENT

The focused tests and event guardrail pass. I’m doing a final architecture guard and diff review now, mainly to catch boundary/import mistakes and accidental legacy leftovers.

> AGENT

The architecture guard passes. I’m checking the final file list now, including new files that weren’t shown in the compact diff command.

> AGENT

The remaining status is only the intended edits and new files. I’m doing one last targeted test for the normal dispatch path, not just direct rule execution, because the game will hit these through `Interactable.action`.

> AGENT

Implemented. What changed: - Added `src/content/interactables/crypt/index.js` with authored chance-table rules for: - urn breaking: ashes/loot, empty ashes, spectral snake, poison dust, shard trap - sarcophagus opening: burial loot, skeleton, trap, restless dead, treasure cache, empty - Removed legacy `breakUrn` / `openSarcophagus` giant payload blocks. - Added typed events: - `UrnInteractionResolved` - `SarcophagusInteractionResolved` - Extended the interaction transaction layer with clean generic ops for removing components, ensuring inventory, and materializing loot into containers. - Added RNG `choice()` to the interaction RNG facade so loot tables work naturally from authored rules. - Updated audio/message wiring to consume the typed urn event. The fungal-spore benchmark is now the intended path: add one weighted entry to `urnBreakTable`, e.g. `weight: 5`, with an `apply(ctx)` function. Verification run: - `deno check ...` targeted changed files/tests - `deno test --allow-read tests/cryptInteractables.test.mjs tests/interaction.test.mjs tests/urnLoot.test.mjs tests/sarcophagusLoot.test.mjs` - `deno task guard:events` - `deno task guard:architecture` All passed.