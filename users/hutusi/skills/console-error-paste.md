---
name: console-error-paste
description: >
  Trigger: hutusi observes an error or warning in Chrome DevTools console, a build failure,
  or a lint failure. He pastes the message verbatim with minimal or zero framing — the paste
  IS the bug report.
---

hutusi reports failures by pasting the exact text from Chrome DevTools, the terminal, or a test runner. He rarely adds "please fix this" — the paste implies it. For build/lint failures, he may add only the command name that failed ("bun run lint failed").

For browser console issues, he includes the full warning/error text including URLs. For build errors, he includes the stack trace excerpt. He does not summarize or paraphrase.

**Examples:**

> "When running 'bun run dev' and inspecting the homepage in Chrome, there is one error and one warning. The error is: 'Content Security Policy of your site blocks the use of eval in JavaScript.' The warning is: 'Deprecated feature used; the Shared Storage API is deprecated and will be removed in a future release.'"

> "there is a warning of console when inspect the homepage: Image with src \"/images/vibrant-waves.avif\" was detected as the Largest Contentful Paint (LCP). Please add the `loading=\"eager\"` property if this image is above the fold.\nRead more: https://nextjs.org/docs/app/api-reference/components/image#loading"

> "when open posts page, the console of dev tools shows warning: Detected `scroll-behavior: smooth` on the `<html>` element..."

> "'bun run build' failed: Creating an optimized production build ...\nError: Can't resolve 'katex/dist/katex.min.css' in '...'"

> "\"bun run validate\" failed"

> "bun run lint failed"

**Pattern**: Either paste verbatim (for detailed errors) or state `"<command>" failed` (for short failures). No preamble, no "please fix", no paraphrasing.
