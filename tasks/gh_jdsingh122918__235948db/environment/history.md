> DEVELOPER

I am running the ./scripts/run-autoresearch-tasks.sh. where is the logs stored?

> TOOL

tool_use Read
id: toolu_01SMdXS4SSCwSKZZxTZpdC3h
```json
{
  "file_path": "/home/<USER>/Projects/AI/forge/scripts/run-autoresearch-tasks.sh"
}
```

> TOOL

tool_result
id: toolu_01SMdXS4SSCwSKZZxTZpdC3h
```
     1→#!/usr/bin/env bash
     2→set -euo pipefail
     3→
     4→# Autoresearch task runner — executes all tasks in wave order
     5→# Council is enabled via .forge/forge.toml
     6→
     7→FORGE="./target/release/forge"
     8→TASKS_DIR="docs/superpowers/specs/autoresearch-tasks"
     9→LOG_DIR="/tmp/forge-autoresearch-logs"
    10→
    11→mkdir -p "$LOG_DIR"
    12→
    13→GREEN='\033[0;32m'
    14→RED='\033[0;31m'
    15→YELLOW='\033[1;33m'
    16→CYAN='\033[0;36m'
    17→NC='\033[0m'
    18→
    19→run_task() {
    20→    local task_file="$1"
    21→    local task_name
    22→    task_name=$(basename "$task_file" .md)
    23→    local log_file="$LOG_DIR/${task_name}.log"
    24→
    25→    echo -e "${CYAN}━━━ Starting: ${task_name} ━━━${NC}"
    26→
    27→    # Step 1: Generate phases
    28→    echo -e "  ${YELLOW}[1/3]${NC} Generating phases..."
    29→    if ! $FORGE implement "${TASKS_DIR}/${task_file}" --autonomous --dry-run >> "$log_file" 2>&1; then
    30→        echo -e "  ${RED}FAILED${NC} generating phases. See: $log_file"
    31→        return 1
    32→    fi
    33→
    34→    # Step 2: Reset state
    35→    echo -e "  ${YELLOW}[2/3]${NC} Resetting state..."
    36→    $FORGE reset --force >> "$log_file" 2>&1
    37→
    38→    # Step 3: Execute
    39→    echo -e "  ${YELLOW}[3/3]${NC} Running phases..."
    40→    if $FORGE run --autonomous --yes >> "$log_file" 2>&1; then
    41→        echo -e "  ${GREEN}✓ DONE${NC}: ${task_name}"
    42→    else
    43→        echo -e "  ${RED}✗ FAILED${NC}: ${task_name}. See: $log_file"
    44→        return 1
    45→    fi
    46→
    47→    echo ""
    48→}
    49→
    50→run_wave() {
    51→    local wave_num="$1"
    52→    shift
    53→    local tasks=("$@")
    54→
    55→    echo -e "${CYAN}══════════════════════════════════════${NC}"
    56→    echo -e "${CYAN}  Wave ${wave_num} (${#tasks[@]} […]

> AGENT

Logs are stored in `/tmp/forge-autoresearch-logs/`. Each task gets its own log file named `<task-name>.log` (e.g., `/tmp/forge-autoresearch-logs/T01-prompt-config-and-loader.log`).