#!/usr/bin/env bash
# Move-conditioned simulator demo: generate (resumable) then score. v4.
set -u
cd "$(dirname "$0")/.."
SLUGS="marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv"
GEN="results/generations_folder_v4mc.jsonl"
RES="results/folder_v4mc_9users.json"
LOG="/tmp/mcdemo.log"
PAR=4
COMMON="--mode folder --slugs $SLUGS --parallel $PAR --move-conditioned --gen-file $GEN --results-file $RES"

for p in $(seq 1 60); do
  out=$(python3 -u scripts/validate.py $COMMON --generate-only 2>&1)
  echo "$out" >> "$LOG"
  miss=$(echo "$out" | grep -oE '[0-9]+ still missing' | grep -oE '^[0-9]+' | head -1)
  echo "[mc gen pass $p] still missing: ${miss:-unknown}"
  [ "${miss:-1}" = "0" ] && break
  sleep 150
done

echo "[mc] scoring"
python3 -u scripts/validate.py $COMMON >> "$LOG" 2>&1
echo "[mc] DONE"
