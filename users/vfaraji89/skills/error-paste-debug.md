---
name: error-paste-debug
description: Reports failures by pasting raw error output verbatim — CI logs, BibTeX parse errors, compiler output — with a 2–5 word annotation appended at the end using "--".
---

When something fails, this user does not describe the failure in their own words. They paste the raw error output (sometimes hundreds of lines) and append a short note after "--" identifying the source or symptom. No markdown, no reformatting.

The note after "--" is the only original text the user contributes. It is often 3–6 words: "error of latex", "is not updated".

For very short errors (one line), the paste and annotation fit in a single short message.

**Examples**:

BibTeX parse error (short):
> "BibTeX: I was expecting a `{' or a `(' : %% @anthropic-ai/tokenizer : replicates this client-side for offline / zero-API-call use.-- error of latex"

GitHub CI output (long paste, then annotation):
> "Annotations 1 error and 12 warnings Web Platform (Build + Test) Process completed with exit code 1. Extension (Build + Test) Node.js 20 actions are deprecated. [...hundreds of lines...] -- [implicit: these are the CI failures to fix]"

Caption text (copied from paper) followed by annotation:
> "Figure 5: Daily commit activity [...full caption text...].-- is not updated"
