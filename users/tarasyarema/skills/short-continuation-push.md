---
name: short-continuation-push
description: How tarasyarema restarts momentum mid-session — one-liner approvals and push-forwards, sometimes with an extra constraint tacked on
---

# Skill: Short Continuation Push

After an agent checks in, pauses, or completes a phase, Taras responds with a short approving push. These are among his most common mid-session messages. They are terse, sometimes a single word, and may tack on a constraint or scope expansion at the end.

## Examples

**Bare approval:**
```
continue
```

**Approval + scope:**
```
nice, continue if there are things left from the feedback
```

**Yes + constraint:**
```
y keep going till the end, make sure to perform all needed e2e tests yourself running services and so on, there are envs available for you to use
```

**Yes + Docker flag:**
```
y pls run w docker!
```

**Casual + redirect:**
```
nice! now from a UI perspective, what is testable? will it be completely broken? maybe spin up a server a 3015 (change the envs to point to that as it does to 3014 now) and create a few workflows so I can check?
```

**Minimal check-in response:**
```
ok authed, created issue. can you restart api and spin up lead to do e2e2
```

**After rate limit cleared:**
```
nice, continue if there are things left from the feedback
```

## Key signals

- "y" / "y pls" for yes
- "nice!" or "nice, …" as opener when satisfied
- Constraints appended with comma: "y pls run w docker!"
- May include a numeric port or specific env detail: "server a 3015", "envs available for you to use"
- Never multi-sentence unless adding a redirect
