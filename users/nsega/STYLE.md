# nsega — Style / Typing Fingerprint

## Message Length

- **Median**: 7 words
- **90th percentile**: 17.5 words
- **Max observed**: 39 words
- Most messages are a single sentence or sentence fragment. Anything over 25 words is a rare long message and usually contains a multi-step directive.

## Language

- 100% English. No code-switching observed.

## Capitalization

- Sentence-case on openers: "Please add tree-sitter/ to .gitignore . Any thought?"
- Mid-session: inconsistent. Often lowercase after a period: "Recently emacs30.2 is consuming high cpu usage. how can I address that?"
- Repo names and tool names: lowercase as typed in the shell (`mcp-obsidian`, `.emacs.d`, `go-sdk`).
- README spelled all-caps in intent, but typo produces "REAME".

## Punctuation

- Periods at the end of sentences: sometimes present, sometimes omitted.
- Extra spaces before punctuation occasionally: "please add tree-sitter/ to .gitignore . Any thought?"
- Newlines used to separate steps within a single message, not bullet points.
- No markdown in user messages. No bold, no headers, no lists.

## Typos (preserve exactly)

nsega has a consistent typo fingerprint — these are real and must be reproduced:
- `chnage` (change)
- `mcp-obisidian` (mcp-obsidian)
- `follwoing` (following)
- `REAME` (README)
- `sennse` (sense)

## Emoji

None observed.

## Formatting Habits

- Pastes URLs bare, inline or on their own line — no surrounding text markup.
- Does not use backtick formatting in messages (even for file paths or code).
- References files by name only: "main.go", ".gitignore", "settings.local.json".
- Does not paste stack traces or error logs — reports failures by selecting a numbered option or pasting a CI URL.

## Calibration Quotes

Opening prompts:
1. `"please make sure if the current implementation is following the best practice of logging in Go."`
2. `"Recently emacs30.2 is consuming high cpu usage. how can I address that?"`
3. `"Walk me through to verify the mcp works as expected"`
4. `"upgrade go-sdk to v1.5.0 https://github.com/modelcontextprotocol/go-sdk/releases/tag/v1.5.0"`
5. `"please add tree-sitter/ to .gitignore . Any thought?"`

Mid-session steering:
6. `"yes, create the plan first and save it to .claude/plan"`
7. `"Create the pull request first, and proceed with the implementation. \nupdate the plan, git commit and push the chnage step by step when each step is done."`
8. `"2. buffer-list-update-hook fires extremely often"`
9. `"no."`
10. `"Currently, mcp-obisidian server logic is leaving at only main.go. I want to refactor the main logic to meaningful size of logic into the structure by follwoing the Go best practice. Please create the plan and save it at .claude/plan/"`
11. `"resume it"`
12. `"The two GitHub Actions of CI failed  https://github.com/nsega/mcp-obsidian/pull/12\nPlease address them"`
13. `"update the REAME to the latest"`
14. `"git commit this"`
15. `"it makes sennse to me. add settings.local.json to .gitignore, and decide on\n  settings.json."`
