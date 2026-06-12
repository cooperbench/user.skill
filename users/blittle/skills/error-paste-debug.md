---
name: error-paste-debug
description: "Trigger: something breaks after a change. blittle pastes the exact error output — terminal logs, browser console errors, stack traces, or localStorage state — with minimal commentary. He names what he expected vs. what happened, often with reproduction steps."
---

# error-paste-debug

When something breaks, blittle reports failures by pasting the exact error verbatim inside a code block. He includes the URL, the reproduction steps (e.g., "hard refresh", "navigate from chapter 2 to chapter 3"), and sometimes the exact localStorage state at the time of failure. He does not paraphrase errors.

Short preamble sets context, then the dump. He may note what changed or what he expected, but the raw output is the substance.

## Examples

**Example 1** (build failure with full stack trace):
> "The build now fails with: ``` blittle@Brets-MacBook-Pro-2:~/dev/pressy(claude/seamless-chapter-transitions-phase-4⚡) » npm run build 1 ↵ > pressy-monorepo@0.0.0 build > pnpm -r --filter './packages/**' build ... packages/@pressy/components build$ tsup │ CLI Building entry: ... ESM ⚡️ Build lugin.ts(305,27): error TS2552: Cannot find name 'dirname'. Did you mean '__dirname'? ..."

**Example 2** (browser routing error with exact URL and steps):
> "If I hard refresh the page at `http://localhost:3000/books/flatland/concerning-a-stranger` (which is the last chapter)\n\nThen if I click the previous page button, I get an error loading `http://localhost:3000/books/flatland/of-recognition-by-sight?page=last`, but if I remove the `page=last` query parameter, it works. Even hard refreshing on `http://localhost:3000/books/flatland/of-recognition-by-sight?page=last` leads to an error \"Cannot GET /books/flatland/of-recognition-by-sight\""

**Example 3** (localStorage state diff showing the bug):
> "Okay, so here's the bug that remains:\n\n1. This is in localStorage: `{\"bookSlug\":\"flatland\",\"chapterSlug\":\"concerning-the-inhabitants\",\"page\":1,\"totalPages\":1,\"scrollPosition\":0}`\n2. I hard refresh the page. Local storage switches to `{\"bookSlug\":\"flatland\",\"chapterSlug\":\"concerning-the-inhabitants\",\"page\":0,\"totalPages\":1,\"scrollPosition\":0}`\n\nSo on hard refresh page load, something is forcing the page property back to 0, instead of sending the user to page 1."

**Example 4** (terse failure acknowledgment, no context):
> "i see another 500 error"

> "Ugh, still doesn't work."

> "That still didn't work :("
