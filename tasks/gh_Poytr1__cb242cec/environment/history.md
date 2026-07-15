> DEVELOPER

https://github.com/cilium/cilium/releases/tag/v1.18.9 Slack notification shows: cilium v1.18.9 ``` Summary of Changes ------------------ It should be: ------------------ Summary of Changes ------------------ REMEMBER every time you fix these format errors, create a UT to avoid regression, there are too many times of such issues

> AGENT

Let me explore the Slack notification formatting code to understand the issue.

> AGENT

Now let me read the specific formatting code to understand the bug.

> AGENT

Now I understand the issue. The user sees: ``` Summary of Changes ------------------ ``` But expects: ``` ------------------ Summary of Changes ------------------ ``` The heading `## Summary of Changes` in the changelog markdown gets converted by `markdownToASCII` (line 144-149). The conversion produces `dashes + "\n" + title + "\n" + dashes` which is correct. But the issue is that when wrapped in the code block on line 203, the `msg.Title` line (`*cilium* \`v1.18.9\`\n\`\`\`\n...`) puts the code block start right before the changelog — and the changelog likely starts with `Summary of Changes` as plain text (not a heading), so the regex doesn't match. Let me check the actual changelog data for cilium to understand what's being received.

> AGENT

Now let me check how `markdownToASCII` handles the heading. The user reports that `Summary of Changes` appears without the leading dashes. Let me look at the test for markdownToASCII.

> AGENT

Now I understand the full picture. The `markdownToASCII` function correctly converts `## Summary of Changes` to: ``` ------------------ Summary of Changes ------------------ ``` But the actual cilium release changelog likely has `Summary of Changes` as plain text (not a markdown heading with `##`), so the regex `^#{1,6}\s+(.+)$` doesn't match it, and it renders as just `Summary of Changes` without the dashes above. Let me verify by checking cilium's actual release format.

> AGENT

Found it. Cilium uses **Setext-style headings** (underlined with dashes), not ATX-style (`## Heading`). The regex only handles ATX-style headings. The Setext heading: ``` Summary of Changes ------------------ ``` gets processed by `markdownToASCII` which strips the dashes (the `reHeading` regex doesn't match Setext), leaving just `Summary of Changes` with the dashes below eaten or kept inconsistently. Wait — actually the dashes would remain as-is since the regex doesn't match. Let me re-examine. The issue is that the `------------------` line in the original markdown stays, but appears *below* the title. The user sees: ``` Summary of Changes ------------------ ``` But expects the dashes also above. Since Setext headings aren't handled, the raw text passes through unchanged — which means the dashes are already there below. But the user's report says: > It should show dashes above AND below So the fix is: add Setext-style heading detection to `markdownToASCII` to produce the same `dashes\ntitle\ndashes` format as ATX headings. Let me now write the plan.

> AGENT

Now add the Setext conversion logic before the ATX heading conversion:

> AGENT

Now add test cases:

> AGENT

Now run the tests:

> AGENT

All 13 tests pass. Let me also run the full routing test suite:

> AGENT

All passing. **Fix**: Added Setext-style heading support (`Title\n======` and `Title\n------`) to `markdownToASCII()` in `internal/routing/sender.go`. Cilium and other projects use this markdown heading format, which was passing through unconverted — producing dashes only below the title instead of the expected ASCII box with dashes above and below. **Tests added**: 3 new cases in `TestMarkdownToASCII` — Setext h1, Setext h2, and a full cilium-style changelog with Setext heading followed by bullet points.