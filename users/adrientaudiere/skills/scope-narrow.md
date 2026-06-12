---
name: scope-narrow
description: Issues a precise "only add X to Y" instruction when the agent has done or is about to do more than asked. Trigger when the agent proposes broad changes but the user only wanted a surgical edit.
---

# Scope narrow

adrientaudiere watches closely for scope creep. When the agent touches more than the exact target, the correction specifies precisely what should and should not be changed. The word "only" is frequently used.

This is one of the most characteristic nitpick patterns: the user does not say "that's too much" generically — they restate the minimal change they actually want.

## Examples

Agent proposed applying multiple fixes after a check; user narrows to a single file/block:
```
only add @importFrom grDevices convertColor and @importFrom stats dist to
  the reorder_colors roxygen block.
```

Agent asked whether to commit specific files or all changes; user says all (opposite direction of narrowing — when the agent under-scoped):
```
all the changes
```

Agent added a complex log10 fix when the user only wanted sort order changed:
```
ok just modify the direction of the ordernig of samples.
```

The "only add X to Y" form is the canonical scope narrow. It names the exact symbol and the exact location. No other changes are implied.
