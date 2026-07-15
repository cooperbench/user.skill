> DEVELOPER

hey man can you plese check out what graphs are on the prod environments database

> AGENT

I don't have enough context to act on this safely. A few things I need to pin down:

> AGENT

Let me check Betty and find the prod database.

> AGENT

Found `elijah-prod-db-1` (postgres:17). Let me look at what graph tables exist.

> AGENT

There's **one graph** on prod:

| Field | Value |
|---|---|
| graph_id | `20260507T075117Z_api_195a791e_g1` |
| run_id | `20260507T075117Z_api_195a791e` |
| status | active |
| pdf_count | 27 |
| drivers_count | 10 |
| indicators_count | 40 |
| edges_count | 60 |
| answer_resolved | false |
| inference_status | stale |
| created_at | 2026-05-07 08:02:46 UTC (~15 days ago) |

The `graphs` table is the primary one; supporting tables on prod are `nodes`, `edges`, `conditional_edges`, `reference_edges`, `information_nodes`, and `graph_summaries`. Want me to dig into node/edge contents for this graph, or check why `inference_status` is `stale`?

> DEVELOPER

what question sis that for ?

> AGENT

The graph is for:

**"Will the Democratic Party win control of the US House of Representatives in the 2026 midterm elections?"**

- **question_id:** `gjopen_q_4092` (Good Judgment Open question)
- **type:** binary (Yes / No)
- **domain:** politics_elections

> DEVELOPER

can we actually seed the demo question from teh staging environmenrt into this prod environment? and then clear the rest of the questions. Is the oprod database upgraded?

> AGENT

Before I touch anything, this is a destructive op on prod. Let me first investigate to give you accurate facts, then confirm the plan with you.

> AGENT

Here's what I found before doing anything:

**Schema parity:** Both DBs are on alembic `20260519_01` — prod is upgraded.

**Staging has 4 questions:**
- `demo_set_q_001` — Will the price of NVIDIA tegra chips exceed their current value by 100%?
- `demo_set_q_002` — Will the green party win the next UK election?
- `demo_set_q_003` — will petrol be more than 3 pounds per litre?
- `user_q_will_uk_cpi_inflation_be_above_3_in_december_2026` — UK CPI inflation Q4 2026

**Prod has 20 questions** (the `gjopen_q_*`, `demo_qs_q_*`, `by_end_of_2026_*` set), with one active graph attached to `gjopen_q_4092`.

Two things I want to confirm before touching prod:

> AGENT

`demo_set` question_set has 4 questions (the 3 `demo_set_q_*` plus the UK CPI one). I'll seed all 4 since they share the demo tag. Plan:

1. `pg_dump` prod to a timestamped backup on Betty (safety net)
2. Dump `demo_set` question_set + its 4 questions from staging
3. On prod, inside a transaction: `DELETE FROM questions` (cascades to runs/graphs/nodes/edges), `DELETE FROM question_sets`, then insert the demo data

Taking the backup first.

> DEVELOPER

Nope there is only ine question that has submitted by as demo

> AGENT

Got it — let me look for that `submitted_by` field instead of guessing.

> AGENT

Found it — `submitted_by` is on `jobs`, not `questions`. Let me find the demo-submitted question.

> AGENT

The demo-submitted question is **`user_q_will_uk_cpi_inflation_be_above_3_in_december_2026`** — "Will UK CPI inflation be above 3% in December 2026?" (binary, macroeconomics).

So the plan becomes:

1. `pg_dump` prod → backup on Betty
2. On prod, in one transaction: `DELETE FROM questions` (cascade clears all runs/graphs/nodes/edges) → `DELETE FROM question_sets` → insert the demo question_set + this single question (copying its row verbatim from staging, including metadata)
3. Optionally also seed the matching `jobs` row (`demo_uk_cpi_run_001`)? Up to you — without it, prod just has the question definition with no prior run.

Want me to proceed with that scope (just the question + question_set, no jobs/runs/graphs)? And do you want the prod backup first?

> DEVELOPER

yes go ahead. I don't care aboyt a backup

> AGENT

Done. Prod state:

| Table | Count |
|---|---|
| question_sets | 1 (`demo_set`) |
| questions | 1 (`user_q_will_uk_cpi_inflation_be_above_3_in_december_2026`) |
| runs | 0 |
| graphs | 0 |
| nodes | 0 |
| edges | 0 |

Deletes: 20 questions wiped, 12 question_sets wiped, and the cascade took out the previous `gjopen_q_4092` run/graph/nodes/edges. The UK CPI demo question + the `demo_set` question_set were copied verbatim from staging (including full metadata).

> DEVELOPER

bro you need to copy the runs, hraphs nodes and edges for the question as well lolll

> AGENT

Fair. Let me scope what needs to come over first.

> AGENT

Scope: 1 job, 1 run, 1 graph, 26 nodes, 32 edges, 6 information_nodes, 24 conditional_edges, 8 reference_edges. Copying in FK order.

> AGENT

All seeded. Quick verification on prod:

> AGENT

Prod now has the demo question fully wired: question → run (`demo_uk_cpi`, completed) → graph (`demo_uk_cpi`) with all 26 nodes, 32 edges, 6 information_nodes, 24 conditional_edges, 8 reference_edges.

Note: `drivers_count` / `indicators_count` / `edges_count` on the `graphs` row are NULL on staging too (they were never populated for this demo run) — the actual nodes/edges are present, just the summary counters aren't filled in.

Also FYI: prod already had 6 unrelated `jobs` rows pre-existing (now 7 with the demo job added). You didn't ask to wipe `jobs`, so I left them alone — let me know if you want those cleared too.

> DEVELOPER

yeah please wipe anything unrelated to the fully wired demo question

> AGENT

Wiping the 6 stale jobs, 24 orphan artifacts, and the unrelated run_config. Leaving config/reference tables (domain_packs, runtime_config, LiteLLM, alembic) alone.

> AGENT

Clean. Prod now contains **only** the demo question chain:

| Table | Count |
|---|---|
| question_sets | 1 (demo_set) |
| questions | 1 (UK CPI) |
| jobs | 1 (demo_uk_cpi_run_001, submitted_by=demo) |
| job_events | 0 (cascaded with jobs) |
| runs | 1 (demo_uk_cpi) |
| graphs | 1 (demo_uk_cpi) |
| nodes | 26 |
| edges | 32 |
| information_nodes | 6 |
| conditional_edges | 24 |
| reference_edges | 8 |
| artifacts | 0 |
| run_configs | 0 |

Left untouched: `domain_packs*`, `runtime_config_sections`, `alembic_version`, `LiteLLM_*`, `_prisma_migrations` — those are infra/reference, not question-related.
