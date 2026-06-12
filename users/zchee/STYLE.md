# Style — zchee

## Message length
- **Human-typed prompts**: 1–6 words (median ~3 words when writing himself)
- **Stat median of 34 words**: inflated by OMX system context injections (`<environment_context>`, `<state_management>`, etc.) that are machine-generated, not zchee's prose
- **p90 of 917 words**: OMX large context dumps (AGENTS.md, keyword tables, skill definitions)
- When zchee writes, aim for ≤8 words unless pasting an OMX status block or quoted skill invocation

## Language and code-switching
- English only in the dataset; his OMX config explicitly says agents must respond in English
- English is non-native: missing articles, dropped copulas, inverted syntax, occasional malapropisms
- He does not switch to Japanese mid-session in the captured data

## Capitalization
- Short commands: mixed / lowercase: `do 1`, `continue`, `do it`, `$commit`, `push to remote`
- Mid-sentence corrections: sentence case but inconsistent: `"WHat is next step?"`, `"Stil \`./zig-out/bin/agentmux new -s test\`, the cursor doesn't show the bar style. Fix it."`
- Backtick-wrapped code is always exact (case-sensitive paths, binary names, build commands)

## Punctuation
- Periods are rare in short commands; used when quoting a skill invocation argument
- Question marks appear in confusion checks: `"WHat is next step?"`, `"Do we need the uncommitted files?"`
- No exclamation marks observed
- No emoji

## Typos (preserve exactly)
- `WHat` (capital H mid-word)
- `priorityp` (extra p)
- `Stil` (missing l)
- `taks` (in OMX config — his own writing that slipped in)
- `Please forgot` (should be "forget")
- `nothing work` (missing s)

## Formatting habits
- **Backticks** for any binary, path, command, or code token: `` `./zig-out/bin/agentmux new -s test` ``, `` `zig build test` ``, `` `$OMX_TEAM_STATE_ROOT/...` ``
- **Skill sigils** prefixed with `$`: `$commit`, `$ralplan`, `$ultrawork`, `$autopilot`, `$deep-interview`, `$plan`, `$cancel`, `$team`
- **Commit range syntax**: `` `c509f558217f...447d59e6c487` `` — backtick-wrapped git hash range
- **OMX relay blocks**: pastes `[OMX_TMUX_INJECT]` messages verbatim, sometimes doubled
- **Quoted skill args**: `$ultrawork "do work both of 'X' and 'Y' using Zig's \`std.Io\`"`

## Verbatim calibration examples

**Openings (task starts):**
1. `$commit`
2. `Squash \`c509f558217f...447d59e6c487\` commits`
3. `$skill-creator Zsh completion script skill.`
4. `Cleanup (or squash) 4e25c18e1a16...7bb2a376ad7a commits. Splits if necessary.`
5. `Convert https://github.com/vercel-labs/agent-browser/tree/main/skills/agent-browser to Codex Skill Style`

**Mid-session steering:**
6. `do 1`
7. `continue`
8. `WHat is next step?`
9. `$ralplan`
10. `push to remote`
11. `high priority`
12. `do it`
13. `continue to high priorityp`

**Corrections and redirects:**
14. `When \`./zig-out/bin/agentmux new -s test\`, the cursor style is shape. Fix to use the block style`
15. `No. In \`tmux\`, will open the new window. Current \`agentmux\` nothing work.`
16. `Please forgot 'GPU rendering', and do work 'real-terminal trace command and the log-reading flow for your live manual repro.'`
17. `I do 'real-home, real-terminal validation', but still very slow launch zsh and key-input. Investigate it.\n- I thought affected by GPU rendering, not?`
18. `Do we need the uncommitted file changes?`
