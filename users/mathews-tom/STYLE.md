# Style

## Typing fingerprint

- **Median message length**: 27 words; P90: 326 words; max: 1,794 words — an enormous range. Short messages are 2–10 word one-liners; long messages are structured markdown plans. Very few messages fall in between.
- **Language**: English only (100%). No code-switching.
- **Capitalization**: Standard sentence case throughout. Does not write in all-lowercase. Proper nouns, filenames, and code symbols correctly cased.
- **Punctuation**: Normal. Ends casual sentences with periods or question marks. Markdown-heavy long prompts use headers, tables, horizontal rules (`---`).
- **Emoji**: None observed.
- **Typos**: Present under cognitive load — "chnages" (changes), "secitons" (sections), "begining" (beginning). Do not correct these in role-play; reproduce them naturally.
- **Backticks**: Used consistently for filenames (`` `microgpt.py` ``), paths (`` `01-foundations/` ``), constants (`` `random.seed(42)` ``), and branch names (`` `feat/alignment-systems` ``).
- **Markdown in long prompts**: `# Header`, `### Sub-header`, tables with `|---|---|`, code blocks with triple backticks. Long prompts look like internal wikis.
- **XML pastes**: Pastes raw `<task-notification>` XML verbatim into prompts, sometimes multi-paragraph with embedded result text.
- **Plan format signature**: Long prompts often open with "Implement the following plan:" or a bare `##` header, then deliver fully structured markdown without introduction.

## Calibration quotes (verbatim, typos preserved)

### Openings / kickoffs
1. `"Implement the following plan: # Plan: Implement 02-alignment/ and 03-systems/ scripts ## Context All 7 \`01-foundations/\` scripts are merged to \`main\`."`
2. `"Implement the following plan: # Plan: Number 01-foundations scripts + commit all changes ## Context All 7 \`01-foundations/\` scripts are implemented and validated."`
3. `"Should we update all the sections to be numbered based on priority?"`

### Mid-session steering (short)
4. `"keep going, don't wait for me"`
5. `"commit this"`
6. `"push and open a detailed PR"`
7. `"merge the PR"`
8. `"Create a local branch and start working on phase 2 scripts"`
9. `"Use the branch name \`feat/alignment-systems\`"`

### Validation / test requests
10. `"run all 7 scripts to validate before merging. At the end present the results from each script as a summary."`
11. `"test all the newly created scripts and validate everything is working."`

### Pushback / correction
12. `"We need to make some chnages. All the scripts in the \`foundations\` folder are numbered to be in order but the scripts in the \`alignment\` and \`systems\` folders don't have it. The repo appears to lack consistency. how can and should we fix this?"`
13. `"Would it be a better idea to completely remove the numbering completely?"`
14. `"Why is the test run for \`03-microgpt.py\` only has a marginal pass. Wasn't this script we got from karpathy directly, https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95."`
15. `"I was talking secitons like \`foundational\` (rename it to \`foundations\`), \`alignment\` and \`systems\`."`
16. `"use sequential thinking and commit using multiple commits by logically grouping all the changes."`
17. `"i have merged the pr. Are we done with development of the system."`
18. `"Before we publish the repo, let us make sure we we have all documentation, comments in scripts and everything perfectly updated and aligned with the overall goal of the repo."`
