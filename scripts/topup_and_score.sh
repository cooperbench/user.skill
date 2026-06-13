#!/usr/bin/env bash
# Gentle top-up driver for rate-limited validation.
# Runs generate-only passes at low parallelism until all generations are clean
# (or MAX_PASSES reached), pausing between passes to let the usage limit recover,
# then does one final full scoring pass that writes validation_results*.json.
set -u
cd "$(dirname "$0")/.."

MODE="${1:-inline}"
SLUGS="marcus-sa jeevanpillay robouden melagiri dipree ujuc asragab pavel401 roo-oliv"
MAX_PASSES=80
PASS_PAUSE=180   # seconds between passes

count_missing() {
  python3 - "$MODE" <<'PY'
import json, sys
mode = sys.argv[1]
f = f"results/generations_{mode}.jsonl"
M = ['hit your session limit','usage limit reached','reached max turns','rate limit',
     'overloaded','service unavailable','internal server error']
def bad(t):
    if not t or not t.strip(): return True
    if t.startswith('Error:'): return True
    low = t.lower(); return any(m in low for m in M)
try:
    recs = [json.loads(l) for l in open(f)]
except FileNotFoundError:
    print(168); raise SystemExit
print(sum(1 for r in recs if bad(r['generated'])) + (168 - len(recs)))
PY
}

for p in $(seq 1 "$MAX_PASSES"); do
  missing=$(count_missing)
  echo "[topup pass $p] missing/bad before pass: $missing"
  if [ "$missing" -eq 0 ]; then
    echo "[topup] all generations clean"
    break
  fi
  python3 scripts/validate.py --mode "$MODE" --slugs $SLUGS --parallel 3 --generate-only \
    >> "/tmp/topup_${MODE}.log" 2>&1
  sleep "$PASS_PAUSE"
done

echo "[topup] final scoring pass"
python3 scripts/validate.py --mode "$MODE" --slugs $SLUGS --parallel 3 \
  >> "/tmp/topup_${MODE}.log" 2>&1
echo "[topup] done; remaining missing/bad: $(count_missing)"
