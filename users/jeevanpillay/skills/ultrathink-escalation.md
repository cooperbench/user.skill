---
name: ultrathink-escalation
description: How jeevanpillay escalates when a solution fails or the agent misses the mark — appends "ultrathink" to a failure report or repeats the failing scenario. Trigger when the agent's output doesn't work and the user is frustrated.
---

When the agent's solution doesn't work and jeevanpillay isn't satisfied with a simple retry, he appends `ultrathink` to signal that the agent should think harder, not just repeat itself. This replaces a detailed critique — the user provides the failure fact and expects the agent to diagnose autonomously.

**Pattern**: `[short failure description].  ultrathink`

Note the double-space before "ultrathink" in some examples — preserve it.

**Examples**:

```
nope didnt work.  ultrathink
```

```
nope running option + k closes it still. ultrathink
```

```
nope didnt work.  ultrathink
```

When the issue is more complex, he may provide the scenario to reproduce before escalating:

```
okay finally, there seems to be a problme where option k in mac is meant to go up but it closes the command dialog. it should be that cmd + k is the only one that can open or close. before changing go throguh the different layer of command dialog @apps/app/src/components/command-palette.tsx and @packages/ui/src/components/ui/command.tsx and figure out the rght solution
```

Contrast with a plain rejection (no `ultrathink`):
```
hmm not convinved its working
```
```
this seems complicated
```

`ultrathink` is reserved for "I already told you it's not working, think harder" — not first-pass skepticism.
