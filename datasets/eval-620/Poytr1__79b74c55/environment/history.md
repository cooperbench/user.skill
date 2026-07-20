> DEVELOPER

https://github.com/cilium/cilium/releases/tag/v1.18.9
Slack notification shows:
cilium v1.18.9
```
Summary of Changes
------------------

It should be:
------------------
Summary of Changes
------------------

REMEMBER every time you fix these format errors, create a UT to avoid regression, there are too many times of such issues

> AGENT

Let me explore the Slack notification formatting code to understand the issue.

> TOOL

tool_use Agent
id: toolu_bdrk_01BTNqjMPavjWxboJbvxCDPb
```json
{
  "subagent_type": "Explore",
  "description": "Explore Slack notification formatting",
  "prompt": "Find the Slack notification formatting code in this Go project. I need to understand how release notifications are formatted for Slack, specifically how the summary/report content is rendered. Look for:\n1. Slack notification sending code (likely in internal/notification/ or similar)\n2. How the report/summary text is formatted into Slack message attachments\n3. Any existing tests for Slack formatting\n\nReport file paths, line numbers, and relevant code snippets. Be thorough - check for markdown-to-slack conversion, code block rendering, and attachment formatting."
}
```

> TOOL

tool_result
id: toolu_bdrk_01BTNqjMPavjWxboJbvxCDPb
```
Perfect! Now I have a comprehensive view of the Slack notification formatting code. Let me provide you with a thorough report:

## Slack Notification Formatting Code Summary

I've found the complete Slack notification formatting implementation in your Go project. Here's what you need to know:

### 1. Main Slack Sender Code
**File:** `/home/<USER>/web3/ReleaseBeacon/internal/routing/slack.go`

#### Core Slack Implementation (Lines 18-319)

**SlackSender struct** (Line 19):
- Implements the `Sender` interface using HTTP client to post to Slack webhook URLs
- Configuration stored in webhook URL from notification channel config

**Message Format Handling** (Lines 171-291):
The code detects two message types and formats them differently:

1. **Semantic Reports** (Lines 177-181): If message body is valid JSON with a `Subject` field, it renders using Block Kit format via `buildSemanticBlocks()`
2. **Fallback Mode** (Lines 182-289): Raw release JSON or plain text, rendered using legacy attachment format

#### Semantic Report Formatting (Lines 83-169)
The `buildSemanticBlocks()` function builds compact Slack Block Kit blocks:
- **Header block** (Lines 104-106): "ProjectName vX.Y.Z — 🟢 Low Urgency" with emoji indicators
- **Urgency reason** (Lines 108-115): Only shown for CRITICAL/HIGH urgency with warning emoji
- **Changelog summary** (Lines 117-127): Rendered as markdown text block
- **Download command** […]

> AGENT

Now let me read the specific formatting code to understand the bug.

> TOOL

tool_use Read
id: toolu_bdrk_018Bbc457AuYH5voGTCRX4Hk
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/sender.go",
  "offset": 110,
  "limit": 60
}
```

> TOOL

tool_use Read
id: toolu_bdrk_01DucGqgAYndftMyE2jRKx2j
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/slack.go",
  "offset": 170,
  "limit": 130
}
```

> TOOL

tool_result
id: toolu_bdrk_01DucGqgAYndftMyE2jRKx2j
```
170	
171	func (s *SlackSender) Send(ctx context.Context, ch *models.NotificationChannel, msg Notification) error {
172		var cfg slackConfig
173		if err := json.Unmarshal(ch.Config, &cfg); err != nil {
174			return fmt.Errorf("parse slack config: %w", err)
175		}
176	
177		// Try to parse body as a SemanticReport for rich formatting.
178		var payload slackPayload
179		var report models.SemanticReport
180		if err := json.Unmarshal([]byte(msg.Body), &report); err == nil && report.Subject != "" {
181			payload.Blocks = buildSemanticBlocks(msg.Title, &report, msg)
182		} else {
183			// Fallback: source-level release notification.
184			// Use attachments for changelog so Slack auto-collapses long text
185			// with a "Show more" button.
186			var changelogText string
187			if fields, ok := parseRawBody(msg.Body); ok {
188				changelogText = fields.Changelog
189			}
190	
191			if changelogText != "" {
192				// Build title link label
193				titleLabel := msg.Title
194				if msg.Repository != "" && msg.Provider != "" {
195					titleLabel = fmt.Sprintf("%s on %s", msg.Repository, ProviderLabel(msg.Provider))
196				}
197	
198				// Build attachment text: title + version badge, then changelog
199				// converted to ASCII and wrapped in a code block. Slack
200				// auto-collapses long code blocks in attachments with a
201				// […]

> TOOL

tool_result
id: toolu_bdrk_018Bbc457AuYH5voGTCRX4Hk
```
110	// Regex patterns for markdown-to-ASCII conversion.
111	var (
112		// GitHub PR/issue URLs → #NNN ( url )
113		reGitHubPR = regexp.MustCompile(`https?://github\.com/([^/]+/[^/]+)/(pull|issues)/(\d+)`)
114		// Markdown links [text](url) → text ( url )
115		reMdLink = regexp.MustCompile(`\[([^\]]+)\]\(([^)]+)\)`)
116		// Headings ## Text → dashed ASCII box
117		reHeading = regexp.MustCompile(`(?m)^#{1,6}\s+(.+)$`)
118		// Bold **text** and __text__
119		reBoldStar = regexp.MustCompile(`\*\*(.+?)\*\*`)
120		reBoldUnderscore = regexp.MustCompile(`__(.+?)__`)
121		// Inline code `text`
122		reInlineCode = regexp.MustCompile("`([^`]+)`")
123		// HTML tags
124		reHTML = regexp.MustCompile(`<[^>]+>`)
125		// Images ![alt](url)
126		reImage = regexp.MustCompile(`!\[([^\]]*)\]\([^)]+\)`)
127	)
128	
129	// markdownToASCII converts GitHub-flavored Markdown into clean ASCII text
130	// suitable for display inside Slack/Discord code blocks.
131	func markdownToASCII(md string) string {
132		s := md
133	
134		// Strip images first (before link processing)
135		s = reImage.ReplaceAllString(s, "$1")
136	
137		// Convert GitHub PR/issue URLs to #NNN ( url )
138		s = reGitHubPR.ReplaceAllString(s, "#$3 ( $0 )")
139	
140		// Convert markdown links [text](url) → text ( url )
141		s = reMdLink.ReplaceAllString(s, "$1 ( $2 )")
142	
143		// Convert headings to ASCII art with dashes
144		s = reHeading.ReplaceAllStringFunc(s, func(match string) string {
145			parts […]

> AGENT

Now I understand the issue. The user sees:

```
Summary of Changes
------------------
```

But expects:

```
------------------
Summary of Changes
------------------
```

The heading `## Summary of Changes` in the changelog markdown gets converted by `markdownToASCII` (line 144-149). The conversion produces `dashes + "\n" + title + "\n" + dashes` which is correct. But the issue is that when wrapped in the code block on line 203, the `msg.Title` line (`*cilium* \`v1.18.9\`\n\`\`\`\n...`) puts the code block start right before the changelog — and the changelog likely starts with `Summary of Changes` as plain text (not a heading), so the regex doesn't match.

Let me check the actual changelog data for cilium to understand what's being received.

> TOOL

tool_use Read
id: toolu_bdrk_01REYCG1cxtrBpJMtLthP8HC
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/slack_test.go",
  "limit": 60,
  "offset": 287
}
```

> TOOL

tool_result
id: toolu_bdrk_01REYCG1cxtrBpJMtLthP8HC
```
287	func TestSlackSender_RawJSONFallback(t *testing.T) {
288		var received []byte
289		srv := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
290			received, _ = io.ReadAll(r.Body)
291			w.WriteHeader(http.StatusOK)
292		}))
293		defer srv.Close()
294	
295		sender := &SlackSender{Client: srv.Client()}
296		ch := &models.NotificationChannel{
297			Type:   "slack",
298			Config: json.RawMessage(`{"webhook_url": "` + srv.URL + `"}`),
299		}
300	
301		// Raw release JSON with metadata on the Notification struct (as worker now provides)
302		msg := Notification{
303			Title:       "zkSync Era",
304			Body:        `{"changelog":"Fixed wrong genesis commit","prerelease":"false","release_url":"https://github.com/matter-labs/zksync-era/releases/tag/zkos-0.29.4-rc1"}`,
305			Version:     "zkos-0.29.4-rc1",
306			ProjectName: "zkSync Era",
307			Provider:    "github",
308			Repository:  "matter-labs/zksync-era",
309			SourceURL:   "https://github.com/matter-labs/zksync-era/releases/tag/zkos-0.29.4-rc1",
310			ReleaseURL:  "https://changelogue.example.com/releases/rel-1",
311		}
312	
313		err := sender.Send(context.Background(), ch, msg)
314		if err != nil {
315			t.Fatalf("unexpected error: %v", err)
316		}
317	
318		var payload slackTestPayload
319		if err := json.Unmarshal(received, &payload); err != nil {
320			t.Fatalf("received invalid JSON: %v", err)
321		}
322	
323		// Should use attachments for changelog (auto-collapse with "Show more")
324		if len(payload.Attachments) != 1 {
325			t.Fatalf("expected 1 attachment, got %d", len(payload.Attachments))
326		}
327	
328		att := payload.Attachments[0]
329	
330		// Attachment title should show repo on provider
331		if !strings.Contains(att.Title, "matter-labs/zksync-era") {
332			t.Fatalf("expected repo […]

> AGENT

Now let me check how `markdownToASCII` handles the heading. The user reports that `Summary of Changes` appears without the leading dashes. Let me look at the test for markdownToASCII.

> TOOL

tool_use Read
id: toolu_bdrk_01RzYJht1GjujzKjschi9PXd
```json
{
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/slack_test.go",
  "offset": 462
}
```

> TOOL

tool_result
id: toolu_bdrk_01RzYJht1GjujzKjschi9PXd
```
462	func TestMarkdownToASCII(t *testing.T) {
463		tests := []struct {
464			name     string
465			input    string
466			contains []string
467			excludes []string
468		}{
469			{
470				name:     "heading converted to ASCII art",
471				input:    "## Protocol",
472				contains: []string{"--------\nProtocol\n--------"},
473				excludes: []string{"##"},
474			},
475			{
476				name:     "h1 heading",
477				input:    "# Release Notes",
478				contains: []string{"-------------\nRelease Notes\n-------------"},
479				excludes: []string{"# "},
480			},
481			{
482				name:     "GitHub PR URL converted",
483				input:    "Fixed bug https://github.com/MystenLabs/sui/pull/25364 today",
484				contains: []string{"#25364 ( https://github.com/MystenLabs/sui/pull/25364 )"},
485			},
486			{
487				name:     "GitHub issue URL converted",
488				input:    "See https://github.com/org/repo/issues/123",
489				contains: []string{"#123 ( https://github.com/org/repo/issues/123 )"},
490			},
491			{
492				name:     "markdown link converted",
493				input:    "Check [the docs](https://example.com/docs) for details",
494				contains: []string{"the docs ( https://example.com/docs )"},
495				excludes: []string{"[the docs]"},
496			},
497			{
498				name:     "bold stripped",
499				input:    "This is **important** text",
500				contains: []string{"important"},
501				excludes: []string{"**"},
502			},
503			{
504				name:     "inline code stripped",
505				input:    "Run `npm install` to start",
506				contains: []string{"npm install"},
507				excludes: []string{"`"},
508			},
509			{
510				name:     "image stripped",
511				input:    "![screenshot](https://example.com/img.png)",
512				contains: []string{"screenshot"},
513				excludes: []string{"![", "https://example.com/img.png"},
514			}, […]

> AGENT

Now I understand the full picture. The `markdownToASCII` function correctly converts `## Summary of Changes` to:
```
------------------
Summary of Changes
------------------
```

But the actual cilium release changelog likely has `Summary of Changes` as plain text (not a markdown heading with `##`), so the regex `^#{1,6}\s+(.+)$` doesn't match it, and it renders as just `Summary of Changes` without the dashes above.

Let me verify by checking cilium's actual release format.

> TOOL

tool_use WebFetch
id: toolu_bdrk_01HD8WSxWpanx7GDpdifZQSL
```json
{
  "url": "https://api.github.com/repos/cilium/cilium/releases/tags/v1.18.9",
  "prompt": "Show me just the first 500 characters of the \"body\" field from this release. I need to see how \"Summary of Changes\" is formatted - is it a markdown heading (## Summary of Changes) or plain text?"
}
```

> TOOL

tool_result
id: toolu_bdrk_01HD8WSxWpanx7GDpdifZQSL
```
The "body" field starts with:

```
Summary of Changes\r\n------------------\r\n
```

It's **not** a markdown `##` heading. Instead, it uses a plain text title with a **Setext-style underline** made of dashes (`------------------`), which Markdown renders as an `<h2>`. The format is the title on one line followed by `\r\n------------------\r\n`.
```

> AGENT

Found it. Cilium uses **Setext-style headings** (underlined with dashes), not ATX-style (`## Heading`). The regex only handles ATX-style headings. The Setext heading:

```
Summary of Changes
------------------
```

gets processed by `markdownToASCII` which strips the dashes (the `reHeading` regex doesn't match Setext), leaving just `Summary of Changes` with the dashes below eaten or kept inconsistently.

Wait — actually the dashes would remain as-is since the regex doesn't match. Let me re-examine. The issue is that the `------------------` line in the original markdown stays, but appears *below* the title. The user sees:

```
Summary of Changes
------------------
```

But expects the dashes also above. Since Setext headings aren't handled, the raw text passes through unchanged — which means the dashes are already there below. But the user's report says:

> It should show dashes above AND below

So the fix is: add Setext-style heading detection to `markdownToASCII` to produce the same `dashes\ntitle\ndashes` format as ATX headings.

Let me now write the plan.

> TOOL

tool_use Write
id: toolu_bdrk_01Tae9dvovpjkYdW2vn14Rmi
```json
{
  "file_path": "/home/<USER>/.claude/plans/scalable-coalescing-parnas.md",
  "content": "# Fix: Setext-style headings not converted in Slack code blocks\n\n## Context\nCilium (and likely other projects) use Setext-style markdown headings where the title is on one line followed by a line of dashes:\n```\nSummary of Changes\n------------------\n```\nThis is valid Markdown (renders as `<h2>`), but `markdownToASCII()` only handles ATX-style headings (`## Title`). The Setext heading passes through unconverted, producing dashes only below the title instead of the expected ASCII box with dashes above AND below.\n\n## Changes\n\n### 1. Add Setext heading regex to `internal/routing/sender.go`\nAdd a new regex pattern after the existing `reHeading` (around line 117):\n```go\nreSetextH1 = regexp.MustCompile(`(?m)^(.+)\\n[=]{2,}$`)\nreSetextH2 = regexp.MustCompile(`(?m)^(.+)\\n[-]{2,}$`)\n```\n\n### 2. Handle Setext conversion in `markdownToASCII()` (same file, ~line 143)\nAdd Setext conversion **before** the existing ATX heading conversion:\n```go\n// Convert Setext headings (Title\\n====== or Title\\n------) to ASCII box\ns = reSetextH1.ReplaceAllStringFunc(s, func(match string) string {\n    parts := reSetextH1.FindStringSubmatch(match)\n    title := strings.TrimSpace(parts[1])\n    dashes := strings.Repeat(\"-\", len(title))\n    return dashes + \"\\n\" + title + \"\\n\" + dashes\n})\ns = reSetextH2.ReplaceAllStringFunc(s, func(match string) string {\n    parts := reSetextH2.FindStringSubmatch(match)\n    title := strings.TrimSpace(parts[1])\n    dashes := strings.Repeat(\"-\", len(title))\n    return dashes + \"\\n\" + title + \"\\n\" + dashes\n})\n```\n\n**Important**: This must run before other transformations (especially before bold/link stripping) since the title line could contain markdown formatting. […]

> TOOL

tool_result
id: toolu_bdrk_01Tae9dvovpjkYdW2vn14Rmi
```
File created successfully at: /home/<USER>/.claude/plans/scalable-coalescing-parnas.md
```

> TOOL

tool_use ExitPlanMode
id: toolu_bdrk_01EWpq7KHZDcwBaBYSbmnHa8
```json
{
  "plan": "# Fix: Setext-style headings not converted in Slack code blocks\n\n## Context\nCilium (and likely other projects) use Setext-style markdown headings where the title is on one line followed by a line of dashes:\n```\nSummary of Changes\n------------------\n```\nThis is valid Markdown (renders as `<h2>`), but `markdownToASCII()` only handles ATX-style headings (`## Title`). The Setext heading passes through unconverted, producing dashes only below the title instead of the expected ASCII box with dashes above AND below.\n\n## Changes\n\n### 1. Add Setext heading regex to `internal/routing/sender.go`\nAdd a new regex pattern after the existing `reHeading` (around line 117):\n```go\nreSetextH1 = regexp.MustCompile(`(?m)^(.+)\\n[=]{2,}$`)\nreSetextH2 = regexp.MustCompile(`(?m)^(.+)\\n[-]{2,}$`)\n```\n\n### 2. Handle Setext conversion in `markdownToASCII()` (same file, ~line 143)\nAdd Setext conversion **before** the existing ATX heading conversion:\n```go\n// Convert Setext headings (Title\\n====== or Title\\n------) to ASCII box\ns = reSetextH1.ReplaceAllStringFunc(s, func(match string) string {\n    parts := reSetextH1.FindStringSubmatch(match)\n    title := strings.TrimSpace(parts[1])\n    dashes := strings.Repeat(\"-\", len(title))\n    return dashes + \"\\n\" + title + \"\\n\" + dashes\n})\ns = reSetextH2.ReplaceAllStringFunc(s, func(match string) string {\n    parts := reSetextH2.FindStringSubmatch(match)\n    title := strings.TrimSpace(parts[1])\n    dashes := strings.Repeat(\"-\", len(title))\n    return dashes + \"\\n\" + title + \"\\n\" + dashes\n})\n```\n\n**Important**: This must run before other transformations (especially before bold/link stripping) since the title line could contain markdown formatting. Actually — […]

> TOOL

tool_result
id: toolu_bdrk_01EWpq7KHZDcwBaBYSbmnHa8
```
User has approved your plan. You can now start coding. Start with updating your todo list if applicable

Your plan has been saved to: /home/<USER>/.claude/plans/scalable-coalescing-parnas.md
You can refer back to it if needed during implementation.

## Approved Plan:
# Fix: Setext-style headings not converted in Slack code blocks

## Context
Cilium (and likely other projects) use Setext-style markdown headings where the title is on one line followed by a line of dashes:
```
Summary of Changes
------------------
```
This is valid Markdown (renders as `<h2>`), but `markdownToASCII()` only handles ATX-style headings (`## Title`). The Setext heading passes through unconverted, producing dashes only below the title instead of the expected ASCII box with dashes above AND below.

## Changes

### 1. Add Setext heading regex to `internal/routing/sender.go`
Add a new regex pattern after the existing `reHeading` (around line 117):
```go
reSetextH1 = regexp.MustCompile(`(?m)^(.+)\n[=]{2,}$`)
reSetextH2 = regexp.MustCompile(`(?m)^(.+)\n[-]{2,}$`)
```

### 2. Handle Setext conversion in `markdownToASCII()` (same file, ~line 143)
Add Setext conversion **before** the existing ATX heading conversion:
```go
// Convert Setext headings (Title\n====== or Title\n------) to ASCII box
s = reSetextH1.ReplaceAllStringFunc(s, func(match string) string {
    parts := reSetextH1.FindStringSubmatch(match)
    title := strings.TrimSpace(parts[1])
    dashes := strings.Repeat("-", len(title))
    return dashes […]

> TOOL

tool_use Edit
id: toolu_bdrk_013N65rMQLBdFr7iYtxakJZG
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/sender.go",
  "old_string": "\t// Headings ## Text → dashed ASCII box\n\treHeading = regexp.MustCompile(`(?m)^#{1,6}\\s+(.+)$`)",
  "new_string": "\t// Headings ## Text → dashed ASCII box\n\treHeading = regexp.MustCompile(`(?m)^#{1,6}\\s+(.+)$`)\n\t// Setext headings: Title\\n====== (h1) or Title\\n------ (h2)\n\treSetextH1 = regexp.MustCompile(`(?m)^(.+)\\n[=]{2,}$`)\n\treSetextH2 = regexp.MustCompile(`(?m)^(.+)\\n[-]{2,}$`)"
}
```

> TOOL

tool_result
id: toolu_bdrk_013N65rMQLBdFr7iYtxakJZG
```
The file /home/<USER>/web3/ReleaseBeacon/internal/routing/sender.go has been updated successfully.
```

> AGENT

Now add the Setext conversion logic before the ATX heading conversion:

> TOOL

tool_use Edit
id: toolu_bdrk_01AK9xdSib63bufDrxXLpfmF
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/sender.go",
  "old_string": "\t// Convert headings to ASCII art with dashes\n\ts = reHeading.ReplaceAllStringFunc(s, func(match string) string {",
  "new_string": "\t// Convert Setext headings (Title\\n====== or Title\\n------) to ASCII box\n\ts = reSetextH1.ReplaceAllStringFunc(s, func(match string) string {\n\t\tparts := reSetextH1.FindStringSubmatch(match)\n\t\ttitle := strings.TrimSpace(parts[1])\n\t\tdashes := strings.Repeat(\"-\", len(title))\n\t\treturn dashes + \"\\n\" + title + \"\\n\" + dashes\n\t})\n\ts = reSetextH2.ReplaceAllStringFunc(s, func(match string) string {\n\t\tparts := reSetextH2.FindStringSubmatch(match)\n\t\ttitle := strings.TrimSpace(parts[1])\n\t\tdashes := strings.Repeat(\"-\", len(title))\n\t\treturn dashes + \"\\n\" + title + \"\\n\" + dashes\n\t})\n\n\t// Convert ATX headings to ASCII art with dashes\n\ts = reHeading.ReplaceAllStringFunc(s, func(match string) string {"
}
```

> TOOL

tool_result
id: toolu_bdrk_01AK9xdSib63bufDrxXLpfmF
```
The file /home/<USER>/web3/ReleaseBeacon/internal/routing/sender.go has been updated successfully.
```

> AGENT

Now add test cases:

> TOOL

tool_use Edit
id: toolu_bdrk_012cZVDg9iAPW2GgFgvMhc6E
```json
{
  "replace_all": false,
  "file_path": "/home/<USER>/web3/ReleaseBeacon/internal/routing/slack_test.go",
  "old_string": "\t\t{\n\t\t\tname:  \"full changelog example\",",
  "new_string": "\t\t{\n\t\t\tname:     \"setext h2 heading (dashes)\",\n\t\t\tinput:    \"Summary of Changes\\n------------------\",\n\t\t\tcontains: []string{\"------------------\\nSummary of Changes\\n------------------\"},\n\t\t},\n\t\t{\n\t\t\tname:     \"setext h1 heading (equals)\",\n\t\t\tinput:    \"Release Notes\\n=============\",\n\t\t\tcontains: []string{\"-------------\\nRelease Notes\\n-------------\"},\n\t\t},\n\t\t{\n\t\t\tname:  \"cilium-style changelog with setext heading\",\n\t\t\tinput: \"Summary of Changes\\n------------------\\n\\n* Fixed a bug in endpoint routing\\n* Updated Hubble version to v1.2.3\",\n\t\t\tcontains: []string{\n\t\t\t\t\"------------------\\nSummary of Changes\\n------------------\",\n\t\t\t\t\"Fixed a bug in endpoint routing\",\n\t\t\t},\n\t\t},\n\t\t{\n\t\t\tname:  \"full changelog example\","
}
```

> TOOL

tool_result
id: toolu_bdrk_012cZVDg9iAPW2GgFgvMhc6E
```
The file /home/<USER>/web3/ReleaseBeacon/internal/routing/slack_test.go has been updated successfully.
```

> AGENT

Now run the tests:

> TOOL

tool_use Bash
id: toolu_bdrk_01BJwuuex3FDS85jGj9N4ULk
```json
{
  "command": "go test -v -run TestMarkdownToASCII ./internal/routing/...",
  "description": "Run markdownToASCII tests"
}
```

> TOOL

tool_result
id: toolu_bdrk_01BJwuuex3FDS85jGj9N4ULk
```
=== RUN   TestMarkdownToASCII
=== RUN   TestMarkdownToASCII/heading_converted_to_ASCII_art
=== RUN   TestMarkdownToASCII/h1_heading
=== RUN   REDACTED
=== RUN   REDACTED
=== RUN   TestMarkdownToASCII/markdown_link_converted
=== RUN   TestMarkdownToASCII/bold_stripped
=== RUN   TestMarkdownToASCII/inline_code_stripped
=== RUN   TestMarkdownToASCII/image_stripped
=== RUN   TestMarkdownToASCII/HTML_tags_stripped
=== RUN   TestMarkdownToASCII/setext_h2_heading_(dashes)
=== RUN   TestMarkdownToASCII/setext_h1_heading_(equals)
=== RUN   REDACTED
=== RUN   REDACTED
--- PASS: TestMarkdownToASCII (0.00s)
    --- PASS: TestMarkdownToASCII/heading_converted_to_ASCII_art (0.00s)
    --- PASS: TestMarkdownToASCII/h1_heading (0.00s)
    --- PASS: REDACTED (0.00s)
    --- PASS: REDACTED (0.00s)
    --- PASS: TestMarkdownToASCII/markdown_link_converted (0.00s)
    --- PASS: TestMarkdownToASCII/bold_stripped (0.00s)
    --- PASS: TestMarkdownToASCII/inline_code_stripped (0.00s)
    --- PASS: TestMarkdownToASCII/image_stripped (0.00s)
    --- PASS: TestMarkdownToASCII/HTML_tags_stripped (0.00s)
    --- PASS: TestMarkdownToASCII/setext_h2_heading_(dashes) (0.00s)
    --- PASS: TestMarkdownToASCII/setext_h1_heading_(equals) (0.00s)
    --- PASS: REDACTED (0.00s)
    --- PASS: REDACTED (0.00s)
PASS
ok  	github.com/sentioxyz/changelogue/internal/routing	0.629s
```

> AGENT

All 13 tests pass. Let me also run the full routing test suite:

> TOOL

tool_use Bash
id: toolu_bdrk_016rWX82Rm1DaG9zeHysj2a7
```json
{
  "command": "go test ./internal/routing/... 2>&1 | tail -5",
  "description": "Run all routing tests"
}
```

> TOOL

tool_result
id: toolu_bdrk_016rWX82Rm1DaG9zeHysj2a7
```
ok  	github.com/sentioxyz/changelogue/internal/routing	0.804s
```

> AGENT

All passing. 

**Fix**: Added Setext-style heading support (`Title\n======` and `Title\n------`) to `markdownToASCII()` in `internal/routing/sender.go`. Cilium and other projects use this markdown heading format, which was passing through unconverted — producing dashes only below the title instead of the expected ASCII box with dashes above and below.

**Tests added**: 3 new cases in `TestMarkdownToASCII` — Setext h1, Setext h2, and a full cilium-style changelog with Setext heading followed by bullet points.