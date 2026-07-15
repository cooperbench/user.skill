> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

what were some big refactorings and cleanups that I've been busy working towards? ** interactions, interactables (defineInteractable) ** improving item, monster authoring (defineItem, defineMonster) I feel like interactions was partially migrated -- but I don't know how many other types of complex interactions there really is beyond fountain -- which I think we did a good enough job at. I feel like we should be focusing on gameplay more; specifically, really making quests more sophisticated, making use of the new `rifts` feature, and beyond. we have a ton of content that can be surfaced. along with making even more use of the lighting engine across the board. help me set the direction please. frankly, I think we've done enough today -- so this might be just planning for the week.

> AGENT

I’ll ground this in the repo’s current state and the project-history skill before suggesting direction, so the plan reflects what’s actually been built rather than a generic roadmap.

> AGENT

The first pass shows there is already a written progression roadmap, plus concrete systems/tests around generated quests, notice-board offers, rifts, and lighting. I’m going to check the recorded checkpoint history next, then narrow the code scan to the specific surfaces you mentioned.

> AGENT

Entire is enabled, but this CLI build doesn’t support the `--no-pager/--json` flags for `dispatch`, so I’ll use its available recap/search commands cautiously and keep source-code observations separate from recorded intent.

> AGENT

The roadmap doc already says the current bottleneck almost exactly: the game has plenty of systems, but the strongest ones are not visible as player-facing promises. That aligns with your instinct to stop doing broad plumbing and move toward quests, rifts, lighting, and surfaced content.

> AGENT

A couple of important repo facts are different from the older roadmap: `defineItem()` is broadly in use, and `defineMonster()` is no longer just “ready” or “not started”; many monsters already live under `src/content/monsters/`. Interactions are more mixed: fountain/mailbox/rift are authored, but there is still a large legacy interaction payload table.

> AGENT

On interactions: the remaining legacy table is not just fountain-grade bespoke content. It also owns core engine verbs like doors, stairs, shops, chest opening, crafting stations, beds, harvest nodes, altars, hydraulics, and dungeon transitions. That suggests “finish interaction migration” should be selective, not a week-long cleanup project.

> AGENT

Rifts are implemented enough to be a real content surface: portal entity, light emitter, `RiftState`, concrete open/close/enter events, and a `defineInteractable("riftPortal")` entry. The likely next step is not “make rifts exist”; it’s to give them authored reasons, rewards, and quest hooks.

> AGENT

`entire recap` hit a sandbox access issue while trying to read the local auth token, so I’m requesting the same non-mutating history lookup outside the sandbox. That should improve the “what have I been busy working toward” part.

> AGENT

The recorded week recap says this was a concentrated burst: 12 sessions, 18 checkpoints, about 2.5M tokens, with today the active day. The recent commits line up with what you named: interaction affordances, define-interactable migration, early rifts, portal/rift visuals, mailbox, NPC sleep, and some performance/transition cleanup.

> AGENT

<proposed_plan> # JSHack Weekly Direction: Surface The Game ## Summary Recorded intent and recent commits show the big work has been about removing bespoke wiring so content can become player-facing faster: - `defineItem()` is effectively established; item content is broadly in `src/content/items/`. - `defineMonster()` is further along than the older roadmap says; `src/rules/data/monsters.js` is now an empty legacy shell, while monsters live under `src/content/monsters/`. - `defineInteractable()` exists and is useful, but the migration should pause at “content-worthy interactions.” Fountain, mailbox, and rift are authored; the remaining legacy table mostly contains core engine verbs like doors, stairs, shops, chests, beds, workstations, hydraulics, altars, and harvest nodes. - Rifts and lighting are now real surfaces: rift portals have authored interaction, state, concrete events, `LightEmitter`, and portal/rift VFX patterns. The week should shift away from broad cleanup and toward gameplay resonance: quests that promise meaningful rewards, rifts as authored quest/content hooks, and lighting as both mood and mechanics. ## Key Changes - Make quest rewards the first gameplay spine. - Treat `docs/PROGRESSION_RESONANCE_PLAN.md` as the current north star. - Keep Rat Infestation as the proven starter slice: it already promises/grants `bow_mirror`; verify tracker, journal, completion event, and inventory grant stay aligned. - Upgrade `The […]

> DEVELOPER

the challenge I think is to make a fun game from all we have -- chckout this writeup from a recent web session. Reading through it, the mechanics are solid. The problem isn't the code. The problem is the story. Right now it's a classic MMO quest: > Rats exist → kill 5 → collect reward. A Witcher quest almost never works like that. It starts with an assumption, then slowly reveals you were wrong. Your quest already has the beginnings of this—the barkeep, the cellar, the key, the rats. We just need to add mystery and escalation. I'd restructure it into acts. --- ## Act I — The Obvious Problem The barkeep is irritated. > "Something's gotten into the cellar again. > Barrels chewed open. > Customers hear scratching all night. > Kill five rats and I'll pay." Nothing unusual. Player accepts. Barkeep hands over the cellar key. Exactly what you have today. --- ## Act II — Something Isn't Right Player enters. Instead of ten rats charging... It's... quiet. One rat runs away. Another ignores the player. Dead rats are everywhere. Gnawed from the inside. Something killed them. Now curiosity begins. --- ## Environmental Storytelling This is where […]

> AGENT

I’ll check what the quest and interaction layers can actually express today, then I’ll map the writeup onto engine-supported slices instead of turning it into a design wish list.

> AGENT

The quest runtime is already capable of the Witcher-style structure: arbitrary event-driven nodes, mutable vars, checklist projection, `quest:advanced`, `quest:progress`, and interactable-driven events. The missing piece is not engine power; it’s authoring a small vocabulary of “clue discovered” interactions and using checklist state instead of kill counts.

> AGENT

The engine can support most of that now. The missing piece is not a big quest engine rewrite; it is a small authoring surface for “clues” and a better authored quest shape. <proposed_plan> # Rat Quest Direction: From Kill Count To Investigation ## Summary Turn Rat Infestation into the first “the obvious story is wrong” quest. Use existing engine support: quest nodes, checklist vars, authored interactables, `ObjectState`, messages, spawned entities, dungeon transition hooks, and reward preview. Avoid new UI and avoid broad interaction migration. ## Key Changes - Replace the quest spine from `offer -> hunt -> report -> complete` with: `offer -> investigate -> discovery -> decision -> report -> complete`. - Keep the tavern rat moment on acceptance: - Barkeep gives cellar key, short bow, arrows. - A rat appears near the barkeep. - Barkeep reacts. - Quest objective becomes: “Investigate the cellar.” - Add a generic authored clue interactable: - `defineInteractable("questClue", ...)` - Params: `questId`, `clueId`, `title`, `message`, optional `stateAfterInspect`. - On interact, emit `quest:clueDiscovered`. - Optionally set `ObjectState` from `fresh` to `inspected`. - Seed tavern-basement clues when the active quest reaches investigation: - dead rats - ripped flour sacks - strange slime - oversized bite marks […]

> DEVELOPER

I'm not sure how I feel about clues since we're lacking "chaff" (story telling decorative stuff), but I do really like more than one way to resolve something. Did the player use a scroll of genocide on rats? How can we make a "rat-king" type of monster. Can the player kill the rat-king and have the game remember it? How can the game tell a story?

> AGENT

I’ll check the existing genocide, monster authoring, and quest memory paths before proposing story mechanics, because the best answer here depends on what the engine can already remember and react to.

> AGENT

Genocide already emits `scroll:genocide:success` with the chosen monster identity, and quests can listen to arbitrary string events. That means “used genocide on rats” can be a real quest resolution path without new infrastructure.

> AGENT

Yes, the engine can support this, and I agree with your hesitation about “clues.” If every inspectable object is meaningful, it feels like a checklist. Without decorative chaff, the better pattern is **consequence-first storytelling**: the story is told by what systems react to, not by scattering lore props. A strong v1 shape: - Player is told “rats are the problem.” - Player can solve it several ways: - kill enough rats - kill the Rat King - use `scroll_genocide` on rats - maybe later: seal the tunnel, feed/appease the nest, burn it out - The quest remembers **how** it was solved. - NPC dialogue and future spawns react to that remembered fact. Mechanically, this is already within reach: - `scroll:genocide:success` already emits `{ identity, name, killed }`. - Quests can listen to arbitrary events. - `DeathApplied` plus a small quest death system can detect `rat_king` dying. - `QuestVars` can store `resolution: "genocide" | "killed_rat_king" | "culled_rats" | "sealed_tunnel"`. - Town dialogue already checks quest records, so the barkeep can say different things later. <proposed_plan> # Rat King Story Slice ## Summary Turn Rat Infestation into a systemic quest with multiple valid resolutions, without relying on decorative clue spam. The story […]

> DEVELOPER

only ammendment, small dungeon, short dungeon generation makes now allowance for "more optional depth" right now -- it's as long as it is and that's it. I cannot think of a clean way to execute on that short of: * expanding the cellar, then ... * placing a gate under lock and key in the middle of the dungeon * at the end of the generation, past the locked cellar door, placing rat_king this strikes me as potentially tricky, doable, but tricky. if you want to start by adding geocide completion path, that would be a good start. but do tell me how hard this second half dungeon actually is. NOTE: reward is now a world outcome in a sense. NOTE: we do have some chaff stuff, but I think we should work to make them interactable, shelving, etc. /plan

> AGENT

I’ll ground the dungeon-half question in the actual generation code and tavern basement template before rating difficulty, then I’ll give you a concrete plan that starts with the genocide completion path.

> AGENT

The tavern entrance is already a very-hard keyed dungeon gate, and the current Rat quest grants that key. That means the “locked middle gate” would be a second lock inside an already locked branch, not just using the existing entrance gate. I’m checking whether the template/profile gives us a clean boss placement hook.

> AGENT

<proposed_plan> # Rat Quest Next Step: Genocide Path First, Rat King Later ## Summary Start with the clean, low-risk gameplay branch: let `scroll_genocide` on rats resolve or alter Rat Infestation. Defer the “second half of the cellar” until after that because forcing optional depth into a fixed one-floor template is doable but not clean. The Rat King itself is not hard. The hard part is guaranteeing a satisfying gated “back half” inside a short generated dungeon without breaking reachability, stair placement, or template simplicity. ## Difficulty Call - **Genocide completion path: low difficulty.** - `genocideSystem` already emits `scroll:genocide:success`. - Quest runtime can already listen to that event. - Rat quest can store `resolution: "genocide"` in `QuestVars`. - Barkeep dialogue can branch from quest state. - **Rat King as a monster: low to medium difficulty.** - Add `rat_king` with `defineMonster()`. - Spawn it with existing monster spawning helpers. - Detect its death through `DeathApplied`, like run contracts do. - **Rat King in a locked second half of tavern basement: medium-high difficulty.** - Tavern basement is one floor, one generated extent, currently `floors: 1`. - The template does not have a concept of optional extra depth. - A middle gate requires reliable […]