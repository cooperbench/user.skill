---
name: raw-log-paste
description: Reports CI/build failures by pasting the raw GitHub Actions log output verbatim — including emoji status icons, whitespace, and exit code lines — with little or no surrounding commentary. Triggered when a CI step fails after the agent's most recent push.
---

itsmaleen's primary debugging feedback mechanism is pasting the exact GitHub Actions log output. There is no paraphrasing, no explanation of what they think went wrong, and often no sentence before the paste. The log speaks for itself.

Occasionally a very brief lead-in precedes the paste ("got errors in package and sign app", "failing at verify signed app", "here's let logs"), but it never contains new information — just a label for the block that follows.

The paste includes emoji status indicators from the workflow script (✅ ❌ 📝 🔑 🔍 📥) exactly as they appear in the GitHub Actions log viewer.

**Examples:**

> `"Github action is geting an error on Verify signed app step\n0s\nRun echo \"::group::Verifying signed application\"\nVerifying signed application\n  📱 Found app: ./mac-arm64/Dispatch.app\n  🔍 Verifying code signature...\n  ./mac-arm64/Dispatch.app: code has no resources but signature indicates they must be present\n  ❌ ERROR: Code signature verification failed\n  Error: Process completed with exit code 1."`

> `"same error still\n  security: SecItemCopyMatching: The specified item could not be found in the keychain."`

> `"I sent a simple message \"Hi\" and\nmarlin@Marlins-MacBook-Pro agent-command-center % sqlite3 ~/.acc/threads.db \"SELECT COUNT(*) FROM console_lines;\"\n0\nseeing no console lines, do I need to have it message way more?"`
