---
# Preferences — AbrahamGeorge8547

## Pushback Distribution

| Type | Rate |
|------|------|
| Correction | 46.6% |
| Non-pushback (acceptance) | 40.9% |
| Failure report | 11.9% |
| Rejection | 0.6% |

## What Triggers Corrections

1. **Agent takes an online-only shortcut** instead of the offline-first sync-meta path. Abraham immediately redirects: "so this path should be removed. its does not follow offline first principles."

2. **Agent declares "all tasks complete" and summarizes** before Abraham has sent the next step. He ignores the summary entirely and sends the next concrete sub-task instruction.

3. **Agent asks a clarifying question** when the answer is already in logs/captures Abraham gave. He responds with a direct pointer: "no i buitl and tested it, /tmp/custom_channel_test/captures/ here you will find the captured events."

4. **Agent uses release build instead of debug build**: "we need a debug build not the release build"

5. **Agent puts protocol logic in the Lua app layer**: "sync_meta should not go through lua layer its protocol owned"

6. **Agent adds verbose logging or long fields to console output**: "the authority permit should be truncated, its taking a lot of console space."

7. **Agent explains what it's doing rather than just doing it**: When Abraham says "yes please" or "lets continue", he wants the next action, not more explanation.

8. **Agent conflates static and dynamic layer paths** or applies the wrong authorization model.

## What Triggers Failure Reports

- Test timeouts (pastes full traceback + session socket info)
- JSONL capture showing 0 events or wrong event counts
- App crashes / Slint panics on main thread
- Missing data on viewer side ("only alice data goes to them")

## What Satisfies (non-pushback triggers)

- Agent implements a step exactly as specified in the plan without deviation
- Integration test passes: "kay now this works"
- Capture analysis confirms expected event flow
- Clean build with correct test count

## Workflow Habits

- **Plan-first**: Writes (or pastes) a detailed multi-section plan before asking for implementation. Plan often includes exact Rust structs and method signatures.
- **Step-by-step execution**: Sends plan sections one at a time as mid-session prompts, not all at once.
- **Capture-driven debugging**: Always has a JSONL event capture system running. Refers to `/tmp/<test>/captures/` paths for debugging.
- **Integration tests over unit tests**: Prefers reproducing bugs in integration tests before fixing: "lets reproduce the same in our integration test only lets not use the e2e tests for this for now."
- **tmux sessions**: Test framework keeps sessions alive; Abraham references them by name for log inspection.
- **Breaking-change tolerance**: "we are totally okay with breaking changes, nothing is in production yet."
- **Dead code awareness**: After a refactor, asks to identify and remove dead code: "after confirming everything works we will remove dead code or dead flows."
- **Documentation updates**: After implementation, prompts to update docs: "so we need to update the documentations with this right."

## Tool/Stack Preferences

- **Build**: Debug builds only during active development (`cargo build`, not `--release`)
- **Test runner**: `integration_tests` crate (Rust) for protocol tests; Python `e2e_tests/` for full-stack tests
- **Observability**: JSONL event captures via a custom capture system; `tmux` for log inspection
- **No mocking at protocol layer**: Prefers real peer connections in integration tests
- **Lua for app logic, Rust for protocol**: Strict separation — anything protocol-owned must stay in Rust
