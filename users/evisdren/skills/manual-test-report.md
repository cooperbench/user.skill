---
name: manual-test-report
description: evisdren ran something manually, it didn't work, and they paste the exact terminal output or JSON config to show what happened. Trigger when evisdren has tested a just-committed change and found a bug.
---

# Skill: manual-test-report

evisdren tests almost every significant change manually before accepting it. When something doesn't work, they paste the exact terminal output (with timestamp prefix) or JSON file contents. They give minimal commentary before the paste — just enough to set context. The paste is verbatim, including timestamps, error text, and git output. Typos appear in the setup text but not in the pasted content.

## Characteristics

- Brief setup sentence with typos: "i just trid it manually with this json:"
- JSON pasted in a code block, verbatim
- Terminal output pasted with `[2026-02-26 15:49] ~/code/repo (branch)%` format
- Ends with either a question ("and when i ran entire enable, it didn't update that field") or just lets the paste speak for itself
- May attach a screenshot for visual evidence

## Verbatim Examples

**Example 1 (settings not updated):**
> "i just trid it manually with this json:\n\n{\n  \"enabled\": true,\n  \"telemetry\": true,\n  \"strategy\": \"manual-commit\"\n}\n\nand when i ran entire enable, it didn't update that field"

**Example 2 (still prompting after fix):**
> "i tried manual testing this with ane xisting repo. I ran entire enable and it updated my settings to: { \"enabled\": true, \"telemetry\": true, \"commit_linking\": \"prompt\" } then i updated prompt to \"always\" and creaed a commit and it still asked me to link? here are the temrinal logs: [2026-02-26 15:49] ~/code/gemini-test (main)% git add . [2026-02-26 15:49] ~/code/gemini-test (main)% git commit -m 'updates' You have an active Claude Code session. Last Prompt: make a small change Link this commit to Claude Code session context? [Y/n]"

**Example 3 (screenshot + terse comment):**
> "its still qasking me to link? if you look at the screenshot and the terminal\n[Image: image/png]"
