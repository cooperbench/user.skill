---
name: terse-approve
description: >
  Triggered when the agent's output is correct and the user wants to acknowledge and move on.
  moven0831 uses one of a small set of single-word or short-phrase approvals with no elaboration.
---

When things are correct, moven0831 approves with the shortest possible signal:

**Core vocabulary** (pick one, lowercase, no punctuation):
- `sure`
- `yes`
- `looks good`
- `it works`
- `yep this work`

**When to use each**:
- `sure` — agent asked a yes/no question or presented a plan for approval
- `yes` — explicit yes/no question answered
- `looks good` — agent showed output (plan, spec section, code) and user has reviewed
- `it works` / `yep this work` — agent fixed something and user tested it

**Verbatim examples**:

```
sure
```

```
yes
```

```
looks good
```

```
it works
```

```
yep this work
```

**Key trait**: After any of these, no further message is sent unless the agent asks something or
produces the next artifact. The approval is a green light to continue, not a conversation opener.
