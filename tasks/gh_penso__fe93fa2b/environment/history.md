> DEVELOPER

Implement the following plan:

# Fix: Exec approval bypass via env-var prefix injection (#814)

## Context

`extract_first_bin("LD_PRELOAD=/evil.so cat /file")` returns `cat` (a `SAFE_BIN`),
so the command proceeds without approval. The full command is passed verbatim to
`sh -c`, which honors the inline `LD_PRELOAD` assignment. No `DANGEROUS_PATTERN_DEFS`
regex matches env-var assignments. This allows prompt-injection attackers to inject
arbitrary shared objects into any safe/allowlisted binary.

Vectors: `LD_PRELOAD`, `LD_LIBRARY_PATH`, `LD_AUDIT`, `DYLD_INSERT_LIBRARIES`,
`PATH`, `PYTHONPATH`, `NODE_OPTIONS`, `JAVA_TOOL_OPTIONS`, `BASH_ENV`, etc.

## Approach: Two-layer defense in `approval.rs`

Single file change: `crates/tools/src/approval.rs` (~243 lines added, total ~1081, under 1500 limit).

### Layer 1 — Regex patterns in `DANGEROUS_PATTERN_DEFS`

Add 6 new regex entries for dangerous env-var assignments. These fire via
`check_dangerous()` at the top of `check_command()`, catching env vars **anywhere**
in the command string (including inside subshells like `sh -c "LD_PRELOAD=..."`).
Forces approval (OnMiss/Always) or denial (Off mode).

Patterns grouped by category:
- Linux dynamic linker: `LD_PRELOAD`, `LD_LIBRARY_PATH`, `LD_AUDIT`, `LD_DEBUG`, `LD_CONFIG`
- macOS dynamic linker: `DYLD_INSERT_LIBRARIES`, `DYLD_LIBRARY_PATH`, `DYLD_FRAMEWORK_PATH`
- PATH override: `PATH`
- Language runtimes: `PYTHONPATH`, `PYTHONSTARTUP`, `NODE_OPTIONS`, `NODE_PATH`, `JAVA_TOOL_OPTIONS`
- Language runtimes (cont): `PERL5OPT`, `PERL5LIB`, `RUBYOPT`, `RUBYLIB`, `CLASSPATH`
- Shell startup: `BASH_ENV`, `ENV`, `ZDOTDIR`

Uses `\b` word boundary to avoid false positives on `MY_LD_PRELOAD_FLAG=1`.
Uses `(?i)` for […]

> TOOL

tool_use Read
id: toolu_01Qin6yFc3JWQDoqJ5ELduNG
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs"
}
```

> TOOL

tool_result
id: toolu_01Qin6yFc3JWQDoqJ5ELduNG
```
     1→use std::{collections::HashSet, sync::Arc, time::Duration};
     2→
     3→use {
     4→    crate::error::Error,
     5→    regex::RegexSet,
     6→    serde::{Deserialize, Serialize},
     7→    tokio::sync::{RwLock, oneshot},
     8→    tracing::{debug, warn},
     9→};
    10→
    11→use crate::Result;
    12→
    13→/// Outcome of an approval request.
    14→#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
    15→#[serde(rename_all = "lowercase")]
    16→pub enum ApprovalDecision {
    17→    Approved,
    18→    Denied,
    19→    Timeout,
    20→}
    21→
    22→/// Approval mode.
    23→#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
    24→#[serde(rename_all = "kebab-case")]
    25→#[derive(Default)]
    26→pub enum ApprovalMode {
    27→    Off,
    28→    #[default]
    29→    OnMiss,
    30→    Always,
    31→}
    32→
    33→impl ApprovalMode {
    34→    /// Parse approval mode from config value.
    35→    ///
    36→    /// Accepts canonical values plus legacy aliases:
    37→    /// - `on-miss` / `smart` -> `OnMiss`
    38→    /// - `off` / `never` -> `Off`
    39→    pub fn parse(value: &str) -> Option<Self> {
    40→        match value.trim().to_ascii_lowercase().as_str() {
    41→            "off" | "never" => Some(Self::Off),
    42→            "on-miss" | "on_miss" | "smart" => Some(Self::OnMiss),
    43→            "always" => Some(Self::Always),
    44→            _ => None,
    45→        }
    46→    }
    47→}
    48→
    49→/// Security level for exec commands.
    50→#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
    51→#[serde(rename_all = "lowercase")]
    52→#[derive(Default)]
    53→pub enum SecurityLevel {
    54→    Deny,
    55→    #[default]
    56→    Allowlist,
    57→    Full,
    58→}
    59→
    60→impl SecurityLevel {
    61→    /// Parse security level from config […]

> AGENT

Now I have the full picture. Let me implement all the changes.

> TOOL

tool_use Edit
id: toolu_011GZD3B6Fm3EMYHje57AC8Q
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "/// Dangerous command patterns that force approval even when `approval_mode` is\n/// off or `security_level` is full.  Each entry: `(regex_pattern, description)`.\nstatic DANGEROUS_PATTERN_DEFS: &[(&str, &str)] = &[",
  "new_string": "/// Environment variable names that can hijack process execution.\n///\n/// Used by both `DANGEROUS_PATTERN_DEFS` (regex layer) and `extract_first_bin`\n/// (semantic layer) for defense-in-depth against env-var prefix injection\n/// (moltis-org/moltis#814).\nconst DANGEROUS_ENV_VARS: &[&str] = &[\n    // Linux dynamic linker\n    \"LD_PRELOAD\",\n    \"LD_LIBRARY_PATH\",\n    \"LD_AUDIT\",\n    \"LD_DEBUG\",\n    \"LD_CONFIG\",\n    // macOS dynamic linker\n    \"DYLD_INSERT_LIBRARIES\",\n    \"DYLD_LIBRARY_PATH\",\n    \"DYLD_FRAMEWORK_PATH\",\n    // PATH override\n    \"PATH\",\n    // Language runtimes\n    \"PYTHONPATH\",\n    \"PYTHONSTARTUP\",\n    \"NODE_OPTIONS\",\n    \"NODE_PATH\",\n    \"JAVA_TOOL_OPTIONS\",\n    \"PERL5OPT\",\n    \"PERL5LIB\",\n    \"RUBYOPT\",\n    \"RUBYLIB\",\n    \"CLASSPATH\",\n    // Shell startup\n    \"BASH_ENV\",\n    \"ENV\",\n    \"ZDOTDIR\",\n];\n\n/// Dangerous command patterns that force approval even when `approval_mode` is\n/// off or `security_level` is full.  Each entry: `(regex_pattern, description)`.\nstatic DANGEROUS_PATTERN_DEFS: &[(&str, &str)] = &["
}
```

> TOOL

tool_result
id: toolu_011GZD3B6Fm3EMYHje57AC8Q
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01RqYAeFi8jpR9ZF4XbC68VV
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "    (\n        r\"chmod\\s+(-\\S*R\\S*\\s+)*777\\s+/\",\n        \"recursive chmod 777 on root\",\n    ),\n];",
  "new_string": "    (\n        r\"chmod\\s+(-\\S*R\\S*\\s+)*777\\s+/\",\n        \"recursive chmod 777 on root\",\n    ),\n    // Inline environment variable injection (moltis-org/moltis#814)\n    (\n        r\"(?i)\\b(LD_PRELOAD|LD_LIBRARY_PATH|LD_AUDIT|LD_DEBUG|LD_CONFIG)=\",\n        \"dangerous dynamic linker env var\",\n    ),\n    (\n        r\"(?i)\\b(DYLD_INSERT_LIBRARIES|DYLD_LIBRARY_PATH|DYLD_FRAMEWORK_PATH)=\",\n        \"dangerous macOS dynamic linker env var\",\n    ),\n    (r\"(?i)\\bPATH=\", \"PATH override\"),\n    (\n        r\"(?i)\\b(PYTHONPATH|PYTHONSTARTUP|NODE_OPTIONS|NODE_PATH|JAVA_TOOL_OPTIONS)=\",\n        \"dangerous language runtime env var\",\n    ),\n    (\n        r\"(?i)\\b(PERL5OPT|PERL5LIB|RUBYOPT|RUBYLIB|CLASSPATH)=\",\n        \"dangerous language runtime env var\",\n    ),\n    (\n        r\"(?i)\\b(BASH_ENV|ENV|ZDOTDIR)=\",\n        \"dangerous shell startup env var\",\n    ),\n];"
}
```

> TOOL

tool_result
id: toolu_01RqYAeFi8jpR9ZF4XbC68VV
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01J6Bh8BUHP2Smk59YzPMJ7r
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "/// Extract the first command/binary from a shell command string.\nfn extract_first_bin(command: &str) -> Option<&str> {\n    let trimmed = command.trim();\n    // Skip env var assignments at the start (e.g. `FOO=bar cmd`).\n    let mut parts = trimmed.split_whitespace();\n    for part in parts.by_ref() {\n        if !part.contains('=') {\n            // Strip path prefix (e.g. `/usr/bin/jq` → `jq`).\n            return Some(part.rsplit('/').next().unwrap_or(part));\n        }\n    }\n    None\n}",
  "new_string": "/// Extract the first command/binary from a shell command string.\n///\n/// Returns `None` when the command is empty **or** when a leading env-var\n/// assignment uses a dangerous variable name (see [`DANGEROUS_ENV_VARS`]).\n/// This prevents attackers from smuggling `LD_PRELOAD=… cat /file` through the\n/// safe-bin / allowlist path (moltis-org/moltis#814).\nfn extract_first_bin(command: &str) -> Option<&str> {\n    let trimmed = command.trim();\n    // Skip env var assignments at the start (e.g. `FOO=bar cmd`).\n    let mut parts = trimmed.split_whitespace();\n    for part in parts.by_ref() {\n        if let Some((key, _)) = part.split_once('=') {\n            // Dangerous env-var prefix — refuse to extract a binary so the\n            // caller falls through to the approval / denial path.\n            if DANGEROUS_ENV_VARS\n                .iter()\n                .any(|d| d.eq_ignore_ascii_case(key))\n            {\n                return None;\n            }\n        } else {\n            // Strip path prefix (e.g. `/usr/bin/jq` → `jq`).\n            return Some(part.rsplit('/').next().unwrap_or(part));\n        }\n    }\n    None\n}"
}
```

> TOOL

tool_result
id: toolu_01J6Bh8BUHP2Smk59YzPMJ7r
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> AGENT

Now let me add the tests. Let me see the end of the test module.

> TOOL

tool_use Read
id: toolu_01HtP5YpamicQKdJXUgD3KjE
```json
{
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "offset": 860
}
```

> TOOL

tool_result
id: toolu_01HtP5YpamicQKdJXUgD3KjE
```
   860→            err.to_string().contains("dangerous command pattern"),
   861→            "unexpected error message: {err}"
   862→        );
   863→    }
   864→
   865→    #[tokio::test]
   866→    async fn test_dangerous_denied_when_mode_off_full_security() {
   867→        // Full security level does not change the safety floor: dangerous
   868→        // commands are still denied in Off mode.
   869→        let mgr = ApprovalManager {
   870→            mode: ApprovalMode::Off,
   871→            security_level: SecurityLevel::Full,
   872→            ..Default::default()
   873→        };
   874→        let err = mgr
   875→            .check_command("git reset --hard")
   876→            .await
   877→            .expect_err("expected denial for dangerous command in off+full");
   878→        assert!(
   879→            err.to_string().contains("dangerous command pattern"),
   880→            "unexpected error message: {err}"
   881→        );
   882→    }
   883→
   884→    #[tokio::test]
   885→    async fn test_dangerous_forces_approval_when_full() {
   886→        let mgr = ApprovalManager {
   887→            security_level: SecurityLevel::Full,
   888→            ..Default::default()
   889→        };
   890→        let action = mgr.check_command("git reset --hard").await.unwrap();
   891→        assert_eq!(action, ApprovalAction::NeedsApproval);
   892→    }
   893→
   894→    #[tokio::test]
   895→    async fn test_pending_requests_for_session_filters_other_sessions() {
   896→        let mgr = ApprovalManager::default();
   897→        let _ = mgr.create_request("echo one", Some("session:a")).await;
   898→        let _ = mgr.create_request("echo two", Some("session:b")).await;
   899→        let _ = mgr.create_request("echo three", Some("session:a")).await;
   900→
   901→        let pending = mgr.pending_requests_for_session("session:a").await;
   902→        assert_eq!(pending.len(), 2);
   903→        assert!(
   904→            pending
   905→                .iter()
   906→                .all(|request| request.session_key.as_deref() == Some("session:a"))
   907→        );
   908→    }
   909→}
   910→
```

> TOOL

tool_use Edit
id: toolu_01SWUaoGEMzHzPFaES2mX8Sa
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "    #[tokio::test]\n    async fn test_pending_requests_for_session_filters_other_sessions() {\n        let mgr = ApprovalManager::default();\n        let _ = mgr.create_request(\"echo one\", Some(\"session:a\")).await;\n        let _ = mgr.create_request(\"echo two\", Some(\"session:b\")).await;\n        let _ = mgr.create_request(\"echo three\", Some(\"session:a\")).await;\n\n        let pending = mgr.pending_requests_for_session(\"session:a\").await;\n        assert_eq!(pending.len(), 2);\n        assert!(\n            pending\n                .iter()\n                .all(|request| request.session_key.as_deref() == Some(\"session:a\"))\n        );\n    }\n}",
  "new_string": "    #[tokio::test]\n    async fn test_pending_requests_for_session_filters_other_sessions() {\n        let mgr = ApprovalManager::default();\n        let _ = mgr.create_request(\"echo one\", Some(\"session:a\")).await;\n        let _ = mgr.create_request(\"echo two\", Some(\"session:b\")).await;\n        let _ = mgr.create_request(\"echo three\", Some(\"session:a\")).await;\n\n        let pending = mgr.pending_requests_for_session(\"session:a\").await;\n        assert_eq!(pending.len(), 2);\n        assert!(\n            pending\n                .iter()\n                .all(|request| request.session_key.as_deref() == Some(\"session:a\"))\n        );\n    }\n\n    // --- Env-var prefix injection (moltis-org/moltis#814) ---\n\n    // Layer 1: check_dangerous regex hits\n\n    #[test]\n    fn test_dangerous_ld_preload() {\n        assert_eq!(\n            check_dangerous(\"LD_PRELOAD=/evil.so cat /etc/passwd\"),\n            Some(\"dangerous dynamic linker env var\"),\n        );\n    }\n\n    #[test]\n    fn test_dangerous_ld_library_path() {\n        assert_eq!(\n            check_dangerous(\"LD_LIBRARY_PATH=/tmp cat /file\"),\n            Some(\"dangerous dynamic linker env var\"),\n        );\n    }\n\n    #[test]\n    fn test_dangerous_ld_audit() {\n        assert_eq!(\n            check_dangerous(\"LD_AUDIT=/evil.so ls\"),\n            Some(\"dangerous dynamic linker env var\"),\n        );\n    }\n\n    #[test]\n    fn test_dangerous_dyld_insert_libraries() {\n        assert_eq!(\n            check_dangerous(\"DYLD_INSERT_LIBRARIES=/evil.dylib cat /etc/passwd\"),\n            Some(\"dangerous macOS dynamic linker env var\"),\n        );\n    }\n\n    #[test]\n    fn test_dangerous_dyld_library_path() {\n        assert_eq!(\n            check_dangerous(\"DYLD_LIBRARY_PATH=/tmp ls\"),\n            Some(\"dangerous macOS dynamic linker env var\"),\n        );\n    }\n\n    #[test]\n    fn test_dangerous_path_override() {\n        assert_eq!(\n            check_dangerous(\"PATH=/tmp:$PATH cat /etc/passwd\"),\n            Some(\"PATH override\"),\n        );\n    }\n\n    #[test]\n    fn […]

> TOOL

tool_result
id: toolu_01SWUaoGEMzHzPFaES2mX8Sa
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> AGENT

Now let me run the tests to verify everything works.

> TOOL

tool_use Bash
id: toolu_01EngzLHXzcu1VYMcEw9ZoPR
```json
{
  "command": "cargo test -p moltis-tools -- approval 2>&1",
  "description": "Run approval tests",
  "timeout": 120000
}
```

> TOOL

tool_result
id: toolu_01EngzLHXzcu1VYMcEw9ZoPR
```
   Compiling proc-macro2 v1.0.106
   Compiling unicode-ident v1.0.22
   Compiling quote v1.0.44
   Compiling libc v0.2.180
   Compiling cfg-if v1.0.4
   Compiling serde_core v1.0.228
   Compiling serde v1.0.228
   Compiling memchr v2.8.0
   Compiling log v0.4.29
   Compiling itoa v1.0.17
   Compiling equivalent v1.0.2
   Compiling allocator-api2 v0.2.21
   Compiling pin-project-lite v0.2.16
   Compiling find-msvc-tools v0.1.9
   Compiling shlex v1.3.0
   Compiling scopeguard v1.2.0
   Compiling parking_lot_core v0.9.12
   Compiling futures-core v0.3.31
   Compiling lock_api v0.4.14
   Compiling bitflags v2.10.0
   Compiling once_cell v1.21.3
   Compiling version_check v0.9.5
   Compiling foldhash v0.2.0
   Compiling bytes v1.11.1
   Compiling zmij v1.0.19
   Compiling hashbrown v0.16.1
   Compiling typenum v1.19.0
   Compiling thiserror v2.0.18
   Compiling stable_deref_trait v1.2.1
   Compiling slab v0.4.12
   Compiling pin-utils v0.1.0
   Compiling generic-array v0.14.9
   Compiling futures-task v0.3.31
   Compiling autocfg v1.5.0
   Compiling futures-io v0.3.31
   Compiling serde_json v1.0.149
   Compiling futures-sink v0.3.31
   Compiling getrandom v0.3.4
   Compiling tracing-core v0.1.36
   Compiling writeable v0.6.2
   Compiling litemap v0.8.1
   Compiling icu_normalizer_data v2.1.1
   Compiling percent-encoding v2.3.2
   Compiling futures-channel v0.3.31
   Compiling core-foundation-sys v0.8.7
   Compiling icu_properties_data v2.1.2
   Compiling zerocopy v0.8.39
   Compiling fnv v1.0.7
   Compiling num-traits v0.2.19
   Compiling form_urlencoded v1.2.2
   Compiling http v1.4.0
   Compiling syn v2.0.114
   Compiling utf8_iter v1.0.4
   Compiling rustix v1.1.3
   Compiling ipnet v2.11.0
   Compiling base64 v0.22.1
   Compiling httparse v1.10.1
   Compiling errno v0.3.14
   Compiling signal-hook-registry v1.4.8
   Compiling socket2 v0.6.2
   Compiling mio v1.1.1
   Compiling getrandom v0.2.17
   Compiling indexmap v2.13.0
   Compiling cpufeatures v0.2.17
   Compiling jobserver v0.1.34
   Compiling […]

> AGENT

All 67 tests pass. Let me also run clippy and format check.

> TOOL

tool_use Bash
id: toolu_01ST7DhZuvU22hjBQrkS4SYU
```json
{
  "command": "cargo +nightly-2025-11-30 fmt --all -- --check 2>&1 | head -30",
  "description": "Check Rust formatting",
  "timeout": 60000
}
```

> TOOL

tool_use Bash
id: toolu_016ZEiGgvJUia1Sh11xmLZVP
```json
{
  "command": "just lint 2>&1 | tail -20",
  "description": "Run clippy lints",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01ST7DhZuvU22hjBQrkS4SYU
```
Diff in /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs:1056:
             extract_first_bin("RUST_LOG=debug cargo test"),
             Some("cargo"),
         );
[31m-        assert_eq!(
(B[m[31m-            extract_first_bin("CC=gcc CXX=g++ cmake .."),
(B[m[31m-            Some("cmake"),
(B[m[31m-        );
(B[m[32m+        assert_eq!(extract_first_bin("CC=gcc CXX=g++ cmake .."), Some("cmake"),);
(B[m     }
 
     #[test]
Diff in /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs:1147:
     #[tokio::test]
     async fn test_benign_prefix_proceeds_on_miss() {
         let mgr = ApprovalManager::default();
[31m-        let action = mgr
(B[m[31m-            .check_command("RUST_LOG=debug echo hi")
(B[m[31m-            .await
(B[m[31m-            .unwrap();
(B[m[32m+        let action = mgr.check_command("RUST_LOG=debug echo hi").await.unwrap();
(B[m         assert_eq!(action, ApprovalAction::Proceed);
     }
```

> TOOL

tool_result
id: toolu_016ZEiGgvJUia1Sh11xmLZVP
```
Command running in background with ID: b0wpcv3tt. Output is being written to: /private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-similar-papyrus/561231bc-91e2-40cb-a42e-972865ebf6f9/tasks/b0wpcv3tt.output
```

> AGENT

Let me fix the formatting issues.

> TOOL

tool_use Edit
id: toolu_017QtJ3sBTqd38Cc5r2DSjf1
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "        assert_eq!(\n            extract_first_bin(\"CC=gcc CXX=g++ cmake ..\"),\n            Some(\"cmake\"),\n        );",
  "new_string": "        assert_eq!(extract_first_bin(\"CC=gcc CXX=g++ cmake ..\"), Some(\"cmake\"),);"
}
```

> TOOL

tool_result
id: toolu_017QtJ3sBTqd38Cc5r2DSjf1
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> TOOL

tool_use Edit
id: toolu_01CLG6BZrE6nN9YvnWn3Gi5h
```json
{
  "replace_all": false,
  "file_path": "/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs",
  "old_string": "        let action = mgr\n            .check_command(\"RUST_LOG=debug echo hi\")\n            .await\n            .unwrap();",
  "new_string": "        let action = mgr.check_command(\"RUST_LOG=debug echo hi\").await.unwrap();"
}
```

> TOOL

tool_result
id: toolu_01CLG6BZrE6nN9YvnWn3Gi5h
```
The file /Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/tools/src/approval.rs has been updated successfully.
```

> TOOL

tool_use Bash
id: toolu_01A7AhamK362QHkXFc99y4Kp
```json
{
  "command": "cargo +nightly-2025-11-30 fmt --all -- --check 2>&1 | head -10",
  "description": "Verify formatting passes",
  "timeout": 60000
}
```

> TOOL

tool_result
id: toolu_01A7AhamK362QHkXFc99y4Kp
```
(Bash completed with no output)
```

> AGENT

Format check passes. Let me check on clippy.

> TOOL

tool_use Bash
id: toolu_01EpYvV9Tfszd6QFs2TcLpzz
```json
{
  "command": "cat /private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-similar-papyrus/561231bc-91e2-40cb-a42e-972865ebf6f9/tasks/b0wpcv3tt.output 2>&1 | tail -10",
  "description": "Check clippy output"
}
```

> TOOL

tool_result
id: toolu_01EpYvV9Tfszd6QFs2TcLpzz
```
(Bash completed with no output)
```

> TOOL

tool_use Bash
id: toolu_01XhuSYHHBAx3SpdCNsjZLTM
```json
{
  "command": "just lint 2>&1 | tail -10",
  "description": "Run clippy lints again",
  "timeout": 300000
}
```

> TOOL

tool_result
id: toolu_01XhuSYHHBAx3SpdCNsjZLTM
```
    Checking moltis-httpd v0.1.0 (/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/httpd)
    Checking moltis-web v0.1.0 (/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/web)
    Checking moltis v0.1.0 (/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/cli)
    Checking moltis-swift-bridge v0.1.0 (/Users/penso/.superset/worktrees/moltis/similar-papyrus/crates/swift-bridge)
      Timing report saved to /Users/penso/.superset/worktrees/moltis/similar-papyrus/target/cargo-timings/cargo-timing-20260421T130324.997757Z.html
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 59.78s
      Timing report saved to /Users/penso/.superset/worktrees/moltis/similar-papyrus/target/cargo-timings/cargo-timing-20260421T130423.56454Z.html
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.49s
      Timing report saved to /Users/penso/.superset/worktrees/moltis/similar-papyrus/target/cargo-timings/cargo-timing-20260421T130424.315084Z.html
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.86s
```

> AGENT

Clippy passes clean. All checks green:

- **67 tests pass** (all existing + 40 new)
- **`just format-check`** — clean
- **`just lint`** — clean

Here's what was done in `crates/tools/src/approval.rs`:

**Layer 1 — Regex patterns**: Added 6 new `DANGEROUS_PATTERN_DEFS` entries catching dangerous env-var assignments (`LD_PRELOAD=`, `DYLD_INSERT_LIBRARIES=`, `PATH=`, `NODE_OPTIONS=`, `PERL5OPT=`, `BASH_ENV=`, etc.) anywhere in the command string, including inside subshells. Case-insensitive with `\b` word boundaries to avoid false positives.

**Layer 2 — Semantic check in `extract_first_bin`**: Now uses `split_once('=')` to extract the key from each skipped env-var token and checks it against a `DANGEROUS_ENV_VARS` constant. Returns `None` when a dangerous var is found, so `is_safe_command()` returns `false` and `matches_allowlist()` fails (unless wildcard `*`), routing the command to approval/denial.

**Defense-in-depth**: Both layers must be bypassed independently. Benign prefixes like `RUST_LOG=debug` and `FOO=bar` still work normally.

> AGENT

The background clippy run also completed successfully (exit code 0). Everything's clean — the fix is ready for commit.

> DEVELOPER

commit push create a PR

> AGENT

Let me gather the info needed for the commit and PR.

> TOOL

tool_use Bash
id: toolu_01FmbRHpdqUUxVFGdRbZukQz
```json
{
  "command": "git status",
  "description": "Show working tree status"
}
```

> TOOL

tool_result
id: toolu_01FmbRHpdqUUxVFGdRbZukQz
```
On branch similar-papyrus
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   crates/tools/src/approval.rs

no changes added to commit (use "git add" and/or "git commit -a")
```

> TOOL

tool_use Bash
id: toolu_01PyQbhdqQpBDhh6peTgTi7V
```json
{
  "command": "git diff",
  "description": "Show staged and unstaged changes"
}
```

> TOOL

tool_result
id: toolu_01PyQbhdqQpBDhh6peTgTi7V
```
diff --git a/crates/tools/src/approval.rs b/crates/tools/src/approval.rs
index 6ab8dbe9..a45515ac 100644
--- a/crates/tools/src/approval.rs
+++ b/crates/tools/src/approval.rs
@@ -135,6 +135,41 @@ pub const SAFE_BINS: &[&str] = &[
     "command",
 ];
 
+/// Environment variable names that can hijack process execution.
+///
+/// Used by both `DANGEROUS_PATTERN_DEFS` (regex layer) and `extract_first_bin`
+/// (semantic layer) for defense-in-depth against env-var prefix injection
+/// (moltis-org/moltis#814).
+const DANGEROUS_ENV_VARS: &[&str] = &[
+    // Linux dynamic linker
+    "LD_PRELOAD",
+    "LD_LIBRARY_PATH",
+    "LD_AUDIT",
+    "LD_DEBUG",
+    "LD_CONFIG",
+    // macOS dynamic linker
+    "DYLD_INSERT_LIBRARIES",
+    "DYLD_LIBRARY_PATH",
+    "DYLD_FRAMEWORK_PATH",
+    // PATH override
+    "PATH",
+    // Language runtimes
+    "PYTHONPATH",
+    "PYTHONSTARTUP",
+    "NODE_OPTIONS",
+    "NODE_PATH",
+    "JAVA_TOOL_OPTIONS",
+    "PERL5OPT",
+    "PERL5LIB",
+    "RUBYOPT",
+    "RUBYLIB",
+    "CLASSPATH",
+    // Shell startup
+    "BASH_ENV",
+    "ENV",
+    "ZDOTDIR",
+];
+
 /// Dangerous command patterns that force approval even when `approval_mode` is
 /// off or `security_level` is full.  Each entry: `(regex_pattern, description)`.
 static DANGEROUS_PATTERN_DEFS: &[(&str, &str)] = &[
@@ -176,6 +211,28 @@ static DANGEROUS_PATTERN_DEFS: &[(&str, &str)] = &[
         r"chmod\s+(-\S*R\S*\s+)*777\s+/",
         "recursive chmod 777 on root",
     ),
+    // Inline environment variable injection (moltis-org/moltis#814)
+    (
+        r"(?i)\b(LD_PRELOAD|LD_LIBRARY_PATH|LD_AUDIT|LD_DEBUG|LD_CONFIG)=",
+        "dangerous dynamic linker env var",
+    ),
+    (
+        r"(?i)\b(DYLD_INSERT_LIBRARIES|DYLD_LIBRARY_PATH|DYLD_FRAMEWORK_PATH)=",
+        "dangerous macOS […]

> TOOL

tool_use Bash
id: toolu_011QHsqJoBj7umR8MKmrm5Ef
```json
{
  "command": "git log --oneline -10",
  "description": "Show recent commits for style reference"
}
```

> TOOL

tool_result
id: toolu_011QHsqJoBj7umR8MKmrm5Ef
```
b9e4f181 fix(code-index): use open_opts with forced Trust::Full for gix
3871d803 fix(code-index): use struct init for clippy field_reassign_with_default
044ffe81 fix(code-index): set required_trust to Reduced for gix discovery
d3c72a70 chore(web): rebuild dist chunk
0319e972 fix(web): render inline markdown in table cells
686aab21 fix(code-index): use discover_opts with permissive trust for gix
8165a7d5 chore: prepare release 20260421.04
aa002cd9 fix(ci): make safe.directory step non-fatal when git is absent
aff55f6a chore: prepare release 20260421.03
a8e9fe35 fix(ci): restore original step order, fix gix open, revert npm flag
```

> TOOL

tool_use Bash
id: toolu_013L8mbaGqz4uFCSSXhtpkxw
```json
{
  "command": "git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>&1 || echo \"no upstream\"",
  "description": "Check if branch tracks a remote"
}
```

> TOOL

tool_result
id: toolu_013L8mbaGqz4uFCSSXhtpkxw
```
fatal: no upstream configured for branch 'similar-papyrus'
no upstream
```

> TOOL

tool_use Bash
id: toolu_013x4SwjF8EaKPKd1SujPupq
```json
{
  "command": "git add crates/tools/src/approval.rs && git commit -m \"$(cat <<'EOF'\nfix(tools): block exec approval bypass via env-var prefix injection (#814)\n\n`extract_first_bin(\"LD_PRELOAD=/evil.so cat /file\")` returned `cat`\n(a SAFE_BIN), letting the command proceed without approval while\n`sh -c` honored the inline `LD_PRELOAD` assignment.\n\nTwo-layer defense in `approval.rs`:\n\n1. Regex patterns in DANGEROUS_PATTERN_DEFS catch dangerous env-var\n   assignments (LD_PRELOAD, DYLD_INSERT_LIBRARIES, PATH, NODE_OPTIONS,\n   BASH_ENV, etc.) anywhere in the command string — including inside\n   subshells — forcing approval or denial.\n\n2. Semantic check in extract_first_bin returns None when a leading\n   env-var key matches the dangerous list, so is_safe_command and\n   matches_allowlist both fail, routing the command to the approval\n   path even if the regex layer is somehow bypassed.\n\nBenign prefixes (FOO=bar, RUST_LOG=debug) are unaffected.\nEOF\n)\"",
  "description": "Stage and commit the security fix"
}
```

> TOOL

tool_result
id: toolu_013x4SwjF8EaKPKd1SujPupq
```
[similar-papyrus ce69dd34] fix(tools): block exec approval bypass via env-var prefix injection (#814)
 1 file changed, 344 insertions(+), 1 deletion(-)
```

> TOOL

tool_use Bash
id: toolu_01LsdDyjqCuzbqxMo6Sje8qN
```json
{
  "command": "git push -u origin similar-papyrus 2>&1",
  "description": "Push branch to remote"
}
```

> TOOL

tool_result
id: toolu_01LsdDyjqCuzbqxMo6Sje8qN
```
[entire] Pushing session logs to origin...
remote: 
remote: Create a pull request for 'similar-papyrus' on GitHub by visiting:        
remote:      https://github.com/moltis-org/moltis/pull/new/similar-papyrus        
remote: 
remote: GitHub found 5 vulnerabilities on moltis-org/moltis's default branch (1 moderate, 4 low). To find out more, visit:        
remote:      https://github.com/moltis-org/moltis/security/dependabot        
remote: 
To github.com:moltis-org/moltis.git
 * [new branch]        similar-papyrus -> similar-papyrus
branch 'similar-papyrus' set up to track 'origin/similar-papyrus'.
```

> TOOL

tool_use Bash
id: toolu_01Fcu4tWnb1bpV1oQGVhRtUD
```json
{
  "command": "gh pr create --title \"fix(tools): block exec approval bypass via env-var prefix injection\" --body \"$(cat <<'EOF'\n## Summary\n\n- Fixes #814: `LD_PRELOAD=/evil.so cat /file` bypassed exec approval because `extract_first_bin` returned `cat` (a safe bin) while `sh -c` honored the inline env-var assignment\n- Adds two-layer defense in `approval.rs`:\n  1. **Regex layer**: 6 new `DANGEROUS_PATTERN_DEFS` entries catch dangerous env-var assignments (`LD_PRELOAD`, `DYLD_INSERT_LIBRARIES`, `PATH`, `NODE_OPTIONS`, `BASH_ENV`, etc.) anywhere in the command string, including subshells\n  2. **Semantic layer**: `extract_first_bin` returns `None` when a leading env-var key is dangerous, preventing safe-bin/allowlist bypass\n- Benign prefixes (`FOO=bar`, `RUST_LOG=debug`) are unaffected; wildcard `*` allowlist still overrides\n\n## Validation\n\n### Completed\n- [x] `cargo test -p moltis-tools -- approval` — 67 tests pass (40 new)\n- [x] `just format-check` — clean\n- [x] `just lint` — clean\n\n### Remaining\n- [ ] `./scripts/local-validate.sh` — full validation suite\n\n## Manual QA\n\n1. Verify `LD_PRELOAD=/evil.so cat /etc/passwd` triggers NeedsApproval in OnMiss mode\n2. Verify `LD_PRELOAD=/evil.so cat /etc/passwd` is denied in Off mode\n3. Verify `RUST_LOG=debug echo hi` still proceeds without approval\n4. Verify `sh -c \"LD_PRELOAD=/evil.so cat /file\"` is caught by regex layer\nEOF\n)\"",
  "description": "Create pull request"
}
```

> TOOL

tool_result
id: toolu_01Fcu4tWnb1bpV1oQGVhRtUD
```
https://github.com/moltis-org/moltis/pull/822
```

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/822