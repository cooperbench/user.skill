> DEVELOPER

Read https://github.com/moltis-org/moltis/issues/813 and plan for a fix, add a test

> AGENT

Good, clear issue. Let me explore the relevant code.

> AGENT

Now let me check how `extract_document_file` is used in the implementation to see the full call path.

> AGENT

Now I have the full picture. Here's the plan: ## Issue #813: Plan **Root cause**: In `extract_document_file()` (`media.rs:123-143`), when Telegram sends `mime_type: null` or `"application/octet-stream"`, the code uses that value as-is. The existing `mime_from_extension()` helper in `crates/media/src/mime.rs` is never consulted, so `.md`, `.toml`, `.yaml`, etc. all get `application/octet-stream` → `is_supported_document_type()` returns `false` → file silently dropped. **Fix** (single-function change in `extract_document_file`): When the resolved MIME is `application/octet-stream`, derive a better MIME from the filename extension via `moltis_media::mime::mime_from_extension`. This matches the issue's suggested fix exactly. ```rust // In extract_document_file(), after computing `raw`: let media_type = if raw == "application/octet-stream" { d.document.file_name.as_deref() .and_then(|name| name.rsplit('.').next()) .and_then(moltis_media::mime::mime_from_extension) .unwrap_or(&raw) } else { &raw }; ``` **Test**: Add a unit test `extract_document_file_infers_mime_from_extension_for_octet_stream` that sends a document with `mime_type: "application/octet-stream"` and `file_name: "notes.md"`, asserts `media_type == "text/markdown"`. Let me check that `moltis_media` is already a dependency of the telegram crate.

> AGENT

Good, already a dependency. Let me implement the fix.

> AGENT

Now let me check what's at the end of the test file to see the imports and add the new test.

> AGENT

Let me find the end of the media test file and add the new test after the existing `extract_document_file_defaults_media_type_when_missing` test (since that's the most related one).

> AGENT

Now I need to update the existing test (`.bin` with no mime should still be `application/octet-stream`) and add new tests for the extension fallback. The existing test is still correct — `.bin` has no known MIME mapping, so it stays `application/octet-stream`.

> AGENT

Now let me verify the MIME values that `mime_guess` returns for these extensions to make sure the test expectations are correct.

> AGENT

Let me quickly check what `mime_guess` actually returns for `md`, `toml`, `yaml`, `yml` since the exact string matters.

> AGENT

Fix the MIME expectation for `.toml`:

> AGENT

All 5 tests pass. Now I should also consider: `.toml` and `.yaml` resolve to `text/x-toml` and `text/x-yaml`, but `should_inline_document_text()` doesn't include those. Let me check if those should be inlinable too — the issue says these are "all likely affected."

> AGENT

The `should_inline_document_text` function doesn't cover `text/x-toml` or `text/x-yaml`. These are plain-text config formats that should absolutely be inlinable. The fix for the main issue (#813) is the MIME detection in `extract_document_file`, but to fully solve the ".toml/.yaml are also affected" part, I should add those to `should_inline_document_text` as well. Let me also add a broader `text/*` catch — actually, that would be too broad. Let me just add the specific types.

> AGENT

Now run the full telegram test suite to make sure nothing is broken.

> AGENT

All 112 tests pass. Let me also run a quick format and clippy check on the changed files.

> AGENT

Clippy passes clean. Here's a summary of the changes: ## Summary **Issue**: Telegram sends `application/octet-stream` (or no MIME type) for files it doesn't recognise — `.md`, `.toml`, `.yaml`, etc. The handler saw an unsupported MIME and silently dropped the file. **Two changes in `crates/telegram/src/handlers/media.rs`:** 1. **`extract_document_file()`** (line ~123): When the resolved MIME is `application/octet-stream`, derive a better MIME from the filename extension using the existing `moltis_media::mime::mime_from_extension` helper. If that returns `None` (truly unknown extension like `.bin`), keep `application/octet-stream`. 2. **`should_inline_document_text()`** (line ~255): Added `text/csv`, `text/x-toml`, `text/x-yaml`, `application/toml`, `application/yaml`, `application/x-yaml` — config/data formats that are plaintext and should be inlined, covering the additional extensions the issue mentions. **Three new tests in `crates/telegram/src/handlers/tests/media.rs`:** | Test | What it verifies | |------|-----------------| | `extract_document_file_infers_mime_from_extension_for_octet_stream` | `.md` with `application/octet-stream` → `text/markdown`, and `is_supported_document_type` returns `true` | | `extract_document_file_infers_mime_for_other_text_extensions` | `.toml`, `.yaml`, `.yml`, `.txt`, `.json` all get correct MIME from extension | | `extract_document_file_keeps_explicit_mime_when_not_octet_stream` | Explicit MIME (e.g. `image/jpeg`) is never overridden | All 112 telegram tests pass, formatting and clippy are clean.

> TOOL

<task-notification> <task-id>b601pi83r</task-id> <tool-use-id>REDACTED</tool-use-id> <output-file>/private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-abalone-place/36c89018-c8ec-4ad7-a7a7-2fe78ec0b3a3/tasks/b601pi83r.output</output-file> <status>completed</status> <summary>Background command "Run clippy lint check" completed (exit code 0)</summary> </task-notification> Read the output file to retrieve the result: /private/tmp/claude-501/-Users-penso--superset-worktrees-moltis-abalone-place/36c89018-c8ec-4ad7-a7a7-2fe78ec0b3a3/tasks/b601pi83r.output

> AGENT

Already retrieved that output — clippy passed clean. The fix is ready for commit whenever you'd like.

> DEVELOPER

commit push create a PR

> AGENT

PR created: https://github.com/moltis-org/moltis/pull/819