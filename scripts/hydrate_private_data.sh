#!/usr/bin/env bash
# Hydrate private SWESimBench-derived data from SSE-KMS S3 (us-east-1).
# Requires CURSOR_AWS_ASSUME_IAM_ROLE_ARN (or any AWS creds that can read the bucket).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BUCKET="${SWE_SIM_S3_BUCKET:-swe-sim-private-use1-999404134598}"
REGION="${AWS_DEFAULT_REGION:-us-east-1}"
PREFIX="${SWE_SIM_S3_PREFIX:-derived/v2-58}"

export AWS_DEFAULT_REGION="$REGION"

echo "Hydrating s3://${BUCKET}/${PREFIX}/ → ${ROOT}/ (region=${REGION})"

mkdir -p "$ROOT/data" "$ROOT/users_atK" "$ROOT/.private"

# Bench expects digests/holdout under data/; users_atK at repo root.
aws s3 sync "s3://${BUCKET}/${PREFIX}/digests/" "$ROOT/data/digests/" --only-show-errors
aws s3 sync "s3://${BUCKET}/${PREFIX}/holdout/" "$ROOT/data/holdout/" --only-show-errors
aws s3 sync "s3://${BUCKET}/${PREFIX}/users_atK/" "$ROOT/users_atK/" --only-show-errors

# V2 cohort artifacts (clean sessions, manifests, harbor datasets) — keep out of git tree root noise
aws s3 sync "s3://${BUCKET}/${PREFIX}/" "$ROOT/.private/v2-58/" \
  --exclude "digests/*" --exclude "holdout/*" --exclude "users_atK/*" --only-show-errors
aws s3 sync "s3://${BUCKET}/indexes/" "$ROOT/.private/indexes/" --only-show-errors

if [[ ! -f "$ROOT/data/manifest.json" ]] && [[ -f "$ROOT/.private/v2-58/clean_manifest.json" ]]; then
  # Optional: leave a pointer; do not invent a legacy manifest from v2 clean_manifest.
  echo "Note: data/manifest.json not present; v0 bench may need legacy digests only."
fi

echo "Done. Cohort users: $(wc -l < "$ROOT/.private/indexes/v2_users.txt" 2>/dev/null || echo unknown)"
du -sh "$ROOT/data/digests" "$ROOT/data/holdout" "$ROOT/users_atK" "$ROOT/.private" 2>/dev/null || true
