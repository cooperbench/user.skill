---
name: at-file-reference
description: User references source files using @relative/path notation inline in messages, and GitHub PRs/issues by full URL. Trigger: any message that points to a file or an external resource for context.
---

# at-file-reference

ravwojdyla never says "the tokenize file" or "that PR". They reference files with `@path/to/file.py` inline and GitHub resources with full URLs. No paraphrasing of what those resources contain — the reference IS the context.

## File references

Uses `@` prefix for files within the repo, matching how Claude Code's `@` file mention works:

> `"ok, in @lib/marin/src/marin/processing/tokenize/tokenize.py there's some logging..."`

> `"in @tests/integration_nomagic_test.py use click instead of draccus"`

> `"in the @.github/workflows/claude-review.yml add trigger on labelled event"`

> `"Follow @docs/recipes/fix_issue.md"`

## GitHub URL references

Full URL for PRs and issues, no `#number` shorthand:

> `"Now that we have https://github.com/marin-community/marin/pull/2986, we can use shared data again in tokenize, so we can largely revert the disk_cache change from https://github.com/marin-community/marin/pull/2984 ?"`

> `"open an issue for a flaky Iris test: https://github.com/marin-community/marin/actions/runs/22209723838/job/64241198248"`

## Notes

- Always gives the full path, not a shorthand.
- File references are lowercase, matching the actual filesystem path.
- Never describes what the file does — assumes the agent can read it.
