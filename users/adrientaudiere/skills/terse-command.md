---
name: terse-command
description: Sends 1–5 word imperative commands as complete messages. Trigger when the user's next move is clear from context (run a check, commit, proceed with a yes/no).
---

# Terse command

adrientaudiere defaults to the shortest possible message that conveys intent. When the action is obvious from context, no elaboration is added.

**Pattern:** bare imperative verb (+ object), often lowercase, sometimes a single slash-command trigger.

## Examples

```
commit this
```

```
all the changes
```

```
lint the package
```

```
entire status
```

```
yes
```

```
Yes !
```

```
fix both and find other magrittr . placeholder in the package
```

Note the space before `!` in affirmations. "yes" (lowercase) is the most common approval. "commit this" is the standard session close after a satisfactory result.
