> DEVELOPER

Hello, making sure we are connected before the task. A short yes works.

> AGENT

Yes.

> DEVELOPER

Read the full megaplan phase prompt from this file and follow it exactly: /Users/user_c042661f/Documents/Veas/.megaplan/plans/hector-commitments-sprint/plan_shannon_prompt.txt. Your final response must satisfy the structured output contract in that file. Do not summarize the file; execute its instructions.

> AGENT

{"plan":"# Implementation Plan: Hector Fitness Bot — Commitments, Events, Adherence\n\n## Overview\nAdd Hector as a solo fitness bot (`bot_id='hector'`, primary topic `fitness`) following the existing Tante Rosi pattern. Introduce two generic, bot/topic-scoped tables — `commitments` and `events` — with Hector-only tool exposure in v1. Compute and render an adherence checklist in `hot_context_solo` for Hector. Add persona + prompt module, registry gate, tool allowlist, and focused tests/evals for commitments, events, adherence state computation, hot-context rendering, scope, allowlist, and prompt behavior. Preserve existing user changes (`.env.example`, `app/config.py`, `app/services/agentic.py`, `tests/test_config.py`, `tests/test_llm_phase.py`, `app/services/deepseek.py`) and avoid unrelated refactors.\n\nKey reuse points: `BotSpec`/`ReadScopes`/`WriteScopes` (`app/bots/base.py`), `app/bots/ids.py`, `app/bots/registry.py` (staging-gated lazy registration), `app/bots/tante_rosi.py` (pattern), `app/bots/prompts/tante_rosi.py` (prompt module pattern), `app/services/hot_context_solo.py` (solo hot-context block), `app/services/tools/registry.py` + `read_tools.py` + `write_tools.py` + `scope_guard.py`, `migrations/` numbering, `topic_status` for current focus.\n\n## Phase 1: Data Model — Migrations & Topic\n\n### Step 1: Add `fitness` topic + `hector` bot row (`migrations/0037_fitness_topic.sql`)\n**Scope:** Small\n1. **Create** `migrations/0037_fitness_topic.sql` mirroring `migrations/0033_pregnancy_topic.sql`: `INSERT INTO mediator.topics (id, slug, display_name) VALUES (gen_random_uuid(), 'fitness', 'Fitness') ON CONFLICT (slug) DO NOTHING;`.\n2. **Insert** the Hector row into `mediator.bots` (mirroring how `tante_rosi` / `mediator` are seeded — verify in existing seed/migration; if bots table seeding lives elsewhere, add Hector there).\n3. **Add** a matching `0037_fitness_topic.down.sql` for symmetry with `0033_pregnancy_topic.down.sql`.\n\n### Step 2: Commitments […]