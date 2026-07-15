# AGENTS.md

## Privacy (non-negotiable)

- Never commit raw scrapes, digests, holdout, `users_atK`, or API keys. Scrubbed `train/` markdown from the clean cohort is allowed.
- Private corpus lives in SSE-KMS S3 (`us-east-1`, same region as Cursor Cloud Agent artifacts).
- Do not paste secrets into chat, PRs, or this file.

## Cursor Cloud specific instructions

Primary Cloud Agent repo: **`cooperbench/user.skill`** branch **`kevin`** (shows in the Cloud Agents picker). The AlienKevin copy is a personal remote mirror only.

Seoul scrape/cohort scripts live under `data-pipelines/` (`claude-crawl/`, `swesimbench-v2/`). Harbor eval packages live at repo-root `tasks/`. Scrubbed train sessions live at `train/` (markdown). Raw scrapes/digests stay in S3, not git.

### Secrets (dashboard)

Set environment-scoped Runtime Secrets:

| Name | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter for bench / generation |
| `GEMINI_API_KEY` | Gemini API profileopt paths (if used) |
| `AWS_ACCESS_KEY_ID` | IAM user `swe-sim-cloud-agent` (S3 R/W on private bucket) |
| `AWS_SECRET_ACCESS_KEY` | Matching secret for that user |
| `AWS_DEFAULT_REGION` | `us-east-1` |

Personal/Ultra plans do **not** get Cursor assume-role External ID; use the scoped IAM user keys above. Rotate keys that previously lived in `.env` on Seoul/Mac, and rotate the IAM access key if it leaks.

### AWS / S3

- Bucket: `swe-sim-private-use1-999404134598`
- Region: `us-east-1`
- Exact host allowlist (no `*.s3` wildcard): `swe-sim-private-use1-999404134598.s3.us-east-1.amazonaws.com`
- IAM user: `swe-sim-cloud-agent` (read/write on this bucket + KMS for SSE)

`environment.json` `install` runs `scripts/hydrate_private_data.sh`, which syncs:

- `derived/v2-58/digests` → `data/digests/`
- `derived/v2-58/holdout` → `data/holdout/`
- `derived/v2-58/users_atK` → `users_atK/`
- remaining v2 cohort artifacts → `.private/v2-58/`

Authoritative v2 cohort is **57 developers** (policy `swesimbench-v2-cohort-policy-2026-07-13.8`), listed in `.private/indexes/v2_users.txt`.

### Smoke

```bash
python3 bench/v0.py --limit 6
```

One profileopt job only after hydrate succeeds and secrets are present.

### Do not

- Restart Seoul `build_clean_cohort.py` or huge file watchers for day-to-day swe-sim work.
- Upload duplicate Mac `swe-chat-scan` trees; Cloud Agents use the filtered private prefix only.
