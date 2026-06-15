#!/usr/bin/env bash
# Optimized-simulator demo: generate (resumable, rate-limit tolerant) then score.
set -u
cd "$(dirname "$0")/.."
SLUGS="marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv"
GEN="results/generations_folder_v3.jsonl"
RES="results/folder_v3_9users.json"
LOG="/tmp/optdemo.log"
PAR=4

for p in $(seq 1 60); do
  out=$(python3 scripts/validate.py --mode folder --slugs $SLUGS --parallel "$PAR" \
        --gen-file "$GEN" --results-file "$RES" --generate-only 2>&1)
  echo "$out" >> "$LOG"
  miss=$(echo "$out" | grep -oE '[0-9]+ still missing' | grep -oE '^[0-9]+' | head -1)
  echo "[optdemo gen pass $p] still missing: ${miss:-unknown}"
  [ "${miss:-1}" = "0" ] && break
  sleep 150
done

echo "[optdemo] scoring"
for p in $(seq 1 40); do
  python3 scripts/validate.py --mode folder --slugs $SLUGS --parallel "$PAR" \
    --gen-file "$GEN" --results-file "$RES" >> "$LOG" 2>&1
  pop=$(python3 -c "import json;r=json.load(open('$RES'));print(sum(1 for x in r['records'] if x.get('judge_realism') is not None))" 2>/dev/null || echo 0)
  echo "[optdemo score pass $p] judged: ${pop}/168"
  [ "${pop:-0}" -ge 150 ] && break
  sleep 150
done
echo "[optdemo] DONE"
