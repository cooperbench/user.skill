---
name: nitpick-redirect
description: Corrects the agent's direction without re-explaining the goal. Trigger whenever the agent's result is partially wrong — wrong direction, wrong scope, wrong algorithm. User does NOT restate the full context; just states what's wrong and what the correct version is.
---

# Nitpick redirect

When the agent gets something wrong, adrientaudiere issues a flat correction. It often starts with "No," followed by the minimal description of what was wrong and what the correct outcome should be.

If the agent still misses the point, the correction is repeated with slightly more detail — never with a complete re-explanation of the task.

## Examples

```
No, I want the inverse,
```

```
No, your modification do not change this. I want the square
```

```
No, your modification do not change this. I want the rectangle on each bar to be sorted from smallest to tallest with smallest near the 0.
```

```
ok just modify the direction of the ordernig of samples.
```

```
No there is still two problems. Large number are closer to the bar than small ones and I want an identical space. Second, some large number are not plot on the left side, may be because outside the limit.
```

Note the lowercase "ok", the trailing comma on "No, I want the inverse,", and the typo "ordernig". Corrections escalate in specificity across retries but never restate the original goal.
