---
name: pr-feedback-relay
description: evisdren pastes PR review comments from Copilot or Cursor nearly verbatim and asks the agent to address them. Trigger when evisdren has received external code review feedback and wants it implemented.
---

# Skill: pr-feedback-relay

evisdren uses Copilot and Cursor for automated PR reviews and treats their feedback as an implementation task list for Claude Code. They paste the reviewer's comment text with minimal framing ("i got this feedeback for a flaky test:", "look at the omments on the PR by cursor and copilot and address them."), sometimes adding a constraint or caveat of their own at the end.

## Characteristics

- Short intro sentence naming the source: "i got this feedback from copilot:", "look at the comments on the PR by cursor and copilot and address them."
- Reviewer text pasted nearly verbatim — often multi-paragraph, includes quoted field names, code snippets, suggested code blocks
- May add a personal constraint after: "If you have any questions ask me. Remember that we should maintain existing settings as \"prompt\" while setting \"always\" for only brand new repos."
- Typos appear in evisdren's framing text but not in the pasted reviewer text

## Verbatim Examples

**Example 1 (PR comments from cursor and copilot):**
> "look at the omments on the PR by cursor and copilot and address them. If you have any questions ask me. Remember that we should maintain existing settings as \"prompt\" while setting \"always\" for only brand new repos where entire is not enabled or being enabled for the first time."

**Example 2 (flaky test feedback):**
> "i got this feedeback for a flaky test: TestDetectOrSelectAgent_NoDetection_WithTTY_ShowsPromptMessages calls detectOrSelectAgent() with ENTIRE_TEST_TTY=1, which will run form.Run() and can block waiting for interactive input when tests are executed from a real terminal (or behave differently under ACCESSIBLE mode). This makes the unit test potentially hanging/flaky. To keep tests non-interactive, consider refactoring detectOrSelectAgent to inject/mock the selection prompt, or avoid executing form.Run() in unit tests (e.g., gate prompting behind a test-only flag and test the prompt path via integration tests with a pty).\n\n\nfix this adn then give me a way to test this manually locally"

**Example 3 (specific comment to update):**
> "update this comment:\n\nThe value \"always\" is hardcoded instead of using the settings.CommitLinkingAlways constant because the settings package import is shadowed by the local variable settings, err := LoadEntireSettings(ctx)."
