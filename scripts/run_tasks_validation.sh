#!/usr/bin/env bash
# Full tasks/-based validation driver (no S3), rate-limit tolerant.
# For each mode (folder, inline): run generate-only passes until every job has a clean
# generation (or MAX_PASSES), pausing between passes to let usage limits recover, then one
# scoring pass that writes results/validation_tasks_<mode>.json. Resumable: clean generations
# persist in results/generations_tasks_<mode>.jsonl and are skipped on restart.
#
# Usage: run_tasks_validation.sh [parallel]
set -u
cd "$(dirname "$0")/.."

PAR="${1:-4}"
MAX_PASSES=300
PASS_PAUSE=90
COMMON="--folder-devs-only"

for MODE in folder inline; do
  LOG="/tmp/tasksval_${MODE}.log"
  echo "[tasksval] === mode=$MODE start ===" | tee -a "$LOG"
  for p in $(seq 1 "$MAX_PASSES"); do
    out=$(python3 scripts/validate_tasks.py $COMMON --mode "$MODE" --parallel "$PAR" --generate-only 2>&1)
    echo "$out" >> "$LOG"
    line=$(echo "$out" | grep -oE '[0-9]+/[0-9]+ clean generations' | head -1)
    have=$(echo "$line" | grep -oE '^[0-9]+')
    need=$(echo "$line" | sed -E 's#^[0-9]+/([0-9]+).*#\1#')
    echo "[tasksval $MODE pass $p] ${line:-no-count}"
    if [ -n "${need:-}" ] && [ "${have:-0}" -ge "$need" ]; then
      echo "[tasksval $MODE] all $need generations clean after $p passes" | tee -a "$LOG"
      break
    fi
    sleep "$PASS_PAUSE"
  done
  echo "[tasksval $MODE] final scoring pass" | tee -a "$LOG"
  python3 scripts/validate_tasks.py $COMMON --mode "$MODE" --parallel "$PAR" >> "$LOG" 2>&1
  echo "[tasksval $MODE] DONE -> results/validation_tasks_${MODE}.json" | tee -a "$LOG"
done
echo "[tasksval] ALL DONE" | tee -a /tmp/tasksval_folder.log
