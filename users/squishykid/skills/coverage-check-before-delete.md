---
name: coverage-check-before-delete
description: How squishykid verifies test coverage before deleting code or tests — pauses the deletion flow to explicitly ask for a coverage audit. Trigger when tests are about to be deleted alongside dead production code.
---

When dead code has associated tests that are being deleted, squishykid does not just let the agent remove them. They pause and explicitly ask the agent to verify that all previously-covered scenarios are still covered under the new code path.

The ask is specific: name both the deleted test files, name the old function being tested, name the replacement function, and ask to ensure each scenario transfers.

**Example:**
> `lets double check that we haven't lost any valuable test scenarios in the claude_test and gemini_test deletions. check both gemini_test.go and claude_test.go and for each deleted test which tests ParseHookInput, make sure we cover that scenario for ParseHookEvent`

After the agent reports coverage is maintained, squishykid proceeds:
> `ok, go ahead and commit, then create a PR on top of 427`

This behavior reflects the Expert Nitpicker persona (50%): squishykid trusts the agent's execution but audits structural correctness independently.
