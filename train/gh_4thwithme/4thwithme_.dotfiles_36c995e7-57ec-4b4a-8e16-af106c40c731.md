---
session_id: "4thwithme/.dotfiles|36c995e7-57ec-4b4a-8e16-af106c40c731"
developer: "gh:4thwithme"
split: train
source: crawl
repo: 4thwithme/.dotfiles
start_time: "2026-04-10T11:15:01.658Z"
n_turns: 22
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

hey bro, do i understand it right, when i turn off orb stack, my index in elastic dissappear?

> AGENT

Depends on your setup:

- **Container stopped** (OrbStack shut down) → data persists. Next start, index is there.
- **Container removed** (`docker rm`) → data gone, unless you mounted a volume.

Check if your Elasticsearch has a volume:

```bash
docker inspect <elastic-container> | grep -A5 Mounts
```

If you see a volume mount for `/usr/share/elasticsearch/data` → your index survives restarts and even container removal.

If no volume → index lives only inside the container layer. Stop is fine, remove kills it.

**TL;DR**: Turning OrbStack off = stopping containers. Data survives. Your index should be there when you turn it back on.

> DEVELOPER

but whrn I started dev seraver and tried request to the vector search model i got

{ level: 'log', pid: 49989, timestamp: 1775819631519, correlationId: '7ec76b93-bfa9-4126-9e0a-fc5ba8fa7ab2', message: `[LogExecution]: Method invoked with parameters, {"params":{"queryText":"I'm looking for a MagSafe power bank for iphone","size":12},"className":"OpensearchNeuralService","methodName":"searchProducts","timestamp":"2026-04-10T11:13:51.519Z"}`, context: 'OpensearchNeuralService.searchProducts' }
{ level: 'error', pid: 49989, timestamp: 1775819631536, correlationId: '7ec76b93-bfa9-4126-9e0a-fc5ba8fa7ab2', message: '[LogExecution]: Method failed after 12.99ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"OpensearchNeuralService","methodName":"searchProducts","timestamp":"2026-04-10T11:13:51.532Z","executionTimeMs":12.993500000000495,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10187:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10581:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19911:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19795:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'OpensearchNeuralService.searchProducts' }
{ level: 'error', pid: 49989, timestamp: 1775819631544, correlationId: '7ec76b93-bfa9-4126-9e0a-fc5ba8fa7ab2', message: '[LogExecution]: Method failed after 25.27ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"NeuralSearchService","methodName":"search","timestamp":"2026-04-10T11:13:51.544Z","executionTimeMs":25.267250000000786,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10187:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10581:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19911:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19795:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'NeuralSearchService.search' }
{ level: 'error', pid: 49989, timestamp: 1775819631544, correlationId: '7ec76b93-bfa9-4126-9e0a-fc5ba8fa7ab2', message: '[LogExecution]: Method failed after 26.18ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"NeuralSearchController","methodName":"search","timestamp":"2026-04-10T11:13:51.544Z","executionTimeMs":26.17979099999866,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10187:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10581:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19911:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19795:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'NeuralSearchController.search' }
{ level: 'error', pid: 49989, timestamp: 1775819631546, correlationId: '7ec76b93-bfa9-4126-9e0a-fc5ba8fa7ab2', message: Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search
       at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10187:19)
       at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10581:56)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19911:61)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19795:41)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29
       at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
       at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28, context: 'ExceptionsHandler' }

> AGENT

Yes, that's exactly what happened. OrbStack restart killed your OpenSearch container's in-memory model state.

The error tells you the fix:

```bash
npm run cli:dev -- bootstrap-neural-search
```

This re-registers the neural search model in OpenSearch. You need to run it every time OpenSearch restarts (i.e., every OrbStack restart) — unless your OpenSearch data is volume-mounted AND the model was persisted to the index.

> DEVELOPER

what does it mean container's in-memory model state.

> AGENT

OpenSearch loads ML models (like your text embedding model for vector search) into RAM when they're deployed. The model registration and deployment state lives in a system index (`.plugins-ml-model`), but the **running model process** is in memory.

When OrbStack stops → container stops → OpenSearch process dies → RAM is gone → model is no longer deployed.

When OrbStack restarts → OpenSearch starts back up → data indexes are restored from disk → but the model needs to be **re-deployed** (loaded back into RAM) before it can serve inference requests.

That's what `bootstrap-neural-search` does — it re-deploys the model so OpenSearch can run embeddings again.

> DEVELOPER

check files before making advices @src/modules/cli/commands/bootstrap-neural-search.command.ts @docs/features/neural-search/ @src/modules/opensearch/ @src/modules/cli/commands/

> AGENT

OK, now I have the full picture. Let me correct my earlier explanation.

After OrbStack restart, your OpenSearch **data is fine** (volumes persist). What breaks:

1. Model state goes from `DEPLOYED` → `REGISTERED` (weights on disk, not loaded in RAM)
2. `OpensearchNeuralService.resolveModelId()` (`opensearch-neural.service.ts:49`) searches for `model_state === 'DEPLOYED'` → finds nothing → `modelId` stays `null`
3. `getModelId()` (`opensearch-neural.service.ts:69`) throws because `modelId` is null

Your index and embeddings are intact. Only the model needs re-deployment.

**The problem**: neither command has a "just redeploy" option. `setup-neural-search` re-registers a new model. `bootstrap-neural-search` without `--cleanup` creates duplicates.

Fastest path right now:

```bash
npm run cli:dev -- bootstrap-neural-search --cleanup
```

This nukes everything and rebuilds (takes several minutes due to model download + product re-indexing).

**Better long-term fix**: add a lightweight `redeploy-neural-search` command that just finds the existing registered model and deploys it — would take seconds instead of minutes. Want me to build that?

> DEVELOPER

lets add redeploy-neural-search... create it as @src/modules/cli/commands/ and execute when serve started and opensearch loaded, in case no model just warning

> AGENT

Four changes needed.

> AGENT

Diagnostic is just LSP lag — method is in the same class. Now the CLI command and module registration.

> AGENT

Let me verify the final state.

> AGENT

Type-check passes clean.

**Summary of changes:**

1. **`opensearch.service.ts`** — Added `redeployRegisteredModel()`. Finds model group → checks for DEPLOYED (returns early) → finds REGISTERED/UNDEPLOYED model → deploys it → waits → returns model ID.

2. **`opensearch-neural.service.ts`** — Added `attemptAutoRedeploy()`. Called from `onModuleInit()` when `resolveModelId()` finds no deployed model. Warns if no registered model exists.

3. **`redeploy-neural-search.command.ts`** — New CLI command. Usage:
   ```bash
   npm run cli:dev -- redeploy-neural-search
   ```

4. **`cli.module.ts`** — Registered the new command.

**Behavior after OrbStack restart:**
- Server starts → `onModuleInit` → no DEPLOYED model found → auto-redeploy kicks in → deploys existing REGISTERED model → neural search works
- If no model exists at all → warning log, no crash

> DEVELOPER

bro...
  ~/Documents/repo/recommendations-service   RECO-000-neural-search wip *18 !3 ?1 ❯ npm run start:dev                                                                                           ✘ INT   13:27:14

> recommendations-service@0.0.1 start:dev
> nest start --watch --webpack --webpackPath webpack.config.js


 Info  Webpack is building your sources...

webpack 5.103.0 compiled successfully in 3572 ms
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL_READ_REPLICA, converter: String
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: REDSHIFT_READ_URL, converter: String
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: GLOBAL_PREFIX, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: PORT, converter: Number
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: SERVER_NAME, converter: none
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: IS_COMPACT_LOGS, converter: Boolean
[Nest] 58920  - 04/10/2026, 1:27:22 PM     LOG [EnvConfigService] Fetching environment variable: IS_JSON_LIKE_LOGS, converter: Boolean
{ level: 'log', pid: 58920, timestamp: 1775820443031, correlationId: 'f2776be2-10de-4cc2-a055-9b1e93a19ce9', message: 'Starting Nest application...', context: 'NestFactory' }
{ level: 'log', pid: 58920, timestamp: 1775820443099, correlationId: 'ff633f41-e560-4f32-8ba5-a09fcc9f8e6c', message: 'Fetching environment variable: OPENAI_API_KEY, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443101, correlationId: '3757433f-b009-4830-8d53-e8fb8327fda4', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '9cbfbce1-1e64-4d51-8a56-cf97716bcd88', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: 'f788e909-61a6-4b19-98d4-a88e7c0b8eab', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '375c7b8e-6ddc-45e1-993f-e674aaa681e8', message: 'OpenAIModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '8b053428-d7a1-4176-a6d3-cf285bcd56b9', message: 'ThrottlerModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: 'b1889468-4aa5-41c2-8999-5ba3463e05a2', message: 'ConfigHostModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: 'bfe4b4c6-0cf5-44a1-9f59-d980650498d0', message: 'HttpModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: 'f93ba22b-1aa9-4425-9278-47bfb2480feb', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '3ab7101a-0037-45c3-9abd-5081615ace42', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '57a80d83-efed-4c76-b460-dfad13a1af4b', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '99af6f7f-d4bc-4189-b91a-6fc2639572ff', message: 'DiscoveryModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443102, correlationId: '9341e489-b970-4304-8e08-3d9ae92e76a0', message: 'RobotsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: 'f51621ba-6137-4756-a23d-14f2d3873e8a', message: 'ConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: 'a6abb897-253a-49e5-877a-e475ecd42462', message: 'ScheduleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: '174d6f13-0532-40c4-8ac3-e2c20d66207f', message: 'TerminusModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: 'c562cd60-872f-4287-a7f2-cd46da1a042d', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: 'd6db2b3e-e452-44cc-af5f-938f2671e9eb', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443103, correlationId: '1745c3ed-d572-4442-bace-692ba4099452', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443111, correlationId: 'd4333187-88bb-49c1-a70f-d7bcec9ba44a', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443111, correlationId: 'a1d79146-766b-4a09-8033-3456ac79e4bd', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443111, correlationId: '009c31bf-dbe5-4170-b800-3bca646612a0', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443122, correlationId: 'fd2987d3-6e8e-4201-89e3-737c621bd8e8', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443123, correlationId: '873f49ec-60ea-40e9-a164-132a7953f570', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443123, correlationId: '11abac81-bd15-4635-acb2-28d96ab47677', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443123, correlationId: '47409697-ff01-4534-bfc1-a9b58777e02c', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443123, correlationId: '2b34964a-6349-4f2c-ac66-99e28847f0f5', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443128, correlationId: '119c6a52-9bc3-4491-a38d-14b41828b8bc', message: 'EnvConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443128, correlationId: 'd611556f-308f-4b42-a1f8-05db4feb9d3e', message: 'AppModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: '7b325eee-afed-441e-b83f-4380911f0945', message: 'ProductHydrationModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: 'e6aae289-8267-413b-bb52-b343b385811a', message: 'DBModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: '5d82e09b-4b0d-4c04-bdb3-89bd5fb9d6a4', message: 'NewrelicModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: 'c1ff0d5a-3a7d-4a40-9052-8b52786e6796', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: '2da08772-a19a-44b0-b41e-23b228717a97', message: 'Fetching environment variable: MMS_INTERNAL_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: 'a807cd94-c0d7-4188-b0f2-93c28e8c106e', message: 'Fetching environment variable: CI_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: 'f4d1488f-e59f-462b-8443-1fb6ac3235bd', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443129, correlationId: '0d924cb2-7252-4862-aab4-b99c5cf37187', message: 'OpensearchModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: '88ced594-baee-4055-b1df-9ca21ab2408b', message: 'MetricsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'efce2395-6253-4307-ad09-da25b9f6c22d', message: 'MmsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: '0403f2f4-cad4-4a74-9ab6-f90a86cc7da3', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'e238467d-d0be-428d-866c-8637c8082a8f', message: 'PromosModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: '13ad38b4-9667-4e7e-9e64-b8d49bd0026d', message: 'FrequentlyBoughtTogetherModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: '4578173f-00bc-4b19-8482-41c75a1c9c27', message: 'Fetching environment variable: MMS_IMAGES_LAMBDA_HOST, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'efefa675-d670-4800-b0b1-3b5484293404', message: 'AlgoliaModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'c9e006a6-9efc-4a4b-a639-4c8c8a8036bc', message: 'PromotionalProductsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: '2f5a9923-ece5-4127-b6ce-17befdde644d', message: 'TrendingProductsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'f64817a1-f1cf-4152-8b43-a0ce0235ba63', message: 'NeuralSearchModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'f5c9540b-322b-4913-886c-0ebe23db78e3', message: 'Fetching environment variable: AWS_SQS_QUEUE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443130, correlationId: 'd6b2e3dc-e796-4696-899d-887829ec74e7', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: 'cc68dda2-4aca-430b-ae48-dad7b51ff6e3', message: 'ProcessStyleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: 'e80b0b91-3b87-48e2-8295-046c309f8015', message: 'AddonsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: 'a455fe19-337a-4fc6-bc1c-1c842c18579f', message: 'HealthModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: '591e7358-f918-40e8-b23a-ee83fcef7415', message: 'MmsStylesSyncModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: 'a3b8f29c-7be5-4fa3-b657-aa9d24e14095', message: 'EmailRecommendationsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443132, correlationId: 'a37bd5ea-04d6-4734-a614-2233b19ae01d', message: 'RelatedProductsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 58920, timestamp: 1775820443179, correlationId: '09d7959e-a610-43b0-9602-6b4d8930a546', message: '[Main file] Application is running on 9009 port' }
{ level: 'log', pid: 58920, timestamp: 1775820443181, correlationId: 'e6c180de-4aa9-4002-be84-f98d1914023d', message: 'HealthController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443182, correlationId: '07248628-bcd0-4f0e-b736-e9d21c635922', message: 'Mapped {/is_it_up, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443182, correlationId: '94d41912-d600-41f7-800a-8b745848b71c', message: 'Mapped {/is_it_working, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '4bf42fe1-11c7-4832-a1e1-0594b6134afa', message: 'RelatedProductsController {/api/v1/related-products}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: 'e0ccea0e-d285-4255-b450-be21a984b541', message: 'Mapped {/api/v1/related-products/brand, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '43edc655-7d72-488b-b3bf-df8397b07871', message: 'Mapped {/api/v1/related-products/:productId, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '27569bcd-acfc-4bc5-9643-4b00879d73f5', message: 'FrequentlyBoughtTogetherController {/api/v1/frequently-bought-together}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '2c4fd720-fd7c-451f-ad1c-a5c01d766a09', message: 'Mapped {/api/v1/frequently-bought-together, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '11defa43-2b2f-4e9c-bd50-7250a7c5c4d4', message: 'Mapped {/api/v1/frequently-bought-together/root-categories, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '64864fbb-9f4f-4cb1-b29c-dd1b2ee59c6c', message: 'EmailRecommendationsController {/api/v1/email-recommendations}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '424c7c58-df1e-40cd-85fc-b51099e7fae3', message: 'Mapped {/api/v1/email-recommendations, POST} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443183, correlationId: '9569bdae-5716-4e15-946d-743ecf93704b', message: 'TrendingProductsDashboardController {/api/v1/trending-products}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '66b54b2a-0baa-4a27-b6bb-1cf94b50c6ab', message: 'Mapped {/api/v1/trending-products/dashboard, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '54491821-2313-4692-9399-4617295eb300', message: 'Mapped {/api/v1/trending-products/by-category, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: 'a38c8869-9f2d-41ca-93ec-b3b77698609b', message: 'RobotsController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '8a3037ae-64b1-492a-a9f2-536579ce33f0', message: 'Mapped {/robots.txt, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '0d0b5924-9a4a-4e97-96ea-e53779488143', message: 'PromotionalProductsController {/api/v1/promotional-products}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '78ec82fe-ae9a-4ca7-af96-4834808430f1', message: 'Mapped {/api/v1/promotional-products, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '39521427-67ce-470c-bbbd-19b27c936712', message: 'PromosController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: 'ef881bd8-8510-4294-9aa2-a22663e61f27', message: 'Mapped {/api/v1/hat-promo, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: 'fe91affa-073f-4ddb-b712-7dfce4a4483b', message: 'Mapped {/api/v1/sweats-promo, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '961f0ae8-458b-4e83-a888-1f0ee4dfd025', message: 'AddonsController {/api/v1/addons}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: 'b575d6d0-fc9a-432b-8765-5e41bcdc796f', message: 'Mapped {/api/v1/addons/curated, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443184, correlationId: '32a7c6ae-36dc-4c70-9cfa-c08786596522', message: 'NeuralSearchController {/api/v1/neural-search}:', context: 'RoutesResolver' }
{ level: 'log', pid: 58920, timestamp: 1775820443185, correlationId: '5f36b88c-2b5b-49b0-b6ec-31355f58d70a', message: 'Mapped {/api/v1/neural-search, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443185, correlationId: '66259fad-bbc3-4ff8-a2f7-3bf9e50bd108', message: 'Mapped {/api/v1/neural-search/use-case/:useCase, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443185, correlationId: 'd63e466d-11ab-4d1e-b257-e70167300905', message: 'Mapped {/api/v1/neural-search/view, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 58920, timestamp: 1775820443187, correlationId: '4d8aa546-07b9-4454-be27-990f9e6bab91', message: 'Initializing Algolia client...', context: 'AlgoliaService' }
{ level: 'log', pid: 58920, timestamp: 1775820443187, correlationId: '5806c1e8-01c3-42b7-92ac-f9ff1956ef12', message: 'Fetching environment variable: ALG_APP_ID, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443187, correlationId: '1d111060-ab83-48da-a3f8-3b0470b41aa7', message: 'Fetching environment variable: ALG_API_KEY, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443187, correlationId: 'dce090aa-a008-4c1d-ae6f-91a6c231d4bc', message: 'Fetching environment variable: ALG_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443188, correlationId: '1cfd2a83-1561-45be-b6ef-693938e7eca0', message: 'Algolia client initialized successfully', context: 'AlgoliaService' }
{ level: 'log', pid: 58920, timestamp: 1775820443188, correlationId: '2a52c689-681a-4d1e-b084-60890afd6abd', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443188, correlationId: '3e14a94c-c240-440f-a903-38ff42a61401', message: 'Fetching environment variable: OPENSEARCH_HOST, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443188, correlationId: 'b3fdd040-66e0-4300-beed-18c152fa5b9f', message: 'Fetching environment variable: OPENSEARCH_USERNAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443188, correlationId: '2c96c90a-84ae-435a-af2d-ad66ff7d0c16', message: 'Fetching environment variable: OPENSEARCH_PASSWORD, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443286, correlationId: 'ff92e0fd-ceb3-427f-a386-79cc5db44d3c', message: 'OpenSearch client initialized successfully. Host: http://localhost:9201', context: 'OpensearchService' }
{ level: 'log', pid: 58920, timestamp: 1775820443286, correlationId: '2f27a367-89a7-4c6d-b79b-b9e638c1c0f5', message: 'Fetching environment variable: OPENSEARCH_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443286, correlationId: '1677403e-50c9-41df-8ee0-7cb4c1747f1d', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupName":"neural-search-model-group"}],"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:27:23.286Z"}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'log', pid: 58920, timestamp: 1775820443286, correlationId: '6778a1ea-43aa-4ac6-9bbc-c8ec64379fcb', message: '[LogExecution]: Method invoked with parameters, {"params":[{"name":"neural-search-model-group"}],"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:27:23.286Z"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 58920, timestamp: 1775820443314, correlationId: '05623efc-3ddd-46c0-9b26-46f8b5110f5c', message: 'Read replica connection restored', context: 'CacheService' }
{ level: 'log', pid: 58920, timestamp: 1775820443324, correlationId: 'f1f5f311-07cb-47f8-a55a-1bcf307abd7f', message: '[LogExecution]:Method completed in 37.76ms. Result: {"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:27:23.286Z","executionTimeMs":37.76083299999982,"response":"7cXMoJwBx1UzTzWJUDT9"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 58920, timestamp: 1775820443324, correlationId: '52326ee2-6e04-4d0a-81ce-d73d33872938', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupId":"7cXMoJwBx1UzTzWJUDT9"}],"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:27:23.324Z"}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 58920, timestamp: 1775820443332, correlationId: '56e47104-9398-48ea-bd56-b87d0afe99a8', message: '[LogExecution]:Method completed in 7.90ms. Result: {"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:27:23.324Z","executionTimeMs":7.904875000000175,"response":[{"model_id":"78XMoJwBx1UzTzWJVTQ1","model_state":"DEPLOY_FAILED"},{"model_id":"5WyGAZ0Bc-LbwYBiF2Cm","model_state":"DEPLOY_FAILED"}]}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 58920, timestamp: 1775820443332, correlationId: 'cdfaf2c6-305c-425f-a475-b36f1b302043', message: '[LogExecution]:Method completed in 45.92ms. Result: {"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:27:23.286Z","executionTimeMs":45.91783299999997,"response":null}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'warn', pid: 58920, timestamp: 1775820443332, correlationId: 'd126b5c8-5243-43ce-96d5-f0afbe15c47e', message: 'No deployed model found. Neural search will not work until bootstrap is run.', context: 'OpensearchNeuralService' }
{ level: 'log', pid: 58920, timestamp: 1775820443332, correlationId: '1eeabe5e-2fa8-44b3-ae84-41851ca5d2db', message: 'Attempting auto-redeploy of neural search model...', context: 'OpensearchNeuralService' }
{ level: 'log', pid: 58920, timestamp: 1775820443332, correlationId: '6bcda562-43c4-477c-bdaf-755eddf2e0c7', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupName":"neural-search-model-group"}],"className":"OpensearchService","methodName":"redeployRegisteredModel","timestamp":"2026-04-10T11:27:23.332Z"}', context: 'OpensearchService.redeployRegisteredModel' }
{ level: 'log', pid: 58920, timestamp: 1775820443332, correlationId: '5b4c5da8-41f0-4638-a0e6-51081602fdeb', message: '[LogExecution]: Method invoked with parameters, {"params":[{"name":"neural-search-model-group"}],"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:27:23.332Z"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 58920, timestamp: 1775820443341, correlationId: '6efc033a-1da1-438d-a9f6-655743900a04', message: '[LogExecution]:Method completed in 8.98ms. Result: {"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:27:23.332Z","executionTimeMs":8.98216699999989,"response":"7cXMoJwBx1UzTzWJUDT9"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 58920, timestamp: 1775820443341, correlationId: 'b9384fd8-fa4a-4477-879d-e48d982bc0c9', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupId":"7cXMoJwBx1UzTzWJUDT9"}],"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:27:23.341Z"}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 58920, timestamp: 1775820443345, correlationId: '46ec7228-f2ba-478d-ba14-79dc759d33d6', message: '[LogExecution]:Method completed in 3.17ms. Result: {"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:27:23.341Z","executionTimeMs":3.1707920000001195,"response":[{"model_id":"78XMoJwBx1UzTzWJVTQ1","model_state":"DEPLOY_FAILED"},{"model_id":"5WyGAZ0Bc-LbwYBiF2Cm","model_state":"DEPLOY_FAILED"}]}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 58920, timestamp: 1775820443345, correlationId: '2f1aa140-aa99-443f-8bce-082b202d2ba4', message: '[LogExecution]:Method completed in 12.41ms. Result: {"className":"OpensearchService","methodName":"redeployRegisteredModel","timestamp":"2026-04-10T11:27:23.332Z","executionTimeMs":12.411875000000009,"response":null}', context: 'OpensearchService.redeployRegisteredModel' }
{ level: 'warn', pid: 58920, timestamp: 1775820443345, correlationId: '31d16beb-36c0-44f6-bb2d-388ee0729ab4', message: 'No registered model found for auto-redeploy. Run: npm run cli:dev -- bootstrap-neural-search', context: 'OpensearchNeuralService' }
{ level: 'log', pid: 58920, timestamp: 1775820443345, correlationId: 'a4219742-8107-46c9-963b-21b210935f10', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443345, correlationId: 'd0f33be4-72f2-4dc7-900e-a2a4a742849e', message: 'Robots.txt content loaded from /Users/4thwithme/Documents/repo/recommendations-service/src/assets/robots.txt', context: 'RobotsController' }
{ level: 'log', pid: 58920, timestamp: 1775820443346, correlationId: '9d6dc9ae-71bf-4610-aac2-a2bfebdcca48', message: 'Fetching environment variable: CURATED_ADDONS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 58920, timestamp: 1775820443346, correlationId: '8bd4f822-7ba5-42fc-9331-d24952e4fd56', message: 'Skipping SQS consumer, development mode', context: 'MmsStylesSyncService' }
{ level: 'log', pid: 58920, timestamp: 1775820443346, correlationId: '015d334b-4b5c-429a-b700-7865de57ffda', message: 'Nest application successfully started', context: 'NestApplication' }
{ level: 'log', pid: 58920, timestamp: 1775820463105, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: `[LogExecution]: Method invoked with parameters, {"params":{"q":"I'm looking for a MagSafe power bank for iphone","limit":12},"className":"NeuralSearchController","methodName":"search","timestamp":"2026-04-10T11:27:43.105Z"}`, context: 'NeuralSearchController.search' }
{ level: 'log', pid: 58920, timestamp: 1775820463105, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: '[LogExecution]: Method invoked with parameters, {"params":{},"className":"NeuralSearchService","methodName":"search","timestamp":"2026-04-10T11:27:43.105Z"}', context: 'NeuralSearchService.search' }
{ level: 'log', pid: 58920, timestamp: 1775820463106, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: `[LogExecution]: Method invoked with parameters, {"params":{"queryText":"I'm looking for a MagSafe power bank for iphone","size":12},"className":"OpensearchNeuralService","methodName":"searchProducts","timestamp":"2026-04-10T11:27:43.106Z"}`, context: 'OpensearchNeuralService.searchProducts' }
{ level: 'error', pid: 58920, timestamp: 1775820463117, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: '[LogExecution]: Method failed after 10.60ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"OpensearchNeuralService","methodName":"searchProducts","timestamp":"2026-04-10T11:27:43.116Z","executionTimeMs":10.59874999999738,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10232:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10626:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19956:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19840:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'OpensearchNeuralService.searchProducts' }
{ level: 'error', pid: 58920, timestamp: 1775820463123, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: '[LogExecution]: Method failed after 17.48ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"NeuralSearchService","methodName":"search","timestamp":"2026-04-10T11:27:43.123Z","executionTimeMs":17.480875000001106,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10232:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10626:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19956:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19840:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'NeuralSearchService.search' }
{ level: 'error', pid: 58920, timestamp: 1775820463123, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: '[LogExecution]: Method failed after 18.20ms: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search, errorLogContext: {"className":"NeuralSearchController","methodName":"search","timestamp":"2026-04-10T11:27:43.123Z","executionTimeMs":18.19695800000045,"error":{"message":"Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search","stack":"Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search\\n    at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10232:19)\\n    at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10626:56)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19956:61)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19840:41)\\n    at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)\\n    at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29\\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\\n    at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28","name":"Error"}}', context: 'NeuralSearchController.search' }
{ level: 'error', pid: 58920, timestamp: 1775820463125, correlationId: '8cd5faf6-65c8-4946-a196-509963545e14', message: Error: Neural search model not available. Run: npm run cli:dev -- bootstrap-neural-search
       at OpensearchNeuralService.getModelId (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10232:19)
       at OpensearchNeuralService.searchProducts (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:10626:56)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at NeuralSearchService.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19956:61)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at NeuralSearchController.search (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:19840:41)
       at descriptor.value (/Users/4thwithme/Documents/repo/recommendations-service/dist/main.js:2333:53)
       at /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:38:29
       at process.processTicksAndRejections (node:internal/process/task_queues:103:5)
       at async /Users/4thwithme/Documents/repo/recommendations-service/node_modules/@nestjs/core/router/router-execution-context.js:46:28, context: 'ExceptionsHandler' }

> AGENT

Both models are `DEPLOY_FAILED`, not `REGISTERED` or `UNDEPLOYED`. My filter missed that state.

```
"response":[{"model_id":"78XMoJwBx1UzTzWJVTQ1","model_state":"DEPLOY_FAILED"},{"model_id":"5WyGAZ0Bc-LbwYBiF2Cm","model_state":"DEPLOY_FAILED"}]
```

> AGENT

That said — `DEPLOY_FAILED` means the model couldn't load into memory last time. Re-deploying might fail again if the root cause persists (usually insufficient JVM heap). Check your OpenSearch container's `OPENSEARCH_JAVA_OPTS`. The docker-compose config allocates `-Xms2g -Xmx2g` — if that's not enough for the model, you might need to bump it or run `bootstrap-neural-search --cleanup` to clear the stale models and start fresh with one.

Restart your dev server and see if the redeploy succeeds now.

> DEVELOPER

  ~/Doc/r/recommendations-service   RECO-000-neural-search wip *18 !3 ?1 ❯ npm run cli:dev bootstrap-neural-search --cleanup                                                            ✘ INT  2m 8s   13:29:25
npm warn Unknown cli config "--cleanup". This will stop working in the next major version of npm.

> recommendations-service@0.0.1 cli:dev
> ts-node --log-error -r tsconfig-paths/register src/cli.ts bootstrap-neural-search

[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:35 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL_READ_REPLICA, converter: String
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: REDSHIFT_READ_URL, converter: String
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: SERVER_NAME, converter: none
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: IS_COMPACT_LOGS, converter: Boolean
[Nest] 60028  - 04/10/2026, 1:29:36 PM     LOG [EnvConfigService] Fetching environment variable: IS_JSON_LIKE_LOGS, converter: Boolean
{ level: 'log', pid: 60028, timestamp: 1775820576223, correlationId: 'ed906e20-6ca7-4888-a8bf-3ad8b98eeb81', message: 'Starting Nest application...', context: 'NestFactory' }
{ level: 'log', pid: 60028, timestamp: 1775820576274, correlationId: '5cb0fc92-bedb-40fb-a36c-b4e94b8ca1d9', message: 'Fetching environment variable: OPENAI_API_KEY, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '3672acbf-5b07-4106-8d0b-d503f28e1215', message: 'CommandRootModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '515d9f67-df4f-4881-82c7-65d235020b98', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '8b2a048f-eed7-41b4-8a9d-215c7aa3be3a', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '2cf9448e-8602-4216-ab3d-fb1def55ac29', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '0763c29d-1211-46ac-b203-a62cc36dd37d', message: 'OpenAIModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'a6929afd-3fb0-4d0c-a4a3-c10f36cd7190', message: 'ConfigHostModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'c736349f-3e1d-4cfe-bac4-8a2c85aa4a88', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'ee4af54a-9dd5-41ca-a5e4-799816114b8f', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'e52767cf-d710-4e9b-b214-fbb89d50e1a3', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'cd3b3d3b-0303-476a-8997-8675b10ccc47', message: 'HttpModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'fc4e9c20-d38a-4a45-9724-36704d9b2ab1', message: 'DiscoveryModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'a578369f-e4a1-4851-bb6c-af92e52c2f6e', message: 'DiscoveryModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: '3711ce8e-afb1-4fa9-81f3-495fd6fa399e', message: 'ConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576276, correlationId: 'd35e91a7-b493-4ef9-b2d7-8aa4e5619aca', message: 'ScheduleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576277, correlationId: 'f1c267f4-8db9-42ba-a52e-33449d2e1cc4', message: 'CommandRunnerModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576277, correlationId: '1e3c5331-d624-4d47-a4c1-0816d628cc5d', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576277, correlationId: '54110fe1-4f9b-4d87-a879-cee0758b0ca9', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576277, correlationId: '4a0f6c2b-2fd6-4c5a-9ac0-43e17d8d48f3', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576284, correlationId: 'e7f945d4-bf02-482a-84dc-5ede84f7d556', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576284, correlationId: '41499be6-08c6-4e05-b68a-ad9b454680b8', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576284, correlationId: 'be63cdff-917a-4dde-a5c6-b8f79dd39139', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576288, correlationId: 'b638bc8d-a88b-4742-af29-acfd16fa83bb', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576289, correlationId: 'b09833fc-0b43-432b-9500-78d99ae919ca', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576289, correlationId: '975f69ff-3125-4378-a36d-7808dd7b9e27', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576289, correlationId: 'eede60ac-f7d1-4cc5-8ba4-5a0c7985d781', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576289, correlationId: '52756f93-a66f-4f4b-af7a-5bf82225fa89', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576293, correlationId: 'e2785c63-58b7-428d-b2af-74127b88edcc', message: 'Fetching environment variable: MMS_INTERNAL_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576293, correlationId: '10fe356d-cd09-4096-98a2-6bba5ebde2ff', message: 'EnvConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '120ae03e-2d41-4887-953c-e069df2a188d', message: 'ProductHydrationModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '7206ff97-9373-4477-8f21-58ad2d467bdb', message: 'DBModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: 'f91ba65a-b047-4dc9-a22d-45a16c992bc9', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }                                                                                                                                                                                                           { level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '82628bdb-f04e-4f09-aca6-52fc5351b5bb', message: 'Fetching environment variable: MMS_INTERNAL_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: 'e0b797e6-f651-4899-a672-5be48e6b738b', message: 'Fetching environment variable: CI_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '6f8b5dc9-ed8b-4085-bb4b-168f7077b9de', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '55b056ad-1426-4548-a32e-6e6ab0018dc6', message: 'OpensearchModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '4c263915-3478-4cd7-b66a-e6a8bf51f808', message: 'MetricsModule dependencies initialized', context: 'InstanceLoader' }                            { level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: 'cdfe2caf-c291-4121-89b6-8de4f464ce15', message: 'MmsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '502dd48d-053f-48ae-8329-bd38fa5d609b', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: '1ee0a0f8-02b5-4d34-87fd-dd598b5310b3', message: 'Fetching environment variable: MMS_IMAGES_LAMBDA_HOST, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576294, correlationId: 'dcd3b1be-9b67-4136-ba43-45e3c65f2137', message: 'Fetching environment variable: MMS_INTERNAL_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576295, correlationId: 'e0da1e68-3182-422a-8450-789f062b497d', message: 'AlgoliaModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576295, correlationId: 'a2761714-13f3-4bdb-90ad-158e39fab8cf', message: 'TrendingProductsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576295, correlationId: '3a178f4b-f853-4af3-9901-98d8df3bb59c', message: 'Fetching environment variable: AWS_SQS_QUEUE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576295, correlationId: '88df7ed1-51ad-4dc6-bad3-18f5978a6c8e', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576296, correlationId: '253c5038-be9b-4627-b798-83700801abc2', message: 'ProcessStyleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576296, correlationId: '6aa48d0a-f8a7-4a61-a70c-284eee48a8d3', message: 'CliModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576296, correlationId: 'c805cae3-70df-48c2-bbe3-c89be05122d9', message: 'MmsStylesSyncModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60028, timestamp: 1775820576300, correlationId: '0b334b7b-4b2d-48a1-82ef-5393ca660e8b', message: 'Initializing Algolia client...', context: 'AlgoliaService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '6809c08d-122e-467c-b54b-6c54c3fbbace', message: 'Fetching environment variable: ALG_APP_ID, converter: none', context: 'EnvConfigService' }      { level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: 'f4c7e0af-d34a-4d07-8eef-c26bcde9bb2e', message: 'Fetching environment variable: ALG_API_KEY, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: 'e42426ce-7b9e-4cfc-9fad-b4a84d282506', message: 'Fetching environment variable: ALG_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '5a8ce077-d5f4-4417-8dc2-8c82b22d7c48', message: 'Algolia client initialized successfully', context: 'AlgoliaService' }                           { level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '19337fcd-aacb-4d5f-9a98-63215b5d1fe9', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '4a8d8d00-427b-4360-ae30-be3512d91cf0', message: 'Fetching environment variable: OPENSEARCH_HOST, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '2e4b6d87-ffd2-470f-a00c-dac6612fbc1c', message: 'Fetching environment variable: OPENSEARCH_USERNAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576301, correlationId: '9c2cbf0e-de0d-4a40-94c2-a46de2120df2', message: 'Fetching environment variable: OPENSEARCH_PASSWORD, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576391, correlationId: 'a2aa8d49-c18c-410b-b030-692dfe6ae048', message: 'OpenSearch client initialized successfully. Host: http://localhost:9201', context: 'OpensearchService' }
{ level: 'log', pid: 60028, timestamp: 1775820576391, correlationId: '07a8a4f8-1cdc-41a2-a455-eeeb60913412', message: 'Fetching environment variable: OPENSEARCH_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576392, correlationId: '4f0220ed-dc3e-4c38-9553-03a6d5d57082', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupName":"neural-search-model-group"}],"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:29:36.392Z"}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'log', pid: 60028, timestamp: 1775820576392, correlationId: '7aa50fb5-9692-4916-80f6-fba018de62c3', message: '[LogExecution]: Method invoked with parameters, {"params":[{"name":"neural-search-model-group"}],"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:29:36.392Z"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 60028, timestamp: 1775820576404, correlationId: 'cbefbb70-4f04-4db8-9e70-37a620fe4fc4', message: 'Read replica connection restored', context: 'CacheService' }
{ level: 'log', pid: 60028, timestamp: 1775820576411, correlationId: '26cb4a6b-4c93-462e-8a71-7a6295879f4c', message: '[LogExecution]:Method completed in 19.68ms. Result: {"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:29:36.392Z","executionTimeMs":19.682000000000244,"response":"7cXMoJwBx1UzTzWJUDT9"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 60028, timestamp: 1775820576412, correlationId: 'd2643d32-2106-443a-b601-b469c4f0f57b', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupId":"7cXMoJwBx1UzTzWJUDT9"}],"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:29:36.412Z"}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 60028, timestamp: 1775820576417, correlationId: '3f27a384-3ded-42db-8908-59fc5b3bc205', message: '[LogExecution]:Method completed in 5.56ms. Result: {"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:29:36.412Z","executionTimeMs":5.556374999999662,"response":[{"model_id":"5WyGAZ0Bc-LbwYBiF2Cm","model_state":"DEPLOY_FAILED"},{"model_id":"78XMoJwBx1UzTzWJVTQ1","model_state":"DEPLOYED"}]}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 60028, timestamp: 1775820576417, correlationId: '015c6318-a652-432a-b198-b4d495e4ba1d', message: '[LogExecution]:Method completed in 25.67ms. Result: {"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:29:36.392Z","executionTimeMs":25.6748749999997,"response":"78XMoJwBx1UzTzWJVTQ1"}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'log', pid: 60028, timestamp: 1775820576417, correlationId: 'a882bed8-0978-4c0e-bc6d-f04dc39c908f', message: 'Model ID updated: none -> 78XMoJwBx1UzTzWJVTQ1', context: 'OpensearchNeuralService' }
{ level: 'log', pid: 60028, timestamp: 1775820576418, correlationId: '790984db-dae2-4748-8724-cfc96b31226f', message: 'Skipping SQS consumer, development mode', context: 'MmsStylesSyncService' }
{ level: 'log', pid: 60028, timestamp: 1775820576418, correlationId: 'e1a44341-8b07-429e-b084-773403844ecb', message: '[CLI file] Executing CLI application' }
{ level: 'log', pid: 60028, timestamp: 1775820576419, correlationId: 'e84a7b26-54bb-4f18-ae09-1d3cd4fcad61', message: 'Starting bootstrap-neural-search', context: 'BootstrapNeuralSearchCommand' }
{ level: 'log', pid: 60028, timestamp: 1775820576422, correlationId: '9d47b649-d988-4fe9-8e3f-66dd7681693e', message: 'Fetching environment variable: OPENSEARCH_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60028, timestamp: 1775820576422, correlationId: '5a4a9a77-7d00-4453-9b63-94d541480125', message: '=== Step 1/8: Configuring cluster ML settings ===', context: 'BootstrapNeuralSearchCommand' }
{ level: 'log', pid: 60028, timestamp: 1775820576422, correlationId: 'c7255793-e059-4b57-93a6-38815475da49', message: '[LogExecution]: Method invoked with parameters, {"params":[],"className":"OpensearchService","methodName":"configureClusterMLSettings","timestamp":"2026-04-10T11:29:36.422Z"}', context: 'OpensearchService.configureClusterMLSettings' }
{ level: 'log', pid: 60028, timestamp: 1775820576458, correlationId: '28ecbbc5-f996-4816-9c2a-c81cf2279ae4', message: 'Configured ML cluster settings', context: 'OpensearchService' }
{ level: 'log', pid: 60028, timestamp: 1775820576458, correlationId: 'b9f6c9d4-ffeb-4950-91f6-a139a9813775', message: '[LogExecution]:Method completed in 35.47ms. Result: {"className":"OpensearchService","methodName":"configureClusterMLSettings","timestamp":"2026-04-10T11:29:36.422Z","executionTimeMs":35.46916599999986}', context: 'OpensearchService.configureClusterMLSettings' }
{ level: 'log', pid: 60028, timestamp: 1775820576458, correlationId: '759906be-e616-434f-9ef2-eedd0b8b445c', message: '=== Step 2/8: Registering model group ===', context: 'BootstrapNeuralSearchCommand' }
{ level: 'log', pid: 60028, timestamp: 1775820576458, correlationId: '8de902bc-4571-4a74-8deb-045dc3aabe26', message: '[LogExecution]: Method invoked with parameters, {"params":[{"name":"neural-search-model-group","description":"Model group for neural search embeddings"}],"className":"OpensearchService","methodName":"registerModelGroup","timestamp":"2026-04-10T11:29:36.458Z"}', context: 'OpensearchService.registerModelGroup' }
{ level: 'error', pid: 60028, timestamp: 1775820576476, correlationId: '2ac1ed83-6aeb-4974-8848-5645db46f272', message: 'Failed to register model group: illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9.', context: 'OpensearchService', stack: 'ResponseError: illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9.\n    at onBody (/Users/4thwithme/Documents/repo/recommendations-service/node_modules/@opensearch-project/opensearch/lib/Transport.js:426:23)\n    at IncomingMessage.onEnd (/Users/4thwithme/Documents/repo/recommendations-service/node_modules/@opensearch-project/opensearch/lib/Transport.js:341:11)\n    at IncomingMessage.emit (node:events:520:35)\n    at IncomingMessage.emit (node:domain:489:12)\n    at endReadableNT (node:internal/streams/readable:1701:12)\n    at processTicksAndRejections (node:internal/process/task_queues:89:21)' }
{ level: 'error', pid: 60028, timestamp: 1775820576476, correlationId: '7e7e3b91-d41d-4c1c-ab9b-598cc62063b7', message: '[LogExecution]: Method failed after 18.46ms: illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9., errorLogContext: {"className":"OpensearchService","methodName":"registerModelGroup","timestamp":"2026-04-10T11:29:36.476Z","executionTimeMs":18.46199999999999,"error":{"message":"illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9.","stack":"ResponseError: illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9.\\n    at onBody (/Users/4thwithme/Documents/repo/recommendations-service/node_modules/@opensearch-project/opensearch/lib/Transport.js:426:23)\\n    at IncomingMessage.onEnd (/Users/4thwithme/Documents/repo/recommendations-service/node_modules/@opensearch-project/opensearch/lib/Transport.js:341:11)\\n    at IncomingMessage.emit (node:events:520:35)\\n    at IncomingMessage.emit (node:domain:489:12)\\n    at endReadableNT (node:internal/streams/readable:1701:12)\\n    at processTicksAndRejections (node:internal/process/task_queues:89:21)","name":"ResponseError"}}', context: 'OpensearchService.registerModelGroup' }
{ level: 'error', pid: 60028, timestamp: 1775820576477, correlationId: '62e7164f-8d6e-48db-81a9-f3494576c9b7', message: 'Bootstrap failed: illegal_argument_exception: [illegal_argument_exception] Reason: The name you provided is already being used by a model group with ID: 7cXMoJwBx1UzTzWJUDT9.', context: 'BootstrapNeuralSearchCommand' }

> AGENT

Two things:

1. **Model is already deployed.** Look at the logs — `78XMoJwBx1UzTzWJVTQ1` is `DEPLOYED`. Just restart your dev server.

2. **`--cleanup` wasn't passed.** npm ate the flag. You need the `--` separator:
   ```bash
   npm run cli:dev -- bootstrap-neural-search --cleanup
   ```
   Not:
   ```bash
   npm run cli:dev bootstrap-neural-search --cleanup
   ```

Restart `npm run start:dev` and it should work — `findDeployedModelId` will pick up `78XMoJwBx1UzTzWJVTQ1`.

> DEVELOPER

  ~/Documents/repo/recommendations-service   RECO-000-neural-search wip *18 !3 ?1 ❯ npm run start:dev                                                                                           ✘ INT   13:30:26

> recommendations-service@0.0.1 start:dev
> nest start --watch --webpack --webpackPath webpack.config.js


 Info  Webpack is building your sources...

webpack 5.103.0 compiled successfully in 3327 ms
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL_READ_REPLICA, converter: String
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: DATABASE_URL, converter: String
[Nest] 60548  - 04/10/2026, 1:30:33 PM     LOG [EnvConfigService] Fetching environment variable: REDSHIFT_READ_URL, converter: String
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: GLOBAL_PREFIX, converter: none
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: PORT, converter: Number
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: NODE_ENV, converter: none
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: SERVER_NAME, converter: none
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: IS_COMPACT_LOGS, converter: Boolean
[Nest] 60548  - 04/10/2026, 1:30:34 PM     LOG [EnvConfigService] Fetching environment variable: IS_JSON_LIKE_LOGS, converter: Boolean
{ level: 'log', pid: 60548, timestamp: 1775820634413, correlationId: '7d8a33ef-7817-42f3-9516-ee57b08dfc90', message: 'Starting Nest application...', context: 'NestFactory' }
{ level: 'log', pid: 60548, timestamp: 1775820634461, correlationId: 'cf161fde-8d25-4830-83eb-cad3bf794bad', message: 'Fetching environment variable: OPENAI_API_KEY, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634462, correlationId: '45149112-15d7-47ab-8d7c-7da4088b3323', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634462, correlationId: '5c2a8125-374a-4a34-9ff0-af3094a3d44e', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634462, correlationId: 'f2829ce9-0519-40de-8ebb-f7c5c4146421', message: 'KnexModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634462, correlationId: '3a7f593e-7668-47aa-a8cb-d32a6fa457f5', message: 'OpenAIModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '298791df-77e0-4fde-bec9-74af56bfea55', message: 'ThrottlerModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '112b4d89-2f31-47c1-a987-42eb3ca6f515', message: 'ConfigHostModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: 'c8c8a2f1-cc9d-4b87-a9b0-ef83e2915f5f', message: 'HttpModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '05835acc-0174-42b7-9a38-37e026939c58', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '29f599a1-30cf-463c-9474-9a9bba107a01', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '2f300d84-d994-4d50-bead-25edcc24a797', message: 'KnexCoreModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: 'b0019295-b454-465b-9483-7841bf4c520b', message: 'DiscoveryModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '4180d3dc-f72d-48e6-a241-69ee47055038', message: 'RobotsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '346642f7-db0f-4c12-91d0-61db128a550c', message: 'ConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '268c1783-b7ae-4639-9883-70d439b35d62', message: 'ScheduleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: 'd9cc6f90-ad82-4510-bce8-01dda16e9325', message: 'TerminusModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '680025c2-4fba-45d4-8b2d-47a8ad5511ed', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '79ef502d-e67a-42d6-b1a9-d2611214c91d', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634463, correlationId: '928ed645-ec8b-4521-87f1-d501c3d0db27', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634469, correlationId: '19a1756a-3e32-441c-8762-002713a715b4', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634469, correlationId: '5784c62d-d1a0-4a73-b887-bb52a00891b4', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634469, correlationId: '54e21d95-c894-4cb9-80fd-888d92756c56', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634477, correlationId: '24fd15f8-8606-477d-9ca7-804f50c29803', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634478, correlationId: '86a6a74c-5feb-44f0-8a59-a69be6b9a3fd', message: 'Fetching environment variable: REDIS_READ_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634478, correlationId: '63feea87-171c-450e-9d30-05631b2bf71b', message: 'Fetching environment variable: SERVER_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634478, correlationId: 'b02802b5-7606-42cb-8d01-c68b04509d02', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634478, correlationId: '74b9f5a7-bceb-4cad-bd53-b11fa39215fa', message: 'Fetching environment variable: REDIS_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634483, correlationId: '0cdbd0c9-b828-47b6-a5c9-1cfd18703809', message: 'EnvConfigModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634483, correlationId: '83a1a3b7-2429-46ed-9b29-6e243dee8f3f', message: 'AppModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: 'c4f06ac9-5c09-41ce-8833-66629df261bd', message: 'ProductHydrationModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: '238f798a-d1d6-4d89-996c-804185dccb7c', message: 'DBModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: 'a1d84ef5-24e4-47c2-9ad8-51416e4f740d', message: 'NewrelicModule dependencies initialized', context: 'InstanceLoader' }                           { level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: '569e18d9-da80-49c8-817b-e4cfe8e21a0c', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }                                                                                                                                                                                                           { level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: 'ef6abb90-83d2-4595-9830-5003342678be', message: 'Fetching environment variable: MMS_INTERNAL_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: '48755ce4-c6dd-4721-afd7-0f54c1ad6375', message: 'Fetching environment variable: CI_BASE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: 'cf9adc4a-1d62-417a-8e7d-e72a8d7fa5d6', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634484, correlationId: 'd887a5ad-e2b4-411a-a72b-ab1defe9a014', message: 'OpensearchModule dependencies initialized', context: 'InstanceLoader' }                         { level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '75d88e27-ba4b-461b-a5b3-9982682973a4', message: 'MetricsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: 'e85db8a1-7a2e-49b7-a8bf-c3df02d787fd', message: 'MmsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '0d14acf4-5b4e-4cc0-964d-309105fc3d91', message: 'CacheModule dependencies initialized', context: 'InstanceLoader' }                              { level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: 'c992b236-9866-447d-a88c-849d49bcad55', message: 'PromosModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: 'fdd1ca96-a70c-4402-8d97-bde2d6671ce8', message: 'FrequentlyBoughtTogetherModule dependencies initialized', context: 'InstanceLoader' }           { level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '0d32a33b-c1c7-441a-b5db-2dda6420255d', message: 'Fetching environment variable: MMS_IMAGES_LAMBDA_HOST, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '2c89e1c8-81b9-48a1-8d18-ee1a1f8b15ef', message: 'AlgoliaModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '63076836-4958-4905-9a88-e9c561fa5262', message: 'PromotionalProductsModule dependencies initialized', context: 'InstanceLoader' }                { level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '2add3d08-d14a-4dab-9dfe-861bd6097da3', message: 'TrendingProductsModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '9914af89-8fc5-4bcd-acd2-b60ac1c5094b', message: 'NeuralSearchModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '75459855-2761-4e89-aef4-931e2d3a14c8', message: 'Fetching environment variable: AWS_SQS_QUEUE_URL, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634485, correlationId: '47dc13b4-673e-4222-9984-7bf313fc599f', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: 'fe76bbe6-a878-427d-bb96-d665fde8250c', message: 'ProcessStyleModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: '3a36d475-a136-4162-8942-e76b5cc92e0b', message: 'AddonsModule dependencies initialized', context: 'InstanceLoader' }                             { level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: '9c6f4ab0-f5bc-41d9-8b6b-754a113cacd4', message: 'HealthModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: 'e4a7aab1-d889-497d-9ce9-24484dc76d36', message: 'MmsStylesSyncModule dependencies initialized', context: 'InstanceLoader' }
{ level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: '5b1d1ecd-fd38-490d-9e85-60d5dba795b5', message: 'EmailRecommendationsModule dependencies initialized', context: 'InstanceLoader' }               { level: 'log', pid: 60548, timestamp: 1775820634487, correlationId: '6534750a-a12c-47f9-b9de-450e2d93445b', message: 'RelatedProductsModule dependencies initialized', context: 'InstanceLoader' }                    { level: 'log', pid: 60548, timestamp: 1775820634527, correlationId: '744fb644-f0cd-490c-9951-6d9d1da63b4a', message: '[Main file] Application is running on 9009 port' }
{ level: 'log', pid: 60548, timestamp: 1775820634532, correlationId: '167b85cd-f2a9-4b0b-95dd-2ec0b5e21fb7', message: 'HealthController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: 'a927c747-df20-44c6-9179-c58a9c797ab5', message: 'Mapped {/is_it_up, GET} route', context: 'RouterExplorer' }                                     { level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: 'f6ccba8f-0a31-457e-aa6e-5c0b02e6ca68', message: 'Mapped {/is_it_working, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: '04663a94-53d9-4684-876d-9a6ebb3036fd', message: 'RelatedProductsController {/api/v1/related-products}:', context: 'RoutesResolver' }             { level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: 'dae7e1e0-88aa-432b-8946-e07600d8e990', message: 'Mapped {/api/v1/related-products/brand, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: '5af0cb42-a3c2-4cc5-97f6-767da2dbf233', message: 'Mapped {/api/v1/related-products/:productId, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634533, correlationId: '4c73e021-8789-456d-ab76-8584f2e98154', message: 'FrequentlyBoughtTogetherController {/api/v1/frequently-bought-together}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '3b55a00b-ff11-4884-be2e-64297afd9eb6', message: 'Mapped {/api/v1/frequently-bought-together, GET} route', context: 'RouterExplorer' }            { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '3440488b-e6cd-4aa2-b9e0-0f0e1c3735d1', message: 'Mapped {/api/v1/frequently-bought-together/root-categories, GET} route', context: 'RouterExplorer' }                                                                                                                                                                                                                   { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '5cf6218c-3657-4bb3-84bb-3257a25be10b', message: 'EmailRecommendationsController {/api/v1/email-recommendations}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '82a42439-5100-4c7f-b668-9e5d7c248480', message: 'Mapped {/api/v1/email-recommendations, POST} route', context: 'RouterExplorer' }                { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '7e153760-d7af-4a84-bb0d-0a924d11c6e4', message: 'TrendingProductsDashboardController {/api/v1/trending-products}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '675c6431-e7af-4cd3-8fd5-072e58fda0ea', message: 'Mapped {/api/v1/trending-products/dashboard, GET} route', context: 'RouterExplorer' }           { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: 'e1f7b22e-2c1b-4c78-b9ca-2d8f0a1507c8', message: 'Mapped {/api/v1/trending-products/by-category, GET} route', context: 'RouterExplorer' }         { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '5f3c5a6f-99b3-4980-b424-7a40c92b1888', message: 'RobotsController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '97bfffc5-f425-4da9-9560-b356076b4756', message: 'Mapped {/robots.txt, GET} route', context: 'RouterExplorer' }                                   { level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '2ef8b757-e5da-4f2d-b1ea-eefb877545d8', message: 'PromotionalProductsController {/api/v1/promotional-products}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '5c987d0c-f239-4337-8aa6-183f528c0a3c', message: 'Mapped {/api/v1/promotional-products, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634534, correlationId: '96861c5b-8e9e-402c-9d6d-5d5ebce6663c', message: 'PromosController {/api/v1}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: '30048c4c-5f86-4974-a5b8-cb1ba689a934', message: 'Mapped {/api/v1/hat-promo, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: 'ff388dbc-7716-4564-80d8-53f67b140c9d', message: 'Mapped {/api/v1/sweats-promo, GET} route', context: 'RouterExplorer' }                          { level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: 'e14683ed-c47d-474b-893a-ef1fcbf3679c', message: 'AddonsController {/api/v1/addons}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: '91480d57-7ae0-4924-b155-d665f43f7307', message: 'Mapped {/api/v1/addons/curated, GET} route', context: 'RouterExplorer' }                        { level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: 'd35665d1-a20f-49a0-bcc6-51ac98c00a1d', message: 'NeuralSearchController {/api/v1/neural-search}:', context: 'RoutesResolver' }
{ level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: '78ba2be5-db80-469b-b10f-f1698ca61b60', message: 'Mapped {/api/v1/neural-search, GET} route', context: 'RouterExplorer' }                         { level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: '40989f99-1cee-41e6-9d86-1c5c6c95173f', message: 'Mapped {/api/v1/neural-search/use-case/:useCase, GET} route', context: 'RouterExplorer' }
{ level: 'log', pid: 60548, timestamp: 1775820634535, correlationId: '40fb2fd8-5866-46dd-818c-e1f708ae4b7a', message: 'Mapped {/api/v1/neural-search/view, GET} route', context: 'RouterExplorer' }                    { level: 'log', pid: 60548, timestamp: 1775820634537, correlationId: 'b1b030bc-85c3-484b-a427-2ed00edd9cd6', message: 'Initializing Algolia client...', context: 'AlgoliaService' }
{ level: 'log', pid: 60548, timestamp: 1775820634537, correlationId: '52739abd-a289-4a0d-b4c7-e9a5cc9e6ec3', message: 'Fetching environment variable: ALG_APP_ID, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634537, correlationId: '208b3372-3315-43e0-882c-fa1a9e8a2cf3', message: 'Fetching environment variable: ALG_API_KEY, converter: none', context: 'EnvConfigService' }     { level: 'log', pid: 60548, timestamp: 1775820634537, correlationId: 'e4270dd6-6028-4cbc-962c-9df176fdf565', message: 'Fetching environment variable: ALG_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634538, correlationId: '0afcbdc8-d256-4fc6-846c-ed241bd3368b', message: 'Algolia client initialized successfully', context: 'AlgoliaService' }                           { level: 'log', pid: 60548, timestamp: 1775820634538, correlationId: '345708c4-398a-4018-9229-ef431378ebc8', message: 'Fetching environment variable: RELATED_PRODUCTS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634538, correlationId: '0a41b144-5c7b-4873-8167-31ce00559fa6', message: 'Fetching environment variable: OPENSEARCH_HOST, converter: none', context: 'EnvConfigService' } { level: 'log', pid: 60548, timestamp: 1775820634538, correlationId: '90e4fb60-b1cd-41cd-83c2-eb5fc88569d7', message: 'Fetching environment variable: OPENSEARCH_USERNAME, converter: none', context: 'EnvConfigService' }                                                                                                                                                                                                                    { level: 'log', pid: 60548, timestamp: 1775820634538, correlationId: '5d43b520-38e2-421b-b56f-98fc6eecd801', message: 'Fetching environment variable: OPENSEARCH_PASSWORD, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634623, correlationId: '0ea7b116-6029-4a2a-bc7f-401be7e98a56', message: 'OpenSearch client initialized successfully. Host: http://localhost:9201', context: 'OpensearchService' }
{ level: 'log', pid: 60548, timestamp: 1775820634623, correlationId: 'd2b9479b-d622-4bfe-b130-238a55ba082a', message: 'Fetching environment variable: OPENSEARCH_INDEX_NAME, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634623, correlationId: '9865b3ae-36b3-4cb0-882c-a9788e71ea97', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupName":"neural-search-model-group"}],"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:30:34.623Z"}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'log', pid: 60548, timestamp: 1775820634623, correlationId: 'b070426f-4b9a-4aa0-964c-fa6d33e67b69', message: '[LogExecution]: Method invoked with parameters, {"params":[{"name":"neural-search-model-group"}],"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:30:34.623Z"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 60548, timestamp: 1775820634644, correlationId: 'd41c3860-edab-48d3-bad8-a7dafe870ee8', message: 'Read replica connection restored', context: 'CacheService' }                                    { level: 'log', pid: 60548, timestamp: 1775820634647, correlationId: '14473297-effc-4f83-98e3-cc7e1a0cb79b', message: '[LogExecution]:Method completed in 23.52ms. Result: {"className":"OpensearchService","methodName":"searchModelGroupByName","timestamp":"2026-04-10T11:30:34.623Z","executionTimeMs":23.524417000000085,"response":"7cXMoJwBx1UzTzWJUDT9"}', context: 'OpensearchService.searchModelGroupByName' }
{ level: 'log', pid: 60548, timestamp: 1775820634647, correlationId: '0d3e28d3-5ea2-42e0-866e-46ad5b641721', message: '[LogExecution]: Method invoked with parameters, {"params":[{"modelGroupId":"7cXMoJwBx1UzTzWJUDT9"}],"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:30:34.647Z"}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 60548, timestamp: 1775820634652, correlationId: 'b39e5a95-7b55-4171-a945-02582a094587', message: '[LogExecution]:Method completed in 4.92ms. Result: {"className":"OpensearchService","methodName":"searchModelsByGroup","timestamp":"2026-04-10T11:30:34.647Z","executionTimeMs":4.918791999999939,"response":[{"model_id":"5WyGAZ0Bc-LbwYBiF2Cm","model_state":"DEPLOY_FAILED"},{"model_id":"78XMoJwBx1UzTzWJVTQ1","model_state":"DEPLOYED"}]}', context: 'OpensearchService.searchModelsByGroup' }
{ level: 'log', pid: 60548, timestamp: 1775820634652, correlationId: '38a16d6b-7dce-40f5-9e9a-795a5de9ec2f', message: '[LogExecution]:Method completed in 28.69ms. Result: {"className":"OpensearchService","methodName":"findDeployedModelId","timestamp":"2026-04-10T11:30:34.623Z","executionTimeMs":28.68683299999998,"response":"78XMoJwBx1UzTzWJVTQ1"}', context: 'OpensearchService.findDeployedModelId' }
{ level: 'log', pid: 60548, timestamp: 1775820634652, correlationId: '50b2fc9a-1c44-4b09-b4b5-04ed3238e873', message: 'Model ID updated: none -> 78XMoJwBx1UzTzWJVTQ1', context: 'OpensearchNeuralService' }
{ level: 'log', pid: 60548, timestamp: 1775820634652, correlationId: 'd63dfad6-efeb-4020-ab50-a62d79cd7e6b', message: 'Fetching environment variable: NODE_ENV, converter: none', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634652, correlationId: '4d353f2e-21fc-45a7-a639-5ed5969f0361', message: 'Robots.txt content loaded from /Users/4thwithme/Documents/repo/recommendations-service/src/assets/robots.txt', context: 'RobotsController' }
{ level: 'log', pid: 60548, timestamp: 1775820634653, correlationId: '05212a80-7efe-4039-a743-355330283f26', message: 'Fetching environment variable: CURATED_ADDONS_CACHE_TTL, converter: Number', context: 'EnvConfigService' }
{ level: 'log', pid: 60548, timestamp: 1775820634653, correlationId: '6c385368-9bd0-483d-bf7d-a02075e2f477', message: 'Skipping SQS consumer, development mode', context: 'MmsStylesSyncService' }
{ level: 'log', pid: 60548, timestamp: 1775820634653, correlationId: '9ffe7572-a995-4535-b683-9d43dbb2d3be', message: 'Nest application successfully started', context: 'NestApplication' }

> AGENT

Model `78XMoJwBx1UzTzWJVTQ1` resolved on startup. No auto-redeploy needed — it was already `DEPLOYED`. Neural search should work now.

> DEVELOPER

how to test it

> AGENT

```
curl "http://localhost:9009/api/v1/neural-search?q=MagSafe+power+bank+for+iphone&limit=5"
```

Or open in browser:

```
http://localhost:9009/api/v1/neural-search/view?q=MagSafe+power+bank+for+iphone&limit=5
```
