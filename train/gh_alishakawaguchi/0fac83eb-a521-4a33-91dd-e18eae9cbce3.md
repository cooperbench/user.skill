---
session_id: 0fac83eb-a521-4a33-91dd-e18eae9cbce3
developer: "gh:alishakawaguchi"
split: train
source: entire
repo: entireio/cli
start_time: "2026-03-05T22:23:48.103741Z"
n_turns: 7
policy_version: swesimbench-v2-cohort-policy-2026-07-13.15
---

> DEVELOPER

Implement the following plan: # Local test script for Kiro SQLite auth injection ## Context The workflow changes are already applied. This plan adds a local test script that mirrors the CI "Inject Kiro auth token" step so we can verify auth works before pushing. ## Approach Create `scripts/test-kiro-auth.sh` that: 1. Reads auth values from the real macOS kiro DB (`~/Library/Application Support/kiro-cli/data.sqlite3`) 2. Backs up the real DB 3. Replaces it with a fresh DB built using the exact same logic as CI (sqlite3 schema + python3 parameterized insert) 4. Runs `kiro-cli-chat whoami -f json` to verify auth works 5. Restores the original DB (via trap, so it restores even on failure) **Why swap the real DB?** `kiro-cli-chat` ignores `XDG_DATA_HOME` on macOS — it always reads `~/Library/Application Support/kiro-cli/data.sqlite3`. So we must temporarily replace it. ## File to create - `scripts/test-kiro-auth.sh` ```bash #!/usr/bin/env bash # Test that the CI kiro auth injection logic works locally. # Backs up your real kiro DB, creates a fresh one using the CI script logic, # runs "kiro-cli-chat whoami", then restores the original. set -euo pipefail REAL_DB="$HOME/Library/Application Support/kiro-cli/data.sqlite3" if [[ ! -f "$REAL_DB" ]]; then echo "ERROR: No kiro DB found at: $REAL_DB" echo "Run 'kiro-cli-chat login' first." exit 1 fi # Extract auth values from real DB echo "Extracting auth values from real DB..." KIRO_AUTH_TOKEN=$(sqlite3 "$REAL_DB" "SELECT value FROM auth_kv WHERE key='kirocli:odic:token';") KIRO_DEVICE_REG=$(sqlite3 "$REAL_DB" "SELECT value FROM auth_kv WHERE key='kirocli:odic:device-registration';") export KIRO_AUTH_TOKEN KIRO_DEVICE_REG if [[ -z "$KIRO_AUTH_TOKEN" || -z "$KIRO_DEVICE_REG" ]]; then echo "ERROR: Could not extract auth values. Is kiro logged in?" exit 1 fi # Back up real DB BACKUP="${REAL_DB}.bak.$$" echo "Backing up real DB to: $BACKUP" cp "$REAL_DB" "$BACKUP" restore() { echo "Restoring original DB..." mv "$BACKUP" "$REAL_DB" echo "Restored." } trap restore EXIT # Remove real DB and create fresh …

> AGENT

`★ Insight ─────────────────────────────────────` This script uses a backup-and-restore pattern with `trap ... EXIT` — a shell idiom that guarantees cleanup even if the script fails midway. The Python parameterized insert (`?` placeholders) prevents SQL injection from auth token values that might contain quotes or special characters. `─────────────────────────────────────────────────`

> AGENT

Now let me make it executable.

> AGENT

Created `scripts/test-kiro-auth.sh` and made it executable. `★ Insight ─────────────────────────────────────` - The `trap restore EXIT` pattern ensures the original DB is restored even if the script fails at any point (e.g., `sqlite3` errors, `kiro-cli-chat` crash). The `EXIT` signal fires on both success and failure. - Using `$$` (current PID) in the backup filename avoids collisions if the script is accidentally run twice concurrently. - The Python parameterized insert (`?` placeholders) is critical here — auth tokens often contain characters like `'`, `"`, `;` that would break raw SQL string interpolation. `─────────────────────────────────────────────────` Run it with: ```bash bash scripts/test-kiro-auth.sh ```

> DEVELOPER

just commit whats already staged and push

> AGENT

Staged changes are the two workflow files. Committing and pushing now.

> AGENT

Pushed `40ee0d1e` to `origin/alisha/kiro-oneshot`.
