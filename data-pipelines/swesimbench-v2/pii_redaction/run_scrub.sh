#!/usr/bin/env bash
# Convenience wrapper — always use run-heavy for the full artifact pass.
set -euo pipefail
ROOT=/data/swesimbench-v2-harbor
VENV="$ROOT/.venv-pii"
BIN="$ROOT/.local/bin/trufflehog"
REPORT="$ROOT/meta/pii_scrub_report.json"

if [[ ! -x "$VENV/bin/python" ]]; then
  echo "missing $VENV — see pii_redaction/README.md" >&2
  exit 1
fi

exec run-heavy "$VENV/bin/python" -u "$ROOT/pii_redaction/scrub_artifacts.py" \
  --targets "${TARGETS:-train,eval,v2tasks,kevin}" \
  --trufflehog-bin "$BIN" \
  --report "$REPORT" \
  --backup-dir "$ROOT/meta/pii_backups" \
  "$@"
