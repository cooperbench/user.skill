# Preferences: AlienKevin

## Pushback Distribution

- **Non-pushback** (63.8%): Agent output accepted; user continues with status checks or new tasks
- **Correction** (23.9%): Agent did something wrong or suboptimal — user redirects with a why-question or a directive
- **Failure report** (11.2%): Background task failed or agent's claim was wrong — user surfaces the discrepancy
- **Rejection** (1.0%): Outright refusal, very rare ("Can you retry the TB-lite eval?" when no retry was warranted)
- **Takeover** (0.1%): User takes over directly, essentially never

## What Triggers Corrections

1. **Wrong cluster/infrastructure**: Running on Ray when should use Iris; using wrong TPU slice size; wrong GCS region for checkpoints
2. **Config drift**: Changing `max_grad_norm`, sequence length, or TPU slice without being asked — "Don't mess with training config/TPU slice size"
3. **Running simultaneous exclusive jobs**: "You can only run 1 Harbor eval at the same time due to Daytona sandbox concurrency limitations"
4. **Wrong branch or worktree**: Committing to main instead of `kevin/agentic-sft`; working in wrong worktree
5. **Duplicate tracking**: Mentioning 131K details in the 32K GitHub issue
6. **Overwriting comments**: Updating an existing GitHub comment instead of posting a new one at the bottom
7. **Timing/progress claims that don't add up**: "<1h left" that becomes 11h; step counts that don't match expected
8. **Summarizing instead of showing**: "Not eval commands but actual SFT launch command"

## What Satisfies

- Agent accurately monitors and reports status without being asked twice
- GitHub comments posted/updated exactly at the specified URL
- SFT runs resumed correctly from prior checkpoints
- Eval results reported with comparison to paper numbers (e.g., "14/89 = 15.7% (target: 13.0 ± 2.2)")
- Agent proactively records constraints in memory without being asked a second time

## Workflow Habits

- **Monitoring-heavy**: Sets background polling tasks; checks in with "how's it going?" every 30–60 minutes across sessions that span days
- **Parallel-by-default for independent work**: Explicitly asks for parallelism ("run the rest of the shards in parallel")
- **Sequential for dependent work**: "Start with TB-Lite first. Once it finishes successfully and the score is within the acceptable range, start TB2."
- **Plan-then-inspect**: "Before you run anything, update harbor evals to run on Iris. Then let me inspect."
- **No test-driven development**: Does not write tests; validates by running evals and comparing against paper baselines
- **Commit cadence**: Cares about which branch/commit is used for reproducibility; asks for commit hashes in GitHub comments
- **Explanation-seeking**: High "understand" intent (45.2%) — frequently asks why something happened, expects the agent to reason out loud

## Tool/Stack Preferences (visible in prompts)

- **Cluster**: Iris (NOT Ray) — enforced as a hard rule
- **TPU preference**: v5p-64 if available; v5p-32 as fallback; v5p-256 for memory-intensive 131K jobs
- **GCS convention**: `gs://marin-us-central1/` with fixed `MARIN_PREFIX` across reruns
- **Training framework**: Levanter + JAX (not LlamaFactory)
- **Eval runner**: Harbor with Daytona sandboxes; concurrency = 1 Harbor eval at a time
- **GitHub**: Issue comments as the canonical progress log; expects agent to post formatted markdown tables
- **WandB**: Expects wandb links for any training run
- **Python toolchain**: `uv run` for scripts, `gcloud storage` for GCS ops
- **Node**: nvm-managed, v22+; codex CLI from `@openai/codex`
