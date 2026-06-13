#!/usr/bin/env bash
# Full-cohort validation driver, robust to rate limits.
# Runs generate-only passes (parsing "<N> still missing" from validate.py) until all
# generations are clean or MAX_PASSES is hit, pausing between passes to let the usage
# limit recover, then runs one final scoring pass that writes validation_results*.json.
#
# Usage: run_full_validation.sh [mode] [num_users] [parallel]
set -u
cd "$(dirname "$0")/.."

MODE="${1:-inline}"
USERS="${2:-99}"
PAR="${3:-4}"
MAX_PASSES=150
PASS_PAUSE=150
LOG="/tmp/fullval_${MODE}.log"

for p in $(seq 1 "$MAX_PASSES"); do
  out=$(python3 scripts/validate.py --mode "$MODE" --users "$USERS" --parallel "$PAR" --generate-only 2>&1)
  echo "$out" >> "$LOG"
  miss=$(echo "$out" | grep -oE '[0-9]+ still missing' | grep -oE '^[0-9]+' | head -1)
  echo "[fullval $MODE pass $p] still missing: ${miss:-unknown}"
  if [ "${miss:-1}" = "0" ]; then
    echo "[fullval] all generations clean after $p passes"
    break
  fi
  sleep "$PASS_PAUSE"
done

echo "[fullval] final scoring pass"
python3 scripts/validate.py --mode "$MODE" --users "$USERS" --parallel "$PAR" >> "$LOG" 2>&1
echo "[fullval] DONE mode=$MODE users=$USERS"
