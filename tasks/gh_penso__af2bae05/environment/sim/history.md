> DEVELOPER

Implement the following plan: # Fix: Exec approval bypass via env-var prefix injection (#814) ## Context `extract_first_bin("LD_PRELOAD=/evil.so cat /file")` returns `cat` (a `SAFE_BIN`), so the command proceeds without approval. The full command is passed verbatim to `sh -c`, which honors the inline `LD_PRELOAD` assignment. No `DANGEROUS_PATTERN_DEFS` regex matches env-var assignments. This allows prompt-injection attackers to inject arbitrary shared objects into any safe/allowlisted binary. Vectors: `LD_PRELOAD`, `LD_LIBRARY_PATH`, `LD_AUDIT`, `DYLD_INSERT_LIBRARIES`, `PATH`, `PYTHONPATH`, `NODE_OPTIONS`, `JAVA_TOOL_OPTIONS`, `BASH_ENV`, etc. ## Approach: Two-layer defense in `approval.rs` Single file change: `crates/tools/src/approval.rs` (~243 lines added, total ~1081, under 1500 limit). ### Layer 1 — Regex patterns in `DANGEROUS_PATTERN_DEFS` Add 6 new regex entries for dangerous env-var assignments. These fire via `check_dangerous()` at the top of `check_command()`, catching env vars **anywhere** in the command string (including inside subshells like `sh -c "LD_PRELOAD=..."`). Forces approval (OnMiss/Always) or denial (Off mode). Patterns grouped by category: - Linux dynamic linker: `LD_PRELOAD`, `LD_LIBRARY_PATH`, `LD_AUDIT`, `LD_DEBUG`, `LD_CONFIG` - macOS dynamic linker: `DYLD_INSERT_LIBRARIES`, `DYLD_LIBRARY_PATH`, `DYLD_FRAMEWORK_PATH` - PATH override: `PATH` - Language runtimes: `PYTHONPATH`, `PYTHONSTARTUP`, `NODE_OPTIONS`, `NODE_PATH`, `JAVA_TOOL_OPTIONS` - Language runtimes (cont): `PERL5OPT`, `PERL5LIB`, `RUBYOPT`, `RUBYLIB`, `CLASSPATH` - Shell startup: `BASH_ENV`, `ENV`, `ZDOTDIR` Uses `\b` word boundary to avoid false positives on `MY_LD_PRELOAD_FLAG=1`. Uses `(?i)` for […]

> AGENT

Now I have the full picture. Let me implement all the changes.

> AGENT

Now let me add the tests. Let me see the end of the test module.

> AGENT

Now let me run the tests to verify everything works.

> AGENT

All 67 tests pass. Let me also run clippy and format check.

> AGENT

Let me fix the formatting issues.

> AGENT

Format check passes. Let me check on clippy.

> AGENT

Clippy passes clean. All checks green: - **67 tests pass** (all existing + 40 new) - **`just format-check`** — clean - **`just lint`** — clean Here's what was done in `crates/tools/src/approval.rs`: **Layer 1 — Regex patterns**: Added 6 new `DANGEROUS_PATTERN_DEFS` entries catching dangerous env-var assignments (`LD_PRELOAD=`, `DYLD_INSERT_LIBRARIES=`, `PATH=`, `NODE_OPTIONS=`, `PERL5OPT=`, `BASH_ENV=`, etc.) anywhere in the command string, including inside subshells. Case-insensitive with `\b` word boundaries to avoid false positives. **Layer 2 — Semantic check in `extract_first_bin`**: Now uses `split_once('=')` to extract the key from each skipped env-var token and checks it against a `DANGEROUS_ENV_VARS` constant. Returns `None` when a dangerous var is found, so `is_safe_command()` returns `false` and `matches_allowlist()` fails (unless wildcard `*`), routing the command to approval/denial. **Defense-in-depth**: Both layers must be bypassed independently. Benign prefixes like `RUST_LOG=debug` and `FOO=bar` still work normally.

> TOOL

<task-notification> <task-id>b0wpcv3tt</task-id> <tool-use-id>toolu_016ZEiGgvJUia1Sh11xmLZVP</tool-use-id> <output-file>/private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-similar-papyrus/561231bc-91e2-40cb-a42e-972865ebf6f9/tasks/b0wpcv3tt.output</output-file> <status>completed</status> <summary>Background command "Run clippy lints" completed (exit code 0)</summary> </task-notification> Read the output file to retrieve the result: /private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-similar-papyrus/561231bc-91e2-40cb-a42e-972865ebf6f9/tasks/b0wpcv3tt.output

> AGENT

The background clippy run also completed successfully (exit code 0). Everything's clean — the fix is ready for commit.