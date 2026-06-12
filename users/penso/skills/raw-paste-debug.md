---
name: raw-paste-debug
description: Reports CI or test failures by pasting the full raw terminal output with zero commentary. Triggered any time a local-validate run, cargo test, or E2E test produces failures. penso never summarizes or explains the failure — the paste is the entire message.
---

## Behavior

When `./scripts/local-validate.sh <PR#>` or a test run fails, penso copies the entire terminal output — including the passing test lines, timing, STDERR, diff hunks, and error trace — and sends it as his next message. No introductory sentence. No "here's the error". No explanation of what he tried. The block of output starts immediately.

The output may be hundreds of lines. It always includes:
- Lines of `PASS [Ns] crate::test::name`
- One or more `TRY N FAIL [Ns] crate::test::name` blocks with STDOUT/STDERR
- The panic message and location
- Possibly retry attempts (`RETRY 2/3`, `RETRY 3/3`)
- Format diffs (from `cargo fmt --check`)
- Clippy errors with suggestion lines

The agent is expected to read the failure, identify the root cause, fix it, and push — without being asked explicitly.

## Verbatim example

> "PASS [ 0.019s] moltis-agents model::tests::convert_skips_metadata_fields
> PASS [ 0.018s] moltis-agents model::tests::convert_skips_notice_entries
> …
> TRY 1 FAIL [ 0.019s] moltis-agents model::tests::convert_skips_tool_result_entries
> ──── TRY 1 STDOUT: …
> thread 'model::tests::convert_skips_tool_result_entries' (14562115) panicked at crates/agents/src/model.rs:721:9:
> assertion `left == right` failed
>   left: 3
>  right: 2
> …"

## Short-form variant

When the CI run URL is available instead of local output:
> "CI failed: https://github.com/moltis-org/moltis/actions/runs/22933477161/job/66559788743"
