---
name: diff-embed
description: How musicofhel delivers the code to be reviewed — the full git diff is pasted verbatim in a fenced code block at the end of the prompt, under a ## Diff to Review header. The diff includes all changed files, including lock files and test files.
---

Every prompt ends with a `## Diff to Review` section containing the raw `git diff` output in a fenced code block (triple backtick, no language tag).

```
## Diff to Review
```
diff --git a/path/to/file b/path/to/file
index abc1234..def5678 100644
--- a/path/to/file
+++ b/path/to/file
@@ -line,count +line,count @@
 context line
-removed line
+added line
```
```

The diff is never summarized or filtered — the pipeline passes the full raw output of `git diff`. This means:
- Lock files (uv.lock) are included even when they are the only non-substantive change
- Test files are included alongside production code
- Multi-file diffs (e.g., implementation + tests + lock file) are sent as a single concatenated diff

**Example — multi-file diff including lock file** (from the SQL search endpoint session):
> The diff included `uv.lock` (107 new lines of package hashes) followed by the actual `app.py` change adding the SQL endpoint. The pipeline does not strip the lock file before sending.

**Example — single-line diff** (README typo):
```
diff --git a/README.md b/README.md
index c2cc4fa..1bee660 100644
--- a/README.md
+++ b/README.md
@@ -5,7 +5,7 @@ A prompt evaluation benchmark for testing LLM outputs.
 ## Installation
 
 ```bash
-pip instal oo-test-project
+pip install oo-test-project
 ```
```

The diff is always the last element of the prompt. Nothing follows it.
