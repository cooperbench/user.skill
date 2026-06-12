---
name: error-paste
description: How malkoG reports failures — pastes raw terminal output with no surrounding commentary; sometimes the entire message is just the error block
---

# Error Paste

When something fails, malkoG pastes the raw terminal output as the entire message — no framing, no "I got this error", no "what went wrong?". The error block speaks for itself.

This applies to:
- Gradle build failures (full FAILED block with exception chain)
- Git command errors (stderr only: "error: cannot pull with rebase...")
- Korean-language terminal output (keytool, system tools) — pasted verbatim, untranslated
- Sometimes a one-liner question follows a raw paste: "Why I can't still reaction?"

The agent is expected to read the error, identify the problem, and fix it without being asked explicitly.

**Examples:**

(full Gradle output pasted, agent message was unrelated):
> `> Task :app:packageRelease FAILED`  
> `FAILURE: Build failed with an exception.`  
> `* What went wrong: Execution failed for task ':app:packageRelease'.`  
> `> com.android.ide.common.signing.KeytoolException: Failed to read key hackerspub from store...`

(Korean keytool output pasted after agent asked for keystore info):
> `키 저장소 유형: PKCS12`  
> `키 저장소 제공자: SUN`  
> `[...full Korean keytool -list -v output...]`

(git stderr pasted as entire message):
> `error: cannot pull with rebase: You have unstaged changes.`  
> `error: Please commit or stash them.`

(verbal failure with question):
> "Why I can't still reaction?"

> "And, For each actions for post, most of all are broken. Take a deep look again"
