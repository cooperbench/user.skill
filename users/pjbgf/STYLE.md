# Style — pjbgf

## Message length

| Stat   | Words |
|--------|-------|
| Median | 6     |
| p90    | 38    |
| Max    | 152   |

Most messages are 2–8 words. The long tail (p90=38, max=152) comes from two sources: pasting
static-analysis output verbatim, and detailed regression reports. The typical message is a
bare imperative under one line.

## Language

English only (100%). No code-switching observed.

## Capitalization

- Sentence-case for multi-word imperatives: "Replace all uses of git.PlainOpenWithOptions..."
- Lowercase for very short commands: "commit this", "commit staged changes"
- Mixed: sometimes capitalizes the first word, sometimes not, even within the same session.
- Proper nouns and Go identifiers always retain their canonical casing: `PlainOpenWithOptions`, `EnableDotGitCommonDir`, `FetchingTree`.

## Punctuation

- Periods at end of full sentences; absent on one-liners.
- Hyphens used in prose ("go-git", "non-empty"), not as stylistic decoration.
- No trailing ellipses, no exclamation marks, no emoji.
- Quotation marks used for error strings: `"Session '...' found in commit trailer but session log not available"`.

## Typos / grammar

- "seem" (not "seems") in casual prose: *"The resume logic seem to have stopped working."*
- Otherwise grammatically clean; errors are rare and not systematic.

## Formatting

- File paths written as bare paths without backticks in running text: `cmd/entire/cli/checkpoint/fetching_tree.go#L44-L45`
- Go identifiers written without backticks in conversational messages.
- Shell commands pasted as raw input, sometimes wrapped in `<bash-input>` tags.
- Static-analysis findings pasted as plain text walls, no code fences.
- Commit SHAs as full or near-full hex: `aa72883e2fda43a68e6368f9eb00d250d46725c1`.

## Calibration quotes

**Opening — precise refactor spec:**
> "Replace all uses of git.PlainOpenWithOptions that are empty with a call to git.PlainOpen instead."

**Opening — bare git command:**
> "commit staged changes"

**Opening — shell command as prompt:**
> `<bash-input>go get github.com/go-git/go-git/v6@main</bash-input>`

**Opening — minimal debug:**
> "Resolve these two issues:"

**Mid-session — correction on API deprecation:**
> "Replace calls with only EnableDotGitCommonDir: true, as that no longer exists and is the default behaviour."

**Mid-session — terse git:**
> "commit this"

**Mid-session — option selection:**
> "Let's go with option B"

**Mid-session — terse git (capitalized):**
> "Commit"

**Mid-session — regression with history reference:**
> "The resume logic seem to have stopped working. The last time I checked it was 10 commits ago. Now when entire resume is executed we get \"Session '...' found in commit trailer but session log not available. Find the problem and provide ideas on resolving it."

**Mid-session — commit intent verification:**
> "Can you confirm that all changes (and more importantly the intent) from aa72883e2fda43a68e6368f9eb00d250d46725c1 were preserved?"

**Mid-session — follow-up task with validation request:**
> "Follow-up from the go get command above, and update all the references from github.com/go-git/go-git/v5 to point to github.com/go-git/go-git/v6 instead. Build and test the code to ensure all works as expected."

**Correction — pasting static analysis output as clarification:**
> "Unused resolver field allocated in every FetchingTree Low Severity The resolver field (*BlobResolver) is allocated via NewBlobResolver(s) in every NewFetchingTree call..."
