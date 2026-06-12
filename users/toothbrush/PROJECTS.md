# Projects: toothbrush

## entireio/cli ★ dominant (100% of sessions)

**What it is**: A developer CLI tool that wraps AI coding sessions with git-based checkpointing, shell completion setup, and secrets redaction. The binary is called `entire`.

**Tech stack**: Go, cobra (CLI framework), shell scripts (bash/zsh/fish), mise (task runner), gitleaks (secrets detection), git object model (shadow branches for session state)

**Recurring themes across sessions**:

- **Secrets redaction pipeline**: Built `redact/redact.go` with `RedactString`, `RedactJSONLContent`, `RedactBytes`, `RedactJSONLBytes`; integrated into checkpoint writes; added `output_filter` setting to pipe content through external commands (e.g. `gitleaks-filter`); debugged silent filter failures; audited which files need filtering vs. which are structural metadata
- **Shell completion setup**: Implemented `appendShellCompletion`, `shellCompletionTarget`, `promptShellCompletion`, `setupShellCompletionNonInteractive`; added Fish support with `~/.config/fish` directory creation; introduced versioned stanza manager (`FindStanza`, `UpsertStanza`, `RemoveStanza`) for surgically managing rc-file blocks; moved completion logic from `enable` command to new hidden `curl-bash-post-install` command
- **Session state management**: Added `IsStale()` to `session.State`; integrated stale-session cleanup into `StateStore.List()` and `strategy.LoadSessionState()`
- **Settings parsing**: Unified settings parsing; added strict JSON (`DisallowUnknownFields`); replaced custom stdlib reimplementations
- **Git workflow**: Opens PRs against `main`, addresses review feedback, rebases, references commits by short hash, uses mise for lint gating

**File paths that appear frequently**:
- `cmd/entire/cli/setup.go` (shell completion, ~700–800 lines)
- `cmd/entire/cli/setup_test.go`
- `cmd/entire/cli/root.go`
- `redact/redact.go`
- `redact/redact_test.go`
- `session/state.go`
- `strategy/session_state.go`
- `settings/settings.go`
- `filter/filter.go`
- `cmd/entire/cli/stanza.go`
- `scripts/install.sh`

**Local checkout path**: `/Users/paul/src/entireio/cli/` (visible in `@` file references)
