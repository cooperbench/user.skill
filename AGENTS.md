# AGENTS.md

## Privacy (non-negotiable)

- Never commit raw scrapes, digests, holdout, `users_atK`, or API keys.
- Private corpus lives in SSE-KMS S3 (`us-east-1`, same region as Cursor Cloud Agent artifacts).
- Do not paste secrets into chat, PRs, or this file.

## Cursor Cloud specific instructions

### Secrets (dashboard)

Set environment-scoped Runtime Secrets:

| Name | Purpose |
|---|---|
| `OPENROUTER_API_KEY` | OpenRouter for bench / generation |
| `GEMINI_API_KEY` | Gemini API profileopt paths (if used) |
| `CURSOR_AWS_ASSUME_IAM_ROLE_ARN` | `arn:aws:iam::999404134598:role/swe-sim-cursor-cloud-readonly` |

Rotate any keys that previously lived in `.env` on Seoul/Mac before relying on them in Cloud.

### AWS / S3

- Bucket: `swe-sim-private-use1-999404134598`
- Region: `us-east-1`
- Exact host allowlist (no `*.s3` wildcard): `swe-sim-private-use1-999404134598.s3.us-east-1.amazonaws.com`
- Role trust must use Cursor `roleAssumer` + team External ID (Dashboard → Settings → Advanced).

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
