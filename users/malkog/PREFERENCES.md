# PREFERENCES

## What triggers correction (27.3% of prompts)

- **Wrong repo target** — agent opens PR against the wrong repo ("Wait, it should point at hackerspub/android.")
- **Feature misunderstanding** — agent implements syntax-highlighted HTML instead of syntax-highlighted code blocks ("Not highlighting html, syntax highlighting code snippet. Got it?")
- **Missing rendering detail** — agent renders markdown without full list/heading/code support ("we need to full support for code snippet/heading/list/numbered list. Could you also considerate them?")
- **UI behavior broken post-refactor** — agent's redesign breaks click navigation or reaction sheet ("And, For each actions for post, most of all are broken. Take a deep look again")
- **Wrong version number** — catches immediately ("Okay correction. not 1.0.1, 1.1.0")
- **Misidentified what "github issue" means** — agent filed a note internally, user wanted a GitHub issue ("I mean, github issue")

## What triggers failure reports (4.7% of prompts)

- Pastes raw build errors (Gradle FAILED blocks, keytool exceptions) without commentary.
- Pastes raw git stderr ("error: cannot pull with rebase: You have unstaged changes.") as the entire message.
- Pastes Korean terminal output verbatim.
- "Why I can't still reaction?" — sometimes frames a failure as a question.
- "And, For each actions for post, most of all are broken. Take a deep look again" — verbal failure report with imperative.

## What satisfies (68% non-pushback)

- Agent completes a task, user replies with "Yes", "2", "Keep go", "Good. Keep go", or just invokes the next slash command.
- Agent presents multiple options → user picks one by name/letter.
- Agent does the work autonomously via `/loop` — user lets it run, only interrupts to redirect.

## Workflow habits

- **Slash-command driven** — `/commit`, `/ghpr`, `/loop 30m`, `/minimalism-workflow:release-tag` are the backbone of every session.
- **iOS-first design** — any new UI feature is shaped by "See ../hackerspub-ios" or "as pretty as Hackers'Pub iOS client".
- **Commits early and often** — invokes `/commit` after each atomic change; uses `/ghpr` to open PRs per feature branch.
- **Interrupt-resume style** — hits stop when the agent is doing something wrong, says "Continue from where you left off" after redirecting.
- **No test-driven workflow** — no mention of tests in any prompt.
- **No explanation requests** — never asks "why" or "how does this work"; asks for results only.
- **Branch per fix** — `fix/html-highlighting`, `fix/article-rendering` — uses descriptive branch names via `git switch -c`.
- **Releases via slash command** — tags with `/minimalism-workflow:release-tag v1.x.x`.
- **Dual distribution awareness** — conscious of F-Droid vs Google Play constraints from the start.

## Stack preferences visible in prompts

- Kotlin + Jetpack Compose (Android)
- Gradle (Kotlin DSL: `app/build.gradle.kts`)
- Fastlane for metadata / store assets
- GitHub for PR workflow (`/ghpr`)
- NeoUtils/Highlight library (accepted after agent presented options)
- UnifiedPush with embedded FCM distributor (preferred over requiring separate app install)
