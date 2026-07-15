> DEVELOPER

ehck out this pr and checkfor BS https://github.com/elijahintelligence/elijah/pull/343/

> AGENT

Checked out `pr-343` (1506+/265− across 85 files, integration PR by `hqmf8104`). Tests on touched paths pass and ruff is clean. But there's a lot of BS to call out.

## Process violations (AGENTS.md / CLAUDE.md)

1. **Bundled mega-PR.** Body itself says it "supersedes #342, absorbs #344, #345, #347, #348, #349, partially absorbs #346." That's a direct violation of "one logical change per PR; do not bundle unrelated cleanup."
2. **Wrong PR body structure.** Uses `## Summary` / `## What changed` / `## Validation`. Required structure is `## What this is` then `## Technical detail` with the named sub-headings.
3. **Wrong title prefix.** `[codex]` isn't in the allowed set (`FS<N>:`, `Cross-FS:`, `#<issue>:`).
4. No `@kungfusaini` tag visible in PR.

## Anti-patterns from your port-review memory

5. **Defensive `str(x or "").strip().lower()` everywhere.** New helpers in `services/worker/research_driver_question_pipeline.py:174-200`, `services/api/routes/questions.py:728-737`, `core/research_driver/conditional_edge_quality.py:323-336`. Exactly the anti-pattern your memory says to catch.
6. **`except Exception` + silent fallback.** `packages/domain/baselines/dispatch.py:165` and `core/research_driver/conditional_edge_quality.py:367` both `# noqa: BLE001` and substitute a hard-coded fallback (p=0.5, or direction-based 1.2/0.8/1.0 multiplier). Eats real errors.

## Functional risks not called out in the PR body

7. **FS10 ingest now clobbers existing records.** `fs10_validation/ingest.py:197-216` flipped from `if question_id in lookup: continue` to always-overwrite. Behavior change, not mentioned.
8. **Always flushes.** Same function: `if added > 0` → `if question_payloads`. Triggers flush + new `questions.json` write even when nothing was added.
9. **`resolve_pipeline_run_id` has surprising override.** `research_driver_question_pipeline.py:884-895` — if a caller passes `run_id == batch_run_id`, it silently rewrites to `{batch_run_id}--{question_id}`. Explicit caller values shouldn't be re-interpreted by string equality with a dir name.
10. **FS4 race-timeout default dropped to "no cap."** `packages/domain/baselines/dispatch.py:47-78` removes the 60s default and the FS4 §17.3 spec citation in the comment. If §17.3 mandates 60s, this is a silent spec deviation; either way it's a cost/latency footgun.
11. **`max_output_tokens` defaults are now `None` everywhere.** Many tools went from explicit caps (relevance filter 80, IWVerdict 400, FS11 scorer 600, base tools 1200, indicator 1800, promotion 2000, native 3200, summary 4000) to unbounded. The Haiku **relevance filter dropping its 80-token cap** is especially worrying — it returns a tiny JSON, no reason to uncap.
12. **Prompt cache invalidation.** `max_output_tokens` is part of the cache key (`packages/inference/llm/runtime.py:322,373`). Flipping defaults from ints to `None` busts every cached LLM call. Not mentioned anywhere.
13. **FS10 incoherent comment.** `fs10_validation/runner.py:70-74` forces `max_parallel_questions=1` "until batch run_id collision fix is relied on everywhere" — but the same PR ships that fix. Either the override is now dead, or the fix isn't actually trusted yet.
14. **Dead complexity in FS11 scorer.** `packages/domain/qc/llm_scorer.py:260` routes between `prompts/FS11/defensibility_scorer_type_{a,b}/user.md` — but both files are byte-identical (`{body}\n\nScore the nine axes per the schema.`). Two files and a router for zero behavior difference.
15. **Magic numbers.** Slimline fallback `p=0.5`, multipliers `1.2 / 0.8 / 1.0` — hard-coded, no spec citation.

## What's actually fine

- Tests added on the touched paths pass; ruff/format clean.
- Inline-prompt extraction into `prompts/` is a real cleanup (one of the listed anti-patterns).
- Alembic migration has a proper downgrade that backfills `3200` before re-tightening NOT NULL.

Bottom line: even if the individual edits are mostly defensible, this PR should not land as one unit. It violates the bundling rule outright, ships several silent behavior changes (FS10 ingest overwrite, FS4 timeout removed, every LLM cap removed, cache invalidation) that aren't in the body, and reintroduces port-review anti-patterns you've explicitly told me to flag.

> DEVELOPER

We might have to merge it als one thing, but let's talk about the reason for these decisoin

> AGENT

Sure. My best read of the motivations, grouped by what's actually load-bearing vs incidental:

**Uncapping `max_output_tokens` everywhere.** Most likely motivation: GPT-5 / reasoning models bill (and stall) when `max_tokens` is too tight — the model hits the cap mid-reasoning and returns truncated JSON, which then either fails schema parse or gets retried. Letting the provider use its own model-aware default sidesteps that. The cost is that uncapped means *uncapped* — a stuck model can burn a lot. The relevance filter (was 80 tokens, now None) is the one that looks like a copy-paste mistake rather than a deliberate choice; that one returns 1-line JSON and there's no reasoning-model justification for it.

**Dropping the FS4 60s race timeout default.** Same family of motivation: a wall-clock cap that fires mid-estimator throws away partial work and forces the fallback path. If the parallel race always has the slow estimator finish after 60s, you're paying for the LLM call and getting nothing. Making it opt-in via env is defensible. The thing that's *not* defensible is silently deleting the FS4 §17.3 citation in the comment — if the spec mandates 60s, the spec needs updating in the same PR or this is a documented deviation.

**Batch run_id `{batch}--{question_id}`.** This is the cleanest motivation in the PR. The DB has a unique constraint on `run_id`; batch question runs were colliding because every sub-question reused the batch's run dir name as run_id. The chosen shape preserves artifact paths (`run_dir/question_id/...`) while making the DB row unique. Reasonable. The brittle part is the equality check (`if explicit and explicit != batch_run_id: return explicit`) — that's trying to detect "caller passed the dir name as run_id by accident" but it conflates "explicit override" with "implicit default." A cleaner shape is `run_id=None` ⇒ derive, `run_id=str` ⇒ trust.

**FS10 forcing `max_parallel_questions=1`.** Best read: the run_id fix lets the *DB writes* not collide, but other shared state (file paths, in-memory caches, graph persistence state) hasn't been audited for thread-safety yet. So the override is belt-and-suspenders. The comment is misleading though — it reads like "we don't trust this fix" rather than "parallelism has other unaudited surfaces."

**FS1 binary-only enforcement at every entrypoint.** Motivation is real: the binary-only gate exists, but only enforced at the drafter. Question records can enter via create, update, step-run, and batch paths that bypass the drafter. The fan-out of duplicated `_enforce_fs1_binary_only_*` helpers across api and worker is the price of not having a single chokepoint. A cleaner design would be a validator on `QuestionRecord` itself so every code path benefits, but I can see why they didn't want to touch the contract model in a stability PR.

**Slimline routing (`crude_plus_tuning_head`) with hardcoded fallbacks.** Read: this is the MVP routing tier — skip the full Fermi race, use crude estimate + a tuning head, fall back to neutral (0.5 / direction-multiplier) if the crude LLM call fails. The magic numbers (0.5, 1.2, 0.8) are placeholder priors for "we have no signal." Those should probably live in `core/run_config.py` or the routing config, not as module constants in dispatch.py.

**FS11 type_a/type_b identical prompts.** This one I genuinely can't infer a good motivation for. Either the split was planned (the routing code exists) and the second prompt was never written, or someone refactored away the difference and forgot the files. My guess is the former — this is a scaffold for a future split, but shipping two identical files isn't the right way to scaffold.

**FS10 ingest overwrite-on-rewrite.** Best read: ingest needs to be idempotent on re-run with edited source rows. Old code preserved the first record forever, so re-ingesting an updated `questions.json` had no effect. New code makes ingest behave like an upsert. Defensible — but it's a real behavior change that belongs in the PR body.

Which of these do you want to dig into? My picks for "actually matters before merge" are (1) uncapping the relevance filter specifically, (2) the FS4 spec deviation, and (3) the magic-number fallbacks in slimline routing — the rest are either real wins or cosmetic.

> DEVELOPER

check the PR bodies and the closed PRs mentioned to get a full pictire

> AGENT

That completely changes the picture. Reframing what's actually in this PR:

## Real shape of #343

The git history shows two distinct phases:

- **One new commit (`afa1a3f`)**: the "MVP routing" work that was *never* a standalone PR — FS1 binary-only enforcement, slimline `crude_plus_tuning_head` routing, uncapped token defaults, the alembic migration.
- **Six cherry-picks** of already-closed PRs: #344, #345, #346, #347, #348, #349.

So calling #343 an "integration PR" is generous — it's really one new feature commit (the routing/uncapping work) plus a clean rebundle of six previously well-formed PRs. The author *can* do small PRs; they did six of them, then collapsed them.

## Revisions to my critique now that I've seen the absorbed PRs

**PR #342 is the real story.** It was titled "Make LLM token caps runtime configurable" and added `core/llm_token_caps.py` — a *central resolver* backed by `config/run_profile.toml [llm_output_tokens]` and env overrides. That PR closed and #343 replaced it with "default everything to None, let the provider decide." That's not just a different default — it's an **architectural retreat**. Operators were going to be able to raise/lower caps via config without source edits; now they can't, because no resolver exists. If the original motivation was "stress runs are fragile because caps are embedded in source code," the #343 approach swaps "fragile because hardcoded" for "fragile because uncapped." Worth asking the author why the resolver was abandoned.

**The FS10 `max_parallel_questions=1` "incoherence" I flagged is real but explained.** PR #345's body says explicitly: the sequential default exists "until #346 lands" (the run-id collision fix). #343 ships both #345 *and* #346 — so the safety belt is now redundant by the original author's own logic. They preserved it anyway. Either the author forgot to drop it post-bundling, or there are other unaudited shared-state issues beyond run_id collisions. The comment in `runner.py` ("until batch run_id collision fix is relied on everywhere") supports the second reading but should be rewritten if so.

**FS4 timeout is cleaner than I assumed.** PR #347 says explicitly: "60s cut off slow but valid runs during long validation batches." Not GPT-5 reasoning models — just validation runs that legitimately take longer than a minute. The risk ("teams that relied on the 60s safety valve should set the env var explicitly") was acknowledged in #347's body. Fine.

**PR #343 body has a factual error.** It says "Partially absorbs #346: the run-id fix is included; the source-free driver behavior is intentionally omitted." But #346 is *only* the run-id fix — it has no source-free driver behavior. The source-free driver work is in #341. Either the author confused #346 with #341, or they're describing a third scope. Either way the description is wrong about what's in vs out.

**Two open PRs (#341, #350) are stranded with no description of how #343 affects them.** #343 *ships* `prompts/FS3/indicator_extraction_free/*` files (cherry-picked from #349), but the Python wiring lives in #341/#350 which haven't merged. So those prompt files are dead-on-arrival in #343 — they sit in the tree with no caller until #341 or #350 lands. Not broken, just confusing.

**The contract test from #349 (`tests/test_prompt_store_contract.py`) is genuinely valuable.** It guards against new inline `system_prompt=("You...` prose. That's a real port-review anti-pattern getting enforced via test. Good.

## What I'd actually push back on before merge

Re-prioritized:

1. **Why was #342's centralized token-cap resolver abandoned?** The "MVP routing" commit goes the opposite direction (no caps, no resolver). The original author of #342 might just have been the same agent in a different conversation — worth confirming this wasn't a regression from forgetting context.
2. **Drop the now-redundant `max_parallel_questions=1` override OR rewrite the comment to say what *other* shared state isn't audited.** As written it's self-contradictory.
3. **The FS1 binary-only fan-out and slimline routing got zero standalone review.** They're the novel work in this PR and they're the parts with the defensive-string patterns and `except Exception` fallbacks. Those deserve their own review pass before they hide inside a 1500-line diff.
4. **Fix the #346 vs #341 mislabel in the PR body.** Small but reviewers shouldn't be guessing scope.

Everything else (FS4 timeout, FS10 questions sync, run_id, prompts move, smoke/calibration defaults) was already reviewed-and-closed as small PRs. Re-reviewing them as part of #343 is wasted work; the audit should focus on the `afa1a3f` commit only.

> DEVELOPER

Can you make comment on the PR for all of this please.

> AGENT

Posted: https://github.com/elijahintelligence/elijah/pull/343#issuecomment-4519192304

> DEVELOPER

this failed the runs? https://github.com/elijahintelligence/elijah/pull/341

> AGENT

Yes, but the real failure isn't what the PR checks page surfaces.

**Latest run on `8b3d8be5` (3s, all jobs):** these failed before any step ran — no runner, no steps, no log. That's a GitHub Actions infrastructure/concurrency artifact (runner unavailable or auto-cancellation), not a code failure. Likely just needs a re-run.

**The meaningful failure** is the previous run on commit `2f08a23b`. There lint and docker-smoke passed, and `test` ran for ~2.5 minutes before hitting:

```
FAILED tests/test_code_quality_conventions.py::test_graph_any_in_research_driver_within_budget
AssertionError: graph: Any count 40 exceeds budget 39; use BayesianGraph or narrow the type.
assert 40 <= 39
```

That's a guard-rail test that counts `Any` type annotations on `graph` parameters across the research driver and caps them at a budget. PR #341 introduced one new `graph: Any` usage and bumped the count from 39 to 40. The fix is one of:

- Replace the new `graph: Any` with `graph: BayesianGraph` (or a narrower type) — preferred.
- Bump the budget constant `GRAPH_ANY_IN_RESEARCH_DRIVER_BUDGET` to 40 — only if the new `Any` is actually justified.

If you want, I can check out #341 locally, find the offending line, and propose the typed fix.

> DEVELOPER

it seems like we exceed our 3000mins of CICD time. Is that expected or is that wayyy to much

> AGENT

Way too much, and very fixable. Estimate from sampling 49 of 578 May runs:

**~4,500 billable minutes this month** vs the 3,000-minute Team allowance — ~50% overrun, and ~225% of the 2,000-minute Free tier.

## Where the minutes are going (per-PR-run)

| Job | Runner | Avg | Share |
|---|---|---|---|
| `test` (pytest + mypy) | ubuntu-latest | 4.05 min | ~52% |
| `docker-smoke` (`docker build`) | ubuntu-latest | 2.17 min | ~28% |
| `build-and-push` (dev/main only) | ubuntu-latest | 4.41 min × ~17 runs | small |
| `lint` | ubuntu-latest | 0.75 min | ~10% |
| `deploy-*` | self-hosted (Betty) | — | **not billed** |

So every PR push costs ~7 billable minutes. 578 runs in 22 days = ~26 runs/day. That's the math; nothing structurally insane, just no cost controls.

## The quick wins (rough impact)

1. **`concurrency:` cancel-in-progress on PR runs.** No such block in `docker-build.yml`. Right now every force-push to a PR triggers a full new run *and* the old one finishes. Looking at #341, you can see paired runs 7 minutes apart, both running to completion. **Estimated saving: 20–30%.** Add this at workflow root:
   ```yaml
   concurrency:
     group: ci-${{ github.workflow }}-${{ github.ref }}
     cancel-in-progress: ${{ github.event_name == 'pull_request' }}
   ```

2. **`paths-ignore:` for docs-only changes.** Right now any `.md` edit triggers the whole pipeline. **Saving: 5–15%** depending on doc cadence.

3. **`docker-smoke` is the heaviest fixed cost.** It does `docker build` from scratch each PR (~2.2 min × 100% of PRs = ~130 min/month). Options:
   - Add `docker/build-push-action@v5` with `cache-from: type=gha, cache-to: type=gha`. Saves ~70% of that job after the first run.
   - Or gate `docker-smoke` to only run when `Dockerfile`, `compose.*.yml`, or `pyproject.toml` change. Most PRs don't touch any of those.

4. **`test` job runs mypy on full repo every time.** That's `uv run python -m mypy .` — easily 30–60s of the 4-minute test run. Add mypy cache (`.mypy_cache` in `actions/cache@v4`) keyed on `pyproject.toml` hash. Saving: ~15s × 578 = ~2.5 hours.

5. **`uv sync` cache.** `astral-sh/setup-uv@v5` has a built-in cache option (`enable-cache: true` with a key on `uv.lock`). If you're not using it, every job re-downloads the dep tree. Saving: ~30s × ~150 hosted jobs = ~75 min.

## The "is this normal" answer

For an active repo with 26 PR-pushes/day and a heavy test + docker-smoke pipeline, 4,500 minutes is on the high end of normal *without* cost controls, and totally avoidable *with* them. Adding just `concurrency: cancel-in-progress` and gating `docker-smoke` to relevant paths would likely bring you under 3,000 min/mo on the same workload.

Want me to draft the workflow edit?

> DEVELOPER

hmmm so if you could optimise this, how would you? let's just talk about it

> AGENT

OK, thinking out loud about this.

**The biggest lever by far is `cancel-in-progress`.** Agent workflows (Codex/Cursor/Claude) force-push a lot — every "fix lint", "rebase", "address review" pushes a new commit and triggers a full new run while the old one keeps grinding to completion. On PR #341 alone I saw two runs 7 minutes apart, both running to the same job. If even half your 578 runs are superseded duplicates, that's ~2,000 billable minutes wasted on builds whose results no one will look at. One YAML block at the workflow root makes that go away tomorrow. This is the "before you optimize anything, stop doing free work" fix.

**Second biggest is asking what `docker-smoke` is actually catching.** Every PR builds the full Docker image (~2.2 min × every run = ~21 hours/month). Most PRs don't touch `Dockerfile`, `compose.*.yml`, or `pyproject.toml` — they touch Python under `services/` or `core/`. If you gate that job on `paths:` covering just the files that can break the build, you skip it on ~80% of PRs. Cost of being wrong: a Docker breakage slips through on a PR that "couldn't possibly affect it" — usually those are easy to spot and fix after merge. So the question is really "is the marginal value of running this on every PR worth ~20 hours/month?" — and I'd argue no.

**Third lever: you already have a self-hosted runner.** Betty handles deploys for free. The interesting question is whether you trust it for the `test` job too. If yes, your single biggest billable line item (52% of usage) goes to zero. The pushbacks are real though:
- If Betty is busy or down, CI is down. Right now Betty failure only blocks deploys, not PR review.
- If you ever accept PRs from forks or untrusted contributors, running their code on Betty is a security problem. For this repo it looks like everything's first-party or agent-authored under your control, so probably fine.
- Concurrency: 26 runs/day × 4 minutes = ~104 minutes/day of test job time on Betty. That's <10% of a day, so queueing shouldn't be an issue unless Betty is heavily used for other things.

I'd put this in the "consider once you've done the cheap wins" bucket — it's a real architectural shift and you want to be deliberate.

**Fourth lever, more about wall clock than billing:** `test` currently does `uv sync --frozen --dev --extra worker` from scratch (~30s) + mypy on the whole repo (~30-60s) + pytest (~3 min). The mypy step is the interesting one — it's a static check that doesn't depend on the postgres service or the test fixtures, so it has no reason to share a job with pytest. If you split it out:
- It can run in parallel with pytest (wall-clock win, not billing win on its own)
- It can be cached aggressively (mypy's incremental cache is good when the keys are right)
- You can decide it's merge-gating only, not push-gating, which means it doesn't run on every iterative push during PR development

That third point is the conceptually interesting one: **not every check needs to run on every push.** Lint and fast unit tests give you the signal you need while iterating. Type-checking and full integration tests can run when the PR transitions to "ready for review" or when it enters a merge queue. Agents iterating against a smaller cheap loop is faster *and* cheaper.

**Fifth lever, more speculative:** if you're going to be doing this much agent-driven CI, consider whether a merge queue makes sense (`merge_group` event). PRs queue up, get one final full-suite run against the integration tip, and merge if green. You skip running full CI on every intermediate PR commit because the queue check is the authoritative gate. Lots of complexity to set up though, and only pays off at higher PR volume than yours.

**Things I'd explicitly *not* recommend:**
- Splitting pytest into shards. More parallelism, same total billable minutes. Helps wall clock, doesn't help budget.
- Moving everything to self-hosted. Single point of failure, and you lose the "GitHub-managed" sanity-check that your build runs on a clean env.
- Going to a different CI provider. The work is in the workflow files; the platform isn't the problem.

**My honest read of priority:**

1. `concurrency: cancel-in-progress` — probably 25-35% saving, costs nothing, takes 30 seconds.
2. `paths-ignore` on docker-smoke (or `paths` to only run when relevant) — probably 15-20% saving.
3. `setup-uv` cache + mypy cache — probably 5-10% saving, mostly wall-clock improvement.
4. Then re-measure. The above three alone likely get you under 3,000.
5. *Only if still over budget:* consider moving `test` to Betty or splitting mypy/pytest with merge-gate-only mypy.

The interesting design question hiding underneath all this is: *what are you actually using CI to tell you?* If it's "did the agent break something," you want fast feedback on every push — so optimize for cheap iteration loops. If it's "is this safe to merge to dev," you want the full suite at merge time and minimal noise in between. Right now the workflow treats every push as a merge candidate, which is the most expensive possible default.

> DEVELOPER

let's check this out then   1. concurrency: cancel-in-progress — probably 25-35% saving, costs nothing, takes 30 seconds.
  2. paths-ignore on docker-smoke (or paths to only run when relevant) — probably 15-20% saving.
  3. setup-uv cache + mypy cache — probably 5-10% saving, mostly wall-clock improvement.

> AGENT

I'll make these changes on a fresh branch from `dev` and open a draft PR.

> AGENT

Done. Draft PR opened: https://github.com/elijahintelligence/elijah/pull/352

**Summary of the change:**
- Workflow-level `concurrency` group with `cancel-in-progress` only on PR events (push events to dev/main are never cancelled, so deploys are safe). Group key uses ref for PRs, SHA for pushes — so dev pushes don't serialize.
- `paths-ignore` at workflow root for `**/*.md`, `docs/**`, `agent_rules/**`, `.gitignore`, `LICENSE`.
- `docker-smoke` keeps cheap compose validation always-on, but gates the expensive `docker build` step via `dorny/paths-filter@v3` on Docker-affecting paths. Always rebuilds on push to dev/main so deploy artifacts stay fresh.
- `setup-uv@v5` with `enable-cache: true` in lint + test.
- `actions/cache@v4` for `.mypy_cache` in test, with progressive restore-keys fallback.

**What I deliberately left out:** moving `test` to Betty, splitting mypy into its own parallel job, and tiering checks by PR-readiness. Those are bigger architectural calls that deserve their own conversation — they should be on the table only if these three controls aren't enough to get under 3,000 minutes.

CI will run on the PR itself, which is also the first real test of the concurrency + cache behavior. Promote to ready when you've eyeballed the run.

> DEVELOPER

docker smoke failed for it!

> AGENT

The action needs `pull-requests: read` to query the PR's changed files via API, and the default token doesn't grant that. Fixing.

> AGENT

Cancel-in-progress is verified working — the prior run on `c6bbc179` flipped from `in_progress` to `cancelled` the moment the new push came in. That's the savings mechanism doing exactly what we want.

Now waiting on the new run to confirm `dorny/paths-filter` actually loads with the permission fix.

> AGENT

The background watch will notify me when the new run completes. While we wait, the win is already half-confirmed: the prior run (`c6bbc179`) flipped to `cancelled` the instant the new push landed — that's the concurrency mechanism saving ~7 billable minutes on this one push alone. Multiply by every iterative agent push and you can see where the budget goes.

> AGENT

All green:

| Job | Time | Notes |
|---|---|---|
| lint | 42s | first run, uv cache will warm on next |
| test | 5m9s | first run, mypy cache will warm on next |
| docker-smoke | 2m11s | `paths-filter` succeeded; build ran (this PR modifies the workflow file, which is in the filter) |

**What got verified in flight:**
- ✅ `concurrency: cancel-in-progress` works — the previous run on `c6bbc179` flipped from `in_progress` to `cancelled` the moment the new push arrived. Roughly 5 minutes of test-job time recovered on that one cancellation alone.
- ✅ `dorny/paths-filter@v3` runs with the `pull-requests: read` grant.
- ✅ `Build Docker image` step correctly fired because the workflow file is in the filter list — proving the gate evaluates rather than silently skipping. On a typical Python-only PR, this step would be skipped (~2 min saved per PR).

**Not yet verified in flight (will show on second run of this branch):**
- uv cache warm-hit savings on lint/test setup
- mypy cache warm-hit (since `restore-keys` cascade exists, even a same-key cold miss falls back to the previous `uv.lock`-hashed entry)

PR #352 is now green as a draft. Ready for you to promote when you're satisfied.
