> DEVELOPER

Look at the "entire explain" command with a checkpoint ID. It outputs a transcript. Add a new "entire profile" command that similarly takes a checkpoint ID and calculates the time between a user message that start a turn and the last agent message before the next user message. Output the times with the respective user message.

> AGENT

Implemented a new `entire profile` command that profiles turn durations from a checkpoint transcript.

- Added `entire profile <checkpoint-id>` in `cmd/entire/cli/profile.go`.
- Wired command into root in `cmd/entire/cli/root.go:85`.
- `profile` resolves committed checkpoint IDs by prefix (with not-found + ambiguous-prefix errors, similar to `explain` behavior).
- It computes per-turn duration as: user message timestamp → last assistant timestamp before the next user message.
- Output includes each duration with its corresponding user prompt (collapsed/truncated to one line for readability).
- Parsing supports timestamp extraction across transcript formats (JSONL/Claude-style, OpenCode export JSON, Gemini JSON when timestamps are present).

Tests added in `cmd/entire/cli/profile_test.go`:

- command construction (`TestNewProfileCmd`)
- end-to-end profiling output with expected durations (`TestRunProfile_OutputIncludesTurnDurations`)
- ambiguous checkpoint prefix handling (`TestRunProfile_AmbiguousPrefix`)

Validation run:

- `go test ./cmd/entire/cli -run 'Profile|NewProfileCmd'`
- `go test ./cmd/entire/cli`

Note: I left unrelated untracked `.opencode/` content untouched.