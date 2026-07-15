> SYSTEM

# AGENTS.md instructions for /home/pjensen/Repos/JSHack <INSTRUCTIONS> @/home/pjensen/.codex/RTK.md --- project-doc --- # AGENTS.md - JSHack Field Manual JSHack is a zero-dependency browser roguelike: pure JavaScript, pure ES modules, ECS architecture, Deno tooling. This file is optimized for coding agents. Prefer the commands below over manual spelunking. Deeper docs: - [README.md](README.md) - [SEPARATION_MANIFEST.md](docs/architecture/SEPARATION_MANIFEST.md) - [RUNTIME_TOPOLOGY_DOCTRINE.md](docs/architecture/RUNTIME_TOPOLOGY_DOCTRINE.md) - [TEN_COMMANDMENTS.md](docs/architecture/TEN_COMMANDMENTS.md) - [ecs-js/AGENTS.md](src/lib/ecs-js/AGENTS.md) --- ## Hard Laws - **No build step.** Pure ES modules. No webpack, babel, JSX, TypeScript, or bundling. - **Deno, not Node.** Tests and tools run with Deno. Default test command: `deno test --allow-read`. - **JavaScript only.** Keep source as `.js` / `.mjs`. - **Mobile-first.** Touch is primary; desktop keyboard is secondary. - **Separation is law.** `rules/` never imports `display/` or `bridge/`; `display/` never imports `rules/`; `bridge/` projects read-only rule state. - **No system-to-system calls.** Systems communicate with `world.emit` / `world.on`; scheduler owns ordering. - **New events use concrete event classes.** Any new event contract must define a concrete `EcsEvent` class and emit an instance with `world.emit(new Event(...))`. Do not introduce string-only events or parallel string re-emits for new contracts. - **Touched listener installers use canonical extensions.** Any new listener installer, or any existing listener installer touched during a task, must use `defineExtension(...)` […]

> DEVELOPER

Add an experimental generic LLM cloud extension. Goal: introduce a clean seam for AI usage without binding gameplay code directly to any one model provider. Implement two pieces: 1. A cloud extension for OpenAI-compatible LLM access. 2. An `AI` resource that fronts all model access. Future direction: The `AI` resource should eventually support two backend paths: 1. Browser-native LLM pathway, using Chrome / future browser-supported language model APIs. 2. OpenAI-compatible chat completions endpoint, which may be local, LAN-hosted, or remote. For now, implement only the OpenAI-compatible chat completions endpoint path. Use this as the default endpoint value: ```txt id="yri0f7" http://10.0.0.69:8080/v1/chat/completions ``` Do not hard-code this as the only option. Treat it as a configurable default. Any compatible chat completions endpoint plus optional API key should be allowed. Add an experimental configuration section inside the existing Settings tab in the character sheet. Settings should include only transport/provider-level configuration: ```txt id="dc6812" Enabled Endpoint URL API Key Model name ``` Do not put `temperature`, `maxTokens`, or other generation parameters in global settings. Those belong at the call site because NPC speech, procedural books, quest drafts, rumors, and other future uses will require different generation behavior. Persist these settings using the project’s existing settings/storage […]

> TOOL

<turn_aborted> The user interrupted the previous turn on purpose. Any running unified exec processes may still be running in the background. If any tools/commands were aborted, they may have partially executed. </turn_aborted>

> DEVELOPER

one second -- small ammendment incoming. Add an experimental generic LLM cloud extension. Default endpoint: ```txt http://10.0.0.69:8080/v1/chat/completions ``` This should be the default configured value, not the only supported value. Goal: introduce a clean seam for AI usage without binding gameplay code directly to any one model provider. Implement two pieces: 1. A cloud extension for OpenAI-compatible LLM access. 2. An `AI` resource that fronts all model access. Future direction: The `AI` resource should eventually support two backend paths: 1. Browser-native LLM pathway, using Chrome / future browser-supported language model APIs. 2. OpenAI-compatible chat completions endpoint, which may be local, LAN-hosted, or remote. For now, implement only the OpenAI-compatible `/v1/chat/completions` endpoint path. Add an experimental configuration section inside the existing Settings tab in the character sheet. Settings should include only: ```txt Enabled Endpoint URL API Key Model name ``` Do not put `temperature`, `maxTokens`, or other generation parameters in global settings. Those belong at the call site because NPC speech, procedural books, quest drafts, rumors, and other future uses will require different generation behavior. Persist these settings using the project’s existing settings/storage approach. Create an `AI` resource that gameplay systems can call without knowing endpoint details. Shape the resource roughly […]

> AGENT

I’ll inspect the settings/storage and character sheet UI first, then trace any NPC speech/dialogue seam before editing so the new AI surface fits the existing architecture.

> AGENT

I found the settings path in `inventoryDataProvider` and the character sheet settings renderer, plus an existing `npc:dialogue` bubble path. I’ll also read the repo-specific cloud notes before adding the extension.

> AGENT

The cloud layer explicitly allows optional `fetch`-backed clients as long as failures do not affect gameplay. The likely implementation is a small `src/cloud/llm` client plus a `main` resource module that reads persisted UI settings.

> AGENT

Settings rendering is DOM-built directly in `overlayRenders.js`, with input settings using localStorage helpers in display code. I’m going to keep AI configuration in its own small settings module so both UI and the AI resource read the same persisted contract.

> AGENT

I’m going to add three small surfaces: a shared persisted AI settings module, a cloud OpenAI-compatible chat client, and a world resource wrapper in `main/resources`. Then I’ll wire the Settings tab to read/write only the four provider-level fields.

> AGENT

The AI resource itself will be installed as an ECS world extension, but its backing state is runtime-only and non-serializable. Calls return text or `null`; generation options stay on each `complete()` call.

> AGENT

The Settings tab now has an “Experimental AI” section with only the requested transport fields. Next I’m adding focused tests around persistence, disabled behavior, request shaping, and safe failure.

> AGENT

I added focused tests without touching generation parameters in settings. I’m going to run just the new tests first, then a relevant architecture/event guard if the focused set passes.

> AGENT

I noticed a boundary issue before running guardrails: if rules systems eventually call the resource, its resource token cannot live in `main/` with cloud imports. I’m splitting the token into `rules/resources/AI.js` and keeping the cloud-backed implementation installer in `main/`.

> AGENT

Focused tests and architecture guardrails pass. I’m doing a final diff/status pass now, mainly checking that the resource boundary is clean and no unrelated files were touched.

> AGENT

`git diff --stat` only shows tracked files, so the new modules are untracked as expected. I’m running the standard project `check` task once since the scheduler import path changed.

> AGENT

`deno task check` also passes, including event guardrails. I’m checking the final file contents now for naming, defaults, and the disabled/null behavior before I wrap up.

> AGENT

The split looks clean: `rules/resources/AI.js` is just the stable token and disabled fallback, while `main/resources/AI.js` installs the OpenAI-compatible implementation. I’m adding one more resource-level test to prove enabled calls read settings and still hide endpoint details from callers.

> AGENT

Everything still passes after the added resource integration test. I’m grabbing final status and line references for the summary.

> AGENT

One last adjustment: I’m removing the invented default model value. The request only specified a default endpoint, so an unset model should remain unset and fail closed until configured.

> AGENT

Implemented the experimental AI seam. Key changes: - Added persisted AI settings with default endpoint `http://10.0.0.69:8080/v1/chat/completions` in [aiSettings.js](/home/pjensen/Repos/JSHack/src/shared/aiSettings.js:1). - Added OpenAI-compatible chat completions client in [openAICompatible.js](/home/pjensen/Repos/JSHack/src/cloud/llm/openAICompatible.js:37). - Added stable `AIResource` token with disabled/null fallback in [AI.js](/home/pjensen/Repos/JSHack/src/rules/resources/AI.js:16). - Installed the cloud-backed experimental implementation from [AI.js](/home/pjensen/Repos/JSHack/src/main/resources/AI.js:32) via [scheduler.js](/home/pjensen/Repos/JSHack/src/main/scheduler.js:134). - Added Settings tab fields for `Enabled`, `Endpoint URL`, `API Key`, and `Model name` in [overlayRenders.js](/home/pjensen/Repos/JSHack/src/display/ui/overlayRenders.js:206). - Wired settings persistence through [inventoryDataProvider.js](/home/pjensen/Repos/JSHack/src/main/ui/inventoryDataProvider.js:895). Usage shape is: ```js const AI = world.resource(AIResource); const text = await AI.complete({ messages, temperature, maxTokens }); ``` It returns `null` when disabled, unconfigured, unavailable, or failed. I did not wire LLM output directly into NPC speech yet; the resource is ready for that flavor-text path without making AI authoritative over simulation state. Verification: - `deno test --allow-read tests/aiSettings.test.mjs tests/openAICompatible.test.mjs tests/aiResource.test.mjs` - `deno task check`

> DEVELOPER

question: why wouldn't rules be able to access it -- the split there is not clear to me, this resource specifically should be accessible from just about any system. (e.g.) an NPC speaks is that not true?

> AGENT

Yes, rules systems can access it. That is exactly why I split it. The distinction is: - [src/rules/resources/AI.js](/home/pjensen/Repos/JSHack/src/rules/resources/AI.js:16) defines the stable `AIResource` token that rules systems can import and call with `world.resource(AIResource)`. - [src/main/resources/AI.js](/home/pjensen/Repos/JSHack/src/main/resources/AI.js:32) installs the browser/cloud-backed implementation for that token at world setup time. So an NPC speech system can do: ```js import { AIResource } from "../resources/AI.js"; const AI = world.resource(AIResource); const line = await AI.complete({ messages: [ { role: "system", content: "Generate short NPC flavor speech." }, { role: "user", content: "Barkeep greeting the player." }, ], temperature: 0.8, maxTokens: 40, }); ``` What rules should not import is the provider implementation, because that would make deterministic rules code depend directly on `cloud/`, `fetch`, endpoint settings, bearer keys, etc. The resource token is the seam; the implementation is injected by `main`. One important caveat: existing rules systems are synchronous and deterministic. So while rules can access the resource, we should be careful about introducing `await` inside normal scheduler systems. The cleaner NPC speech integration may be a main/cloud listener that decorates `npc:dialogue` or a separate async flavor pipeline, unless we deliberately add an async-capable non-authoritative speech surface.