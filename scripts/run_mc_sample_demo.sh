#!/usr/bin/env bash
# Move-SAMPLED simulator demo (v5): Stage-1 samples the move from the user's prior. Generate then score.
set -u
cd "$(dirname "$0")/.."
SLUGS="marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv"
GEN="results/generations_folder_v5samp.jsonl"
RES="results/folder_v5samp_9users.json"
LOG="/tmp/v5demo.log"
COMMON="--mode folder --slugs $SLUGS --parallel 4 --move-conditioned --move-source sample --gen-file $GEN --results-file $RES"
for p in $(seq 1 60); do
  out=$(python3 -u scripts/validate.py $COMMON --generate-only 2>&1); echo "$out" >> "$LOG"
  miss=$(echo "$out" | grep -oE '[0-9]+ still missing' | grep -oE '^[0-9]+' | head -1)
  echo "[v5 gen pass $p] still missing: ${miss:-unknown}"
  [ "${miss:-1}" = "0" ] && break
  sleep 150
done
echo "[v5] scoring"
python3 -u scripts/validate.py $COMMON >> "$LOG" 2>&1
echo "[v5] DONE"
