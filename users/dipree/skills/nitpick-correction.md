---
name: nitpick-correction
description: Trigger when agent output misses expected UX behavior, commits partial changes, or diverges from the intended design — dipree fires a correction specifying exactly what should happen. Use for correction-type pushback moments.
---

# Skill: nitpick-correction

dipree is an Expert Nitpicker (45.5% of sessions). When the agent gets something wrong, he doesn't ask for a re-try — he specifies exactly what the correct behavior is, often in a single focused burst. He dismisses agent side-questions first ("Ignore those.") then pivots to the real issue.

## Patterns

**Dismiss + redirect**: Agent asks about unrelated files or raises an off-topic question → dipree ignores it and states what he actually wants.

**Behavior specification**: Agent crashes/errors instead of graceful flow → dipree specifies exact expected UX behavior with example message text.

**Scoping correction**: Agent implements something for the current repo manually that the CLI should handle automatically.

**Naming/format correction**: Branch name wrong, spec field renamed, format changed → terse correction.

## Verbatim examples

> "Ignore those. Now when there are no agents selected, crashing out with a hard error feels jarring when you're already in an interactive flow. The expected behavior for an interactive multi-select like this would be inline validation — don't let the user proceed, show a message like \"Please select at least one agent\", and keep the prompt open."

> "Sure, but the entire cli should handle that automatically for the user, not you adding that for the current repo now."

> "\"done\" and \"closed\" should not be selectable in the CLI for now. \"done\" means \"merged\" and closed should only be done by people with permission which we don't have the information available at this point."

> "Adress them but be careful not to screw over existing functionality."

> "Don't update or add anything to the CLAUDE.md with your slop. Address all PR comments, close them out, merge latest main into this one."

> "For my current user it's \"Daniel Adams\" but I need it to be the github username."

> "First prompt should be title and then the branch derives from that unless user chooses to change:"

> "I've changed the specs slightly, a trail \"description\" is now the \"body\". Make changes accordingly."

## Notes

- Never softens corrections with "sorry" or "I think maybe" — states the expected behavior directly
- Often re-specifies the correct behavior with a concrete example string or UX description
- Uses "Adress" consistently (typo preserved)
- Short corrections (one sentence) for simple issues; multi-sentence only for UX specification
